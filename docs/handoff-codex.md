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
Codex stalled on token limits. On 2026-10-15 Claude started two read-only
static studies on the next step below: the writers of the records read by
`0x102f1412`, and the producers of worker flag bit 16. Their results will be
appended to facts.md as F-014 to F-019 and summarized here. Check
[project-status.md](project-status.md) and the facts file before repeating
that work.

## Next step

Trace the producer of the records that `0x102f1412` reads and decide whether
they can represent an OK-button press. Keep type-9 handling and state
dependencies explicit. Propose no simulator input call yet.

## To resume

1. Read AGENTS.md, collaboration.md, facts.md, then the four reports above.
2. Run the tests and both checks with `python3`.
3. Private WORK is
   `/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
   Re-run a `codex_*_verify_private.py` script into a fresh output folder.
4. Branch `codex/<topic>` from main; one finding per PR.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.
