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

Key routing in live view is in F-020: the key dispatcher walks a screen
stack, and the live-view screen's key table was not found. One Claude study is
still running, on the writers of the records read by `0x102f1412`. Its result
will appear as F-021. Check facts.md before repeating it.

## Next step

1. Find what fills the screen-object group array at `0xc2006594`, resolve the
   live-view screen to its key table, and read its entries for 0x27E, 0x2a3,
   0x2a8 and the default 0x31e. Decode `0x102f1cae`, which `0x102f1e10` calls.
2. Trace the per-object task loop at `0x10235576` and what wakes it, and
   decode the table rows for internal codes 0x24e to 0x252 with their guards.
3. Writers of the records `0x102f1412` reads, unless F-021 answers it.
4. Observation only: log the sampler, router and worker addresses over 20 to
   30 virtual seconds in a live-view session.

Propose no simulator input call yet.

## To resume

1. Read AGENTS.md, collaboration.md, facts.md, then the four reports above.
2. Run the tests and both checks with `python3`.
3. Private WORK is
   `/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
   Re-run a `codex_*_verify_private.py` script into a fresh output folder.
4. Branch `codex/<topic>` from main; one finding per PR.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.
