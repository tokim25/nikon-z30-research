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
F-026. Two record-field bit-13 paths have different normalized outputs:
`0x102f0488` maps `+0x164` bit 13 to `+0x18` mask 2, while `0x102f056e`
maps `+0x150` bit 13 to `+0x18` mask 4, clearing the corresponding source
bit. Their candidate/menu-map links are respectively `0x1a` / `0x24f` and
`0x19` / `0x280`. Observed bounded static links, high confidence,
independently checked. Neither source field is proven to be SW0 or physical
AE-L/AF-L; execution and final event delivery remain unverified. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex-sw0-normalization-verify-private.py" --output "$WORK/private-inputs/codex-sw0-normalization-review-03"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-mask-namespaces.md).
F-027. In the bounded structured-record path at `0x1008ad26`, selector 5
chooses mask `0x2000`. State at record `+0x08` equal to 1 sets the mask in
staging word `0xc1811e74`; zero clears it. Other states skip that update but
still reach setter `0x101e383a`, which copies the word to cache
`0xc181182c + 0x30`. Observed static code/data links, high confidence,
independently checked. Sender, physical SW0/button identity, runtime delivery
and tracking meaning are unverified. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex-input-field-source-verify-private.py" --output "$WORK/private-inputs/codex-input-field-source-review-04"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-input-source.md).
F-036. Supersedes F-034's unrun-test status: two simulator A/B/A runs of
geometry routine `0x101d5b36` with temporary data-only changes returned a
centered area 5216 by 1936 at origin (192, 896), with rectangle 5200 by 1920
(65:24). DX and 16:9 controls were unchanged; restoration exactly recovered
baseline outputs. Observed runtime results, high confidence. Original file
and instructions were unchanged; capture, saved RAW crop and hardware
support remain unverified. Repro:
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex_agent_geometry_data_probe_private.py" --output "$WORK/private-inputs/codex-geometry-reproduce-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](xpan-capture-geometry-probe.md).
F-029. Two unchanged-firmware simulator runs found count zero in screen stack
`0xc181e4f0` before startup, after assisted live-view startup and after stock
refresh. An audited menu-entry control populated two entries (IDs 1 and
`0x351`). Observed runtime counts, high confidence; bounded fixture
interpretation, moderate. Getter `0x1046109a` / `0x10365ff0` confirms count
at container `+8`. Ordinary camera state and tracking input are unverified.
Repro: `PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex_screen_stack_private.py" --output "$WORK/private-inputs/codex-screen-stack-review-04" --menu-control`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-screen-stack.md).
F-028. Mode-3 path in initializer `0x1008ad72` supplies callback
`0x1008ac2e` through registrar `0x101e1c04`, word limit 4, flags 0.
Consumer `0x101e1c22` calls numeric-text parser `0x101e230e` before the
registered callback. This establishes one registered numeric-command route
into the handler containing `0x1008ad26`. Observed bounded static links,
high confidence, independently reviewed. Diagnostic purpose is inference;
registration success, transport and physical-button identity are unverified.
Repro: `"$WORK/analysis-env/bin/python" "$WORK/codex-registered-input-verify-private.py" --output "$WORK/private-inputs/codex-registered-input-review-03"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-numeric-input-route.md).
F-035. Compose job `0x42010019` reaches `0x104787f2` before invoking its
completion callback `0x10476ea2`. That callback is too late to add guides
before the current flush. Gate helper `0x103bc388` reads signed 16 bits at
`0xc1808744`; zero selects direct compose, nonzero queueing. Observed bounded
static links plus passive runtime support, high confidence; no safe guide
hook established. Repro: `"$WORK/analysis-env/bin/python" "$WORK/codex-guide-worker-verify-private.py" --output "$WORK/private-inputs/codex-guide-worker-reproduce-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](xpan-compose-completion.md).
F-037. The pinned simulator contains an opt-in functional ISP model with
explicit pixel-layout hypotheses, fixed RAW-transaction checks and bounded
processed output. This corrects categorical claims that it has no image
processor. SD transport exists, but neither source presence nor geometry
tests establish native NEF serialization or saved RAW cropping. Observed
source, high confidence; runtime/hardware fidelity unverified. Repro:
`python3 "$WORK/codex_agent_raw_model_source_audit_private.py" --output "$WORK/private-inputs/codex-raw-model-reproduce-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](xpan-simulator-raw-limits.md).
F-040. Setter `0x104540ee` controls retained border color at `0xc1820138`
and retention at `0xc1820134`. Nonzero color reaches refresh request
`+0x168`, render-context `+0x44` and producer `0x103c1b54`. Retention 1
preserved synthetic white across two refreshes in two runs; retention 0
cleared stored color after one use in a control run. Observed bounded static
and runtime behavior, high confidence. No visible guides or new geometry
established. Repro: `PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-guide-border-color-observe-private.py" --retention 1 --output "$WORK/private-inputs/codex-border-color-reproduce-02"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](xpan-border-color-state.md).
F-042. Two calibrated simulator A/B/A runs produced persistent stock black
crop masks: 107 rows top/bottom, centered 266-row visible strip at width 720
(rounded 65:24). After one diagnostic clip-flag write and native geometry /
color setup, the mask appeared autonomously and survived three refreshes
without per-cycle rectangle injection. Restoration recovered baseline outside
the animated band. Observed runtime behavior, high confidence; natural
startup, overlays, saved RAW and hardware unverified. Repro:
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-guide-clip-mask-private.py" --bounds -1 106 721 374 --output "$WORK/private-inputs/codex-native-mask-reproduce-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](xpan-persistent-native-mask.md).
F-038. Queued consumer `0x103a3f9e` maps record ID `+0x11` through 16-row
banks at `0xc18c9a7c + 128 * BYTE(0xc18c9a64)`, stride 8. Operations
0–2 set mapped bits, 3–4 clear; changed staging at `0xc18c9a68` reaches
setter `0x101e383a` at `0x103a400c`. Handler `0x103a3d14` builds this
route for code `0x2083`. Observed static links, high confidence; transport,
physical identity, press/release and tracking unverified. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex-agent-queued-input-verify-private.py" --output "$WORK/private-inputs/codex-queued-route-reproduce-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-queued-bank-route.md).
F-043. Query `0x103a3cb0` selects input bank 1 via byte store
`0x103a3cdc`. Initialized bank `0xc18c9afc`, row 11, associates logical
ID 41 with mask `0x2000`; the query sends tag/ID pairs as code `0x2082`.
Observed static links, high confidence. Execution, physical SW0/button
identity, transport and tracking remain unverified. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex-agent-input-bank-verify-private.py" --output "$WORK/private-inputs/codex-input-bank-reproduce-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-input-bank-selection.md).
F-041. Assisted startup changed live-view object `0xc1821d44` selector
`+0x74` from 4 to 1 while the menu/screen stack stayed empty. The separate
registry `0xc2006594` had groups 2/3 before startup and gained group 5.
Getter `0x104571fe` uses descriptor stride 44 without reviewed ID/null-base
guards. Observed static/runtime state, high confidence; fixture
generalization moderate. No input/AF readiness inferred. Repro:
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex_mode_object_20261016_private.py" --output "$WORK/private-inputs/codex-mode-state-reproduce-01" --menu-control`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](tracking-registry-mode-state.md).
F-039. Builder `0x101e779c` repacks selected source halfwords `+0x208`
through `+0x218`; caller `0x101ea022` supplies source argument plus
`0x1c` and destination `0xc233addc`. A later reviewed path copies
2024 bytes through `0x100aa43a` and submits via `0x100c9f24`. Observed
static links, high confidence; original capture-request identity, NEF
semantics, runtime delivery and saved crop unverified. Repro:
`"$WORK/analysis-env/bin/python" "$WORK/codex_agent_geometry_pack_verify_private.py" --output "$WORK/private-inputs/codex-geometry-pack-reproduce-01"`,
using confirmed WORK and a fresh output directory.
[Evidence and limits](xpan-packed-config-boundary.md).
F-044. Under assisted simulator startup, two diagnostic clip-flag on/off
cycles at property `0xc1d87838 + 0x2c` produced the calibrated 214 black
border rows on and restored baseline pixels outside the animated band off.
Audited menu entry `0x102355ee` grew the screen stack from zero to two;
the mask, bank, property and retained color remained unchanged. A subsequent
live-view entry did not remove those stack entries, so natural menu exit is
unverified. Observed runtime, high within this fixture; independently repeated.
Original owned fields were restored. Repro: confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-guide-mask-reliability-private.py" --output "$WORK/private-inputs/codex-mask-lifetime-fact-reproduce-01"`
with a fresh output directory. [Report](xpan-mask-menu-lifetime.md).

F-045. The surface initializer `0x104b5fd4` has exactly two direct Thumb
`bl` callers, at `0x10452e56` and `0x10452ea8`, both in the same function
region. A scan for its address (with and without the Thumb bit) as a 32-bit
word found no pointer-table references. Observed static scan of the verified
original over the code range `0x10020000` to `0x11f81c94`; the first-pass
result was run by the owner in a terminal on 2026-10-16. Confidence medium:
the scan sees direct branches only, so indirect calls through registers are
not ruled out, and mixed code/data decoding is heuristic. The callers'
arguments are not yet read. Next: decode a short window around each caller
to see what config pointer they pass. Method: read-only Thumb branch scan,
SHA-256 checked first; no bytes recorded here.

F-046. Both callers of the surface initializer `0x104b5fd4` (F-045) sit
inside nested loops that count to 3 (compare-with-3 at `0x10452e5c`,
`0x10452e62`, `0x10452eae`, `0x10452eb4`), so each runs up to nine times per
pass over a 3 by 3 set. The first passes mode value 1 in r1, the second mode
value 2. Each sets up r0 from an indexed table, r2 from a literal-pool word
and several stack arguments; the second first clears a `0x198`-byte local
buffer and passes its address. Observed static decode of a short window
before each call, produced by the owner in a terminal (and repeated by
Claude) on 2026-10-16. Inferred, confidence low to medium: the initializer is
bulk per-item surface setup for a 3 by 3 set in two modes, not a one-off
clip-state setter, so it should not be called alone as a clip-only step. The
literal-pool values and what the indexed tables hold are unread. Method:
read-only Thumb decode, SHA-256 checked first; no bytes recorded here.

