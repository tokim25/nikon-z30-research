# Native XPan preview call-site map

Codex static decode of the verified Z 30 C 1.20 EG, 2026-10-17. This map
identifies candidate call paths only; it is not a patch manifest or acceptance
result. Firmware bytes and raw disassembly remain outside the repository.

## Direct calls to preview getters

A hash-pinned halfword sweep decoded Thumb-2 `BL` immediates across the full
image and found 16 direct call sites to the small, large, thumbnail and fixed
thumbnail getters. This is a direct-call inventory, not an inventory of
indirect calls or every producer. Nearby code shows materially different
contexts:

| Call site(s) | Getter | Context visible nearby | Status |
|---|---|---|---|
| `0x100a4f60`, `0x100a51a8` | small | Reads capture-size selector at record `+0x226`; stores returned dimensions into a newly built record | Call-chain and area guard still need tracing |
| `0x101434f8`, `0x10143540`, `0x1014363c`, `0x1014366c` | small / large | A large image-record builder reads capture selector at `+0x226`; it also reads area `+0x208` in adjacent branches | Candidate capture path; per-branch area-4 guard and output buffer contracts remain open |
| `0x101438d6` | large | Reads selector `+0x226`, then derives more dimensions from a nested record | Parent caller and area guard remain open |
| `0x10146732`, `0x10146768` | small / large | Reads selector from a nested record at `+0x4e8` and stores returned dimensions in an output object | Nested record ABI and area source remain open |
| `0x1018ae6a` | large | Uses the getter after another preview-size lookup, then scales dimensions | Playback/capture ownership remains open |
| `0x10221b56`, `0x10221b5e`, `0x10221b64` | small / large / fixed | Generic size dispatcher selects among the getter families | Do not change globally; playback callers may share it |
| `0x10340ada`, `0x10340ae0` | thumbnail / small | Selects a getter by an enum-like branch and stores dimensions in a display object | UI/capture ownership remains open |
| `0x1038face` | small | Caller at `0x1038fa8c` obtains a current record through object `+0x3a4`; it reads selector `+0x226`, separately forms the area record at `+0x208`, then scales dimensions | Generic dimension-scaling callback, not established as capture-only; not an approved hook |

Changing every area slot would affect unrelated consumers, and generic
playback/editor routes share these getters. The current candidate changes
only area slot 4 under the owner's still-photo-guard waiver; playback/editor
consumers that select area 4 may still be affected. The earlier suggested
640×236 and 1920×708 dimensions apply to the upstream area-2 experiment, not
to this area's replacement of the 1:1 slot. The verified table values for
area slot 4 are 480×480 (small preview), 1080×1080 (large preview), 120×120
(thumbnail), and 374×374 (the separate reduced-preview list). F-169 records
the correction. Fitting the 5200×1920 XPan still into the first two stock
allocations, using the upstream nearest-four-pixel rule, gives candidate
dimensions 480×176 and 1080×400. These are proposed output dimensions, not
yet a validated native buffer contract.

## Builder path and next verification

At `0x1038face`, the caller passes the `+0x226` index into the small-preview
table. Its separate area record begins at `+0x208`; subsequent native code
reads fields from that record while calculating scaled output dimensions.
This function has callback-table references but no direct `BL` callers in the
bounded sweep. It is a generic scaler; its capture-only status is unproved,
so it is not the preferred patch point.

The native record builder at `0x1014319e` has four preview getter call sites.
It reads both `+0x226` and `+0x208` in its broader body, but those values are
used on separate branches. A correct hook must prove the relevant branch has
the area-4 value live at the call; a nearby load alone is insufficient.

## Direct pixel-buffer constructors

The pinned upstream C 1.20 investigation identifies three independent native
constructors that read preview dimensions directly and bypass the getter
functions: `0x10142d86`, `0x1014376e`, and `0x101464c4`. The first consumes the
index at capture record `+0x226`; the third consumes the nested record at
`+0x4e8`. Their direct table bases are `0x1157223c` (small dimensions) and
`0x11572264` (large dimensions); row-stride tables at `0x11572250` and
`0x11572278` remain separate. The five upstream hook sites are
`0x10142de4`, `0x10142e46`, `0x101437a2`, `0x1014651c`, and `0x10146552`.
Cross-checks against the verified original confirm these are instruction
addresses in the named constructors and that the area-4 table slot contains
480×480 and 1080×1080, with strides 960 and 2160.

