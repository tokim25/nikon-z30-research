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

## Hardware access: still gated

Flashing a real camera is not authorized by this file alone. All of the
following must be true first:

1. The simulator shows the feature working without a debugger hook, or that
   hook's risk is fully understood.
2. A written recovery plan exists ([draft](recovery-plan.md), not yet credible), and it does not rely on the camera's
   ordinary firmware-update menu.
3. The patcher checks firmware version and hash, and refuses anything but
   the owner's exact verified original.
4. [hardware-readiness.md](hardware-readiness.md) no longer says NO-GO; it
   says NO-GO today and has not been reviewed since this authorization.

None of these are true yet. When they are, ask the owner again, explicitly,
before any hardware step.

## What stays forbidden, always

Publishing Nikon firmware, extracted bytes, dumps, or patched images, in any
repository, issue, release, or anywhere else. This project's own patcher
stores no Nikon bytes and ships no patched image. The owner's modified
firmware copy stays on their own machine, never in this repository. Hardware
steps, once authorized, are done by the owner alone.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
