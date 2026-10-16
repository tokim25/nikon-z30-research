# Codex handoff

Updated 2026-10-15 from main `32a9da5`. The owner explicitly asked Codex to
continue both features and approved taking over the guide and RAW-crop
files. Tracking research is resumed. Personal build work is open under
[build-phase-gate.md](build-phase-gate.md); camera access still requires
separate approval. [The feature plan](tracking-feature-plan.md) states the
requested behavior and the evidence still needed.

## Current work

Dedicated worktree: `work/codex-tracking-resume`. Active branch:
`codex/feature-continuation-plan`. The primary checkout is left on main.

- [PR #34](https://github.com/tokim25/nikon-z30-research/pull/34) corrects
  F-021: the input ring has at least two writers with different input sizes.
  F-025 and its report are in that PR; it is unmerged as of this handoff.
  Its CI passed on Python 3.11, 3.12 and 3.13.
- This branch adds F-026: two record fields use bit 13 but normalize to
  different candidates. Neither is proven to be SW0 or AE-L/AF-L.
  [Evidence and repro](tracking-mask-namespaces.md).
- No tracking entry point, physical-button delivery or RAW crop is verified.
  This session made no firmware changes or simulator input calls.
- Baseline: 54 unit tests, tracked-artifact and encoded-data checks pass.
  Private identity-gated checks and independent static reviews agree with
  both findings.

Merge PR #34 before this branch's PR, retaining F-025 and F-026 and this
newer handoff. Both branches start from main, so the ledger/footer and handoff
may need a manual conflict resolution. Never merge our own PRs.

## Single next step

Trace the producers of snapshot fields `+0x150` and `+0x164` and establish
whether either represents hardware SW0. Do not match AE-L/AF-L merely by its
bit-13 mask. A subagent continues the bounded producer check in this session;
its result must be recorded before it is relied upon.

The longer trail includes the live-view screen key table, dispatcher
`0x103ce96e`, packet decoder `0x1030705a` and the stock worker. These are
landmarks, not safe call interfaces. See F-014 to F-024 for previous claims;
several are helper results that still need independent verification.

## Private inputs and reproduction

Owner-confirmed WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
The original module, simulator and existing helpers stay unchanged. New
private helpers and run folders have `codex_` or `codex-` prefixes. Never
search the disk for more firmware. Never import detailed private output.

Private helpers for this session:
`codex_input_record_verify_private.py` and
`codex-sw0-normalization-verify-private.py`. Use a fresh output folder under
`$WORK/private-inputs/`; report pages give commands and known run names.
All work was static and offline. The pinned simulator checkout stays clean.

## Ownership and remaining limits

The owner approved Codex taking over `docs/native-*`, `docs/guide*`,
`docs/image-area-tables.md` and `docs/capture-geometry-baseline.md`.
`.github/lanes.json` records that transfer on this branch. Simulator
infrastructure retains its previous assignment. Claude should read this
handoff before resuming and agree file ownership before concurrent edits.

RAW cropping needs evidence beyond the capture-geometry routine; the
simulator has no image processor. Native guides still require a debugger
hook. Recovery and failure containment remain unresolved. Hardware readiness
remains NO-GO, even though the research pause is lifted. No hardware steps or
installation workflow are authorized here.

F-025 is allocated in PR #34; F-026 is allocated on this branch. F-027 to
F-029 remain reserved for tracking. Check main and open PRs before numbering
another fact. All new documents must end with collaboration attribution.

Written by Codex in collaboration with Tony Kim; continues Claude's handoff and includes independent Codex subagent reviews.
