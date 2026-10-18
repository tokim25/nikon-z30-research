# Hardware-readiness checkpoint

Reviewed 2026-10-16. **NO-GO for hardware testing or installation.**
Personal build-phase authorization does not grant permission to connect,
flash or install on the owner's camera. No installable firmware was produced.

Current XPan update (2026-10-17): a private offline standalone-EG candidate
exists and passes independent exact-edit, layout, length and native-CRC
checks (F-198). Nikon updater acceptance, lifecycle condition 1 and hardware
behavior remain unverified; condition 1 is explicitly unmet. This candidate
does not change this record's NO-GO status or authorize camera contact/write.
See [Codex handoff](handoff-codex.md) for the private artifact identity.

This checkpoint does not certify hardware safety. Safety cannot be proved
before the first camera test. It tracks progress toward three states defined in
[build-phase-gate.md](build-phase-gate.md): **SIMULATOR ACCEPTED**, **READY
FOR AN EXPERIMENTAL HARDWARE TEST**, or **HARDWARE VALIDATED**. The current
state is below the first of those for the complete feature set.

## Owner call on build-gate condition 1, Lane 1 (live-view-bars hook) --
## dissenting review recorded, 2026-10-16

The owner has called `build-phase-gate.md`'s condition 1 ("the simulator
must show the feature working without a debugger memory write, and the
relevant state transitions must pass") **satisfied for Lane 1 specifically**,
on this evidence: the native in-ROM hook (a pre-boot loader overlay, not a
live debugger write) passed its direct area-change and ten-cycle controls
and, via a diagnostic dispatch call, the full live-view-ready transition
(F-101); the natural trigger for that same transition is now understood
end to end down to the exact event code (F-107, F-108).

**This call is provisional, not final, and does not by itself authorize any
build-phase work on this feature.** The gate's current wording ("the
relevant state transitions must pass") does not explicitly distinguish a
diagnostic-call transition from a naturally-triggered one, and the hook was
only observed passing via the former -- F-108 explains the natural trigger's
mechanism but does not demonstrate it firing in the simulator. Whether that
distinction matters is exactly what requires scrutiny.

**Before any build-phase work begins on this feature, a dissenting review
from Codex, run as its own independent session (not by the session that
reached this call), is required.** The review should take the skeptical
side on purpose: does the diagnostic-call evidence actually satisfy "the
relevant state transitions must pass," or does the gate require observing
a natural trigger specifically; is F-108's mechanism-level understanding of
the trigger event sufficient given the natural trigger itself still was not
found; and is there anything else this call missed. Record the review's
conclusion here, in this section, when it happens -- agreeing, disagreeing,
or asking the owner to decide. Until that review is recorded, treat this
call as not yet in effect for any build step. The review is recorded
below and does not support treating the call as in effect.

### Dissenting review (independent Claude session, 2026-10-16)

Scope: a document-only review. I read `AGENTS.md`'s priority section,
`build-phase-gate.md`, the Lane 1 section of `handoff-codex.md`, F-101 and
F-107 through F-109, and `native-xpan-liveview-hook.md`. I did not rerun the
simulator or any script. The brief asked for a Codex session. The owner
asked for a session other than the one that made the call, and this one was
run by Claude. The owner confirmed on 2026-10-16 that this substitution is
acceptable.

**Conclusion: I disagree that condition 1 is satisfied as worded. It is
partly met. Whether to proceed anyway is the owner's risk-acceptance
decision, and it should be recorded as an explicit deviation from the gate,
not as the gate having passed.**

**1. Does diagnostic-call evidence satisfy "the relevant state transitions
must pass"?** Not on a plain reading, for three reasons.

- The gate defines its own first state as passing "natural-startup, state,
  control and stress checks in the pinned simulator." Condition 1 is the
  measurable form of that state, so "natural" is part of the gate's intent
  even though condition 1's sentence leaves it out.
- The project's own documents say the check was not run. The hook doc's
  Limits section says a true return from the menu to live view "has not been
  observed" and that "natural transition coverage ... remain[s] open." This
  file's table still lists "Natural startup and supported state lifecycle"
  and "verified return to live view" as remaining gaps. The owner call sits
  directly above those rows and contradicts them. Both cannot be current.
- "Without a debugger memory write" is met, because the overlay loads before
  CPU start. But every one of the three trigger moments was exercised by a
  synthetic stand-in: direct stock row callbacks for the area change, an
  "audited screen-activation call" for the menu pick, and a diagnostic type-2
  dispatch for live-view-ready. None was reached by the firmware's own
  control flow. The diagnostic call also ran with the live-view worker
  dormant, so the state it returned into is not the state a running camera
  has.

**2. Is F-108's mechanism-level understanding enough?** It is a real gap,
not a formality.

- The only bug this effort found was in an unnatural path. The unguarded
  close hook turned the mask on in the `0x24e`/`0x250` non-live-view close.
  The guard (empty stack plus selector 1) was designed against that case and
  was never exercised on the transition it is meant to allow. That the guard
  admits the real return to live view is inferred, and F-101 rates it
  medium confidence.
