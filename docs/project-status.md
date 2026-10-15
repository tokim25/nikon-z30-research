# Project status

Last updated 2026-10-15 by Claude. Update this file whenever a pull request
merges, a session starts or stops, or a decision changes.

## Where to start

Codex: [handoff-codex.md](handoff-codex.md). Claude: [handoff.md](handoff.md).

## Open pull requests, in merge order

1. #18 rolls up Codex's four tracking branches (#13 to #16). Merge it first,
   then close #13 to #16 as superseded.
2. #17 adds the thread-aware call helper. Merge after #18. It touches
   facts.md near the same lines, so rebase it first.

## Sessions in flight

- Claude, simulator: issue #8 (guides in menu states). Branches `claude/*`.
- Claude, tracking: read-only static research for issue #10, continuing the
  next step in the Codex handoff. Findings go to facts.md and the notes in
  the Codex handoff.
- Codex: stalled on token limits. Resumes from its handoff file.

## Fact numbers

F-013 is taken by #17. F-014 to F-019 are reserved for the Claude tracking
research. Other sessions start at F-020. Before adding a fact, check main and
open pull requests for the next free number.

## Owner decisions

- Every change goes through a pull request, and the owner merges. The repo
  stays private. Branch protection is unavailable on this plan.
- The build phase is closed. Research stays offline and in the simulator.
- Each session works in its own git worktree. The primary checkout stays on
  `main`.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
