# Tracking the AE-L/AF-L input chain: producers, routing and dispatch

Consolidated 2026-10-16 from: tracking-input-source.md, tracking-input-sampler.md,
tracking-input-records.md, tracking-numeric-input-route.md,
tracking-queued-bank-route.md, tracking-input-bank-selection.md,
tracking-dispatch-registration.md. Content is unchanged from those files
except for heading levels (bumped one level to nest under this file) and
the correction already recorded in the former tracking-dispatch-registration.md
section, carried forward as-is. Sections below are in the order the
research happened; later sections build on earlier ones where noted.

No section here shows a successful physical button press, tracking
activation, or incoming transport/identity for AE-L/AF-L. Each section
states its own confidence and limits; read them individually before citing
any single address as an approved entry point.

---

## 2026-10-15: A structured-control path into the input cache

*(formerly `tracking-input-source.md`)*

Date: 2026-10-15. Read-only static analysis of verified firmware C1.20.

The reviewed path can produce bit 13 without directly reading a hardware
switch. It receives a structured record, chooses a mask from a selector,
updates a staging word and passes that word to an input-cache setter.
This establishes one producer path, not the physical identity of its input.

| Landmark | Observed bounded behavior |
| --- | --- |
| `0x1008ad26` | Reads selector at record `+0x04`; an unsigned check admits values below 6 to the branch table at `0x1008ad2c`. |
| `0x1008ad4a` | Selector 5 chooses mask `0x2000`. |
| `0x1008ad50` onward | Reads state at record `+0x08`. State 1 sets the mask in staging word `0xc1811e74`; state 0 clears it. Other values skip that staging update. |
| `0x1008ad6e` | Transfers to setter `0x101e383a` with the staging-word address, including when the state skipped the update. |
| `0x101e383a` | Reads its pointed-to input word and stores it at cache `0xc181182c + 0x30`, at `0x101e3840`; then continues pending-state handling. |
| `0x101e3858` | A separate setter copies its pointed-to word to the same cache's `+0x38`, at `0x101e385e`. |

Confidence is high for these observed code and data links. Upstream
reachability, the record sender, transport, selector meaning and physical
SW0 relationship remain unverified. State values 1 and 0 resemble on/off
control, but calling them physical press and release would be inference.
Neither path has been shown to activate tracking or even to run during the
simulator's normal refresh.

The staging address needs care: the literal is `0xc1811e70`, then the code
adds 4 before accessing and passing the word. The accessed word is therefore
`0xc1811e74`. Also, an unrecognized state does not imply no cache side
effects: the setter still runs. Independent review caught both errors in
the draft analysis before publication.

### Reproduce privately

With confirmed WORK and a fresh output folder:

```sh
"$WORK/analysis-env/bin/python" \
  "$WORK/codex-input-field-source-verify-private.py" \
  --output "$WORK/private-inputs/codex-input-field-source-review-04"
```

The private helper checks the original module hash and selected instruction,
literal and branch-table relationships. Independent inspection in
`codex-agent-field-source-review-01` checked surrounding branches and
register flow. These are bounded static checks, not a complete proof of
execution. Private outputs and all firmware content stay outside Git.

No firmware changes, simulator calls or hardware access were used. None of
these addresses is an approved call or patch interface. Next: identify the
sender and meaning of the structured records before assigning a button name.

Written by Codex in collaboration with Tony Kim; independently checked by Codex subagents.

---

## 2026-10-15: A numeric-command route into the candidate input handler

*(formerly `tracking-numeric-input-route.md`)*

Date: 2026-10-15. Bounded static analysis, unchanged firmware.

The structured handler containing `0x1008ad26` has a registered route that
parses numeric text. This is not evidence of a physical AE-L/AF-L reader.
Diagnostic purpose is an inference; the incoming transport remains unknown.

Initializer `0x1008ad72`, on its argument-0-equals-3 path, supplies callback
`0x1008ac2e` through registrar `0x101e1c04`, with word limit 4 and flags 0.
The registration code stores callback, limit and flags at slot offsets
`+0x18`, `+0x1c` and `+0x20`. Duplicate/missing-entry branches mean this
does not prove registration succeeds at runtime.

Consumer `0x101e1c22` uses the flags-zero branch to call parser `0x101e230e`
at `0x101e1c62`, then the registered callback at `0x101e1c6c`. Arguments
are the registration key, a parsed-word array and its count. The parser
splits text at spaces, modifies delimiters in its input, and converts tokens
to words. It initializes radix 10 and can select radix 16; the reviewed
loop can retain that radix for later tokens. Numeric validation is not
established. The private registration label is omitted and provides no
independent physical-switch attribution.

