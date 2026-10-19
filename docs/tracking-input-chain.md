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

## 2026-10-17: option 2 tried for one masking idiom, negative (F-116)

Tried this section's option 2: a full-image search for a dispatcher that
tests property ids by their high byte (`0x20`) rather than by exact
literal value, the same category-plus-sub-id shape F-104 found for SD
commands. Searched specifically for `cmp rX, #0x20` fed by an `lsrs rX,
rY, #8`-style extraction. Found one real, cleanly-decoded hit
(`0x105afa0e`) and four decode artifacts; the one real hit is a
text/string-formatting routine (ASCII-range checks on a character buffer),
not a property dispatcher -- unrelated to `0x2021`/`0x2087`.

Two more idioms tried in the same pass: `ubfx` bitfield-extract (zero
hits) and `and #0xff00` (two raw hits, both false positives on inspection
-- ordinary peripheral-register-programming code, not dispatch). **Three
of four plausible static masking idioms are now exhausted with nothing
found**; only a `tbb`/`tbh` range-dispatch table keyed on the high byte
remains untried, and it needs a different search (locate jump tables
first) rather than a quick extension of this scan. Option 1 (live
simulator breakpoint on `0x10475ecc`) is now the more promising next step.
Full detail in facts.md F-116.

Method: read-only static decode (capstone, Thumb), full-image instruction
scan, SHA-256 checked first; addresses only, no firmware bytes recorded.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.

## 2026-10-17: both remaining leads tried, both negative (F-117)

Tried the fourth static masking idiom (`tbb`/`tbh` range dispatch) and
option 1 (a live simulator breakpoint on the post primitive `0x10475ecc`
during ordinary navigation). Both negative.

The `tbb`/`tbh` scan found 2,817 table-branch sites image-wide -- far too
many to review by hand -- and zero matched a narrow gate shape (an
immediate `sub rX, #0x20xx` writing the index register directly before
the branch). This only rules out that one narrow shape, not `tbb`/`tbh`
dispatch on the high byte in general; a real dispatcher could compute the
index less directly. Not a clean negative like the other three idioms.

The live-breakpoint test is the more informative result: armed on
`0x10475ecc`, then ran an idle checkpoint, real menu activation
(`0x102355ee`), eight real internal UI-event codes through the real key
dispatcher (`0x103ce96e` -- OK, back, four directional codes, all from
F-017/F-020/F-023), and a second idle checkpoint. **The primitive was
never called at all, for any id, across the whole sequence** -- not a
miss on `0x2021` specifically, but zero property posts of any kind via
this call path. Matches this project's long-documented dormant-worker
pattern (F-018, F-019) rather than saying anything specific about
`0x2021`/`0x2087`.

**Handoff, updated:** no consumer for `0x2021` found by any method tried
across F-116/F-117 (three clean-negative static idioms, one inconclusive-
by-volume static idiom, one dormant-worker-shaped simulator negative).
What's left is either reading `tbb`/`tbh` tables by hand near plausible
sites (slow, no good filter yet) or finding a way to keep the relevant
background task alive long enough in the simulator for a real post to
happen -- the same harder problem this project has hit on other lanes and
not solved. Full detail in facts.md F-117.

Method: software breakpoints via the existing diagnostic-call mechanism
(no memory write); static decode (capstone, Thumb); firmware hash and
QEMU checkout verified before and after; no firmware bytes recorded.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.

## 2026-10-18: tracking-action hook takes priority (F-212/F-213/F-214)

The `0x2021` property-consumer question is closed as a historical lead; do not
continue the dormant post-primitive or broad jump-table search absent new
evidence. The active one-button tracking work is the native Subject tracking
action route summarized in Lane 3 of `handoff-codex.md`. A private candidate's
constructed-context guard/ABI cases pass in QEMU (F-212), while a separate
powered candidate diagnostic found the task before a native notification but
no worker-entry/cleanup probe hits (F-213). Neither result establishes normal
AE-L/AF-L event delivery. F-214 confirms the candidate adapter and native Fn
handler issue the same action-45 request to the same native object. This
supports delegating the toggle to Nikon's state machine; the QEMU object is
unmodeled, so consumer state is not observable. Nikon's manual defines
start-on-press / stop-on-second-press behavior for Auto-area AF modes. The
open gap is natural AE-L/AF-L hook admission and full candidate ABI review,
not the semantics of the requested action. Keep candidate data and firmware
inputs private and do not access the camera.

Method: bounded QEMU-only diagnostics with memory-only edits; no firmware
bytes or dumps recorded.

## 2026-10-18: AF-area menu is a precondition, not the tracking entry (F-215)

Following the AF-area label table through its menu option mapper and setter
resolves the Z 30's selectable modes, but does not lead to a `3D-TRACKING`
activation row. The option table contains Auto-area AF and its people/animal
variants (encoded 600/601/602); the setter stores base mode 6 and submode
0/1/2 in properties `0x0c2b` and `0x0c3d`. The label reference at
`0x103edc2e` is label output, not evidence of an action callback. The generic
OK/J UI dispatcher calls whichever event callback is registered on the active
menu object. On the AF-area option path, that callback sets the selected mode.

Nikon's Z 30 manual makes the distinction explicit: after Auto-area AF (or
its people/animal variant) is selected, subject tracking is a separate J
operation. J first displays the targeting reticle, the next J starts tracking,
and another J ends it; W(Q) exits subject-tracking mode. An assigned native
Subject-tracking control starts/ends the same operation. This matches F-214's
candidate-versus-native-Fn request comparison. Therefore the actionable hook
remains the native Subject-tracking action path; the AF-area menu trace
establishes the required mode eligibility only. The current evidence does
not decode the live-view J callback itself, and the menu simulator dispatcher
cannot stand in for it. Continue only if a real-firmware patch decision needs
that callback identity; do not treat the generic OK handler as the hook.

Method: read-only static decode and initialized option-table checks, plus
Nikon's official Z 30 manual; no firmware bytes/dumps recorded and no camera
access.

## 2026-10-18: candidate patch-readiness audit remains incomplete (F-216)

A bounded static audit of the private candidate's storage/layout checks found
the following explicit gaps: worst-case worker-stack headroom is not proven;
the candidate code spans have not been verified executable; and code packing
is incomplete. The existing proposed code/data regions pass only bounded
zero-fill and pointer/branch spot checks. In addition, the Subject-tracking
menu/navigation manifest needs 72 bytes beyond the current proposed data
spans. No assembly encoding or complete overlay exists. The candidate is
therefore not ready for a camera test even though F-212's constructed-context
guard/ABI controls pass and F-214's action request matches Nikon's native Fn
path. This is a patch-completion problem now; more AF-area menu tracing will
not resolve it. Keep hardware untouched and firmware inputs private.

Method: private read-only static candidate audits; no firmware bytes/dumps
recorded and no camera access.

## 2026-10-18: composed candidate action path passes a repeated QEMU call (F-217)

The current private layout script assembles and links the candidate in memory,
checks its relocations, and produces 45 planned edits. A memory-only QEMU
probe applied those edits to the hash-verified stock guest, then called the
candidate action adapter twice with a manually constructed worker context.
Both calls completed and restored context; both issued action 45 and the same
native request tuple measured in F-214. The existing layout now includes the
72-byte navigation table at an additional candidate region, resolving the
earlier data-capacity arithmetic as a layout proposal. The probe also sampled
an 11,264-byte worker allocation. The original image and QEMU checkout
remained unchanged.

This verifies the linked candidate composition and repeatable dispatch under
the synthetic context; it does not establish natural AE-L/AF-L hook
admission, camera-load executable mapping, worst-case stack headroom, full
image acceptance, or the consumer's start/cancel transition. QEMU does not
model the consumer object and the test context was constructed explicitly.
Therefore the patch has advanced, but is still not test-ready. Continue with
candidate mapping/stack proof and natural input admission only where it can
change that real-camera test decision.

Method: pinned-QEMU memory-only instrumentation with the verified stock image;
no firmware image written and no camera access.

## 2026-10-18: AF-area label catalog is not the tracking entry (F-218)

The older firmware map described the `0x103edda0` label catalog as the
AF-area mode list and called 3D-TRACKING the camera's tracking mode. That
collapsed two different data paths. The address is a text block containing
AF-area labels; the selection case at `0x103edc2e` forms the address of the
3D-TRACKING label and passes it to a shared text-output helper. It is not a
menu option dispatcher. The selectable options are in the separate table
rooted at `0x1074a688`. Its eight rows are Single-point AF, four Wide-area AF
variants, and Auto-area AF plus its people/animal variants. The three
Auto-area values are 600/601/602; the setter stores base mode 6 and a
submode. None of these option rows selects the 3D-TRACKING label.

The menu's OK/J event (`0x27e`) is dispatched through the active screen's
callback. On the AF-area option screen it applies the selected mode. In
shooting view the same J/OK control has a different screen context; the
generic dispatcher/filter has references to the central live-view handler
`0x102f1e10`, but the actual live-view J callback and its link to action 45
remain unidentified. A stock-QEMU probe invoked UI event `0x27e` directly
after simulated live-view setup and completed with context restored, but
only the dispatcher-entry breakpoint fired. This does not demonstrate a
physical input or a complete screen callback and is inconclusive about the
camera route.

This resolves the label/table ambiguity but does not change the patch choice:
use the native Subject-tracking action route compared in F-214, rather than
changing the AF-area selection. Do not use the 3D-TRACKING text as proof of a
selectable Z 30 mode or as an activation hook. The next real-firmware trace,
if needed for the patch decision, is the live-view J callback registration
behind the active-screen key table, compared with the action-45 native Fn
handler. Candidate test readiness is still blocked by the unobserved native
start/stop transition and incomplete executable-mapping/stack proof; no
camera test is authorized by this finding.

Method: read-only verified-image static decoding and option-table
enumeration; bounded stock-QEMU synthetic UI event. No bytes/dumps recorded,
no firmware image written, no camera access.

## 2026-10-18: J reaches generic live-view input handling, not a proven tracking action (F-219)

Continued from the AF-area text labels and the key dispatcher rather than
from the old property `0x2021` lead. The `3D-TRACKING` text is selected by
the status renderer when descriptor byte `[r4+0x83]` is 8, then sent through
text helper `0x1027f3cc`. The same routine reads several status properties,
including `0x10b4`, but the available static edges do not identify the
producer or semantics of that descriptor byte. This is a display path; it
does not call the tracking action helper.

Auto-area selection is separate: mapper `0x10430c8c` reads the eight-row
table at `0x1074a688`, and setter `0x1042b2d8` stores base mode 6 and submode
0 for Auto-area value 600 (people/animal variants use submodes 1/2). The
selection handler's visible continuation updates dependent AF-area state; it
does not directly invoke the native tracking action.

For shooting-view J/OK (`0x27e`), the generic dispatcher `0x103ce96e`
consults filter `0x104e2cbc`. The filter first consults runtime key-to-
function lookup `0x10460ba2`, which can invoke a registered callback. A
separate matching screen-context path calls generic live-view input handler
`0x102f1e10` with `(r0=0, r1=1, r2=0, r3=0)` plus a stack argument. Its
direct body tests input/status changes
through `0x102f1cae` and `0x102f0e1e`; no direct branch from it reaches
action helper `0x10368b6e` or request service `0x1045a47e`. The actual
runtime J callback is not statically resolved, and an
indirect callback-to-action edge remains possible but unproved. This is the
precise boundary of the current static trace: Auto-area selection establishes
eligibility, while J reaches generic live-view event handling; neither path
yet proves the tracking-start/stop action.

Patch decision is unchanged. F-214's matched action-45 request remains the
best concrete native tracking hook for the AE-L/AF-L candidate. The next
real-firmware trace, if it can change that hook decision, is resolving the
runtime active-screen J callback registration and comparing its target with
the action-45 path. Do not infer activation from the 3D-TRACKING label or
from the generic live-view handler.

Method: read-only Thumb decode and full-image direct-branch scan against the
hash-verified input; no firmware bytes/dumps recorded, no image written, no
camera access.

## 2026-10-18: action 45 AF-state routing and correction (F-221)

The higher-value trace from the AF-area mode setter into native action 45
shows the action itself consumes AF-subsystem state. Helper `0x10368b6e`
calls mapper `0x1044dc5a`; the mapper snapshots 0x468 bytes, requires base
mode 6 at snapshot offset `+0x44`, then reads submode `+0x61` and another
state byte `+0x62`. In submodes 0 and 2, state bytes 0/2 select internal
state 1 and byte 1 selects state 0. In submode 1, state 0 selects internal
state 2 and state 1/2 selects state 3. Selector 45 routes internal states
0/1, 2, and 3 to helpers `0x1045a1ae`, `0x1045a1e6`, and `0x1045a21c`.
The mapper receives a copied AF subsystem snapshot; the match between base
mode 6/submodes 0-2 and the separately decoded Auto-area AF setter is strong,
though the snapshot's exact field identity with those public properties is
not independently proven.

This trace also corrects two earlier descriptions. `0x1045a47e` is a
boolean gate (it calls `0x102240ac` and reads state at `0xc23a51a8`), not
the request service reported in F-214. And the helpers' apparent event
destination `0x1046296e` is a one-instruction `bx lr` stub, not an event
poster. Their downstream semantics remain unknown, including which path
starts or ends tracking. The native action still appears to be the right
patch-side operation because its handler branches on current AF state; no
second patch-side cycle should be invented from the present evidence.

The next valuable decode is the state writer for snapshot byte `+0x62` or
the substantive callees under `0x1019596e`, if it can distinguish tracking
start/cancel without returning to the exhausted property-`0x2021` lead. The
patch is still not ready: natural AE-L/AF-L hook admission, camera-load
executable mapping, worst-case stack, and an integrated test image remain
open. No camera contact or firmware artifact.

Method: read-only, hash-verified Thumb disassembly; addresses and field
offsets only, no firmware bytes/dumps recorded.

## 2026-10-18: action 45 helper chains remain semantically unlabeled (F-222)

Continued through the helper chains selected by the AF-state mapper. In
Auto-area AF submodes 0 and 2, both mapped state values 0 and 1 route through
`0x1045a1ae` to `0x10230832`, which calls `0x1019596e` with byte input 0.
That routine gates on AF readiness/state and writes byte value 6 at an
AF-related object offset; its alternate input 1 writes 7, but the action-45
caller supplies 0. This is a native state operation, though its meaning is
not established.

