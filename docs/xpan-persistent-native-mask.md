# Persistent native crop masking after diagnostic setup

Date: 2026-10-16. Two calibrated simulator A/B/A runs, unchanged firmware.

Stock drawing produced 107-row opaque black bars at the top and bottom of
the 720 by 480 synthetic preview, leaving rows 107 through 372 visible.
That centered 266-row strip is the rounded 65:24 framing target. No host
guide pixels or per-frame rectangle calls were used.

The mask appeared during a two-second autonomous run, before any explicit
refresh, then survived three stock refreshes. Restoring the original state
removed it. In both runs, differences outside the animated preview band
were exactly the 214 masked rows; the restored control had zero changed
rows outside that band. The mask hides UI graphics outside the center too.

## Setup and observed drawing

The native property getter confirmed mode 1, category 1, bank 0 and the
existing property at `0xc1d87838`. Native geometry setter `0x104b7976`
received synthetic bounds (-1, 106, 721, 374), with matching readback.
Native color setter `0x104540ee` supplied retained opaque black.

One explicit diagnostic write enabled the existing property's flag at
`+0x2c`. This is a limit of the result: the inspected flag-setting API
`0x104b79cc` only accepts mode 2, category 0, so it was not a valid setter
for this active property. No new object or firmware instruction was written.

After setup, stock code submitted only the expected top/bottom rectangles
through `0x10477af2` before composition. It did so automatically across the
observed refreshes; the old per-cycle guide injector and queue-gate override
were not used. Each run restored the original flag, bounds and color state.
The original module hash and clean pinned simulator were unchanged.

The first geometry hypothesis failed: bounds (0, 107, 720, 373) left only
264 center rows and unwanted one-pixel side borders. The calibrated bounds
removed the side borders and recovered the 266-row target.

Confidence is high for the measured native drawing and restoration in this
fixture. Natural startup, menus, focus-overlay behavior, repeated toggling,
reboot persistence, saved RAW output and hardware remain untested. This is
persistent stock drawing after diagnostic setup, not an installable hook.

## Reproduce privately

Use confirmed WORK and a fresh directory:

```sh
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex-guide-clip-mask-private.py" --bounds -1 106 721 374 \
  --output "$WORK/private-inputs/codex-native-mask-reproduce-01"
```

Calibrated runs: `codex-guide-clip-mask-02` and independent
`codex-root-clip-mask-20261016-01`. Static contract repeat:
`codex-root-clip-contract-20261016-01`, using
`codex-guide-clip-contract-verify-private.py`. Detailed pixels, logs and
memory stay private. The helper restores data and closes its simulator.

Next: find the native enable/startup ownership for the current mode, then
test menus, overlays, toggling and cleanup. Initializer `0x104b5fd4` is an
unverified lead because it also initializes rendering surfaces; do not call
it as a clip-only setter.

Written by Codex in collaboration with Tony Kim; calibrated drawing independently repeated by Codex agents.
