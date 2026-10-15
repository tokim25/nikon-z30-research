# XPan-style host simulation

This fresh offline prototype uses original synthetic RGB frames. No camera display
hook or native capture behavior has been validated. It does not load firmware,
access hardware, or change saved JPEG/NEF dimensions or metadata.

## Coordinates and rounding

Display coordinates start at the upper-left; x increases right and y down. The
viewport's `left` and `top` locate its origin within the display. Rectangles use
inclusive left/top and exclusive right/bottom bounds. Geometry is independent of
rendering, returned by `guide_geometry`.

Orientation is clockwise rotation from oriented image coordinates into the
display viewport. At 90/270 degrees the oriented width and height are swapped
before fitting. The 65:24 ratio is always horizontal in oriented image coordinates;
its display rectangle is vertical at 90/270 degrees. A portrait viewport at zero
degrees still receives a horizontal guide, with larger top/bottom margins.

The crop is the largest **exact integer** 65:24 rectangle: scale is
`min(oriented_width // 65, oriented_height // 24)`, with dimensions `65*scale`
and `24*scale`. Ratio error is zero. This deliberately trims both dimensions when
necessary instead of rounding a fractional height. Margins use floor division;
an odd extra pixel goes right/bottom in oriented coordinates, then rotates with
the rectangle. Opposite margins differ by at most one pixel, so the center moves
at most half a pixel along either axis. A 1300x900 viewport gives 1300x480 with
210-pixel vertical margins; 1600x480 gives 1300x480 with 150-pixel horizontal margins.

Dimensions must be positive integers; offsets must be nonnegative integers.
Booleans, floats (including NaN/infinity), strings, unsupported rotations and
out-of-display viewports are rejected. An oriented viewport smaller than 65x24
is rejected even when guides are disabled. No approximate-ratio fallback is used.

## Preview

Run from the project root, with Python 3.10+ and no third-party runtime packages:

```sh
PYTHONPATH=src python3 -m nikon_z30_research xpan-demo ../xpan-preview.html --width 1300 --height 900 --left 24 --top 32 --orientation 0
PYTHONPATH=src python3 -m nikon_z30_research xpan-demo ../xpan-disabled.html --width 1300 --height 900 --left 24 --top 32 --orientation 0 --no-guides
```

Generated previews belong outside this repository; these commands write to its
parent outputs directory. Do not track generated HTML, SVG, or image files or change
the artifact allowlist. HTML embeds a standard-library-generated PNG, works offline,
and visibly labels the image “host simulation”. A `.ppm` suffix instead writes
binary RGB PPM (P6) with the same label in its comment. CLI JSON also carries the
label. Use a new output path:
existing files are never overwritten; parent directories must exist. Demo displays
are limited to 4,000,000 pixels. Display size is viewport size plus twice each
origin offset, producing symmetric outer margins.

The source is a deterministic gradient/checker pattern. Enabled guides dim pixels
outside the crop but inside the viewport to `channel // 4`. Pixels within the guide
and outside the viewport are unchanged. Disabled guides return identical source
pixels. Rendering accepts immutable RGB bytes and produces a separate result;
orientation maps the guide, while the synthetic display background stays fixed.
This demonstrates overlay placement, not camera image rotation.

## Validation

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

Tests cover both specified viewport examples, explicit rotation mappings, offsets,
portrait and odd dimensions, exact ratio and centering, malformed/too-small inputs,
every rendered pixel for all four orientations, source nonmutation, disabled
identity, CLI PPM payloads, output labels, and overwrite protection. Tests use only
synthetic fixtures and temporary output paths; no network or Nikon files are needed.

Actual result on 2026-10-15: all 24 tests passed (8 XPan, 6 research scaffold,
10 tracking tests). The preview command produced the expected 1300x480 guide at
display bounds (24, 242)–(1324, 722), inside the offset 1300x900 viewport.
