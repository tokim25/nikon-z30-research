# Exact-edit audit

2026-10-17. F-137. Newly written read-only code in
`src/nikon_z30_research/patch_audit.py`; synthetic tests in
`tests/test_patch_audit.py`. No real firmware edits or image writes.

## Contract

`audit_exact_edits` receives immutable original/candidate bytes, the original's
independently trusted full size/hash, and an ordered tuple of `ExactEdit`.
Each edit specifies a label, file offset, length, original-span SHA-256 and
replacement-span SHA-256. Concrete firmware-derived manifests stay private.
Offsets are relative to the supplied file/module, never runtime addresses.

The function verifies original identity first, requires equal input lengths,
rejects malformed, empty/no-change, overlapping or out-of-order edit spans,
checks both hashes for every complete span, and compares every intervening
and trailing byte. An empty manifest permits only an unchanged candidate.
Adjacent edits and edits at either file boundary are allowed.

A broad span grants no freedom to alter other bytes inside it: the digest
pins the complete replacement. Required edits cannot be omitted or partially
applied. Checksum fields receive no automatic exemption; changed checksum
bytes need an exact planned edit just like code or data. CRC correctness
remains the responsibility of the decoded-container validator.

The immutable report contains original/candidate hashes, a deterministic
versioned manifest hash, file size, edit count and actual changed-byte count.
It contains no raw bytes or labels. Errors likewise do not echo payloads or
labels. An edit policy must come from an independent reviewed plan, not from
hashing an untrusted candidate and declaring its contents approved.

## Evidence

Fourteen synthetic tests cover exact acceptance, determinism, boundary and
adjacent edits, changes in every gap, extra edits inside a broad planned span,
missing/partial/wrong replacements, wrong originals, reapplication, insertion
and deletion, invalid identity/manifest fields, mutable input and error output.

The combined test uses an invented decoded container with a changed payload
and regenerated CRCs. The exact planned component passes both checks. A plan
allowing only the payload byte rejects the checksum changes. Conversely, a
candidate matching that payload-only plan passes the edit audit but fails
component CRC validation. This checks the two tools' separate responsibilities.

The private round-trip helper also audits the verified original package
against its identical in-memory reconstruction using an empty manifest.
It reports zero changed bytes. The decoded-container validator and unchanged
round trip still pass; the original file remains unchanged. This is an
unchanged-input baseline, not a real modified-firmware validation.

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -p test_patch_audit.py -v
PYTHONPATH=src python3 -B "$WORK/codex-package-roundtrip-audit-private.py"
```

## Limits and next step

These checks establish compliance with a supplied edit policy and checksum
format, not correctness of that policy, instruction semantics, address
translation, camera authentication, updater behavior or recovery.

F-138 composes identity, both container checks, unchanged-component pinning
and exact edits into one report tied to the same immutable inputs and full
policy identity; see [native-combined-preflight.md](native-combined-preflight.md).
Its scope remains offline decoded-container validation, with hardware readiness
not established.

No commit, push or PR was made. Hardware remains NO-GO.