For the replacement slot, candidate preview dimensions are 480×176 and
1080×400, computed by fitting the exact 5200×1920 large still into the stock
width limits and choosing the nearest four-pixel-aligned height. The dimensions
remain below the stock allocations and the original row strides need no
change. Before these values enter the manifest, execute the full native
constructors with synthetic area-4 records and verify every output field,
stride, allocation extent and non-target slot against the original.

The upstream hook approach uses small immutable per-profile copies instead of
globally replacing shared dimensions. The current local candidate uses exact
area-slot data edits under the recorded owner waiver rather than runtime
capture hooks; it does not use the upstream area-2 constant or index-1 data.
Other area slots and the fixed thumbnail remain unchanged, while area-4
old-photo/playback behavior may change.

## Same-firmware capture-callsite cross-check (F-193)

The pinned upstream source `aspect_ui.py` (commit
`f6630588810f6ecb9363bc7881fccb47e4fdb87b`, Git blob
`ce8f3dbbecc113a5cb6880fa832892ee35ecf70b`) supplies an exact return-address
allowlist for the generic small/large preview getters. Its seven small and
five large entries match a subset of the direct callers listed above: the
capture-record builders and `0x1038face` scaler. It excludes `0x10340ae0`
(display-object path) and `0x1018ae6f` (scaling path). The upstream verifier
(`tools/verify_aspect_profiles.py`, Git blob
`f0efbc7cbb3c31a57654a478debcf7b4233fde75`) executes the allowed callsites
and one excluded caller across profile values 0–7, areas 0/2/4 and indices
0–4; it checks original pointers/values on declines and preserves
callee-saved registers. This is actionable same-firmware evidence for using
the same return-address whitelist on our area-4 getter hooks, after checking
the area-4 index and ABI against the local data plan.

The upstream direct-buffer hook takes a different approach: it redirects the
dimension-table pointer when its profile is active and user area is 2, without
checking the outer caller return address. The local F-171 map shows our
corresponding constructor is shared by preview creation and existing-object
rebuild paths. Therefore that direct-hook guard is insufficient for our
required playback/rebuild preservation. The next useful static trace is the
provenance of those constructor calls—especially the path through
`0x1009f8c6`—or a per-record capture-origin field. Only then can the direct
buffer hooks be scoped safely. The upstream whitelist narrows the generic
getter work; it does not close the direct-buffer gate or approve a candidate.

## Recovering outer caller provenance (F-194)

The wrapper `0x10142f5e` begins with `push {r4,r5,r6,lr}` and calls the
shared `0x10142d86` constructor at `0x10142f7e`. It has three known callers:
`0x1009f8c6`, `0x100a356a`, and `0x100a579c`. At the first direct-table hook
inside `0x10142d86` (`0x10142de4`), the constructor has pushed six registers
(24 bytes) but has not otherwise changed SP; the wrapper's saved caller LR is
therefore at `[sp,#36]`. A site-specific stub can inspect that saved return
address before selecting an area-4 shadow table, without a shared global
one-shot flag. The three returns remain semantically unresolved: the first is
inside the dimension-based preview-object creator at `0x1009f884`, and the
other two rebuild existing objects. This establishes a possible caller guard
mechanism, not which caller is eligible or whether it covers every route.

Next trace the first creator's upstream indirect dispatch and input-record
provenance. If it cannot be proved to represent a newly captured still (or a
record already carrying the exact 65:24 geometry), leave the direct-buffer
hook unapproved. Validate the `[sp,#36]` contract in a complete synthetic
wrapper→constructor run before adding any corresponding edit to the private
manifest.

## Dimension-based creator review (F-195)

The verified original's `0x1009f884` body reads an input width at `+0x0a`,
maps width classes to a preview-size choice, writes that choice into the
record at `+0x226`, allocates a resource, calls the shared wrapper, then
attaches the returned object to the supplied parent at `+0x28`. Its local
control flow contains no still-capture predicate, area-4 check, or
capture-origin read. F-196 corrects the earlier negative-reference report:
the factory is called directly at `0x1021d952` and `0x1021d994` from helper
`0x1021d946`. That helper has one direct caller at `0x1021da84`, reached from
dispatcher `0x1021d9e2` when input flag bit 20 is set. The helper uses current
object/record state, constructs and attaches preview objects, clears a state
slot, then invokes an indirect continuation. This is a concrete event path,
but bit 20's meaning and the records' capture provenance remain unknown. The
factory itself remains unapproved; next trace the producer/meaning of bit 20
and preserve stock behavior unless the event is proven to denote new still
capture. F-184/F-195's prior statement that the factory had no direct caller
is superseded.

