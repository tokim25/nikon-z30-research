# Research roadmap

This page tracks progress on two camera features we are studying, step by
step, inside a simulator. A simulator is a program that acts like the
camera's hardware, so we can test ideas without a real camera. Nothing here
has been installed on, or connected to, an actual Nikon camera.

## The two features

**A framing guide.** Lines on the screen that show a wide, panoramic crop (a
65:24 shape) while shooting, so a photographer can compose for that crop
before taking the picture.

**Subject tracking.** A way to turn on the camera's own subject-tracking
with one button press, instead of the usual multi-step menu process.

## What we have proven

- The framing guide now works. The camera's own built-in drawing code draws
  the guide lines on screen, in the live shooting view, inside the
  simulator. We did not paste the lines on top from outside; the camera's
  own software drew them. See [the simulator results](native-guides-simulator.md).
- An early bug that made this unreliable, where a background process could
  randomly stall a command, is now fixed and tested.
- The guide does not yet work inside the camera's menu screens, only in the
  live shooting view. We checked this carefully and stopped trying, rather
  than force it.

## What we are still researching

- Which button could turn on subject tracking with one press. We have found
  that the camera recognizes a physical switch for this, but we have not yet
  traced the full path from a button press to the tracking feature turning
  on. See [the shared findings log](facts.md): every finding there is marked
  as confirmed or as a reasoned guess.
- Where, inside saved photos, the camera stores the exact pixel area it
  captured. See [the image-area research](image-area-tables.md).

## What is off-limits

- No real camera is ever touched. All testing happens on a computer, inside
  the simulator described above.
- Nikon's own camera software is never published in this project; see the
  README's [boundaries section](../README.md#boundaries).
- Turning this research into something a person could install on a camera
  is a separate, later decision that has not been made. For now, this
  project only studies and documents how the camera works.

## Where things stand overall

As of October 2026, the framing guide works in the simulator's live shooting
view, with known limits around menu screens. Subject tracking is still at
the research stage: we know a lot about how the camera handles buttons and
events, but the full path from a button press to the tracking feature has
not been confirmed.

For day-to-day status and the next task, see [the simulator-work
handoff](handoff.md) and [the tracking-research handoff](handoff-codex.md).

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
