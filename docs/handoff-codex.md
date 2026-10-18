# Codex handoff

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

## Rules, unchanged

Offline/simulator only. Never touch a real camera. Never commit firmware
bytes, dumps, or patched images, anywhere, ever — this applies doubly to
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
