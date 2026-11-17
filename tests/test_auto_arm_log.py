import struct
import unittest

from nikon_z30_research.auto_arm_log import parse, report


def synthetic_log(entries, flags=0, ticks=100):
    header = struct.pack("<8sIIIII4x", b"AUTOARM1", len(entries), len(entries), ticks, 12, flags)
    return header + b"".join(struct.pack("<IBBBBI", *entry) for entry in entries)


class AutoArmLogTests(unittest.TestCase):
    def test_dry_run_in_live_view_is_expected(self):
        log = parse(synthetic_log([(1600, 1, 6, 0, 0, 1), (3200, 2, 6, 0, 0, 1)]))
        self.assertFalse(log.pressed_ok)
        self.assertTrue(all(e.expected for e in log.entries))
        self.assertIn("All entries were in photo live view", report(log))

    def test_entries_outside_live_view_are_flagged(self):
        log = parse(synthetic_log([(1600, 1, 6, 0, 3, 1), (3200, 1, 4, 0, 0, 1), (4800, 1, 6, 0, 0, 0)]))
        self.assertEqual([e.expected for e in log.entries], [False, False, False])
        self.assertIn("3 unexpected entries", report(log))

    def test_remap_build_reports_writer_results(self):
        log = parse(synthetic_log([(1600, 1, 6, 0x0D, 0, 1), (3200, 1, 6, 0x05, 0, 1)], flags=1))
        text = report(log)
        self.assertTrue(log.pressed_ok)
        self.assertIn("OK sent", text)
        self.assertIn("writer refused", text)

    def test_rejects_wrong_magic_and_length(self):
        with self.assertRaises(ValueError):
            parse(b"NOTALOG!" + bytes(24))
        with self.assertRaises(ValueError):
            parse(synthetic_log([(1, 1, 6, 0, 0, 1)])[:-1])


if __name__ == "__main__":
    unittest.main()
