# Milestone 1 recovered and checked

Date: 2026-10-15.

## What was recovered

The user supplied Nikon-Z30-Firmware-Research-M1.zip: 11 files totaling
40,646 uncompressed bytes. Archive SHA-256:
`ff723c1d2bbf2284e2290328cda4f2c92d4aa2c99124182185b8829438373f89`.
It includes four analysis tools, three saved reports, three documents, and one
test file. It does not contain a complete firmware binary.

The original archive was inspected before its code ran. Its instructions,
including suggestions for camera tests, were treated as source material rather
than new authorization. The recovered originals remain outside this repository
under the chat workspace's work/recovered-m1 directory.

## Reproduced results

The recovered verify_and_map.py was run against the previously hash-checked
official firmware input. It decodes in memory, checks identities and integrity,
and writes a local report rather than an extracted binary.

| Check | Result |
| --- | --- |
| Archive unit tests | 3 passed |
| Original package size | 34,496,798 bytes |
| Original package SHA-256 | 1a5449ef505f1f347ed4e066a6a3f588ea542240680e83f4ebcae3b16da3434a |
| Main EG module size | 33,939,514 bytes |
| Main EG SHA-256 | 8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa |
| Other component sizes | EX: 524,290 bytes; TPJ: 32,802 bytes |
| Container and component integrity checks | Passed |
| Known source locations checked | All 6 matched |
| Comparison with saved report | Firmware, decoded EG, module list, known locations, dimension index, and feature flags all equal |

The main module was decoded only in memory. No patched or installable image was
created. Matching a digest establishes identity consistency, not independent
proof of provenance or working camera behavior. The three archive tests are
separate from the repository's 24 synthetic tests.

## What was not imported

The archive's claim that it contains no proprietary executable bytes is too
broad: verify_and_map.py embeds short original instruction windows for comparison.
Other tools can write raw hex fragments, nearby words, or text excerpts from
decoded firmware. Their originals and outputs therefore remain local, even
though their filenames end in .py or .json. No archive file was copied into Git.
Only this newly written summary is published.

The tool includes upstream-derived decoding logic and a compact sample table.
Its attribution file was preserved locally. Any later code reuse needs a
file-specific license review and removal of copied firmware material.

The recovered address-reading helper also needs stronger input checks before
general reuse: it does not explicitly reject negative lengths or reads that
cross the initialized-data mapping boundary. Some invariants use Python
assertions, which disappear in optimized execution. The reproduction used
normal Python execution and the verified fixed input; it does not establish
that this helper is suitable for arbitrary inputs.

## Next step

Use the now-reproduced histogram landmarks to trace the existing display path.
Keep any decoded bytes and detailed intermediate reports local. Publish only
reviewed conclusions and source references. Do not treat matching landmarks as
proof of a general drawing service.

The old label searches remain leads, not functions: this recovery did not rerun
the raw-text triage tools or establish a tracking-start routine. No physical
camera tests from the old checklist were performed.
