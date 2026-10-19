# Codex handoff

## Current Lane 3 direction, 2026-10-19 (F-370)

Candidate 02 remains NO-GO. F-369 confirms the standard QEMU stills-view
fixture does not reach AF snapshot callback `0x1016139e` or install the
status-root pointer. Do not repeat it. F-370 confirms setter caller
`0x10430c6c` belongs to the explicit AF-area menu routine `0x10430baa`: it
reads `0x0c2b/0x0c3d`, maps the selected option, invokes setter `0x1042b2d8`,
and updates the menu. A setter hook catches explicit selection but not
Auto-area already selected on view entry. Continue static tracing for the
stills-view/AF-application path that receives the live context pointer and
updates its mode; require pointer provenance. Do not repeat the setter probe,
status-pair branch, or QEMU view fixture. No reticle, half-press, or camera
behavior is proved. Analysis stays offline and raw output remains private.
See F-368–F-370.

## Current Lane 3 direction, 2026-10-19 (F-369)

Candidate 02 remains NO-GO. F-368 retired the generic snapshot event queue as
a demonstrated arm hook. F-369's standard pinned-QEMU stills-view setup never
reached callback `0x1016139e`; the status-root pointer at `0xc237c7b4 + 0`
remained null. Do not repeat that simulator setup. A targeted full-image scan
also found no simple same-register immediate-6 store to `+0x40`; this does
not exclude loaded/copied or indirect values. Resume with static pointer
provenance for the live object and its writer, and trace the actual
Auto-area-application path only where it reaches that object. Do not use
offset-only matches or return to the retired status-pair/event callback
branches. No reticle, half-press, or camera behavior is proved. Analysis
stays offline; firmware bytes/raw output stay outside the repo. See F-369.

## Current Lane 3 direction, 2026-10-19 (F-368)

Candidate 02 remains NO-GO. F-367 retired the status-root pair accessors as
unrelated to the live-view mode object. F-368 followed the snapshot callback
table into queue setup helper `0x1021cce8` from routine `0x10161642`, then
through dispatcher `0x1021dee4`. A nearby keyed-registry registration is a
separate path. The dispatcher forwards event IDs and payloads; its ordinary
`0x041a0040` path is rejected by callback `0x1016139e`, which snapshots only
for accepted event `0x0002fe3d`. No direct `MOVW #0xfe3d` or `MOVT #2` was
found; computed sources remain possible. Retire this callback as a patch hook
unless a new accepted-event producer is identified. Continue with the live
AF object's context `+0` installation and `+0x40` writer, requiring pointer
provenance rather than offset-only matches. Do not repeat the setter-hook or
status-pair probes. No reticle, half-press, or camera behavior is proved.
Analysis stays offline; firmware bytes/raw output stay outside the repo. See
F-368 and `tracking-input-chain.md`.

## Current Lane 3 direction, 2026-10-19 (F-367)

Candidate 02 remains NO-GO. F-366's setter-hook QEMU prototype reached a
native state write but did not update the sampled live AF context. F-367
retires the nearby `0xc237c7b4 + 0x414/+0x415` pair accessors: they do not
identify the live-view mode object read by `0x101925ee`. A stock-QEMU InitTask
sample found status-root `+0` null before simulated stills-view entry. A
full-image `+0x428` displacement scan produced many unrelated structures and
did not find a unique installer for the pointer loaded by callback
`0x1016139e`. Continue on the actual firmware side: identify the owner and
initializer of the event context passed in `r1` to `0x1016139e`, then follow
its `+0x428` object and the object's `+0x40` mode writer. Do not repeat the
pair-accessor or setter-hook probe. Keep candidate 02 NO-GO; no reticle or
half-press behavior is proved. Analysis stays offline and firmware bytes/raw
output stay outside the repository. See F-367 and `tracking-input-chain.md`.

## Current Lane 3 direction, 2026-10-19 (F-366)

Candidate 02 remains NO-GO and is not ready for installation or testing. The
target remains stills-mode Auto-area AF with People/Animal detection, an
automatically visible tracking reticle, and acquisition on shutter half-press.
F-359 through F-364 retired the generic GUI notification, property-cache,
observer-table, configuration-reconciler, snapshot-consumer, and known
configurable-function callback leads as complete hooks.

F-366's throwaway guest-RAM QEMU prototype calls native helper `0x1045a1ae`
from the Auto-area setter for encodings 601/602 and reaches its state write of
value 6; encoding 600 skips the helper. The sampled live AF context remains
unchanged. This was a constructed setter call, not natural menu dispatch or
view-entry testing, so it proves only the local helper route. The setter is a
partial mode-change candidate, not the full implementation. Do not call
selector 45 unconditionally; it depends on mapped AF state. The next step is
to trace who installs the object at live-view context `+0` and updates its
`+0x40` mode, including the path when Auto-area is already selected on stills
view entry. Then test a valid context-triggered ready transition in the pinned
QEMU. Analysis stays offline; do not access the camera or card, and keep
firmware bytes/raw output outside the repository.

## Candidate status and hook direction, 2026-10-18 (F-334/F-335)

The standalone candidate was generated before the requested behavior had been
verified. That was premature: exact-span/CRC and hook-target checks do not
prove Auto-area People/Animal readiness, a visible reticle, or shutter
half-press acquisition. The camera displayed no Update action, and no update
began. The candidate remains NO-GO; do not describe or share it as ready to
install or test. F-333 provides only constructed QEMU evidence for native
state writes. F-335's xref sweep finds two direct callers of mode setter
`0x1042b2d8`, but no direct call/reference to guarded wrapper `0x1028f200`.
Review the setter ABI and whether its post-set state can safely establish
native ready state; keep the wrapper's trigger unresolved. Do not produce a
new installable image yet. See F-333/F-334/F-335.

F-336 adds a bounded QEMU check: after the synthetic callback moved source
state to 4/pair `(1,1)`, another call to ready helper `0x1045a1ae` left those
bytes unchanged. This is useful for evaluating duplicate ready callbacks,
but does not prove preservation of camera acquisition or reticle behavior.
Next review setter return/argument contracts and test the setter-first and
view-ready-first orders with a disposable simulator overlay only. Keep the
candidate NO-GO.

F-337's standard simulated shooting-view setup still leaves AF context mode
byte `+0x44` at zero after setter values 601/602, even though the public
properties read back correctly. This is a simulator snapshot-population gap,
not a real-camera conclusion. Do not repeat the setup. Trace the native AF
context producer for `+0x44` and the callback after that update; this settles
whether the setter is an immediate hook or only one side of a two-trigger
design.

F-338 directly sampled the callback's stack snapshot after setter 601/602,
ready helper and status bridge. It contained mode 0, pair `(1,0)`, and extra
guard 0, so the callback skipped the active-state transition for both modes.
This is a bounded simulator result, not a camera conclusion. The setter alone
does not complete the callback preconditions in QEMU. Next trace the AF-context
producer that supplies snapshot mode `+0x44`; do not repeat this sequence.

F-339 now identifies that snapshot field's direct source: builder `0x101925ee`
copies the live AF object's `+0x40` field into context `+0x44`, while setter
`0x1042b2d8` only writes public mode/submode properties. The public setter is
therefore not a proven immediate arm hook; a downstream AF-object update must
populate the source field first. Next trace the writer/update path for live AF
object `+0x40` and when the snapshot runs relative to it. Do not repeat the
property-setter QEMU test or create another installable image. Candidate 02
remains NO-GO and must not be presented as ready to install or test. See F-339.

F-340 narrows the setter timing: the generic property-write path calls runtime
observer dispatcher `0x10132f8c` synchronously before returning. A post-setter
hook could therefore run after a registered observer update, but the handlers
for properties `0x0c2b`/`0x0c3d` and their effect on AF-object `+0x40` are not
identified. Next trace those observer registrations/resolution and the live
field writer. Candidate 02 remains NO-GO; do not create an installable image.
See F-340.

F-341 observed both properties enter `0x10132f8c` in stock QEMU, but neither
reached an indirect listener or fallback resolver in the shooting-view
fixture. Property values read back correctly; the simulator has no observed
observer to update live AF-object `+0x40`. This is not evidence that the real
camera lacks the callback. Next inspect static observer registration and the
live-field writer; do not repeat this simulator sequence. Candidate 02 remains
NO-GO. See F-341.

F-342 finds neither direct setter caller writes the AF object's mode field or
calls a ready/action helper after the property write. One returns immediately;
the other performs menu-value mapping and selection adjustment only. This
confirms the setter is a property boundary, not a proven tracking hook. Next
trace the AF-object `+0x40` writer outside those callers and its timing before
snapshot builder `0x101925ee`. Candidate 02 remains NO-GO. See F-342.

F-343 retires another apparent property consumer: `0x10489832` reads
`0x0c2b`/`0x0c3d` and maps Auto-area People/Animal values to menu labels and
UI updates; it does not populate the live AF object's `+0x40` mode byte or
tracking snapshot. Generic `STRB [register,#0x40]` hits are not enough to
identify the writer because their base pointers differ. Continue with the AF
object's lifecycle/registration and the callback that consumes snapshot
`+0x44`; do not repeat the property-setter probe. Candidate 02 remains NO-GO.
See F-343.

F-344 follows the snapshot builder to its only direct caller: event handler
`0x1016139e` calls `0x101925ee` with live-view context `[r1+0x428]`, then
reads AF fields including `+0x40`. Its Thumb pointer appears in a static
callback table at `0x10161a44`; the reviewed handler path does not write the
mode byte. This is a snapshot consumer, not the missing producer or arm hook.
Next trace the live AF object's lifecycle/registration upstream and identify
the handler's dispatcher and event semantics. Candidate 02 remains NO-GO.
See F-344.

## Lane 3 scope correction, 2026-10-18

The owner has clarified that movie behavior is irrelevant because this camera
is never used for movies. The feature target is still-photo Auto-area AF:
People/Animal mode automatically enters the native Subject-tracking ready
state, shows its reticle, and shutter half-press begins acquisition. A
still/movie exclusion guard is not a requirement and must not consume more
research time. F-288/F-289's control-flow observations remain valid, but
their missing-guard conclusion is superseded as a feature blocker.

This scope correction does not prove candidate behavior or clear the other
test gates. Candidate 01 was copied to the card and the camera offered only
Done and Delete firmware update files; no update began. Review then found
candidate 01 was the diagnostic source that omitted the native AF status-copy
bridge. Candidate 02 now includes that bridge and passes exact-edit/CRC plus
hook-target checks, but its focused QEMU call timed out without observations.
It remains private, is not on the card, and has no updater-acceptance or
camera-behavior evidence. Do not treat it as ready for copying or installation;
do not rename an image or bypass updater eligibility.
Same-version rejection is a weak hypothesis: upstream Wonder Lantern reports
installing a standalone EG on a Z 30 C 1.20, but that precedent does not
validate either candidate. F-295/F-296
show the type-2 standalone parser does not branch on version-like metadata at
`0x24`, and preserves/accepts the candidate's unchanged compatibility field at
`0x10`; the post-CRC type-2 path also skips the version-formatting handlers.
No static same-version rejection is found. The unexplained failure is earlier
card discovery/UI eligibility or an untraced gate. F-298 through F-300 map
the scanner and callback: media-state-selected directory enumeration and
wildcard filename match precede the standalone parser; a successful parser
result takes a distinct callback path from the fallback message. The reported
no-Update screen is consistent with that fallback, but the actual camera
branch and failed filesystem/parser condition remain unobserved. The owner
confirms the card was camera-formatted (F-301) and now reports that the camera
is reading its root (F-304). This closes the selected-root question by owner
observation. F-303 confirms that the canonical `EG209020.BIN` name matches
the standalone row's wildcard pattern. Neither fact proves that this file
appears in the updater list, is opened or accepted by the parser, or causes an
Update option. The latest known menu offered only Done and Delete firmware
update files, and the owner has confirmed that remains the current result
(F-305). Do not ask for the same menu check again or attempt installation.
F-306 through F-309 correct F-299: scanner acceptance skips the fallback
message, but the callback passes a local menu-like record through helper
`0x102342a6`. It fills fields at `+4`, `+5` and `+0xf`; the callback then
dispatches record status values 1, 2, 4 and 8 into distinct outcomes (unknown
values take a report path). Next, trace the record/status producer and callback
result consumer to a menu action or label. F-309 locates this callback in a
five-entry property callback table but not its dispatcher; trace that registry
path once to see whether it reaches the menu result. If no concrete gate
emerges, record that runtime filesystem/parser observation is required and
stop. F-311 completes the local bridge ABI/relocation review: candidate 02
passes the two-byte pointer contract, preserves aligned SP and returns through
the native cleanup helper. F-312's interpretation of the action/state record
is corrected by F-313: `0x10230832` passes a zeroed pair, skipping the first
indirect callback in `0x10225012`. F-314 identifies `0xc18a7540` as a shared
mask word; setters and clearers update its bits, and `0x10066714` enters event
processing only when the word is zero. The camera-time mask and its
feature-level meaning remain unknown. F-315 follows one action-45
state-handler branch through `0x1045a1ae` into the mask-gated dispatcher;
neither that helper nor its observed callers mutates the mask, so the gate's
value is ambient and unresolved. This action chain is distinct from
candidate 02's status-copy bridge `0x101925b0`. F-317 resolves its two
firmware-side synchronization wrappers to ARM-mode SVC #6 stubs, each with an
8-byte local frame and no further firmware call; the SVC implementation's
stack is outside this bound. F-316's bounded body scan found 103 direct call
sites to 70 routines and no register-indirect call or table-branch instruction
inside the event body. F-319 corrects F-318: `0xc23a63b4` is the
synchronization object passed to the lock service, while bit-63 dispatch loads
the callback from `0xc18a748c`. F-321 found its initializer at `0x1006516c`;
F-322 corrects the target to Thumb entry `0x10064a9a`. Its fixed selector
enters case 3, which calls `0x10061aa6` and then broadcasts through
`0x100660f2`. F-323 traces that broadcast: it walks the runtime listener count
at `0xc18a74d5` and dispatches function pointers from `0xc18a7520`. F-324
followed the shared base references once; the broadcast reads the table, and
the bounded reference sweep did not expose a statically traceable subscriber
writer. This leaves callback stack depth unresolved. Candidate 02 stays
NO-GO. Stop listener-table tracing and pivot to a direct AF-ready/reticle hook
search for a build alternative. F-325's source review confirms candidate 02
already joins both transition orders: Auto-area People/Animal selected before
live view, or selected while live view is open. It uses a one-shot latch and
the native AF status-copy bridge, but the focused QEMU callback timed out, so
there is still no proof of reticle or half-press behavior. Do not invent a
second trigger or repeat the same QEMU run; the unresolved build decision is
whether the action-45 dispatch can be bounded or observed through a valid
native route. Do not revisit root, filename or parser checks. See F-292 through F-325 and
`hardware-readiness.md`.

**F-326 correction and next step:** stock pinned QEMU showed one stable
listener target, `0x1022adee`, across three post-startup samples. Static
selector-3 control flow emits event `0xB5` through the listener broadcast, so
this is now the concrete callback target for the action-45 event branch; the
previous statement that listener targets were unknown is superseded. Its
0xB5 arm has an 88-byte local frame and proceeds through state/value
translation and a native notification helper. The remaining build decision
is to bound this callback's transitive stack and the nested notification/SVC
tail, or identify an AF-ready/reticle hook that avoids this action path.
Candidate 02 remains NO-GO: no completed candidate runtime, visible reticle,
or half-press acquisition is established. Do not repeat the timed-out full
callback run. See F-326 and `hardware-readiness.md`.

**F-327 callback probe:** in disposable stock QEMU, the native selector
handler with selector event `0x04100004` and payload 1 emitted `0xB5`, entered
`0x1022adee`, and returned. Breakpoint sampling measured 176 bytes from
handler entry to the lowest observed SP. The nested callback at
`0x1022c4b8` was not reached because its enable mask was zero in ordinary
post-startup state. This is useful completion evidence for the constructed
event path, not a worst-case stack bound: it ran on InitTask, and the candidate
uses APPLV. No candidate action completion, reticle, or half-press result was
observed. F-328 corrects the earlier F-280/F-282/F-283 interpretation:
`0x101885e8` is a generic list pop, and the null at `0x1007450e` means that
the callback's work queue was empty, not that an AF object was missing. Drop
the proposed object-constructor/registration search. Next pursue the direct
AF-ready/reticle hook against the real firmware; trace the queue producer only
if identifying it could change the chosen hook. Keep candidate 02 NO-GO. See
F-327/F-328 and `hardware-readiness.md`.

**F-329 state check:** native Auto-area setter values 601 and 602 read back
correctly as base mode 6/submodes 1 and 2, but action 45's mapper still
returns reject state 5 in stock QEMU. Setting the separate boolean gate in
synthetic guest memory does not supply the missing AF context. The mapper
copies the AF context fields that bridge `0x101925b0` updates, so this run
does not test candidate activation. The only useful continuation is to trace
the real producer of that AF source pair or a direct ready-state hook; do not
repeat the same QEMU setup. Candidate 02 remains NO-GO, and reticle and
half-press behavior are unverified. See F-329.

**F-330 native transition lead:** static Thumb tracing found `0x1007756e`,
reached from dispatch entry `0x10162f14`, which passes a lock and writes state
4 and source pair `(1,1)` only when the current source state is exactly 1;
sibling `0x10162f18` to
`0x100775c6` follows state-dependent clearing paths. The existing `(1,0)`
writer `0x10078aa0` remains in the event-driven updater. These are concrete
state-transition routines, but their external command semantics and visible
reticle/half-press effects are not established. Next identify the dispatch
input/registration and half-press consumer; do not select or invoke a routine
by its writes alone. Candidate 02 remains NO-GO and is not installable. No
camera access. See F-330 and `tracking-input-chain.md`.

**F-331 action-45 toggle implication:** with Auto-area byte 6, source pair
`(1,1)` maps to state 3. Action 45 routes state 3 through
`0x1045a21c -> 0x10230866 -> 0x10162f18 -> 0x100775c6`; when the source state
is 4, that routine clears the state and pair. This is consistent with
replaying the native toggle canceling a state established by `0x1007756e`.
Do not use action 45 as the auto-arm operation. Next trace the native caller
that first reaches `0x1007756e` and its guards. Reticle and shutter half-press
behavior remain unverified, and Candidate 02 remains NO-GO. See F-331.

**F-332 mode-conditioned arming path:** wrapper `0x1028f200` branches to
`0x102bdbb4`, which checks an AF snapshot for base mode 6, source pair `(1,0)`,
and byte `+0x415 == 0`; the downstream transition additionally requires the
current source state to be exactly 1 before setting state 4 and pair `(1,1)`.
This appears to be a native AF callback conditioned on
Auto-area state, but its runtime trigger/registration and the extra byte's
meaning are unknown. Next trace that callback dispatch or a recoverable caller
to determine whether AF-area selection reaches it. It does not yet prove
reticle visibility or half-press acquisition. Candidate 02 remains NO-GO.
See F-332 and `tracking-input-chain.md`.

**F-333 QEMU state-cycle confirmation:** the native helper `0x1045a1ae` with
a synthetic zero-byte argument produced source state 1 and pair `(1,0)` via
`0x10230832 -> 0x1019596e -> 0x10162f10 -> 0x100774f4`. After bridge
`0x101925b0` copied the pair into AF context, the synthetic guarded callback
`0x1028f200` changed it to state 4 and pair `(1,1)` only for Auto-area mode 6,
context pair `(1,0)`, byte `+0x415 == 0`, and source state 1. Negative guard
cases and source state 0 did not arm. This is a native state result in stock
QEMU, not reticle rendering or proof that the wrapper is the physical
half-press callback. The next patch candidate should establish native state 1
on People/Animal Auto-area selection and preserve the guarded active
transition. Candidate 02 remains NO-GO. See F-333.

**Current host check, 2026-10-18 (F-297):** the approved descriptor-only USB
probe found zero matching Z 30 devices, and `gphoto2 --auto-detect` listed
none. This establishes only that the camera was not visible to this host; it
does not establish whether the camera is powered, cable-connected, or what
the card format is. No PTP command or write was attempted. Resume the menu
check after the camera is visible again and the card-format condition is
known. Do not treat this transport observation as a firmware result.

## Current continuation, 2026-10-17

### F-198/F-199 current state

