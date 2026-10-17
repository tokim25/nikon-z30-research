# Read-only installation model in preflight

2026-10-17. F-143. Newly written `src/nikon_z30_research/installation.py`,
integrated into `preflight_decoded`. The native basis is
[native-install-span.md](native-install-span.md), F-142.

## Contract and report scope

`InstallationPolicy` names one component, target start, full capacity,
high-level chunk size and optional protected address ranges. The policy
must come from independently reviewed original evidence, never candidate
contents. The public code contains no real target manifest or component
names. Its fixed preparation rules exclude two trailing component CRC bytes
and model the remaining target capacity as `0xFF`.

`model_installation` checks the component CRC, immutable input, payload fit,
32-bit address bounds, power-of-two chunk alignment and ordered protected
ranges. Any intersection with the full target, including padding, fails.
Adjacent protected ranges that end at the target start or begin at its end
are accepted. A malformed component or policy produces an explicit error.

The immutable report contains the component and payload hashes, target
start/end, full capacity, payload/padding lengths, excluded CRC length and
an expected full-span hash. Padding is fed to SHA-256 in bounded temporary
chunks; no complete padded image is constructed or written. The expected
hash describes the model, not physical flash readback.

Chunk lookup reports one bounded address range at a time. Erase order is
ascending; program order processes later chunks before the leading chunk.
No device commands or installation workflow are exposed. A one-chunk model
has the same sole range in both orders.

## Integration with the candidate checks

`preflight_decoded(..., installation=policy)` selects the named component
from the same immutable candidate that passed container and exact-edit
checks. It passes those exact component bytes to the model and includes the
full installation policy in the combined policy identity. A changed target
therefore changes the policy hash even if the modeled contents are identical.

Only the named component is modeled; this is not a model of every package
component updater. Omitting the argument leaves report `installation=None`,
explicitly indicating no installation modeling. Existing callers remain
compatible. The combined scope stays `decoded_container_only`; the nested
model says `static_installation_model`, and hardware readiness remains
`not_established`. No report certifies runtime geometry, updater execution,
authentication or recovery.

## Validation

Ten standalone synthetic tests cover CRC exclusion, exact payload/padding
hashes, empty padding, one/multiple chunks, order and bounds, invalid types,
alignment and address overflow, malformed/overlapping protected ranges,
padding-only protection overlap and streamed padding beyond one hash chunk.
Five additional preflight integration tests cover candidate/component binding,
policy identity changes, explicit omission, unknown component/invalid policy,
capacity/protection failures and changed payload hashes.

The private install-span audit now runs combined preflight on the unchanged
verified original with a policy read from its audited initializer. Its model
agrees on 33,939,512 payload bytes, 9,314,248 padding bytes and 330 chunks,
including first erase and last program at the leading chunk. The expected
span is hashed only; no firmware image is generated. The actual native
updater still was not executed.

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -v
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-install-span-audit-private.py"
```

## Next concrete patch review

Review the existing private F-101 XPan overlay's instruction/call contracts
against the verified original and the installation mapping: hook/cave spans,
ARM/Thumb mode, displaced instructions, branch reach, registers/flags,
stack alignment and return paths. Keep bytes and concrete patch material
private and publish reviewed conclusions only. This is read-only review of
the existing experiment, not authorization to create a camera build.

The native package digest still lacks its eight-byte boot-region input.
Natural feature lifecycle and saved RAW/JPEG crop evidence remain open.
Hardware remains NO-GO. No commit, push or PR was made.
