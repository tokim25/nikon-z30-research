# Project status

Owner direction: [owner-direction-2026-10-17.md](owner-direction-2026-10-17.md).
The saved-crop question is an on-camera test item, not a blocker for feature
work. Hardware remains NO-GO.
Patch work is governed by [patch-readiness-checklist.md](patch-readiness-checklist.md);
do not begin another patch loop until its required inputs are explicit.

Updated 2026-10-17 by Codex. Read [handoff-codex.md](handoff-codex.md) for
the current integration map and next step. Older paused-lane notes are stale.

## Open work

**New, 2026-10-17, for Codex — PR #167: consolidated firmware static map.**
[firmware-map-2026-10-17.md](firmware-map-2026-10-17.md) is an
addresses-and-descriptions map of C 1.20 for all five user-story areas
(buttons, menus, live-view, crop, AE-L/AF-L tracking), with call chains and
confidence. New since prior notes: the screen fan-out driver 0x10595844 behind
the bars, the image-area function table at 0x11f9a4dc behind crop, and the
AE-L/AF-L queued-input router (callback + handler table at 0x1037a2c4, task-init
entry 0x1059c2c8). The three largest open leads (crop-table dispatcher, bars
fan-out entry, router input writer) all need an address-building (MOVW/MOVT or
base-register) index pass that was not done. No firmware bytes in the doc;
extracted components stay outside the repo. Owner reviews/merges PR #167.

