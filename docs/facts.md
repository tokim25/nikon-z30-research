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

F-009. Candidate routines `0x1029d8aa` and `0x1029d8ea` contain byte reads
from MMIO `0x2016c010` at `0x1029d8c6` and `0x1029d906`, respectively.
Observed in bounded static decode, high confidence. Bit-1 and high-nibble
output semantics are static inference, high confidence; button, live-view and
AF attribution are unverified. The simulator comment's `0x102595de` /
`0x1025961e` attribution was not reproduced. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex_input_sampler_verify_private.py" --output "$WORK/private-inputs/codex-input-sampler-review-01"`,
using the confirmed WORK path and a new output directory.
[Evidence and limits](tracking-input-sampler.md).

F-010. Static caller `0x1028b040` supplies a pointer to a destination byte to sampler
`0x1029d8aa`; a final normalized state change can reach the callback slot at
`0xc1807ecc`. Setter `0x1028b134` receives callback `0x10396cde` from
`0x10396f98`; the callback constructs a record containing `0x4206101e`.
Observed bounded call/data-flow structure, high confidence. Debounce-like
filtering and HDMI-status attribution are inference, high confidence; no button,
live-view or AF connection is established. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex_sampler_consumer_verify_private.py" --output "$WORK/private-inputs/codex-sampler-consumer-review-01"`,
using the confirmed WORK path and a fresh output directory.
[Evidence, public register comparison and limits](tracking-sampler-consumers.md).

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

F-013. Supersedes the cause open in F-007. The hangs came from the simulator
tools' call helper, which treats the first stop reply after a resume as
completion without checking which thread stopped. A thread-aware helper
(`guest_call_safe.py`) that resumes on unrelated stops ran 112 fires (224
calls) in 8 sessions with no hangs, against 10 to 15 percent before. Observed,
high that the hangs are gone in this setup; the mechanism is inferred, medium.
Issue #7.

F-014. Worker flag bit 16 is set by the live-view mode-enter routine
`0x102f2990` itself (call site `0x102f2a10`, right after its state-0 write at
`0x102f2a04`). A scan of all 288 direct callers of the group-set wrapper
`0x10462894` found five such setters, one per mode object (live view, menu and
three others). No timer, interrupt or physical-control setter was found.
Observed, high. Task-context reading is inferred, medium. Helper-agent result,
not re-verified.

F-015. State 1 is written by `0x102f57e2` (write at `0x102f5810`) with no
focus or mode test. The condition is that a mode-change request targeting the
live-view object (code high half 0x100000) passes dispatcher `0x10462970`,
which returns early when the current object's selector is 2 or 3. Observed
code, high. Combined meaning inferred, medium. Helper-agent result.

F-016. Event type 9 is sent on every worker iteration (`0x102f2c14`). In state
1 its handler `0x102f7942` runs a gate, then property resync helpers, and does
not write the selector. No dereference of the payload was found, but not all
helpers were read. Observed shape, medium; "ignores the payload" is inferred,
medium-low. Helper-agent result.

F-017. A table of 16-byte UI-event rows (552 of them, in the initial-data
area) links internal codes 0x24e to 0x252 to handlers that call mode
dispatcher `0x10462970` with targets 0x10000, 0x100000, 0x108000 and 0x40000.
An input map maps input codes 0x15, 0x17, 0x1a, 0x1c, 0x1f to those internal
codes, and 0x1b to 0x27e, the menu OK code. Which physical control is which
input code was not established. Inferred, medium. Helper-agent result.

F-018. The simulator has no model of buttons, dials, touch or HDMI status.
A one-byte read of `0x2016c010` returns constant 0; the four I2C buses reply
NACK; no input state is writable from the host, whose only channel is the
debugger stub. Observed in the simulator source, high. Helper-agent result.

F-019. A stock refresh in the simulator does not run the live-view task, its
worker, or the enter routine: 14 addresses were observed and none fired. The
selector-1 path through normal tasks is therefore unobserved. Observed, high.
Helper-agent result.

F-020. The key dispatcher `0x103ce96e` is a screen-stack dispatcher. It takes
the top of the UI screen stack (pointer at `0xc181e4f0`) and looks up the code
in a per-screen key table of 16-byte entries (handler, guard, parameter).
Codes from 0x248 up, including OK 0x27E, go only to the top screen. A key
filter `0x104e2cbc` diverts 0x27E to a live-view routine `0x102f1e10` for some
screens. Physical-button states appear to reach the menu through a type-10
event into this dispatcher and live view through type 3 into `0x102f7448`.
Observed dispatch mechanics, high. Why OK does nothing in live view is not
settled: the live-view screen's group, id and key table were not found.
Inferred, low. Helper-agent result, not re-verified.

F-021. The ring at `0xc2008ea0` and the single record at `0xc200a7a0` (read
by `0x102f1412`) are not button-press records. The ring holds typed 60-byte
events (touch/drag/sync-shaped, written only by `0x102f0a36`); the single
record is a 0x18c-byte copy of a separate global input snapshot, written only
by `0x102f0d14`. That snapshot is built from a 5-byte packet decoded by
`0x1030705a`, whose byte 0-2 become key-mask words and bytes 3-4 become
signed deltas (dial-shaped). Decoder `0x102f0e38` maps mask-group-1 bit 0 to
internal code 0x1b, which the known input map (F-017) sends to event 0x27e,
the same code the menu dispatcher treats as OK. Observed data flow, high;
packet source (a front-panel controller) and which physical button maps to
which mask bit are inferred, medium-low. A passive stock-refresh trace saw
none of these addresses fire, so the live-view input path is dormant absent
real input. Helper-agent result, not re-verified.

