# Model 65:24 XPan-style live-view framing offline

## Problem and scope

Provide a deterministic composition-guide prototype using synthetic frames. Nikon's [image-area documentation](https://onlinemanual.nikonimglib.com/z30/en/09-03-05.html) does not document a 65:24 still-image area. This issue specifies a display-only model; native capture requires separate research. The ratio is a project choice, not a claimed Nikon mode.

## Proposed behavior

Fit a centered 65:24 guide inside the active image viewport, respecting its offset within a larger display. Return geometry separately from rendering. Define orientation relative to the oriented image coordinates. Reject invalid inputs explicitly. An optional mask must not alter the source frame; disabling the guide restores the unmodified presentation.

## Offline acceptance criteria

- [ ] Document the coordinate convention, 65:24 ratio, portrait behavior, rounding, and one-pixel centering tolerance.
- [ ] For a 1300 × 900 viewport, assert a 1300 × 480 guide with top and bottom margins of 210 pixels.
- [ ] For a 1600 × 480 viewport, assert a 1300 × 480 guide with left and right margins of 150 pixels.
- [ ] Test nonzero viewport origins, odd dimensions, portrait dimensions, and 90/180/270-degree orientation mappings. Every guide stays within its active viewport, with ratio error bounded by the declared one-pixel rounding rule.
- [ ] Test zero, negative, non-finite, and malformed dimensions; reject them without emitting invalid rectangles. Document a policy for viewports too small to represent the ratio.
- [ ] Use original synthetic frames to demonstrate enabled/disabled guides; verify the source image remains identical and rendering touches no pixels outside the viewport.
- [ ] Record a reproducible offline test command and actual results. Tests require neither network access nor Nikon files.
- [ ] Label the demo “host simulation”; explicitly state that no camera display hook or native capture behavior has been validated.

## Exclusions and completion evidence

No firmware loading, modification, extracted bytes, patches, SD deployment, or hardware access. No changes to saved JPEG/NEF dimensions or metadata. Attach original geometry code, synthetic examples, test results, and limitations. Do not represent this as recovered milestone code or as a working camera feature.
