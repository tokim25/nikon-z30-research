"""Offline JSON reports; exit 0 on success, 1 on mismatch, 2 on invalid input."""

import argparse
from dataclasses import asdict
import json

from .firmware import inspect_firmware, verify_firmware
from .geometry import centered_crop
from .verified_firmware import require_verified_eg_module
from .xpan import write_demo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report", help="Report file size and SHA-256")
    report.add_argument("path")
    verify = commands.add_parser("verify", help="Compare with a supplied full SHA-256")
    verify.add_argument("path")
    verify.add_argument("--sha256", required=True)
    verify.add_argument("--size", type=int)
    require = commands.add_parser(
        "require-verified-eg",
        help="Hard gate: exit nonzero unless this is the one verified EG module",
    )
    require.add_argument("path")
    crop = commands.add_parser("crop", help="Compute largest exact centered 65:24 crop")
    crop.add_argument("width", type=int)
    crop.add_argument("height", type=int)
    demo = commands.add_parser("xpan-demo", help="Write a synthetic host simulation as HTML or PPM")
    demo.add_argument("output", help="New output path; existing files are never overwritten")
    demo.add_argument("--width", type=int, default=650)
    demo.add_argument("--height", type=int, default=450)
    demo.add_argument("--left", type=int, default=24)
    demo.add_argument("--top", type=int, default=24)
    demo.add_argument("--orientation", type=int, choices=(0, 90, 180, 270), default=0)
    demo.add_argument("--no-guides", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "xpan-demo":
            guide = write_demo(args.output, args.width, args.height, args.left, args.top,
                               args.orientation, not args.no_guides)
            result = {"label": "host simulation", "output": args.output,
                      "guides_enabled": not args.no_guides, "guide": asdict(guide),
                      "limitation": "No camera display hook or native capture behavior validated"}
        elif args.command == "crop":
            result = asdict(centered_crop(args.width, args.height))
        elif args.command == "require-verified-eg":
            result = asdict(require_verified_eg_module(args.path))
            result["verified"] = True
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