F-047. The call chain above the surface initializer `0x104b5fd4` (F-045,
F-046) is: a handler at `0x102ae5e8`, listed in a table of Thumb function
pointers at `0x11fa38f8` onward (the entry at `0x11fa38fc`; neighbors point
to other handlers near `0x102ae5db` and `0x102ae7c3`); that handler checks a
flag at structure offset `+0x10`, and when it is set calls `0x1045300e`,
`0x1045348a` and then the wrapper `0x10452f34`, and clears the flag. The
wrapper's first call is the function at `0x10452d86` (clears a `0x60`-byte
buffer, runs the 3 by 3 loops that call the initializer, then a third loop of
calls to `0x10452d26`, then returns); the wrapper then calls `0x104ed666` and
`0x104ed67a`. The wrapper's only direct caller is the handler (`0x102ae60c`);
the handler has no direct callers, only the table pointer. Observed static
decode on 2026-10-16, run by Claude after the owner changed a permission
setting. Inferred, confidence low to medium: when the flag is set, this
handler rebuilds a 3 by 3 set of surface objects, so it is a mode or event
handler and not a menu-exit cleanup by itself. What sets the flag at `+0x10`,
which event the table slot belongs to, and what `0x104ed666` and `0x104ed67a`
do are unread. Method: read-only Thumb decode, SHA-256 checked first; no
bytes recorded here.

F-048. The handler of F-047 reaches its flag through a global RAM structure
whose pointer literal is `0xc1821c2c` (the handler subtracts `0x1c` to get
`0xc1821c10`, so the flag it tests is the word at `0xc1821c20`). The same
literal appears at five places (`0x102ae990`, `0x102aedf0`, `0x102af260`,
`0x102afb6c`, plus `0xc1821c10` at `0x102afd1c`), and about 80 pc-relative
loads of it fall between `0x102ae5a8` and `0x102afca0`. Observed static scan
on 2026-10-16. Inferred, confidence medium: this is one module-wide state
object shared by that whole code range (the handler table of F-047 lives
there too), so whatever sets the flag at `0xc1821c20` is most likely a
function in the same range, found among those loaders. Not yet done: telling
the writers of that one word apart from the many other users. Method:
read-only literal-pool scan, SHA-256 checked first; no bytes recorded here.

F-049. No writer that sets the handler flag at `0xc1821c20` (F-047, F-048)
was found by two static patterns. (1) The only code that loads the literal
`0xc1821c10` (the structure base itself) is the function at `0x102afc8e`,
which uses the structure at offset `+0x14`, not `+0x10`. (2) Of six places in
`0x102ae500` to `0x102b0000` that load `0xc1821c2c` and subtract `0x1c` to
reach the base (`0x102ae5fa`, `0x102aea22`, `0x102aea72`, `0x102af1be`,
`0x102afaa8`, `0x102afae8`), only the handler at `0x102ae5fa` touches `+0x10`,
and it only reads and clears it. No literal for `0xc1821c20` exists in the
scanned image. Observed static scan on 2026-10-16; confidence medium, since
the scan misses writers that receive the structure as a pointer argument,
use other base registers, or live outside the scanned range. Inferred: the
flag is set through a pointer passed from elsewhere, or from code outside
`0x102ae500` to `0x102b0000`. Next: trace what the first call `0x102bd612` and
callers of the other module functions pass, or look for stores through the
table-registered handlers' neighbors. Method: read-only Thumb scan,
SHA-256 checked first; no bytes recorded here.

F-050. The surface initializer `0x104b5fd4` (F-045 to F-049) takes a config
block as its fifth argument (the first stack argument, read as `[sp + 0x20]`
after its own push). It validates two config words (`+0x14` and `+0x18`, each
must be below 7), fetches a surface object through `0x104b5e30` using the
first two arguments, and then copies config fields into the object: config
`+0`, `+4`, `+8` into object `+0x24`, `+0x28`, `+0x2c`; config `+0xc` and
`+0x10` into object `+0x30` and `+0x34`; config `+0x14` through `+0x28` into
object `+0x38` through `+0x4c`; a `0x168`-byte block from config `+0x2c` into
object `+0x50`; and two bytes from config `+0x194`, `+0x195` into object
`+0x1b8`, `+0x1b9`. If object `+0x24` and `+0x28` are both nonzero it then
calls registration-style functions (`0x103bcb64`, `0x1039c17e`, `0x103bd144`,
`0x103bd25c`, `0x103bcb6a`). Observed static decode on 2026-10-16. Object
`+0x2c` is the same offset as the diagnostic clip flag in F-042
(`0xc1d87838 + 0x2c`). Inferred, confidence low to medium, and not yet
shown: `0xc1d87838` is such a surface object, so rebuilding it through this
path overwrites the clip flag from config `+8`. If so, the F-047 handler is a
candidate for clearing the black mask on its own whenever its config clip
word is zero, and a call to the initializer with a config whose `+8` is
nonzero would be a candidate for setting it. This must be checked in the
simulator with a fresh run before anyone relies on it. Method: read-only
Thumb decode, SHA-256 checked first; no bytes recorded here.

F-051. Runtime check of F-050 in the simulator: calling the surface
initializer `0x104b5fd4` with object index 1, mode 1 (the pair for which
`0x104b5e30` returns `0xc1d87838`), and a 0x1a0-byte config block copied the
config words into the object. With the clip flag at `0xc1d87838 + 0x2c` set to
1 beforehand, a call with config `+8` equal to 0 left the flag at 0, and a
second call with config `+8` equal to 1 left it at 1. Object `+0x24` and
`+0x28` took the config values at `+0` and `+4` (both 0, so they went from
`1` and `0xd0959600` to 0), which is why config word 0 was kept at zero: it
skips the registration calls. Both calls returned 1. The whole `0x1c0`-byte
object was restored byte for byte afterward. Observed runtime, high within
this fixture (assisted startup, one run). Not shown: any effect on the
display, because the check was memory-level only. Repro: confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/claude-initializer-copy-check-private.py" --output "$WORK/private-inputs/claude-initializer-copy-check-NN"`
with a fresh output directory. The script stays under WORK and is not committed.

F-052. Display check of F-050 and F-051 in the simulator, with a negative
and ambiguous result. With the persistent black mask on (the F-042 setup: 214
black rows, clip flag 1), the surface initializer `0x104b5fd4` was called for
object index 1, mode 1 with a config rebuilt from the object's own current
contents, except that config `+8` (the clip flag) was set to 0, and with
config words 0 and 4 kept so the registration calls ran. The call returned 1
and the flag at `0xc1d87838 + 0x2c` read 0 afterwards, but after the normal
refresh (`0x1032427e` and a 0.6 second run) the screen still showed 214 black
rows, so the rebuild did not remove the mask. Unexpectedly, object `+0x24`,
copied from the object's own value 1, read 0 afterwards (object `+0x28` was
unchanged); what zeroed it is unknown. Observed runtime, one run, assisted
startup, medium confidence. The whole object was restored byte for byte. Not
explained: whether an object with `+0x24` equal to 0 is skipped on refresh and
so leaves old pixels in place, which would make the rebuild a poor cleanup. So
a rebuild through this initializer is not shown to be a cleanup path; the
F-047 handler remains unproven as one. Repro: confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/claude-initializer-rebuild-mask-private.py" --output "$WORK/private-inputs/claude-initializer-rebuild-mask-NN"`
with a fresh output directory. The script stays under WORK and is not committed.

F-053. The "Choose image area" menu text lives in the firmware as UTF-16
strings inside one packed text blob, not as separate files. The title appears
at `0x10e88c22` and `0x10e890da`/`0x10e890fe`, the last two sitting next to
the choice label "DX (24x16)" and neighbouring menu titles (white balance,
12-bit/14-bit). Help text for the image-area control appears at `0x10e8ed56`
and `0x10e8ede8` ("hold the button and rotate a command dial"), and a
confirmation message "DX image area selected" at `0x10e8a200`. A search for
ASCII names (`ImageArea`, `IMAGE_AREA`) found nothing; the only `ID_IMAGE`
hit is an unrelated save-media name at `0x11c991ab`. Observed static string
search on 2026-10-16. Inferred, confidence low to medium: the menu builds its
list from numeric string IDs that index this blob, so adding an "XPan" choice
means more than adding a string; it needs a new list entry, a new area value
that the capture side accepts (see F-033, `image-area-tables.md`), and
saved-file size rows. Not yet found: the code that builds the list, or how
the "i" menu points at it. Method: read-only string search, SHA-256 checked
first; only short UI labels are recorded, no firmware bytes.

F-054. The 38 entries of the per-area table at `0x12049a7c` (F-033,
`image-area-tables.md`) read as seven groups of five slots plus three more.
Slot 4 of each group is the 1:1 area; slots 1 and 3 point to all-zero
records, so only slots 0 (DX), 2 (16:9) and 4 (1:1) carry data. The 1:1
records are square in every group: sensor readout 3728 by 3728 (groups 0 and
2), output sizes 3712 by 3712 (and 2784, 1856 squared for medium and small),
and tiny margin records `(16, 8)`/`(8, 8)` elsewhere. Their widths are well
under the 5568-wide DX readout, so a 5200 by 1920 XPan record would fit inside
the DX readout. The records sit at `0x115a4d6c` onward, right after a
parameter block whose base literal is `0x115a4c80`. A cluster of small
helpers at `0x1020bfc8` to `0x1020c0a0` each return the address of one entry
in that block (steps of `+4`, `+8`, `+0xc`, `+0x14`, `+0x28`, and so on up to
`+0xcc`). A scan found 117 direct callers of those helpers spread from
`0x10098e24` to well past `0x101d5c38`, plus six pointer-table references, so
reads of the block are widespread, not confined to the capture code. Observed
static decode and scan on 2026-10-16. Inferred, confidence medium: replacing
the 1:1 slot is largely a data rewrite of its records (and the matching
crop-window tables), but the helpers serve many tables, so each of the 117
callers would have to be checked for 1:1 assumptions (for example width equal
to height). Not yet done: sorting those callers by which table they read.
Method: read-only Thumb decode and scan, SHA-256 checked first; sizes are
Nikon's published numbers and no firmware bytes are recorded.