In people submode 1, mapped state 0 selects `0x1045a1e6` -> `0x10230856` ->
`0x10162f14` -> `0x1007756e`, while mapped state 1 or 2 selects
`0x1045a21c` -> `0x10230866` -> `0x10162f18` -> `0x100775c6`. The last two
functions branch on a shared configuration object's state and modify
multiple internal fields through common config helpers. Their values and
field names are not decoded as subject tracking state, so the two paths
cannot safely be labeled start and cancel from this evidence.

The static evidence now shows a state-aware native action and the distinct
helper paths it selects. Nikon's manual still supplies the user-visible
contract (press to start, press again to stop in Auto-area AF); neither the
static trace nor the unmodeled QEMU consumer verifies that cycle at runtime.
The candidate's natural AE-L/AF-L admission and build-readiness checks remain
open. No camera contact or firmware artifact.

Method: read-only, hash-verified Thumb disassembly; addresses and field
offsets only, no firmware bytes/dumps recorded.

## 2026-10-18: queued-input route does not establish physical AE-L/AF-L delivery (F-223)

Reinspection of the queued-input consumer corrects the physical-input
attribution previously made in the deep firmware map. `0x103a3f9e` consumes
queued logical-ID/operation records, looks up the record ID in the selected
map, applies the resulting mask to staging word `0xc18c9a68`, and calls
`0x101e383a` if that word changes. It does not read a physical SW-bank word;
`0x115c694c` belongs to the surrounding module's object/initialization path.

The map's ID 41 -> mask `0x2000` relation and the debug switch table's
AEAF_LOCK -> SW0 mask `0x2000` relation remain valid independently. No
reviewed edge joins the physical switch to queued ID 41 or to the candidate
accessor hook `0x102f14b2`. The native action-45 design remains the best action-
side evidence, but natural AE-L/AF-L admission is unresolved. Do not treat the
logical mask match as proof that the physical button reaches the candidate.

Method: bounded reinspection of hash-verified Thumb disassembly around
`0x103a3d14`–`0x103a400c`; data-flow description only. No bytes/dumps, image
writes, or camera access.

## 2026-10-18: candidate mask checks decode as a one-sided change (F-225)

Rechecked the candidate's raw ring-word tests against the exact helper layout
before changing its predicate. Helper `0x101dd502` writes two input words,
their XOR, and the first-input-only and second-input-only portions at offsets
0, 4, 8, 12 and 16. The first such block built by `0x102f199a` begins at
record offset +4. It compares `input1 | input2` against `input2`, so the
candidate's tests for bit `0x2000` at record offsets +4/+8/+12/+16 as
set/clear/set/set mean the bit appears only in the first input. That is a
valid one-sided difference shape; the fields are not mutually exclusive after
the record-relative offset is applied.

The two direct callers of `0x102f199a` are `0x1039e1d4` and `0x1046497e`.
The candidate hook is evaluated in a separate live-view context (`0x102f751c`)
and receives the selected record from `0x102f1412`. The mask algebra alone
does not identify the input words as physical switch state, prove which side
is the newer sample, or connect `0x2000` to AE-L/AF-L. Continue by tracing
those builder callers' input records to their producer and only then decide
whether the current candidate edge guard is a valid AE-L/AF-L trigger.

Method: hash-verified Thumb static data-flow review; addresses and field
offsets only. No firmware bytes/dumps, image edits or camera access.

## 2026-10-18: AE-L/AF-L remap uses the native action, but its input hook remains open (F-226)

The configurable-action comparison identifies the correct action-side
primitive. Fn1's handler `0x1036957c` reads setting `0x1150`; when it is 77,
it passes its argument to `0x10368b6e`, Nikon's native Subject-tracking
handler. The AE-L/AF-L handler `0x10369468` instead reads setting `0x1184`
(or `0x1187` in its alternate mode), checks values 25 and 42, and never
calls action 45. This means that adding an AE-L/AF-L menu label alone cannot
produce the desired behavior; the button's real fresh-press path must reach
the native action-45 handler, or the AE-L/AF-L configured-action route must
be extended to do so.

The nearby calls at `0x103020b4` and `0x10302108` are not the physical key
action entry: the surrounding dispatcher combines returned handler bits and
returns a status mask. They are unsuitable as the proposed press hook. The
current candidate at `0x102f14b2` remains unproven because its returned
record has not been traced to the physical AE-L/AF-L switch (F-223–F-225).
The next build-relevant trace is to identify the actual button action path
and determine whether it can safely branch to action 45 on a fresh press
only. Keep Auto-area AF as the camera configuration; no AF-area remap is
needed.

Method: bounded, hash-verified Thumb disassembly review of the action
handlers and their status dispatcher. High confidence for the call and
return-mask relationships; physical input origin, settings-menu behavior,
and start/stop cycle remain unknown. No firmware bytes/dumps, image edits,
or camera access.

## 2026-10-18: registered snapshot callback reaches AE-L/AF-L's AF-ON route (F-227)

Callback `0x102f2eae` is registered through the module's snapshot callback
slot. It calls `0x102f0d14`, whose result indicates that the larger input
snapshot changed, then inspects the snapshot. Its AE-L/AF-L branch tests bit
`0x2000` at record offset +4. If setting `0x1184` is 9 (the AF-ON assignment),
it posts event `0x14` through `0x1044e68c`. This is the first static path in
this trail that ties the named AEAF_LOCK bit to AE-L/AF-L's existing
assignment behavior.

The callback is a useful prospective hook for the remap, but it does not yet
prove a fresh AE-L/AF-L edge: `0x102f0d14` reports a broad snapshot change,
and the callback tests the current switch bit. If another input changes while
AE-L/AF-L stays held, the branch may run again. A safe action-45 substitution
needs a per-button rising-edge guard and must preserve current AF-ON behavior
for the normal assignment. The callback's registration proves a route exists;
it does not prove the physical event cadence, exact previous/current field
relationship, or successful tracking cycle. Continue by tracing the
snapshot-difference record around this callback and identify a specific
AE-L/AF-L transition field that can guard one native action-45 call.

Method: read-only, hash-verified Thumb control-flow/data-flow review. High
confidence for the callback, mask test, setting check, and event post; no
claim about press-only execution or camera behavior. No firmware bytes/dumps,
image edits, or camera access.

## 2026-10-18: keep the shared action dispatcher in scope (F-228)

Correction to F-226: `0x103020b4` and `0x10302108` are within the same
input/action dispatcher family that calls the Fn1 configurable-action handler
`0x1036957c`; that sibling handler calls action 45 when setting `0x1150` is
77. Although the dispatcher combines returned bits into a mask, that does not
establish that it is only a status query. The two cited sites call AE-L/AF-L
handler `0x10369468`, whose body still has no action-45 branch. The dispatcher
and handler are therefore valid static candidates for the remap trace, while
the physical key-to-case selection remains unknown. Do not discard this path
or treat it as confirmed physical delivery until the event input is traced.

Method: bounded Thumb disassembly review of the shared switch and the
configured-action sibling. High confidence for dispatcher/callee control
flow; physical delivery and the correct patch seam remain open. No firmware
bytes/dumps, image edits, or camera access.

## 2026-10-18: AE-L/AF-L input mapping and OK/J simulator boundary (F-229)

The live-view input mapper walks a group-1 mask-to-logical-input table. The
`0x2000` mask maps to logical ID 13; the UI table maps ID 13 to event `0x28b`,
labelled “AE-L/AF-L button.” The registered snapshot callback
`0x102f2eae` independently checks that same bit and posts the existing AF-ON
route when the AE-L/AF-L assignment has value 9. This is stronger input
provenance for the snapshot callback than for the candidate ring-record
accessor at `0x102f14b2`. The candidate's context dispatcher explicitly
admits logical ID 13, matching the mask-to-ID table. The candidate's paired
ring-record source remains the gap; the table alignment makes the trigger
candidate more plausible but is not an end-to-end producer trace.

The current private candidate implements the requested user-facing
assignment: its extended AE-L/AF-L list uses the verified “Subject tracking”
label, stores configurable-action value 77 in setting `0x1184`, and routes
that selection to native action 45. This closes the menu-value/action mapping
at design level; it has not been validated as a rendered, saved camera menu.
The remaining work is candidate-side edge/cycle control and build readiness,
with physical press admission reserved for the permitted device test after
all other gates.

The `3D-TRACKING` text remains in the status-renderer label catalog, not the
selectable AF-area option table. Auto-area AF is therefore the operating
precondition for Nikon's native Subject-tracking action 45; the user-facing
remap target is Subject tracking on AE-L/AF-L, not a selectable 3D-TRACKING
AF-area row. The shooting-view J/OK action is routed through the generic
dispatcher `0x103ce96e`, which obtains handlers from runtime tables. In a
pinned-QEMU probe, synthetic `0x27e` reached that dispatcher and generic
lookup, but no registered callback, action 45, or AF-area setter was observed.
A separate synthetic `0x28b` probe also produced no downstream action. These
negative observations reflect the simulator's incomplete event setup/model;
they do not negate the static firmware links.

Build implication: the current candidate already supplies the intended menu
and action mapping, and its ID-13 gate matches the static AE-L/AF-L input map.
Keep Auto-area AF and retain action 45 as the native bridge. The ring-record
producer and real press admission remain unproven, but the owner has assigned
physical press confirmation to the later device test. Before that test, the
candidate itself still needs a sequential fresh-start, held-suppression,
release, and fresh-second-edge action/cleanup control in the bounded
simulator. No camera access.

Method: read-only hash-verified Thumb/table review and synthetic pinned-QEMU
event dispatch. High confidence for static input-map and callback relations;
the simulator probes did not reach the real registered callback, and no
physical press or tracking cycle is claimed. No firmware bytes/dumps, image
edits, or camera access.

## 2026-10-18: sequential candidate edge/control probe (F-230)

A separate memory-only probe drove the private candidate through fresh,
held, release, and second-fresh records. First fresh and second fresh each
passed the edge guard and called native helper `0x10368b6e` (action 45) once;
held and release produced no action call. The adapter returned and restored
its constructed context, and the candidate's dispatch-finish cleanup block
was executed with a constructed caller frame. The recorded ABI save/restore
checks passed.

This closes the candidate's bounded edge-arbitration and dispatch-control
check. It does not close the full cycle criterion: the consumer's AF state is
not modeled, so the probe cannot say whether the first call starts tracking
or the second call ends it. Full native context dispatch was not traversed;
the guest was patched through debugger writes, not loaded from a private
overlay. Physical hook admission, camera-load executable mapping, worst-case
stack headroom, and complete-image acceptance also remain open. Keep Auto-area
AF and the AE-L/AF-L assignment design, but the candidate is not yet ready for
a camera test. No camera was accessed.

Method: private pinned-QEMU run with hash-verified stock image; synthetic
input records and constructed caller frames. See F-230 in `facts.md`.

## 2026-10-18: action-45 AF snapshot state source (F-231)

The action state mapper `0x1044dc5a` reads snapshot bytes `+0x61` and `+0x62`
after its 0x468-byte state snapshot is formed. The AF snapshot producer copies
the corresponding bytes from internal AF-context offsets `+0x364` and
`+0x365` in the context rooted at `0xc237c7b4`. Builder `0x101925ee` assembles
this context and subcontext from the live AF object; `0x101914ae` fills the
state slots through mode-dependent branches. Some branches copy the state
byte from an AF subcontext field at `+0x25`; others leave it zero or set the
companion discriminator. This proves that action 45 consumes a native AF
state tuple. The code does not give the tuple a tracking name or label its
values as active/inactive, so start/cancel semantics remain unresolved.

A new disposable-QEMU run exercised native Auto-area setter `0x1042b2d8`
with encoding 600. Properties `0x0c2b` and `0x0c3d` read back as base mode 6
and submode 0; the AF snapshot property's value and Fn assignment value 77
also read back. Yet action 45's AF mapper returned state 5 for each of three
native Fn-handler calls and did not reach the Auto-area-specific helpers.
This shows the stock simulator fixture fails to reflect those properties in
the AF snapshot consumed by action 45. It cannot validate the actual toggle.
Together with F-230, the evidence supports one fresh action-45 dispatch per
fresh AE-L/AF-L edge, but does not prove native start or second-press cancel.
The private candidate still requires no-debugger-write overlay loading,
executable mapping, worst-case stack proof, and full-image acceptance before
it can be considered testable; the physical press/cycle remains the assigned
later device test. No camera was accessed.

Method: read-only hash-verified Thumb review with LLVM disassembly, then
pinned-QEMU stock firmware with guest-RAM-only property setter/action calls.
See F-231 in `facts.md` and private report `action45-autoarea-03/semantic.json`
under the owner's local private input directory; the report is not in the
repository.

## 2026-10-18: LLVM-linked candidate loaded by QEMU (F-232)

The private candidate was rebuilt and linked using the installed LLVM tools,
without Capstone. The bounded link/layout audit placed 964 bytes of code in
the planned 1,408-byte code regions, checked 24 relocations and 15 four-byte
hook windows, and emitted the same 45 planned edits. No full firmware image
was written.

The edits were split into 35 private loader regions and passed to the pinned
QEMU process through its generic loader at startup. Before resuming the guest,
the probe read every region back and matched it byte-for-byte to its intended
overlay. The source firmware hash and QEMU checkout stayed unchanged. With
those loader regions active, a bounded synthetic fresh/held/release/fresh
sequence exercised the candidate: first and second fresh records each
dispatched action 45 once; held and release records dispatched nothing. The
constructed cleanup and ABI controls passed.

This closes private-overlay loading without debugger writes and candidate
assembly/layout reproduction in QEMU. It does not prove the camera's loader
maps the code executable, physical AE-L/AF-L delivery, or whether action 45
starts tracking and cancels it on the second press. The AF consumer remains
unmodeled in the simulator, and worst-case task-stack headroom is still open.
Keep Auto-area AF and the Subject-tracking assignment on AE-L/AF-L as the
target behavior; the private candidate remains not camera-testable. No camera
was accessed and no firmware bytes/dumps were added to the repository.

Method: LLVM assembly/disassembly and a private overlay passed to the pinned
QEMU generic loader before guest resume; guest memory was read back before
execution, followed by constructed-context edge/action probes. See F-232 in
`facts.md`.

## 2026-10-18: runtime TTBR0 mapping remains a camera-load gate (F-233)

The candidate code spans all lie in VA page `0x1002d000`, within the startup
L1 section for VA `0x10000000`. Reset-time table entry `0x10030400` is a valid
section mapping with XN clear under the ARMv7 short-descriptor format. This
does not settle the camera's runtime table: full-image ARM/Thumb disassembly
found later TTBR0 writes in scheduler/context-switch paths. The scheduler
loads an optional TTBR0 pointer from a task context at `+0xc0`; a distinct
helper accepts a table pointer and changes TTBR0 with the MMU temporarily
disabled.

