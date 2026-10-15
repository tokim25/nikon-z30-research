"""Explicit local stock-display experiment; never proof of native XPan or AF."""

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys

from .firmware import inspect_firmware


SIMULATOR_REVISION = "0ba0c3547ccbec09e7c861eaca35db8e82795f15"
EG_HASH = "8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa"
EG_SIZE = 33939514
PROFILES = {
    "refresh": (0x10453FAC, 0x10453AC2, 0x10453E2E, 0x10453D14),
    "worker": (0x104B74F4, 0x104B740A, 0x103C3810, 0x103C3568),
    "render": (0x103C0AC2, 0x103C0BC0, 0x103C1B54, 0x103C05D2),
}


def private_paths(repository: Path, simulator: Path, firmware: Path, output: Path):
    repository = repository.resolve()
    paths = tuple(path.resolve() for path in (simulator, firmware, output))
    for path in paths:
        if path == repository or repository in path.parents:
            raise ValueError("Simulator, firmware and raw output must be outside the research repository")
    simulator, firmware, output = paths
    if output.exists():
        raise ValueError("Use a new private output directory for each run")
    if output == simulator or simulator in output.parents:
        raise ValueError("Raw output must be outside the simulator checkout")
    return paths


def summarize(profile: str, calls: list, completed: bool, unchanged: bool) -> dict:
    expected = {hex(address) for address in PROFILES[profile]}
    if any(address not in expected for address in calls):
        raise ValueError("Observation is outside the selected trace profile")
    return {
        "profile": profile,
        "observed_calls": calls,
        "call_completed": completed,
        "firmware_unchanged": unchanged,
        "assisted_startup": True,
        "synthetic_preview": True,
        "native_xpan_demonstrated": False,
        "native_tracking_demonstrated": False,
        "hardware_readiness": "not_established",
    }


def validate_simulator(simulator: Path) -> None:
    revision = subprocess.check_output(
        ["git", "-C", str(simulator), "rev-parse", "HEAD"], text=True,
    ).strip()
    if revision != SIMULATOR_REVISION:
        raise ValueError("Simulator revision differs from the reviewed version")
    changes = subprocess.check_output(
        ["git", "-C", str(simulator), "status", "--porcelain", "--untracked-files=all"],
        text=True,
    )
    if changes.strip():
        raise ValueError("Simulator checkout has unreviewed changes")
    manifest = json.loads((simulator / ".local/build-manifest.json").read_text())
    binary = simulator / ".build/build/qemu-system-arm"
    if inspect_firmware(binary).sha256 != manifest["binary_sha256"]:
        raise ValueError("Simulator binary differs from its local build manifest")
    for relative, expected in manifest["sources"].items():
        source = (simulator / relative).resolve()
        if simulator.resolve() not in source.parents:
            raise ValueError("Invalid build source path")
        if inspect_firmware(source).sha256 != expected:
            raise ValueError("Simulator source differs from its local build manifest")


def run_probe(simulator: Path, firmware: Path, output: Path, profile: str) -> dict:
    repository = Path(__file__).resolve().parents[2]
    simulator, firmware, output = private_paths(repository, simulator, firmware, output)
    if profile not in PROFILES:
        raise ValueError("Unknown trace profile")
    before = inspect_firmware(firmware)
    if (before.sha256, before.size_bytes) != (EG_HASH, EG_SIZE):
        raise ValueError("Expected the unchanged verified C1.20 EG module")
    validate_simulator(simulator)
    options = [name for name in os.environ if name.startswith("Z30_")]
    if options:
        raise ValueError("Remove inherited Z30 device options before this controlled experiment")
    sys.path.insert(0, str(simulator / "tools"))
    display = importlib.import_module("display_session")
    liveview = importlib.import_module("liveview_session")
    session = display.Session(str(output), firmware_image=firmware,
                              device_env=liveview.DEVICE_ENV)
    try:
        liveview.start(session)
        session.frame("stock-before")
        result = session.input(0x1032427E, [], observe=PROFILES[profile])
        session.run_for(2)
        session.frame("stock-after")
        after = inspect_firmware(firmware)
        summary = summarize(profile, [entry["pc"] for entry in result["observations"]],
                            result["completed"], before == after)
        summary["simulator_revision"] = SIMULATOR_REVISION
        summary["frame_sha256"] = hashlib.sha256(
            (session.graphics / "gui-latest.ppm").read_bytes()
        ).hexdigest()
        (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        if not summary["firmware_unchanged"]:
            raise RuntimeError("Firmware identity changed during experiment")
        return summary
    finally:
        session.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--simulator", required=True, type=Path)
    parser.add_argument("--firmware", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--profile", choices=PROFILES, default="refresh")
    arguments = parser.parse_args()
    result = run_probe(arguments.simulator, arguments.firmware, arguments.output,
                       arguments.profile)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
