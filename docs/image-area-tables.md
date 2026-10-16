# Where the firmware keeps image-area sizes

Date: 2026-10-15. Static reading of the unmodified image. Addresses are
landmarks. Sizes are Nikon's published numbers. Which setting drives which
record is inference unless marked observed.

## Why this matters

The owner is fine with an XPan crop replacing an existing crop option such as
1:1. If the firmware picks its image size from data, a replacement is a data
question before it is a code question.

## Table A: sizes by aspect ratio

Near 0x10750650, in the code region, sits a run of width and height pairs. For
each size class (large, medium, small) it lists several aspect ratios,
including 3:2, 4:3, 5:4, 1:1 and 16:9. Five literals in code around
0x10596c9c to 0x10598640 point into it, so code reads it directly.

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

## Open

The code that reads these records, and what each group drives (live view,
capture, thumbnails), is not traced yet. Saved-file sizes may depend on
several records.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