These are observed code/data links, high confidence, independently reviewed.
No execution, switch ownership, normal transport or tracking activation was
verified. Other producers of the same input cache are not excluded.

### Reproduce privately

With confirmed WORK and a fresh output directory:

```sh
"$WORK/analysis-env/bin/python" \
  "$WORK/codex-registered-input-verify-private.py" \
  --output "$WORK/private-inputs/codex-registered-input-review-03"
```

Passing root repeat: `codex-registered-input-root-01`; independent full-block
review: `codex-agent-registered-review-01`. The helper checks original identity
and selected relationships; it is not a complete control-flow proof.
All restricted evidence stays outside Git.

Next: inspect independent cache-setter calls at `0x103a3e88` and
`0x103a400c`, outside this numeric handler, for a physical input source.

Written by Codex in collaboration with Tony Kim; independently reviewed by Codex agents.

---

## 2026-10-15: Input records: two ring writers

*(formerly `tracking-input-records.md`)*

Date: 2026-10-15. Read-only static analysis of the verified C1.20 EG module.
No simulator input calls or firmware edits were made for this finding.

### Result

F-021's claim that only one routine writes the ring is incorrect. At least
two routines write records into the store at `0xc2008ea0`, using the index
state at `0xc182004c`. Their input sizes differ. This matters because treating
every ring entry as a 60-byte event would hide another input path.

| Routine | Observed static behavior |
| --- | --- |
| `0x102f0a36` | Copies 60 bytes into a cleared 400-byte slot and forces the leading kind word to 1 at `0x102f0c02`. |
| `0x102f1844` | Clears a 400-byte slot and copies 396 bytes from its input at `0x102f1946`. A conditional path advances the index modulo 16. |
| `0x102f1412` | Mode 0 selects the ring with a 400-byte stride. Mode 1 selects the separate record at `0xc200a7a0`. |

These are observed code and data links, with high confidence. They do not
show that either path ran in the simulator or that a record came from a
physical button. This report corrects the exclusive-writer and universal
record-size claims; it does not reassess every other claim in F-021.

### Links to input decoding

The paired-record builder `0x102f199a` calls the larger writer at
`0x102f1a4a` and `0x102f1aa0`, after calls to `0x102f0d14`. Its field helper
`0x101dd502` stores two masks and their changed, first-only and second-only
bits. Interpreting this as logical transition construction is inference.
Press and release meaning remains unverified.

A separate static chain agrees with the earlier menu-OK candidate:
getter `0x101dd616` reads record field `+0x18`; decoder `0x102f0e38` uses
that field in its loop at `0x102f101a`. Table row `0x1073be50` associates
mask 1 with candidate `0x1b`. Menu translator `0x1045933e` maps `0x1b` to
event `0x27e` through row 32 of table `0x1073b400`.

Candidate creation is insufficient to prove input delivery. Later decoder
branches can clear all three output words, including the path at
`0x102f1404` to `0x102f140c`. No physical OK bit, AE-L/AF-L mapping or
tracking entry point is established by this chain.

The live-view callback also has a call to the larger writer at
`0x102f2fd0`, followed conditionally by a flag-2 signal at `0x102f2fdc`.
The preceding gates, task context and successful runtime delivery remain
unresolved. None of these addresses is an approved call interface.

### Reproduce privately

Use the WORK path confirmed by the owner. The helper is private because it
reads the original module and saves detailed decode output. It checks the
module hash, pinned simulator revision and clean simulator checkout, then
asserts the selected instruction and table relationships. Use a fresh output
folder each time:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex_input_record_verify_private.py" \
  --output "$WORK/private-inputs/codex-input-record-review-02"
