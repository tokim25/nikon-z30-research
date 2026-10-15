# Hardware-readiness checkpoint

Date: 2026-10-15. Decision: **NO-GO for hardware testing or installation.**

This is an interim assessment, not completion of the five-milestone program.
The user authorized continued offline research through a readiness decision;
that does not authorize hardware access or production of installable firmware.

## Milestone status

| Milestone | Current evidence | Remaining acceptance gate |
| --- | --- | --- |
| Prerequisite: native XPan guides | Native stock display baseline runs; host geometry works. | Actual guides rendered by native code and removed cleanly. |
| 1. Framing reliability | Synthetic geometry and overlay tests pass. | Native guide placement across layouts, menus and focus graphics, repeated toggle and cleanup checks. |
| 2. Tracking entry point | Documented behavior and a host interaction model; no verified callable entry point. | Trace the original reticle activation path and establish its state requirements. |
| 3. One-step native activation | Host model only. | One verified native input, visible reticle transition, cancellation and rejection in unsupported modes. |
| 4. Combined native checks | Neither native feature is established. | Run both together and verify display/input isolation, cleanup and recovery in simulation. |
| 5. Final readiness decision | Interim no-go is justified by missing evidence. | Review completed preceding evidence and unresolved emulator-to-camera differences. A no-go remains a valid eventual decision. |

Passing host tests cannot advance native milestones. A successful simulated
reticle transition would still not prove actual autofocus performance.

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

1. Complete native simulator acceptance evidence with repeatable procedures.
2. Keep measured behavior separate from startup fixtures and emulator assumptions.
3. Establish version checks, failure containment and a credible recovery plan;
   do not assume an ordinary firmware-update menu can recover a failed device.
4. Review publication content and third-party licensing independently of tests.
5. Ask the user for separate, informed approval of a clearly bounded hardware
   plan. This document grants no permission to connect, flash or install.

Next: establish the native drawing interface and tracking input route. Until
those are verified, guide reliability and combined native testing remain blocked
by research dependencies, not by a need for more user approval.
