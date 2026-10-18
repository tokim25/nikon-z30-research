# Stills lifecycle acceptance decision

Historical decision record: main's later session-manager-brief.md and
test-readiness-2026-10-17.md record an explicit owner lifecycle waiver.
The earlier retain-unmet decision below remains historical evidence, not the
current owner disposition. Coverage remains unproved; no hardware approval.

Owner decision, 2026-10-17: **keep the lifecycle gate unmet**. The owner
selected that option explicitly. No coverage deviation was accepted.
Subsequent narrow read-only identity/version authorization does not change
this decision or authorize modified-firmware testing.

2026-10-17. This record consolidates existing evidence after the owner asked
to proceed with the stills workflow. No new simulator run was performed:
the required input routes are missing or were already tested without a
verified live-view return. Repeating those controls would not add acceptance
evidence. The candidate remains unchanged.

## Exact candidate and scope

Existing F-148 private overlay, twelve individually hashed entries. Manifest
SHA-256:
`5a933892e98effb0ba114adc1ad0e3a4be40daf2cac021df73e8bc1661ef37c9`.
The manifest and every referenced file hash were rechecked read-only for
this record. This identifies a diagnostic overlay, not an installable
camera package. The stored 1:1 choice is the XPan stand-in.

The scope is stills. Movie behavior is unvalidated and is not a prerequisite
for this prototype under the owner's later direction. Saved RAW/JPEG crop
remains an on-camera verification item, not a simulator blocker. No camera
access is authorized by this record.

## Workflow evidence

| Required observation | Current evidence | Acceptance |
| --- | --- | --- |
| Select XPan and show bars | F-156 native setting callback; 214 full-width black rows | Pass for assisted callback input |
| Open menu and remove bars | Earlier screen activation/signal controls clear the mask; candidate confirmation observations keep it off with menu stack count 3 | Pass for checked assisted controls |
| Return through the native menu path and restore bars | GUI Back leaves the last screen open; earlier internal close events target another mode; other tested events leave the last entry open | Not established |
| Select DX and remove bars | F-156 callback controls and ten cycles; F-160 ready/phase-3 calls | Pass for checked diagnostic inputs |
| Keep playback unobstructed | No validated playback input route in the reviewed harness/evidence | Not established |
| Keep warnings unobstructed | No validated warning trigger and lifecycle in the reviewed harness/evidence | Not established |
| Natural startup with stored XPan choice | Existing runs use assisted startup and diagnostic setting/activation calls | Not established |

The exposed GUI supplies only navigation, OK and Back. Internal events are
not identified physical buttons. Earlier evidence directories
`codex-menu-exit-24f-01`, `codex-menu-exit-251-01`,
`codex-menu-exit-252-01` retain one final stack entry. Events tested in
`codex-menu-exit-24e-01` and `codex-menu-exit-250-01` remove it but do not
establish the required live-view return. Those are historical stock controls,
not fresh acceptance runs on F-148. No arbitrary mode value or event was
used to manufacture playback, a warning or a successful return here.

F-157/F-158 also leave confirmation completion mixed. Finer-stepped
completion and diagnostic live activation are not substituted for the
missing lifecycle. F-159's flash-response explanation thread remains closed.

## What has already been checked

F-148 supplies bounded state/writer stack, register, return and flag evidence.
F-160 adds four paired close/live-ready cases and reviews the named native
continuations' use of volatile outputs. These checks do not establish global
code acceptance or resolve missing lifecycle coverage. The static guard
review finds no proven still-photo predicate and no demonstrated substitute;
UI stack/selector state is not an eligibility guarantee.

The package path has an unchanged original round trip and read-only
container, exact-edit and installation-span models. These are not acceptance
of a modified camera update package. The native digest still has missing
input, and physical acceptance, installation and recovery remain unverified.
See [native-firmware-preflight-plan.md](native-firmware-preflight-plan.md),
[native-installation-model.md](native-installation-model.md) and
[recovery-plan.md](recovery-plan.md).

## Decision requiring the owner

Current decision: **condition 1 remains unmet; hardware NO-GO**. The owner's
“Go” authorized the work, not an exception to an acceptance requirement.

The concrete choice is whether to retain that unmet gate, or explicitly
record a deviation for the missing native startup, menu-return, playback and
warning coverage for this exact stills prototype. A deviation would accept
those unmeasured behaviors as residual risk; it would not turn them into
passing tests or guarantee unobstructed screens.

The source is [build-phase-gate.md](build-phase-gate.md), hardware-access
condition 1: “The simulator must show the feature working without a debugger
memory write, and the relevant state transitions must pass.”
[The minimal checklist](patch-readiness-checklist.md) likewise requires
simulator essentials unless an explicit owner deviation is recorded.

Even an explicit deviation here would not approve camera access or satisfy
the other gates: exact build/package preflight, remaining code review,
original backup/recovery decision, readiness record and separate approval
immediately before hardware access remain required. Offline preparation can
continue without calling the feature simulator-accepted.

No waiver was inferred or entered. No simulator, new overlay/image, patch
change, camera access, commit, push, merge or PR occurred in this checkpoint.