```

The successful session output is `codex-input-record-resume-01`. An
independent reviewer decoded the writer and reader paths again in
`codex-agent-producer-resume-01`. All detailed output stays outside Git.
The private helper's earlier range ended halfway through an instruction;
that analysis-tool error was corrected before its assertions passed.

Repository checks pass: 54 unit tests, the tracked-artifact check and the
encoded-data check. Those checks validate the repository, not camera behavior.

### Next step

Trace the named AE-L/AF-L switch's bit-13 reader and its event destination.
Keep the switch-name table separate from the logical record masks until an
actual code path connects them.

Written by Codex in collaboration with Tony Kim; independently checked by a Codex subagent.

---

## 2026-10-15: Bounded MMIO sampling lead

*(formerly `tracking-input-sampler.md`)*

Reviewed 2026-10-15. Static analysis only; no guest control calls or hardware.

Candidate routines at `0x1029d8aa` and `0x1029d8ea` read a byte from
`0x2016c010`. Their bounded control flow supports a single-bit output and a
four-bit output. Their callers, device purpose and connection to live-view
input remain unknown. Neither address is a verified tracking entry point.

### Source lead and failed hypotheses

The clean simulator checkout was at revision
`0ba0c3547ccbec09e7c861eaca35db8e82795f15`. Its
[MMIO source](https://github.com/WonderLantern/z30-qemu/blob/0ba0c3547ccbec09e7c861eaca35db8e82795f15/qemu/nikon-z30-display.c#L3031-L3036)
returns zero for recovery-profile byte reads at `0x2016c010`. That is observed
source behavior, not a measured external input. The accompanying comment
labels the all-low value an unmeasured hypothesis.

The comment attributes bit sampling to `0x102595de` and `0x1025961e`.
Bounded decoding at those addresses in the verified module did not reproduce
the stated sampling sequence. Adding `0x20000` did not repair the attribution:
the resulting windows contained byte reads but did not establish the claimed
MMIO sampling. Both address hypotheses failed. The cause of the comment's
address discrepancy remains unknown; no simulator source was changed.

Searching for the MMIO base constant, then checking bounded PC-relative
references to it, supplied the independent landmarks below. The search was
limited to the confirmed private module. It was not a search for new firmware.

### Static observations and interpretation

The module is 33,939,514 bytes, mapped at `0x10020000`, with SHA-256
`8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
The hash and size were checked before analysis. Capstone 5.0.6 decoded Thumb
instructions. Detailed decode output stays outside this repository.

| Landmark | Observed in bounded static decode | Interpretation and confidence |
| --- | --- | --- |
| `0x1029d8aa`–`0x1029d8e9` | A stack-save start, preservation of the incoming second argument as a destination, a PC-relative load at `0x1029d8c2` through `0x1029dbbc`, addition of 16, and a byte read at `0x1029d8c6`. The literal value is the MMIO base `0x2016c000`. | High confidence in a byte read from `0x2016c010` within this window. Reachability from stock live view is unverified. |
| Same window | The sampled byte is shifted left by 30; sign-dependent branches choose zero or one and store a byte through the preserved destination. | Static inference, high confidence: destination byte represents sampled bit 1. No button identity follows. |
| `0x1029d8ea`–`0x1029d94f` | The incoming second argument is preserved as a destination. A PC-relative load at `0x1029d902` uses the same literal, adds 16 and reads a byte at `0x1029d906`. | High confidence in another byte read from `0x2016c010`. |
| Same window | Shifts by 27, 26, 25 and 24 feed sign-dependent branches. The destination is cleared, then conditionally receives output bits 0–3. | Static inference, high confidence: sampled bits 4–7 form the destination's low nibble. Device and input semantics remain unknown. |

The windows also call helpers before and after sampling. Their contracts,
locking requirements, side effects and error handling have not been established.
The stack-save starts and adjacent tail branches support candidate routine
boundaries; a full control-flow graph and all incoming references have not been
reconstructed. No address in this report is approved for a diagnostic call.

The existing GUI limitation was rechecked in source: its live-view worker
refreshes instead of passing a key event, the HTTP input allowlist accepts only
`refresh` in live-view mode, and page construction disables keyboard forwarding.
The menu route's `0x103ce96e` therefore supplies no demonstrated connection to
these samplers. This is source inspection, not a browser or guest execution test.

### Reproduce privately

Use the owner-confirmed workspace. The verifier is newly written research
code, not recovered code. It checks identity and bounded decode structure,
creates a new output directory and keeps detailed output private. Choose a
fresh `codex-` output name on each run.

```sh
WORK=/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work
"$WORK/analysis-env/bin/python" "$WORK/codex_input_sampler_verify_private.py" \
  --output "$WORK/private-inputs/codex-input-sampler-review-01"
git -C "$WORK/z30-qemu" rev-parse HEAD
git -C "$WORK/z30-qemu" status --porcelain
```

The reproduction depends on private files confirmed by the owner; it is not
self-contained CI evidence. Do not upload the verifier's raw decode or private
run folders. The reported run used `codex-input-sampler-verified-01`; all bounded
checks passed. The simulator checkout remained clean. No simulator was started,
no firmware instruction was changed, and no restricted artifact was added here.

