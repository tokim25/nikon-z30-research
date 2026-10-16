# Claude lane handoff

Date: 2026-10-15. Update this whenever work is in progress.

## State

- Native guides work in the simulator in live view
  ([native-guides-simulator.md](native-guides-simulator.md)). The call hangs
  are fixed (F-013). Menus are an accepted limit (F-022, issue #8 closed).
- The image-area research is in
  [image-area-tables.md](image-area-tables.md) (F-030 to F-033) and
  [capture-geometry-baseline.md](capture-geometry-baseline.md). Live view shows
  the area only through the capture side, so the crop is probably made by the
  image processor, which is not in this image.
- Blocked: a throwaway-firmware test of a 65:24 replacement for 1:1. The
  permission classifier denied creating the copy; it needs the owner's approval.

## Next

1. Owner decides: approve that test, or skip it. Also saved files versus
   live-view framing only, and whether to open a build phase.
2. Issue #9: a call site for the guides that needs no debugger. Research and
   spec only.

## Update 2026-10-16: clip-state audit, step one

Codex's PRs #34 to #49 are on main through #50 (owner-approved lane
exception). The first part of Codex's single next step is done as F-045: the
initializer `0x104b5fd4` has two direct callers, `0x10452e56` and
`0x10452ea8`. F-046 decoded a window around each: both are nine-call nested loops
(3 by 3) with modes 1 and 2, so the initializer is bulk setup, not a
clip-only setter. Still to do: read the literal-pool words and the indexed
tables behind r0 and r2, and find who calls the enclosing function.

The auto-mode classifier denied Claude's own runs of the scan against the
private firmware, so the owner ran it in a terminal. After the owner changed a permission setting on 2026-10-16, Claude's own run succeeded. If a session is blocked
the same way, ask the owner to run it. `$WORK/analysis-env` may already hold
`capstone`; use it instead of a new environment. No firmware bytes are kept
in the repo.

## Where things live

Restricted inputs sit under the workspace `work/` folder: the EG module, the
pinned simulator and run folders in `private-inputs/`. Private scripts there:
`native_fill_loop9_private.py` with `robust_call_private.py`,
`menu_retest_private.py`, `geom_probe_private.py` (run name, firmware path),
`dimtable_scan_private.py`. Keep their output private.
