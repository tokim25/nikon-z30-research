# Native updater digest: selector and input boundaries

2026-10-17. F-140. Read-only follow-up to
[native-updater-validation.md](native-updater-validation.md). No updater
execution, digest regeneration, firmware modification or image writes.

## Result and build consequence

The previously unknown selector is an encoded-container flag carried through
the per-file cache. Static evaluation of the verified original's header
selects flag 1. Restoring that successfully parsed body-file record selects
the validation path containing the additional digest check. This is a static
prediction of that path, not an observed camera or simulator transition.

The digest's message and expected-value boundaries are now identified. One
eight-byte input still comes from `0x10000088`, outside EG's direct mapping,
and has no verified source in the current analysis. The native digest check
has therefore not been reproduced, and F-138 remains decoded-container-only.

## Encoded-format flag chain

The header reader `0x101d5900` is called with file offset 32. It reads the
container prefix/header, tests the encoded count/header field, decodes that
region and verifies the decoded field. On success, it writes 1 to its parser
state byte at offset 8 (`0x101d5960`). Initialization clears this state.
The original input has a nonzero pre-decode test field and the expected zero
post-decode field; these were checked privately without emitting bytes.

`0x101d5ab2` returns this parser byte. The per-file snapshot code calls that
getter at `0x101cf352` and stores the result at record offset `0x1a0`.
It then clears the shared field, so reading the global at an arbitrary
moment would not establish the selected file's format.

The selected-file restore routine `0x101cf858` copies the cached `+0x1a0`
value into the shared state at `+0x2c` (`0x101cf8c2`), and restores the
discovery type from the same record. Getter `0x101cf8cc` returns that flag
only for discovery type 4, the camera-body package type.

Execution setup calls that getter at `0x10234440`: nonzero reaches
`0x101ce518`; zero reaches `0x101ce324`. Thus the successful encoded-original
parse and selected-record restore explain the additional-check branch. Its
natural UI reachability and execution have not been tested here.

## Digest inputs and their origins

| Input | Source and current evidence |
| --- | --- |
| Expected 20-byte digest | First 20 bytes of the original outer package, copied into checker state by setup helper `0x101d701a`. |
| Main message | Decoded container beginning after the 32-byte outer prefix, with length equal to package length minus 32. |
| Additional eight-byte message suffix | Checker `0x101d816a` transforms configured metadata via callback, copies eight bytes to the message end, increases its length by eight, then computes the digest. |
| Metadata source | Setup helper `0x101d7026` copies eight bytes from address `0x10000088`. This source remains unmapped in the verified EG input. |
| Other suffix configuration | A fixed numeric seed and a short local string supplied by setup in `0x101ce518`; callback `0x101ce514` transfers to the metadata transform `0x101d3f14`. Their source locations are identified; their bytes are retained privately. |

The 20-byte computation remains consistent with SHA-1 at the instruction
level. This pass traced its call/input boundaries, not a complete independent
implementation. The unknown low-memory input prevents reproducing the expected
digest comparison on the original; no candidate digest was guessed or generated.

A full-image literal search found one aligned code-region reference to
`0x10000088`, the known setup literal. Other raw matches were unaligned and
not promoted to code references. This does not exclude computed pointers,
aliases or a separate boot-region source. The pinned simulator's machine
source names the loaded main-module base at `0x10020000` and provides no
verified value for this lower address; this is not grounds to substitute
simulator defaults for a camera input.

## Reproduction and next step

The private updater-audit helper now verifies the flag producer, snapshot,
restore, getter and branch landmarks plus the original header predicates,
digest suffix-copy/length landmarks and external input pointer. The native
mask/CRC comparisons and unchanged package/preflight baselines still pass.
It emits metadata only and explicitly reports that the digest branch was
not executed and its inputs are not fully resolved.

```sh
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-native-updater-audit-private.py"
```

F-141 checks startup page-table/scatter evidence and finds no verified source
for this input; see [native-boot-mapping-boundary.md](native-boot-mapping-boundary.md).
It also maps the updater RAM block back to verified EG bytes. The current
next step is tracing that block toward actual flash-write boundaries; the
digest input remains a recorded missing-input boundary.

Hardware remains NO-GO. Original inputs and recovered tools are unchanged;
no commit, push or PR was made.
