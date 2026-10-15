"""Offline JSON reports; exit 0 on success, 1 on mismatch, 2 on invalid input."""

import argparse
from dataclasses import asdict
import json

from .firmware import inspect_firmware, verify_firmware
from .geometry import centered_crop


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report", help="Report file size and SHA-256")
    report.add_argument("path")
    verify = commands.add_parser("verify", help="Compare with a supplied full SHA-256")
    verify.add_argument("path")
    verify.add_argument("--sha256", required=True)
    verify.add_argument("--size", type=int)
    crop = commands.add_parser("crop", help="Compute largest exact centered 65:24 crop")
    crop.add_argument("width", type=int)
    crop.add_argument("height", type=int)
    args = parser.parse_args(argv)
    try:
        if args.command == "crop":
            result = asdict(centered_crop(args.width, args.height))
        else:
            firmware = inspect_firmware(args.path)
            result = asdict(firmware)
            if args.command == "verify":
                result["verified"] = verify_firmware(firmware, args.sha256, args.size)
        print(json.dumps(result, sort_keys=True))
        return 1 if result.get("verified") is False else 0
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
