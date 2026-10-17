# Combined decoded-container preflight

2026-10-17. F-138. Newly written `src/nikon_z30_research/preflight.py`
composes the F-136 container validator and F-137 exact-edit auditor. It
operates on immutable bytes in memory and writes no firmware or reports.

## Contract

`preflight_decoded` accepts original/candidate decoded containers, an
independently trusted original size/hash, original component specifications,
an explicit tuple of changed component names, and the exact edit manifest.
It accepts no precomputed pass/fail results. Every original component must
have its full hash pinned.

The function runs original identity and exact-edit checks, validates the
original container, restricts edits to individually declared components or
the two container-CRC bytes, then validates the candidate with unchanged
component hashes retained. It rejects edits crossing component boundaries,
header/directory/trailer-padding edits, unknown or duplicate change permissions,
and declared changed components that actually remain unchanged. Resizing is
already rejected by the edit auditor.

Candidate checks and report hashes refer to the same immutable inputs used
by the edit audit. There is no interface for submitting a separately checked
candidate's report. A deterministic policy hash covers the version, decoded
scope, exact-edit manifest identity, complete original component policy and
declared component permissions. The report also retains original/candidate
container reports and the edit report, exposing their hashes and counts.

The report always identifies its scope as `decoded_container_only` and
hardware readiness as `not_established`. A returned report means these
offline checks passed. It does not authorize hardware access or prove the
edit policy itself correct. Callers must retain the independent policy and
code revision used for review; a hash is an identity, not a signature.

F-143 adds an optional installation policy and nested static span report;
see [native-installation-model.md](native-installation-model.md). It models
one validated component and includes the complete policy in report identity.
When omitted, `installation=None` explicitly records that absence. Hardware
readiness remains not established.

## Evidence

Twelve synthetic integration tests cover a modified-container pass, the
unchanged baseline, original identity mismatch, missing component hashes,
unknown/duplicate/malformed permissions, undeclared edits, unused permissions,
cross-component spans, header edits, wrong CRCs despite matching edits, a
different candidate reusing an old plan, and policy/report binding.

The private round-trip helper also invokes the combined preflight on the
original decoded container versus itself, after the recovered verifier has
validated the original package and all component identities. All component
hashes stay pinned and the empty manifest reports zero changed bytes. The
decoded original identity for that baseline is computed from the original
validated input, not from a modified candidate. This is an unchanged baseline,
not a test of modified real firmware. The original file and recovered tools
remain unchanged; no firmware image was written.

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -p test_preflight.py -v
PYTHONPATH=src python3 -B "$WORK/codex-package-roundtrip-audit-private.py"
```

## Next real-build decision

The offline decoded-container checking chain is now implemented. Next audit
the real updater's validation boundary using read-only local evidence: where
it checks package/component integrity, compatibility/version and any
authentication, and which bytes become installed executable code. Start from
already identified local sources or firmware references; do not assume the
desktop verifier implements the camera's checks. Record missing evidence
explicitly rather than treating this preflight as camera acceptance.

F-139 has now identified the native body-package path and an additional
20-byte digest comparison outside this API's scope; see
[native-updater-validation.md](native-updater-validation.md).
F-140 traces its encoded-format selector and message boundaries; see
[native-updater-digest-inputs.md](native-updater-digest-inputs.md).
The eight-byte source at `0x10000088` remains unmapped. This API continues
to report decoded-container-only validation.

Runtime-to-file address mapping and instruction-level hook review remain
separate prerequisites before a concrete patch is approved. Natural feature
transitions and saved RAW/JPEG crop evidence remain unresolved. Hardware
stays NO-GO. No commit, push or PR was made.
