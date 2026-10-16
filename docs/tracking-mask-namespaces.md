# Bit 13 does not identify a physical button

Date: 2026-10-15. Read-only analysis of the verified C1.20 module.

Two fields in the copied input snapshot use bit 13. The code maps them to
different logical masks and menu events. Neither field is proven to be the
hardware SW0 word named in F-024. Matching the AE-L/AF-L mask to a test of
bit 13 is therefore insufficient to identify its button path.

| Source field in record | Normalizer | Destination field and mask | Candidate | Menu event |
| --- | --- | --- | --- | --- |
| `+0x164`, bit 13 | `0x102f0488` | `+0x18`, mask 2 | `0x1a` | `0x24f` |
| `+0x150`, bit 13 | `0x102f056e` | `+0x18`, mask 4 | `0x19` | `0x280` |

On their corresponding conditional paths, both normalizers clear the source
bit after setting the destination bit. Routine `0x102f0d14` calls them on
the fixed snapshot at `0xc200a7a0`: `0x102f056e` at `0x102f0d54`, then
`0x102f0488` at `0x102f0d5a`. Earlier calls must return for these paths to
run. The table links select candidate rows at `0x1073be48` and `0x1073be40`,
then menu-map rows 31 and 30 at `0x1073b400`.

These code/data relationships are observed statically with high confidence.
They are candidate links, not demonstrated event delivery. Later decoder
checks can suppress an output. Physical source, press/release behavior,
live-view consumption and tracking activation remain unresolved.

## Reproduce

With the owner's confirmed private WORK path and a fresh output folder:

```sh
"$WORK/analysis-env/bin/python" \
  "$WORK/codex-sw0-normalization-verify-private.py" \
  --output "$WORK/private-inputs/codex-sw0-normalization-review-03"
```

This helper verifies the original module hash, selected instruction
properties and table relationships. It does not prove complete control flow.
Two independent bounded inspections checked the surrounding branches and
snapshot call sites. Session outputs include `codex-sw0-normalization-root-01`
and `codex-agent-normalize-review-01` and `-02`, all outside Git.

No simulator controls or firmware changes were used. A search for an
AE-L/AF-L reader based only on the matching bit number has failed to identify
the physical button. The next step is to trace the producers of `+0x150`
and `+0x164` and test whether either actually represents SW0.

Written by Codex in collaboration with Tony Kim; independently checked by Codex subagents.
