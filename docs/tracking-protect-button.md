# Protect identifies a separate playback assignment and a shooting-side candidate

Date: 2026-10-16. Owner-directed follow-up to the Protect/key icon on the
AE-L/AF-L button. This opening section records the initial read-only static
pass on verified C1.20, without execution or modification. The dated
continuations below include two later diagnostic QEMU runs. No camera
access or firmware modification occurred in any pass.

The Protect name was useful: indexed UI labels link a named AE-L/AF-L
button descriptor to playback setting `0x1186`, and value 24 selects its
Protect action. A separate shooting descriptor uses `0x1184`. This is
substantially stronger evidence than the retired BLE control cluster,
but physical delivery and native tracking activation remain unverified.

## Two input identities, not one interchangeable event

The named switch table includes both AE-L/AF-L and Protect. The existing
normalization and logical-to-UI tables give these distinct static paths:

| Named switch | Mask | Logical input | UI event |
| --- | --- | --- | --- |
| SW0 AE-L/AF-L, named row `0x1072e540` | `0x2000` | `0x0d` | `0x28b` |
| SW1 Protect, named row `0x1072e900` | `0x20` | `0x16` | `0x282` |

SW0's mask/input pair is at `0x1073bdb8`; SW1's at `0x1073be28`.
The latter is in the 19-row table at `0x1073be20`, actually walked by
`0x102f0e38` using snapshot field `+0x18`. Logical-to-UI translation
uses the established 179-row table at `0x1073b400`.

These labels and matching maps do not prove that the Z30 body electrically
posts both inputs, or that a mode transition renames one bit to the other.
Do not substitute `0x282` for `0x28b` merely because the physical button
has both roles. Some screen tables intentionally converge both events on
the same handler, while others differ.

## Playback Protect route through the named AE-L/AF-L button

English label index 1170 names the AE-L/AF-L button. The descriptor at
`0x1074df80` contains that label at `+4` and setting id `0x1186` at
`+0x0e`. The playback-assignment builder reads that setting at
`0x103d4e44`. Independently, the function-choice table at `0x1074cbd8`
contains 47 entries with a 12-byte stride. Row `0x1074cd58` pairs value
24 with label index 789, Protect. Other checked rows pair 23 with Rating,
25 with Zoom on/off, and 9 with AF-ON.

The table interpretation is checked against its real consumer:
`0x103d3328` loads the base and count 47; `0x103d32c2` searches with
stride 12, then `0x103d32ca..0x103d32d2` computes that same stride and
loads the selected label at `+4`. This is not an inference from adjacent
numbers alone. Labels resolve through F-064's checked English index.

A validated UI-event row at `0x1148c7ac` sends `0x28b` to handler
`0x10523c46`, guarded by `0x10523dd2`. The screen dispatcher
`0x103ce804` establishes the row format: 16-byte stride, handler `+4`,
guard `+8`, parameter `+0xc`.

The handler reads `0x1186`. Value 24 takes the branch at `0x10523c80`
to `0x10523c92`, then reaches Protect action `0x105224bc` after its
state checks. That action chooses among `0x1051cec0`, `0x1043cd24` and
`0x1051d030` based on active screen state. The first two read metadata
byte `+8` bit 0 and submit operation `0x0b` through `0x103665ba`; this
pass did not follow that asynchronous operation through storage or prove
a saved file's protection changed. The action's Protect identity comes
from the checked assignment label and dispatch branch.

Shared-handler examples also exist: rows `0x1137700c` and `0x1137703c`
send `0x282` and `0x28b` respectively to `0x104c5f30`; rows
`0x1149b3cc` and `0x1149b4dc` both send them to `0x1051dda6`.
Those shared handlers are not automatically protection toggles. This is
why searching the event alone was insufficient to identify the operation.

## Separate shooting-side candidate

The button descriptor at `0x1074c8c4` also has label index 1170, but uses
setting `0x1184`. The original live-view mode object `0xc1821d44` holds
Thumb-tagged callback `0x102f2eaf` at `+0x4c`; its verified initialized
ROM origin is `0x11fa3a24`.

In that callback, `0x102f2eae`, the branch at `0x102f2f96` tests bit 13
of the incoming snapshot's halfword `+4`. It reads `0x1184`, compares
the assignment to 9, and on that match reaches `0x102f2fc0`, which
sets selector `0x14` to 1 through `0x1044e68c`. The independently
indexed function table labels value 9 AF-ON. Thus the shooting code
explicitly couples the named button's bit and its shooting assignment.
It is not inferred solely from a matching mask in an unrelated bank.

The known type-3 live-view consumer `0x102f7448` reads selector `0x14`
at `0x102f7480`, records it in local state and clears it at
`0x102f748e`. Later processing reuses that local register, so this is
not yet a proof of an autofocus start contract or its final effect.
Press, hold, release, repeat and simultaneous-input semantics were not
established. No tracking action was identified or called.

**Build implication:** a future tracking-button hook should investigate
the shooting callback/assignment branch, preserving the separate playback
Protect dispatch. Neither the generic Protect action nor its file-operation
path is an appropriate tracking entry point on this evidence. These are
candidate landmarks, not approved patch sites.

