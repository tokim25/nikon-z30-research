# Patch readiness checklist

This checklist prevents more research from becoming an endless preparation
loop. Work on a camera patch only when the required items below are either
proved or explicitly recorded as an accepted limitation.

## Required for a simulator patch

- [ ] Exact hook points are named for the live-view bars and, if included,
  AE-L/AF-L tracking.
- [ ] The image-area choice input and the tracking input are both identified
  at the native boundary where the patch will read them.
- [ ] Each hook's trigger and guard are specified, including ordinary startup,
  menu return, state changes, and cleanup paths.
- [ ] Code space, instruction mode, branch reach, literal loads, register use,
  stack layout, flags, and return behavior fit the reserved spans.
- [ ] The patch can be represented as an exact edit manifest without storing
  firmware bytes or a patched image in the repository.
- [ ] The pinned simulator loads the private overlay, with no debugger writes,
  and passes baseline-versus-patched comparisons for all relevant states.
- [ ] The patch does not claim saved RAW/JPEG cropping. That remains an
  owner-approved on-camera test item and is not a blocker here.

## Required before calling the patch simulator-accepted

- [ ] Natural lifecycle checks pass, not only direct debugger or helper calls.
- [ ] Non-target screens and modes remain unchanged.
- [ ] Repeated transitions, cleanup, and recovery behavior are checked.
- [ ] Tracking, if included, preserves native eligibility, chord arbitration,
  press-edge handling, completion cleanup, and playback-protect behavior.
- [ ] A fresh independent review confirms the ABI and branch/space audit.
- [ ] Standard unit, artifact, encoded-data, and diff checks pass.

## Required before any hardware test

- [ ] The exact original firmware identity is verified offline.
- [ ] The read-only preflight accepts only the planned edits and policy.
- [ ] A backup and recovery decision are documented, including the possibility
  of Nikon service or total loss if recovery cannot be verified.
- [ ] `hardware-readiness.md` names the exact build and says READY FOR AN
  EXPERIMENTAL HARDWARE TEST.
- [ ] The owner gives separate approval immediately before touching hardware.

## Current status

- Live-view bars: hook and private simulator evidence exist, but the full
  natural-lifecycle acceptance gate is not yet complete.
- AE-L/AF-L tracking: property-post breakpoint experiment is authorized and
  in progress; no patch should be designed until its result is documented.
- Saved crop: static research is closed; on-camera test item, not a blocker.
- Hardware: NO-GO.
