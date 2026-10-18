# Regression baseline, 2026-10-18

A snapshot of the repository's automated checks on one day, so a later run has
something to compare against. This is tooling and test health only. It says
nothing about the camera, the firmware, or whether any feature is ready. No
camera was touched and no firmware was read.

## How to reproduce

From the repository root, with Python 3.11, 3.12, or 3.13:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 .github/scripts/check_artifacts.py
PYTHONDONTWRITEBYTECODE=1 python3 .github/scripts/check_byte_dumps.py
git diff --check
```

The lane-ownership check (`.github/scripts/check_lane_ownership.py`) only does
something on a pull request from a `claude/` or `codex/` branch, so it is not
part of a local baseline.

## Results on this date

Branch `claude/plain-docs-and-manifest-checks`, taken from `main` at `71133cd`.

| Check | Result |
| --- | --- |
| Unit tests (Python 3.11) | pass |
| Unit tests (Python 3.12) | pass |
| Unit tests (Python 3.13) | 148 tests, pass |
| `check_artifacts.py` | pass |
| `check_byte_dumps.py` | pass; no encoded-data patterns found |
| `git diff --check` | clean |

The suite grew from 130 to 148 tests on this branch: 20 new tests for the
`edit_policy` module described below, minus overlap counted in one file. The
130-test figure is the `main` baseline.

## Line coverage

Measured on Python 3.13 with `coverage`, statements plus branches. Coverage is
not installed in CI; this was run once by hand.

| Module | Coverage | Note |
| --- | --- | --- |
| `edit_policy` | 100% | new this branch |
| `patch_audit`, `preflight`, `installation`, `package_digest`, `firmware`, `geometry`, `verified_firmware` | 100% | |
| `package_container`, `tracking`, `xpan`, `call_contract` | 96–99% | one or two error paths each |
| `cli` | 94% | |
| `guest_call_safe` | 92% | a few rejection paths |
| `simulator_probe` | 38% | the part that launches the simulator needs the pinned simulator, which is not in this environment |
| `__main__` | 0% | entry-point shim |
| whole package | ~91% | |

## What these numbers do not mean

- High coverage means the test code runs most of the project's own lines. It
  does not mean any firmware behavior is proven.
- Every test uses made-up (synthetic) data. No test reads the real firmware or
  any candidate image. The results are identical whether or not the private
  files are present.
- `simulator_probe`'s low number is expected: the code that starts the
  simulator cannot run without the pinned simulator, which lives only on the
  owner's machine.

Written by Claude in collaboration with Tony Kim.
