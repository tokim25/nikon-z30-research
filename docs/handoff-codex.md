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

Live-view payload research started 2026-10-15 on
`codex/tracking-liveview-payload`, from main. Prior static routing evidence is
in [PR #15](https://github.com/tokim25/nikon-z30-research/pull/15): shared router
`0x104b912c`, conditional type-3 send at `0x102f2c22`, and state-1 input branch
`0x102f7448`. No tracking entry point or normal button delivery is verified.

Confirmed private WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Read existing inputs only. New private scripts and outputs use `codex_` or
`codex-` prefixes outside Git. Do not change the simulator or firmware.

The [payload report](tracking-liveview-payload.md) records the new findings.
The actual builder is `0x102f2ad2`, called by worker loop `0x102f2ca8`.
The planned `0x102f2990` builder attribution was wrong; that initializer returns
before event building. The builder prepares 188 bytes, but parsers also use
separate records. Do not treat this size as a complete input contract.

Record-fetch helper `0x102f1412` uses base `0xc2008ea0`, a 400-byte stride and
wrapped indexing in mode 0. Mode 1 returns separate record `0xc200a7a0`.
Their producers and meaning remain unknown. Earlier type-9 handling can pass
the payload pointer to more helpers; effects on data and selected state remain
unresolved. No input calls have been attempted.

State-1 chain: worker flag bit 16 -> type 2 -> selector-0 handler case 2 ->
object `+0x30` getter -> `0x102f57e2` -> selector-1 write `0x102f5810`.
This is static control flow. Flag production, helper behavior and runtime
delivery remain unverified. State 4 is also a stock value; do not force states.

Private verifier `codex_liveview_payload_verify_private.py` passed with output
`private-inputs/codex-liveview-payload-verified-01`. All raw output stays outside
Git. Two subagents checked parser and state claims. Module identity matched;
the pinned simulator stayed clean. No guest controls, hardware or firmware edits.

All 40 repository tests passed with `python3`. Tracked-artifact and encoded-data
checks passed. Publication contains documentation only.

## Next step

Trace the producer of records read by `0x102f1412` and determine whether and how
they represent an OK-button press, keeping prior type-9 handling and state
dependencies explicit. Do not propose a simulator input call yet.

## Notes for the next session

- Record each finding in facts.md as an append-only entry, marked observed or
  inferred.
- Keep raw output, firmware and screenshots outside the checkout.

Written by Codex in collaboration with Tony Kim; incorporates the prior Claude handoff.
