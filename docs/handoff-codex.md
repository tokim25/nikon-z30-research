# Codex handoff

Codex owns this file. Update it whenever work is in progress, so a fresh
session can resume. Rules are in [collaboration.md](collaboration.md).

## Read this first: research resumed

The owner explicitly asked this Codex session to pick up the latest GitHub
work toward personal-use XPan live view, RAW cropping and AE-L/AF-L tracking.
This resumes tracking research. Camera access still needs separate approval
under the build-phase gate. Worktree: `work/codex-tracking-resume`, branch
`codex/tracking-resume`, based on main `32a9da5`.

Baseline: all 54 tests and both artifact checks pass. F-025 corrects F-021's
exclusive-writer claim: two writers use the same ring, with different input
sizes. See [input-record evidence](tracking-input-records.md). The private
identity-gated verifier passes; an independent decode agrees. No firmware
change or simulator input call has been made in this session.

## Lane

Tracking entry-point research: where the original firmware starts and ends
the subject-tracking reticle, and what state it needs. Static analysis,
simulator observation, tests and tooling.

## State

No tracking entry point is verified, and no input call has been attempted.
Findings merged so far, each marked observed or inferred in
[facts.md](facts.md):

- F-009 to F-012: an MMIO input sampler, its consumers, the shared
  menu/live-view event router, and the live-view event builder.
- F-014 to F-021: where the live-view flag that starts tracking is set, what
  state 1 requires, and (F-021) a working traced example of a physical
  button bit reaching an internal event.
- F-023, F-024: the input map is fully decoded; the four candidate guard
  functions turned out to be ordinary navigation buttons, not AE-L/AF-L. A
  named switch, `ID_SW0_AEAF_LOCK`, has its own dedicated bit (mask 0x2000),
  separate from the d-pad. The owner confirmed the button exists on the
  camera body.

## Wider project context, outside this lane

- The owner opened a build phase for their own, non-distributed camera
  ([build-phase-gate.md](build-phase-gate.md)). This authorizes writing a
  real patcher and a recovery plan; it does not authorize flashing
  anything. This session resumes the previously paused research.
- A firmware version-and-hash gate is merged
  (`src/nikon_z30_research/verified_firmware.py`).
- [hardware-readiness.md](hardware-readiness.md) was reviewed and still
  says NO-GO. It names the unverified tracking entry point as one of two
  remaining blockers, alongside a missing recovery plan.
- F-022 and the guide/menu-state work came from Claude. The owner has now
  approved Codex taking over the guide and RAW-crop files; see below.

## Where the trail was left

This is where the previous research stopped:

1. Find the routine that scans the SW0 switch word, reads bit 13 (mask
   0x2000), and follows it to an input code or event. Then find press and
   release handling, and whether it meets `0x102f2990`.
2. Resolve the live-view screen's key table from group array `0xc2006594`,
   and read its entries for 0x27E, 0x2a3, 0x2a8 and the default 0x31e.
3. Trace task loop `0x10235576` and the code tables for 0x24e to 0x252.
4. Trace upward from `0x1030705a` to the message framework and packet
   sender, for issue #11.

The owner's current request authorizes continuing this research.

## Single next step

Trace the named AE-L/AF-L switch's bit-13 reader and event destination. Do not
equate the diagnostic name table with logical input masks without a code
link. An independent helper is checking this path in the current session.

The owner also requested RAW cropping and explicitly approved Codex taking
over both the RAW-crop and guide files in this conversation. That feature is
not yet demonstrated by capture-geometry calculations: the simulator has no
image processor. Record the ownership update in the next feature PR before
editing the former Claude lane.
`project-status.md` and the readiness report still describe the earlier
tracking pause; this handoff records the owner's later resumption.

## To resume

1. Read this whole file first, then AGENTS.md, collaboration.md,
   project-status.md and facts.md. This session has resumed the lane.
2. Run the tests and both checks with `python3`.
3. Private WORK is
   `/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
   Re-run a `codex_*_verify_private.py` script into a fresh output folder.
4. F-025 is used here. F-026 to F-029 remain reserved for this lane; check project-status.md for
   the actual next free number, since other lanes have used numbers past
   F-029 while this one was paused.
5. Branch `codex/<topic>` from main; one finding per PR.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.
