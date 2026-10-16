# Research roadmap

Updated 2026-10-16. All results so far come from offline analysis and a
simulator. No real camera was connected or changed.

## The goal, in plain words

Two things, both from the owner:

1. **XPan framing you can see and keep.** The wide 65:24 look shows in live
   view, and the camera also records every photo in that same crop. A guide
   on screen alone is not the goal.
2. **One-press subject tracking.** Pressing the AE-L/AF-L button starts the
   camera's own subject tracking. Losing the button's lock job is fine.

First version: stills only, RAW and JPEG, only the XPan crop kept.

## 0. XPan as a menu choice (how you turn it on)

You want XPan to be a choice in the camera's "Choose image area" menu,
reached from the "i" quick menu, for stills only, applied to RAW and JPEG.
The owner chose to replace the 1:1 choice with XPan (it may keep the 1:1
label), which is simpler than adding a new one. The menu text has been
located (F-053); the code that builds the list is not found yet. Finding how
the camera builds that list, and how the "i" menu opens it, comes first,
because the on-screen bars and the saved crop should both follow from that
one choice. Decisions are in [user-stories.md](user-stories.md).

The concrete change list is in [xpan-replace-1to1-plan.md](xpan-replace-1to1-plan.md).

## 1. XPan in live view (what you see)

**Works in the simulator.** The camera's own drawing code puts black bars on
the top and bottom, leaving a 65:24 strip. Two independent runs passed, and
turning the bars off restores the normal picture.

**Not finished.** The bars stay stuck when a menu opens and can cover menu
graphics. We traced which part of the camera sets up the screen layers (PR
#51 to #60 notes, facts F-045 to F-052). One idea, rebuilding the layer to
clear the bars, was tested and did not work: the switch turned off but the
bars stayed. Next is finding another way to clear them when a menu opens.

## 2. XPan in the saved photo (what gets recorded)

**Not shown yet.** This is the less proven half of the goal.
- A simulator test showed the camera's capture settings can be set to the
  XPan size, 5200 by 1920 pixels, an exact 65:24 shape.
- That does not show a saved photo with that crop. We do not yet know
  whether the saved file, RAW or JPEG, would come out cropped, or whether the
  file's own size notes would be right.
- The simulator's image-processing part is only partly modeled, so it may not
  be able to prove this at all.

**Next:** find where the camera decides the size of the saved file, and see
whether the simulator can show a cropped save. Do not treat a masked preview
or a size number as proof of a cropped photo.

## 3. One-press tracking (the AE-L/AF-L button)

**Allowed, but nobody is working on it right now.** The owner un-paused it.
The button exists on the body and has its own signal inside the camera, and
several paths for button signals are mapped. Nobody has yet shown that
signal reaching the tracking feature. A visible tracking box, canceling it,
and refusing it in modes that cannot track are all still unproven.

## Where things stand overall

- All of Codex's pending work is merged. Nothing is waiting.
- No combined feature test exists, and no installable firmware exists.
- Hardware remains NO-GO. A recovery plan is drafted but not credible yet
  ([recovery-plan.md](recovery-plan.md)).
- What you should be able to do on the camera: [user-stories.md](user-stories.md).
- See [the Codex handoff](handoff-codex.md), [the Claude handoff](handoff.md)
  and [the readiness checkpoint](hardware-readiness.md) for details.

Written by Claude (Opus 5.5) and Codex in collaboration with Tony Kim.
