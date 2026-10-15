# Why the stock refresh draws no border rectangles

Date: 2026-10-15. Simulator observation plus static reading, same limits as
[native-dispatch-chain.md](native-dispatch-chain.md).

## Result

In four bounded runs, the three rectangle wrappers (0x10477af2, 0x10477596,
0x10477a5c) were never entered. The reason is a size check inside 0x103c1b54:
the synthetic image fills its region, so every border size is zero.

## Evidence

After a four-pass loop at 0x103c2252, the function tests a stack argument. It
was zero, so the border code runs. That code reads four signed halfwords from
its local frame: left, top, right and bottom of the image rectangle. It draws
a border only if left or top is positive, or if right or bottom falls short of
the width and height held in two other locals.

Captured at that point, all from the synthetic scene:

- Left and top were 0.
- Right was 720 and bottom was 480.
- The compared width and height were 720 and 480.

Every comparison took the skip path. None of the 17 call sites inside
0x103c1b54 was reached, and the four other wrapper entries and backends
(0x10477a88, 0x10477528, 0x104779f4, 0x104773c6) saw no hits either.

## Limits

The 720 by 480 reading describes the simulator's synthetic scene, not a real
camera layout or LCD. Five other call sites reach the wrappers (near
0x1047a390, 0x104b588c, 0x104b59d6, 0x10517afe and 0x10517c5e). Whether any
runs in a reachable state is unknown.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
