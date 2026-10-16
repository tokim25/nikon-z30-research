# Project status

Updated 2026-10-15. Codex stopped research at the owner's remaining-usage
cutoff and saved its final handoff for Claude. No agents continue working.
Start with [handoff-codex.md](handoff-codex.md) on this branch, then review
the pending PRs. Older paused-lane instructions are superseded by the owner's
explicit resumption and approved guide/RAW file transfer.

PRs #34 to #40 are open, covering F-025 to F-029, F-035 and F-036.
The current `codex/final-claude-handoff` branch adds F-037, the simulator
RAW-model source audit, and the final cross-track handoff.

All start from main `32a9da5`. Merge #34 through #40, then this branch,
retaining all facts and using this final handoff when resolving conflicts.
The owner merges; Codex never merges its own PRs or pushes main.
PR #35 records the exact ownership transfer and matching test changes.
Simulator infrastructure retains its previous assignment.

The native geometry A/B/A experiment succeeded twice with centered 5200 by
1920 geometry. This is not a saved RAW crop. Physical AE-L/AF-L mapping,
tracking activation, debugger-free guides, failure containment and recovery
remain unresolved. Personal build work is open; hardware readiness is NO-GO.

Single next step: inspect independent input-cache setter calls at
`0x103a3e88` and `0x103a400c`. The handoff preserves separate guide and
RAW leads, reproduction scripts, private run names and failed hypotheses.

All publication branches passed 54 local tests and artifact checks. Check
latest CI heads on GitHub. Original inputs and simulator checkout are clean.
F-025 to F-037 are allocated; check main/open PRs before using F-038.

Written by Codex in collaboration with Tony Kim; continues Claude's status notes.
