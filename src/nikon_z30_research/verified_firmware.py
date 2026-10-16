"""A hard gate on the owner's one verified original firmware module.

Build-phase work (docs/build-phase-gate.md) must refuse anything but the
exact module already verified in docs/milestone-1-recovery.md: same size,
same SHA-256. This module holds those two known-good values and a function
that raises, rather than returning a value a caller could ignore, on any
mismatch. It never reads, stores, or returns firmware bytes; it only reports
whether a file's identity matches.
"""

from pathlib import Path

from .firmware import FirmwareReport, inspect_firmware, verify_firmware

# From docs/milestone-1-recovery.md: the main EG module, decoded in memory
# from the owner's verified original package and never altered since.
VERIFIED_EG_SIZE = 33_939_514
VERIFIED_EG_SHA256 = "8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa"


class UnverifiedFirmwareError(ValueError):
    """Raised when a file's size or hash does not match the verified original."""


def require_verified_eg_module(path: str | Path) -> FirmwareReport:
    """Return the report for `path`, or raise if it is not the one verified module.

    This is the only acceptable way for build-phase code to accept a firmware
    path: call this first, and only proceed on a normal return. A caught
    exception, a bare `except`, or ignoring the return value are all misuse.
    """
    report = inspect_firmware(path)
    if not verify_firmware(report, VERIFIED_EG_SHA256, VERIFIED_EG_SIZE):
        raise UnverifiedFirmwareError(
            f"{path} does not match the verified original EG module "
            f"(expected {VERIFIED_EG_SIZE} bytes, got {report.size_bytes}); refusing to proceed"
        )
    return report
