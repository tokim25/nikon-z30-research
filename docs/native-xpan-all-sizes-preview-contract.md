# Area-4 all-size geometry and embedded-preview contract

Codex, 2026-10-17. Static decode of the verified Z 30 C 1.20 EG plus
independent arithmetic checks. No firmware was changed and no simulator or
camera was used for this result. This is a proposed data contract, not a
candidate acceptance claim.

## Capture geometry selectors

The native builder `0x101d5b36` selects the area-4 crop dimensions through
`0x1020c07c`, margins through `0x1020c128`, and insets through `0x1020c17e`.
The crop helper's selector combines context byte `+0x20` and size byte
`+0x22`; in the normal context used by the builder, area 4 resolves to crop
record pair indices **0, 3, and 5** for large, medium, and small. The prior
assumption that medium/small were pair indices 1 and 2 was wrong: the second
selector input is the output-size byte, not a constant zero.

The exact area-4 data pointers were resolved from the initialized pointer
table at `0x12049a7c`. The candidate values below preserve the native record
layout and use the geometry formula already verified for the large case:

| Output size | Group-1 output pair | Group-3 crop pair | Group-5 margin pair | Group-6 inset pair | Candidate rectangle |
|---|---:|---:|---:|---:|---|
| Large | 0: 5200×1920 | 0: 5200×1920 | 0: (8,8) | 0: (0,0) | (8,8)–(5208,1928) |
| Medium | 1: 3900×1440 | 3: 3900×1440 | 3: (0,0) | 3: (0,0) | (0,0)–(3900,1440) |
| Small | 2: 2600×960 | 5: 2600×960 | 5: (6,6) | 5: (0,0) | (6,6)–(2606,966) |

Each output is exactly 65:24 and aligned to four pixels. The area-4 padded
readout remains 5216×1936 with origin `(192,896)` inside the 5600×3728 parent.
The large rectangle agrees with F-162. Medium and small dimensions are
derived from the same ratio at 3/4 and 1/2 scale. F-165 compares all three
through the native builder using synthetic guest records; their capture and
saved-file behavior remain untested.

## Embedded preview route

The index in capture-record field `+0x226` selects a five-slot preview-size
table; the area record at `+0x208` is a separate input. The table rows track
the native area slots: for slot 4, the small and large preview getters
`0x1020c02e` and `0x1020c038` return 480×480 and 1080×1080. Slot 4's
thumbnail entry is 120×120. The upstream area-2 experiment's 640×236 and
1920×708 targets therefore do not apply to this replacement of the 1:1 slot.

For the proposed 5200×1920 still, fitting to the stock area-4 preview widths
and rounding each height to the nearest multiple of four yields small
480×176 and large 1080×400. These are candidate dimensions only. The local
static cross-check also identifies separate direct-buffer dimensions at
`0x1157223c` and `0x11572264`, with row strides at `0x11572250` and
`0x11572278`; slot-4 strides are 960 and 2160 and should remain unchanged.
F-169 records the table values and address mapping. The fixed thumbnail path
is separate and remains unchanged.

F-168's 16-call inventory remains useful for separating generic and capture
contexts, but its “capture-size selector” wording and inherited area-2 preview
dimensions were premature. `+0x226` is an index into the five-slot
preview-size list; it is not a proven capture-size field name. The getter
callers include generic playback/display code, so patching their shared tables
globally could change old-photo behavior. See the corrected
[caller map](native-xpan-preview-callers.md).

The getters are also used outside capture, and direct pixel-buffer
constructors bypass them. For this offline candidate, the owner's still-photo
guard waiver allows a data-only edit to area-4 slot 4 in both getter and
direct-buffer tables. This intentionally affects any context selecting area
4, including possible playback/movie/warning use; those effects remain
unmeasured residual risk. Slots 0–3, row strides, thumbnail data and code
paths remain unchanged. The upstream implementation's area-2 guard and values
do not transfer to this area-4 patch.

The pinned upstream Z 30 aspect-profile investigation documents the split:
capture-only caller selection, separate preview and area fields, three direct
buffer constructors, five exact hooks, and a fixed thumbnail path. Its area-2
implementation identifies native paths but is not an area-4 patch. See
[capture preview investigation](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/aspect-playback-investigation.md)
and [aspect profile implementation](https://github.com/WonderLantern/wonder-lantern-z30/blob/f6630588810f6ecb9363bc7881fccb47e4fdb87b/src/z30_extensions/features/aspect_ui.py).

## Verification and remaining work

A fresh pinned-QEMU run executed the native builder `0x101d5b36` for baseline
and proposed area-4 large/medium/small descriptors. It used the exact verified
C 1.20 image and the pinned simulator commit, with temporary synthetic records
and repointed data-table entries in guest RAM only. The modified descriptors
returned these geometry fields:

| Size | Padded readout | Origin | Crop origin | Margins | Crop endpoint | Output size |
|---|---|---|---|---|---|---|
| Large | 5216×1936 | (192,896) | (2608,968) | (8,8) | (5208,1928) | sentinel (0,0) |
| Medium | 5216×1936 | (192,896) | (1950,720) | (0,0) | (3900,1440) | 3900×1440 |
| Small | 5216×1936 | (192,896) | (1306,486) | (6,6) | (2606,966) | 2600×960 |

The large endpoint is a bound, not a dimension: subtracting its origin
(8,8) yields 5200×1920. Baseline descriptors were captured for all three
selectors as well. All synthetic guest writes were restored; the original
firmware SHA-256 and simulator checkout commit/status were unchanged. This
validates native descriptor construction for the proposed table values only.
It does not exercise capture, preview buffers, lifecycle, menu labels, parser
acceptance, artifact integrity or camera behavior. Private raw results remain
outside the repository.

The exact private candidate now includes the four area-4 table edits and has
passed an independent byte-level preflight against the verified original.
F-170 synthetically exercised the native constructors with the same preview
dimensions, but did not test the resulting candidate through camera startup.
Offset `0x24` remains preserved byte-for-byte. The owner keeps lifecycle
condition 1 unmet; the candidate is not hardware-ready.