## Event-dispatch lead (F-196)

A full halfword-aligned Thumb-2 `BL` sweep of the exact hash-verified original
finds only one direct call to helper `0x1021d946`, at `0x1021da84`. The caller
is inside event-flag dispatcher `0x1021d9e2`; `LSLS r0,r5,#11` followed by
`BPL` makes the call conditional on bit 20 of `r5`. The helper at
`0x1021d946` uses a current object at global+`0x60`, invokes the dimension
factory for that record and a nested record, attaches a result at parent
`+0x28`, clears the current-object slot, and calls a continuation through a
function pointer. No direct `BL` to the dispatcher was found; one aligned
word at `0x1021dd08` contains the dispatcher Thumb pointer, so table-based
dispatch is plausible but its registration/use is not yet traced. This is a
productive next trace toward capture provenance, not a finding that the flag
represents capture. Identify the table use, producer and meaning of bit 20,
and inspect the event's record source before using this route as a hook. No
candidate or camera access.

## Callback registration trace (F-197)

Initializer `0x1021dac2` constructs callback descriptors from adjacent static
table values. It loads the `0x1021d9e3` Thumb callback pointer at
`0x1021db04` and passes the key/callback/context tuple to shared registration
routine `0x10199cae`; that routine builds a callback object and delegates to
common service code. The key itself is computed through an indexed lookup
helper, and the common service's event semantics are still unresolved. This
supports the interpretation that `0x1021d9e2` is a registered event handler,
but it does not establish what bit 20 means or whether the event corresponds
to a new still. Trace the identifier lookup and callback-argument producer
before using this path as a hook.

## Evidence and limits

Private reproduction helpers verify the original EG SHA-256 before decoding
or reading any tables. The address cross-check used
Apple Clang to wrap exact, private instruction slices as temporary Thumb ELF
objects for LLVM disassembly; it did not modify the firmware or simulator.
The getter sweep identifies direct Thumb-2 `BL` references only. It does not
find computed calls, prove the full capture lifecycle, or test generated
preview pixels. F-168's initial area-4 dimensions were corrected by F-169.
See F-168/F-169 and
[the all-size/preview contract](native-xpan-all-sizes-preview-contract.md).

## Synthetic constructor execution (F-170)

The three direct-buffer constructors were called from the pinned simulator
using synthetic records. For `0x1014376e`, the area-4 large output fields
followed a guest-only change from 1080×1080 to 1080×400; its calculated
size-related fields changed with the reduced height. For `0x10142d86`,
synthetic area-4 calls with stock and proposed small/large pairs returned;
the output records reflected 480×176 and 1080×400, with the fixed 160×120
thumbnail unchanged. `0x101464c4` likewise returned with the synthetic
pairs and unchanged thumbnail fields. Stack scratch and guest table entries
were restored after each call, and original/QEMU identities matched before
and after.

A deliberate area-0 control while the direct tables held the proposed values
also changed non-target output. This rules out a shared-table edit. A private
area-4 shadow copy selected only on a proven capture path remains the viable
shape. These calls validate that the constructors consume the proposed
dimension values and calculate their records; they do not prove backing
allocation capacity, hook-site register/stack contracts, exact capture-only
guards, generated preview pixels, or lifecycle behavior. The raw reports
remain private and no firmware candidate was created.

## Shared caller warning (F-171)

The `0x10142d86` constructor is reached through wrapper `0x10142f5e`.
A verified-original direct Thumb `BL` sweep finds callers at
`0x1009f8c6`, `0x100a356a`, and `0x100a579c`. The first is inside a creator
that selects a preview slot using an input dimension. The other two are
object-rebuild paths that pass a current record obtained at `+0x3a4`. Their
capture-only role is not established, and indirect callers are outside the
sweep. This demonstrates that an area-4 check alone cannot be treated as a
capture guard. Any candidate must identify exact capture callers and leave
the other routes on stock dimensions; if that cannot be proven, this
constructor is not a safe patch point.

## Enclosing object-construction routes (F-173)

