# Project status

## Lane 3 current build state, 2026-10-19 (F-370)

Candidate 02 remains NO-GO. Setter callsite `0x10430c6c` is within the
explicit AF-area menu-selection routine; it does not provide a stills-view
entry hook. Therefore the setter hook cannot cover Auto-area already active
when the camera enters stills view. The QEMU stills-view fixture does not
install the context or reach the snapshot callback, so do not repeat it.
Continue static tracing for the real AF-application/view-entry path using
verified pointer provenance. No reticle, half-press, or camera behavior is
established. See F-368–F-370 and the Codex handoff.

## Lane 3 current build state, 2026-10-19 (F-369)

Candidate 02 remains NO-GO. F-369's standard pinned-QEMU stills-view setup
never reached callback `0x1016139e` and left status-root pointer
`0xc237c7b4 + 0` null; do not repeat the fixture. A targeted scan found no
simple same-register immediate-6 store to `+0x40`, but loaded/copied and
indirect values remain possible. Continue static pointer-provenance tracing
for the live object and its writer, tying any candidate to Auto-area
application before selecting a patch hook. No reticle, half-press, or camera
behavior is established. See F-369 and the Codex handoff.

## Lane 3 current build state, 2026-10-19 (F-368)

Candidate 02 remains NO-GO. F-368 traced the AF snapshot callback through its
generic queue setup and event dispatcher. The ordinary `0x041a0040` event is
rejected; the callback's accepted `0x0002fe3d` source is still unidentified,
and no direct immediate construction was found. Retire this callback as a
patch hook unless a new producer is found. Next trace the live AF object's
context `+0` installation and mode `+0x40` writer using proven pointer
provenance. No reticle, half-press, or camera behavior is established. See
F-368 and the Codex handoff.

## Lane 3 current build state, 2026-10-19 (F-367)

Candidate 02 remains NO-GO. The setter-hook prototype reached a native state
write but left the sampled live AF context unchanged (F-366). F-367 retires
the status-root `0xc237c7b4 + 0x414/+0x415` accessors as unrelated to the
mode-6 object read by `0x101925ee`; a stock-QEMU InitTask sample also found
status-root `+0` null before simulated stills-view entry. A bounded full-image
scan for context displacement `+0x428` did not identify a unique installer
for the pointer consumed by callback `0x1016139e`. Next trace the owner and
initializer of that callback's event context, then follow context `+0x428`
to its object's `+0x40` mode writer. No reticle, half-press, or camera
behavior is established. See F-367 and the Codex handoff.

## Lane 3 current build state, 2026-10-19 (F-366)

F-361 excludes Auto-area base/submode IDs from the fixed generic property
observer table. F-362 classifies AF-like callback `0x1036c066` as a
configuration reconciler; its `0x1045a47e` call only queries global status
and does not arm tracking. Neither lead selects a patch hook. Continue from
a proven live-context mode writer or native ready-state caller tied to
Auto-area People/Animal. F-363 shows the mode-6 snapshot path in
`0x101925ee` consumes an already-present live-context mode value and only
builds snapshot output. Trace who installs that object at context `+0` and
writes its `+0x40` mode. Candidate 02 remains NO-GO; no install-ready image
or camera behavior is established. F-364 also closes the known
configurable-function callback as an AE-L/AF-L route. F-365 shows the
Auto-area setter is a property boundary and selector 45 is state-dependent,
so neither is yet an auto-arm hook. Next test a disposable QEMU setter-hook
prototype for native state effects and trace the live-context path for
Auto-area already active on view entry. F-366 completed that prototype: it
reaches a native state write for People/Animal encodings but does not update
the sampled live AF context in QEMU. The call was constructed rather than a
natural menu event. Candidate 02 remains NO-GO. Next trace context
creation/update and stills-view entry, then test a valid context-triggered
ready transition. See F-361–F-366 and the Codex handoff.

F-345/F-346 extend the live AF-object trace: property-batch processor
`0x104579a0` maps base-mode property `0x0c2b` to mask `0x04000000`, then sets
that mask on a shared event-flag-like handle. The `0x56` discriminator reaches
a return stub and is not the queued event. The waiting consumer and any
resulting write to live AF-object `+0x40` remain unknown. Trace the handle's
initialization/wait path and compare its consumer order with the registered
snapshot callback. Candidate 02 remains NO-GO; no install-ready image or
camera behavior is established. See F-345/F-346 and the Codex handoff.

F-347 narrows the shared-handle route: the mode-3 initializer creates three
synchronization objects and registers seven callbacks, but their keys and
effects are not yet tied to Auto-area mask `0x04000000`, live AF-object
`+0x40`, or snapshot callback `0x1016139e`. Many generic wait calls prevent a
unique consumer assignment from direct xrefs alone. Next map the registration
keys and callback callers; Candidate 02 remains NO-GO and no install-ready
image exists. See F-347.

F-348 identifies `0x101e1c04` as a keyed callback-registration wrapper. Its
registry hashes short zero-terminated keys and stores callback and auxiliary
fields. The seven initializer keys have not been named or matched to the
Auto-area notification. Next map those keys to dispatch sites and AF-object
updates; Candidate 02 remains NO-GO. See F-348.

F-349 links registered callback `0x1016139e` to the snapshot of live-view AF
context: its filter accepts event `0x0002fe3d` and excludes the generic
`0x041a0040` path. The producer of `0x0002fe3d` is unknown, so this is not yet
an Auto-area hook. Trace that event's source and ordering against AF-context
updates; Candidate 02 remains NO-GO. See F-349.

F-350 bounds the visible callback source: located callers of `0x1021dfa0`
pass `0x041a0081`, which the AF snapshot handler rejects, and the accepted
snapshot event `0x0002fe3d` has no literal occurrence in the image. This path
does not identify the Auto-area update or a patch hook. Pivot to the live
AF-context producer/event order; Candidate 02 remains NO-GO. See F-350.

F-353: mode source is `*(context + 0) + 0x40`; a writer family at
`0x1d84c28`/`0x1e0a9f4` sets a table-derived boolean there. No Auto-area or
ready-helper connection is established. Trace table producer and event
registration semantics; do not patch this as arm hook. Candidate 02 remains
NO-GO. F-355 withdraws F-354's store-site/provenance claims: `0x1d6ba30` is
inside a ring-buffer helper and `0x1d6cd6` is unrelated iteration. Keep only
F-353's verified table-derived boolean writer; its producer is unresolved.
Resume from direct ready-helper callers at section offsets `0x348bc6` and
`0x438dfe`, tracing their dispatch/input sources before assigning semantics.
F-357 shows neither direct ready-helper caller is tied to Auto-area: one is a
configurable-action route reading settings other than the verified AE-L/AF-L
setting `0x1184`; the other is guarded by generic key `0x188c` and record
state. Resume from the Auto-area notification consumer or a proven AF-context
producer, checking for an idempotent ready-state entry separate from toggle
action 45. Do not access the camera or card under current project rules. See
F-355–F-357.

F-358 follows the table-derived writer through `0x1d85b44` and its four
direct callers; the bounded paths do not connect it to Auto-area properties,
setter `0x1042b2d8`, or ready helper `0x1045a1ae`. Stop that branch. Resume
from the Auto-area notification route only through a candidate dispatcher
tied to the three initialized handles; generic wait-wrapper enumeration has
not identified the consumer. Candidate 02 remains NO-GO. See F-358.

F-359 identifies the three-handle initializer's registered callbacks as GUI
debug/log controls. Auto-area changes signal its second handle, but this
shared GUI/property notification does not establish an AF-context consumer.
Retire the callback-key/waiter branch; trace the AF-application path from
setter `0x1042b2d8` or another positively identified AF lifecycle callback.
Candidate 02 remains NO-GO. See F-359.

F-360 rules out generic property-cache handler `0x1008955c` as a demonstrated
AF-application hook: it updates a cached property record, with no proven
registration or local AF ready/context effect. Continue by resolving the
observer target for `0x0c2b`/`0x0c3d` or the AF-application callback after
setter `0x1042b2d8`. Candidate 02 remains NO-GO; do not access the camera/card.
See F-360.

F-340 shows the property setter synchronously dispatches runtime observers
before returning, so a post-setter hook could observe callback side effects.
The observers for `0x0c2b`/`0x0c3d` and their connection to live AF-object
`+0x40` are unresolved. Trace their registration/resolution and field writer;
Candidate 02 remains NO-GO. See F-340.

F-341's setter-only QEMU probe saw both property IDs enter the observer
dispatcher but no indirect listener/resolver in the shooting-view fixture.
This is simulator-only and does not establish real-camera registration. Next
inspect static observer initialization and the live field writer; Candidate
02 remains NO-GO. See F-341.

F-342 confirms neither direct Auto-area setter caller writes AF-object `+0x40`
or invokes a ready/action helper afterward. The setter is a property boundary,
not a proven arm hook. Trace the live-field writer and timing; Candidate 02
remains NO-GO. See F-342.

F-343 rules out a static Auto-area property reader as the field producer:
`0x10489832` only maps mode/submode values to menu labels and UI updates.
The AF-object mode-byte writer and its event ordering remain unresolved; trace
the object's lifecycle/registration next. Candidate 02 remains NO-GO. See
F-343.

F-344 identifies the snapshot builder's only direct caller as registered
handler `0x1016139e`; it snapshots the live-view context, then reads AF fields
including `+0x40`, with no write to that field in the reviewed path. The
handler's dispatcher, event meaning, and upstream AF-object producer remain
open. Candidate 02 remains NO-GO. See F-344.

