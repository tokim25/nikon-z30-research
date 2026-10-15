import base64
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import struct
import zlib

from nikon_z30_research.cli import main
from nikon_z30_research.xpan import guide_geometry, render_overlay, synthetic_frame, write_demo


class GuideTests(unittest.TestCase):
    def test_acceptance_examples(self):
        first = guide_geometry(1300, 900)
        self.assertEqual((first.width, first.height, first.top, 900 - first.bottom), (1300, 480, 210, 210))
        second = guide_geometry(1600, 480)
        self.assertEqual((second.width, second.height, second.left, 1600 - second.right), (1300, 480, 150, 150))

    def test_known_rotation_mappings_with_offset(self):
        expected = {0: (11, 45, 141, 93), 90: (53, 4, 101, 134),
                    180: (12, 46, 142, 94), 270: (52, 5, 100, 135)}
        for orientation, bounds in expected.items():
            with self.subTest(orientation=orientation):
                guide = guide_geometry(131, 131, 11, 4, orientation)
                self.assertEqual((guide.left, guide.top, guide.right, guide.bottom), bounds)

    def test_portrait_odd_dimensions_bounds_ratio_and_center(self):
        for width, height in ((901, 1301), (1301, 901), (1601, 481), (65, 65)):
            for orientation in (0, 90, 180, 270):
                guide = guide_geometry(width, height, 7, 13, orientation)
                self.assertTrue(7 <= guide.left < guide.right <= 7 + width)
                self.assertTrue(13 <= guide.top < guide.bottom <= 13 + height)
                self.assertLessEqual(abs(guide.left - 7 - (width + 7 - guide.right)), 1)
                self.assertLessEqual(abs(guide.top - 13 - (height + 13 - guide.bottom)), 1)
                wide, narrow = (guide.height, guide.width) if orientation % 180 else (guide.width, guide.height)
                self.assertEqual(wide * 24, narrow * 65)

    def test_invalid_geometry(self):
        for value in (0, -1, float("nan"), float("inf"), "130", None, True, 130.0):
            for field in ("width", "height"):
                args = {"width": 130, "height": 130, field: value}
                with self.subTest(args=args), self.assertRaises(ValueError):
                    guide_geometry(**args)
        for args in ((64, 24, 0, 0, 0), (65, 23, 0, 0, 0), (24, 65, 0, 0, 0),
                     (130, 130, -1, 0, 0), (130, 130, 0, -1, 0),
                     (130, 130, 0, 0, 45), (130, 130, 0, 0, True)):
            with self.assertRaises(ValueError):
                guide_geometry(*args)
        self.assertEqual(guide_geometry(24, 65, orientation=90).height, 65)


class RenderTests(unittest.TestCase):
    def test_html_embedded_png_pixels(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preview.html"
            write_demo(path, 65, 65, 2, 3, 90)
            html = path.read_text()
            self.assertIn("XPan host simulation", html)
            self.assertIn("No camera display hook", html)
            png = base64.b64decode(html.split("base64,", 1)[1].split("'", 1)[0])
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            offset, compressed = 8, b""
            while offset < len(png):
                length = struct.unpack(">I", png[offset:offset + 4])[0]
                kind = png[offset + 4:offset + 8]
                data = png[offset + 8:offset + 8 + length]
                crc = struct.unpack(">I", png[offset + 8 + length:offset + 12 + length])[0]
                self.assertEqual(crc, zlib.crc32(kind + data))
                if kind == b"IHDR":
                    self.assertEqual(struct.unpack(">IIBBBBB", data), (69, 71, 8, 2, 0, 0, 0))
                if kind == b"IDAT":
                    compressed += data
                offset += length + 12
            expected = render_overlay(synthetic_frame(69, 71), 69, 71, 65, 65, 2, 3, 90)
            rows = zlib.decompress(compressed)
            self.assertEqual(rows, b"".join(b"\0" + expected[start:start + 207]
                                          for start in range(0, len(expected), 207)))

    def test_every_pixel_and_source_nonmutation(self):
        source = synthetic_frame(145, 147)
        original = bytes(bytearray(source))
        for orientation in (0, 90, 180, 270):
            guide = guide_geometry(131, 131, 7, 8, orientation)
            rendered = render_overlay(source, 145, 147, 131, 131, 7, 8, orientation)
            self.assertNotEqual(rendered, source)
            self.assertEqual(render_overlay(source, 145, 147, 131, 131, 7, 8, orientation, False), original)
            for row in range(147):
                for column in range(145):
                    offset = (row * 145 + column) * 3
                    expected = original[offset:offset + 3]
                    inside = 7 <= column < 138 and 8 <= row < 139
                    retained = guide.left <= column < guide.right and guide.top <= row < guide.bottom
                    if inside and not retained:
                        expected = bytes(channel // 4 for channel in expected)
                    self.assertEqual(rendered[offset:offset + 3], expected)
            self.assertEqual(source, original)

    def test_invalid_render_inputs(self):
        source = synthetic_frame(130, 130)
        for kwargs in ({"left": 1}, {"enabled": 1}, {"orientation": 360}):
            with self.assertRaises(ValueError):
                render_overlay(source, 130, 130, 130, 130, **kwargs)
        with self.assertRaises(ValueError):
            render_overlay(b"", 130, 130, 130, 130)

    def test_cli_demo_payload_label_and_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "demo.ppm"
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(["xpan-demo", str(path), "--width", "131", "--height", "131",
                                       "--left", "7", "--top", "8", "--orientation", "270", "--no-guides"]), 0)
            self.assertEqual(json.loads(output.getvalue())["label"], "host simulation")
            content = path.read_bytes()
            header, payload = content.split(b"\n255\n", 1)
            self.assertIn(b"host simulation", header)
            self.assertEqual(payload, synthetic_frame(145, 147))
            with self.assertRaises(FileExistsError):
                write_demo(path, 131, 131)
            self.assertEqual(path.read_bytes(), content)
            enabled_path = Path(directory) / "enabled.ppm"
            write_demo(enabled_path, 131, 131, 7, 8, 270)
            self.assertEqual(enabled_path.read_bytes().split(b"\n255\n", 1)[1],
                             render_overlay(payload, 145, 147, 131, 131, 7, 8, 270))
            invalid_path = Path(directory) / "invalid.ppm"
            for options in ((0, 130), (10000, 10000)):
                with self.assertRaises(ValueError):
                    write_demo(invalid_path, *options)
                self.assertFalse(invalid_path.exists())
