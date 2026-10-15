import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from nikon_z30_research.cli import main
from nikon_z30_research.firmware import inspect_firmware, verify_firmware
from nikon_z30_research.geometry import centered_crop


class FirmwareTests(unittest.TestCase):
    def test_known_digest_and_no_modification(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.bin"
            path.write_bytes(b"abc")
            before = path.stat()
            report = inspect_firmware(path)
            self.assertEqual(report.size_bytes, 3)
            self.assertEqual(report.sha256, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
            self.assertTrue(verify_firmware(report, report.sha256.upper(), 3))
            self.assertFalse(verify_firmware(report, "0" * 64))
            self.assertFalse(verify_firmware(report, report.sha256, 4))
            self.assertEqual(path.read_bytes(), b"abc")
            self.assertEqual(path.stat().st_mtime_ns, before.st_mtime_ns)
            for invalid in (report.sha256[:12], "g" * 64, report.sha256 + "\n", ""):
                with self.assertRaises(ValueError):
                    verify_firmware(report, invalid)
            for invalid in (-1, True, 3.0):
                with self.assertRaises(ValueError):
                    verify_firmware(report, report.sha256, invalid)

    def test_empty_and_multiple_chunks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.bin"
            for payload in (b"", b"a" * (2 * 1024 * 1024 + 17)):
                path.write_bytes(payload)
                report = inspect_firmware(path)
                self.assertEqual(report.size_bytes, len(payload))
                self.assertEqual(report.sha256, hashlib.sha256(payload).hexdigest())
            with self.assertRaises(ValueError):
                inspect_firmware(directory)
            with self.assertRaises(FileNotFoundError):
                inspect_firmware(Path(directory) / "missing")


class GeometryTests(unittest.TestCase):
    def test_common_frame(self):
        crop = centered_crop(3840, 2160)
        self.assertEqual((crop.width, crop.height), (3835, 1416))
        self.assertEqual((crop.left, crop.top, crop.right, crop.bottom), (2, 372, 3837, 1788))

    def test_bounds_center_ratio_and_maximality(self):
        for width, height in ((65, 24), (130, 48), (131, 49), (6000, 4000), (4000, 6000), (10000, 240), (66, 100)):
            with self.subTest(width=width, height=height):
                crop = centered_crop(width, height)
                self.assertEqual(crop.width * 24, crop.height * 65)
                self.assertTrue(0 <= crop.left < crop.right <= width)
                self.assertTrue(0 <= crop.top < crop.bottom <= height)
                self.assertEqual(crop.right - crop.left, crop.width)
                self.assertEqual(crop.bottom - crop.top, crop.height)
                self.assertLessEqual(abs(crop.left - (width - crop.right)), 1)
                self.assertLessEqual(abs(crop.top - (height - crop.bottom)), 1)
                self.assertTrue(crop.width + 65 > width or crop.height + 24 > height)

    def test_invalid_dimensions(self):
        for width, height in ((0, 24), (-65, 24), (64, 24), (65, 23), (True, 24), (65.0, 24), (65, "24")):
            with self.subTest(width=width, height=height), self.assertRaises(ValueError):
                centered_crop(width, height)


class CliTests(unittest.TestCase):
    def run_cli(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main(args)
        return status, json.loads(output.getvalue())

    def test_commands_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.bin"
            path.write_bytes(b"abc")
            status, report = self.run_cli(["report", str(path)])
            self.assertEqual(status, 0)
            self.assertNotIn("verified", report)
            for digest, expected in ((report["sha256"], 0), ("0" * 64, 1)):
                status, result = self.run_cli(["verify", str(path), "--sha256", digest, "--size", "3"])
                self.assertEqual(status, expected)
                self.assertEqual(result["verified"], expected == 0)
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                main(["verify", str(path), "--sha256", "1234"])
            self.assertEqual(error.exception.code, 2)
        status, result = self.run_cli(["crop", "130", "48"])
        self.assertEqual(status, 0)
        self.assertEqual(result["left"], 0)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main(["crop", "0", "48"])
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