The private offline XPan candidate and complete 176-span manifest are retained
in an owner-only directory outside this repository. The exact filesystem path
is intentionally kept out of Git. Retain both artifacts privately; do not
commit, attach, or share them. An independent read-back audit confirms exact
listed edits, no unplanned
changes beyond the regenerated two-byte CRC trailer, unchanged protected
header/metadata, native CRC, unchanged length/capacity, slot-4 dimensions,
unchanged other slots/strides and mode 0600. F-170 previously ran the same
preview dimensions through synthetic constructors, but this exact binary has
not been accepted by Nikon's updater or tested on hardware. The still-photo
guard waiver accepts unmeasured playback/movie/warning effects. Lifecycle
condition 1 remains unmet: hardware is NO-GO, and no camera contact/write is
authorized. F-199 re-opened the known original, candidate and manifest and
repeated manifest-driven exact-byte/CRC checks. It also compared all five rows
in both getter and direct-buffer dimension tables, confirming slots 0–3 are
unchanged, slot 4 contains the intended dimensions, and both five-entry stride
tables remain byte-identical with slot-4 values 960/2160. F-200 tested the
exact candidate against the existing pinned QEMU: both the Python launcher and
the machine's C firmware loader reject every image except the pinned stock
hash, before emulation. The QEMU checkout and binary were not changed. Do not
continue simulator work by weakening that guard or modifying the simulator;
this is one documented simulator limitation, not a build blocker. The
candidate remains a testable offline artifact, but native updater acceptance,
lifecycle condition 1, recovery/readiness checks and separate exact-step camera
authorization still gate any hardware test. In F-201 the owner reaffirmed the
existing still-photo guard waiver after the capture path was found not to be
proven new-still-specific; the accepted playback/movie/warning side effects
remain unmeasured.

### F-204 capture-path disposition

No new-still-exclusive hook is proven, and playback/editor output isolation is
not proven. Shared callers include dimension-based construction, existing-
object rebuild and refresh paths; area-4 slot-4 edits can be observed by any
consumer selecting that slot. The existing waiver covers possible
playback/movie/warning effects, but does not cover editor outputs. The owner
directs keeping the waiver as scoped; editor outputs are not added. Do not
continue capture-hook research, build a new candidate, or proceed to hardware
preflight. Lifecycle condition 1 remains unmet. See F-204 and the [caller
map](native-xpan-preview-callers.md).

### F-205 still-only gate review

The owner has now narrowed the requirement: any XPan preview changes must
apply only to still capture and must leave playback/editor outputs unchanged.
Review of the four named contexts found no proven gate: `0x1009f8c6` is called
from a dimension-based preview factory with no local capture predicate;
`0x100a356a` and `0x100a579c` rebuild existing objects; `0x101eccb0` refreshes
an existing object. The possible upstream bit-20 dispatcher condition has
unknown event semantics and record provenance, so it cannot be treated as a
still-only gate. Do not build a candidate or proceed to camera readiness on
this evidence. Remaining work requires tracing a capture-origin predicate
that excludes playback/editor and proves dominance at all relevant edit
points. See F-205 and the caller map. The existing waiver remains as scoped,
editor excluded; lifecycle condition 1 remains unmet.

### F-206 bounded stopping point

The repository-only trace adds no caller/producer evidence beyond F-171,
F-180 and F-196/F-197. The unresolved evidence is the producer and semantics
of bit 20 at dispatcher `0x1021d9e2`, the registered callback key/service
meaning, and the new-still versus reused-object provenance of the current and
nested records consumed by `0x1021d946`. The F-198 global area-4 table edit
cannot meet the owner's new playback/editor exclusion requirement. Do not
build or test it under this scope. The safe next step is for the owner to
provide or point to an already-authorized, bytes-free decode of those edges;
until then keep preview changes blocked. A guarded override with stock
fallback is only a design constraint, not a proven hook. No firmware artifact
or hardware was accessed in this continuation.

### F-207 bounded runtime registration result

The verified initializer registers callback `0x1021d9e3` through generic
registry ID `0x1003a`; its initialized runtime record is labeled `BACKEND`.
A pinned stock-QEMU run through the standard assisted live-view startup
sequence observed one callback entry with flags `0x10`, not bit 20. This was
not correlated to a particular setup call and says nothing about capture
provenance. It confirms the route is a generic backend callback, not a proven
capture-only hook. The bit-20 producer/semantics and current/nested record
origins remain the exact blockers. Do not use the table-only candidate under
the still-only requirement. The next useful evidence is a bounded decode of
the backend event producer and record source; do not broaden into unrelated
backend tracing. Simulator output remained under `/private/tmp`; no camera or
candidate was touched.

### F-208 bit-20 producer and hook disposition

The bit-20 branch's producer is now statically connected: setter `0x10220fd6`
stores a supplied object in the module's `+0x60` current-object slot only when
empty, then posts `0x100000` through `0x10199cdc`. This is the event bit tested
by callback `0x1021d9e2` before it rebuilds a preview object. Two direct calls
to the setter were found (`0x1015672c`, `0x103e5d1c`); the latter receives a
stack-built descriptor from a generic backend worker path. Neither decoded
route has a still-capture predicate, and indirect callers remain possible.
The event is current-object assignment, not a verified new-still signal. The
specific event hook is therefore not safe for the still-only requirement, and
the shared area-4 table candidate remains incompatible. Further work should
only proceed by tracing the runtime-object source at `0x1015672c` and the
queued bit-24 producer feeding `0x103e5e88`, then proving both routes exclude
playback/editor at every relevant preview edit. If those edges do not provide
that proof, defer the preview patch. Full detail is in F-208 and the caller
map. No candidate or camera was accessed.

### F-209/F-210 producer continuation and disposition

The queued bit-24 edge is traced through `0x103e5e70` to descriptor builder
`0x103e5bdc`, which reads shared backend state, builds a multi-record
descriptor and calls setter `0x10220fd6`. The event notifier `0x103e89c2` is
reached through branch stub `0x1056a636` from shared helper `0x1055f834`.
A full-image cross-reference sweep found multiple callers of that helper in
state-management and cleanup/invalidation paths; it carries no capture
argument or local capture predicate. This strengthens the determination that
bit 24/bit 20 describe shared current-object state, not a still-only boundary.
The record's ultimate origin and playback/editor exclusion remain unproven.

A bounded pinned-stock-QEMU run observed no hits at the notifier, descriptor
builder, setter or preview callback during assisted live-view startup and
ordinary up/down/back/OK navigation. This closes only that simulator sequence;
it does not show the route is unreachable on-camera. The stock firmware hash
and QEMU checkout remained unchanged. Do not treat this simulator absence as
capture evidence. No safe still-only hook is established, so the preview
candidate stays blocked under the current requirement. Next useful progress
must identify an actual callsite that proves new-still provenance and
playback/editor exclusion; otherwise defer the patch. No camera or candidate
was accessed.

### F-211 runtime-object source route

The other direct setter caller is routine `0x10156714`. It passes a
base-derived object pointer only when two shared table counters satisfy
`r1 < r0`, then walks state-indexed entries and reads several backend values
while building descriptors. No capture-origin predicate is visible there.
A full-image direct-BL sweep and exact halfword-aligned pointer-word scan
found no direct caller/reference to the routine; computed/registered dispatch
remains possible. The bounded stock-QEMU startup/navigation run also did not
hit this routine or the setter. These are bounded absences, not proof of
camera unreachability. No still-only gate has been found. Next static progress
requires identifying the routine's inbound dispatcher and semantics for the
shared table counters, then proving any specific route excludes
playback/editor. Keep the preview patch blocked until that proof exists. No
camera or candidate was accessed.

## Historical research log (superseded where it conflicts with F-198/F-199)

F-191/F-192 comparison closes the baseline question: the public 65:24 feature
is not a drop-in because it switches to area 2/profile state and draws a grid,
while our target replaces 1:1 in area 4 and needs black bars. Preserve our
specified area-4 feature. F-193 provides a valuable same-firmware preview
lead: upstream uses an explicit return-address whitelist for its generic
preview getters, matching 12 of our local capture-builder/scaler calls and
excluding two display/scaling callers. Reuse that callsite method only after
checking the area-4 selector index and ABI. Its direct-buffer hooks are not
capture-caller guarded, and our matching constructor has known rebuild
callers. F-194 finds the wrapper's saved outer LR at `[sp,#36]` at the first
constructor table hook, allowing a site-specific caller guard without a
global one-shot flag. F-195 disqualifies the dimension-based creator itself:
it has no capture discriminator. F-196 corrects the earlier negative
reference claim: the creator is called by helper `0x1021d946`, whose direct
caller `0x1021da84` is conditional on flag bit 20 in dispatcher
`0x1021d9e2`. Trace the producer/meaning of that flag and the helper's record
source before considering any capture hook. F-197 shows initializer
`0x1021dac2` registers the dispatcher through shared callback machinery, but
the key and service semantics are unresolved. Next trace that key/argument
source; also verify the wrapper frame in a complete synthetic
wrapper→constructor run. No candidate exists; lifecycle gate remains unmet. See
[preview map](native-xpan-preview-callers.md).

The owner directed Codex to develop the camera-build solution, not Claude.
The concrete stills-only design is now added to
[native-xpan-build-architecture.md](native-xpan-build-architecture.md):
reuse the stored 1:1 choice, use the F-165 all-size area-4 crop descriptors,
and adjust embedded-preview dimensions only in proven capture-side
constructors guarded by area 4. Preserve shared playback/display getters,
the fixed thumbnail path, native RAW/JPEG encoding, and the standalone EG
compatibility/version metadata. Keep output, manifest and builder private.

No candidate exists yet. F-169 corrected the preview target: area-4 stock
limits are 480×480 and 1080×1080, so candidate four-pixel-aligned dimensions
for a 5200×1920 still are 480×176 and 1080×400. The upstream area-2 values
640×236/1920×708 do not apply. Three native direct-buffer constructors and
five candidate hook sites are now mapped and locally disassembled. F-170
executed those complete constructors synthetically; now prove exact
still-capture callers and each hook's input record, ABI, allocation extent,
row-stride and playback behavior. F-176 maps the localized label/size spans
into a private exact-length text-only manifest (144 edits; not a candidate).
Next trace the `0x24` version-policy consumer and complete the preview-hook
contracts and full manifest. F-177 disqualifies the `0x1021e7a8` route as a
capture guard: it attaches/reuses existing record-linked preview objects.
F-178 combines the localized text and proposed area-4 geometry as a private
160-span exact data-only manifest, checked in memory; no candidate output was
written. F-179 finds no tested PC-relative direct reference to the type-`0x24`
registration table. Continue tracing the other producers and base-relative or
indirect dispatch; then finish preview contracts, bars payload, metadata
policy, and full artifact checks. The offline Thumb trace now uses a validated
temporary ELF wrapper with Apple Clang/LLVM; do not assume hook safety from
address matching alone. Lifecycle condition 1 remains unmet; no camera
contact/write approval or candidate readiness follows from this research.

F-180 also rejects the native builder `0x1014319e` as an approved hook for
now: it is called while shared constructors materialize or refresh missing
records, not from a proven new-still boundary. The nearby helper
`0x100a4f0a` is a resource lifecycle path with cleanup callers and a context
byte check, not a capture discriminator. Resume by tracing the actual still
record producer into these builders, or finding a per-record provenance bit
that distinguishes a new capture from playback/rebuild. Do not make more
simulator-fidelity probes; no camera contact or write.

F-181 verifies the original EG's CRC-16/XMODEM trailer convention by exact
read-only comparison and adds a synthetic-tested in-memory composer/auditor
for exact spans, bounded pre-CRC payload insertion, protected header fields,
parser capacity and full changed-byte accounting. No real input was passed to
it and no candidate exists. Next, trace the new-still producer; only after the
hook and metadata contracts close should a private driver load the completed
manifest through the exact-original gate and emit a candidate outside Git.

F-182 exercises that composer against the exact original plus the existing
private 160-span text/geometry manifest in memory: all spans and CRC pass,
length is unchanged, and temporary output is discarded. The plan is still
incomplete. Continue tracing capture provenance; do not treat this data-only
composition as the requested XPan candidate.

F-183 adds a strict private-manifest parser gate and the expanded composer
tests (14 synthetic tests in the standalone-EG module). The `COMPLETE_REVIEWED_PLAN`
marker is only a declared status; it does not itself provide human review or
semantic completeness. F-184 traces the dimension-based adapter at
`0x1009f884` to preview-object creation/attachment, but its dispatch source
and capture provenance remain unknown. It is not an approved hook. Continue
from real still-capture producers; do not build a candidate until preview
capture scoping and metadata policy are closed.

F-185 adds a private file writer guarded by an exact reviewed-manifest hash,
the verified-original check, repository-path rejection, exclusive output
creation, and independent read-back audit. Four synthetic filesystem tests
pass; the full suite now has 148 passing tests. The writer has not processed
real inputs and no candidate exists. Continue with static capture-producer
provenance and offset-0x24 policy; only then review a complete manifest and
use the private writer.
F-186 tightens its output mode to `0600` and verifies that in a synthetic
filesystem test, keeping any future local artifact owner-readable only.
F-187 exercised the writer against the verified original and incomplete
private data manifest: source identity passed, the incomplete plan was
refused, and no output file was created.
F-188 classifies offset `0x24` as printable version-like text and locates
formatter calls inside the CRC-success policy dispatch, but does not prove
the selected standalone callback's comparison semantics. Keep the field
unchanged and trace that callback alongside still-capture provenance.
F-189 merges the exact 12-span F-148 bars overlay with the 160-span text and
geometry plan. All 172 spans pass exact hashes, overlap checks, length and
CRC in memory; the output was discarded. The resulting private manifest is
still incomplete because preview hooks remain absent.

F-170 has since executed all three native direct-buffer constructors in
pinned QEMU with synthetic guest records. Proposed slot-4 dimensions flow
through the output records, and the fixed thumbnail remains unchanged. A
non-target area control also changes under a shared-table edit, confirming
that the candidate needs an area-4 shadow table selected only on a proven
capture path. The next step is to prove the exact still-capture callers and
close the hook ABI, allocation and playback contracts. Do not assume area 4
is itself a capture guard.
F-171 shows the wrapper for `0x10142d86` also has three direct callers in
preview/object-rebuild contexts. Treat these as potentially non-capture until
proved otherwise; an area-4 check alone is insufficient. Resume by proving
which caller paths are actual still capture and how each direct-buffer hook
can preserve all other contexts.
F-172 rejected the full adjacent 10 KB zero run as a code cave because
firmware pointers land throughout it. A 1,642-byte aligned zero subspan at
`0x1002d996–0x1002e000` has no direct pointer or scanned Thumb branch/
MOVW-MOVT hits, but is not cleared for use: section boundaries, computed
references and execution permissions remain open. Continue by proving exact
capture callers and the loaded code range. F-173 shows the current wrapper
callers build or rebuild objects from existing records but do not prove a
capture-only route. Evaluate a bounded EG-tail append with a local branch
veneer against the native loaded extent before selecting stub locations.
F-174 shows five candidate four-byte hook windows fit Thumb-2 BL reach to the
nearby zero subspan, and an eight-byte register-preserving literal veneer
assembles in a synthetic check. Executable mapping and displaced-instruction
semantics remain open. F-175 places a code append at `0x1207e038` before the
CRC, inside the modeled destination capacity; executable mapping is still
unproved.

Known corrections: see [corrections.md](corrections.md).

## Resumed by owner, 2026-10-17

The owner directed Codex to do this work, not hand it to Claude, and to keep
working toward a testable patch candidate. Continue offline against the
verified private Z 30 C 1.20 inputs; never touch the camera. The proposed
artifact/build/check architecture is in
[native-xpan-build-architecture.md](native-xpan-build-architecture.md).
The preferred format is standalone EG discovery type 2 with the native CRC
path, but candidate acceptance remains unproved.

Pinned upstream docs corroborate standalone EG output and a bounded code
append before CRC; F-166 confirms its `0x2940000` capacity matches the native
parser limit. A minimal append with a nearby branch veneer is a candidate
layout after loaded-range and instruction contracts are validated.
F-165 validates the proposed area-4
large, medium, and small descriptors through the native full builder in
pinned QEMU with temporary synthetic guest RAM; the original image and
simulator checkout were verified unchanged. F-166 confirms the parser's
0x2940000 capacity and the requirement to preserve the four-byte field at
offset 0x10. Preview hook ABI/buffer bounds, label and size strings, the
metadata/version policy for offset 0x24, and the exact private manifest remain
open. F-168 maps 16 direct preview-getter call sites; F-169 identifies three
direct-buffer constructors and five candidate hook sites and corrects the
area-4 preview dimensions. No capture hook's full ABI or bounds are yet
validated. Do not emit a candidate yet. The next step is a bounded native
constructor execution and register/stack/bounds review. Owner's latest
disposition keeps lifecycle condition 1 unmet; no camera readiness or write
approval follows from this work.

## PR #155 reconciliation, 2026-10-17

Lane 0 F-127 verifies native APPLV creation and 196 passive worker iterations.
A general scheduler stall is not supported in that fixture; property-producer
identity and complete lifecycle remain unproved. See native-worker-scheduling.md.
Old next-step proposals are historical: follow session-manager-brief.md and
current owner waivers, not simulator-completeness or closed save-path traces.
No hardware permission or firmware change; owner review remains required.

Owner direction for this checkpoint is recorded in
[owner-direction-2026-10-17.md](owner-direction-2026-10-17.md): saved crop is an
on-camera test item, not a blocker for the feature plan. Hardware remains
NO-GO.
Before further patch work, use [patch-readiness-checklist.md](patch-readiness-checklist.md)
to confirm that the hook, inputs, ABI, simulator acceptance, and hardware gate
are all explicitly accounted for.

Owner disposition, 2026-10-17: physical tracking activation cannot be supplied
by this simulator; test it in the tracking-enabled patch on the owner's real
Z 30. The missing press-to-start/stop behavior remains unverified and is an
explicit device-test objective, not a passed result or write approval. Tracking
candidate review revalidates a private 45-span plan, but no image is built.
The accepted package format/integrity contract is still unresolved, and the
test order still puts XPan before tracking. Modified firmware remains NO-GO.

## Current session update, 2026-10-17

Owner asked Codex to perform the bounded standalone-EG review instead of
handing it to Claude. F-163 resolves the main format question: standalone
discovery type 2 takes the native CRC route and does not take the unresolved
outer-package digest branch for type 4. See
[native-standalone-eg-route.md](native-standalone-eg-route.md). This is a
static branch result, not proof of candidate acceptance. Since this checkpoint,
F-165 has validated the all-size geometry through the native builder,
F-166 has confirmed parser capacity and the offset-0x10 compatibility rule,
and F-168 has mapped direct preview call sites. Preview hook ABI/bounds,
labels, offset-0x24 metadata preservation and the exact manifest remain
before constructing a stills-only XPan EG candidate from the verified
original. Include bars, label, geometry and previews; exclude
tracking. Keep firmware artifacts outside Git and preserve native checks.
Hardware remains NO-GO.

Latest scope: XPan geometry only, completed at F-162. Read
[native-xpan-5200-contract.md](native-xpan-5200-contract.md). The apparent
5208x1928 mismatch was endpoint-versus-dimensions confusion: bounds 8,8 to
5208,1928 are exactly 5200x1920. Static native arithmetic/table mapping and
both preserved full-builder probe reports agree; 256 synthetic arithmetic
cases pass. Group 3/index 19 drives rectangle dimensions; joint changes to
indices 4/14 alone do not. Origin is separately read. No new simulator,
firmware file/encoding, tracking or hardware work. Geometry's scoped large-
size contract is resolved; complete all-size/preview/label edits and native
artifact-format/integrity acceptance remain separate build blockers. No new
publication authorized by this geometry task; results remain local.
Merged PRs: #170 at 5c68bea, #155 at 71133cd; exact main verified with 130
tests and artifact/byte-dump/diff checks. Owner override was verified directly
in the session-manager thread; only these two PRs were merged. The standalone
format branch is now resolved statically; exact parser constraints and the
complete feature manifest are the remaining pre-build research.

Approved merge checkpoint: the owner explicitly overrode the earlier
owner-merge-only process. PR #170 merged at 5c68bea after passing CI. PR #155
is being reconciled with that main; only its facts append conflicted, and
all main facts plus unique F-127 are preserved. Merge #155 only after its
updated checks pass. No other PR is approved by this instruction.
Build status from existing evidence: private F-148 bars overlay and private
tracking object/in-memory candidate exist; no complete XPan or installable
firmware image exists. Most important blocker is a verified artifact-format/
integrity contract: full outer package needs the unresolved digest input;
standalone EG is a native lead, not yet fully validated. Complete crop/label/
preview edits, exact-build preflight/review and risk binding remain. Saved
RAW/JPEG correctness is reserved for camera testing; owner waivers remain
as recorded. No new research, firmware build/encoding or hardware access.