## Reproduce and resume

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex-protect-button-route-private.py"
```

WORK is the private directory in handoff-codex.md. The helper checks original
SHA-256, named masks, both maps, indexed labels, descriptor fields, actual
table-consumer strides, UI dispatch edges, the shooting bit/assignment
branch and its mode-object callback pointer. It prints a semantic summary
only and writes no files. Exact firmware strings and instructions remain
outside Git.

The original next step above was completed by the continuation below.

## 2026-10-16: held input, explicit edges, and a native tracking assignment

The owner confirmed the shooting setting as the intended control to
investigate. Static continuation establishes the input-field contract and
finds a native Subject tracking assignment, with two specific gaps between
that existing implementation and AE-L/AF-L. No firmware was modified or
executed for this continuation.

### The AF-ON branch does not provide a once-per-press contract

The transition builder `0x101dd502` accepts a current mask and a previous
mask. It stores both, their XOR, current-only bits and previous-only bits.
Its real caller `0x101e337e` supplies the current source at `0xc1f87bfc`
and previous source at `0xc1f87c38`, builds the snapshot at `0xc1f87a70`,
then copies current to previous at `0x101e3470..0x101e3478`.
The reset builder `0x101e347c` supplies the previous mask as both inputs,
retaining the held state while clearing the transition fields.

| Snapshot field, first switch group | Meaning |
| --- | --- |
| `+4` | Current mask |
| `+8` | Previous mask |
| `+0x0c` | Changed bits: current XOR previous |
| `+0x10` | Press edges: current AND changed |
| `+0x14` | Release edges: previous AND changed |

Thus the AE-L/AF-L bit-13 test at `0x102f2f96` reads a **level**. It
is inside the activity gate from `0x102f0d14`, which includes changed bits
from multiple input groups, dial-like fields and other state. An unchanged
held button alone does not satisfy that changed-bit term, but a change to
another button while AE-L/AF-L stays held can. The native AF-ON branch
therefore cannot be borrowed as a once-per-press tracking trigger.
Release clears the tested current bit and does not set the AF-ON flag
through this button branch. There is no independent debounce, repeat
timer or one-press latch in this branch; delivery timing remains untested.

The same level also checks `0x1187 == 9` after `0x1184` fails to match.
The explicit mode-selected assignment reader `0x10369468` reads `0x1184`
when `0xc2016a68 + 0x44` is 0 and `0x1187` when it is 1. Preserve that
context distinction instead of treating both as the same shooting setting.

For a prospective single-press hook, the available input predicate is
bit 13 of `+0x10`. This is a static contract, not a tested hook location.
Earlier AF-ON checks in the callback can branch around the AE-L/AF-L
test when another assigned control is held; placement must account for
that short circuit rather than merely replacing the local bit test.

### Selector `0x14` is an auxiliary flag, not the tracking command

Resolving the real getter/setter jump tables maps selector `0x14` to
the word at `0xc201685c + 0x68`, or `0xc20168c4`. It stores a boolean
pending indication, so several sets before a worker read coalesce.
The type-3 worker copies it to local `r6` and clears the word.

Only one subsequent branch uses that original value: when
`0x1045c3d4` returns zero, the path through `0x102f7814` can reach
`0x102f7834`. Further gates require `0x1045bf1c == 3`, setting
`0x188c == 0`, `0x104bd4e8 == 0`, and the intervening handler not
returning early. A nonzero flag or the separate `r7` condition takes
`0x102f7842`, dispatches the decoded logical input through `0x10310bf8`,
then calls `0x104c0206(1)`. If `0x1045c3d4` is nonzero, the value
from `0x1045bf1c` overwrites `r6`; later comparisons to 1 and 3 on that
path are not comparisons of the pending AF-ON flag.

`0x10310bf8` selects a context object from `0xc201a36c` and invokes
its `+0x14` callback through `0x10484e80`. Initialization
`0x10310758` populates that array from actual getters. In context 0,
getter `0x10301be8` supplies object `0xc18292b0`; its initialized
callback is `0x10302220`, which eventually dispatches the logical input
through `0x10301f36` after its own gates.

The additional `0x104c0206(1)` call updates module state through
`0x1045c3f4` and invokes `0x102bd87c`, which can notify a registered
callback with id `0x0504001a` through `0x102bdea0`. The apparent
operation-`0x21` call inside `0x102bd87c` goes to `0x1046296e`, which
is a return-only stub in this image. Do not describe it as a submitted
autofocus command. These mechanics explain why selector `0x14` alone
is neither a tracking request nor an unconditional focus-start interface.

### Native Subject tracking exists, but AE-L/AF-L omits its dispatch case

The same checked 47-row function table contains row `0x1074cc98`:
value **77** (`0x4d`), English label index **1561**, Subject tracking.
This is actual indexed UI text, independent of the retired BLE cluster.
The built-in help entry at index 250 describes a press-to-start,
press-again-to-end action during auto-area AF; that is intended behavior,
not an observation of the code executing.

Four actual setting consumers recognize 77 and call `0x10368b6e`:

| Handler | Mode-0 setting | Mode-1 setting | Tracking call |
| --- | --- | --- | --- |
| `0x1036938c` | `0x1141` | `0x1170` | `0x103693ca` |
| `0x103693ee` | `0x1144` | `0x1173` | `0x1036942c` |
| `0x1036951a` | `0x114e` | `0x1302` | `0x10369558` |
| `0x1036957c` | `0x1150` | `0x1304` | `0x103695ba` |

The helper accepts logical inputs `0x0b`, `0x28`, `0x2c`, `0x2d`,
plus distinct cases `0x1b` and `0x19`. Its state getter
`0x1044dc5a` derives values 0..5 from a copied status record: field
`+0x44` must equal 6 for states 0..4, and `+0x61`/`+0x62` determine
the remaining mapping. For the four configurable-button inputs, another
status predicate `0x1045a47e` must be false. State 0 or 1 calls
`0x1045a1ae` with a pointer to a zero byte; state 2 or 3 calls
`0x1045a21c`. Other states return without either request. The numerical
gates are established; their full AF-area/status semantics still need
to be tied to settings.

The request chains reach real state-changing implementations:

- `0x1045a1ae` -> `0x10230832` -> eligibility check `0x1019596e`,
  preparation `0x1022fbf4`, then `0x10162f10` -> `0x100774f4`.
  The last routine uses a lock at `0xc259eeec`; for internal state 0,
  2 or 3 it sets state byte `0xc259ff0c + 0x10` to 1 and updates
  associated request/status fields. State 1 makes no new transition;
  values at least 4 do not take the start branch.
- `0x1045a21c` -> `0x10230866` -> `0x10162f18` -> `0x100775c6`.
  With a separate gate byte at `0xc25a1eb4 + 0x0c` clear, states 1,
  4 or 6 can clear that state byte and the associated request fields.
  Other state/gate cases do not perform that clear.

These are statically identified native tracking request candidates, linked
to the labelled assignment and real state updates. Neither successful
acquisition nor a runtime start/stop cycle has been demonstrated. The
wrappers' calls to `0x1046296e` are again return-only.

Two concrete integration gaps prevent an assignment-only solution:

1. Logical input `0x0d` takes the real jump-table branch at
   `0x103020b4` to `0x10369468`. That handler recognizes the existing
   Zoom and center-focus choices (25 and 42), but has no value-77 case.
2. Passing `0x0d` straight to `0x10368b6e` also falls through without
   either tracking request. The helper has a deliberate accepted-input
   set; AE-L/AF-L is outside it. It can perform preliminary flag/timer
   work before rejecting, so it is not a side-effect-free eligibility test.

**Build decision:** retain the existing native tracking machinery, and
investigate a shooting-only adapter with explicit press-edge gating and
the proper assignment/context checks. Changing a menu label or merely
storing 77 into `0x1184` is insufficient on this path. Preserve playback
`0x1186` and Protect. No adapter or firmware patch was created.

Reproduce privately with `codex-tracking-native-contract-private.py` under
the confirmed WORK directory. It verifies the original hash through the
earlier helper, decoded field construction, real source/copy direction,
selector jump targets, native enum/branches and request implementations.
Synthetic arithmetic checks cover press, hold, release and a second-button
change while AE-L/AF-L stays held; they are not firmware execution tests.

The next step at this point was to resolve `0x1044dc5a`'s status fields `+0x44`,
`+0x61` and `+0x62` through the producer behind `0x104b9348`, alongside
`0x1045a47e`'s predicate. Establish the exact AF-area and active-tracking
preconditions before selecting the adapter's native request interface.
Do not restart BLE, hardware access or menu-reachability sweeps.

Validation: the private semantic verifier and synthetic transition checks
passed. The standard suite passed all 54 tests; artifact and byte-dump
checks and `git diff --check` passed. The new, untracked report was also
checked directly for encoded-data patterns and manually reviewed. No
commit, push or pull request was made.

## 2026-10-16: native status bridge and a bounded input-decoder probe

### Native request state reaches the helper's status record

`0x104b9348` calls `0x101925ce`, which locks and copies `0x468`
bytes from `0xc237c7b4`. The larger builder `0x101925ee` copies its
source configuration's `+0x40` to record `+0x44`. Its detailed result
builder `0x101914ae` produces fields `+0x2a8`/`+0x2a9` in a block
placed at record `+0xbc`; the outer builder then copies the resulting
`+0x364`/`+0x365` bytes to the public `+0x61`/`+0x62` fields.

There is also a direct bridge from the native tracking implementation:
`0x100762fc..0x10076314` reads `0xc259ff0c + 0x38` and `+0x39`,
then passes that two-byte pair to `0x101925b0`, which writes it to
`0xc237c7b4 + 0x61` and `+0x62` under the same module lock.
This links the previously identified request routines back to the state
getter; it is not inferred from neighboring addresses.

With area field `+0x44 == 6`, the getter's complete mapping is:

| `+0x61` | `+0x62` | Getter state | Configurable-button branch |
| --- | --- | --- | --- |
| 0 | 0 or 2 | 1 | Start request |
| 0 | 1 | 0 | Start request |
| 1 | 0 | 2 | Stop request |
| 1 | 1 or 2 | 3 | Stop request |
| 0 or 1 | Other | 4 | Neither request |
| Other | Any | 5 | Neither request |

An area other than 6 also returns 5. The separate exclusion predicate
must still be false. The successful start-state update writes native
pair `(1, 0)`, which becomes getter state 2 after the bridge runs; the
stop-state clear writes `(0, 0)`, which becomes state 1. This explains
the intended next-press reversal without calling either tuple acquisition
success. The shared helper ignores the request wrapper's return value
and returns a handled indication after taking either branch; its return
must not be treated as evidence of successful focus or tracking acquisition.

The exclusion predicate is mechanically resolved:
`0x1045a47e` -> `0x102240ac`, testing whether byte `0xc23a51ad`
is nonzero. Real writers include `0x10232bbc` (3) and
`0x10232c36`/`0x10232c8e`/`0x10232cf6`/`0x10232d5a` (2).
Its full human-facing operation identity remains unproved. Preserve the
native predicate rather than replacing it with a guessed eligibility rule.

The Auto-area interpretation of base value 6 has independent menu support.
The checked eight-row table at `0x1074a688` contains labels 679, 1563
and 1564 with encoded values 600, 601 and 602: Auto-area AF, people and
animals variants. Consumer `0x10430c8c` uses an actual 12-byte stride,
reads the label at `+4` and encoded value at `+8`, and puts that value
into the selection arrays. Its selection path calls `0x1042b2d8`,
which divides by 100 into base setting `0x0c2b` and stores the remainder
separately for base 6. The photo counterpart `0x1042b30e` uses base
setting `0x056d`. The status consistency check `0x1032b756` separately
compares status `+0x44` with effective setting `0x1869`. This corroborates
the area-family interpretation; the full producer from stored photo/movie
settings into that effective setting was not re-derived here.

### Original decoder executed with synthetic transitions

One disposable run called stock decoder `0x102f0e38` 32 times from
the existing audited service checkpoint, using synthetic snapshots only.
It covered decoder mode arguments 0 and 1, masks `0x2000` and `0x4000`,
and eight transitions for each: released, press, unchanged hold, another
button press while held, that other button's release, release, second press
and second release. The other button was switch-group-1 mask 1.

Both mode arguments produced these three-word outputs:

| Transition | AE-L/AF-L mask | Comparison mask |
| --- | --- | --- |
| Released | `(0, 0, 0)` | `(0, 0, 0)` |
| Press | `(0x0d, 0, 0)` | `(0x0b, 0, 0)` |
| Unchanged hold | `(0x0d, 0, 0)` | `(0x0b, 0, 0)` |
| Other press while held | `(0x1b, 0, 1)` | `(0x1b, 0, 1)` |
| Other release while held | `(0, 0, 0)` | `(0, 0, 0)` |
| Release | `(0, 0, 0)` | `(0, 0, 0)` |
| Press again | `(0x0d, 0, 0)` | `(0x0b, 0, 0)` |
| Release again | `(0, 0, 0)` | `(0, 0, 0)` |

The return register is not an interchangeable logical event code: in mode
1 a release returned `0x20` for AE-L/AF-L and `0x40` for the comparison
mask while all three output words were zero. Consumers must use their
actual documented output contract. The comparison inputs agree with the
static normalization table; this test does not identify real switch delivery.

All 32 calls returned, restored the diverted thread context and restored
the synthetic scratch region. Breakpoints at `0x10368b6e`,
`0x10230832` and `0x10230866` saw zero calls. Stock assignment reads
were 4 for both `0x1184`/`0x1187`, and 34 for both `0x1141`/`0x1170`.
No assignment, status byte or native tracking state was forced. The
original firmware hash remained unchanged and the pinned QEMU checkout
remained clean. This is an assisted decoder test, not a physical-button,
natural worker-delivery or tracking-activation demonstration.

**Build implication:** adding a value-77 case and forwarding logical input
`0x0d` is insufficient to guarantee once-per-press behavior. The decoder
can return the held logical id when explicitly called on a held snapshot.
The upstream activity/queue gates affect natural delivery and were not
bypassed in a claimed hardware result. A proposed adapter must retain the
original snapshot's press edge and respect chord arbitration, run in the
existing shooting worker context, preserve the native state/exclusion
checks, and keep playback Protect separate. Calling the shared tracking
helper directly from the input callback is not an established interface.

Reproduce with `codex-tracking-input-semantics-private.py --output
private-inputs/codex-tracking-input-semantics-NN`, a new output directory
under confirmed WORK. Run 01's private `summary.json` is the evidence;
its raw session audit and graphics remain outside Git. The extended
`codex-tracking-native-contract-private.py` checks the static status bridge
and real AF-area table consumers as well as the earlier route.

The next step at this point was to establish where the same queued snapshot's `+0x10`
press edge remains available immediately around the type-3 call to
`0x102f1d5a` / its decoder call `0x102f1dbc`. Identify a place to gate
the proposed AE-L/AF-L value-77 action in the existing worker context,
without reusing a newer global snapshot or invoking it in the input task.
This is a hook-contract question, not another simulator reachability sweep.

## 2026-10-16: same-record worker edge is available across the decoder

The next question above is resolved mechanically, with static decode and
one bounded diagnostic FIFO run. In `0x102f1d5a`, the mode-0 ring pop
through `0x102f1412` returns a snapshot pointer. The caller saves it in
callee-saved `r5` at `0x102f1da8`. A non-null, non-touch record reaches
the decoder call at `0x102f1dbc` with this contract:

| Location | Available data |
| --- | --- |
| Before `0x102f1dbc` | `r0 == r5`: the popped snapshot; `r1 == sb`: caller option; `r2 == 1`; `r3 == r4`: three-word output destination |
| After return, `0x102f1dc0` | `r5`: same popped snapshot; `r4`: same output destination; record `+0x10` still contains the original press-edge mask |

The type-3 handler calls this function at `0x102f7518` and reads its
three output words at `0x102f751c..0x102f7524`. A full-image Thumb
direct-call scan found that one direct caller of `0x102f1d5a`; this is
not a claim about every possible indirect or ARM-mode reference.
The ring-pop mutex is released at `0x102f14b6` before returning the
pointer. Capture the relevant edge immediately; do not retain a ring
slot pointer across later blocking calls or assume it cannot wrap/reuse.

The disposable run queued all three synthetic records through the stock
writer `0x102f1844` before consuming any through `0x102f1d5a`:

| FIFO record | Slot address | Press edge | Release edge | Decoded output |
| --- | --- | --- | --- | --- |
| Press | `0xc2008ea0` | `0x2000` | 0 | `(0x0d, 0, 0)` |
| Hold | `0xc2009030` | 0 | 0 | `(0x0d, 0, 0)` |
| Release | `0xc20091c0` | 0 | `0x2000` | `(0, 0, 0)` |

Breakpoints immediately before and after the decoder verified the same
record pointer and edge fields for each pair of stops. These were three
distinct FIFO slots, not repeated reads of the newest global snapshot.
All six diagnostic calls returned and restored thread context and scratch
memory. Tracking-helper/request breakpoints saw zero calls. Original
firmware hash and pinned QEMU checkout checks passed afterward.

This confirms the record/ABI contract of code called by the real worker;
the probe invoked those stock routines from the audited service checkpoint.
It did not demonstrate natural type-3 scheduling, install an adapter,
exercise native tracking or establish that a replacement hook is correct.

**Candidate integration boundary:** the normal-record path around
`0x102f1dbc`/`0x102f1dc0` has both the matching press edge and decoded
arbitration result. It can support a future per-press gate without reading
`0xc200a7a0`, which can represent a different input generation. Any design
must leave the original context-specific dispatch checks in place; directly
calling tracking before those checks would bypass stock gating. Merely
zeroing a held decoded id can also introduce normal release/no-input
behavior elsewhere, so that is an untested design option, not a fix.

Native action-side changes remain necessary: AE-L/AF-L's
`0x10369468` has no 77 case, and the shared tracking helper's accepted
input set excludes `0x0d`. The full-image Thumb direct-call scan found
two calls to that AE-L/AF-L handler, at `0x103020b4` and `0x10302108`;
the second is a combined-input path. Account for both when designing the
gate. The existing configurable-button tracking branches also perform
completion cleanup through `0x1036925e` / `0x10368402`; do not assume
that forwarding only the start/stop helper reproduces the full handler.

Private helper: `codex-tracking-queued-edge-private.py`. Evidence:
`private-inputs/codex-tracking-queued-edge-01/summary.json` under WORK.
Rerun only with a new output directory. Raw audits remain private.

**Single next step for handoff:** trace the AE-L/AF-L assignment menu's
actual option rows, selected-value mapping and setter callbacks around
`0x103d4222` and `0x103d9898`. Document the minimum coordinated changes
to expose value 77 and route its action, including the verified same-record
edge gate and native completion cleanup. Preserve mode-1 `0x1187` and
playback `0x1186` as separate decisions. Do not repeat the completed FIFO,
decoder or BLE reachability probes. No executable adapter is ready yet.

## 2026-10-16: the menu-side gap confirmed, with a working template

Picked up the single next step above (Claude, continuing on this branch
per the handoff). Read-only static decode only; no simulator run, no
firmware modification.

### `0x103d4222` is the display-side mapper, not an option list

This function reads the current value of setting `0x1184` (via
`0x10465984`, a property getter), then selects a label/preview context
for the currently-selected function. Values 0-8 are handled by a Thumb
`tbb [pc, r4]` jump table at `0x103d424a` (9 one-byte entries, confirmed
by direct read: targets `0x103d42f0, 0x103d4266, 0x103d4266, 0x103d4266,
0x103d42de, 0x103d42d8, 0x103d42d2, 0x103d42cc, 0x103d4260`). Values 9,
`0x19` (25), `0x2a` (42) and `0x4e` (78) are each one additional
`cmp r4,#N; beq <label>` in a linear chain immediately after the `tbb`
bound check (`cmp r4,#8`). **This function has no case for `0x4d` (77,
Subject tracking)** -- confirmed by reading every comparison in the
chain; an unrecognized value falls through to the default path at
`0x103d4266`. Adding a case does not require `tbb` table expansion (the
table only covers 0-8); it needs one more `cmp`/`beq` in the existing
linear chain, the same shape as the four cases already there.