**New, 2026-10-17, for Codex — action-half correction (one-button tracking).**
The old "tracking candidate" cluster (0x11cf4e90/0x11cf5774/matcher 0x11cf5248)
is **Bluetooth HCI**, not AF tracking (strings "Tracking BtPacket", "Tracking
HCI Rx Buffer"); ruled out. Real on-camera tracking is the **AF-area-mode
subsystem**: label table 0x103edda0 (PINPOINT…3D-TRACKING…AUTO-AREA), label
routine 0x103edc2e, settings near 0x11c9b.. (AfAreaMode*, AfTrackingSensitivity);
3D-TRACKING is the tracking mode. Button behavior is set by
eDSID_Setting_FuncAeAfLockButtonShooting. These are reached via MOVW/computed
addresses, so **Codex** must: (1) resolve the AF-area-mode set function from
0x103edda0/0x103edc2e, and (2) resolve the FuncAeAfLockButtonShooting
option→action dispatch (does an option engage 3D-TRACKING / AF-ON-with-track).
Detection hook is already confirmed (ID-41 / SW word 0x115c694c). See
[firmware-map-deep-2026-10-17.md](firmware-map-deep-2026-10-17.md).

**New, 2026-10-17, for Codex — deep cross-reference companion.**
[firmware-map-deep-2026-10-17.md](firmware-map-deep-2026-10-17.md) adds the
static branch/literal/pointer cross-reference results (confirmed call chains;
the bars screen fan-out driver 0x10595844; the crop function table 0x11f9a4dc;
the AE-L/AF-L queued-input router) and the complete named hardware-switch table
at 0x1072e3b0 — three registers SW0/SW1/SW2, with AE-L/AF-L = SW0 bit 0x2000
and the "i" button = SW1 bit 0x400. **Codex must own the MOVW/MOVT (or
base-register) address-building index pass**: the Claude lane is blocked from
it by a safety classifier, and the three largest leads (crop dispatcher at
0x11f9a4dc, bars fan-out entry 0x10595844, AE-L/AF-L SW-register writer) all
dead-end on addresses that only that pass resolves. Prose only, no firmware
bytes.

**New, 2026-10-17, owner-requested handoff to Codex: Lane 0** (see
handoff-codex.md's new "Lane 0" section). The dormant-worker pattern that
blocks both Lane 1's and Lane 3's natural-trigger questions (F-019,
F-109, F-115 through F-117) is handed off as its own thread rather than
re-attempted per-lane. Likely needs the QEMU machine model
(`z30-qemu/qemu/nikon-z30.c`), not just Python scripts -- a better fit for
Codex regardless of the owner's specific ask. Explicitly: resolving this
does not by itself authorize or reach hardware install; that still needs
the owner's separate written risk acceptance (hardware-readiness.md) and
conditions 2 through 4.

**F-120 found this firmware genuinely contains ARM-mode code** (a real
`memcpy` routine at two separate linked addresses, plus compiler-runtime-
shaped helpers), confirmed via live code decode -- something every prior
static scan in this project assumed away. Does not show any of the
project's specific "zero callers" dead ends (`0x10459d80`, Lane 3's
property dispatch) live there; flagged as a cheaper thing to check before
touching QEMU's C source if Lane 0's steps 1-2 come back empty.

Local F-135 on `codex/firmware-preflight-plan`: recovered package verifier
audited; unchanged in-memory decode/re-encode reproduced the original exactly.
See [native-package-verifier-audit.md](native-package-verifier-audit.md).
No modified firmware image was written. Local F-136 implements the decoded
container reader with synthetic rejection tests; all three original components
also passed with their hashes pinned. See
[native-container-validator.md](native-container-validator.md).
Local F-137 implements exact-edit manifest comparison with synthetic and
combined CRC/edit checks; the unchanged package baseline passes with zero
changed bytes. See [native-exact-edit-audit.md](native-exact-edit-audit.md).
Local F-138 combines those checks in one decoded-container preflight, tested
with synthetic modified containers and the unchanged original baseline.
See [native-combined-preflight.md](native-combined-preflight.md).
Local F-139 identifies native body-package parsing, confirms decoder-mask
and CRC-table equivalence, and finds an additional 20-byte digest check
not covered by our preflight. EG installation reaches a relocated target;
physical flash writes remain unverified. See
[native-updater-validation.md](native-updater-validation.md).
Local F-140 traces the encoded-format flag through parser/cache/selection;
the original statically predicts the extra-digest branch after record restore.
Expected digest/message/suffix boundaries are traced, but an eight-byte source
at `0x10000088` remains unmapped. See
[native-updater-digest-inputs.md](native-updater-digest-inputs.md).
Local F-141 finds no digest-input mapping in the startup page table or 18
scatter records. It maps the updater RAM block to verified EG source bytes;
see [native-boot-mapping-boundary.md](native-boot-mapping-boundary.md).
Local F-142 identifies native erase/program/readback paths and the initialized
43,253,760-byte EG target, including 9,314,248 bytes of tail padding. No
native update was executed. See [native-install-span.md](native-install-span.md).
Local F-143 adds the read-only installation model to preflight; synthetic
tests and the unchanged audited original baseline pass. See
[native-installation-model.md](native-installation-model.md).
Local F-144 reviews both existing private overlay revisions. Mapped layout
checks pass, but both retain a four-byte stack displacement at the state
wrapper's stock-service call; condition 3 remains unmet. See
[native-xpan-contract-review.md](native-xpan-contract-review.md).
Local F-145 adds a supplied-boundary contract checker and synthetic operation
tests. The abstract restored-frame tail transfer passes; existing real
overlay code is not approved. See [native-call-contract-tests.md](native-call-contract-tests.md).
Local F-146 checks textual instruction forms and layout: the corrected state
wrapper plus adjacent writer uses 48 of 52 bytes. Writer entry/hook must move;
no final overlay encoding or execution was checked. See
[native-xpan-layout-proposal.md](native-xpan-layout-proposal.md).
Local F-147 runs that correction in paired pinned-QEMU fixtures. Measured
service-entry stack/register preservation passes; the other-state return
changes NZCV and still fails the strict contract. Writer relocation/frame
checks pass within diagnostic scope. See
[native-xpan-abi-experiment.md](native-xpan-abi-experiment.md).
Local F-148 resolves the measured flag mismatch in a new private overlay:
both strict state cases pass with entry flags additionally required; writer
frame/results/CPSR match the baseline. Scratch writer LR still differs;
saved return target/mode match. See
[native-xpan-flags-remediation.md](native-xpan-flags-remediation.md).
Local F-149 restarts saved-crop research with initialized RAM mappings for
F-110's two filename-pointer tables, cross-checked after stock assisted
startup. Nearby references are found; actual filename-field consumption and
save creation remain unproved. See
[native-save-table-ram-mapping.md](native-save-table-ram-mapping.md).
Next: trace actual filename-pointer loads from those RAM mappings toward
serialization/file creation. Full lifecycle and global code review remain open.
Camera-side acceptance remains unverified.

Main carries facts through **F-114**. F-101 merged via PR #119; F-102/F-103
via PR #123; F-104 via PR #124; F-105 via PR #126; F-106 via PR #127;
F-107 via PR #128; F-108 via PR #129; F-110 via PR #138; F-111 via PR
#139; F-112 via PR #140; F-113 via PR #141. The SD-card-
detect/enumeration thread (F-102, F-104) is retired per owner direction
(see AGENTS.md's "Priority" section and handoff-codex.md). Lane 1's
mode-state chain is resolved through F-108; F-109 closes the one
remaining thread (who posts the live-view trigger event) as a
deliberately-dropped simulator-reachability question, not a real-
firmware gap.

**Owner call, dissenting review recorded, audit fix-and-retest done
(F-115):** the owner called build-gate condition 1 satisfied for Lane 1;
the required dissenting review (PR #144) disagreed as worded, and a
separate instruction-level audit (PR #145) found three things to fix.
F-115 fixes two of the three in a private generator copy, re-runs every
simulator control against the rebuilt overlay (all pass), and re-attempts
the dissenting review's cheapest natural-path remediation option against
the fixed overlay, reaching the guard and mask for the first time outside
a diagnostic call (see hardware-readiness.md's new follow-up section).
**Condition 1's status is unchanged** -- still not satisfied as worded;
the owner's call is still pending on that review, and this pass does not
claim to resolve it.

**Lane 2's capture-descriptor question is accepted as settled toward the
settings/property-dispatch reading (F-106) -- meaning the real save-crop
mechanism remains unfound, not merely unverified.**
`hardware-readiness.md`'s "RAW crop"/"RAW output path" rows were stale
(citing only PR #37/#47) and understated this; corrected via PR #137.
F-110 opened a fresh angle (the firmware's actual file-naming system).
F-111's property module was dropped on direct check (no image-area
reference). F-112 found the real geometry table family, confirmed via
image-area property `0x501`'s readers. **F-113 decoded the crop-window
builder's own body for the first time** (`0x101d5b36`). **F-114
completes the picture**: the centering arithmetic resolves to an
unambiguous crop-rectangle descriptor (top-left corner, bottom-right
corner, their center, final output size), and the gate function is
trivial. A response-safety-classifier stop blocked checking which of
the builder's seven callers reaches a real save -- dropped, not
retried; F-095/F-096 already characterized all seven and that read is
unchanged (none confirmed as a save path, the most-traced one leaning
away from it). This remains the single biggest open research gap for
Build 1. **F-118 did the live-simulator-read step for the geometry math
itself**: re-running F-078's existing script confirms F-114's center-is-
midpoint claim against real execution across all 15 tested combinations
(not a sample), and fully explains the final-output-size field's `(0,0)`
pattern as a consistent "no resize" sentinel. **F-119 then read F-112's
RAM-resident width/height table directly** (real values, cross-matching
three of F-118's outputs exactly) but found the table's own indexing
doesn't match the builder's (quality,area) byte values the simple way --
flagged, not solved, for whoever maps the remaining sibling tables next.
The caller/save-path question is unchanged by either -- still the actual
remaining gap, and still not re-attempted after its classifier stop.

The owner approves merges; nobody merges their own PRs. Check main again
before allocating F-135.

**Lane 3 (AE-L/AF-L tracking) now has a proper section in handoff-codex.md
for the first time**, with a concrete handoff point: a real event-code
cluster (`0x2006`/`0x2020`/`0x2021`/`0x2087`, near tracking's own `0x2083`)
was found and is the strongest lead so far, but property `0x2021`'s
consumer could not be found by exhaustive literal-comparison search (zero
hits, full image). Two untried next steps (live simulator breakpoint on
the post primitive, or a masked/family-level static search) are named in
handoff-codex.md's new Lane 3 section and in `docs/tracking-input-chain.md`.
This is on `claude/tracking-handoff-property-2021`.

**F-116/F-117 exhausted the cheap options on property `0x2021`'s
consumer, all negative.** Four static masking idioms tried (`lsr #8`,
`and #0xff00`, `ubfx`: clean negatives; `tbb`/`tbh`: 2,817 sites, too
many to review, only a narrow index-shape ruled out). The live-simulator
breakpoint option (F-117) is the most informative: `0x10475ecc` was never
called at all during an idle wait plus a real menu-activation and eight
real key-dispatch calls -- a dormant-worker-shaped negative (F-018/F-019
pattern), not a hit on any id. **No consumer found by any method tried.**
What's left is slow (hand-reading `tbb`/`tbh` tables) or hits the same
unsolved problem as other lanes (keeping a background task alive in the
simulator long enough for a real post).

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
does not close that gap; settle it with the separately authorized on-camera
test when appropriate, not as a prerequisite for feature work. Physical
AE-L/AF-L input delivery and a tracking entry point remain unverified.

The immediate F-147 flag defect is resolved by F-148. Active priority:
F-149 is the final static filename-table trace: no concrete route to the
filename getter or save path remains, so this static thread is dropped. The
actual crop question is reserved for the separately authorized on-camera test
and is not a blocker.
Retired simulator event-poster searches are not the default next step.

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
