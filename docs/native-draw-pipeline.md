# How the simulator turns UI drawing into the frame

Date: 2026-10-15. Simulator runs and its source, unchanged firmware.

## Pipeline

The saved frame is the animated preview composited with two overlay planes
(color and alpha). The stock UI draws into a 720 by 480 RGBA staging buffer,
and a later GPU "YUV draw" converts it into the overlay. The UI redraws
continuously: zero the staging plane, draw, convert.

## Experiments

- The rectangle fill (0x105124de, then 0x1053e40a) did not write the staging
  buffer. It sets dirty bits in the drawing context through 0x1055ea48, so it
  looks deferred until a flush that has not been identified.
- Calling the wrapper from the idle checkpoint, and from inside a stock
  refresh at 0x103c2478, changed no visible pixel.
- Changing two local border extents in 0x103c1b54 (data only) makes stock code
  call 0x10477596 twice, at y = 0 and y = 373, each 720 wide and 107 tall.
- Those requests carry color 0, mode 0 and state byte 3. Zero color clears the
  overlay, so they are not visible guides. Setting the color to opaque white
  in that request still changed no visible pixel.

## Compose step

Per stock refresh, 0x104787f2 runs twice, called from 0x103bc556. Its r0 is a
descriptor whose second word is 1 and whose third word is a source layer
address: first 0xd0959600, then 0xd045f200 (the library fill's target). Each
call matches one simulator "YUV draw" log line, so this is the layer-to-overlay
conversion, not a drawing call. A third layer that this function composited
would show on screen, but pixels placed there by the host would not count as
native drawing.

## The flush

The library's no-argument flush is 0x1050a306 (from static analysis, with
runtime observation of its call chain). The compose function 0x104787f2 calls
it at its start, twice per refresh. It emits the pending display list as a
type 10 job through 0x10514ebe, queued at 0x1058217e and run by a worker task.

A dump of uploaded tables confirmed the fill is not lost: the next table grew by
216 bytes, and its first draw was mine (white, target 0xd045f200). It ran
before 16 stock draws in the same table, which cleared it. The simulator
logged no unsupported command.

## Open

The fill needs to be recorded after the stock draws and before the second
compose. The only tried route, calling the wrapper from a breakpoint in that
gap, never returned: the call stopped in the idle thread, probably blocked on
a lock or worker handshake. Calls from the idle checkpoint do return, but land
too early in the cycle.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
