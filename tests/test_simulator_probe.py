from pathlib import Path
import tempfile
import unittest

from nikon_z30_research.simulator_probe import private_paths, summarize


class ProbeContractTests(unittest.TestCase):
    def test_raw_paths_cannot_enter_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "research"
            for index in range(3):
                paths = [root / "simulator", root / "input.bi", root / "new-output"]
                paths[index] = repository / "nested"
                with self.assertRaises(ValueError):
                    private_paths(repository, *paths)

    def test_symlink_cannot_bypass_output_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "research"
            repository.mkdir()
            alias = root / "alias"
            alias.symlink_to(repository, target_is_directory=True)
            with self.assertRaises(ValueError):
                private_paths(repository, root / "simulator", root / "input.bi",
                              alias / "new-output")

    def test_existing_output_and_simulator_output_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            existing = root / "existing"
            existing.mkdir()
            for output in (existing, root / "simulator" / "new-output"):
                with self.assertRaises(ValueError):
                    private_paths(root / "research", root / "simulator",
                                  root / "input.bi", output)

    def test_private_paths_allowed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = [root / "simulator", root / "input.bi", root / "new-output"]
            self.assertEqual(private_paths(root / "research", *paths),
                             tuple(path.resolve() for path in paths))

    def test_trace_never_claims_feature_success(self):
        for completed in (False, True):
            report = summarize("worker", ["0x104b740a"], completed, True)
            self.assertFalse(report["native_xpan_demonstrated"])
            self.assertFalse(report["native_tracking_demonstrated"])
            self.assertEqual(report["hardware_readiness"], "not_established")
            self.assertEqual(report["call_completed"], completed)

    def test_unobserved_addresses_are_not_inferred(self):
        self.assertEqual(summarize("render", [], True, True)["observed_calls"], [])
        with self.assertRaises(ValueError):
            summarize("render", ["0x10453fac"], True, True)
