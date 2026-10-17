# Instruction-level audit of the live-view-bars hook

Date: 2026-10-16. Reviewer: Claude (Sonnet 5.5), one reader, at the owner's
request. This is a partial answer to build-gate condition 3 (code layout,
instruction mode, branches, register handling, stack use, return paths). It
is not a hardware safety result, and a second reader has not confirmed it.

## What was reviewed

The private generator for the guarded overlay (the guarded build script
named in [native-xpan-liveview-hook.md](native-xpan-liveview-hook.md)). I ran its own
encoder functions, disassembled every routine and every rewritten branch
with a disassembler, and compared them with the original code around each
hook site and each call target. I did not rerun the simulator. No firmware
bytes, overlay bytes or disassembly are recorded here; this file uses
addresses and prose only.

## Planned changes (for condition 2)

Five new routines in zero-filled spans, one data change and four rewritten
sites:

- New code at `0x1002d78c` (mask), `0x1002d7b4` (close wrapper),
  `0x1002d80c` (screen-activation wrapper), `0x1002d830` (writer wrapper),
  `0x1002d860` (guard) and `0x1027f468` (live-view-ready wrapper).
- Four rewrites of one 4-byte branch each, at `0x102355f4`, `0x102355c0`,
  `0x102f5810` and `0x1008d3fe`.
- A 12-byte data change at `0x1073dbe4 + 8`: the layer template's clip flag
  and bounds. This is a data edit to the firmware image, not code, and any
  patcher and checksum review must cover it separately.

## Checked and correct

- **Encoding.** Every branch, call, literal load and conditional branch
  decodes to its intended target. Literal-pool words are aligned and sit
  after each routine's return. The generator asserts offset ranges, and the
  longest call is about 4 MB, well inside the 16 MB limit.
- **Mode.** All new code is Thumb-2. Every call target begins with a valid
  Thumb prologue. Rewrites are same-size (4-byte to 4-byte), so no
  neighbouring instruction moves.
- **Space.** The routines fit their spans (40 + 12 of 52, 36 + 8 of 52,
  28 of 32, 16 of 24) and do not overlap. The generator refuses to run
  unless the spans are zero and the firmware hash matches.
- **Writer wrapper.** The original instruction replaced is the function's
  final multi-register pop. The wrapper calls the guard, then runs that same
  pop, which reloads all registers and the return address from the stack.
  This is an exact equivalent and cannot disturb the caller.
- **Live-view-ready wrapper.** It calls the original function first, saves
  and restores its return value, and then runs the guard, so the selector is
  already set when the guard reads it. The code after the call overwrites
  or does not use the registers the wrapper clobbers.
- **Close wrapper.** The code after the original call reloads every register
  it uses, so clobbering the return value and scratch registers is safe.
- **Screen-activation wrapper.** It reproduces a tail call as call, pop, and
  return, and preserves the two argument registers the target needs and the
  return value.
- **Guard and mask.** The guard's read of the screen-stack count is a
  side-effect-free memory read (no lock, no call into the kernel). The mask
  routine saves what it uses, writes one flag word and one color pair into
  RAM, and calls a short leaf routine.

## Findings

None of these is a defect that, on this reading, would crash the camera by
itself. They are ordered by how much they matter.

1. **Shared helper may clear the mask too often (functional, medium).** The
   screen-activation wrapper clears the mask flag for every activation that
   is not the live-view layer. The hooked block is shared, so overlays that
   appear during live view (focus display, shooting info, zoom) could pass
   through it and blank the bars until the next live-view start. The
   simulator has none of those overlays, so this is untested. This is the
   most likely visible bug on a real camera.
2. **Register `r2` is clobbered on the tail call (low).** The wrapper
   preserves the first two registers, which is what the call site sets, but
   `r2` is overwritten before the target runs. The target is a kernel
   service call stub, whose argument count I could not confirm. The call
   site setting only two arguments suggests two, so the risk is low, but
   saving two more registers removes the question.
3. **Stack alignment (low).** The close wrapper and the guard push a single
   register. In the close wrapper that leaves the stock callback running
   with the stack 4 bytes off 8-byte alignment. The rest of the firmware
   keeps 8-byte alignment. Plain loads and stores tolerate this on this
   core; instructions with an alignment hint would not. Pushing a second
   register fixes it. The simulator did not trap, but it did not run this
   path through the real callback either.
4. **The guard never clears the mask (design note).** If the area changes
   while the guard's conditions fail, the flag keeps its old value until the
   next screen activation or live-view start. The activation wrapper covers
   most cases, so this matters only if the `i` menu does not use the
   activation path. That route is untested (the simulator has no `i` button).
5. **Hard-coded addresses.** The screen object, selector, flag and choice
   byte are fixed RAM addresses of this exact build. That is fine only
   because the patcher accepts one verified original.

## Not answerable from this review

- Whether the camera accepts a modified image at all: checksum, signature or
  update-time validation. This is the largest hardware risk and is condition
  2 and 4 territory.
- Whether the zero-filled spans stay writable and unclobbered at run time,
  and are not covered by integrity checks.
- Calling context of the hooks on a running camera (thread, lock and
  interrupt state, timing). The close wrapper has only run through a
  non-admitting control; no path where the guard admits has run through it
  naturally.
- The identity of the kernel service behind finding 2.

## Suggested changes before any build

Pushing `r0`-`r3` plus one more register in the activation wrapper (finding
2), pushing a second register in the close wrapper and guard (finding 3),
and deciding whether finding 1 needs a stricter test (activate only for the
live-view layer, never clear for others). All three are small and can be
re-tested in the simulator.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