F-055. The parameter block at `0x115a4c80` (F-054) is a run of short lists of
packed 16-bit width and height pairs, five entries per list, reached by the
helpers at `0x1020bfc8` to `0x1020c07c`. The helper offsets map to lists
starting at `+0x14`, `+0x28`, `+0x34`, `+0x40`, `+0x54`, `+0x68`, `+0x7c`,
`+0x90`, `+0xa4`, `+0xb8` and `+0xcc`. Where a list holds sizes, entry 4 (the
1:1 slot) is square: for example 928 by 928 at `+0x78`, 480 by 480 at `+0x8c`,
1080 by 1080 at `+0xa0`, 120 by 120 at `+0xb4` and 374 by 374 at `+0xc8`. The
other entries in the same lists are rectangles of 3:2 and 16:9 shape (for
example 1392 by 928, 1392 by 782 and 1920 by 1080), and the entry order is
not the same in every list (the list at `+0x90` puts 16:9 at entry 1 and the
list at `+0x68` puts it at entry 2). The helper at `0x1020bfda` uses a
different base, RAM `0xc18c7de8`, with two-level indexing. Direct caller
counts: `0x1020bfda` 38, `0x1020bfc8` 23, `0x1020c05c` 12, `0x1020c02e` 8,
`0x1020c07c` 6, `0x1020c038` 6, and 17 more spread over the rest. Observed
static decode on 2026-10-16; what each list is used for (playback, thumbnail,
live-view output or something else) is NOT established, so the earlier claim
that the block does not feed live view (F-033) is neither confirmed nor
refuted here. Inferred, low to medium: replacing the 1:1 slot means giving
each size list a 65:24 rectangle in its slot 4, and checking each caller for
a square assumption. Method: read-only decode, SHA-256 checked first; sizes
only, no firmware bytes recorded.

F-056. The function at `0x101d5b36` (the main consumer named in
`image-area-tables.md`) is a crop-window builder. It takes a pointer to an
input structure and a pointer to an output structure. It reads the area slot
as a byte at input offset `+0x26` (0 to 4, with 4 the 1:1 slot) and a second
byte at input offset `+0`, and calls the block helpers of F-054 and F-055: the
list at `+0x14` (helper `0x1020bfc8`), the list at `+0x28` (`0x1020c05c`), the
list at `+0xcc` (`0x1020c072`), the list at `+0xc` (`0x1020c07c`), and two
more helpers at `0x1020c128` and `0x1020c17e`, plus `0x1020bfda` for a third
size. It copies width and height pairs into output offsets `+0` to `+0xb`,
then, when the input is valid (checked by `0x101d5ad0`), works out a centered
rectangle: an x and y offset (output `+0xc`, `+0xe`) from half the difference
between a full size and a window size, a rectangle at output `+0x10` to
`+0x16` (left, top, right, bottom), and a further width and height at output
`+0x18`, `+0x1a` that depends on a third byte (`+0x22`, values 0 to 2). When
the input is invalid it writes zeros. Observed static decode on 2026-10-16.
Inferred, confidence medium: the 1:1 slot is selected purely by the data
index in the byte at `+0x26`, with no square test in this function, and the
crop is centered, which matches a centered 65:24 strip. Not yet read: who
fills the input structure, the helpers at `0x1020c128` and `0x1020c17e`, and
what `0x101d5ad0` checks. Method: read-only Thumb decode, SHA-256 checked
first; no bytes recorded here.

F-057. The crop-window builder `0x101d5b36` (F-056) has seven direct
callers, at `0x1015382a`, `0x10153a18`, `0x1015f978`, `0x1016238e`,
`0x101936da`, `0x10193a24` and `0x101d5de8`, and no pointer-table
references. Its validity check `0x101d5ad0` returns true only when a byte at
input offset `+0x20` is 0 or 1; otherwise the builder writes zeros and
returns. In the first caller (`0x1015382a`, inside a routine that also calls
`0x10152fc8` and `0x10153444`) the input structure is not local: it is the
address `[object + 0x3a4] + 0x208`, a sub-structure of a larger state
object, so the area byte at input `+0x26` sits at `[object + 0x3a4] + 0x22e`.
Observed static decode on 2026-10-16. Inferred, confidence low to medium:
that larger object is the camera's live copy of the current shooting
settings, and the menu's image-area choice ends up in that byte; this has
not been shown. Not yet done: the other six callers, and finding the code
that writes that byte (the link from the menu pick to the crop window).
Method: read-only Thumb decode, SHA-256 checked first; no bytes recorded.

F-058. A scan of the whole image for byte stores at offset `0x22e` (the
location of the area byte from F-057, `[object + 0x3a4] + 0x22e`) found five
stores. (1) In the main code area, `0x101ae68e` writes the fixed value 1 (and
3 at `+0x22f`) while setting up a settings-like object, inside a routine whose
entry is probably `0x101ae57a`; it stores a constant, so it is a fixed setup
and not the menu pick. (2) Two stores each at `0x11defa8e`/`0x11defada` and
`0x11e758be`/`0x11e7590a`, in a higher code region, fill the byte at `+0x22e`
as part of a grid: bytes at `+0x22e`, `+0x232`, `+0x236`, `+0x23a` and so on
at steps of 4 within a row and `0xc` between rows, twelve in all, set to
either zero or a value returned by `0x11dc4530`. Six loads of the byte exist,
at `0x1034101a`, `0x10d32d32`, `0x11dbf980`, `0x11dc27fc`, `0x11e45718` and
`0x11e48594`. Observed static scan on 2026-10-16. Inferred, confidence low:
the byte is one cell of a small grid, not a single global setting, and the
code that fills the grid from the real menu choice is in the higher region
(`0x11dc....` to `0x11e7....`), not yet read. Also unread: what
`0x11dc4530` returns and the six loaders. Method: read-only scan and decode,
SHA-256 checked first; no bytes recorded here.

F-059. The grid values of F-058 come from a settings store, not from fixed
code. The supplier `0x11dc4530` is a two-instruction thunk (it sets r3 to 0
and jumps to `0x11dc4508`). That routine calls a gate `0x11dc44d0` (which
reads a global flag byte; when the flag is 1 it returns a not-ready result)
and, when allowed, tail-calls `0x11df06b8`. That routine reads a record count
at object offset `+0x3ce`, builds a text key from two strings with a
printf-style formatter (`0x11bf18c4`), looks the key up in a table object at
offset `+0xf0` (`0x11bf26ec` and `0x11bf26d4`), and falls back to a default
passed in r3 (here 0) when the key is missing or out of range. Observed
static decode on 2026-10-16. Inferred, confidence medium: the higher code
region (`0x11dc....` to `0x11e7....`) holds a text-keyed settings database,
and the area byte is read from it by key. If so, the menu's saved image-area
choice has a text name that can be found as a string. Not yet done: finding
which key names the image area (an earlier search for `ImageArea` and
`IMAGE_AREA` found nothing, so the key may be spelled differently or built
from pieces), and who writes it when the menu is used. Method: read-only
decode, SHA-256 checked first; no bytes recorded here.

F-060. The firmware holds a run of 354 setting names, each prefixed
`eDSID_`, in one block from `0x11c99170` to `0x11c9db60` (the earlier hits at
`0x11c991a8` and `0x11c9bda8` are part of it). They name settings in the
camera's settings store (F-059). Observed static string search on 2026-10-16.
Three findings matter to the owner's goals. (1) The "i" quick menu is
customizable in the data: names `Setting_CustomizeImenuStill_UpperRowLeft1`
to `...6` and `...BottomRowLeft1` to `...6`, with Movie twins, give twelve
slots per kind. (2) There is a setting for the AE-L/AF-L button's job:
`Setting_FuncAeAfLockButtonShooting` and `Setting_FuncAeAfLockButtonMovie`.
The camera already lets that button be reassigned, so a tracking function
could be a new choice in that list, a different route from the input-routing
research. (3) No name in the list mentions image area, crop or aspect. The
only image-related names are `Setting_ImageSize`, `Setting_ImageCombination`,
`Setting_MovieSize`, `Setting_RawRecord` and `Setting_JpegPolicy`. So the
"Choose image area" choice is either stored under another name, not in this
list, or kept in the size setting. Inferred, confidence low. Not yet done:
reading what `Setting_ImageSize` holds, and finding where the list's names
map to numeric setting ids. Method: read-only string search, SHA-256 checked
first; only short setting names are recorded, no firmware bytes.

F-061. The `eDSID_` names of F-060 are referenced from one pointer table.
The entry for `Setting_ImageSize` sits at `0x1204ea68`; its neighbours in the
same table are `Setting_JpegEncodeQuality` (`0x1204ea5c`),
`Setting_ImageCombination`, `Setting_JpegPolicy` (before it) and
`Setting_RawRecord`, `Setting_IsoSense`, `Setting_IsoSenseType` (after it),
so the table runs in a fixed order with the image-quality settings grouped
together. A run of small numbers ends right before the table
(`0xc31` to `0xc34`, `0x204`, `0x20b`, `0x1d05`, `0x106`, then
`0xffffffff`), which may be a list of ids for an earlier group, but it is
not paired entry for entry with these names. No entry between the quality
settings and the ISO settings names an image area, crop or aspect, which
fits F-060. Observed static decode on 2026-10-16. Inferred, confidence low:
the image-area choice is not one of the named data-store settings, so it
probably lives in the shooting-parameter structures of F-056 and F-057 and is
reached through a separate menu item table. Not yet done: the table that
defines the "Choose image area" menu item itself, found from the menu text
(F-053), and the numeric id that goes with the `Setting_ImageSize` name.
Method: read-only decode, SHA-256 checked first; only short setting names are
recorded, no firmware bytes.

