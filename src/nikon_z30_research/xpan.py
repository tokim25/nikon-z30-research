"""Synthetic host simulation; no camera display or capture behavior is validated."""

import base64
from pathlib import Path
import struct
import zlib

from .geometry import Crop, centered_crop


def _integer(value: int, minimum: int, name: str) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def guide_geometry(
    width: int, height: int, left: int = 0, top: int = 0, orientation: int = 0
) -> Crop:
    """Map an oriented image's centered guide into display coordinates."""
    for value, minimum, name in ((width, 1, "width"), (height, 1, "height"),
                                 (left, 0, "left"), (top, 0, "top")):
        _integer(value, minimum, name)
    if type(orientation) is not int or orientation not in (0, 90, 180, 270):
        raise ValueError("orientation must be 0, 90, 180, or 270 degrees clockwise")
    oriented_width, oriented_height = (height, width) if orientation % 180 else (width, height)
    crop = centered_crop(oriented_width, oriented_height)
    if orientation == 0:
        bounds = (crop.left, crop.top, crop.right, crop.bottom)
    elif orientation == 90:
        bounds = (width - crop.bottom, crop.left, width - crop.top, crop.right)
    elif orientation == 180:
        bounds = (width - crop.right, height - crop.bottom, width - crop.left, height - crop.top)
    else:
        bounds = (crop.top, height - crop.right, crop.bottom, height - crop.left)
    start_x, start_y, end_x, end_y = bounds
    return Crop(left + start_x, top + start_y, left + end_x, top + end_y,
                end_x - start_x, end_y - start_y)


def synthetic_frame(width: int, height: int) -> bytes:
    """Create original RGB pixels with a gradient and checker pattern."""
    _integer(width, 1, "width")
    _integer(height, 1, "height")
    return bytes(channel for row in range(height) for column in range(width)
                 for channel in (column * 255 // max(1, width - 1),
                                 row * 255 // max(1, height - 1),
                                 80 + 100 * ((column // 32 + row // 32) % 2)))


def render_overlay(
    source: bytes, display_width: int, display_height: int,
    viewport_width: int, viewport_height: int, left: int = 0, top: int = 0,
    orientation: int = 0, enabled: bool = True,
) -> bytes:
    """Return RGB pixels, dimming only the viewport outside the guide by 75%."""
    _integer(display_width, 1, "display width")
    _integer(display_height, 1, "display height")
    if not isinstance(source, bytes) or len(source) != display_width * display_height * 3:
        raise ValueError("source must be immutable RGB bytes matching display dimensions")
    if type(enabled) is not bool:
        raise ValueError("enabled must be a boolean")
    guide = guide_geometry(viewport_width, viewport_height, left, top, orientation)
    if left + viewport_width > display_width or top + viewport_height > display_height:
        raise ValueError("viewport must fit inside the display")
    if not enabled:
        return source
    output = bytearray(source)
    for row in range(top, top + viewport_height):
        for column in range(left, left + viewport_width):
            if not (guide.left <= column < guide.right and guide.top <= row < guide.bottom):
                offset = (row * display_width + column) * 3
                output[offset:offset + 3] = bytes(channel // 4 for channel in source[offset:offset + 3])
    return bytes(output)


def _png(width: int, height: int, pixels: bytes) -> bytes:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data)))

    rows = b"".join(b"\0" + pixels[start:start + width * 3]
                    for start in range(0, len(pixels), width * 3))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def write_demo(
    output: str | Path, width: int = 650, height: int = 450,
    left: int = 24, top: int = 24, orientation: int = 0, enabled: bool = True,
) -> Crop:
    """Write synthetic HTML or PPM, refusing to overwrite any existing path."""
    destination = Path(output)
    if destination.suffix.lower() not in (".html", ".ppm"):
        raise ValueError("output extension must be .html or .ppm")
    guide = guide_geometry(width, height, left, top, orientation)
    display_width, display_height = width + 2 * left, height + 2 * top
    if display_width * display_height > 4_000_000:
        raise ValueError("demo display must not exceed 4,000,000 pixels")
    source = synthetic_frame(display_width, display_height)
    rendered = render_overlay(source, display_width, display_height, width, height,
                              left, top, orientation, enabled)
    header = ("P6\n# host simulation; no camera display hook or native capture validated\n"
              f"{display_width} {display_height}\n255\n").encode("ascii")
    content = header + rendered
    if destination.suffix.lower() == ".html":
        encoded = base64.b64encode(_png(display_width, display_height, rendered)).decode("ascii")
        state = "enabled" if enabled else "disabled"
        content = ("<!doctype html><html lang='en'><meta charset='utf-8'>"
                   "<meta name='viewport' content='width=device-width,initial-scale=1'>"
                   "<title>XPan host simulation</title>"
                   "<style>body{background:#181b20;color:#eee;font:18px system-ui;margin:32px}"
                   "img{max-width:100%;height:auto}p{max-width:75ch}</style>"
                   "<h1>XPan host simulation</h1>"
                   "<p>No camera display hook or native capture behavior has been validated.</p>"
                   f"<p>Guides {state}; orientation {orientation}° clockwise. "
                   f"Viewport {width} × {height} at ({left}, {top}). "
                   f"Guide {guide.width} × {guide.height}.</p>"
                   f"<img alt='Synthetic gradient and checkerboard with guides {state}' "
                   f"width='{display_width}' height='{display_height}' src='data:image/png;base64,{encoded}'>"
                   "</html>").encode("utf-8")
    with destination.open("xb") as stream:
        stream.write(content)
    return guide
