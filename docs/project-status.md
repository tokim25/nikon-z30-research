# Project status

Last updated 2026-10-15 by Claude. Update this file whenever a pull request
merges, a session starts or stops, or a decision changes.

## Where to start

Codex: [handoff-codex.md](handoff-codex.md). Claude: [handoff.md](handoff.md).

## Open pull requests, in merge order

1. The tracking research record (F-014 to F-019) is in review. Merge it
   before any Codex pull request that edits facts.md.

Merged on 2026-10-15: #17 (thread-aware call helper) and #18 (Codex tracking
rollup). Pull requests #13 to #16 are superseded by #18 and can be closed.

## Sessions in flight

- Claude, simulator: issue #8 (guides in menu states). Branches `claude/*`.
- Claude, tracking: read-only static research for issue #10, continuing the
  next step in the Codex handoff. Findings go to facts.md and the notes in
  the Codex handoff.
- Codex: stalled on token limits. Resumes from its handoff file.

## Fact numbers

F-013 was taken by #17 and F-014 to F-019 by the tracking research record.
F-020 and F-021 are reserved for two Claude studies still running. Other
sessions start at F-022. Before adding a fact, check main and open pull
requests for the next free number.

## Owner decisions

- Every change goes through a pull request, and the owner merges. The repo
  stays private. Branch protection is unavailable on this plan.
- The build phase is closed. Research stays offline and in the simulator.
- Each session works in its own git worktree. The primary checkout stays on
  `main`.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
