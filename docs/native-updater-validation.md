# Native updater validation boundary

2026-10-17. F-139. Read-only static analysis of the verified original EG;
no updater execution, firmware modification or camera access.

## Build decision

Follow-up F-140 traces the selection predicate and digest input boundaries;
see [native-updater-digest-inputs.md](native-updater-digest-inputs.md).
The original statically predicts the extra-digest branch after successful
selected-record restore. The eight-byte low-memory source remains unresolved.
The rest of this report records the initial F-139 findings.

The native body-package path has been identified. Its decoding transform
and CRC primitive agree with the desktop tooling. It also contains an
additional 20-byte digest comparison that F-135 through F-138 do not check.
The condition selecting that validation branch and all digest inputs are
not yet resolved. A passing decoded-container preflight must not be promoted
to a camera-acceptable package claim.

## Body-package discovery and parsing

The firmware-management menu calls `0x10234274`, which reaches discovery
`0x101ce206`. Its table row at `0x11570f48` associates the camera-body
package filename pattern with discovery type 4. The type-4 table branch
reaches parser `0x101cdcea`, not the neighboring component-specific parsers.

That parser calls `0x101d5900` to read the encoded container header and
directory, then `0x101d5a20` to match component names against four wildcard
templates. All three components in the verified original match exactly one
template. The verified EG matches template index 1. Parser output classifies
that main component as execution type 3. Discovery type 4 and execution type
3 are different namespaces; neither is the stored image-area choice.

The parser checks read/seek results, header-derived component extents against
device-side limits, selected component lengths and selected internal fields.
This pass does not establish its complete malformed-input acceptance rules,
all compatibility checks or same-version/downgrade policy.

## Algorithms checked against the original

Native decoding is at `0x101d5882`, using three 256-byte tables addressed
from `0x115711f0`. Its zero-offset path skips the first 32 container bytes.
The tables were compared privately with the recovered decoder's original-
derived masks. Each normalized table and the combined constant agree,
establishing equivalent effective masks over their indexed domains. No
tables or sample bytes are reproduced here.

The CRC wrapper `0x101d3f0c` supplies a zero seed to `0x101d3ee8`.
All 256 entries of the native table at `0x11c5c304` agree with the table
implied by Python's `binascii.crc_hqx` with initial value zero. Static code
shows byte-wise accumulation to a 16-bit result. This supports the desktop
CRC primitive; it does not alone establish every native coverage boundary.

## Additional digest check: unresolved preflight requirement

The execution setup at `0x10234374` selects between validation paths at
`0x101ce324` and `0x101ce518`, using `0x101cf8cc`. That getter checks the
body discovery type and returns a state field. Its producer and the exact
value for the verified original have not been established in this pass.

The latter path decodes the loaded package and calls `0x101d816a` before
its subsequent CRC check. This routine computes and compares a 20-byte
digest; the comparison is at `0x101d81e0`. Its initialization, block mixing
and finalization are consistent with SHA-1 (static inference, high confidence),
but the complete package-level scheme has not been reproduced.

The setup copies the original package's first 20 bytes as the expected digest.
It also configures a callback and other inputs, including an eight-byte read
from `0x10000088`, which is below the verified EG's direct file mapping.
The callback transforms metadata and the checker appends eight bytes to its
message before computing the digest. All work here only read that code;
no such buffer mutation was executed. The source/mapping of the low-memory
input and the complete digest construction remain unverified.

This is evidence of a digest check, not proof of a public-key signature,
a secret-key scheme or their absence. Do not add a guessed hash or weaken
the camera's check. Resolve its predicate and inputs from offline evidence
before deciding what candidate-package validation must require.

## Installation handoff: where this pass stops

The main component's execution-type-3 branch reaches `0x101ce89e` through
the dispatcher at `0x10233d1c`. Its arguments come from the prepared
component pointer/length arrays. The preparation strips the two component
CRC bytes from the length passed downstream.

`0x101ce89e` prepares and aligns the buffer, handles a configured remainder,
collects execution state and calls an ARM trampoline at `0x1017e370`.
That trampoline transfers to Thumb code at `0xc2b10cd5`. This relocation
target has not been mapped back to its source in this pass. The actual
erase/program operations, destination layout, readback, activation and
power-loss behavior remain unverified. Neighboring component paths were
examined for disambiguation and are not evidence of the EG install path.

## Reproduction and limits

The private helper checks original identities through the existing audit,
then selected call/dispatch landmarks, component-template matching, effective
decoder-table equivalence, CRC-table equivalence and the EG-specific handoff.
It uses Capstone 5.0.6 and emits metadata only. It is newly written code,
not recovered code or an exhaustive control-flow verifier.

```sh
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-native-updater-audit-private.py"
```

The helper and restricted inputs stay at the known private WORK path. No
firmware image, extracted tables or raw decode report was written. Existing
recovered tools and the original package remain unchanged.

F-140 completes that selector trace; the current next step is mapping the
extra digest's eight-byte input from verified local boot/relocation evidence.
The relocated installation target is a separate open thread. Hardware remains NO-GO.