Owner-authorized publication completed: [PR #155](https://github.com/tokim25/nikon-z30-research/pull/155)
is reconciled at e655f5d, conflict-free with passing CI; not merged.
Preflight/handoff work is [PR #170](https://github.com/tokim25/nikon-z30-research/pull/170),
research commit 1674371 plus main reconciliation 81598fe and this publication
record. All 130 tests/scanners/lane/diff checks pass locally; no firmware bytes,
dumps, tables or installable patches published. F-156--F-161 are unique against
main 512e6b3; merged findings preserved. The unrelated approved owner-rule
addition remains uncommitted in proposed-rules-2026-10-17.md, restored exactly
from its transfer backup. No firmware build, address decoding or hardware work.
Claude's next task remains the standalone-EG contract review, separately from
this publication. Owner decides both merges; Codex research remains paused.

Historical publication checkpoint: older notes described lifecycle as
waived. The owner's latest disposition explicitly keeps lifecycle condition
1 unmet; that current decision supersedes the historical waiver wording.
Still-photo guard and byte-exact identity dispositions are separate and do
not establish lifecycle coverage or hardware approval. No hardware/build
work was part of that publication.
F-135--F-149 are already merged and preserved. Only unmerged local
F-150--F-155 were renumbered to F-156--F-161 against main 512e6b3.

PAUSED at the owner's request for handoff to Claude. Read
[native-claude-build-research-handoff.md](native-claude-build-research-handoff.md)
first when resuming. Consolidated packet includes tracking's separate-checkout
candidate/allocation/placement/constructed-control status, exact hardware
approval boundary, public-repo triage and permissions-parity checklist.
Its static standalone-route review was the single next Claude task at that
time;
tracking stays out of the first test. No permissions are assumed transferable.
New concrete lead: original native discovery type 2
recognizes standalone EG, parses it separately and selects CRC validation
without the outer-package digest path. Static landmarks agree with upstream
standalone-installation reports; complete compatibility/version/buffer contracts
still need review before adoption. Outer digest remains unresolved but may
not be needed for that format. No flag/check was changed. Critical scope:
F-148 covers bars only; label and capture/preview geometry are not in it.
Current upstream aspect-profile work has relevant area-sync/preview findings,
but uses area 2, whereas our requested replacement is area 4. Other requested
repo triage is in the handoff. No image, simulator run, encoding, hardware,
publication or new fact number. Single next step belongs to Claude: bounded
static standalone-route and minimum complete-edit contract. Keep lifecycle
condition 1 unmet by current owner disposition; do not repeat digest
source loops or infer readiness.

Transfer cleanup: all substantive local/untracked files and all seven
worktrees preserved. See the cleanup record in
native-claude-build-research-handoff.md. F-081/F-110 duplicates are inherited
from main. The cross-branch F-150 collision is resolved by renumbering only
our unmerged findings to F-156--F-161. Generated Python caches only were removed.

### Earlier checkpoints (historical; current handoff above takes precedence)

F-161: owner's Do it completed a bounded digest engineering checkpoint.
New private instruction evaluator matches native SHA-1 compression arithmetic
against hashlib on twelve synthetic message lengths and native suffix-loop
arithmetic against its closed form on 1,024 synthetic cases. Native config
parser/update/finalize were not executed; no suffix recovered and original
digest still unverified. New public read-only package_digest verifier requires
an eight-byte suffix, checks original first, then candidate; seven synthetic
tests added, total 130 pass. No firmware output, simulator boot or hardware.
See native-digest-arithmetic-verification.md for exact scope/private helper
identity. This supersedes the earlier no-code checkpoint below. Single next
step remains independently justified offline Z30 suffix/input evidence and
original-digest reproduction; do not ask owner for camera acquisition or
mistake synthetic passes for resolution. Local/uncommitted, no publication.

Bounded digest-source check completed: recovered verifier hash matches F-135;
its call structure and pinned upstream container reader have original-hash/
CRC checks, not a native modified-package digest implementation. Focused
public-source lookup found WonderLantern/nikon-fw-key-tool: Z30 decoding is
listed, but digest recovery/repacking is limited to Z8/Z9. Its EXPEED 6
instruction-constant hint did not establish a usable Z30 replacement; actual
Z30 setup still copies the external eight-byte source into digest state.
No foreign code installed/executed, no key guesses, simulator or hardware.
Owner does not know of an existing boot capture/verifier; do not ask them
to obtain camera data. Current stopping point remains blocked, not READY.
Next technical step needs verified Z30 digest recovery/input evidence; do
not repeat these same source checks without new evidence or request camera
approval for a package that has not passed. Source references recorded in
native-real-camera-readiness.md. All 123 tests and artifact/encoded-data/diff
checks pass; local uncommitted documentation, no publication.

Latest owner direction stops simulator-completeness/low-value research.
Minimum-test preparation now prioritizes one hard technical blocker: native
package digest needs eight verified bytes at 0x10000088 outside captured EG.
F-140/F-141 already establish this missing-input boundary; do not repeat
searches, guess inputs, change the validation path or access hardware to fill
it. No authorized offline source/equivalent is identified. Single next step:
supply independently verified digest input/equivalent and reproduce the
original check, then final exact-candidate preflight/review/risk record.
See the new minimum-test stopping-point section in
[native-real-camera-readiness.md](native-real-camera-readiness.md).
No package is accepted, so status remains blocked/NO-GO, not READY. Retained
lifecycle gate has not been silently waived; residual coverage gets a concrete
owner disposition rather than more simulator-completeness work. Stop once
the exact-build READY gate is genuinely met and report its hash/scope/risk
for separate immediate owner approval; no camera action follows automatically.
No simulator, encoding/build, camera or publication this checkpoint. All 123
tests and artifact/encoded-data/diff checks pass; changes local/uncommitted.

Future-camera readiness consolidated in
[native-real-camera-readiness.md](native-real-camera-readiness.md).
Modified firmware remains NO-GO: retained lifecycle gate, final package/native
digest, global exact-build review, exact-test backup/risk record, named READY
record and immediate approval are not complete. Read-only check is reported
through step 5, closure not yet reported. No new hardware activity authorized.
First eventual modified test remains XPan stills plus saved-crop verification,
without tracking; tracking audit lacks native activation/cancellation proof.
Recovery is service-or-total-loss risk, not safe or verified recovery.
Next owner hardware decision is session closure confirmation; exact-build
modified-test approval comes only after required gates pass. This was repo
review/documentation only: no simulator, encoding, build or camera operation.
All 123 tests and artifact/encoded-data/diff checks pass. Local uncommitted
on codex/firmware-preflight-plan; no commit/push/PR.

Owner reports read-only instructions 1–5 complete: camera version “1.2,”
consistent with target C 1.20; host identity NIKON DSC Z 30, vendor/product
04b0/0452, USB product version 0120, 480 Mb/s. Serial/full host report
excluded from Git. User-reported observations only: no installed-code hash
or zero-write guarantee. Step 6 idle shutdown/disconnection is not yet
reported complete; that is the single next owner step. No agent camera
operation or expanded access. Owner explicitly retained the unmet lifecycle
gate; modified firmware remains NO-GO. Result recorded in
native-hardware-gate-recommendation.md. Documentation/123-test checks pass;
no commit/push/PR.

Owner directly chose to keep lifecycle condition 1 unmet. Separately, the
session manager conveyed explicit narrow read-only connection authorization;
the owner asked Codex to choose the tool. Selected camera firmware-version
display plus macOS System Information USB identity view (local app metadata
11.0/build 915, read without hardware probing), after official Nikon/Apple
documentation review. Owner-operated instructions, evidence and stop rules
are appended to native-hardware-gate-recommendation.md. This is not a traffic
audit or zero-write guarantee; no camera-control commands or update tools.
No further permission requested for the already-authorized narrow scope.
Next single step: owner performs only that bounded check and reports model/
C version and USB identity or the stop condition encountered. No agent
connection, hardware command or settings change; modified firmware NO-GO.
Standard 123 tests and artifact/encoded-data/diff checks pass; no publication.

Hardware-gate recommendation written at
[native-hardware-gate-recommendation.md](native-hardware-gate-recommendation.md).
Recommend a separately approved, owner-operated identity/version-only
connection first. Existing rules grant no automatic read-only exception;
exact method review and immediate owner authorization are still absent.
Modified-firmware gates remain unmet/NO-GO. Recovery basis is accepted
service-or-total-loss risk for planning, explicitly not safe or a verified
recovery path; exact-build/test consent is still separate. XPan eligibility
and tracking gaps do not block a bounded stock read-only step, but retain
their feature-specific modified-build gates. Single next decision: owner
approval of the narrowly defined read-only scope/exception, followed by
method review and session-specific go-ahead. No hardware, patch, commit,
push or PR. Standard 123 tests and artifact/encoded-data/diff checks pass.

Lifecycle acceptance checkpoint: route inventory confirms the requested
end-to-end workflow cannot currently be established by the existing harness.
Historical 24f/251/252 events retain the last menu entry; 24e/250 close to
another mode; GUI Back and playback/warning routes do not supply acceptance.
No new simulator run or arbitrary event/activation was used to claim success.
Exact F-148 manifest/all twelve file identities reverified read-only.
Concrete owner decision packet:
[native-xpan-lifecycle-decision.md](native-xpan-lifecycle-decision.md).
Condition 1 remains unmet unless the owner explicitly records a deviation
for native startup/menu-return/playback/warning coverage. No waiver or camera
approval inferred from Go. Next single step: obtain that specific acceptance
decision; offline preparation remains allowed, hardware remains NO-GO.
All 123 tests and artifact/encoded-data/diff checks passed; changes local,
uncommitted, no PR. No new research fact number allocated for this inventory.

Static branch review completed for claude/sharp-bartik-ed4fb7 at 9a60deb
against current remote/local main 8802ab7. No proven still-photo predicate
at 0x102f5810; empty stack plus selector 1 is insufficient to guarantee
excluded-state protection, but actual movie/playback reachability or damage
was not established. No proven static replacement guard found. Camera-ready
NO-GO remains; owner-authorized offline stills prototype remains in scope
without reopening the superseded movie prerequisite. Single decision: retain
the hook only at that bounded prototype status. Branch F-150 was subsequently
merged; the formerly colliding local finding is now F-156.
See [native-xpan-guard-branch-review.md](native-xpan-guard-branch-review.md).
No simulator/encoding/build/patch change or hardware. Review stopped here;
no publication or other lane edits. Documentation checks passed.

F-160 completes the bounded close/live-ready contract review on exact F-148.
Four paired cases (target/DX, ready/phase3) all return. Native inputs, known
runtime callback inputs, r4–r11, aligned/balanced stack, caller-stack words
and return CPSR pass. Ready preserves its original r0 result. Volatile
differences are listed explicitly and overwritten by the named native
continuations before use. No patch change is indicated by these cases.
See [native-xpan-close-ready-contracts.md](native-xpan-close-ready-contracts.md).
Private bars-only checklist/build-decision packet updated to this evidence;
no global condition-3 or natural-menu acceptance is claimed. Next required
evidence is a native menu return without diagnostic live activation or finer
stepping; do not repeat the retired flash-response investigation. The owner
must select any deviation from that acceptance gate; none is inferred.
Both sessions closed; original/QEMU unchanged. All 123 tests and artifact/
encoded-data/diff checks passed. Local uncommitted docs, no PR/hardware.

F-159: owner's subsequent Go authorized the next bounded read-only check.
The stop's LR maps to cached flash identity/geometry discovery. That native
initializer is shared by information, erase and program wrappers; retained
evidence lacks the outer caller, so no installation/persistence/corruption
cause is established. No new simulator run or patch change. Menu acceptance
remains open. Retire flash-response explanation work here; next single build
task is close/live-ready native hook contract review, using the exact F-148
overlay and original continuations. Existing private preliminary decodes:
codex-xpan-remaining-wrapper-review-01.json and
codex-xpan-remaining-wrapper-callers-01.json; neither is a completed audit.
See F-159 in [native-xpan-menu-boundaries.md](native-xpan-menu-boundaries.md).
Standard 123 tests and artifact/encoded-data/diff checks passed. All changes
local/uncommitted; no hardware or publication.

F-158: the one owner-approved writer-disabled control is complete. Omitting
only writer-branch redirection, with all eleven other overlays and nine coarse
candidate observation points retained, still stops at the same simulated
flash access/PC. Writer boundary matches stock; choice 1, menu mask off,
stack count 3. Subsequent live activation/bars check was not reached.
Writer redirection is not necessary for the observed stop; removing it is
not an established fix. Keep patch unchanged and menu acceptance open.
Stop here: no additional control or lifecycle/model work authorized for this
checkpoint. Next decision belongs to owner selection of a bounded follow-up.
See the F-158 section of [native-xpan-menu-boundaries.md](native-xpan-menu-boundaries.md).
Private evidence tag writer-disabled-01; session closed; firmware/QEMU
unchanged. Standard validation: 123 tests and artifact/encoded-data/diff checks
passed. Local uncommitted documentation only; no publication or hardware.

F-157 completed the paired menu-boundary observation. Stock/coarse returns;
candidate/coarse stops on an unmodeled simulated flash write, not timeout.
Writer entry-to-return-boundary registers and stack match stock. Candidate
with finer breakpoints returns through the original caller, count 3 skips
the mask, NZCVQ/frame/SP/target checks pass. Mixed, instrumentation-sensitive
completion is not a fix or menu acceptance. No code/overlay change.
Single next step: coarse comparison with only writer-branch redirection
omitted from candidate loading, retaining all other overlays and inputs.
This informs that hook's inclusion; do not open a flash-model fidelity trace.
See [native-xpan-menu-boundaries.md](native-xpan-menu-boundaries.md).
All sessions closed; firmware/QEMU unchanged; local uncommitted, no PR.

F-156 stills-only controls reuse the exact F-148 overlay. Callback-driven
rendering passes target/DX/target/16:9: 214/0/214/0 black rows. Ten setting
cycles pass with unchanged bounds/stack count, final DX mask off. Two native
menu-confirmation attempts on the candidate did not return; one stock control
returned. Do not assign a cause from that small sample or claim menu acceptance.
Next bounded step: paired stock/candidate menu-confirmation observations at
the writer/state boundaries. Movie evidence remains out of the prerequisite
set. See [native-xpan-stills-controls.md](native-xpan-stills-controls.md).

Owner scope correction: still/movie transition evidence is not a blocker for
the current stills-only candidate. Movie behavior remains unvalidated; do not
claim it is disabled. The earlier predicate-review NO-GO below is superseded
on that scope point only. Continue bounded stills controls on the exact F-148
overlay without weakening ABI checks or treating assisted calls as natural
menu return. See owner-direction-2026-10-17.md.

Still-photo predicate follow-up stopped UNKNOWN: reviewed mode-object/event
evidence does not establish a native still/movie field/value mapping or a
validated movie-switch input for the required paired control. The exposed GUI
has only navigation/OK/Back inputs; this is not proof that no firmware route
exists. No arbitrary internal-mode event or selector was treated as a movie
control. Paired behavior and cleanup ordering remain unverified; no new
overlay or simulator run occurred. Private result:
`$WORK/private-inputs/codex-xpan-still-predicate-review-01.json`.
Next decision: retain build NO-GO pending one verified native still/movie
input/transition route and semantic mapping for the bounded paired test.

Bars-only planning checkpoint after PR #156 merge: private packet at
`$WORK/private-inputs/codex-xpan-bars-spec-01` contains the existing F-148
reference specification, twelve before/after-hashed edit spans, minimal
checklist, native-lifecycle test plan and NO-GO build decision. First essential
unknown: a verified still-photo eligibility/disable predicate at the hooks;
choice, empty stack and selector 1 do not establish movie/playback exclusion.
Next single evidence: native predicate field/value mapping with a paired
still/movie control and cleanup ordering. Stopped on that unknown as directed;
no new overlay or simulator run, no saved-crop/tracking work, no publication.

PR #156 maintenance checkpoint: rebased onto main `c58ac95`; the only manual
conflict was in `docs/project-status.md`, retaining both main's newer lane
updates and this branch's evidence. F-135--F-149, owner-direction wording and
the minimal checklist are preserved. All 123 unit tests, artifact and encoded-
data checks, and `git diff --check` passed. No new research or experiment ran.

Clean stopping point, requested by owner/session manager: no new experiment
is running or scheduled. F-148's measured stack/flag correction passes the
bounded paired diagnostics; F-149's RAM mappings pass startup comparisons.
The static filename/getter thread is now closed; saved crop is reserved for
an owner-approved on-camera test.
Last full validation: 123 unit tests, artifact/encoded-data checks (including
new reports directly) and `git diff --check` passed. All changes remain local
and uncommitted on `codex/firmware-preflight-plan`; no push or PR was made.
Before publication, include the untracked source/tests/reports in manual
review: ordinary tracked diff statistics omit them. Older story/roadmap and
lower handoff status prose remain historical and partly stale; current
F-128/F-129 reports and project-status.md take precedence. Retain earlier
private experiment tags as rejected/control evidence; do not load them as
the current prototype or delete them during cleanup.

Story-level checkpoint requested by owner: neither complete shooting workflow
is accepted yet. Live-view bars/menu controls have assisted simulator evidence;
actual saved RAW/JPEG crop and button-driven tracking remain unproved. The
saved-crop question is now an on-camera test item, not a blocker. Recent
F-135..F-147 chiefly strengthen preflight and hook review. The persisted-choice,
quick-menu, in-strip readout and recovery stories remain open. Existing next
step below is unchanged; no additional experiment ran during this checkpoint.

Owner asked how firmware should be patched and checked before camera loading.
The proposed offline sequence is in
[native-firmware-preflight-plan.md](native-firmware-preflight-plan.md).
Audit completed: [native-package-verifier-audit.md](native-package-verifier-audit.md),
F-135. The recovered verifier accepted the original and an in-memory inverse
reproduced the complete original package exactly. Original file unchanged;
no firmware image written. A new private audit helper lives at WORK's
`codex-package-roundtrip-audit-private.py`; recovered tools remain unchanged.
Camera-side authentication/acceptance and CRC regeneration remain untested.
F-136 implements that reader in `src/nikon_z30_research/package_container.py`;
see [native-container-validator.md](native-container-validator.md). Synthetic
rejection tests and the original decoded container pass. All three original
component hashes were pinned; the unchanged round trip still passes.
F-137 adds `src/nikon_z30_research/patch_audit.py`, a read-only exact-edit
comparison; [native-exact-edit-audit.md](native-exact-edit-audit.md) records
the contract and combined CRC/edit tests. The verified unchanged package
also passed the empty-manifest baseline with zero changed bytes.
F-138 composes those checks in `src/nikon_z30_research/preflight.py`, with
synthetic integration tests and an unchanged original decoded-container
baseline. See [native-combined-preflight.md](native-combined-preflight.md).
Reports bind both inputs and the full policy; scope is decoded-container
only and hardware readiness is not established.
F-139 traces native body discovery/parser, confirms native effective decode
masks and CRC table against the desktop algorithms, and finds an additional
20-byte digest comparison outside our preflight coverage. See
[native-updater-validation.md](native-updater-validation.md). Main EG is
execution type 3; its handoff reaches relocated Thumb target `0xc2b10cd5`,
not yet mapped back to source. No actual flash operation is verified.
F-140 resolves the selector as the parser's encoded-format flag, carried in
the per-file cache and restored on selection. The verified original predicts
flag 1 and the extra-digest path after successful record restore; no runtime
transition was observed. Message boundaries and suffix configuration are
traced, but the eight bytes read from `0x10000088` remain unmapped. See
[native-updater-digest-inputs.md](native-updater-digest-inputs.md).
F-141 checks the startup page table and all 18 scatter records: the digest
address maps to itself below EG, and no copy/clear covers it. This records
the missing-input boundary, not an exhaustive later-remapping audit. Do not
repeat literal/offset searches without new evidence. The updater RAM block
is now mapped: ROM `0x12079f00` -> RAM `0xc2b10000`, length `0xfb0`;
entry `0xc2b10cd5` corresponds to EG offset `0x0205abd4` (Thumb address
`0x1207abd4` in ROM mapping). See
[native-boot-mapping-boundary.md](native-boot-mapping-boundary.md).
F-142 traces the native callback into erase/program/readback code. The
initialized EG target is `0x10020000..0x12960000` (end exclusive), capacity
43,253,760 bytes; EG payload excludes its two CRC bytes, and 9,314,248 tail
bytes are filled with FF. Erase starts with the leading 128 KiB chunk;
programming writes that chunk last. No updater function was executed.
See [native-install-span.md](native-install-span.md). `0x1011a028` adjusts
mapping; the worker handoff uses callback `0xc2b10c8b` via `0x101a27f4`.
F-143 implements `installation.py` and integrates an optional policy into
preflight. The model checks CRC exclusion, padding, target/protected bounds,
chunk ordering and an expected full-span hash without constructing an image.
Synthetic tests and the audited unchanged original baseline pass. See
[native-installation-model.md](native-installation-model.md).
F-144 reviews the existing F-101 overlay and later private revision read-only.
Checked file/install bounds, branches, literal loads and displaced returns
pass; both revisions retain a saved LR word at the state wrapper's stock
service call, shifting its entry SP and stack-argument view by four bytes.
Condition 3 does not pass. See [native-xpan-contract-review.md](native-xpan-contract-review.md).
F-145 implements a supplied-boundary checker and synthetic operation tests:
restoring the complete incoming frame before tail transfer passes; residual
stack words, register/stack corruption and wrong returns fail. This is an
abstract contract only; no actual wrapper implementation is approved. See
[native-call-contract-tests.md](native-call-contract-tests.md).
F-146 checks a private textual layout: 40-byte state wrapper plus 8-byte
writer fits the 52-byte candidate span with four bytes spare. Fourteen forms,
six branch distances and two literal displacements pass. Writer entry moves
four bytes and its hook must be retargeted; no overlay was produced. See
[native-xpan-layout-proposal.md](native-xpan-layout-proposal.md).
F-147 executes the throwaway correction in paired pinned-QEMU processes.
Final branches and loaded file hashes pass. Both state branches preserve
stock service-entry r0-r12/SP/LR/caller stack; the other-screen branch still
returns changed NZCV and fails F-145. The relocated writer consumes the same
working return frame and reaches its original return target; scratch LR and
flags are not certified. See [native-xpan-abi-experiment.md](native-xpan-abi-experiment.md).
F-148 corrects application-status preservation in a throwaway overlay. Both
state branches pass F-145 with entry flags additionally required; writer
frame/result/return flags match the baseline. Scratch writer LR differs but
its saved return target and mode match. No global condition-3 acceptance;
finite assisted diagnostics only. See
[native-xpan-flags-remediation.md](native-xpan-flags-remediation.md).
F-149 restarts saved-crop research with verified initialized RAM addresses
for F-110's two filename tables. Both four-pointer blocks and F-112's
eight-word geometry header match their mapped sources after stock assisted
startup. Nearby RAM references now exist, but reviewed ones do not yet read
the filename-pointer fields. No save path or cropped file is established.
See [native-save-table-ram-mapping.md](native-save-table-ram-mapping.md).
Single next step: trace actual filename-pointer-field loads using these RAM
addresses/module anchors, then follow their request toward file creation or
serialization. Require a field load before naming a consumer; do not resume
the retired builder-caller or SD-model threads.
Missing native digest input
and natural lifecycle/saved-crop gaps remain open.
Private reproducible helpers:
`$WORK/codex-boot-mapping-audit-private.py` and
`$WORK/codex-native-updater-audit-private.py` (use WORK/analysis-env Python,
PYTHONPATH=src). Runtime/file mapping and instruction review remain open.
Latest private helper: `$WORK/codex-install-span-audit-private.py`.
Overlay review helper: `$WORK/codex-xpan-contract-audit-private.py`; it reads
the two existing overlays only and writes no overlay or firmware bytes.
Layout helper: `$WORK/codex-xpan-layout-proposal-private.py`; captures textual
assembler output in memory only. No final encoding or execution is verified.
F-147 helpers: `$WORK/codex-xpan-abi-experiment-private.py` and
`$WORK/codex-xpan-abi-compare-private.py`. Final paired fixture tag `03`;
earlier tags `01`/`02` did not establish settled bars-on controls. New private
overlay files exist under WORK inputs only; no combined firmware image exists.
F-148 helpers: `$WORK/codex-xpan-flags-experiment-private.py` and
`$WORK/codex-xpan-flags-compare-private.py`, passing paired tag `01`.
The shared private ABI runner now reads writer location from the supplied
manifest, retaining reproduction of its earlier layout.
F-149 helper: `$WORK/codex-save-table-ram-audit-private.py`, recorded tag `01`.
Both user features remain incomplete. The saved-crop path is the active
research priority after the measured stack/flag remediation.
No candidate image, commit, push or PR was produced.

Correction to the older pending-review notes below: hardware-readiness.md now
records the independent dissenting review and remediation attempt. The owner
accepted a Claude session as the reviewer. The review found condition 1 only
partly met, and remediation (a) did not reach the guard/mask. Feature build
work remains gated pending further evidence or an explicit owner deviation.
The complete XPan build also lacks a verified saved-crop path. Hardware remains
NO-GO. Do not resume retired simulator event-poster archaeology by default.

Rewritten 2026-10-16 by Claude, with the owner's explicit approval to edit
this Codex-owned file (a lane exception, same as PR #50). Read this file,
then [facts.md](facts.md), [project-status.md](project-status.md) and
[AGENTS.md](../AGENTS.md) before doing anything. This version adds a second
handed-off lane (saved-crop) on top of the first (live-view-bars hook); both
are below. If you remember an older copy of this file with fact numbers
below F-050, ignore it.

## Read this first

**Owner direction, 2026-10-16 — read [AGENTS.md](../AGENTS.md)'s new "Priority"
section first.** This project tests modded firmware on the owner's own real
camera; every thread should lead toward a concrete patch, hook point, or
build decision for the real firmware, not toward explaining a limit of this
project's own simulator. A card-detect/SD-command-enumeration thread
(F-102, F-104) was explored this session and retired for exactly this
reason — see "Lane 2" below for where it stopped and why.

Main carries facts through **F-114**; check main before allocating F-135.
Hardware access stays **NO-GO**
([hardware-readiness.md](hardware-readiness.md)); nothing here authorizes
touching a real camera. Build-phase work is open for the owner's own,
non-distributed camera ([build-phase-gate.md](build-phase-gate.md)), but all
work stays in the offline simulator.

Owner decision recorded 2026-10-16: absolute hardware safety is no longer an
acceptance criterion because it cannot be proved before a first hardware
test. The gate now distinguishes **SIMULATOR ACCEPTED**, **READY FOR AN
EXPERIMENTAL HARDWARE TEST**, and **HARDWARE VALIDATED**. A missing recovery
path must be stated as an accepted service-or-total-loss risk; it may not be
described as safe. The current state remains NO-GO.

The owner's goal, restated plainly, is in
[user-stories.md](user-stories.md) and [roadmap.md](roadmap.md): an XPan
(65:24) choice that replaces "1:1" in "Choose image area", live view shows
black bars that track that choice, and the saved RAW/JPEG is actually
cropped. The concrete data-level plan is
[xpan-replace-1to1-plan.md](xpan-replace-1to1-plan.md).

Both lanes below were handed to you because Claude hit a genuine wall for
each — a repeated safety-classifier stop on one, and the simulator's actual
functional limits on the other — not because either question was shown to
be unanswerable. Treat both as open research.

## Lane 0: why natural triggers never fire (blocks Lane 1 and Lane 3 both)

**New section, 2026-10-17, handed off at the owner's explicit request** to
try the harder approach "if necessary to get to hardware install" after
Claude ran out of cheap options on both lanes' natural-trigger questions
(F-019, F-109, F-115 through F-117). Claude did not attempt this itself —
the owner asked for it to go to Codex directly, and the scope (likely
touching the QEMU machine model, not just Python scripts) is a better fit
here regardless.

**The pattern, stated once instead of per-lane.** Every lane that depends
on a background worker or the RTOS's own task scheduler servicing
something — Lane 1's live-view-enter/menu-close triggers, Lane 3's
`0x2006`/`0x2020`/`0x2021`/`0x2087` property-event producer — comes back
dormant. F-019: a stock refresh runs none of 14 observed worker/task
addresses. F-109: event `0x4100012`'s poster has zero references in the
image by four independent static methods, and is "obviously" delivered on
real hardware (F-090) by some mechanism this simulator doesn't reproduce.
F-117: the shared property-post primitive `0x10475ecc` was never called
at all across an idle wait plus a real menu-activation-and-eight-key
sequence — not a miss on one id, a miss on everything.

**This is probably not "the QEMU model has no scheduler."** Read
`qemu/nikon-z30.c` before assuming that: the machine wires a real GICv2
IRQ controller to both CPUs and has a real `QEMUTimer`
(`platform_timer`), gated by an `assisted` flag that only shortcuts
specific MMIO addresses (`0x20010034`, `0x24074000`-`0x24074800`,
`0x04287010`/`0x04287004`, the UART regs) for bring-up — it is not a pure
host-orchestrated step machine. The more likely explanation, not yet
checked: every observation in this project so far comes from either (a) a
synchronous diagnostic call (`guest_call.py`'s `call()` / `display_session.py`'s
`run_to()`) that hijacks one thread's register context, forces `pc` to a
target function and a sentinel return address, and runs only until that
sentinel is hit — which never gives the RTOS scheduler a reason or a
window to switch to a different task — or (b) a short passive `run_for()`
window too brief for whatever the worker is actually waiting on. Nobody
in this project has yet tried a long, uninterrupted free-run (seconds to
tens of seconds, no diagnostic call in flight, real timer/IRQ ticking)
after setting up the right preconditions, to see whether the firmware's
own scheduler services the worker on its own.

**The actual ask, in order of cost:**
1. **Check whether the relevant worker tasks are even created.** Find
   where the firmware creates/registers background tasks during startup
   (an RTOS task-create primitive should have a findable signature — this
   project has already identified several task/screen-stack-shaped data
   structures, e.g. `0xc181e4f0`, the various `0xc182xxxx`/`0xc2xxxxxx`
   globals named throughout `facts.md` — reuse what's already known rather
   than starting from zero). If a worker this project cares about (the
   live-view worker, whatever posts `0x2006`/`0x2087`) is never created in
   this assisted boot, that's the actual answer and the rest of this list
   doesn't matter — document it as a fact and stop there.
2. **If workers are created, try a long free-run instead of a diagnostic
   call for the trigger step.** Set up state with the usual diagnostic
   calls (as F-101/F-115/F-117's scripts already do), then switch to
   `run_for()` with a materially longer window (tens of seconds, not the
   few seconds used so far) with the relevant breakpoints armed via
   `run_to(..., observe=(...))`, and see whether the scheduler reaches the
   worker on its own. This needs no QEMU source changes, just a different
   use of tools already in `z30-qemu/tools`.
3. **Only if 1 and 2 both come back empty**, investigate whether the
   `assisted` profile's MMIO shortcuts (listed above, in `nikon-z30.c`) are
   themselves what stalls the scheduler — e.g. a real IRQ source the
   firmware's idle/scheduler loop waits on that `assisted` mode fakes or
   skips. This is the only item on this list that would mean touching the
   QEMU machine model's C source, and it's the one to treat as a real,
   possibly multi-session undertaking — not something to start speculatively
   before 1 and 2 are tried.

**What this does and does not authorize.** This is still simulator-only
research. **Resolving this does not by itself get to hardware install** —
`hardware-readiness.md` is explicit that install needs the owner's written
risk acceptance plus conditions 2 through 4 (checksum/signature review,
patcher review, recovery risk), none of which this lane touches. Treat
"get to hardware install" as this project's long-term direction, not as
something a scheduler fix hands to the owner automatically. The usual
rules apply in full: offline/simulator-only, never touch the owner's real
camera, never commit firmware bytes, overlay bytes, disassembly or patched
images. If this turns out to need changes to `z30-qemu`'s C source (item 3
above), that is new territory for this project's commit conventions —
check with the owner before committing machine-model source changes, the
same way build-phase firmware changes get owner review.

Full detail behind this handoff: F-018, F-019, F-109, F-115 through F-117
in [facts.md](facts.md); [tracking-input-chain.md](tracking-input-chain.md)'s
two 2026-10-17 sections; `qemu/nikon-z30.c` and `qemu/nikon-z30-display.c`
in the pinned `z30-qemu` checkout.

**Side note, not part of this handoff's scope but worth knowing before
digging into any "zero callers found" dead end:** F-120 confirmed this
firmware genuinely contains ARM-mode code (a real `memcpy` routine, at
two separate addresses, reached via Thumb `blx`-immediate), something
every prior static scan in this project -- including this task's own
dormant-worker reasoning -- assumed away. Nothing checked so far shows
it's relevant to event `0x4100012`, `0x10459d80`, or Lane 3's property
dispatch specifically, but if 1 (task-creation check) and 2 (long
free-run) above both come back empty, checking whether a relevant
dispatcher's one missing caller lives in an undiscovered ARM island is a
cheaper thing to try before touching `z30-qemu`'s C source.

## Lane 1: the live-view-bars hook

Claude hit the same safety-classifier stop twice in a row researching
firmware code-insertion mechanics; the owner decided Codex should try
instead. The full design doc is [xpan-bars-design.md](xpan-bars-design.md)
— read it in full; this section only summarizes.

**What's proven:**
- The camera can draw a persistent black-bar mask on one screen layer with
  one flag, one geometry and one color (F-042, F-044).
- Those layer settings come from a stored template copied at startup
  (F-088), not from the image-area choice.
- Two of the three trigger moments the bars need (live view starts, return
  from a menu) have found candidate code locations (F-089, F-090); "the
  area changes" does not yet.
- The image-area pick can now be driven through the real simulated menu
  (F-093) — it hangs on the OK key about half the time and must be retried,
  but when it returns the choice really persists. A byte at `0xc1811d90`
  follows the pick (0 DX, 1 for 1:1, 2 for 16:9); its readers/writers are
  not found (F-094). **Important correction**: an earlier chain built on
  three other bytes (F-081 through F-087) turned out to be wrong when tested
  against a real driven pick — those bytes stay 0 regardless. Don't trust
  that old chain; F-093/F-094 supersede it.

**What's blocked (the actual ask):**
1. Find where in the firmware a safe place exists to add a handful of new
   instructions that run at the three trigger moments and toggle the layer
   mask based on the stored image-area choice. This is build-gate condition
   1 ("the simulator shows the feature working without a debugger hook, or
   that hook's risk is fully understood" — `build-phase-gate.md` line 33).
2. Once a candidate spot exists, tie it to the three trigger moments
   (F-089, F-090) and to the `0xc1811d90`-style choice byte, and test it in
   the simulator per the "How we will know it works" checklist in the
   design doc.

### F-101 result on `codex/xpan-liveview-hook-space`

- The exact property writer is at `0x1008d38c`, with the choice-record store
  at `0x1008d3fc`. The final byte at `0xc1811d90` is 0 for DX, 1 for 1:1 and
  2 for 16:9. The older value-4 statement describes the callback argument,
  not this stored byte.
- Four zero-filled candidate instruction spans were found and checked at
  their real ARM/Thumb boundaries: `0x1002d78c..0x1002d7bf`,
  `0x1002d80c..0x1002d83f`, `0x1002d860..0x1002d87f`, and
  `0x1027f468..0x1027f47f`.
- A private QEMU loader overlay placed synthetic new code in those spans
  before CPU start. It used wrappers at the exact writer, live-view-ready
  transition, screen close and generic screen activation. The debugger did
  not write code, choice, mask state, bounds or color during the run.
- A real 1:1 menu pick left the mask off over the menu. An audited live-view
  activation restored it. DX and 16:9 kept it off. Ten alternating screen
  signal cycles passed. Direct stock callback tests also changed the mask
  immediately while live view stayed active.
- The later menu-notification callback was tested and rejected as a general
  change trigger. QEMU write watchpoints also failed a known-store self-test.
- A follow-up rejected an unguarded screen-close trigger. Internal events
  `0x24e` and `0x250` close the last stack entry but request mode `0x10000`,
  not live view; the unguarded hook enabled the mask on that transition
  screen. The final overlay requires an empty stack and live-view selector 1.
- The live-view trigger now sits at `0x102f5810`, where `0x102f57e2` sets
  selector 1. The guarded build passed the area controls and ten signal
  cycles, and stayed off after the non-live-view close control.
- A diagnostic call through the stock type-2 dispatcher reached that full
  live-view-ready path and returned with selector 1, stack count zero and the
  1:1 mask on. The natural worker trigger remains dormant in the fixture.
- Full evidence, repro commands and limits are in
  [native-xpan-liveview-hook.md](native-xpan-liveview-hook.md). A true menu
  return to live view, the natural startup caller and the exact `i`-menu
  route are still open.

### Single next step for Lane 1 (superseded below)

Find a stock menu-close event sequence that reaches `0x102f57e2` without a
direct diagnostic call, then confirm that the guarded hook restores the mask.
The exposed Back key cannot close the final menu screen, and the tested
internal close events do not request live view.

**Update (2026-10-16, picking up PR #119's own "single next step"):** a
prior Codex run (before running out of budget, work not committed) found
that the normal menu-close handler reaches the live-view-ready path when an
internal mode-state check comes out a specific way, and was tracing what
naturally sets that state. Claude continued the same trace a little further
before hitting its own repeated classifier stop on this exact sub-question
(three in a row) and is handing it back: the close handler (one of
`docs/native-xpan-liveview-hook.md`'s key addresses) has no direct callers
and exactly one table entry, at `0x113033a8`. Its branch between the two
internal modes reads a small helper, which in turn checks a function whose
return value of 0, 3, or 4 selects the live-view-targeting mode (any other
value selects the non-live-view mode already shown not to reach the hook).
That function's own addresses and what feeds it were not yet read. This is
exactly the open thread PR #119 names as its "single next step"; pick it up
from there rather than re-deriving it.

**Owner note on the pattern:** this one specific sub-question (what
naturally drives the menu-close-to-live-view transition) had stopped
Claude three times in a row via the safety classifier, more than any other
single topic in that session.

**Update (2026-10-16), resolved one level further, no classifier stop this
time (F-107):** the close handler is confirmed as `0x10460c3c`. Its chain
is now: `0x10460c3c` -> calls `0x1045b27e` ("the small helper") -> calls
`0x10457db2` (this is exactly where the prior session stopped) -> which
turns out to be a trivial 3-instruction getter reading one byte at
`0xc181f6fc` and returning it directly (not the `cmp`-dispatcher an
earlier reading assumed -- that's a different, unrelated function one
step over). Two more literal-pool references to `0xc181f6fc` were found
and both are **reads** into small lookup tables anchored near it, not
writes. Full detail in facts.md F-107.

**Update (2026-10-16), the natural trigger found, three-stop question
resolved (F-108):** a register-arithmetic scan (not a literal match)
found the setter, `0x10457dac`, the plain sibling of F-107's getter. It
has exactly one direct caller anywhere in the image, inside a dispatcher
at `0x10459d80`: when the incoming event code equals **`0x4100012`**, it
calls the setter with `r0 = 4` -- one of F-107's three live-view-selecting
values -- then calls `0x1046283c` and `0x10462894` with no further gating.
**Those are the same two calls F-090 already found inside the live-view-
start routine `0x102f2990` itself.** That match is independent
corroboration this is the real trigger, not a coincidental write. No
classifier stop encountered anywhere in this chain. Full detail in
facts.md F-108.

**Closed, deliberately, not pursued further (F-109):** who posts event
`0x4100012` was checked by four independent full-image methods (direct
calls, tail branches, raw pointer-table words, table-branch jump tables)
-- all four found nothing. Not escalated to ARM-mode scanning or manual
UI-pump archaeology, because the question itself had drifted into
simulator-reachability territory (can the simulator's limited key set
post this event) rather than a real-firmware question -- the real camera
obviously already delivers this event through ordinary use (F-090), and
F-108's hook sites sit downstream of it, not upstream. A real build does
not need this answered.

**Update (2026-10-17), the "ARM-mode scanning" item checked, general
finding not specific to this question (F-120):** this firmware does
contain real ARM-mode code, confirmed for the first time -- a `memcpy`-
style routine (duplicated at two separate addresses, one called from the
InitTask entry function itself), and compiler-runtime-shaped helpers,
all reached via genuine Thumb `blx`-immediate calls this project's
Thumb-only decoding had never surfaced before. **This does not show
`0x10459d80` or event `0x4100012` are themselves ARM-reachable** -- every
confirmed site is a mundane library routine, not application logic, and
mapping the full extent of every ARM island to check was not attempted
(real, separately-scoped work). Worth keeping in mind for Lane 0 and for
any future "zero callers by every static method" dead end on any lane --
the blind spot is now confirmed real, not just theoretical. Full detail
in facts.md F-120.

**Update (2026-10-16), owner call made, pending a dissenting review:** the
owner has called build-gate condition 1 satisfied for Lane 1 on this
evidence (instruction space and native-execution proven, F-101; the
natural trigger's mechanism fully understood end to end, F-107/F-108,
though not demonstrated firing naturally in the simulator). **Correction**
to the "second branch" framing used earlier in this file and in F-109: the
current gate text (post the PR #119 hardware-safety rewrite) has no
explicit "or that hook's risk is fully understood" alternative any more --
condition 1 now reads only "the simulator must show the feature working
without a debugger memory write, and the relevant state transitions must
pass." Whether the diagnostic-call evidence already available satisfies
that, given the natural trigger itself was never observed firing, is
exactly the ambiguity the owner's call rests on.

**This call does not authorize any build-phase work yet.** A dissenting
review from Codex, run as its own independent session, is required first
-- see [hardware-readiness.md](hardware-readiness.md)'s new section for
the review's exact scope. Record the review's conclusion there when it
happens.

**Update (2026-10-17), dissenting review recorded and an instruction-level
audit done (F-115, fix-and-retest pass):** the dissenting review (PR #144)
disagreed that condition 1 is satisfied as worded -- see
[hardware-readiness.md](hardware-readiness.md). Separately, an
instruction-level audit (PR #145,
[native-xpan-liveview-hook-audit.md](native-xpan-liveview-hook-audit.md))
reviewed the private guarded-hook generator and found no crash-level
defect but three things worth fixing and re-testing: `r2` clobbered on the
screen-activation wrapper's tail call, 4-byte stack misalignment in the
close wrapper and guard, and a shared mask-clear helper that runs on every
non-live-view screen activation, not just live-view's own.

F-115 fixed the first two (same-size push/pop bitmask edits; re-disassembled
every routine after rebuilding) and re-ran every existing simulator control
against the fixed overlay -- all passed, firmware hash and QEMU checkout
unchanged. It deliberately left the third (the shared helper) unchanged:
tracing it confirmed the audit's concern is architecturally real (the
activation path is a generic per-object-type dispatch, not live-view-
specific), but properly narrowing it would require an open-ended trace of
which object types are legitimate live-view overlays -- exactly what this
project's priority rule says not to start for a simulator-side question.

F-115 also repeated the dissenting review's cheapest remediation option
(preset the mode-state byte via the firmware's own setter, call the real
close handler `0x10460c3c` directly) against the fixed overlay. Unlike the
same test against the pre-fix overlay (PR #146, where the guard and mask
were never reached), this run reached both the guard and the mask helper on
the close-handler's own code path -- the first time this project has
observed that happen outside a diagnostic dispatch call. The mask flag's
value did not change in this one run (it was already 1 before and after),
so this does not demonstrate a flag flip caused by the close path, and the
likely explanation (the stack-alignment fix changing the stock callback's
behavior) was not pursued further. **Condition 1's status is unchanged by
any of this** -- the dissenting review still stands, and whether this new
evidence moves the owner's call is the owner's decision, not something this
pass claims to have resolved.

## Lane 2: saved-crop (does a saved RAW/JPEG actually come out cropped?)

This remains an on-camera test item, not a blocker for feature work. Static
the static filename/getter thread is now dropped: Claude's F-131--F-134
searches found no concrete route. Any simulator run requires the owner's
approval, and hardware remains NO-GO until separately authorized.

Claude worked this in its own worktree (`nikon-savedcrop`, branch
`claude/saved-crop-research`, now idle and available to reuse or ignore),
facts F-095 through F-100. Two different approaches were tried and both
hit real limits; a third angle is the open suggestion below.

**Approach A: trace the crop-window builder's callers toward a save path.**
Of the builder `0x101d5b36`'s seven callers (F-057), six build small
display/menu info structs (F-095). The seventh, `0x101d5de8` inside a
function at `0x101d5c54`, is different: it assembles one large record
(growing past `0x328` bytes) combining the crop geometry, bit-depth/size
math (`0x101dc204`, dividing 24 bits across 1/2/3/6 components — F-096),
and copied device-config blocks. It has exactly four direct callers in one
tight code region (F-097), three sharing a shape: a capability check keyed
on a per-area id byte, a prepare call, the record build, then a size pair
copied from `base+0x2b00+0x4c` into the finished record. **This is
genuinely ambiguous between two explanations and nothing found so far
picks one**: (a) a capture/save request descriptor, or (b) a
"shots-remaining-at-this-quality" UI estimator, which needs the same
ingredients (geometry + bit depth + per-mode math) but never touches
storage. F-098 found two of the three next-outer callers are reached only
by pointer/table dispatch (weak lean toward UI, not conclusive).

**Approach B: test it live instead of reasoning about code shape.**
Three simulator runs with a breakpoint on the record builder and all four
callers, across menu screens most likely to show a shots-remaining count
plus a full menu-tab sweep, got zero hits (F-099) — but the simulator's key
set has no shutter/capture button and no info-overlay button at all, so the
capture-triggered half of hypothesis (a) can't be tested through normal
input either way. Separately, attaching a synthetic blank SD card with SD
trace enabled showed the controller sees a card insert, but the firmware's
own "Format memory card" menu item stays greyed out and zero SD read/write
commands ever happen (F-100) — something in the firmware's card-presence
check rejects the synthetic card before any file I/O could occur, closing
off the live-observation angle structurally, matching what the simulator's
own README already said about photo/movie recording being out of its
supported scope.

**Update (2026-10-16), card-presence check traced (F-102):** the detect
function itself (`0x104157b8`) is a plain, satisfiable bit test (SDHCI
Present State bit 16 on controller 0) — not the blocker. The stronger
candidate is a downstream stall: `0x104164ba`, a generic "issue
command, wait for completion" primitive used ~8 times during SD bring-up,
always waits on controller 0's specific hardware event object, matching the
QEMU model's own comment that "polling commands can work there but DMA
completion never reaches the event object awaited by 0x104164ba." Not
proven end-to-end. The direct link from card-detect's result (or the global
status struct at `0xc18015e8`) forward into the Setup-menu enable/grey-out
check was not found — that's the open gap, along with decoding the 8
`0x104164ba` call sites individually. Full detail in facts.md F-102.

**Update (2026-10-16), Approach A continued, F-098 partly corrected
(F-103):** `0x101568ca` and `0x1015be26` are internal basic-block labels,
not function entries — their real enclosing functions are `0x10156714` and
`0x1015bc3e`. Re-checked against the real entries, `0x1015bc3e` turns out to
have ordinary direct callers (not table-dispatched as F-098 implied); only
`0x10156714` still has zero references found by any literal mechanism.
`0x1015a93c` itself decodes as a property/event-ID dispatcher (compare
against ID constants, then jump table) shared as a callback pointer from 17
separate literal-pool sites across ~65KB of code — the textbook shape this
project has already tied to menu/property tables (F-072/F-090), not a
capture/save pipeline. Leans toward hypothesis (b) (settings/property
handler, not a capture descriptor) at low-to-medium confidence; no
unambiguous storage-write or UI-counter call was found either way. Full
detail in facts.md F-103.

**Update (2026-10-16), the 8 `0x104164ba` callers decoded (F-104):** they
collapse to exactly 4 enclosing functions, each loading a command word that
decodes as a standard SDHCI command register value for CMD17
READ_SINGLE_BLOCK, CMD18 READ_MULTIPLE_BLOCK, CMD24 WRITE_BLOCK and CMD25
WRITE_MULTIPLE_BLOCK (high byte = SD command index, shared low byte `0x3a`
= data-present + index/CRC-check + R1-response flags). Each calls
`0x104164ba` twice in what reads as the standard two-stage "buffer
ready, then transfer complete" wait. This strengthens the F-102 stall
theory: if any of these four ever fire against controller 0, they'd stall
at the first wait under the QEMU model's own documented limitation —
independently explaining both F-100's zero `sdcard_read_block` events and
the "Format memory card" grey-out. Still open: whether the firmware's
bring-up sequence reaches these four commands at all before giving up
earlier (e.g. during CMD0/ACMD41/CMD2/CMD3 enumeration, not decoded here),
and the menu-enable/grey-out link itself. Full detail in facts.md F-104.

**Retired, 2026-10-16 (owner direction):** the card-detect/SD-enumeration
thread (F-102, F-104) stops here. It traced real firmware addresses (useful
background: card-detect `0x104157b8`, the block-transfer commands CMD17/18/
24/25, and most of the CMD0/CMD8/ACMD41/CMD2/CMD3 enumeration sequence —
see F-102/F-104 for the addresses if ever needed again), but confirmed the
open question at this point is "why does this project's own QEMU SDHCI
model fail to complete a command" — a simulator-fidelity limit, not a real
firmware question, and not something a hardware build needs answered. Do
not resume it, and do not decode CMD0's enumeration further (F-105 was
drafted and discarded for the same reason), unless a specific build
decision later turns out to depend on it.

**Update (2026-10-16), direct-write path checked and ruled out (F-105):**
an automated call-graph walk from the F-097 four, following every direct
`bl`/`blx` transitively (867 distinct functions, exhaustive -- the search
queue emptied, not a node cap; method validated against F-102's
hand-decoded card-detect function), never reaches F-104's CMD24/25 write
wrappers or the shared command-submit primitive. This rules out the
simplest form of hypothesis (a): none of the four callers, or anything
they call directly or transitively, synchronously writes the finished
record to storage right after building it.

**It does not settle the question.** The walk only follows literal
`bl`/`blx` targets -- it cannot see a hand-off through a function-pointer
table or a queued/global slot read by a separate worker, which is this
project's established pattern for handler dispatch elsewhere (F-072,
F-090, F-098).

**Update (2026-10-16), both follow-ups run, leans toward (b) at medium
confidence (F-106):** the global-write scan over F-105's 867 functions
found two real leads, both ambiguous on their own; `0x1015bd18`'s four
modes were fully decoded (correcting F-103's mode assignment) alongside
`0x101e729e`/`0x101efb9e`. The strongest finding: `0x101efb9e` leads to a
function that **synchronously calls** the `0x1015a93c` property dispatcher
directly with an id and output pointer -- a property get/notify call, not
a job registration -- and the one event queue found (`0x101e729e`'s path)
is generic and posts to a queue architecturally distant from the SD code
block. Both lean toward (b). The one open thread: mode 2 of `0x1015bd18`
dereferences a global slot (`0xc18a6890`) and, when non-null, copies data
from it using the exact same offset/size as F-096's record-builder's first
block copy -- real but unconfirmed evidence the slot holds that record's
output. The slot's actual producer was not found by a literal-word scan
(6 hits, none resembling a write) and likely computes the address via
register arithmetic on the module's wider base (`0xc18a6810`, used 52
times across `0x10152000`-`0x1015c600`) rather than its own literal. Full
detail in facts.md F-106.

**Resolved, accepted as the working answer (owner decision, 2026-10-16):**
(b) is the working hypothesis; the `0xc18a6890` slot-producer thread was
not pursued further. `hardware-readiness.md`'s "RAW crop"/"RAW output
path" rows were corrected to say so plainly: the record-builder chain is
not the save path, and the real save-crop mechanism is still unfound --
this was previously understated.

**Update (2026-10-16), a fresh, separate angle opened (F-110):** rather
than continuing on the (ruled-out) record-builder chain, traced the
firmware's actual file-naming system instead. Found a real filename-
template table (`DSC_0000.NDF/NEF/TIF/JPG`, `0x11c9a5fc`) and two
distinct tables referencing it (`0x1204d280`, `0x1204d440`) with
different preceding data -- one a clean six-bit format/quality bitmask
plus two trailing label-like ids, the other five words not yet
interpreted. Neither table's consumer was found by two tried methods
(full-image word scan, register-arithmetic scan over one module). Full
detail in facts.md F-110.

**Update (2026-10-16), the real module found via a different route
(F-111):** the first table's two trailing words (`0x539`, `0x53b`) led,
via a full-image property-id scan (not a table-address search), to a
real property-driven settings handler at `0x1034e674` that actively
reads and dispatches on a family of related ids (`0x539`-`0x53b`,
`0x540`, `0x544`, `0x548`, `0x1838`, `0x1839`) -- very likely the
firmware's actual image-quality/format setting handler. This is the
closest this research has come to real save-path code since abandoning
the record-builder chain. Three separate methods (full-image word scan,
full-image register-arithmetic scan, full-image `movw`/`movt` pair scan)
still could not find the literal instruction dereferencing either table
address directly -- that specific question is now lower priority than
following the property-id family itself. Full detail in facts.md F-111.

**Update (2026-10-16), the real geometry table found (F-112):** checked
`0x1034e674` directly for image-area property `0x501` -- zero
references anywhere in either of its two address clusters, so that
module is very unlikely to be crop-aware; dropped rather than decoded
further. Instead found every direct reader of `0x501` itself (8 sites,
full-image scan). One, `0x105a7946`, is a real width/height-by-area
lookup: calls `0x1020bfda(quality, area)` twice, reading a `{width,
height}` struct. `0x1020bfda` is a confirmed 2D indexer (quality -> row
pointer -> area-indexed `{i16,i16}` entries), with at least nine
sibling tables of the identical shape immediately following it in ROM
-- almost certainly one per save/display format class.

**The strongest lead this research has found, with one hard limit:**
the table itself is RAM-resident (`0xc18c7de8`), not present in the ROM
image, so its actual width/height numbers cannot be read statically --
live simulator inspection is required to see real values. Separately,
whether the one traced call chain (`0x105a7946` -> `0x10237934`, which
adjusts the value and calls two unidentified helpers shaped like
string/count formatters) is a save-time computation or only a menu
display-label formatter was **not determined** -- say this plainly, do
not assume either answer. Full detail in facts.md F-112.

**Update (2026-10-16), the crop-window builder's own internals decoded
for the first time (F-113):** traced `0x105a7946` -> confirmed it's a
menu-display getter (dropped per the plan above), then pivoted to
finding every caller of the geometry-table function `0x1020bfda`
itself (37 found, full-image scan) rather than one specific wrapper.
One caller, `0x101d5c38`, turned out to sit inside `0x101d5b36` --
**the crop-window builder this whole project has studied since F-057,
whose own body was never decoded until now.**

The builder calls at least six sibling tables from the same confirmed
family (`0x1020bfc8`, `0x1020c05c`, `0x1020c072`, `0x1020c07c`,
`0x1020c128`, `0x1020c17e`) to build three unconditional width/height
pairs plus a conditionally-gated, centered-offset computation -- the
real shape of crop-rectangle construction, not display formatting.
This does not resolve F-097/F-106's capture-vs-estimator ambiguity
(the builder is shared by all seven known callers; nothing here says
which one reaches an actual save versus a live-view/UI preview -- Lane
1's own preview work is exactly the kind of non-save context that would
also need this). It substantially deepens understanding of the tool
itself. Full detail in facts.md F-113.

**Update (2026-10-16), the crop-window descriptor fully resolved
(F-114):** the centering arithmetic is now unambiguous -- top-left
corner, bottom-right corner, their center, and a separate final
output size from F-112's table. The gate function is trivial (an
operating-mode byte must be 0 or 1). This is textbook crop-rectangle
construction, fully understood at the instruction level.

**Dropped, not retried:** checking F-057's seven callers for which one
reaches a real save hit a response-safety-classifier stop. This needs
no new attempt regardless -- F-095/F-096 already characterized all
seven (six display/menu-info builders, one record-builder chain
leaning away from being a save descriptor per F-106), and that read is
unchanged. If this specific question needs pursuing further, hand it
to the owner's own terminal rather than retrying it in a session (the
same handling Lane 1's three-stop pattern used).

**What's left, concretely:** mapping the rest of the
`0x1020bfxx`/`0x1020cxxx` table family (six confirmed in F-113, likely
more); and, since static tracing of "which caller is the save path" is
now deliberately not being pursued, a live simulator read is the
remaining way to test any of this against real behavior -- e.g.
breakpointing `0x101d5b36` during an actual (simulated) capture
attempt and reading the resulting rectangle, or reading F-112's
RAM-resident table directly for the known DX/1:1/16:9 area values. This
is still the fresh thread opened in F-110; do not revisit the retired
record-builder chain (F-095 through F-106) or F-111's `0x1034exxx`
module without new evidence pointing back to either.

**Update (2026-10-17), the live-simulator-read step done for the center
field (F-118):** re-ran F-078's existing, unmodified diagnostic-call
script against the builder, across all 15 area/quality/flag combinations
it already tests. F-114's claim that the `+0xc`/`+0xe` field is the exact
midpoint of the top-left and bottom-right corners is now confirmed by
live execution, not just static algebra, in every single row, including
the degenerate all-zero rows for areas 1 and 3. The `+0x18`/`+0x1a`
final-output-size field's `(0, 0)` pattern is also now fully explained
(a consistent "no resize" sentinel at the large quality byte and at the
`+0x26` flag, across every area) rather than an open detail. **Still
does not touch the caller/save-path question** -- F-095/F-096/F-103's
read stands unchanged; this only strengthens confidence in the geometry
math, which was already high. Full detail in facts.md F-118.

**Update (2026-10-17), F-112's RAM table read directly (F-119):**
answers F-112's own open question -- real width/height values from the
table at `0xc18c7de8`, no diagnostic call needed, just a memory read
after ordinary startup. Three of F-118's non-zero output-size results
match specific table entries exactly, confirming it's the same data
source. **One correction worth flagging before anyone maps the
remaining ~8 sibling tables F-112 found:** the table's (outer, inner)
indices are not simply the builder's own (quality byte, area byte) --
F-118 held quality constant across all three matches but the matching
outer row varied. A rough aspect-family grouping (DX/16:9/1:1 clusters
within the 6-entry rows) is offered as an unproven lead, not a solved
mapping. Full detail in facts.md F-119.

## Lane 3: AE-L/AF-L subject tracking (new section, 2026-10-16)

This lane didn't have its own section here before -- it was tracked only
through `docs/hardware-readiness.md`'s table row and the `docs/tracking-*.md`
files directly. Adding this section now because the owner asked for a
clean handoff point.

**Where this stands relative to the other two lanes:** far behind. Lane 1
has its mechanism fully traced (F-107/F-108) down to one owner judgment
call. Lane 2's capture-vs-estimator ambiguity is resolved (F-106). Lane 3
has **no verified native entry point at all** -- this is still the actual
blocker, not a refinement.

**What's established**, all in `docs/tracking-input-chain.md` (read it in
full; this is only a summary):
- The prior candidate activation lead (`0x11cf4e90`/`0x11cf4ea0`) was
  falsified: it resolves to Bluetooth/HCI packet processing, not AF
  (`docs/tracking-entry-research.md`).
- A queued input-bank route exists for property codes `0x2082`/`0x2083`
  (logical ID 41, mask `0x2000`), traced up through two layers of generic
  event dispatchers (`0x10379a68`, and the `tbb`-dispatched state-machine
  step `0x10379d5a`) to a registration mechanism that remains unresolved
  -- `0x10379d5a` has zero direct callers anywhere in the image by any
  method tried (direct calls, tail branches, raw pointer words, `tbb`/
  `tbh` tables), the same dead-end shape Lane 1 hit and dropped for
  `0x4100012`'s poster.
- **The actually promising lead**: a sibling event-code dispatcher
  (`0x1037aae2`) with codes `0x2006` (touch), `0x2020`, `0x2021`, and
  **`0x2087`** -- four codes from tracking's own `0x2083`. Most of
  `0x2087`'s sub-codes post a simple few-state payload to property
  `0x2021`: a toggle/lock shape, materially more promising than the
  falsified Bluetooth lead, though **not confirmed as AE-L/AF-L**.
- An exhaustive search (module-level, then full-image) for anything that
  *reads* property `0x2021` by direct comparison found **nothing** -- the
  consumer is reached some other way (likely registration-based, matching
  F-106's finding on a different property family), not a literal-value
  dispatch a static text search can find.

**Exact handoff point, two concrete options, neither tried yet:**
1. **Live simulator verification**: breakpoint `0x10475ecc` (the shared
   property-post primitive) for id `0x2021` during ordinary simulated
   navigation, and separately check whether `0x2087` is reachable from
   the simulator's key set at all.
2. **A masked/family-level static search**: check whether any dispatcher
   compares the *high byte* (`0x20`) of incoming ids rather than the
   exact value `0x2021`, the same encoding shape F-104 found for SD
   commands. Requires finding candidate generic property dispatchers
   first -- not attempted this session.

Do not restart from the Bluetooth lead or from `0x10379d5a`'s
registration search -- both are exhausted by direct static method in
`tracking-input-chain.md`. Start from option 1 or 2 above.

**Historical one-button candidate (2026-10-18): native action route validated;
candidate not ready for a camera test.** The
`0x2021` consumer search and simulator post breakpoint are historical; they
did not identify the tracking action. The current first-patch priority is a
single-button Subject tracking action. Static decoding identifies native UI
action enum 77 and a shared configurable-action route, while the AE-L/AF-L
assignment handler omits that enum and rejects logical input ID 13. Thus a
menu-value-only change is not a viable bridge. The proposed private candidate
uses a fresh AE-L/AF-L press edge at the input-record accessor return site
`0x102f14b2`, then routes through native action call sites
`0x103020b4`/`0x10302108`; it preserves stock behavior outside the guarded
context. Protect is a separate SW1 input and playback setting, so its key
icon is not evidence for the AE-L/AF-L route.

The candidate's constructed-context guard/ABI test now passes in the pinned
QEMU (F-212): register/flag and stack preservation, cleanup, and reject
controls for held/release/other-context/other-mode/wrong-owner/consumed cases.
F-213 adds a separate memory-only QEMU diagnostic: the worker task existed
before a native object notification and its saved stack pointer changed after
that notification, but the worker entry/cleanup probes did not fire. This
still does not prove natural key delivery or worker admission through the
hook; no complete modified firmware image exists. F-214 compared the
candidate adapter against the native Fn Subject tracking handler in pinned
QEMU: both reach helper `0x10368b6e` with action 45. F-221 corrects its
request-service attribution: `0x1045a47e` is a boolean gate, and the reported
request tuple at that address is unconfirmed. Action 45 nevertheless
delegates into Nikon's native state-dependent handler. The official manual says the assigned
control starts tracking in Auto-area AF modes and a second press ends it.
QEMU's action object is not modeled, so its state transition cannot be
observed there.

This one-button behavior is no longer the requested first-patch outcome. The
owner now wants tracking always armed in shooting mode, with a persistent
reticle and shutter half-press acquisition. The previous action-45 work stays
useful as the native activation mechanism, but the trigger moves to the
already-researched live-view-ready path; see the owner target update below.

**Update (2026-10-18, F-215): AF-area menu and tracking entry are distinct.**
The AF-area options include Auto-area AF and people/animal variants, but no
selectable 3D-TRACKING row. F-218 clarifies that `0x103edda0` is a text-label
catalog that includes a 3D-TRACKING string; the label-selection case at
`0x103edc2e` is output formatting, not an option or activation callback.
The distinct selectable table at `0x1074a688` maps Auto-area values 600/601/602
to base mode 6 and submode 0/1/2; this establishes eligibility, not activation.
The generic menu OK/J dispatcher invokes the active screen object's registered
callback; the AF-area callback stores a mode selection. Nikon documents subject
tracking as a separate live-view J operation (reticle, then start, then end)
or a control assigned to native Subject tracking. F-214's action-selector
comparison remains evidence that the candidate and native Fn handler both
enter selector 45; F-221 corrects its earlier request-service attribution.
The
F-219 further traces the label-selection case to a status renderer: descriptor
byte `[r4+0x83] == 8` selects the 3D-TRACKING text and sends it to
`0x1027f3cc`; its producer remains unknown. Auto-area selection stores mode
6/submode 0 through `0x1042b2d8` and has no direct Subject-tracking action
call. For J event `0x27e`, filter `0x104e2cbc` first consults runtime
key-to-function lookup `0x10460ba2`, which can invoke a registered callback.
A separate matching screen-context path calls generic input handler
`0x102f1e10`. The handler's direct flow compares input/status state, with no
direct branch to action 45. The callback table is runtime-backed, so an
indirect J-to-action edge remains unresolved; the earlier powered synthetic
QEMU event hit only the dispatcher entry.

**Build decision:** the research supports routing AE-L/AF-L into Nikon's
native Subject-tracking action rather than changing AF-area selection or
adding a new state machine. The private candidate still lacks proven natural
hook admission. F-217 verifies the candidate assembled and linked in memory,
with all 45 planned edits applied to a hash-verified stock
QEMU guest; two calls from a constructed worker context completed, restored
context, and issued the native action request. The 72-byte navigation table
is included at an additional candidate region. This resolves layout
arithmetic and exercises candidate composition, but natural hook admission,
camera-load executable mapping, worst-case stack headroom, full image
acceptance, and the consumer's actual start/cancel transition remain
unverified. No firmware image was written. The next real-firmware trace is
resolving the runtime active-screen J callback and comparing its target with
the native action-45 handler; continue only if it could change the selected
patch hook. Then close executable-mapping and stack-headroom proof and the
candidate-side start/stop test-readiness gap. Do not touch the camera or
publish firmware-derived bytes/artifacts. See Nikon's [focus
manual](https://onlinemanual.nikonimglib.com/z30/en/05-01.html)
and [f2 custom-controls manual](https://onlinemanual.nikonimglib.com/z30/en/09-05-40.html).

**Update (2026-10-18, F-221): action 45 directly consults AF state.** The
state mapper `0x1044dc5a`, called by `0x10368b6e`, snapshots the AF subsystem
and branches on base mode 6, submode, and a state byte. In base mode 6,
submodes 0 and 2 map state bytes 0/2 to internal state 1 and byte 1 to state
0; submode 1 maps byte 0 to state 2 and bytes 1/2 to state 3. Action 45
routes these states to three distinct native helpers. `0x1045a47e` is a
boolean gate, not a request service; the alleged event-post destination
`0x1046296e` is only a return stub. Downstream helper semantics do not yet
identify start versus stop. This gives a direct real-firmware reason to
retain Auto-area AF and route to action 45, but does not verify a tracking
cycle.

**Update (2026-10-18, F-222): downstream helper semantics remain unresolved.**
Plain Auto-area and animal submodes both reach `0x1019596e` with input 0;
people submode dispatches to two shared configuration-state routines,
`0x1007756e` or `0x100775c6`, depending on the mapped AF state. Those paths
mutate internal state but have no decoded start/stop labels. The manual
specifies the expected cycle, but constructed-context QEMU calls cannot
observe the unmodeled AF consumer. The readiness criterion requires one
fresh start, no repeats while held, and a native cancellation on a fresh
second edge; the present simulator evidence does not meet it. Do not call the
candidate testable until natural hook admission, executable mapping, stack
headroom, and that cycle check are resolved or explicitly assigned to a
permitted device test.

**Owner's current operating choice:** keep AF-area mode on Auto-area AF and
map the native Subject-tracking action to AE-L/AF-L. This fixes the manual's
mode precondition and keeps the first patch focused on the button remap; the
`3D-TRACKING` string is not a selectable AF-area row. F-221 further traces
action 45's AF-state-dependent helper routing, but cannot assign start/end
semantics to those helpers. F-222 traces the helper callees: plain/animal
routes converge on one AF state operation, while people mode selects between
two shared state routines. Neither path has start/stop labels. The decisive remaining build question is natural AE-L/AF-L
press admission at the candidate hook `0x102f14b2`, followed by the already
listed camera-load mapping and stack proof. Do not spend more time resolving
the J callback unless new evidence suggests it could replace the validated
action-45 route. The present evidence supports the design choice to delegate
every fresh press to native action 45, but it does not validate the current
candidate's full one-button cycle. Readiness also requires no duplicate while
held and native cancellation on a fresh second edge; constructed-context
QEMU cannot observe the unmodeled consumer. The candidate remains not
testable pending those checks and the hook/build proofs above.

**Correction (2026-10-18, F-223): physical input route is less established
than previously stated.** Reinspection shows `0x103a3f9e` consumes queued
logical-ID/operation records and updates staging word `0xc18c9a68`; it does
not read a live SW-bank word at `0x115c694c`. The logical table maps ID 41 to
mask `0x2000`, while a separate debug naming table labels that mask AEAF_LOCK,
but no reviewed edge proves physical AE-L/AF-L delivery to ID 41 or to the
candidate's input-record accessor hook `0x102f14b2`. Do not describe the physical
detection hook as confirmed. The action-45 comparison is still the best
action-side evidence, but candidate natural admission and all listed
build-readiness gates remain open. The next useful task is to resolve the
candidate hook's exact source fields against a live physical-switch producer
in static firmware code, only if that can affect the candidate trigger. F-224
places `0x102f14b2` at the common exit of record accessor `0x102f1412`: it
unlocks the record mutex, then returns the selected pointer in `r0`. The
accessor returns either a ring record or the separate snapshot record,
depending on mode. It is an accessor-return site, not a copy or physical
button handler. See F-223/F-224 and the correction in
`firmware-map-deep-2026-10-17.md`.

**Update (2026-10-18, F-225): candidate edge fields decoded, source still
open.** The private guard's `0x2000` test at ring-record offsets +4/+8/+12/+16
maps to the first paired-mask difference block created by `0x102f199a`.
After accounting for the block's +4 placement, those conditions describe a
bit present only in the first input, so the predicate is structurally
consistent. This corrects any interpretation that the fields were mutually
exclusive. It still does not establish that either builder input is a
physical AE-L/AF-L sample: the two direct builder callers are `0x1039e1d4`
and `0x1046497e`, while the candidate is evaluated from the live-view
consumer context at `0x102f751c`. Next, trace these inputs back only far
enough to prove or reject physical AE-L/AF-L provenance and whether the
candidate's rising-edge test is valid for that source. Keep Auto-area AF as
the operating precondition and retain native action 45 as the selected
action-side design. No camera access.

**Correction and remap route (2026-10-18, F-226):** the Fn1 configurable
action handler `0x1036957c` accepts setting value 77 and calls native Subject
tracking action `0x10368b6e`; the AE-L/AF-L handler `0x10369468` does not.
Calls at `0x103020b4`/`0x10302108` query handler status and assemble a mask,
so they are not physical-key action hooks. Do not patch those sites as the
remap. The required behavior is still feasible as a design: keep Auto-area AF,
detect a fresh AE-L/AF-L press, and dispatch action 45 so Nikon owns the
toggle. But no verified physical press source or complete test image exists.
Next trace the real AE-L/AF-L action path and determine whether a direct
action bridge or configurable-handler extension is the smaller safe patch;
keep the record accessor candidate on hold until its input provenance is
proven. Do not call this camera-testable yet. See F-226 and
`tracking-input-chain.md`.

**Update (2026-10-18, F-234): stack measurement did not run through the
candidate.** A constructed QEMU canary attempt returned from the adapter but
observed zero native action calls and no candidate/native path. Its one
64-byte canary change is attributable to synthetic call setup, so this is not
stack-depth evidence and the stack gate remains open. The probe did not check
every restoration write; the disposable QEMU process exited and original
image hash and simulator checkout remained unchanged. Next, repair the
constructed action-path setup and require native action entry before using a
watermark; independently trace the candidate task's inherited runtime TTBR0
table and the `0x1002d000` entry. Neither gate is closed and the candidate is
not camera-testable. Keep Auto-area AF with Subject tracking assigned to
AE-L/AF-L; this adds an assignment and does not disable the stock OK/J route.
No camera contact. See F-234 and the last section of `tracking-input-chain.md`.

**Update (2026-10-18, F-235): corrected stack probe now observes the native
path.** Reusing the loaded overlay and validated fresh-edge context, the
candidate dispatched native action 45 once on each fresh edge, zero times on
held/release, and returned with context restored. A 2,048-byte canary below
the constructed action SP changed 1,364 bytes on first-fresh and 1,324 on
second-fresh. The worker TCB reports an 11,264-byte allocation. This is a
bounded constructed-path watermark, not worst-case stack proof: natural
admission, interrupt/scheduler interleavings, and the full AF consumer are not
covered. F-235 corrects the invalid setup in F-234 but does not close stack
headroom. Continue by proving the stack bound for the real worker call chain
and tracing runtime TTBR0 setup for candidate page `0x1002d000`; start/cancel
semantics remain unmodeled. The candidate is still not camera-testable. Keep
Auto-area AF and additive AE-L/AF-L Subject tracking; preserve stock OK/J.
See F-235 and the last section of `tracking-input-chain.md`.

**Update (2026-10-18, F-236): action 45 has a specific AF-state gate.**
Native caller `0x1044dcbe` continues only when mapper `0x1044dc5a` returns 2,
which requires snapshot mode byte `+0x44 == 6`, byte `+0x61 == 1`, and byte
`+0x62 == 0`. QEMU reports state 5 and therefore correctly takes the native
reject path. Accepted state 2 calls helper `0x1045a21c`, which reaches a
stateful routine at `0x100775c6` before referring event code `0x3d` to
return-only stub `0x1046296e`. Static evidence does not label the state or
prove toggle semantics/event delivery. This explains the simulator's failure
more precisely but does not close start/cancel. Next determine whether
`0x100775c6`'s object-state transitions can be identified from its writers and
callers, without extending QEMU fidelity. Runtime executable mapping and
worst-case stack remain open; the candidate is not camera-testable. See F-236.


**Correction (2026-10-18, F-237):** `0x1044dcbe` is a separate caller of the
AF-state mapper, not the principal action-45 selector at `0x10368b6e`. Its
state-2-only route to `0x1045a21c` must not be generalized to all action-45
calls; the main selector routes mapped states 0-3 as F-221/F-222 describe.
QEMU state 5 is rejected, but F-236 did not establish state 2 as the only
accepted action state. For plain Auto-area AF, continue with the semantics of
`0x1019596e` and its AF-related field; also trace the per-button rising edge
around callback `0x102f2eae` as the stronger physical input seam. The
candidate's ring producer remains unproved. No camera-testable patch yet. See
F-237.

**F-228 corrects one F-226 conclusion:** `0x103020b4`/`0x10302108` are in the
same input/action dispatcher family as Fn1's configured handler, which does
call action 45 for setting 77. The combined return mask does not prove this
is only a status query. Keep the shared dispatcher and its AE-L handler in
scope as possible remap seams; trace how its cases are selected from physical
input. The AE-L handler itself still has no action-45 path, and the snapshot
callback still needs an AE-L-specific edge guard. Auto-area AF remains the
intended setup; no camera-testable patch exists.

**F-229 input-map result:** the live-view mask table maps AEAF_LOCK mask
`0x2000` to logical ID 13 and the UI table maps ID 13 to the AE-L/AF-L event
`0x28b`. Snapshot callback `0x102f2eae` tests that same bit and handles the
current AF-ON assignment. This is the strongest static AE-L/AF-L input
boundary so far. The candidate dispatcher also admits logical ID 13, matching
the input map; its paired ring-record producer is still unlinked. Synthetic
QEMU `0x27e` reaches the OK/J generic dispatcher
but no action callback; synthetic `0x28b` also yields no downstream action.
Treat those as simulator limitations. The `3D-TRACKING` string is a status
label, not an AF-area choice. Keep Auto-area AF and target Subject-tracking
action 45 on AE-L/AF-L. The private candidate already adds the verified
“Subject tracking” label to
the AE-L/AF-L assignment list, stores value 77 in `0x1184`, and routes it to
action 45. Treat this as a concrete candidate design, not a camera-validated
menu. Do not discard it for the unresolved ring-record producer alone: the
candidate accepts logical ID 13, which the input table maps to AE-L/AF-L;
physical press admission is assigned to the later device test. The blocker
that still must be closed before that test is candidate-side sequential
fresh/held/release/second-edge action and cleanup control, stack, and image
acceptance. The callback hook at `0x102f2eae` remains an alternate if the
candidate's record path fails, but it needs its own per-button latch and must
preserve AF-ON behavior.

**F-227 advances the hook search:** registered callback `0x102f2eae` reads
the snapshot's `0x2000` AE-L/AF-L bit and, for setting `0x1184 == 9` (AF-ON),
posts event `0x14`. This gives a direct native AE-L route, but the callback
first receives a broad “snapshot changed” result and tests current bit state;
it has no demonstrated per-button rising-edge guard. If reused for action 45,
unrelated input changes during a held AE-L press could retrigger it. Next
trace the callback's current/previous snapshot fields and isolate the
AE-L-specific rising edge. Retain Auto-area AF and native action 45; no
testable overlay yet.

**Update (2026-10-18, F-230): sequential edge/control gate partly passes.**
The private memory-only QEMU probe ran fresh, held, release, fresh in sequence.
Each fresh record produced one completed candidate adapter call to action 45;
held and release produced none. The dispatch-finish cleanup code block and
ABI save/restore cases passed using constructed context. This proves the
candidate's synthetic edge arbitration and native action dispatch, not the
tracking state transition: QEMU's AF consumer remains unmodeled, so second
press cancellation is still unverified. This run also used debugger writes,
not a private overlay, and did not naturally traverse the full context
dispatcher. Do not label the candidate testable yet. Next concrete gates are
private-overlay load without debugger writes, executable mapping at camera
load, worst-case stack headroom, and full-image/layout acceptance; physical
press admission and native start/end outcomes remain assigned to the later
device test under the existing owner disposition. Keep Auto-area AF and the
action-45 remap. No camera access. See F-230 in `facts.md` and the latest
section of `tracking-input-chain.md`.

**Update (2026-10-18, F-231): AF state byte provenance narrowed.** The native
snapshot maps bytes `+0x61/+0x62` from AF context `+0x364/+0x365`; the builder
and mode-dependent subcontext writer are now traced. The state byte comes
from a live AF subcontext field under some branches and is initialized under
others, but it has no decoded tracking-active name and does not identify
start versus cancel. The stock simulator remains unable to validate that
cycle: after invoking native Auto-area setter 600 and confirming base mode 6,
submode 0 and Fn setting 77 by property readback, action 45 still sees mapper
state 5 and never takes an Auto-area helper path. Do not extend simulator
fidelity work. Preserve the native action-45 remap; next build-readiness work
is private-overlay loading without debugger writes, then executable mapping,
stack proof and full-image acceptance. Candidate is still not camera-testable.
See F-231 and the last section of `tracking-input-chain.md`.

**Update (2026-10-18, F-232): LLVM-linked loader overlay exercised.** The
private AE-L/AF-L Subject-tracking candidate now assembles and links using the
installed LLVM tools despite Capstone being unavailable. The link/layout pass
placed 964 code bytes in the planned 1,408-byte space, checked 24
relocations, all 15 hook windows, and 45 edits. QEMU's generic loader loaded
35 merged overlay regions before guest resume; every region was read back
byte-for-byte. The stock firmware hash and simulator checkout remained
unchanged. With the overlay loaded, synthetic fresh/held/release/fresh
records passed edge arbitration and dispatched native action 45 once per
fresh edge, with cleanup and ABI controls passing. This closes the
no-debugger-write overlay-loading gate in QEMU, not camera-load executable
mapping or full native UI dispatch. The AF consumer is still unmodeled, so
start/second-press cancellation remain unverified; physical press is assigned
to the later device test, and worst-case stack headroom is still open. Keep
Auto-area AF and the Subject-tracking assignment on AE-L/AF-L. The candidate
remains not camera-testable. Next, complete a bounded worst-case stack proof
for the candidate worker and assess whether the simulator can check camera
load mapping; do not extend simulator-fidelity work if it cannot. See F-232
and the last section of `tracking-input-chain.md`.

**Correction (2026-10-18, F-233): runtime mapping is still unproved.** The
candidate cave is in the reset table's XN-clear section, but scheduler paths
can install a different TTBR0. In pinned QEMU the candidate task has no
per-task TTBR0 override and inherits the active table. `ATS1CPR` reports its
candidate VA translating outside modeled RAM while the loader-based code
still executes there, exposing a simulator address-map mismatch. Do not treat
the reset descriptor or QEMU's translation output as proof of camera-load
execution. Next, trace the runtime page-table setup used by the tracking task
and identify the `0x1002d000` entry; then complete the stack-headroom proof.
The candidate remains not camera-testable. See F-233 and the last section of
`tracking-input-chain.md`.

**Update (2026-10-18, F-238): corrected rising-edge hook passes a synthetic
QEMU dispatch check.** The shared snapshot updater hook is aligned at
`0x102f0d30`; `0x102f0d32` bisected a 32-bit instruction and was invalid. The
corrected private prototype compares old/new AE-L/AF-L bit `0x2000`, checks
assignment value 77, and calls native action 45 only on a fresh edge. Its
LLVM link audit passes; a private QEMU loader test produced action-45 entry
counts 1/0/0/1 for fresh/held/release/fresh snapshots. The test returned
through a test-only trampoline before the native snapshot-update tail. The
shared updater has seven direct callers, so inline action call context and
stack are not yet established. Next inspect those callers and determine
whether the callback-specific seam at `0x102f2eae` can preserve the rising
edge without executing on unrelated stacks. Keep Auto-area AF and preserve
stock OK/J. This is not a camera-testable patch: physical input, runtime
executable mapping, worst-case stack, native start/cancel, and full-image
acceptance remain open. No camera contact. See F-238.

**Update (2026-10-18, F-239): plain Auto-area action path is stateful but
still unnamed.** Action 45's `0x1045a1ae` helper clears an AF-related field,
then reaches `0x1019596e` through `0x10230832`. The routine writes 6 or 7 to
an AF-related object byte after readiness checks and performs more update
calls. Its event `0x3b` target is the return-only stub `0x1046296e`. Static
evidence does not name the fields or values as Subject-tracking state. The
cycle question remains reserved for behavior testing after build gates. The
immediate research next step is to inspect the seven updater callers for
execution context/stack suitability and compare the common-site hook against
the callback-specific seam. No camera access. See F-239.

**Update (2026-10-18, F-240): common-site stack risk is concrete.** The
paired-record builder `0x102f199a` calls the snapshot updater twice with stack
buffers after reserving `0x31c` bytes. The other wrappers, including registered
callback `0x102f2eae`, have smaller visible frames, but their task stack owners
are not identified. A callback-only hook can miss an edge if another caller
updates the global snapshot first; a common-site action can run on the
builder's deeper stack. Next map caller task identities and stack budgets, or
design a pending-edge handoff to the known action worker. Keep Auto-area AF,
AE-L/AF-L assignment and stock OK/J. The current common-site prototype is not
camera-testable. See F-240.

**Update (2026-10-18, F-241): prioritize the configurable-handler route.**
Dispatcher `0x10301f36` sends function code `0x2d` to Fn1 handler
`0x1036957c`, which calls action 45 for assignment 77. AE-L/AF-L handler
`0x10369468` reads properties `0x1184`/`0x1187` but only handles values 25
and 42. The likely remap point is its handler, with Fn1-handler reuse as a
secondary hypothesis. The dispatcher also assembles a status mask; its
physical-edge cadence and handler argument/return equivalence are unproved.
Next trace its caller and compare those contracts. Do not patch the status
mask call sites. Keep Auto-area AF and stock OK/J. No camera contact. See
F-241.

**Update (2026-10-18, F-242): handler-extension branch passes a synthetic
QEMU test.** A temporary value-77 branch in AE-L/AF-L handler `0x10369468`
reached action 45; assignments 42 and 25 reached their existing branches.
All guest writes were restored and firmware/simulator identities were
unchanged. This proves handler-level feasibility only. The function-code 13
producer, physical fresh-press cadence, held-repeat behavior, native
second-press cancellation, and full-image/runtime mapping/stack gates remain
open. Next trace the handler's runtime registration/producer. Do not return to
the snapshot updater unless the per-button event route requires it. Keep
Auto-area AF, native action 45 and stock OK/J. No camera contact. See F-242.

**Update (2026-10-18, F-243): dispatcher call path narrows the remap
claim.** The only direct dispatcher caller found is callback `0x10302220`;
it forwards only codes 26/27/28, which select other handlers. AE-L/AF-L and
Fn1 are switch entries 13 and 45. No literal dispatcher function pointer was
found, though runtime/computed routes remain possible. F-242 therefore
validates the handler branch only, not button delivery. Next trace callback
registration/producer and indirect dispatch; if code 13 cannot be tied to an
AE-L/AF-L edge, return to the input-chain edge source. Do not treat the
handler extension as testable yet. See F-243.

**Update (2026-10-18, F-244):** a direct synthetic call to callback
`0x102f2eae` timed out before return and produced no action-45 observation.
The constructed record/callback context is unvalidated, so this does not
falsify the natural route. Do not repeat that same call. Next trace the
callback's registration/call context statically and resolve stack/runtime
gates for the common rising-edge hook already tested with synthetic records.
No camera contact. See F-244.

**Update (2026-10-18, F-245):** followed the suggested Auto-area AF → OK/J →
3D-TRACKING path to its actual boundary. The AF-area option setter establishes
mode 6/submode 0; `3D-TRACKING` is only a formatted status label. Shooting-
view J lookup `0x10460ba2` searches a runtime key/callback table and invokes
the selected callback indirectly. The bounded QEMU `0x27e` event did not
reach a callback or action 45. Callback identity remains unresolved, and the
trace does not change the preferred native action-45 remap to AE-L/AF-L.
Retain Auto-area AF. Continue only with a callback-table producer trace if it
can yield a concrete competing action hook; otherwise prioritize the
candidate's runtime mapping/stack and image-acceptance gates. The candidate
remains not camera-testable. See F-245.

**Update (2026-10-18, F-246):** sampled the filter table in the simulator.
It holds three callbacks (`0x104e2e85`, `0x104e2ea1`, `0x104e2ec7`) and one
empty slot; those callback bodies do not directly call action 45. Synthetic
`0x27e` hit only generic dispatcher/screen-handler entries, not the filter,
table callbacks, or action 45. This is a simulator-path limit and does not
identify the camera's physical J callback. No stronger J-side patch hook
emerged; keep action 45 as the remap target. Continue build-readiness work on
the AE-L/AF-L candidate and preserve the open cycle claim. See F-246.

**Update (2026-10-18, F-247):** the combined private production overlay
installs two independent action-45 paths: common snapshot updater hook
`0x102f0d30` calls inline, while ring-record hook `0x102f14b2` queues through
the worker. Their tests were separate; no integrated test rules out two
requests from one press if it reaches both. Drop the common updater action
hook from the test candidate because it also runs in seven caller contexts,
including the deep paired-record builder. Retain the worker-mediated route
as the sole candidate; its physical record provenance is reserved for the
owner's later device test. This resolves the design choice, not readiness:
mapping, full-image acceptance, and hardware-readiness records remain open.
See F-247.

**Update (2026-10-18, F-248):** a local ABI review of the selected
`0x102f14b2` worker hook confirms it restores the stock mutex argument,
returned record pointer, NZCV result, callee-saved registers and SP before
the original unlock/return tail. This closes that insertion's continuation
contract only; it does not change the manifest's incomplete full-candidate
ABI review or the open worst-case stack claim. The worker-only overlay's
`guest_execution: false` manifest field is build-time metadata; F-232/F-235
record its separate loader-based QEMU execution. Remaining candidate gates
are camera-load executable mapping and complete-image acceptance, followed
by the existing owner hardware-readiness process. See F-248.

**Update (2026-10-18, F-249):** one later MMU setup path disables translation,
loads TTBR0 from a literal pointing to RAM at `0xc11f8000`, then reenables
translation. That page table is outside the captured firmware module, so its
entry for candidate code VA `0x1002d000` cannot be statically inspected here.
The scheduler's optional per-task table is another independent path. The
specific worker's inherited camera mapping and executable permission remain
unproved; simulator ATS results cannot supply the missing table. Stop
simulator-mapping work and treat camera-load mapping as an unresolved build
gate unless the owner already has a read-only source for that runtime table.
See F-249.

**Update (2026-10-18, F-250):** no simple relocation cave was found. The
1 MiB sections containing the trigger/action/menu hooks have no all-zero run
of 32 bytes or more, while candidate code needs about 964 bytes. Reusing an
existing nonzero function block would be a separate redesign and ABI/behavior
review. Keep the candidate in its reviewed code cave for now, but leave its
runtime mapping unresolved. Next useful evidence is the runtime TTBR0 entry
for `0x1002d000` from an existing read-only source; otherwise an alternate
placement requires a new design, not more simulator mapping probes. See
F-250.

**Follow-up: runtime mapping access and simulator route (2026-10-18).** The
owner authorized exploring camera connection, but approved rules still
require an exact memory-read method review, recovery plan, and approval of
that method. Existing PTP review found no documented Nikon command that reads
live RAM; identity/property, live-view and card-file reads do not expose
TTBR0 contents, and `gphoto2` is not read-only as shipped. Do not probe with
generic vendor commands. The source map distinguishes the simple
`nikon-z30` profile, whose RAM begins at `0xc1800000`, from the display profile,
whose mapped RAM already includes the TTBR0 table address `0xc11f8000`.
An isolated QEMU 10.2.4 build and read-only guest diagnostic in the display
profile read the active TTBR0 entry for VA `0x1002d000`: it was a valid section
mapping with XN clear, the translation had no fault and its physical page was
inside the modeled map. The diagnostic code ran from the same VA section and
returned with its caller context restored. This sample ran in the diagnostic
task, not a verified tracking-worker context; it narrows but does not close
the worker-specific mapping question or prove camera runtime equivalence.
F-252 attempted a worker-entry capture with a thread-aware wait, but the
simulator did not reach the worker. No repo simulator source changed. The
camera remains gated on a specific reviewed read method and its exact
approval.

**F-252 closes the current worker-context simulator probe:** after the
standard assisted live-view setup, a thread-aware QEMU wait held a breakpoint
at worker entry `0x102f7448` for 20 seconds, but the entry was not reached.
No worker CP15 state or descriptor was captured. This agrees with F-213's
bounded non-hit and is a simulator-scheduling limit, not camera evidence.
Do not spend another session trying to make this same setup schedule the
worker. Resume only with a new, build-relevant real-firmware source for the
runtime descriptor or a specifically reviewed camera-read method; the
existing gphoto2 route remains unapproved and no camera is currently
enumerated over USB. See F-252 and the last section of
`tracking-input-chain.md`.

**F-253 refinement:** the standard diagnostic task's read-only CP15 probe
reports active TTBR0 `0xc2ad4000`, with a valid executable section entry for
`0x1002d000` into modeled display RAM. A watchpoint on that actual entry saw
no write during an eight-second post-setup window. This is distinct from the
later static MMU setup at `0xc11f8000`; neither result establishes the
tracking worker's camera mapping. The worker-entry non-hit remains the
simulator limit. Do not extend this path without a new worker stimulus; the
camera remains pending connection, and any memory read still needs a
specific reviewed method and approval. See F-253.

**F-254 camera-connect preflight:** a local direct-libusb probe is now
implemented at `src/nikon_z30_research/ptp_device_info.py`. Its only PTP
request is standard GetDeviceInfo (`0x1001`, transaction ID zero); it returns
identity and advertised operation codes, omits the serial number, and stops
if it cannot claim the active PTP interface. It does not invoke vendor
operations or retrieve live RAM, so it may identify a firmware-advertised
candidate but cannot itself resolve the worker's TTBR0. Six synthetic tests
pass; the camera was not connected or queried. When it is connected, use only
the command in `docs/camera-readonly-identity-method.md`; review any
advertised unknown operation separately before considering it. Do not resume
the failed simulator scheduling path without a new worker stimulus. See
F-254.

**F-255 host check:** libusb initializes and enumerates successfully, with
zero matching `04b0:0452` devices. The check read USB descriptors only; it
did not open a device or send a PTP operation. The camera remains pending
connection. This confirms host discovery is available, not camera PTP support
or a live-memory path. See F-255.

**F-256 descriptor ABI check:** compared the Python `ctypes` descriptor
structures used by the preflight with the installed libusb C header and
compiler ABI. Sizes and accessed field offsets match for the device,
endpoint, interface, alternate-setting, and configuration descriptors. This
reduces a host-layout risk before the camera is connected; it is not a
hardware transport result. The next step remains the single documented
GetDeviceInfo preflight after the owner connects the camera. Do not resume the
QEMU worker scheduling path without a new stimulus. See F-256.

**F-257 transport mismatch:** after the owner connected the camera,
IORegistry exposed the Z 30 USB identity, but both Python and native C
libusb 1.0.30 enumeration returned zero devices. The exact documented PTP
preflight stopped at its one-device check; it opened no handle and sent no
PTP command. The descriptor's USB release `0x0120` is not a camera firmware
version. Next, resolve why the host registry sees the device while libusb
does not, using only reviewed host-side/read-only methods; do not try
`gphoto2`, vendor operations, or memory reads. See F-257.

**F-258 resolves the identity transport:** after the owner connected the
camera, the documented probe succeeded when run with host USB access. It sent
only standard GetDeviceInfo (`0x1001`) and returned Nikon Corporation, Z 30,
device version V1.20, and the supported-operation list; serial was omitted.
The familiar property, live-view, and card-object families match the bounded
local review. `0x9535` is advertised but unresolved by local references, so
do not invoke it. This proves the identity/inventory route works, not a
live-memory route or the worker's TTBR0. The local-source lookup is now
complete under F-259; do not repeat it absent a newly available source. See
F-258 and F-259.

**F-259 local-source lookup complete:** searched project notes, source and
tests and the installed libgphoto2 PTP documentation/headers for `0x9535` and
candidate runtime-memory operations. No mapping or reviewed memory-read
operation was found. This closes the local lookup branch, not the possibility
of an undocumented interface. Do not invoke `0x9535`. At the time of F-259,
only identity access was approved. The owner has since authorized read/write
experiments in principle and named stock-firmware reinstallation as the
recovery plan; this does not replace the project's exact-method review and
approval requirement for a camera read or write. The identity run therefore
does not resolve the active tracking-worker table. Keep the tracking patch at
its existing NO-GO gates; resume with useful static evidence or a specifically
reviewed camera method. Do not repeat the closed QEMU worker-scheduling trace
without a new stimulus. See F-259 and `camera-readonly-identity-method.md`.

**F-260 native cycle control:** a corrected paused-QEMU diagnostic using the
status record consumed by action 45 routed a fresh decision to native start,
a second fresh decision to native stop, and held/no-decision to neither path.
This verifies the candidate/native request cycle under constructed Auto-area
status; it does not establish that the camera naturally creates that status,
that AE-L/AF-L reaches the candidate, that a subject is acquired, or that
asynchronous completion works. Do not repeat this constructed QEMU test.

The owner has offered human-run testing. First use the stock camera's existing
Fn1 Subject-tracking assignment in Auto-area AF as a reference for the real
native action: record first-press response, tracking acquisition, release and
hold behavior, and whether a fresh second press cancels. This can resolve the
native action's real start/stop behavior; it cannot validate the AE-L/AF-L
candidate hook. Runtime executable mapping remains the major patch gate. Any
direct assistant access beyond the identity query still requires an exact
reviewed method and recovery plan under the camera rules. See F-260.

**Owner-provided recovery plan (2026-10-18):** for a future camera write, the
owner identifies reinstalling stock firmware as the recovery route. This is
recorded as the owner's stated plan, not as a verified recovery procedure;
before any assistant-performed camera write, the exact operation and restore
procedure still need review and explicit step approval.

**F-261 stock-camera result:** owner tested stock Z 30 V1.20 with Fn1 assigned
to Subject tracking. Tap/release and hold both display the tracking target;
it persists after release. A second tap ends tracking; hold behaves like tap.
The owner reports that tracking does not activate until a shutter half-press,
after which the target began following the subject. This establishes
successful native acquisition in the reported scenario, but not AE-L/AF-L
admission to the candidate. See F-261 and `tracking-input-chain.md`.

**Next step:** ask the owner to approve the revised exact monitor procedure in
`camera-ptp-event-monitor-method.md`. It opens one standard PTP session,
listens for 15 seconds, and requests enough transfer space for a complete
event container over the observed 8-byte endpoint. If approved, run the same
bounded button sequence. A no-event result is inconclusive. Do not run the
revised method or another camera operation before approval. It may correlate
physical controls with PTP events but cannot prove the candidate hook.
Runtime executable mapping and physical AE-L/AF-L delivery remain patch gates.

**F-262 connection refresh:** the host USB registry sees the camera and the
pre-approved GetDeviceInfo probe again reports Z 30 V1.20 when run with host
USB access; sandboxed libusb sees no device. The operation list includes
standard OpenSession/CloseSession needed by the event monitor. This confirms
transport readiness only. See F-262 and `camera-readonly-identity-method.md`.

**F-263 event-monitor preflight:** owner approved the exact PTP event monitor,
but its only attempt stopped before opening/claiming the device or sending a
PTP command. The active descriptors did not satisfy the unique default PTP
interface plus interrupt-IN endpoint selector. This is not evidence that no
event endpoint exists; no press test occurred. A separate descriptor-only
inspection is prepared in `camera-usb-descriptor-method.md` and needs separate
approval. Do not retry the monitor or try another interface under the earlier
approval. See F-263.

**F-264 descriptor result and current approval gate:** descriptor-only
inspection found a unique standard PTP interface and an 8-byte interrupt-IN
endpoint. F-263 was a tool threshold bug: it assumed one packet must hold the
entire 12-byte header. The revised monitor requests up to 24 bytes so USB
packets may be collected into one PTP event container. This is a changed
transfer method and requires the owner's exact approval before retry. The
revised monitor has synthetic endpoint tests but no camera run. See F-264.

**F-265 empty-transfer result:** the revised monitor opened the PTP session,
then stopped on a successful zero-byte interrupt-IN transfer before any event
container arrived. Its cleanup path attempted CloseSession; acknowledgement
was not exposed. The same bounded method now treats zero-byte transfers as
idle polls and continues through the 15-second limit. The owner says not to
ask permission again for this same method. Before another run, warn the owner
and wait for an explicit “start” signal. Do not begin the next window until
then. See F-265.

**F-266/F-267 PTP property-event correlation:** two approved bounded monitor
windows completed on the stock camera. With four AE-L/AF-L presses, the first
reported four `DevicePropChanged` (`0x4006`) events for standard property
`0x501c` (`FocusMeteringMode`). With three presses, the second reported two
events for the same property. This is real-camera evidence that the control
sequence coincides with changes/signals for the focus-metering mode, but it
rules out assuming one event per press and does not identify a physical-key
event or prove the firmware hook. Next review offline a single-property,
read-only standard PTP descriptor/current-value query for `0x501c`; use no
vendor operation or write. Do not run it until its exact method and approval
boundary are settled. If repeating the existing event monitor, warn before
the 15-second window and wait for the owner's explicit “start.” See F-266,
F-267, and `tracking-input-chain.md`.

**Owner's latest target:** whenever Auto-area AF is active, Subject tracking
must remain in the native ready/reticle state without a button press, and
shutter half-press should begin acquisition. The lifecycle point was already
researched: selector-1 live-view-ready site `0x102f5810` inside `0x102f57e2`
is reused from the XPan hook work, so do not repeat broad lifecycle discovery.
Its simulator validation covered display-mask behavior, not AF readiness or
action-45 call safety. A view-entry-only hook also misses Auto-area AF being
selected while shooting view is already open. The specific design task is to
reconcile both known transitions—Auto-area selection (`0x1042b2d8`) and
shooting-view readiness—against native tracking state, then issue exactly one
action-45 start request when the condition becomes true. The action is
stateful and a second request can stop tracking (F-260), so a reliable armed-
state check or transition latch must prevent duplicate calls and reset when
the condition ends. Existing research does not establish the live armed-state
signal, setter continuation safety, or AF-ready timing; these are the remaining
gaps. The read-only PTP descriptor query in
`camera-focus-mode-descriptor-method.md` was run once after owner
authorization. The camera returned `0x200A` (`DeviceProp Not Supported`) for
`0x501c`; it did not expose the property's current value or tracking armed
state. Do not retry that standard query or substitute a vendor operation
without a newly reviewed method. Resume with the focused firmware-state and
QEMU candidate proof. See F-260/F-261/F-268 and Lane 3 in
`tracking-input-chain.md`.

**Human-run native-action reference scenario (completed; F-261):** on stock Z 30
V1.20 in still-photo mode, Auto-area AF/AF-C and Fn1 assigned to Subject
tracking, a tap/release displayed a persistent target; hold behaved like tap;
a second tap ended it. The target began following after a shutter half-press.
This tests the native Subject-tracking action on hardware; it does not verify
AE-L/AF-L delivery to the candidate hook or camera-load executable mapping.

**F-269 narrows the 6/7 hypothesis:** those byte values do not directly
classify people versus animals. People submode 1 takes separate configuration
routes; animal submode 2 shares the plain Auto-area path, whose action-45
caller passes input 0 and therefore writes 6. The routine writes 7 only for
input 1. The byte meaning is still unknown. Keep the continuous Auto-area
goal; the next useful firmware trace is to identify the AF object/state that
the common and people-specific helpers modify and whether a native ready-state
signal can support exactly-once arming across both mode selection and
shooting-view readiness. See F-269 in `facts.md` and
`tracking-input-chain.md`.

**F-270/F-271 simulator result and correction:** action 45 (`0x10368b6e`,
selector `0x2d`) routes mapper states 0/1 through `0x1045a1ae` and states 2/3
through `0x1045a21c` -> `0x10230866` -> `0x100775c6`. The earlier
`0x1045a1e6` attribution is corrected: it belongs to selector 27. In the
disposable pinned-QEMU run, supplying initial tuple `(6,0,0)` and explicitly
calling native bridge `0x101925b0` between action calls produced a native
software cycle: first call to the plain helper, bridge to tuple `(6,1,0)`,
second call to `0x100775c6`, bridge back to `(6,0,0)`, then the plain helper
again. This is stronger simulator evidence than the earlier constructed
candidate-only test, but still does not prove natural AF-state production,
visible reticle, or subject acquisition. Next, integrate the status bridge
into a disposable live-view-ready auto-arm overlay and test one-shot behavior
across repeated ready callbacks plus Auto-area changes while view is open.
Keep this QEMU-only; original firmware and QEMU checkout stayed unchanged.
See F-270/F-271.

**F-272 auto-arm test disposition:** a temporary overlay targeted the known
live-view-ready call and Auto-area setter continuation. It included an
Auto-area check, one-shot latch, and the native status bridge. All loader
regions were placed in the disposable guest, but startup halted before live
view on an unmodeled write at `0x10000aaa` from `0xc2b1065a`. The documented
no-lens simulator peer did not resolve it. The overlay never ran; do not cite
this as ABI, readiness, one-shot, reticle, or tracking evidence. Stop the
simulator-fidelity branch. The next build-relevant step is static analysis of
native AF state writers/readers and action-45 call contract to decide whether
a one-shot hook is viable. No patch is testable yet. See F-272.

**F-273 narrows the status guard:** `0x101925b0` has one direct call site,
inside event-driven update routine `0x10076268`, reached directly from
`0x10156ba0` (input 0) and `0x10159092` (input 1). It is not a per-frame
refresh, which explains the stale snapshot in QEMU after action 45. A
candidate must use a reliable one-shot latch or explicitly refresh status
before treating the mapper tuple as an armed-state guard. Next trace the event
routes' relationship to AF readiness and review the exact action-45 call
contract at both known triggers; do not spend more time extending QEMU's
peripheral model. No patch is testable yet. See F-273.

**Correction (F-274):** the F-272 QEMU startup failure was caused by an
undersized verified cave: the 44-byte temporary wrapper crossed a 24-byte
zero span and overwrote firmware. Withdraw the conclusion that an unmodeled
write proves a QEMU peripheral gap. The corrected overlay fits a verified
512-byte zero cave, starts normally, reaches live-view setup, and calls
native action 45 from the ready path; the action's internal return reports
success, followed by the explicit status bridge. The outer live-view callback
still times out in the diagnostic run amid repeated AF-mapper stops. No
reticle, acquisition, or completed callback is established. Next isolate the
callback/worker interaction or drive the ready event through normal guest
execution, then verify exactly-once and mode-transition behavior. Keep the
experiment disposable and simulator-only. See F-274.

**F-275/F-276 identify the corrected test path and stop:** the stock
live-view object's type-2 dispatcher is `0x104b912c([object, 2, 0])`. Through
that route the corrected overlay reaches native action 45 and its successful
return, then QEMU pauses on unknown halfword write `0x10000aaa = 0xaa` from
runtime code `0xc2b1065a`. A private exact-address no-op reveals the next
write `0x10000554 = 0x55` from the same code. These values are consistent
with a NOR-flash unlock sequence, but the device contract is not confirmed.
Do not guess a response or extend the simulator branch. No-op handling does
not complete dispatch; no reticle/acquisition or testable patch exists. The
F-272 run remains invalid because its wrapper overflowed the verified cave;
the same unknown-write family is independently reproduced by the corrected
overlay. See F-274 through F-276.

**F-277 cross-references the stop to F-159:** the captured PC/LR
(`0xc2b1065a`/`0xc2b1013f`) match the shared cached flash identity/geometry
initializer at `0xc2b1012c`. Its information-getter and erase/program callers
are known, but the outer caller and operation in this run are not. The access
is not attributable to tracking or a firmware update. Further flash-response
modeling was retired; return to the tracking action's real-firmware hook/state
contract. See F-159 and F-277.

**F-278 AF-byte cross-check:** the byte written as 6/7 by `0x1019596e` is
also read by `0x1018cd9c`, whose guarded path proceeds only when that byte is
1. This confirms it participates in wider AF state handling but does not
identify 6/7 as people/animal classes or a native ready state. A standard USB
event monitor cannot report this internal field; previous `FocusMeteringMode`
events were not one-per-action and its standard descriptor query was
unsupported. Continue with offline tracing for the native AF-ready signal
and exactly-once auto-arm contract. No camera contact. See F-278.

**F-279 identifies a native state-pair producer:** `0x10078aa0` writes
`(1,0)` to the mapper source pair at `0xc259ff0c+0x38/+0x39`. Its direct
caller is `0x10073ed2` inside an event-driven updater reached from the
`0x100746dc` event-mask dispatcher. The triggering object-state checks are
not yet tied to Auto-area or Subject tracking. Next useful simulator work is
a bounded QEMU test that drives this callback with constructed context and
observes whether the native pair update occurs; this can test a real producer
without modeling the retired flash path. No reticle/acquisition or ready-state
claim follows from the static trace. See F-279 and F-271.

**F-280 corrects the event bit and bounds the QEMU path:** dispatcher
`0x100746dc` selects input bit 0 (`lsls #31`). With synthetic mask 1, QEMU
entered `0x10074492` but returned through `0x100745f4` because the service
check returned 1 and no AF object was present (`r4 == 0`). The mapper source
pair stayed `(0,0)` and the producer was not reached. A valid live AF context
or a guest-driven event after live-view initialization is still needed; do
not infer a hardware or peripheral failure from this diagnostic. See F-280.

**F-281 clarifies the 6/7 field:** the action-45 Auto-area state-0/1 branch
clears the helper input byte before calling the routine that writes 6/7; this
route serves plain Auto-area and animal submode. A different direct caller
passes 1 after checking an AF record byte `+4` is 2 or 3 under additional
configuration/native-helper gates. The alternate record's producer and those
values' meanings are unknown, so a broader AF-category role remains
possible. A standard USB PTP window cannot read that internal record and is
low value for this uncertainty. If continuing this trace, first establish
whether the alternate record producer touches the native ready state or the
auto-arm hook contract; otherwise prioritize that direct hook/state
decision. See F-281 and the last section of `tracking-input-chain.md`.

**F-282 bounds the QEMU AF-context test:** the hash-verified local QEMU run
completed synthetic live-view setup and the native Auto-area setter returned
success for value 600. The following callback still saw service check 1 and
`r4 == 0`, exited before the AF updater, and left source pair `(0,0)`. Thus
live-view setup plus Auto-area selection do not create the required AF object
in this QEMU fixture. Do not model guessed EXMCU/ISP behavior. A next
simulator test is justified only after tracing a native AF-object constructor
or registration path that can populate this context; otherwise this remains a
simulator-only blocker and not evidence of camera-side absence. See F-282.

**F-283 tests the dispatcher's own initialization sequence:** event mask
`0x801` invokes bit-11 initializer `0x10078c50` before bit-0 AF callback
`0x10074492`. In hash-verified QEMU, the callback still found no AF object
after live-view setup and Auto-area selection; service check returned 1 and
the status pair remained `(0,0)`. The initializer alone is not the missing
context. Next trace the producer/registration for the object list consumed by
`0x101885e8`; use a QEMU fixture only if this identifies a native setup path.
This narrows a named auto-arm state test and does not justify guessed device
responses. See F-283.

**F-284 sets the hardware-test threshold:** the owner says QEMU cannot fully
establish readiness and has approved testing a prepared patch on the connected
camera. The private auto-arm overlay now gates on Auto-area base mode 6 and
People/Animal submode 1/2, but the diagnostic QEMU callback did not return
from the wrapper or show the helper/action entry. The run establishes neither
the new gate nor reticle/acquisition behavior. Stop repeating this full
callback test. The candidate remains a loader overlay, has no proven
stills-only guard, and has not been composed/audited as a camera-format
image. The correct point for the bounded camera test is after that exact
candidate exists, its instruction layout/register/stack/return contracts are
reviewed, an independent exact-edit and integrity audit passes, and the stock
recovery path/risk is recorded. At that point use hardware for the native
reticle, half-press acquisition and camera-runtime mapping questions QEMU
cannot settle. Keep the test scoped to still-photo Auto-area People/Animal;
hardware readiness remains NO-GO until the candidate and preflights are
complete. See F-284 and `hardware-readiness.md`.

**F-285 composes and audits the first concrete auto-arm image:** the private
Z 30 C 1.20 standalone EG candidate was built from the hash-verified original
with a four-span plan (the 512-byte code cave plus three same-length hook
branches). The in-repository builder regenerated the native component CRC;
an independent reread verified each expected/replacement span, no unplanned
body change, unchanged length, valid stored CRC and zero residue. Thumb decode
verified branches to the intended three wrappers. Static review found
16-byte-aligned wrappers, callee-saved/LR preservation and native setter
return-value preservation. QEMU still did not observe helper/action entry,
reticle or acquisition; the active trigger’s runtime mapping and worst-case
stack remain camera risks. Nikon's official update instructions use a
camera-formatted SD card with the outer package; the same-firmware Z30 C 1.20
WonderLantern build docs independently document installing a standalone EG.
This exact candidate has not been accepted by the updater. The Z 30 enumerates
over USB at the OS level, but gphoto2 opened no PTP session and no card is
mounted; no transfer or camera write occurred. The next step is to place the
reviewed private EG on the camera-formatted card through a supported card
reader, then run the bounded still-photo People/Animal test under the owner's
existing approval. Do not invent or try an undocumented USB update command.
The hardware-readiness status remains NO-GO until the final named test record
and scope are entered. See F-285 and `hardware-readiness.md`.

**F-286 corrects the transport record and names the risk threshold.** The
historical read-only gphoto2 summary and storage-list calls did open PTP and
reported the removable memory card; F-285's “no PTP session/no card” statement
is stale. The private card-test copy remains local and was never uploaded.
There was no camera write or updater attempt. The candidate and independent
exact-span/CRC audit are complete, but worst-case callback stack/context
headroom is unmeasured and the QEMU callback did not return. The correct
decision point is after a bounded static stack/context review, or an explicit
owner waiver of that named residual, with the recovery risk and bounded test
scope recorded. The current `AGENTS.md` explicitly requires offline analysis
and prohibits camera contact; do not transfer or install the candidate under
that rule. No further simulator-fidelity retry is warranted. See F-286 in
`facts.md` and `hardware-readiness.md`.

**F-287 owner decision and transfer result:** the owner explicitly overrode
the no-camera-contact rule and approved a one-file PTP copy. gphoto2 2.5.32
reported the card root as `/store_00010001`; the upload operation to that path
returned `PTP Specification Of Destination Unsupported`. The initial `/`
attempt also failed before transfer. No file was written and the updater was
not started. No external card-reader volume is mounted on the host. Use a
card reader for any future transfer; the exact candidate stays local. This
does not waive the open worst-case stack/context review or establish updater
acceptance. See F-287 in `facts.md` and `hardware-readiness.md`.

**F-288 still-photo guard trace:** hash-verified decode of `0x102f57e2`
shows the bit-6 test on `0xc181b4b4` only conditionally calls `0x104bd3c0`;
both paths rejoin before the live-view selector setter. This does not provide
a still-photo boundary for auto-arm. The existing candidate is unchanged and
lacks the requested stills-only guard. Next, trace an actual photo/movie
predicate and its writer only if the state/value can be proved to dominate
the reticle-arm path; do not infer the guard from live-view selector 1 or
this unknown global bit. Hardware remains NO-GO. See F-288 in `facts.md` and
`hardware-readiness.md`.

**F-289 mode-entry re-check:** re-inspection of `0x102f2990` repeated F-089's
pointer-table and callback findings but did not identify the dispatcher or
prove still/movie meanings for its inputs. This adds no build evidence; do
not spend another pass re-decoding the same routine. The candidate still
lacks a proven still-photo guard, and the direct APPLV callback's stack/context
bound is unresolved. Candidate unchanged; no firmware edit or camera write;
hardware remains NO-GO. See F-288/F-289 in `facts.md` and `hardware-readiness.md`.

**F-290 APPLV stack request:** the captured creation descriptor for APPLV
requests `0x2000` bytes (8 KiB), forwarded by `0x10219876` to scheduler
creation. This resolves configured size only; current action-45 call depth
from the candidate live-view callback is not bounded. Next, statically bound
the new wrapper/helper frames and native call chain against this allocation,
including indirect calls and error/retry paths, or identify a safe shallower
native dispatch boundary. Do not treat the current candidate as install-ready;
the stills/shooting eligibility and runtime behavior gates also remain open.
See F-290 in `facts.md`.

**F-291 eligibility-byte correction:** `0x102f57fc` tests bit 7 of byte
`0xc181b4b4` (F-288 incorrectly said bit 6). Unrelated subsystems use that
same byte with other bit tests before the same `0x104bd3c0` helper, consistent
with shared instrumentation/filter gating. It is not a defensible
still-photo/Auto-area predicate. Continue searching for a semantically
identified state at the AF-area setter or shooting-state producer; do not
add this byte to the candidate. Candidate remains unchanged and NO-GO. See
F-291 in `facts.md`.

**F-345 Auto-area notification route:** property-batch processor
`0x104579a0` maps base-mode property `0x0c2b` to notification mask
`0x04000000` through `0x104575d0`. F-346 corrects the notification detail:
discriminator `0x56` reaches return stub `0x1046296e`; the actual next edge
sets the mask on a shared event-flag-like handle through `0x10199e04` and
platform primitive `0x10036334`. The waiting consumer and its relationship
to AF-object `+0x40` remain unknown. Next trace initialization of this handle
and its waiters, then compare their update order with registered callback
`0x1016139e`. Candidate 02 remains NO-GO; do not repeat the earlier setter-only
QEMU probe or touch the camera. See F-345/F-346 in `facts.md`.

**F-347 shared-handle initialization:** the mode-3 branch at `0x10595840`
creates three synchronization objects through `0x10462840`, `0x1046285e`,
and `0x1046287c`, storing handles in adjacent slots based at `0xc181e4e4`.
It then registers seven callbacks through `0x101e1c04` (targets include
`0x104650f8` and `0x104bd422`–`0x104bd4da`). Their registration keys and
state effects have not been tied to Auto-area mask `0x04000000`, AF-object
`+0x40`, or snapshot callback `0x1016139e`. There are many unrelated generic
wait-wrapper call sites, and direct xrefs did not identify a unique consumer.
Next inspect the registry's key/data contract and trace only callback targets
whose keys or state flow can connect to the Auto-area notification or AF
snapshot. Do not repeat the setter-only QEMU probe or touch the camera.
Candidate 02 remains NO-GO. See F-347.

**F-348 registry contract:** `0x101e1c04` swaps key and callback arguments
and enters keyed registry `0x101e1b86`. The registry hashes zero-terminated
keys up to 16 bytes, compares existing entries, and stores callback and
auxiliary fields. The seven keys passed by the mode-3 initializer remain
unidentified; the registry's existence alone does not connect those callbacks
to Auto-area mask `0x04000000`. Next map those keys to other dispatch sites or
key producers, then follow a matched callback toward AF-object `+0x40` and
snapshot handler `0x1016139e`. Candidate 02 remains NO-GO. See F-348.

**F-349 snapshot callback filter:** initialization stores the Thumb pointer
for `0x1016139e` in shared callback slot `0xc1885f30`. The related dispatcher
`0x1021dfa0`/`0x1021dee4` can route into the slot, while the handler itself
only snapshots live-view AF context `[r1+0x428]` for event `0x0002fe3d` (the
generic `0x041a0040` branch is rejected). The producer of `0x0002fe3d` and its
ordering relative to Auto-area property/context updates are still unknown.
Trace that producer and compare it with `0x0c2b`/`0x0c3d` and the tracking
ready helper. Do not treat this as a proven hook or repeat setter-only QEMU
work. Candidate 02 remains NO-GO. See F-349.

**F-350 callback source bound:** the two located indirect call sites for
`0x1021dfa0` pass event `0x041a0081`, which is rejected by `0x1016139e` before
the AF snapshot path. A full-image literal search found no occurrence of the
accepted snapshot event `0x0002fe3d`. This bounds the visible static route but
does not exclude runtime-generated or indirect sources. Do not select the
callback as a patch hook from F-349 alone. Pivot to the live AF-context
producer and its order relative to Auto-area property changes; keep Candidate
02 NO-GO. See F-350.

## Rules

Research is offline/simulator-only by default. A camera read beyond the
pre-approved model/version identification requires a specific read method,
review for write paths, a recovery plan, and the owner's approval of that exact
method before use. No unreviewed memory access or firmware-update route.
Any camera write needs separate approval for that exact step and the applicable
readiness gates. Never commit firmware bytes, dumps, or patched images,
anywhere, ever — this applies doubly to
any work on "a safe place to add instructions" (Lane 1), since that
research must stay entirely descriptive (addresses, offsets, constraints)
and never include an actual patch or binary diff. Each PR: fresh branch
from `main`, run the three checks below, one fact per PR where practical,
append-only to `facts.md`. The owner merges everything; you don't merge
your own PRs. Check `project-status.md` for the next free fact number
before choosing your own, since both lanes share one `facts.md`.

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 .github/scripts/check_artifacts.py
python3 .github/scripts/check_byte_dumps.py
```

Private WORK (firmware, pinned simulator, private helper scripts) remains in
the owner's private local storage, outside this repository, and was not
altered by this handoff. If the auto-mode classifier blocks
a read-only firmware scan, the owner can run it in their own terminal and
paste the output back — that unblocked this exact kind of work for Claude
repeatedly this session.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.

**F-353 writer lead:** F-352 corrects the mode source to `*(context + 0) +
0x40`; context `+0x144` is separate. The earlier F-351 object classification
is withdrawn. A concrete writer family at section offsets `0x1d84c28` and
`0x1e0a9f4` sets the pointed object's `+0x40` byte to a table-derived 0/1
after scanning eight entries. Its callers are in an AF-like event-processing
routine, but no Auto-area property or ready-helper link is established. Next
trace the table producer and event/registration semantics; do not patch this
writer as the arm hook. Candidate 02 remains NO-GO. See F-353.

F-355 correction and next trace: withdraw F-354's state-record store
addresses and proposed producer. Section offset `0x1d6ba30` is inside a
ring-buffer helper, and `0x1d6cd6` is unrelated counter/table iteration; they
do not substantiate the claimed `+0x268/+0x26c` writes. Keep F-353's narrower
verified result only: a table-derived boolean is written through the
context-first pointer at `+0x40`, but its table producer is unresolved. The
best next trace is native ready helper `0x1045a1ae`'s direct callers at
section offsets `0x348bc6` and `0x438dfe`. Follow their containing dispatchers
and input sources; these callsites do not yet identify OK, Fn1, or tracking.
Candidate 02 remains NO-GO and the card being formatted does not change that.
No camera or card access under current project rules. See F-355.

F-357 retires the direct ready-helper caller lead as the automatic-arm hook:
one route belongs to configurable-action helpers that query settings
`0x1170`/`0x1141`/`0x1173`/`0x1144`, not the verified AE-L/AF-L setting
`0x1184`; the other is guarded by generic key `0x188c` and record state.
Neither is tied to Auto-area. Return to the Auto-area notification consumer
or a proven AF-context producer, and evaluate the idempotent ready-state path
without toggle action 45. Candidate 02 remains NO-GO. No camera/card access
under current project rules. See F-355–F-357.

F-358 bounded the F-353 table-writer lead through processing routine
`0x1d85b44` and its four direct callers (`0x1d8551a`, `0x1d860c4`,
`0x1d86302`, `0x1d87570`). No reviewed call path locally connects the writer
to Auto-area properties, setter `0x1042b2d8`, or ready helper `0x1045a1ae`.
Stop this branch absent a new cross-reference. Resume from the Auto-area
notification route only through a candidate dispatcher tied to the three
initialized handles; generic waiter enumeration has not identified its
consumer. Candidate 02 remains NO-GO. See F-358.

F-359 identifies the three-handle initializer's seven registrations as GUI
debug/log controls. The Auto-area property-batch path signals the second
handle, but that does not identify an AF-context consumer. Retire this
callback-key/waiter branch. Resume from the Auto-area setter's AF-application
path or another positively identified AF lifecycle callback; do not treat
the shared GUI notification mechanism as the arm hook. Candidate 02 remains
NO-GO. See F-359.
