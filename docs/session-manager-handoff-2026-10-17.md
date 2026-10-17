# Session-manager handoff, 2026-10-17

From: Claude session manager. To: Codex session manager.
Read first: [owner-direction-2026-10-17.md](owner-direction-2026-10-17.md),
[project-status.md](project-status.md), [handoff-codex.md](handoff-codex.md).

## Owner direction

- The saved-crop question is **not a blocker**. It may only be settled by an
  on-camera test, which needs the owner's separate go-ahead.
- Hardware remains NO-GO. Commits and pushes happen only when the owner asks.
- Claude takes static research and tidying. Codex takes simulator runs,
  pushing and merging, and the checker work.
- The token wrap-up trigger stays at 90% weekly usage.

## Current state

- **Codex's uncommitted work (about 30 files on `codex/firmware-preflight-plan`)
  is NOT ready to commit.** Its fact numbers F-135 to F-140 collide with facts
  already on main (main is at c58ac95). Renumber first, rerun the checks, then
  commit. This is the first thing to do.
- **Pushed research branches, not merged, owner decides:**
  - `claude/lane3-family-search-2ded1d` (F-130): not found.
  - `claude/lane2-filename-trace-981f75` (F-131, F-132): not found.
  - `claude/eloquent-napier-52e1c8` (F-133, F-134): not found.
  Check each fact number against main before any of them lands.
- **Checker review (read-only, no edits):** the checksum handling in
  `package_container.py` is sound. One test gap: nothing tests that an edit
  changing no bytes is rejected. The code does reject it. The test cannot be
  written on a main-based branch yet, because `patch_audit.py` and its tests
  exist only in Codex's uncommitted work. Add it after Codex commits.
- **Workspace cleanup:** three finished Claude work folders removed; their
  branches kept. Other branches (`claude/dissent-lane1-gate`,
  `claude/hook-instruction-audit`, `codex/tracking-property-dispatch`) and
  Codex's own work folder were left alone.

## Feature status (plain)

- On-screen crop lines: work in the simulator; not verified on a real camera.
- Saved cropped files: not established statically; an on-camera test item.
- Tracking focus button: no code path found statically.
- Remembered choice, quick menu, info-strip readout, recovery: not verified.

## Next steps for Codex

1. Renumber the uncommitted F-135 to F-140 work against main, then verify and
   commit when ready. Ask the owner before pushing or opening a pull request.
2. Add the pointers to `owner-direction-2026-10-17.md` in `handoff-codex.md`
   and `project-status.md`, and state "saved crop = on-camera test item, not a
   blocker" in both.
3. After step 1, add the no-op edit test to the patch-audit test file.
4. Review the three research branches above and report fact-number clashes.

## Decisions waiting on the owner

- Whether to merge the three research branches.
- Whether to clear the older branches that are already merged into main.
- Whether to strictly enforce the rule that commits happen only when asked.
