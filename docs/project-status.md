# Project status

Updated 2026-10-15 by Codex. Start with [handoff-codex.md](handoff-codex.md).
The owner has resumed tracking research and approved Codex taking over
guide and RAW-crop files. Personal build work is open; hardware access is not.

## Integration order

- [PR #34](https://github.com/tokim25/nikon-z30-research/pull/34): F-025,
  correction to the input-ring writer claim.
- [PR #35](https://github.com/tokim25/nikon-z30-research/pull/35): F-026,
  distinct bit-13 record fields; approved ownership transfer and feature plan.
- Current branch `codex/tracking-input-source`: F-027, structured-control
  path into an input cache, with physical meaning still unverified.

All three start from main `32a9da5`. Merge in that order, retaining all
facts and the latest handoff when resolving conflicts. PRs #34 and #35 have
passed CI. They are unmerged as of this update; Codex never merges its PRs.

## Sessions and ownership

Codex is working in `work/codex-tracking-resume`. The primary checkout stays
on main. Tracking and button research is resumed by the owner's request.
The user also approved transfer of guide/native documents and the image-area
and capture-geometry reports. PR #35 records the exact lane patterns and
updates their tests. Simulator infrastructure retains its previous assignment.
Agree ownership before concurrent edits.

## Fact numbers

F-001 to F-024 and F-030 to F-034 are merged. F-025 is allocated in PR #34,
F-026 in PR #35, and F-027 on this branch. F-028 and F-029 remain reserved
for tracking. The next free number for other work is F-035; check main and
open PRs before using it.

## Next step and readiness

Identify the sender and meaning of the structured records consumed near
`0x1008ad26`. A matching bit number alone does not identify AE-L/AF-L.

Guide drawing works with a debugger in simulated live view. A hook without
the debugger, saved RAW crop behavior, tracking activation and recovery
evidence remain missing. Hardware readiness stays NO-GO. The research pause
described in older readiness text is lifted; its unmet technical gates remain.

Written by Codex in collaboration with Tony Kim; continues Claude's project status.
