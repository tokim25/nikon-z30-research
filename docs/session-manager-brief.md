# Session-manager brief (read first, updated 2026-10-17)

## Engineering route update, 2026-10-17

Lane 3 F-202 resolves the candidate's playback-Protect separation statically
and corrects its candidate-side start/stop status cycle. The action changes
only shooting assignment `0x1184`; Protect remains `0x1186`, while movie-mode
`0x1187` is not handled. The candidate publishes the native tracking pair
through the existing locked setter after a handled request. A bounded
memory-only QEMU cycle now takes start then stop without an injected status
fixture; this does not prove physical input, AF acquisition or camera
lifecycle. The updated private source assembles/links and passes the bounded
ABI/frame audit. F-203 records the subsequent private standalone-EG image,
which passed exact-span, protected-header, capacity and native-CRC read-back
checks. It has not been loaded by QEMU or accepted by Nikon's updater.
Remaining candidate-side runtime controls, hardware readiness and exact
camera-write approval remain open. Details:
[tracking cycle review](tracking-cycle-review.md).

F-191/F-192 conclude the public same-camera 65:24 profile is not a drop-in:
it uses area 2, persisted profile state and a grid reference, whereas our
target replaces stored 1:1 in area 4 and requires black bars. Keep our area-4
feature contract. F-193 identifies a same-firmware return-address whitelist
for generic preview getters that overlaps our capture-builder/scaler callers;
it is a usable reference for the getter hooks after area-4 selector/ABI
validation. The public direct-buffer hooks are not caller guarded, and local
F-171 found those constructors are shared with object rebuilds. F-194 finds
the wrapper's saved outer LR at `[sp,#36]` at the first table hook, allowing a
specific caller guard. F-195 disqualifies the dimension-based creator itself
as a hook; its body has no capture discriminator. F-196 corrects the earlier
negative-reference claim: the creator is called from helper `0x1021d946`,
which is directly invoked by dispatcher `0x1021d9e2` when flag bit 20 is set.
F-197 finds the dispatcher is registered through shared callback machinery;
its key/flag semantics remain unknown. F-198 applies the documented owner
waiver for still-photo guard side effects and builds a complete, private
area-4 table-only candidate: 176 exact spans, unchanged file length, native
CRC and independent exact-diff/layout checks pass. The candidate changes only
area-4 preview dimensions and may affect playback, movies or warnings; that
risk is accepted but unmeasured. Lifecycle condition 1 remains unmet and
hardware remains NO-GO. See [preview map](native-xpan-preview-callers.md) and
[build architecture](native-xpan-build-architecture.md).

F-201 records the owner's reaffirmation of the still-photo guard waiver after
reviewing the unresolved capture-path specificity. The waiver and its
unmeasured side effects remain in effect; lifecycle condition 1 is still
unmet, and this decision does not authorize camera contact or a write.

## Codex resumed build work, 2026-10-17

The owner asked Codex to devise and pursue the camera-loadable patch, not
delegate to Claude. F-198 has produced a private standalone-EG candidate from
the exact verified original. Its complete 176-span manifest and independent
exact-byte/CRC/layout audit are recorded above and in
[handoff-codex.md](handoff-codex.md). This avoids the unresolved outer-package
digest branch but does not prove Nikon updater acceptance. The candidate stays
offline; lifecycle condition 1 remains unmet, and camera contact/write
remains prohibited. Older entries below describe the chronological research
that led to the candidate and are not the current build status.

### Historical preview-trace log (F-169–F-189)

F-169 corrects the earlier preview target: slot 4's stock small/large
allocations are 480×480 and 1080×1080. The candidate heights fitted from the
verified 5200×1920 still are 176 and 400 (nearest multiple of four), retaining
native row strides 960 and 2160. Upstream's 640×236 / 1920×708 values belong
to area 2 and must not be used for this area-4 patch. F-170 executed all
three native direct-buffer constructors with synthetic data. Hook ABI,
capture-only routes, allocation bounds and playback guards remain open. See
[caller map](native-xpan-preview-callers.md). No candidate or camera access.

F-170 now confirms all three direct-buffer constructors return under
synthetic slot-4 calls with proposed 480×176/1080×400 dimensions; the fixed
thumbnail fields remain unchanged. The first two use area-4 records; the
third consumes a nested slot-4 record whose area guard is still unknown. A
shared-table mutation also changes area-0 output, so a guarded private shadow
table is required. Output records are not yet a capacity proof, and no exact
hook ABI/capture guard has been approved. Continue with those contracts
before candidate construction.

F-171 finds that the `0x10142d86` constructor's shared wrapper has three
direct callers, including preview/object-rebuild contexts whose capture role
is unknown. Area-4 gating alone is not enough. The next review must prove the
exact capture callers and retain stock behavior for generic/old-photo paths.

F-172 rejects the full nearby 10 KB zero span as free space because it has
many existing pointer targets. A 1,642-byte aligned zero subspan at
`0x1002d996–0x1002e000` has no direct pointer or scanned Thumb branch and
MOVW/MOVT references; section boundaries, computed uses and executable
mapping remain unproved. Do not place code there until those are checked.

