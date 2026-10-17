# Lane 3: stack-space and code-placement check for the 424-byte candidate

Date: 2026-10-17. Read-only reconciliation of Codex's tracking-storage
work (`tracking-storage-abi-audit.md`, `tracking-candidate-review.md`,
`tracking-claude-handoff.md` in the Codex tracking checkout, branch
`codex/tracking-menu-contract`). No new decoding, no simulator, no camera.
Numbers below are Codex's; this document only checks that they agree.

## Verdict

**Static stack and placement accounting is consistent and sufficient for
the candidate as specified. It is not proof of hardware safety.**

## Stack space

- Task configured for 8192 bytes; the candidate raises the request to
  9216 (origin `0x1206bd90`). Native run confirmed request 9216 and
  allocation 11264, up 1024 from stock (10240). Task handle `0x10000d7`,
  TCB `0xc2b7a498`, entry `0x1021986d`.
- Added live stack: outer frame 424 plus at most one 64-byte wrapper frame
  (design ceiling 552; encoded result 472). Spare of the 1024 increment:
  552 as built.
- Every stock path gains 1024 of capacity and at most 472 of depth, so
  headroom never drops below stock. This is relative non-regression, not
  an absolute stock-headroom proof; stock worst-case depth stays unknown.
- Admission requires entry SP = TCB top minus 272 and return landmark
  `0x102f2c26`; mismatches fall through to stock. Constructed controls
  passed (rejection 48 instructions, admission 133, cleanup restores SP,
  r0-r11, flags, original return).

## Code placement

- Code 964 bytes, 972 with gaps, inside 1408 checked zero-fill code bytes.
- Menu data 952 bytes inside 968 reviewed. 45 disjoint spans, 24
  relocations, no XPan interval taken. Relocation, alignment, return and
  flag checks pass statically.

## Open risks (unchanged by this check)

- An extra 1 KiB heap request and shifted allocation addresses are
  untested on hardware.
- Natural worker admission, real queued-edge delivery and asynchronous
  lifecycle are unobserved; startup notifications never reached the guard.
- Decoder callbacks keeping the record pointer is not fully excluded.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
