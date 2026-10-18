# Exact 5200 by 1920 geometry contract

2026-10-17. F-162. Read-only original-code analysis and reinspection of
existing private probe reports; no new simulator run, firmware image,
instruction encoding or hardware access. Scope is area 4, large size,
normal mode-0 context, kind 0 as used by the recorded probes. This is not
a complete all-sizes XPan patch contract or saved-file acceptance.

## Result: endpoints were mistaken for dimensions

The native descriptor rectangle is `(left, top, right, bottom)`.
`(8, 8, 5208, 1928)` has width **5200** and height **1920**. Its ratio is
exactly 65:24. There is no eight-pixel oversize to fix by changing the
right/bottom coordinates or declaring 5208 by 1928 the output resolution.

The earlier [geometry probe](xpan-capture-geometry-probe.md) already reports
this correctly. Later [partial offset-map notes](xpan-5200x1920-offset-map.md)
misread the endpoint pair as dimensions and tested different table groups.

## Descriptor and table mapping

Native builder `0x101d5b36` writes fourteen 16-bit fields. For the scoped
large-size case, the traced lookups and their initialized mappings are:

| Descriptor offset | Meaning | Native source |
| --- | --- | --- |
| `+0x00/+0x02` | Parent extent | Group 0, area 0, through `0x1020bfc8` |
| `+0x04/+0x06` | Selected padded area extent | Group 2, area 4, first pair at `0x115a4e14`, through `0x1020c05c` |
| `+0x08/+0x0a` | Area origin in parent | Pair at `0x115a4d5c`, through `0x1020c072` |
| `+0x0c/+0x0e` | Rectangle center in selected area | Computed from the three inputs below |
| `+0x10/+0x12` | Rectangle left/top | Computed margin plus inset |
| `+0x14/+0x16` | Rectangle right/bottom | Computed left/top plus effective width/height |
| `+0x18/+0x1a` | Additional size fields | Zero in the scoped large-size path; other sizes use a separate output-size lookup |

The arithmetic inputs are **group 3** dimensions, **group 5** margin and
**group 6** inset. For area 4 and large size their first pairs are at
`0x115a4e80`, `0x115a4f10` and `0x115a4f88`, respectively. Helpers
`0x1020c07c`, `0x1020c128` and `0x1020c17e` select them. The RAM pointer
base `0xc18c7de8` maps back to original ROM pointer table `0x12049a7c`;
the table is initialized data, not an unrelated direct-ROM table.

The relevant helper offsets from that pointer base are `+0x3c`, `+0x64`
and `+0x78`, confirming groups 3, 5 and 6. The size selectors jointly
choose a pair within each group's record. Large/large uses pair zero.
Medium/small variants must not be inferred by treating all records as
identical arrays of L/M/S dimensions.

For positive effective sizes, the arithmetic at `0x101d5be0..0x101d5c24` is:

```text
width  = dimension_x - 2 * inset_x
height = dimension_y - 2 * inset_y
left   = margin_x + inset_x
top    = margin_y + inset_y
right  = left + width
bottom = top + height
center = (left + floor(width/2), top + floor(height/2))
```

Group 0 area 4 (pointer index 4) and group 2 area 4 (index 14) are **not**
the rectangle-dimension input to this arithmetic. Index 14 supplies the
area header; index 19 supplies group 3 dimensions. Changing only indices
4 and 14, including their 36 joint single-pair combinations, therefore
does not test the actual large rectangle-dimension source. Earlier probes
that did produce the target also repointed index 19.

The separate output-size list at `0x115a4dd8` (group 1, area 4, index 9)
is not the dimension input used in the builder's large rectangle calculation.
Changing it alone cannot change that rectangle. Its required consistency
with other output consumers is a separate build check, not proof the list
is unnecessary or that saved JPEG dimensions are established.

## Concrete scoped output

The existing five-pair sensitivity experiment supplies a coherent large
case with parent 5600 by 3728, padded area 5216 by 1936, origin `(192,896)`,
rectangle center `(2608,968)` and local bounds `(8,8,5208,1928)`.
Its parent-coordinate bounds are `(200,904,5400,2824)`, exactly centered
and 5200 by 1920. The routine reads the area origin; it does not derive
that origin from dimensions. Keep that distinction in any edit contract.

This five-pair experiment is a sufficient checked set, not a minimal
complete firmware manifest. Do not reinterpret its six-short scratch records
as twelve-short in-place records, write across neighboring objects, or
promote one large-size result to medium/small/preview acceptance. Concrete
firmware-derived manifests remain outside Git.

## Verification and limit

The private geometry helper evaluates the actual original arithmetic
instructions with supplied inputs,
after verifying identities, lookup-call landmarks and initializer/table
mapping. It matches the stock DX/16:9/1:1 large cases and the target, and
256 deterministic synthetic cases match the independently written formula.
It does not execute the complete builder/control flow in a fresh guest.

Both original full-builder probe reports are present and agree with the
target bounds. Their restored-state, unchanged-control-area, original-file
and clean-simulator assertions pass. Private report identities:

- `codex-agent-raw-geometry-probe-02`:
  `5a17d7961000520a8f5872b63b8a79f914177b9e7664127bdc33413965615b4d`
- `codex-root-geometry-probe-01`:
  `44a53b3e538da20c8d505383940bc5fd83ce180b8fd3fe48cd618d789cdb938b`

New helper SHA-256:
`998803ed7d32ab79149b5d7915448ebc92e36e4a1d501d0bb638715e797818c3`.
Metadata result SHA-256:
`69b4740156dad29f25e82e81ef5eee235f7d661cea931c72b6f0445f71e9e111`.
These temporary private files are not a durable evidence archive. No raw
descriptor bytes, original tables or installable patch is published here.

Geometry evaluation needs no digest input, so that dependency did not block
this result. F-198/F-199 later incorporated the verified geometry tables into
the complete private candidate and passed exact edit, length, CRC and layout
checks. This does not establish Nikon updater acceptance, natural lifecycle
behavior or saved RAW/JPEG correctness; those remain outside this scoped
geometry result. Lifecycle condition 1 remains unmet and hardware stays
NO-GO.