### Single next step

Trace static callers of `0x1029d8aa` and `0x1029d8ea` and identify their output
consumers. Establish the peripheral's purpose before calling either a button
sampler or a live-view route. Tracking activation remains unverified.

Written by Codex in collaboration with Tony Kim, with source review by Codex subagents.

---

## 2026-10-16: A bank-mapped queued route into the input cache

*(formerly `tracking-queued-bank-route.md`; continues this file's
"2026-10-15: A numeric-command route" section's "Next" pointer to the
independent cache-setter calls at `0x103a3e88` and `0x103a400c`)*

Date: 2026-10-16. Bounded static analysis of verified C1.20.

The independent caller at `0x103a400c` publishes staging word `0xc18c9a68`
through setter `0x101e383a`. Unlike the earlier numeric-command route, its
consumer `0x103a3f9e` obtains a queued record and maps its ID byte (`+0x11`)
to a mask. Operation byte `+0x10` selects set or clear behavior.

The table formula is `0xc18c9a7c + 128 * BYTE(0xc18c9a64) + 8 * row`,
with at most 16 rows. Each row has ID byte `+1` and mask word `+4`.
Operations 0–2 OR the mask; 3–4 clear it. The queued route calls the setter
when staging changes. Separate caller `0x103a3e88` publishes a reset when
the staging word was nonzero.

Handler `0x103a3d14` processes code `0x2083`, builds the ID/operation fields,
queues the record and invokes the consumer path. The reviewed upstream chain
includes `0x10379f00` and `0x10379a68`. Incoming transport, physical SW0
identity, press/release meaning and tracking activation remain unverified.
The same numeric code in an unrelated UI path is not a proven sender.

The bank selector is a byte, not a word. An earlier provisional interpretation
as a relative pointer was wrong: exact subtraction and shift checks establish
the banked formula above. Initial bank 0 is empty; that does not exclude a
later selection of another initialized bank. Confidence is high for these
bounded code/data links, not runtime delivery.

### Reproduce privately

Private repro, confirmed WORK and fresh directory:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex-agent-queued-input-verify-private.py" \
  --output "$WORK/private-inputs/codex-queued-route-reproduce-01"
```

Corrected agent verification: `codex-agent-queued-input-verify-03`;
root repeat: `codex-root-queued-input-20261016-01`. The helper checks original
identity and selected instructions, table branches and copy mapping. Detailed
evidence stays private. No firmware execution or hardware was used.

Next: trace the incoming producer of the property-event record and establish
the meaning of its ID before assigning it a physical button name.

Written by Codex in collaboration with Tony Kim; selected checks independently repeated by Codex agents.

---

## 2026-10-16: Selecting a populated input-map bank

*(formerly `tracking-input-bank-selection.md`; continues the queued-bank
route above)*

Date: 2026-10-16. Read-only static analysis of verified C1.20.

Query `0x103a3cb0` selects bank 1 with a byte store at `0x103a3cdc` into
`0xc18c9a64`. That selects initialized bank `0xc18c9afc` for the queued
input lookup. Zero-based row 11, at `0xc18c9b54`, associates logical ID 41
with mask `0x2000`; its initialized-data origin is `0x1204b7e8`. The root
also checked that this ID has no earlier duplicate in the 16-row bank.

The query emits each row's first two bytes as tag/ID pairs through property
code `0x2082` at `0x103a3d06`. This supplies a concrete selection path for
a populated bank, rather than assuming the initially empty bank 0 is the
only available mapping.

Confidence is high for these bounded code/data links. Actual query execution,
incoming transport, the ID's physical meaning and tracking remain unverified.
The matching mask is insufficient to identify AE-L/AF-L: the named hardware
SW0 table and this logical input bank are not proven to share a namespace.

### Reproduce privately

Private repro, confirmed WORK and fresh directory:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex-agent-input-bank-verify-private.py" \
  --output "$WORK/private-inputs/codex-input-bank-reproduce-01"
```

Agent run: `codex-agent-input-bank-verify-01`; independent root repeat:
`codex-root-input-bank-20261016-01`. Original identity and selected instructions,
copy mapping and row values are checked; detailed evidence stays outside Git.
No firmware execution, modification or hardware was used.

Next: identify the sender/meaning of incoming event IDs before calling
logical ID 41 a physical button.

Written by Codex in collaboration with Tony Kim; selected mapping independently checked by Codex agents.

---

## 2026-10-16: Tracing the queued-bank route upward: an event dispatcher and its registration

