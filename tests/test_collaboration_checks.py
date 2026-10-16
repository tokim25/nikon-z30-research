"""Synthetic tests for the repository's collaboration checks."""

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / ".github" / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ByteDumpTests(unittest.TestCase):
    def setUp(self):
        self.scan = load("check_byte_dumps").suspicious_lines

    def test_identity_hashes_are_allowed(self):
        self.assertEqual(self.scan("commit " + "a1" * 20 + " and digest " + "b2" * 32), [])

    def test_long_hex_run_is_flagged(self):
        self.assertEqual(self.scan("data " + "c3" * 30), [(1, "long hex run")])

    def test_spaced_bytes_are_flagged(self):
        self.assertEqual(self.scan(" ".join(["d4"] * 20)), [(1, "spaced byte sequence")])

    def test_base64_like_run_is_flagged(self):
        self.assertEqual(self.scan("QUJD" * 20), [(1, "long base64-like run")])

    def test_urls_are_ignored(self):
        self.assertEqual(self.scan("see https://example.org/" + "e5" * 40), [])

    def test_plain_prose_is_clean(self):
        self.assertEqual(self.scan("Addresses such as 0x1050a306 are landmarks."), [])


class LaneTests(unittest.TestCase):
    def setUp(self):
        self.module = load("check_lane_ownership")
        self.lanes = json.loads((ROOT / ".github" / "lanes.json").read_text())

    def test_branch_lane(self):
        self.assertEqual(self.module.branch_lane("claude/topic", self.lanes), "claude")
        self.assertEqual(self.module.branch_lane("codex/topic", self.lanes), "codex")
        self.assertIsNone(self.module.branch_lane("feature/x", self.lanes))
        self.assertIsNone(self.module.branch_lane("shared/x", self.lanes))

    def test_own_and_shared_files_are_allowed(self):
        changed = ["docs/simulator-new.md", "docs/facts.md", "AGENTS.md"]
        self.assertEqual(self.module.violations("claude", changed, self.lanes), [])
        transferred = ["docs/native-new.md", "docs/guide-new.md",
                       "docs/image-area-tables.md", "docs/capture-geometry-baseline.md"]
        self.assertEqual(self.module.violations("codex", transferred, self.lanes), [])

    def test_other_lane_files_are_rejected(self):
        found = self.module.violations("claude", ["docs/tracking-new.md"], self.lanes)
        self.assertEqual(found, [("docs/tracking-new.md", "codex")])
        found = self.module.violations("codex", ["docs/simulator-new.md"], self.lanes)
        self.assertEqual(found, [("docs/simulator-new.md", "claude")])
        found = self.module.violations("claude", ["docs/guide-new.md"], self.lanes)
        self.assertEqual(found, [("docs/guide-new.md", "codex")])

    def test_every_pattern_set_is_a_list_of_strings(self):
        for patterns in self.lanes.values():
            self.assertTrue(all(isinstance(p, str) for p in patterns))


if __name__ == "__main__":
    unittest.main()
