# Project status

Updated 2026-10-16 by Codex. Read [handoff-codex.md](handoff-codex.md) for
the current integration map and next step. Older paused-lane notes are stale.

## Open work

PRs [#34 through #48](https://github.com/tokim25/nikon-z30-research/pulls)
are open and had successful checks on their published heads when reviewed.
They share main base `32a9da5`; preserve every appended fact and report when
resolving conflicts. This session's final handoff branch is
`codex/session-handoff-20261016`. The owner approves merges; Codex merges none.

The owner resumed tracking and approved Codex taking over guide/native and
RAW-crop documents. PR #35 records the ownership metadata change. Simulator
infrastructure remains in Claude's lane. No Codex agents continue working.
A new explicit session may resume from the handoff.

F-001 through F-052 are allocated on main. F-053 is next,
subject to checking new changes before use.

## Feature state

Persistent stock native black masks now work after diagnostic simulator
setup, with independent repeats and two toggle cycles. They remain over
audited menu entry and can cover menu graphics. Natural startup and a clean
return from menus remain unverified.

A centered 5200 by 1920 capture-geometry experiment passed, but no saved RAW
crop or NEF metadata writer is verified. The later structure-pack trace
does not close that gap. Physical AE-L/AF-L input delivery and a tracking
entry point remain unverified.

Single next step: audit native clip-state lifecycle and callers of
`0x104b5fd4` before testing automatic menu cleanup and live-view restoration.

## Decisions and limits

Personal, non-distributed build work is open; hardware remains NO-GO.
No installable firmware or installation workflow was produced. All work
this session stayed offline in static analysis and disposable simulator
processes. Original restricted inputs and the pinned simulator remain
unchanged. No firmware, raw logs, screenshots or extracted data enter Git.
The repository stays private; every change goes through owner-reviewed PRs.

Written by Codex in collaboration with Tony Kim; replaces stale session status with the verified publication state.
