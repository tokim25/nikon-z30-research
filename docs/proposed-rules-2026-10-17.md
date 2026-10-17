# Proposed rule revisions, 2026-10-17

Status: APPROVED by the owner on 2026-10-17, with the owner's edits to items 5 and 6 applied below.
Drafted by the Claude session manager at the owner's request, outside Codex's
lane, because Codex has uncommitted work in the same checkout.

## Camera contact

1. **Pre-approved read-only identification.** The owner pre-approves a
   category: connecting the Z 30 and reading its model and firmware version
   through a command the owner has confirmed read-only. No per-session
   readiness write-up is needed for this category.
2. **Writes need per-step approval.** Any command that could change the camera
   (flash, install, settings write, file write) needs the owner's explicit
   approval for that exact step, given in one reply that names the command and
   its purpose.
3. **Tool safety check before first use.** Before a new tool touches the
   camera, its source or documentation is reviewed for write paths and the
   result is recorded. The check is done once per tool version.
4. **Recovery record.** Any write step must have a recorded recovery path,
   stated as an accepted service-or-total-loss risk, not as safe.

## Firmware and publication (unchanged)

5. Firmware bytes, dumps, installable patches, or proprietary artifacts are
   allowed on the owner's local machine. They must never enter any repository,
   pull request, or published artifact.
6. Camera contact for research or feature work is allowed only within the
   approved identification category in item 1.

## Gates (for owner decision)

7. The owner may record a waiver for a named gate, with a reason, for the
   camera-test stage only. Waivers are visible in the readiness record.
8. Research sessions do not change gate status. Only the owner does.

## Still required, not relaxed

- No flashing without an exact, reviewed method and a recovery record.
- No camera contact for research or feature work beyond the pre-approved
  identification category.
- The lifecycle gate and the XPan still-photo guard stay open until resolved
  or explicitly waived by the owner.

## Owner decisions needed

- Approve or edit the pre-approved identification category (item 1).
- Confirm the per-step write approval rule (item 2).
- Decide whether waivers (item 7) are allowed at all.

## Owner confirmation, 2026-10-17

Item 7 is approved: the owner may waive a named gate at the camera-test stage.
Each waiver must name the gate, give the owner's reason, and appear in the
readiness record. The lifecycle gate and the XPan still-photo guard are not
waived by default; each needs its own explicit, named waiver.
