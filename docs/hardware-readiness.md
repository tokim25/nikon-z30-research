# Hardware-readiness checkpoint

Date: 2026-10-15, reviewed the same day after a round of simulator and
tracking work. Decision: **NO-GO for hardware testing or installation.**

This is an interim assessment, not completion of the five-milestone program.
The owner has separately authorized build-phase work for personal,
non-distributed use ([docs/build-phase-gate.md](build-phase-gate.md)); that
is authorization to start the work below, not a hardware go-ahead. Flashing
or connecting a real camera still needs the owner's separate, explicit
approval at that point, after the conditions below are met.

## Milestone status

| Milestone | Current evidence | Remaining acceptance gate |
| --- | --- | --- |
| Prerequisite: native XPan guides | Met in live view. Native code draws the guides, toggles cleanly, and survives repeated on/off and color/alpha checks ([native-guides-simulator.md](native-guides-simulator.md)). | None remaining for live view; see milestone 1 for other layouts. |
| 1. Framing reliability | Live view is reliable. Menu screens are confirmed, not just unverified, to not support the same mechanism ([guides-ui-states.md](guides-ui-states.md)); that is an accepted limit. | A guide path that also works in menus and focus-graphic overlays, or an explicit decision that live view is sufficient. |
| 2. Tracking entry point | A named hardware switch for a candidate button exists with its own bit ([facts.md](facts.md), fact F-024). The path from that bit to a callable tracking entry point is not established. This research is paused by the owner. | Trace the original reticle activation path and establish its state requirements. |
| 3. One-step native activation | Host model only. | One verified native input, visible reticle transition, cancellation and rejection in unsupported modes. |
| 4. Combined native checks | Guides are established in live view; tracking is not, so the two cannot yet be run together. | Run both together and verify display/input isolation, cleanup and recovery in simulation. |
| 5. Final readiness decision | Reviewed 2026-10-15; still no-go. One native feature (guides) works in live view; the other (tracking) has no verified entry point and its research is paused. | Unchanged: complete milestones 2 to 4, then decide again. |

One milestone being met does not advance the others. Guides working does not
establish anything about tracking, and a successful simulated reticle
transition would still not prove actual autofocus performance.

## Known limitations

- Assisted startup supplies diagnostic state; it is not a demonstrated natural boot.
- Color bars are synthetic processed image input, not a verified sensor pipeline.
- The tested simulator's live-view GUI key branch calls refresh rather than
  forwarding the requested direction/OK/back event. Its menu branch is different.
  GUI key clicks therefore cannot validate live-view tracking input routing.
- Display call arguments, object ownership, clipping, scheduling and cleanup
  are not sufficiently mapped to register new native guide objects safely.
- No physical recovery procedure, failure containment, timing margins, power
  behavior, or compatibility across camera configurations has been validated.

Simulator source for the GUI behavior:
[pinned tools/gui.py](https://github.com/WonderLantern/z30-qemu/blob/0ba0c3547ccbec09e7c861eaca35db8e82795f15/tools/gui.py).
Local execution evidence is summarized in [the baseline report](simulator-baseline.md).

## Conditions before proposing a separate hardware phase

1. Complete native simulator acceptance evidence with repeatable procedures,
   for guides and for tracking. Guides are done for live view; tracking has
   no verified entry point yet.
2. Keep measured behavior separate from startup fixtures and emulator assumptions.
3. Version checks are done: `require_verified_eg_module` refuses anything
   but the owner's exact verified original. Failure containment and a
   credible recovery plan are not done; do not assume an ordinary
   firmware-update menu can recover a failed device.
4. Review publication content and third-party licensing independently of tests.
5. Ask the owner for separate, informed approval of a clearly bounded
   hardware plan, distinct from the personal-use build-phase authorization
   already given. This document grants no permission to connect, flash or
   install.

Next: the native drawing interface is established for live view. The
tracking input route is not, and that research is paused pending the
owner. A written recovery plan and failure containment are the other
remaining blockers, and neither needs the owner's resumption of tracking
research to start.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
