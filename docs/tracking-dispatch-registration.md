# Tracing the queued-bank route upward: an event dispatcher and its registration

Date: 2026-10-16, corrected 2026-10-16 (see "Correction" below). Read-only
static analysis of verified C1.20, continuing tracking-queued-bank-route.md's
"reviewed upstream chain" (`0x10379f00`, `0x10379a68`) one level further to
the owning state-machine step function. An attempt to find that function's
dispatch-table registration did not hold up on re-verification; see the
correction in "The enclosing state-machine step and its registration" below.
This is not a native simulator observation and does not establish incoming
transport, physical button identity, or tracking activation.

## The event-code dispatcher

`0x10379a68` is a generic event-range dispatcher. It reads a 16-bit event
code from offset `0` of an incoming struct and compares it against a base
of `0x2006`:

- Delta `0` (code `0x2006`): copies several fields from the incoming
  struct (offsets `0`, `2`, `3`, `4`, `5`, `6`, `0xa`, `0xb`, `8` --
  the shape of a touch/duration input descriptor), computes a timing
  constant (`0x1e`, `0x3c`, `0x78`, or `0xffff` depending on one of those
  fields), and calls a **registered callback** loaded from
  `[0x10379c9c-literal-base + 0x54]` via `blx r2` -- i.e. this specific
  branch is itself extensible through a separate registration slot, not
  hardcoded.
- Delta `1` (code `0x2007`): a separate branch, not decoded in this pass.
- Delta `0x7d` (code `0x2083`): calls `0x103a3d14` directly -- this is
  tracking-queued-bank-route.md's tracking-queue handler.
- Other deltas, bounded by a second comparison against a literal-loaded
  constant, fall through to `0x103a37dc` or a shared default path at
  `0x10379c24`.

This confirms code `0x2083` is handled as one case among several in a
general-purpose event-code range (`0x2006`-`0x2083`+), alongside what
looks like a touch-input case (`0x2006`) with its own separate callback
registration. Observed static decode, high confidence for the dispatch
shape; the meaning of codes `0x2006`/`0x2007` and the other deltas was
not pursued.

## The enclosing state-machine step and its registration

`0x10379a68` has exactly one caller: `0x10379f00`, itself one case
(`ldr r0, [r4, #0x14]; bl 0x10379a68`) inside a much larger function whose
real entry is `0x10379d5a`. That function reads a mode/state value from
`[r0 + 0x10]`, subtracts `0x20000`, bounds-checks the result against
`0x1b` (27), and dispatches through a Thumb `tbb` jump table -- a
textbook state-machine "step" function with ~27 cases, of which our case
forwards a sub-object at `[r4+0x14]` into the event-code dispatcher above.
Most of the other cases call similarly-shaped single-purpose helpers
(`0x1037aae2`, `0x1037ab88`, `0x1037abd0`, `0x103a2ac6`, `0x103a3efc`,
etc., not decoded here).

`0x10379d5a` itself has no direct `bl`/tail-`b.w` caller anywhere in the
image -- consistent with this project's established pattern of table-
dispatched handlers (F-072, F-090, F-098, and Lane 1's F-107/F-108 close
handler). This zero-direct-reference finding is solid (direct instruction-
level decode and a full-image literal/branch xref scan) and still stands.

**Correction (2026-10-16), the "{handler, type-id} table" claim below was
wrong and is withdrawn:** an earlier pass of this file read a raw
pointer-word hit at `0x1037a2c4` (Thumb-tagged, resolving to `0x10379d5a`)
immediately followed at `0x1037a2c8` by the word `0x20016`, and concluded
this was a clean `{handler, type-id}` registration-table entry, because
`0x20016`'s shape happened to match the `[x] - 0x20000` subtraction
`0x10379d5a` performs on its own input. Direct Thumb disassembly of the
enclosing region (capstone, same firmware, SHA-256 confirmed) shows this
is wrong: `0x1037a2c4`/`0x1037a2c8` sit inside the literal pool for the
small dispatch-case function entered at `0x1037a20c`, which cleanly
returns at `0x1037a294` with `movs r0, #1; pop {r3, r4, r5, pc}`. None of
that function's own `ldr rX, [pc, #imm]` literal loads resolve to
`0x1037a2c4` or `0x1037a2c8` when computing `((insn_addr+4) & ~3) + imm`
for each one -- they resolve elsewhere in the same pool (`0x1037a2d4`
through `0x1037a2f4`). The bytes immediately around the pointer/tag pair
(`0x1037a2a4`-`0x1037a2c0`) decode as ASCII-looking string fragments, not
other table entries, confirming this is scattered literal-pool data for
one or more small neighboring functions, not a standalone registration
table with defined boundaries. The pointer-to-`0x10379d5a` word at
`0x1037a2c4` may still be a genuine literal reference to the handler used
by *some* unidentified caller elsewhere (literal pools do hold real
function-pointer constants), but no evidence ties it to a coherent
`{handler, type-id}` table, and no code anywhere was found that computes
a base address that would walk through it as one.

**Where this leaves it:** the registration/reachability mechanism for
`0x10379d5a` itself remains unresolved. The apparent table pattern spotted
near `0x1037a2c4`/`0x1037a2c8` was investigated and found to be literal-
pool data for an unrelated function, not a real registration entry. The
zero-direct-reference finding above is the only solid fact about how this
handler is reached; nothing else found so far explains it.

## What this establishes and what it does not

This is new ground beyond tracking-queued-bank-route.md, which stopped at
naming `0x10379f00` and `0x10379a68` without decoding either. It traces
the queued tracking-event route one full level further: from the
mask-table consumer, up through the event-code dispatcher, up through the
owning state-machine step function -- which itself has zero direct
references anywhere in the image. It does **not** reach a physical input
source, an input-pump/message-loop caller, a working registration
mechanism for `0x10379d5a`, or anything that names AE-L/AF-L specifically.
The physical-identity gap tracking-input-bank-selection.md and
tracking-queued-bank-route.md both flagged remains fully open.

Confidence: high for the bounded code shapes and addresses reported
(direct instruction-level decode) and for the zero-direct-reference
finding on `0x10379d5a`; the registration/reachability mechanism for that
function is unresolved (see the correction above) -- no confidence claim
is made about it either way.

Not yet done: finding how `0x10379d5a` is actually reached, given it has
zero direct callers and the apparent nearby registration-table pattern
turned out to be an unrelated function's literal pool (a register-
arithmetic scan over candidate table-walker code, the same technique that
resolved F-108's slot producer, is the next thing to try, not another
literal-word search), and decoding the `0x2006`/touch-input branch's
separate callback-registration slot, which may be a more direct route to
a physical input descriptor than the `0x2083` tracking branch is.

Method: read-only static decode (capstone, Thumb) and literal-pool/direct-
branch xref scans (`rom_xrefs.py`), SHA-256 checked first; addresses,
offsets and event/type codes only, no firmware bytes recorded.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim, continuing
Codex's tracking-queued-bank-route.md and tracking-input-bank-selection.md
(owner-approved lane work, same basis as the handoff-codex.md exception
used throughout this session).
