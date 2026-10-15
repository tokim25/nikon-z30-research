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

F-012. Builder `0x102f2ad2` prepares a 4-byte header and 184-byte status region
for conditional type-3 dispatch. Reviewed parsers also fetch separate records
through `0x102f1412`; the producer extent is not a complete safe-call contract.
Worker flag bit 16 can route type 2 through selector-0 handler `0x102f61d2`
to `0x102f57e2`, which writes selector 1 at `0x102f5810`. Observed static links,
high confidence; ring-like storage is inference. Flag production, record
contents, prior type-9 effects and tracking meaning remain unverified. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex_liveview_payload_verify_private.py" --output "$WORK/private-inputs/codex-liveview-payload-review-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-liveview-payload.md).

Written by Codex in collaboration with Tony Kim.
