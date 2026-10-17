# On-camera test readiness record

2026-10-17. Preparation only. No camera was connected, flashed or touched.
No push or merge. Hardware remains **NO-GO** (see
[hardware-readiness.md](hardware-readiness.md) and
[build-phase-gate.md](build-phase-gate.md)).

## Exact-firmware identity check: NOT RUN

- The owner's original package is not present in this environment. The
  `WORK` variable is unset, and a bounded search of the home directory for
  `Z_30_0120*` and `EG2090*` found nothing. No identity result is claimed.
- Required identities, from [milestone-1-recovery.md](milestone-1-recovery.md):
  - Original package: 34,496,798 bytes, SHA-256
    `1a5449ef505f1f347ed4e066a6a3f588ea542240680e83f4ebcae3b16da3434a`.
  - Main EG module: 33,939,514 bytes, SHA-256
    `8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
- Command to run once the owner supplies the file path, from the repo root
  with the restricted input kept outside Git:

```bash
PYTHONPATH=src python3 -m nikon_z30_research require-verified-eg /path/to/extracted-eg.bin
```

  Exit code 0 is required. Any other result blocks every build step.

## Readiness state

| Gate item | State |
| --- | --- |
| Exact original identity (EG) | Not run; input absent here |
| Digest input at `0x10000088` | Unresolved (F-140, F-141) |
| Native standalone-EG route | Not verified end to end ([xpan-build-decision.md](xpan-build-decision.md)) |
| Simulator acceptance, bars and geometry | Not complete |
| Lifecycle gate (condition 1 natural transitions) | Open; not waived |
| Backup and recovery decision | Not recorded here; owner decision |
| Owner approval immediately before any hardware step | Not given |

## Result

Test readiness is **not achieved**. The identity check is the first blocker,
and the digest input is the principal technical blocker. Neither can be
cleared by this session.
