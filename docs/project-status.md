# Project status

Last updated 2026-10-15 by Claude. Update this file whenever a pull request
merges, a session starts or stops, or a decision changes.

## Where to start

Codex: [handoff-codex.md](handoff-codex.md). Claude: [handoff.md](handoff.md).

## Open pull requests

None, as of the last update to this file.

Merged: #5, #6, #13 to #26 (#13 to #16 superseded by #18, the rest landed),
and #29 to #32. Local, simulator-only firmware experimentation is allowed
in AGENTS.md. Personal, non-distributed build-phase work is open
(build-phase-gate.md); hardware access is not. A version-and-hash gate is
merged (`verified_firmware.py`).

## Sessions in flight

- Claude, simulator: issue #8 (guides in menu states) and the guide docs,
  owned by one session. Branches `claude/*`.
- Claude, tracking and button mapping: paused by the owner. The research so
  far is merged (#20, #24); do not resume it without the owner's say-so.
- Codex: stalled on token limits. Resumes from its handoff file.

## Fact numbers

F-001 to F-024 and F-030 to F-034 are used. F-025 to F-029 are reserved for
the tracking lane, which the owner has paused; do not use them without the
owner's say-so. The next free number for other work is F-035. Before adding
a fact, check main and open pull requests for the next free number.

## Owner decisions

- Every change goes through a pull request, and the owner merges. The repo
  stays private. Branch protection is unavailable on this plan.
- Build-phase work is open for the owner's own, non-distributed camera
  (build-phase-gate.md). Hardware access stays closed until the gate's
  remaining conditions are met and the owner separately approves it.
- Each session works in its own git worktree. The primary checkout stays on
  `main`.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
