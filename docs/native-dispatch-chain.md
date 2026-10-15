# From refresh request to render setup

Date: 2026-10-15. Simulator observation of one explicit stock refresh, plus
static reading of the unmodified EG image. Addresses are landmarks, not
approved entry points. Names are inferences.

## What runs, in order

- 0x10453d14 is entered with r0 = 3 and r1 = 1. It builds a request and calls the next landmark.
- 0x104b74f4 is a two-instruction stub. It sets r2 to 1 and branches to 0x104b740a.
- 0x104b740a treats r0 as a bit mask and r1 as five 24-byte entries per bit. For each entry whose first word is nonzero, it calls 0x104b729c, and if that returns zero it calls 0x103c3810.
- 0x103c3810 receives r0 = 1 and the same array pointer, then hands off to 0x103c3568.
- 0x103c3568 loops over five categories. 0x103c0bc0, 0x103c0ac2 and 0x103c05d2 then look up the object and set up render state, all with category 1.
- 0x103c1b54 computes the image bounds. See [native-border-gate.md](native-border-gate.md).

## Limits

Bit 1 of the mask selects a second array 0x78 bytes further on, with the same
pattern. A mask of exactly 3 takes a separate branch that this run did not
exercise. Ownership of the array and the meaning of the 0x104b729c test are
not established.

Everything above is dispatch and state preparation. No pixel is written at
any of these landmarks. Earlier context is in
[native-drawing-investigation.md](native-drawing-investigation.md).

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
