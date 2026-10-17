# Read method for the digest input at 0x10000088: review

2026-10-17. Written for owner review. Nothing has been run. No camera was
connected. Hardware remains **NO-GO**.

## Result: no method passes review

- Claude cannot specify a command or procedure that reads the eight bytes at
  `0x10000088` from the camera without a vendor, service, or boot-level
  interface. No such interface is documented, identified or reviewed in this
  repository.
- The only candidate reads are PTP or USB operations. Standard PTP exposes
  device identity only. The libgphoto2 review found write-capable calls and
  firmware-update opcodes in the PTP vocabulary (see
  [digest-and-tool-review-2026-10-17.md](digest-and-tool-review-2026-10-17.md)).
- A boot-region read would require a non-standard or update-mode path, which
  is the class of operation that can alter camera state. Proving it cannot
  modify state needs an operation log of a reviewed tool, and none exists.

## Consequences

- No procedure is proposed, so no write-path review, recovery plan, or
  "proof of no modification" is offered; each would be unsupported.
- Owner-approved rules 9 and 10 do not change this outcome; they authorize
  reviewed read methods, and none has been reviewed.
- Digest input: **still open**. What would resolve it: a static source for the
  eight bytes in offline evidence, or a reviewed read path that passes all four
  requirements above.
