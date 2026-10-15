# Codex handoff

Codex owns this file. Update it whenever work is in progress, so a fresh
session can resume. Rules are in [collaboration.md](collaboration.md).

## Current lane

Tracking entry-point research: find where the original firmware starts and
ends the subject-tracking reticle, and what state it needs. Static analysis,
simulator observation, tests and tooling. Documented behavior is in
[tracking.md](tracking.md), and earlier leads are in the tracking research
notes.

## State

Nothing in progress. No tracking entry point has been verified.

## Next step

Read AGENTS.md, collaboration.md and facts.md. Run the tests and both checks.
Confirm the restricted-input paths with the owner. Then pick one open lead,
open a `codex/<topic>` branch, and write the plan in this file before running
anything.

## Notes for the next session

- Record each finding in facts.md as an append-only entry, marked observed or
  inferred.
- Keep raw output, firmware and screenshots outside the checkout.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
