# Codex handoff

Codex owns this file. Update it whenever work is in progress, so a fresh
session can resume. Rules are in [collaboration.md](collaboration.md).

## Lane

Tracking entry-point research: where the original firmware starts and ends the
subject-tracking reticle, and what state it needs. Static analysis, simulator
observation, tests and tooling.

## State

Four findings are merged here, each with a private verifier script and a
fact in [facts.md](facts.md):

- F-009 [input sampler lead](tracking-input-sampler.md): MMIO byte reads.
- F-010 [sampler consumers](tracking-sampler-consumers.md): caller and callback.
- F-011 [event router](tracking-ui-event-router.md): shared menu and live-view router.
- F-012 [live-view payload](tracking-liveview-payload.md): event builder, state-1 path.

No tracking entry point is verified, and no input call has been attempted.
Codex stalled on token limits. Claude continued on 2026-10-15 with read-only
helper studies, recorded as F-014 to F-019 (helper results, not re-verified):

- Bit 16 is set by the live-view mode-enter routine, not by a control (F-014).
- State 1 needs only a processed mode switch to live view (F-015).
- Type 9 looks like a settings resync (F-016).
- Input codes reach mode switches through a table (F-017).
- The simulator has no button model (F-018), and a stock refresh never runs
  the live-view task (F-019).

Key routing in live view is in F-020. F-021 shows that neither store
`0x102f1412` reads is a button record, but traces internal code 0x1b (event
0x27e, OK) back to a physical packet byte: a working example of a button
reaching an internal event.

The owner added a goal: map AE-L/AF-L to the tracking entry point (flag bit
16 -> state 1, F-014/F-015), research and spec only. A study on that is
running; its result starts at F-022. Check facts.md first.

## Next step

1. AE-L/AF-L: find its input code and press/release handling (likely through
   decoder `0x102f0e38` from F-021), and whether its handler shares a
   dispatch point with `0x102f2990`. Priority; the rest wait on it.
2. Resolve the live-view screen's key table from group array `0xc2006594`,
   and read its entries for 0x27E, 0x2a3, 0x2a8 and the default 0x31e.
3. Trace task loop `0x10235576` and the code tables for 0x24e to 0x252.
4. Trace upward from `0x1030705a` to the message framework and packet
   sender, for issue #11.

Propose no simulator input call yet.

## To resume

1. Read AGENTS.md, collaboration.md, facts.md, then the four reports above.
2. Run the tests and both checks with `python3`.
3. Private WORK is
   `/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
   Re-run a `codex_*_verify_private.py` script into a fresh output folder.
4. Branch `codex/<topic>` from main; one finding per PR.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.
