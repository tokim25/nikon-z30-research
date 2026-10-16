# Project status

Last updated 2026-10-15 by Claude. Update this file whenever a pull request
merges, a session starts or stops, or a decision changes.

## Where to start

Codex: [handoff-codex.md](handoff-codex.md). Claude: [handoff.md](handoff.md).

## Open pull requests, in merge order

1. #20 (F-021 and the AE-L/AF-L goal) then #24 (F-023, F-024), stacked on it.
   Both are tracking research, waiting for the owner's review.
2. #25 (image-area research, F-030 to F-033) is independent.
3. #26 is this status hub.

Merged: #17, #18, #19, #21, #22 and #23. #13 to #16 are superseded by #18.
Local, simulator-only firmware experimentation is now allowed in AGENTS.md.

## Sessions in flight

- Claude, simulator: issue #8 (guides in menu states) and the guide docs,
  owned by one session. Branches `claude/*`.
- Claude, tracking and button mapping: paused by the owner. #20 and #24 stand
  as they are. Do not resume without the owner's say-so.
- Codex: stalled on token limits. Resumes from its handoff file.

## Fact numbers

F-001 to F-024 are used, and F-030 to F-033 belong to the image-area
research (#25). F-025 to F-029 are reserved for the tracking lane. The next
free number after that is F-034. Before adding a fact, check main and open
pull requests for the next free number.

## Owner decisions

- Every change goes through a pull request, and the owner merges. The repo
  stays private. Branch protection is unavailable on this plan.
- The build phase is closed. Research stays offline and in the simulator.
- Each session works in its own git worktree. The primary checkout stays on
  `main`.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
