# Guide color, thickness and stress results

Date: 2026-10-15. Simulator only, unchanged firmware. Mostly from a helper's
roughly 60 runs; I confirmed the black result myself.

## Color

The request color word is RGBA: red in the top byte, alpha in the low byte.
Earlier "black does not draw" findings read it as ARGB, which gave alpha 0.

- Alpha FF draws exact color within about 2 per channel. 0x000000FF is pure
  black, so black letterbox bars render.
- Alpha 0 draws nothing. Other alpha values blend over the scene by the
  standard formula (checked to the byte for two colors).

## Thickness

Bars of 1, 2, 4 and 8 rows landed on the intended rows, full width.

## Stress

Two sessions ran 12 and 13 on/off cycles with no stale or partial bars. A bar
appeared at the next stop after a call and vanished at the third stop after
the last.

## Reliability problem

- About 10 to 15 percent of calls were followed by a hang with no breakpoint
  stop. Sessions lasted 1 to 23 calls. A call-free control showed none.
- Many hangs followed a stray pause stop in a RAM loop that appears to write
  flash commands. The root cause is unknown.
- In both full sessions, one 1.7 second stop briefly lost the lower bar and
  left a small lasting scene change.

So this per-cycle hook is not reliable for long sessions.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