F-326 supersedes the F-323 unknown-subscriber statement below: stock pinned
QEMU sampled one stable listener callback target (`0x1022adee`), and the
static action-45 selector-3 branch broadcasts event `0xB5` to the listener
table. F-327 exercised that selector-to-listener path in stock QEMU with a
constructed event; the listener returned, with 176 bytes between handler
entry and the lowest sampled SP. Its conditional nested callback was not
enabled in the ordinary startup state. This is not a worst-case stack bound
for the candidate's APPLV execution context. Candidate 02 remains NO-GO with
reticle and half-press behavior unverified. Do not repeat the timed-out full
candidate callback run. F-328 corrects the QEMU callback interpretation:
`0x101885e8` pops a generic linked-list entry, so `r4 == 0` means the work
queue was empty, not that an AF object was missing. Drop the proposed AF
object-constructor search and pursue the direct AF-ready/reticle hook; inspect
the queue producer only if it could change that hook decision.

F-329 confirms that native Auto-area setter values 601/602 read back as
People/Animal submodes, but the stock QEMU action mapper remains at reject
state 5 even with its separate boolean gate synthetically enabled. Ordinary
simulated AF-area selection does not populate the action's copied AF context.
Do not repeat that QEMU setup; trace the real AF source-pair producer or a
direct ready-state hook. Candidate 02 remains NO-GO; reticle/acquisition are
unverified.

Candidate 01 was the diagnostic source and omitted the native AF status-copy
bridge after action 45. Candidate 02 privately adds that bridge after a
successful native action and passes exact-edit/CRC and hook-target checks.
Its focused QEMU call timed out without usable observations; it has not been
copied to the SD card or accepted by the updater. The prior no-Update result
is for candidate 01's card state, not evidence about candidate 02. Neither
candidate is camera-test ready. F-311 confirms the bridge ABI. F-313 corrects
F-312: the action path passes a zeroed pair, skips the first indirect callback
and continues into state-dependent event dispatch when shared mask word
`0xc18a7540` is zero. F-314 maps helpers that set and clear its bits, but the
camera-time mask remains unknown. F-315 follows an action-45 state-handler
branch to the gated dispatcher; neither it nor its observed callers mutate
the mask, leaving its value unresolved. This is separate from candidate 02's
status-copy bridge synchronization path.
F-316 found 103 direct call sites to 70 routines in the event body. F-317
bounds the status-copy bridge's visible SVC wrapper frames to 8 bytes each,
while SVC internals remain outside that bound. F-322 corrects F-321's
callback target to `0x10064a9a`, whose selector-3 branch reaches a runtime
listener broadcast in `0x100660f2`. F-323 locates its dynamic listener count
and function-pointer list at `0xc18a74d5` and `0xc18a7520`; subscriber target
stacks remain unknown. Candidate 02 is NO-GO. Trace the listener-list
producer once, then pivot to the AF-ready/reticle hook if it remains dynamic.
See
F-285/F-305/F-311/F-312/F-313/F-314/F-315/F-316/F-317/F-318/F-319/F-320/F-321/F-322/F-323 and
`handoff-codex.md`.

F-298 maps the scanner's static outcome: a matched standalone file must parse
successfully before the scanner returns its accepted-file status; no match or
parser rejection takes a different return path. The menu wrapper branches on
that status. Runtime camera branch and visible UI mapping remain unknown.

F-299 maps the callback's fallback path. F-306 through F-308 correct the
accepted path: it skips the fallback message, fills a menu-like record through
helper `0x102342a6`, then routes status values 1, 2, 4, and 8 separately.
F-309 locates the callback in a five-entry property callback table, but its
dispatcher is unknown. The menu meaning remains untraced; the owner confirms
no Update option.

F-300 maps the pre-parser scan: media-state bits select a directory path and
the updater enumerates entries against the standalone filename pattern. The
camera's actual match result remains unknown.
F-302 narrows the path values to runtime RAM pointers, and F-303 confirms the
canonical `EG209020.BIN` filename matches the standalone discovery pattern.
F-304 closes root selection by owner report, while F-305 confirms no Update is
offered for candidate 01's card state. F-306 through F-309 trace this post-scan
path but do not map its result to a visible menu action; do not repeat without
new evidence.

## Lane 3 updater eligibility follow-up, 2026-10-18 (F-293)

Upstream Wonder Lantern documents installing its standalone Z 30 C 1.20 EG
on a C 1.20 camera. This weakens the hypothesis that the base camera/module
version alone explains our candidate's missing Update option; it does not
validate our image or show whether upstream changed its version metadata.
F-295/F-296 later found no same-version rejection in our standalone parser or
type-2 post-CRC path, superseding the proposed metadata comparison. F-298
maps the scanner's result handling; the camera-side discovery result remains
unknown. See F-293 through F-298 and `handoff-codex.md`.

F-296 finds no same-version rejection in the standalone parser or type-2
post-CRC route. The parser reads/formats `0x24` without gating success on the
formatter result, and the candidate preserves its four-byte compatibility
field at `0x10`. The missing Update option points to card discovery/UI
eligibility or another untraced gate. Verify camera-format and fresh
power-cycle conditions, then trace the scanner/UI return if needed.

## Lane 3 updater rejection, 2026-10-18 (F-292)

The owner says the camera is never used for movies. Movie behavior and a
still/movie exclusion guard are outside the feature requirements; the target
is still-photo Auto-area AF People/Animal auto-arm, visible reticle, and
half-press acquisition. This supersedes F-288/F-289 only as an acceptance
blocker. The owner approved a bounded real-camera patch test and accepted the
candidate's remaining runtime-mapping and stack/context risks. The candidate
and SD-card copy were verified to match in filename, size (33,939,514 bytes)
and SHA-256 (`6a31dc39264fa73459d68605f9ce3a1f69c9017de4f2c99f980c7bdfe6fc52de`).
The Firmware version screen offered only Done and Delete firmware update
files, with no Update option. No update began. The card copy is sound, but
this candidate is not installable as presented. Its unchanged C 1.20
module-version metadata makes same-version rejection plausible, not proven.
Do not rename it or bypass updater eligibility. Continue with offline
eligibility research. This does not ready the XPan or combined build; see
`hardware-readiness.md` and the latest Lane 3 note in `handoff-codex.md`.

## Lane 3 PTP transfer result, 2026-10-18 (F-287)

The owner overrode the current no-camera-contact prohibition and approved one
candidate-to-card PTP copy. gphoto2 2.5.32 identified the camera card root,
then the device rejected upload as unsupported. No file transfer or updater
attempt occurred. No card-reader volume is mounted. A card reader is the
remaining practical transfer path. The candidate remains local; worst-case
callback stack/context and test readiness remain unresolved. Hardware stays
NO-GO. See F-287 and `hardware-readiness.md`.

## Lane 3 still-photo eligibility, 2026-10-18 (F-288)

Static decode of the candidate's live-view hook found no still-photo gate:
the nearby bit test only conditionally calls a helper, then rejoins before
the common selector setter. The candidate is unchanged and cannot yet meet
the requested stills-mode behavior. Continue tracing a native photo/movie
state only if the state value and its dominance over the arm path can be
proved. Hardware stays NO-GO; see F-288 and `hardware-readiness.md`.

## Lane 3 mode-entry trace re-check, 2026-10-18 (F-289)

Re-inspection of `0x102f2990` repeats F-089's callback and pointer-table
findings but does not identify the dispatcher or map its inputs to stills or
movie. It adds no build evidence and is not a usable guard. The candidate is
unchanged; hardware stays NO-GO. See F-288 and F-289.

## Lane 3 APPLV stack request, 2026-10-18 (F-290)

The APPLV creation descriptor requests an 8 KiB stack and the native wrapper
forwards that value to the scheduler. Candidate/native peak depth remains
unbounded, so this narrows but does not close the stack-safety gate. Hardware
stays NO-GO. See F-290.

## Lane 3 live-view byte correction, 2026-10-18 (F-291)

F-288 misidentified the tested bit: the handler tests bit 7 of
`0xc181b4b4`. Cross-subsystem use points to an instrumentation/filter gate,
not a stills/Auto-area state. It cannot guard this patch. Readiness remains
NO-GO; see F-291.

## Lane 3 risk threshold, 2026-10-18 (F-286)

Corrects F-285's stale USB status: historical read-only gphoto2 PTP summary
and storage listing succeeded and identified removable-card storage. The
private candidate is staged only in a local temporary folder; there was no
upload or camera write. Candidate construction and exact-edit/CRC audit are
complete, but callback stack/context headroom and modified-callback completion
remain open. Keep hardware NO-GO until those are resolved or the owner
explicitly waives the named residual, the recovery risk and test scope are
recorded, and the exact-step approval requirements are met. The current
AGENTS.md prohibits camera contact, so no hardware step is authorized by this
record. See F-286 and `hardware-readiness.md`.

## Lane 3 candidate update, 2026-10-18 (F-285)

A private Z 30 C 1.20 standalone EG auto-arm candidate has now been composed
and independently exact-span/CRC audited. Its three Thumb hook branches
target the reviewed wrappers; static review covers saved registers, aligned
frames and original setter return values. This closes candidate construction
and exact-edit audit, not runtime mapping, worst-case callback stack, updater
acceptance, reticle or acquisition. The owner has authorized patch testing and
directed that QEMU cannot fully establish readiness. The camera enumerates at
USB level, but no PTP session or card mount is available; Nikon's official
update flow is SD-card based, and this exact standalone EG has not yet been
accepted by the updater. Hardware remains NO-GO pending a supported card
transfer path and a concrete bounded test record. See F-285 and Lane 3 in
`handoff-codex.md`.

## Lane 3 hardware-test decision, 2026-10-18 (F-284)

The owner says QEMU cannot fully establish readiness and approves testing a
prepared patch on the connected camera. This supports a bounded camera test
once a concrete candidate passes preflight; it does not make the current
overlay testable. The private candidate is not yet a camera-format image,
the exact edit/integrity audit and code-contract review are incomplete, and
the live-view hook lacks a proven stills-only guard. Hardware remains NO-GO
until those items and the recovery record are complete. Then test the native
reticle, half-press acquisition and runtime mapping on the camera instead of
extending QEMU's full-callback path. See F-284 and Lane 3 in
`handoff-codex.md`.