A second verified-original Thumb `BL` sweep followed the direct constructor
wrappers upward. Wrapper `0x10143862` has one direct caller at `0x1021e7a8`;
its inputs come from the current record/object chain. Wrapper `0x1014389c` is
called at `0x100a0b9c` while another object is built from an existing record.
The wrapper `0x101465e8` for direct constructor `0x101464c4` is called at
`0x1009ece0` from a function that checks an object type byte (`+0x0d == 0x24`)
and a field at `+0x144` before creating an output object. These facts narrow
the routes but do not establish new-still capture: object type, current-record,
and allocator context do not exclude display, playback, or rebuild paths.

The other constructor routes remain shared: `0x1014376e` is called by
wrapper `0x10143862`, and `0x10142d86` is reached from the three F-171 wrapper
callers. No capture-only producer has been established. Next, trace the source
and lifecycle of the type-`0x24` object and the factory inputs at
`0x1021e7a8` to a concrete still-capture event; do not add hooks based only on
these object-construction checks.

F-177 narrows the `0x1021e7a8` route. It is inside the routine beginning at
`0x1021e3f4`, which attaches/reuses a nested record-linked object, creates a
preview object when its current field is empty, stores that object into its
parent and continues state handling. This remains an existing-object
lifecycle path; it does not identify a new-capture guard. A whole-image
direct-branch check found no direct call to the routine entry, so any caller
trace must account for computed/indirect dispatch.

F-179 adds bounded whole-module scans for Thumb PC-relative literal/ADR and
MOVW/MOVT address formation, plus ARM PC-relative literal/ADR forms, against
the object-constructor table regions. None directly references the inspected
table addresses. The constructor pointer remains present in a data entry, so
base-relative use or runtime registration remains possible and unresolved.

## Candidate branch layout (F-174)

Instruction-width inspection identifies candidate four-byte patch
windows immediately around the five direct-buffer hook areas:
`0x10142de4`, `0x10142e42`, `0x101437a0`, `0x10146518`, and `0x10146550`.
Each window contains either one 32-bit Thumb instruction or two complete
16-bit instructions; the exact displaced effects must be reproduced and
reviewed before use. A Thumb-2 `BL` from each window to `0x1002d996` has a
displacement of about 1.1 MiB, inside its ±16 MiB reach. The appended code at
the native EG tail is about 31.9 MiB from these sites, so it cannot be called
directly by `BL`.

A synthetic LLVM assembly check confirms that an eight-byte Thumb veneer can
use `LDR.W PC` plus a Thumb-tagged absolute pointer without consuming a general
register. Five such veneers would need 40 bytes of the candidate zero subspan.
The first 40 bytes also have no hit in a bounded whole-image Thumb/ARM
PC-relative literal/ADR scan.
This proves an encoding/layout option only: the subspan is not cleared as
executable space, the pointer uses have not been exhaustively closed, and no
hook semantics or capture-only guards are established. No firmware bytes
were changed.

## Image-record builder route (F-180)

The native builder at `0x1014319e` reads the current area record and preview
selector and populates several preview-related fields. Its only direct
`BL` caller is `0x10143708`, inside constructor `0x101436c2`. That constructor
is reached from `0x100a42d8` when an object's record slot `+0x320` is empty,
and from `0x101eccb0` during an existing-object refresh path. The latter
checks object state and fills a missing record; neither caller establishes
that the object was just produced by a still capture. This makes the builder
useful as a record-layout reference, but not a safe hook point yet.

The adjacent helper `0x100a4f0a` is also not a capture boundary: its only
direct callers check and then release/clear a record-linked resource, with
one caller additionally gating on a context byte equal to 4. That value is
not evidence of a new-still event. Do not patch either lifecycle route based
only on area or selector fields. This was the pre-waiver hook decision and is
superseded for the current offline candidate by F-198 below.

## Area-4 table-only candidate decision (F-198)

The owner's still-photo-guard waiver accepts possible movie, playback and
warning side effects for the offline prototype. The candidate therefore does
not use the unresolved `0x1021d946` callback or any constructor hook. It
changes only area slot 4 in the small/large getter tables and direct-buffer
dimension tables, with all other slots, row strides and the fixed thumbnail
left unchanged. This does not claim that the callback is capture-only or that
area-4 playback behavior is clean; the residual risk is within the recorded
scope. The exact private 176-span manifest and candidate passed independent
byte/layout/CRC checks (F-198). Natural lifecycle condition 1 remains unmet,
and the candidate is not authorized for camera use.
