# Codex handoff

Updated 2026-10-15. The owner resumed research and approved Codex taking over
guide and RAW-crop files. Continue offline work toward 65:24 live-view framing,
a matching saved RAW crop, and AE-L/AF-L tracking. Personal build work is open;
camera access is not. The owner asked this session to stop when remaining
account usage reaches 8% and publish a handoff for Claude.

## Published work and integration

Main baseline: `32a9da5`. Dedicated worktree: `work/codex-tracking-resume`;
the primary checkout stays on main. PRs #34, #35 and #36 are open and have
passed CI. Merge in order, retaining every appended fact and the latest handoff:

- #34: F-025 corrects the input ring's single-writer claim.
- #35: F-026 distinguishes bit-13 fields, records the user-approved guide/RAW
  file transfer, and sets separate feature acceptance requirements.
- #36: F-027 traces a structured-control path into an input cache; its physical
  meaning remains unverified.

Each new finding also starts from main. Ledger and handoff edits can conflict;
retain all facts and use the latest handoff when integrating. Codex never
merges its own PRs or pushes main.

## Current branch and single next step

Branch: `codex/xpan-geometry-data-probe`, from main. F-036 and
[xpan-capture-geometry-probe.md](xpan-capture-geometry-probe.md) record the
completed geometry comparison. Next: follow the native descriptor consumers
into NEF metadata and storage writes; do not infer saved RAW success.

## New results in progress

A native geometry A/B/A test ran twice: temporary data changes in a disposable
guest produced a centered 5200 by 1920 rectangle, exactly 65:24. DX and 16:9
controls stayed unchanged; restoring the data restored all baseline outputs.
No original firmware file or instruction was changed. This is geometry
evidence, not proof of saved RAW output.

Other bounded results are being documented separately: compose completion
callback timing, empty screen stack in the assisted live-view fixture, and
the simulator's optional functional ISP limits. Do not assume a physical
button mapping from a matching bit number.

## Private inputs and reproducibility

Confirmed WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Keep existing inputs and helpers unchanged. New private helpers and run
folders use `codex_` or `codex-` prefixes outside Git. No firmware content,
raw logs, screenshots or extracted listings may enter any repository surface.
Do not search the disk for more firmware.

Use the report's private helper with a fresh output folder under
`$WORK/private-inputs/`. Runtime imports disable bytecode writes. Simulator
sessions use separate local debugger ports and absolute private output paths.
The original module hash and pinned simulator revision are checked; the
simulator checkout must stay clean. No patch builder or hardware is used.

## Ownership and readiness

The owner transferred guide/native documents and image-area/capture-geometry
reports to Codex; PR #35 records the exact file patterns and matching tests.
Simulator infrastructure retains its previous assignment. Claude should
agree ownership before concurrent edits, then read the latest report and
handoff rather than resuming older paused-lane instructions.

Guides still require a debugger hook. The physical input-to-tracking path,
saved RAW behavior and recovery evidence remain unresolved. The simulator
has an optional functional ISP with unverified layout assumptions; there is
no validated saved-RAW pipeline. Hardware readiness stays NO-GO.

Baseline tests: 54 passing. Restricted outputs remain private; reproduction
commands and semantic results are the published evidence.

Written by Codex in collaboration with Tony Kim; continues Claude's research and includes independent Codex subagent checks.
