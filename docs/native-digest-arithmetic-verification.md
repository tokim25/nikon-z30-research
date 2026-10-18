# Native digest arithmetic checkpoint

2026-10-17, F-161. Offline engineering only. Original-package digest remains
unverified; modified firmware remains NO-GO.

The new private evaluator decodes the verified original EG instructions with
the existing Capstone installation and evaluates only the native compression
arithmetic and suffix loop. Unsupported executed operations, uninitialized
reads and excessive steps fail. It does not boot firmware, run an updater,
model peripherals or write a firmware file. This is newly written analysis
code, not recovered code or an independent ARM emulator certification.

## Results

- Compression arithmetic at `0x101d7080` through `0x101d80bc` matches
  Python `hashlib.sha1` using independently supplied standard initialization
  and padding. Twelve synthetic messages cover lengths 0, 1, 3, 55, 56,
  63, 64, 65, 119, 120, 128 and 257, including both padding boundaries and
  multiple blocks. Native update/finalization routines were read statically,
  not executed by this evaluator.
- Suffix-loop instructions at `0x101d3f7a` through `0x101d3f8e` match the
  recurrence below on 1,024 synthetic cases. Four coefficient pairs cover
  zero and byte-overflow boundaries, each with 256 synthetic seeds.
- For zero-based byte index `i`, the loop XORs its input byte with
  `(b + a * ((i + 1) * 608 + i * (i + 1) / 2)) mod 256`.
  Here `a` and `b` are loop inputs. Their native configuration parsing and
  table lookups were not executed in these comparisons. No model key or
  missing boot-region bytes were recovered.

The distinction matters: this verifies the compression arithmetic and loop
formula; it does not reproduce the original package's expected twenty bytes.
The eight-byte input at `0x10000088` remains absent from available evidence.
No search over guessed key inputs was performed.

## Reusable verifier

[package_digest.py](../src/nikon_z30_research/package_digest.py) checks
`SHA1(complete decoded body || supplied eight-byte suffix)` against supplied
original and candidate header digests, in that order. It refuses absent,
malformed or baseline-mismatching inputs. It returns body identities and a
bounded scope, never the suffix or hardware readiness. It neither constructs
packages nor replaces decoded-container, CRC, exact-edit or installation
checks. Callers remain responsible for supplying the correct complete body
and independently justified suffix; the function cannot attest provenance.

Seven synthetic unittest cases cover a valid pair, missing/malformed inputs,
wrong suffix, stale original digest on changed content, trailer corruption,
and body/digest types. The complete suite has 130 passing tests.

## Private reproduction and next decision

The evaluator remains outside Git at
`/private/tmp/z30-digest-20261017/check_native_sha1.py`, source SHA-256
`a9b44b10f70467689099f7158338122384e9cdbb6cb12dcae025322af65a220e`.
It reads the previously recorded private audit helper and pinned original;
run with the existing private analysis Python, `-B`, and `PYTHONPATH=src`.
It emits metadata only. Temporary storage is not a durable evidence archive.

The next build-enabling input remains verified offline Z30 suffix evidence
or a demonstrated equivalent that passes the original digest. Then check
the exact candidate. No additional camera collection is requested or
authorized. Lifecycle condition 1 remains unmet by the owner's decision.
