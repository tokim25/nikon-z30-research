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
clip-only setter. F-047 traced the chain upward: table slot `0x11fa38fc` -> handler
`0x102ae5e8` (flag at +0x10) -> wrapper `0x10452f34` -> `0x10452d86` ->
initializer. F-048: the flag is the word at `0xc1821c20`, part of a module-wide state
object (about 80 loaders in `0x102ae5a8`..`0x102afca0`). F-049: two static patterns found no writer of that word (negative
result, medium confidence). F-050 decoded the initializer: it copies config +8 into object +0x2c, the
same offset as the F-042 clip flag, so rebuilds may reset the mask (inferred; F-051
confirmed the copy at memory level in the simulator; display effect
unproven: F-052 found a rebuild did not remove the mask on screen, and
object +0x24 went to zero for an unknown reason). Still to do: find the flag writer another way, which event owns the
table slot, and what `0x104ed666`/`0x104ed67a` do; then decide whether any
step is a clip-only path.

The auto-mode classifier denied Claude's own runs of the scan against the
private firmware, so the owner ran it in a terminal. After the owner changed a permission setting on 2026-10-16, Claude's own run succeeded. If a session is blocked
the same way, ask the owner to run it. `$WORK/analysis-env` may already hold
`capstone`; use it instead of a new environment. No firmware bytes are kept
in the repo.

## Update 2026-10-16: XPan as a menu choice

Owner decisions are in user-stories.md. First research (F-053): the "Choose
image area" text sits in a packed UTF-16 string blob near `0x10e88c22`.
Next: find the code that builds the image-area list (look for readers of the
blob near those addresses), and how the "i" quick menu opens that list. Same
read-only method; if a run is blocked, ask the owner to run it. Owner
decision: XPan REPLACES the 1:1 choice (area 4), may keep the "1:1" label
where hard to change. So the work is rewriting what area 4 means, not adding
a list entry. Known obstacles from image-area-tables.md: the 1:1 records
hold square sizes (3712, 2784, 1856 and sensor readout 3728 squared) that
must become 5200 by 1920 style rectangles; the Retouch Trim code forces
width equal to height for the 1:1 slot (separate feature, may be left alone);
one menu interlock is 1:1 specific (F-033). F-054 mapped the table: slot 4 per group of five, records square, 117 direct
callers of the parameter-block helpers at `0x1020bfc8`. F-055 sorted them by helper and decoded the block: size lists with a square
slot 4, purposes unknown. Next: find what the biggest users (helper
`0x1020bfda`, 38 callers; `0x1020bfc8`, 23) do with the sizes, then check each reader of the 1:1 slot
for width-equals-height assumptions, and find the per-area crop-window tables.

## Where things live

Restricted inputs sit under the workspace `work/` folder: the EG module, the
pinned simulator and run folders in `private-inputs/`. Private scripts there:
`native_fill_loop9_private.py` with `robust_call_private.py`,
`menu_retest_private.py`, `geom_probe_private.py` (run name, firmware path),
`dimtable_scan_private.py`. Keep their output private.