F-062. The menu text for image areas is stored once per language, about 30
blocks, with no string terminators and no plain pointers to the strings
(a search for pointer words to the four copies of the title, at `0x10e88c14`,
`0x10e890cc`, `0x10e890f0` and `0x10e8ed48`, found none), so the menu most
likely refers to each string by number and offset. In the English block the
area labels read "DX   (24x16)" at `0x10e89112`, then "1:1   (16x16)" and
"16:9  (24x14)", with the label text of each area followed by size lines such
as "3712x3712; 13.8 M" and "2784x2784" (which echo the 1:1 sizes of F-054).
Ten language blocks hold the 1:1 label, for example at `0x10e75bbe`,
`0x10e9423a`, `0x110cf248` and `0x1125fc1e`, and about thirty hold the "DX"
label (for instance `0x10eae006` German, `0x10ed7e70` French,
`0x10f8e532` Chinese). Observed static string search on 2026-10-16. Inferred,
confidence medium: because the owner accepts keeping the "1:1" label, no text
needs to change for a first version. A shorter in-place label such as
"65:24 (24x9)" (the 24 mm DX width gives about 8.9 mm of height) would fit the
13 characters of the 1:1 label, but the size lines next to it ("3712x3712;
13.8 M" and similar) are also wrong for XPan and would need the same care.
Not yet done: the table that maps menu items to string numbers, and whether
text lengths are stored somewhere that must also change. Method: read-only
string search, SHA-256 checked first; only short UI labels recorded, no
firmware bytes.

F-063. The image-area strings carry no length prefix or terminator: the bytes
directly before each title copy (`0x10e88c14`, `0x10e890cc`, `0x10e890f0`)
and the first choice label (`0x10e89112`) are just the last characters of the
previous string. So each language block must be read through a separate
index of offsets or lengths, not by scanning for terminators. The language
blocks are about `0x24ef4` bytes apart in the examples checked (English
`DX` label at `0x10e89112`, German at `0x10eae006`). Observed static
inspection on 2026-10-16. Inferred, confidence low: the index sits at the
start of each block or in a single shared table, and a label change that
keeps the exact string length (for example "1:1   (16x16)" to
"65:24 (24x9) ", both 13 characters) would not need the index touched. Not
yet found: the index itself. Method: read-only inspection, SHA-256 checked
first; only a few raw bytes were looked at and none are recorded here.

F-064. The menu strings of F-053, F-062 and F-063 are indexed. Three
36-entry pointer tables at `0x112f41e0`, `0x112f4270` and `0x112f4300` give,
for each of 36 languages, the start of three regions. For the second language
(English) they are `0x10e79dac`, `0x10e7bc4c` and `0x10e9a9c2`. The first
region (`0x1ea0` bytes) is a list of 1960 32-bit byte offsets; the second is
the packed UTF-16 text, and string number n runs from offset n to offset n+1
(checked: the offsets of the three "Choose image area" copies, the "DX"
label and its neighbours all match). String numbers found: size lines 733
and 734, title 735, a title variant 736, the DX label 737, "12-bit" 738,
"14-bit" 739, the 1:1 label 1454 and the 16:9 label 1455. So the area
labels have numbers, and the 1:1 label is string 1454. Observed static
decode on 2026-10-16; confidence high for the index, since every checked
string matched. Because strings are packed back to back, a label of a
different length means changing the offsets after it, so a same-length label
(F-063) remains the safe form. Not yet done: the table or code that uses
these string numbers to define the menu items. Method: read-only decode,
SHA-256 checked first; only short UI labels and numbers recorded, no
firmware bytes.

F-065. The three area-label string numbers of F-064 sit together in a small
list at `0x11ff2b4c`: 32-bit values 737 (DX), 1454 (1:1) and 1455 (16:9),
followed by the value `0x15aa` and a zero, and preceded by the value
`0x123e`. A similar list sits just before it at `0x11ff2b34`: 681, 682, 683
and 1014, preceded by a word that holds `0x15aa` and `0x123c` as two 16-bit
halves. Another record at `0x11ff2b60` starts with 737 again. Observed
static read of about twenty words on 2026-10-16, run after the owner approved
the narrower read. Inferred, confidence low: each list is one menu item's
choices, the values `0x123c` and `0x123e` (two apart) are menu item or
setting ids, and `0x15aa` is a type or end marker shared by the lists. None
of this is shown. What matters for the plan is that the 1:1 choice is
reached by a plain list of string numbers, so keeping the "1:1" string
number and swapping the text in place would leave the list alone. Not yet
done: what reads this list, what `0x123e` is, and what stores the pick.
Method: read-only read of one small data list, SHA-256 checked first; only
numbers recorded, no firmware bytes.

F-066. No word in the image equals the address of the label list of F-065
(`0x11ff2b4c`) or of the three neighbouring words checked (`0x11ff2b34`,
`0x11ff2b44`, `0x11ff2b48`), with or without the Thumb bit, and no word
points anywhere in `0x11ff2b20` to `0x11ff2b80`. Observed static scan on
2026-10-16, run by the owner in a terminal. Inferred, confidence medium: the
list is one record inside a larger array that is reached from its base (or by
an index and a stride), not by pointing at each record. Not yet done:
finding the base of that array (scan backward from `0x11ff2b34` for the
repeating record shape) and searching for pointers to the base. Method:
read-only scan, SHA-256 checked first; addresses only, no firmware bytes.

F-067. Layout around the label list of F-065, from an owner-run read of 512
bytes (`0x11ff2a4c` to `0x11ff2c4c`) on 2026-10-16. (1) From `0x11ff2a4c`
there are two runs of 32-bit pointers into low image data: 26 pointers into
`0x11c912b4` to `0x11c913e0` (to `0x11ff2ab4`), then one into `0x11c9832c`,
then 24 pointers into `0x11c926bc` to `0x11c9277c` (to `0x11ff2b10`). They
look like pointers to name strings, in two groups, but the names were not
read. (2) From `0x11ff2b14` on there are no more pointers: small numbers and
16-bit pairs, with the lists of string numbers packed back to back. Examples:
the list `0x2a9, 0x2aa, 0x2ab, 0x3f6` at `0x11ff2b34`; the area-label list
`0x2e1, 0x5ae, 0x5af` at `0x11ff2b4c`; a descending run `0x14e` to `0x149`
at `0x11ff2b78`; and repeated groups such as `0x2e7, 0x4c1, 0x2ee, 0x2f0,
0x2f1, 0x2e9, 0x2ea, 0x2ef, 0x2f2, 0x314` twice at `0x11ff2bb4` and
`0x11ff2bdc`. (3) No word in the image points to any aligned address in the
512 bytes. Observed. Inferred, confidence low to medium: the two pointer runs
are name tables for menu items, and the lists after them are the items'
choice lists, tied together by position or by a stored count rather than by
pointers. Not yet done: reading the names the pointers lead to, to learn
which name belongs to the area-label list. Method: read-only read of one
small data block, SHA-256 checked first; numbers and addresses only, no
firmware bytes.

F-068. Correction to F-067. The two pointer runs before the area-label list
are not menu-item name tables. An owner-run read of the text they lead to
(on 2026-10-16) shows the first run, `0x11ff2a4c` to `0x11ff2ab4`, is a list
of 27 focal-length labels from "50mm" through "4000mm" (in a scrambled
order), then one label "F--" at `0x11ff2ab8`, and the second run,
`0x11ff2abc` to `0x11ff2b10`, is 22 f-number labels from "F1.2" through
"F22". These look like the value lists for manual lens data entry. So the
block from `0x11ff2a4c` onward is a flat pool of choice and value lists for
many different settings, one after another, and the area-label list is one
entry in that pool. Observed (the text) and inferred (the pool, confidence
medium). Because nothing points at individual lists (F-066), the code most
likely reaches them by an index into the pool or by a base address plus a
running offset. Not yet done: finding that base. The next read is to list
every word in the image whose value falls inside the pool's address range,
and every code address that loads such a value. Method: read-only read of
short text labels, SHA-256 checked first; only labels recorded, no firmware
bytes.

F-069. Why nothing in the code points at the label pool (F-066, F-068). An
owner-run scan on 2026-10-16 found no code that builds a `0x11ff....` address
in two halves, and only two data words in `0x11ff2000` to `0x11ff3000`
(`0x11ff2da4` at `0x1063cd48` and `0x11ff2200` at `0x109b3378`); the one
instruction-looking "loader" at `0x1063cb64` sits in data and decodes to
nonsense, so it is a false match. This region is initialized data, copied to
RAM at startup, so code uses the RAM copy. Two known pairs give the same
fixed offset between stored address and RAM address: `0x12049a7c` to
`0xc18c7de8` (F-032) and `0x1204b7e8` to `0xc18c9b54`
(`tracking-input-bank-selection.md`), both `+0xaf87e36c`. If that offset holds
across the region, the pool `0x11ff2000` to `0x11ff3000` lives at RAM
`0xc187036c` to `0xc187136c`, and the area-label list `0x11ff2b4c` at RAM
`0xc1870eb8`. Observed (the scan results and the two pairs), inferred,
confidence medium (the offset is assumed to hold for the pool). Next: search
for code that loads values in `0xc187036c` to `0xc187136c`. Method: arithmetic
on recorded addresses plus the owner-run scan; no firmware bytes recorded.

F-070. The RAM copy of the pool is referenced directly by code. An owner-run
scan on 2026-10-16 found 416 32-bit words in the image whose values fall in
the predicted RAM range `0xc187036c` to `0xc187136c` (F-069), and 406
pc-relative loads of them. The first 60 (sorted by address) all sit in a code
module that starts near `0x1030bf08` and runs at least to `0x1030ea14`, and
point at items inside the pool. This confirms F-069: the stored-to-RAM offset
`+0xaf87e36c` holds for the pool, and menu code reaches its lists by direct
RAM address. One of the loaded values is `0xc1870e80`, loaded into r8 by code
at `0x1030c880`; it is `0x38` bytes before the area-label list at RAM
`0xc1870eb8`, which is the start of the record whose header words precede the
list (stored address `0x11ff2b14`, F-067). Observed. Inferred, confidence
medium: the code near `0x1030c880` builds or reads the menu record that holds
the image-area label list. The full 416-word list was not printed (the scan
shows only 60). Next: decode the code around `0x1030c880` and list the words
and loaders in `0xc1870e00` to `0xc1870f40`. Method: owner-run read-only scan,
SHA-256 checked first; addresses only, no firmware bytes recorded.

F-071. Who uses the area-label list. An owner-run read on 2026-10-16 of every
word and load in the RAM range `0xc1870e00` to `0xc1870f40` (50 words, 54
loads) shows that the area-label list, at RAM `0xc1870eb8`, is loaded in
exactly two places, both in one routine in the `0x1030f...` block: `0x1030f87a`
and `0x1030f8a8`. The two lists next to it are loaded there too: `0xc1870eb0`
at `0x1030f856`, and `0xc1870e98` and `0xc1870ea0` at `0x1030f7b6` and
`0x1030f78c`, with `0xc1870ed8`, `0xc1870ee4`, `0xc1870efc` and `0xc1870f08`
at `0x1030fa18`, `0x1030f9dc`, `0x1030faae` and `0x1030fa6e`. In contrast,
the pool entries at `0xc1870e98`, `0xc1870ea0`, `0xc1870ec4`, `0xc1870ecc`,
`0xc1870ed8`, `0xc1870ee4`, `0xc1870efc`, `0xc1870f08` and `0xc1870f20` are
each loaded again in at least four other code blocks (around `0x10315a..`,
`0x103767..`, `0x103e04..` and `0x10430f..`), but `0xc1870eb0` and
`0xc1870eb8` are not. Separately, the routine at `0x1030c874` loads
`0xc1870e80` as a base and loops over elements, calling `0x1030bc58`,
`0x10454210` and `0x1030bc00` for each, which is consistent with a menu or
list builder that creates one object per element of a table; its use of the
table at `0xc1870e80` is not fully read. Observed (the loads) and inferred,
confidence low to medium (the builder reading). So the "Choose image area"
choices appear to be used only by the routine around `0x1030f87a`. Next:
decode `0x1030f780` to `0x1030f920`. Method: owner-run read-only scan and
decode, SHA-256 checked first; addresses and instructions only, no firmware
bytes recorded.

F-072. The routine that builds the image-area menu choices, read from an
owner-run decode of `0x1030f780` to `0x1030f920` on 2026-10-16. The routine
at `0x1030f844` (entry pushes 14 registers) copies four words from a source
table onto its stack, then loops with counter r4 from 0 to 1 (compare with 2
at `0x1030f8dc`). Each pass tests one of the stack words with the function
`0x10484d90`; if that returns nonzero, or if the word equals the current
value, it appends an entry to an output list. The current value is the byte
at offset `+0x15b` of a settings structure whose address is a literal near
`0x1030f84c`; the neighbouring byte at `+0x15a` is used by two similar
routines at `0x1030f7a0` and `0x1030f7be`, so the structure holds several
adjacent selection bytes. An appended entry gets a 16-bit string number from
the list at RAM `0xc1870eb8` (the area-label list, F-065), indexed by r4, at
offset `+4` (the first word of the list, 737 for the DX label, goes into a
separate header slot at `0x1030f88e`), so pass 0 contributes string 1454 (the
1:1 label) and pass 1 string 1455 (the 16:9 label). The routine also stores
the entry's numeric value into a table with an 8-byte stride and a count at
`[r8 + 0xc]`. A sibling routine at `0x1030f8e4` calls it, then calls
`0x1051a17c` with the current value to look up the matching entry. Observed
(the code), inferred, confidence medium (the reading of the loop as the
image-area choice builder rests on the string numbers 1454 and 1455 and the
two-pass shape). Consequences if right: DX is always shown, 1:1 and 16:9 are
shown only when `0x10484d90` allows them or they are current, and the 1:1
slot's numeric value and label come from one source table and the
area-label list. Not yet read: the literals this routine uses, the source
table of numeric values, and what `0x10484d90` checks. Method: owner-run
read-only decode, SHA-256 checked first; addresses and instruction reading
only, no firmware bytes recorded.

F-073. What the area-choice builder of F-072 reads, from an owner-run
read on 2026-10-16. Its literals are: the source table of numeric values at
`0x10740eb0` (in the main image, read as four words by the routine, not yet
printed); the settings structure at RAM `0xc2016a68` (the current-value byte
is then at `0xc2016bc3`); the output list holder at RAM `0xc1828be4` (stored
copy at `0x11faa878`, first word `0x1900`; a count at `+0xc` and a 16-bit
array at `+0x20`); the output table at RAM `0xc2019624`; the 16-bit id array
at RAM `0xc1870eb0` (stored `0x11ff2b44`); and the string-number list at RAM
`0xc1870eb8` (stored `0x11ff2b4c`). The 16-bit id array reads `0x15aa`,
`0x123c`, `0x123e`, so the header id is `0x15aa`, and the two choices carry
ids `0x123c` (pass 0, string 1454, the 1:1 label) and `0x123e` (pass 1,
string 1455, the 16:9 label), while the DX label (string 737) is the list's
first word and goes to a header slot. The checking function `0x10484d90` is
only a one-instruction branch to `0x1052d7c2`; the block around it is a run of
branch thunks and short wrappers that test bit 4 of a flag byte and call
`0x104bd3c0` before tail-calling another routine (`0x104762ca`, `0x104762ce`,
`0x104762d2` and `0x104762d6` for the first four). Observed. Inferred,
confidence medium: the item ids `0x123c` and `0x123e` identify the 1:1 and
16:9 entries in the menu, and the real check is at `0x1052d7c2`. Not yet
read: the four words at `0x10740eb0`, the code at `0x1052d7c2`, and what
uses the item ids. Method: owner-run read-only scan and decode, SHA-256
checked first; addresses and numbers only, no firmware bytes recorded.

F-074. Numeric values behind the image-area choices, from an owner-run read
on 2026-10-16. The four words at `0x10740eb0` are `0x1003`, `0x1004`, `4`
and `2`. In the choice builder of F-072 and F-073 the first two are passed
one at a time to the check `0x10484d90`, and the last two are compared with
the current-value byte at `0xc2016bc3`. So the choice with the 1:1 label
(string 1454, id `0x123c`) uses availability code `0x1003` and stored value
4, and the choice with the 16:9 label (string 1455, id `0x123e`) uses code
`0x1004` and stored value 2; DX is the default and, by elimination and by the
slot layout of F-054 (slots 0, 2 and 4 carry data), value 0. A neighbouring
routine at `0x1030f7e4` maps a stored value to the same codes (value 4 to
`0x1003`, value 2 to `0x1004`). This agrees with the capture tables, where the
1:1 area is slot 4 and 16:9 is slot 2. The check chain is longer than first
read: `0x10484d90` jumps to `0x1052d7c2`, which is itself one instruction, a
branch to `0x104270a4`, so the real availability test is at `0x104270a4`. The
code that follows `0x1052d7c6` is a different routine (it switches on a
passed value). Observed (the words), inferred, confidence medium (the reading
of the four words as codes and values rests on the loop shape and the
neighbouring routine). Consequence for XPan: replacing 1:1 can keep the same
stored value 4, the same item id `0x123c` and the same string number 1454,
and change only what slot 4 means in the size tables and the label text.
Not yet read: `0x104270a4`, what decides whether a code is available, and the
setter that writes the stored byte. Method: owner-run read-only read and
decode, SHA-256 checked first; numbers only, no firmware bytes recorded.

F-075. Correction to the end of F-074's check chain. An owner-run decode of
`0x104270a4` to `0x10427170` on 2026-10-16 shows that code is not an
availability test. The first stub loads a pointer and the number `0x20c`
(524) and branches to a shared routine at `0x101993de`; the following stubs
load other pointers and numbers (`0x21e`, `0x22d`, `0x243`, `0x25a`) and
call shared routines at `0x10199436`, `0x101995c8`, `0x101995da` and
`0x10199674`. That shape (a text pointer and a source line number passed to
a shared routine) is typical of error or assertion reporting. After the
stubs comes a table of about 30 branches to routines at `0x102364..`,
`0x105060..` and `0x104762..`. So the route `0x10484d90` to `0x1052d7c2` to
`0x104270a4` does not reach a predicate for 1:1. More likely the first jump at
`0x1052d7c2` is a linker or patch veneer that was misread, and the routine
that actually takes the code (`0x1003` or `0x1004`) is the one starting at
`0x1052d7c6`, which saves registers, switches on its first argument by
comparing it with literals, and uses constants such as `0x3ef` and `0x118`.
Observed (the stubs), inferred, confidence low (the veneer reading). Not
yet done: printing the raw encodings at `0x10484d90` and `0x1052d7c2` to
confirm the targets, and reading the literals and the switch in the routine
from `0x1052d7c6`. Method: owner-run read-only decode; instructions only, no
firmware bytes recorded.

F-076. Corrects F-075. An owner-run read on 2026-10-16 printed the raw bytes
of the two jump instructions and the routine after them. Working the
encodings by hand confirms both jumps: `0x10484d90` branches to `0x1052d7c2`
(`a8 f0 17 bd`), and `0x1052d7c2` branches on to `0x104270a4`
(`f9 f6 6f bc`). So the chain from the image-area builder's check call is
real: two one-line long-jump veneers ending at the stub at `0x104270a4`. That
stub keeps the caller's first argument (the availability code `0x1003` or
`0x1004`), adds a text pointer and the number `0x20c`, and branches to the
shared routine at `0x101993de`. Its siblings do the same with other numbers
(`0x21e`, `0x22d`, `0x243`, `0x25a`) and other shared routines. This pattern
fits a wrapper that records the caller's source file and line next to the
query (the same macro style used for logging), so it is probably not error
reporting, and the real availability test is the shared routine at
`0x101993de`. The routine at `0x1052d7c6` is unrelated: it compares a message
value against event numbers such as `0x4100040`, `0x4100024` and `0x410001c`
and works on RAM structures at `0xc18c568c`, `0xc2588e6c`, `0xc2589338` and
`0xc2588c38`, so it is an event dispatcher. The earlier guess that it is the
check is withdrawn. Observed (the bytes, the literals), inferred,
confidence low to medium (the wrapper reading). Not yet read: `0x101993de`.
Method: owner-run read-only decode; instructions and numbers only, no
firmware bytes recorded.

