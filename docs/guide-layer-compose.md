# Guide layer composited by stock code (looser than the milestone)

Date: 2026-10-15. Simulator only, unchanged firmware. **This does not meet
"native drawing, no host pixel overlay."** The host debugger writes the guide
pixels into guest memory. Only the compositing is native.

## Method

A third 720 by 480 RGBA layer (0xd075f200, unused by stock code) holds two
orange bars sized for 65:24: a strip 266 rows tall, centered, so top edge 107
and bottom edge 372. A debugger-side loop calls the stock compose function
0x104787f2 once per UI cycle, with the stock descriptor's source pointer
swapped to the third layer, then restored. No instruction is changed.

## Observed

- On: bars appear one or two UI cycles later, 720 pixels wide.
- Off (compose stopped): bars gone within two cycles and stayed gone.
- On again: bars return after about three cycles.
- Outside the moving color-bar band, only the four bar rows differed from a
  control frame. The firmware hash never changed.

## Limits

- Row mapping (measured by a calibration helper over 3 runs of 36 cycles):
  screen row = 479 minus staged row, with no offset. Columns map 1 to 1. My
  earlier "one or two rows above" reading was wrong: those marks were
  symmetric about the centre, so the flip looked like a shift. A one-pixel
  colored line loses about half its color to horizontal chroma sharing, so
  use lines at least two pixels wide.
- Only live view was tested, with a 720 by 480 image area. Menus, focus
  graphics and other layouts are untested.
- The loop stands in for a per-cycle hook. It is not deployable, and it says
  nothing about the camera.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
