# One native call of the rectangle wrapper

Date: 2026-10-15. Simulator only, unchanged firmware. This is an explicit
diagnostic call at the established InitTask checkpoint, not passive evidence.
The request bytes were synthetic and written by this project.

## What the call did

0x10477af2 takes r0 as a pointer to a 28-byte request. It copies the request,
asks 0x103bd330 for the surface size (720 by 480), and replaces the vertical
origin with surface height minus y minus height. It then calls 0x10477a88.

With a 720 by 60 request at y = 380, observed in order:

- 0x10477a88 received r1 = 480.
- 0x104773c6 took its direct branch.
- 0x1050aad6 received x = 0, y = 40, width 720 and height 60. The converted y matches 480 minus 440.
- It obtained a nonzero handle from 0x1050b9ea and entered 0x105124de with the same four values.

The call completed and the firmware hash was unchanged.

## What did not happen

The frame showed no change outside the moving color bars (rows 161 to 319).
That was true for a thin bar, a white bar and a no-draw control. The colour
helper 0x104772a6 reads alpha from the top byte, so the white request was
opaque by that reading.

## Open

Whether 0x105124de draws to a layer the frame dump shows, and whether a
later refresh presents or clears it, is not yet known. The mode and flag
fields were guesses.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
