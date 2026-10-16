# Codex handoff

Rewritten 2026-10-16 by Claude, with the owner's explicit approval to edit
this Codex-owned file (a lane exception, same as PR #50). The previous
version of this file was stale, written before this session and still
pointing at fact numbers below F-050; ignore anything you remember from an
older copy. Read this file, then [facts.md](facts.md),
[project-status.md](project-status.md) and [AGENTS.md](AGENTS.md) before
doing anything.

## Read this first

Main carries facts through **F-095**. Nothing is open on GitHub (no PRs,
no diverging branches). Hardware access stays **NO-GO**
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

## Your lane for this handoff: the live-view-bars hook

This is the one piece Claude is handing to you, because Claude hit the same
safety-classifier stop twice in a row researching firmware code-insertion
mechanics and the owner decided Codex should try it instead, not because the
research itself is unusual for this project (hundreds of similar read-only
decodes went through fine all session). The full design doc is
[xpan-bars-design.md](xpan-bars-design.md) — read it in full; this section
only summarizes.

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
   Claude did not get far into this before hitting repeated stops; there is
   essentially no prior art here to build on beyond what F-088 through F-094
   already establish.
2. Once a candidate spot exists, tie it to the three trigger moments
   (F-089, F-090) and to the `0xc1811d90`-style choice byte, and test it in
   the simulator per the "How we will know it works" checklist in the
   design doc.

Treat this as genuinely open research, not a known dead end — Claude
stopped because of its own tooling limits, not because the question was
shown to be unanswerable.

## Other work in flight (do not duplicate)

Claude is separately and actively researching the saved-RAW/JPEG crop path
in its own worktree (`nikon-savedcrop`, branch
`claude/saved-crop-research`), picking up from the seven callers of the
crop-window builder `0x101d5b36` (F-056, F-057, F-095). That is unblocked
and ongoing — don't start on it; check `project-status.md` for the latest
fact number before choosing your own next fact ID, since both tracks commit
to the same `facts.md`.

## Rules, unchanged

Offline/simulator only. Never touch a real camera. Never commit firmware
bytes, dumps, or patched images, anywhere, ever — this applies doubly to
any work on "a safe place to add instructions," since that research must
stay entirely descriptive (addresses, offsets, constraints) and never
include an actual patch or binary diff. Each PR: fresh branch from `main`,
run the three checks below, one fact per PR where practical, append-only to
`facts.md`. The owner merges everything; you don't merge your own PRs.

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

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
