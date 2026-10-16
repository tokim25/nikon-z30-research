# Codex handoff

Updated 2026-10-15. The owner asked Codex to continue both features and
approved taking over the guide and RAW-crop files. Tracking research is
resumed. Personal build work is open; camera access still needs separate
approval. No installable build has been produced.

## Current work and integration

Dedicated worktree: `work/codex-tracking-resume`. Active branch:
`codex/tracking-input-source`, from main `32a9da5`.
The primary checkout is left on main.

1. [PR #34](https://github.com/tokim25/nikon-z30-research/pull/34): F-025
   corrects F-021's single-writer claim; two writers use the ring.
2. [PR #35](https://github.com/tokim25/nikon-z30-research/pull/35): F-026
   distinguishes two bit-13 record fields. It also records the approved
   file transfer, feature requirements, status and ownership tests.
3. This branch: F-027 identifies a structured-control path that can set or
   clear bit 13 in a staging word and copy it to an input cache.
   [Evidence and repro](tracking-input-source.md).

All start from main. Merge in that order, retaining every append-only fact
and this latest handoff when resolving conflicts. Codex never merges its
own PRs. PRs #34 and #35 have passed CI on Python 3.11, 3.12 and 3.13;
they are unmerged as of this update.

No physical AE-L/AF-L path, tracking entry point or saved RAW crop is
verified. No firmware change, guest input call or hardware action occurred
in this session. Baseline: 54 tests and both artifact checks pass.

## Single next step

Identify the sender and meaning of the structured records consumed near
`0x1008ad26`. Selector 5 and state 1/0 control bit 13, but neither that
selector nor the resulting cache word is proven to represent SW0 or the
physical AE-L/AF-L switch. Do not turn this candidate into a button remap
without the missing source link.

An optional upstream lead from the helper's producer analysis remains
unreviewed: cache pairs based at `0xc181182c` may feed snapshot fields
`+0x150` and `+0x164`. Private script
`codex-snapshot-field-producers-private.py` uses a limited linear symbolic
pass, not full control flow. Verify before relying on it. F-027 deliberately
does not claim that complete link.

## Private inputs and reproduction

Owner-confirmed WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Keep original inputs, existing helpers and the simulator unchanged. Use new
`codex_` or `codex-` private scripts and output folders outside Git; never
search the disk for firmware.

Helpers for the three findings:
`codex_input_record_verify_private.py`,
`codex-sw0-normalization-verify-private.py` and
`codex-input-field-source-verify-private.py`. Use a fresh output directory
under `$WORK/private-inputs/`. Report pages give reproduction commands.
Private raw output never enters Git. The simulator checkout remains clean.

Independent review caught an address-arithmetic error in the last helper:
the staging base is `0xc1811e70`, but the accessed word is base plus 4,
`0xc1811e74`. It also corrected the claim about other state values: they
skip the staging update but still call the cache setter. The report records
the corrected bounded behavior.

## Feature ownership and limits

The owner approved Codex taking over `docs/native-*`, `docs/guide*`,
`docs/image-area-tables.md` and `docs/capture-geometry-baseline.md`.
PR #35 records the transfer in lane configuration and collaboration notes;
simulator infrastructure retains its previous assignment. Claude should read
this handoff and agree file ownership before concurrent edits.

Guides still depend on a debugger hook. The RAW goal needs saved-file and
image-processor evidence beyond geometry calculations; this simulator has no
image processor. Tracking needs a proven input-to-reticle path. Recovery and
failure containment remain unresolved. Hardware readiness stays NO-GO.

F-025, F-026 and F-027 are allocated in these three PRs. F-028 and F-029
remain reserved for tracking. Check main and open PRs before adding facts.

Written by Codex in collaboration with Tony Kim; continues Claude's work and includes independent Codex subagent reviews.
