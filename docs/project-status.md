# Project status

Updated 2026-10-16 by Codex. Read [handoff-codex.md](handoff-codex.md) for
the current integration map and next step. Older paused-lane notes are stale.

## Open work

Main carries facts through **F-109**. F-101 merged via PR #119; F-102/F-103
via PR #123; F-104 via PR #124; F-105 via PR #126; F-106 via PR #127;
F-107 via PR #128; F-108 via PR #129. The SD-card-detect/enumeration
thread (F-102, F-104) is retired per owner direction (see AGENTS.md's
"Priority" section and handoff-codex.md). Lane 2's capture-descriptor
question is accepted as settled toward the settings/property-dispatch
reading (F-106). Lane 1's mode-state chain is resolved through F-108;
F-109 closes the one remaining thread (who posts the live-view trigger
event) as a deliberately-dropped simulator-reachability question, not a
real-firmware gap.

**Owner call, pending review:** the owner has called build-gate condition
1 satisfied for Lane 1 (see hardware-readiness.md's new section for the
exact evidence and the one ambiguity it rests on). **This does not
authorize any build-phase work yet** -- a dissenting review from Codex,
run as its own independent session, is required first and must be
recorded in hardware-readiness.md before proceeding. F-109 is on
`claude/f109-event-origin-deadend`; the condition-1 call and dissenting-
review requirement are on `claude/condition1-owner-call`. The owner
approves
merges; nobody merges their own PRs. Check main again before allocating
F-110.

**Lane 3 continuation, local on `codex/tracking-property-dispatch`:**
the table-based property consumer and subscriber were resolved. The old
dispatcher map was corrected, two bounded menu probes completed without
reaching the cluster, and diagnostic provenance identified BLE camera-
controller/authentication modules. The original non-Bluetooth attribution
is withdrawn. This cluster is retired as evidence for physical AE-L/AF-L
delivery. It supplies no verified tracking entry point. See the updated
Lane 3 handoff and tracking-input-chain.md's final sections.

The owner's Protect-button clue produced a separate static route:
indexed button/function labels link playback assignment `0x1186` to the
Protect action; the shooting assignment `0x1184` and snapshot bit 13
reach a selector consumed by the live-view type-3 handler. Details are in
tracking-protect-button.md. The continuation establishes explicit press
edges and shows the AF-ON branch instead tests a held level. It also finds
native Subject tracking assignment 77 and real request/state routines.
AE-L/AF-L's assignment handler omits that case, and the shared tracking
helper rejects its logical input. A menu-only change is insufficient.
The native status bridge and numerical start/stop/exclusion gates are now
traced. A bounded QEMU run of 32 synthetic stock-decoder calls returned
the held logical id on both press and hold; tracking routines were never
called. A second run queued three records through the stock writer and
verified FIFO consumption and the matching edge before/after the worker's
decoder call. The candidate boundary has the same record and output,
but an adapter is not implemented or approved. Next: trace AE-L/AF-L's
actual assignment-menu options and document the coordinated menu/action/
edge-gate changes, preserving native checks and completion cleanup.
No tracking activation tested. Details and limits are in the report's
final dated section.
Claude pickup: [tracking-claude-handoff.md](tracking-claude-handoff.md).

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
does not close that gap. Native tracking request candidates are statically
identified; physical AE-L/AF-L delivery and runtime tracking activation
remain unverified.

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
