# Native 65:24 guides in the simulator

Date: 2026-10-15. Simulator only, unchanged firmware.

## Result

Two 2-row white bars appear at screen rows 107 to 108 and 371 to 372, the
edges of a centered 266-row strip (65:24). Stock firmware drew them: the
rectangle wrapper 0x10477af2 ran with synthetic requests. The host wrote no
guide pixels.

## How it was run

Each UI cycle, a debugger loop stops at the second stock compose (0x104787f2,
source layer 0xd045f200) and calls the wrapper twice (y = 371 and y = 107,
height 2, color 0xffffffff).

- That slot is after the stock draws are recorded and before the compose
  flush emits them. Earlier slots let stock clears wipe the fill.
- When a global at 0xc1808744 is nonzero, the wrapper queues to the display
  worker and waits. The breakpoint stops that worker, so the loop sets the
  global to 0 per call and restores it.
- Drawing lands on the overlay unflipped: for screen row R and height h,
  request y = 480 minus R minus h.

## Observed

- On: both bars full width. Off: gone within two stops. On again: back.
- Outside the moving color-bar band, only the four bar rows differed from a
  control frame. The firmware hash never changed.

## Limits

The loop is not a deployable hook, and it hangs in about 10 to 15 percent of
calls ([guide-color-and-stress.md](guide-color-and-stress.md)). The 720 by 480
area is the synthetic scene's. Menus do not work ([guides-ui-states.md](guides-ui-states.md)).

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