F-077. End of the check chain, from an owner-run decode on 2026-10-16. The
shared routine `0x101993de` is a five-instruction wrapper: it overwrites its
second argument with a stack address, calls `0x10199ab4` with the code and
that address, and returns the result. So the text pointer and line number
that the stub at `0x104270a4` passes (F-076) are ignored here; they look like
debug arguments. Nearby are batch versions that loop over arrays of codes
and values (`0x101993e8`, `0x1019941e`, `0x10199438`) and call
`0x100f303c`, `0x100f308a` and `0x100f3114`, which read like get and
compare calls on a settings store keyed by 16-bit codes. Observed. Inferred,
confidence medium: whether 1:1 is offered is a lookup of the property code
`0x1003` (16:9 is `0x1004`) in that store, not logic in the menu routine. So
an XPan choice that keeps value 4, item id `0x123c`, string 1454 and code
`0x1003` inherits whatever rule already decides when 1:1 is offered. Not read:
`0x10199ab4` and the code that sets `0x1003`; neither is needed for a first
version, so they are parked. Method: owner-run read-only decode; instructions
and numbers only, no firmware bytes recorded.

F-078. Corrects the area byte of F-057 and records a read-only baseline. In
the simulator (assisted startup, one fresh run, guest scratch memory only,
nothing modified), calling the crop-window builder `0x101d5b36` with an
input structure of zeros except for chosen bytes shows that the area slot is
the first byte of the structure, not the byte at offset `+0x26`. With the
first byte 0, 2 and 4 the builder returns, for the large size, a readout of
5600 by 3728 and a window of 5584 by 3720 (DX, offsets 16 and 8), 5584 by
3136 (16:9, offsets 16 and 8) and 3720 by 3720 (1:1, offsets 8 and 8); the
medium and small sizes (third structure byte `+0x22` set to 1 and 2) give
4176 by 2784 and 2784 by 1856 for DX, and 2784 by 2784 and 2790 by 2790 for
1:1. Slots 1 and 3 return all zeros. A nonzero byte at `+0x26` returns one
fixed result (readout 5656 by 3918) whatever the area, so that byte is a mode
flag, not the area. Observed runtime, high within this fixture. This confirms
F-054 to F-056 on a running simulator: the 1:1 slot yields a square window
because its records are square. Repro: confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/claude-cropbuilder-byte0-private.py" --output "$WORK/private-inputs/claude-cropbuilder-byte0-NN"`
with a fresh output directory. The script stays under WORK and is not
committed.

