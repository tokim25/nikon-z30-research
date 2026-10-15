# Menu and live-view events share a router

Reviewed 2026-10-15. Read-only code analysis; no simulator controls were run.

Stock code has a shared router that chooses an event handler based on a state
byte. The menu object and the object used by the simulator's live-view setup
have different handlers. In state 1, event type 3 leads to separate menu and
live-view routines. This gives us a concrete live-view path to study.

It does not show a successful button press or tracking activation. The event's
data format, required state and link to an OK-button press remain unknown.

## What the code shows

An object here is a block of state and function pointers. The router reads a
byte at object offset `+0x74`. We call that byte the selector because it chooses
which handler to use. The byte is not a simple on/off flag.

| Code location | Observed in static code | Limit |
| --- | --- | --- |
| Shared router `0x104b912c`–`0x104b9148` | Reads the selector and loads a function pointer from `object + 0x78 + 4 × selector`. If the pointer is nonzero, calls it with the event type and payload originally passed to the router. | This is a code path, not proof that a physical button reaches it. There is no selector range check in this routine. |
| Selector setter `0x104b9116`–`0x104b9126` | Stores the selector byte. An input value of zero also clears object fields `+0x94` and `+0x98`. | Changing this state has other effects. No setter call or manual state change was attempted. |
| Live-view worker call at `0x102f2c22` | When a flag test passes, calls the shared router with object `0xc1821d44`, event type 3 and a pointer to a stack buffer at `sp + 8`. | Delivery is conditional. The buffer's format and lifetime have not been mapped. Type 3 is an internal event category; it has not been identified as an OK-button code. |

The worker's flag test checks bit 1 of its saved flags. The code that produces
those flags and fills the payload still needs study. A pointer to a stack
buffer is not interchangeable with a menu event number.

## The two objects and their handlers

The simulator setup supplies menu object `0xc182e688` and live-view object
`0xc1821d44` to the same startup routine. These names describe how the harness
uses them; their full native object contracts remain unresolved.

The module's initialization record maps source `0x11f81c94` to RAM
`0xc1800000`, for length `0xf8258`, through copy routine `0x1002006c`.
That record and bounded inspection of the copy routine support the following
initial pointer map. It was not checked in running RAM.

| Setup object | Initial data source | State 0 handler, field `+0x78` | State 1 handler, field `+0x7c` |
| --- | --- | --- | --- |
| Menu `0xc182e688` | `0x11fb031c` | `0x103cf512` | `0x103cf78e` |
| Live view `0xc1821d44` | `0x11fa39d8` | `0x102f61d2` | `0x102f79ac` |

The stored Thumb function pointers include a low-bit flag. The table above
shows code addresses with that flag removed. It records selected fields, not
a claim about the objects' total size.

Both state-1 handlers use a table to choose among event types 0–19. Resolving
those tables gives these type-3 paths:

| Setup | State-1 type-3 path | Observed continuation |
| --- | --- | --- |
| Menu | `0x103cf78e` → case at `0x103cf7ca` → `0x103cf696` | Passes the payload into a processing routine. Conditional paths later call menu handler `0x103ce96e` at `0x103cf712` and `0x103cf71c`. |
| Live view | `0x102f79ac` → case at `0x102f79e2` → `0x102f7448` | Passes the payload into a different, larger routine with several state checks and helper calls. No tracking action has been identified there. |

The type-3 branch was decoded from table entries, then checked at its actual
destination. Treating the table itself as instructions would produce false
code. Some earlier exploratory linear windows crossed tables or literal pools;
those apparent instructions were not used as evidence.

## State requirements still matter

Both initialization paths select state 0: menu at `0x103ce5b0` and live view
at `0x102f2a04`. The live-view state-0 handler accepts only event types below 3;
type 3 returns without taking the larger input path.

Other live-view code selects state 1 at `0x102f5810`, and state 4 at
`0x102f61b0`. The conditions for reaching those writes have not been traced.
State 4 selects a field outside the two shown above; its handler was not mapped
in this pass. We cannot assume that drawing a live-view frame means state 1
is active, or that setting it manually would reproduce a normal transition.

This is a verified static connection between the router and distinct handlers.
Normal event delivery, button identity, eligibility, cancellation and reticle
changes remain unverified. No address here is a proposed diagnostic call.

## Reproduce privately

The verified module is 33,939,514 bytes, mapped at `0x10020000`, with SHA-256
`8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
The newly written verifier checks identity, the data mapping, selected pointer
fields, router instructions, table destinations and state-write sites. It uses
Capstone 5.0.6 and does not run firmware code. Use a fresh output name:

```sh
WORK=/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work
"$WORK/analysis-env/bin/python" "$WORK/codex_ui_route_verify_private.py" \
  --output "$WORK/private-inputs/codex-ui-route-review-01"
```

The verifier passed in `private-inputs/codex-ui-route-verified-02`. Raw decode
and exploratory outputs stay outside Git. The simulator remained clean at
revision `0ba0c3547ccbec09e7c861eaca35db8e82795f15`. Two Codex subagents
checked the source/object mapping and routing claims independently. The private
reproduction depends on owner-supplied files; it is not a CI test.

## Single next step

Trace how the live-view worker builds its type-3 payload and what
`0x102f7448` expects to read from it. Include the conditions that select state 1.
Do this before proposing any simulator input call.

Written by Codex in collaboration with Tony Kim, with independent Codex subagent review.
