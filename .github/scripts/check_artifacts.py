"""Reject unexpected tracked artifacts without printing file contents."""

from pathlib import Path
import subprocess
import sys


ALLOWED_SUFFIXES = {".py", ".md", ".toml", ".yml", ".yaml", ".txt", ".json"}
ALLOWED_NAMES = {".gitignore", ".gitattributes", "LICENSE"}
BLOCKED_DIRECTORIES = {
    "firmware", "extracted", "dumps", "patches", "private", "scratch", "work",
}
MAX_BYTES = 1_000_000


def rejection_reason(path):
    if path.is_symlink():
        return "symlinks are not allowed"
    if path.name not in ALLOWED_NAMES and path.suffix.lower() not in ALLOWED_SUFFIXES:
        return "unexpected file type"
    if not path.is_file():
        return "tracked path is not a regular file"
    if path.stat().st_size > MAX_BYTES:
        return "file exceeds review size limit"
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeError:
        return "file is not UTF-8 text"
    if "\x00" in content:
        return "file contains binary data"
    return None


def main():
    root = Path(__file__).resolve().parents[2]
    git_root = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=root, text=True,
    ).strip()
    if Path(git_root).resolve() != root:
        print("Artifact check requires a Git repository at the project root.")
        return 1
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root)
    failures = []
    for filename in tracked.decode("utf-8").split("\0"):
        if filename:
            relative = Path(filename)
            if any(part.lower() in BLOCKED_DIRECTORIES for part in relative.parts):
                reason = "restricted directory"
            else:
                reason = rejection_reason(root / relative)
            if reason:
                failures.append(f"{filename}: {reason}")
    if failures:
        print("Artifact check failed:\n" + "\n".join(failures))
        return 1
    print("Tracked artifact checks passed. Manual content review is still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
