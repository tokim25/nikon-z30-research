"""Synthetic edits only. No firmware content or real patch manifests."""

from dataclasses import replace
import hashlib
import unittest

from nikon_z30_research.patch_audit import ExactEdit, PatchAuditError, audit_exact_edits


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ExactEditTests(unittest.TestCase):
    def setUp(self):
        self.original = b'abcdefghij'
        self.candidate = b'abXYefgZij'
        self.edits = (ExactEdit('first synthetic edit', 2, 2, digest(b'cd'), digest(b'XY')),
                      ExactEdit('second synthetic edit', 7, 1, digest(b'h'), digest(b'Z')))

    def audit(self, original=None, candidate=None, edits=None, **policy):
        return audit_exact_edits(
            self.original if original is None else original,
            self.candidate if candidate is None else candidate,
            original_size=policy.get('size', len(self.original)),
            original_sha256=policy.get('sha', digest(self.original)),
            edits=self.edits if edits is None else edits)

    def test_exact_plan_accepted_and_report_is_deterministic(self):
        report = self.audit()
        self.assertEqual(report, self.audit())
        self.assertEqual(report.changed_bytes, 3)
        self.assertEqual(report.edit_count, 2)
        self.assertEqual(report.candidate_sha256, digest(self.candidate))
        self.assertEqual(self.original, b'abcdefghij')

    def test_unexpected_change_at_every_unapproved_offset(self):
        for offset in (0, 1, 4, 5, 6, 8, 9):
            with self.subTest(offset=offset):
                candidate = bytearray(self.candidate)
                candidate[offset] ^= 1
                with self.assertRaisesRegex(PatchAuditError, 'outside'):
                    self.audit(candidate=bytes(candidate))

    def test_extra_change_inside_approved_span_rejected(self):
        # Broad span includes unchanged neighbors; its full replacement is pinned.
        broad = ExactEdit('broad synthetic edit', 1, 5, digest(b'bcdef'), digest(b'bXYef'))
        self.assertEqual(self.audit(edits=(broad, self.edits[1])).changed_bytes, 3)
        with self.assertRaisesRegex(PatchAuditError, 'candidate digest'):
            self.audit(candidate=b'abXYQfgZij', edits=(broad, self.edits[1]))

    def test_missing_partial_and_wrong_edits_rejected(self):
        for candidate in (self.original, b'abXdefgZij', b'abYXefgZij'):
            with self.subTest(candidate=candidate):
                with self.assertRaisesRegex(PatchAuditError, 'candidate digest'):
                    self.audit(candidate=candidate)

    def test_wrong_original_and_reapplication_rejected(self):
        for original in (b'ABCDEFGHIJ', self.candidate):
            with self.assertRaisesRegex(PatchAuditError, 'original identity'):
                self.audit(original=original)

    def test_wrong_original_span_digest_rejected(self):
        with self.assertRaisesRegex(PatchAuditError, 'original digest'):
            self.audit(edits=(replace(self.edits[0], original_sha256=digest(b'xx')), self.edits[1]))

    def test_insertions_deletions_rejected(self):
        for candidate in (self.candidate[:-1], self.candidate + b'x'):
            with self.assertRaisesRegex(PatchAuditError, 'candidate size'):
                self.audit(candidate=candidate)

    def test_empty_manifest_only_accepts_unchanged_input(self):
        self.assertEqual(self.audit(candidate=self.original, edits=()).changed_bytes, 0)
        with self.assertRaisesRegex(PatchAuditError, 'outside'):
            self.audit(edits=())

    def test_policy_rejects_invalid_types_digests_and_bounds(self):
        first = self.edits[0]
        invalid = [(None,), list(self.edits), (replace(first, offset=-1),),
                   (replace(first, offset=True),), (replace(first, size=True),),
                   (replace(first, size=0),), (replace(first, offset=9),),
                   (replace(first, original_sha256='bad'),),
                   (replace(first, candidate_sha256='A' * 64),),
                   (replace(first, candidate_sha256=first.original_sha256),),
                   (replace(first, label=' '),),
                   (first, replace(self.edits[1], label=first.label)),
                   tuple(reversed(self.edits)), (first, replace(self.edits[1], offset=3))]
        for edits in invalid:
            with self.subTest(edits=edits):
                with self.assertRaises(PatchAuditError):
                    self.audit(edits=edits)
        for policy in ({'size': True}, {'size': -1}, {'sha': 'invalid'}):
            with self.assertRaisesRegex(PatchAuditError, 'identity policy'):
                self.audit(**policy)

    def test_mutable_input_rejected(self):
        for kwargs in ({'original': bytearray(self.original)}, {'candidate': bytearray(self.candidate)}):
            with self.assertRaisesRegex(PatchAuditError, 'immutable'):
                self.audit(**kwargs)

    def test_adjacent_and_boundary_edits_accepted(self):
        candidate = b'XYcdefghiZ'
        edits = tuple(ExactEdit(str(i), i, 1, digest(self.original[i:i+1]), digest(candidate[i:i+1]))
                      for i in (0, 1, 9))
        self.assertEqual(self.audit(candidate=candidate, edits=edits).changed_bytes, 3)

    def test_manifest_identity_changes_with_plan(self):
        renamed = (replace(self.edits[0], label='different review label'), self.edits[1])
        self.assertNotEqual(self.audit().manifest_sha256, self.audit(edits=renamed).manifest_sha256)

    def test_errors_do_not_include_bytes_or_labels(self):
        edits = (replace(self.edits[0], label='private label', candidate_sha256=digest(b'QQ')),)
        with self.assertRaises(PatchAuditError) as caught:
            self.audit(edits=edits)
        self.assertNotIn('private label', str(caught.exception))
        self.assertNotIn('XY', str(caught.exception))

    def test_crc_validation_and_edit_audit_are_both_required(self):
        from test_package_container import fixture
        from nikon_z30_research.package_container import (
            ComponentSpec, ContainerValidationError, validate_container,
        )
        original, specs = fixture()
        planned, _ = fixture((b'Invented main payload', b'invented auxiliary payload'))
        start, size = 112, specs[0].size
        # This synthetic plan includes the first component's exact repaired CRC.
        edits = (ExactEdit('synthetic component and CRC', start, size,
                           digest(original[start:start+size]), digest(planned[start:start+size])),)
        report = audit_exact_edits(original, planned, original_size=len(original),
                                   original_sha256=digest(original), edits=edits)
        self.assertGreater(report.changed_bytes, 1)
        policy = (ComponentSpec(specs[0].name, size), specs[1])
        validate_container(planned, policy)
        # Allowing just the payload byte must not exempt the checksum changes.
        byte_only = (ExactEdit('payload only', start, 1,
                              digest(original[start:start+1]), digest(planned[start:start+1])),)
        with self.assertRaisesRegex(PatchAuditError, 'outside'):
            audit_exact_edits(original, planned, original_size=len(original),
                              original_sha256=digest(original), edits=byte_only)
        broken = bytearray(original)
        broken[start] = planned[start]
        broken = bytes(broken)
        # Matching a bad plan alone does not make the component's CRC correct.
        audit_exact_edits(original, broken, original_size=len(original),
                          original_sha256=digest(original), edits=byte_only)
        with self.assertRaisesRegex(ContainerValidationError, 'component 0 CRC'):
            validate_container(broken, policy)


if __name__ == '__main__':
    unittest.main()