F-022. Menu states cannot show the guides. With the thread-aware helper for
both the key event and the nested call: up, down and Back complete with no
bars; OK hangs when any nested call, even a no-op one, is made at the first of
its three compose stops (3 of 3 runs, no-call control completes), and
completes with no bars when the call is made at the last stop. Observed in a
handful of runs, medium. The OK hang's cause is unexplained. Repro: private
`menu_retest_private.py` with `CALLAT`, `NOOP` and `FORCEGATE` switches.
[guides-ui-states.md](guides-ui-states.md)

F-023. The input map at `0x1073b400` is 179 rows of 8 bytes: input code,
internal UI-event code, two zero bytes. It matches every known code (input
0x4, 0x5, 0x3, 0x6, 0x8 and 0x1b give 0x253, 0x254, 0x255, 0x257, 0x258 and
0x27e). Four guards on UI-event table rows (`0x1045fb20`, `0x1045fb24`,
`0x1045fb50`, `0x1045fb10`) gate internal codes 0x24f, 0x250, 0x251 and
0x26d to 0x270 (input codes 0x1a, 0x15, 0x1f and 0x45 to 0x48). Every handler
examined is a one-shot screen switch through dispatcher `0x10462970`, with no
press/release split and no lock-style write. Observed, high. That these are
navigation controls and not AE-L/AF-L is inferred, medium. Helper-agent
result, not re-verified.

F-024. The firmware holds a named hardware-switch table: 40-byte slots (a
36-byte name, then a 4-byte bitmask), the first group starting at
`0x1072e3b0`. It names `ID_SW0_AEAF_LOCK` (slot 10, mask 0x2000) and a twin
`ID_SW0_AEAF_LOCK_VPOS` (slot 11, mask 0x1000). The same word names the d-pad
(bits 0 to 8) and top-deck controls, so AE-L/AF-L has its own bit apart from
every d-pad direction. Strings for the button's custom-function settings
(`eDSID_Setting_FuncAeAfLockButtonShooting` and `...Movie`) also exist. The
owner confirmed the button is physically on the body. Observed, high. Not
closed: the code that reads bit 13 and links it to an input code or an event.
No reference to the table's base address was found. Press/release handling is
unknown. Helper-agent result, not re-verified.

F-030. Image-area sizes are stored as data in two places. A run of width and
height pairs at `0x10750650` lists sizes by aspect ratio and size class; code
reads it through five literals near `0x10596c9c` to `0x10598640`. A 38-entry
pointer table at `0x12049a7c` (initialized-data region, reached through its RAM
copy) points to records near `0x115a4d6c` with, per area (DX, 16:9, 1:1),
output sizes, padded sensor-readout sizes, large-size copies, and thumbnail
sizes. Observed static layout, high. Which record drives live view, capture or
thumbnails is not traced, so a 1:1 replacement may need several records.
Inferred, low. [image-area-tables.md](image-area-tables.md)

F-031. Corrects F-030's first store. The run of size pairs at `0x10750658` is
the Retouch Trim editor's table: 110 entries indexed by orientation, source
group and five aspects, each the largest crop that fits, rounded to multiples
of 16. A data-only 65:24 swap would fail: `0x10597440` hard-codes the five
ratios and forces width equal to height for 1:1, labels are 5-byte slots, and
the counts are compile-time bounds. Observed static, high. Helper result.
[image-area-tables.md](image-area-tables.md)

F-032. The pointer-table records (RAM copy at `0xc18c7de8`) feed capture and
readout geometry, output sizes, margins, thumbnails and movie sizes; 1:1 is
area 4. Live-view render-object offsets `0x320` and `0x324` are the display
surface size, not image size, which corrects the earlier reading. The live-view
image size comes from a frame-size table at `0x1073db04`, with no path found
from the image-area records. Observed static, high. That the path is absent:
moderate, as 58 callers were not all traced. Helper result.
[image-area-tables.md](image-area-tables.md)

F-033. No display-side code reads the image area (setting id `0x189e`; value 4
is 1:1). Live view shows a layer that is almost always full-screen; the area
reaches only the capture side, where `0x101d5c54` copies it into a request and
tables give per-area crop windows (live-view readout `0x115a4cc0`, crop sizes
`0x115729b4`). The only 1:1-specific branch is an interlock bit at `0x1022d5f8`.
Observed, high for the capture-side facts. That the crop is made upstream by the
separate image-processor firmware, which is not in this image, is inference at
about 45 percent. Helper result. [image-area-tables.md](image-area-tables.md)

F-034. The capture-geometry function `0x101d5b36`, called natively in the
simulator, gives per-area results straight from the records: 1:1 at large size
is area 3728 by 3728, crop origin (936, 0), image rectangle out to 3720 by 3720;
16:9 is area 5600 by 3144 with origin (0, 292). Origin equals half the readout
minus area. Observed, high; hash unchanged. A test with 1:1 changed to a 65:24
shape was blocked by the permission classifier and has not been run.
[capture-geometry-baseline.md](capture-geometry-baseline.md)

F-025. Corrects F-021's exclusive-writer and universal 60-byte ring-record
claims. Both `0x102f0a36` and `0x102f1844` write into the ring at
`0xc2008ea0`, using index state `0xc182004c` and 400-byte slots. The former
copies 60 bytes and forces kind 1; the latter copies 396 bytes and can advance
the index modulo 16. Observed static code/data links, high confidence,
independently checked. Physical source, runtime delivery and tracking meaning
remain unverified. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex_input_record_verify_private.py" --output "$WORK/private-inputs/codex-input-record-review-02"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-input-records.md).

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.
