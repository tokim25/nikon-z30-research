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
slot 4, purposes unknown. F-056: the main consumer `0x101d5b36` is a centered crop-window builder keyed
by a byte at input +0x26 (no square test inside it). F-057: seven callers; in the first one the input structure lives at
`[object+0x3a4]+0x208`, so the area byte is at `[object+0x3a4]+0x22e`.
F-058: five stores of that byte; one is a fixed 1, the rest fill a 12-cell grid
in the higher code region (`0x11dc....` to `0x11e7....`). F-059: the grid values come from a text-keyed settings store (`0x11df06b8`).
F-060: 354 `eDSID_` setting names; none mention image area. F-061: the names sit in one pointer table at `0x1204ea5c` onward (ImageSize
at `0x1204ea68`), and the image area is not among them. F-062: the area text is stored per language (about 30 blocks) with no plain
pointers; labels can stay "1:1", an in-place "65:24 (24x9)" would fit.
F-063: strings have no length marker, so an offset or length index exists
elsewhere; same-length label swaps avoid it. Owner wants the "65:24" label
where safe (user-stories.md). F-064: the string index is found (three 36-entry language tables at
`0x112f41e0`, `0x112f4270`, `0x112f4300`; English region index at
`0x10e79dac`); labels are DX 737, 1:1 1454, 16:9 1455. A safety classifier
stopped the last step, a read of the table that lists these numbers
together; the owner approved a narrower read, done as F-065 (the list at `0x11ff2b4c`).
F-066/F-067: nothing points at that list; it sits after two pointer runs (name
tables, 26 and 24 entries) and among packed lists of string numbers. F-068 corrects that: the pointers are focal-length and f-number labels (a
value-list pool), not menu names. F-069: the pool is initialized data, so code uses its RAM copy (stored
address + `0xaf87e36c`); the pool is probably at RAM `0xc187036c` to
`0xc187136c`. F-070: done; 416 pool words and 406 loaders found in a code module from
`0x1030bf08`; `0xc1870e80` (just before the area-label list) is loaded at
`0x1030c880`. F-071: done; the area-label list is loaded only at `0x1030f87a` and
`0x1030f8a8`. F-072: decoded; `0x1030f844` builds the DX/1:1/16:9 choice list (two-pass loop,
filtered by `0x10484d90`, current value is a byte at `+0x15b` of a settings
structure). F-073: literals resolved; item ids `0x123c` (1:1) and `0x123e` (16:9), header
`0x15aa`; the check is a thunk to `0x1052d7c2`. F-074: done; stored values 4 (1:1, code 0x1003) and 2 (16:9, code 0x1004); the
F-075/F-076: the chain is two veneers to a wrapper stub at `0x104270a4` that
passes the code, a pointer and a line number to the shared routine
`0x101993de`, which is the real availability test; `0x1052d7c6` is an event
dispatcher, unrelated. F-077: the chain ends in a generic settings lookup, parked. The concrete plan is
`xpan-replace-1to1-plan.md`; step 1 is done for the crop-window builder: F-078,
F-079, F-080 (full-length XPan records give 65:24 at all three sizes). F-081: the stored area byte
is a mirror reset within a second and live view ignores it. F-082: ten byte stores and
eight loads at offset `0x15b` found. F-083: the mirror byte is
probably copied from `+0x2cc` of a source structure (r8) by the routine around
`0x10367fd2`. F-084: only two byte stores with offset `0x2cc` exist (`0x1019a068`, `0x10367d26`).
F-085: the useful store copies `r8+0x408` into `+0x2cc`, in a routine starting
near `0x10367260`. F-086: the routine has 20 callers and the source byte is stored only by the
settings-store module (`0x11dcd08e`, `0x11dcd14c`, `0x11dcd198`, `0x11dcd674`,
plus a duplicate copy at `0x11e52...`). Next: owner runs a decode around those
stores and the loads `0x11dcd662`, `0x11dcdbfa`, `0x1037416c`, and resolves the
routine's two literal addresses. Avoid write watchpoints on the
simulator link; they left it out of step once. Then what `0x123e` is, then the table that defines "Choose image area" (start from the text at
`0x10e890da`, look for the code or table that references those string ids),
and who writes the area on a menu pick; also note the i-menu slots and the
AE-L/AF-L button setting `Setting_FuncAeAfLockButtonShooting` (a possible
tracking route); read the other six callers, read helpers `0x1020c128`
and `0x1020c17e` and check `0x101d5ad0`, then the other big users (helper
`0x1020bfda`, 38 callers; `0x1020bfc8`, 23) then check each reader of the 1:1 slot
for width-equals-height assumptions, and find the per-area crop-window tables.

## Where things live

Restricted inputs sit under the workspace `work/` folder: the EG module, the
pinned simulator and run folders in `private-inputs/`. Private scripts there:
`native_fill_loop9_private.py` with `robust_call_private.py`,
`menu_retest_private.py`, `geom_probe_private.py` (run name, firmware path),
`dimtable_scan_private.py`. Keep their output private.
