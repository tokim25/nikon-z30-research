# Live-view event data and the path into state 1

Reviewed 2026-10-15. Read-only code analysis; no firmware code was run.

The live-view input path needs more than an event number. Its builder prepares
a 188-byte region, and the reviewed parsers also use records stored elsewhere.
The header can choose a stored-record path rather than supply a new button
action. We have not identified an OK-button record or a tracking-start action.

We also found a stock code path from state 0 to state 1. That closes part of
the state question from [PR #15](https://github.com/tokim25/nikon-z30-research/pull/15).
It does not prove that the simulator reaches that state during normal startup.

## What builds the event data

The builder starts at `0x102f2ad2`. It is called at `0x102f2cd8` by the
live-view worker loop at `0x102f2ca8`. The earlier plan named `0x102f2990` as
the likely builder, but that routine returns at `0x102f2a94`. Reading the code
separated initialization from event building; the earlier assumption was wrong.

The builder uses a stack buffer starting at `sp + 8`:

| Part | Observed producer behavior | Meaning and limit |
| --- | --- | --- |
| First 4 bytes | Starts at zero. The builder writes 1 only after helper `0x10460dac` returns nonzero, its first output word is nonzero, and saved flag bit 1 was previously clear. It also sets that flag bit. | This is a header used by later code. Its full meaning is unresolved; it is not an identified button number. |
| Next 184 bytes | Cleared through zero-fill helper `0x10199c40`, then passed to `0x10460dac`. That helper loops over 46 word slots, writing zero or one to the supplied output. | Status-word layout observed in this producer. Individual slots have not been tied to camera controls. |

These sizes describe the region prepared by this code. They do not establish
the full event contract or a buffer that would be safe to pass into firmware.

There is also an earlier processing step. At `0x102f2c14`, the worker sends
event type 9 with the address of a local pointer to this region. In state 1,
that event routes to `0x102f7942`, which passes its argument to several helpers.
Their effects are unresolved. The later type-3 call at `0x102f2c22` is
conditional. We cannot assume that the data or selected handler stays unchanged
between the two calls, or that type 3 will run after type 9.

## The input data also lives elsewhere

Routine `0x102f7448` chooses between parsing helpers after several state checks.
Both reviewed helpers inspect the first word of the incoming buffer. Their
later input comes partly from separate state and record storage.

| Helper | Observed code path | Limit |
| --- | --- | --- |
| `0x102f1b30` | A nonzero header leads through `0x102f14c4`, then compares its result with saved state at `0xc18200a4`. A zero header can reach `0x102f1412(0)` and record translation through `0x102f28ee`. | Some special records bypass translation. This is not a complete map of input behavior. |
| `0x102f1d5a` | Checks its input and output pointers first. A nonzero header copies three words from separate state. A zero header can fetch a record through `0x102f1412(0)`. | The three words' meanings and later handling are unresolved. |
| `0x102f1412` | Mode 0 computes record addresses from base `0xc2008ea0` with a 400-byte stride and updates an index using mask `0x0f`. Mode 1 returns fixed record address `0xc200a7a0`. | Ring-like record storage is inference. Producers, synchronization rules and valid record contents are unknown. |
| `0x102f14c4` | Fetches through mode 1, then passes that separate record to `0x102f28ee`. | A nonzero header alone does not construct a new record. |

The reviewed parsers directly read only the incoming header before moving to
other state. This does not prove that the larger handler or earlier type-9
helpers ignore the rest of the region. Putting a menu code into the header
would not establish a native button press.

## How stock code can select state 1

The following static chain is now connected:

1. Worker code at `0x102f2c00` tests bit 16 of its saved flags. If set, the
   call at `0x102f2c0a` sends type 2 to object `0xc1821d44`, with a null payload.
2. With selector 0, router `0x104b912c` chooses handler `0x102f61d2`.
   Its table sends type 2 to `0x102f61ec`.
3. That case reads object field `+0x30` through `0x104b9128`, then passes the
   result to `0x102f57e2`.
4. The prefix of that routine writes selector 1 at `0x102f5810`. One branch
   controls an intervening helper call; both branches converge before the write.

This chain assumes that the called helpers return. The source of worker flag
bit 16 and the full transition's side effects remain unknown. No local AF
eligibility test was established before the state write. State 1 therefore
cannot be treated as permission to start tracking or as a state to force by hand.

## Reproduce privately

Analysis used the unchanged 33,939,514-byte module, mapped at `0x10020000`,
with SHA-256
`8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
Capstone 5.0.6 decoded the selected Thumb code. The newly written verifier
checks the producer layout, selected parser paths, record-address calculations
and state-transition links. It keeps raw decode outside Git. Choose a fresh
output name:

```sh
WORK=/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work
"$WORK/analysis-env/bin/python" "$WORK/codex_liveview_payload_verify_private.py" \
  --output "$WORK/private-inputs/codex-liveview-payload-review-01"
```

The verifier passed in `private-inputs/codex-liveview-payload-verified-01`.
Two Codex subagents checked the state and parser claims independently. The
simulator stayed clean at revision
`0ba0c3547ccbec09e7c861eaca35db8e82795f15`. This private reproduction is not
a CI test. No simulator controls, hardware work or firmware edits occurred.

## Single next step

Trace the producer of the records read through `0x102f1412`, then determine
whether and how those records represent an OK-button press. Keep the type-9 and state
dependencies in that trace before proposing a simulator input call.

Written by Codex in collaboration with Tony Kim, with independent Codex subagent review.
