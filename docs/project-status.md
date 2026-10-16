# Project status

Last updated 2026-10-15 by Codex. Update this file whenever a pull request
merges, a session starts or stops, or a decision changes.

## Where to start

Codex: [handoff-codex.md](handoff-codex.md). Claude: [handoff.md](handoff.md).

## Open pull requests

PR #34 corrects the input-ring writer claim (F-025). The current
`codex/feature-continuation-plan` branch records the owner's feature-file
takeover, resumed research and F-026. Merge #34 first, then retain both facts
and the latest Codex handoff when integrating this branch. Neither PR is
merged by Codex.

Merged: #5, #6, #13 to #26 (#13 to #16 superseded by #18, the rest landed),
and #27 to #33. Local, simulator-only firmware experimentation is allowed
in AGENTS.md. Personal, non-distributed build-phase work is open
(build-phase-gate.md); hardware access is not. A version-and-hash gate is
merged (`verified_firmware.py`).

## Sessions in flight

- Codex resumed tracking research at the owner's explicit request and, with
  separate approval, took over the guide and RAW-crop files. The assignment
  is in `.github/lanes.json`; simulator infrastructure retains its previous
  assignment. See `docs/handoff-codex.md` before resuming another session.
- Guide menu limits are established (issue #8 closed). The remaining guide
  task is a hook that needs no debugger (issue #9).

## Fact numbers

F-001 to F-024 and F-030 to F-034 are merged. F-025 is in PR #34; F-026 is on
the current continuation branch. F-027 to F-029 remain reserved for tracking.
The next free number for other work is F-035. Before adding
a fact, check main and open pull requests for the next free number.

## Owner decisions

- Every change goes through a pull request, and the owner merges. The repo
  stays private. Branch protection is unavailable on this plan.
- Build-phase work is open for the owner's own, non-distributed camera
  (build-phase-gate.md). Hardware access stays closed until the gate's
  remaining conditions are met and the owner separately approves it.
- Each session works in its own git worktree. The primary checkout stays on
  `main`.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.
