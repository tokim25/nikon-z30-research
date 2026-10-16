# User stories: what the owner should be able to do

Written 2026-10-16. The user is the owner, shooting with their own Nikon Z30.
Each story says what you do, what you should see, and when it counts as done.
"Status" is where the research stands today. Nothing here has run on a real
camera.

## Shooting with XPan

**Story 1: turn XPan on and off.**
As a photographer, I switch XPan on and off quickly so I can use it only when
I want it.
- Done when: one action I choose turns it on, the same action turns it off,
  and turning it off returns everything to normal.
- Status: works only in the simulator, switched by a test tool. Which action
  (a button, a menu item) is **not decided**; see Questions.

**Story 2: frame the shot in XPan.**
As a photographer, I see solid black bars at the top and bottom of live
view, so I know exactly what the photo will include.
- Done when: the bars are black, the strip left over is a 65:24 shape, and
  the picture inside stays smooth and sharp.
- Status: works in live view in the simulator.

**Story 3: use the menus with XPan on.**
As a photographer, I open a menu and read it without bars covering it, then
go back to live view and the bars are back.
- Done when: no bars cover any menu, and live view returns to XPan.
- Status: **not working.** The bars stay on and can cover the menu.

**Story 4: the photo is saved in XPan.**
As a photographer, the photo I take is recorded in the same 65:24 crop I
saw, so I do not have to crop it later.
- Done when: I open the saved file on my computer and it is a 65:24 image
  that matches what I framed, with the right size in its file details.
- Status: **not shown.** The camera's capture settings can be set to the
  right size in the simulator, but no cropped saved photo has been seen.

**Story 5: both kinds of file.**
As a photographer, this works for the file types I shoot.
- Done when: it works for the file types listed in Questions.
- Status: not started.

## Subject tracking

**Story 6: start tracking with one press.**
As a photographer, I press AE-L/AF-L once and the camera starts following my
subject, the same as its own tracking does.
- Done when: one press shows the tracking box and the camera follows.
- Status: **not shown.** The button's signal is mapped inside the camera,
  but no one has shown it reaching tracking.

**Story 7: stop tracking.**
As a photographer, I press the button again (or use the normal way) and
tracking stops cleanly.
- Done when: the tracking box goes away and nothing is left stuck.
- Status: not started.

**Story 8: no surprises where tracking cannot work.**
As a photographer, in modes where tracking is not available, the press does
nothing harmful.
- Done when: the camera stays stable and the picture is unchanged.
- Status: not started.

## Living with it

**Story 9: nothing else changes.**
As a photographer, everything else works as before: other buttons, menus,
battery, shooting speed, lenses.
- Done when: the checks in Questions find no difference.
- Status: not tested.

**Story 10: I can get back to normal.**
As an owner, if I do not like it, I can return my camera to Nikon's original
software.
- Done when: a written, checked way back exists.
- Status: **not met.** A draft is in [recovery-plan.md](recovery-plan.md) and
  it is honest that it is not credible yet.

**Story 11: it stays mine.**
As an owner, I apply it myself, on my own camera only, and nothing of
Nikon's is shared.
- Done when: the result lives only on my computer and camera.
- Status: rule already in place; nothing built to apply yet.

## Questions for you

1. **Turning XPan on and off (Story 1):** which action do you want? For
   example a button, a menu item, or a custom control.
2. **File types (Stories 4 and 5):** RAW only, JPEG only, or both?
3. **Tracking with AE-L/AF-L (Story 6):** this button normally locks exposure
   and focus. Are you fine losing that, or should it need a long press or a
   mode?
4. **Video (not covered):** should XPan apply to video, or stills only?
5. **Still the plan:** photos keep the XPan crop only, with no way to get the
   full frame back from the same file? Say if you want the full frame kept.

## What stays true

No real camera is touched until the recovery plan is credible and you say go
separately. See [hardware-readiness.md](hardware-readiness.md) and
[roadmap.md](roadmap.md).

Written by Claude (Opus 5.5) in collaboration with Tony Kim.
