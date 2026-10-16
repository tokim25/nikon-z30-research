# Replace 1:1 with XPan: what has to change

Written 2026-10-16. This is a plan built from simulator-side reading of the
original firmware. Nothing here has run on a real camera, and hardware stays
NO-GO. It follows the owner's decisions in [user-stories.md](user-stories.md):
XPan takes the place of the 1:1 choice in "Choose image area", for stills,
RAW and JPEG, with only the XPan crop kept.

## What can stay as it is

The 1:1 choice is stored as the value 4, has the menu item id `0x123c`, the
label string 1454 and the availability code `0x1003` (F-072 to F-077). If XPan
keeps all four, the menu itself, the "i" quick menu slot and the rule for
when the choice is offered keep working without code changes.

## What has to change (data)

1. **The label.** Replace the text of string 1454 with an XPan label of the
   same length (F-062 to F-064). English first; other languages can keep "1:1".
   The size lines beside the labels also show 1:1 numbers and need the same
   care.
2. **The size records.** In the per-area table, the fifth slot of each group is
   1:1 and holds square sizes (F-054). Each needs a 65:24 rectangle that fits
   inside the DX readout.
3. **The shared size lists.** The block of size lists has a square entry in the
   1:1 slot of each list (F-055). Each used list needs a matching rectangle. The
   crop-window builder centers whatever sizes it is given and has no square
   test (F-056).

## What is not solved

- **Live view.** The on-screen bars work only when switched on by a test tool
  and stay on in menus. Tying them to the stored value 4 is not done.
- **The saved file.** A centered 5200 by 1920 setting worked in the simulator,
  but no cropped RAW or JPEG has been seen, and the image processor may not
  accept the shape.
- **Other square assumptions.** The photo-editing crop tool forces width equal
  to height for 1:1, and about 117 readers of the size block still have to be
  checked (F-054).
- **Frame lines and focus points** must stay inside the strip (owner decision).
- **Applying it.** The recovery plan is still a draft ([recovery-plan.md](recovery-plan.md)).

## Progress in the simulator (2026-10-16)

- The area slot is the first byte of the crop builder's input, and 1:1 gives a
  square window from square records (F-078).
- Repointing the 1:1 records at XPan-shaped ones made the large-size window
  5208 by 1928, close to 65:24, with DX and 16:9 unchanged (F-079).
- The medium and small sizes gave nonsense because my test record was too
  short. With full-length records all three sizes follow (large 5208 by 1928,
  medium 3900 by 1440, small 3906 by 1446); see F-080. Step 1 is done for the
  crop-window builder. It shows nothing yet about live view, capture or saved
  files.

- Setting the stored area byte alone changes nothing on screen and is reset
  within a second, so live view does not follow it and the byte is a mirror of
  a stored setting (F-081). The bars need their own link to the choice.

## Where this leaves the plan (2026-10-16)

- **Saved data and size tables:** a data-only replacement of the 1:1 records is
  enough for the crop-window builder (F-080). The menu already stores the
  value 4 for 1:1, and the snapshot routine carries it to the tables (F-085,
  F-087), so no change to the code that writes the setting is needed.
- **Live-view bars:** nothing in the display path reads the stored value
  (F-033, F-081). Showing the bars for value 4 needs new code, a small hook in
  the live-view path. That is the open "no debugger hook" condition in
  [build-phase-gate.md](build-phase-gate.md) and the main remaining risk.
- **Saved files:** the image processor may or may not accept the shape; the
  simulator cannot settle it.

## Options for the live-view bars (F-088)

1. **Data only, always on.** Edit the stored layer template so the clip flag
   and bounds make the 65:24 strip permanent. No code changes, but the bars
   are not tied to the XPan choice, and they would clip the menus too.
2. **A small hook (new code).** A few instructions that run when live view is
   entered and turn the mask on only when the stored area value is 4. Ties the
   bars to the choice; needs a code patch, which is the open "no debugger
   hook" condition in [build-phase-gate.md](build-phase-gate.md).
3. **Skip the bars in version 1.** Ship the XPan choice, the size tables and
   the label, and treat the on-screen bars as a later addition. The saved crop
   is the main goal.

## Order of work

1. Confirm the three data changes in the simulator, with a fresh run.
2. Tie the black bars to the stored value 4.
3. Test what the simulator can show about a cropped save.
4. Read the remaining readers of the size block.
5. Only then ask whether hardware can be considered.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
