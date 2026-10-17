# Project status

Updated 2026-10-16 by Codex. Read [handoff-codex.md](handoff-codex.md) for
the current integration map and next step. Older paused-lane notes are stale.

## Open work

Main carries facts through **F-113**. F-101 merged via PR #119; F-102/F-103
via PR #123; F-104 via PR #124; F-105 via PR #126; F-106 via PR #127;
F-107 via PR #128; F-108 via PR #129; F-110 via PR #138; F-111 via PR
#139; F-112 via PR #140. The SD-card-
detect/enumeration thread (F-102, F-104) is retired per owner direction
(see AGENTS.md's "Priority" section and handoff-codex.md). Lane 1's
mode-state chain is resolved through F-108; F-109 closes the one
remaining thread (who posts the live-view trigger event) as a
deliberately-dropped simulator-reachability question, not a real-
firmware gap.

**Owner call, pending review:** the owner has called build-gate condition
1 satisfied for Lane 1 (see hardware-readiness.md's new section for the
exact evidence and the one ambiguity it rests on). **This does not
authorize any build-phase work yet** -- a dissenting review from Codex,
run as its own independent session, is required first and must be
recorded in hardware-readiness.md before proceeding; not yet done. F-109
is on `claude/f109-event-origin-deadend`; the condition-1 call and
dissenting-review requirement are on `claude/condition1-owner-call`.

**Lane 2's capture-descriptor question is accepted as settled toward the
settings/property-dispatch reading (F-106) -- meaning the real save-crop
mechanism remains unfound, not merely unverified.**
`hardware-readiness.md`'s "RAW crop"/"RAW output path" rows were stale
(citing only PR #37/#47) and understated this; corrected via PR #137.
F-110 opened a fresh angle (the firmware's actual file-naming system).
F-111's property module was dropped on direct check (no image-area
reference). F-112 found the real geometry table family, confirmed via
image-area property `0x501`'s readers. **F-113 decoded the crop-window
builder's own body for the first time** (`0x101d5b36`, central to this
research since F-057, but never previously read internally) -- it calls
at least six sibling tables from F-112's family to build real
width/height pairs plus a centered-offset computation, the genuine
shape of crop-rectangle construction. This substantially deepens
understanding of the tool, but does not resolve F-097/F-106's
capture-vs-estimator ambiguity: the builder is shared by all seven
known callers, and nothing yet says which one reaches an actual save
versus a preview (Lane 1's live-view work is exactly such a non-save
context). This remains the single biggest open research gap for Build
1, with several concrete next steps named in handoff-codex.md rather
than an open-ended search.

The owner approves merges; nobody merges their own PRs. Check main again
before allocating F-114.

**Lane 3 (AE-L/AF-L tracking) now has a proper section in handoff-codex.md
for the first time**, with a concrete handoff point: a real event-code
cluster (`0x2006`/`0x2020`/`0x2021`/`0x2087`, near tracking's own `0x2083`)
was found and is the strongest lead so far, but property `0x2021`'s
consumer could not be found by exhaustive literal-comparison search (zero
hits, full image). Two untried next steps (live simulator breakpoint on
the post primitive, or a masked/family-level static search) are named in
handoff-codex.md's new Lane 3 section and in `docs/tracking-input-chain.md`.
This is on `claude/tracking-handoff-property-2021`.

## Feature state

An assisted simulator prototype now loads a native hook before CPU start and
makes the stock screen-layer mask follow the stored image-area choice. A real
1:1 menu pick kept the bars off over the menu, an audited live-view activation
restored them, DX and 16:9 kept them off, and ten signal cycles passed. The
instruction-space and native-execution part of build-gate condition 1 is met
in this assisted simulator setup. A broad menu-close hook was tested and
rejected because it enabled the mask on a non-live-view transition screen.
The replacement requires an empty screen stack and live-view selector 1; it
passed the same area and cycle controls and stayed off in that transition.
The exact selector-1 wrapper also passed through the stock internal type-2
dispatcher; only the natural worker caller remains unobserved.
Natural startup, a true menu return to live view and the unavailable `i`-menu
path remain unverified.

A centered 5200 by 1920 capture-geometry experiment passed, but no saved RAW
crop or NEF metadata writer is verified. The later structure-pack trace
does not close that gap. Physical AE-L/AF-L input delivery and a tracking
entry point remain unverified.

Single next step: find a stock menu-close event sequence that reaches
`0x102f57e2` without a direct diagnostic call, then confirm that the guarded
hook restores the mask.

## Decisions and limits

Personal, non-distributed build work is open; hardware remains NO-GO.
No installable firmware or installation workflow was produced. All work
this session stayed offline in static analysis and disposable simulator
processes. Original restricted inputs and the pinned simulator remain
unchanged. No firmware, raw logs, screenshots or extracted data enter Git.
The repository stays private; every change goes through owner-reviewed PRs.

The owner removed absolute hardware safety as an acceptance criterion on
2026-10-16 because it cannot be proved before the first hardware test. The
replacement gate uses three states: simulator accepted, ready for an
experimental hardware test, and hardware validated. Missing recovery must be
recorded as an accepted service-or-total-loss risk, never as proof of safety.

Written by Codex in collaboration with Claude and Tony Kim.
