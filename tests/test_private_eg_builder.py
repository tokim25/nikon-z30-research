"""Filesystem boundary checks using synthetic EG data only."""

import binascii
import hashlib
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

from nikon_z30_research.private_eg_builder import build_private_eg_candidate
from nikon_z30_research.standalone_eg import EgBuildError, EgBuildPolicy


def synthetic_eg():
    value = bytearray((i * 29 + 7) & 0xFF for i in range(96))
    value[-2:] = binascii.crc_hqx(value[:-2], 0).to_bytes(2, "big")
    return bytes(value)


class PrivateEgBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.repo = base / "repo"
        self.repo.mkdir()
        self.private = base / "private"
        self.private.mkdir()
        self.original = synthetic_eg()
        self.original_path = self.private / "original.eg"
        self.original_path.write_bytes(self.original)
        self.manifest_bytes = b'{"synthetic":"reviewed-plan"}'
        self.manifest_path = self.private / "plan.json"
        self.manifest_path.write_bytes(self.manifest_bytes)
        self.policy = EgBuildPolicy(
            len(self.original), hashlib.sha256(self.original).hexdigest(), (),
        )
        self.identity_gate = patch(
            "nikon_z30_research.private_eg_builder.require_verified_eg_module",
            return_value=object(),
        )
        self.manifest_parser = patch(
            "nikon_z30_research.private_eg_builder.policy_from_complete_manifest",
            return_value=self.policy,
        )
        self.identity_gate.start()
        self.manifest_parser.start()
        self.addCleanup(self.identity_gate.stop)
        self.addCleanup(self.manifest_parser.stop)

    def build(self, output, *, manifest_sha=None):
        return build_private_eg_candidate(
            original_path=self.original_path,
            manifest_path=self.manifest_path,
            output_path=output,
            reviewed_manifest_sha256=(manifest_sha or
                hashlib.sha256(self.manifest_bytes).hexdigest()),
            repository_root=self.repo,
        )

    def test_build_writes_audited_output_without_overwrite(self):
        output = self.private / "candidate.eg"
        report = self.build(output)
        self.assertEqual(output.read_bytes(), self.original)
        self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
        self.assertTrue(report.crc_valid)
        with self.assertRaisesRegex(EgBuildError, "already exists"):
            self.build(output)

    def test_reviewed_manifest_hash_is_required_before_output(self):
        output = self.private / "candidate.eg"
        with self.assertRaisesRegex(EgBuildError, "manifest SHA-256 mismatch"):
            self.build(output, manifest_sha="0" * 64)
        self.assertFalse(output.exists())

    def test_failed_readback_audit_removes_partial_candidate(self):
        output = self.private / "candidate.eg"
        with patch(
            "nikon_z30_research.private_eg_builder.audit_standalone_eg",
            side_effect=EgBuildError("synthetic audit failure"),
        ), self.assertRaisesRegex(EgBuildError, "synthetic audit failure"):
            self.build(output)
        self.assertFalse(output.exists())

    def test_repository_inputs_and_output_are_rejected(self):
        repo_original = self.repo / "original.eg"
        repo_original.write_bytes(self.original)
        with self.assertRaisesRegex(EgBuildError, "outside the repository"):
            build_private_eg_candidate(
                original_path=repo_original,
                manifest_path=self.manifest_path,
                output_path=self.private / "candidate.eg",
                reviewed_manifest_sha256=hashlib.sha256(self.manifest_bytes).hexdigest(),
                repository_root=self.repo,
            )
        with self.assertRaisesRegex(EgBuildError, "outside the repository"):
            self.build(self.repo / "candidate.eg")


if __name__ == "__main__":
    unittest.main()
