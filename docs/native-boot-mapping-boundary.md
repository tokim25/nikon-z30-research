# Boot mapping boundary and updater relocation

2026-10-17. F-141. Read-only static follow-up to
[native-updater-digest-inputs.md](native-updater-digest-inputs.md).
No firmware image or extracted table was written, and no camera was accessed.

## Result

The checked startup mappings do not recover the digest's eight-byte input.
The virtual address `0x10000088` maps to physical `0x10000088` in the
startup page table, below the verified EG's base `0x10020000`. No startup
scatter copy or clear destination covers it. This establishes a precise
missing-input boundary in the inspected evidence, not that all possible
runtime mappings or external boot sources have been ruled out.

The same audit resolves the formerly unmapped updater handoff: its RAM code
comes from the verified EG. That opens a concrete static path toward the
actual installation operations while the digest input remains unresolved.

## Startup table evidence

The reset path loads a translation-table base of `0x10030000` at
`0x1002bcf0` and writes it to TTBR0. The entry for the digest address is at
`0x10030400`: an ordinary section descriptor, with the supersection bit clear,
mapping that section to physical base `0x10000000`. Therefore this startup
table provides no alias from the digest input into the captured EG module.

The compiler scatter loader at `0x10020038` computes table bounds
`0x10034000` through `0x10034120` (end exclusive). Its 18 descriptors select
three copies and fifteen zero fills. The handlers at `0x1002006c` and
`0x10020088` were decoded in Thumb mode to identify those operations.
None of their destination intervals includes `0x10000088`.

The pinned simulator explicitly reports its boot ROM as missing and loads
the verified main module at `0x10020000`. Its unmodeled address region is
not a source of verified camera bytes. This simulator fact only bounds the
available evidence; no simulator-fidelity experiment was started.

Later page-table changes, bank switching, another boot image or a separate
device memory source are not ruled out by this startup-only audit. No value
was substituted from the same offset in EG or from an unmodeled read.

## Updater code mapped back to verified bytes

| Item | Verified mapping |
| --- | --- |
| Scatter descriptor | `0x10034010` |
| ROM copy source | `0x12079f00` |
| RAM destination | `0xc2b10000` |
| Copy length | 4,016 bytes (`0xfb0`) |
| Main updater trampoline | ARM entry `0x1017e370`, target `0xc2b10cd5` |
| Target instruction mode | Thumb, instruction address `0xc2b10cd4` |
| Target source in ROM mapping | `0x1207abd4` |
| Target offset in verified EG file | `0x0205abd4` |

The copy handler implements an ordinary copy, so this relocation requires
no decompression assumption. The mapped entry decodes coherently and begins
by preparing state; it is not itself proof of a flash program operation.
The caller continues through `0x1011a028` and other handoff/status helpers.
Erase/program addresses, destination layout, readback and recovery remain open.

## Reproduction and current next step

The newly written private helper checks the original identities and existing
updater audit, then the startup table, exact scatter bounds/handler kinds,
digest-address noncoverage and updater source/target mapping. It emits only
addresses, lengths and booleans. Neither the helper nor its restricted input
is copied into this repository.

```sh
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-boot-mapping-audit-private.py"
```

The check passed with 18 scatter records, three copy records, no digest-input
destination coverage and one unambiguous updater relocation. The existing
unchanged round trip and decoded preflight are rerun by the helper and pass.

Do not repeat the same literal/offset searches for the missing digest bytes
without new evidence. Single next step: trace the relocated `0xfb0`-byte
updater block, together with its handoff through `0x1011a028`, to identify
the actual erase/program boundary and which main-module bytes it installs.
This can proceed using the verified original without the missing boot input.

Follow-up F-142 traces that worker and its initialized span; see
[native-install-span.md](native-install-span.md). It identifies erase/program
and readback code statically, with no physical execution. The current next
step is modeling the full installation span in preflight.

The native digest check remains unreproduced. Hardware remains NO-GO.
Original inputs and recovered tools are unchanged; no commit, push or PR.