F-079. First change test for the plan in `xpan-replace-1to1-plan.md`, in the
simulator only (one run, guest memory only). The RAM copy of the per-area
pointer table (`0xc18c7de8`, F-032) was temporarily repointed, for the four
1:1 entries (indices 4, 9, 14 and 19), at scratch records with XPan-shaped
sizes (5216 by 1936 readout, 5200 by 1920 output sizes), then the builder was
called for area 4. Result, large size: the window became 5208 by 1928 with
offsets 8 and 8, a ratio of 2.70 to 1 (65:24 is 2.71 to 1), so the output
follows the 1:1 records and a 65:24 shape comes out when the records are
changed; the DX and 16:9 results did not change. Result, medium and small
sizes: nonsense values (negative and huge windows), so the records I wrote for
indices 9 and 19 do not match the layout those paths expect; the layout of
those two groups is still unread. The original pointers were restored and
verified. Observed runtime, medium confidence: the large-size path is
confirmed, the other two are not. Repro: confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/claude-xpan-records-private.py" --output "$WORK/private-inputs/claude-xpan-records-NN"`
with a fresh output directory. The script stays under WORK and is not
committed. No firmware changed.

F-080. Completes the change test of F-079 and explains its failure. An
owner-approved simulator run on 2026-10-16 called the three lookup helpers of
the crop-window builder (`0x1020c07c`, `0x1020c128`, `0x1020c17e`) with the
arguments the builder passes. For area 4 (1:1) they return addresses inside
the per-area records: the size helper reads record 19 at byte offsets 12 and
20 (for the medium and small sizes), the margin helpers read records 29 and
34. The records are longer than first thought: record 19 spans 24 bytes (12
shorts: three large pairs, then medium pairs), as does the DX record 15. In
F-079 the scratch record for index 19 was only 12 bytes, so the medium and
small reads ran past it into stray memory; that explains the nonsense. A
repeat with a 24-byte record for index 19 and the earlier records for 4, 9
and 14 gives, for area 4: large window 5208 by 1928 (offsets 8, 8), medium
3900 by 1440 (a ratio of 2.708, exactly 65:24), small 3906 by 1446 (offsets
6, 6), with the 'extra' pair following the records at 3900 by 1440 and 2600 by
960. DX (5584 by 3720) and 16:9 (5584 by 3136) were unchanged, and the
original table pointers were restored and verified. Observed runtime,
high within this fixture: replacing the data of the four 1:1 records is enough
for the crop-window builder to give a 65:24 shape at all three sizes. The
large window is 2.70 to 1 because the margin offset of 8 is subtracted, so
the readout record would need to be 5208 by 1936 to land on exactly
5200 by 1920. Not shown: any effect on live view, capture or saved files.
Repro: confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/claude-xpan-records2-private.py" --output "$WORK/private-inputs/claude-xpan-records2-NN"`
with a fresh output directory; the probe is
`claude-helpers-probe-private.py`. The scripts stay under WORK and are not
committed. No firmware changed.

F-081. The stored image-area byte is a mirror that the camera refreshes.
In the simulator (assisted startup, guest memory only, one run for the
timing and one earlier run for the live-view check), the byte at
`0xc2016a68 + 0x15b` (`0xc2016bc3`, the current-value byte of F-072 and
F-073) reads 0 at start. A write of 4 held when read back immediately and
after 0.05 simulated seconds, and was back at 0 after 0.65 seconds, so
something rewrites it from another source within that time. With the byte
set to 4 or 2 and the live view refreshed, the picture showed no black rows
and no change beyond the animated band already present in the baseline
(159 changed rows both times), so the live view does not react to this
byte. Observed runtime, medium confidence (one run each). This agrees with
F-033 (no display code reads the image area). Consequence for the plan: to
make the camera adopt the XPan choice, the source behind the mirror (the
settings store of F-059 and F-077) has to change, or the code that writes the
mirror has to be found; writing the mirror alone does nothing. A write
watchpoint to find that code left the debugger link out of step and a
simulator process behind, which I stopped; the firmware file hash and the
simulator tree were checked unchanged afterwards. Next: a static scan for
stores to offset `0x15b` from the structure at `0xc2016a68`. Repro of the
timing: confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/claude-areabyte-probe-private.py" --output "$WORK/private-inputs/claude-areabyte-probe-NN"`
with a fresh output directory. The scripts stay under WORK and are not
committed. No firmware changed.

F-082. Owner-run scan on 2026-10-16 for who touches the stored area byte of
F-081. The structure address `0xc2016a68` is loaded by 446 pieces of code
(literal words at `0x102f3a30`, `0x102f4d38`, `0x1030b46c` and others), so
it is a large shared state structure, not a private one. Byte stores with
offset `0x15b` from any base register: ten, at `0x100fc0b8` and
`0x10367fd2` (main code) and at `0x11dc04fe`, `0x11dc17e6`, `0x11de6eba`,
`0x11deef16`, `0x11e46296`, `0x11e4757e`, `0x11e6ccee` and `0x11e74d46` (the
higher settings-store region of F-058 and F-059). Byte loads with that
offset: eight, at `0x101df8b8`, `0x101e00da`, `0x1030f862` (the choice
builder), `0x1030f8e8`, `0x1030f928`, `0x1030f92e`, `0x11dc0422` and
`0x11e461ba`. Observed static scan. Inferred, confidence low to medium: the
eight high-region stores include the code that refreshes the mirror from the
stored setting, since that region fills the neighbouring grid bytes at
`+0x22e` (F-058); which of them writes this byte for the image area is not
known, and some may be other structures that share the offset. Next: decode a
short window around each of the ten stores and the two main-code readers.
Method: owner-run read-only scan, SHA-256 checked first; addresses only, no
firmware bytes recorded.

F-083. What the ten stores of F-082 do, from an owner-run decode on
2026-10-16. (1) `0x100fc0b8` is inside a reset routine that writes pairs of
bytes at low offsets (`+0x11`, `+0x12`, `+0x15` to `+0x1c`) and a copy of each
pair `0x140` higher (`+0x151` to `+0x15c`), so the area `+0x151` to `+0x15c`
is a shadow of the bytes at `+0x11` to `+0x1c`. (2) `0x10367fd2` is inside a
routine that copies settings one byte at a time from a source structure
(register r8) into this structure: a run from r8 offsets `0x430` to `0x448`
(stride 4) goes into `+0x153` to `+0x15a`, then `ldrb r0, [r8, #0x2cc]` goes
into `+0x15b`, then r8 `+0x44c` goes into `+0x15c`. The `0x2cc` source breaks
the stride, which fits an unrelated setting copied in between. (3) The
stores at `0x11dc04fe`, `0x11e46296`, `0x11dc17e6` and `0x11e4757e` write a
register or the value 1 to `+0x15b` through a base loaded from `[object +
0xe4]`, followed by a store of 1 to `+0x15c`, which reads like marking an
entry as set or changed; and the stores at `0x11de6eba`, `0x11e6ccee`,
`0x11deef16` and `0x11e74d46` clear it in reset code. (4) The two main-code
readers, `0x101df8b8` and `0x101e00da`, read `+0x15b` in loops of 18 entries
(three-byte steps), so the offset is also one entry of an 18-entry array, and
the value there may not be the image area in every structure that uses the
offset. Observed (the code). Inferred, confidence low to medium: for the
structure at `0xc2016a68`, the mirror byte `+0x15b` is filled from `+0x2cc` of
the source structure by the routine around `0x10367fd2`, so the real stored
image-area setting is at `+0x2cc` of that source. Not yet read: the start of
that routine, which structure r8 is, who calls it, and who writes `+0x2cc`.
Method: owner-run read-only decode; instructions only, no firmware bytes
recorded.