*(formerly `tracking-dispatch-registration.md`, including its own
2026-10-16 in-file correction, carried forward unchanged; continues the
queued-bank route's "reviewed upstream chain" `0x10379f00`, `0x10379a68`)*

Date: 2026-10-16, corrected 2026-10-16 (see "Correction" below). Read-only
static analysis of verified C1.20, continuing this file's "2026-10-16: A
bank-mapped queued route into the input cache" section's "reviewed upstream
chain" (`0x10379f00`, `0x10379a68`) one level further to the owning
state-machine step function. An attempt to find that function's
dispatch-table registration did not hold up on re-verification; see the
correction in "The enclosing state-machine step and its registration" below.
This is not a native simulator observation and does not establish incoming
transport, physical button identity, or tracking activation.

### The event-code dispatcher

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
  this file's "2026-10-16: A bank-mapped queued route" section's
  tracking-queue handler.
- Other deltas, bounded by a second comparison against a literal-loaded
  constant, fall through to `0x103a37dc` or a shared default path at
  `0x10379c24`.

This confirms code `0x2083` is handled as one case among several in a
general-purpose event-code range (`0x2006`-`0x2083`+), alongside what
looks like a touch-input case (`0x2006`) with its own separate callback
registration. Observed static decode, high confidence for the dispatch
shape; the meaning of codes `0x2006`/`0x2007` and the other deltas was
not pursued.

### The enclosing state-machine step and its registration

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

### What this establishes and what it does not

This is new ground beyond this file's "2026-10-16: A bank-mapped queued
route" section, which stopped at naming `0x10379f00` and `0x10379a68`
without decoding either. It traces the queued tracking-event route one
full level further: from the mask-table consumer, up through the
event-code dispatcher, up through the owning state-machine step function
-- which itself has zero direct references anywhere in the image. It does
**not** reach a physical input source, an input-pump/message-loop caller,
a working registration mechanism for `0x10379d5a`, or anything that names
AE-L/AF-L specifically. The physical-identity gap flagged by this file's
"2026-10-16: Selecting a populated input-map bank" and "2026-10-16: A
bank-mapped queued route" sections remains fully open.

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
Codex's queued-bank-route and input-bank-selection sections above
(owner-approved lane work, same basis as the handoff-codex.md exception
used throughout this session).

## 2026-10-16: a real event-code cluster around property 0x2021 (not Bluetooth)

Followed this section's own suggested next step -- decoding the `0x2006`
touch-input branch's separate callback slot -- rather than chasing
`0x10379d5a`'s unresolved registration mechanism further. This surfaced a
different, more promising cluster entirely.

The touch-input dispatcher's callback slot (`global base 0xc28fbf04 + 0x54
= 0xc28fbf58`, resolved from the literal at `0x10379e58`) has three other
literal-pool references to its base besides the known touch consumer:
`0x1037a72c` (inside `0x1037a6fe`, an unrelated setter -- not decoded
further), `0x1037ab68` (inside `0x1037aae2`), and `0x1037ade4` (inside
`0x1037ad86`, a string-building helper -- not decoded further).

`0x1037aae2` is its own small event-code dispatcher, structured just like
`0x10379a68` but with different cases: code `0x2006` exactly reads a
*different* callback slot (`[literal_base + 0x48]`, a separate global from
the touch slot above) and calls it if non-null; delta `0x1a` (code
`0x2020`) tail-branches to `0x103a2a9c`; delta `0x1b` (code `0x2021`)
tail-branches to `0x103a31a6`; **delta `0x81` (code `0x2087`) tail-
branches to `0x103a341a`** -- four codes away from this project's known
tracking code `0x2083`, in the same family.

`0x103a341a` reads a sub-code byte from offset `2` of its event struct and
dispatches on it (values checked: `1`, `0xf`, `0x10`, `0x11`, `0x12`,
`0x13`, `0x14`, `0x17`). **Four of these sub-codes -- `1`, `0x10`, `0x12`,
`0x13`, `0x14` -- all build a small payload (1 to 4 bytes, encoding a
simple state: zero/one, or one of a handful of small integers) and post
it as property event `0x2021`** through the shared primitive
`0x10475ecc`. Sub-code `0x11` is different: it reads one byte from
`[[r0+4]]`, checks it against `1`, and tail-branches to one of two
*different* functions (`0x103a3360` or `0x103a2e88`) depending on the
result -- read-a-state-and-branch shaped, not a post.

This is a materially different and more promising shape than the
project's one prior tracking-activation lead (the `0x11cf4e90` cluster in
tracking-entry-research.md), which resolved to Bluetooth/HCI packet
processing. Here: a touch-input event family (`0x2006`), two adjacent
state-change codes (`0x2020`, `0x2021`), and a multi-sub-code dispatcher
(`0x2087`) whose sub-codes nearly all converge on posting a simple
few-state value into `0x2021` -- the general shape of a toggle or
lock-style control, not protocol bookkeeping. **This does not establish
AE-L/AF-L identity.** It establishes a real, non-Bluetooth control
cluster worth testing against that hypothesis, nothing more.

Observed static decode on 2026-10-16, no classifier stop. Confidence
high for the bounded code shapes and addresses reported; low for any
claim about what property `0x2021` actually controls or whether this
cluster is AE-L/AF-L specifically, Intelligent/other toggle, or something
else entirely.

Not yet done: decoding `0x10475ecc` (the shared post primitive, to see if
it reveals anything about the property's consumer) and, more directly,
finding what *reads* property `0x2021` -- i.e. what branch of firmware
state actually changes when this event posts. That is the real test of
the lock/toggle hypothesis, not anything in this event-posting chain
itself. Sub-codes `0xf` and `0x17` of `0x103a341a` were also not fully
decoded.

Method: read-only static decode (capstone, Thumb) and literal-pool xref
scans, SHA-256 checked first; addresses, offsets and event/property codes
only, no firmware bytes recorded.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim, continuing
the section above.

## 2026-10-16: no consumer found by direct comparison -- handoff point

Searched for property `0x2021`'s consumer (the section above's named next
step), exhaustively, two ways:

1. A scan of the module around the known post sites (`0x10370000`-
   `0x103b0000`) for any `cmp`/`sub`/`movw` referencing `0x2021` found
   only the 6 already-known post sites (`movw r0/r3, #0x2021` immediately
   before a call to `0x10475ecc`). No compare/dispatch site in that
   range.