### `0x103d9898`'s stub cluster: zero stubs for 77 under 0x1184/0x1187, four working templates elsewhere

This address opens a long run of tiny setter trampolines, each shaped
`movs/movw r1, #<value>; movw r0, #<setting>; b.w 0x10465990` (a generic
property-setter call) or occasionally a two-step variant that also
writes a sub-setting (`0x1185`) immediately after. A full scan of the
containing module (`0x103d8000`-`0x103dc000`) for every site loading
setting `0x1184` or `0x1187` found **26 setter stubs, covering values
`0, 4, 5, 6, 7, 8, 9, 0x19, 0x2a, 0x2c, 0x4e` -- none of them `0x4d`
(77)**. This independently confirms, at the menu-assignment level, what
the prior section already found at the handler level: AE-L/AF-L's
assignment menu has no wired path to select Subject tracking at all,
for either mode-0 (`0x1184`) or mode-1 (`0x1187`).

The same scan, widened to `r1 == 0x4d` regardless of setting, found
**the four buttons that already support tracking each have exactly this
shape of stub**, matching this file's existing table of tracking-capable
handlers exactly:

| Stub address | Setting | Matches handler |
| --- | --- | --- |
| `0x103d9b62` | `0x114e` | `0x1036951a`'s mode-0 setting |
| `0x103d9c52` | `0x1150` | `0x1036957c`'s mode-0 setting |
| `0x103da810` | `0x1302` | `0x1036951a`'s mode-1 setting |
| `0x103da892` | `0x1304` | `0x1036957c`'s mode-1 setting |

