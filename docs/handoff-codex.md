# Codex handoff

Rewritten 2026-10-16 by Claude, with the owner's explicit approval to edit
this Codex-owned file (a lane exception, same as PR #50). Read this file,
then [facts.md](facts.md), [project-status.md](project-status.md) and
[AGENTS.md](AGENTS.md) before doing anything. This version adds a second
handed-off lane (saved-crop) on top of the first (live-view-bars hook); both
are below. If you remember an older copy of this file with fact numbers
below F-050, ignore it.

## Read this first

Main carried facts through **F-100** when this branch started. F-101 is the
live-view hook finding on `codex/xpan-liveview-hook-space`; check main before
allocating F-102. Hardware access stays **NO-GO**
([hardware-readiness.md](hardware-readiness.md)); nothing here authorizes
touching a real camera. Build-phase work is open for the owner's own,
non-distributed camera ([build-phase-gate.md](build-phase-gate.md)), but all
work stays in the offline simulator.

The owner's goal, restated plainly, is in
[user-stories.md](user-stories.md) and [roadmap.md](roadmap.md): an XPan
(65:24) choice that replaces "1:1" in "Choose image area", live view shows
black bars that track that choice, and the saved RAW/JPEG is actually
cropped. The concrete data-level plan is
[xpan-replace-1to1-plan.md](xpan-replace-1to1-plan.md).

Both lanes below were handed to you because Claude hit a genuine wall for
each — a repeated safety-classifier stop on one, and the simulator's actual
functional limits on the other — not because either question was shown to
be unanswerable. Treat both as open research.

## Lane 1: the live-view-bars hook

Claude hit the same safety-classifier stop twice in a row researching
firmware code-insertion mechanics; the owner decided Codex should try
instead. The full design doc is [xpan-bars-design.md](xpan-bars-design.md)
— read it in full; this section only summarizes.

**What's proven:**
- The camera can draw a persistent black-bar mask on one screen layer with
  one flag, one geometry and one color (F-042, F-044).
- Those layer settings come from a stored template copied at startup
  (F-088), not from the image-area choice.
- Two of the three trigger moments the bars need (live view starts, return
  from a menu) have found candidate code locations (F-089, F-090); "the
  area changes" does not yet.
- The image-area pick can now be driven through the real simulated menu
  (F-093) — it hangs on the OK key about half the time and must be retried,
  but when it returns the choice really persists. A byte at `0xc1811d90`
  follows the pick (0 DX, 1 for 1:1, 2 for 16:9); its readers/writers are
  not found (F-094). **Important correction**: an earlier chain built on
  three other bytes (F-081 through F-087) turned out to be wrong when tested
  against a real driven pick — those bytes stay 0 regardless. Don't trust
  that old chain; F-093/F-094 supersede it.

**What's blocked (the actual ask):**
1. Find where in the firmware a safe place exists to add a handful of new
   instructions that run at the three trigger moments and toggle the layer
   mask based on the stored image-area choice. This is build-gate condition
   1 ("the simulator shows the feature working without a debugger hook, or
   that hook's risk is fully understood" — `build-phase-gate.md` line 33).
2. Once a candidate spot exists, tie it to the three trigger moments
   (F-089, F-090) and to the `0xc1811d90`-style choice byte, and test it in
   the simulator per the "How we will know it works" checklist in the
   design doc.

### F-101 result on `codex/xpan-liveview-hook-space`

- The exact property writer is at `0x1008d38c`, with the choice-record store
  at `0x1008d3fc`. The final byte at `0xc1811d90` is 0 for DX, 1 for 1:1 and
  2 for 16:9. The older value-4 statement describes the callback argument,
  not this stored byte.
- Four zero-filled candidate instruction spans were found and checked at
  their real ARM/Thumb boundaries: `0x1002d78c..0x1002d7bf`,
  `0x1002d80c..0x1002d83f`, `0x1002d860..0x1002d87f`, and
  `0x1027f468..0x1027f47f`.
- A private QEMU loader overlay placed synthetic new code in those spans
  before CPU start. It used wrappers at the exact writer, live-view start
  and generic screen activation. The debugger did not write code, choice,
  mask state, bounds or color during the run.
- A real 1:1 menu pick left the mask off over the menu. An audited live-view
  activation restored it. DX and 16:9 kept it off. Ten alternating screen
  signal cycles passed. Direct stock callback tests also changed the mask
  immediately while live view stayed active.
- The later menu-notification callback was tested and rejected as a general
  change trigger. QEMU write watchpoints also failed a known-store self-test.
- Full evidence, repro commands and limits are in
  [native-xpan-liveview-hook.md](native-xpan-liveview-hook.md). The natural
  menu exit, natural startup caller and exact `i`-menu route are still open.

### Single next step for Lane 1

Drive a natural return from the real image-area menu under the same loader
overlay and confirm that the generic screen-state wrapper restores the mask
without an audited activation call.

## Lane 2: saved-crop (does a saved RAW/JPEG actually come out cropped?)

Claude worked this in its own worktree (`nikon-savedcrop`, branch
`claude/saved-crop-research`, now idle and available to reuse or ignore),
facts F-095 through F-100. Two different approaches were tried and both
hit real limits; a third angle is the open suggestion below.

**Approach A: trace the crop-window builder's callers toward a save path.**
Of the builder `0x101d5b36`'s seven callers (F-057), six build small
display/menu info structs (F-095). The seventh, `0x101d5de8` inside a
function at `0x101d5c54`, is different: it assembles one large record
(growing past `0x328` bytes) combining the crop geometry, bit-depth/size
math (`0x101dc204`, dividing 24 bits across 1/2/3/6 components — F-096),
and copied device-config blocks. It has exactly four direct callers in one
tight code region (F-097), three sharing a shape: a capability check keyed
on a per-area id byte, a prepare call, the record build, then a size pair
copied from `base+0x2b00+0x4c` into the finished record. **This is
genuinely ambiguous between two explanations and nothing found so far
picks one**: (a) a capture/save request descriptor, or (b) a
"shots-remaining-at-this-quality" UI estimator, which needs the same
ingredients (geometry + bit depth + per-mode math) but never touches
storage. F-098 found two of the three next-outer callers are reached only
by pointer/table dispatch (weak lean toward UI, not conclusive).

**Approach B: test it live instead of reasoning about code shape.**
Three simulator runs with a breakpoint on the record builder and all four
callers, across menu screens most likely to show a shots-remaining count
plus a full menu-tab sweep, got zero hits (F-099) — but the simulator's key
set has no shutter/capture button and no info-overlay button at all, so the
capture-triggered half of hypothesis (a) can't be tested through normal
input either way. Separately, attaching a synthetic blank SD card with SD
trace enabled showed the controller sees a card insert, but the firmware's
own "Format memory card" menu item stays greyed out and zero SD read/write
commands ever happen (F-100) — something in the firmware's card-presence
check rejects the synthetic card before any file I/O could occur, closing
off the live-observation angle structurally, matching what the simulator's
own README already said about photo/movie recording being out of its
supported scope.

**Suggested next angle, not yet tried:** rather than continuing to chase
Approach A's ambiguity or Approach B's dead end, trace the firmware's
card-presence check itself (what makes "Format memory card" greyed out) —
if it's a simple flag the simulator can be made to satisfy, Approach B
might become viable after all. Separately, forcing a direct call into one
of the four F-097 callers with synthetic-but-plausible register values
(more invasive than anything tried, less certain to mean something) was
floated and not attempted. Either is a reasonable starting point; use your
own judgment.

## Rules, unchanged

Offline/simulator only. Never touch a real camera. Never commit firmware
bytes, dumps, or patched images, anywhere, ever — this applies doubly to
any work on "a safe place to add instructions" (Lane 1), since that
research must stay entirely descriptive (addresses, offsets, constraints)
and never include an actual patch or binary diff. Each PR: fresh branch
from `main`, run the three checks below, one fact per PR where practical,
append-only to `facts.md`. The owner merges everything; you don't merge
your own PRs. Check `project-status.md` for the next free fact number
before choosing your own, since both lanes share one `facts.md`.

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 .github/scripts/check_artifacts.py
python3 .github/scripts/check_byte_dumps.py
```

Private WORK (firmware, pinned simulator, private helper scripts) lives at
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`,
confirmed and untouched by this handoff. If the auto-mode classifier blocks
a read-only firmware scan, the owner can run it in their own terminal and
paste the output back — that unblocked this exact kind of work for Claude
repeatedly this session.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.