2. A full 33.9MB image scan for any `cmp`/`cmp.w`/`subs`/`sub.w`
   instruction referencing the immediate `0x2021`, anywhere, found
   **zero** hits.

Nothing in this firmware image explicitly compares against the literal
`0x2021` to decide what to do about it. Combined with F-106's finding on
a different property family (`0x0418xxxx`, Lane 2) that posted events
there reach their consumer through a generic queue-and-registration
primitive rather than a hardcoded comparison, the likely explanation is
architectural: this firmware's property-notification system dispatches
by registration (a consumer subscribes once, generically, and reads the
posted id as data at runtime) rather than by compile-time literal
comparison, so a literal-value search cannot find the consumer no matter
how exhaustive.

**This is a deliberate handoff point, not a dead end treated as closed.**
Two concrete ways forward exist, both requiring techniques beyond what
this session used:

1. **Live simulator verification.** Set a breakpoint on the shared post
   primitive `0x10475ecc` (the same technique this project has used
   throughout for event/property tracing) and observe calls with
   id `0x2021` during ordinary simulated menu/button navigation, to see
   what state changes afterward. This would also help determine whether
   `0x2087` is reachable from the simulator's limited key set at all --
   unknown and not yet checked.
2. **A masked/family-level static search**, not a literal-value search:
   check whether any dispatcher compares a *masked or shifted* form of
   incoming property ids (e.g. testing only the high byte, `0x20`, the
   way F-104's SD command words encoded a category in one byte and a
   sub-id as plain data) rather than the exact value `0x2021`. This
   session did not attempt this -- it requires finding candidate generic
   property-dispatch functions first (a different search than anything
   tried in this file so far) and checking their comparison shape, not
   just literal matches.

**State to hand off:** the touch-input event family (`0x2006`/`0x2020`/
`0x2021`/`0x2087`, all reached through the dispatcher at `0x1037aae2`)
remains the strongest lead this project has found for AE-L/AF-L or any
related physical-button identity -- materially stronger than the
falsified Bluetooth/HCI lead in tracking-entry-research.md, because it is
a real, locally-coherent control cluster with a toggle/lock-shaped
payload, not packet-protocol bookkeeping. It is not confirmed. Whoever
picks this up next should not restart from the Bluetooth lead or from
`0x10379d5a`'s unresolved registration (both already exhausted by direct
static search in this file); start from option 1 or 2 above.

Method: read-only static decode (capstone, Thumb) and full-image
instruction scans, SHA-256 checked first; addresses and event/property
codes only, no firmware bytes recorded.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
