# Design: black bars that follow the XPan choice

Written 2026-10-16. This is a paper design. It says what the bars should do,
not how the code does it. Nothing here has run on a real camera, and hardware
stays NO-GO. It follows the owner's decision that the bars follow the XPan
choice ([xpan-replace-1to1-plan.md](xpan-replace-1to1-plan.md)).

## The goal in one sentence

When XPan is the selected image area, live view shows a solid black bar above
and below a 65:24 strip, and when any other image area is selected, live view
looks exactly like the original camera.

## When the bars are on

| Situation | Bars |
|---|---|
| Still shooting, live view, XPan selected | On |
| Still shooting, live view, DX or 16:9 selected | Off (original look) |
| Any full-screen menu open | Off, so nothing is covered |
| Image area changed from the "i" menu while live view stays on screen | Update at once: on for XPan, off for anything else |
| Back from a menu to live view with XPan selected | On again |
| Playback of a photo | Off |
| Movie mode | Off in version 1 (stills only) |
| Camera switched off and on with XPan selected | On when live view appears |

## Owner requirement (2026-10-16)

The owner will change the image area from the "i" menu while live view stays
on screen, so the bars must turn on or off right away when the choice changes,
not only the next time live view starts. That makes "the area changes" a
required trigger moment, not an optional one.

## What must never happen

1. The bars must not cover a menu, a warning or a message.
2. The bars must not change what DX or 16:9 look like.
3. The camera must not freeze, restart or show a corrupted picture when XPan is
   selected or deselected, or when a menu opens and closes.
4. The focus points, frame lines and readouts stay inside the strip (owner
   decision). If they cannot, version 1 hides the ones that fall outside.
5. Nothing about the saved photo depends on the bars. The bars are only a
   guide; the saved crop comes from the size tables.

## What we already know (facts, in plain words)

- The camera can draw the bars with its own drawing code, after one flag, one
  shape and one color are set on one screen layer. It keeps them on without
  being redrawn (F-042).
- The bars stay on when a menu opens, because nothing clears them (F-044).
- The screen layers are built once at startup from a stored template (F-088),
  not when the image area changes.
- The stored image-area value is a mirror that is refreshed about every
  second, and live view ignores it today (F-081).
- The choice itself already works end to end for sizes: picking 1:1 stores the
  value 4, and that value reaches the size tables (F-080, F-087).

## The parts of the change

1. **Know the state.** Read the stored image-area value (4 means XPan) and
   whether live view is the active screen.
2. **Turn the bars on or off.** On: set the flag, shape and color on the
   live-view layer. Off: clear the flag.
3. **Run at the right moments.** When live view starts, when the image area
   changes, and when the camera returns from a menu. Not on every frame.
4. **Stay out of the way.** Do nothing in menus, playback and movie mode.

## How we will know it works (simulator only)

Each check runs in the simulator with memory restored afterward, and the
firmware file hash is rechecked.

1. Selecting XPan turns the bars on within one second; deselecting turns them
   off.
2. Opening and closing a menu removes the bars and brings them back.
3. DX and 16:9 pictures are byte-for-byte unchanged from the baseline.
4. Ten on/off cycles in a row leave no leftover bars and no stuck state.
5. The screen layer stack and memory use are the same as the baseline after
   the cycles.

## Open questions

1. **Where do the three moments (live view starts, area changes, return from a
   menu) happen in the camera's code?** Two candidates found (F-089): the
   point where live view is activated, for "live view starts", and the generic
   activate step, for "return from a menu". "The area changes" has no
   candidate yet. F-090 adds that each screen object has a table of handlers
   chosen by its selector, which is data, so live view starting can be reached
   by a table entry. If changing the area from the "i" menu leaves live view
   in place, the bars may need to be updated at that moment too.
2. **Is there a safe place to add a few instructions?** The camera's software
   has no obvious spare space, and adding code means changing the image. This
   is build-gate condition 1.
3. **Can the focus points be limited to the strip?** Unknown.
4. **Does the image processor draw its own live-view frame?** If it does, the
   picture may already be cropped or may fight the bars (F-033).

## How the area change can be tested

Writing bytes into the camera's settings structures cannot imitate an area
change: both the mirror and the source are rewritten from something deeper
within a second (F-081, F-091). Driving the simulated menu to the pick itself
also hangs (F-092): the simulator could reach the "Choose image area" screen,
but confirming the 1:1 choice did not complete, even with the thread-aware
call helper. This moment can be tested by driving the menu, but the pick
hangs about half the time and must be retried (F-093). When it returns, the
stored choice changes, and a byte at `0xc1811d90` follows it (0 for DX, 1 for
1:1, 2 for 16:9). The earlier chain through the mirror bytes was wrong and is
being redone.

## What this does not cover

Flashing, applying the change to a real camera, and the recovery plan. Those
stay behind the build gate and need the owner's separate go-ahead
([build-phase-gate.md](build-phase-gate.md), [recovery-plan.md](recovery-plan.md)).

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
