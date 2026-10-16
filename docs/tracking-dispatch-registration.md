# Tracing the queued-bank route upward: an event dispatcher and its registration

Date: 2026-10-16. Read-only static analysis of verified C1.20, continuing
tracking-queued-bank-route.md's "reviewed upstream chain" (`0x10379f00`,
`0x10379a68`) one level further and reaching a dispatch-table registration.
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
handler). A raw pointer-word scan found it registered, Thumb-tagged, at
`0x1037a2c4`, immediately followed at `0x1037a2c8` by the word `0x20016`
-- a `{handler, type-id}` pair, where `0x20016`'s shape (`0x2` + a 16-bit
sub-id) matches exactly the `[x] - 0x20000` subtraction this same function
performs on its own input, suggesting `0x20016` is this handler's
registered object-type/class ID in some larger type-to-handler table. The
immediately surrounding words (`0x1037a2a4`-`0x1037a2c0`) do not fit the
same clean stride-8 pattern (one region decodes as ASCII-looking bytes
rather than a pointer/tag pair), so the full table's boundaries and entry
count were not established. A direct literal-word search for the table's
likely base addresses (`0x1037a2c0`, `0x1037a2a4`) found no referencing
code, meaning whatever walks this table computes its base through
register arithmetic rather than loading either address as its own
literal -- the same pattern already seen in F-106 and F-108's unresolved
slot producers in the XPan research.

## What this establishes and what it does not

This is new ground beyond tracking-queued-bank-route.md, which stopped at
naming `0x10379f00` and `0x10379a68` without decoding either. It traces
the queued tracking-event route one full level further: from the
mask-table consumer, up through the event-code dispatcher, up through the
owning state-machine step function, to that function's own registration
in a type-keyed dispatch table. It does **not** reach a physical input
source, an input-pump/message-loop caller, or anything that names AE-L/AF-L
specifically. The physical-identity gap tracking-input-bank-selection.md
and tracking-queued-bank-route.md both flagged remains fully open.

Confidence: high for the bounded code shapes and addresses reported
(direct instruction-level decode); low for any claim about what object
type `0x20016` represents or what ultimately posts the incoming struct
that reaches `0x10379d5a`.

Not yet done: finding what computes the base of the `{handler, type-id}`
table containing `0x1037a2c4`/`0x1037a2c8` (register-arithmetic scan, not
a literal match -- the same technique that resolved F-108's slot
producer), and decoding the `0x2006`/touch-input branch's separate
callback-registration slot, which may be a more direct route to a
physical input descriptor than the `0x2083` tracking branch is.

Method: read-only static decode (capstone, Thumb) and literal-pool/direct-
branch xref scans (`rom_xrefs.py`), SHA-256 checked first; addresses,
offsets and event/type codes only, no firmware bytes recorded.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim, continuing
Codex's tracking-queued-bank-route.md and tracking-input-bank-selection.md
(owner-approved lane work, same basis as the handoff-codex.md exception
used throughout this session).
