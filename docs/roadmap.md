# Research roadmap

Updated 2026-10-16. The goal is XPan framing in live view and saved RAW
files, plus the camera's own subject tracking from one AE-L/AF-L press.
All results so far come from offline analysis and a simulator. No actual
camera was connected or changed.

## Live-view framing

The earlier guide-line experiment works through native drawing calls.
The new result in PR #43 uses stock border drawing after one diagnostic
clip flag and native geometry/color setup. It keeps black masks on screen
as the preview refreshes without repeated debugger drawing calls.

The calibrated result leaves a 720 by 266 visible strip, rounded to 65:24.
Two independent runs pass. Two later on/off cycles also restore the
baseline when disabled. However, PR #48 shows that the mask remains when
the menu opens and can cover menu graphics. The following live-view entry
call did not prove a natural menu exit.

Next: trace the native clip-state lifecycle, then test menu cleanup and a
verified return to live view. Natural startup, focus graphics and reboot
remain open. This is not yet an automatic camera feature.

## Saved RAW crop

PR #37 proves that temporary guest data can produce centered 5200 by 1920
capture geometry, an exact 65:24 rectangle. It does not prove that the
camera captures or saves that rectangle.

PR #47 traces selected geometry-like fields into a packed structure and
processing submission. The source object's identity and a NEF writer remain
unverified. Reviewed TIFF-like constants were unrelated error/UI values.

Next in this trail: establish the source object and the actual save boundary,
then obtain simulator evidence of saved-image behavior. Do not infer a RAW
crop from a masked preview or a geometry return value.

## One-button tracking

The named hardware switch and several input paths are known. New queued
input work traces a selected bank containing logical ID 41 and mask 0x2000.
Matching that mask to the named AE-L/AF-L switch does not prove they refer
to the same physical event.

Next in this trail: trace the queued-event producer to its source and
press/release handling. A tracking entry point, visible reticle transition,
cancellation and rejection in unsupported modes are still unverified.

## Integration and readiness

The single next session task is the native clip-state lifecycle above.
The other trails can resume in separate agreed lanes. No combined feature
test or installable firmware is available. Hardware remains NO-GO.

The owner resumed tracking and approved Codex taking over guide/native and
RAW-crop documents; older pause notes are stale. PRs #34 through #48 hold
the pending findings. Use [the current handoff](handoff-codex.md) for their
integration order, private repros and exact limits, and
[the readiness checkpoint](hardware-readiness.md) for remaining gates.

Written by Codex in collaboration with Tony Kim; updates Claude's roadmap with verified simulator progress and unfinished work.
