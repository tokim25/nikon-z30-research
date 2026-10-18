# Owner direction, 2026-10-17

Recorded by the Claude session manager at the owner's request.

## Latest priority: minimum justified camera test

The session manager conveyed the owner's direction to stop pursuing simulator
completeness and further low-value research. Prepare the smallest justified
modified-firmware test once essential gates are met; stop at readiness and
report the exact approval needed before the first camera action. No camera
access or flashing is authorized by this preparation request. The previous
explicit decision to keep the lifecycle gate unmet is not automatically a
waiver; report bounded evidence and residual risks for a concrete decision.

## Saved-crop question is not a blocker

The owner's direction: being unable to confirm, through static reading or the
simulator, whether the camera saves cropped RAW/JPEG files is **not a blocker**.
The saved-crop behavior may only be settled by a test on the real camera.

What this means for planning:

- Do not hold feature work waiting for a static or simulator answer to
  "does the camera save a cropped file." Treat that as an on-camera
  verification item.
- Any on-camera test still requires the owner's separate, explicit go-ahead
  at that step (see [build-phase-gate.md](build-phase-gate.md) and AGENTS.md).
  Nothing here authorizes touching the camera.
- Research that would only prove a save path statically (for example, the
  filename-getter and record-builder threads) has lower priority than
  preparing a safe, owner-approved on-camera test plan.

## Stills-only XPan scope clarification

The owner subsequently directed: "We won’t use XPan for movies. Keep it
focused on stills and keep going." A still/movie transition or exclusion
predicate is therefore not a blocker for the current stills-only simulator
candidate. Movie behavior remains unvalidated; this does not establish that
bars disable in movie mode. Continue stills area selection, live-view/menu
behavior and existing ABI checks. Hardware authorization is unchanged.

## Session-manager operating notes (from the same direction)

- Codex is the handoff recipient for simulator runs and pushing/merging work.
  Claude's strengths are static, non-simulator research.
- Commits and pushes happen only when the owner asks. Research branches
  pushed on 2026-10-17 (`claude/lane2-filename-trace-981f75`,
  `claude/lane3-family-search-2ded1d`, `claude/eloquent-napier-52e1c8`) are
  unmerged and need owner review.
- Token wrap-up trigger: stays at 90% weekly usage, per owner.

## Open items carried forward

- Codex must fix the fact-number clash (F-115 to F-120) against main before
  its uncommitted work is committed.
- Tracking (AE-L/AF-L) static search is exhausted; a live simulator check
  needs owner approval first.
- Hardware remains NO-GO.
