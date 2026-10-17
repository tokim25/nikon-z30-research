# Corrections index

A short, append-only-in-spirit log of known corrections to earlier facts or
docs in this project. `facts.md` is append-only by its own hard rule (a
correction there is a new entry that supersedes an old one, never an edit in
place), and research docs scatter corrections across whichever PR happened
to catch them — this file exists so a reader doesn't have to cross-reference
PRs to find out something was wrong. Add an entry here whenever a later PR
corrects an earlier fact, doc claim, or handoff statement; never remove or
rewrite an entry once added.

Format per entry: original claim, what was wrong, which file/PR corrected
it, date.

---

## 1. `build-phase-gate.md` condition 1's "second branch" (F-109 over-claim)

- **Original claim:** the F-109 PR (merged as part of
  `claude/f109-event-origin-deadend`) described `build-phase-gate.md`'s
  condition 1 as having two branches — "the simulator shows the feature
  working without a debugger hook, **or that hook's risk is fully
  understood**." That phrasing was also carried into `docs/handoff-codex.md`.
- **What was wrong:** the second branch ("or that hook's risk is fully
  understood") does not exist in the current gate text. It was removed by
  PR #119's hardware-safety rewrite, which replaced the old safety-proof
  criterion with the three-state gate (SIMULATOR ACCEPTED / READY FOR AN
  EXPERIMENTAL HARDWARE TEST / HARDWARE VALIDATED). Condition 1 now reads
  only: "the simulator must show the feature working without a debugger
  memory write, and the relevant state transitions must pass." By the time
  the F-109 PR cited the two-branch framing, that second branch had already
  been gone for several PRs.
- **Corrected in:** PR #131 ("Record owner call on build-gate condition 1;
  require Codex dissenting review"), which updated `docs/hardware-readiness.md`
  (new section) and `docs/handoff-codex.md` (the "Update ... owner call made"
  paragraph under Lane 1) to state the gate's actual current wording and flag
  that the missing second branch is itself part of the ambiguity a dissenting
  review needs to weigh.
- **Date:** 2026-10-16.

## 2. `tracking-dispatch-registration.md`'s `{handler, type-id}` table claim

(That file is now consolidated into [tracking-input-chain.md](tracking-input-chain.md)'s
"2026-10-16: Tracing the queued-bank route upward" section; see entry 3 below.)

- **Original claim:** the "The enclosing state-machine step and its
  registration" section claimed a raw pointer-word scan found handler
  `0x10379d5a` registered in a clean `{handler, type-id}` table at
  `0x1037a2c4` (handler, Thumb-tagged) / `0x1037a2c8` (tag `0x20016`),
  because the tag's shape matched the `[x] - 0x20000` subtraction
  `0x10379d5a` performs on its own input.
- **What was wrong:** direct Thumb disassembly of that region (capstone,
  same firmware, SHA-256 `8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`,
  base `0x10020000`) shows `0x1037a2c4`/`0x1037a2c8` are literal-pool data
  belonging to the small dispatch-case function entered at `0x1037a20c`,
  which returns cleanly at `0x1037a294` (`movs r0, #1; pop {r3, r4, r5,
  pc}`). None of that function's own `ldr rX, [pc, #imm]` literal loads
  resolve to either address — each one, computed as
  `((insn_addr+4) & ~3) + imm`, lands elsewhere in the same pool. The
  surrounding bytes decode as ASCII-looking string fragments, not further
  table entries, confirming scattered literal-pool data rather than a
  standalone registration table with defined boundaries. What remains
  solid from that doc: the `0x10379a68` event-code dispatcher decode, the
  `0x7d` delta routing code `0x2083` to `0x103a3d14`, the `0x10379d5a`
  state-machine step function and its `tbb` dispatch, and the fact that
  `0x10379d5a` has zero direct `bl`/tail-`b.w`/raw-pointer-word callers
  anywhere in the image (that negative finding still stands — it is just
  no longer explained by the withdrawn table claim).
- **Corrected in:** PR merging `claude/tracking-table-correction`, in the
  then-standalone `docs/tracking-dispatch-registration.md`, which replaced
  the table claim with an honest statement that the registration/
  reachability mechanism for `0x10379d5a` remains unresolved. That file was
  later folded into [tracking-input-chain.md](tracking-input-chain.md) by
  the docs-consolidation PR (entry 3 below); the corrected text moved with
  it unchanged.
- **Date:** 2026-10-16.

## 3. tracking-*.md sprawl consolidated into topic files

- **What changed (not a factual correction, a reorganization):** 13
  single-finding `docs/tracking-*.md` stub files from 2026-10-15/16 were
  consolidated into three topic files with zero content loss (every
  address, finding, confidence level, "Observed"/"Inferred" distinction,
  repro command and "Written by" line carried forward as dated sections):
  - `docs/tracking-input-chain.md` <- tracking-input-source.md,
    tracking-input-sampler.md, tracking-input-records.md,
    tracking-numeric-input-route.md, tracking-queued-bank-route.md,
    tracking-input-bank-selection.md, tracking-dispatch-registration.md
    (including its entry-2 correction above, carried forward as-is).
  - `docs/tracking-screen-state.md` <- tracking-screen-stack.md,
    tracking-registry-mode-state.md, tracking-mask-namespaces.md,
    tracking-ui-event-router.md
  - `docs/tracking-sampler-payload.md` <- tracking-sampler-consumers.md,
    tracking-liveview-payload.md

  `tracking-entry-research.md` and `tracking-feature-plan.md` were left as
  separate files (decision/plan documents, referenced by name elsewhere).
  Old filenames were deleted (`git rm`); links elsewhere in the repo were
  updated to the new filenames, except inside `docs/facts.md`'s numbered
  `F-###` entries, which that file's append-only rule forbids editing in
  place -- those links now point at deleted filenames. See the
  docs-consolidation PR body for the specific `F-###` entries affected.
- **Date:** 2026-10-16.

## 4. Tracking property 0x2021 payload and consumer-search limits

- **Original claims:** tracking-input-chain.md described the post payload
  as 1 to 4 bytes and inferred a simple toggle/lock shape; its later
  literal-immediate search was summarized as no explicit test of `0x2021`
  anywhere. The upward trace also summarized the state-machine index as
  subtracting `0x20000`.
- **Correction:** the property uses a structured record with length
  4..512, subtype/status-like fields and an optional tail, stored in a
  516-byte buffer. A generic object lookup compares register-loaded ids;
  a separate query wrapper explicitly excludes `0x2021` using two
  subtractions. The state-machine table index is `event - 0x20001`.
  Neither the old small values nor the new notification route identifies
  AE-L/AF-L. Details and private verification are in
  [the table-dispatched consumer section](tracking-input-chain.md#2026-10-16-table-dispatched-consumer-and-structured-payload-for-0x2021).
- **Date:** 2026-10-16.

## 5. Tracking cluster dispatcher edges were assigned to the wrong ids

- **Original claim:** the control-cluster section assigned `0x2020` to
  `0x103a2a9c`, `0x2021` to `0x103a31a6`, and `0x2087` to
  `0x103a341a`; Codex's first continuation carried the wrong `0x2021`
  assignment forward. It also attributed the global `+0x48` callback
  branch to `0x2006`.
- **Correction:** checked branch destinations give `0x2020` ->
  `0x103a31a6`, `0x2021` -> `0x103a341a`, and `0x2087` ->
  `0x103a2a9c` -> `0x103a29ca`. The `+0x48` callback is for `0x2002`;
  `0x2006` is ignored by this dispatcher. The subtype handler gates on
  an operation flag preserved from property notifications. The
  command/reply interpretation replaces the earlier small-lock-state
  lead; AE-L/AF-L and tracking identity remain unverified. See
  [the corrected map and simulator evidence](tracking-input-chain.md#2026-10-16-bounded-menu-probe-and-corrected-commandreply-map).
- **Date:** 2026-10-16.

## 6. The tracking control cluster is a BLE controller path

- **Original claim:** the `0x2020`/`0x2021`/`0x2087` cluster was called
  a real, non-Bluetooth lead for physical AE-L/AF-L delivery.
- **Correction:** diagnostic references in the actual handlers identify
  a BLE camera-controller module and its authentication sibling. This
  was found by following the new property path, independently of the
  already-retired HCI lead. It is not evidence of physical-button
  provenance. The corrected build decision retires it as a physical
  AE-L/AF-L lead without claiming remote control code cannot share
  downstream camera operations. See
  [diagnostic provenance and the build decision](tracking-input-chain.md#2026-10-16-diagnostic-provenance-identifies-a-ble-controller-cluster).
- **Date:** 2026-10-16.
