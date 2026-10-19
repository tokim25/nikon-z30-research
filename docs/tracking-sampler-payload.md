# Tracking sampler consumers and the live-view payload

Consolidated 2026-10-16 from: tracking-sampler-consumers.md,
tracking-liveview-payload.md. Content is unchanged from those files except
for heading levels (bumped one level to nest under this file). Sections
below are in the order the research happened.

No section here shows a successful physical button press or tracking
activation. Each section states its own confidence and limits; read them
individually before citing any single address as an approved entry point.

---

## 2026-10-15: MMIO sampler caller and peripheral attribution

*(formerly `tracking-sampler-consumers.md`)*

Reviewed 2026-10-15. Static analysis and public-source comparison only.

The sampling lead from [PR #13](https://github.com/tokim25/nikon-z30-research/pull/13)
now has a caller and a callback registration path. The register pattern strongly
suggests HDMI connection status. That attribution is inference, not a measured
Nikon peripheral identity. Deprioritize these samplers as a subject-tracking
input lead: no evidence connects them to a camera button, reticle or AF action.

### Caller and output consumer

The unchanged verified C1.20 module was read at mapping base `0x10020000`.
SHA-256 remained
`8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
Analysis used Capstone 5.0.6 in Thumb mode. The following are semantic summaries
of bounded static decode; raw listings remain outside this checkout.

| Landmark | Observed static structure | Interpretation and limit |
| --- | --- | --- |
| Candidate routine `0x1028afee`, call at `0x1028b040` | Supplies its stack as the second argument to `0x1029d8aa`, then reads the destination byte and normalizes it to zero or one. | A consumer of the bit-1 sampler, not a tracking-start call. High confidence in the bounded call and data flow. |
| `0x1028b04e`–`0x1028b06e` | Compares the sample with state at `0xc1807ed4`. Differences increment a counter at `0xc1807ef4`; equal samples reset it. A differing sample is accepted only when the unsigned counter exceeds the cached threshold. | Debounce-like filtering is static inference, high confidence. Threshold and pacing values are loaded from configuration; no camera timing is established. |
| `0x1028b06e`–`0x1028b0b2` | Calls intervening helpers on selected paths, normalizes a final state at `0xc1807edc`, compares its previous value and checks a callback slot at `0xc1807ecc`. A changed final state can reach an indirect call at `0x1028b0b2`. | Conditional state notification is inference. The helpers can filter or clear state; a sampled change does not guarantee a callback. |
| Setter `0x1028b134`; caller `0x10396f98` | The setter stores its argument at `0xc1807ecc`. The caller supplies Thumb pointer `0x10396cdf`, corresponding to code at `0x10396cde`. | A statically connected registration path. Initialization, later overwrites and runtime invocation are unverified. |
| Callback `0x10396cde`–`0x10396d06` | Requires first argument 1, calls a helper with size 28, checks the returned pointer, and writes identifier `0x4206101e` plus the incoming payload pointer into a record. The successful path continues through `0x10396cc6`. | Allocation-like and notification behavior are inference. The helper contracts, record ownership and delivery are unresolved. This identifier is not a verified tracking event. |

A scan for 32-bit Thumb BL, B.W and immediate BLX patterns at halfword positions
over `0x10020000`–`0x11f81c94` found the call at
`0x1028b040` to the first sampler. It found no direct branch candidate to
`0x1029d8ea`; whole-module word searches found no exact even or Thumb-pointer
occurrence for either sampler address. These negative results do not prove
that other callers are absent. Mixed code/data, indirect dispatch, constructed
addresses, omitted narrow/conditional branches and incomplete function recovery
limit the scan. The bounded caller
window and registration path were inspected separately from the scan matches.

### Peripheral inference

Using proposed base `0x20160000` and spacing four, several simulator register
addresses match [Linux v6.12 DesignWare HDMI definitions](https://github.com/torvalds/linux/blob/v6.12/drivers/gpu/drm/bridge/synopsys/dw-hdmi.h#L350-L378):

| Simulator address | Register offset | Corresponding public definition |
| --- | --- | --- |
| `0x2016c010` | `0x3004` | PHY status |
| `0x2016c018` | `0x3006` | PHY interrupt mask |
| `0x2016c0a4` | `0x3029` | PHY I2C divider |
| `0x2016c0a8` | `0x302a` | PHY I2C soft reset |
| `0x2016c0ac`–`0x2016c0c8` | `0x302b`–`0x3032` | PHY I2C timing registers |

The same header [defines status bit 1 as hot-plug detect and bits 4–7 as
receiver-sense signals](https://github.com/torvalds/linux/blob/v6.12/drivers/gpu/drm/bridge/synopsys/dw-hdmi.h#L844-L850),
matching the previously observed sampled fields. This multi-register agreement
supports HDMI attribution with high confidence as an inference. It does not
establish the Nikon integration, access-width requirements or runtime behavior.

Local source provenance is
[the pinned simulator register table](https://github.com/WonderLantern/z30-qemu/blob/0ba0c3547ccbec09e7c861eaca35db8e82795f15/qemu/nikon-z30-display.c#L2979-L2996).
Its comment labels `0x2016c0a8` as a zero-error polling value, which conflicts
with the soft-reset analogy. Do not use that comment as a register-name proof.
The simulator's all-low status response remains an unmeasured startup hypothesis.

### Reproduce privately

The owner-confirmed WORK directory contains the newly written verifier and
verified module. Use a fresh `codex-` output name; the command refuses to replace
an existing directory. No firmware instructions are modified or executed.

```sh
WORK=/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work
"$WORK/analysis-env/bin/python" "$WORK/codex_sampler_consumer_verify_private.py" \
  --output "$WORK/private-inputs/codex-sampler-consumer-review-01"
```

To repeat the branch-candidate scan and bounded caller inspection:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex_tracking_static_private.py" \
  --output "$WORK/private-inputs/codex-sampler-callers-review-01" \
  --target 0x1029d8aa --target 0x1029d8ea --window 0x1028afee:0xe2
```

The verifier passed in `private-inputs/codex-sampler-consumer-verified-01`.
The simulator stayed clean at revision
`0ba0c3547ccbec09e7c861eaca35db8e82795f15`. A Codex subagent independently
checked the caller and callback summaries. These commands depend on private
files and are not CI evidence. Keep all raw output outside the repository.

### Single next step

Trace registration and callers of the known menu dispatcher `0x103ce96e` back
to its shared event router, then check for a separate live-view branch. Treat
every result as menu-only until a live-view connection is demonstrated. Do not
invoke the dispatcher as a substitute for native live-view input.

Written by Codex in collaboration with Tony Kim, with independent Codex subagent review.

### Candidate ring predicate follow-up (2026-10-18, F-225)

The mask fields tested by the private AE-L/AF-L candidate are consistent with
the first 20-byte difference record produced by `0x102f199a`. Helper
`0x101dd502` writes `(input1, input2, input1 XOR input2, input1-only,
input2-only)` at offsets 0, 4, 8, 12 and 16. The candidate sees this block
starting at ring-record offset +4. In this caller, the helper receives
`input1 | input2` and `input2`; the candidate's bit checks therefore mean
that `0x2000` exists only in the first input. This is a coherent one-sided
change shape, not an impossible simultaneous condition.

That interpretation does not identify the inputs as old/new physical switch
states or connect the mask to AE-L/AF-L. The two direct callers found for the
builder, `0x1039e1d4` and `0x1046497e`, still require tracing to their source
records. The separate facts that logical ID 41 maps to `0x2000` and that a
debug name table labels the same SW0 mask `AEAF_LOCK` do not close this gap.
The current candidate action remains native Subject tracking action 45; the
remaining trigger question is physical admission, not AF-area selection.

Method: read-only Thumb data-flow review; addresses and field offsets only.
No firmware bytes/dumps recorded, no image written and no camera access.

---

## 2026-10-15: Live-view event data and the path into state 1

*(formerly `tracking-liveview-payload.md`)*

Reviewed 2026-10-15. Read-only code analysis; no firmware code was run.

The live-view input path needs more than an event number. Its builder prepares
a 188-byte region, and the reviewed parsers also use records stored elsewhere.
The header can choose a stored-record path rather than supply a new button
action. We have not identified an OK-button record or a tracking-start action.

We also found a stock code path from state 0 to state 1. That closes part of
the state question from [PR #15](https://github.com/tokim25/nikon-z30-research/pull/15).
It does not prove that the simulator reaches that state during normal startup.

### What builds the event data

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

### The input data also lives elsewhere

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

### How stock code can select state 1

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

### Reproduce privately

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

### Single next step

Trace the producer of the records read through `0x102f1412`, then determine
whether and how those records represent an OK-button press. Keep the type-9 and state
dependencies in that trace before proposing a simulator input call.

Written by Codex in collaboration with Tony Kim, with independent Codex subagent review.