In the pinned simulator, the candidate task's TTBR override at `+0xc0` was
zero, while a read-only CP15 probe found a runtime TTBR0 table and MMU enabled.
`ATS1CPR` translated candidate VA `0x1002da00` outside the simulator's
modeled RAM, yet the QEMU loader overlay executed from that VA. The simulator
machine defines no matching backing alias, so this discrepancy makes its
translation result unsuitable as camera mapping proof. It does not invalidate
the bounded overlay behavior test. The camera-load executable mapping remains
open; next trace which runtime table the Subject-tracking task inherits and
how its entry for `0x1002d000` is constructed or updated. Keep Auto-area AF
and native action 45 as the remap design. No camera contact.

Method: read-only LLVM disassembly of the verified original plus a private
loader-based QEMU run with privileged-register and `ATS1CPR` reads. See F-233
in `facts.md` and the ARMv7-A/R [short-descriptor reference](https://documentation-service.arm.com/static/5f8daeb7f86e16515cdb8c4e).

## 2026-10-18: candidate stack watermark attempt was inconclusive (F-234)

A read-only QEMU canary probe gave the constructed candidate adapter a
synthetic caller stack pointer and marked the available bytes below it. The
adapter returned, but the probe recorded zero native action calls and no
candidate/native execution path. The only changed bytes were a 64-byte
boundary region attributable to synthetic call setup, so this run cannot
measure candidate stack depth or establish headroom. The harness also did not
verify every restoration write; the disposable QEMU process exited and the
verified original firmware hash and simulator checkout remained unchanged.
Treat this as a probe/harness failure, not a stack pass or firmware behavior.
Repair the constructed action-path setup and require observed native action
entry before interpreting a watermark, while tracing runtime TTBR0 table
construction separately. No camera contact.

Method: private pinned-QEMU loader overlay with synthetic stack canary and
constructed context; output retained outside the repository. See F-234 in
`facts.md`.

## 2026-10-18: corrected stack watermark reaches action 45 (F-235)

The follow-up reused the validated loaded-overlay setup and successful
fresh-edge copy/action construction, then marked 2,048 bytes below the
synthetic action-call SP. First fresh reached native helper `0x10368b6e`
once with action 45 and changed 1,364 canary bytes; held and release reached
it zero times; second fresh reached it once and changed 1,324 bytes. The
worker TCB reports an 11,264-byte stack. The changed spans are bounded
measurements for this constructed path; they do not cover natural task
admission, all interrupt/scheduler interleavings, or full native AF-consumer
execution. They narrow the stack risk but do not prove worst-case headroom.
F-235 supersedes F-234's failed probe setup while retaining its warning that
the first measurement was invalid. Runtime executable mapping and AF
start/cancel gates remain open. No camera contact.

Method: private pinned-QEMU generic-loader overlay; 2,048-byte synthetic
stack canary below a constructed action frame and SP captures at candidate
and native call boundaries. See F-235 in `facts.md`.

## 2026-10-18: action-45 AF gate requires one exact snapshot state (F-236)

Read-only disassembly resolves why the simulator's action-45 run stops early.
The caller at `0x1044dcbe` calls mapper `0x1044dc5a`; it returns immediately
unless the mapper result is 2. The mapper returns 2 only when the snapshot's
AF mode byte at `+0x44` is 6, state byte `+0x61` is 1, and companion byte
`+0x62` is 0. The mode value matches the Auto-area base mode previously
identified in F-215/F-231. QEMU's observed mapper result 5 therefore follows
the native rejection branch and never calls `0x1045a21c`.

On the accepted state-2 branch, `0x1045a21c` calls `0x10230866` before
forming an event-code `0x3d` request. `0x10230866` in turn invokes
`0x100775c6`, a stateful routine that reads and updates a native object; its
tracking semantics are not named by static evidence. The event call target
`0x1046296e` is a return-only stub in the verified image. Thus the route
through the AF-state gate is real and its exact precondition is now known,
but this does not prove that the stateful routine toggles Subject tracking or
that the stub delivers an event. Static analysis and the current simulator
cannot establish start-versus-cancel behavior. The candidate still emits
action 45 on each fresh edge; its edge logic passed constructed controls but
does not compensate for a failed native AF-state precondition. Keep Auto-area
AF, runtime executable mapping, worst-case stack, and native consumer
semantics open. No camera contact.

Method: LLVM Thumb disassembly of mapper, action gate/helper, event call, and
the downstream stateful routine in the verified original. High confidence in
the numeric state conditions and call edges; no semantic label is assigned to
state 2 or the stateful routine. See F-236 in `facts.md`.


## 2026-10-18: scope correction for the state-2-only mapper caller (F-237)

Cross-checking against F-221/F-222 shows `0x1044dcbe` is a separate caller of
mapper `0x1044dc5a`, not the main action-45 selector `0x10368b6e`. The
state-2-only condition and tuple recorded in F-236 apply to that separate
caller and its path to `0x1045a21c`; they must not be generalized to all
action-45 dispatch. The main selector handles mapped states 0 through 3 as
already documented: in Auto-area submodes 0/2 it routes states 0/1 to
`0x1045a1ae`, while submode 1 uses the other two helpers. State 5 still
produces no helper call in the observed QEMU case, but this is not evidence
that state 2 is the sole permitted action-45 state. F-237 supersedes that
overbroad reading of F-236 without discarding the separate caller's exact
precondition. For the requested plain Auto-area mode, the useful next trace
is the semantics of `0x1019596e` and its written AF-related byte, plus a
per-button rising edge at snapshot callback `0x102f2eae`; do not treat the
unproven ring producer as resolved. Start/cancel and candidate natural
admission remain open. No camera contact.

Method: cross-checked read-only Thumb disassembly of both mapper callers and
the selector branch against F-221/F-222. High confidence in call-site
separation and mapped-state routing; no action-cycle claim. See F-237.

## 2026-10-18: corrected AE-L snapshot-edge hook prototype (F-238)

The snapshot updater's aligned four-byte instruction is at `0x102f0d30`, not
`0x102f0d32`; the latter is the second halfword of that instruction. The
corrected private prototype hooks the aligned instruction before the native
snapshot clear/copy, where `r4` is the new snapshot and `r6` is the previous
global snapshot. It tests the `0x2000` AE-L/AF-L mask for a 0-to-1 change,
checks setting `0x1184 == 77`, and calls native Subject-tracking action 45.
The normal assignment value 9 does not take this new branch.

LLVM assembled and linked the corrected prototype, checked 27 relocations,
16 hook windows and 47 planned edits, and kept all output outside the
repository. A disposable pinned-QEMU loader run read back 39 overlay regions
and exercised synthetic fresh/held/release/fresh snapshots. Action 45 entry
counts were 1/0/0/1. For this test only, the shim returned through a private
`bx lr` trampoline instead of running the native updater tail; the production
layout replays the displaced `movw r1, #0x190` and branches to the aligned
continuation `0x102f0d34`.

This closes a synthetic edge-dispatch check, not physical AE-L/AF-L delivery
or Subject-tracking start/cancel. The shared updater has seven direct callers,
including callback `0x102f2eae` and paired-record construction paths; an inline
action at the shared site can run on more than one caller's stack/context.
That call-context and stack risk, runtime executable mapping, worst-case
stack, and full-image acceptance remain open. The official Auto-area AF
precondition remains the chosen operating mode. No camera contact.

Method: hash-verified read-only Thumb disassembly, LLVM assembly/link, and
private pinned-QEMU generic-loader overlay with synthetic snapshots. High
confidence for alignment and the bounded dispatch counts; no physical-input
or consumer-cycle claim. See F-238 in `facts.md`.

## 2026-10-18: plain Auto-area helper mutates AF state but remains unnamed (F-239)

The main action-45 selector's plain Auto-area helper is `0x1045a1ae`. It
clears an AF-related object field at `+0x40` and calls `0x10230832`, which
reads an input byte and passes it to `0x1019596e`. That routine checks several
readiness/status conditions, then writes byte 6 for input 0 or byte 7 for
input 1 at an AF-related object field at `+0x38`; it performs additional
object/update calls before returning. The wrapper then forms event `0x3b`
through `0x1046296e`, which is a return-only stub in the verified image.

This establishes a stateful native route behind action 45, but no available
label ties the object fields or values 6/7 to tracking active/inactive. The
second fresh action may select a different AF state route, but that mapping
does not by itself prove cancel behavior. Keep the manual's expected cycle as
the real-camera validation criterion; do not claim the native cycle is solved
by static analysis or the synthetic QEMU edge test. No camera contact.

Method: read-only LLVM Thumb disassembly and register/data-flow review of the
plain Auto-area helper, wrapper and writer. High confidence for control flow
and byte values written, none for Subject-tracking semantics. See F-239 in
`facts.md`.

## 2026-10-18: shared updater callers expose inline-stack tradeoff (F-240)

The seven direct callers of `0x102f0d14` do not establish a single safe
execution context. Callback `0x102f2eae` and four other wrappers pass a
snapshot pointer through `r4` and invoke the shared updater. Paired-record
builder `0x102f199a` invokes it twice, first with `sp`, then with `sp+0x18c`,
after reserving a `0x31c`-byte local frame. An action-45 call inserted at the
common updater would execute on whichever of these callers first observes the
fresh bit; the builder path adds the native action stack to an already deep
frame. The remaining wrappers have small visible frames, but their owning
task/thread and total available stack have not been traced.

Hooking only callback callsite `0x102f2ece` gives a narrower context but may
miss the rising edge if an earlier caller updates the shared previous
snapshot first. The next build decision is to map the callers to their task
contexts and stack budgets, then choose a common edge latch or callback
consumer that preserves both reliable edge delivery and bounded stack. No
camera contact; no claim that the current inline common-site candidate is
safe. See F-240 in `facts.md`.

Method: read-only LLVM Thumb review of the seven direct callsites and the
paired-record builder prologue. High confidence for callsite shapes and the
`0x31c` frame reservation; thread identity and stack capacity remain unknown.

## 2026-10-18: configurable-handler route is a narrower remap hypothesis (F-241)

The dispatcher `0x10301f36` selects handlers by a function-code argument.
Its code `0x2d` branch reaches Fn1 handler `0x1036957c`. That handler reads
Fn1 assignment property `0x1150`; value 77 calls native Subject-tracking
action 45. The separate AE-L/AF-L handler `0x10369468` reads assignment
property `0x1184` or `0x1187`; the reviewed branches recognize values 25 and
42 and do not accept 77. The existing AE-L/AF-L custom-control assignment
candidate can store value 77, so the missing native-side behavior is localized
to the handler path.

Two patch hypotheses remain: add a value-77 branch to the AE-L/AF-L handler,
or route the AE-L/AF-L function code through the Fn1 handler. The dispatcher
also builds a status mask, and the current review does not establish its
entry cadence, physical press semantics, whether the caller passes identical
state to both handlers, or whether the Fn1 branch is safe with AE-L/AF-L's
context. Do not patch the status-mask call sites themselves. Next trace the
dispatcher caller and compare both handlers' argument and return contracts;
prefer a narrow AE-L/AF-L handler extension if it can be shown to preserve
the configured control's normal behavior and fresh-press semantics. Keep
Auto-area AF; native action 45 remains the desired behavior. No camera
contact.

Method: read-only LLVM Thumb disassembly of the function-code switch and both
handlers, cross-checked against the existing action-45 static trace. High
confidence for the property IDs and numeric branches, no claim for physical
press cadence or native start/cancel. See F-241 in `facts.md`.

## 2026-10-18: handler extension reaches action 45 in synthetic QEMU (F-242)

A private pinned-QEMU test temporarily redirected the value-77 case inside
AE-L/AF-L handler `0x10369468` to native action 45 (`0x10368b6e`). The tested
branch point was `0x103694a4`, after the handler reads the assignment from
property `0x1184` or `0x1187`; the helper calls action 45 for value 77 and
continues to the existing handler exit. In constructed direct calls, value
77 reached action 45, value 42 reached the existing `0x103691fc` path, and
value 25 reached `0x1036845a`. The helper and branch were restored before the
simulator exited, and both the firmware hash and simulator checkout remained
unchanged.

This demonstrates that a small handler extension can preserve the sampled
25/42 alternatives while routing 77 to Nikon's native action. It does not
show the event that invokes function code 13, whether that event is a fresh
AE-L/AF-L press, or whether it repeats while held. Nor can QEMU's unmodeled AF
consumer show the action's second-press cancellation. Next trace the runtime
producer/registration for the function-code dispatcher and determine whether
AE-L/AF-L invokes handler 13 once per button event. Keep Auto-area AF and the
native action-45 target. Do not call the design testable until physical-event
cadence and remaining image/runtime build gates are resolved or explicitly
assigned to the permitted device test. No camera contact.

Method: LLVM-assembled helper and temporary GDB memory writes in a disposable
pinned-QEMU process, with action-45 and existing handler-path breakpoints;
all guest writes were restored and verified. High confidence for synthetic
handler behavior only. See F-242 in `facts.md`.

## 2026-10-18: dispatcher caller does not establish button dispatch (F-243)

A full-image scan of Thumb BL and B.W immediates finds one direct caller of
function-code dispatcher `0x10301f36`, at `0x10302270`. This lies inside
callback `0x10302220`, which accepts only incoming values `0x1a`, `0x1b`, or
`0x1c` before forwarding that value. The dispatcher's first TBB maps value
13 to AE-L/AF-L handler `0x10369468` and value 45 to Fn1 handler
`0x1036957c`; values 26/27/28 map to different handlers. The high-range
dispatch table also contains an AE-L/AF-L status call, but the observed
callback inputs do not reach it. A literal pointer to dispatcher
`0x10301f36` is absent from the firmware image. Computed or runtime
registration-based invocations remain possible, so the static direct-call
scan does not rule them out.

This weakens the dispatcher as a remap hook: F-241/F-242 show that the
handler can route value 77 to action 45, but not that an AE-L/AF-L press
invokes it. Next trace how callback `0x10302220` is registered/populated and
look for indirect dispatcher invocations; if that path does not connect value
13 to the physical control, resume the input-chain rising-edge source rather
than extending this handler further. Keep Auto-area AF and action 45 as the
desired behavior. No camera contact.

Method: address-only Thumb BL/B.W immediate scan over the verified module,
then LLVM disassembly of the caller and TBB table. High confidence for the
direct call and decoded switch indices; runtime/indirect callers remain
unresolved. See F-243 in `facts.md`.

## 2026-10-18: direct synthetic callback probe did not return (F-244)

A direct thread-aware QEMU call to registered snapshot callback
`0x102f2eae`, with a synthetic 396-byte record containing mask `0x2000`,
timed out before return and produced no action-45 breakpoint. The test's
record validity and callback scheduling contract are unknown. The result
does not establish failure of the natural callback or absence of an action
route. The simulator process exited and the firmware identity and simulator
checkout were unchanged. Treat this as a single negative simulator diagnostic;
do not repeat the same direct-call setup. Next continue static registration
and caller-context analysis for the callback, while resolving the common
updater's stack/runtime gates for the already-tested rising-edge candidate.
No camera contact.

Method: memory-only GDB call in disposable pinned QEMU with synthetic input;
high confidence for timeout and zero observed action entries, no inference
about natural callback execution. See F-244 in `facts.md`.

## 2026-10-18: shooting-view J callback remains a runtime table target (F-245)

The AF-area label and selectable mode paths remain separate from Subject
tracking activation. Label routine `0x103edc2e` passes the `3D-TRACKING` text
to formatter `0x1027f3cc`; the selectable table at `0x1074a688` contains
Auto-area AF and its variants but no 3D-TRACKING row. Selecting value 600
calls setter `0x1042b2d8`, which stores base mode 6/submode 0. This is the
documented eligibility setup, not the action itself.

For shooting-view key event `0x27e`, filter `0x104e2cbc` calls runtime lookup
`0x10460ba2` with the four-entry table at RAM address `0xc183d150`. The lookup
compares the key in each table record, loads its callback pointer, and invokes that
pointer indirectly with `blx r3`. Thus the J callback depends on the active
screen's runtime table; there is no static direct edge from the generic
dispatcher to Subject-tracking action 45. The bounded synthetic QEMU event
reached the generic screen dispatcher but did not observe a
callback-table invocation or action 45. It remains inconclusive about natural
J delivery.

This reinforces keeping Auto-area AF as the prerequisite and native action
45 as the best action-side remap target. The actual runtime J callback could
still be compared against action 45 if its table population is resolved, but
the current trace does not offer a safer or more direct patch hook. The
AE-L/AF-L candidate remains untestable pending input admission and build
readiness gates, and the native start/cancel cycle is still not observable in
QEMU. No camera contact.

Method: read-only Thumb disassembly of the key filter/lookup and AF-area label
routine, cross-checked against the prior synthetic `0x27e` QEMU result. High
confidence for the runtime indirect lookup and label/option distinction; no
claim for callback identity or physical J behavior. See F-245.

## 2026-10-18: sampled J callback table has no direct tracking action (F-246)

Read-only guest-RAM inspection after the standard simulated live-view setup
sampled the filter's four-entry key/callback table at `0xc183d150`. Entries
were `(0x161b, 0x104e2e85)`, `(0x23e4, 0x104e2ea1)`,
`(0x1536, 0x104e2ec7)`, and `(0x14c2, null)`. The three callback bodies
perform state checks and fill response records; none directly calls native
Subject-tracking action 45.

A fresh pinned-QEMU synthetic event `0x27e` reached `0x103ce96e` and generic
screen handler `0x103ce804`. Breakpoints on filter `0x104e2cbc`, runtime
lookup `0x10460ba2`, the three callbacks above, and action 45 did not fire.
So this simulator event did not reach the active key callback lookup. It
does not exclude the camera's physical J route or identify the real active
screen callback. This bounded trace gives no competing direct action hook;
retain native action 45 as the best target for the AE-L/AF-L assignment and
do not claim OK/J has been remapped or verified. No camera contact.

Method: address-only static decode of the three targets and read-only QEMU
guest-memory/breakpoint inspection. High confidence for the sampled table
contents, callback bodies and stop locations; no claim for camera J behavior
or native tracking cycle. See F-246.

## 2026-10-18: use one trigger path in the AE-L/AF-L candidate (F-247)

The private production overlay currently combines two independently tested
trigger paths: common snapshot updater hook `0x102f0d30` and ring-record
accessor hook `0x102f14b2`. The snapshot hook detects the `0x2000` rising edge
with assignment 77 and calls action 45 inline. The accessor hook captures a
matching ring-record edge, then its worker adapter calls the same action 45.
F-238's snapshot-hook edge test and F-230/F-235's worker-route sequence were
separate; neither tested one physical event through the composed overlay.
Without shared deduplication, a press reaching both paths can issue two
native toggle requests. The snapshot hook also runs on any updater caller,
including the paired builder with its `0x31c`-byte local frame (F-240).

For the single-button test candidate, select only the worker-mediated
accessor route at `0x102f14b2` and omit the common-updater action hook. This
uses the constructed fresh/held/release/fresh dispatch evidence and bounded
worker stack watermark while avoiding inline action on seven updater
contexts. The ring record's physical AE-L/AF-L provenance remains explicitly
unverified and belongs to the owner's later device test after all other
gates; the existing input map and callback both use mask `0x2000`, but this
does not prove the complete source path. The native action's start/second-
press cancel result is likewise reserved for that bounded device test under
the existing owner disposition. Do not present the combined two-hook overlay
as testable. Remaining pre-test gates include camera-load executable mapping,
complete image/layout acceptance, and hardware-readiness/recovery records. No
camera contact.

Method: compared address-only private manifests and hook bodies with the
separate synthetic QEMU tests F-230/F-235/F-238. High confidence that the
candidate has independent action paths and unarbitrated duplicate potential;
no claim that natural camera input reaches both. See F-247.

## 2026-10-18: worker hook continuation ABI review (F-248)

The selected single-hook candidate branches from `0x102f14b2` over the stock
mutex-address load and `ADDS` that computes the unlock argument. The stock
`ADDS` leaves NZCV for the continuation, so this is a live mid-function ABI
contract. The candidate's ordinary and tracking paths both end by loading the
same address and performing the same addition, then branch to the original
unlock call at `0x102f14b6`. In the tracking path it saves/restores `r0-r3`,
`r5-r7`, and LR; it does not modify `r4` or `r8-r11`, and returns with SP
restored. This preserves the original returned record pointer and flag result
at the stock tail. This closes the local ABI contract at the selected
accessor hook, not the complete ABI review of the larger 15-hook candidate or
worst-case task-stack analysis. The worker-only 35-region overlay was executed
by the separate loader-based QEMU runs F-232/F-235; the generated manifest's
`guest_execution: false` records build-time state only. Camera-load executable
mapping and complete-image acceptance remain open. No camera contact.

Method: read-only Thumb disassembly and candidate assembly inspection, with
cross-check against the existing private QEMU reports. High confidence for
the local hook continuation/register/flag contract; no claim for natural
button delivery or camera execution. See F-248.

## 2026-10-18: runtime candidate-page table is outside the captured module (F-249)

A bounded ARM-mode scan of TTBR0 writers found a later MMU setup sequence at
`0x11c9e784`–`0x11c9e7c0`. It disables the MMU, loads a literal with value
`0xc11f8000`, writes that address to TTBR0, flushes translation state, then
reenables the MMU. This is a real firmware table-selection path, but the table
itself is in RAM outside the captured firmware module. Its descriptor for
candidate code VA `0x1002d000` is therefore not available in the static input.
The scheduler's per-task TTBR0 override at context `+0xc0` remains a separate
path from F-233. This pass does not establish that the later setup feeds the
candidate worker or that the page is executable in its inherited map. The
camera-load mapping gate remains open; further simulator translation probing
cannot fill in the absent runtime table. No camera contact.

Method: full-image ARM disassembly filtered to TTBR0 writes, plus read-only
literal decode at the identified setup sequence. High confidence for the
sequence and RAM table base; no claim for the missing descriptor or task
mapping. See F-249.

## 2026-10-18: no simple executable-cave relocation in hook sections (F-250)

The current candidate needs about 964 bytes of code. A bounded scan of the
verified image found no zero-filled span of 32 bytes or more in the 1 MiB
sections containing the relevant trigger/action/menu hook sites
(`0x10200000`, `0x10300000`, `0x10400000`). This rules out a straightforward
move into an empty span alongside those existing hooks. It does not rule out
reusing nonzero dead code, but that would be a new code-replacement design
requiring fresh control-flow, behavior and ABI review. The reviewed free code
capacity remains at `0x1002d000`, where runtime mapping is unresolved by
F-249. Keep the patch candidate on hold rather than claiming the alternate
placement is safe. No camera contact.

Method: read-only scan for zero-filled intervals in the three hook-related
1 MiB sections; only interval addresses and lengths were retained. High
confidence for the scan and minimum span threshold; it does not establish
that every nonzero interval is active code. See F-250.

## 2026-10-18: QEMU runtime descriptor read for candidate code page (F-251)

The existing display-machine map includes the firmware's RAM table address
`0xc11f8000`; the simpler `nikon-z30` machine profile does not. In an isolated
QEMU 10.2.4 build using the display profile and the verified original C1.20
module, the standard assisted live-view diagnostic setup was followed by a
read-only CP15 probe. Its active TTBR0 table was in modeled RAM. The probe
read the computed L1 entry for candidate VA `0x1002d000` through QEMU's
physical-memory monitor, decoded a valid section descriptor with XN clear,
and confirmed that its target is in modeled display RAM. `ATS1CPR` for
`0x1002da00` agreed with the descriptor and reported no translation fault.
The probe itself executed from that VA page and returned with the caller's
register context restored.

This is QEMU evidence for the diagnostic task's active table. It is not yet
the tracking worker's descriptor, and it does not establish that the camera
constructs the same table at runtime. Next, run the descriptor check while
executing in the tracking worker context. No QEMU source change was made in
the repository, and the camera was not accessed.

Method: isolated QEMU machine-model build, original module identity check,
guest CP15 diagnostic call, QEMU physical read of the computed table entry,
and cross-check against `ATS1CPR`; descriptor bits and firmware bytes were
not retained in the repository. High confidence for this QEMU task/context;
no claim for camera behavior. See F-251 in `facts.md`.

## 2026-10-18: worker-context table probe remains unavailable in QEMU (F-252)

A follow-up used a thread-aware wait after the same standard assisted
live-view setup and held a breakpoint at tracking-worker entry
`0x102f7448`. The guest ran for 20 seconds without reaching that entry, so no
worker-context CP15 state or table descriptor could be captured. This
matches F-213's earlier absence of worker-entry/cleanup hits. It is a limit of
this bounded simulator setup, not evidence about the camera's scheduler or
the worker's real mapping. No repository QEMU source changed. Do not extend
simulator scheduling work on this path; return to real-firmware static
evidence or a reviewed, available source for the runtime table. See F-252.

## 2026-10-18: diagnostic task's active table differs from the boot table path (F-253)

A fresh read-only CP15 probe after the standard assisted live-view setup
reported active TTBR0 base `0xc2ad4000`. Its computed L1 entry for candidate
VA `0x1002d000` is a valid section mapping with execute permission, targeting
the modeled display RAM; `ATS1CPR` agreed without a translation fault. A GDB
write watchpoint on this exact entry did not fire during an eight-second
window after setup. This is the diagnostic task's active table, not a
tracking-worker capture. It also distinguishes that table from F-249's
separate static MMU path selecting `0xc11f8000`; the latter cannot be assumed
to be the active table for this QEMU context. The result does not establish
the real camera's mapping or close the worker-context gate. Per F-252, stop
this simulator scheduling path absent a new worker stimulus.

Method: isolated pinned QEMU 10.2.4, standard assisted live-view fixture,
read-only CP15/ATS probe and QEMU-memory watchpoint on the computed entry;
no raw descriptor or firmware bytes retained. High confidence for this
diagnostic task and interval only. No camera access. See F-253.

## 2026-10-18: bounded camera identity and operation inventory probe (F-254)

Added `src/nikon_z30_research/ptp_device_info.py`, a direct libusb PTP client
that sends one standard GetDeviceInfo request to USB ID `04b0:0452`. It
returns identity fields and the camera-advertised PTP operation codes, while
discarding the serial number and storing no response file. It opens no PTP
session and sends no vendor operation, property, object, or memory request.
The transport does not change USB configuration, select another alternate
setting, detach a host driver, or reset the device; a busy interface is a
hard stop. This may show whether stock firmware advertises a read operation,
but it cannot read the runtime table itself. No camera was connected or
queried.

Six synthetic tests cover the exact request, identity/operation parsing,
serial omission, and malformed containers. No hardware transport result is
claimed. Use only the documented identity command after the owner connects
the camera; do not call any advertised Nikon vendor operation without its own
review and approval. See F-254 and `camera-readonly-identity-method.md`.

## 2026-10-18: host USB enumeration path is available, camera absent (F-255)

Loaded the installed libusb runtime, enumerated the host USB device list, and
checked only descriptors for the Z 30 USB ID. Enumeration succeeded and found
zero matching devices. This check opened no device, claimed no interface, and
sent no PTP operation. It confirms the host-side discovery prerequisite for
the new identity probe, not the camera's USB interface or any live-memory
route. Once the owner connects the camera, run only the documented
GetDeviceInfo preflight; any advertised vendor command remains a separate
review. See F-255.

## 2026-10-18: camera identity query succeeds with host USB access (F-258)

The documented probe succeeded when run with host USB access after the
sandboxed libusb enumeration returned zero devices. It sent only standard PTP
GetDeviceInfo (`0x1001`) and reported Nikon Corporation, Z 30, device version
V1.20, and the camera-advertised operation list. The serial was not returned
or saved. The list includes familiar Nikon property, live-view, and object
operations from the prior local review, and operation `0x9535`, which is not
identified by the local reviewed references. No vendor operation was sent.
This confirms identity/inventory access only; it does not expose runtime
TTBR0 or a live-memory read. Do not invoke the unknown code without a separate
source/method review and approval. See F-258.

## 2026-10-18: local PTP lookup does not identify a runtime read (F-259)

Searched project notes, source and tests, along with installed libgphoto2 PTP
documentation and headers, for advertised operation `0x9535` and reviewed
runtime-memory reads. No operation mapping or suitable read method was found.
Do not invoke the unknown code. This exhausts the local-source lookup branch,
but does not prove no undocumented interface exists. The owner later
authorized read/write experiments in principle and named stock-firmware
reinstallation as the recovery plan. That does not identify or review a
specific command; exact-method review and method-specific approval remain
required. The camera's active tracking-worker mapping is unobserved. Resume
with relevant static firmware evidence or a newly reviewed camera method; do
not repeat the closed QEMU scheduling trace without a new stimulus. See F-259.

## 2026-10-18: native request cycle passes constructed QEMU controls (F-260)

A corrected paused-QEMU memory-only diagnostic supplied the status record
action 45 actually reads. With mode 0, assignment `0x1184=77`, Auto-area
status `(area=6, pair=0,0)`, and a fresh decision, the candidate reached the
native start request and changed the tracking pair to `(1,0)`. A second fresh
decision with `(area=6, pair=1,0)` reached the native stop request and cleared
the pair to `(0,0)`. Held/no-decision called neither path. The earlier state-5
result was a fixture error: it populated low-level fields instead of the
copied status record. This confirms native request-cycle routing under a
constructed state contract, but not natural camera state, physical AE-L/AF-L
admission, successful subject acquisition, or asynchronous completion. See
F-260.

The next high-value device observation is a stock-camera reference through a
control already assigned to native Subject tracking. It can verify real
start/second-press cancellation and release/hold behavior without claiming
that the AE-L/AF-L candidate hook has been admitted. Keep runtime code mapping
and physical AE-L/AF-L delivery as separate candidate gates.

The owner offered to run the test manually. Use the reproducible scenario in
the Lane 3 handoff: stock V1.20, still-photo, Auto-area AF/AF-C, temporarily
assign Fn1 to Subject tracking, tap/release once, observe marker/acquisition,
then fresh-press to cancel; separately check hold/release and restore Fn1's
original assignment. Record the exact state changes and any half-press needed.
The owner states that stock-firmware reinstallation is the recovery plan for
a future camera write; that path has not been independently verified. See
F-260 and `handoff-codex.md`.

## 2026-10-18: stock Fn1 Subject-tracking behavior (F-261)

The owner tested the stock Z 30 with Fn1 assigned to Subject tracking. A single
press and release displayed the target; holding also displayed it, and the
target persisted after release. A second tap ended tracking. Holding behaved
like tapping. The owner reports tracking did not activate until shutter
half-press, after which the target began following the subject. This is useful
native-control evidence: Fn1 appears toggle-like, shutter half-press gates
activation, and acquisition succeeded in the reported scenario. It does not
prove AE-L/AF-L input delivery or operation of the candidate hook. See F-261.

The proposed PTP event-endpoint monitor is implemented and locally tested,
but has not been run on the camera. It listens for standard PTP events during
a bounded button sequence; no event would be inconclusive. Its exact method
and approval boundary are in `camera-ptp-event-monitor-method.md`. Do not run
it until the owner approves that exact method. See Lane 3 in
`handoff-codex.md`.

## 2026-10-18: identity transport revalidated (F-262)

The host USB registry sees the Z 30. Sandboxed libusb enumeration returns no
matching device, while the existing pre-approved standard PTP GetDeviceInfo
probe succeeds with host USB access and reports firmware V1.20. The advertised
operation list includes standard OpenSession and CloseSession, the two session
operations used by the bounded event monitor. This resolves the current
connection-path question for identity access; it does not show that button
events are delivered on PTP or expose runtime memory. See F-262 and
`camera-ptp-event-monitor-method.md`.

## 2026-10-18: PTP event monitor preflight stop (F-263)

The owner approved the bounded event monitor. It stopped before opening the
device or sending OpenSession because the active descriptors did not satisfy
the unique default PTP interface plus interrupt-IN endpoint check. No event
poll or button test occurred. The result does not prove that no event endpoint
exists; the aggregate error does not expose which descriptor condition failed.
A separate, descriptor-only report is prepared at
`camera-usb-descriptor-method.md` and needs its own approval before use. See
F-263.

## 2026-10-18: PTP endpoint packet-size mismatch corrected (F-264)

The approved descriptor-only report found a single default Still Image PTP
interface with the expected bulk-IN, bulk-OUT, and interrupt-IN endpoints.
The event endpoint's maximum packet size is 8 bytes. This explains F-263:
the monitor had required at least 12 bytes in a single USB packet, although
the PTP event container header is 12 bytes and can be collected across
multiple smaller USB packets. The monitor was revised offline to request up
to 24 bytes (header plus three 32-bit parameters) per event transfer and to
accept the 8-byte endpoint. Synthetic tests cover endpoint selection. The
revised camera method needs new exact approval; no retry has occurred. See
F-264 and `camera-ptp-event-monitor-method.md`.

## 2026-10-18: zero-byte event poll handled within bound (F-265)

The next approved monitor run opened its PTP session, then the first
successful interrupt-IN transfer returned zero bytes. No event container was
received. The code treated the zero-byte transfer as malformed and stopped
early; its cleanup path attempted CloseSession, but the acknowledgement was
not surfaced. USB permits zero-length data transfers, so the revised monitor
now treats an empty transfer as no event and continues within the original
15-second bound; malformed nonempty data still stops. The owner says the
bounded method does not require renewed permission, but wants a warning before
each window and an explicit start signal before it begins. No retry has yet
occurred. See F-265 and the method document.

## 2026-10-18: four AE-L/AF-L presses correlate with FocusMeteringMode events (F-266)

After the owner gave the requested start signal, the revised bounded PTP event
monitor completed a 15-second run. The owner pressed AE-L/AF-L four times
during the window. The monitor returned exactly four standard
`DevicePropChanged` event containers (`0x4006`), each carrying property code
`0x501c`, and no other event. In the standard PTP property table, `0x501c` is
`FocusMeteringMode`, a UINT16 property selecting the automatic focus
mechanism. It is not a named physical button event, and Nikon-specific enum
values are not yet known.

The one-for-one count is the first live evidence that AE-L/AF-L presses on
this body coincide with a specific PTP-visible tracking/focus-mode property
notification. It is not enough to claim causality: the event does not include
the new value, and another concurrent change could produce the same property
notification. The result narrows the next real-firmware question from generic
button delivery to the mode transition represented by `FocusMeteringMode`.
The monitor used only standard OpenSession/CloseSession and interrupt-IN
polling; it issued no property query, vendor operation or write and retained
no raw packet. See F-266 and `camera-ptp-event-monitor-method.md`.

Next useful step: offline-review a single-property, read-only PTP query for
the standard descriptor/current value of `0x501c` before and after a controlled
button press, with no property-set or vendor command. Any new camera query
method requires its own method review and the applicable exact approval; if
using the event monitor again, warn first and wait for the owner's start
signal before every 15-second window.

## 2026-10-18: second PTP window repeats the property, not the press count (F-267)

In a second 15-second run of the same approved event monitor, the owner pressed
AE-L/AF-L three times. Two events arrived, both `DevicePropChanged` (`0x4006`)
for `FocusMeteringMode` (`0x501c`). This is consistent with the first run's
association but disproves a dependable one-event-per-button-press assumption.
Possible causes include a press that did not change the property, event
coalescing, or unrelated focus-mode activity; this monitor cannot distinguish
them because it reports no property value or physical-key identity.

The hook question is therefore not answered by counting PTP events. The
highest-value follow-up is to determine the camera's current `0x501c` value and
supported values using a strictly read-only standard PTP property descriptor
request, then compare the value across a controlled press sequence. Prepare
and review that exact method offline first; do not query the property until
the method and approval boundary are settled. Any further event window still
requires a pre-run warning and the owner's explicit start signal. See F-267.

## 2026-10-18: owner redirects target to always-armed tracking

The owner wants Subject tracking armed continuously in shooting mode: the
reticle should remain visible without pressing a control, and shutter
half-press should begin acquisition. No button should be responsible for
toggling the feature off. This changes the leading build concept from the
AE-L/AF-L input-edge remap to a one-shot call of Nikon's native Subject-
tracking action on a shooting-view entry path.

The lifecycle research already identifies the selector-1 live-view-ready site
at `0x102f5810` inside `0x102f57e2`; the guarded overlay exercised that site
for screen-mask behavior (F-101 and `native-xpan-liveview-hook.md`). Reuse
that work rather than reopening generic lifecycle discovery. The hook's
execution after AF initialization and its suitability for action 45 have not
been tested. Action 45 is stateful, and the constructed native cycle shows a
second fresh request reaches the stop path (F-260). A candidate therefore
needs an exactly-once guard across view transitions and a proof that the first
call is accepted in the real AF-ready context. F-261 supplies the user-visible
contract from stock Fn1 behavior: a persistent reticle followed by tracking
on shutter half-press. No automatic-arm firmware candidate or device result
exists yet.

The event result narrows the state to inspect: `0x501c` is the standard
`FocusMeteringMode` property. An offline-prepared, read-only descriptor query
is documented at `camera-focus-mode-descriptor-method.md`; its exact camera
use is a separate approval step. See F-266/F-267.

## 2026-10-18: scope clarification for continuous Auto-area arming

The owner clarified the condition: while Auto-area AF is selected, Subject
tracking must be in the same ready/reticle state as the native OK/Fn1 action,
without a button press; shutter half-press should start acquisition. This
requires reconciliation at two already-known state changes: selecting or
entering Auto-area AF, and entering a shooting-view-ready state. The existing
selector-1 site `0x102f5810` covers only the latter candidate and has not been
validated for AF readiness or action-45 call context. The Auto-area setter
`0x1042b2d8` establishes base mode 6/submode 0-2, but current research did not
prove that calling action 45 from its selection continuation is safe or that
it observes the settled mode.

Do not repeat broad lifecycle discovery: the lifecycle point is already
researched. The remaining build question is where to reconcile the two state
changes without toggling action 45 twice. Since action 45 has start/stop paths,
the implementation needs a reliable armed-state check or a transition latch
whose reset is tied to leaving Auto-area AF / losing shooting-view readiness.
The native action must be invoked once when the condition becomes true, and
never on ordinary repeated ready callbacks. F-260 only establishes the action
cycle in a constructed simulator context; it does not provide the live camera
armed-state signal or prove either hook's call safety. This is a focused
integration/state-proof gap, not a request to restart the general lifecycle
trace.

## 2026-10-18: standard FocusMeteringMode descriptor is unsupported (F-268)

With the owner's authorization after offline review, the fixed standard PTP
`GetDevicePropDesc` request for `0x501c` was sent once. The camera returned
response `0x200A`, `DeviceProp Not Supported`, on transaction 1. Thus the
property notification observed in F-266/F-267 cannot be read through this
standard descriptor path on the Z 30. The event remains a correlation signal;
it does not reveal the value or an armed-state bit. No Nikon vendor command or
alternate property operation has been tried. The probe reports numeric
response status fields without retaining raw PTP data. Resume with the
firmware state trace / QEMU candidate tests; do not retry this standard
descriptor query expecting a value. See F-268 and
`camera-focus-mode-descriptor-method.md`.

## 2026-10-18: AF byte values 6/7 do not map directly to people/animal modes (F-269)

The proposed people-versus-animal interpretation does not match the decoded
action-45 routes. The Auto-area setter uses submodes 0/1/2 for plain Auto-area,
people, and animals. People submode 1 dispatches to separate configuration
helpers. Plain Auto-area and animal submode 2 share the route through
`0x1019596e`; its action-45 caller supplies input 0, selecting byte value 6.
The same routine selects 7 only for input 1. Thus 6/7 follows the routine's
input argument rather than the people/animal submode. The field's purpose and
the people-specific helpers' meanings are still unknown, so this does not
settle whether either path represents tracking-ready state. See F-269.

## 2026-10-18: action-45 route corrected and status bridge exercised in QEMU (F-270/F-271)

An independent decode of `0x10368b6e` corrects the helper assignment in
F-221/F-222. With action selector 45, mapped AF states 0/1 route to
`0x1045a1ae`; states 2/3 route to `0x1045a21c` -> `0x10230866` ->
`0x100775c6`. The `0x1045a1e6` call is on the separate selector-27 branch.
A bounded four-case QEMU test injected each mapper tuple at the native stack
snapshot after its copy routine and observed the expected mapped state and
helper path. This does not establish how live AF state produces that tuple.

The same QEMU setup then exercised the native status bridge. Routine
`0x101925b0` copies two bytes from its argument to context `+0x61/+0x62` at
`0xc237c7b4`; the decoded caller at `0x10076300` sources them from
`0xc259ff0c+0x38/+0x39`. Starting with synthetic tuple `(6,0,0)`, action 45
took the plain helper chain and changed the status pair to `(1,0)`. Calling
the bridge caused the next action to take `0x1045a21c` -> `0x100775c6`, which
changed the pair back to `(0,0)`. A second bridge and third action returned to
the plain helper. This demonstrates a native software toggle cycle when the
starting tuple is supplied and the status bridge is explicitly called; the
simulator still does not naturally produce the AF tuple or render/track a
subject. See F-270/F-271.

## 2026-10-18: auto-arm overlay blocked before callback (F-272)

A temporary loader overlay was assembled around the known live-view-ready
call and Auto-area setter continuation. It checked Auto-area eligibility,
used a one-shot latch, and called the native status bridge after action 45.
QEMU loaded all five overlay regions into its disposable guest, but stopped
during normal startup before the shooting-view setup. The display profile
reported an unmodeled write to `0x10000aaa` from `0xc2b1065a`; enabling the
documented synthetic no-lens peer did not change the failure. The overlay did
not execute. This does not validate its ABI, timing, exactly-once behavior,
reticle, or acquisition, and must not be treated as a patch candidate. Stop
the simulator-fidelity branch here. Resume with static real-firmware analysis
of the AF state semantics and activation hook contract. See F-272.

## 2026-10-18: AF status bridge is event-driven (F-273)

A static Thumb-call scan found one direct call to `0x101925b0`, at
`0x10076314` inside update routine `0x10076268`. Two direct sites reach that
routine: `0x10156ba0` passes input 0, while `0x10159092` passes input 1. On
the input-0 route, the bridge runs only after AF-state comparison and callback
checks; this is an event-driven update, not a per-frame snapshot refresh. That
matches the QEMU observation that action 45 changed the source pair but the
mapper kept its old tuple until the bridge was explicitly called. Therefore a
live-view auto-arm hook cannot rely on passive context refresh for its
one-shot guard. It needs a reliable latch or a reviewed explicit status refresh
before consulting the mapper snapshot. The event routes' exact relationship to
AF readiness, possible indirect bridge callers, and hook safety remain open.
See F-273.

## 2026-10-18: correction to auto-arm QEMU startup result (F-274)

The startup failure attributed to an unmodeled write in F-272 came from an
invalid temporary overlay: its 44-byte wrapper exceeded the 24-byte verified
zero span and overwrote adjacent firmware. That result does not establish a
simulator peripheral limitation. The corrected wrapper and hooks fit in a
separately verified 512-byte zero cave; the guest then reached live-view
setup. A synthetic Auto-area call through the known ready path reached native
action 45 and its internal return reported success (`r0 == 1`), after which
the overlay called the explicit AF status bridge. The enclosing callback did
not return in the 20-second diagnostic window, with repeated AF-mapper
breakpoint stops afterward. No reticle or subject acquisition was observed.
Next resolve the enclosing callback/worker interaction or exercise the
wrapper through a normal guest-driven ready event; do not treat this as a
testable patch. See F-274.

## 2026-10-18: sparse-breakpoint auto-arm rerun (F-275)

A rerun of the corrected overlay observed only action-45 entry, its internal
return, and the status bridge. The action returned success (`r0 == 1`) and the
bridge ran, but the enclosing direct call to `0x102f57e2` still timed out at
20 seconds. This rerun had only one ignored stop, so repeated AF-mapper
breakpoints were not necessary for the timeout. The cause remains unresolved:
the direct diagnostic may lack the stock worker dispatch context or a normal
completion condition may be missing. Next identify and exercise the live-view
task's stock type-2 dispatch arguments with the corrected overlay. No reticle
or acquisition result exists; this is not a testable patch. See F-275.

## 2026-10-18: corrected type-2 run reaches unmodeled MMIO (F-276)

The stock live-view-object dispatcher is `0x104b912c` with arguments
`[live_view_object, 2, 0]`. Through that route the corrected overlay reached
the ready hook and native action 45, which returned success. QEMU then paused
on a write at `0x10000aaa` (`size=2`, value `0xaa`) from runtime code
`0xc2b1065a`. A private diagnostic no-op for only this exact access allowed
the next write, `0x10000554` (`size=2`, value `0x55`), which paused QEMU in
the same code. This pair is consistent with a NOR-flash unlock sequence, but
the device semantics are unverified. Therefore the earlier timeout is
explained by a concrete unmodeled access in this run, not evidence that the
status bridge itself blocks. Do not fill in guessed flash responses; this
simulator branch ends unless a correct device contract is established. The
dispatcher did not complete, and no reticle/acquisition result exists. See
F-276.

## 2026-10-18: F-276 stop matches the retired flash initializer (F-277)

The stop PC `0xc2b1065a` and LR `0xc2b1013f` match the region and helper-call
return mapped in F-159: shared cached flash identity/geometry initialization
at `0xc2b1012c`. F-159 already found that information-getter and erase/program
wrappers share this initializer, while the outer caller and operation remain
unknown. This is not evidence of a tracking-owned flash write or firmware
update. The `0xAA/0x55` pair is consistent with discovery-command setup, but
the device response remains unknown. F-159 retired further flash-response
modeling, so do not extend the one-off no-op shim. Resume with the tracking
hook and AF-state contract. See F-159 and F-277.

## 2026-10-18: AF byte consumer does not identify 6/7 (F-278)

The field written as 6 or 7 by `0x1019596e` is read by a separate routine at
`0x1018cd9c`, which proceeds only when that same byte equals 1 and its own
context/flag checks pass. The access confirms a shared AF-state byte but does
not label values 6/7 as people/animal selection or as tracking-ready. A
standard USB PTP event window would not expose this internal byte: the earlier
`FocusMeteringMode` notifications lacked a one-event-per-action mapping, and
the standard descriptor query for that property was unsupported. Continue
with offline state-writer/consumer tracing; do not use another PTP window to
infer the byte's value. See F-278.

## 2026-10-18: native AF status-pair writer found (F-279)

Routine `0x10078aa0` writes `(1,0)` to the mapper source bytes
`0xc259ff0c+0x38/+0x39`, plus adjacent AF configuration fields. A direct
call-site scan found its caller at `0x1007445c` within updater `0x10073ed2`.
The updater is called by `0x10078b50`, which is reached from an event-mask
path through `0x10074492` and dispatcher `0x100746dc`. The branch into the
writer depends on state at `0xc18c7228+0x14` and `0xc18c7128+0x10`; no decoded
evidence connects those checks to Auto-area selection or tracking readiness.
This supplies a concrete native state producer to target in a focused QEMU
callback test, but it does not name `(1,0)` as ready/tracking-active. See
F-279.

## 2026-10-18: callback-level QEMU control lacks AF object context (F-280)

The event dispatcher `0x100746dc` tests input bit 0 via `lsls #31`; it does
not select bit 31. In a bounded pinned-QEMU call with synthetic mask 1, the
dispatcher entered `0x10074492` but took its early branch: the service check
at `0x100744bc` returned 1, and `r4` remained zero at `0x1007450e`, leading
to `0x100745f4`. The call completed and source pair stayed `(0,0)`; the AF
updater and pair writer were not reached. Thus this direct callback test
needs a native AF object context to go further. No peripheral contract was
tested or changed. See F-280.

## 2026-10-18: Auto-area action input does not encode people versus animals (F-281)

Rechecked the precise caller data-flow behind F-269. In action selector
`0x10368b6e`, the Auto-area state-0/1 route stores zero in a local byte at
`0x10368bc2`, then passes that byte's address through `0x1045a1ae` to
`0x10230832`. That helper loads the byte and calls `0x1019596e`; this final
routine writes 6 for input 0 and selects 7 only for input 1. The same selector
route applies to Auto-area submodes 0 and 2, while people submode 1 uses
separate helpers. Consequently, the action-45 path writes 6 for both plain
Auto-area and animal Auto-area, so 6/7 is not the People vs Animals selection
in this selector path.

A second direct caller, at `0x10458dfe`, passes 1 into `0x1045a1ae`. Its
branch is gated by a configuration property check, native-helper success
checks, and an AF record byte at `+4` equal to 2 or 3. The record producer
and the meaning of those values remain unresolved; this separate path could
still represent an AF category. It prevents extending the action-45
conclusion into a claim about every use of the 6/7 field.

A repeated USB PTP button-event window would observe external events only; it
cannot read this local stack byte or the internal AF record. The existing PTP
event correlation also was not one-event-per-press, and the standard property
descriptor query was unsupported. Another USB window therefore has low value
for resolving this byte. No camera contact or firmware bytes/dumps. See F-269
and F-281.

## 2026-10-18: Auto-area setting still lacks AF callback context in QEMU (F-282)

Repeated the F-280 callback probe after the synthetic live-view setup and
after invoking the native Auto-area setter with value 600. The setter
returned success. The subsequent event dispatch at `0x100746dc` still
entered `0x10074492` with service check `0x100744bc == 1`, then observed
`r4 == 0` at `0x1007450e` and returned through `0x100745f4`. The source pair
at `0xc259ff0c+0x38/+0x39` stayed `(0,0)`; the AF updater and pair writer
were not reached.

This narrows the simulator limitation: the ordinary synthetic live-view
startup plus native Auto-area selection do not create the AF object required
by this callback in the present QEMU setup. It does not establish that the
callback is unavailable on the camera, nor does it name the pair as a ready
state. A useful next QEMU experiment needs a statically traced native
AF-object constructor/registration path to seed the context. Do not guess
EXMCU or ISP responses. The run used a QEMU binary and custom machine sources
matching their private build manifest, checked the original firmware
identity, and did not contact the camera. See F-280 and F-282.

## 2026-10-18: dispatcher initialization bit does not create AF object (F-283)

The dispatcher `0x100746dc` tests bit 11 first and calls `0x10078c50` when it
is set; it then tests bit 0 and calls AF callback `0x10074492`. A combined
mask `0x801` exercised this native order in pinned QEMU after synthetic
live-view setup and successful native Auto-area selection (600). The
initializer ran, but the callback's service check at `0x100744bc` still
returned 1, its AF object lookup at `0x1007450e` returned null, and the
source pair at `0xc259ff0c+0x38/+0x39` stayed `(0,0)`. This rules out the
dispatcher initializer alone as the missing fixture step. Continue by tracing
the producer/registration for the object list read through `0x101885e8`, and
use a native constructor only if that trace supports it. The QEMU binary,
custom source, and firmware identity matched the private manifest; no camera
or USB was contacted. See F-283.

## 2026-10-18: correction to the empty-queue interpretation (F-328)

Static Thumb reinspection shows `0x101885e8` is a generic linked-list
pop-front helper. In `0x10074492`, the list at `0xc259e920+0x70` is checked
for emptiness; a nonempty head is inspected, popped, and moved to another
list at `0xc259e920+0x90`. The QEMU value `r4 == 0` at `0x1007450e` therefore
means the first list was empty in that fixture. It does not indicate a failed
AF-object lookup, and the helper is not an AF-object registry. This corrects
F-280/F-282/F-283 and retires the proposed object-constructor/registration
search through `0x101885e8`. The producer and the queue's relationship to
tracking remain unknown. Resume with the direct AF-ready/reticle hook; follow
the queue producer only if its identity could change that hook choice. No
camera contact or firmware bytes/dumps.

## 2026-10-18: native source-pair transition candidate (F-330)

Hash-verified static Thumb review shows `0x1007756e` is reached through the
dispatch entry at `0x10162f14`. After taking a native lock, it checks the
source state byte at `0xc259ff0c+0x10`; only value 1 takes the write path;
value 0 returns without changing state. It writes
state 4, the pair `(1,1)` at `+0x38/+0x39`, and adjacent status fields. Sibling
dispatch entry `0x10162f18` reaches `0x100775c6`, whose state-dependent
branches clear the pair and related fields. The known writer `0x10078aa0`
still sets `(1,0)` and is called from the event-driven updater through
`0x1007445c`. This identifies concrete native state transitions, but not
their command names or reticle/acquisition effects. Trace the dispatcher
input/registration and half-press consumer before choosing a patch call site;
do not call the `(1,1)` routine based on its writes alone. Candidate 02 stays
NO-GO. No camera contact or firmware bytes/dumps.

## 2026-10-18: action-45 clear path for source state 4 (F-331)

For Auto-area base-mode byte 6, source pair `(1,1)` maps through
`0x1044dc5a` to mapper state 3. The main action-45 selector routes states
2/3 to `0x1045a21c`, which calls bridge `0x10230866`. That bridge tail-calls
`0x10162f18`, reaching `0x100775c6`. When source byte `0xc259ff0c+0x10` is 4,
the routine takes its state-4 table entry, clears the state and resets the
pair to `(0,0)`. Thus after `0x1007756e` sets state 4 and `(1,1)`, replaying
action 45 can take the clear transition. This is consistent with the native
start/cancel toggle cycle and argues against using action 45 itself as the
auto-arm operation. It does not prove visible reticle or half-press
acquisition. Trace the actual native caller that first reaches
`0x1007756e`, including its guards, before selecting the patch hook. No camera
contact or firmware bytes/dumps. See F-331.

## 2026-10-18: mode-conditioned native arming callback (F-332)

The F-330 transition is reached from callback wrapper `0x1028f200`, which
calls the return-only request stub with code `0x33` and then branches to
`0x102bdbb4`. That routine snapshots AF context and calls
`0x1045a1e6` with argument 1 only when base mode byte `+0x44` is 6, source
pair `+0x61/+0x62` is `(1,0)`, and additional byte `+0x415` is zero. The
remaining native chain `0x1045a1e6 -> 0x10230856 -> 0x10162f14 -> 0x1007756e`
sets source state 4 and pair `(1,1)` only when the source state byte is 1.
This is a concrete Auto-area-conditioned
path into the action-45 state-3 pair, but its extra context-byte meaning and
runtime trigger/registration are unknown. It does not prove execution on AF
mode selection or visible reticle behavior. Trace the callback dispatch or
its runtime registration next; avoid repeating generic action 45. No camera
contact or firmware bytes/dumps. See F-332.

## 2026-10-18: native ready-to-active state cycle in QEMU (F-333)

In pinned stock QEMU, a synthetic call to the native ready helper
`0x1045a1ae` with a zero byte followed its normal chain through
`0x10230832`, `0x1019596e`, `0x10162f10`, and `0x100774f4`, producing source
state 1 and pair `(1,0)`. The native status bridge `0x101925b0` copied that
pair into the AF context. Then callback wrapper `0x1028f200`, with Auto-area
mode 6, context pair `(1,0)`, and byte `+0x415 == 0`, reached
`0x1045a1e6 -> 0x10230856 -> 0x10162f14 -> 0x1007756e` and produced source
state 4 and pair `(1,1)`. Wrong mode, wrong context pair, or nonzero extra
byte left the state at 1; calling the final transition with initial source
state 0 also did not arm. This is a constructed native state-cycle result,
not proof that state 1 renders the reticle or that `0x1028f200` is the
physical half-press callback. The patch direction is now to establish state 1
when People/Animal Auto-area becomes active, then preserve the native guarded
state-4 transition. Candidate 02 remains NO-GO. No camera contact or firmware
bytes/dumps. See F-333.

## 2026-10-18: direct xrefs narrow the next hook review (F-335)

A full-image direct-Thumb-call and exact literal-word sweep finds two callers
of Auto-area setter `0x1042b2d8` (`0x1042bac2`, `0x10430c6c`) and two callers
of ready helper `0x1045a1ae` (`0x10368bc6`, `0x10458dfe`). The state-1 writer
`0x100774f4` is reached through tail branch `0x10162f10`; state-4 writer
`0x1007756e` is reached through `0x10162f14`. The guarded wrapper
`0x1028f200` has no direct branch or exact literal-pointer reference in this
sweep; its only observed branch is its tail to `0x102bdbb4`. Thus its runtime
trigger remains indirect or dynamically registered, with no proven link to
physical half-press. The setter is the strongest current hook candidate for
establishing ready state after mode changes, but its complete ABI, settled
AF-context timing, reticle effect and indirect callers remain unverified.
This scan identifies the next review target; it does not make an installable
candidate. No camera access or firmware bytes/dumps. See F-335.

## 2026-10-18: repeating native ready helper preserves sampled active state (F-336)

In pinned stock QEMU with synthetic AF context, native ready helper
`0x1045a1ae` produced source state 1/pair `(1,0)`. After the status bridge
copied the pair into AF context, guarded wrapper `0x1028f200` reached the
state-4 transition and source pair `(1,1)`. Calling the ready helper again
completed its helper chain but left source state 4/pair `(1,1)` unchanged.
This makes a duplicate ready-state write less likely to undo the sampled
native state transition. It does not establish that the other helper side
effects preserve active tracking, identify state 4 semantically, or prove
reticle/half-press behavior. The direct mode-setter hook remains a candidate;
next verify its exact return contract and exercise both event orderings in a
throwaway simulator overlay, without producing an installable image. No
camera access or firmware bytes/dumps. See F-336.

## 2026-10-18: Auto-area properties do not refresh QEMU AF context (F-337)

After standard simulated shooting-view setup, setter values 601 and 602
returned successfully and property getters read back Auto-area base mode 6
with People/Animal submodes 1/2. The separate AF context `0xc237c7b4` still
reported base-mode byte `+0x44 == 0` and pair `+0x61/+0x62 == (0,0)` after
each call. This is the same simulator disconnect between public mode
properties and the native AF snapshot, not evidence of camera behavior or a
failed setter. Stop repeating this setup. The useful next static trace is the
real AF-context producer that populates mode byte `+0x44`, and the callback
that follows its update; this determines whether the setter can be the
immediate ready-state hook or must be paired with that producer. No camera
access or firmware bytes/dumps. See F-337.

## 2026-10-18: callback snapshot exposes the missing QEMU mode field (F-338)

A follow-up sampled the callback's actual local AF snapshot after native
setter values 601/602, the ready helper and status bridge, without writing the
AF-context mode byte. Both property pairs read back correctly, and the source
and copied status pairs were `(1,0)` with the extra guard zero. At callback
snapshot offsets `+0x44`, `+0x61/+0x62`, and `+0x415`, the values were
`(0, (1,0), 0)`. The callback therefore skipped `0x1045a1e6`, leaving source
state 1. This confirms the exercised stock-QEMU route does not fill the mode
byte needed by the callback. It does not establish a camera-side failure.
F-337's read of global context `+0x44` was not the callback snapshot; this
stack sample is the decisive evidence. Stop repeating the property-setter
sequence and trace the AF-context producer/event order that supplies the
callback's mode snapshot. No camera access or firmware bytes/dumps. See
F-338.

## 2026-10-18: AF snapshot mode byte comes from the live AF object (F-339)

Static Thumb tracing resolves the source of callback snapshot byte `+0x44`.
Builder `0x101925ee` copies 0x6c bytes from the live AF object at
`*(root + 0x144) + 0x40` into the constructed context starting at `+0x44`.
It also reads the live object's `+0x40` byte in a mode-dependent branch. The
Auto-area setter `0x1042b2d8`, by contrast, only decomposes its encoded value
and writes public properties `0x0c2b` plus `0x0c3c` or `0x0c3d`; no direct
write from that function updates the live AF object or constructed context.
This provides a concrete explanation for the QEMU observation that public
People/Animal properties read back while the callback snapshot mode stays 0.
It also means the public setter alone is not a proven immediate ready-state
hook: the downstream AF-object writer/update must run before a valid snapshot
exists. The next static target is the writer for live-object offset `+0x40`
and its ordering relative to snapshot construction. This does not establish
real-camera timing, reticle visibility, or half-press behavior. Hash-verified
Thumb decode, 2026-10-18; high confidence in the copy and property-write
dataflow, no claim about camera behavior. No camera access or firmware
bytes/dumps. See F-339.

## 2026-10-18: Auto-area property writes dispatch runtime observers (F-340)

The setter's generic property-write route is synchronous through a callback
dispatcher. Auto-area setter `0x1042b2d8` calls `0x10465990`, which tail-routes
to `0x1021a0c6`. After its property update, `0x1021a0c6` calls `0x10132f8c`
with the property ID and new value before returning. That dispatcher searches
runtime callback records and invokes a matching function pointer, with a
resolver path when its cached target is empty. Therefore a post-return hook
may observe side effects from a synchronous property observer. The exact
observers for `0x0c2b`/`0x0c3d` and whether they update live AF-object `+0x40`
remain unknown; no static evidence yet connects them to the source byte copied
into snapshot `+0x44`. Next trace observer registration/resolution for those
IDs and the live-field writer. This does not prove camera behavior or settle
the hook. Hash-verified Thumb decode, 2026-10-18; high confidence in the
setter-to-dispatch route and indirect-callback structure, no resolved handler.
No camera access or firmware bytes/dumps. See F-340.

## 2026-10-18: QEMU has no observed Auto-area property observer (F-341)

A setter-only pinned-QEMU probe recorded property IDs `0x0c2b` and `0x0c3d`
entering runtime dispatcher `0x10132f8c` for native encodings 601/602. Neither
property reached the dispatcher's indirect listener call or fallback resolver
in the simulated shooting-view fixture. The property getters still returned
base mode 6 and submodes 1/2. This explains the absence of a simulator-side
AF-object update in the tested route, but it does not show that the real camera
lacks these runtime registrations. The stock firmware hash and simulator
checkout remained unchanged; this probe did not call the ready helper or
tracking callback. Next inspect static observer registration/initialization
and the live AF-object `+0x40` writer. Read-only QEMU; no camera access or
firmware bytes/dumps. See F-341.

## 2026-10-18: direct Auto-area setter callers do not arm AF (F-342)

Both direct callers of setter `0x1042b2d8` were reviewed through their
continuations. `0x1042bac2` returns immediately after the setter. `0x10430c6c`
then calls `0x10430b46` for property-to-menu mapping and `0x1042d6de` for
selection adjustment, then returns success. Neither slice calls the ready or
action helper, builds the AF context, or writes live AF-object `+0x40`.
Together with F-340/F-341, this makes the setter a property-selection boundary
but not a proven arm hook; an indirect observer or separate AF lifecycle path
could still update the object. Next find the live AF-object field writer and
its ordering relative to snapshot builder `0x101925ee`. Hash-verified Thumb
review, 2026-10-18; high confidence in the two direct caller continuations,
no completeness claim for indirect dispatch and no camera behavior. No camera
access or firmware bytes/dumps. See F-342.

## 2026-10-18: Auto-area property label consumer is not the AF producer (F-343)

Reviewed static property reader `0x10489832`, which reads base mode
`0x0c2b`, then People/Animal submode `0x0c3d` for Auto-area and maps those
values to menu-label identifiers before issuing UI updates. It does not write
live AF-object `+0x40` or construct the tracking snapshot, so this property
consumer is a menu/display path rather than the missing AF-context producer.
A full-image search for byte stores at displacement `+0x40` yields many
unrelated structure fields; without proving the base pointer, those matches
cannot identify the live AF-object writer. Continue from the object's
lifecycle/registration and the AF callback that consumes snapshot `+0x44`,
not from this label reader or another setter probe. This is static evidence
only; it does not establish runtime observer behavior, reticle visibility, or
half-press acquisition. Hash-verified Thumb decode, 2026-10-18; high
confidence in the label-reader branch and property accesses, no claim about
camera behavior. No camera access or firmware bytes/dumps. See F-343.

## 2026-10-19: snapshot builder's caller is a registered consumer (F-344)

The only direct caller found for snapshot builder `0x101925ee` is handler
`0x1016139e`, which calls it at `0x101613b2` using live-view context
`[r1+0x428]`. A Thumb pointer to the handler appears in a static table at
`0x10161a44`. On the relevant handler path, the builder snapshots the live AF
object, after which the handler reads its fields, including `+0x40`, for
further decisions. The reviewed caller path does not write that mode byte.
This locates an event-driven consumer but does not identify the event
dispatcher, its runtime trigger, or the AF-object producer. Continue tracing
the live AF object's lifecycle/registration upstream; do not treat the
snapshot callback as an arm hook. Hash-verified Thumb decode and bounded
xref review, 2026-10-19; high confidence in the direct caller and local data
flow, no runtime or camera conclusion. No camera access or firmware
bytes/dumps. See F-344.

## 2026-10-18: QEMU limit and hardware-test threshold (F-284)

The owner states QEMU cannot fully establish readiness and approves testing a
prepared patch on the connected camera. A private auto-arm overlay was
rebuilt with an eligibility check for Auto-area base mode 6 and People/Animal
submode 1/2. The bounded type-2 callback did not return from the candidate
wrapper or record the helper/native action entry, so it did not test that
gate, one-shot behavior, reticle or acquisition. Do not repeat this full
callback test. The candidate is still only a disposable loader overlay; it
has no proven still-photo guard and has not been composed or independently
audited as a camera-format image. The appropriate hardware-test point is
after an exact candidate exists, static instruction/layout/register/stack/
return review and independent exact-edit/integrity audit pass, and recovery
risk is recorded. At that point, use a bounded camera test for native reticle,
half-press acquisition and runtime mapping rather than demanding that QEMU
model those camera-specific behaviors. Hardware remains NO-GO until those
preflights are complete. See F-284.

## 2026-10-19: Auto-area property changes set a shared notification mask (F-345/F-346)

The property-batch processor `0x104579a0` sends each changed property ID to
classifier `0x104575d0`. Its exact `0x0c2b` case returns mask `0x04000000`;
then the notification helper passes discriminator `0x56` to return stub
`0x1046296e`. The next edge loads the shared handle and sets the mask through
`0x10199e04` and platform primitive `0x10036334`. This places Auto-area
base-property changes on a concrete asynchronous notification path that
could lead to the AF-object update missing from the direct setter path. The
waiting consumer and its relationship to the registered snapshot callback
`0x1016139e` are unresolved; this trace shows no write to live AF-object
`+0x40` or tracking-ready state. Next trace initialization of the shared
handle and code that waits on it, then establish whether the consumer updates
the object before the snapshot is built. Hash-verified Thumb decode,
2026-10-19; high confidence in the property-to-mask and flag-set path, no
runtime timing or camera conclusion. No camera access or firmware bytes/dumps.
F-346 corrects F-345's description of `0x56` as the queued event.

## 2026-10-19: offset-only AF mode writer candidates classify as setup/reset (F-351)

Reviewed the strongest `+0x40` store candidates from a bounded instruction
scan against the concrete object provenance in F-339. Routine `0x135762`
allocates an object, stores its pointer at root `+0x144`, then initializes
the object's `+0x40` word to zero. Routine `0x143718` resets a similarly
shaped object and also clears `+0x40`. Other candidates operate on a stack
record, an unrelated global structure, or nested subobjects at offsets other
than the root's `+0x144` AF object. These are not the Auto-area mode writer;
they show why a displacement-only match is insufficient. The bounded review
does not exclude indirect aliases or byte-sized writes outside the selected
patterns. Next trace exact root `+0x144` pointer provenance and non-initializer
accesses; if no mode-setting writer emerges, stop static guessing and record
the hook as unresolved pending a valid runtime AF-context trace. This gives no
reticle, half-press, or camera evidence. Hash-verified Thumb review,
2026-10-19; medium confidence in candidate classification, no runtime
conclusion. No camera access or firmware bytes/dumps. See F-351.

## 2026-10-19: correction to the AF mode-byte source pointer (F-352)

Re-read snapshot builder `0x101925ee` instruction-by-instruction. Its input
context is in `r5`; at the mode-6 guard it executes `r1 = [r5]` and then reads
`[r1 + 0x40]`. The mode byte therefore comes from the object pointer stored at
context offset `+0`, plus `+0x40`. The separate object pointer at context
`+0x144` supplies other fields and is not this guard's mode-byte source.
F-339's expression `*(root + 0x144) + 0x40` was incorrect, and F-351 wrongly
classified stores to root/context records as initialization/reset of the mode
object; withdraw that classification. A bounded taint scan from direct
`ldr reg,[base,#0x144]` loads found no immediate same-register byte writer to
`+0x40`; word store `0x307bec` targets the separate `+0x144` subobject. The
next static target is the pointer at context `+0` and its `+0x40` writers,
anchored to the callback's actual context root. No tracking hook or behavior
is established. Hash-verified Thumb review, 2026-10-19; high confidence in
the local pointer/dataflow correction, no runtime or camera conclusion. No
camera access or firmware bytes/dumps. See F-352.

## 2026-10-19: context+0 writer family is table-derived state (F-353)

The corrected pointer-level scan found direct context-first-pointer writers at
section offsets `0x1d84c28` and `0x1e0a9f4`, which are duplicated code paths.
Each receives a state record, loads its first pointer, scans eight entries in
a four-byte-stride table, derives a boolean from entry flags/counts, and
stores it at pointed-object `+0x40`. The first variant then calls a helper
with the inverse boolean. Located callers of `0x1d84c28` are
`0x1d86396`, `0x1d86528`, `0x1d86a6c`, and `0x1d87abe`; the reviewed callers
sit in a larger AF-like event-processing routine and include a zero second
argument. This is a concrete state writer, but its value is table-derived 0/1
rather than Auto-area mode 6, and no local dataflow connects it to properties
`0x0c2b`/`0x0c3d` or the ready helper. Do not patch it as the auto-arm hook.
Next identify the table producer and caller event/registration semantics, and
stop if no Auto-area or ready-state link appears. Hash-verified Thumb review,
2026-10-19; high confidence in local pointer/dataflow, low confidence in
feature semantics, no runtime or camera conclusion. No camera access or
firmware bytes/dumps. See F-353.

## 2026-10-19: correction to the table-producer lead (F-355)

F-354's proposed update address was misidentified. Section offset `0x1d6ba30`
is inside a ring-buffer helper beginning at `0x1d6ba22`, and the cited
`0x1d6cd6` region decodes as unrelated counter/table iteration. These do not
establish the claimed state-record stores or the producer of the table
pointer; withdraw F-354's specific store-site and next-address claims. Keep
only F-353's verified local result: a table-derived boolean is written
through the context-first pointer at `+0x40`, while table provenance remains
unresolved. The next higher-value trace is the direct callers of native ready
helper `0x1045a1ae` at section offsets `0x348bc6` and `0x438dfe`, following
their enclosing dispatch/input sources before assigning feature semantics.
Hash-verified Thumb re-decode, 2026-10-19; high confidence in rejecting the
misidentified addresses, no runtime or camera conclusion. No camera access or
firmware bytes/dumps. See F-355.

## 2026-10-19: native ready-helper callers (F-356)

The ready helper `0x1045a1ae` has two direct callsites. At section offset
`0x348bc6`, an event-like handler switches over codes `0x0b`, `0x19`, `0x1b`,
`0x28`, `0x2c`, and `0x2d`. For `0x1b`, result 0/1 reaches ready with byte 0;
result 2 reaches clear helper `0x1045a1e6`; result 3 reaches active transition
`0x1045a21c` and may loop to ready. At `0x438dfe`, a record-driven dispatcher
checks flags, key/property `0x188c`, record byte `+4` equal to 2 or 3, and
successful state helpers before ready with byte 1. This narrows the native
ready-state routes but does not identify either source as OK, Fn1, or
Auto-area tracking. Trace the containing dispatchers and source-record
producers; stop unless one connects to AF-area selection or tracking state.
Hash-verified Thumb decode, 2026-10-19; high confidence in local control flow,
no feature/runtime/camera conclusion. No camera access or firmware bytes/dumps.
See F-356.

## 2026-10-19: ready-helper callers are not linked to Auto-area (F-357)

Following the callsites into their callers did not produce the desired arm
hook. The `0x348b6e` route is inside configurable-action helpers that read
settings `0x1170`, `0x1141`, `0x1173`, and `0x1144`, then branch on action
values including `0x19`, `0x2a`, and `0x4d`. The known AE-L/AF-L stills
assignment setting is `0x1184`; no local edge ties these setting reads to
that control or to Auto-area. The second caller remains guarded by generic
record state and key `0x188c`. Neither direct ready-helper callsite is the
automatic-arm hook on present evidence. Resume from the Auto-area
base/submode notification consumer or a proven AF-context producer, and
determine whether it can enter the idempotent ready state without toggle
action 45. Static Thumb review and setting-ID cross-check, 2026-10-19; high
confidence for local call paths, no feature/runtime/camera conclusion. No
camera access or firmware bytes/dumps. See F-357.

## 2026-10-19: the table-derived writer caller path does not identify the arm hook (F-358)

Followed F-353's table-derived writer `0x1d84c28` into its processing routine
`0x1d85b44` and enumerated that routine's four direct callsites at section
offsets `0x1d8551a`, `0x1d860c4`, `0x1d86302`, and `0x1d87570`. The reviewed
calls pass internal object/record pointers within the same processing family;
none locally ties the writer to Auto-area properties `0x0c2b`/`0x0c3d`, setter
`0x1042b2d8`, or ready helper `0x1045a1ae`. Dynamic producers/computed
dispatch remain possible, but this bounded static path does not select a
patch hook. Stop extending it absent a new cross-reference. Return to the
Auto-area notification route only through a candidate dispatcher tied to the
three initialized handles; generic wait-wrapper enumeration has not found
its consumer. Hash-verified Thumb disassembly and direct-call sweep,
2026-10-19; high confidence in the direct callers and reviewed local flow,
no feature/runtime/camera conclusion. No camera access or firmware
bytes/dumps. See F-358.

## 2026-10-19: Auto-area mask notification belongs to GUI/property signaling (F-359)

Revisited F-347/F-348's mode-3 initializer at `0x10595840`. Its seven
registered key strings name GUI debug/log controls: debug logging, interface
logging, category/task selection, log skipping, and debug-mode get/set. The
Auto-area property-batch path signals the second of the three handles that
initializer creates. This ties the `0x0c2b` mask to a GUI/property-notification
mechanism, but does not identify an AF-context consumer; the registered
debug-command callbacks do not establish tracking-ready behavior. Retire the
callback-key branch and do not use the shared notification as an AF hook.
Resume from the Auto-area setter's AF-application/update path or another
positively identified AF lifecycle callback. Hash-verified Thumb decode and
local key-string classification, 2026-10-19; high confidence in the key
domain and slot usage, no runtime receiver or camera behavior. No camera
access or firmware bytes/dumps. See F-359.

## 2026-10-19: generic Auto-area property cache is not the AF apply hook (F-360)

Candidate handler `0x1008955c` compares Auto-area base/submode IDs `0x0c2b`,
`0x0c3c`, and `0x0c3d`, then gathers values into a change record passed to
`0x1008945c` for merging into a generic cached-property table. The reviewed
local path does not call the ready helper, write AF-context mode `+0x40`, or
invoke tracking action 45. A bounded direct-call and literal-pointer search
found no static registration/reference to the handler, so it is not
established as an observer callback; computed/runtime registration remains
possible. Do not use it as the automatic-arm hook. Continue only through an
identified AF-application callback after setter `0x1042b2d8`, or resolve a
runtime observer for `0x0c2b`/`0x0c3d` and trace its live-context/ready-state
effects. Candidate 02 remains NO-GO. Hash-verified Thumb review and bounded
xref sweep, 2026-10-19; high confidence for local property-cache behavior and
absence of direct static references, no reachability, AF, or camera
conclusion. No camera access or firmware bytes/dumps. See F-360.

## 2026-10-19: static property observer table excludes Auto-area IDs (F-361)

The dispatcher `0x10132f8c` scans a fixed 200-record table whose IDs are
copied by initializer `0x10132eac` from static table `0x115db4ec`. Scanning
each table record's ID field found no Auto-area base/submode IDs `0x0c2b`,
`0x0c3c`, or `0x0c3d`; the dispatcher's explicit fallback branches also do
not match them. Resolver `0x10132e66` is called only by the initializer and
by the dispatcher after a matching record has no cached handler, so this
resolver cannot supply a missing static Auto-area registration on the reviewed
path. This retires the F-360 generic-observer lead as the AF-application hook,
without ruling out unrelated runtime mechanisms. Resume from AF-specific
context/application code, keeping both Auto-area selection and shooting-view
readiness in scope. Candidate 02 remains NO-GO. Hash-verified Thumb review,
bounded static-table scan, and direct-call sweep, 2026-10-19; high confidence
for this table and its local dispatch, no conclusion about other runtime
paths or camera behavior. No camera access or firmware bytes/dumps. See F-361.

## 2026-10-19: AF-like configuration callback is not an arm hook (F-362)

Followed callback `0x1036c066`, which reads Auto-area properties through
helper `0x1036bff0` and calls `0x1045a47e` on one internal-state branch. The
helper selectors read `0x0c2a`/`0x0c2b` (or alternate properties
`0x56c`/`0x56d`) into generic property records. The callback compares two
configuration structures and changes cached status bytes. The call to
`0x1045a47e` only queries a global status byte through `0x102240ac`; it does
not write tracking-ready state or invoke a tracking action. Its branch is
gated by an internal configuration byte equal to 5, with no proven mapping
to Auto-area People/Animal. This is a configuration reconciler, not the
automatic-arm hook. Resume from a proven live-context mode writer or a
native ready-state caller tied to Auto-area selection. Hash-verified Thumb
dataflow review, 2026-10-19; high confidence in local property reads,
cached-state writes, and status-query contract, no runtime, feature-semantic,
reticle, or camera conclusion. No camera access or firmware bytes/dumps. See
F-362.

## 2026-10-19: snapshot builder consumes an already-present mode-6 context (F-363)

Re-traced `0x101925ee` from registered callback `0x1016139e`. The builder
reads state byte `+0` and mode byte `+0x40` from the object pointer stored at
live-view context `+0`. It enters the extended mode-specific snapshot path
only when those bytes are 1 and 6 and its local output flags at `+0x364` and
`+0x365` are clear. It then builds derived snapshot data through
`0x101914ae`; subsequent copies use the distinct object at context `+0x144`.
The reviewed code reads the source mode/context and populates snapshot output,
but does not set the source mode byte or call the native ready helper. This
is a downstream snapshot consumer gate, not the auto-arm hook. Next identify
who installs the object pointer at context `+0` and updates its `+0x40` byte
before this callback. Hash-verified Thumb review, 2026-10-19; high confidence
in the local gate and copy path, no runtime event order, tracking semantics,
reticle, half-press, or camera conclusion. No camera access or firmware
bytes/dumps. See F-363.

## 2026-10-19: configurable-function callback does not reach AE-L/AF-L case (F-364)

Continued F-243's callback-source search. One static Thumb pointer to
`0x10302220` occurs at file offset `0x1f8af58`, among sibling callbacks in
the configurable-function subsystem. The callback gates through
`0x10485b50`, admits only codes `0x1a`, `0x1b`, and `0x1c`, then calls
`0x10301f36`. Those inputs dispatch to cases other than AE-L/AF-L handler
index 13. Although handler `0x10369468` reads assignment `0x1184`, that
setting read does not establish that a physical AE-L/AF-L press reaches this
handler. The static table initializer and physical-key source remain
unresolved; this dispatcher is not the remap hook. Hash-verified Thumb decode
and full-image pointer scan, 2026-10-19; high confidence in the pointer,
callback gate, and case routing, no physical-input or camera conclusion. No
camera access or firmware bytes/dumps. See F-364.

## 2026-10-19: setter and action selector are not yet an auto-arm hook (F-365)

Rechecked the setter and native action transition against the verified
original. Setter `0x1042b2d8` decodes base mode/submode and writes properties
`0x0c2b` and, for base mode 6, `0x0c3d`; it does not call the tracking-ready
helper. Its known callers at `0x1042bac2` and `0x10430c6c` are setting-commit
and mode-table application paths, without a proven live AF-context lifecycle
edge. Helper `0x1045a1ae` takes a pointer to a byte and delegates through
`0x10230832` into guarded state/configuration code. Selector 45
(`0x10368b6e`) maps the current AF snapshot and selects different native
helpers for mapped states 0/1 and 2/3; therefore calling selector 45
unconditionally on a mode-property update is not a safe automatic-arm design.
The setter is a plausible trigger for explicit mode changes, but cannot alone
cover Auto-area already active on view entry. Next use only a disposable
QEMU overlay to test a setter-hook prototype's native state side effects, and
continue tracing the AF-context lifecycle for the already-selected case.
This remains incomplete: no reticle, half-press, event-order, or camera
behavior is established. Candidate 02 remains NO-GO. Hash-verified Thumb
decode and direct-caller review, 2026-10-19; high confidence in local
contracts, no feature-level or camera conclusion. No camera access or
firmware bytes/dumps. See F-365.

## 2026-10-19: setter-hook guest-RAM prototype reaches native state writer (F-366)

Built a private throwaway overlay, booted the verified stock image in the
pinned QEMU, then wrote only the stub and hook into guest RAM. Constructed
calls to setter `0x1042b2d8` with encodings 601 and 602 hit the new tail-call
stub, called `0x1045a1ae`, and reached its downstream state write with value
6. Encoding 600 hit the stub but skipped the helper. The sampled AF-context
window around `+0x40` did not change for any case. This proves the local hook
branch and helper path under constructed QEMU calls; it does not establish
natural menu dispatch, a visible reticle, half-press acquisition, or startup
with Auto-area already selected. The setter-plus-helper therefore remains a
partial mode-change candidate and does not produce the sampled live-context
mode in this fixture. Next trace who creates/updates the AF context and how
that path runs on stills-view entry. Candidate 02 remains NO-GO. Pinned-QEMU
guest-RAM overlay, 2026-10-19; high confidence in the branch and observed
helper/state-write sequence, no feature-level or camera conclusion. No
firmware bytes/dumps in the repository and no camera access. See F-366.

## 2026-10-19: AF-status pair accessors do not identify the live mode object (F-367)

Followed the only located direct callers of AF-status pair accessors. Getter
`0x10197828` reads bytes `+0x414/+0x415` from status root `0xc237c7b4`; setter
`0x10197c3c` writes those same bytes, and its located caller is
`0x102222aa`. These fields are distinct from the mode-6 snapshot gate, which
reads mode byte `+0x40` from the object pointed to by live-view context `+0`.
They therefore do not establish the mode writer or an auto-arm hook. A
read-only stock-QEMU boot sample found the status root's `+0` pointer null at
the InitTask checkpoint, before simulated stills-view entry. A full-image
instruction scan for displacement `+0x428` found many unrelated structures
and re-observed the known context loads at `0x101613ac` and `0x101613b8`, but
no unique installer. Stop following the pair accessors; trace the event
context owner/initializer that supplies `r1` to `0x1016139e`, then identify
the object stored at its `+0x428` and that object's `+0x40` writer. Candidate
02 remains NO-GO. Hash-verified original Thumb review and pinned-QEMU
boot-state read, 2026-10-19; high confidence in the accessor locations and
boot sample, no stills-view, camera, reticle, or half-press conclusion. No
firmware bytes/dumps in the repository. See F-367.

## 2026-10-19: snapshot callback table belongs to a generic event queue (F-368)

The short routine at `0x10161642` passes two ADR-derived data addresses near
the static callback data to queue setup helper `0x1021cce8`; a separate
nearby registration at `0x101617e4` calls keyed registry `0x101e1c04`. These
setup calls do not identify an AF-context installer. Generic event dispatcher
`0x1021dee4` receives a payload pointer, reads payload fields `+0x42c` and
`+0x428`, then uses the context pointer at `payload+0x428` (including its
byte `+0xe`) before forwarding an event ID and payload to the callback. Its
ordinary `0x041a0040` event is rejected by the AF handler's `0x0002fe3d`
filter. A full-image Thumb scan found neither `MOVW #0xfe3d` nor `MOVT #2`;
computed or table-derived sources remain possible. This confirms the handler
is an event consumer, not a demonstrated Auto-area context installer or
tracking hook. Stop this callback branch unless a new source for the accepted
event appears. Return to the live AF object's context `+0` installation and
its `+0x40` writer, using proven pointer flow rather than offset-only
matching. Candidate 02 remains NO-GO. Hash-verified Thumb/table review,
2026-10-19; high confidence in the local queue/dispatch flow, no accepted-
event producer, reticle, half-press, or camera conclusion. No firmware
bytes/dumps in the repository. See F-368.

## 2026-10-19: standard QEMU view setup still lacks the AF context (F-369)

Ran the project's standard pinned-QEMU stills-view setup with a breakpoint on
snapshot callback `0x1016139e`. Setup completed, but the callback was not
reached and status-root `0xc237c7b4 + 0` remained null. This fixture cannot
expose the camera-time AF-context producer; stop repeating this simulated
view-entry sequence. A targeted full-image Thumb scan also found no simple
same-register sequence that moves immediate 6 directly into a
`STRB [register,#0x40]` within the previous 12 decoded instructions. Loaded
constants, copies, indirect stores, and computed values remain possible.
Continue static work on the proven object pointer and writer; do not select a
hook from offset-only matches. Candidate 02 remains NO-GO. Pinned-QEMU
diagnostic and targeted static scan, 2026-10-19; high confidence in the
bounded observations, no camera or feature-behavior conclusion. No firmware
bytes/dumps in the repository. See F-369.

## 2026-10-19: Auto-area setter caller is the explicit menu path (F-370)

Decoded the enclosing routine for setter callsite `0x10430c6c`.
`0x10430baa` reads current base/submode properties `0x0c2b`/`0x0c3d`, maps
the selected AF-area table entry, calls setter `0x1042b2d8`, then updates
selection state and menu UI through `0x10430b46` and `0x1042d6de`. This is an
explicit menu-selection operation, not a stills-view entry or live AF-object
lifecycle callback. A setter hook can catch a menu change but cannot cover
Auto-area already active on stills-view entry. Continue looking for the
stills-view/AF-application path with the live context pointer; candidate 02
remains NO-GO. Hash-verified Thumb decode, 2026-10-19; high confidence in the
local menu dataflow, no reticle, half-press, or camera conclusion. No
firmware bytes/dumps in the repository. See F-370.
