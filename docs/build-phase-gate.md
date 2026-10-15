# Gate for a build phase

Status: closed. Nothing here authorizes a build, flashing, or any hardware
access. Research stays offline and in the simulator.

A build phase would turn feature specs into something a person could apply to
their own camera. That carries real risk: a failed update can leave a camera
unusable, and Nikon's firmware is copyrighted. So it needs its own decision
from the owner, recorded in AGENTS.md.

## Conditions before the owner is asked

1. The simulator shows the feature working without a debugger hook, or the
   hook point and its hang risk are understood and written up.
2. A recovery plan exists for a failed update, and it does not rely on the
   ordinary firmware-update menu.
3. Version and hash checks refuse anything but the exact verified firmware.
4. Licensing and publication content have had an independent review.
5. [hardware-readiness.md](hardware-readiness.md) no longer says NO-GO.

## What a build phase may contain

- Original code and a patcher that works on the owner's own firmware copy.
  It stores no Nikon bytes and ships no patched image.
- Hardware steps are done by the owner alone, after a written plan.

## What stays forbidden

Publishing Nikon firmware, extracted bytes, dumps, or patched images, in any
repository, issue, or release.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
