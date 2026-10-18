# Readiness for a future real-camera test

2026-10-17. **Modified-firmware test: NO-GO.** This report authorizes no
camera operation and contains no installation procedure. Current rules are
[AGENTS.md](../AGENTS.md) and [build-phase-gate.md](build-phase-gate.md).

**Current 2026-10-17 addendum:** the private offline XPan stills candidate and
its 176-span manifest now exist; see [Codex handoff](handoff-codex.md) and
[fact F-198](facts.md). Exact edits, protected fields, unchanged length,
native CRC, capacity and preview-table layout pass an independent read-back
audit. This does not establish Nikon updater acceptance or hardware behavior.
Lifecycle condition 1 remains **unmet** by the owner's latest disposition;
older statements below that call it waived are superseded. Hardware remains
NO-GO, and no camera contact or write is authorized.

The native standalone-EG route is documented in
[native-standalone-eg-route.md](native-standalone-eg-route.md). A private
offline candidate now exists, but no READY record exists. The historical
outer-package digest investigation below applies only to that alternative
format; it does not block the standalone-EG candidate. Hardware NO-GO is
unchanged.

**F-163 correction:** bounded static decode resolves the branch for the
standalone format. Standalone EG is discovery type 2 and selects native CRC
validation; the unresolved 20-byte digest branch is selected for encoded
body-package type 4. The missing eight-byte input does not block the
standalone-EG route. F-198's private candidate passes parser-capacity and
compatibility-field preservation checks, but native updater acceptance and
hardware readiness remain unverified.
See [native route contract](native-standalone-eg-route.md). Hardware NO-GO is
unchanged.
The owner waived the XPan still-photo guard and accepted possible area-4
playback/movie/warning side effects. The latest disposition keeps lifecycle
condition 1 unmet; earlier lifecycle-waiver wording below is superseded.
Installed-firmware byte identity remains waived at version level only. The
private extracted EG source itself passes the exact size/SHA-256 verifier.

## Minimum-test stopping point (historical F-163 review; superseded by F-198)

Latest owner direction: do not pursue simulator completeness or low-value
research. The latest state and risk decisions are recorded in the addendum at
the top of this file and in session-manager-brief.md. Lifecycle condition 1
remains unmet; the still-photo guard side-effect waiver is separate and does
not authorize camera access.

The outer-package digest remains unresolved. F-161 verifies native
compression and suffix-loop arithmetic against synthetic controls, but does
not recover the suffix or reproduce the original digest. The check consumes
an eight-byte input at `0x10000088`, outside the captured EG module. F-163
establishes that standalone EG discovery type 2 selects native CRC validation,
while the digest branch is selected for encoded body-package type 4. The
missing input does not block a standalone-EG candidate. The private candidate
passes the recorded parser-capacity and protected-field checks, but Nikon
updater acceptance remains unverified. See [digest
inputs](native-updater-digest-inputs.md), [mapping
boundary](native-boot-mapping-boundary.md), and [standalone
route](native-standalone-eg-route.md).

If using the outer-package route, supply independently verified input from
an authorized offline source or establish a verified equivalent that
reproduces the original digest. Do not guess bytes, substitute simulator
defaults, reuse the original digest for changed content, alter the
validation-path flag, or start another literal-search/mapping loop. The
prior identity-only camera permission does not authorize memory acquisition
to obtain it. The private candidate's parser capacity and protected fields
have passed offline checks; Nikon updater acceptance remains unverified.

At the time this historical stopping-point plan was written, the standalone
parser contract and full edit manifest remained unfinished. F-198/F-199
supersede those build steps. Remaining hardware gates are:

1. Bind one XPan-only candidate to its exact original, edit manifest and
   final artifact hash; independently check only planned changes, standalone
   parser compatibility/capacity, native CRC and installation bounds. The
   outer digest applies only if the outer-package route is chosen.
2. Review the exact candidate's residual behavior for a future named test.
   Lifecycle condition 1 remains unmet; do not describe it as waived.