F-173 follows direct preview wrappers upward. The observed enclosing paths
construct or rebuild objects from current records; even the path gated on
type byte 0x24 is not proved to be new-still capture. No capture-only producer
is established. The build design now considers a bounded EG-tail code append
plus a nearby branch veneer as an alternative to depending on a large
unverified cave; loaded extent, exact veneer space and hook ABI still need
validation.

F-174 identifies complete four-byte patch windows near all five direct-buffer
hooks. Each is within about 1.1 MiB of the candidate zero subspan, so a local
Thumb-2 BL veneer is reachable. An LLVM synthetic check confirms an
eight-byte register-preserving literal veneer can reach an appended Thumb
stub. This is encoding geometry only; executable mapping, displaced
instructions, hook ABI and capture guards remain unproved.

F-175 computes the appended-code start at `0x1207e038` immediately before the
original CRC (`0x1207e039` as a Thumb pointer). The parser's known destination
span ends at `0x12960000`, leaving over 9 MB of capacity. This sizes the
candidate append but does not prove executable mapping or runtime acceptance.

F-176 maps string IDs 1454 and 1456–1458 in all 36 language blocks and records
144 length-preserving UTF-16 edits in a private manifest. It is text-only and
not a candidate; preview hooks, metadata/version handling, geometry edits and
the rest of the exact manifest are still open.

F-177 rejects the `0x1021e7a8` call to `0x10143862` as a capture-only guard:
it belongs to a routine that attaches or reuses record-linked preview objects.
The routine's entry has no direct whole-image branch caller; indirect dispatch
remains untraced. Continue on the other preview producer paths, not this
object-lifecycle route.

F-178 consolidates the text and proposed geometry edits as a private
160-span exact data manifest, applied and checked only in memory. No firmware
candidate was written. F-179 finds no tested direct PC-relative reference
form to the type-`0x24` registration table; base-relative/indirect dispatch
remains unresolved. Preview hooks, bars payload, metadata policy and complete
candidate integrity checks remain open.

F-180 follows the native image-record builder to shared object materialization
and refresh routes, not a proven new-still boundary. The record's area and
preview selector do not supply capture provenance. The next research step is
to trace a newly captured still's record producer into this builder or identify
a per-record source flag; do not patch this shared path yet.

F-181 validates the original's CRC-16/XMODEM trailer and adds an in-memory
composer/auditor covered by synthetic tests. It supports exact same-length
spans and an optional bounded append before the CRC, while protecting header
metadata. It has not processed a real candidate. Capture provenance and the
offset-0x24 version-policy consumer remain open.

F-182 applies the present F-178 text/geometry manifest to the verified input
in memory and passes exact-span, length and CRC checks; the incomplete result
was discarded. No candidate exists. Preview/capture provenance and the full
feature manifest remain the active blockers.

F-183 adds a strict parser for complete private manifests and 14 synthetic
composer tests; the plan's complete/reviewed marker remains a declaration,
not proof of semantic review. F-184 follows the dimension-based preview
adapter into preview-object construction and attachment, but its dispatch
source is unresolved and it is not a proven still-capture hook. Resume by
tracing a new-still producer into a preview constructor. Do not emit a feature
candidate while capture scoping and offset-0x24 metadata policy remain open.

F-185 adds a private exact-manifest-hash build writer with the verified-original
gate, repository-path rejection, no-overwrite output, and read-back audit.
Four synthetic filesystem tests pass; the complete suite is 148 tests. It has
not processed the real original or any complete feature manifest. The next
action remains tracing capture-specific preview construction and resolving
metadata policy; no candidate or camera write is authorized.
F-186 verifies the writer creates candidates with owner-only `0600` mode.
F-187 verifies the real-source builder gate refuses the current incomplete
manifest before creating an output.
F-188 confirms offset `0x24` contains printable version-like text and reaches
formatter calls in post-CRC selector-based policy handlers, but the standalone callback's
comparison semantics remain unknown. Preserve it exactly while tracing that
handler and a fresh-still preview producer.
F-189 merges the existing exact F-148 bars overlay into the private data
manifest: 172 spans now pass source/hash/non-overlap, unchanged-length and
native-CRC checks in memory. The temporary output was discarded. Preview
hooks remain the missing feature spans; the merged plan is still incomplete.

## Codex update, 2026-10-17

F-162 resolves the large crop rectangle as 5200x1920. F-163 statically
confirms that standalone EG discovery type 2 takes the native CRC path and
bypasses the unresolved outer-package digest used for encoded body-package
type 4. The outer digest is therefore not a blocker for a standalone-EG
candidate. This does not establish camera acceptance or readiness. F-165
validates the proposed all-size geometry through the full native builder in
pinned QEMU with synthetic guest data, and F-166 closes parser capacity and
the offset-0x10 field rule. Remaining pre-build work: complete localized
label/size text and embedded-preview records/selectors, preserve and verify
the offset-0x24 metadata, then build and preflight an exact local candidate.
See
[route contract](native-standalone-eg-route.md). Hardware remains NO-GO.

