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
- **Corrected in:** this same file, `docs/tracking-dispatch-registration.md`
  (PR on `claude/tracking-table-correction`), which replaces the table claim
  with an honest statement that the registration/reachability mechanism for
  `0x10379d5a` remains unresolved.
- **Date:** 2026-10-16.
