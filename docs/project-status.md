# Project status

Updated 2026-10-16 by Codex. Read [handoff-codex.md](handoff-codex.md) for
the current integration map and next step. Older paused-lane notes are stale.

## Open work

Main carries facts through **F-106**. F-101 merged via PR #119; F-102/F-103
via PR #123; F-104 via PR #124; F-105 via PR #126. The SD-card-detect/
enumeration thread (F-102, F-104) is retired per owner direction (see
AGENTS.md's "Priority" section and handoff-codex.md). F-106 (direct test
of the capture-descriptor vs. shots-remaining-estimator hypothesis --
leans toward the estimator/property-dispatch reading at medium confidence,
with one open thread: who writes the global slot F-106 found at
`0xc18a6890`) is on `claude/f106-hypothesis-b-evidence`. The owner
approves merges; nobody merges their own PRs. Check main again before
allocating F-107.

## Feature state

An assisted simulator prototype now loads a native hook before CPU start and
makes the stock screen-layer mask follow the stored image-area choice. A real
1:1 menu pick kept the bars off over the menu, an audited live-view activation
restored them, DX and 16:9 kept them off, and ten signal cycles passed. The
instruction-space and native-execution part of build-gate condition 1 is met
in this assisted simulator setup. A broad menu-close hook was tested and
rejected because it enabled the mask on a non-live-view transition screen.
The replacement requires an empty screen stack and live-view selector 1; it
passed the same area and cycle controls and stayed off in that transition.
The exact selector-1 wrapper also passed through the stock internal type-2
dispatcher; only the natural worker caller remains unobserved.
Natural startup, a true menu return to live view and the unavailable `i`-menu
path remain unverified.

A centered 5200 by 1920 capture-geometry experiment passed, but no saved RAW
crop or NEF metadata writer is verified. The later structure-pack trace
does not close that gap. Physical AE-L/AF-L input delivery and a tracking
entry point remain unverified.

Single next step: find a stock menu-close event sequence that reaches
`0x102f57e2` without a direct diagnostic call, then confirm that the guarded
hook restores the mask.

## Decisions and limits

Personal, non-distributed build work is open; hardware remains NO-GO.
No installable firmware or installation workflow was produced. All work
this session stayed offline in static analysis and disposable simulator
processes. Original restricted inputs and the pinned simulator remain
unchanged. No firmware, raw logs, screenshots or extracted data enter Git.
The repository stays private; every change goes through owner-reviewed PRs.

The owner removed absolute hardware safety as an acceptance criterion on
2026-10-16 because it cannot be proved before the first hardware test. The
replacement gate uses three states: simulator accepted, ready for an
experimental hardware test, and hardware validated. Missing recovery must be
recorded as an accepted service-or-total-loss risk, never as proof of safety.

Written by Codex in collaboration with Claude and Tony Kim.