Each is the exact pattern `movs r1, #0x4d; movw r0, #<setting>;
b.w #0x10465990`. (Two other `r1 == 0x4d` sites, `0x103d8f4e` and
`0x103db924`/`0x103dbbb8`, use a different calling shape -- `mov r4, r0;
mov r0, r5; bl 0x10465990` -- for settings not yet identified in this
pass; not decoded further here.) These four are a working, in-image
template for exactly the stub this button is missing: the minimum menu-
side change is two new stubs of this same three-instruction shape, one
for `0x1184` and one for `0x1187`, each writing `0x4d`.

### What a coordinated change needs, combining this with the prior section

This does not change the prior section's build decision or its warnings
-- it narrows "trace the option rows" to a confirmed, minimal shape.
Three independent pieces, all previously identified, now need to move
together, and none alone is sufficient:

1. **Menu/assignment (this section):** one new setter stub per mode,
   matching the four-button template exactly, writing `0x4d` to `0x1184`
   and `0x1187`. One new `cmp`/`beq` case in `0x103d4222`'s display chain
   so the menu shows the right label/preview once 77 is selected (not
   decoded here: which label index or preview context the new case
   should target -- follow the shape of the `0x19`/`0x2a`/`0x4e` cases,
   not invented).
2. **Action dispatch (prior section):** `0x10369468` needs a `0x4d` case
   forwarding to `0x10368b6e`, covering both its callers (`0x103020b4`
   and the combined-input path `0x10302108`), and `0x10368b6e`'s own
   accepted-input set needs `0x0d` added alongside its existing
   `0x0b, 0x28, 0x2c, 0x2d, 0x1b, 0x19` cases.