- F-108 links event `0x4100012` to the hook only through `0xc181f6fc`, which
  is not the selector byte the guard reads (`0xc1821db8`). F-108 itself
  rates "this is the natural trigger" medium confidence. The match to
  F-090's two calls is real corroboration but is not an observation.
- F-109 then found no reference of any kind to the dispatcher `0x10459d80`
  across the whole image, using four methods. F-109 allows that it may be
  dead code in this build. The justification that the real camera "obviously
  already delivers" the event rests on F-090 showing live view works, and
  that does not show this event is the path. So F-108's trigger may not be
  the live one. F-109 was correctly deprioritized as a simulator question,
  but it also removes the support the owner call leans on.
- A diagnostic call from the test harness does not reproduce the calling
  context of a real trigger: thread, stack depth, interrupt or lock state,
  and timing. The hook adds code on a path that runs in that context. Those
  are the properties the gate's condition 3 asks to be reviewed, and no one
  has recorded that review for these insertion points.

**3. What else the call missed or understated.**

- Only the mask hook was tested. The area-change trigger was never driven
  through the real `i` menu (the simulator has no such button), and the
  design's own checklist items (menu cleanup, focus graphics, reboot) remain
  open in the table above.
- The four candidate spans are zero-filled in the image and have no
  references found. On hardware, whether zero-filled regions are writable
  or covered by a checksum or signature is unknown. That belongs to
  conditions 2 and 3, but the owner call reads as if instruction space is
  settled. It is settled for the simulator only.
- The call is labeled "Lane 1 specifically", but the build order in the
  gate's test plan is the XPan bars and the saved crop together. Condition 1
  met for the hook alone says nothing about the crop half.

**What would close this, in order of cost.** (a) Run the real close handler
`0x10460c3c` with `0xc181f6fc` preset to 4 through the loader overlay, not
the debugger. That exercises the real consumer and the guard on the
transition it must admit, without needing to know who posts the event.
(b) Run the guarded hook with the live-view worker active, if the fixture
can be made to do so. (c) If neither is feasible, the owner can accept the
residual risk in writing: naming that the three triggers were observed only
through diagnostic calls, that the guard's admit path is inferred, and that
the event poster is unknown. The gate permits accepted risk for recovery
(condition 4), but it has no such waiver for condition 1, so the owner
should amend the gate or record this as a deviation rather than let
"satisfied" stand.

**Status of the call after this review:** not satisfied as worded; no
build-phase work on this feature should start on the strength of it until
the owner either has (a) or (b) done or records the deviation in (c).

### Attempt at remediation option (a), 2026-10-16

Ran the review's cheapest option. Read-only/simulator-only; no firmware
modified, no hardware touched.

A loader-overlay row presetting `0xc181f6fc` to `4` (loaded before CPU
start, exactly like every other overlay row -- not a debugger write) did
**not** survive to the point of the call: by the time the diagnostic call
ran, the byte read back as `1`. The exact writer was not identified in
this pass.

A diagnostic call to the firmware's own setter (`0x10457dac`, F-108),
not a memory write, did set the byte to `4` and it held through the
close-handler call. The close handler's own internal chain executed
exactly as F-107/F-108 predicted. The overlay's guard and mask were
**not reached** -- consistent with this same doc's own "natural
transition coverage ... remain[s] open" gap and the live-ready probe's
documented limit that the natural worker caller stays dormant in this
assisted fixture. Option (a) alone does not close this. Option (b),
or the owner's written risk acceptance in option (c), remain the ways
forward.

### Follow-up: instruction-level audit fixed and re-tested, 2026-10-17 (F-115)

A separate instruction-level audit of the generator (PR #145,
[native-xpan-liveview-hook-audit.md](native-xpan-liveview-hook-audit.md))
found no crash-level defect but three things to fix and re-test. This pass
fixed two of them in a private, throwaway copy of the generator -- the
screen-activation wrapper's clobbered `r2` and the close
wrapper/guard's stack misalignment, both same-size push/pop edits -- and
deliberately left the third (a shared mask-clear helper that runs on every
non-live-view screen activation) unchanged after confirming by static trace
that properly narrowing it would require an open-ended investigation of
which object types legitimately overlay live view, which the project's own
priority rule says not to start for a simulator-side question.

Every existing simulator control (direct area-change sequence, ten-cycle
signal test, the `0x250` non-live-view close control, the diagnostic
live-view-ready probe) was re-run against the rebuilt, fixed overlay and
passed, with firmware hash and the pinned QEMU checkout unchanged.

This pass also repeated option (a) above -- unchanged in method, run again
against the *fixed* overlay. The result differs from the attempt recorded
just above: this time the guard (`0x1002d860`) and mask helper
(`0x1002d78c`) were both reached during the close-handler call, where
before (against the pre-fix overlay) neither was. The mask flag's value did
not change in this one run (already 1 before and after), so this is not a
demonstrated flag flip on the natural-ish path -- it is the guard/mask
being reached at all on this consumer-side path, for the first time outside
a diagnostic dispatch call. The most likely explanation is the stack-
alignment fix changing how the stock callback the close wrapper calls
behaves; this was not confirmed by single-stepping and was not pursued
further, per the task's own instruction to try one such test and stop.