## Engineering route update, 2026-10-17

F-191/F-192 establish that the public 65:24 profile is not a drop-in: it uses
area 2, persisted profile state and a grid rather than our area-4 replacement
of 1:1 plus black bars. F-198 records a private 176-span standalone-EG
candidate and an independent byte-level audit. Four area-4 preview-table
entries set slot 4 to 480x176 and 1080x400; other slots, strides, thumbnail,
headers and metadata are preserved. The candidate and manifest remain in
owner-only storage outside Git; audit details are in
[handoff-codex.md](handoff-codex.md) and [facts.md](facts.md). The accepted
still-guard waiver leaves playback/movie/warning effects unmeasured. Lifecycle
condition 1 remains unmet, native updater acceptance is unproven, and camera
access remains NO-GO.

F-201 records the owner's reaffirmation that the XPan still-photo guard remains
waived despite the capture path not being proven specific to new stills. The
accepted playback/movie/warning effects remain unmeasured; lifecycle condition
1 stays unmet and the decision grants no camera-write authorization.

F-204 finds neither a new-still-exclusive hook nor proof that playback/editor
outputs are unchanged. The candidate's shared area-4 tables may affect still
previews, playback/editor object paths, and the already-waived movie/warning
contexts. The owner directs keeping the waiver as scoped, excluding editor
outputs; no capture-hook investigation or candidate build is planned.
Hardware remains NO-GO under unmet lifecycle condition 1.

F-205 records the owner's narrower requirement that future preview changes be
still-capture-only and leave playback/editor unchanged. The four named caller
contexts still have no proven capture-origin gate: one is a dimension-based
factory, two rebuild existing objects, and one refreshes an existing object.
The upstream bit-20 event semantics remain unresolved. Do not build or advance
hardware readiness until a gate and its playback/editor exclusion are proved.

F-206 bounds the current static trace: no further producer/key or record-
provenance decode exists in repository evidence. The F-198 table-only artifact
changes shared area-4 slot values and cannot meet the owner's newer
playback/editor exclusion requirement. Keep preview patch work blocked until
the missing edges are available in an owner-authorized static decode.

F-207 identifies the callback's generic runtime registry label as `BACKEND`;
the bounded assisted-startup probe saw one callback with flags `0x10`, not bit
20. The callback is not a proven capture-only hook. The bit-20
producer/meaning and record provenance remain unresolved; keep the still-only
preview patch blocked.

F-208 identifies bit 20 as the current-object assignment event posted by
`0x10220fd6` after filling the shared slot. Its two bounded direct callers
have no decoded still-capture predicate; one is a generic backend worker.
Therefore this event is not a safe still-only hook, and playback/editor
exclusion remains unproved.

F-209 traces queued bit 24 through descriptor builder `0x103e5bdc` to the
same setter and links its notifier to shared helper `0x1055f834`, which has
multiple state-management and cleanup callers and no capture predicate. This
further disfavors the event as a still-only hook. F-210's bounded stock-QEMU
startup/navigation run did not exercise the path; that is only a simulator
limit and does not establish real-camera unreachability. Keep preview work
blocked until a new-still caller and playback/editor exclusion are proven.

F-211 traces the other direct setter caller to shared routine `0x10156714`,
which gates on shared table counters and then walks backend descriptors without
a visible capture predicate. No direct static inbound caller was found, and
the bounded simulator run did not hit it. Its inbound dispatch and table
semantics remain unresolved; it does not establish a capture-only hook.

F-200 checked the existing pinned-QEMU path with the exact private candidate.
Both its launcher and C machine loader enforce the stock firmware hash, so the
candidate is rejected before emulation. The simulator was not modified. Treat
this as a closed simulator limitation; it does not invalidate the audited
standalone-EG candidate or establish native updater acceptance. Hardware
remains NO-GO.

## Codex resumed build work, 2026-10-17

The owner directed Codex to continue this work rather than hand it to Claude.
The private standalone-EG architecture is recorded in
[native-xpan-build-architecture.md](native-xpan-build-architecture.md). F-198
emits a candidate with the exact original gate, reviewed manifest and private
writer; the independent audit verifies exact listed spans, no unplanned
changes beyond the native CRC trailer, length/capacity, protected fields and
area-4 table layout. F-166 establishes the `0x2940000` parser capacity and
preservation of offset `0x10`; F-165 validates crop descriptors with synthetic
guest RAM. The artifact is testable offline but not camera-ready. Lifecycle
condition 1 remains unmet; no camera access or write is authorized.

### Historical research before the F-198 candidate

The notes in this section record earlier intermediate findings; the current
candidate scope and remaining gates are summarized above.

F-170 executed all three direct preview-buffer constructors synthetically.
F-198 changes only area-4 slot 4 in the getter and direct-buffer tables;
non-target slots and both stride tables pass an independent unchanged-byte
audit. Playback/movie/warning effects remain accepted but unmeasured.
F-171 further shows the `0x10142d86` wrapper has direct preview/object-rebuild
callers of unproved capture role, so an area-4 test alone is insufficient.
At that point, capture-caller discrimination and stock generic/playback
behavior were still hook requirements; F-198 superseded that hook design
with the accepted table-only candidate.
F-172 rejects the full adjacent zero run as a cave; a smaller 1,642-byte
subspan is only a candidate pending address-use and executable-layout review.
The previous capture-hook and code-location research is superseded for this
data-only candidate by the owner's still-photo-guard waiver. Lifecycle and
native updater acceptance remain unresolved.
F-173 traces several wrappers into existing-record object constructors, but
none proves a capture-only route. The design now evaluates a minimal native
EG-tail payload plus a local veneer, based on the same-version upstream build
pattern; loaded extent and branch/ABI contracts remain unverified.
F-174 confirms candidate 4-byte patch windows are within BL reach of the
nearby zero subspan and validates a register-preserving literal veneer in a
synthetic assembly check. It does not clear that subspan as executable.
F-175 bounds a minimal append at `0x1207e038` before the CRC, within the known
native destination span; executable mapping remains to be checked.
F-176 completes the localized text-span map in a private text-only manifest;
this does not create or validate a candidate.
F-177 rules out the `0x1021e7a8` caller path as a capture guard because it
attaches or reuses existing record-linked preview objects. Exact capture
caller discrimination remains the first build blocker.
F-178 consolidates the localized text and proposed area-4 geometry into a
private 160-span exact data manifest; it remains incomplete and is not a
firmware candidate. F-179 leaves the type-`0x24` registration dispatch
unresolved after bounded direct-reference sweeps.
F-180 follows the native image-record builder to two existing-object
materialization/refresh routes and rejects it as a capture hook until record
provenance is proved. Next, trace the source of a newly captured still into
the builder or identify a per-record capture-origin field; do not patch the
shared lifecycle path based on area/selector alone.
F-181 verifies the original EG CRC-16/XMODEM trailer and adds a synthetic-only
in-memory composer/auditor. Ten tests pass; it has not been run on firmware,
and it does not close the preview hook or metadata policy.
F-182 runs the composer against the verified original and current private
160-span data manifest in memory; exact spans, length and CRC pass. The
incomplete output was discarded. No feature candidate exists.
F-183 adds the complete-plan parser gate and 14 synthetic tests; its status
marker does not itself prove semantic review. F-184 traces the dimension-
based preview adapter to object creation/attachment, but leaves its dispatch
and still-capture provenance unresolved. Neither finding approves a hook or
candidate. Continue with actual still-capture producer tracing and close the
offset-0x24 metadata policy.
F-185 adds a private writer requiring the reviewed manifest hash and exact
source gate, with out-of-repository paths, no-overwrite behavior, and a full
read-back audit. Four synthetic filesystem tests pass; 148 tests pass across
the suite. F-186 verifies output file mode `0600`. No real candidate was
written. F-188 narrows metadata handling to post-CRC, selector-based policy
callbacks; the standalone callback and version-comparison semantics remain
unresolved, so preserve offset `0x24` exactly.
F-189 adds the exact 12-span F-148 bars overlay to the private data manifest.
All 172 spans pass exact in-memory composition and CRC/length audit; temporary
output was discarded. Capture-preview hook edits are still missing.

## Historical project and merge checkpoints

The following checkpoints are retained for context and are superseded by the
current engineering summary at the top of this file.

### PR #155 review checkpoint

Lane 0 F-127 verifies task creation and passive worker execution. Main conflicts
are reconciled without rewriting merged facts. See native-worker-scheduling.md
and native-lane-gap-review.md; their old next steps are historical. Saved-file
correctness is an on-camera test item. Current owner waivers and hardware
NO-GO remain as recorded in session-manager-brief.md. No new runtime test.

Owner direction: [owner-direction-2026-10-17.md](owner-direction-2026-10-17.md).
The saved-crop question is an on-camera test item, not a blocker for feature
work. Hardware remains NO-GO.
Latest scope clarification: XPan simulator work stays focused on stills;
movie-transition/predicate evidence is not a blocker. Movie behavior is
unvalidated. Still-photo ABI and lifecycle requirements remain applicable.
Patch work is governed by [patch-readiness-checklist.md](patch-readiness-checklist.md);
do not begin another patch loop until its required inputs are explicit.

Updated 2026-10-17 by Codex. Read [handoff-codex.md](handoff-codex.md) for
the current integration map and next step. Older paused-lane notes are stale.

Owner disposition for tracking: simulator cannot supply the physical
AE-L/AF-L press, so press-to-start/stop behavior is assigned to the later
tracking-patch device test. The private tracking manifest/source are verified
against the extracted original, but no image exists. The standalone-EG
format/integrity contract remains open; hardware is NO-GO. The prescribed
first modified test remains XPan, then tracking alone, then combined.

### Earlier open-work checkpoints

