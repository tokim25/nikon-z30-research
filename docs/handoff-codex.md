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

Menu input research started 2026-10-15 on `codex/tracking-menu-router`, from
`main` at `cc817de166999f7ec47491e551d732738e918a6f`. No tracking entry point
has been verified. Prior findings are in
[PR #13](https://github.com/tokim25/nikon-z30-research/pull/13) and
[PR #14](https://github.com/tokim25/nikon-z30-research/pull/14). Neither PR is
part of this branch's base. The MMIO sampler lead now favors HDMI status
handling, as an inference, and is no longer the main tracking lead.

The owner confirmed private inputs under
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Use `private-inputs/eg2090_0120a0.bi`, `z30-qemu`, `recovered-m1`, and
`analysis-env/bin/python` only there. Keep existing files unchanged. New private
helpers and output folders use `codex_` or `codex-` prefixes outside Git.

The [shared event-router report](tracking-ui-event-router.md) records a static
connection: `0x104b912c` chooses a callback using state byte `object + 0x74`.
State 1 selects menu handler `0x103cf78e` or live-view-setup handler
`0x102f79ac`. Their type-3 branches reach `0x103cf696` and `0x102f7448`.
The live-view worker conditionally sends type 3 at `0x102f2c22`, with a stack
payload. No physical button, reticle or AF action has been verified.

Both initializers select state 0; the live-view state-0 handler ignores type 3.
Other code writes live-view state 1 at `0x102f5810` and 4 at `0x102f61b0`.
Their conditions are unknown. Do not treat the selector as a boolean or change
it manually. The setter also clears two fields when called with zero.

Private verifier `codex_ui_route_verify_private.py` passed, with output at
`private-inputs/codex-ui-route-verified-02`. Other `codex-menu-*` and
`codex-ui-*` folders contain exploratory raw output outside Git. Early linear
windows crossed data tables; only checked code blocks and resolved table
destinations support the report. Two subagents checked mapping and routing.
The module hash matched and simulator checkout stayed clean at the pinned
revision. No simulator or native controls were run; no firmware was modified.

All 40 repository tests passed with `python3`. Tracked-artifact and encoded-data
checks passed. Only documentation is being published.

## Next step

Map the live-view worker's type-3 payload and its use by `0x102f7448`, including
the conditions that select state 1. Establish that contract before proposing
a simulator input call. Current results map code paths, not tracking activation.

## Notes for the next session

- Record each finding in facts.md as an append-only entry, marked observed or
  inferred.
- Keep raw output, firmware and screenshots outside the checkout.

Written by Codex in collaboration with Tony Kim; incorporates the prior Claude handoff.
