# Package verifier audit and unchanged round trip

2026-10-17. F-135. Read-only firmware analysis and an unchanged round trip
entirely in memory. No firmware image was written; hardware remains NO-GO.

## Result

The recovered verifier accepted the exact original package and decoded EG.
A separately expressed inverse of its transform reproduced the entire
34,496,798-byte original package exactly. The source file was reread and
remained identical. This establishes reversible packaging for this original,
not acceptance of a modified package by the camera.

Input identities match [milestone-1-recovery.md](milestone-1-recovery.md).
The audited `tools/verify_and_map.py` source SHA-256 is
`09b0ca2c001191e76748b96678d82c3ed50c1daaba562f3f77922802c2fd4d1a`.

## What the recovered verifier checks

| Check | Coverage and limit |
| --- | --- |
| Original package identity | Complete size and SHA-256, before decoding; rejects any changed package. |
| Decode-mask recovery | Sample count, consistency, connected ordering and completeness; depends on original-specific samples retained privately. |
| Decoded header | Fixed prefix and expected component-count/table-end fields. |
| Container integrity | CRC-16 via `binascii.crc_hqx` with initial value zero, over the decoded container excluding its final 16 bytes; compares a big-endian stored CRC and requires the remaining 14 trailer bytes to be zero. |
| Component layout | Three 32-byte directory entries; payloads contiguous from directory end; reserved fields zero; minimum component size two; no payload crosses the trailer; final component ends exactly at the trailer. |
| Component integrity | CRC residue zero over each complete component, including its trailing check bytes. |
| Main module identity | EG presence, exact size and SHA-256. |
| Memory layout | Scatter descriptor equality is checked using a Python assertion; it disappears under optimized execution. |

The package has a 32-byte outer prefix, followed by the encoded container.
The first 32 bytes inside that container are left unchanged by the transform.
The directory ends at decoded-container offset 144; its component offsets
are relative to that container, not to the outer package or runtime memory.
The outer prefix is covered by the original hash, but not by the decoded
container CRC. Names are parsed as ASCII; the verifier does not independently
require the complete ordered component-name set or reject duplicate names.
The exact original hash currently prevents alternative inputs from exploiting
that gap, but a future candidate validator cannot rely on that original hash.

There is no signature-verification or camera-updater code in this tool.
Therefore camera-side authentication, compatibility and version policy remain
unverified. The observed transform and CRCs do not establish their absence.

## Round-trip method and limits

A newly written private helper loads the recovered definitions without
invoking their report CLI. It instruments only `extract`'s return to retain
decoded data and the recovered mask in memory; all existing validation still
runs. It re-encodes with direct index decomposition instead of the decoder's
precomputed pattern, preserves the untouched prefixes, compares the full
result with the original and verifies the source again. No byte arrays,
mask tables or decoded excerpts are emitted.

Reproduce from the known private WORK directory:

```sh
python3 -B "$WORK/codex-package-roundtrip-audit-private.py"
```

The helper is outside Git beside the previously identified private inputs.
It reports identities and pass/fail metadata only. It shares the recovered
decoder and its mask recovery, so this is not an independent format
implementation or a malformed-candidate test. An unchanged round trip also
does not exercise CRC regeneration or any code modification.

For future candidate validation, retain the encoding parameters derived from
the verified original. Do not rediscover them from changed content: their
recovery relies on original-specific sample assumptions.

## Build decisions from the audit

1. Reversible encoding of this exact original is demonstrated. A feature
   package writer is not needed to investigate that question further.
2. Keep original identity verification separate from candidate integrity
   validation. Removing the original hash checks from the recovered tool
   would discard its main protection without adding sufficient validation.
3. A candidate reader needs explicit bounds, ordered unique component names,
   expected sizes, reserved fields, both CRC levels and unchanged-component
   comparisons. Convert required assertions to explicit errors. Test each
   rejection branch with synthetic fixtures; the recovered three tests do
   not exercise malformed container or CRC paths after the identity gate.
4. Runtime-address translation needs its own bounded API. The recovered
   `window` checks the start of a scatter-mapped read but not a read crossing
   that mapping's end, and does not reject negative lengths explicitly.
5. Before relying on packaging for a hardware decision, investigate the real
   updater's validation boundary offline: which components it accepts, which
   integrity/authentication checks it performs, and whether proposed edits
   reach installed code. A self-consistent package cannot answer that alone.

Follow-up: F-136 implements the decoded-container reader with synthetic tests
and checks the decoded original; see
[native-container-validator.md](native-container-validator.md).
Encoding samples and firmware-derived material remain private. This does
not resolve the separate feature gate in hardware-readiness.md.

The recovered attribution identifies the adapted verifier as MIT-licensed
from Wonder Lantern commit `10e7335977d613075e4e5feed1e3ac331ba90a8a`.
That attribution stays with the private originals. No recovered source or
embedded sample/instruction material was imported into this repository.
