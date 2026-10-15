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

Session started 2026-10-15 on `codex/tracking-input-route`, branched from
`main` at `cc817de166999f7ec47491e551d732738e918a6f`. The fresh checkout is
`work/nikon-z30-research` under this chat workspace. No tracking entry point
has been verified in this session.

Read AGENTS.md, handoff.md, native-guides-simulator.md, roadmap.md,
hardware-readiness.md, collaboration.md, build-phase-gate.md, facts.md and
tracking-entry-research.md before analysis. The previous static report rejects
the Bluetooth/HCI convergence lead. That is prior evidence, not a finding
reproduced by this session.

Baseline validation passed: 40 tests and the tracked-artifact check. The
requested `python` commands could not start because that executable is absent;
the equivalent `python3` commands passed:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 .github/scripts/check_artifacts.py
```

The owner confirmed restricted inputs under
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
The verified module is `private-inputs/eg2090_0120a0.bi`; simulator checkout is
`z30-qemu`; recovered originals are `recovered-m1`; static-analysis Python is
`analysis-env/bin/python`. Existing files must stay unchanged. New private
scripts and run directories use the owner's required `codex-` or `codex_`
prefix. No restricted material belongs in this checkout.

Hash and size matched the verified module. Simulator revision matched
`0ba0c3547ccbec09e7c861eaca35db8e82795f15` and its checkout stayed clean.
The new [bounded sampling report](tracking-input-sampler.md) records the first
finding: candidate routines `0x1029d8aa` and `0x1029d8ea` read `0x2016c010`.
The source-comment addresses and a diagnostic offset hypothesis failed.
No simulator execution, native control calls or firmware modifications ran.

Private scripts in the confirmed WORK directory:
`codex_tracking_input_audit_private.py` and its six synthetic tests reproduce
GUI source patterns without importing or executing the GUI. All six passed.
These are source-pattern checks, not reachability or runtime proof.
`codex_input_sampler_verify_private.py` reproduces bounded static evidence;
its first successful run is `private-inputs/codex-input-sampler-verified-01`.
Earlier `codex-input-*` directories retain exploratory raw output privately.
Two Codex subagents reviewed source landmarks and the audit's claim wording.

## Next step

Trace static callers of `0x1029d8aa` and `0x1029d8ea`, then identify their
output consumers and peripheral purpose. Do not call them button samplers or
live-view handlers until that connection is established. The GUI refresh
substitution was rechecked in source; it is not an input landmark.

Follow a source-supported input landmark through static callers and state
checks before proposing any simulator control call. Record addresses,
observations, inference, confidence and a reproduction command in a tracking
report and append-only facts entry. A candidate address alone does not meet
the tracking-entry gate. Publish each supported finding as a small PR after
validation and manual diff review; leave merging to the owner.

## Notes for the next session

- Record each finding in facts.md as an append-only entry, marked observed or
  inferred.
- Keep raw output, firmware and screenshots outside the checkout.

Written by Codex in collaboration with Tony Kim; incorporates the prior Claude handoff.