**Condition 1 remains the owner's call, exactly as this review left it.**
This follow-up fixes code-quality findings from a separate audit and adds
one more data point to the natural-path question; it does not itself
satisfy "the relevant state transitions must pass," and nothing here
should be read as marking condition 1 satisfied. Full detail, confidence
levels and the full set of control results: `docs/facts.md` F-115.

| Requirement | Evidence | Remaining gap |
| --- | --- | --- |
| Live-view framing | Prior native guide lines; PR #43 adds persistent native black masks after diagnostic setup. | Natural startup and supported state lifecycle. |
| Display reliability | PR #48 repeats two clean on/off cycles. Mask remains over audited menu entry. | Menu cleanup, verified return to live view, focus graphics and reboot. |
| RAW crop | PR #37 changes capture geometry to centered 5200 by 1920 in a disposable guest. F-095 through F-106 traced the leading candidate save-path chain (a crop/record builder, `0x101d5c54`) in depth: F-105's exhaustive call-graph check ruled out the simplest direct-write hypothesis, and F-106's direct test of the alternative leans toward that chain being a settings/property handler, not a capture/save descriptor. **The actual save-crop mechanism remains unfound; this is not close to resolved.** | A real save-path candidate. The one serious lead investigated points away from itself. |
| RAW output path | PR #47 verifies a selected structure pack and processing submission. Same caveat as above -- no confirmed link from that structure pack to an actual storage write has been established by this session's work. | Source-object identity and native serialization/storage boundary; a confirmed save-path candidate to investigate once one exists. |
| AE-L/AF-L tracking | PRs #44/#45 trace a queued bank mapping; tracking-input-chain.md finds a real, non-Bluetooth event-code cluster (touch input `0x2006`, state codes `0x2020`/`0x2021`, multi-sub-code dispatcher `0x2087` near tracking's own `0x2083`) where most sub-codes post a simple few-state value to property `0x2021` -- a toggle/lock shape worth testing against AE-L/AF-L, not yet confirmed. Physical identity remains unresolved. | Verified button press/release, tracking entry point, reticle and cancellation; specifically, what reads property `0x2021`. |
| Combined features | Neither complete feature is available. | Concurrent display/input behavior, rejection in unsupported states and recovery. |
| Failure containment | Exact original identity gate exists. | Timing, power behavior, compatibility, and either a verified recovery path or explicit acceptance that recovery may require service or may fail. |
| Instruction/call-contract review (condition 3) | F-128 resolves F-127's measured flag mismatch. Both strict state contracts, including entry flags, pass; writer frame, result, return CPSR and target match in paired diagnostic QEMU runs. | Scratch writer LR differs; finite fixtures do not cover every flag, concurrent/interrupt context or ready/close lifecycle. Global condition 3 remains open; see native-xpan-flags-remediation.md. |
| Update-package acceptance | F-115 through F-118 provide unchanged packaging and decoded/exact-edit preflight. F-119/F-120 trace native checks. F-121/F-122 map native erase/program/readback; F-123 adds full-span/padding modeling tied to the candidate. | The native digest's eight-byte source remains missing; validation/update branches were not executed. Runtime device geometry and physical writes/recovery remain unverified. See native-installation-model.md. |

The masked preview leaves 720 by 266 visible pixels, rounded to 65:24.
It hides UI outside that strip as well. The test uses one diagnostic guest
clip-flag write and native geometry/color setup; it is not an automatic
firmware feature. The audited live-view entry after menu entry leaves the
screen stack populated, so it does not establish natural menu exit.

Assisted startup and synthetic preview input do not establish sensor,
physical input or save-pipeline readiness. An empty screen stack also does
not mean the live-view mode object is uninitialized (PR #46). The simulator
has functional ISP support (PR #41), but that alone does not prove it can
validate a complete RAW capture/save path.

Tracking research has resumed by owner request; earlier paused-lane wording
is stale. No physical-button input or tracking activation is verified.
Matching a logical input mask to the named hardware switch is insufficient.

All new observations are bounded in the milestone PRs listed in
[the current handoff](handoff-codex.md). Original firmware files/instructions
and the pinned simulator remain unchanged; runtime data was restored before
each disposable process was discarded. No hardware was used.

Next: establish native clip-state lifecycle across menu entry and a verified
return to live view. Complete the remaining simulator evidence and containment
work before proposing a separate, concrete hardware plan for owner approval.

Changing this file to **READY FOR AN EXPERIMENTAL HARDWARE TEST** would mean
that the measurable preflight checks passed and the owner accepted the written
residual risk. It would not mean that the modified firmware was proved safe.

Written by Codex in collaboration with Tony Kim; updates Claude's earlier checkpoint with the new simulator findings and their limits.