F-084. Owner-run scan on 2026-10-16 for byte stores with offset `0x2cc`, the
source offset of the image-area setting in F-083. The whole image has exactly
two: `0x1019a068` and `0x10367d26`. The second lies `0x2ac` bytes before the
mirror store at `0x10367fd2`, so it is probably in the same long routine,
which would then copy settings in both directions (one half into the
structure at `+0x2cc`, another half out of it). The search for the start of
that routine found no instruction that saves the return register within
`0x600` bytes before `0x10367fd2`, so the routine is longer than that. Byte
loads at offset `0x2cc` were not counted. Observed static scan. Inferred,
confidence low to medium. Not yet read: the code around both stores, the true
start of the routine and its callers. Method: owner-run read-only scan,
SHA-256 checked first; addresses only, no firmware bytes recorded.

F-085. What the two stores at offset `0x2cc` do, from an owner-run decode on
2026-10-16. (1) `0x1019a068` is in a routine that fills a small block at
`+0x2c8` to `+0x2cf` of one object from another record (`ldrb r1, [r0, #0x67]`
then `strb r1, [r4, #0x2cc]`, with a 32-byte block copy to the same area on
the other path), so it is an unrelated structure and not the image-area
setting. (2) `0x10367d26` is in a long routine whose start is probably
`0x10367260` (the nearest register-saving instruction before both
`0x10367d26` and `0x10367fd2`). There it runs `ldrb r0, [r8, #0x408]` then
`strb r0, [r6, #0x2cc]`, between similar copies (`r8 + 0x2f4` to `r6 +
0x2cb`, `r8 + 0x1b4` to `r6 + 0x278`), and then adds `0xd8` to r6, so the
destination steps by `0xd8` bytes per item in a loop. Observed (the code).
Inferred, confidence low to medium: the image-area value starts as a byte at
`+0x408` of the source structure in r8, is copied into a per-item snapshot at
`+0x2cc`, and from the snapshot into the mirror byte `+0x15b` (F-083). Not
yet read: the start of the routine, what r8 is, its callers, and who stores a
byte at `+0x408`. Method: owner-run read-only decode; instructions only, no
firmware bytes recorded.

F-086. The snapshot routine and the writers of its source byte, from an
owner-run read on 2026-10-16. (1) The routine at `0x10367260` is confirmed as a
function start (it saves eight registers and reserves `0x638` bytes of
stack). It first calls `0x10367196`, loads two structure addresses from its
literal pool (r8, the source, and r6, the destination), and copies a series of
fields from the source into the destination, including `r8 + 0x44`, `+0x48`
and `+0x4c` and single bytes at `+0`, `+4`, `+8`, `+0xc`, `+0x34` and
`+0x1e0`. (2) It has 20 direct callers: `0x10301e46`, `0x103039e6`,
`0x10304552`, `0x1030b40c`, `0x1030b6b4`, `0x1030b7a4`, `0x1030ca70`,
`0x1030f9ce`, `0x1030fc80`, `0x103117ba`, `0x10311b9a`, `0x10368250`,
`0x10368360`, `0x10369994`, `0x103cbf68`, `0x103dddf6`, `0x103df306`,
`0x10450112`, `0x104c2cac` and `0x104c2cd0`; one of them, `0x1030f9ce`, sits
right beside the image-area choice builder (F-072) in the same module, which
fits the quick rewriting of the mirror seen in F-081. (3) Byte stores with
offset `0x408`: eight, at `0x11dcd08e`, `0x11dcd14c`, `0x11dcd198`,
`0x11dcd674` and, in a second copy of the same code, `0x11e52e12`,
`0x11e52ed0`, `0x11e52f1c` and `0x11e533f8`. Byte loads with that offset:
six, at `0x10367d22` (the snapshot routine), `0x1037416c`, `0x11dcd662`,
`0x11dcdbfa`, `0x11e533e6` and `0x11e5397e`. Observed (the scan and the
routine start). Inferred, confidence low to medium: the real image-area
setting is written by code in the higher settings-store region (the four
stores in `0x11dcd...`, with a duplicate copy in `0x11e52...`), and the
snapshot routine copies it forward on demand. Not yet read: the code around
those stores and the loads, and which structure the two literal addresses are.
Method: owner-run read-only decode and scan; instructions and addresses only,
no firmware bytes recorded.

F-087. Corrects F-086. An owner-run decode on 2026-10-16 shows the eight
byte stores at offset `0x408` in the higher settings-store region
(`0x11dcd08e`, `0x11dcd14c`, `0x11dcd198`, `0x11dcd674` and the duplicate
copy) do not write the image-area setting. In that code the object at r4 has
a buffer pointer at `+0x3fc`, a byte at `+0x400`, a handle at `+0x404` and a
byte at `+0x408` that is set to 1 after a buffer is allocated and filled, and
to 0 when the buffer is freed (`0x11dcd060` frees `[+0x3fc]` and clears
`+0x3fc` and `+0x400`). So `+0x408` there is a "buffer ready" flag in an
unrelated object, a coincidence of offset. What stands: the snapshot routine
at `0x10367260` loads two structure addresses, `0xc2018a2c` (the source, r8,
also passed to `0x10484d8c`) and `0xc2016a68` (the destination, r6), and
copies the image-area byte from source `+0x408` to the snapshot `+0x2cc`
(F-085). A serializer at about `0x10374128` to `0x1037416c` copies a run of
source bytes `+0x3e0` to `+0x408` (one byte per 4-byte slot, plus a word at
`+0x3fc`) into a record, so the source structure holds the settings as bytes
in four-byte slots, and the image area is the slot at `+0x408`. Who writes
that slot is not found: no byte store with offset `0x408` writes it, so it is
set through an indexed or generic setter that does not use a fixed offset.
Observed (the code), inferred, confidence medium. Consequences: a data-only
replacement of 1:1 needs no change to the writer, because the menu already
stores the value 4 for 1:1 and the snapshot carries it to the tables. The
live-view bars are different: nothing in the display path reads the value
(F-033, F-081), so showing them for value 4 needs new code (a hook), which is
the open question of build-gate condition 1. Method: owner-run read-only
decode; instructions and addresses only, no firmware bytes recorded.

F-088. Where the screen layers get their clip flag and bounds, from an
owner-run decode of `0x10452d86` to `0x10452f34` on 2026-10-16. The routine
builds the layer objects at startup in four passes. Pass 1 copies a `0x60`-byte
block from `0x1073db78`, then calls `0x104b5f2a` for each of three layer ids
listed at `0x1073d888`. Pass 2 copies a `0x198`-byte template from
`0x1073dbe4` (the table at `0x1073db78` plus `0x6c`) into a local buffer and
calls the initializer `0x104b5fd4` (F-050) for each of 3 by 3 combinations
with mode 1. Between calls it changes only three fields of the local buffer:
a word at config `+0x20` from a three-word table at `0x1073dbd8`, a flag at
config `+0x24`, and a byte at config `+0x194`; the rest is the template.
Passes 3 and 4 do the same with a second template at `0x1073dd88` (mode 2),
and a third pass (mode 3, `0x104b699e`) and a fourth (mode 4, `0x104b6a30`,
template `0x1073df20`) follow. The clip flag and the bounds that the
initializer copies into each layer object (config `+8` and `+0xc`, F-050) are
therefore fields of the stored template, which sits in the main image
(address below `0x11f81c94`), not in the copied-to-RAM data. Observed (the
code and the literals). Inferred, confidence medium: (a) changing the clip
flag and bounds in the template would make every layer built this way carry
the same mask, always on and for all three layer ids, which would include the
menu layers (so menus would be clipped, as in F-044), and nothing in this
routine reads the image-area value; (b) tying the mask to the XPan choice
needs new code, for example a few instructions that run when live view is
entered and set the flag from the stored area byte. The routine runs at
startup, not when the area changes. Not read: the template contents
themselves, the callers of this routine, and the live-view entry sequence.
Method: owner-run read-only decode; instructions and numbers only, no
firmware bytes recorded.

F-089. Candidate trigger points for the bars, from an owner-run decode on
2026-10-16 of the first `0x90` bytes of the live-view mode-enter routine
`0x102f2990` and of `0x102355ee`. (1) `0x102f2990` takes one argument (a mode
number, compared with 1 and `0xc`), stores a byte 9 on its stack, reads a
global flag, calls `0x10484e20` with 0, reads the property `0x1a0e` through
`0x10465984` (and calls `0x1044f238` when it is 6, `0xe` or `0xf`), makes two
calls to `0x10465b0e` and `0x104555f2`, and then loads the live-view mode
object at `0xc1821d44` and calls `0x104b9116` with it and 0, followed by
`0x1046283c`, `0x10462894` with `0x10000`, `0x10453cc6` and `0x103685dc`. It
has no direct callers, so it is reached through a pointer table. (2)
`0x102355ee` stores its second argument at `[object + 0x30]`, then calls the
shared routine `0x10199e04` with `object + 0x20` and 1 as a tail call; the code
after it is a run of small virtual-call thunks (they load a function pointer
from offsets `0x44` to `0x70` of the object and jump to it), so the object is
an interface with methods, and `0x102355ee` is a generic "set state and
signal" step. It has no direct callers either, and earlier simulator tests
called it with both the menu object (`0xc182e688`) and the live-view object
(`0xc1821d44`). Observed. Inferred, confidence low to medium: the place just
after the activation of the live-view object in `0x102f2990` is a natural spot
to apply or clear the mask for "live view starts", and `0x102355ee` (when its
object is the live-view object) is a candidate for "return from a menu";
"the area changes" has no candidate yet. Not read: the rest of `0x102f2990`
and what `0x104b9116` does. Method: owner-run read-only decode; instructions
and numbers only, no firmware bytes recorded.

