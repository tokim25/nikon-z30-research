# Tracking screen/UI state: stacks, mode selectors and event routing

Consolidated 2026-10-16 from: tracking-screen-stack.md,
tracking-registry-mode-state.md, tracking-mask-namespaces.md,
tracking-ui-event-router.md. Content is unchanged from those files except
for heading levels (bumped one level to nest under this file). Sections
below are in the order the research happened; later sections build on
earlier ones where noted.

No section here shows a successful physical button press or tracking
activation. Each section states its own confidence and limits; read them
individually before citing any single address as an approved entry point.

---

## 2026-10-15: An empty screen stack in the assisted live-view fixture

*(formerly `tracking-screen-stack.md`)*

Date: 2026-10-15. Two offline simulator runs, unchanged firmware.

The screen-stack container reached through `0xc181e4f0` had count zero
before startup, after the known assisted live-view startup, and after one
stock refresh. A second run repeated those results, then the existing
audited menu-entry diagnostic populated two entries (screen IDs 1 and
`0x351`). No direction, OK, AE-L/AF-L or tracking event was injected.

Getter `0x1046109a` uses helper `0x10365ff0`: count is at container `+8`,
stride at `+0`, storage at `+0x0c`; count zero returns no slot. The outer
getter then returns no descriptor. Independent static review confirmed this
layout. The menu control supports the observation method; it does not
identify the shooting screen or its key map.

The fixture can render its synthetic preview with this native stack empty.
A preview alone therefore does not establish the screen state needed by
the menu/screen dispatcher. This does not show that an ordinary camera's
live view has an empty stack, or that the separate live-view worker cannot
process input. Confidence is high for measured counts and bounded getter
behavior, moderate for generalizing to this fixture. Other startup paths
were not tested.

### Reproduce privately

Use confirmed WORK and a fresh directory:

```sh
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex_screen_stack_private.py" \
  --output "$WORK/private-inputs/codex-screen-stack-review-04" --menu-control
```

Runs: `codex-screen-stack-run-02` and `-03`. Independent layout review:
`codex-guide-stack-review-09`. The helper checks original identity, pinned
simulator revision and clean checkout. Detailed memory, logs and frames stay
private; runtime imports disable bytecode writes.

Next: establish stock shooting-screen initialization and its prerequisites
before treating screen-dispatcher events as evidence of tracking activation.

Written by Codex in collaboration with Tony Kim; layout independently checked by a Codex subagent.

---

## 2026-10-15: Bit 13 does not identify a physical button

*(formerly `tracking-mask-namespaces.md`)*

Date: 2026-10-15. Read-only analysis of the verified C1.20 module.

Two fields in the copied input snapshot use bit 13. The code maps them to
different logical masks and menu events. Neither field is proven to be the
hardware SW0 word named in F-024. Matching the AE-L/AF-L mask to a test of
bit 13 is therefore insufficient to identify its button path.

| Source field in record | Normalizer | Destination field and mask | Candidate | Menu event |
| --- | --- | --- | --- | --- |
| `+0x164`, bit 13 | `0x102f0488` | `+0x18`, mask 2 | `0x1a` | `0x24f` |
| `+0x150`, bit 13 | `0x102f056e` | `+0x18`, mask 4 | `0x19` | `0x280` |

On their corresponding conditional paths, both normalizers clear the source
bit after setting the destination bit. Routine `0x102f0d14` calls them on
the fixed snapshot at `0xc200a7a0`: `0x102f056e` at `0x102f0d54`, then
`0x102f0488` at `0x102f0d5a`. Earlier calls must return for these paths to
run. The table links select candidate rows at `0x1073be48` and `0x1073be40`,
then menu-map rows 31 and 30 at `0x1073b400`.

These code/data relationships are observed statically with high confidence.
They are candidate links, not demonstrated event delivery. Later decoder
checks can suppress an output. Physical source, press/release behavior,
live-view consumption and tracking activation remain unresolved.

### Reproduce

