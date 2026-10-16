"""Synthetic tests for the verified-original hard gate. No real firmware."""

import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from nikon_z30_research.verified_firmware import (
    VERIFIED_EG_SHA256,
    VERIFIED_EG_SIZE,
    UnverifiedFirmwareError,
    require_verified_eg_module,
)

MODULE = "nikon_z30_research.verified_firmware"


class RequireVerifiedEgModuleTests(unittest.TestCase):
    def test_wrong_size_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.bin"
            path.write_bytes(b"not the real module")
            with self.assertRaises(UnverifiedFirmwareError):
                require_verified_eg_module(path)

    def test_right_size_wrong_bytes_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.bin"
            path.write_bytes(b"x" * VERIFIED_EG_SIZE)
            with self.assertRaises(UnverifiedFirmwareError):
                require_verified_eg_module(path)

    def test_matching_file_is_accepted(self):
        # A real SHA-256 preimage cannot be brute-forced, so this test
        # patches the two known-good constants to a small synthetic value
        # and proves the same accept path works. It never touches real
        # firmware bytes or the real constants' value.
        payload = b"synthetic fixture"
        fixture_hash = hashlib.sha256(payload).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.bin"
            path.write_bytes(payload)
            with mock.patch(f"{MODULE}.VERIFIED_EG_SIZE", len(payload)), \
                 mock.patch(f"{MODULE}.VERIFIED_EG_SHA256", fixture_hash):
                report = require_verified_eg_module(path)
        self.assertEqual(report.size_bytes, len(payload))
        self.assertEqual(report.sha256, fixture_hash)

    def test_error_message_names_the_path_and_not_the_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.bin"
            path.write_bytes(b"short")
            try:
                require_verified_eg_module(path)
                self.fail("expected UnverifiedFirmwareError")
            except UnverifiedFirmwareError as error:
                message = str(error)
                self.assertIn(str(path), message)
                self.assertIn(str(VERIFIED_EG_SIZE), message)
                self.assertNotIn("short", message)

    def test_missing_file_raises_oserror_not_unverified(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "does-not-exist.bin"
            with self.assertRaises(OSError):
                require_verified_eg_module(missing)

    def test_constants_match_the_recovery_report(self):
        # Pins the two values this module relies on against accidental
        # edits; docs/milestone-1-recovery.md is the source of truth.
        self.assertEqual(VERIFIED_EG_SIZE, 33_939_514)
        self.assertEqual(
            VERIFIED_EG_SHA256,
            "8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa",
        )


if __name__ == "__main__":
    unittest.main()
