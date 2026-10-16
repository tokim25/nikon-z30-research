# Native masks toggle, but remain over menus

Date: 2026-10-16. Offline, assisted simulator startup; F-044.

The persistent mask setup from PR #43 passed two on/off cycles. Each on
produced black rows 0 through 106 and 373 through 479, leaving 266 visible
rows. Each off restored baseline pixels outside the animated band at rows
160 through 319. This tests a diagnostic flag toggle followed by the known
refresh call, not a camera button or a complete feature.

The setup uses property `0xc1d87838`, bounds (-1, 106, 721, 374), retained
opaque black through `0x104540ee`, and a temporary guest-data write to the
property's flag at `+0x2c`. No per-cycle rectangle calls are needed.

With the mask left on, audited entry `0x102355ee(menu_object, 1)` completed.
The screen stack grew from zero to two entries and the menu object's selector
at `+0x74` changed from 4 to 1. The same 214 black rows remained, with bank
zero, the same property, bounds, flag and color. This setup does not clear
the mask for menus and can cover menu graphics.

Calling the known live-view object's entry also completed. Both selectors
were then 1 and the stack still had two entries. The mask remained through
another refresh. That is not evidence of a natural menu exit or a clean
mode transition. Focus graphics, reboot and natural startup remain untested.

Observed runtime results, high confidence within this fixture. The helper
restores the original owned flag, bounds and global color fields before
discarding the process. Original firmware and pinned simulator remain
unchanged. No saved RAW file, firmware instruction change or hardware was used.

Private repro with confirmed WORK and a fresh output directory:

```sh
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex-guide-mask-reliability-private.py" \
  --output "$WORK/private-inputs/codex-guide-mask-reliability-reproduce-01"
```

Agent run: `codex-guide-mask-reliability-01`; independent root repeat:
`codex-root-mask-reliability-20261016-01`. The root reviewed the helper's
owned-field cleanup and confirmed the exact measured row sets.

Next: establish the native clip-state lifecycle so menu entry clears the
mask and returning to live view restores it through an audited route.

Written by Codex in collaboration with Tony Kim; simulator experiment independently repeated by Codex and a Codex agent.
