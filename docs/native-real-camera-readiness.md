# Readiness for a future real-camera test

2026-10-17. **Modified-firmware test: NO-GO.** This report authorizes no
camera operation and contains no installation procedure. Current rules are
[AGENTS.md](../AGENTS.md) and [build-phase-gate.md](build-phase-gate.md).

Latest transfer update: review the native standalone-EG route recorded in
[Claude's consolidated handoff](native-claude-build-research-handoff.md)
before extending the outer-package digest investigation below. That separate
format may remove the outer digest dependency; its complete contract remains
unverified. No complete candidate or READY record exists. The older
minimum-test section describes the outer-package route, not proof that every
native format requires its missing input. Hardware NO-GO is unchanged.
Later main records owner waivers for lifecycle, still-photo guard and installed
byte-exact identity in session-manager-brief.md/test-readiness-2026-10-17.md.
Those supersede earlier retained-gate wording below, without changing absent
measurements or granting hardware approval. Local original-hash checks remain
required; the installed-identity waiver does not waive them.

## Minimum-test stopping point

Latest owner direction: do not pursue simulator completeness or low-value
research. Use the existing bounded evidence to prepare the smallest justified
stills-only XPan test; record unmeasured behavior as residual risk. Do not
expand tests merely to explain missing simulator behavior. This changes the
work priority; it does not turn missing measurements into passes or authorize
camera access. The earlier explicit decision to retain lifecycle condition 1
has not been silently reversed.

**Smallest next technical blocker: reproduce the native package digest.**
F-161 now verifies native compression and suffix-loop arithmetic against
synthetic controls and adds a baseline-first read-only digest verifier.
Those checks do not recover the suffix or reproduce the original digest.
See [arithmetic verification](native-digest-arithmetic-verification.md).
The known additional check consumes an eight-byte input at `0x10000088`,
outside the captured EG module. F-140/F-141 already locate this missing-input
boundary. The original round trip and CRC checks do not cover it. There is
no accepted final modified camera package to approve while this remains
unresolved. See [digest inputs](native-updater-digest-inputs.md) and
[mapping boundary](native-boot-mapping-boundary.md).

The single next technical step is to supply that independently verified
input from an authorized offline source, or establish a verified equivalent
that reproduces the original digest check. No such source is identified in
the current record. Do not guess bytes, substitute simulator defaults, reuse
the original digest for changed content, alter the validation-path flag, or
start another literal-search/mapping loop. The prior identity-only camera
permission does not authorize memory acquisition to obtain it.

Once that blocker is resolved, the finite remaining preparation is:

1. Bind one XPan-only candidate to its exact original, edit manifest and
   final package hash; independently check only planned changes, component/
   container integrity, native digest and installation bounds.
2. Finish review of that exact candidate's layout/call behavior for the
   named test. Record the remaining guard/lifecycle uncertainties and obtain
   the owner's concrete disposition of the retained lifecycle gate; do not
   resume open-ended simulator work.
3. Bind the verified original backup, bounded observations/stop rules and
   service-or-total-loss risk acceptance to that build. When the required
   gate decisions and checks are complete, name the test in
   `hardware-readiness.md` and mark it READY FOR AN EXPERIMENTAL HARDWARE TEST.

**Stop immediately at that readiness point.** Report the exact package
hash, test scope and residual risks, then request separate immediate owner
approval before any camera action. No camera instructions or operation are
part of this preparation. Current stopping point is instead **blocked on
the missing digest input, not READY**; the other outstanding gates below
are not claimed complete.

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
- The owner explicitly chose to keep lifecycle condition 1 unmet. No
  simulator-coverage exception or modified-test approval was granted.

Reference overlay manifest SHA-256:
`5a933892e98effb0ba114adc1ad0e3a4be40daf2cac021df73e8bc1661ef37c9`.
This is a diagnostic-overlay identity, not a camera-package identity.

## Unmet gates and exact blockers

| Build gate | What still prevents acceptance |
| --- | --- |
| 1. Relevant simulator transitions without debugger memory writes | Natural startup, genuine menu return, playback and warning exclusion remain unproved. Assisted calls and finer-stepped confirmation do not fill this gap. The owner retained this requirement. |
| 2. Exact original and only planned changes | No final modified camera package has passed independent exact-edit/container/integrity checks. The additional native digest remains unreproduced because an eight-byte input at `0x10000088` is unmapped. |
| 3. Exact-build code review | Finite ABI/layout checks pass, but global acceptance is not established. No proven still-photo eligibility guard is available; empty stack plus selector 1 does not guarantee protection of excluded states. |
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
native tracking. This blocks tracking-enabled firmware, not an XPan-only
candidate containing no tracking edits. See
[tracking audit](tracking-entry-research.md) and
[input-chain limits](tracking-input-chain.md).

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

The next hardware-related owner confirmation is closure of the existing
read-only session. There is no modified-test approval to seek while the
retained lifecycle gate remains unmet. When every required gate is met,
the owner must approve the exact build/package hash, bounded test scope,
stop rules and service-or-total-loss risk immediately before personally
performing that test. General “Go,” version identification and earlier
general risk acceptance do not substitute for that decision.

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

Preparation of this report involved repository review only: no simulator,
patch encoding/build, camera connection, power-cycle, configuration or flash.