3. **Press-edge gate (prior section):** the same-record boundary around
   `0x102f1dbc`/`0x102f1dc0` is the verified place to read the press
   edge without substituting a newer global snapshot; AE-L/AF-L's native
   AF-ON branch (bit 13 of `+0x10`) cannot be reused as a once-per-press
   trigger on its own (it tests a level, not an edge, per the prior
   section's finding).

No executable adapter was written in this pass either. This stays a
documented, coordinated change plan -- not a patch -- consistent with
the prior section's build decision and the project's offline/read-only
rules.

### Open after this pass

- Which label/preview target the new `0x103d4222` case should reach
  (the four-button templates' own display cases were not decoded for
  their exact label indices).
- The two `mov r4,r0; mov r0,r5; bl 0x10465990`-shaped `r1==0x4d` sites
  (`0x103d8f4e`, `0x103db924`, `0x103dbbb8`) and what settings they
  target -- possibly a third calling convention for the same stub
  family, not yet resolved.
- Everything the prior section already listed as open (AF-area/status
  semantics behind `0x1044dc5a`, `0x1045a47e`'s full operational
  identity, and runtime/hardware verification of all of the above).

Validation: all 54 standard unit tests, both artifact scripts, and
`git diff --check` passed before this edit. No commit was pushed to
`main`; per the owner's existing instruction on this branch, no merge is
authorized from this checkpoint either.

Written by Claude (Sonnet 5.5), continuing Codex's checkpoint on this
branch per the owner's handoff in `docs/tracking-claude-handoff.md`, in
collaboration with Tony Kim.

## 2026-10-16: both open questions from the prior pass resolved

Picked up both items the prior section left open, in parallel. Read-only
static decode only; no simulator run, no firmware modification.

### The three unresolved `r1==0x4d` sites are not a mystery -- they're the remaining two handlers' stubs

`0x103d8f4e`, `0x103db924` and `0x103dbbb8` (the different calling shape
flagged as open) are **read-modify-write "swap" stubs**: each reads the
setting's current value first (`bl 0x10465984`), saves it (`mov r4,r0`),
writes the new value (`r1 = 0x4d`), calls the setter, then returns the
*old* value in `r1` (`mov r1,r4`) before popping -- a confirm/undo shape,
not a different feature. Their settings:

| Stub | Setting | Matches |
| --- | --- | --- |
| `0x103d8f4e` | `0x1141` | `0x1036938c`'s mode-0 setting |
| `0x103db924` | `0x1170` | `0x1036938c`'s mode-1 setting |
| `0x103dbbb8` | `0x1173` | `0x103693ee`'s mode-1 setting |

Combined with the prior section's four-stub table, this accounts for the
menu-side wiring of **all four** tracking-capable handlers across both
modes (the remaining `0x1144` stub, `0x103693ee`'s mode-0 setting, was
not individually located but is expected to exist with the same shape
given the other seven do). No open calling-convention question remains;
both stub shapes (plain post, and read/write/return-old) are accounted
for and neither implies anything AE-L/AF-L-specific.

### The display-case label IDs are per-button, not shared -- AE-L/AF-L needs a genuinely new one

Located the other three handlers' own display dispatchers (same shape as
`0x103d4222`: read the setting via `0x10465984`, then a `cmp`/`beq` chain
per selectable value) and read each one's case for `0x4d`:

