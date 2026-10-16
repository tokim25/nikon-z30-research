# Capture geometry per image area: simulator baseline

Date: 2026-10-15. Simulator only, unchanged firmware (hash checked before and
after). The stock function 0x101d5b36 was called natively. Its inputs are a
settings context (area byte at +0, size class at +0x22, mode at +0x26) and a
pointer to a 0x1c-byte output. It only computes.

## Results at the large size

- 16:9: area 5600 by 3144, crop origin (0, 292), image rectangle out to 5584
  by 3136.
- 1:1: area 3728 by 3728, origin (936, 0), margins 8 and 8, rectangle out to
  3720 by 3720.
- DX is the full 5600 by 3728 readout with origin (0, 0).

The origin is half the difference between readout and area. Medium and small
outputs match Nikon's published sizes (1:1 gives 2784 and 1856 squared).

## What this shows

Each area's geometry comes from per-area records, with no ratio arithmetic in
this function. That fits the data-driven reading in
[image-area-tables.md](image-area-tables.md).

## Test not run

A planned test would copy the firmware to a private throwaway file, change the
1:1 rows to a 65:24 shape, and compare this output. PR #21 permits that, but
the permission classifier blocked creating the copy, so the owner must approve
it. It was not run. The edit list stays out of the repo.

## Limits

The simulator has no image processor, so this cannot show whether the real
camera accepts a new crop window.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
