# Session handoff: native XPan guides

Date: 2026-10-15. Update this file whenever a workflow is in progress.

## State

Offline simulator work only. Uncommitted: nothing is staged, and the user has
not declared integration ready. The checkout started at 014ab00 on `main`.

Findings so far:

- [Dispatch chain](native-dispatch-chain.md): refresh request to render setup.
- [Border gate](native-border-gate.md): why stock draws no border rectangles.
- [Rectangle call](native-rectangle-call.md): one native call reaches 0x105124de, but no pixels appear in the frame dump.

First acceptance item (native guides) is not verified.

## Looser stage approved by the user

The user approved a looser simulator stage: host-written pixels in a third
layer, composited by native code ([guide-layer-compose.md](guide-layer-compose.md)).
Toggle on, off and on again worked. It is not native drawing, and the
original acceptance wording still stands for the final milestone. Remaining
reliability work: menu and focus-graphic states, more toggle cycles, and
calibrating the one-to-two-row vertical offset. Private script:
`guides_loop_private.py`.

## Where things live

Restricted inputs stay outside this checkout, under the chat workspace's
`work/` directory: the verified EG module, the pinned simulator checkout, and
run folders such as `private-inputs/call-c`. Private scripts there:
`rect_trace_wide.py`, `rect_call_private.py` (arguments: run name, y, height,
colour), `frame_compare_private.py`, `disasm_private.py`. They print raw
observations, so keep their output private.

## Next step

Native guides now work in the simulator: see
[native-guides-simulator.md](native-guides-simulator.md). The earlier blocker
was a queue-and-wait gate (global 0xc1808744) that deadlocked a call made from
the display worker's own breakpoint. Private script that produced the result:
`native_fill_loop8_private.py` (arguments: run name, 0, 0, color, cycles).
The call hangs are fixed: the debugger call helper now checks which thread
stopped (`src/nikon_z30_research/guest_call_safe.py`, fact F-013). The private
loop using it is `native_fill_loop9_private.py` with `robust_call_private.py`.
Repeats, colors, alpha and thickness are checked. Still open: menu states
(issue #8) and a call site that needs no debugger (issue #9). The loop is a
debugger hook, not a deployable mechanism.

## Constraints

No hardware, no firmware edits, no installable output. Do not commit or
publish until told.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
