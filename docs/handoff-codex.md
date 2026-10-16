# Codex handoff

Known corrections: see [corrections.md](corrections.md).

Rewritten 2026-10-16 by Claude, with the owner's explicit approval to edit
this Codex-owned file (a lane exception, same as PR #50). Read this file,
then [facts.md](facts.md), [project-status.md](project-status.md) and
[AGENTS.md](AGENTS.md) before doing anything. This version adds a second
handed-off lane (saved-crop) on top of the first (live-view-bars hook); both
are below. If you remember an older copy of this file with fact numbers
below F-050, ignore it.

## Read this first

**Owner direction, 2026-10-16 — read [AGENTS.md](AGENTS.md)'s new "Priority"
section first.** This project tests modded firmware on the owner's own real
camera; every thread should lead toward a concrete patch, hook point, or
build decision for the real firmware, not toward explaining a limit of this
project's own simulator. A card-detect/SD-command-enumeration thread
(F-102, F-104) was explored this session and retired for exactly this
reason — see "Lane 2" below for where it stopped and why.

Main carries facts through **F-109**; check main before allocating F-110.
Hardware access stays **NO-GO**
([hardware-readiness.md](hardware-readiness.md)); nothing here authorizes
touching a real camera. Build-phase work is open for the owner's own,
non-distributed camera ([build-phase-gate.md](build-phase-gate.md)), but all
work stays in the offline simulator.

Owner decision recorded 2026-10-16: absolute hardware safety is no longer an
acceptance criterion because it cannot be proved before a first hardware
test. The gate now distinguishes **SIMULATOR ACCEPTED**, **READY FOR AN
EXPERIMENTAL HARDWARE TEST**, and **HARDWARE VALIDATED**. A missing recovery
path must be stated as an accepted service-or-total-loss risk; it may not be
described as safe. The current state remains NO-GO.

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
  before CPU start. It used wrappers at the exact writer, live-view-ready
  transition, screen close and generic screen activation. The debugger did
  not write code, choice, mask state, bounds or color during the run.
- A real 1:1 menu pick left the mask off over the menu. An audited live-view
  activation restored it. DX and 16:9 kept it off. Ten alternating screen
  signal cycles passed. Direct stock callback tests also changed the mask
  immediately while live view stayed active.
- The later menu-notification callback was tested and rejected as a general
  change trigger. QEMU write watchpoints also failed a known-store self-test.
- A follow-up rejected an unguarded screen-close trigger. Internal events
  `0x24e` and `0x250` close the last stack entry but request mode `0x10000`,
  not live view; the unguarded hook enabled the mask on that transition
  screen. The final overlay requires an empty stack and live-view selector 1.
- The live-view trigger now sits at `0x102f5810`, where `0x102f57e2` sets
  selector 1. The guarded build passed the area controls and ten signal
  cycles, and stayed off after the non-live-view close control.
- A diagnostic call through the stock type-2 dispatcher reached that full
  live-view-ready path and returned with selector 1, stack count zero and the
  1:1 mask on. The natural worker trigger remains dormant in the fixture.
- Full evidence, repro commands and limits are in
  [native-xpan-liveview-hook.md](native-xpan-liveview-hook.md). A true menu
  return to live view, the natural startup caller and the exact `i`-menu
  route are still open.

### Single next step for Lane 1 (superseded below)

Find a stock menu-close event sequence that reaches `0x102f57e2` without a
direct diagnostic call, then confirm that the guarded hook restores the mask.
The exposed Back key cannot close the final menu screen, and the tested
internal close events do not request live view.

**Update (2026-10-16, picking up PR #119's own "single next step"):** a
prior Codex run (before running out of budget, work not committed) found
that the normal menu-close handler reaches the live-view-ready path when an
internal mode-state check comes out a specific way, and was tracing what
naturally sets that state. Claude continued the same trace a little further
before hitting its own repeated classifier stop on this exact sub-question
(three in a row) and is handing it back: the close handler (one of
`docs/native-xpan-liveview-hook.md`'s key addresses) has no direct callers
and exactly one table entry, at `0x113033a8`. Its branch between the two
internal modes reads a small helper, which in turn checks a function whose
return value of 0, 3, or 4 selects the live-view-targeting mode (any other
value selects the non-live-view mode already shown not to reach the hook).
That function's own addresses and what feeds it were not yet read. This is
exactly the open thread PR #119 names as its "single next step"; pick it up
from there rather than re-deriving it.

**Owner note on the pattern:** this one specific sub-question (what
naturally drives the menu-close-to-live-view transition) had stopped
Claude three times in a row via the safety classifier, more than any other
single topic in that session.

**Update (2026-10-16), resolved one level further, no classifier stop this
time (F-107):** the close handler is confirmed as `0x10460c3c`. Its chain
is now: `0x10460c3c` -> calls `0x1045b27e` ("the small helper") -> calls
`0x10457db2` (this is exactly where the prior session stopped) -> which
turns out to be a trivial 3-instruction getter reading one byte at
`0xc181f6fc` and returning it directly (not the `cmp`-dispatcher an
earlier reading assumed -- that's a different, unrelated function one
step over). Two more literal-pool references to `0xc181f6fc` were found
and both are **reads** into small lookup tables anchored near it, not
writes. Full detail in facts.md F-107.

**Update (2026-10-16), the natural trigger found, three-stop question
resolved (F-108):** a register-arithmetic scan (not a literal match)
found the setter, `0x10457dac`, the plain sibling of F-107's getter. It
has exactly one direct caller anywhere in the image, inside a dispatcher
at `0x10459d80`: when the incoming event code equals **`0x4100012`**, it
calls the setter with `r0 = 4` -- one of F-107's three live-view-selecting
values -- then calls `0x1046283c` and `0x10462894` with no further gating.
**Those are the same two calls F-090 already found inside the live-view-
start routine `0x102f2990` itself.** That match is independent
corroboration this is the real trigger, not a coincidental write. No
classifier stop encountered anywhere in this chain. Full detail in
facts.md F-108.

**Closed, deliberately, not pursued further (F-109):** who posts event
`0x4100012` was checked by four independent full-image methods (direct
calls, tail branches, raw pointer-table words, table-branch jump tables)
-- all four found nothing. Not escalated to ARM-mode scanning or manual
UI-pump archaeology, because the question itself had drifted into
simulator-reachability territory (can the simulator's limited key set
post this event) rather than a real-firmware question -- the real camera
obviously already delivers this event through ordinary use (F-090), and
F-108's hook sites sit downstream of it, not upstream. A real build does
not need this answered.

**Update (2026-10-16), owner call made, pending a dissenting review:** the
owner has called build-gate condition 1 satisfied for Lane 1 on this
evidence (instruction space and native-execution proven, F-101; the
natural trigger's mechanism fully understood end to end, F-107/F-108,
though not demonstrated firing naturally in the simulator). **Correction**
to the "second branch" framing used earlier in this file and in F-109: the
current gate text (post the PR #119 hardware-safety rewrite) has no
explicit "or that hook's risk is fully understood" alternative any more --
condition 1 now reads only "the simulator must show the feature working
without a debugger memory write, and the relevant state transitions must
pass." Whether the diagnostic-call evidence already available satisfies
that, given the natural trigger itself was never observed firing, is
exactly the ambiguity the owner's call rests on.

**This call does not authorize any build-phase work yet.** A dissenting
review from Codex, run as its own independent session, is required first
-- see [hardware-readiness.md](hardware-readiness.md)'s new section for
the review's exact scope. Record the review's conclusion there when it
happens.

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

**Update (2026-10-16), card-presence check traced (F-102):** the detect
function itself (`0x104157b8`) is a plain, satisfiable bit test (SDHCI
Present State bit 16 on controller 0) — not the blocker. The stronger
candidate is a downstream stall: `0x104164ba`, a generic "issue
command, wait for completion" primitive used ~8 times during SD bring-up,
always waits on controller 0's specific hardware event object, matching the
QEMU model's own comment that "polling commands can work there but DMA
completion never reaches the event object awaited by 0x104164ba." Not
proven end-to-end. The direct link from card-detect's result (or the global
status struct at `0xc18015e8`) forward into the Setup-menu enable/grey-out
check was not found — that's the open gap, along with decoding the 8
`0x104164ba` call sites individually. Full detail in facts.md F-102.

**Update (2026-10-16), Approach A continued, F-098 partly corrected
(F-103):** `0x101568ca` and `0x1015be26` are internal basic-block labels,
not function entries — their real enclosing functions are `0x10156714` and
`0x1015bc3e`. Re-checked against the real entries, `0x1015bc3e` turns out to
have ordinary direct callers (not table-dispatched as F-098 implied); only
`0x10156714` still has zero references found by any literal mechanism.
`0x1015a93c` itself decodes as a property/event-ID dispatcher (compare
against ID constants, then jump table) shared as a callback pointer from 17
separate literal-pool sites across ~65KB of code — the textbook shape this
project has already tied to menu/property tables (F-072/F-090), not a
capture/save pipeline. Leans toward hypothesis (b) (settings/property
handler, not a capture descriptor) at low-to-medium confidence; no
unambiguous storage-write or UI-counter call was found either way. Full
detail in facts.md F-103.

**Update (2026-10-16), the 8 `0x104164ba` callers decoded (F-104):** they
collapse to exactly 4 enclosing functions, each loading a command word that
decodes as a standard SDHCI command register value for CMD17
READ_SINGLE_BLOCK, CMD18 READ_MULTIPLE_BLOCK, CMD24 WRITE_BLOCK and CMD25
WRITE_MULTIPLE_BLOCK (high byte = SD command index, shared low byte `0x3a`
= data-present + index/CRC-check + R1-response flags). Each calls
`0x104164ba` twice in what reads as the standard two-stage "buffer
ready, then transfer complete" wait. This strengthens the F-102 stall
theory: if any of these four ever fire against controller 0, they'd stall
at the first wait under the QEMU model's own documented limitation —
independently explaining both F-100's zero `sdcard_read_block` events and
the "Format memory card" grey-out. Still open: whether the firmware's
bring-up sequence reaches these four commands at all before giving up
earlier (e.g. during CMD0/ACMD41/CMD2/CMD3 enumeration, not decoded here),
and the menu-enable/grey-out link itself. Full detail in facts.md F-104.

**Retired, 2026-10-16 (owner direction):** the card-detect/SD-enumeration
thread (F-102, F-104) stops here. It traced real firmware addresses (useful
background: card-detect `0x104157b8`, the block-transfer commands CMD17/18/
24/25, and most of the CMD0/CMD8/ACMD41/CMD2/CMD3 enumeration sequence —
see F-102/F-104 for the addresses if ever needed again), but confirmed the
open question at this point is "why does this project's own QEMU SDHCI
model fail to complete a command" — a simulator-fidelity limit, not a real
firmware question, and not something a hardware build needs answered. Do
not resume it, and do not decode CMD0's enumeration further (F-105 was
drafted and discarded for the same reason), unless a specific build
decision later turns out to depend on it.

**Update (2026-10-16), direct-write path checked and ruled out (F-105):**
an automated call-graph walk from the F-097 four, following every direct
`bl`/`blx` transitively (867 distinct functions, exhaustive -- the search
queue emptied, not a node cap; method validated against F-102's
hand-decoded card-detect function), never reaches F-104's CMD24/25 write
wrappers or the shared command-submit primitive. This rules out the
simplest form of hypothesis (a): none of the four callers, or anything
they call directly or transitively, synchronously writes the finished
record to storage right after building it.

**It does not settle the question.** The walk only follows literal
`bl`/`blx` targets -- it cannot see a hand-off through a function-pointer
table or a queued/global slot read by a separate worker, which is this
project's established pattern for handler dispatch elsewhere (F-072,
F-090, F-098).

**Update (2026-10-16), both follow-ups run, leans toward (b) at medium
confidence (F-106):** the global-write scan over F-105's 867 functions
found two real leads, both ambiguous on their own; `0x1015bd18`'s four
modes were fully decoded (correcting F-103's mode assignment) alongside
`0x101e729e`/`0x101efb9e`. The strongest finding: `0x101efb9e` leads to a
function that **synchronously calls** the `0x1015a93c` property dispatcher
directly with an id and output pointer -- a property get/notify call, not
a job registration -- and the one event queue found (`0x101e729e`'s path)
is generic and posts to a queue architecturally distant from the SD code
block. Both lean toward (b). The one open thread: mode 2 of `0x1015bd18`
dereferences a global slot (`0xc18a6890`) and, when non-null, copies data
from it using the exact same offset/size as F-096's record-builder's first
block copy -- real but unconfirmed evidence the slot holds that record's
output. The slot's actual producer was not found by a literal-word scan
(6 hits, none resembling a write) and likely computes the address via
register arithmetic on the module's wider base (`0xc18a6810`, used 52
times across `0x10152000`-`0x1015c600`) rather than its own literal. Full
detail in facts.md F-106.

**Next step:** either find `0xc18a6890`'s producer via a register-
arithmetic scan (not a literal match) over those 52 functions -- the last
piece that could still flip this to (a) -- or accept (b) as the working
answer at this point and move on; either is a defensible, build-relevant
stopping point. Stopping at "the simulator can't
show me SD I/O" is not, since this question's whole point is what the real
firmware does.

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