F-163 resolves the native format split: standalone EG discovery type 2 is
checked by the native CRC path and bypasses the unresolved body-package
digest selected for type 4. This makes standalone EG the preferred build
format; it does not prove a candidate accepted by the camera. F-166 closes
the numeric file capacity and direct compatibility-field rule. The complete
XPan edit manifest still needs preview hooks and geometry edits, plus the
offset-0x24 metadata/version disposition. F-176 supplies the private 144-span
localized label/size text manifest. F-165 validates the proposed
crop values and output sizes through the native full builder. See
[native route decision](native-standalone-eg-route.md). No firmware candidate
was built or encoded.

F-162 resolves the scoped large-size geometry question: bounds
`(8,8,5208,1928)` are exactly 5200x1920. Native arithmetic and both original
probe reports agree; 256 synthetic arithmetic cases pass. Group 3/index 19
provides rectangle dimensions; indices 4/14 alone cannot exercise that field.
See [exact contract](native-xpan-5200-contract.md). No new simulator, firmware
encoding, saved-file research, tracking work or camera access. Complete
artifact integrity, label and preview contracts remain open.
PR #170 merged at 5c68bea and #155 at 71133cd under the owner's explicit
override; exact merged main passes 130 tests and required scanners/diff checks.
This geometry follow-up is local/uncommitted, with no new PR authorization.

Owner-authorized merges: PR #170 merged at 5c68bea; PR #155 is reconciled
against it and awaits passing updated CI before the separately authorized
merge. This owner instruction explicitly overrides the earlier self-merge
restriction for these two PRs only. No other merge or hardware authorized.
No complete camera firmware artifact exists: private bars overlays and a
private tracking object/in-memory candidate are components, not installable
builds. Primary blocker: validate the native output format/integrity contract
(outer digest unresolved; standalone EG review incomplete), then finish the
XPan crop/label/preview edit contract and exact-artifact checks. No new
address-decoding research, build or firmware encoding in this merge task.

