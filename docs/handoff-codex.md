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

Caller analysis started 2026-10-15 on `codex/tracking-sampler-callers`, from
`main` at `cc817de166999f7ec47491e551d732738e918a6f`. No tracking entry point
has been verified. Prior [PR #13](https://github.com/tokim25/nikon-z30-research/pull/13)
records static MMIO sampling candidates `0x1029d8aa` and `0x1029d8ea`;
that PR is not part of this branch's base.

The owner confirmed private inputs under
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Use `private-inputs/eg2090_0120a0.bi`, `z30-qemu`, `recovered-m1`, and
`analysis-env/bin/python` only at those confirmed locations. Existing files
stay unchanged. New private helpers and outputs use `codex_` or `codex-`
prefixes outside the checkout.

Caller analysis completed in [the consumer report](tracking-sampler-consumers.md).
The first sampler has a bounded caller at `0x1028b040`, followed by debounce-like
filtering and a conditional callback path. Registration connects callback
`0x10396cde` to slot `0xc1807ecc`; its record contains identifier `0x4206101e`.
Record delivery and runtime callback execution remain unverified.

Public Linux register definitions and the simulator's register table strongly
support HDMI-status attribution as inference. Deprioritize this lead for
tracking. No simulator run, native control call, firmware modification or
hardware operation occurred. The module hash matched; the pinned simulator
checkout stayed clean. Two Codex subagents independently reviewed peripheral
attribution and caller semantics.

Private reproduction: `codex_sampler_consumer_verify_private.py` passed with
output `private-inputs/codex-sampler-consumer-verified-01`. The broader original
helper `codex_tracking_static_private.py` records branch candidates, pointer
occurrences and bounded windows in new `codex-` directories. Neither helper nor
its raw output belongs in Git. See the report for exact fresh-run commands.

Validation: all 40 repository tests passed with `python3`; tracked-artifact
and encoded-data checks passed. Changes contain documentation only.

## Next step

Trace registration and callers of menu dispatcher `0x103ce96e` to a shared
event router, then check for a separate live-view branch. Keep results menu-only
until that connection is demonstrated; do not call the dispatcher as a live-view
input substitute.

## Notes for the next session

- Record each finding in facts.md as an append-only entry, marked observed or
  inferred.
- Keep raw output, firmware and screenshots outside the checkout.

Written by Codex in collaboration with Tony Kim; incorporates the prior Claude handoff.
