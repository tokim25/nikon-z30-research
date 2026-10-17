# XPan 5200 x 1920 centered: partial offset map (static, scratch copy)

2026-10-17. Read-only static mapping on a scratch working copy of the owner's
original. Restricted bytes, decoded module and raw output stay outside the
repo; only addresses, sizes and values listed here are recorded. No patch,
no manifest, no checker run, no flash, no camera access. Hardware remains
**NO-GO**.

## Identity

- Original container SHA-256 matched the pinned value (size 34,496,798).
- Decoded EG passed the existing stock-module identity check (size 33,939,514,
  SHA-256 pinned in [milestone-1-recovery.md](milestone-1-recovery.md)).

## Candidate sites for the 1:1 slot (EG, ROM address to file offset = address - 0x10020000)

| Address | Current u16 pair | Meaning (inferred) | Probe change |
| --- | --- | --- | --- |
| `0x115a4d5c` | (936, 0) | 1:1 internal origin | origin 192,896 in probe |
| `0x115a4d9c` | (3728, 3728) | 1:1 readout area, large | area 5216 x 1936 in probe |
| `0x115a4dd8` | (3712, 3712) | 1:1 output, large | derived 5200 x 1920 in probe |
| `0x115a4e14` | (3728, 3728) | 1:1 readout area, second table | not in probe; check |

Neighbouring 16:9 origin pair at `0x115a4d54` is (0, 292) and DX origin pair
at `0x115a4d58` is (0, 0); these are not edited.

## Not established

- Whether the probe's origin and area values map one-to-one to the entries
  above. The probe changed guest memory, not these file bytes.
- Whether the output record at `0x115a4dd8` must change for the 5200 x 1920
  result, or is derived.
- The second table entry at `0x115a4e14`, and the other repeated 3712 entries
  near `0x115a4e80`.
- Retouch Trim's square-forcing for the 1:1 slot (table A), not mapped here.

## Next

A probe-level check: in the simulator, confirm which entries must change, using
a temporary guest-memory edit that is never written to a file. Then produce the
exact manifest for the checker. Neither has been done.

## RAM mapping and probe status (2026-10-17, scratch copy)

- The per-area pointer table at ROM `0x12049a7c` (38 entries) is outside the
  scatter source range, so its entries are read as ROM addresses, not RAM
  copies. Index 4 points to `0x115a4d9c` (1:1 readout area record) and index 9
  to `0x115a4dd8` (1:1 output record); the 1:1 readout pair there matches the
  table above.
- Writes to those addresses would be debugger writes into ROM-mapped data. Not
  yet checked whether the pinned QEMU accepts them.
- The crop-builder probe was not run. It needs a constructed input object and
  the area/origin lookups in a started state; the harness (`tools/run.py`,
  `tools/guest_call.py`) is available but the object setup is not written.
- Result: the 5200 x 1920 derivation is **not confirmed** in the simulator.
  The output-record question remains open. The digest input stays open.

## Repoint method (F-079/F-080) status

- F-079 and F-080 (2026-10-16) repointed the RAM pointer copy at `0xc18c7de8`
  for indices 4, 9, 14, 19 and called the builder for area 4. Prior result:
  large window 5208 x 1928 (offsets 8, 8); not 5200 x 1920.
- The repro script for that method lives under the private WORK folder, which
  is not present on this machine. Re-running it, or writing an equivalent
  harness, needs a memory-write helper and a free RAM region for the scratch
  records, neither of which is in `tools/`. Blocked; no run made.
