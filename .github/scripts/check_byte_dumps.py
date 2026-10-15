"""Flag text that looks like encoded binary data in tracked files.

Allowed: git object ids and SHA-256 digests (exactly 40 or 64 hex characters).
Everything else that looks like a hex or base64 dump is reported by line number
only, never printed, so a failing run does not leak the content.
"""

import re
import subprocess
import sys
from pathlib import Path

HEX_RUN = re.compile(r"(?<![0-9A-Za-z])[0-9A-Fa-f]{24,}(?![0-9A-Za-z])")
B64_RUN = re.compile(r"[A-Za-z0-9+/]{60,}={0,2}")
SPACED_BYTES = re.compile(r"(?:(?<![0-9A-Za-z])[0-9A-Fa-f]{2}(?![0-9A-Za-z])[ :,-]){16,}")
URL = re.compile(r"https?://\S+")
IDENTITY_LENGTHS = {40, 64}
TEXT_SUFFIXES = {".py", ".md", ".toml", ".yml", ".yaml", ".txt", ".json"}


def suspicious_lines(text):
    """Return (line number, reason) pairs for lines that look like dumps."""
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = URL.sub("", line)
        reason = None
        for run in HEX_RUN.findall(stripped):
            if len(run) not in IDENTITY_LENGTHS:
                reason = "long hex run"
        if reason is None:
            for run in B64_RUN.findall(stripped):
                is_identity = re.fullmatch(r"[0-9A-Fa-f]+", run) and len(run) in IDENTITY_LENGTHS
                if not is_identity:
                    reason = "long base64-like run"
        if reason is None and SPACED_BYTES.search(stripped):
            reason = "spaced byte sequence"
        if reason:
            hits.append((number, reason))
    return hits


def main():
    root = Path(__file__).resolve().parents[2]
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    failures = []
    for name in filter(None, tracked):
        path = root / name
        if path.suffix.lower() in TEXT_SUFFIXES and path.is_file():
            for number, reason in suspicious_lines(path.read_text(encoding="utf-8")):
                failures.append(f"{name}:{number}: {reason}")
    if failures:
        print("Possible encoded data found (contents not shown):\n" + "\n".join(failures))
        return 1
    print("No encoded-data patterns found. Manual content review is still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
