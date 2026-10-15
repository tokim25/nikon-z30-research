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

F-011. Router `0x104b912c` selects a callback at
`object + 0x78 + 4 × byte(object + 0x74)` and passes event type and payload.
In the initialized object map, selector 1 leads to menu handler `0x103cf78e`
or live-view-setup handler `0x102f79ac`; their type-3 branches reach
`0x103cf696` and `0x102f7448`, respectively. Observed static code/data links,
high confidence; normal delivery, payload format and tracking meaning remain
unverified. Live-view initialization selects 0, and another path selects 1;
the transition conditions are unresolved. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex_ui_route_verify_private.py" --output "$WORK/private-inputs/codex-ui-route-review-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-ui-event-router.md).

Written by Codex in collaboration with Tony Kim.
