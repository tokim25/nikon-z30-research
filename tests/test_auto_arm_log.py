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

    def test_diag_log_separates_samples_and_names_failed_checks(self):
        header = struct.pack("<8sIIIII4x", b"AUTOARM1", 3, 1, 60, 24, 2)
        records = [
            (1000, 1, 6, 2, 0, 1, 1, 0, 0),   # sample: AF busy
            (2000, 1, 6, 2, 0, 1, 0, 0, 0),   # sample: idle
            (2100, 1, 6, 0, 0, 1, 0, 0, 0),   # would-press entry
        ]
        log = parse(header + b"".join(struct.pack("<IBBBBIIII", *r) for r in records))
        self.assertTrue(log.diag)
        self.assertEqual(len(log.samples), 2)
        self.assertEqual(len(log.presses_logged), 1)
        self.assertEqual(log.samples[0].failed_checks(), ["af_busy=0x1"])
        self.assertEqual(log.samples[1].failed_checks(), [])
        text = report(log)
        self.assertIn("1 entries", text)
        self.assertIn("none (idle)", text)

    def test_diag_log_with_photo_selector_flags_movie(self):
        header = struct.pack("<8sIIIII4x", b"AUTOARM1", 2, 1, 40, 28, 2)
        records = [
            (1000, 2, 6, 2, 0, 1, 0, 0, 0, 1),   # sample: movie (photo_sel 1)
            (1100, 2, 6, 0, 0, 1, 0, 0, 0, 1),   # would-press entry in movie
        ]
        log = parse(header + b"".join(struct.pack("<IBBBBIIIII", *r) for r in records))
        self.assertEqual(log.samples[0].failed_checks(), ["photo_sel=0x1"])
        self.assertFalse(log.presses_logged[0].expected)
        self.assertIn("1 unexpected entries", report(log))

    def test_box_events_report_presses_before_the_box(self):
        header = struct.pack("<8sIIIII4x", b"AUTOARM1", 4, 2, 40, 28, 3)
        records = [
            (1000, 2, 6, 0x0D, 0, 1, 0, 0, 0, 0),   # press
            (1500, 2, 6, 0x0D, 0, 1, 0, 0, 0, 0),   # press
            (1700, 2, 6, 0x10, 0, 1, 0, 1, 0, 0),   # box up
            (9000, 4, 6, 0x10, 0, 1, 0, 0, 0, 0),   # box gone
        ]
        log = parse(header + b"".join(struct.pack("<IBBBBIIIII", *r) for r in records))
        self.assertEqual(len(log.presses_logged), 2)
        self.assertEqual(len(log.box_events), 2)
        text = report(log)
        self.assertIn("box up, 0.20 s after a press (2 presses since the last box)", text)
        self.assertIn("box gone", text)

    def test_direct_build_reports_tracking_mode_calls(self):
        header = struct.pack("<8sIIIII4x", b"AUTOARM1", 1, 1, 20, 28, 7)
        record = struct.pack("<IBBBBIIIII", 1000, 2, 6, 0x21, 0, 1, 0, 0, 0, 0)
        log = parse(header + record)
        self.assertTrue(log.direct)
        text = report(log)
        self.assertIn("called the tracking mode directly", text)
        self.assertIn("tracking mode called", text)
        self.assertNotIn("writer refused", text)

    def test_rejects_wrong_magic_and_length(self):
        with self.assertRaises(ValueError):
            parse(b"NOTALOG!" + bytes(24))
        with self.assertRaises(ValueError):
            parse(synthetic_log([(1, 1, 6, 0, 0, 1)])[:-1])


if __name__ == "__main__":
    unittest.main()
