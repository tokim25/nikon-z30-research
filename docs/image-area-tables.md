# Where the firmware keeps image-area sizes

Date: 2026-10-15. Static reading of the unmodified image. Addresses are
landmarks. Sizes are Nikon's published numbers. Which setting drives which
record is inference unless marked observed.

## Why this matters

The owner is fine with an XPan crop replacing an existing crop option such as
1:1. If the firmware picks its image size from data, a replacement is a data
question before it is a code question.

## Table A: the Retouch Trim editor's sizes

Correction from a helper's trace: Table A (0x10750658 to 0x1075080f) belongs to
the in-camera Retouch Trim crop tool, not to capture or live view. It holds 110
width and height pairs indexed by orientation, source group, and five aspects
(3:2, 4:3, 5:4, 1:1, 16:9). Each entry is the largest crop of that aspect that
fits the source, rounded down to multiples of 16. Source groups are the
1:1, 16:9 and DX areas at three sizes, plus 4K and full-HD movie frames.

A data-only 65:24 swap would not work here. A function at 0x10597440 hard-codes
the five ratios and forces width equal to height for the 1:1 slot, the aspect
labels are 5-byte slots, and the aspect and group counts are compile-time
bounds.

## Table B: per-area records

A 38-entry pointer table at 0x12049a7c points to small records near
0x115a4d6c to 0x115a4fc8:

- Output sizes per area, large, medium and small: DX, 16:9 and 1:1 (the 1:1
  record holds 3712, 2784 and 1856 squared).
- Slightly padded sensor-readout sizes for the same three areas (for 1:1,
  3728 squared).
- Large-size copies, then thumbnail and preview sizes.

This table sits in the initialized-data region, so code reaches it through a
RAM copy, not a direct literal.

## What Table B drives

A helper traced the readers (cluster 0x1020bfc8 to 0x1020c1de, main consumer
0x101d5b36). The records feed capture and readout geometry, output sizes,
alignment margins, thumbnails and movie sizes. The 1:1 slot is area 4, so
indices 4, 9, 14, 19, 24, 29 and 34.

They do not feed live view. The live-view dimensions at render-object offsets
0x320 and 0x324 are the display surface size, not the image size, which
corrects an earlier note. The image size comes from a separate object set from
a live-view frame-size table at 0x1073db04. No path from the records to that
chain was found (moderate confidence: 58 callers were not all traced).

## Open

How live view shows the 1:1 area is still unknown, and so is how capture turns
these records into saved files.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