F-090. What the live-view start routine does at its end, and what
`0x104b9116` is, from an owner-run decode on 2026-10-16. (1) `0x104b9116` is
not an activation call. It is a short setter: it stores its second argument
at `[object + 0x74]` (the selector byte seen in earlier simulator tests for
the live-view object `0xc1821d44` and the menu object `0xc182e688`), and when
that argument is 0 it first clears two words at `+0x94` and `+0x98`. The live
view start routine `0x102f2990` calls it with the live-view object and 0. (2)
The next routine, `0x104b912c`, is a dispatcher: it reads the selector, loads
a function pointer from `[object + 0x78 + 4 * selector]` and, if it is not
zero, jumps to it with the event arguments. So each screen object has a
table of handlers indexed by its selector. (3) After setting the selector,
the start routine calls `0x1046283c` and `0x10462894`, then (after a mode
check on the values 7, 8 and `0xc`) calls `0x102f8340` with the address of its
mode byte, `0x1035871e`, `0x10356fb0` with 4 or 3, `0x1044e49c` and
`0x1035764e` with 3, and returns. (4) The call to the snapshot routine at
`0x1030f9ce` is in the same module as the area-choice builder (F-072). The
code just before it copies a byte from `[0xc1828be4 + 0xc]` (the count of the
choice list the builder produced) into `[r4 + 0x20]`, checks two conditions,
then calls `0x10366bd0` with 0, `0x103683be`, the snapshot routine
`0x10367260` and `0x1036994a`. This reads as "after the choice list is built,
refresh the snapshot", which is the menu being shown, not necessarily the
choice being picked. Observed. Inferred, confidence low to medium: (a) a
clean way to run new code when live view starts is an entry in the handler
table at `object + 0x78` of the live-view object, and the table is data; (b)
"the area changes" is still not located. Not read: the contents of the handler
tables, `0x102f8340` and `0x10356fb0`. Method: owner-run read-only decode;
instructions and numbers only, no firmware bytes recorded.

F-091. The source byte is also a copy, and the pick stubs only post messages.
(1) Simulator check on 2026-10-16 (assisted startup, one run, guest memory
only, restored): the source byte at `0xc2018a2c + 0x408` (F-087) was set to
4. Within 0.2 simulated seconds it read 0 again, and the mirror
(`0xc2016a68 + 0x15b`) and the snapshot byte (`0xc2016a68 + 0x2cc`) stayed 0
at 0.2, 0.5, 1.0 and 2.0 seconds. So the source is rewritten from something
deeper, and the refresh that fills the mirror did not pick up a changed
source. Writing bytes into these structures therefore cannot imitate "the
area changed"; the real value lives behind the settings store and must be
changed through its own path. Observed runtime, medium confidence (one run).
(2) Owner-run decode on 2026-10-16: the shared routine `0x1030cc68` takes an
item id, allocates a message of size `0x100` (through `0x10454210`, with a
context from `0x10324244`), fills fields (including the value `0x2ed`), posts
it with `0x104546c6` and tail-calls `0x1030bc9c`. Three stubs near the
area-choice builder (`0x1030f78c`, `0x1030f82e`, `0x1030f9dc`) look an item
id up in a list by index, call it, and set the byte at `0xc1828be4` to 1; a
fourth stub at `0x1030ccce` sets it to 2. The routine has 24 direct callers
(`0x1030ccaa`, `0x1030ccd8`, `0x1030ce88`, `0x1030dc76` and others). These
stubs refresh the on-screen list, not the stored setting. Observed (the code);
inferred, confidence low to medium (the reading as a view update). Result for
the design: the "area changes" moment is still not located, and it cannot be
tested by writing memory; it can be tested by driving the simulated menu.
Not yet tried: whether the simulator's menu branch can be driven to pick an
image area. Repro of (1): confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/claude-sourcefollow-private.py" --output "$WORK/private-inputs/claude-sourcefollow-NN"`
with a fresh output directory; the script stays under WORK and is not
committed. No firmware changed.

F-092. Driving the simulated menu to pick "1:1" in "Choose image area" hangs,
even with the thread-aware call helper. On 2026-10-16, a session navigated
from the stock menu to Photo Shooting Menu > Choose image area (confirmed by
screenshots matching the real menu text and layout: DX framed as current,
1:1 highlighted) and pressed the menu OK key (`0x27e` through
`0x103ce96e`). The call did not complete even with a timeout and retried
stops (`timed_out: true, ignored_stops: 1`), the same symptom the
thread-aware helper was built to work around (see `guest_call_safe.py`), but
it did not resolve this one. The simulator process exited afterward; no
process was left running, and the firmware file hash was confirmed unchanged.
Observed runtime. Inferred, confidence medium: this specific key press,
confirming a 1:1 or 16:9 pick, triggers a path the simulator cannot step
through cleanly, separate from the general call-hang issue already
documented. Consequence for the design: "the area changes" cannot currently
be tested by driving the simulated menu either, the same limit noted for
direct memory writes (F-091). Not tried: picking 16:9 instead, or pressing OK
with a different method (for example sending the key without waiting for
completion). Repro: confirmed WORK, run
`PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/claude-menu-session-private.py" --output "$WORK/private-inputs/claude-menu-session-NN"`
with a fresh output directory and drive it with a second small script that
appends to its `cmd.txt`; scripts stay under WORK and are not committed. No
firmware changed.

F-093. The picked image area can be driven in the simulator, and it is stored
somewhere other than the bytes of F-081 to F-087. Simulator runs on
2026-10-16 (assisted startup, guest input only; route: back, up five times, OK
to enter the list, down three times to "Choose image area", OK, down, OK;
screens checked by eye against the real menu). (1) The OK on the 1:1 row
returned in 6 of 13 attempts and hung in the other 7 (it also hung in F-092);
the same OK on the 16:9 row returned in its one attempt. The hang is timing
dependent (an added 5-second pause did not remove it); it needs more work, so
the pick should be retried until it returns. (2) When the pick returns, the
menu shows the 1:1 icon next to "Choose image area", and re-opening the
screen shows 1:1 as the current choice, so the choice is really stored. (3) The
three bytes of F-081 to F-087 (`0xc2016bc3`, `0xc2018a2c + 0x408`,
`0xc2016a68 + 0x2cc`) stayed 0 for 6 seconds after a returned 1:1 pick, so they
do not hold the image area; the chain built on them (F-083, F-085, F-086,
F-087) is not supported and must be redone. (4) A comparison of 16 MB of guest
memory (`0xc1800000` to `0xc2800000`) before and after a returned pick, with an idle control, found about 3,200 changed bytes, mostly screen
drawing. Among them one byte, `0xc1811d90`, went from 0 to 1 for the 1:1 pick
and from 0 to 2 for the 16:9 pick (two runs), stayed at 1 after leaving the
screen, going back and re-opening it, and read 0 before the pick. It matches the
picker's row order (DX 0, 1:1 1, 16:9 2). Observed runtime, medium confidence;
the setting could also live outside the range read. Inferred, low to medium: `0xc1811d90` is the stored
image-area index or a close copy of it. Not yet done: finding which code reads
and writes that byte, and what the values 4 and 2 of F-074 really are.
Repros: confirmed WORK, scripts `claude-pickdiff4-private.py` and
`claude-pickkeep-private.py` with `--downs 1` (1:1) or `--downs 2` (16:9) and a
fresh `--output` folder under `private-inputs`; they stay under WORK and are
not committed. No firmware changed.

F-094. Static search for code that uses the candidate area byte of F-093
(`0xc1811d90`), from owner-run scans on 2026-10-16. Fifteen words in the image
hold an address in `0xc1811d40` to `0xc1811de0` (five distinct values:
`0xc1811d40`, `0xc1811d58`, `0xc1811d60`, `0xc1811d74` and, most often,
`0xc1811dbc`), loaded by 55 pieces of code, all in one module from `0x10084000`
to about `0x1008d4ff`. For the four bases below the byte (`0xc1811d40`,
`0xc1811d58`, `0xc1811d60`, `0xc1811d74`), 22 loaders were checked: none is
followed within `0x70` bytes by an access at the exact offset that reaches
`0xc1811d90` (`+0x50`, `+0x38`, `+0x30` and `+0x1c`). Negative result,
confidence medium (the scan sees only direct accesses within a short window).
Inferred, low: the byte is reached through an index into an array (the whole
`0xc1811d40` to `0xc1811dbc` area is a set of small state arrays of one
subsystem) or through a pointer, not by a fixed offset from one of these bases.
The code that reads and writes the byte therefore has not been found, and a
hook does not need it if it can read the byte itself (0 for DX, 1 for 1:1, 2 for
16:9). Method: owner-run read-only scans; addresses only, no firmware bytes
recorded.

F-095. Of the seven callers of the crop-window builder `0x101d5b36` (F-057),
the other six (besides `0x1015382a`, already read) were decoded on
2026-10-16. Five build small on-stack or per-item context structs from an
object at `+0x3a4` and immediately feed a property query or UI item builder
(`0x10194cca` with id `0x2cf`, `0x1015336c`/`0x10364232`/`0x10364250`
clusters, or loop bodies that copy fields into per-item records at growing
offsets) -- the same shape as display/menu info builders, not save paths.
The sixth, at `0x101d5de8` (enclosing function entry near `0x101d5a14`), is
different: right after the crop call it does two large block copies through
`0x10199bdc` (96 bytes from `source+0x4f0` to `dest+0x260`, then 80 bytes
from `source+0x550` to `dest+0x2c0`), then a run of individual byte/word
copies from the source at `+0x553`, `+0x554`, `+0x5a7`, `+0x5a8` and more
(cut off) into the destination at `+0x2ec`, `+0x2ed`, `+0x310` and beyond,
with a further pointer at `source + 0x1400` referenced soon after. Observed
static decode on 2026-10-16. Inferred, confidence low to medium: this is
assembling one composite record (destination, growing past `0x310` bytes)
out of several source sub-blocks, which is a more promising shape for a
capture/save descriptor than the other five callers. Not yet read: the rest
of this copy sequence, the destination object's identity, and what consumes
the assembled record afterward (a save call, a queue post, or another display
use). Method: owner-run read-only decode, SHA-256 checked first; addresses
and offsets only, no firmware bytes recorded.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.
