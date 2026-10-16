# Gate for a build phase

Status: open, for personal use on the owner's own camera, not for
distribution. Research work (studying the firmware, testing ideas in the
simulator) has never needed this gate; it covers only the step of producing
something meant to run on real hardware.

A build phase turns feature specs into something a person could apply to
their own camera. That carries real risk: a failed update can leave a camera
unusable, and Nikon's firmware is copyrighted.

## The owner's authorization

Recorded 2026-10-15. The owner has said, directly: they want to modify their
own Z30's firmware, understand the hardware risk, and do not plan to
distribute the result to anyone. This authorizes starting the work listed
below. It does not by itself authorize flashing a camera; see "Hardware
access" below.

## Owner-approved test order

When every hardware-access condition below has passed and the owner gives
separate approval to flash the camera, test builds in this order:

1. XPan live-view bars and the saved RAW/JPEG crop together.
2. AE-L/AF-L subject tracking by itself.
3. Both features together.

This order is a test-plan decision. It does not approve a build for hardware
or waive any recovery, version, hash, or readiness requirement.

## What this opens

- Writing a patcher and the actual feature code meant for the camera, not
  just the simulator, using the owner's own local firmware copy.
- Writing the recovery plan and the version and hash checks required before
  any hardware step. That work was previously out of scope; now it is the
  priority.

## Hardware testing: evidence and accepted risk

Absolute hardware safety is not an acceptance criterion. It cannot be proved
before the first camera test because the simulator does not model the Z30's
boot loader, update process, power-loss behavior or every hardware timing
condition.

The project uses three states instead:

1. **Simulator accepted.** The feature passes its natural-startup, state,
   control and stress checks in the pinned simulator.
2. **Ready for an experimental hardware test.** The measurable checks below
   pass, the remaining risks are written down, and the owner gives a separate
   final approval.
3. **Hardware validated.** This state can be earned only after a successful,
   bounded test on real hardware. It is never inferred from the simulator.

Uploading to a real camera is not authorized by this file alone. Before the
second state can apply:

1. The simulator must show the feature working without a debugger memory
   write, and the relevant state transitions must pass.
2. The patcher must accept only the owner's exact verified original and must
   produce only the planned changes.
3. The code layout, instruction mode, branches, register handling, stack use
   and return paths must be reviewed.
4. The original firmware must be backed up offline. A verified recovery path
   is preferred. If none can be verified, the record must say so plainly and
   the owner must explicitly accept that recovery may require Nikon service
   or may be impossible.
5. [hardware-readiness.md](hardware-readiness.md) must say **READY FOR AN
   EXPERIMENTAL HARDWARE TEST**, with the exact build and test scope named.
6. The owner must approve that concrete test immediately before any hardware
   step.

The current state remains NO-GO. Meeting these checks would permit a bounded
experiment; it would not certify the firmware as safe.

## What stays forbidden, always

Publishing Nikon firmware, extracted bytes, dumps, or patched images, in any
repository, issue, release, or anywhere else. This project's own patcher
stores no Nikon bytes and ships no patched image. The owner's modified
firmware copy stays on their own machine, never in this repository. Hardware
steps, once authorized, are done by the owner alone.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