Read this before any other doc. It is the short state of the project. Deeper
detail lives in the linked docs; open them only when a step needs them.

## Owner rules (approved 2026-10-17)

- Read-only identification of the Z 30 is pre-approved. Any camera write needs
  the owner's approval for that exact step, in one reply.
- Firmware bytes stay on the owner's local machine; never in git or a PR.
- Simulator work (pinned QEMU 10.2.4) is pre-approved. No camera contact, no
  flashing, no installation workflow from simulator work.
- Owner may waive named gates for the camera-test stage, with a reason.
- Full rules: [proposed-rules-2026-10-17.md](proposed-rules-2026-10-17.md).

## Hardware and identity

- Camera: Z 30 reports firmware V1.20 (read-only check, gphoto2 --summary).
- Original firmware: Z_30_0120.bin in the owner's Documents folder; SHA-256 and
  size match the pinned original. A scratch working copy exists outside the repo.
- Byte-exact identity: WAIVED by owner ("I assume the risks"). Recorded in
  [test-readiness-2026-10-17.md](test-readiness-2026-10-17.md).
- gphoto2 is NOT read-only as shipped (write-capable calls). Do not use it
  beyond the identity query without a reviewed command and owner approval.
- Hardware status: NO-GO for modified firmware. A private offline candidate
  exists, but is not marked READY or authorized for camera use.

## Owner dispositions (2026-10-17)

- Lifecycle condition 1: **unmet**. The owner's latest disposition explicitly
  keeps this gate unmet; earlier text describing it as waived is superseded.
- XPan still-photo guard: waived; risk accepted (crop lines may appear during
  movies, playback, or warnings).
- Byte-exact identity: waived.
- Tracking activation/physical input: simulator verification is not available;
  owner directs that this behavior be tested with the tracking patch on the
  real Z 30. This is a test disposition, not evidence of activation, package
  acceptance, readiness, or approval to write the camera.

## Feature status

| Feature | Status | Blocker |
|---|---|---|
| XPan crop (bars, geometry, label) | Private offline candidate built | Candidate SHA-256 `6614df3a…cadb6a1`; complete 176-span manifest and independent exact-diff/CRC/layout checks pass. Native modified-file acceptance and real-camera behavior remain unverified; lifecycle condition 1 remains unmet. |
| Tracking (AE-L/AF-L) | Private design/manifest only | Menu stores 77 and candidate allocation/constructed ABI controls pass. Physical press-to-start/stop remains unverified and is assigned to the eventual tracking-patch device test. Not built or ready. |
| Saved crop files | Not testable yet | Depends on XPan; needs real-camera test |

## Research that is closed or parked

- Saved-crop static research: closed (getter callers, filename trace: not found).
- Tracking static search (property 0x2021 consumer): not found. Stack and
  placement of 424-byte candidate: passes on paper (dfad2ef).
- Still-photo predicate: unresolved at hook 0x102f5810 (F-150).
- Outside repos (WonderLantern z30-qemu, bullton/nikon): no help for blockers.

## Simulator facts (QEMU 10.2.4, pinned)

- Works: stock menu/live-view paths in assisted profile; area pick; bars hook
  on live-view start (F-101 line); guest memory writes via debugger.
- Cannot: press AE-L/AF-L, press shutter, use i-menu, write saved files,
  model natural startup fully.
- F-079 method (repoint RAM area table at 0xc18c7de8 to scratch records) is
  not reproducible here: its script is in a private WORK folder not on this
  machine.

## Codex lane (owner-directed)

- Uncommitted work on codex/firmware-preflight-plan: fact numbers collide with
  main; Codex must renumber before commit.
- Codex owns simulator runs with pushes and merges; Claude does static
  research and tidying.

## Next actions (in order)

1. Preserve the verified original, candidate and firmware-derived manifest in
   owner-only storage outside Git; retain the files privately and do not
   attach or distribute them. Exact filesystem locations stay out of Git.
2. If offline candidate testing continues, first determine whether the
   existing pinned-QEMU harness can load this exact standalone EG without
   changing the pinned simulator. F-200 answered no: the launcher and QEMU C
   loader enforce the stock-image hash before boot. Record this single
   simulator limitation and drop that test path; do not weaken the guard or
   modify QEMU. Do not resume the superseded capture-hook trace or promote
   hardware readiness; lifecycle condition 1 remains unmet.
3. No camera contact or write is authorized by this candidate work.
4. Tracking's physical press and activation are assigned to the eventual
   tracking-patch test on the real Z 30 by owner direction. This test remains
   later than the first XPan test and requires an accepted patch format,
   exact-build review, backup/risk binding, and separate approval naming the
   exact camera write.
5. Do not restart closed research threads without new evidence.

## Branches (all local or pushed, none merged)

- claude/lane2-filename-trace-981f75, claude/lane3-family-search-2ded1d,
  claude/eloquent-napier-52e1c8, claude/owner-rules-2026-10-17 (rules commit
  9a495c4, local), claude/xpan-stills-route-94393a (readiness record).
