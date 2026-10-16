# Codex handoff

Resumed 2026-10-16 at the owner's request. Continue until either account
window reaches 8% remaining, then publish the final handoff. Initial remaining
usage: 100% five-hour, 54% weekly. All 54 baseline tests and both artifact
checks pass. No new hardware authorization was given.

## Current work

Dedicated worktree: `work/codex-tracking-resume`. Branch:
`codex/xpan-border-color-state`, from main `32a9da5`.
The primary checkout remains on main. PRs #34 through #41 are still open;
there is no newer merged research. The previous final handoff is in
[PR #41](https://github.com/tokim25/nikon-z30-research/pull/41).
Retain all pending facts and reports when integrating, and never merge our
own PRs or push main.

Three private research tasks are active: physical input sources outside the
numeric-command handler; geometry request consumers toward NEF output; and
persistent guide drawing before composition. Root is checking stock shooting
screen initialization because the assisted live-view fixture's screen stack
was empty. These are research tasks, not verified interfaces.

Reserved new facts: F-038 input, F-039 RAW, F-040 guides, F-041 root screen
research. Check main and open PRs before publication or assigning more.

## Single next step

F-040 records a persistent native border-color setting, independently repeated;
see [the evidence](xpan-border-color-state.md). Next: establish matching clip
geometry and whether stock border commands survive composition. A data-only
guest experiment is in progress; no visible guides are claimed yet.

## Limits and private inputs

The owner approved the guide/native and RAW-crop document takeover; PR #35
records file patterns and tests. Simulator infrastructure retains its previous
assignment. Personal build work is open, but physical camera access is closed.
Hardware readiness remains NO-GO. Original firmware instructions and files
stay unchanged; no patch builder or installation workflow is used.

Confirmed WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Existing inputs/helpers are immutable. New private scripts and outputs use
codex prefixes outside Git. Disable bytecode writes for simulator imports,
use separate debugger ports and absolute private output paths, and check the
original hash and clean pinned simulator. No bytes, logs, dumps, screenshots
or extracted listings enter Git.

Prior strongest result: native geometry A/B/A produced centered 5200 by 1920
geometry twice, with unchanged controls and exact restoration. Saved RAW
cropping, physical AE-L/AF-L tracking, debugger-free guide drawing and recovery
remain unresolved. The optional functional ISP is not a validated NEF pipeline.

Written by Codex in collaboration with Tony Kim; continues Claude's research and the previous Codex handoff.