| Handler's display dispatcher | Setting | `0x4d` case's label/preview ID |
| --- | --- | --- |
| `0x103d47b2` | `0x114e` | `0x1ca5` |
| `0x103d4a92` | `0x1150` | `0x1ca6` |
| `0x103d680e` | `0x1302` | `0x1cd8` |

All three IDs differ. This rules out a single shared "Subject tracking"
preview constant reused across buttons -- each handler's dispatcher
carries its own distinct ID for the same selected value, allocated as
part of that handler's own numbering (note `0x1ca5`/`0x1ca6` are
sequential, consistent with per-handler allocation at table-build time,
not a semantic grouping). **This means AE-L/AF-L's new case in
`0x103d4222` cannot simply reuse one of these existing IDs -- it needs
its own new label/preview-context ID**, following the same allocation
pattern as the three found here, not an invented or borrowed value. What
exactly that ID should reference (which string/preview resource) was not
traced in this pass -- the IDs found (`0x1ca5`, `0x1ca6`, `0x1cd8`) are
themselves opaque constants whose consuming table was not decoded here.

### Updated coordinated-change picture

This replaces the prior section's open item 1 (menu/display case) with
a concrete answer: a new case is needed, but it requires **a newly
allocated label/preview ID**, not just a new `cmp`/`beq` referencing an
existing one. The two-piece-plus-gate picture from the prior section is
now:

1. **Menu/assignment:** two new setter stubs (one of the two known
   shapes, following any of the seven examples now located) for `0x1184`
   and `0x1187`, **plus** a new `cmp r4,#0x4d; beq <label>` case in
   `0x103d4222` pointing at a *newly allocated* label/preview ID (not
   reusable from the three found here) -- and whatever table or resource
   that ID indexes into has not yet been traced.
2. **Action dispatch** (unchanged from prior section): `0x10369468`
   needs a `0x4d` case; `0x10368b6e`'s accepted-input set needs `0x0d`.
3. **Press-edge gate** (unchanged from prior section): the
   `0x102f1dbc`/`0x102f1dc0` boundary.

Still no adapter or patch written. Not yet done: tracing what the
`0x1cXX`-range IDs actually index into (a string table, a preview-image
table, or something else), and whether allocating a new one in that same
range is as simple as it sounds or requires its own table-expansion
consideration (the same kind of "safe instruction/data space" question
Lane 1 had to resolve for its own hook).

Validation: all 54 standard unit tests, both artifact scripts, and
`git diff --check` passed before this edit. No commit was pushed to
`main`; no merge is authorized from this checkpoint.

Written by Claude (Sonnet 5.5), continuing on this branch, in
collaboration with Tony Kim.

## 2026-10-16: the label-ID table is bounded and (likely) per-context, not global

Traced where the `0x1cXX`/`0x1dXX` label-id values actually go, picking up
this pass's own open item. Read-only static decode only.

Both dispatcher tails (`0x1045f7c8` and `0x1045d54c`) pass the id through
to `0x1045c968(object, id)`. That function is a **bounded linear search**:
it reads a row count from `[[object+0x28]+0x14]` (a 16-bit field), walks
rows of a 28-byte stride starting from `[[object+0x28]+0xc]`, matches the
target id against a 16-bit field at each row's offset `+0x18`, and
**returns NULL if no row matches** -- the lookup fails gracefully (no
crash), it just silently produces no label/preview, rather than looking
anything up dynamically or falling back to a default.

Two things follow from this:

