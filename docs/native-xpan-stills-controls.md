# Stills-only XPan controls

2026-10-17. F-156. The owner removed movie-transition/predicate evidence as
a prerequisite for the current stills-only candidate. Movie behavior stays
unvalidated. This scope change does not alter ABI checks or hardware gates.

The tests reuse the exact F-148 private overlay, with no new encoding:
manifest SHA-256
`5a933892e98effb0ba114adc1ad0e3a4be40daf2cac021df73e8bc1661ef37c9`.
All file hashes matched loaded simulator memory. The original firmware and
pinned simulator checkout remained unchanged. No camera was accessed.

## Rendering and repeated setting controls

The existing assisted startup and original image-area callbacks were used.
These are controlled diagnostic inputs, not proof of the physical quick-menu
or a natural menu-return path. Frames come from the actual simulated drawing
buffer with the existing deterministic preview fixture.

| Selection | Observed mask | Full-width black rows |
| --- | --- | ---: |
| 1:1 as XPan | On | 214 |
| DX | Off | 0 |
| 1:1 again | On | 214 |
| 16:9 | Off | 0 |

Target black rows are 0–106 and 373–479, leaving rows 107–372 visible in the
720-by-480 frame. Outside the previously identified animation band, target
frame changes are confined to those 214 rows. DX and 16:9 controls match the
baseline outside that band. This is not a claim of physical-camera sharpness
or smoothness, nor a comparison of every animation pixel.

Ten additional target/DX setting cycles passed. Bounds and screen-stack count
remained unchanged. The final DX selection leaves mask flag zero and stack
count zero. This establishes controlled setting updates and disable cleanup;
it does not establish native menu-transition or power-cycle acceptance.

## Native menu confirmation remains unresolved

Two fresh candidate processes reached the real image-area list but their
confirm operations did not return within the bounded diagnostic call.
Both left the observed mask off; the cycle test was not reached in either.
One fresh unmodified-firmware control completed the same scripted menu pick.

This is insufficient to establish the cause or an intermittent-failure rate.
It does mean candidate menu acceptance cannot be claimed or its failures
simply dismissed as an unavoidable simulator limitation. No further retries
were performed. The successful callback/rendering controls do not substitute
for the failed menu control.

## Private evidence and next step

All frames, captures and scripts remain under private WORK. Evidence:
`codex-xpan-stills-control-01`/`02`, `codex-xpan-stills-stock-menu-01`, and
`codex-xpan-stills-pixels-01`. The new `codex-xpan-stills-control-private.py`
and `codex-xpan-stills-pixels-private.py` run the bounded controls; the stock
menu control uses the existing runner with an empty loader manifest.

Next bounded step: compare stock and candidate at the menu-confirmation
writer/state boundaries to isolate the observed candidate hang before
accepting native menu return. Keep this on the stills path; movie eligibility
is not a prerequisite. Hardware remains NO-GO. No commit, push or PR.
