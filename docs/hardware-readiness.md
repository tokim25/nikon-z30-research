# Hardware-readiness checkpoint

Reviewed 2026-10-16. **NO-GO for hardware testing or installation.**
Personal build-phase authorization does not grant permission to connect,
flash or install on the owner's camera. No installable firmware was produced.

This checkpoint does not certify hardware safety. Safety cannot be proved
before the first camera test. It tracks progress toward three states defined in
[build-phase-gate.md](build-phase-gate.md): **SIMULATOR ACCEPTED**, **READY
FOR AN EXPERIMENTAL HARDWARE TEST**, or **HARDWARE VALIDATED**. The current
state is below the first of those for the complete feature set.

## Owner call on build-gate condition 1, Lane 1 (live-view-bars hook) --
## pending a dissenting review, 2026-10-16

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
call as not yet in effect for any build step.

| Requirement | Evidence | Remaining gap |
| --- | --- | --- |
| Live-view framing | Prior native guide lines; PR #43 adds persistent native black masks after diagnostic setup. | Natural startup and supported state lifecycle. |
| Display reliability | PR #48 repeats two clean on/off cycles. Mask remains over audited menu entry. | Menu cleanup, verified return to live view, focus graphics and reboot. |
| RAW crop | PR #37 changes capture geometry to centered 5200 by 1920 in a disposable guest. F-095 through F-106 traced the leading candidate save-path chain (a crop/record builder, `0x101d5c54`) in depth: F-105's exhaustive call-graph check ruled out the simplest direct-write hypothesis, and F-106's direct test of the alternative leans toward that chain being a settings/property handler, not a capture/save descriptor. **The actual save-crop mechanism remains unfound; this is not close to resolved.** | A real save-path candidate. The one serious lead investigated points away from itself. |
| RAW output path | PR #47 verifies a selected structure pack and processing submission. Same caveat as above -- no confirmed link from that structure pack to an actual storage write has been established by this session's work. | Source-object identity and native serialization/storage boundary; a confirmed save-path candidate to investigate once one exists. |
| AE-L/AF-L tracking | PRs #44/#45 trace a queued bank mapping; tracking-input-chain.md finds a real, non-Bluetooth event-code cluster (touch input `0x2006`, state codes `0x2020`/`0x2021`, multi-sub-code dispatcher `0x2087` near tracking's own `0x2083`) where most sub-codes post a simple few-state value to property `0x2021` -- a toggle/lock shape worth testing against AE-L/AF-L, not yet confirmed. Physical identity remains unresolved. | Verified button press/release, tracking entry point, reticle and cancellation; specifically, what reads property `0x2021`. |
| Combined features | Neither complete feature is available. | Concurrent display/input behavior, rejection in unsupported states and recovery. |
| Failure containment | Exact original identity gate exists. | Timing, power behavior, compatibility, and either a verified recovery path or explicit acceptance that recovery may require service or may fail. |

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