1. **The table is bounded by a count field, not open-ended.** A value
   that isn't already a row cannot resolve, so simply inventing a new
   `0x1cXX`-style constant and writing it into a new `cmp`/`beq` case
   (as the prior section assumed) would resolve to NULL and silently
   fail to show a label/preview -- it would not crash, but it would not
   work either. Either an existing row's id must be reused, or a new row
   must be added to this table (increasing its count field), which is a
   firmware *data* change, not just a code change, and needs its own
   safety consideration (same category of question as Lane 1's "safe
   place to add instructions," but for data/table space instead).
2. **The table pointer comes from the passed-in object**
   (`[object+0x28]`), not a fixed global address. This is consistent with
   each settings-screen or context having its *own* local table of valid
   preview rows, which would mean the three different ids found in the
   prior section (`0x1ca5`, `0x1ca6`, `0x1cd8`) are not interchangeable
   even if they described the same text -- they may belong to three
   separate per-context tables, not three entries in one shared table.
   **Not yet confirmed**: whether AE-L/AF-L's own settings-screen object
   points at the same table as any of the three already-found handlers
   (in which case reusing an existing id might actually work), or a
   distinct one (in which case a new row is unavoidable). This requires
   identifying AE-L/AF-L's own screen/context object and checking its
   `+0x28` table pointer against the other three handlers' -- not done
   in this pass.

### Updated coordinated-change picture

Item 1 from the prior section's three-piece plan now has a more precise,
and slightly more cautious, shape:

1. **Menu/assignment:** the two setter stubs are unchanged (confirmed
   templates exist). The display case is **not** simply "add a cmp/beq
   with a new constant" -- it is contingent on resolving whether AE-L/
   AF-L's context shares a table with an existing tracking-capable
   handler (reuse, no data change) or not (new row required, a data-
   table change needing its own review). This is now the single most
   important open question for the menu side.
2. **Action dispatch** (unchanged): `0x10369468` needs a `0x4d` case;
   `0x10368b6e`'s accepted-input set needs `0x0d`.
3. **Press-edge gate** (unchanged): the `0x102f1dbc`/`0x102f1dc0`
   boundary.

Not yet done: identifying AE-L/AF-L's own settings-screen object and its
`+0x28` table pointer, comparing it against the three handlers already
traced, and -- if a new row genuinely is required -- finding whether
zero-filled or otherwise safe space exists near that table for one more
28-byte row (the same category of check Lane 1's instruction-space
search did, applied to data instead of code).

Validation: all 54 standard unit tests, both artifact scripts, and
`git diff --check` passed before this edit. No commit was pushed to
`main`; no merge is authorized from this checkpoint.

Written by Claude (Sonnet 5.5), continuing on this branch, in
collaboration with Tony Kim.

## 2026-10-16: the action-dispatch piece now has an exact, confirmed template

Independently decoded `0x10369468` (AE-L/AF-L's own handler) and
`0x10368b6e` (the shared tracking helper) directly, rather than relying
on the prior handoff's summary. Both confirm exactly what was reported,
and one of the handler's own sibling functions supplies the precise
instruction template needed.

### `0x10369468` confirmed: genuinely no `0x4d` case

Full decode of `0x10369468`: it reads a mode byte, then checks `0x1184`
(mode 0) or `0x1187` (mode 1) against `0x19` (Zoom on/off) or `0x2a`
(center-focus), calling `0x103691fc` or `0x1036845a` on a match. No
comparison against `0x4d` exists anywhere in the function; an
unrecognized value falls through and returns unhandled. This matches the
prior handoff's claim exactly, now independently confirmed by direct
decode rather than taken on report.

### A working sibling handler supplies the exact template

Immediately following in the same module, `0x1036951a` (one of the four
tracking-capable handlers, settings `0x114e`/`0x1302`, matching this
file's own earlier table) contains, verbatim:

```
cmp r0, #0x4d
beq #0x10369556
...
0x10369556: mov r0, r5      ; r5 = the logical input id for this button
0x10369558: bl #0x10368b6e   ; the shared tracking helper
0x1036955c: b #0x1036956a    ; join the shared cleanup tail
0x1036956a: mov r0, r6
0x1036956c: bl #0x1036925e   ; completion-cleanup check
0x10369570: cbz r0, #0x10369578
0x10369572: movs r0, #0
0x10369574: bl #0x10368402   ; completion cleanup
0x10369578: mov r0, r4
0x1036957a: pop {r4, r5, r6, pc}
```

This is the exact minimal instruction shape `0x10369468` would need: one
`cmp r0,#0x4d; beq <label>` added to its existing chain, and a new label
that calls `0x10368b6e` with the button's own logical input id, then
joins the same two-call cleanup sequence (`0x1036925e` then
conditionally `0x10368402`) this working sibling already uses. Nothing
here was invented -- it is copied directly from working code already in
the image.

### `0x10368b6e` confirmed: exact accepted-input chain, no `0x0d` case

Full decode of `0x10368b6e`'s cmp chain: it explicitly checks input
values `0x28, 0xb, 0x19, 0x1b, 0x2c, 0x2d` (confirmed instruction-by-
instruction, matching the prior handoff's reported set exactly) and
falls through to `0x10368bee` (returns unhandled, `r5` stays 0) for
anything else, including `0x0d` -- AE-L/AF-L's own logical input id.
Adding support needs one more `cmp r7,#0xd; beq <branch>` in this same
chain, matching the shape of the `0x1b`/`0x19` cases already there (both
of which branch into the same state-dependent start/stop logic at
`0x10368bb0`/`0x10368bde`).

### Updated coordinated-change picture

Item 2 from the running plan is now fully specified with working
templates, not just named addresses:

1. **Menu/assignment** (unchanged from the prior two sections): two new
   setter stubs (templates confirmed), and a display case contingent on
   the still-open per-context table question (prior section).
2. **Action dispatch (this section, now template-complete):**
   - `0x10369468`: add `cmp r0,#0x4d; beq <new_label>`, where
     `<new_label>` mirrors `0x10369556`'s exact shape (call
     `0x10368b6e` with the logical input id, then the same two-call
     cleanup sequence).
   - `0x10368b6e`: add `cmp r7,#0xd; beq <branch>` to the existing
     chain, mirroring the `0x1b`/`0x19` cases' shape.
3. **Press-edge gate** (unchanged): the `0x102f1dbc`/`0x102f1dc0`
   boundary.

Still no adapter or patch written -- this documents exact templates for
a future patch, not a patch itself. The remaining open items are
unchanged from the prior two sections: the per-context label-id table
question (menu side) and runtime/hardware verification of all of the
above.

Validation: all 54 standard unit tests, both artifact scripts, and
`git diff --check` passed before this edit. No commit was pushed to
`main`; no merge is authorized from this checkpoint.

Written by Claude (Sonnet 5.5), continuing on this branch, in
collaboration with Tony Kim.

## 2026-10-16: the per-button widget-descriptor table found; the preview-table question still open

Attempted to resolve the prior pass's open question (does AE-L/AF-L
share a preview/label table with an existing tracking-capable handler,
or need its own new row) by finding what calls the display dispatchers.
This surfaced real architecture, but does not conclusively settle the
question. Read-only static decode only.

### A per-button widget-descriptor table exists, confirmed structurally

`0x103d47b2` (the `0x114e` handler's display function) is referenced as
a raw pointer word at `0x1075af3c`. Reading the surrounding memory finds
a table of 20-byte (5-word) rows, each: `[fn1, fn2, shared_fn, fn3,
fn4]`, where **word index 2 of every row is the identical constant
`0x1045fda1`** (confirmed across 5 consecutive rows) and the other four
words differ per row and resolve to addresses inside the known
`0x103d4xxx`-`0x103d4bxx` handler cluster. `0x103d47b3` (Thumb-tagged
`0x103d47b2`) sits at word index 0 of its row. `0x103d4a93` (Thumb-
tagged `0x103d4a92`, the `0x1150` handler's display function) sits at
word index 0 of the next-but-one row, confirming this is one row per
button-widget type, each carrying that widget's own distinct callback
set (display function among them), plus one callback (`0x1045fda1`)
shared identically across every row -- plausibly a common validator or
housekeeping routine, not decoded here. `0x103d4222` (AE-L/AF-L's own
display function) was not found as a raw pointer word anywhere in the
image (same register-computed-reference pattern seen elsewhere in this
file), so its own row in this table was not directly located, though
one almost certainly exists given the table's one-row-per-button shape.

### What this does and doesn't resolve

This confirms each button has a genuinely distinct row with its own
function pointers -- consistent with, but not proof of, each row also
having its own distinct preview/label table at runtime. The table found
here is a **code**-pointer table (which functions to call), not the
**data** table `0x1045c968` searches (which preview rows are valid) --
they are different tables at different addresses, and nothing here
establishes whether the latter is built once per widget *type* (shared
across all buttons using the same underlying control class) or once per
widget *instance* (separate per button, per the render context). That
remains the open question. Resolving it needs either a live simulator
object inspection (constructing the AE-L/AF-L assignment menu and
reading the actual `[object+0x28]` pointer at runtime, then comparing it
against the same read for one of the four working buttons) or finding
the constructor/initializer for this specific widget class and reading
where it sets that field -- neither attempted in this pass; the
constructor was not located by the methods tried so far (a 111-hit
syntactic scan for `str ..., [.., #0x28]` in the containing module was
too noisy, mostly stack-slot writes, to isolate it).

**Recommendation for whoever picks this up:** live simulator inspection
is likely the faster path here, not further static search -- this is
exactly the kind of question Lane 1 resolved by observing a running
value rather than continuing to search ROM text for it.

Validation: all 54 standard unit tests, both artifact scripts, and
`git diff --check` passed before this edit. No commit was pushed to
`main`; no merge is authorized from this checkpoint.

Written by Claude (Sonnet 5.5), continuing on this branch, in
collaboration with Tony Kim.

## 2026-10-16: an outer per-button RAM-instance table found; stopping the static search here

Followed the widget-descriptor table's own references one hop further.
This surfaces real structure but confirms the question needs a different
method, not more static tracing. Read-only static decode only.

### Finding: a regular, 44-byte-stride table of per-button RAM instances

The row-table base addresses found in the prior section
(`0x1075af14`, `0x1075af28`) are themselves referenced as raw pointer
words at `0x11fb84bc` and `0x11fb84e8`. Reading the surrounding memory
finds a clean, regular outer table, stride `0x2c` (44 bytes), structure
per entry: `[RAM object pointer, packed word, shared manager pointer
0xc1832d50 (identical across all three entries read), two zero words,
pointer into the row-table from the prior section]`. The RAM object
pointers increment by exactly `0x18` (24 bytes) between entries
(`0xc1872998`, `0xc18729b0`, `0xc18729c8`) -- each button widget type has
its own dedicated, statically-assigned RAM record, not a shared/reused
scratch object. The shared manager pointer (`0xc1832d50`) is common
across every entry checked, plausibly a parent screen/controller object.

The shared callback `0x1045fda1` found in the row table (prior section)
has **677** raw pointer-word references across the full image -- a
generic, firmware-wide default handler used by a huge number of unrelated
widgets, not evidence of anything specific to this button cluster. Worth
recording so it isn't mistaken for a tracking-specific link in a future
pass.

### Why this doesn't resolve the open question, and why the static search stops here

The per-button RAM records are only 24 bytes -- too small to contain a
full preview-table (each preview row alone is 28 bytes, per the prior
section's `0x1045c968` finding). This means the `[object+0x28]` field
the display-dispatch functions read cannot belong to one of these small
per-button records directly; it must belong to a larger object (plausibly
the shared manager/parent at `0xc1832d50`, or a per-screen object
constructed when the assignment menu opens), which this static trace
cannot distinguish from here without guessing.

**This confirms the prior section's own recommendation rather than adding
a new one:** the remaining question (is the preview table shared across
all button widgets, or built per-instance per screen) depends on a
runtime object layout and value that static ROM reading cannot settle by
further inference -- continuing to guess from table shapes risks
documenting a plausible-sounding but unverified architecture as fact.
**Static tracing on this specific question stops here.** Live simulator
inspection (construct the AE-L/AF-L assignment menu, read the actual
pointer at the display function's incoming object `+0x28`, compare it
against the same read for one of the four working buttons) is the next
real step, not more ROM reading.

### Everything else from this session's passes remains valid and unaffected

To be clear about scope: this open question affects only the menu-
display label/preview piece (item 1 of the coordinated-change plan).
The action-dispatch template (prior section, `0x10369468`/`0x10368b6e`)
and the press-edge gate (`0x102f1dbc`/`0x102f1dc0`, Codex's original
pass) are unaffected and remain the most concretely specified pieces of
the plan.

Validation: all 54 standard unit tests, both artifact scripts, and
`git diff --check` passed before this edit. No commit was pushed to
`main`; no merge is authorized from this checkpoint.

Written by Claude (Sonnet 5.5), continuing on this branch, in
collaboration with Tony Kim.
