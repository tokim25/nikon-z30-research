"""Preflight integration tests using invented containers and edit plans only."""

from dataclasses import asdict, replace
import hashlib
import unittest

from test_package_container import fixture, fix_container_crc
from nikon_z30_research.package_container import ContainerValidationError
from nikon_z30_research.patch_audit import ExactEdit, PatchAuditError
from nikon_z30_research.preflight import PreflightError, preflight_decoded
from nikon_z30_research.installation import AddressRange, InstallationModelError, InstallationPolicy


def digest(data):
    return hashlib.sha256(data).hexdigest()


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.original, self.specs = fixture()
        self.candidate, _ = fixture((b'Invented main payload', b'invented auxiliary payload'))
        self.edits = (self.edit(112, self.specs[0].size),)

    def edit(self, offset, size, candidate=None):
        candidate = self.candidate if candidate is None else candidate
        return ExactEdit('synthetic review span', offset, size,
                         digest(self.original[offset:offset+size]), digest(candidate[offset:offset+size]))

    def run_preflight(self, **changes):
        params = dict(original=self.original, candidate=self.candidate,
                      original_size=len(self.original), original_sha256=digest(self.original),
                      components=self.specs, changed_components=(self.specs[0].name,), edits=self.edits)
        params.update(changes)
        return preflight_decoded(**params)

    def test_modified_container_report_binds_same_inputs_and_policy(self):
        report = self.run_preflight()
        self.assertEqual(report.original.sha256, digest(self.original))
        self.assertEqual(report.candidate.sha256, digest(self.candidate))
        self.assertEqual(report.edits.original_sha256, report.original.sha256)
        self.assertEqual(report.edits.candidate_sha256, report.candidate.sha256)
        self.assertTrue(report.candidate.components[1].unchanged_checked)
        self.assertFalse(report.candidate.components[0].unchanged_checked)
        self.assertEqual(report.scope, 'decoded_container_only')
        self.assertEqual(report.hardware_readiness, 'not_established')
        self.assertEqual(report, self.run_preflight())
        self.assertNotIn('synthetic review span', str(asdict(report)))

    def test_unchanged_baseline(self):
        report = self.run_preflight(candidate=self.original, changed_components=(), edits=())
        self.assertEqual(report.edits.changed_bytes, 0)
        self.assertTrue(all(c.unchanged_checked for c in report.candidate.components))

    def test_original_identity_checked(self):
        with self.assertRaisesRegex(PatchAuditError, 'original identity'):
            self.run_preflight(original_sha256='0' * 64)

    def test_missing_original_component_hash_rejected(self):
        with self.assertRaisesRegex(PreflightError, 'all original'):
            self.run_preflight(components=(replace(self.specs[0], unchanged_sha256=None), self.specs[1]))

    def test_changed_component_policy_rejected(self):
        for policy in (('unknown',), (self.specs[0].name,) * 2, [self.specs[0].name], (None,)):
            with self.subTest(policy=policy):
                with self.assertRaises(PreflightError):
                    self.run_preflight(changed_components=policy)

    def test_undeclared_component_edit_rejected(self):
        with self.assertRaisesRegex(PreflightError, 'scope'):
            self.run_preflight(changed_components=())

    def test_unused_change_permission_rejected(self):
        with self.assertRaisesRegex(PreflightError, 'unchanged'):
            self.run_preflight(changed_components=tuple(s.name for s in self.specs))

    def test_edit_cannot_cross_component_boundary(self):
        edit = self.edit(112, self.specs[0].size + 1)
        with self.assertRaisesRegex(PreflightError, 'crosses'):
            self.run_preflight(edits=(edit,), changed_components=tuple(s.name for s in self.specs))

    def test_header_edit_rejected_even_if_in_exact_plan(self):
        candidate = bytearray(self.original)
        candidate[43] = 1
        candidate = fix_container_crc(candidate)
        edits = (self.edit(43, 1, candidate),
                 replace(self.edit(len(candidate)-16, 2, candidate), label='synthetic CRC'))
        with self.assertRaisesRegex(PreflightError, 'scope'):
            self.run_preflight(candidate=candidate, edits=edits, changed_components=())

    def test_bad_crc_rejected_even_when_exact_plan_matches(self):
        candidate = bytearray(self.original)
        candidate[112] ^= 1
        candidate = bytes(candidate)
        with self.assertRaisesRegex(ContainerValidationError, 'CRC'):
            self.run_preflight(candidate=candidate, edits=(self.edit(112, 1, candidate),))

    def test_different_candidate_cannot_reuse_plan(self):
        other, _ = fixture((b'iNvented main payload', b'invented auxiliary payload'))
        with self.assertRaisesRegex(PatchAuditError, 'candidate digest'):
            self.run_preflight(candidate=other)

    def test_component_policy_is_in_report_identity(self):
        # An invalid component digest cannot be substituted into a passing plan.
        with self.assertRaisesRegex(ContainerValidationError, 'unchanged digest'):
            self.run_preflight(components=(replace(self.specs[0], unchanged_sha256='0' * 64), self.specs[1]))
        renamed = (replace(self.edits[0], label='another reviewed plan'),)
        self.assertNotEqual(self.run_preflight().policy_sha256,
                            self.run_preflight(edits=renamed).policy_sha256)

    def test_install_model_binds_validated_component_and_full_policy(self):
        policy = InstallationPolicy(self.specs[0].name, 0x1000, 32, 8)
        report = self.run_preflight(installation=policy)
        self.assertEqual(report.installation.component_sha256, report.candidate.components[0].sha256)
        self.assertEqual(report.installation.payload_size, self.specs[0].size - 2)
        self.assertEqual(report.installation.padding_size, 32 - self.specs[0].size + 2)
        self.assertEqual(report.hardware_readiness, 'not_established')
        moved = self.run_preflight(installation=replace(policy, target_start=0x2000))
        self.assertNotEqual(report.policy_sha256, moved.policy_sha256)
        self.assertEqual(report.installation.expected_span_sha256, moved.installation.expected_span_sha256)

    def test_install_model_omission_is_explicit(self):
        self.assertIsNone(self.run_preflight().installation)

    def test_install_policy_cannot_select_unknown_component(self):
        with self.assertRaisesRegex(PreflightError, 'not in validated'):
            self.run_preflight(installation=InstallationPolicy('unknown', 0x1000, 32, 8))
        with self.assertRaisesRegex(PreflightError, 'invalid installation'):
            self.run_preflight(installation={})

    def test_install_bounds_checked_after_container_validation(self):
        for policy in (InstallationPolicy(self.specs[0].name, 0x1000, 8, 8),
                       InstallationPolicy(self.specs[0].name, 0x1000, 32, 8,
                                          (AddressRange(0x1018, 0x1020),))):
            with self.assertRaises(InstallationModelError):
                self.run_preflight(installation=policy)

    def test_install_hash_changes_with_validated_payload(self):
        policy = InstallationPolicy(self.specs[0].name, 0x1000, 32, 8)
        baseline = self.run_preflight(candidate=self.original, changed_components=(), edits=(),
                                      installation=policy)
        changed = self.run_preflight(installation=policy)
        self.assertNotEqual(baseline.installation.expected_span_sha256,
                            changed.installation.expected_span_sha256)


if __name__ == '__main__':
    unittest.main()