3. Bind the verified original backup, bounded observations/stop rules and
   service-or-total-loss risk acceptance to that build. When the required
   gate decisions and checks are complete, name the test in
   `hardware-readiness.md` and mark it READY FOR AN EXPERIMENTAL HARDWARE TEST.

**Stop immediately at that readiness point.** Report the exact package
hash, test scope and residual risks, then request separate immediate owner
approval before any camera action. No camera instructions or operation are
part of this preparation. That historical stopping point was superseded by
F-198/F-199: a private offline candidate and manifest now pass exact-byte,
layout and CRC checks. The candidate remains **not READY** because lifecycle
condition 1 remains unmet, Nikon updater acceptance is unproven, recovery/risk
records remain open, and separate immediate approval for any camera write has
not been given. The outer-package digest does not block the standalone route.

### Bounded source check, 2026-10-17

The recovered verifier's source identity still matches F-135. Static review
of its function/call structure and recovered provenance identifies original
SHA-256 and CRC checks, not a native package-digest implementation or boot
input. Its pinned upstream
[container reader](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/src/z30_extensions/container.py)
likewise accepts only the exact original and validates decoded structure/CRCs;
it is not an equivalent modified-package verifier.

A focused public-source lookup found
[nikon-fw-key-tool](https://github.com/WonderLantern/nikon-fw-key-tool#checksums-and-header-digest).
It lists Z30 decryption support, but limits digest-key recovery/repacking to
Z8/Z9. Its EXPEED 6 instruction-constant hint is not a verified Z30 solution.
A bounded check of the actual Z30 setup still shows the eight-byte source
at `0x10000088` copied into digest state; no replacement source was established.
No third-party code was installed or executed, and no derived key was guessed.

The owner does not know of an existing boot capture or independent verifier;
do not treat this as a request for the owner to acquire one. No new camera
activity is needed or authorized by this checkpoint. Further progress needs
verified Z30 digest recovery/input evidence rather than repetition of these
source checks. No simulator run, image,
hardware action or readiness promotion occurred.

## Completed prerequisites

- The owner reported the separately authorized identity/version check
  complete through step 5: NIKON DSC Z 30, camera version “1.2,” USB IDs
  04b0/0452. This is consistent with the C 1.20 target, not a hash check of
  installed code. Session closure/disconnection has not been reported.
- The offline original is identified and preserved. Original package
  round-trip, synthetic container/exact-edit checks and the installation-span
  model have passing evidence; this does not validate a modified package.
- The existing F-148 prototype has twelve hashed overlay entries. F-156
  shows controlled rendering and ten setting cycles; F-148/F-160 add bounded
  state/writer/ready/close call-contract evidence.
- The owner's latest disposition keeps lifecycle condition 1 unmet. Natural
  lifecycle coverage remains unproved and no modified-test approval was
  granted. The earlier waiver wording is superseded.

Reference overlay manifest SHA-256:
`5a933892e98effb0ba114adc1ad0e3a4be40daf2cac021df73e8bc1661ef37c9`.
This is a diagnostic-overlay identity, not a camera-package identity.

## Unmet gates and exact blockers

| Build gate | What still prevents acceptance |
| --- | --- |
| 1. Relevant simulator transitions without debugger memory writes | Lifecycle condition 1 remains unmet. Natural startup, genuine menu return, playback and warning exclusion remain unproved. |
| 2. Exact original and only planned changes | Private F-198 candidate passes independent exact-edit, protected-field, length/capacity, native CRC and table-layout checks. Nikon modified-EG updater acceptance remains unverified; the unresolved outer digest applies only to that alternative route. |
| 3. Exact-build code review | Finite ABI/layout checks pass, but global acceptance of a complete candidate is not established. The owner waived the still-photo guard requirement and accepts the risk that bars may show during movies, playback or warnings; this remains unvalidated behavior. |
| 4. Backup and recovery decision | Bind the preserved original backup and service-or-total-loss acceptance to the exact proposed build/test, with its residual risks and stop rules. No verified independent recovery route exists. |
| 5. Named readiness record | `hardware-readiness.md` remains NO-GO; no exact camera build/test is marked READY FOR AN EXPERIMENTAL HARDWARE TEST. |
| 6. Immediate owner approval | Separate approval of that concrete modified-firmware test has not been given. The read-only authorization does not transfer to it. |

The XPan guard review establishes missing exclusion proof, not observed
harm in every excluded state. Movie behavior remains unvalidated and is not
reintroduced as a prerequisite for the owner's offline stills prototype.
Still-photo menu/playback/warning requirements remain open. See
[lifecycle decision](native-xpan-lifecycle-decision.md) and
[guard review](native-xpan-guard-branch-review.md).

The tracking audit has no verified AE-L/AF-L physical press/release-to-native
acquisition contract, reticle/completion/cancellation path or coexistence
acceptance. Synthetic tracking behavior and menu-input traces do not prove
native tracking. The owner assigns those items to the tracking-patch device
test as recorded below. See
[tracking audit](tracking-entry-research.md) and
[input-chain limits](tracking-input-chain.md).

**Owner disposition, 2026-10-17:** because the simulator cannot supply the
physical AE-L/AF-L press, the owner directs that tracking activation be tested
with a tracking-enabled patch on the real Z 30. Treat this as an explicit
unverified test objective, not a passed gate or blanket hardware approval.
Keep the test order (XPan first, tracking alone second, combined third),
package-integrity checks, exact-build review, backup/risk binding and
immediate per-write approval. Tracking remains unbuilt and hardware NO-GO.

## Narrowest first test and owner decision

The narrowest permitted hardware activity was the owner-operated stock
identity/version check described in
[the hardware recommendation](native-hardware-gate-recommendation.md).
It has already been reported through step 5; this report does not request
a repeat or broaden that session. Its closure remains to be reported.

The first **future modified-firmware** test, only after all gates pass,
must follow the existing owner order: one named stills-only XPan candidate
with saved RAW/JPEG crop verification, without tracking edits or combined
features. Saved-crop uncertainty is an on-camera verification item, not an
additional simulator blocker. No concrete hardware package is ready now.

The next hardware-related status item is closure of the existing read-only
session. Lifecycle condition 1 remains unmet; the required
XPan first-test order, accepted package, exact-build review, backup/risk and
stop records still apply. For each write, the owner must approve the exact
build/package hash and bounded test scope immediately before personally
performing it. General “Go,” version identification and earlier general risk
acceptance do not substitute for that decision.

The eventual approval must explicitly identify the final package SHA-256,
the one owner-performed stills-only XPan/crop test, its stop rules and the
accepted possibility of service or permanent loss. It must state that no
tracking or broader hardware activity is included. The final package hash
does not exist in an accepted readiness record yet, so a request to approve
that exact test would be premature. No additional generic risk waiver is
requested at this stopping point.

## Recovery and explicit NO-GO conditions

Recovery is recorded as **accepted service-or-total-loss risk for planning**,
not a safe procedure or a verified recovery path. A preserved original does
not prove it can be restored to a camera that will not start. Service may
fail or be unavailable; permanent loss is possible. Exact-build/test risk
acceptance remains separate under the [recovery plan](recovery-plan.md).

Do not proceed if any required gate above is unmet; the original, manifest,
package or installed-version evidence disagrees; a change falls outside the
reviewed scope; package integrity has unexplained results; tracking is added
without its own acceptance; backup/risk/stop records are incomplete; or
immediate owner approval is absent. Unexplained camera behavior during any
authorized activity ends that activity's approved scope; it does not permit
diagnostic commands, settings changes or improvised recovery.

Preparation of this report involved repository review and bounded static
decode only: no simulator, patch encoding/build, camera connection,
power-cycle, configuration or flash.
