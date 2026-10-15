"""Fail a pull request from a lane branch that edits another lane's files.

Branches named claude/<topic> or codex/<topic> belong to that lane. Files
matching the other lane's patterns in .github/lanes.json are off limits. Shared
files are open to both lanes. Other branches, including the owner's, are not
restricted. Outside a pull request the check does nothing.
"""

import fnmatch
import json
import os
import subprocess
import sys
from pathlib import Path


def branch_lane(branch, lanes):
    prefix = branch.split("/")[0]
    return prefix if prefix in lanes and prefix != "shared" else None


def violations(lane, changed, lanes):
    """Return (file, owning lane) pairs the given lane may not touch."""
    found = []
    for name in changed:
        for other, patterns in lanes.items():
            if other in (lane, "shared"):
                continue
            if any(fnmatch.fnmatch(name, pattern) for pattern in patterns):
                found.append((name, other))
    return found


def main():
    root = Path(__file__).resolve().parents[2]
    lanes = json.loads((root / ".github" / "lanes.json").read_text())
    head, base = os.environ.get("GITHUB_HEAD_REF", ""), os.environ.get("GITHUB_BASE_REF", "")
    lane = branch_lane(head, lanes) if head else None
    if not lane or not base:
        print("Lane check skipped: not a pull request from a lane branch.")
        return 0
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", f"origin/{base}...HEAD"], cwd=root, text=True,
    ).split()
    bad = violations(lane, changed, lanes)
    if bad:
        print(f"Branch {head} (lane {lane}) edits files owned by another lane:")
        print("\n".join(f"  {name} (owned by {owner})" for name, owner in bad))
        print("Move the change to the owning lane, or ask the owner to approve it.")
        return 1
    print(f"Lane check passed for lane {lane}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
