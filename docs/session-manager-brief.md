# Session-manager brief (read first, updated 2026-10-17)

Read this before any other doc. It is the short state of the project. Deeper
detail lives in the linked docs; open them only when a step needs them.

## Owner rules (approved 2026-10-17)

- Read-only identification of the Z 30 is pre-approved. Any camera write needs
  the owner's approval for that exact step, in one reply.
- Firmware bytes stay on the owner's local machine; never in git or a PR.
- Simulator work (pinned QEMU 10.2.4) is pre-approved. No camera contact, no
  flashing, no installation workflow from simulator work.
- Owner may waive named gates for the camera-test stage, with a reason.
- Full rules: [proposed-rules-2026-10-17.md](proposed-rules-2026-10-17.md).

## Hardware and identity

- Camera: Z 30 reports firmware V1.20 (read-only check, gphoto2 --summary).
- Original firmware: Z_30_0120.bin in the owner's Documents folder; SHA-256 and
  size match the pinned original. A scratch working copy exists outside the repo.
- Byte-exact identity: WAIVED by owner ("I assume the risks"). Recorded in
  [test-readiness-2026-10-17.md](test-readiness-2026-10-17.md).
- gphoto2 is NOT read-only as shipped (write-capable calls). Do not use it
  beyond the identity query without a reviewed command and owner approval.
- Hardware status: NO-GO for modified firmware. No modified firmware exists.

## Waivers (owner, 2026-10-17)

- Lifecycle gate: waived.
- XPan still-photo guard: waived; risk accepted (crop lines may appear during
  movies, playback, or warnings).
- Byte-exact identity: waived.

## Feature status

| Feature | Status | Blocker |
|---|---|---|
| XPan crop (bars, geometry, label) | Not built | Crop-offset probe blocked: no RAM helper or WORK script on this machine; 5208×1928 prior result not 5200×1920; output record unchecked; digest input at 0x10000088 unresolved |
| Tracking (AE-L/AF-L) | Not built | Simulator cannot press AE-L/AF-L; tracking start point unproven; needs real-camera test |
| Saved crop files | Not testable yet | Depends on XPan; needs real-camera test |

## Research that is closed or parked

- Saved-crop static research: closed (getter callers, filename trace: not found).
- Tracking static search (property 0x2021 consumer): not found. Stack and
  placement of 424-byte candidate: passes on paper (dfad2ef).
- Still-photo predicate: unresolved at hook 0x102f5810 (F-150).
- Outside repos (WonderLantern z30-qemu, bullton/nikon): no help for blockers.

## Simulator facts (QEMU 10.2.4, pinned)

- Works: stock menu/live-view paths in assisted profile; area pick; bars hook
  on live-view start (F-101 line); guest memory writes via debugger.
- Cannot: press AE-L/AF-L, press shutter, use i-menu, write saved files,
  model natural startup fully.
- F-079 method (repoint RAM area table at 0xc18c7de8 to scratch records) is
  not reproducible here: its script is in a private WORK folder not on this
  machine.

## Codex lane (owner-directed)

- Uncommitted work on codex/firmware-preflight-plan: fact numbers collide with
  main; Codex must renumber before commit.
- Codex owns simulator runs with pushes and merges; Claude does static
  research and tidying.

## Next actions (in order)

1. Find or recreate the RAM-write helper for the crop-offset probe, or report
   that the WORK script is needed (ask the owner for its location).
2. Resolve the output-record question with a re-measured 5200×1920 window.
3. Resolve the digest input at 0x10000088 before any modified image is built.
4. Tracking: decide the real-camera test plan; needs owner approval per step.
5. Do not restart closed research threads without new evidence.

## Branches (all local or pushed, none merged)

- claude/lane2-filename-trace-981f75, claude/lane3-family-search-2ded1d,
  claude/eloquent-napier-52e1c8, claude/owner-rules-2026-10-17 (rules commit
  9a495c4, local), claude/xpan-stills-route-94393a (readiness record).