Owner review: [PR #155](https://github.com/tokim25/nikon-z30-research/pull/155)
updated at e655f5d, conflict-free with passing CI; preflight/handoff
[PR #170](https://github.com/tokim25/nikon-z30-research/pull/170) contains the
reconciled research and synthetic digest verifier. Neither PR was merged.
Primary local suite: 130 passing tests; scanners/lane/diff checks pass.
Unrelated owner-rule addition remains uncommitted and preserved. No hardware,
firmware build/encoding or expanded research in this publication task.

Publication reconciliation against main 512e6b3: preserve merged F-135--F-155;
renumber only our six unmerged findings to F-156--F-161. Later owner waivers
for lifecycle, still-photo guard and byte-exact installed identity are recorded
in session-manager-brief.md and test-readiness-2026-10-17.md. Earlier retained-
gate statements below are historical. No waiver is hardware approval or proof
of measured behavior; modified firmware remains NO-GO.

Owner-requested pause/handoff to Claude: see
[consolidated session/permissions packet](native-claude-build-research-handoff.md).
Includes tracking's separate candidate review and observed stack-allocation
increment; no installable tracking image or natural activation accepted.
Publication is now owner-authorized for review; no hardware authorized. New static evidence
identifies a native standalone-EG discovery/parser/CRC route, potentially
removing the outer-package digest dependency for that format. Complete route
and compatibility review remain open; no candidate image was built and
hardware remains NO-GO. F-148 alone is bars-only, not the complete crop/label
feature. Next task: Claude's bounded static route and complete-edit contract.

Transfer cleanup preserves all research and seven registered worktrees;
only generated Python caches removed. Fact IDs F-081/F-110 repeat on main;
the local F-150 collision is resolved by renumbering our unmerged entries to
F-156--F-161. Merged findings remain unchanged.

### Earlier checkpoints (historical; current handoff above takes precedence)

F-161: native SHA-1 compression arithmetic passes twelve synthetic lengths;
native suffix-loop arithmetic passes 1,024 synthetic cases. New read-only
package digest verifier checks the supplied original before a candidate and
fails closed without its eight-byte suffix. Total 130 unit tests pass. The
actual Z30 suffix/input remains unavailable, so the original package digest
is still unverified and hardware remains NO-GO. See
[scope and reproduction](native-digest-arithmetic-verification.md).

Latest owner priority: no simulator-completeness or low-value research loops.
Prepare the smallest justified XPan-only hardware test, then stop at the
exact-build READY gate for separate owner approval. First technical blocker
is the native package digest's missing eight-byte input outside captured EG;
no authorized offline source/equivalent is identified. No new camera access
or memory acquisition is authorized. Current state remains blocked/NO-GO.
See the minimum-test stopping point in
[native-real-camera-readiness.md](native-real-camera-readiness.md).

Current consolidated hardware decision:
[native-real-camera-readiness.md](native-real-camera-readiness.md).
Modified-firmware test remains NO-GO; the separately authorized read-only
identity check does not waive any modified-build gate. Its closure is still
unreported. No hardware or simulator work was performed for this report.

Owner chose to keep the stills lifecycle gate unmet: existing controls establish
diagnostic rendering/setting/ABI behavior, but the harness lacks verified
native startup/menu-return/playback/warning coverage. No new run repeated the
known input-route limits. Exact F-148 identities reverified. Condition 1
remains unmet; no owner exception was granted. See
[native-xpan-lifecycle-decision.md](native-xpan-lifecycle-decision.md).

The separately authorized owner-operated identity/version check is reported
complete through step 5: NIKON DSC Z 30, reported camera version “1.2,” USB
IDs 04b0/0452. Idle shutdown/disconnection (step 6) is not yet reported.
This is not installed-firmware hash verification or modified-build approval.
See [native-hardware-gate-recommendation.md](native-hardware-gate-recommendation.md).

F-160: bounded close/live-ready contracts pass four stock/candidate pairs.
Known native callback inputs, callee-saved registers, aligned/balanced stack,
return flags and ready result pass; measured volatile differences are dead
at the named continuations. Retain exact F-148 wrappers. Global review and
native menu acceptance remain open. See
[native-xpan-close-ready-contracts.md](native-xpan-close-ready-contracts.md).

F-159: a bounded read-only stop-provenance check identifies shared flash
identity/geometry initialization; the outer operation remains unknown.
No new simulator run or patch change. Further flash-response explanation
work is retired; menu acceptance stays open. Next build-focused task:
remaining close/live-ready hook contract review. See F-159 in
[native-xpan-menu-boundaries.md](native-xpan-menu-boundaries.md).

F-158 supersedes the next-control instruction below: the single approved
writer-disabled/coarse control still stops at the same simulated flash
access. Menu mask remains off; post-menu bars check was not reached.
Writer redirection is not necessary for this observed stop, so removal is
not an established remedy. Patch unchanged, menu acceptance open; checkpoint
stopped pending owner selection of further bounded work. See the F-158
section of [native-xpan-menu-boundaries.md](native-xpan-menu-boundaries.md).

Latest stills checkpoint, F-157: stock/coarse menu confirmation returns;
candidate/coarse stops on unmodeled simulated flash access. Finer candidate
observations return through the original caller with count-3 mask exclusion
and matching frame/SP/target. This instrumentation-sensitive result does not
establish a fix. Next bounded control omits only candidate writer-branch
redirection while retaining all other overlays and coarse inputs/observations.
See [native-xpan-menu-boundaries.md](native-xpan-menu-boundaries.md).

Current stills checkpoint, F-156: exact F-148 overlay passes callback-driven
pixel and ten-cycle controls. Candidate menu confirmation failed to return
in two attempts; an unmodified control returned. Menu acceptance remains
unproved. Next: bounded stock/candidate comparison at the confirmation
writer/state boundaries. See [native-xpan-stills-controls.md](native-xpan-stills-controls.md).

### Main-lane reports preserved during reconciliation

**New, 2026-10-17, for Codex — PR #167: consolidated firmware static map.**
[firmware-map-2026-10-17.md](firmware-map-2026-10-17.md) is an
addresses-and-descriptions map of C 1.20 for all five user-story areas
(buttons, menus, live-view, crop, AE-L/AF-L tracking), with call chains and
confidence. New since prior notes: the screen fan-out driver 0x10595844 behind
the bars, the image-area function table at 0x11f9a4dc behind crop, and the
AE-L/AF-L queued-input router (callback + handler table at 0x1037a2c4, task-init
entry 0x1059c2c8). The three largest open leads (crop-table dispatcher, bars
fan-out entry, router input writer) all need an address-building (MOVW/MOVT or
base-register) index pass that was not done. No firmware bytes in the doc;
extracted components stay outside the repo. Owner reviews/merges PR #167.

**Historical action-half lead, superseded by F-215/F-218.** The old
"tracking candidate" cluster (0x11cf4e90/0x11cf5774/matcher 0x11cf5248) is
**Bluetooth HCI**, not AF tracking, and remains ruled out. The firmware text
catalog at 0x103edda0 contains a 3D-TRACKING label, but the separate
selectable AF-area table at 0x1074a688 contains eight options and no
3D-TRACKING row. Auto-area AF values 600/601/602 set base mode 6 and one of
three submodes; the OK callback stores that choice. Nikon documents subject
tracking as a separate shooting-view J operation or assigned action. The
specific live-view J callback is not yet identified. The active hook evidence
is the native action-45 request path compared in F-214, not the label
catalog. See F-215/F-218 and [tracking-input-chain.md](tracking-input-chain.md).

**New, 2026-10-17, for Codex — deep cross-reference companion.**
[firmware-map-deep-2026-10-17.md](firmware-map-deep-2026-10-17.md) adds the
static branch/literal/pointer cross-reference results (confirmed call chains;
the bars screen fan-out driver 0x10595844; the crop function table 0x11f9a4dc;
the AE-L/AF-L queued-input router) and the complete named hardware-switch table
at 0x1072e3b0 — three registers SW0/SW1/SW2, with AE-L/AF-L = SW0 bit 0x2000
and the "i" button = SW1 bit 0x400. **Codex must own the MOVW/MOVT (or
base-register) address-building index pass**: the Claude lane is blocked from
it by a safety classifier, and the three largest leads (crop dispatcher at
0x11f9a4dc, bars fan-out entry 0x10595844, physical AE-L/AF-L input link) all
dead-end on addresses that only that pass resolves. Prose only, no firmware
bytes.

**New, 2026-10-17, owner-requested handoff to Codex: Lane 0** (see
handoff-codex.md's new "Lane 0" section). The dormant-worker pattern that
blocks both Lane 1's and Lane 3's natural-trigger questions (F-019,
F-109, F-115 through F-117) is handed off as its own thread rather than
re-attempted per-lane. Likely needs the QEMU machine model
(`z30-qemu/qemu/nikon-z30.c`), not just Python scripts -- a better fit for
Codex regardless of the owner's specific ask. Explicitly: resolving this
does not by itself authorize or reach hardware install; that still needs
the owner's separate written risk acceptance (hardware-readiness.md) and
conditions 2 through 4.

**F-120 found this firmware genuinely contains ARM-mode code** (a real
`memcpy` routine at two separate linked addresses, plus compiler-runtime-
shaped helpers), confirmed via live code decode -- something every prior
static scan in this project assumed away. Does not show any of the
project's specific "zero callers" dead ends (`0x10459d80`, Lane 3's
property dispatch) live there; flagged as a cheaper thing to check before
touching QEMU's C source if Lane 0's steps 1-2 come back empty.

Local F-135 on `codex/firmware-preflight-plan`: recovered package verifier
audited; unchanged in-memory decode/re-encode reproduced the original exactly.
See [native-package-verifier-audit.md](native-package-verifier-audit.md).
No modified firmware image was written. Local F-136 implements the decoded
container reader with synthetic rejection tests; all three original components
also passed with their hashes pinned. See
[native-container-validator.md](native-container-validator.md).
Local F-137 implements exact-edit manifest comparison with synthetic and
combined CRC/edit checks; the unchanged package baseline passes with zero
changed bytes. See [native-exact-edit-audit.md](native-exact-edit-audit.md).
Local F-138 combines those checks in one decoded-container preflight, tested
with synthetic modified containers and the unchanged original baseline.
See [native-combined-preflight.md](native-combined-preflight.md).
Local F-139 identifies native body-package parsing, confirms decoder-mask
and CRC-table equivalence, and finds an additional 20-byte digest check
not covered by our preflight. EG installation reaches a relocated target;
physical flash writes remain unverified. See
[native-updater-validation.md](native-updater-validation.md).
Local F-140 traces the encoded-format flag through parser/cache/selection;
the original statically predicts the extra-digest branch after record restore.
Expected digest/message/suffix boundaries are traced, but an eight-byte source
at `0x10000088` remains unmapped. See
[native-updater-digest-inputs.md](native-updater-digest-inputs.md).
Local F-141 finds no digest-input mapping in the startup page table or 18
scatter records. It maps the updater RAM block to verified EG source bytes;
see [native-boot-mapping-boundary.md](native-boot-mapping-boundary.md).
Local F-142 identifies native erase/program/readback paths and the initialized
43,253,760-byte EG target, including 9,314,248 bytes of tail padding. No
native update was executed. See [native-install-span.md](native-install-span.md).
Local F-143 adds the read-only installation model to preflight; synthetic
tests and the unchanged audited original baseline pass. See
[native-installation-model.md](native-installation-model.md).
Local F-144 reviews both existing private overlay revisions. Mapped layout
checks pass, but both retain a four-byte stack displacement at the state
wrapper's stock-service call; condition 3 remains unmet. See
[native-xpan-contract-review.md](native-xpan-contract-review.md).
Local F-145 adds a supplied-boundary contract checker and synthetic operation
tests. The abstract restored-frame tail transfer passes; existing real
overlay code is not approved. See [native-call-contract-tests.md](native-call-contract-tests.md).
Local F-146 checks textual instruction forms and layout: the corrected state
wrapper plus adjacent writer uses 48 of 52 bytes. Writer entry/hook must move;
no final overlay encoding or execution was checked. See
[native-xpan-layout-proposal.md](native-xpan-layout-proposal.md).
Local F-147 runs that correction in paired pinned-QEMU fixtures. Measured
service-entry stack/register preservation passes; the other-state return
changes NZCV and still fails the strict contract. Writer relocation/frame
checks pass within diagnostic scope. See
[native-xpan-abi-experiment.md](native-xpan-abi-experiment.md).
Local F-148 resolves the measured flag mismatch in a new private overlay:
both strict state cases pass with entry flags additionally required; writer
frame/results/CPSR match the baseline. Scratch writer LR still differs;
saved return target/mode match. See
[native-xpan-flags-remediation.md](native-xpan-flags-remediation.md).
Local F-149 restarts saved-crop research with initialized RAM mappings for
F-110's two filename-pointer tables, cross-checked after stock assisted
startup. Nearby references are found; actual filename-field consumption and
save creation remain unproved. See
[native-save-table-ram-mapping.md](native-save-table-ram-mapping.md).
Next: trace actual filename-pointer loads from those RAM mappings toward
serialization/file creation. Full lifecycle and global code review remain open.
Camera-side acceptance remains unverified.

Main carries facts through **F-114**. F-101 merged via PR #119; F-102/F-103
via PR #123; F-104 via PR #124; F-105 via PR #126; F-106 via PR #127;
F-107 via PR #128; F-108 via PR #129; F-110 via PR #138; F-111 via PR
#139; F-112 via PR #140; F-113 via PR #141. The SD-card-
detect/enumeration thread (F-102, F-104) is retired per owner direction
(see AGENTS.md's "Priority" section and handoff-codex.md). Lane 1's
mode-state chain is resolved through F-108; F-109 closes the one
remaining thread (who posts the live-view trigger event) as a
deliberately-dropped simulator-reachability question, not a real-
firmware gap.

**Owner call, dissenting review recorded, audit fix-and-retest done
(F-115):** the owner called build-gate condition 1 satisfied for Lane 1;
the required dissenting review (PR #144) disagreed as worded, and a
separate instruction-level audit (PR #145) found three things to fix.
F-115 fixes two of the three in a private generator copy, re-runs every
simulator control against the rebuilt overlay (all pass), and re-attempts
the dissenting review's cheapest natural-path remediation option against
the fixed overlay, reaching the guard and mask for the first time outside
a diagnostic call (see hardware-readiness.md's new follow-up section).
**Condition 1's status is unchanged** -- still not satisfied as worded;
the owner's call is still pending on that review, and this pass does not
claim to resolve it.

**Lane 2's capture-descriptor question is accepted as settled toward the
settings/property-dispatch reading (F-106) -- meaning the real save-crop
mechanism remains unfound, not merely unverified.**
`hardware-readiness.md`'s "RAW crop"/"RAW output path" rows were stale
(citing only PR #37/#47) and understated this; corrected via PR #137.
F-110 opened a fresh angle (the firmware's actual file-naming system).
F-111's property module was dropped on direct check (no image-area
reference). F-112 found the real geometry table family, confirmed via
image-area property `0x501`'s readers. **F-113 decoded the crop-window
builder's own body for the first time** (`0x101d5b36`). **F-114
completes the picture**: the centering arithmetic resolves to an
unambiguous crop-rectangle descriptor (top-left corner, bottom-right
corner, their center, final output size), and the gate function is
trivial. A response-safety-classifier stop blocked checking which of
the builder's seven callers reaches a real save -- dropped, not
retried; F-095/F-096 already characterized all seven and that read is
unchanged (none confirmed as a save path, the most-traced one leaning
away from it). This remains the single biggest open research gap for
Build 1. **F-118 did the live-simulator-read step for the geometry math
itself**: re-running F-078's existing script confirms F-114's center-is-
midpoint claim against real execution across all 15 tested combinations
(not a sample), and fully explains the final-output-size field's `(0,0)`
pattern as a consistent "no resize" sentinel. **F-119 then read F-112's
RAM-resident width/height table directly** (real values, cross-matching
three of F-118's outputs exactly) but found the table's own indexing
doesn't match the builder's (quality,area) byte values the simple way --
flagged, not solved, for whoever maps the remaining sibling tables next.
The caller/save-path question is unchanged by either -- still the actual
remaining gap, and still not re-attempted after its classifier stop.

The owner approves merges; nobody merges their own PRs. Check main again
before allocating F-135.

**Lane 3 update (2026-10-18; F-212/F-213/F-214/F-215/F-218):** the property `0x2021` investigation
is historical and not the active one-button tracking lead. A private
candidate for an AE-L/AF-L rising-edge hook now passes constructed-context
guard, register/flag preservation and cleanup cases in pinned QEMU. A
separate powered simulator run found the worker task present before a native
notification and its saved stack pointer changed afterward, but worker
entry/cleanup probes did not hit (F-213). Native
Subject tracking action enum 77 and a shared configurable-action route are
identified statically; the AE-L/AF-L settings handler does not support that
enum, so a menu-only addition is insufficient. F-214 compared the candidate
adapter with the native Fn Subject tracking handler: both reach action 45.
F-221 corrects the claimed request tuple destination: `0x1045a47e` is a
boolean gate, not the request service. Action 45's state mapper snapshots AF
state and branches on base mode 6, submode, and a state byte, then routes to
three native helpers. The official
manual specifies the toggle behavior, while QEMU cannot observe the consumer
because that object is unmodeled. This validates the action route, not
natural worker admission or the full image ABI; no complete modified image
exists. F-215/F-218 distinguish the AF-area label catalog from the selectable
options: the former contains 3D-TRACKING text; the latter has Auto-area
variants but no 3D-TRACKING row. The menu's OK callback stores the mode, while
shooting-view Subject tracking is a separate J or assigned-action operation.
A synthetic live-view J probe did not reach its callback, leaving that path
unresolved. F-219 traces the special J/OK filter through runtime key-to-
function lookup, which can invoke a registered callback, plus a separate
generic live-view input path with no direct edge to action 45; the actual
callback remains indirect. The 3D-TRACKING string is
selected by a descriptor field in a status renderer and is not an activation
call. Next: resolve the runtime J callback against native action 45 only if it
could alter the chosen hook, and close candidate ABI/readiness gaps before any
device-test preparation. No
camera test/write follows from this evidence. F-216
identified stack and layout gaps; F-217 then assembled/linked the candidate
in memory and applied all 45 planned edits to stock QEMU guest RAM. Two
constructed-context action calls restored context and issued the native
request; the navigation region is now included in the layout. Natural input,
camera-load executable mapping, worst-case stack and the consumer transition
remain open, so no testable overlay is ready. See F-212 through F-217 and the
updated Lane 3 handoff.

**Owner's operating choice / F-221:** keep Auto-area AF and assign the native
Subject-tracking action to AE-L/AF-L. F-221 corrects F-220's alleged internal
event-post path: the supposed poster is a return stub. Action 45's AF-state
dependent helper routing supports reusing Nikon's action handler without
adding patch-side state, but does not map helper calls to start/end behavior.
F-222 traces the helper callees; their internal state mutations remain
semantically unlabeled. The manual defines the external cycle, but constructed
QEMU calls cannot observe the unmodeled consumer. This supports the route
design, not the candidate's cycle reliability. Prioritize natural AE-L/AF-L
press admission, then candidate executable mapping and stack proof. The
shooting-view J callback is lower priority unless it can change the action-45
hook decision. The candidate remains not testable because held-repeat and
fresh-second-edge cancellation behavior have not been observed.

**F-225 trigger refinement (2026-10-18):** the private candidate's mask
predicate is structurally coherent with the first difference block built by
`0x102f199a`: it detects `0x2000` present in one input and absent from the
other. The builder inputs have not been tied to the physical AE-L/AF-L switch,
so natural press admission remains unproved. Continue from the builder input
sources while keeping Auto-area AF and native action 45 as the selected
feature design.

**F-227 hook candidate:** registered callback `0x102f2eae` handles the
AE-L/AF-L bit and current AF-ON assignment (`0x1184 == 9`) through event
`0x14`. It follows a broad snapshot-change check and has no proven
AE-L-specific rising edge, so action 45 cannot safely replace that event yet.
Trace the snapshot's old/new fields; then design a one-shot edge bridge while
preserving ordinary AF-ON behavior. Auto-area AF remains the intended setup.

**F-228 correction:** keep the `0x103020b4`/`0x10302108` dispatcher family
under investigation. It also routes to the Fn1 handler that invokes action
45, so its combined status mask does not exclude it as an action path. Trace
the physical event-to-case mapping and the AE-L handler before selecting the
remap seam.

**F-229 advances the trigger mapping:** the live-view mask table maps
AEAF_LOCK `0x2000` to logical input 13, and the UI table labels its event
`0x28b` “AE-L/AF-L button.” Snapshot callback `0x102f2eae` tests the same bit
and preserves the existing AF-ON assignment route. This is the strongest
static AE-L boundary. The candidate's logical-ID-13 gate matches the table,
but the paired-record producer is not linked to it. Synthetic OK/J `0x27e`
and AE-L `0x28b` dispatches in QEMU did
not reach a downstream action. The `3D-TRACKING` label remains a renderer
string rather than a selectable AF-area mode. Keep Auto-area AF. The current
private candidate adds “Subject tracking” to the AE-L/AF-L list as value 77
and routes it to action 45; its ID-13 gate aligns with the AE-L input map.
Physical press admission is assigned to the later device test. Before then,
prove the candidate's sequential fresh/held/release/second-edge action and
cleanup control in simulator. See F-229 and Lane 3 in
`handoff-codex.md`.

**F-230 advances (but does not finish) the candidate control gate:** the
memory-only sequential probe passed fresh/held/release/fresh arbitration and
dispatched native action 45 once on each fresh edge, with constructed cleanup
and ABI save/restore passing. The AF consumer is unmodeled, so start then
second-press cancellation remains unobserved. The candidate still lacks a
private-overlay load without debugger writes, camera-load executable mapping,
worst-case stack proof, and full-image acceptance. Keep Auto-area AF and the
AE-L/AF-L action-45 remap. Do not promote this to camera-testable yet; see
F-230 and the tracking section in `handoff-codex.md`.

**F-231 narrows native AF-state provenance:** action 45's state mapper reads
bytes copied from the native AF context's mode-dependent state tuple, but the
fields carry no decoded tracking-active label and do not identify start or
cancel. A disposable-QEMU test set Auto-area value 600 through the native
setter and verified base 6/submode 0 and Fn action 77, yet action 45 still
read simulator state 5 and skipped Auto-area helper branches. The simulator
cannot verify the cycle. Stop simulator-fidelity work; continue with private
overlay loading without debugger writes, then executable mapping, stack proof
and full-image acceptance. Candidate is still not testable; see F-231.

**F-232 closes two simulator build checks:** using installed LLVM tools, the
private candidate reassembled and linked with 964 code bytes, 24 checked
relocations, and all 15 hook windows validated. QEMU's generic loader loaded
all 35 overlay regions before guest resume; every region read back exactly,
with the original firmware hash and QEMU checkout unchanged. The loaded
candidate passed the constructed fresh/held/release/fresh sequence and
cleanup/ABI controls. Native start/cancel, physical button delivery,
camera-load executable mapping and worst-case stack headroom remain open.
Keep Auto-area AF and the AE-L/AF-L Subject-tracking assignment. The candidate
is still not ready for a camera test; see F-232.

**F-233 keeps executable mapping open:** the reset page table maps the
candidate code section with XN clear, but ARM/Thumb scans found later scheduler
TTBR0 writers. In the pinned simulator, the candidate task inherits a
runtime table whose `ATS1CPR` result points outside modeled RAM, despite the
loader-based overlay executing at the VA. This is not camera mapping proof.
Trace the runtime table setup for the tracking task; do not promote the
candidate to camera-testable. See F-233.

**F-234 keeps stack headroom open:** the synthetic stack-watermark attempt
returned from its adapter but observed no native action call or candidate
path. The changed boundary bytes do not measure candidate depth. Repair the
constructed action-path setup and require native action entry before using a
watermark; independently trace runtime TTBR0 setup for page `0x1002d000`.
The AE-L/AF-L Subject-tracking candidate remains not camera-testable. See
F-234.

**F-235 narrows, but does not close, stack risk:** a corrected loaded-overlay
probe reached action 45 on both constructed fresh edges and suppressed held
and release. It changed 1,364/1,324 bytes of a 2,048-byte canary below the
action SP; the task allocation is 11,264 bytes. This is bounded path evidence,
not a worst-case proof. Runtime executable mapping and native start/cancel
semantics also remain open. Keep the candidate not camera-testable; see F-235.

**F-236 identifies the AF action gate:** action 45 passes beyond mapper
`0x1044dc5a` only for numeric state 2, requiring mode byte `+0x44 == 6`,
snapshot byte `+0x61 == 1`, and `+0x62 == 0`. QEMU's state 5 is rejected.
The accepted route calls a stateful routine but does not prove start/cancel;
the later event target is a return-only stub. Trace the stateful object's
writers/callers; keep runtime mapping and worst-case stack open. See F-236.


**F-237 corrects mapper scope:** caller `0x1044dcbe` is separate from the
main action-45 selector `0x10368b6e`; its state-2 condition is not the only
accepted action state. The main selector routes mapped states 0-3 per
F-221/F-222. Trace plain Auto-area state writer `0x1019596e` and the
AE-L-specific edge at callback `0x102f2eae`; candidate ring admission remains
unproven. See F-237.

**F-238 corrects and tests the snapshot-edge hook:** the valid boundary is
`0x102f0d30`, not the middle of its instruction at `0x102f0d32`. A private
LLVM-linked prototype dispatches action 45 on a synthetic fresh AE-L/AF-L
edge and suppresses held/release, passing a 1/0/0/1 QEMU sequence. This test
used a private return trampoline and did not run the native updater tail.
The shared updater has seven callers, leaving inline task context/stack
suitability open along with runtime mapping, worst-case stack, physical input,
native start/cancel and full-image acceptance. Candidate remains not
camera-testable. See F-238.

**F-239 narrows the native state route:** plain Auto-area action 45 reaches
`0x1019596e`, which writes 6/7 to an AF-related object byte after readiness
checks. The helper also forms event `0x3b` through a return-only stub. This is
stateful behavior, but the fields are not labelled tracking active/inactive;
start and second-press cancel remain unproved. See F-239.

**F-240 makes the hook context tradeoff explicit:** paired-record builder
`0x102f199a` calls the shared updater twice from a `0x31c`-byte frame; other
callers have smaller visible frames but unknown task stacks. A common-site
inline action risks stack use on the builder path, while callback-only can
miss an edge already consumed by another updater caller. Map task contexts
and stack budgets or design a pending-edge handoff. No testable hook yet. See
F-240.

**F-241 narrows the remap search:** Fn1's configurable handler invokes
Subject-tracking action 45 for assignment value 77; AE-L/AF-L's handler
reads its own assignment property but handles only 25/42. Trace the
function-code dispatcher caller and compare event cadence and handler
contracts before extending the AE-L/AF-L handler. This is a patch hypothesis,
not a selected or testable hook. Keep Auto-area AF. See F-241.

**F-242 validates only the handler-level branch:** private QEMU observed
assignment 77 reaching native action 45 and sampled 25/42 assignments
retaining their existing branches. Guest writes were restored; firmware and
simulator remained unchanged. Physical button cadence, held-repeat behavior,
native second-press cancellation and full-image/runtime build gates remain
unproved. Trace the function-code 13 event producer before selecting this as
the remap hook. See F-242.

**F-243 leaves the handler route unselected:** the dispatcher's only direct
caller forwards codes 26–28, while AE-L/AF-L is switch entry 13. No static
physical-button edge is established. Trace registration/indirect callers or
resume the input-chain edge source. See F-243.

**F-244 records one inconclusive simulator attempt:** direct synthetic entry
to snapshot callback `0x102f2eae` timed out before return, with no observed
action-45 entry. The synthetic record/context was not validated. Do not
repeat that probe; continue static caller analysis and resolve stack/runtime
gates for the tested rising-edge candidate. See F-244.

**F-245 closes the requested AF-area/OK trace at runtime dispatch:** Auto-area
AF stores base mode 6/submode 0; the 3D-TRACKING string is a status label.
Shooting-view J (`0x27e`) is looked up in a runtime key/callback table and
invoked indirectly. The bounded QEMU event did not reach a callback or action
45. No competing action hook was identified, so retain native action 45 on
AE-L/AF-L as the leading design. The candidate remains not camera-testable;
runtime mapping, stack, full-image acceptance, and native cycle evidence are
still unresolved. See F-245.

**F-246 completes the bounded J-table comparison:** the sampled four-entry
runtime table has three response callbacks and one empty slot; their reviewed
bodies do not directly invoke action 45. Synthetic `0x27e` reached generic
dispatch/screen handling only, not the filter lookup or action. This is a
simulator boundary, not proof against camera J behavior, and yields no better
patch hook. Keep native action 45 as the AE-L/AF-L remap target. See F-246.

**F-247 selects a single candidate trigger path:** the private production
overlay combines a common-updater inline action and a ring-record worker
action. Their independent tests do not rule out duplicate action-45 calls
from one press, and the inline path inherits seven caller contexts. Keep only
the worker-mediated accessor path for the test candidate; physical source and
native cycle are owner-assigned device-test items after all other gates.
Mapping, complete image acceptance, and hardware readiness remain open. See
F-247.

**F-226 remap-path correction (2026-10-18):** the Fn1 configured-action
handler calls native action 45 for value 77; AE-L/AF-L's separate handler
does not. The nearby calls previously treated as possible routing points
only produce a control-status mask. The candidate's input record has no
proven physical AE-L/AF-L source. Next identify the actual button action path
and branch it to action 45 on a fresh press; keep Auto-area AF. No complete
test image or camera-ready patch exists.

**F-116/F-117 exhausted the cheap options on property `0x2021`'s
consumer, all negative.** Four static masking idioms tried (`lsr #8`,
`and #0xff00`, `ubfx`: clean negatives; `tbb`/`tbh`: 2,817 sites, too
many to review, only a narrow index-shape ruled out). The live-simulator
breakpoint option (F-117) is the most informative: `0x10475ecc` was never
called at all during an idle wait plus a real menu-activation and eight
real key-dispatch calls -- a dormant-worker-shaped negative (F-018/F-019
pattern), not a hit on any id. **No consumer found by any method tried.**
What's left is slow (hand-reading `tbb`/`tbh` tables) or hits the same
unsolved problem as other lanes (keeping a background task alive in the
simulator long enough for a real post).

## Feature state

An assisted simulator prototype now loads a native hook before CPU start and
makes the stock screen-layer mask follow the stored image-area choice. A real
1:1 menu pick kept the bars off over the menu, an audited live-view activation
restored them, DX and 16:9 kept them off, and ten signal cycles passed. The
instruction-space and native-execution part of build-gate condition 1 is met
in this assisted simulator setup. A broad menu-close hook was tested and
rejected because it enabled the mask on a non-live-view transition screen.
The replacement requires an empty screen stack and live-view selector 1; it
passed the same area and cycle controls and stayed off in that transition.
The exact selector-1 wrapper also passed through the stock internal type-2
dispatcher; only the natural worker caller remains unobserved.
Natural startup, a true menu return to live view and the unavailable `i`-menu
path remain unverified.

A centered 5200 by 1920 capture-geometry experiment passed, but no saved RAW
crop or NEF metadata writer is verified. The later structure-pack trace
does not close that gap; settle it with the separately authorized on-camera
test when appropriate, not as a prerequisite for feature work. Physical
AE-L/AF-L input delivery and a tracking entry point remain unverified.

The immediate F-147 flag defect is resolved by F-148. Active priority:
F-149 is the final static filename-table trace: no concrete route to the
filename getter or save path remains, so this static thread is dropped. The
actual crop question is reserved for the separately authorized on-camera test
and is not a blocker.
Retired simulator event-poster searches are not the default next step.

## Decisions and limits

Personal, non-distributed build work is open; hardware remains NO-GO.
No installable firmware or installation workflow was produced. All work
this session stayed offline in static analysis and disposable simulator
processes. Original restricted inputs and the pinned simulator remain
unchanged. No firmware, raw logs, screenshots or extracted data enter Git.
The repository stays private; every change goes through owner-reviewed PRs.

The owner removed absolute hardware safety as an acceptance criterion on
2026-10-16 because it cannot be proved before the first hardware test. The
replacement gate uses three states: simulator accepted, ready for an
experimental hardware test, and hardware validated. Missing recovery must be
recorded as an accepted service-or-total-loss risk, never as proof of safety.

Written by Codex in collaboration with Claude and Tony Kim.

Lane 3 latest: F-248 closes the local return/register/flag contract for the
selected worker-only accessor hook. The generated manifest's execution flag
is not the final simulator result; F-232/F-235 document the separate
loader-based QEMU run. Complete candidate ABI/stack review, camera-load
executable mapping, full-image acceptance, and hardware-readiness/recovery
records remain open. See `tracking-input-chain.md` and `handoff-codex.md`.

F-249 narrows the unresolved camera-load mapping: later MMU setup selects a
RAM TTBR0 table at `0xc11f8000`, outside the captured firmware module, and
the candidate-page descriptor was not available from the static image. F-251
read a runtime descriptor in the QEMU display profile, but not from the
tracking-worker context. See Lane 3 handoff; hardware readiness remains
NO-GO.

F-250 found no simple zero-filled code relocation span in the sections with
the current hook sites. The reviewed candidate cave remains the only
currently reviewed placement, with its runtime mapping unresolved. See Lane
3 handoff; no patch is ready for camera testing.

**F-251 mapping follow-up (2026-10-18):** the owner authorized exploring an
on-camera read, but the approved rules still require a specific method review,
recovery plan, and exact-method approval. Existing PTP review identified no
documented live-RAM read; do not probe generic vendor commands. The current
simulator route uses the existing display-profile RAM map, which includes the
TTBR0 address. An isolated QEMU 10.2.4 diagnostic read the active entry for
`0x1002d000`: valid section, XN clear, matching ATS result without fault, and
a target inside modeled display RAM. The probe ran in a diagnostic task, not
verified tracking-worker context; F-252's thread-aware retry did not reach
the worker entry, so the simulator route is closed without a worker
descriptor. No repo QEMU source changed and no camera was accessed. Details
are in `handoff-codex.md` and `tracking-input-chain.md`.

**F-252 worker-context probe (2026-10-18):** the thread-aware QEMU check did
not reach tracking-worker entry during a 20-second run after standard
assisted live-view setup, so it did not capture the worker's runtime table.
This is a bounded simulator result, consistent with F-213, and not camera
evidence. Stop extending this scheduling path. The USB inventory currently
shows no Nikon device; broader camera reads still need a specific reviewed
method and exact approval. See F-252 and the Lane 3 handoff.

**F-253 table-base refinement (2026-10-18):** in the diagnostic task, the
active QEMU TTBR0 was `0xc2ad4000`, with an executable candidate-page entry
into modeled display RAM. A watchpoint on that exact entry saw no write in
the bounded post-setup interval. This differs from F-249's static setup path
at `0xc11f8000` and does not establish the tracking worker's camera mapping.
Per F-252, stop this simulator scheduling path absent a new worker stimulus.
The camera is not connected yet; a future identity/operation inventory can
check advertised PTP support, but no reviewed live-RAM method is known. See
F-253 and the Lane 3 handoff.

**F-254 camera connection preflight (2026-10-18):** a source-reviewed
single-operation PTP GetDeviceInfo probe is ready at
`src/nikon_z30_research/ptp_device_info.py`. It reports identity and
advertised operations only, sends no Nikon vendor command, and has six
synthetic parser/command tests. No camera is connected and no hardware result
is claimed. When connected, the read-only inventory can show whether firmware
advertises a candidate operation; it cannot read live TTBR0. See F-254 and
`camera-readonly-identity-method.md`.

**F-255 host enumeration check (2026-10-18):** libusb initialization and USB
descriptor enumeration succeeded; no `04b0:0452` device is currently present.
No device was opened and no PTP operation was sent. The camera connection
step is ready for later, but this does not establish camera PTP support or a
live-memory method. See F-255 and the Lane 3 handoff.

**F-256 libusb descriptor ABI check (2026-10-18):** the Python ctypes
descriptor layouts used by the prepared PTP query match the installed
libusb C ABI for the fields the probe reads. This verifies host-side struct
layout only; it does not verify camera enumeration or PTP transport. See
F-256 and `camera-readonly-identity-method.md`.

**F-257 camera visible to IORegistry but absent from libusb (2026-10-18):**
IORegistry lists the connected Z 30 (`04b0:0452`), while Python and a native
C check using libusb 1.0.30 both enumerate zero devices. The documented
GetDeviceInfo probe therefore stopped before opening the camera or sending a
PTP command. USB release `0x0120` is descriptor metadata, not proof of camera
firmware version. The direct-libusb transport is unresolved on this host. See
F-257 and the Lane 3 handoff.

**F-258 GetDeviceInfo succeeds with host USB access (2026-10-18):** the
single standard PTP GetDeviceInfo request succeeded and reported Nikon
Corporation, Z 30, device version V1.20, and advertised operations. The
response serial was omitted. Operation `0x9535` is advertised but not
identified in local reviewed references; do not invoke it without a separate
method review and approval. This resolves identity/inventory transport but
does not provide live RAM or the worker's TTBR0. See F-258 and Lane 3.

**F-259 local PTP source lookup (2026-10-18):** project references and the
installed libgphoto2 documentation/headers do not map `0x9535` or identify a
reviewed runtime-memory read operation. The local lookup branch is closed;
this does not prove no undocumented interface exists. No further camera
command is authorized by identity approval. Keep Lane 3's camera-load mapping
gate open and continue only with useful static real-firmware evidence or a
newly reviewed read method. See F-259 and the Codex handoff.

**F-260 constructed native request cycle:** corrected paused-QEMU controls
with the status record action 45 actually reads reached native start on a
fresh decision and native stop on a second fresh decision; held/no-decision
reached neither. The tracking pair changed `(0,0)->(1,0)->(0,0)`. This is
candidate call-path evidence under constructed Auto-area status, not natural
camera status, physical AE-L/AF-L admission, subject acquisition, or async
completion. The next hardware-derived observation is a user-run stock Fn1
Subject-tracking reference test. Runtime executable mapping remains open.
See F-260 and Lane 3.

**F-261 stock-camera Fn1 behavior:** the owner's V1.20 test found that Fn1
press/release displays a persistent tracking target, a second tap ends it,
and holding behaves like tapping. Tracking activation required shutter
half-press, after which the target followed the subject. This is native-control
and acquisition evidence, not candidate-hook validation. The bounded PTP event
monitor is prepared but awaits approval of its exact method. See F-261 and
Lane 3.

**F-262 identity/transport refresh:** host USB enumeration sees the Z 30 and
the pre-approved standard GetDeviceInfo query succeeds with host USB access,
reporting V1.20. Sandboxed libusb enumeration returns no match. The advertised
operation list includes standard OpenSession/CloseSession. This verifies
transport availability, not event capture or live memory. See F-262.

**F-263 event-monitor preflight stop:** the owner-approved monitor found no
unique default PTP interface with the expected interrupt-IN endpoint and
stopped before device open or PTP transfer. No button events were captured.
A descriptor-only diagnostic is proposed separately and awaits approval. See
F-263 and Lane 3.

**F-264 endpoint descriptor result:** the approved descriptor inspection
found the expected PTP interface and an 8-byte interrupt-IN endpoint. The
monitor rejected it only because of its incorrect 12-byte single-packet
threshold. The monitor is corrected offline to collect up to 24-byte PTP
event containers. This revised transfer method awaits exact approval before
retry. See F-264 and Lane 3.

**F-265 zero-byte event poll:** the approved monitor opened its PTP session,
then received a successful zero-byte interrupt transfer and stopped before
any event container. It attempted best-effort CloseSession; acknowledgement
was not surfaced. The monitor now treats zero-byte transfers as idle within
the same 15-second limit. Owner requests a warning and explicit start signal
before each run, with no repeated permission request for this method. See
F-265 and Lane 3.

**F-266/F-267 event correlation:** two approved 15-second windows completed.
Four AE-L/AF-L presses coincided with four PTP `DevicePropChanged` events for
`FocusMeteringMode` (`0x501c`); three presses coincided with two events for
that same property. This associates the control sequence with a
focus-metering-mode signal, but event counts are not one-to-one and the value
transition is unknown. Next, offline-review a strictly read-only standard PTP
descriptor/current-value query for only `0x501c`. Any further event window
requires a warning and explicit owner start signal. See F-266/F-267 and
Lane 3.

**Owner target update:** Subject tracking should be continuously armed in
shooting mode: reticle visible without a control press, acquisition starts on
shutter half-press, and no key toggles it off. Reuse the known live-view-ready
site `0x102f5810` as the candidate one-shot native action-45 hook; its existing
QEMU evidence covers only XPan mask behavior. Prove AF-ready timing, action
context/ABI, and one-shot behavior across view transitions before treating it
as a patch. A narrowly scoped `GetDevicePropDesc` query for `0x501c` is
prepared offline in `camera-focus-mode-descriptor-method.md`, but has not been
approved or run. See Lane 3.

**F-268 correction:** the owner-authorized standard PTP descriptor query for
`0x501c` was run and returned `0x200A` (DeviceProp Not Supported). It exposed
no value or armed-state signal; no vendor query was attempted. The continuous
Auto-area goal also requires reconciling mode selection with shooting-view
readiness, since a view-entry hook alone misses a mode change in an already
open view. See F-268 and Lane 3.

**F-269:** the AF byte values 6/7 are selected by the input argument to
`0x1019596e`, not directly by people/animal mode. People submode uses separate
helpers; animal submode shares the plain Auto-area path and supplies input 0,
which writes 6. The field's purpose remains unknown. See F-269 and Lane 3.

**F-270/F-271 QEMU progress:** action 45's exact route is corrected: states
0/1 take `0x1045a1ae`; states 2/3 take `0x1045a21c`; `0x1045a1e6` belongs to
selector 27. With a constructed initial tuple and explicit call to native
status copier `0x101925b0`, QEMU executed the native state cycle through first,
second, and third action calls. This closes the “no native software state
cycle” simulator gap under synthetic state. It does not prove natural AF-state
production, reticle rendering, or subject acquisition. F-272's temporary
auto-arm overlay loaded, but QEMU halted during startup on an unmodeled write
at `0x10000aaa` before live view; the documented no-lens test peer did not
resolve it, and the overlay never executed. Stop simulator-fidelity work.
Resume with static analysis of the real AF state and hook contract; no
testable patch is established. See F-270/F-271/F-272 and Lane 3.

**F-273 AF-status refresh finding:** the native status-copy bridge has one
direct call site, inside an event-driven state update, not a per-frame loop.
QEMU's stale mapper tuple after action 45 is therefore consistent with the
static call path. Any auto-arm candidate needs a reliable latch or an
explicitly reviewed refresh before using that tuple as a guard. This does not
prove hook timing or safety; continue static AF-state and caller-contract
analysis. See F-273 and Lane 3.

**F-274 corrects the auto-arm simulator result:** F-272's startup failure was
caused by a temporary 44-byte wrapper overflowing its 24-byte verified cave,
not by a demonstrated QEMU peripheral gap. The corrected overlay stays in a
verified 512-byte cave, reaches live-view setup, and invokes native action 45
successfully from its internal return point before the explicit status
bridge. The outer callback still times out amid repeated mapper breakpoints;
reticle and acquisition remain unobserved. Continue with a narrow callback
completion or guest-driven ready-event test. No camera-testable patch exists.
See F-274 and Lane 3.

**F-275/F-276 identify the corrected test path and stop:** stock type-2
dispatch `0x104b912c([object, 2, 0])` reaches action 45's successful return,
then QEMU pauses on unknown write `0x10000aaa = 0xaa`. A private exact-address
no-op exposes `0x10000554 = 0x55`, consistent with—but not proof of—a flash
unlock sequence. Do not invent a device response or extend this simulator
branch. The callback, reticle, acquisition and testable-patch status remain
unverified. See F-274 through F-276 and Lane 3.

**F-277 resolves stop provenance only:** the PC/LR at F-276 match F-159's
shared flash identity/geometry initializer; its outer caller and operation
remain unknown. The current trace does not tie this access to tracking or an
update. Further flash-response modeling is retired. Continue with the
tracking action's real-firmware hook/state contract. See F-159/F-277 and Lane
3.

**F-278 AF-byte check:** a separate guarded consumer reads the byte that the
tracking helper writes as 6/7, but proceeds only when it equals 1. This does
not establish a people/animal code or tracking-ready signal. Standard USB PTP
events cannot expose the internal byte; the previous focus-mode event
correlation and unsupported descriptor query do not resolve it. See F-278
and Lane 3.

**F-279 native state writer:** `0x10078aa0` writes `(1,0)` to the same source
pair copied into the action-45 mapper context. It is reached through an
event-driven updater, but the triggering object-state checks are not tied to
Auto-area or tracking readiness. A focused callback-level QEMU test is now a
better next simulator step than trying to boot through the retired flash
initializer. See F-279 and Lane 3.

**F-280 QEMU callback control:** the synthetic event reaches `0x10074492` but
returns before the AF updater because `r4` has no AF object. The mapper source
pair remains `(0,0)`. This is a context-fixture limitation for the named
producer test, not evidence of a missing peripheral. Continue only with a
valid guest AF context or context construction. See F-280 and Lane 3.

**F-281 qualifies the 6/7 interpretation:** action 45 explicitly supplies
input 0 to the helper for both plain Auto-area and animal Auto-area, so that
path does not use 6/7 to distinguish those modes. Another caller supplies 1
when an AF record field is 2 or 3 under additional gates; the record source
and meaning remain unknown. Standard USB PTP events cannot expose that
internal record, so another USB window is low value for this question. The
next useful static step is tracing the alternate record's producer only if
it changes the auto-arm state or hook decision. See F-281 and Lane 3.

**F-282 bounds the AF callback in QEMU:** after synthetic live-view setup,
the native Auto-area setter returned success for value 600, but the event
callback still returned before the AF updater with a null AF object; source
pair `(0,0)` was unchanged. The current QEMU fixture therefore does not
create this context from ordinary live-view setup plus AF-area selection.
This is not camera-side evidence. Only pursue more QEMU work if a native
AF-object constructor or registration path can supply the context without
inventing device behavior. See F-282 and Lane 3.

**F-283 tests dispatcher initialization ordering:** combined mask `0x801`
runs bit-11 initializer `0x10078c50` before AF callback `0x10074492`, yet the
callback's AF-object lookup remains null and the status pair stays unchanged.
The initializer is not sufficient to construct the missing fixture context.
Trace the object-list producer/registration consumed by `0x101885e8` before
another simulator run. See F-283 and Lane 3.
