"""Integer pixel geometry only; no images or camera settings are modified."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Crop:
    left: int
    top: int
    right: int
    bottom: int
    width: int
    height: int


def centered_crop(width: int, height: int) -> Crop:
    """Largest exact 65:24 integer crop, with exclusive right/bottom bounds.

    Dimensions are multiples of 65 and 24. Odd spare pixels go to the
    right/bottom, placing the center at most half a pixel off the source center.
    This may trim both axes to preserve the exact ratio without resampling.
    """
    if type(width) is not int or type(height) is not int or min(width, height) <= 0:
        raise ValueError("source dimensions must be positive integers")
    scale = min(width // 65, height // 24)
    if scale == 0:
        raise ValueError("source is too small for an exact 65:24 integer crop")
    crop_width, crop_height = 65 * scale, 24 * scale
    left, top = (width - crop_width) // 2, (height - crop_height) // 2
    return Crop(left, top, left + crop_width, top + crop_height, crop_width, crop_height)
