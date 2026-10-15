# Facts ledger

Both lanes append here. Never edit an old entry: add a new one that
supersedes it. Format: ID, statement, observed or inferred, confidence, source.
Addresses are landmarks, not approved entry points.

F-001. Rectangle wrapper 0x10477af2 draws filled rectangles in the simulator
when called with a 28-byte request. Observed, high.
[native-guides-simulator.md](native-guides-simulator.md)

F-002. The request color word is RGBA with alpha in the low byte. Observed,
high. [guide-color-and-stress.md](guide-color-and-stress.md)

F-003. On the overlay, drawing is unflipped: request y is 480 minus screen row
minus height. Observed, high.

F-004. A global at 0xc1808744 makes the wrapper queue and wait when nonzero.
Called from the display worker's own breakpoint it deadlocks, so it is forced
to 0 around the call. Observed, high.

F-005. The flush is 0x1050a306, called at the start of the compose function
0x104787f2. Inferred from static analysis plus observed call chains, medium.
[native-draw-pipeline.md](native-draw-pipeline.md)

F-006. In menu states the compose function does not fire at idle. Observed in
a few runs, medium. [guides-ui-states.md](guides-ui-states.md)

F-007. The per-cycle debugger call hangs in about 10 to 15 percent of calls.
Observed, root cause unknown. [guide-color-and-stress.md](guide-color-and-stress.md)

F-008. No tracking entry point has been verified. Open.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.

F-009. Candidate routines `0x1029d8aa` and `0x1029d8ea` contain byte reads
from MMIO `0x2016c010` at `0x1029d8c6` and `0x1029d906`, respectively.
Observed in bounded static decode, high confidence. Bit-1 and high-nibble
output semantics are static inference, high confidence; button, live-view and
AF attribution are unverified. The simulator comment's `0x102595de` /
`0x1025961e` attribution was not reproduced. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex_input_sampler_verify_private.py" --output "$WORK/private-inputs/codex-input-sampler-review-01"`,
using the confirmed WORK path and a new output directory.
[Evidence and limits](tracking-input-sampler.md).

Written by Codex in collaboration with Tony Kim.
