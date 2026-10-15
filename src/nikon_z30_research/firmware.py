"""Read-only file inventory and comparison against user-supplied expectations."""

from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import stat


@dataclass(frozen=True)
class FirmwareReport:
    size_bytes: int
    sha256: str


def inspect_firmware(path: str | Path) -> FirmwareReport:
    """Hash a regular file in bounded chunks without decoding or writing it."""
    source = Path(path)
    if not stat.S_ISREG(source.stat().st_mode):
        raise ValueError("firmware input must be a regular file")
    digest = hashlib.sha256()
    size_bytes = 0
    with source.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            size_bytes += len(chunk)
    return FirmwareReport(size_bytes, digest.hexdigest())


def verify_firmware(
    report: FirmwareReport, expected_sha256: str, expected_size: int | None = None
) -> bool:
    """Compare full SHA-256 and optional size; this does not prove authenticity."""
    if not isinstance(expected_sha256, str) or not re.fullmatch(
        r"[0-9a-fA-F]{64}", expected_sha256
    ):
        raise ValueError("expected SHA-256 must contain exactly 64 hexadecimal characters")
    if expected_size is not None and (
        type(expected_size) is not int or expected_size < 0
    ):
        raise ValueError("expected size must be a nonnegative integer")
    return report.sha256 == expected_sha256.lower() and (
        expected_size is None or report.size_bytes == expected_size
    )
