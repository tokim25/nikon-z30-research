# Firmware patch and preflight plan

Proposed 2026-10-17. Planning only: no patcher, modified firmware, update
package or installation workflow was produced. Hardware remains NO-GO.
The feature-specific restriction recorded in
[hardware-readiness.md](hardware-readiness.md) still applies.

## First decision: prove the package path

The simulator loads a decoded EG module. A loader overlay demonstrates code
execution there; it does not demonstrate that a rebuilt camera update
package is valid or accepted. The first offline task should be an audit of
the recovered package verifier, using the already identified private input
locations rather than searching the disk for firmware.

Record the package layout, component boundaries, address-to-file mapping,
decoding/encoding requirements and each integrity check's coverage. Distinguish
checksums from cryptographic authentication. The recovery report establishes
that checks passed for the original, not that modified packages can be made
acceptable. If authentication needs an unavailable signing key, record that
as a feasibility blocker; do not assume recomputing checksums solves it.

The audit is read-only research. Implementing a package writer is a later
build step, subject to the existing gate. Before adding feature changes,
require an unchanged decode/re-encode round trip that reproduces the original
package exactly. Any difference needs an understood explanation and an
explicitly reviewed acceptance rule; unexplained differences fail.

## Proposed build contract

1. Verify both the original package and decoded EG against their complete
   sizes and SHA-256 identities in [milestone-1-recovery.md](milestone-1-recovery.md).
   The existing `require_verified_eg_module` covers EG only. Verify the same
   captured input used for building so a later file change cannot evade the
   identity check. Refuse unsupported versions and already modified inputs.
2. Use a reviewed manifest of named changes with exact component, offset,
   extent and purpose. Keep any original-byte comparisons and concrete
   firmware-derived patch material outside Git. Reject overlapping edits,
   out-of-bounds writes, ambiguous address mapping and unexpected lengths.
3. Preserve the original; write a fresh candidate outside the repository.
   Refuse overwrites. Never leave a partially written file labelled verified.
   Repeated builds from identical inputs and pinned tools must match.
4. Independently compare original and candidate. All module changes must be
   inside approved spans; container changes must be limited to the explained
   encoding and integrity consequences. Confirm other components remain
   unchanged after decoding. A patcher's own success message is insufficient.
5. Decode the completed package again with a separately reviewed read path.
   Check structure, lengths, integrity fields and exact equality of its EG
   with the intended patched module. Use that extracted module for simulator
   acceptance, tying the simulation evidence to the final candidate hash.

Public tooling and tests must contain only original project code and
synthetic fixtures. Test malformed packages, wrong identities, overlapping
edits, truncated input, corrupted output, repeated application and failed
writes before using restricted inputs locally. Recovered tools require the
license and embedded-material review noted in the recovery report before reuse.

## Code and behavior review

Review every inserted instruction and displaced instruction: ARM/Thumb mode,
alignment, branch reach, literal pools, register and condition-flag preservation,
stack alignment/depth, return paths and calling context. Zero-filled space is
only a candidate until its mapping, ownership and integrity coverage are
understood. Include concurrency, repeated entry and unsupported-state behavior.

Compare stock and candidate in fresh runs of the pinned simulator. Exercise
startup, area changes, menu entry/return, repeated transitions, disabled-feature
controls, focus graphics and reboot wherever modeled. Mark diagnostic calls
and absent hardware behavior explicitly; an unavailable check stays unverified.

For the first owner-approved feature scope, XPan bars and saved crop together,
require evidence for RAW and JPEG dimensions, crop placement, metadata and
file decoding. A crop descriptor alone cannot establish saved-file correctness.
If the simulator cannot produce those files, record the precise limitation
and any proposed deviation for owner decision rather than claiming a pass.
Tracking remains a separate later build, followed by the combined build.

## Review packet before any hardware decision

Record source and candidate hashes, tool revisions, manifest identity,
independent diff result, package checks, code review, simulator results and
each unverified behavior. Name the exact feature scope and stop criteria.
Keep the original backed up offline and distinguish a backup from a verified
recovery mechanism. If recovery remains unknown, record the service-or-total-loss
risk required by [recovery-plan.md](recovery-plan.md).

Only after those records exist should readiness be reassessed for that exact
candidate. The owner's separate approval immediately before any hardware step
is still required. Offline checks cannot prove camera acceptance, hardware
timing or recovery after a failed update.

## Immediate next step

The read-only audit and unchanged in-memory round trip passed on 2026-10-17;
see [native-package-verifier-audit.md](native-package-verifier-audit.md), F-135.
The decoded-container reader is implemented and tested in F-136; see
[native-container-validator.md](native-container-validator.md).
The exact-edit comparison is implemented and tested in F-137; see
[native-exact-edit-audit.md](native-exact-edit-audit.md).
F-138 composes those checks into a read-only decoded-container preflight;
see [native-combined-preflight.md](native-combined-preflight.md).
F-139/F-140 identify the native body-package path and extra digest check;
see [native-updater-digest-inputs.md](native-updater-digest-inputs.md).
F-141 finds no source for that input in the checked startup mappings and
resolves the updater block's relocation; see
[native-boot-mapping-boundary.md](native-boot-mapping-boundary.md).
F-142 traces native erase/program/readback paths and the initialized full
installation span; see [native-install-span.md](native-install-span.md).
F-143 adds that installation-span model and synthetic tests to preflight;
see [native-installation-model.md](native-installation-model.md).
F-144 reviews both existing private overlay revisions and finds a residual
state-wrapper stock-call stack displacement; condition 3 does not pass. See
[native-xpan-contract-review.md](native-xpan-contract-review.md).
F-145 implements that abstract contract checker and synthetic tests; see
[native-call-contract-tests.md](native-call-contract-tests.md). This does not
approve actual instructions. F-146's private textual layout fits in 48 of
52 available bytes, with a required writer relocation; see
[native-xpan-layout-proposal.md](native-xpan-layout-proposal.md). Next: a
throwaway simulator-only ABI-remediation experiment, final decode and
entry/return comparison against the unwrapped service. F-147 completed that
experiment: the stack correction passes, but an other-state NZCV return
mismatch fails the strict contract. See
[native-xpan-abi-experiment.md](native-xpan-abi-experiment.md). Next: review
and test flags-preserving remediation in the pinned simulator. F-148 resolves
the measured stack/flag contracts in bounded paired diagnostics; see
[native-xpan-flags-remediation.md](native-xpan-flags-remediation.md). Next:
return to the actual saved RAW/JPEG crop gap. F-149 verifies initialized RAM
addresses for the filename-pointer tables and begins that trace; see
[native-save-table-ram-mapping.md](native-save-table-ram-mapping.md). Next:
establish actual filename-field consumption toward file creation. No camera build.
Camera-side validation remains
unverified; no installable patch format or feature package writer is approved
by this result.