With the owner's confirmed private WORK path and a fresh output folder:

```sh
"$WORK/analysis-env/bin/python" \
  "$WORK/codex-sw0-normalization-verify-private.py" \
  --output "$WORK/private-inputs/codex-sw0-normalization-review-03"
```

This helper verifies the original module hash, selected instruction
properties and table relationships. It does not prove complete control flow.
Two independent bounded inspections checked the surrounding branches and
snapshot call sites. Session outputs include `codex-sw0-normalization-root-01`
and `codex-agent-normalize-review-01` and `-02`, all outside Git.

No simulator controls or firmware changes were used. A search for an
AE-L/AF-L reader based only on the matching bit number has failed to identify
the physical button. The next step is to trace the producers of `+0x150`
and `+0x164` and test whether either actually represents SW0.

Written by Codex in collaboration with Tony Kim; independently checked by Codex subagents.

---

## 2026-10-15: Menu and live-view events share a router

*(formerly `tracking-ui-event-router.md`)*

Reviewed 2026-10-15. Read-only code analysis; no simulator controls were run.

Stock code has a shared router that chooses an event handler based on a state
byte. The menu object and the object used by the simulator's live-view setup
have different handlers. In state 1, event type 3 leads to separate menu and
live-view routines. This gives us a concrete live-view path to study.

It does not show a successful button press or tracking activation. The event's
data format, required state and link to an OK-button press remain unknown.

### What the code shows

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

### The two objects and their handlers

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

### State requirements still matter

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

### Reproduce privately

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

### Single next step

Trace how the live-view worker builds its type-3 payload and what
`0x102f7448` expects to read from it. Include the conditions that select state 1.
Do this before proposing any simulator input call.

Written by Codex in collaboration with Tony Kim, with independent Codex subagent review.

---

## 2026-10-16: Screen registry and mode selector are distinct state

*(formerly `tracking-registry-mode-state.md`; extends the "2026-10-15: An
empty screen stack" section above)*

Date: 2026-10-16. Read-only static analysis and assisted simulator observation.

The empty menu/screen stack reported in F-029 does not imply the native
live-view mode object is uninitialized. In the instrumented startup run,
object `0xc1821d44` changed selector `+0x74` from 4 to 1, while the screen
stack remained empty. Stock refresh preserved that combination. The menu
control subsequently selected 1 for menu object `0xc182e688` and populated
two stack entries. These are observed values, not proof of working input.

The separate group registry at `0xc2006594` contained groups 2 and 3 before
the fixture; startup added group 5 at `0xc2017a8c`. Other group slots were
zero at the observed checkpoints. A separate registry-only run agreed.
Static caller `0x10324b60` registers group 5 through `0x104571e8`.

Getter `0x104571fe` accepts group values below 7 and computes registered
base plus 44 times the supplied descriptor ID. It does not guard the ID or
a null registered base on the reviewed path. Do not treat it as a safe
interface for guessed shooting-screen IDs. Registration alone does not put
a descriptor on the active screen stack.

Confidence is high for the bounded code and recorded state, moderate for
generalizing beyond this startup fixture. No shooting-screen key table,
physical event delivery or tracking activation is verified. The separate
type-3 live-view worker remains a relevant path; an empty menu stack alone
does not rule it out.

### Reproduce privately

Private repro, confirmed WORK and fresh directory:

```sh
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex_mode_object_20261016_private.py" \
  --output "$WORK/private-inputs/codex-mode-state-reproduce-01" --menu-control
```

Runs: `codex-mode-object-20261016-run-01` and registry-only
`codex-screen-registry-20261016-run-01`. Static selected code is retained in
`codex-screen-group-registration-05` and `codex-screen-group-callers-06`.
Original hash and clean pinned simulator were checked; logs and memory stay
private. The only calls were the established startup, refresh and menu control.

Next: establish the type-3 input contract using the observed selector state;
do not substitute menu key injection into the empty stack.

Written by Codex in collaboration with Tony Kim; extends the prior Codex screen-stack observation.
