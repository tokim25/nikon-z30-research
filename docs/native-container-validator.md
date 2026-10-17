# Decoded-container validator

2026-10-17. F-136. Implemented in `src/nikon_z30_research/package_container.py`.
This newly written read-only code checks an immutable decoded container in
memory. It has no decoder, encoder, patch writer or hardware interface.

## Contract

`validate_container(data, expected)` takes decoded bytes and an ordered tuple
of `ComponentSpec` objects supplied independently of the candidate. Every
spec pins the name and size. An optional full SHA-256 also pins components
that must remain unchanged. Deriving these specs from a candidate would
defeat that comparison; use the verified original or a reviewed manifest.

The function checks exact total length before parsing, the fixed prefix,
header count and directory extent, reserved fields, ordered canonical names,
contiguous component bounds, each component CRC residue, optional unchanged
hashes, trailer padding and the container CRC. It uses explicit exceptions,
not assertions. Errors identify the failing check/index without including
payloads or untrusted names.

The immutable report contains sizes, offsets, hashes and per-component
`unchanged_checked` flags. A missing hash intentionally means structural/CRC
validation only. The report contains no firmware bytes and makes no claim
about permissible changes or camera acceptance. No original-specific
component names, mask tables or executable excerpts are embedded in the code.

## Evidence

Fourteen synthetic tests cover valid input, every truncation of the small
fixture, trailing data, header and trailer corruption, out-of-range/overlapping
offsets, wrong sizes, reserved fields, wrong/duplicate/swapped names and bad
padding, component and container CRC failures, invalid policy and mutable
input. Malformed structural fixtures have their container CRC repaired so
tests reach the intended checks.

One test changes a synthetic payload and repairs both CRC levels. The
original digest still rejects it. Unpinning only that component permits the
structurally valid change while the other component remains hash-pinned;
a separate test confirms that a change to the second pinned component fails.
This demonstrates why CRC validity alone cannot enforce an edit plan.

The private F-135 helper now passes its validated original component metadata
to this reader and checks the decoded original container entirely in memory.
All three components passed with their hashes pinned; reports agreed with
the recovered verifier. The unchanged package round trip still passed and
the original file remained unchanged. No firmware image was written.

Reproduce from this repository, with WORK set to the known private directory:

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -p test_package_container.py -v
PYTHONPATH=src python3 -B "$WORK/codex-package-roundtrip-audit-private.py"
```

The reader is independently written from the audited format description;
the private live-input check still shares the recovered decoder. The new
tests contain only invented payloads and names.

## Next boundary

F-137 implements a read-only original/candidate comparison against exact
permitted edits; see [native-exact-edit-audit.md](native-exact-edit-audit.md).
It pins original identity and rejects unexpected changes inside or outside
planned spans. Check checksum regeneration separately. This reader alone does not
validate the encoded outer prefix, mapping of runtime addresses, instruction
semantics, cryptographic authentication or updater compatibility.

Hardware remains NO-GO. The feature gate and missing saved-crop evidence are
unchanged. No commit, push or PR was made.
