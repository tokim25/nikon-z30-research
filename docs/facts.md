# Facts ledger

Known corrections: see [corrections.md](corrections.md).

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

F-096. Corrects and extends F-095. The crop-builder caller `0x101d5de8`
sits inside a function whose real entry is `0x101d5c54` (push of 9
registers, `sub sp, #0x1c`), not the `0x101d5a14` landmark F-095 guessed,
which was an unrelated record-matching loop. An owner-run decode on
2026-10-16 of `0x101d5c54` through past the crop call confirms and extends
F-095's reading. (1) Before the crop call, the function calls
`0x101dc204` twice (passing a mode value 2 or 3 and a pointer to two loaded
words, derived from a settings byte at `source+0x2000+0xa52`). That
function is not a geometry lookup: for a first argument of 1, 2, 3 or 6 it
divides the constant 24 by that argument (`sdiv`, with rounding), scaled by
a second value, which reads as bits-per-component or similar size math
dividing a 24-bit depth across 1 to 6 components, not another crop-window
call. (2) After the crop call and the two previously found block copies
(96 bytes from `source+0x4f0`, 80 bytes from `source+0x550`), individual
field copies continue well past the `+0x310` offset already found: more
bytes from `source+0x5a0` through `+0x5a8`, a doubleword from
`source+0x1400+0x1c`, and a conditional word at destination `+0x320`, ending
with destination `+= 0x328` and a further block load (`ldm` of four words
from `source+0x5d0`) before three mode branches
(`0x101d601c`/`0x101d5ffe`/`0x101d602e`) selected by settings bytes from
the same `source+0x2000` block (`+0xaa5`, `+0xa71`, `+0xa8e`, `+0xa90`).
Observed. Inferred, confidence medium: the destination record (well over
0x328 bytes, combining geometry, bit-depth/size math and copied device
config) is a stronger candidate for a capture or save-side descriptor than
any of the other six crop-builder callers (F-095), none of which build
anything this large or include size-in-bytes arithmetic. Not yet found: who
calls `0x101d5c54`, what identifies its destination record, and what reads
the finished record afterward (continuing into the three mode branches is
the immediate next step). Method: owner-run read-only decode, SHA-256
checked first; addresses, offsets and constants only, no firmware bytes
recorded.

F-097. The record-assembly function `0x101d5c54` (F-096) has exactly four
direct callers, all in one tight code region (`0x10155bf4`, `0x101560d0`,
`0x101564f4`, `0x1015b062`, spanning roughly `0x10155b00` to `0x1015b100`),
from an owner-run decode on 2026-10-16. Three of the four (`0x101564f4`,
`0x1015b062`, and `0x10155bf4` loosely) share a shape: a capability-style
check through `0x10163546`, keyed on a per-area id byte at source `+0x4ea`
(the same source block F-096 copies id bytes `+0x4e8` to `+0x4eb` from into
the built record); a prepare call `0x1015350e`; the record-builder call;
then, after it returns, a doubleword is read from
`[some_pointer + 0x2b00 + 0x4c]` and copied into the finished record at
offsets `+0x124`/`+0x128`. Observed. Inferred, confidence low, stated as two
competing explanations rather than one, because both fit equally well so
far: (a) this assembles and submits a capture/save request, where the
finished record eventually reaches a storage write; or (b) this is a
"remaining shots at this quality" style estimator, which also needs crop
geometry, bit-depth math (F-096) and a per-mode call shape, but only feeds a
UI counter and never touches storage. Nothing read so far distinguishes
these. Not yet done: finding what calls each of these four outer sites (one
level further out), to see whether that context is nearer a storage/write
call or a shots-remaining/UI display. Method: owner-run read-only decode,
SHA-256 checked first; addresses and offsets only, no firmware bytes
recorded.

F-098. One hop further from F-097. Two of the three outer enclosing
functions (`0x101568ca`, `0x1015be26`) have no direct `bl` callers anywhere
in the image, so they are reached by pointer/table, not a straight call
chain; the third (`0x1015a93c`) has two direct callers, `0x1015c208` and
`0x1015c29c`, close together. Observed static scan on 2026-10-16. Inferred,
confidence low: pointer dispatch is the pattern this project has
consistently found for menu/event handler tables (F-072, F-090), which
leans slightly toward the shots-remaining/UI-display explanation of F-097
over a straight-line capture pipeline, but this is not conclusive either
way; capture code could equally be dispatched by table. Not yet done:
finding the pointer tables that reference `0x101568ca`/`0x1015be26`, and
reading the two callers of `0x1015a93c`. Method: owner-run read-only scan,
SHA-256 checked first; addresses only, no firmware bytes recorded.

F-099. Three live simulator checks on 2026-10-16 (assisted startup, breakpoint
observation via the thread-aware helper's `observe` support, nothing
modified, firmware hash and simulator tree confirmed unchanged after each)
found zero hits on the record builder `0x101d5c54` or its four known callers
(F-096, F-097) while navigating: "Choose image area", "Image quality",
"Image size", and a broad sweep across all top-level menu tabs (Photo, Video,
Retouch, Setup) several items deep each. The simulator's key set has no
shutter/capture button and no "i" quick-menu or info-display button (only
up/down/left/right/ok/back), so a true capture trigger cannot be attempted
through this interface at all, and neither can some on-camera info overlays.
Observed runtime (negative result), medium confidence: ordinary menu
browsing does not reach this code, which is modest evidence against the
simplest form of the "shots remaining" hypothesis from F-097 (a counter
shown directly on these menu screens), but it does not rule in the
capture-path hypothesis either, since the one trigger that would prove it
(an actual capture or info-overlay keypress) is not reachable here. The two
hypotheses in F-097 remain open. Repro: confirmed WORK, scripts
`claude-recordbuilder-observe2-private.py` and
`claude-recordbuilder-sweep-private.py` with a fresh `--output`; they stay
under WORK and are not committed. Separately, an owner-run string search
found "shots"/"remaining" UI text in the known menu-text blob (around
`0x10e8....`, F-053's region) and one `.NEF` ASCII literal at `0x11c9a614`,
neither tied to these specific functions by address proximity. Next: either
accept this ambiguity and move to a different saved-crop angle, or call the
builder's outer callers directly with synthetic register state (more
invasive, less certain) to force a hit and inspect the record.

F-100. The simulator cannot be used to directly observe real SD card
activity for a save. A fresh, blank, FAT32-formatted synthetic disk image
(created locally, zero real data, attached with `snapshot=on` so writes go
to QEMU's own temporary overlay and the image itself is never modified) was
attached as the SD card with SD trace events enabled, on 2026-10-16. The SD
host controller reports a card insert and reads its capability registers
once at boot, plus two register writes (a reset sequence) -- and nothing
else, even after 20 seconds idle or after navigating menus. Setup Menu's
"Format memory card" item is shown greyed out (unselectable), meaning the
firmware itself does not consider a usable card present, despite the
controller-level insert event. No `sdcard_read_block` trace event fired at
any point. Observed runtime, high confidence for what was tried. This
closes off the SD-trace angle at this level of effort: the simulator's own
README already said photo/movie recording is outside its supported scope
(`xpan-simulator-raw-limits.md`), and this confirms it structurally -- the
firmware's card-presence check (not modeled here, possibly a detect pin or a
deeper validation this synthetic image fails) gates it off before any
command traffic can occur. Not yet tried: finding and tracing that
card-presence check itself (separate research, not a simulator experiment).
Repro: confirmed WORK, script `claude-sdcard-format-private.py`
(single-shot) or `claude-menu-session-sd-private.py` (interactive, paired
with a `cmd.txt`-polling helper) with a fresh `--output`; the synthetic image
is `private-inputs/claude-synthetic-sdcard.img`, created locally via
`newfs_msdos`, never committed. No firmware changed.

F-101. A private QEMU loader overlay proved a native live-view mask hook in
the assisted simulator on 2026-10-16. Read-only static review found four
zero-filled candidate instruction spans: `0x1002d78c..0x1002d7bf` (52
bytes), `0x1002d80c..0x1002d83f` (52 bytes),
`0x1002d860..0x1002d87f` (32 bytes), and
`0x1027f468..0x1027f47f` (24 bytes). The surrounding functions return
before each span, and no aligned literal or table reference into a span was
found. Correct-mode review rejected apparent mixed ARM/Thumb branch hits as
decode artifacts. The exact image-area writer is the function at
`0x1008d38c`; its store at `0x1008d3fc` updates the record containing the
choice byte at `0xc1811d90` (DX 0, 1:1 1, 16:9 2). Observed, high confidence
in the simulator: synthetic new code loaded before CPU start, without
debugger writes to code or mask state, made the mask follow the choice at
the writer, live-view-start and generic screen-activation paths. A real 1:1
menu pick kept the mask off over the menu; an audited live-view activation
enabled full-width black rows 0..106 and 373..479. Ten menu/live-view signal
cycles alternated correctly. Direct stock callback tests produced 1:1, DX,
1:1, 16:9 with mask states on, off, on, off; a 16:9 menu control stayed off.
The firmware hash and QEMU tree remained unchanged. Inferred, confidence
medium: these spans are viable insertion space beyond the simulator; hidden
hardware references and execution behavior are not proved. Limits: natural
menu exit and the natural startup caller were not exercised, the simulator
has no `i` button, and the immediate-update test used the exact stock row
callbacks. The later menu-notification trigger hypothesis failed, and QEMU
write watchpoints failed a known-store self-test. Repro: confirmed WORK,
private scripts `codex-linker-gaps-private.py`,
`codex-choice-module-trace-private.py`, `codex-xpan-hook-build-private.py`
and `codex-xpan-hook-run-private.py`, always with fresh `codex-` output;
detailed commands and constraints are in
[native-xpan-liveview-hook.md](native-xpan-liveview-hook.md). No overlay,
firmware bytes, raw logs or patched image enter Git.

Follow-up on the same F-101 branch tested final-menu closure. The exposed
Back event stopped at one stack entry. Stock internal events `0x24e` and
`0x250` removed the last entry, but both requested mode `0x10000`, not the
live-view target `0x100000`; the physical controls behind those events remain
unknown. An unguarded close hook turned the mask on in that non-live-view
state and was rejected. The final private overlay routes its close, writer
and live-view-ready paths through a guard that requires an empty screen stack
and live-view selector byte 1 at `0xc1821db8`. It also moves the live-view
transition hook to the exact selector-1 call at `0x102f5810` inside
`0x102f57e2`. Observed, high confidence in the
assisted simulator: the guarded build passed the direct 1:1/DX/1:1/16:9
sequence and ten menu/live-view signal cycles, and stayed off after the
non-live-view `0x250` close. Inferred, medium confidence: the guarded close
and selector-1 sites cover a real return to live view without enabling the
mask in playback or another base screen. A natural caller of `0x102f57e2`
was not observed because the assisted fixture's live-view worker is dormant.
A diagnostic stock type-2 dispatch did reach `0x102f57e2`, `0x102f5810`,
the new wrapper, guard and mask helper in order, then returned with selector
1, stack count zero and the 1:1 mask on. This observes the full internal
route, high confidence, but not its natural worker trigger.
Repro: confirmed WORK, private scripts
`codex-xpan-guarded-hook-build-private.py`,
`codex-xpan-hook-run-private.py`,
`codex-xpan-menu-event-return-private.py`, and
`codex-xpan-live-ready-probe-private.py`, always with fresh `codex-` output.

F-102. Follows up F-100's open question (what gates "Format memory card")
with a static trace of the card-detect function itself. The function at
`0x104157b8` (the comment-cited address `0x104157dc` is a test inside it,
not its entry) reads the SDHCI Present State register (offset `0x24`) of
controller 0 only (MMIO base `0x2a100000`) and tests bit 16 ("Card
Inserted") via `lsls r0,r0,#0xf; bmi` -- a plain bit test against nothing
else. On a miss it ORs failure bits into a global status struct at
`0xc18015e8` and returns; on a hit it probes four more helpers, re-checks
Present State bit 12, and writes pass bits into the same struct before
returning a boolean. Three direct callers exist: a self-retry inside the
function's own trailer (`0x104159a4`), a periodic re-poll branch inside a
generic notification dispatcher (`0x102c3a1c`, reached only for a specific
event code), and a controller-0 bring-up routine at `0x102aa414` that
retries up to twice on failure and, on success, dispatches on a separate
global byte at `0xc18015ea` (values 2 vs 3) into a call to `0x10417890`.
Observed static decode on 2026-10-16. The exact link from that dispatch (or
from the `0xc18015e8` struct) to the Setup-menu enable/grey-out check was
not found -- this is the open gap.

Separately, the function at `0x104164ba` is a generic
"issue command, wait for completion" primitive (not detect-specific): it
branches on capability bit 25 of the same `0xc18015e8` struct (offset
`+0x44`) and, on the non-fast path, calls two OS primitives
(`0x10199e0a`, `0x10199e4e`) against a fixed event object at
`0xc1d2da74`. That exact object is the one registered together with
controller 0's IRQ (`0x1019dfd6(0xe6, ...)` at `0x102aa2d4`) -- confirming
the nikon-z30-display.c comment's IRQ claim (0xe6 for controller 0, 0xe9 for
controller 1, the latter against a different event object `0xc1d2df30` with
no card-detect caller found into controller 1). `0x104164ba` has 8 call
sites clustered at `0x1041678e`, `0x10416818`, `0x104169e0`, `0x10416a02`,
`0x10417040`, `0x104170c4`, `0x104172ee` and `0x10417310` (likely individual
SD command handlers), none individually decoded yet. Observed static
decode. Inferred, medium confidence: because `0x104164ba` always waits on
controller 0's specific hardware event rather than a generic/parameterized
one, and the project's QEMU model comment already states "polling commands
can work there but DMA completion never reaches the event object awaited by
0x104164ba", a stall here during SD bring-up (CMD0/ACMD41/CMD2/CMD3-class
initialization, not bulk-data DMA specifically) is a stronger candidate for
blocking "Format memory card" than card-detect itself, which is a simple,
satisfiable bit test. Not proven end-to-end: no single call site among the 8
was confirmed to sit inside the same bring-up sequence that `0x102aa414`
drives.

Also checked and ruled unlikely as the cause: the ADMA2/vendor-revision
check at `0x10415e12`..`0x10415e26` (inside a mode-select function at
`0x10415d80` that tries transfer modes 1/2/3 in turn). Mode 3 requires a
capability-register byte at `[r4+0xfc]` bits 24-31 to equal 1; QEMU's
generic SDHCI model exposes a different vendor byte there. On mismatch the
function returns 0 ("mode unavailable") via a plain `pop {pc}` at
`0x10415dae` -- no abort, trap, or storage-disabling side effect -- leaving
mode 1 (not gated by this byte at all) still selectable. This matches the
QEMU source comment's own framing ("a driver-compatible revision, not a
silicon ID"). Observed static decode, high confidence this path does not
block the card entirely.

Not yet done: tracing `0x10417890` and the `0xc18015ea` dispatch forward
into the menu/UI layer (the direct lead to the enable/grey-out check), and
decoding the 8 `0x104164ba` callers individually to identify which SD
commands they correspond to and whether one sits in the same bring-up path
as `0x102aa414`. Method: read-only static decode (capstone, Thumb),
SHA-256 checked first; addresses, offsets and register/field names only, no
firmware bytes recorded.

F-103. Continues F-097/F-098's ambiguity between a capture/save descriptor
and a shots-remaining/UI estimator, and corrects F-098's premise. The two
addresses F-098 called "reached only by pointer/table" -- `0x101568ca` and
`0x1015be26` -- are internal basic-block labels, not function entries; their
real enclosing functions (found by walking back to the nearest `push`
prologue) are `0x10156714` and `0x1015bc3e`. Checked against the real
entries: `0x1015bc3e` has 3 direct `bl` callers (`0x1015bd2c`, `0x1015c162`,
`0x1015da18`) and one tail `b.w` caller (`0x1015d7a6`), scattered across
roughly `0x10153000`-`0x1015da00` -- ordinary direct calls, not table
dispatch, weakening F-098's lean. Only `0x10156714` still has zero `bl`,
tail-`b.w`, or raw-pointer-word references anywhere in a full 33.9MB image
scan (both plain and Thumb-bit-set variants checked); no dispatch table was
found referencing it either, so this one remains genuinely unresolved
(unreached by any literal mechanism a flat scan can see, or dead code in
this build -- not determined). Observed static decode on 2026-10-16.

`0x1015a93c` (F-098's third function) decodes as a large multi-way
dispatcher: it compares an incoming id against a long run of literal-pool
constants shaped like category-plus-subid pairs (`0x0419xxxx`, `0x0418xxxx`,
`0x0417xxxx`), then falls into Thumb jump tables (`tbb [pc,r0]`) for finer
dispatch -- the same property/event-ID dispatch shape this project has
already tied to menu/property tables (F-072, F-090), not a save/capture
consumer. It is referenced with the Thumb bit set (`0x1015a93d`) from 17
separate literal-pool sites spread across roughly `0x10153158`-`0x10162ff4`
(~65KB of code, no regular stride -- each its own small literal near its own
use site), i.e. handed around as a callback/handler argument from many call
sites, not read out of one fixed table. Its two F-098 callers, `0x1015c208`
and `0x1015c29c`, sit as ordinary straight-line code inside one enclosing
function `0x1015beb0` (found via `push.w` prologue): each builds a small
stack struct, calls `0x1015a93c` (fires the dispatch), then calls
`0x1015bd18` with a mode argument (0 or 1). `0x1015bd18` is a small
mode-dispatch wrapper (modes 0/1/2/3): it sets a flag bit at `[base+0x68]`,
runs a check through `0x101883b2`, and in modes 2/3 only, loads the
`0x1015a93d` callback and feeds it into `0x101e729e` then `0x101efb9e`; for
other modes it is also what calls `0x1015bc3e` (at `0x1015bd2c`). One hop
further out, `0x1015beb0` has exactly one direct `bl` caller,
`0x1015c13e`, but the function boundary there is ambiguous (looks like
shared/merged tail code) and was not fully resolved. Observed static decode.

Net picture: F-096/097's crop/record-builder chain, F-098's two targets, and
`0x1015a93c`'s property dispatch all sit inside one tight function cluster
(`0x1015beb0`-`0x1015c450`), reading as one "apply an image-area/quality/size
setting" handler -- build the descriptor, fire a property/event notification,
then apply/persist flags. Inferred, confidence low to medium: this leans
toward hypothesis (b) from F-097 (a settings/property-change handler feeding
UI and internal state) over (a) (a capture/save request descriptor),
because `0x1015a93c`'s dispatcher shape and its reuse as a shared callback
match this project's established property/menu-table pattern rather than a
single fixed capture-pipeline call site. Not conclusive: no unambiguous
storage/SD-write primitive or UI-text/counter-formatting call was identified
among the functions touched here (`0x10163e5c`, `0x1006e4b4`/`0x1006e494`/
`0x1006e48c`, `0x101883b2`, `0x10199c40`, `0x101e729e`, `0x101efb9e`,
`0x10156b62`, `0x1007631e`, `0x100763c2` -- all still undecoded). Not yet
done: decoding `0x1015bd18`'s mode 2/3 branches and `0x101e729e`/
`0x101efb9e` to confirm the callback theory, sampling more of the 17
`0x1015a93d` literal sites, and resolving `0x1015c13e`'s real function
boundary. Method: read-only static decode (capstone, Thumb), full-image
literal/branch scans, SHA-256 checked first; addresses, offsets and
constants only, no firmware bytes recorded.

F-104. Decodes the 8 call sites into `0x104164ba` left open by F-102. They
collapse to exactly 4 enclosing functions, each containing 2 of the 8 (the
backward function-entry scan had too short a window for 4 of the 8; the
true entries are far above them in the same function). Each enclosing
function loads a 16-bit "command word" into a register early on:
`0x104168aa` loads `0x113a`, `0x104165b8` loads `0x123a`, `0x104171ce` loads
`0x183a`, `0x10416e6c` loads `0x193a`. Read as `(CMD_INDEX << 8) | flags`,
the high bytes `0x11/0x12/0x18/0x19` are exactly SD command indices 17, 18,
24, 25 -- CMD17 READ_SINGLE_BLOCK, CMD18 READ_MULTIPLE_BLOCK, CMD24
WRITE_BLOCK, CMD25 WRITE_MULTIPLE_BLOCK -- and the shared low byte `0x3a`
decodes against the standard SDHCI Command-register bit layout (offset
0x0E, upper half of the 32-bit Argument2/Transfer-Mode-and-Command word) as
bit5 Data Present Select=1, bit4 Command Index Check Enable=1, bit3 Command
CRC Check Enable=1, bits1-0 Response Type Select=2 (48-bit/R1-class
response) -- a completely standard data-transfer command encoding, not an
arbitrary constant. Observed static decode on 2026-10-16, high confidence:
these four functions are the firmware's real SD single/multi block
read/write command-issue routines.

Each function's command word is stored into fields of the per-controller
state struct (byte at `+7`, word at `+0x40`, a stack slot) before being
passed to `0x1041372c` (apparent "submit command" call, tested for
success/failure immediately after); on success the function proceeds
through a pair of `0x104164ba` waits, each preceded by a short, near-
identical preamble (`bl 0x104131b2` and either `0x102c2eee`/`0x102c2cc8` or
`0x1041612a`/`0x104161dc`, varying slightly per function) before loading the
controller struct pointer into r0/r1/r2 and calling `0x104164ba`. This
shape -- two sequential completion waits per command, the first gated by a
`cbz` that branches to an error/retry path on failure, the second feeding
a final success/failure decision -- reads as the standard SDHCI two-stage
wait (a per-transfer "buffer ready" signal, then "transfer complete"), not
two unrelated waits. Neither `0x1041372c`, `0x104131b2`,
`0x102c2eee`/`0x102c2cc8`, nor `0x1041612a`/`0x104161dc` were decoded in
this pass. Observed static decode, medium confidence for the two-stage-wait
reading (consistent with the shape, not confirmed by decoding the waited-on
interrupt bits themselves).

This strengthens F-102's inference: if F-102's "DMA completion never
reaches the event object awaited by 0x104164ba" holds for controller 0 under
QEMU's generic SDHCI model, then every one of CMD17/18/24/25 issued against
controller 0 would stall at the first of these two waits, well past
card-detect, which would independently explain both F-100's zero
`sdcard_read_block` events and the "Format memory card" grey-out -- the
firmware's SD stack would never progress far enough to consider the card
usable, regardless of what synthetic image is attached. Still not proven
end-to-end: whether the firmware's actual bring-up sequence reaches
CMD17/18/24/25 at all before giving up (it may fail earlier, e.g. during
CMD0/ACMD41/CMD2/CMD3-class enumeration, which are not among these 4
functions) was not checked, and the menu-enable/grey-out check itself
(F-102's still-missing link) was not pursued further here. Method:
read-only static decode (capstone, Thumb), SHA-256 checked first; addresses,
offsets, register fields and standard SDHCI register semantics only, no
firmware bytes recorded.

F-105. Directly attacks F-097's capture-descriptor vs. shots-remaining-
estimator ambiguity by checking reachability from the record builder's
four direct callers (`0x10155bf4`, `0x101560d0`, `0x101564f4`,
`0x1015b062`) to F-104's real SD write commands (CMD24/CMD25 at
`0x104171ce`/`0x10416e6c`) or the shared command-submit primitive
(`0x1041372c`). Method: an automated breadth-first walk of the direct
`bl`/`blx` call graph starting at these four, decoding each reached
function from its entry to the next function's prologue (a `push`/`push.w`
with `lr`, used as the end-of-function boundary -- validated against
F-102's manually-decoded card-detect function, which the naive
"stop at the first return" version of this method had under-counted by
missing a later exit path; the corrected version recovers all of
card-detect's known calls). Starting from the four callers, the walk
reaches exactly 867 distinct functions and terminates (the work queue
empties, not a node cap) -- none of them is in the SD command block
(`0x10413000`-`0x10418000`) or the submit primitive. Observed static
BFS on 2026-10-16, SHA-256 checked first.

This is a real but limited negative result, not a resolution. It rules out
the simplest form of hypothesis (a) -- the four callers, or anything they
call directly or transitively, synchronously writing the finished record to
storage right after building it. It does not rule out a version of (a)
where the record is instead handed off indirectly: written to a queue or
global slot that a separate worker function reads and acts on later,
reached only through a function-pointer table rather than a direct call.
This project has repeatedly found pointer/table dispatch to be the normal
pattern for handler code here (F-072, F-090, F-098's `0x101568ca`/
`0x1015be26`), so this is a real possibility, not a stretch -- it was simply
not checked by this BFS, which only follows literal `bl`/`blx` targets.
Confidence: medium-high against the direct-write form of (a); the
indirect-handoff form of (a), and (b), remain open. Not yet done: scanning
the 867 reached functions (or the four callers themselves) for a store into
a global pointer/queue slot that isn't consumed by anything in this same
reachable set, which would be the signature of a hand-off to an
unreached worker. Method: read-only static decode (capstone, Thumb) and an
automated call-graph BFS, SHA-256 checked first; addresses only, no
firmware bytes recorded.

F-106. Tests F-097's capture-descriptor vs. shots-remaining-estimator
ambiguity directly, on two fronts, continuing from F-105's negative
result. Corrects and extends F-103 along the way.

**Front 1: full decode of `0x1015bd18`'s four modes (corrects F-103).**
F-103 said modes 2/3 feed the `0x1015a93c` callback into `0x101e729e`
then `0x101efb9e`. The actual assignment is the opposite: **modes 0 and 1**
are the ones that build a small stack struct and call `0x101efb9e` with the
`0x1015a93d` callback pointer; mode 2 and mode 3 call `0x101e729e` only
(with a fixed object, never the callback). All four modes converge on a
shared tail that, **only in mode 2**, dereferences a global pointer at a
computed slot address `0xc18a6810 + 0x80 + 0x80 = 0xc18a6890` and, if
non-null, copies 96 bytes from `+0x4f0` and 752 bytes from `+0x2a50` of the
pointed-to object into a fixed destination object at `0xc239d91c`. The
96-byte-from-`+0x4f0` copy is the **same source offset and size** as the
first block copy F-096 found inside the record builder `0x101d5c54`
itself -- real evidence, not proof, that the slot's pointer is or matches
`0x101d5c54`'s output.

**Front 2: decode of `0x101e729e` and `0x101efb9e`.** `0x101e729e` is an
argument-setting stub (not a full function entry) for a shared "post an
event" primitive at `0x101e725a`: allocate a 12-byte `{code, id, ptr}`
record, lock a global struct at `0xc21c0eec`, append to a linked list at
`[0xc21c0eec+0xa4]`, signal, unlock. `0x1015bd18`'s call posts
`{code=6, id=0x04180041, ptr=<fixed object>}` -- a generic notification,
architecturally distant from the SD/storage code block
(`0x10413000`-`0x10418000`, F-102/F-104) and tagged with an id numerically
adjacent to `0x04180042`, one of `0x1015a93c`'s own dispatch-ID constants
(F-103) -- the same `0x0417`-`0x0419` property/event-ID family, not
anything capture-specific. `0x101efb9e` is a thin wrapper
(always returns 1) around `0x1007c094`, which **synchronously calls the
`0x1015a93c` dispatcher directly** -- `callback(id=0x042d0027,
&output_slot)` -- rather than registering it anywhere for later/async use.
That is the shape of a property get/notify call, not a capture-job
submission.

Observed static decode on 2026-10-16 (subagent-assisted). Inferred,
confidence medium, leaning toward hypothesis (b): both mechanisms found in
modes 0/1 and mode 3 are notification/property-dispatch shaped, and the
one queue found (`0xc21c0eec`) is generic and storage-distant. What keeps
this from higher confidence: mode 2's slot-dereference-and-copy (front 1)
is a genuinely new, unexplained data movement whose size/offset match to
F-096's record builder is suggestive but not confirmed, since the slot's
actual producer was not found. A literal-pool word scan for the slot
address `0xc18a6890` (6 hits total) found no site resembling a producer --
the two resolved so far (`0x1016145c`, `0x1015dfb8`) load it only to
immediately subtract `0x80` back to the module's wider base
(`0xc18a6810`, used 52 times across `0x10152000`-`0x1015c600`, an
unrelated-looking convenience pointer) for other fields, not to write a
record pointer there. The true producer may compute the slot via register
arithmetic on the base literal rather than ever loading `0xc18a6890` as its
own literal, which this word-scan cannot find. Several called functions
remain undecoded (`0x1014cc88`, `0x1018916e`, `0x101635b8`, `0x1015bbb0`,
`0x1015ba4c`, `0x10220e14`, `0x10220d8e`, `0x1007631e`, `0x100763c2`,
`0x10156b62`), any of which could still hide a storage hand-off. Not yet
done: finding `0xc18a6890`'s real producer via a register-arithmetic scan
(not a literal match) over the 52 functions that use the wider base.
Method: read-only static decode (capstone, Thumb) and literal-pool word
scans, SHA-256 checked first; addresses, offsets and ids only, no firmware
bytes recorded.

F-107. Resolves the Lane 1 close-handler mode-state sub-question that
stopped a prior session three times (handoff-codex.md's "owner note on
the pattern"), one level past where that session left off. Confirms the
exact close handler: the table slot `0x113033a8` named in the prior
hand-off holds `0x10460c3d` (Thumb-tagged), i.e. the real close handler is
`0x10460c3c`.

Full chain, decoded in order:
- **`0x10460c3c`** (the close handler): calls `0x1045b27e`; if that
  returns 0, selects mode `0x100000` (the live-view target); any nonzero
  return selects `0x10000`.
- **`0x1045b27e`** (the "small helper" the prior hand-off described):
  calls `0x10457db2` and returns 0 if that result is 0, 3, or 4, else 1 --
  exactly matching the prior hand-off's abstract description, now with the
  concrete function identified.
- **`0x10457db2`**: this is where the prior session stopped. It is a
  trivial 3-instruction getter -- `ldr r0, [pc, #0x13c]; ldrb r0, [r0]; bx
  lr` -- that reads one byte from a fixed global address and returns it
  directly; it is not itself the `cmp r0,#1/2/3`-style dispatcher an
  earlier reading assumed (that shape belongs to the next function over,
  `0x10457dbe`, which calls a different function, `0x1045a7f2`, and is
  unrelated to this chain). Resolving its literal pool entry
  (`0x10457ef0`) gives the byte's address: **`0xc181f6fc`**.

A literal-pool word scan for `0xc181f6fc` across the full image found
three references: the getter above (`0x10457ef0`), and two more at
`0x10458310` and `0x104593b0`. Both of the other two are **read**
accessors into small lookup tables anchored near this address, not
writers: the first (`0x104582fa`) indexes a stride-8 table at
`0xc181f6fc + 0x50` with a bounds check at 10 entries and reads a byte at
`+4` of the selected entry; the second (`0x10459366`) indexes a different
stride-8 table (resolved via a second literal, not yet read) with a bounds
check at `0xb3` (179) entries and reads a full word. Neither writes
`0xc181f6fc` itself.

Observed static decode on 2026-10-16, no classifier stop encountered at
any point in this chain (contrast with the prior session's three stops on
this exact sub-question -- the earlier stops were apparently specific to
decoding past `0x10457db2`, which this pass did without incident).
Confidence high for the chain itself (direct instruction-level reads, no
inference). Not yet done: finding what actually **writes**
`0xc181f6fc` -- none of the three literal-pool references found is a
write, so the writer either loads a different literal that resolves to
the same address via arithmetic (the same pattern F-106 ran into with its
unresolved slot producer), or writes it through one of the two
stride-8 tables' sibling entries rather than the plain byte directly. This
is the natural next step for whoever picks this up: a register-arithmetic
scan (not a literal match) for writes landing on `0xc181f6fc`, or fully
mapping the two stride-8 tables to see if a write-side sibling function
exists for either. Method: read-only static decode (capstone, Thumb) and
literal-pool word scans, SHA-256 checked first; addresses and offsets
only, no firmware bytes recorded.

F-108. Closes F-107's open thread: finds the writer of `0xc181f6fc` and
with it the natural trigger for the menu-close-to-live-view transition
that stopped a prior session three times and that F-107 only got one
step closer to.

A register-arithmetic scan (resolving `ldr`-literal + `add`/`sub`
sequences, not a literal-word match, over the `0x10440000`-`0x10470000`
module) found two writers:

- `0x10459140`, inside a larger module-init routine (`0x104590e4`) that
  sets up a 10-entry array and several other fixed objects at startup --
  it unconditionally zeroes the byte as part of general initialization,
  not a per-event trigger.
- **`0x10457dac`**: a plain setter, `ldr r1, [pc, #imm]; strb r0, [r1]; bx
  lr` -- the natural sibling to F-107's getter at `0x10457db2`, sitting
  immediately before it in the same instruction stream. Takes whatever
  value is passed in `r0`.

The setter has **exactly one direct caller** in the whole image:
`0x10459db2`, inside a dispatcher function (`0x10459d80`) that branches on
an incoming event code. The specific branch is taken when the event code
equals **`0x4100012`**: it stores a caller-supplied value (or zero) into a
secondary field, then calls the setter with **`r0 = 4`** -- one of the
three values (0, 3, 4) F-107 already showed route the close handler
(`0x10460c3c`) to the live-view target instead of the generic
menu-close target. Immediately after, the same branch calls `0x1046283c`
and `0x10462894` with no further gating. **These are the same two calls
F-090 already found inside the live-view-start routine `0x102f2990`
itself**, right after it sets the live-view object's selector --
independent corroboration, not just circumstantial, that event
`0x4100012` is the real live-view-entry trigger, not an unrelated code
path that happens to write the same byte.

Observed static decode on 2026-10-16 (register-arithmetic scan plus
direct disassembly), no classifier stop encountered. Confidence high for
the mechanical chain (setter identity, sole caller, the value written,
the two post-call matches to F-090); confidence medium for "this is *the*
natural trigger the menu-close path needs" specifically, since what
*posts* internal event `0x4100012` (a physical button, an internal state
machine, or something else) was not traced -- the simulator's exposed key
set has already been shown (native-xpan-liveview-hook.md's "Limits"
section) not to reach the two internal close events it could drive
(`0x24e`, `0x250`), and `0x4100012` was not among those tested either.

This resolves the mechanism build-gate condition 1 was waiting on for
Lane 1: a safe-to-add hook no longer needs to guess at what sets the
live-view mode-state, since `0x10457dac` is a conventional setter
reachable the same way any other code would call it. Not yet done: find
what posts event `0x4100012` (to confirm it is reachable through the
camera's normal `i`-menu or live-view-entry controls, not only through
this one dispatcher's internal branch), and test the existing guarded
hook (`native-xpan-liveview-hook.md`) against a simulator run that drives
this event directly, if a way to post it is found. Method: read-only
static decode (capstone, Thumb) and a register-arithmetic write scan
(not a literal-word match), SHA-256 checked first; addresses, offsets and
event/mode codes only, no firmware bytes recorded.

F-109. Closes the "what posts event `0x4100012`" thread as a deprioritized
dead end, not a finding to build on. Four independent methods, each
checked across the **full** 33.9MB image (not a bounded window): direct
`bl` calls, tail `b.w` branches, raw pointer-table words (plain and
Thumb-tagged), and Thumb table-branch (`tbb`/`tbh`) jump tables with their
computed targets resolved. All four found zero references to
`0x10459d80`, the dispatcher that receives this event code as its own
parameter (F-108). This mirrors F-103's identical dead end for
`0x10156714` -- consistent with this being either dead code in this
build, or reached through a mechanism these methods cannot see (e.g. an
ARM-mode call, a double-indirection table, or a `tbb`/`tbh` whose own
reachability wasn't itself checked).

This was not pursued further on purpose, matching AGENTS.md's priority
rule, not because of a classifier stop (none occurred) or exhausted
technique space (ARM-mode scanning and a manual search of the UI/input
event-pump module remain untried). The reasoning: this question is about
*simulator reachability* (can the simulator's limited key set be made to
post this event), not about the real firmware, which obviously already
delivers it through ordinary use -- F-090 already shows live view working.
F-108's hook sites (`0x102f5810`, `0x102355c0`, the guard in
native-xpan-liveview-hook.md) sit downstream of this event, not upstream
of it, so a real hardware build does not need this answered. Recorded so
a future session does not redo this exact search, not as an invitation to
continue it. Method: read-only static scans (capstone, direct branch-
immediate decoding, literal-pool word search, table-branch resolution),
SHA-256 checked first; addresses only, no firmware bytes recorded.

F-110. A fresh angle for the saved-crop question, deliberately separate
from the record-builder chain F-095 through F-106 already exhausted (that
chain leans toward a settings/property handler, not a save path -- see
the correction to this project's hardware-readiness.md). This traces the
firmware's actual file-naming system instead of the capture-descriptor
candidate.

The `.NEF` ASCII literal noted in passing by F-099 resolves to a real
filename-template table at `0x11c9a5fc`: four 16-byte, null-padded ASCII
entries in order -- `DSC_0000.NDF`, `DSC_0000.NEF`, `DSC_0000.TIF`,
`DSC_0000.JPG` -- immediately followed by shooting-mode labels (`U1`,
`U2`, `U3`, `PSAM`, `Othe[r]`). A full-image raw-word scan for pointers
to each of the four filename strings found exactly two referencing
tables, at `0x1204d280` and `0x1204d440`, each holding the same four
string pointers in the same order (JPG, NEF, NDF, TIF) but with
different preceding data:

- `0x1204d280`'s preceding five words are three packed 16-bit pairs of
  consecutive power-of-two bit flags (`0x0002/0x0004`, `0x0008/0x0010`,
  `0x0020/0x0040`) -- a six-flag bitmask, one bit per format/quality
  option, plausibly covering two extensions not in this four-entry
  filename table. Two more words follow the pointers (unread until this
  point): `0x0539` and `0x053b` (1337, 1339), shaped like label or
  setting ids.
- `0x1204d440`'s preceding five words (`0xc1c, 0x111c, 0x42b, 0x1123,
  0x401`) do not fit the same bitmask pattern and were not interpreted
  in this pass. No trailing ids follow its pointer block (all zero).

Both tables are genuinely distinct data, not duplicates, referencing the
same underlying strings -- consistent with two different save contexts
(e.g. photo vs. movie, or two different quality/format menus) sharing one
filename-template resource. Observed static decode and full-image word
scan on 2026-10-16, high confidence for the table contents themselves.

Neither table's own consumer was found. Two methods were tried and both
came back empty: a full-image raw-word scan for either table's base
address (same method that found the filename-pointer tables themselves),
and a register-arithmetic scan (ldr-literal plus adds/mov propagation,
the technique that resolved F-108's slot producer) over a 0x60000-byte
window of a plausible nearby module. Neither is conclusive that no
consumer exists -- only that these two specific techniques, in the
range tried, did not find one. The consumer is the actual next step:
it is very likely the real file-save/naming routine, which is the kind
of code that could show whether and how saved dimensions or a crop
region get chosen, something the record-builder chain never
established.

Not yet done: a wider or different-range register-arithmetic scan for
the table consumer; decoding the `0x1204d440` table's five non-bitmask
preceding words (possibly geometry, not format flags); and, once a
consumer is found, tracing whether it reads any image-area/crop state
at all before naming or writing a file. Method: read-only static decode
(capstone, Thumb), full-image raw-word scans and a register-arithmetic
scan, SHA-256 checked first; addresses, offsets and table contents only
(ASCII filename templates transcribed as the existing project convention
allows for UI/system strings, no firmware bytes otherwise recorded).

F-111. Continues F-110's fresh angle. Neither filename-table consumer
(`0x1204d280`, `0x1204d440`) was found by any of three tried methods
this pass -- a full-image raw-word scan, a full-image `ldr`-literal
register-arithmetic scan (resolving `ldr rX,[pc,#imm]` plus `adds`/`mov`
propagation across all 15.7 million decoded instructions in the image),
and a full-image `movw`/`movt` pair scan (direct 32-bit constant
construction, bypassing literal pools entirely) -- all three came back
with zero hits for either table address. A wide dump of the surrounding
region (`0x1204d000`-`0x1204d600`) found other structured data (repeated
small-integer id sequences, a run of ASCII spaces) but no further
instance of the two tables' own shape, so they do not appear to be two
entries of one larger indexed array with a findable common base either.

A different search succeeded: F-110's two trailing words after the first
table's filename pointers, `0x0539` and `0x053b`, are not isolated --
a full-image scan for `movw`/`cmp` referencing either value as an
immediate found 31 hits, clustered in two modules
(`0x1034e000`-`0x1034fb00`, 8 hits; `0x104dd000`-`0x104e1400`, 9 hits).
Decoding the first cluster's entry point, `0x1034e674`, finds a real
property-driven settings handler: it reads a mode/selector property
(`0x2010`), then, depending on an earlier condition, reads either
`0x0539` or `0x1838` into a working register, then `0x053a`/`0x1839`
into another, and dispatches on the result (values 1, 2, 3) into
branches that compute three more sequential property ids each
(`0x0540`, `0x0544`, `0x0548` for one branch). This is a genuine
property-id family -- `0x539`-`0x53b`, `0x540`, `0x544`, `0x548`,
`0x1838`, `0x1839` -- being actively read and dispatched on by name, not
a coincidence of nearby numbers, and it directly includes the exact two
values (`0x539`, `0x53b`) found appended to the first filename table in
F-110.

A second function in the same module, `0x1034e86c`, reads an incoming
mode byte, searches a small 2-entry array for a match, and on specific
outcomes calls `0x1034e4cc`, `0x1035e7d6`/`0x10360d3c` (a setter,
paired with the getter `0x10360bba` used throughout the first function)
with property `0x0539`, then a refresh-style call (`0x1021994a` with
argument `0x32`). `0x1035e7d6` itself, and its sibling `0x1035e7f4`,
resolved to generic stride-8 search-and-return helpers (binary/linear
search over a small fixed array, used with several different small
lookup tables elsewhere in the same module for unrelated fixed keys,
e.g. `0x1035e852`'s wrapper) -- shared utility code, not evidence
specific to this property family on their own.

Inferred, confidence medium: this `0x1034exxx` module is very likely the
firmware's actual image-quality/format setting handler (reading and
writing which RAW/JPEG/TIFF variant is selected), given it operates
directly on the same property ids found attached to the filename-
template table. This is the closest this research has come to the real
save-path code since abandoning the record-builder chain (F-095-F-106).
Not established: the literal instruction that dereferences
`0x1204d280`/`0x1204d440` themselves (still not found), what the second
module cluster at `0x104ddxxx`-`0x104e1xxx` does (not decoded in this
pass), and -- the actual question this whole thread exists to answer --
whether anything in this property family reads or writes a crop/image-
area state before a file gets named or saved. Observed static decode
and full-image scans on 2026-10-16, no classifier stop. Method:
read-only static decode (capstone, Thumb), full-image raw-word,
register-arithmetic and `movw`/`movt` scans, SHA-256 checked first;
addresses, offsets and property ids only, no firmware bytes recorded.

F-112. A genuinely stronger lead for the saved-crop question than
anything found so far, reached by abandoning F-111's module (checked
directly: zero references to image-area property `0x501` anywhere in
either of its two address clusters, so it is very unlikely to be
crop-aware) and instead finding every direct reader of `0x501` itself.

A full-image scan for `movw/movs r0,#0x501` followed by a getter call
found exactly 8 sites, split between two accessor families: 6 use the
familiar `0x10465984` getter (already known from the XPan live-view
research); the remaining 2 use `0x10360bba`/`0x10360d3c` -- the same
getter/setter pair F-111's quality module used. One of those two,
`0x105a7946` (inside enclosing function `0x105a792a`), is a real
**width/height-by-area lookup**: it reads `0x501` (or accepts an area
value directly as a parameter), then calls `0x1020bfda(quality, area)`
**twice**, reading a signed 16-bit value from offset `0` (width) and
offset `2` (height) of the returned pointer each time -- the classic
shape of a `{width, height}` struct lookup.

`0x1020bfda` itself is confirmed as a genuine two-dimensional indexer:
`row = [table_base + 0x14][quality]; return row + area*4`, i.e. an
outer array indexed by quality/format, each entry a pointer to a row of
4-byte `{width:i16, height:i16}` structs indexed by area. **At least
nine sibling functions follow it immediately** (`0x1020bfe8`,
`0x1020bff2`, `0x1020bffc`, `0x1020c006`, `0x1020c010`, `0x1020c01a`,
`0x1020c024`, `0x1020c02e`, `0x1020c038`, ...), each with the identical
shape but a different literal offset (`+0x14, +0x28, +0x34, +0x40,
+0x54, +0x68, +0x7c, +0x90, ...`) -- almost certainly one such table
per save/display format class (RAW, several JPEG qualities, movie,
etc.), not one table total.

The table itself is **RAM-resident, not statically present in this
firmware image**: `0x1020bfda`'s own literal resolves to `0xc18c7de8`
(a RAM address), so its actual width/height content cannot be read from
the ROM image directly. A literal-word search for that RAM address
found only the one already-known reference (the getter's own literal);
no ROM-side initializer or template copy was found by this method in
this pass. This is the same category of limit this project has hit
before (F-106's unresolved slot, Lane 1's unresolved registration) --
live simulator inspection, not more static search, is the way to read
the actual numbers.

The lookup's result is consumed by `0x10237934`, which adjusts the
value (adding width+height-1 when a flag is set) and calls
`0x101ff4d2`/`0x101ff4f8` -- names not otherwise identified in this
project, shaped like generic string/count-formatting helpers given the
stack-buffer and `adr`-relative argument pattern. **Whether this is a
display-label formatter (showing pixel dimensions in the image-area
menu) or a real save-time size computation was not determined in this
pass** -- say so plainly rather than assume either.

Observed static decode and full-image scans on 2026-10-16, no
classifier stop. Confidence high for the table/lookup structure itself
(direct instruction-level decode); confidence low for whether this
specific call chain (`0x105a7946` -> `0x10237934`) is on the save path
or only a UI-preview path -- that is the open question, not the table's
existence. Not yet done: finding the ROM-side initializer that
populates the RAM table (to read real width/height values without a
simulator), decoding the other 8+ sibling tables to see which save/
format class each belongs to, and tracing `0x105a7946`'s own caller(s)
to see whether they sit in a menu-display context or an actual
capture/save context. Method: read-only static decode (capstone,
Thumb), full-image property-id and raw-word scans, SHA-256 checked
first; addresses, offsets and table structure only, no firmware bytes
recorded.

F-113. Decodes the crop-window builder's own body for the first time.
`0x101d5b36` has been central to this project's saved-crop research
since F-057 (as the function seven callers reach, studied in F-095
through F-098), but its internals were never read -- only its existence,
its callers, and (in F-096) the two block copies inside one caller's own
record-assembly code. This pass reads the builder itself, reached while
finding every caller of F-112's confirmed geometry table `0x1020bfda`
(one of the 37 callers found, `0x101d5c38`, is inside this function, not
a separate one as first suspected -- a backward push-scan confirms the
real entry is `0x101d5b36`, correcting that initial read).

The builder's body:

1. **Three unconditional lookups, always executed:** `ldrb [r5+0x26]`
   (a format/class byte) feeds `0x1020bfc8` (a sibling of `0x1020bfda`
   not previously catalogued, immediately before it); then `[r5]` (an
   area byte) plus the same format byte feed `0x1020c05c`; then `[r5]`
   alone feeds `0x1020c072`. Each call's result is a pointer whose
   offsets `0`/`2` (signed 16-bit width/height, the same shape F-112
   established) are copied into the output record at `+0`/`+2`,
   `+4`/`+6`, and `+8`/`+0xa` respectively -- three distinct
   width/height pairs, unconditionally.
2. **A gate, `0x101d5ad0(r5)`:** if false, the record's remaining
   fields (`+0xc` through `+0x1a`) are all zeroed and the function
   returns -- no crop offset is computed.
3. **If true, a mode/quality byte at `[r5+0x22]`** (0, 1, or 2) selects
   a value `r6` (0, 1, or 2) passed as a parameter to three more
   lookups: `0x1020c07c`, `0x1020c128`, `0x1020c17e` (area, format and
   `r6` all passed as arguments), each again returning a width/height
   pointer. The three results' width/height values are combined with
   addition and negation (`add r1,r6; rsbs r6,r6,#0; add r0,r0,r6<<1`,
   continuing past this read) -- centering/offset arithmetic, not a
   simple copy, consistent with computing a centered crop rectangle's
   position from a sensor/working-area size and a target output size.
   This arithmetic was not fully decoded to its end in this pass.

This establishes, for the first time, that the long-studied crop-window
builder performs real geometry computation using at least **six**
distinct sibling tables from F-112's confirmed `0x1020bfda` family
(`0x1020bfc8`, `0x1020c05c`, `0x1020c072`, `0x1020c07c`, `0x1020c128`,
`0x1020c17e` -- meaning more sibling tables exist than the roughly ten
found adjacent to `0x1020bfda` alone in F-112; the full family's extent
is still not mapped). The values produced are exactly the shape a real
crop rectangle needs (base dimensions plus a computed, conditionally-
gated centered offset) -- this is textbook crop-window construction,
not display-label formatting.

**This does not resolve F-097/F-106's capture-vs-estimator ambiguity.**
The builder is a shared utility reached by all seven of F-057's known
callers; nothing here establishes which of those seven call it for a
real save operation versus a UI/live-view preview (Lane 1's own
live-view-bars work is exactly the kind of preview context that would
also need a correctly-sized crop rectangle, independent of any file
being written). It deepens understanding of the tool itself -- what it
computes, and from which real data -- without yet answering which
caller context uses that computation for what purpose. Observed static
decode on 2026-10-16, no classifier stop, high confidence for the
instruction-level reads; medium confidence for the offset layout's
semantic interpretation (sensor/working/target dimensions plus a
centered offset) given the shape fits but was not independently
confirmed.

Not yet done: fully decoding the centering arithmetic to its end; the
gate function `0x101d5ad0`'s own condition; mapping the full extent of
the `0x1020bfxx`/`0x1020cxxx` table family (likely more than six);
and -- unchanged from every prior saved-crop fact -- determining which
of the builder's seven callers reaches an actual file-save operation.
Method: read-only static decode (capstone, Thumb) and a full-image
xref scan (`rom_xrefs.py`) on the confirmed geometry-table function,
SHA-256 checked first; addresses and offsets only, no firmware bytes
recorded.

F-114. Completes two of F-113's three open items; the third hit a
response-safety-classifier stop and was dropped rather than retried,
per this project's established handling of that situation (same as
Lane 1's three-stop pattern on a different sub-question).

**The centering arithmetic (F-113's incomplete item) is now fully
resolved.** Labelling the three lookup results `0x1020c07c` ->
`(W1,H1)`, `0x1020c128` -> `(W2,H2)`, `0x1020c17e` -> `(W3,H3)`, the six
stored fields work out (treating the rounding adjustments as exact
halving) to:

| Offset | Value | Meaning |
| --- | --- | --- |
| `+0x10`/`+0x12` | `(W2+W3, H2+H3)` | top-left corner |
| `+0x14`/`+0x16` | `(W1+W2-W3, H1+H2-H3)` | bottom-right corner |
| `+0xc`/`+0xe` | `(W2+W1/2, H2+H1/2)` | the exact midpoint of the two corners above -- the window's center |
| `+0x18`/`+0x1a` | F-112's table, `(area, quality)` | final output width/height |

This is an unambiguous crop-rectangle descriptor: a top-left corner, a
bottom-right corner, their center, and a separate final output size --
exactly the fields a real crop-and-resize operation needs, not a
display-label format. Confidence high; this is direct algebra on an
already-confirmed instruction sequence, not inference.

**The gate function `0x101d5ad0` is trivial and now fully read:** it
reads a byte at `[input+0x20]` (an operating-mode/state byte on the
same source object the area byte `[input]` and format byte
`[input+0x26]` come from) and returns true only for values 0 or 1. The
centered-rectangle fields (`+0xc` through `+0x1a`) are computed only
when this mode byte is 0 or 1; any other value zeros them instead. What
values 0/1 versus 2+ actually represent (e.g. an active-capture state
versus idle/menu-only) was not established.

**Dropped, not retried, per a response-safety-classifier stop:**
checking F-057's seven known callers of the crop-window builder for
which one reaches a real save operation. This exact question does not
need new work regardless -- F-095 and F-096 already characterized all
seven: six build small display/menu-info structs (not save paths), and
the seventh (`0x101d5de8`, inside `0x101d5c54`) is the record-builder
chain F-096 through F-106 already traced in depth, leaning toward a
settings/property handler rather than a capture descriptor. The honest
state is unchanged by this pass: no caller is confirmed as a real save
path, and the most-traced candidate leans away from being one. Do not
re-attempt this specific check; if it needs doing, hand it to the owner
to run in their own terminal (the pattern already established for this
kind of stop in this project).

Observed static decode on 2026-10-16 for the two completed items,
confidence high for both. Not yet done: mapping the rest of the
`0x1020bfxx`/`0x1020cxxx` table family beyond the six confirmed callers
of `0x101d5b36` itself (F-112 found roughly ten adjacent to
`0x1020bfda`; F-113 found six more scattered further out, so the true
extent and total count remain unmapped); and the still-open question of
which caller, if any, is a real save path -- deliberately not pursued
further by this session after the classifier stop above. Method:
read-only static decode (capstone, Thumb) and direct algebra on already-
confirmed instructions; no new firmware reads beyond what F-113 already
covered.

F-115. Fixes two of the three concrete findings from the instruction-level
audit on PR #145 ([native-xpan-liveview-hook-audit.md](native-xpan-liveview-hook-audit.md))
in a private, throwaway copy of the guarded-hook generator, rebuilds the
private overlay, and re-runs every existing simulator control against it.

**Finding 2 (r2 clobbered) and finding 3 (stack alignment), fixed.** The
screen-activation wrapper's push/pop went from `{r0,r1,r4,lr}` to
`{r0,r1,r2,r3,r4,lr}`, so all four argument registers the call site sets up
survive the wrapper's intervening call before the real target runs. The
close wrapper and the guard each went from pushing `{lr}` alone to pushing
`{r4,lr}`, restoring 8-byte stack alignment for the stock callback and the
guard's own read. All three changes are same-size push/pop bitmask edits
only; no other offset in any of the three routines moves. Re-disassembled
every routine and every rewritten branch with capstone after the rebuild:
all targets and offsets are exactly as intended.

**Finding 1 (shared mask-clear helper), investigated but deliberately left
unchanged.** Traced the shared helper the audit flagged (`0x102355ee`
through `0x102355f4`) to its one caller, `0x10198d12`, which is itself one
entry in a long, flat sequence of individual `b.w` stubs -- a generic
per-object-type activation dispatch table, not something specific to
live-view or to the handful of object types this project has already
named. This confirms the audit's concern is architecturally real: the
activation path the hook sits on is shared across many unrelated object
types, not just live-view's overlays. Properly narrowing the clear
condition (e.g. to "live-view layer is deactivating" rather than "any
other object is activating") would require identifying which of the many
object types reaching this generic dispatch are legitimate screen
overlays during live view -- an open-ended trace this project's own
priority rule says not to start for a simulator-side question. Left the
existing behavior (clear mask on any non-live-view activation) unchanged
as the safest, no-regression choice, and recorded this as a deliberate,
evidence-backed deferral rather than a fix.

**Re-run controls, all passed against the fixed overlay:** the direct
1:1/DX/1:1/16:9 sequence; ten alternating menu/live-view signal cycles; the
internal `0x250` non-live-view close event (the mask correctly stays off --
the field name `natural_return_passed` checks for the *rejected* unguarded
behavior, so `false` here is the passing result, matching this project's
own documented design intent); and the diagnostic live-view-ready probe
(`passed: true`). Firmware hash and pinned QEMU checkout were asserted
unchanged before and after every run.

**One natural-path attempt against the fixed overlay, with a materially
different result than the same test against the pre-fix overlay (PR
#146).** Repeated the dissenting review's cheapest remediation option --
preset the mode-state byte via the firmware's own setter (not a debugger
write) and call the real close handler `0x10460c3c` directly -- against
this fixed overlay. Against the *pre-fix* overlay, the guard (`0x1002d860`)
and mask helper (`0x1002d78c`) were never reached. Against the *fixed*
overlay, both were reached (observed twice each during the one close-handler
call), including the guard being hit with the live-view object and selector
value the guard is designed to admit on. The observed mask flag was already
1 before this call and stayed 1 after, so this run does not by itself show
a flag flip caused by the close path -- it shows, for the first time, that
the guard and mask are *reached* on this consumer-side path when the state
the real setter writes is present, rather than being silently skipped. The
most likely explanation is the stack-alignment fix (finding 3): the close
wrapper's stock callback previously ran 4 bytes off 8-byte alignment, which
plausibly diverted or truncated execution before the subsequent guard call
ran. This explanation was not pursued further (would require single-
stepping the stock callback under both overlays, the kind of open-ended
simulator-fidelity trace this project's priority rule says to avoid) --
recorded as observed, not as a proven cause. Per the task's own instruction
to try exactly one such test and stop, no further variants (e.g. a
different preset value, or starting from flag 0) were attempted.

Confidence: high for the two fixed findings and the re-run controls (direct
disassembly plus simulator result); medium for the natural-path result
(one run, cause not confirmed); the finding-1 deferral is a documented
choice, not a finding. This does not change condition 1's status --
[hardware-readiness.md](hardware-readiness.md)'s dissenting review still
stands, and that call remains the owner's to make. Method: static
disassembly (capstone, Thumb) of a private generator copy and its rebuilt
overlay, plus disposable QEMU loader-overlay simulator runs; no firmware,
overlay bytes or disassembly committed to the repo.

F-116. Tries [tracking-input-chain.md](tracking-input-chain.md)'s option 2
handoff: a masked/family-level static search for a dispatcher that tests
property id `0x2021`/`0x2087` by their shared high byte (`0x20`) rather
than by exact literal value. Negative result; the lead this scan actually
turned up is unrelated.

**Method.** A full-image linear decode (capstone, Thumb, SHA-256 checked
first) looking for any `cmp`/`cmp.w rX, #0x20` immediately or shortly
preceded by an extraction of `rX` as the high byte of some other register
(`lsrs rX, rY, #8`, `ubfx` with lsb 8, or an `#0xff00` mask) -- the same
category-plus-sub-id encoding shape F-104 found for SD command words.
This is a genuinely different search from the prior literal-`0x2021` scans
(`tracking-input-chain.md`'s handoff section): it looks for the *shape* of
a masked dispatch, not a specific immediate.

**Result: six raw hits, one real, zero relevant.** Four of the six are
decode artifacts of scanning data/non-code regions as if they were Thumb
instructions (confirmed by inspecting their surrounding context: nonsense
instruction sequences, e.g. a `movs r0, #0x20` sitting between the
extraction and the compare it was spuriously paired with, which the
matching script did not detect as an intervening overwrite). One real,
cleanly-decoded dispatcher was found at `0x105afa0e`
(`lsrs r1, r0, #8; cmp r1, #0x20; ...; sub.w r1, r0, #0x2000; subs r1,
#0xc; beq ...`) -- but reading its enclosing function (`0x105af9b0`
onward) shows it is a text/string-formatting routine: the surrounding
code checks `r0`'s low byte against ASCII-range values (`0x22`, `0x23`,
`0x25`, `0x27`, `0x44`) and walks a character buffer, not a property-event
struct. The `0x20xx`/`0x6xx` ranges it tests are escape-code categories in
a format string, unrelated to the UI property-notification system this
project has traced elsewhere (F-090, F-106, this file's `0x2021` entries).

**This does not resolve Lane 3's handoff point.** It rules out the one
specific masking idiom this scan checked (`lsr #8` immediately feeding a
`cmp #0x20`) as a way to find `0x2021`'s consumer by this method, in the
sense that the only clean hit it produced is provably unrelated. Confidence
high for the one real hit's unrelatedness (read its full enclosing
function); the negative result for this one idiom is otherwise as
exhaustive as a single-idiom full-image scan can be. Method: read-only
static decode only; no firmware bytes recorded.

**Same pass, two more idioms tried, same result.** `ubfx rX, rY, #8, #8`
(a Thumb-2 bitfield extract of bits [15:8]) feeding a `cmp rX, #0x20`
within a short window: zero hits anywhere in the image. `and`/`and.w rX,
rY, #0xff00` feeding a `cmp rX, #0x2000`: two raw hits (`0x11db2d78`,
`0x11e38b10`), both artifacts of the same matching-script limitation (an
intervening register overwrite -- here, a reload and a *different* mask,
`#0x3800` -- the script didn't treat as breaking the chase). Reading both
sites' context shows ordinary peripheral/register-programming code (a
sequence of helper calls with small integer argument setup, e.g.
`mov.w r2, #0x800`/`#0x700`/`#0x3800`), not event/property dispatch of any
kind. Three masking idioms tried now (`lsr #8`, `and #0xff00`, `ubfx`),
zero genuine property-dispatch hits among them.

A `tbb`/`tbh` range-dispatch table keyed on the high byte was not
attempted -- it requires first locating candidate jump tables and decoding
their index expression, a meaningfully different (and more involved)
search than the three direct-compare idioms above, not a quick addition to
this same scan. [tracking-input-chain.md](tracking-input-chain.md)'s
option 1 (live simulator breakpoint on the post primitive `0x10475ecc`)
remains untried and, given three of four plausible static idioms are now
exhausted with nothing found, is the more promising next step.

F-117. Tries both remaining leads named by F-116: the fourth static
masking idiom (`tbb`/`tbh` range dispatch) and
[tracking-input-chain.md](tracking-input-chain.md)'s option 1 (a live
simulator breakpoint on the shared property-post primitive `0x10475ecc`
during ordinary navigation). Both come back negative, and the second is
more informative than a simple miss.

**`tbb`/`tbh` scan.** A full-image scan found 2,817 table-branch sites
total -- an ordinary count for a firmware this size, and far too many to
review individually. Checked each for a narrow gate shape only: an
immediate `sub rX, #0x20xx` writing the table's index register directly
in the instructions immediately preceding the branch. Zero matches. This
is not a clean negative the way the other three idioms were: it only
rules out *this one* index-computation shape, not `tbb`/`tbh` dispatch on
the high byte in general (a real dispatcher could compute the index
through intervening moves, a different immediate encoding, or a lookup
rather than a subtraction, none of which this narrow check would catch).
Properly exhausting this idiom would mean manually reading dispatch
tables near each of the 2,817 sites -- not attempted, and not a
reasonable next step without a smarter filter first.

**Live simulator breakpoint, `0x10475ecc`, during ordinary navigation.**
A private script armed a software breakpoint on the primitive and ran: an
idle checkpoint wait, the real menu-activation helper (`0x102355ee`,
the same call `display_session.py`'s own example uses to open the menu),
eight real internal UI-event codes through the real key dispatcher
(`0x103ce96e`) -- OK, back, and four directional codes confirmed in
F-017/F-020/F-023 -- and a second idle checkpoint wait. All diagnostic
calls, same technique this project uses throughout; no memory write of
any property or UI state. **The primitive was never called at all --
zero observations, for any id, across the entire sequence**, not just a
miss on `0x2021` specifically. Firmware hash and pinned QEMU checkout
unchanged throughout.

This is a stronger, more informative negative than a miss on one id: it
says the entire property-post mechanism this consumer search is built
around does not fire via this call path at all in this fixture, matching
this project's long-documented "dormant worker" pattern (F-018, F-019,
and Lane 1's own natural-trigger gaps) rather than showing anything
specific about `0x2021` or `0x2087`. It does not distinguish "the
producer of `0x2006`/`0x2020`/`0x2021`/`0x2087` needs a live
background task this fixture doesn't run" from "navigating through
*this* screen/menu never posts those ids regardless." Confidence high for
the zero-observation result itself (the same breakpoint technique
correctly observed other primitives elsewhere in this project); low for
any claim about why, since the dormant-worker explanation is inferred by
analogy, not demonstrated for this specific primitive.

**Net effect on Lane 3's handoff point:** four static masking idioms are
now tried (one inconclusive due to volume, three clean negatives) and the
live-breakpoint option has returned a clean, strongly dormant-worker-
shaped negative rather than a hit. No consumer for `0x2021` has been
found by any method attempted across F-116/F-117. The honest state is
that this project has exhausted its cheap options on this specific
question; what would actually move it forward is either reading
individual `tbb`/`tbh` tables by hand near plausible call sites (slow,
unautomatable without a better filter) or finding a way to keep the
relevant background task alive in the simulator long enough for a real
post to occur (a different, harder problem this project has hit
repeatedly and not solved for any lane). Method: software breakpoints via
the existing diagnostic-call mechanism (no debugger memory write); static
decode (capstone, Thumb); firmware hash and QEMU checkout verified
before and after; no firmware bytes, overlay bytes or disassembly
committed to the repo.

F-118. Picks up Lane 2's own named next step (project-status.md: "a live
simulator read ... not more static search") rather than Lane 3's. Re-runs
F-078's existing diagnostic-call script against the crop-window builder
`0x101d5b36` (no script changes -- it already reads back all 14 output
shorts, covering every field F-113/F-114 later labeled) across every
area/quality/flag combination the script already tests, and checks the
fresh numbers against F-114's centering formulas for the first time.

**F-114's center claim is now confirmed by live execution, not just
static algebra, across every one of the 15 tested combinations** (areas
0 through 4, both quality bytes, both `+0x26` flag states) -- not a
sample, the full set this script covers. The `+0xc`/`+0xe` field equals
the exact arithmetic midpoint of the `+0x10`/`+0x12` top-left and
`+0x14`/`+0x16` bottom-right corners in every single row, including the
degenerate all-zero rows for areas 1 and 3 (consistent with F-057/F-078's
"slots 1 and 3 return all zeros"). Examples: area 4 (1:1), large --
top-left `(8,8)`, bottom-right `(3720,3720)`, center `(1864,1864)`; area
4, medium -- top-left `(0,0)`, bottom-right `(2784,2784)`, center
`(1392,1392)`; area 0 (DX), large with `+0x26` set -- top-left `(72,198)`,
bottom-right `(5640,3910)`, center `(2856,2054)`. All are live
register-and-memory results from real diagnostic calls, not inference
from decoded instructions.

**The "final output size" field's `(0,0)` pattern is now fully explained,
not an open detail.** `+0x18`/`+0x1a` reads `(0,0)` in every row where
the quality byte is `0` (large) or the `+0x26` flag is set, *regardless
of area and regardless of whether the crop window itself is nonzero* --
e.g. area 0 large has a real top-left/bottom-right pair but still reads
`(0,0)` here. In every row where it is nonzero, it exactly equals the
bottom-right corner (top-left is always `(0,0)` in those rows). This is
a consistent sentinel across the whole table, not an anomaly specific to
one area: `(0,0)` most plausibly means "no additional resize -- use the
crop window's own dimensions," matching the ordinary real-world
convention that a RAW "large" size needs no resize step. Confidence
medium-high (consistent across all 15 rows); still not confirmed against
F-112's table rows directly, but no longer needs to be to settle the
pattern itself.

**This does not change the caller/save-path question.** F-095/F-096
still stand: six of the builder's seven callers build small display/menu
structs, and the seventh (the one genuinely ambiguous one) leans toward a
settings/property handler per F-103, not a capture descriptor. This fact
only strengthens confidence in the geometry math itself, which was
already high; it does not touch which caller, if any, is a real save
path -- that remains dropped per the classifier-stop handling already on
record (F-114), not reattempted here. Method: re-run of an existing,
unmodified private script (simulator only, scratch memory, restored after
each call); SHA-256 and QEMU checkout verified before and after. No
firmware bytes recorded.

F-119. Answers F-112's own open question directly: "finding the ROM-side
initializer that populates the RAM table... to read real width/height
values without a simulator" -- no diagnostic call needed, just a direct
memory read after ordinary startup, walking the two-level pointer
structure F-112 already decoded (`row = [0xc18c7de8+0x14][quality]; entry
= row + area*4`).

**Real data, for the first time.** The row-pointer array at `0xc18c7dfc`
holds four non-null pointers (`0x115a4da8`, `0x115a4dcc`, `0x115a4db4`,
`0x115a4dc0` for outer index 0-3), each into ordinary ROM address space
-- confirming F-112's picture exactly: the *array of pointers* is the
RAM-resident part (initialized at boot), each pointer's *target data* is
static ROM. Full 4x6 table, `{width:i16, height:i16}` per cell:

| outer idx | entries (6, inner idx 0-5) |
| --- | --- |
| 0 | `(5568,3712) (4176,2784) (2784,1856) (5568,3128) (4176,2344) (2784,1560)` |
| 1 | `(0,0) (0,0) (0,0) (3712,3712) (2784,2784) (1856,1856)` |
| 2 | `(5568,3128) (4176,2344) (2784,1560) (0,0) (0,0) (0,0)` |
| 3 | `(0,0) (0,0) (0,0) (0,0) (0,0) (0,0)` |

**Cross-validated against F-118's live output, three exact matches.**
F-118's non-zero `+0x18`/`+0x1a` final-output-size results each appear
verbatim somewhere in this table: area 0/medium's `(4176,2784)` ==
outer-0/inner-1; area 2/medium's `(4176,2344)` == outer-0/inner-4 (also
outer-2/inner-1, since those two rows are mirror images of each other);
area 4/medium's `(2784,2784)` == outer-1/inner-4. This confirms the
builder's final-output-size field and this table are the same data
source, not a coincidence.

**Correction to the obvious first guess, stated honestly rather than
glossed over: the (outer, inner) indices are not simply (quality byte,
area byte) in the builder's own numbering.** F-118 held quality constant
(medium, its own byte value `1`) across all three matches above, but the
matching *outer* table index was `0`, `0`/`2`, and `1` respectively --
not a constant. The true transformation from the builder's (area byte,
quality byte) to this table's (outer, inner) indices was not solved this
pass. One pattern worth handing forward, observed not proven: outer row
0's six entries split cleanly into a DX-shaped triple (`~3:2` ratio,
inner 0-2) and a 16:9-shaped triple (inner 3-5, matching row 2's first
three exactly); row 1's nonzero entries (inner 3-5 only) are all square
(1:1-shaped). This looks like the table is organized by aspect-ratio
family in the inner index with the size (large/medium/small) as a
sub-position within each family-of-three, and the outer index may
select *which combination of families is valid for that row* rather
than being "quality" in the builder's sense -- consistent with row 3
being all-zero the same way the builder's own areas 1 and 3 are (F-057/
F-078). Not confirmed; flagged for whoever maps the remaining sibling
tables (F-112's other ~8 offsets) next, since the same index puzzle
will recur there.

Confidence high for the raw table contents and the three exact matches
(direct memory reads, verified programmatically against F-118's full
output set, not eyeballed); low for the aspect-family index theory above
-- explicitly not proven, offered as a lead. Method: direct remote
memory read after ordinary simulated startup, no diagnostic call, no
firmware modification; SHA-256 and QEMU checkout verified before and
after. No firmware bytes recorded.

F-120. Closes one specific item F-109 flagged as untried ("ARM-mode
scanning") -- not by answering F-109's actual question, but by
confirming, for the first time in this project, that this firmware
genuinely contains ARM-mode code at all. Every static decode this
project has ever done (including F-109's four exhaustive methods) was
Thumb-only; this checks whether that was ever actually wrong to assume.

**Real ARM-mode code confirmed, not hypothetical.** A full-image Thumb
scan for `blx` with an immediate operand (the only Thumb instruction that
unconditionally switches the core to ARM state) found 16,066 raw hits
across 7,693 distinct targets -- almost all of that volume is the same
scan-artifact noise this project has hit repeatedly this session (data
decoded as if it were code). But the small number of high-frequency
targets are real: spot-checked four of them by decoding as ARM32 from
their own address, and all four are clean, idiomatic ARM code, not
garbage:

- `0x10199bdc`/`0x10199cf0` (2,144 + 2,763 call sites): a textbook ARM
  `memcpy`-style routine -- 32-byte block transfer with `ldm`/`stm`, a
  byte-aligned tail-handling continuation. One of the two sites
  (`0x10199bdc`) is called directly from the InitTask entry function
  (`0x10053070`), the single most central checkpoint this entire
  project's tooling waits on -- genuinely live, heavily-used code, not an
  obscure corner.
- `0x11d6cc24` (23 call sites): byte-for-byte the same `memcpy` logic as
  `0x10199cf0`, at a completely different address -- a second, separate
  linked copy, consistent with a large multi-module firmware statically
  linking its own C runtime per module rather than sharing one copy.
- `0x1027f154` (156 call sites) and `0x1027ed08` (219 call sites): shaped
  like ordinary ARM EABI compiler-runtime helpers (sign/magnitude
  handling consistent with a software divide/modulo routine; a `clz`-
  based normalization step), not application logic.

**What this does and does not mean.** It means this project's blanket
assumption of Thumb-only code was wrong, and that any future "zero
callers found by every static method" dead end (F-103's `0x10156714`,
F-109's `0x10459d80`, this session's F-116/F-117 for Lane 3) *could* in
principle be explained by a caller living inside one of these ARM
islands, invisible to a Thumb decoder the same way data regions produce
garbage Thumb. **It does not show that any specific one of them is** --
every confirmed-real example found this pass is a mundane compiler
runtime helper (memcpy, a divide-shaped routine), not application-level
event dispatch, and it would be architecturally unusual for a firmware's
own UI/property-notification logic to be hand-written in ARM mode while
everything else is Thumb. Mapping the full extent of every ARM island
and checking whether any of them references `0x10459d80`, `0x4100012`,
or a property-`0x2021`-shaped dispatcher was not attempted -- that is
real, separately-scoped work (find each ARM region's boundaries, decode
it as ARM, search it the same way F-109 searched Thumb code), not a
quick addition to this scan, and is exactly the kind of open-ended
simulator/methodology trace AGENTS.md's priority rule cautions against
starting speculatively. Flagged for whoever (likely Codex, alongside
Lane 0) has reason to revisit one of those specific dead ends next, not
pursued further here.

Confidence high for the four spot-checked sites being genuine ARM code
(clean decode, one directly confirmed live via a well-known caller);
low/unknown for the remaining 7,689 distinct targets, most of which are
presumed noise but were not individually checked. Method: full-image
Thumb decode scanning for `blx`-immediate (capstone), then ARM32 decode
of a handful of the highest-frequency targets for verification; SHA-256
checked first. No firmware bytes recorded.

Written by Claude (Sonnet 5.5) and Codex in collaboration with Tony Kim.

F-135. The recovered package verifier accepted the verified original, and
a newly written private helper inverted its decode transform entirely in
memory, reproducing the complete 34,496,798-byte package exactly. The source
was reread unchanged; no firmware image was written. The verifier checks
original package/EG identities, decoded header/layout, container CRC and all
three component CRC residues. It contains no signature verification or
camera-updater execution; camera-side authentication and modified-package
acceptance remain unverified. Its original-hash gates make it unsuitable as
a candidate validator, and its three synthetic tests do not exercise the
container/CRC rejection paths beyond those gates. Observed source audit and
unchanged in-memory round trip, 2026-10-17, high confidence within that scope.
[Method, reproduction and next build decision](native-package-verifier-audit.md).

F-136. A newly written read-only decoded-container validator checks exact
length/layout, ordered unique expected names/sizes, reserved fields, component
and container CRCs, and independently supplied unchanged-component hashes.
Synthetic tests reject malformed inputs and a changed payload with both CRC
levels repaired when its original hash is pinned. The decoded original passed
with all three component hashes pinned, agreeing with the recovered verifier;
the unchanged in-memory package round trip still passed. No firmware image
was written. This does not establish allowed edits, encoded-package integrity
or camera acceptance. Observed synthetic tests and read-only original-input
validation, 2026-10-17, high confidence within that scope.
[Contract, tests and reproduction](native-container-validator.md).

F-137. A newly written read-only exact-edit auditor pins original size/hash,
checks full original/replacement hashes for ordered nonoverlapping spans,
rejects all other changes and reports candidate/manifest identities. Synthetic
tests cover missing/partial/extra edits, invalid policies and a combined
container case demonstrating that CRC validity and edit-plan compliance are
separate requirements. The verified original package versus its unchanged
in-memory reconstruction passed an empty manifest with zero changed bytes.
No real firmware edits or image writes occurred. Observed synthetic tests
and unchanged-input baseline, 2026-10-17, high confidence within that scope.
This does not establish instruction correctness or camera acceptance.
[Contract and reproduction](native-exact-edit-audit.md).

F-138. A newly written read-only decoded-container preflight composes original
identity, exact edits, both container checks and unchanged-component hashes
on the same immutable inputs. It requires explicit changed-component names,
rejects cross-component/header edits and binds the full policy in its report.
Synthetic integration cases pass/reject as expected; the verified original's
decoded unchanged baseline passes with zero changed bytes. No firmware image
was written. Reports explicitly say decoded-container-only and hardware
readiness not established. Observed tests and unchanged baseline, 2026-10-17,
high confidence within that scope; camera updater behavior remains unverified.
[Contract, reproduction and next real-build decision](native-combined-preflight.md).

F-139. Native camera-body package discovery reaches parser `0x101cdcea`.
All three verified-original components match native templates; EG is execution
type 3 and reaches `0x101ce89e`, then an ARM trampoline to relocated Thumb
target `0xc2b10cd5`. Effective native decode masks and all 256 CRC-table entries
agree with the desktop algorithms. A separate validation path includes a
20-byte digest comparison consistent with SHA-1; its selection predicate and
all input sources remain unresolved, including a read from `0x10000088`
outside EG's direct mapping. This is not proof of a signature scheme or its
absence. Flash erase/program and camera acceptance remain unverified. Observed
bounded static decode and private algorithm comparisons, 2026-10-17, high
confidence in checked links/tables, inference for the digest algorithm.
No firmware was modified or written.
[Evidence, limits and reproduction](native-updater-validation.md).

F-140. Resolves F-139's selector: the native container reader sets an
encoded-format byte; per-file snapshot stores it at `+0x1a0`, and selection
restores it to the field returned by `0x101cf8cc`. The verified original's
header predicts flag 1 and validation path `0x101ce518` after successful
record restore. This was not executed. The digest compares the first 20 outer
package bytes against a computation over the decoded container plus an
eight-byte transformed suffix. The suffix configuration is traced, but its
eight-byte source at `0x10000088` remains unmapped outside EG's direct file
mapping. No digest reproduction, firmware change or image write occurred.
Observed static links and original-header predicates, 2026-10-17, high
confidence in those checks; branch execution and camera acceptance unverified.
[Input boundaries and reproduction](native-updater-digest-inputs.md).

F-141. The checked startup page-table entry maps digest input `0x10000088`
to the same physical address below EG's base. None of the 18 bounded startup
scatter destinations covers it (three copies, fifteen zero fills). This
records a missing-input boundary; later remapping/external boot sources are
not ruled out. The updater relocation is resolved: descriptor `0x10034010`
copies 4,016 bytes from ROM `0x12079f00` to RAM `0xc2b10000`, mapping Thumb
entry `0xc2b10cd5` back to EG offset `0x0205abd4`. The entry prepares state;
actual flash erase/program remains unverified. Observed bounded startup
decode/table analysis and private verifier, 2026-10-17, high confidence within
that scope. No firmware modification or image write.
[Mapping evidence and next step](native-boot-mapping-boundary.md).

F-142. The mapped main-updater callback reaches identifiable native erase,
buffered/halfword programming, polling and readback paths. Initialized logical
region 2 selects target `0x10020000..0x12960000` (end exclusive), capacity
43,253,760 bytes. The 33,939,512-byte EG payload excludes its two component
CRC bytes; preparation fills the 9,314,248-byte remainder with FF. The loop
uses 330 chunks of 128 KiB, erases the leading chunk before programming, and
programs it last. This is not atomicity or recovery evidence. `0x1011a028`
handles mapping; the worker callback is submitted through `0x101a27f4`.
Observed bounded static decode, initialized-table reads and private semantic
verifier, 2026-10-17, high confidence within that scope. Runtime geometry,
physical writes and recovery remain unverified. No updater function executed,
firmware modification or image write.
[Span, handoff and reproduction](native-install-span.md).

F-143. A newly written read-only installation model checks two-byte component
CRC exclusion, full target/padding bounds and protected ranges, reports chunk
order and streams an expected span hash without creating an image. Combined
preflight binds the optional model to its validated candidate component and
includes target policy in report identity; omission is explicit. Synthetic
tests and the audited unchanged original agree on 33,939,512 payload bytes,
9,314,248 padding bytes and 330 chunks. Observed tests and private unchanged
baseline, 2026-10-17, high confidence within that static scope. No firmware
image or device operation; native digest, runtime geometry and recovery remain
unverified.
[Contract, validation and next review](native-installation-model.md).

F-144. Read-only review of the existing F-101 guarded overlay and its later
private revision checks nonoverlapping EG/install mappings, four original
hook instructions, twenty direct branches and five literal loads per
revision. Writer return matches its original frame; adjusted state-pointer
and selector mappings agree. The later revision preserves extra argument
registers and fixes close/guard relative alignment, but both revisions retain
four stack bytes at the state wrapper's stock-service call. The original tail
transfer retains incoming SP; the overlay call shifts it and the kernel
veneer's captured stack view. Condition 3 does not pass. Exact service stack
argument use and physical failure were not observed. Observed bounded static
decode and existing-file audit, 2026-10-17, high confidence within that scope.
No overlay build/change, firmware image, execution or camera access occurred.
[Review, limits and next contract test](native-xpan-contract-review.md).

F-145. A newly written supplied-boundary call checker and fourteen synthetic
operation tests define a corrected state-wrapper contract: restore incoming
registers, SP, LR and caller stack before tail transfer; preserve reference
service results and caller return behavior. Invented traces pass both added-
work branches and ARM/Thumb returns; residual/aligned stack displacement,
argument loss, stack corruption, bad helper alignment and return corruption
fail. Observed abstract-model tests only, 2026-10-17, high confidence within
that scope. No firmware input or encoded instructions were used, no private
overlay changed and no machine-code implementation is approved. F-144's
existing-overlay rejection and hardware NO-GO remain unchanged.
[Contract, tests and evidence boundary](native-call-contract-tests.md).

F-146. A private textual proposal maps F-145's corrected contract to a
32-byte temporary frame, fully restored before the stock-service tail
transfer. The state wrapper including literals uses 40 bytes; its adjacent
writer uses eight, leaving four bytes in the checked 52-byte zero span.
Writer entry moves four bytes and its hook must be retargeted. Local assembler
textual validation accepts fourteen forms/widths; independent arithmetic
checks six branch distances and two literal loads. Observed static layout
and original/existing-file checks, 2026-10-17, high confidence within that
scope. Final external branch encodings and execution remain unverified; no
object, overlay or firmware image was written. Condition 3 remains open.
[Method, limits and simulator-only next experiment](native-xpan-layout-proposal.md).

F-147. A throwaway private correction passes final branch decode and loaded-
file hash checks in the pinned simulator. Paired diagnostic calls with a
settled stock 1:1 choice show original r0-r12, SP/LR and three caller-stack
words at the stock service on both state branches. Live-view mask flag is 1;
other-screen flag is 0. The other-screen return changes NZCV from 8 to 6 and
fails F-145's unchanged strict comparator. Relocated writer calls consume
the same stock working frame and match original register/SP/target results;
scratch LR and flags are not certified. Observed assisted QEMU diagnostics,
2026-10-17, high confidence within that bounded scope. Original firmware and
simulator checkout unchanged; new overlays/raw evidence stay private. No
camera, updater execution, combined firmware image or acceptance of condition
3. [Inputs, controls, results and next correction](native-xpan-abi-experiment.md).

F-148. A private application-status-preserving overlay resolves F-147's
measured flag mismatch. Ten final branch targets, four status-transfer
instructions and three literal loads pass static checks; loaded file hashes
match. Paired pinned-QEMU diagnostics pass both state contracts with entry
flags additionally required and full return registers/CPSR equal. Mask flags
are 1 for live view and 0 for the other state. Both writer working frames,
r0-r12/SP results, return target/mode, CPSR and caller stack match the stock
baseline; scratch LR differs and is explicitly not certified as identical.
Observed finite assisted diagnostics, 2026-10-17, high confidence within that
scope. Original firmware and simulator checkout unchanged; concrete overlays
remain private. Natural lifecycle, global condition 3, saved crop and hardware
readiness remain open. [Review and evidence limits](native-xpan-flags-remediation.md).

F-149. F-110's stored filename-pointer tables map through the checked startup
copy to RAM `0xc18cb5ec` and `0xc18cb7ac`. Both 16-byte pointer blocks and
F-112's 32-byte header at `0xc18c7de8` match their initialized sources after
unmodified stock assisted startup. A full-image aligned-word search within
64 bytes of the two RAM bases finds three and five nearby references, none
at the exact base. Bounded decode of one anchor confirms neighboring indexed
halfword format/flag lookups, not a filename-field consumer or save path.
Observed static mapping/search and bounded simulated RAM comparison,
2026-10-17, high confidence for those mappings only. No firmware change,
capture, cropped file or camera access. Actual filename-field consumption
remains unresolved and is reserved for the owner-approved on-camera test; no
static route remains open. [Evidence and limits](native-save-table-ram-mapping.md).

F-150. Still-versus-movie predicate at the live-view hook `0x102f5810`:
unresolved. Inside the live-view type-2 handler `0x102f57e2`, the only branch
before the selector write is a bit test on a byte at `0xc181b4b4`. It skips
one call to `0x104bd3c0`, and both paths rejoin at `0x102f580c`. The write at
`0x102f5810` stores selector 1 into `0xc1821d44 + 0x74` through setter
`0x104b9116`, with no still, movie, playback, warning or unavailable test.
The guard (empty stack plus selector 1) therefore cannot separate still
capture from movie recording, and it cannot exclude those states. Movie live
view is admitted if it reaches this worker (inferred, medium). The byte at
`0xc181b4b4` is not identified, and the bit-6 gate's meaning is unknown. This
conflicts with the design rule that movie mode stays off
([xpan-bars-design.md](xpan-bars-design.md)). Observed static decode, high
confidence; the natural caller and worker trigger remain unobserved (F-019).
Needed: a state value that marks still capture, traced to a load before
`0x102f57e2`. Hook stays out of build decisions until then.
[Evidence and limits](native-xpan-liveview-hook.md).



F-151. The pointer slots of F-110's two filename tables sit 0x14 bytes after
each table base (five header words come first), so F-129's 16-byte
comparisons covered header words, not pointers. Stored slots are
`0x1204d294` and `0x1204d454`; initialized RAM slots are `0xc18cb600` and
`0xc18cb7c0`. Both blocks hold four pointers into the `0x11c9a5fc` template
table in F-110's order (JPG, NEF, NDF, TIF). Redone anchor search (84 and
260 bytes) with Thumb literal-load tracing finds exactly four word loads of
first-table slots, all in one selector getter at `0x10354350` (loads at
`0x10354366`, `0x1035436a`, `0x1035436e`, `0x10354372`): selector 0/1/2/3
returns slot 0/1/3/2. No second-table slot load exists. Observed static
decode, 2026-10-17, high confidence for those loads and the offset
correction. No firmware change, simulator use or camera access.
[Method and limits](lane2-filename-trace.md).

F-152. The getter `0x10354350` has no static reference anywhere in the image:
no Thumb `bl`/`blx`/`b.w`, short or conditional `b`, ARM branch, raw function
pointer (either Thumb bit) or `movw`/`movt` construction; the scanner was
validated on a known getter with 498 call sites and its adjacent neighbours
all have callers. Neither filename table has a located consumer that reaches
file creation or RAW/JPEG serialization. Verdict: not found. Observed static
scan, 2026-10-17, high confidence that no direct reference exists, unknown
for indirect calls or a block-copy reader. Hardware remains NO-GO. Next step
and limits: [lane2-filename-trace.md](lane2-filename-trace.md).

F-153. Lane 3 family-level search for property `0x2021`'s consumer: no
generic dispatcher compares only the high byte (`0x20`) of an id; this
firmware tests ids by offset from a base id instead. Full detail in
[lane3-family-search.md](lane3-family-search.md).

- **Verdict: not found.** Every high-byte idiom (shift by 8, bit-field
  extract, mask `0xff00`, `tbb`/`tbh` on a high byte) produced only
  unrelated hits (text shaping at `0x105afa0e`, character compares, a
  bit-field test). A Thumb-only whole-image decode was used, so ARM
  islands (F-120) and function-pointer tables are not covered.
- **Why earlier searches saw nothing.** The known event dispatcher
  `0x1037aae2` subtracts base `0x2006` and compares the difference
  (1, `0x1a`, `0x1b`, `0x81`). It routes `0x2020` to `0x103a31a6`,
  `0x2021` to `0x103a341a`, `0x2087` to `0x103a2a9c`. The literal `0x2021`
  never appears in a compare, which explains F-116's clean negatives.
- **New fixed points found by a base-offset scan.** `0x10475d8c` is an
  allow-list check for property ids (base `0x200a`, exact members,
  accepts `0x2020`, `0x2021`, `0x2083`, `0x2087`). Its callers are the
  multi-id post wrappers `0x10475dde` and `0x10475e6a` and the single-id
  wrapper `0x10475f5e`. The single-id wrapper appears to refuse an id of
  exactly `0x2021` (hand-read flag use, not run).
- **Event `0x2021`'s handler `0x103a341a` is a poster, not a reader.** It
  switches on a sub-code byte at record offset 2 and posts property
  `0x2021` via the shared primitive `0x10475ecc`. Property `0x2021` is
  written from at least that handler and its neighbors; what reads it
  remains unfound.
- Confidence high for the dispatcher and allow-list structure (decoded and
  read by hand); medium for the single-id wrapper's refusal of `0x2021`;
  low for the absence of any other consumer (scan windows are bounded).
  Next step is the registration table behind `0x10475ecc`, not more id
  dispatchers. Method: Capstone Thumb decode of the full image after a
  SHA-256 check; no firmware bytes recorded.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.


F-154. Caller search for the filename-table getter `0x10354350`: no static
route reaches it. Route classes checked over the whole image: direct and
conditional Thumb branches, ARM branches and immediate `blx`, raw words equal
to the entry (either Thumb bit), `movw`/`movt` construction, `adr`, bounded
`tbb`/`tbh` tables, and fall-through into the entry. Every class returned
zero matches. The scanner was validated on a known getter (498 direct call
sites, matching the lane 2 note) and on neighbouring entries, which all have
callers. Verdict: not found. Observed static scan, 2026-10-17, high confidence
for direct and literal references, medium overall (computed addresses and
base-relative offset tables not modelled). Hardware remains NO-GO. Method and
limits: [getter-caller-search.md](getter-caller-search.md).

F-155. The getter `0x10354350` sits directly after a return, so nothing falls
through into it, and no table-dispatched callback holds its address. The
filename-table route is therefore a dead end for static reachability; the
lane 2 next step to check indirect calls through tables is done and came back
empty. Recommended next step: treat the filename-table route as low priority
and return to the real file-creation boundary (the card-write path) per
AGENTS.md. Observed static scan, 2026-10-17, medium confidence.

F-156. Under the owner's clarified stills-only scope, the exact private F-148
overlay passes controlled native-setting-callback rendering: target/DX/target/
16:9 yield 214/0/214/0 full-width black rows. Outside the known animation band,
target differences are confined to mask rows and non-target frames match the
baseline. Ten target/DX setting cycles preserve bounds and screen-stack count;
final DX clears the mask. Two candidate native menu-confirmation attempts did
not return; one fresh stock control returned. Cause/rate and natural menu
return remain unproved. Observed bounded assisted simulator controls,
2026-10-17, high confidence within that scope. Original firmware and pinned
simulator unchanged; raw evidence stays private. Movie behavior unvalidated
and no longer a prerequisite for this stills-only work. Hardware NO-GO.
[Results and bounded next comparison](native-xpan-stills-controls.md).

F-157. Paired assisted menu-confirmation traces show stock/coarse returning
and exact F-148 candidate/coarse stopping on an unmodeled simulated flash
write, not timeout. Original writer-boundary registers/CPSR and ten stack
words match; choice is 1 in both. Finer candidate observations return through
the original caller: native stack count 3 skips mask drawing, guard NZCVQ is
preserved, and r0–r8/SP/return target match the working frame. Scratch LR
differs as in F-148. Mixed completion with different breakpoint sets does
not identify a cause or certify menu acceptance. Earlier F-156 candidate
nonreturns share this stop PC and were also not timeouts. Observed bounded
assisted simulator traces, 2026-10-17, high confidence within that scope.
No overlay/code change; original firmware and pinned QEMU unchanged. Raw
evidence stays private; all sessions closed; camera untouched, hardware NO-GO.
[Boundaries, limits and writer-path control](native-xpan-menu-boundaries.md).

F-158. One owner-approved writer-disabled control omits only writer-branch
redirection, retaining the eleven other exact F-148 overlays and nine coarse
candidate observation points. Original writer loading and retained hashes
pass. Confirmation still stops at the same unmodeled simulated flash access,
PC `0xc2b1065c`, without timeout. Writer-boundary registers/CPSR and ten stack
words match stock; choice 1, mask 0, stack count 3. Post-confirmation live
activation and bars check are not reached. Writer redirection is not necessary
for this observed stop; removal is not an established fix. Observed one
bounded assisted-simulator control, 2026-10-17, high confidence within that
scope. No other control or patch change; firmware/QEMU unchanged, session
closed, raw evidence private. Menu acceptance remains open; hardware NO-GO.
[Control identity, comparison and decision](native-xpan-menu-boundaries.md).

F-159. Bounded original-code decode and the retained F-157/F-158 stop LR
identify a cached flash identity/geometry initializer as the stopped command
helper's immediate caller. Information, erase and program wrappers share
that initializer. The outer caller is not captured, so this is not evidence
identifying installation, setting persistence or patch corruption. Later
identity/geometry reads and the initialized flag are static observations,
not completed execution. Observed read-only landmarks and existing contexts,
2026-10-17, high confidence within that scope. No new simulator run, overlay,
firmware modification or hardware access. Keep menu acceptance open; retire
further simulator flash-response explanation work.
[Provenance, limits and next build task](native-xpan-menu-boundaries.md).

F-160. Four paired stock/exact-F-148 diagnostic cases cover target/DX with
live-ready and phase-3 notification wrappers; all eight calls return. Native
inputs, known registered callback inputs, r4–r11, aligned helper SPs,
balanced return SP, caller-stack words and full return CPSR pass. Ready's
original r0 result is preserved. Measured volatile return differences are
overwritten by the named native continuations before use. The reviewed
callback builds its own outgoing stack arguments; these normal-call frames
do not replace F-145's exact state-kernel stack contract. Observed bounded
static review and assisted QEMU diagnostics, 2026-10-17, high confidence
within that scope. No patch change; global condition 3 and natural menu
acceptance remain open. Original/QEMU unchanged, both sessions closed,
raw evidence private, camera untouched.
[Contracts, differences and acceptance limits](native-xpan-close-ready-contracts.md).

F-161. A new private bounded instruction evaluator matches original EG SHA-1
compression arithmetic to hashlib on twelve synthetic message lengths and
matches the native eight-byte suffix-loop arithmetic to its closed form on
1,024 synthetic cases. Standard initialization/padding are supplied by the
helper; native config parsing/update/finalization are not executed. No seed
or suffix is recovered and the original package digest remains unverified.
A new public read-only verifier requires a supplied eight-byte suffix and
checks original before candidate; seven synthetic tests pass, 130 total.
Observed offline arithmetic comparisons, 2026-10-17, high confidence within
that bounded scope; not whole-updater emulation or package acceptance.
No firmware output, simulator boot, hardware access or readiness waiver.
[Method, limits and private reproduction](native-digest-arithmetic-verification.md).

F-127. Lane 0's ordered check finds the live-view task is created and
runs after the existing assisted live-view setup. A reset-time trace at
native task wrapper `0x10219876` observes 249 creation requests without
the 256-hit cap, including APPLV, APPMENU and APP_OBS. Their allocated
kernel records are present before diagnostic setup. APPLV's object
`0xc1821d44` holds worker pointer `0x102f2ca9` at `+0x40`, called by
the generic screen task. This identifies the live-view worker; it does
not identify whichever task produces property events `0x2006`/`0x2087`.

After `liveview_session.start` returns, a 40.005-second passive window
observes payload builder `0x102f2ad2` 196 times, all with return link
`0x102f2cdd`, APPLV stack pointer `0xc56e2ff0` and incoming flags 4.
No diagnostic call is in flight, and no observation cap is reached.
No bit-16 enter dispatch, live-view-ready routine, `0x10459d80`, property
state-machine step, `0x2087` handler or shared post primitive is observed.
A separate 40.004-second window armed only the rare trigger addresses;
it has zero observations and advances the model's counter by about
189.959 virtual seconds, without breakpoint interruptions before timeout.

Thus F-019/F-117's earlier negatives do not establish a globally dormant
scheduler. The native live-view worker demonstrably runs; the missing
event or prerequisite remains open. Step 3's general scheduler/MMIO-stall
investigation was not entered and no QEMU source was changed. Source
inspection also distinguishes the actual `nikon-z30-display` machine
(display file's recovery/platform setup and GICv1 hypothesis) from the
separate assisted machine in `nikon-z30.c`.

High confidence for positive creation/execution observations; bounded
negative for the named triggers, unknown property-producer task identity.
Original firmware hash, pinned simulator source/binary manifest and clean
checkout were checked before and after the successful runtime tests. All
raw evidence and new private helper stay under WORK. Hardware remains
NO-GO; no lifecycle acceptance, recovery-risk acceptance, or build-gate
conditions 2 through 4 are established by this fact. Details and private
reproduction: [native-worker-scheduling.md](native-worker-scheduling.md).

F-162. The scoped area-4/large/mode-0 geometry descriptor's rectangle bounds
`(8,8,5208,1928)` represent exactly 5200 by 1920, not a 5208 by 1928 output.
Original arithmetic instructions read dimensions from group 3/index 19,
margin from group 5/index 29 and inset from group 6/index 34. Indices 4/14
alone do not supply the rectangle dimensions, explaining the later negative
joint probes. Native lookup/initializer mapping, arithmetic evaluation,
256 synthetic cases and both preserved original full-builder probe reports
agree. Origin is separately read; with the recorded area/origin the crop is
centered in the parent. Observed bounded static analysis and prior-evidence
recheck, 2026-10-17, high confidence within the large normal-context scope.
Not a complete edit manifest, all-sizes contract or saved-file validation.
No new simulator, firmware image/encoding, tracking or hardware work.
[Exact field mapping, correction and limits](native-xpan-5200-contract.md).

F-163. The native standalone-EG route does not enter the unresolved outer-
package digest branch. Its discovery row is type 2; selector `0x101cf8cc`
returns the encoded-header flag only for discovery type 4, so caller
`0x10234440` sends type 2 to `0x101ce324` for native file-CRC validation.
Successful execution type 3 then removes the two CRC trailer bytes from the
updater length and reaches shared updater `0x101ce89e`. The digest branch at
`0x101ce518` remains applicable to the encoded body-package path. Observed
through bounded static decode of the verified original, 2026-10-17, high
confidence for branch selection; no updater execution or camera acceptance.
Parser capacity, compatibility/version semantics and complete XPan edits
remain open. [Route and build contract](native-standalone-eg-route.md).

F-164. Bounded static decode of the verified original resolves area-4 crop
selection for the normal builder context: the crop-dimension, margin and
inset helper families select pair indices 0/3/5 for large/medium/small. This
supports a consistent proposed 65:24 output set of 5200×1920, 3900×1440 and
2600×960; the known margins produce the previously checked large bounds and
candidate centered medium/small rectangles. Independent arithmetic and
pointer-table checks pass, but the full native builder was not rerun. The
capture small/large preview getters use a distinct capture-size selector;
the pinned upstream C 1.20 investigation identifies separate direct-buffer
constructors that bypass them and a fixed 160×120 thumbnail path. These
preview hooks and their ABI are not yet validated for area 4. Observed static
decode and synthetic arithmetic, 2026-10-17, high confidence in selector
indices and arithmetic within the inspected context; medium for the complete
feature edit set. No candidate, firmware write, simulator or camera access.
[All-size geometry and preview contract](native-xpan-all-sizes-preview-contract.md).

F-165. A fresh pinned-QEMU full native crop-builder comparison validates the
proposed area-4 large/medium/small descriptors using temporary synthetic guest
RAM records. The builder returns the 5200×1920 large rectangle from bounds
(8,8)–(5208,1928), the 3900×1440 medium rectangle, and the 2600×960 small
rectangle; the large output's endpoint fields are not its width/height. The
baseline descriptors were also captured for all three size selectors. Guest
records and pointer slots were restored in `finally`; verified original
firmware SHA-256 and the pinned QEMU checkout hash/status match before and
after. Observed bounded assisted-simulator diagnostics, 2026-10-17, high
confidence for this native builder path and data set only. This does not test
capture, preview buffers, natural lifecycle, label edits, parser acceptance,
artifact integrity or camera behavior. No firmware file was modified and no
camera accessed. Raw evidence and output remain private.
[Method, complete descriptors and limits](native-xpan-all-sizes-preview-contract.md).

F-166. A read-only startup of the pinned stock QEMU image reads the native
standalone parser's initialized capacity as `0x2940000` bytes, equal to the
upstream C 1.20 platform constant. The verified original EG is 33,939,514
bytes, below this bound; a same-length candidate preserves the size
precondition. Static parser decode shows the four-byte compatibility field
at file offset `0x10` is compared with the currently loaded module's field at
the same offset, so the patch must preserve it exactly. The eight metadata
bytes at file offset `0x24` are parsed for execution type 3, but their later
version-policy consumer is still open. Observed native configuration read and
static decode, 2026-10-17, high confidence for capacity and direct comparison
semantics only. No firmware writes, simulator source changes, updater
execution, or camera access. Raw bytes and reports remain private.
[Route, value sources and unresolved metadata policy](native-standalone-eg-route.md).

F-167. The English 1:1 menu label (string 1454) is 13 UTF-16 code units.
The proposed `65:24  (24x9)` label is also 13 code units, so this one in-place
replacement does not shift packed-string offsets. The neighboring displayed
size lines are separate entries and are not yet mapped to all three XPan
output sizes; do not treat the label fit as a complete menu-text edit. Observed
read-only decode of the verified original and length arithmetic, 2026-10-17,
high confidence for the English label only. No firmware change, candidate or
camera access. [Label and remaining text work](xpan-build-decision.md).

F-168. A hash-verified whole-image Thumb-2 `BL` sweep finds 16 direct calls
to the four preview getter families. They span image-record builders, a
generic dispatcher, display sizing and other contexts; a global getter-table
change would affect unrelated callers. At `0x1038face`, the caller reads
capture selector `+0x226`, separately forms the area record at `+0x208`, and
subsequently uses that record when scaling preview output. The builder at
`0x1014319e` has four getter sites and reads both fields elsewhere in its
body, but branch-local guard availability is not established. These are
candidate tracing points, not accepted hooks. Observed static decode of the
verified original, 2026-10-17, high confidence for the listed direct
references and local field accesses only; indirect calls, parent call chains,
buffer capacity, natural capture behavior and ABI remain open. No firmware or
simulator changes and no camera access. [Caller map and next checks](native-xpan-preview-callers.md).

F-169. Cross-checking the verified original's preview tables corrects the
area-4 preview target. Getter backing lists at `0x115a4cfc` and `0x115a4d10`
select five area slots; slot 4 is 480×480 small preview and 1080×1080 large
preview, with 120×120 in the separate thumbnail-size list. Independent direct
buffer tables at `0x1157223c` and `0x11572264` have the same slot-4 dimensions;
the adjacent row strides are 960 and 2160. Fitting the exact 5200×1920 XPan
large still into the slot-4 width limits and rounding height to nearest four
pixels yields candidate previews 480×176 and 1080×400. The upstream 640×236 /
1920×708 values belong to its area-2 design and must not be copied. Its
investigation identifies three direct buffer constructors (`0x10142d86`,
`0x1014376e`, `0x101464c4`) and five hook sites; local Thumb disassembly
confirms the sites lie in those native constructors. These sites and dimensions
are leads only: no area-4 hook ABI, allocation, output-structure or playback
contract has been executed. Observed static table values and local instruction
cross-check, 2026-10-17, high confidence in values/locations, medium in their
behavioral role. No firmware change, simulator run, camera access or candidate.
[Tables, address map and next checks](native-xpan-preview-callers.md).

F-170. Three native direct-buffer constructors were executed in pinned QEMU
with synthetic guest records. In constructors `0x1014376e` and `0x10142d86`,
the slot-4 output fields followed synthetic large-preview `1080×400` and
small-preview `480×176` dimensions; their size-related output fields changed
accordingly. Constructor `0x101464c4` also returned with those synthetic
dimension pairs from a nested slot-4 record, while its fixed thumbnail fields
remained 160×120; its area guard was not established. A
control call to `0x10142d86` with area 0 while the shared guest table was
changed showed that table mutation also alters non-target output. Therefore
the values are viable constructor inputs, but a capture/area-4-scoped shadow
table or equivalent guarded hook is required; global table edits are unsafe.
All guest table entries and scratch records were restored, original firmware
identity and pinned QEMU checkout were unchanged. Observed bounded synthetic
constructor calls, 2026-10-17, high confidence for the fields exercised;
allocation capacity, per-hook ABI/guards, real capture and preview pixels
remain unverified. No candidate or camera access.
[Constructor map and test limits](native-xpan-preview-callers.md).

F-171. A verified-original Thumb `BL` sweep finds the direct buffer wrapper
`0x10142f5e` called from `0x1009f8c6`, `0x100a356a`, and `0x100a579c`.
`0x1009f8c6` lies in a creator that selects a preview slot from an input
dimension; the other two lie in object-rebuild paths that pass the current
record at `+0x3a4`. These are shared record-construction contexts, not proven
capture-only routes. The constructor's area-4 field check therefore cannot
by itself establish a safe hook; exact caller/capture discrimination and
old-photo behavior must be demonstrated before patching. Observed bounded
static callsite scan and local caller decode, 2026-10-17, high confidence for
the direct references, unknown for indirect callers and full semantic role.
No candidate, simulator mutation, or camera access.
[Caller map and limits](native-xpan-preview-callers.md).

F-172. A hash-gated zero-span audit rejects treating the entire
`0x1002d884–0x10030006` run as free code space: direct pointer values from
elsewhere in the EG target 110 distinct addresses within that run. A smaller
aligned all-zero subspan, `0x1002d996–0x1002e000` (1,642 bytes), has no direct
pointer hits, no whole-image Thumb branch targets from the bounded decoder,
and no detected Thumb MOVW/MOVT address pair. This makes it a candidate for
further code-space review, not an approved cave: base-register address
construction, linker/section boundaries, and executable mapping have not
been closed. Observed static byte/reference scans of the verified original,
2026-10-17, high confidence for the checked direct references and zero span;
medium or lower for all possible indirect/computed uses. No firmware or
simulator changes and no candidate.
[Preview/build architecture](native-xpan-build-architecture.md).

F-173. A hash-verified direct Thumb `BL` trace follows the preview-constructor
wrappers upward. Wrapper `0x10143862` has a direct caller at `0x1021e7a8`;
wrapper `0x1014389c` is called at `0x100a0b9c` in an existing-record object
construction path; and wrapper `0x101465e8` for direct constructor
`0x101464c4` is called at `0x1009ece0` after an object-type check (`+0x0d ==
0x24`) and a non-null-field check (`+0x144`). These remain generic
object/record construction contexts; none is proved to mean new-still capture
or to exclude playback/rebuild. Caller-level capture scoping remains open.
Observed bounded static decode and full-image direct-call sweep of the
verified original, 2026-10-17, high confidence for direct references and local
data flow only. No patch, candidate or camera access.
[Preview caller map](native-xpan-preview-callers.md).

F-174. Instruction-width review identifies candidate four-byte patch windows
near the five direct-buffer hook sites at `0x10142de4`, `0x10142e42`,
`0x101437a0`, `0x10146518`, and `0x10146550`. Each spans complete Thumb
instructions. Branch arithmetic puts each window within about 1.1 MiB of the
candidate zero subspan at `0x1002d996`, inside Thumb-2 `BL` reach; the native EG
tail is about 31.9 MiB away and needs an intermediate veneer. A synthetic
LLVM assembly check confirms an eight-byte `LDR.W PC` literal veneer can
transfer to a Thumb-tagged appended stub without clobbering a general
register. This proves only encoding geometry: cave executable mapping,
exhaustive address-use, displaced-instruction behavior, hook ABI and capture
guard remain open. Observed bounded original-instruction decode plus synthetic
assembly/address arithmetic, 2026-10-17, high confidence for instruction
widths and branch ranges only. No original bytes changed or candidate built.
[Build and hook layout](native-xpan-build-architecture.md).

F-175. Address arithmetic for a bounded code append places the start of code
inserted immediately before the verified original's two-byte CRC at
`0x1207e038` (Thumb pointer `0x1207e039`). The native parser's `0x2940000`-byte
installation span from `0x10020000` ends at `0x12960000`; the original payload
leaves 9,314,248 bytes of modeled `0xFF` padding, so a small append stays under
the known capacity. This supports payload-size and branch-distance planning
only; it does not prove that the appended range is executable or camera
accepted. Observed arithmetic over F-142/F-166 values, 2026-10-17, high
confidence for the numeric bounds. No firmware bytes changed or candidate
built. [Build architecture](native-xpan-build-architecture.md).

F-176. Against the SHA-256-pinned original EG, the three 36-entry language
tables provide indexed UTF-16 spans for the existing 1:1 label and its L/M/S
size strings (IDs 1454, 1456–1458). A private text-only manifest records 144
non-overlapping edits across all languages, each using the same byte length
as its source span; bounds, UTF-16 alignment, replacement fit and source hash
were checked. The plan contains firmware-derived spans and remains in
owner-only storage outside the repository. This closes string-span mapping
and exact-length fit only; translated display semantics, preview hooks,
metadata policy and all other edits remain open. No candidate or camera
access. [Build architecture](native-xpan-build-architecture.md).

F-177. Local disassembly of the `0x10143862` caller at `0x1021e7a8` places it
inside the routine beginning at `0x1021e3f4`. That routine obtains and
initializes/reuses record-linked objects, creates a preview object when a
nested object field is empty, stores the returned object into the parent, and
continues object attachment/state handling. This is an existing-object
lifecycle path, not evidence of a new-still capture boundary; do not use this
call site as the capture discriminator. A whole-image direct-branch check
found no direct call to the enclosing entry; computed/indirect dispatch is
not resolved. Observed bounded static disassembly of the verified original,
2026-10-17, high confidence for local operations and branch edges, unknown
for indirect entry/caller semantics. No firmware or camera access.
[Preview caller map](native-xpan-preview-callers.md).

F-178. A hash-pinned offline composition combines the F-176 text spans with
the mapped area-4 origin, padded extent, L/M/S outputs, crop dimensions,
margins and insets into a private 160-span exact data manifest. Each span has
expected/replacement bytes and hashes; 144 localized UTF-16 spans and 16
two-byte geometry spans are non-overlapping. Source identity and all expected
bytes were rechecked, and applying the manifest to memory preserved the
original length. This is a proposed data-only edit set, not a candidate; the
preview hooks, bars payload, metadata policy, native CRC and complete
out-of-manifest audit remain open. The manifest remains in owner-only storage
outside the repository. Observed offline manifest build
and read-back, 2026-10-17, high confidence for span/hash/non-overlap checks;
medium for downstream correctness of proposed geometry values. No firmware
output or camera access. [Build architecture](native-xpan-build-architecture.md).

F-179. Whole-module reference sweeps found no Thumb PC-relative literal/ADR
reference or ARM PC-relative literal/ADR reference into the inspected object
constructor table regions around `0x1200d000`, `0x1200ddb8` and
`0x1200e480`; no whole-image MOVW/MOVT pair formed those candidate addresses.
The type-`0x24` constructor pointer itself occurs in a data entry, but the
entry's registration/dispatch source is still unresolved. These bounded
negative scans do not rule out base-relative or runtime-populated references.
Observed hash-pinned offline scans of the verified original, 2026-10-17,
high confidence for the tested reference forms only. No firmware output or
camera access. [Preview caller map](native-xpan-preview-callers.md).

F-180. A hash-pinned Thumb-2 call sweep finds the area-4 preview-record helper
`0x1014319e` called from `0x10143708` inside native constructor `0x101436c2`.
That constructor is reached at `0x100a42d8` when an object's `+0x320` record
is absent, and at `0x101eccb0` while an existing object is being refreshed;
the latter route also checks object state before filling the missing record.
Both routes materialize records from current object state, and neither proves
a new-still capture boundary. The helper reads the area and preview selector,
but those fields alone are not a capture discriminator. This rejects the
builder as an approved hook pending a capture-origin proof. Observed bounded
static decode and whole-image halfword-aligned `BL` sweep of the verified
original, 2026-10-17, high confidence for the call edges and local field flow;
unknown for the indirect dispatch and lifecycle semantics. No candidate or
camera access. [Preview caller map](native-xpan-preview-callers.md).

F-181. The verified original standalone EG's stored big-endian two-byte
trailer equals CRC-16/XMODEM (polynomial 0x1021, initial value 0) over all
preceding bytes, and processing the complete file yields zero residue. A new
standard-library-only in-memory composer/auditor implements that trailer rule,
same-length exact spans, optional payload insertion immediately before the
trailer, protected fields at offsets 0x10 and 0x24, capacity bounds, and a
full unchanged-region audit. Ten synthetic tests pass; no real firmware was
passed to the composer and no candidate was emitted. The actual verified
original was read only for the CRC comparison. Observed offline calculation,
2026-10-17, high confidence for this original and CRC convention; no camera
access or artifact. [Composer API](../src/nikon_z30_research/standalone_eg.py)
and [architecture](native-xpan-build-architecture.md).

F-182. The new composer/auditor was exercised in memory against the exact
hash-verified original and private F-178 160-span text/geometry manifest. It
accepted all 160 same-length spans, preserved the original file length,
recomputed a valid native CRC, and reported 2,286 changed bytes under its
accounting. The manifest remains explicitly data-only/incomplete; the output
was discarded and no candidate file was written. This confirms the tool can
apply the current exact data plan to the pinned input, not that the feature
edits are semantically complete or camera-accepted. Observed bounded offline
composition and read-back audit, 2026-10-17, high confidence for span/hash/
length/CRC checks; no simulator or camera access. [Build architecture](native-xpan-build-architecture.md).

F-183. The in-memory standalone-EG composer now exposes a parser for a
private exact-span manifest and refuses plans not explicitly marked
`COMPLETE_REVIEWED_PLAN`, not bound to the pinned Z 30 EG identity/load base,
or with malformed span hashes, offsets, lengths, or append-payload identity.
The composer then independently checks source CRC/identity, ordered spans,
protected header ranges, capacity and every unplanned output region. Fourteen
synthetic tests cover the parser and composer; the status marker is a caller
assertion, not evidence that the plan has passed engineering review. No
complete plan or firmware candidate exists. Observed standard-library unit
tests, 2026-10-17, high confidence for rejection behavior on the fixtures;
no camera or candidate use. [Composer](../src/nikon_z30_research/standalone_eg.py).

F-184. Local review of the dimension-based preview-slot adapter at
`0x1009f884` finds it selects a preview slot from input dimensions, creates a
preview object, and attaches the result to a parent object. The direct wrapper
call at `0x1009f8c6` reaches the already-known shared buffer constructor. A
whole-image direct Thumb `BL` scan and raw pointer-word scan found no direct
entry reference to the adapter; indirect dispatch and its upstream event
source remain unresolved. This is a preview-object construction route, not a
proven still-capture guard and not an approved hook. Observed bounded
static review of the verified original, 2026-10-17, high confidence for the
local dimension-selection and attachment behavior; unknown for its dispatch
and capture provenance. No candidate or camera access.
[Preview caller map](native-xpan-preview-callers.md).

F-185. A private standalone-EG file writer now requires a caller-supplied
SHA-256 for the reviewed manifest, invokes the exact-original gate before
composition, rejects project-repository paths and existing output files,
checks the native parser capacity, and reopens/audits the written result.
If the read-back audit fails, it removes only the output file it created.
Four filesystem tests use synthetic EG fixtures; the complete suite passes
148 tests. The manifest digest is a caller assertion, not proof that someone
reviewed the plan. The writer has not been run on the real original or a
feature manifest, and no candidate exists. Observed synthetic unit tests,
2026-10-17, high confidence for the tested filesystem and refusal behavior;
no camera access. [Private builder](../src/nikon_z30_research/private_eg_builder.py).

F-186. The private candidate writer creates output with mode `0600`
(owner read/write only) after exclusive creation, and a synthetic filesystem
test verifies that mode. This limits accidental exposure of any future local
candidate; it does not change candidate readiness. No real firmware or
candidate was written. Observed local unit test on the current filesystem,
2026-10-17, high confidence for the tested mode and write path. [Private
builder](../src/nikon_z30_research/private_eg_builder.py).

F-187. The private writer was run against the exact verified original and
the current private 160-span data-only manifest using a fresh private output
path. The original-identity gate passed, the manifest's incomplete status
was rejected, and the output path remained absent. This is a real-input
fail-closed build-gate check only: it does not produce or validate an XPan
candidate. Observed local builder invocation, 2026-10-17, high confidence
for exact source identity and incomplete-plan refusal; no camera access.
[Build architecture](native-xpan-build-architecture.md).

F-188. Read-only inspection confirms that the eight-byte field at standalone
EG offset `0x24` is printable, version-like text in the verified original.
The parser passes it through formatter `0x101d3f14`; after CRC validation,
the checker dispatches through selector-based policy callbacks, some of which
also call that formatter. This locates metadata formatting after integrity
validation but does not prove whether the field is compared
against the installed version or only displayed. Preserve all eight bytes;
the exact callback selected for the standalone route remains to be mapped.
Observed bounded static decode and in-memory byte classification,
2026-10-17, high confidence for text shape and call flow only. No candidate
or camera access. [Standalone route](native-standalone-eg-route.md).

F-189. The exact private F-148 bars overlay was merged with F-178's
text/geometry plan after verifying the pinned original identity, all 12
before-span hashes, all 12 replacement-file hashes, and non-overlap with the
160 existing edits. The resulting private manifest has 172 exact spans. The
composer audited an in-memory result against the verified original; length
and native CRC passed, with 2,456 changed bytes under its accounting. The
temporary candidate bytes were discarded. The manifest remains explicitly
incomplete because preview hooks/capture provenance and metadata callback
semantics are unresolved. The manifest remains in owner-only storage outside
the repository, with owner-only permissions.
Observed offline manifest merge and full composer audit, 2026-10-17, high
confidence for source/span/hash/non-overlap/length/CRC checks; no simulator or
camera access. [Build architecture](native-xpan-build-architecture.md).

F-190. A one-time passive read of the pinned QEMU 10.2.4 runtime selector
returned zero at `0xc259c8e4`; the statically decoded selector subtracts six,
then takes the out-of-range fallback for this value. The run booted the exact
verified local original and did not call firmware functions or write guest
memory. This is only the incomplete simulator's startup state, not evidence
of the camera's selected version-policy callback. Do not continue probing
this simulator state; trace the native dataflow or leave the metadata
semantics unresolved. Observed, 2026-10-17, high confidence for this single
QEMU read and low relevance to camera behavior. No camera access.

F-191. The current public Wonder Lantern Z30 C 1.20 source documents a
65:24 aspect profile with native still-size selection, capture-specific
embedded-preview dimensions, and a custom area-2 workflow; it reports user
camera validation. Its profile uses L/M/S dimensions 5568×2056,
4176×1544, and 2784×1024 and keeps the fixed 160×120 thumbnail unchanged.
This is a concrete same-model/same-firmware implementation to evaluate as a
baseline for our testable patch, rather than continuing to invent the
unresolved area-4 preview hooks. It does not supply our separate black-bars
overlay, prove our existing F-148 integration, or establish our lifecycle
gate. Source claims and dimensions observed in public project documentation,
2026-10-17; not independently reproduced by this project and not a camera
authorization. [Aspect profile](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/aspect-profiles.md),
[build contract](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/build.md).

F-192. Comparison with the requested feature contract shows the public
65:24 profile is not a drop-in candidate: it selects area 2 through a
multi-profile persistent setting and uses a native grid reference; our
candidate replaces the stored 1:1 choice in area 4 and has a separate
black-bars overlay. The upstream source is useful as a same-firmware
reference for capture-specific preview handling and profile isolation, but
does not satisfy the requested menu/area/overlay behavior. Preserve the
area-4 plan and do not substitute the different behavior to make a candidate
easier. Observed documentation and project-contract comparison, 2026-10-17,
high confidence for the stated behavior difference. No code or camera access.
[Preview comparison](native-xpan-preview-callers.md),
[build architecture](native-xpan-build-architecture.md).

F-193. At the pinned same-firmware source commit, the upstream 65:24
implementation has explicit return-address allowlists for its small/large
preview-getter hooks. The 7 small and 5 large callsites overlap our local
capture-record builder/scaler inventory and omit two known display/scaling
callers. Its verifier executes the listed callers and one excluded caller,
checking stock pointer/value fallback and callee-saved registers across
profiles, areas and indices. This provides a concrete method and candidate
allowlist for our generic getter hooks, but its area-2/profile-index-1 guard
does not transfer to area 4 without exact index/ABI validation. Its separate
direct-buffer hook checks profile plus area but not the outer caller; our
constructor has known rebuild callers, so this does not close direct-buffer
provenance. Observed in pinned public source commit
`f6630588810f6ecb9363bc7881fccb47e4fdb87b`, 2026-10-17; no local firmware
execution, candidate or camera access. [Cross-check](native-xpan-preview-callers.md).

F-194. Static decode of the verified local original shows wrapper
`0x10142f5e` saves its caller LR in a 16-byte frame, then calls constructor
`0x10142d86`; the constructor pushes 24 bytes before its direct-table hook at
`0x10142de4`. At that hook, the wrapper's original caller LR is recoverable
at `[sp,#36]`, enabling a caller-specific direct-buffer guard without a
global one-shot flag. The three known wrapper callers are the dimension-based
creator at `0x1009f8c6` and two existing-object rebuild paths
(`0x100a356a`, `0x100a579c`). This suggests a testable hook mechanism but
does not establish any caller as new-still-only; a full synthetic wrapper-to-
constructor run must verify the stack contract, and the first caller's
upstream indirect dispatch/provenance remains open. Observed bounded decode,
2026-10-17, high confidence for frame arithmetic from instructions; no code
change or camera access. [Preview caller map](native-xpan-preview-callers.md).

F-195. Bounded disassembly of `0x1009f884` shows a dimension-based
preview-object factory: it reads input width at `+0x0a`, selects a preview
choice, writes it to record `+0x226`, allocates a resource, calls the shared
constructor wrapper, and attaches the result to a parent object at `+0x28`.
There is no local still-capture predicate, area-4 check, or capture-origin
read. The then-reported negative whole-image reference sweep was incomplete:
F-196 finds two direct calls to this factory from `0x1021d946`. This still
disqualifies the factory itself as a capture hook; its callers and input
records need provenance review. Observed read-only disassembly of the exact
verified original, 2026-10-17; no code change or camera access.
[Preview caller map](native-xpan-preview-callers.md).

F-196. A hash-verified Thumb `BL` sweep finds two calls to the
dimension-based preview factory `0x1009f884`, at `0x1021d952` and
`0x1021d994`, both within helper `0x1021d946`. A further whole-image direct
call sweep finds one caller of that helper at `0x1021da84`, reached from
dispatcher `0x1021d9e2` only when input flag bit 20 is set. The helper obtains
current object/record state, builds preview objects, attaches one at parent
`+0x28`, then clears state and invokes an indirect continuation. This gives
a concrete event-dispatch route to trace, but does not identify bit 20 as a
new-still event or prove either input record is capture-only. No direct Thumb
`BL` to the dispatcher was found; one aligned word at `0x1021dd08` contains
its Thumb pointer, suggesting table-based dispatch whose registration/use
remains unknown. Trace that table use and the producer/meaning of the flag;
preserve the generic route unless capture provenance is established. The
earlier F-184/F-195 negative direct reference claim is corrected. Observed
bounded decode and complete direct
Thumb-call sweep of the verified original, 2026-10-17, high confidence for
direct call edges and local flag/data flow; event meaning remains unknown.
No candidate or camera access. [Preview caller map](native-xpan-preview-callers.md).

F-197. Static review of initializer `0x1021dac2` shows it constructs callback
registration records using identifiers from the adjacent static table, loads
the Thumb callback pointer `0x1021d9e3` at `0x1021db04`, and passes the
record through shared registration routine `0x10199cae`. That routine builds
a callback object and delegates to common service code. The identifier lookup
and service semantics are not yet mapped, so this establishes a registered
event-callback route, not the event's meaning. The callback's bit-20 branch
still lacks evidence tying it to a new still. Next resolve the registration
identifier into its producer/consumer and trace where the callback flags and
current object originate. Observed bounded static disassembly of the verified
original, 2026-10-17, high confidence for local calls and data flow; event
semantics and capture provenance remain unknown. No candidate or camera
access. [Preview caller map](native-xpan-preview-callers.md).

F-198. The owner's current XPan still-photo-guard waiver accepts that
area-4 preview dimensions may also affect movie, playback or warning
contexts. This removes capture-caller provenance as a prerequisite for the
offline candidate, while lifecycle condition 1 remains unmet and hardware
approval remains separate. A private complete 176-span manifest combines
144 localized UTF-16 text edits, 16 area-4 geometry edits, 12 F-148 bars
edits, and four area-4 preview-table edits. Only slot 4 changes in the getter
and direct-buffer tables: 480x480 becomes 480x176 and 1080x1080 becomes
1080x400; other slots, row strides, thumbnail, and protected fields remain
unchanged. The private builder produced a 33,939,514-byte standalone-EG
candidate from the verified source. Its SHA-256 is
`6614df3aa5d8b8b223953db7eb680ff04684ddac6730cc98397e907c2cadb6a1`; the
manifest SHA-256 is
`32de8d4d87ac2bb41ea0d450b647f23e15346dfd58712fc9c2fad34ca656374a`.
Independent checks confirmed exact listed edits, no unplanned byte changes
outside the regenerated two-byte CRC trailer, unchanged source length,
protected offsets 0x10/0x24, native CRC residue, parser-capacity fit, mode
0600, unchanged non-target slots/strides, and the four intended preview
values. Candidate and manifest remain in owner-only storage outside the
repository; neither is in Git.
F-170 previously executed the native preview constructors synthetically with
the same dimensions, but the modified file has not been exercised by camera
hardware or accepted by a native updater. Observed local builder plus
independent read-back audit, 2026-10-17, high confidence for byte/layout/CRC
properties; camera acceptance and residual UI behavior remain unverified.
No camera access or write. [Build architecture](native-xpan-build-architecture.md).

F-199. Re-opened the known verified C 1.20 EG, private F-198 candidate and
private 176-span manifest. The original identity gate, complete-manifest
parser, manifest hashes, exact-span composition, independent full-file audit,
native CRC/residue, file length/capacity and artifact permissions passed
again. A separate layout check confirmed slots 0–3 remain unchanged in both
getter tables and both direct-buffer dimension tables; slot 4 is 480×176 and
1080×400 in each; both five-entry row-stride tables are byte-identical with
slot-4 strides 960/2160. Candidate SHA-256 remains
`6614df3aa5d8b8b223953db7eb680ff04684ddac6730cc98397e907c2cadb6a1`, manifest
SHA-256 remains `32de8d4d87ac2bb41ea0d450b647f23e15346dfd58712fc9c2fad34ca656374a`.
This is offline byte/layout verification only; it does not establish Nikon
updater acceptance, lifecycle coverage or camera behavior. No camera access
or write. [Current handoff](handoff-codex.md).

F-200. A bounded attempt to run the exact private F-198 candidate through the
existing pinned QEMU found that the standard Python launcher rejects its
non-stock hash, then source inspection and a direct pinned-binary launch
confirmed that the QEMU C machine loader independently enforces the exact
stock length and SHA-256 before emulation. The launch stopped at that guard;
the simulator did not execute the candidate. The QEMU checkout and binary
remain unchanged. This is a simulator input-policy limitation, not evidence
for or against Nikon updater acceptance. Per the project priority rule, record
the dead end and stop this simulator path rather than weaken its guard or
modify the pinned simulator. The private candidate, firmware, and runtime logs
remain outside Git. Observed local verifier attempt and source review,
2026-10-17; high confidence for rejection at the launcher and C guard; no
camera access or write. [Current handoff](handoff-codex.md).

F-201. After reviewing that the shared preview/capture constructors are not
proven specific to new still-image creation, the owner explicitly reaffirmed
the existing XPan still-photo-guard waiver (“Keep the waiver.”). The current
candidate may therefore retain its area-4 preview-table edits without a
capture-origin guard, with the already-recorded possible playback, movie and
warning-context effects accepted but unmeasured. This waiver is limited to
that guard and does not waive lifecycle condition 1, native updater
acceptance, other readiness/recovery requirements, or the separate approval
required for any exact camera write. No camera access or write. Observed direct
owner disposition, 2026-10-17. [Test-readiness record](test-readiness-2026-10-17.md).

F-204. The capture-path decision remains unresolved on both proof routes. No
new-still-exclusive hook is established: wrapper `0x10142f5e` is called from
dimension-based factory `0x1009f8c6` and existing-object rebuild callers
`0x100a356a`/`0x100a579c`; constructor `0x101436c2` is reached from missing-
record construction at `0x100a42d8` and existing-object refresh at
`0x101eccb0`. The event meaning for the bit-20 dispatcher path is unknown
(F-171/F-180/F-196). No evidence proves playback/editor output is unchanged:
generic getter and object-rebuild routes share the area-4 slot-4 tables
changed by the candidate. Affected or potentially affected contexts are
intended still previews, playback/editor object construction or refresh, and
the already-waived but unmeasured movie/warning contexts. F-201 records the
owner's waiver for playback/movie/warning effects. The owner directs keeping
that waiver as scoped; editor outputs are not added to it. Editor isolation is
unproven and editor behavior must remain outside any accepted test scope.
Lifecycle condition 1 remains unmet, so hardware preflight remains blocked. No
candidate build or camera access.
[Preview caller map](native-xpan-preview-callers.md) and [test-readiness
record](test-readiness-2026-10-17.md).

F-205. The owner reopened capture-path research with the narrower requirement
that preview edits affect still capture only and leave playback/editor outputs
unchanged, specifically at wrapper call sites `0x1009f8c6`, `0x100a356a`,
`0x100a579c`, and refresh caller `0x101eccb0`. Existing hash-pinned static
findings do not provide such a gate. `0x1009f8c6` is inside a dimension-based
preview-object factory with no local capture-origin predicate (F-184/F-195);
`0x100a356a` and `0x100a579c` rebuild objects from current records (F-171);
`0x101eccb0` refreshes an existing object and fills a missing record (F-180).
The possible upstream dispatcher gate tests bit 20, but its event meaning and
record provenance are unresolved (F-196/F-197). Therefore no still-only gate
is established at these four contexts, and playback/editor exclusion is not
proved. The remaining evidence needed is a statically traced capture-origin
predicate whose producer and semantics exclude rebuild, refresh, playback and
editor contexts, plus proof that it dominates each relevant hook without
changing shared outputs. No candidate was built and no camera was accessed
for this finding. Observed review of the cited pinned-original findings,
2026-10-17; [caller map](native-xpan-preview-callers.md).

F-206. The still-only gate trace reaches a bounded static dead end using the
repository's existing caller/dispatcher records. A focused search of project
documentation found no additional decoded producer for the input flag at
`0x1021d9e2`, no mapping for the callback key registered by
`0x1021dac2` through `0x10199cae`, and no new provenance for the current
object/record consumed by `0x1021d946`. The exact unresolved edges are the
source/semantics of bit 20 and whether the current and nested records came
from a new still or an existing playback/editor/rebuild object (F-196/F-197).
The three direct wrapper call sites include two existing-object rebuilds;
the fourth named context refreshes an existing object (F-171/F-180). No
predicate is shown to dominate a still-only edit. The existing F-198
table-only artifact globally changes area-4 slot-4 dimensions and therefore
cannot meet the owner's newer requirement to leave playback/editor unchanged.
Safe continuation requires an existing owner-authorized, bytes-free static
decode of those producers and records; until then, do not build or test a
preview patch. A future implementation must prove a caller-guarded override
with stock fallback outside the new-still predicate; this is a design
constraint, not a proven hook. No firmware bytes were accessed for this
finding and no hardware was touched. [Caller map](native-xpan-preview-callers.md).

F-207. A bounded read-only decode of the verified EG shows initializer
`0x1021dac2` registers callback `0x1021d9e3` using generic registry ID
`0x1003a`. The ID lookup helper `0x10218832` indexes a 28-byte-stride runtime
registry table. In the pinned QEMU at the reviewed revision, a standard
assisted live-view startup initialized the record for `0x1003a` with the
service label `BACKEND`; one observed callback entry had input flags `0x10`.
The probe did not observe bit 20 or correlate that startup callback to a
particular fixture/API call. This identifies a generic backend registration,
not a capture-only event or producer for bit 20, and establishes no still-only
hook. Observed static lookup/registration flow and read-only initialized guest
RAM, 2026-10-17; high confidence for the key label and sampled flags, event
semantics and record provenance remain unknown. No repository firmware data,
candidate, or camera access. [Preview caller map](native-xpan-preview-callers.md).

F-208. The exact bit-20 producer edge is now decoded. Preview callback
`0x1021d9e2` tests bit 20 and calls `0x1021d946`, which reads the module's
current-object slot at state offset `+0x60`. Setter `0x10220fd6` accepts an
object pointer, fills that slot only when empty, and posts event/property
`0x100000` through `0x10199cdc`; this matches the callback's bit-20 test. A
bounded direct-Thumb-call sweep finds two direct setter callers:
`0x1015672c` supplies a pointer derived from a runtime object, and
`0x103e5d1c` supplies a stack-built descriptor from a generic backend worker
path (`0x103e5bdc`), entered from `0x103e5e88` on a queued bit-24 branch. No
still-capture predicate is present in these decoded paths; indirect callers
remain outside the direct sweep. Thus bit 20 represents first assignment of
a generic current object, not a proven new-still signal. The object origins
are not proven to exclude playback/editor, so this event is not a safe
still-only hook. Static call/data flow, verified EG, 2026-10-17; high
confidence for the local setter/event edge, medium for end-to-end callback
delivery, capture provenance unresolved. No candidate or camera access.
[Preview caller map](native-xpan-preview-callers.md).

F-209. The queued bit-24 route was followed one layer farther. Worker
`0x103e5e70` tests queue bit 24 and calls descriptor builder `0x103e5bdc`;
that builder reads shared backend state, constructs a multi-record descriptor,
and calls the same current-object setter `0x10220fd6`. Its bit-24 notifier is
`0x103e89c2`, reached through branch stub `0x1056a636` from shared helper
`0x1055f834`. A full-image direct-branch scan finds multiple callers of
`0x1055f834` across backend/state-management paths, including explicit
cleanup/invalidation paths. The helper has no capture argument or local
capture predicate. This is stronger evidence that the event is shared object
state/invalidation, not a still-only signal; it still does not prove the
origin of every descriptor or exclude playback/editor. Static Thumb trace of
the verified EG, 2026-10-17; high confidence for the call edges, medium for
semantic characterization. [Preview caller map](native-xpan-preview-callers.md).

F-210. A bounded read-only run of the pinned stock QEMU watched the bit-24
notifier, descriptor builder, current-object setter, and preview callback
during standard assisted live-view startup and four ordinary UI navigation
inputs. None fired in the observed windows. Firmware identity remained
unchanged and the QEMU checkout stayed clean. This says only that this
simulator sequence does not exercise the route; it is not evidence that the
route is unreachable on the camera and does not provide capture provenance.
Observed simulator result, 2026-10-17; high confidence for the bounded run,
no inference about real-camera reachability. No candidate or camera access.

F-211. The second direct caller of setter `0x10220fd6` is routine
`0x10156714`. It supplies a base-derived object pointer only when two shared
table counters satisfy `r1 < r0`, then proceeds through a state-indexed
descriptor walk that reads several backend values. No capture-origin test is
visible in the decoded entry. A full-image direct-BL sweep and an exact
halfword-aligned pointer-word scan found no direct caller/reference to this
entry; computed/registered dispatch remains possible. A bounded stock-QEMU
startup/navigation observation also did not hit this routine or the setter.
This leaves the routine's inbound dispatch and table semantics unresolved;
it does not prove camera unreachability or a capture-only route. Static and
simulator observation, 2026-10-17; high confidence for local conditions and
bounded absences, semantic provenance unresolved. [Preview caller map](native-xpan-preview-callers.md).

F-212. A private one-button subject-tracking hook candidate passed a bounded
constructed-context guard test in the pinned QEMU. The tested copy-hook cases
accepted only a fresh press in the intended context/mode, with the expected
worker ownership and unconsumed state; held, release, other context, other
mode, wrong owner, and consumed-state cases followed stock behavior. Both
candidate-entry cases preserved seeded registers/flags and stack geometry,
and accepted-path cleanup restored the caller stack and return state. This
test directly constructed the worker context; it did not establish natural
worker admission, prove the on-camera press-to-start/stop cycle, or execute a
complete modified firmware image. Static evidence separately identifies the
native Subject tracking action enum and a shared configurable-action route,
but action activation/cancellation semantics remain unverified. This advances
the hook ABI/guard evidence only; the candidate is not ready for a real-camera
test. Read-only pinned-QEMU test, 2026-10-18; high confidence for the
constructed guard/ABI cases, no inference about natural dispatch or camera
behavior. No firmware bytes or dumps in the repository; no camera access.

F-214. A private pinned-QEMU call-path comparison tested the candidate's
AE-L/AF-L action adapter in its constructed accepted context and the native
Fn Subject tracking handler independently. Both reached shared helper
`0x10368b6e` with the same action selector (`r0=45`); both then reached
`0x1045a47e` with the same request tuple (`r0=0x20`, `r1=1`,
`r2=0xc201685c`, `r3=1`). The candidate adapter completed with its worker
context restored. This establishes that it reuses the native Subject
tracking request path rather than inventing a second tracking state machine.
The consumer object is unmodeled in this QEMU run, so it cannot show the AF
area-mode transition or prove a real-camera toggle. The official Z 30 manual
defines the behavior contract: in Auto-area AF (including people/animal
variants), the assigned control starts tracking and pressing it again ends
tracking; it does not list AE-L/AF-L as a stock assignment for this role.
The candidate's normal worker admission and full image ABI remain unverified;
this is a native-action hook validation, not a complete testable image.
Read-only pinned-QEMU diagnostic plus official manual, 2026-10-18; high
confidence for matching call arguments, no inference about consumer
execution, worker admission, or camera behavior. No firmware bytes/dumps in
the repository and no camera access.

F-213. A separate private memory-only candidate run in the pinned QEMU reached
the standard boot checkpoint and the powered simulated live-view setup. The
candidate's worker TCB and expected allocation were present before an explicit
native object notification; that notification returned and the saved worker
stack pointer changed afterward. The bounded probes recorded no worker-entry
or cleanup hits, so this shows only that the task existed and its context
changed after notification. It does not show a natural AE-L/AF-L press
reaching the candidate hook, successful hook admission, or subject-tracking
activation/cancellation. The original firmware hash and simulator checkout
were checked by the private harness; no camera access. Read-only simulator
diagnostic, 2026-10-18; high confidence for the sampled task/notification
observations, no inference about button delivery or action semantics.

F-215. The AF-area-label/OK trace distinguishes AF-area selection from the
Z 30's Subject-tracking operation. The AF-area option table has eight
selectable rows: Single-point, four Wide-area variants, and Auto-area AF,
Auto-area AF (people), and Auto-area AF (animals). It contains no selectable
3D-TRACKING row; the `3D-TRACKING` string reference at `0x103edc2e` belongs to
a label-output path and does not establish an activation entry. The option
mapper at `0x10430c8c` reads the option table rooted at `0x1074a688`; the mode
setter at `0x1042b2d8` maps Auto-area encodings 600/601/602 to base mode 6 and
submodes 0/1/2 in properties `0x0c2b`/`0x0c3d`. The generic OK/J menu
dispatcher `0x103ce96e` invokes the current UI object's registered event
callback. In the AF-area option path, that callback stores the selected mode;
it is not the Subject-tracking action call. Nikon's Z 30 manual describes
Subject tracking as a separate operation available while one of the three
Auto-area modes is selected: J enters the reticle stage, a second J begins
tracking, and another J ends it; W(Q) exits the mode. The assigned-control
action has the same start/end semantics. Thus the build-relevant route is the
native Subject-tracking action already compared in F-214, while the AF-area
menu trace supplies its mode precondition, not the activation hook. Static
findings and official manual, 2026-10-18; high confidence for option-table
contents and setter encoding, no direct firmware proof here of the live-view
J callback or tracking state transitions. No firmware bytes/dumps in the
repository and no camera access.

F-234. Attempted a synthetic stack watermark around the private Subject-
tracking candidate adapter in pinned QEMU. The adapter returned, but the
probe observed zero native action calls and no candidate/native path; only a
64-byte boundary region changed. Therefore the measurement provides no
candidate stack-depth or headroom evidence and does not close the stack gate.
The private harness did not verify each restoration write, but its disposable
QEMU process exited; the verified original firmware hash and simulator
checkout remained unchanged. Treat this as an inconclusive harness attempt,
not firmware behavior. Private QEMU output stayed outside the repository,
2026-10-18; low confidence for stack semantics, high confidence that the
required native path was not observed. No camera access or firmware bytes in
the repository.

F-219. A further static trace separates the 3D-TRACKING label and the
shooting-view J path from the native Subject-tracking action. In the renderer
containing the label block at `0x103edda0`, selector byte `[r4+0x83] == 8`
chooses the 3D-TRACKING text and passes it to text helper `0x1027f3cc`; this
is presentation of a descriptor value, not an action call, and the descriptor
producer/semantics remain unresolved. The selectable AF-area mapper and
setter remain `0x10430c8c` and `0x1042b2d8`; Auto-area value 600 stores base
mode 6/submode 0, with no direct call from that selection path to the native
action helper. For UI event `0x27e`, dispatcher `0x103ce96e` calls filter
`0x104e2cbc`; the filter first consults runtime key-to-function lookup
`0x10460ba2`, which can invoke a registered callback. A separate matching
screen-context path calls generic live-view input handler `0x102f1e10`
(arguments include `r0=0`, `r1=1`). That handler compares input/status state
through `0x102f1cae` and `0x102f0e1e`; a full direct-branch sweep found no
direct edge from this handler to native action helper
`0x10368b6e` or request service `0x1045a47e`. The callback table is reached
through a runtime screen object, so the actual J callback and any indirect
route from it to tracking remain unidentified. This strengthens the negative
conclusion that the text label is not a demonstrated tracking hook, but does
not establish camera-side J behavior or alter F-214's action-45 hook evidence.
Read-only, hash-verified static decode, 2026-10-18; high confidence for the
local dispatch/formatting edges, unresolved dynamic callback and descriptor
semantics. No firmware bytes/dumps in the repository, no modified image, and
no camera access.

F-216. A bounded static audit of the private AE-L/AF-L candidate's storage
and layout inputs did not clear its remaining patch-readiness gates. The
worker candidate frame is 540 bytes, including 424 bytes added below the
native worker's observed frame, and the enclosing known frame makes an
848-byte prefix against a configured 8,192-byte task stack. This leaves a
nominal 7,344 bytes before callees, but worst-case call-chain headroom is not
verified. The proposed code spans total 1,408 bytes and data spans total 896
bytes; the spot checks found zero-filled regions and no hits in the bounded
pointer/branch scans, but they do not prove executable mapping or a complete
code layout. The native Subject-tracking menu manifest requires 952 data
bytes before an additional 72-byte navigation table; the candidate's reviewed
data spans are insufficient, and the alternative added region remains only a
candidate. No assembly encoding or complete overlay was produced. Therefore
the candidate remains unsuitable for a camera test. Private static audit,
2026-10-18; high confidence for the listed arithmetic and explicit audit
limits, no conclusion about runtime reachability, complete layout, or camera
behavior. No firmware bytes/dumps in the repository and no camera access.

F-217. A private pinned-QEMU memory-only integration probe assembled and
linked the current AE-L/AF-L candidate in memory, applied all 45 planned edits
to guest RAM after booting the hash-verified stock image, and invoked the
candidate action adapter twice from a deliberately constructed worker
context. Both invocations completed, restored the context, and reached helper
`0x10368b6e` with action 45 followed by the same `0x1045a47e` request tuple
seen in F-214. The worker allocation observed in this run was 11,264 bytes.
The original firmware hash remained unchanged and the pinned QEMU checkout
was clean. This demonstrates composition, relocation, and repeated adapter
dispatch in the tested synthetic context. The probe manually initialized the
worker context and did not deliver a natural AE-L/AF-L press; the consumer
object is unmodeled, so identical requests do not demonstrate the actual
start-then-cancel transition. It also does not prove executable mapping in a
camera load, worst-case stack headroom, or full image acceptance. Private
memory-only pinned-QEMU run, 2026-10-18; high confidence for these bounded
observations, no inference about natural admission or camera behavior. No
firmware image written, no firmware bytes/dumps in the repository, and no
camera access.

F-218. A follow-up from the AF-area label catalog and the OK/J dispatcher
separates a display label from the Z 30's selectable AF-area options.
The block at `0x103edda0` is text, not an option or jump table; the label
selection path at `0x103edc2e` supplies the `3D-TRACKING` label to a shared
text-output helper. The actual selectable table rooted at `0x1074a688` has
eight entries: Single-point AF; Wide-area AF (S), (L), (L-people), and
(L-animals); Auto-area AF; Auto-area AF (people); and Auto-area AF (animals).
Its Auto-area
entries encode 600/601/602. Selecting Auto-area and confirming it reaches the
AF-area setter, which stores base mode 6 and submode 0/1/2; it does not invoke
the Subject-tracking action. The physical J/OK input maps to UI event `0x27e`
and the generic key dispatcher invokes the active screen's callback. Static
cross-references show a route from that dispatcher/filter family to the
central live-view handler, but do not identify the shooting-view J callback
or prove that it calls the native Subject-tracking action. A powered stock
QEMU probe that directly invoked event `0x27e` hit only the dispatcher entry,
not the live-view/action breakpoints; this synthetic call is inconclusive
about the real callback. Accordingly, the 3D-TRACKING text is not evidence of
a selectable Z 30 mode or the Subject-tracking hook. The build-relevant hook
remains the action-45 route matched to Nikon's native Subject-tracking
assignment handler in F-214. Read-only static decode and option-table
enumeration, plus a bounded stock-QEMU synthetic event, 2026-10-18; high
confidence for table contents and setter behavior, no conclusion about the
live-view J callback or camera transition. No firmware bytes/dumps in the
repository and no camera access.

F-220. A bounded instruction-level trace of native action helper
`0x10368b6e` narrows, but does not fully decode, the Subject-tracking toggle
cycle. Selector `0x2d` (45) reaches a state-dependent branch using state from
`0x1044dc5a`; it first checks a shared boolean gate through `0x1045a47e`,
which reads byte `+5` from object `0xc23a51a8`. If the gate is clear, state
0/1 dispatches through `0x1045a1ae` and posts internal event `0x3b`, state 2
uses `0x1045a1e6`/event `0x3c`, and state 3 uses `0x1045a21c`/event `0x3d`.
The gate object is distinct from the nearby state object at `0xc23a5368`; its
0-4 byte-`+5` transitions cannot be attributed to tracking. No decoded string,
property or hardware state ties events `0x3b`-`0x3d` to tracking start/end,
and the gate's producer remains unresolved. This confirms that the action-45
route is stateful inside Nikon's handler, consistent with the user-control
start/stop contract in F-214, but it does not prove which branch starts or
ends tracking or demonstrate a successful cycle. The camera-test question
therefore remains a behavior test, not a reason to add a second patch-side
state machine. Read-only, hash-verified static decode, 2026-10-18; high
confidence for selector, branch conditions, object read and event-post edges;
event semantics and camera behavior unconfirmed. No firmware bytes/dumps in
the repository and no camera access.

F-221. A follow-up trace of action 45 and the AF-area state mapper corrects
the destination and semantics recorded in F-214 and F-220. Address
`0x1045a47e` is a boolean gate: it calls `0x102240ac`, reads a separate
status bit from object `0xc23a51a8`, and returns the boolean. It is not the
request service, and the previously reported request tuple at that address
is not confirmed. The action helper `0x10368b6e` calls state mapper
`0x1044dc5a`, which snapshots 0x468 bytes and selects an internal state from
snapshot offsets `+0x44`, `+0x61`, and `+0x62`. Base mode 6 with submode 0
maps state bytes 0/2 to internal state 1 and byte 1 to state 0; submode 1
maps byte 0 to state 2 and bytes 1/2 to state 3; submode 2 maps like
submode 0. The `0x10368b6e` selector-45 branch then routes internal states
0/1, 2, and 3 respectively through `0x1045a1ae`, `0x1045a1e6`, and
`0x1045a21c`, subject to the shared boolean gate. The first helper calls
`0x10230832`, the second `0x10230856`, and the third `0x10230866`; each then
passes an internal value to `0x1046296e`, whose body is only `bx lr`, so
these are not demonstrated event posts. `0x10230832` continues into
`0x1019596e`, which checks AF-subsystem readiness/state and writes a
mode-dependent byte before invoking further helpers, but those effects do
not identify tracking start versus stop. Selector 45 therefore demonstrably
consults AF-area mode/state and delegates to distinct native helper paths;
this is stronger patch-design evidence for keeping the Auto-area AF
precondition and using Nikon's action than F-214's request-service wording,
but the snapshot fields' exact identity with public properties and the
start/cancel semantics remain unproved. The candidate still lacks natural
AE-L/AF-L hook admission, camera-load executable mapping, worst-case stack
proof, and a complete test image. Read-only, hash-verified static decode,
2026-10-18; high confidence for the listed control flow and instructions,
medium for correlating snapshot bytes with the public Auto-area mode, and no
conclusion on tracking start/stop or camera behavior. No firmware bytes/dumps
in the repository and no camera access.

F-222. A bounded continuation through the action-45 helper callees shows how
the people submode diverges, without resolving the helper semantics. For
base mode 6/submode 1, the mapper's state 0 becomes internal state 2 and
reaches `0x1045a1e6` -> `0x10230856` -> `0x10162f14` -> `0x1007756e`; state
1 or 2 becomes internal state 3 and reaches `0x1045a21c` -> `0x10230866` ->
`0x10162f18` -> `0x100775c6`. The last two routines operate on a shared
configuration/state object (including fields at offsets `+0x10`, `+0x1c`,
`+0x20`, `+0x38`, `+0x39`, `+0x40`, `+0x624`, `+0x628`, and `+0x629`),
with branches on that object's state and results from shared config helpers.
For submodes 0 and 2, both mapped states 0 and 1 reach the same helper chain
`0x1045a1ae` -> `0x10230832`; it passes input 0 to `0x1019596e`, whose
readiness-gated path writes byte 6 to an AF-related object field (input 1
would write 7, but action 45's observed caller supplies 0). These are
stateful operations, not semantic labels. No decoded evidence identifies
which helper means tracking start, cancellation, or another AF operation;
the manual remains the only source for the external start-on-press / stop-on-
second-press contract. This narrows the static map and confirms native
state-dependent handling, but does not verify the camera cycle or make the
candidate test-ready. Read-only, hash-verified Thumb disassembly,
2026-10-18; high confidence for call chain and literal field accesses, no
confidence assigned to start/stop labels. No firmware bytes/dumps in the
repository and no camera access.

F-223. Reinspection of the queued-input consumer corrects a prior physical
input attribution. Handler `0x103a3d14` processes event code `0x2083` and
constructs logical ID/operation records; consumer `0x103a3f9e` maps each
record ID through the selected table, applies the mapped mask to staging word
`0xc18c9a68`, and calls setter `0x101e383a` if the staging word changes.
It does not read a physical SW-bank word. `0x115c694c` belongs to the
surrounding module's object/initialization path and is not the consumer's
input word. Thus the separate facts “ID 41 maps to mask `0x2000`” and
“AEAF_LOCK is named with mask `0x2000`” do not establish physical button
delivery to ID 41 or to the candidate accessor hook `0x102f14b2`. The one-button action-45
design remains separate, but its physical AE-L/AF-L admission is unresolved.
Read-only bounded review of hash-verified Thumb disassembly, 2026-10-18; high
confidence for this consumer's data flow, no conclusion on hardware
transport. No firmware bytes/dumps in the repository and no camera access.

F-224. The candidate hook address `0x102f14b2` is the common exit inside
record accessor `0x102f1412`: it unlocks the accessor's mutex, moves the
selected record pointer from `r4` to the return register, and returns it.
The accessor can select the 400-byte-stride ring at `0xc2008ea0` or the
separate record at `0xc200a7a0`, depending on its mode argument. Therefore
`0x102f14b2` is an accessor-return hook, not a copy operation or a physical
button handler. It gives the candidate a selected-record pointer, but the
record's physical AE-L/AF-L provenance remains unproved. This refines F-212's
hook description and makes the unresolved trigger boundary explicit. Static
reinspection of hash-verified Thumb disassembly, 2026-10-18; high confidence
for instruction placement and return data flow, no conclusion on physical
input origin. No firmware bytes/dumps in the repository and no camera access.

F-225. The candidate's ring-record mask checks are consistent with the
paired mask-difference record built by `0x102f199a`; they are not internally
contradictory. Helper `0x101dd502` stores its two inputs at relative offsets
0/+4, their XOR at +8, first-input-only bits at +12, and second-input-only
bits at +16. The first block begins at record offset +4 and is built from
`input1 | input2` versus `input2`. Thus the candidate's checks at record
offsets +4/+8/+12/+16 for bit `0x2000` set/clear/set/set describe a bit
present only in `input1` for that pair. The builder's callers are
`0x1039e1d4` and `0x1046497e`; neither caller by itself proves that this bit
originated at physical AE-L/AF-L. The candidate's edge predicate is therefore
structurally plausible, but its source attribution remains unresolved. Static
reinspection of hash-verified Thumb disassembly, 2026-10-18; high confidence
for record layout and bit algebra, no physical-input conclusion. No firmware
bytes/dumps in the repository and no camera access.

F-226. A focused re-read of the configurable-button routines narrows the
AE-L/AF-L remap design and corrects the role of the apparent dispatcher
sites. Fn1's configured-action handler `0x1036957c` reads setting `0x1150`,
recognizes action value `0x4d` (77), and calls Nikon's Subject-tracking helper
`0x10368b6e`. AE-L/AF-L's separate handler `0x10369468` reads `0x1184` (and
`0x1187` in its alternate mode), tests values 25 and 42, and does not call
action 45. The callers at `0x103020b4` and `0x10302108` are part of a
dispatcher that combines the handlers' returned bits into a status mask;
they are not established physical-key action callbacks and should not be
used as the remap hook. The sound patch design remains to detect a fresh
physical AE-L/AF-L press and invoke the native action-45 handler, but the
candidate input record's physical source is still unknown (F-223–F-225).
The evidence does not yet establish whether the camera's AE-L/AF-L menu can
be extended to offer action 77 or whether a direct button-route patch is
needed. Auto-area AF remains the correct operating precondition. Static
Thumb control-flow review of the hash-verified image, 2026-10-18; high
confidence for these function relationships and return-mask use, no
conclusion on physical admission, menu behavior, or camera cycle. No
firmware bytes/dumps in the repository and no camera access.

F-227. The registered input-snapshot callback `0x102f2eae` is a more direct
AE-L/AF-L route candidate than the unproven record-accessor hook. It calls
`0x102f0d14`, which updates/compares the input snapshot and returns a broad
change indication; the callback then checks mask `0x2000` in its input record.
When the AE-L/AF-L assignment setting `0x1184` equals 9 (AF-ON), that branch
posts event `0x14` through `0x1044e68c`. This connects the named AEAF_LOCK
switch mask to the existing AE-L/AF-L assignment behavior and event route.
However, the branch tests the current bit after any qualifying snapshot
change; the reviewed code does not show a per-button rising-edge check. An
unrelated input change while AE-L/AF-L is held could therefore re-enter this
branch. A patch that substitutes action 45 here needs a verified per-button
fresh-edge guard and must preserve the stock AF-ON path when that assignment
is selected. Static Thumb review of the registered callback and comparator,
2026-10-18; high confidence for the observed conditional/event flow, no
conclusion that the callback runs only on a physical press or that action 45
can be safely inserted. No firmware bytes/dumps in the repository and no
camera access.

F-228. F-226's warning about calls `0x103020b4` and `0x10302108` was too
strong: those sites are within the same input/action dispatcher family that
also calls Fn1 handler `0x1036957c`, whose value-77 path invokes action 45.
Their return values are combined into a mask, but that alone does not make
the sites mere status queries or rule them out as part of action routing.
The calls specifically reach AE-L/AF-L handler `0x10369468`; its reviewed
body still does not invoke action 45. The unresolved point is how the
dispatcher cases are selected from physical key input and whether extending
the AE-L/AF-L handler is the correct remap seam. Treat the dispatcher as a
live candidate for that trace, not as either a confirmed physical callback
or an excluded hook. Static reinspection of the shared input/action switch,
2026-10-18; high confidence for the sibling call/callee behavior, no
conclusion on physical-key delivery. No firmware bytes/dumps in the
repository and no camera access.

F-229. A separate live-view input mapper walks the group-1 mask table and
maps mask `0x2000` to logical input ID 13; the UI input table maps ID 13 to
event `0x28b`, whose indexed label is “AE-L/AF-L button.” The registered
snapshot callback `0x102f2eae` tests the same `0x2000` bit and routes the
existing AF-ON assignment. This gives the callback a stronger native
AE-L/AF-L link than the candidate ring-record accessor currently has, but
the candidate's dispatcher also explicitly admits logical ID 13. The
mask-to-ID table and candidate ID gate therefore align; the remaining source
gap is whether its paired ring-record fields are produced from that same
physical input route. The private candidate adds the verified “Subject
tracking” label to the AE-L/AF-L assignment list as value 77, writes that
value to setting `0x1184`, and routes it through native action 45. This
verifies the intended menu/action mapping in the candidate layout, not that
it has been shown or saved by a camera. A memory-only QEMU probe sent
synthetic event `0x27e`
through dispatcher `0x103ce96e`; it reached generic dispatch lookup but no
registered callback, action 45, or AF-area setter was observed. A separate
prior probe of event `0x28b` likewise observed no downstream action. These
are simulator-path limits, not evidence that the real firmware lacks the
callback. The current private candidate adds “Subject tracking” to the
AE-L/AF-L assignment menu as value 77 and routes it to native action 45. Its
logical-ID-13 admission matches the AE-L/AF-L input table, so the remaining
physical source uncertainty is covered by the owner's recorded device-test
disposition after all other gates pass. No complete candidate-side
start/held/release/second-edge cycle has been verified; no camera access.
Static hash-verified
input-map review and pinned-QEMU synthetic dispatcher probe, 2026-10-18; high
confidence for table/callback relationships, low confidence for simulator
event reachability, no claim about physical press or cycle behavior. No
firmware bytes/dumps in the repository.

F-230. A sequential memory-only QEMU probe exercised the private AE-L/AF-L
candidate with fresh, held, release, and second-fresh records. The two fresh
edges each passed the candidate guard and completed the adapter with exactly
one call to Nikon's native action helper `0x10368b6e` (selector 45); held and
release records were rejected with no action call. The probe also exercised
the candidate's dispatch-finish cleanup block using a constructed caller
frame, and the recorded ABI save/restore cases passed. This verifies edge
arbitration and request dispatch in that constructed candidate context. It
does **not** verify that the first native call starts tracking or that the
second stops it: the AF consumer is unmodeled, the complete context dispatch
was not naturally traversed, and the guest candidate was applied through
debugger memory writes rather than loaded as a private overlay. The hook's
natural physical-button admission, camera-load executable mapping, worst-case
stack margin, and full-image acceptance remain open. Thus the sequence closes
the bounded dispatch-control check only; it does not make the candidate
camera-testable. Read-only pinned-QEMU run with hash-verified stock image and
private candidate, 2026-10-18; high confidence for the observed guard,
adapter calls, and constructed cleanup block, no claim about consumer state
or natural input. No firmware bytes/dumps in the repository and no camera
access.

F-231. Continued the action-45 state trace through the native AF snapshot
producer. Mapper `0x1044dc5a` reads snapshot bytes `+0x61` and `+0x62`; the
producer copies these from internal AF-context bytes `+0x364` and `+0x365`
of the structure rooted at `0xc237c7b4`. The context builder
`0x101925ee` constructs its `+0x2b8` subcontext from the live AF object, and
`0x101914ae` populates state slots corresponding to global offsets `+0x364`
and `+0x365` from mode-dependent branches. In one branch the state byte is
copied from an AF subcontext field at `+0x25`; other branches initialize it
to zero or set the companion discriminator byte. These instructions establish
that the action mapper consumes a real AF-context state tuple, but neither
the state byte nor its values is named as tracking-active/inactive in the
decoded code. They do not label a branch as tracking start or cancel.

A separate disposable-QEMU probe called native Auto-area setter
`0x1042b2d8` with encoding 600 and read back properties `0x0c2b == 6` and
`0x0c3d == 0`; it also set the state property read by the AF snapshot builder
to 6 and the native Fn assignment to 77. Despite these successful property
readbacks, action 45's mapper returned state 5 on each of three Fn-handler
calls, and no Auto-area helper path was reached. The stock simulator fixture
therefore does not populate the native AF snapshot consistently with those
menu properties and cannot verify the start/cancel transition. The manual's
assigned-control cycle and the candidate's two fresh action-45 dispatches
remain consistent with the intended design, but neither substitutes for an
observed consumer transition. Read-only hash-verified Thumb decode using
LLVM disassembly plus pinned-QEMU guest-RAM calls, 2026-10-18; high confidence
for the observed snapshot copy and setter/readback/mapper results, no
confidence assigned to start/cancel labels. No firmware bytes/dumps in the
repository and no camera access.

F-232. Rebuilt the private AE-L/AF-L Subject-tracking candidate with the
installed LLVM assembler/disassembler, bypassing the unavailable local
Capstone Python package. The link/layout audit placed 964 code bytes in the
planned 1,408-byte code regions, checked 24 relocations, all 15 four-byte
hook windows, and 45 total edits; the candidate remains private. QEMU's
generic loader loaded 35 merged overlay regions before guest resume, and
read-back matched every overlay byte. The stock firmware hash and pinned-QEMU
checkout remained unchanged. A pinned-QEMU sequence through the loaded
candidate then accepted synthetic fresh ID-13-shaped records and dispatched
native action 45 exactly once per fresh edge; held/release records dispatched
nothing. Constructed cleanup and ABI controls passed. These results validate
candidate assembly/layout and no-debugger-write overlay loading in QEMU, not
the camera's executable mapping, natural physical-button admission, AF
consumer start/cancel semantics, or worst-case stack headroom. The candidate
is still not ready for a camera test. Private pinned-QEMU run, 2026-10-18;
high confidence for assembly/layout and observed simulator behavior, no claim
about the native tracking cycle or real camera. No firmware bytes/dumps in
the repository and no camera access.

F-233. Rechecked executable mapping after F-232 using the current startup and
task-table state. The startup TTBR0 table at `0x10030000` maps candidate code
VA section `0x10000000` with a valid section descriptor and XN clear (ARMv7-A/R
short-descriptor rules). A full LLVM ARM/Thumb scan also found later TTBR0
writers: scheduler context paths load an optional table pointer from task
context offset `+0xc0`, and a context-switch helper can replace TTBR0 while
temporarily disabling the MMU. In pinned QEMU, the candidate task's `+0xc0`
override was zero, while the active TTBR0 was a runtime table in RAM. A
read-only `ATS1CPR` probe reported the candidate VA resolving outside the
simulator's modeled RAM, although the same loader-based overlay executed from
that VA in QEMU. The simulator result therefore does not establish the
camera's runtime physical backing or load-time executability; the reset table
alone is insufficient because runtime TTBR0 can differ. The executable
mapping gate remains open pending static tracing of the task's inherited
runtime table setup. Read-only original-image decode and pinned-QEMU register
probe, 2026-10-18; high confidence for the listed instructions/register
results and reset-table descriptor, low confidence that the simulator's
ATS/MMU result models camera physical mapping. No firmware bytes/dumps in the
repository and no camera access.

F-235. Repeated the private pinned-QEMU stack watermark with the validated
loaded-overlay and fresh-edge/action setup. The worker TCB reports an
11,264-byte stack. With a 2,048-byte canary below the constructed action-call
SP, first-fresh dispatched native action 45 once and changed 1,364 canary
bytes; held and release dispatched no action; second-fresh dispatched action
45 once and changed 1,324 bytes. The candidate adapter returned with context
restored, constructed cleanup passed, and the bounded sequence completed.
This gives a measured watermark only for the constructed path and does not
establish worst-case headroom under natural worker admission, all interrupt/
scheduling conditions, or a fully modeled AF consumer. It reduces uncertainty
but leaves the stack gate open. This corrects the harness failure in F-234;
that first run remains invalid. Private output stayed outside the repository,
2026-10-18; high confidence for observed bounded QEMU canary/action behavior,
no claim about worst-case camera stack use. No camera access or firmware bytes
in the repository.

F-236. Static Thumb disassembly traced the action-45 AF-state consumer. Caller
`0x1044dcbe` invokes mapper `0x1044dc5a` and continues to helper `0x1045a21c`
only when the mapper returns numeric state 2. State 2 requires snapshot byte
`+0x44 == 6`, `+0x61 == 1`, and `+0x62 == 0`; this mode value matches the
Auto-area base mode in F-215/F-231. The QEMU mapper result 5 takes the native
reject branch, explaining why its action-45 probe never reached the helper.
The accepted helper calls `0x10230866`, which invokes stateful routine
`0x100775c6`, then forms an event-code `0x3d` request via `0x1046296e`; that
target is a return-only stub in the verified image. The fields and stateful
routine have no tracking-active/inactive labels in available evidence. This
identifies a real AF-state precondition and static route, not proof of Subject-
tracking start/cancel or event delivery. Candidate edge controls do not
override the native state gate. Read-only LLVM Thumb disassembly,
2026-10-18; high confidence for numeric comparisons and call edges, no
confidence assigned to start/cancel semantics. No camera access or firmware
bytes in the repository.


F-237. Scope correction to F-236: `0x1044dcbe` is a separate caller of mapper
`0x1044dc5a`, not the principal action-45 selector `0x10368b6e`. The
state-2-only condition and tuple (`+0x44 == 6`, `+0x61 == 1`, `+0x62 == 0`)
apply only to the separate caller's route to `0x1045a21c`. The main selector
continues to handle mapped states 0-3 as recorded in F-221/F-222; in Auto-area
submodes 0/2, states 0/1 route to `0x1045a1ae`. QEMU's observed state 5
rejects its current path but does not establish state 2 as the sole accepted
action-45 state. F-237 supersedes that overbroad interpretation while
preserving F-236's separate-call-site condition. Read-only LLVM Thumb
cross-check, 2026-10-18; high confidence in caller separation and documented
branch map, no confidence assigned to action start/cancel. No camera access or
firmware bytes in the repository.

F-238. Corrected and exercised the AE-L/AF-L snapshot rising-edge candidate.
The shared updater's four-byte instruction begins at `0x102f0d30`; the earlier
prototype's `0x102f0d32` address lands on its second halfword and is not a
valid hook boundary. The corrected private candidate replaces the aligned
instruction, compares the current and previous snapshot's `0x2000` bit, checks
assignment value 77, and enters Nikon's native action 45 only on a rising
edge. LLVM assembly/link validation checked 27 relocations, 16 hook windows,
and 47 edits in the private manifest. A pinned-QEMU private-loader run
read back 39 overlay regions and drove synthetic fresh/held/release/fresh
snapshots; action 45 was entered once, zero, zero, and once. The test used a
private return trampoline after the shim, so it did not execute the native
snapshot-update tail. The updater has seven direct callers, and their task
stack/context suitability for an inline native action remains unresolved.
This verifies synthetic edge arbitration and dispatch, not physical button
admission, camera-load mapping, worst-case stack, native tracking
start/cancel, or full-image acceptance. Read-only Thumb review, LLVM candidate
link, and pinned-QEMU synthetic records, 2026-10-18; high confidence for the
aligned hook boundary and observed test sequence, no claim about physical
input or tracking state. No camera access or firmware bytes in the repository.

F-239. Narrowed the plain Auto-area action helper without assigning toggle
semantics. The main action-45 selector routes plain Auto-area states through
`0x1045a1ae`; it clears an AF-related object field at `+0x40` and calls
`0x10230832`. That wrapper reads an input byte and passes it to `0x1019596e`,
which has several readiness/status checks and writes byte 6 for input 0 or
byte 7 for input 1 at an AF-related object offset `+0x38` before its remaining
update calls. The helper then forms event `0x3b` through `0x1046296e`, a
return-only stub in this image. These are real state mutations and gates, but
available static labels do not identify the field as Subject-tracking state
or establish whether the two values mean inactive/active. Thus action 45's
plain Auto-area start/second-press cancel cycle remains unproved. Read-only
LLVM Thumb control/data-flow review, 2026-10-18; high confidence for the
branch and writes, no confidence assigned to feature meaning. No camera
access or firmware bytes in the repository.

F-240. The shared snapshot updater's seven direct callers are not equivalent
hook contexts. Paired-record builder `0x102f199a` calls the updater twice,
first with `sp` and later with `sp+0x18c`, after reserving a `0x31c`-byte
local frame. An inline action-45 hook at the common updater therefore adds
the native action stack to more than one caller context, including this
already-deep frame. Callback `0x102f2eae` is one of seven callers. The other
small wrappers have only 8-16 bytes of explicit frame in the reviewed windows,
but their task/thread identities and available stack are not established. A
callback-only hook is narrower but may miss an edge if another caller updates
the shared previous snapshot first. This leaves an unresolved tradeoff between
edge completeness and known stack context; no site is yet camera-testable.
Read-only LLVM Thumb call-site review, 2026-10-18; high confidence for direct
call shapes and builder frame size, task context remains open. No camera
access or firmware bytes in the repository.

F-241. Reinspection of the configurable-function switch identifies a more
direct remap hypothesis than the shared snapshot updater. Dispatcher
`0x10301f36` switches on a function-code argument; its code `0x2d` branch
calls Fn1 handler `0x1036957c`, which reads Fn1 assignment property `0x1150`
and calls native Subject-tracking action 45 when the value is 77. Its
AE-L/AF-L handler `0x10369468` reads assignment properties `0x1184` or
`0x1187`, but its reviewed branches recognize 25 and 42 and do not accept 77.
This suggests extending the AE-L/AF-L handler to route value 77 to action 45,
or mapping its function-code branch through the existing Fn1 handler. The
dispatcher also assembles a status mask, and this review does not establish
that the switch is entered exactly once per physical fresh press or that
reusing the Fn1 handler preserves AE-L/AF-L context. Therefore neither
variant is selected as a patch yet. The immediate build decision is to trace
the dispatcher caller's input/code semantics and compare the handlers'
arguments, side effects, and return contract; retain the snapshot-edge
candidate only as fallback. Read-only LLVM Thumb disassembly, 2026-10-18; high
confidence for the numeric switch and handler branches, no claim for physical
press semantics or Subject-tracking cycle. No camera access or firmware bytes
in the repository.

F-242. A private pinned-QEMU probe tested the narrow AE-L/AF-L handler
extension proposed in F-241. A temporary guest-memory branch at
`0x103694a4` sent assignment value 77 through a helper that preserves the
existing 42 and default branches and calls `0x10368b6e` for value 77. A
constructed call to handler `0x10369468` observed action-45 entry for 77;
values 42 and 25 reached their original handlers (`0x103691fc` and
`0x1036845a`). The hook and helper bytes were restored before QEMU exited;
the verified firmware file and pinned simulator checkout hashes/state were
unchanged. This proves a synthetic handler-level branch and preservation of
these two sampled alternatives, not that function code 13 is invoked by a
fresh physical AE-L/AF-L press, that held input does not repeat, or that
action 45 toggles tracking off on a second press. Read-only source review,
temporary memory-only QEMU probe, 2026-10-18; high confidence for observed
synthetic branch behavior, no physical-input or cycle claim. No camera access
or firmware bytes in the repository.

F-243. The configurable-function dispatcher does not yet provide a proven
physical-button route to the remap. A full-image Thumb BL/B.W immediate scan
found only one direct caller of `0x10301f36`, at `0x10302270`. Its enclosing
callback `0x10302220` admits only input values `0x1a`, `0x1b`, and `0x1c`
before passing the value to the dispatcher. In the dispatcher's first TBB,
AE-L/AF-L handler `0x10369468` is index 13 and Fn1 handler `0x1036957c` is
index 45; the admitted 26/27/28 values map to other handlers. A second
high-range table also contains an AE-L/AF-L status call, but is not reachable
through the observed direct caller's admitted values. No literal function
pointer to dispatcher `0x10301f36` was found in the image, although computed
or runtime registration paths are not excluded. Therefore F-241/F-242 prove
only a handler-level implementation route, not its connection to the physical
AE-L/AF-L button. Next identify the producer/registration for callback
`0x10302220` and search for other indirect invocations of the dispatcher; if
that cannot connect code 13 to an AE-L/AF-L edge, return to the input-chain
edge source. Read-only immediate scan and TBB index decode, 2026-10-18; high
confidence for direct callsites and table indices, no claim that the runtime
callback table is exhaustive. No camera access or firmware bytes in the repo.

F-244. A bounded direct-call attempt to execute registered snapshot callback
`0x102f2eae` in pinned QEMU did not complete. The probe supplied a synthetic
396-byte record with AE-L/AF-L mask `0x2000` and observed no native action-45
entry before the thread-aware call timed out. The synthetic record's validity
and callback's scheduling/return contract are not established, so this is
not evidence that the real callback fails or that the action route is absent.
The disposable QEMU process exited, the private firmware identity was
unchanged, and the simulator checkout remained clean. Do not repeat this
same direct-call setup; use static registration/call-context tracing or a
natural simulator event only if it can inform the named hook decision.
Temporary memory-only QEMU diagnostic, 2026-10-18; high confidence for the
timeout and absence of observed action entry in this attempt, no inference
about natural callback behavior. No camera access or firmware bytes in repo.

F-245. The shooting-view OK/J route remains screen-specific and runtime-bound.
In the generic key filter, event `0x27e` is offered to key-to-function lookup
`0x10460ba2` with table base `0xc183d150` and count four. The lookup scans
`(key, callback)` entries and invokes a matching non-null
callback through `blx r3`; it does not encode a static Subject-tracking
target. Separately, label routine `0x103edc2e` formats the `3D-TRACKING` text
through output helper `0x1027f3cc`, while the selectable AF-area table remains
the eight-entry table at `0x1074a688`; Auto-area setter `0x1042b2d8` stores
mode 6 and submode 0 for value 600. Therefore AF-area selection supplies an
eligibility state but does not activate tracking. A synthetic stock-QEMU
shooting-view `0x27e` dispatch reached the generic screen dispatcher, but no
callback-table lookup or native action 45 was
observed. The runtime callback target and its connection to action 45 remain
unresolved, so this trace does not displace the native action-45 remap
hypothesis for AE-L/AF-L. Read-only Thumb disassembly plus the bounded
synthetic QEMU probe, 2026-10-18; high confidence for the static lookup shape
and AF-area/label distinction, no claim for the runtime callback target,
physical J delivery, or tracking cycle. No camera access or firmware bytes in
the repository.

F-246. A follow-up read-only QEMU observation sampled the runtime key callback
table at `0xc183d150` after the standard simulated live-view setup. Its four
entries were keys `0x161b`, `0x23e4`, `0x1536`, and `0x14c2`; their callback
targets were respectively `0x104e2e85`, `0x104e2ea1`, `0x104e2ec7`, and
null. The three decoded callback bodies perform state checks and populate
small response records; none directly calls native action 45. A fresh
synthetic event `0x27e` through dispatcher `0x103ce96e` stopped at generic
screen handler `0x103ce804`; breakpoints on key filter `0x104e2cbc`, lookup
`0x10460ba2`, all three table callbacks, and action 45 did not fire. This
confirms that this simulator input does not reach the active callback lookup,
not that the camera lacks a J action. No competing static J hook was
identified, so action 45 remains the stronger remap target for AE-L/AF-L.
Read-only guest-RAM inspection and breakpoint observation in pinned QEMU,
2026-10-18; high confidence for sampled table contents and observed stops,
limited to this simulated screen setup. No firmware bytes/dumps in the repo
and no camera access.

F-247. The two AE-L/AF-L trigger implementations must not be combined without
shared edge arbitration. The newer private production overlay installs both
`0x102f0d30` (`snapshot_edge_hook`) and `0x102f14b2` (`copy_hook`). On a fresh
`0x2000` snapshot edge with assignment 77, the first path calls action 45
inline on the shared-updater caller. The second path captures a ring-record
edge and reaches action 45 through the worker adapter. F-238 and F-230/F-235
test these paths independently; no integrated test proves that one physical
press cannot traverse both. If it does, the native toggle may receive two
requests. The common updater also has seven callers, including the
`0x31c`-frame builder, so its inline action retains the F-240 stack/context
risk. Select the worker-mediated `0x102f14b2` design as the sole patch
candidate and omit the common-updater action hook. This preserves the
constructed fresh/held/release/fresh behavior and measured worker-path stack
watermark while making the physical input source an explicit device-test
item. The candidate is still not testable until executable mapping, full
image/layout acceptance, and the required hardware-readiness checks are
closed. Static comparison of the two private manifests and hook bodies,
2026-10-18; high confidence for independent action paths and potential
double-dispatch, no claim that natural camera input traverses both. No camera
access or firmware bytes in the repository.

F-248. Audited the selected worker-only accessor hook's return contract. At
`0x102f14b2`, stock code loads the mutex address and adds `0x20` before its
unlock call; the latter `ADDS` defines flags consumed by the continuation.
The candidate performs the same address load and addition after its checks,
so the continuation sees the stock return pointer and NZCV result. The hook
restores `r0-r3`, `r5-r7`, and LR around its probe, leaves `r4` and `r8-r11`
untouched, restores SP, then reaches the original unlock/return tail. This
closes the local call-site register/flag/return review for the worker hook,
not a complete ABI audit of all 15 hooks or worst-case task-stack proof. The
worker-only overlay has separate loader-based QEMU execution evidence (F-232,
F-235); `guest_execution: false` in its generated build manifest is a
pre-execution default, not the final run status. Camera-load mapping and
complete-image acceptance remain open. Read-only Thumb disassembly, candidate
assembly review and existing private QEMU reports, 2026-10-18; high
confidence for the reviewed hook boundary and continuation contract, no
claim for natural key delivery or camera execution. No camera access or
firmware bytes in the repository.

F-249. A bounded follow-up to the runtime mapping question found a later
ARM-mode MMU setup sequence: `0x11c9e784` disables the MMU, `0x11c9e788`
loads a literal whose value is `0xc11f8000`, and `0x11c9e78c` writes it to
TTBR0 before the sequence reenables the MMU. The translation table is in RAM
outside the captured firmware module, so its descriptor for candidate VA
`0x1002d000` cannot be read from this module. The independent scheduler path
can also install a per-task TTBR0 table from context offset `+0xc0` (F-233).
This narrows the mapping blocker but does not prove whether this later setup
is the table inherited by the camera's worker or whether its candidate-page
mapping is executable. Further simulator translation probes cannot supply
the missing table contents. Read-only full-image ARM disassembly and literal
decode, 2026-10-18; high confidence for the MMU/TTBR write sequence and
literal value, no claim about the runtime table descriptor or camera task
mapping. No camera access or firmware bytes in the repository.

F-250. Checked for a direct executable-cave alternative in the 1 MiB address
sections containing the candidate's trigger, action and menu hook sites
(`0x10200000`, `0x10300000`, `0x10400000`). The verified module contains no
zero-filled run of even 32 bytes in those sections; the candidate needs about
964 bytes of code. This rules out a simple relocation into an existing empty
span in those hook-related sections, not every possible reuse of dead code.
The current candidate's only reviewed capacity remains in section
`0x10000000`, whose runtime descriptor is unavailable (F-249). Moving code
into existing functions would be a new redesign with additional behavioral
and ABI risk. Read-only zero-span scan of the verified module, 2026-10-18;
high confidence for the checked intervals and threshold, no claim that all
nonzero code spans are live. No camera access or firmware bytes in the repo.

F-251. Added an isolated QEMU 10.2.4 read-only diagnostic for the runtime
translation used by the candidate VA page. The display machine's modeled RAM
already covers the firmware's table address at `0xc11f8000`. After the
standard assisted live-view diagnostic setup, a probe read the current TTBR0/TTBCR and
the computed L1 entry for `0x1002d000`; it decoded as a valid section mapping
with XN clear. The target falls in modeled display RAM, and the entry agrees
with an `ATS1CPR` translation of `0x1002da00` with no translation fault. The
diagnostic routine executed from the same candidate VA page and returned with
its caller context restored. This run used the current diagnostic task, not a
verified tracking-worker context, so it does not close the worker-specific
mapping question or establish camera equivalence. Read-only CP15 observation
and QEMU physical-memory inspection with the original C1.20 firmware loaded,
2026-10-18; high confidence for this QEMU configuration, no claim for the
physical camera. No firmware bytes/dumps in the repository and no camera
access.

F-252. Repeated the tracking-worker breakpoint check after the standard
assisted live-view setup using a thread-aware, read-only QEMU wait. The guest
ran for 20 seconds without reaching worker entry `0x102f7448`; the check
therefore did not capture worker registers or its active TTBR0 descriptor.
This is consistent with F-213's finding that the simulator did not exercise
the worker entry/cleanup path. It does not establish that the real firmware
worker is unreachable or that its camera mapping is invalid. No QEMU source
was changed. This closes the current simulator-only attempt; further
scheduler/fidelity work has no new build-relevant evidence unless a specific
new worker stimulus becomes available. Private pinned-QEMU run, 2026-10-18;
high confidence for the bounded timeout, no inference about camera scheduling
or memory mapping. No camera access or firmware bytes in the repository.

F-253. Re-ran the read-only CP15 mapping probe in the standard assisted
live-view QEMU context and recorded the active TTBR0 base as `0xc2ad4000`.
Its entry for candidate VA `0x1002d000` is a valid executable section mapping
to modeled display RAM, consistent with the `ATS1CPR` result. A GDB write
watchpoint on that exact entry did not fire during an eight-second post-setup
window, so this run observed no subsequent change to the diagnostic task's
entry. This is a different runtime table from the later static setup path at
`0xc11f8000` (F-249); the result still does not identify the tracking worker's
context or camera mapping. No more simulator scheduling work is justified
without a new worker stimulus. Isolated pinned-QEMU run with read-only CP15
and memory observations, 2026-10-18; high confidence for the reported QEMU
context only. No camera access or firmware bytes in the repository.

F-254. Added a bounded USB identity/capability probe that sends only standard
PTP GetDeviceInfo (`0x1001`, transaction ID zero) to the Z 30 USB ID. It
reports manufacturer, model, device version and advertised operation codes;
it does not call any Nikon vendor operation or request memory, properties,
objects or images. The operation list can guide a later source review, but it
is not permission to invoke an unknown operation and does not expose runtime
TTBR0. Synthetic parser/container tests pass; no camera was connected or
queried. The implementation stops if the PTP interface cannot be claimed and
does not detach a driver or change a USB configuration. CIPA PTP-IP operation
rules permit transaction ID zero for GetDeviceInfo; local source review and
synthetic tests, 2026-10-18; high confidence for the command generated by the
tool, no hardware/driver claim. No camera access or firmware bytes in the
repository. See `camera-readonly-identity-method.md`.

F-255. The new tool's host-side libusb initialization and USB descriptor
enumeration succeeded, and found zero devices matching the Z 30 USB ID. The
check did not open any device or send a PTP request. This verifies the local
enumeration path and matches the owner's report that the camera is not yet
connected; it does not test the camera interface or PTP transaction. Read-only
local USB enumeration, 2026-10-18; high confidence for this host snapshot,
no camera contact or firmware data. See F-254.

F-256. The ctypes layouts used to inspect libusb device, endpoint, interface,
and configuration descriptors match the installed libusb C header on this
host: sizes 18, 32, 40, 16, and 40 bytes, with the accessed field offsets
matching the C ABI. This reduces descriptor-parsing ABI risk in the prepared
GetDeviceInfo preflight, but does not verify the USB transport against a
camera. Local Python ctypes/C compiler comparison against the installed
libusb header, 2026-10-18; high confidence for this host's ABI. No camera
contact or firmware data.

F-257. With the owner reporting the camera plugged in, macOS IORegistry showed
a Nikon Z 30 USB device (`04b0:0452`, USB release `0x0120`). The reviewed PTP
probe and a separate native C program using installed libusb 1.0.30 each
enumerated zero devices. Running the documented probe stopped at device
selection before opening a handle or sending a PTP command. This establishes
a host transport mismatch, not camera PTP support or firmware version. Read-
only IORegistry metadata and libusb enumeration, 2026-10-18; high confidence
for this host snapshot. No serial number, camera command, or firmware data.

F-258. Re-ran the documented `--read-device-info` probe with host USB access
after the sandboxed libusb path failed. Its sole request, standard PTP
GetDeviceInfo (`0x1001`), succeeded and reported Nikon Corporation, model
Z 30, device version V1.20, and the advertised operation list; the serial was
not returned or saved. The list contains familiar Nikon property, live-view,
and object operations covered by the prior review, plus `0x9535`, which is
not identified in the local reviewed references. Do not invoke `0x9535` or
any other unreviewed vendor operation. This confirms a working host-access
path for identity and capability inventory, not live-memory access. Reviewed
probe run, 2026-10-18; high confidence for the returned identity and list,
no claim about unknown-operation semantics. No response dump or firmware
data retained. See `camera-readonly-identity-method.md`.

F-259. A follow-up search of project research notes, source and tests, plus
the installed libgphoto2 PTP documentation and headers, found no local
mapping for advertised operation `0x9535` and no reviewed PTP operation that
reads runtime memory or the tracking worker's active translation table.
The identity probe remains the only camera method established as safe and
reviewed. Do not invoke the unknown operation. This closes the local-source
lookup branch; it does not prove no such interface exists. Read-only local
reference search, 2026-10-18; high confidence for the searched sources, no
camera contact or firmware data.

F-260. In a paused-QEMU, memory-only diagnostic, the tracking candidate routed
one fresh mode-0 decision with assignment `0x1184=77` and a constructed
Auto-area status record `(area=6, pair=0,0)` through the native start request,
changing the tracking pair to `(1,0)`. A second fresh decision with constructed
active status `(area=6, pair=1,0)` reached the native stop request and cleared
it to `(0,0)`; a held/no-decision control called neither path. This verifies
candidate call routing and the native request cycle only under the constructed
status contract. It does not verify natural camera status production, physical
button delivery, subject acquisition, or asynchronous completion. Private
paused-QEMU run summary, 2026-10-17; high confidence for the tested synthetic
path, no hardware contact or firmware data retained.

F-261. Owner-run test on the stock Nikon Z 30, firmware V1.20, with Fn1
assigned to Subject tracking: pressing and releasing Fn1 once displayed the
tracking target; holding Fn1 also displayed it, and the target remained after
release. A second Fn1 tap ended tracking; holding behaved like tapping. The
owner reports tracking did not activate until shutter half-press, after which
the target began following the subject. This supports a toggle-like native
control, a shutter half-press activation gate, and successful acquisition in
this scenario; it does not establish AE-L/AF-L delivery to the candidate
hook. Owner-run observation, 2026-10-18; no assistant camera command or
firmware data.

F-262. Repeated the pre-approved standard PTP GetDeviceInfo query after
verifying the Z 30 was present in the host USB registry. Sandboxed libusb
enumeration returned no matching device; the same identity-only query with
host USB access succeeded, reporting Nikon Corporation, Z 30, firmware V1.20.
The advertised operations include standard OpenSession and CloseSession
(`0x1002`/`0x1003`), which the separately documented event monitor requires.
The serial was omitted from probe output. This verifies present-day connection
and transport availability, not button events or runtime memory. Read-only
identity probe, 2026-10-18; no vendor operation or write.

F-263. The owner approved the documented 15-second PTP event monitor. Its
single attempt stopped during descriptor preflight because it did not find
exactly one default PTP interface with the required interrupt-IN endpoint.
The selector runs before device open, interface claim, OpenSession, or any
transfer, so no PTP command or event poll occurred. This shows only that the
active descriptors did not satisfy the probe's precondition; it does not
prove the camera lacks an event endpoint. A descriptor-only USB inspection is
prepared as a separate proposed method and awaits approval. No event data,
firmware bytes, or camera state was read; no setting was changed.

F-264. The owner approved the descriptor-only USB inspection. It found one
default Still Image PTP interface (class 6/subclass 1/protocol 1) with bulk-IN,
bulk-OUT, and interrupt-IN endpoints. The event endpoint advertises an
8-byte maximum packet, so the monitor's old minimum-12-byte check—not a
missing interface or event endpoint—caused F-263's preflight stop. Descriptor
inspection opened/claimed no device interface and sent no PTP data. The
monitor has been revised offline to request a full 24-byte event container
across smaller USB packets; this changed transfer behavior requires fresh
method-specific approval before another camera attempt. USB descriptor
inspection, 2026-10-18; no event data or firmware bytes.

F-265. The revised PTP monitor found the approved interface and endpoint,
opened a standard PTP session, and began interrupt-IN polling. The first
successful interrupt transfer returned zero payload bytes, which the then-
current code treated as malformed and used to stop early; no PTP event
container was received. The cleanup path attempted standard CloseSession, but
its acknowledgement was not reported. The owner authorized the same bounded
method to be rerun without renewed permission, with a warning before the
15-second window and an explicit start signal from the owner. The monitor was
updated so zero-byte transfers count as idle polls within that same time bound.
No event payload, property, image, or firmware data was obtained.

F-266. After the owner gave the requested start signal, the revised bounded
15-second PTP event monitor completed successfully on the connected Nikon Z
30. During the window the owner pressed AE-L/AF-L four times. The monitor
reported exactly four standard event containers, each code `0x4006`, each
with one parameter `0x501c`; no other event was reported and the 128-event
limit was not reached. PTP defines `0x4006` as DevicePropChanged, whose first
parameter is a device-property code; the PTP property table identifies
`0x501c` as FocusMeteringMode. The four-for-four temporal match is strong
correlation between those button presses and notifications for this property,
but does not prove that the event is a raw key event or explain the property
value transition. PIMA 15740 describes this UINT16 property as selecting the
automatic focus mechanism; it does not name Nikon's mode-specific values. The
monitor used only standard OpenSession/CloseSession and
interrupt-IN event polling; no property query, vendor operation, write, raw
packet, image, or firmware data was collected. Read-only bounded camera
observation, 2026-10-18; high confidence for event and reported button count,
moderate confidence for correlation, no claim about transition semantics.

F-267. In a second approved-method 15-second PTP event-monitor window, the
owner pressed AE-L/AF-L three times. The monitor completed normally and
reported two events, both `DevicePropChanged` (`0x4006`) for property
`0x501c` (`FocusMeteringMode`). No other event was reported and the event
limit was not reached. This confirms repeated notifications for the same
property during a second button sequence, but the two-for-three count means
the monitor does not expose a reliable one-event-per-press mapping. Combined
with F-266, it supports an association between AE-L/AF-L activity and changes
to the focus-metering-mode property, without identifying the exact state
transition, proving causality, or establishing the firmware input hook. The
run used only standard PTP session commands and interrupt-IN polling; no
property query, vendor operation, write, raw packet, image, or firmware data
was collected. Read-only bounded camera observation, 2026-10-18; high
confidence for the event result and reported count, moderate for association.

F-268. After offline review, the owner authorized one standard PTP
GetDevicePropDesc query for property `0x501c` on the connected Z 30. The
bounded probe opened a standard PTP session, sent only that descriptor request,
and received standard response `0x200A` (`DeviceProp Not Supported`) on
transaction 1. The response identifies `FocusMeteringMode` as unavailable
through this standard descriptor operation on this camera; it does not negate
the earlier `DevicePropChanged` event carrying `0x501c` (F-266/F-267), nor
reveal the property's value. The probe issued no property write, vendor
command, event poll, image/storage request, or firmware operation; it retained
no raw response. The response-status diagnostic reports numeric PTP
container/code/transaction fields only. Read-only PTP query, 2026-10-18; high
confidence for the returned status and command path. No inference about
tracking state or firmware hook.

F-269. Cross-checked the AF-related byte values from F-239 against the
people/animal Auto-area submode routes from F-221/F-222. The setter represents
plain Auto-area, people, and animal selection as base mode 6 with submodes 0,
1, and 2. Action 45 routes people submode 1 through separate configuration
helpers; plain Auto-area and animal submode 2 share the helper that calls
`0x1019596e`. That caller supplies input 0, which selects byte value 6;
`0x1019596e` selects 7 only when given input 1. Therefore the observed 6/7
choice follows that helper argument, not the people-versus-animal submode.
This does not establish what the byte means, and the separate people helpers
remain semantically unnamed. Read-only synthesis of F-218/F-221/F-222/F-239,
2026-10-18; high confidence in route/argument comparison, no conclusion on
feature semantics. No camera access or firmware bytes/dumps.

F-270. Re-audited action selector `0x10368b6e` against the verified image
and a four-case pinned-QEMU diagnostic. For selector 45 (`r7 == 0x2d`),
mapped states 0/1 call `0x1045a1ae`, while states 2/3 call `0x1045a21c`.
Helper `0x1045a1e6` belongs to the separate selector-27 (`r7 == 0x1b`)
branch, not action 45. In QEMU, tuples `(base=6, byte61=0, byte62=0/1)`
mapped to states 1/0 and both took `0x1045a1ae`; tuples `(6,1,0/1)` mapped
to states 2/3 and took `0x1045a21c` -> `0x10230866` -> `0x100775c6`.
This supersedes F-221/F-222's attribution of `0x1045a1e6` to action 45.
The tuple was injected at the mapper's stack snapshot boundary; it does not
prove natural Auto-area-to-tuple production. Verified-image Thumb decode and
four bounded QEMU runs, 2026-10-18; high confidence in action dispatch under
the supplied tuples, no claim about natural AF-state mapping. No camera access
or firmware bytes/dumps.

F-271. A disposable-QEMU diagnostic identified and exercised the native AF
status-copy bridge. Firmware routine `0x101925b0` copies two bytes from its
argument to context bytes `+0x61/+0x62` at `0xc237c7b4`; its caller at
`0x10076300` reads those bytes from the AF configuration object at
`0xc259ff0c+0x38/+0x39`. Starting from a synthetic mapper tuple `(6,0,0)`,
native action 45 called the plain Auto-area helper chain and changed the
configuration state to `(1,0)`. Calling the native bridge made the next
action snapshot `(6,1,0)`; that call took `0x1045a21c` -> `0x10230866` ->
`0x100775c6` and changed the configuration state back to `(0,0)`. Calling the
bridge again and action 45 a third time returned to the plain helper chain.
This verifies a software state cycle through native routines when the initial
tuple is constructed and the bridge is diagnostically invoked. It does not
verify that QEMU naturally schedules the status producer, that the UI reticle
appears, or that AF acquires a subject. Pinned QEMU 10.2.4, stock image,
memory-only guest instrumentation, 2026-10-18; high confidence in the observed
calls and state bytes, no camera or firmware modification.

F-272. A temporary loader overlay was assembled to test automatic arming at
the live-view-ready call and Auto-area setter continuation, with a one-shot
latch and the native status bridge. All five overlay regions loaded into the
disposable pinned-QEMU process, but the simulator halted during normal startup
before shooting-view setup: the display profile reported an unmodeled write
to `0x10000aaa` from `0xc2b1065a`. Enabling the documented no-lens test peer
did not change that result. The overlay never executed, so this run provides
no evidence about its hook behavior, readiness, or tracking. Stop this
simulator-fidelity branch rather than add a broad peripheral model; continue
with build-relevant static analysis of native AF state and hook contract.
Disposable pinned-QEMU attempt, 2026-10-18; high confidence in loader
placement and startup failure, no camera access, no firmware modification,
and no claim that the overlay is testable.

F-273. A static Thumb-call scan found one direct call to the native AF status
bridge `0x101925b0`, at `0x10076314`, inside update routine `0x10076268`.
That routine is directly reached from two sites: `0x10156ba0` passes input 0,
and `0x10159092` passes input 1. In the input-0 route, the bridge runs only
after the routine's AF-state comparison and callback checks; it is not a
per-frame refresh. This explains why the QEMU cycle needed an explicit bridge
call after the action changed the configuration pair. A live-view auto-arm
hook cannot assume the mapper snapshot updates itself; it needs a reliable
one-shot latch or a reviewed explicit refresh before using the snapshot as a
guard. The two event routes' precise relationship to native AF readiness and
the safety of either hook remain unproved. Verified-image decode and bounded
direct-call scan, 2026-10-18; high confidence in the direct-call sites and
control flow, no inference about undocumented indirect callers or hardware
timing.

F-274. Corrects F-272's QEMU startup diagnosis. The first temporary live-view
wrapper was 44 bytes, but only 24 bytes at its chosen address had been
verified as zero-filled; it overwrote the following 20 bytes of firmware.
Therefore the startup write failure at `0x10000aaa` was produced with a
corrupted disposable guest and is not evidence of a QEMU peripheral-model
limit. A replacement overlay placed all code within a separately verified
512-byte zero-filled cave, and normal QEMU startup reached live-view setup.
With a synthetic Auto-area tuple, the known ready callback entered native
action 45; its internal return was observed with `r0 == 1`, followed by the
explicit status-bridge call. The enclosing callback did not return within the
20-second diagnostic window and later observations were repeated AF-mapper
breakpoints, so this does not verify callback completion, a persistent
reticle, or subject acquisition. The previous F-272 stop-simulator-fidelity
conclusion is withdrawn. Next isolate the callback's completion/worker
interaction or test the wrapper through a normal guest-driven ready event;
keep any overlay temporary and simulator-only. Disposable pinned-QEMU run,
2026-10-18; high confidence in the cave-size correction and observed action
return, unresolved outer callback and user-visible behavior. No camera access,
firmware modification, or repository firmware bytes/dumps.

F-276. Refines the F-274/F-275 QEMU diagnosis. With the corrected 512-byte
cave and the stock live-view object's type-2 dispatcher (`0x104b912c`), the
overlay reached the selector-1 ready call, native action 45, and its internal
success return (`r0 == 1`). The QEMU device log then recorded an unmodeled
halfword write to `0x10000aaa`, value `0xaa`, from runtime code at
`0xc2b1065a`; the emulator pauses globally on that access. A private
diagnostic build accepted only that exact write as a no-op and immediately
stopped on a second halfword write from the same PC, `0x10000554 = 0x55`.
The `0xAAA/0x554` addresses and `0xAA/0x55` values are consistent with a
NOR-flash unlock sequence, but that interpretation is not confirmed. This
shows the corrected live-view test is blocked by an unmodeled MMIO/flash-like
sequence; the earlier overflowing wrapper still invalidates F-272's original
startup run, while F-274's broader claim that the unknown-write issue was not
a QEMU gap is superseded here. A single no-op does not model the command
protocol, and the dispatcher did not complete. Do not add guessed responses;
drop this simulator-fidelity branch unless static evidence identifies a
correct device contract that directly gates the named auto-arm build
decision. No reticle, acquisition, or testable patch was established.
Disposable QEMU with one exact-address diagnostic shim, 2026-10-18; high
confidence in both observed writes and the pause, medium-to-low confidence in
the flash-protocol interpretation. No camera access or repository firmware
bytes/dumps.



F-275. A focused rerun of the corrected F-274 overlay watched only native
action-45 entry, its internal return point, and the AF status bridge. The
guest loaded all overlay regions; firmware identity remained unchanged and
the pinned QEMU checkout stayed clean. The ready-path diagnostic reached
action 45 with selector 45, reached its internal return with `r0 == 1`, and
then called bridge `0x101925b0` with the expected configuration-source
pointer. The enclosing direct call to handler `0x102f57e2` still timed out
after 20 seconds, with one ignored stop reported by the thread-aware
diagnostic. Thus repeated mapper breakpoints were not required to produce the
timeout. This still does not establish whether the synthetic direct handler
call is waiting on its normal task-dispatch context or whether another
completion condition is missing; no reticle or acquisition was observed.
Next resolve the stock live-view task's type-2 dispatch arguments and run the
same overlay through that route, rather than directly invoking the handler.
Disposable pinned-QEMU run, 2026-10-18; high confidence in the three observed
native points and timeout, callback cause unresolved. No camera access,
firmware modification, or repository firmware bytes/dumps.

F-277. Cross-reference of the corrected auto-arm run with F-159 identifies
the stop more narrowly. F-159 mapped runtime code around `0xc2b10656` to the
shared cached flash identity/geometry initializer at `0xc2b1012c`; its LR
`0xc2b1013f` matches the LR captured at the F-276 stop. F-276's PC
`0xc2b1065a` is inside that same helper. F-159 found that information-getter
and erase/program wrappers share the initializer, but the outer caller and
operation were not captured; the stop does not identify an update, setting
write, or tracking-owned flash operation. The `0xAA/0x55` writes are
consistent with discovery-command setup, but no response or completion was
observed. Further flash-response modeling was already retired under F-159;
F-276 does not justify reopening it. Resume with the real-firmware tracking
hook/state contract, not a guessed flash device. Hash-verified static
cross-reference and bounded QEMU stop records, 2026-10-18; high confidence in
the PC/LR match and shared initializer attribution, outer caller and actual
flash operation unresolved. No camera access or repository firmware bytes.

F-278. A read-only decode cross-checks the AF byte written by `0x1019596e`.
The routine stores its input-selected 6 or 7 at the same absolute AF-object
byte later read by `0x1018cd9c`. That consumer proceeds only when the byte is
1, and only under additional context/flag conditions; it does not branch on
Auto-area people/animal submode. This confirms the byte participates in
broader AF state handling but gives no semantic label to values 6/7 and no
tracking-ready signal. The standard USB event monitor cannot expose this
internal byte; the earlier `FocusMeteringMode` events and unsupported standard
descriptor query do not identify it. Hash-verified static Thumb decode,
2026-10-18; high confidence for the same-address access and value comparison,
no conclusion on tracking semantics. No camera access or firmware bytes/dumps.

F-279. Traced one real-firmware writer of the native AF status pair used by
the mapper snapshot. Routine `0x10078aa0` writes `(1,0)` to the source bytes
at `0xc259ff0c+0x38/+0x39` and updates adjacent AF configuration fields. Its
direct caller is `0x10073ed2` at `0x1007445c`; that updater is reached through
`0x10078b50` and a bit-31 branch of event dispatcher `0x100746dc`. The path
to the pair writer additionally requires the event object's state checks at
`0x100743a6`-`0x100743bc`; no evidence ties those checks to Auto-area selection
or Subject tracking. This is a candidate natural producer of mapper input
`(1,0)`, not a named ready-state signal. Static Thumb call/data-flow scan,
2026-10-18; high confidence for the write and direct path, no conclusion on
event meaning or tracking semantics. No camera access or firmware bytes/dumps.

F-280. Corrected F-279's event-mask bit description and tested the traced
callback in pinned QEMU. At `0x100746dc`, the `lsls r0,r4,#0x1f` test selects
input bit 0, not bit 31. A bounded diagnostic call with synthetic mask 1
entered `0x10074492`, then followed the early path: the service check returned
1 at `0x100744bc`, and `r4` remained zero at `0x1007450e`, branching to
`0x100745f4`. The call completed with the mapper source pair still `(0,0)`;
the downstream updater and `0x10078aa0` pair writer were not reached. This
shows that the dispatcher is callable in QEMU but the synthetic input lacks
the native AF object context needed to test the producer. It does not prove a
QEMU peripheral gap or identify tracking readiness. Pinned-QEMU call from the
InitTask checkpoint, 2026-10-18; high confidence for the observed route and
unchanged pair, no conclusion on the event's real producer. No camera access
or firmware bytes/dumps.

F-281. Strengthened the F-269 route comparison for the people/animal
hypothesis. In the action-45 selector `0x10368b6e`, the Auto-area state-0/1
branch explicitly clears a local byte at `0x10368bc2` before calling
`0x1045a1ae`. That helper passes the byte through `0x10230832`, which reads
the byte and calls `0x1019596e`; the latter writes 6 for input 0 and 7 only
for input 1. The selector chooses this same route for Auto-area submodes 0
and 2; people submode 1 follows separate helpers. Thus the action-45 route
uses 6 in both plain Auto-area and animal mode, so 6/7 is not the People vs
Animals selection in that selector path. A separate caller at `0x10458dfe`
does pass 1, but only after checking an AF record byte at `+4` for 2 or 3,
along with configuration and native-helper gates. The record producer and
the meaning of values 2/3 remain unresolved; that separate path could still
represent an AF category. A standard USB PTP event window cannot expose the
stack byte or AF record, so repeating that test would not resolve this
question. Hash-verified static Thumb control/data-flow review, 2026-10-18;
high confidence for both caller arguments and their guards, no
feature-semantic conclusion. No camera access or firmware bytes/dumps.

F-282. Repeated the bounded event-dispatch QEMU test after the normal
synthetic live-view setup and after calling the native Auto-area setter with
value 600. The setter returned success, but the callback at `0x100746dc`
still entered `0x10074492` with the service result at `0x100744bc` equal to 1
and `r4 == 0` at `0x1007450e`; it exited through `0x100745f4`. The mapper
source pair at `0xc259ff0c+0x38/+0x39` remained `(0,0)`, and the AF updater
and pair writer were not reached. This shows the current synthetic live-view
and Auto-area stimuli do not create the AF object needed by this callback in
this QEMU setup. It does not show that the native callback or state writer is
unreachable on the camera. The test used a QEMU binary and custom machine
sources matching their private build manifest; the original firmware
identity check passed and the camera was not contacted. Next useful QEMU work
requires tracing a native AF-object constructor/registration path and using
it as the fixture; do not invent an EXMCU/ISP response. Bounded pinned-build
QEMU diagnostic, 2026-10-18; high confidence for the observed callback state
and unchanged pair, no conclusion on camera behavior. No firmware
bytes/dumps.

F-283. Re-read the native event dispatcher `0x100746dc` and tested the
combined mask `0x801`: bit 11 invokes initializer `0x10078c50`, then bit 0
invokes AF callback `0x10074492`. The hash-verified pinned-QEMU run completed
the synthetic live-view fixture and native Auto-area setter (value 600);
the initializer ran before the callback, but the service check at
`0x100744bc` still returned 1, the AF object at `0x1007450e` remained null,
and the source pair stayed `(0,0)`. The callback returned normally without
reaching the updater or pair writer. Thus the dispatcher's own initialization
bit does not supply the missing AF-object context in this fixture. This is a
bounded simulator result, not evidence about the camera. It narrows the next
useful trace to the object-list producer/registration consumed by
`0x101885e8`; do not add guessed peripheral behavior. QEMU binary, custom
source, and firmware identity checks passed; no USB/camera access and no
firmware bytes/dumps.

F-284. Rebuilt the private auto-arm overlay with an additional eligibility
check requiring base AF mode 6 and submode 1 (People) or 2 (Animal). The
submode guard is candidate logic only; the bounded QEMU type-2 live-view
callback did not return from the candidate wrapper during the diagnostic
window, and no observation showed the helper or native action entry. Thus the
run did not test the new gate, one-shot behavior, reticle or acquisition. The
owner states QEMU cannot establish complete camera readiness and has approved
testing a prepared patch on the connected camera. This result supports
stopping repeated full-callback QEMU attempts, not treating the candidate as
ready: it is still only a loader overlay, lacks a proven stills-only guard,
and has no installable-image audit. The next decision point is after an exact
camera-format candidate, static layout/ABI review, independent exact-edit
audit, and recorded recovery plan exist; unresolved reticle/acquisition and
runtime mapping can then be assigned to a bounded owner-run camera test under
the hardware gate. Candidate build and QEMU diagnostic, 2026-10-18; high
confidence for the bounded run's observations, no conclusion on camera
behavior. No camera write or firmware bytes/dumps.

F-285. Composed that private auto-arm overlay into a standalone Z 30 C 1.20
EG candidate using the verified original and a four-span exact-edit manifest:
the 512-byte code cave and three same-length hook branches. The project
builder accepted the pinned source and regenerated the native CRC. A separate
read-back audit found no body changes outside those spans, unchanged file
length, matching expected/replacement digests, valid stored CRC and zero CRC
residue. Independent Thumb disassembly verified the three branch destinations;
manual ABI review found 16-byte-aligned wrapper frames, saved callee-saved
registers/LR and preserved native setter return values. This makes the
candidate concrete, not hardware-validated: QEMU still did not reach the
helper/action entry, runtime executable mapping and worst-case live-view stack
remain unmeasured, and reticle/acquisition remain device-test items. [Nikon's
official Z 30 update instructions](https://downloadcenter.nikonimglib.com/en/download/fw/556.html)
describe the outer package on a camera-formatted SD card; [same-camera C 1.20
build documentation](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/build.md)
records the standalone EG as an installable format, but this exact candidate
has not been accepted by the camera updater. The camera enumerates at USB
level, but gphoto2 did not open a PTP session and no card is mounted; no
transfer or device write occurred.
Private candidate build and independent audit, 2026-10-18; high confidence in
exact edits/CRC and branch decode, no conclusion on updater/runtime behavior.
No firmware bytes/dumps.

F-286. Corrects F-285's transport status and sets the next risk threshold.
The camera was detected by gphoto2 at the PTP layer, and read-only summary
and storage listing calls completed; the storage reported was the removable
memory card. The private candidate has a local card-test copy, but no file was
uploaded, no updater was started, and no camera write occurred. The earlier
statement that gphoto2 could not open a PTP session and no card was available
is stale. Candidate construction and exact-span/CRC integrity checks are
complete, but QEMU did not prove the candidate's live-view callback returns,
and the worst-case callback stack remains unmeasured. Runtime mapping,
updater acceptance, reticle and acquisition are also unknown. Therefore the
right hardware-test threshold has not yet been met: resolve stack/context
headroom from a bounded static call-chain review, or have the owner explicitly
waive that named residual at the camera-test stage, and record the accepted
recovery risk and bounded test scope. Current AGENTS.md instructions prohibit
camera contact, so this is a decision record only; no hardware step was taken.
Observed historical PTP reads and private artifact audit, 2026-10-18; high
confidence for the reported operations and current repository rule, no
conclusion about camera behavior. No firmware bytes/dumps.

F-287. The owner explicitly overrode the current no-camera-contact rule and
approved one exact PTP card-copy operation. On gphoto2 2.5.32, the first
approved command using logical folder `/` failed before transfer because the
camera requires a `/store_...` folder. A read-only folder listing identified
`/store_00010001` as the card root. Retrying the same single-file copy to that
root failed with `PTP Specification Of Destination Unsupported`. Both
attempts exited before a file transfer; no candidate reached the card and
the updater was not started. `diskutil list external physical` could not use
DiskManagement in this host environment, and `/Volumes` showed only the
system and recovery volumes, so no card-reader volume is currently mounted.
The practical transfer route remains a card reader. The exact standalone-EG
candidate remains local and unchanged. The owner authorization covers the
attempted PTP card-copy purpose; it does not make updater acceptance, the
open stack/context review, or installation readiness pass. Owner-directed
PTP write attempts and host volume check, 2026-10-18; high confidence in the
reported command results and absence of transfer, no conclusion about
updater/runtime behavior. No firmware bytes/dumps in the repository.

F-288. Re-decoded live-view handler `0x102f57e2` from the hash-verified
Z 30 C 1.20 module using its mapped base. Its load at `0x102f57fc` reads
global byte `0xc181b4b4`, tests bit 6, and conditionally calls `0x104bd3c0`;
both paths rejoin before the live-view selector setter `0x104b9116` at
`0x102f5810`. This local test does not gate the common live-view transition
and does not establish still-photo eligibility. No still/movie semantic
mapping was found for the byte or its bit. The private auto-arm candidate is
unchanged and still lacks a proven still-photo guard. Hash-verified offline
Thumb decode, 2026-10-18; high confidence in local control flow, unknown
meaning of the global bits/helper. No firmware bytes/dumps.

F-289. Re-validation of the `0x102f2990` mode-entry callback added no new
build evidence: F-089 already records its argument comparisons, lack of
direct callers, and pointer-table dispatch, while later decoding confirms
additional branches without resolving the dispatcher or mapping values to
still/movie semantics. Do not treat this repeated inspection as progress or
use the values as a patch guard. The still-photo eligibility gap in F-288
remains open. Hash-verified static Thumb decode, 2026-10-18; high confidence
in the repeated control-flow observations, unknown producer and semantics.
No firmware bytes/dumps.

F-290. The APPLV task creation record requests `0x2000` bytes (8 KiB) for
its stack. In the captured creation call for object `0xc1821d44` and entry
`0x10235577`, the request descriptor at `r2` has `0x2000` at offset `+8`;
native wrapper `0x10219876` loads that field and forwards it in the scheduler
creation arguments to `0x10035fdc`. This resolves the configured stack-size
input, not peak usage or available headroom: the current candidate calls
property accessors and action 45 inline from a live-view callback, and its
worst-case combined native/candidate stack depth has not been bounded. The
candidate remains NO-GO. Captured native task-creation arguments and
hash-verified Thumb decode, 2026-10-18; high confidence in the forwarded
request value, scheduler allocation semantics inferred from the wrapper
contract, peak stack use unknown. No firmware bytes/dumps.

F-291. Corrects F-288's bit number and rejects its byte as an Auto-area or
still-photo guard. At `0x102f57fc`, the handler loads byte `0xc181b4b4`,
then shifts it left by 25 and branches on the sign flag, testing bit 7 (not
bit 6). Static call sites in unrelated subsystem routines also read this
same byte, test different bit positions, and conditionally call
`0x104bd3c0` before continuing their ordinary operation. The repeated
cross-subsystem pattern is consistent with a shared instrumentation/filter
gate, not a camera shooting-mode predicate; its exact purpose remains
unresolved. Both branches still reach the live-view selector setter. Do not
use this byte as the stills/Auto-area eligibility condition. Hash-verified
Thumb decode and cross-reference sample, 2026-10-18; high confidence in the
bit number and repeated call pattern, inferred instrumentation role, no
photo/movie semantics established. No firmware bytes/dumps.

F-292. The candidate on the owner's SD card was verified to match
`EG209020-autoarm-test-01.BIN`, with size 33,939,514 bytes and SHA-256
`6a31dc39264fa73459d68605f9ce3a1f69c9017de4f2c99f980c7bdfe6fc52de`.
Despite the intact copy, the Z 30 Firmware version screen showed only Done
and Delete firmware update files; it offered no Update option and no update
began. This candidate is not installable as presented. It preserves the
original C 1.20 module-version metadata and the camera is on C 1.20, so a
same-version eligibility rejection is plausible, but the exact refusal rule
has not been established. Do not rename or bypass updater eligibility.
Observed card identity and owner-reported menu result, 2026-10-18; high
confidence that no update was offered or started, inferred same-version
cause. No firmware bytes/dumps.

F-293. The upstream Wonder Lantern Z 30 C 1.20 project reports that its
standalone `EG209020.BIN` was installed on a Z 30 running C 1.20. This
weakens the hypothesis that the base camera/module version alone prevents
same-version standalone EG installation. It does not establish whether that
upstream image changed the eight-byte version-like metadata at offset `0x24`,
or whether its other edits affect eligibility. Compare its documented build
spans and then trace the native selector callback for this field before
changing our candidate. Upstream project build and verification documentation,
checked 2026-10-18; high confidence for the maintainer's published report,
no independent validation of our candidate. No firmware bytes/dumps.
([build guide](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/build.md),
[verification record](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/verification.md))

F-294. Read-only decode of post-CRC checker `0x101ce324` confirms that it
loads a runtime selector, bounds it to a 16-entry range after subtracting 6,
and dispatches through a Thumb table branch. The selected cases call distinct
policy handlers; several construct or format version-like data through
`0x101d3f14`. This is consistent with a policy decision controlling whether
the parsed EG is offered for update, but the selector's producer/value on the
standalone-EG route and the relevant handler's acceptance condition are not
yet traced. Do not infer that offset `0x24` alone is the cause or change it
without resolving this path. Hash-verified static Thumb decode, 2026-10-18;
high confidence in the dispatch structure and called handlers, unknown
runtime selector and eligibility semantics. No firmware bytes/dumps.

F-295. Cross-checking checker `0x101ce324` against the selector getter
`0x101cf8cc` shows its selector is the shared discovery-type byte at the
updater record: `0x101cf8cc` returns the encoded-header flag only for type 4,
and `0x101ce324` reads the same byte before its table branch. The standalone
EG discovery row is type 2, so subtracting 6 underflows the unsigned selector
and takes the default path, bypassing the 16-entry policy table whose some
handlers format version-like metadata. F-294's relevance to the missing
Firmware-version menu option is therefore superseded: this post-CRC dispatch
does not reject the standalone EG on those metadata callbacks. The earlier
parser and menu eligibility decision remain the target. Hash-verified static
Thumb decode plus F-140's discovery-type mapping, 2026-10-18; high confidence
in selector identity and type-2 fallback, menu-offer cause still unknown. No
firmware bytes/dumps.

F-296. The standalone type-2 parser `0x101cd3cc` rejects oversized files,
failed reads and, conditionally, a four-byte compatibility-field mismatch.
For the candidate, the compatibility field at `0x10` is preserved from the
same C 1.20 source module, so that check should pass whether the character
class gate runs or skips it. The parser then reads eight bytes at `0x24`,
formats them through `0x101cd13e`, and proceeds to set execution type 3 and
component count 1; the formatter result is not used as a success predicate.
Combined with F-295, this finds no static same-version rejection in the
standalone parser or the post-CRC type-2 path. The candidate should reach
the parser's success return if the camera opens and reads the card file
normally. The missing Update option therefore remains unexplained in the
card discovery/UI path or an untraced gate. Hash-verified static Thumb decode
and candidate protected-field audit, 2026-10-18; high confidence in observed
control flow, inferred expected pass for preserved compatibility bytes,
unknown camera-side discovery result. No firmware bytes/dumps.

F-297. A fresh host check on 2026-10-18 found no Z 30: `gphoto2
--auto-detect` listed no camera, and the previously approved descriptor-only
USB probe found zero matching devices. This establishes only that the camera
was not visible to the host during this check; it does not establish power,
cable, card-format, or updater-menu state. No PTP command or camera write was
attempted. Observed read-only host enumeration, 2026-10-18; high confidence
for device absence from these host interfaces at that moment. No firmware
bytes/dumps.

F-298. Hash-verified static Thumb control-flow through firmware-menu wrapper
`0x10234274` and scanner `0x101ce206` resolves the standalone discovery
result contract. The wrapper passes zero to the scanner for the all-row
search. The scanner iterates eleven discovery rows; the standalone EG row
uses the filename-match path and calls parser `0x101cd3cc` only after a match.
Parser result 1 registers the parsed record and takes the scanner's zero
return path; exhausted or non-success rows take its return value 3. The menu
wrapper branches on this result, taking a separate helper path only for zero.
This narrows the missing Update symptom to file discovery/open/name match,
parser rejection, or a later UI condition; it does not reveal which occurred
on the camera or prove the helper path is the visible Update row. Hash-verified
static Thumb decode of the verified original, 2026-10-18; high confidence in
the control flow, no camera runtime observation. No firmware bytes/dumps.

F-299. Following the scanner wrapper one caller higher resolves the menu
callback's two outcomes. Callback `0x10594c1c` calls `0x10234274`; a nonzero
return exits through the callback's success return, while zero stores a separate
message state and calls message helper `0x1033c88c`. The wrapper's nonzero
outcome is reached only when the scanner returns zero after a successful
type-2 parser result; in that case it copies a fixed-size descriptor template
into the caller's output buffer. This makes the reported absence of Update
consistent with the no-accepted-file/fallback-message branch. The camera's
actual callback result and exact visible string remain unobserved; this does
not prove which filesystem or parser condition failed. Hash-verified static
Thumb decode, 2026-10-18; high confidence in branch structure, no runtime
observation. No firmware bytes/dumps.

F-300. Static decode of the standalone row's filename matcher `0x101ce106`
shows that media-state bits select one of two directory-path candidates; the
updater then opens/enumerates entries through filesystem helpers and compares
entry names against the row pattern, including wildcard characters. A match
is required before scanner `0x101ce206` invokes the standalone parser. This
makes card/volume selection and root-file visibility the next pre-parser
checks; no runtime path or directory listing was observed. Hash-verified
static Thumb decode, 2026-10-18; high confidence in control flow and matcher
behavior, path-string semantics not independently decoded. No firmware
bytes/dumps.

F-301. The owner confirms that the SD card carrying the candidate was
formatted in the Z 30 before the updater-menu test. A fresh host check after
this clarification still found no camera via `gphoto2 --auto-detect` or the
approved descriptor-only probe. The format precondition is therefore known by
owner report, but the camera's current menu state and whether it is presently
powered/connected remain unknown. Owner report and read-only host check,
2026-10-18; high confidence in the report and host result, no independent
card-filesystem inspection. No firmware bytes/dumps.

F-302. A bounded pointer-resolution pass on the standalone filename matcher
`0x101ce106` found that its two directory-path choices are loaded indirectly
through runtime RAM pointer locations; the static image does not embed the
resolved path values at those references. This pass did not locate the
runtime producers or establish which value denotes the SD-card root. It
therefore does not resolve why the camera did not offer Update. The owner
confirms the card was camera-formatted, but the next useful evidence remains
a fresh Firmware-version menu result and, if Update is still absent, a direct
check that the candidate is at the selected card root. Hash-verified static
Thumb pointer analysis, 2026-10-18; high confidence in the indirect runtime
lookup, unresolved path semantics and camera-side selection. No firmware
bytes/dumps.

F-303. Using the verified original's standalone discovery row (type 2), the
native filename wildcard pattern was compared in memory with the candidate's
canonical card filename `EG209020.BIN`; it matches. This rules out a mismatch
between that canonical filename and the standalone row pattern. It does not
prove that the camera selected the SD-card root, enumerated that entry, opened
or parsed it, or offered Update. The next useful evidence remains the fresh
Firmware-version menu result; if Update is still absent, verify root-file
visibility on the selected card path. Hash-verified row/pattern comparison,
2026-10-18; high confidence in the match, no runtime discovery or parser
observation. No firmware bytes/dumps.

F-304. The owner reports that the camera is reading the SD-card root. This
closes the selected-root question by owner observation, but does not by itself
confirm that `EG209020.BIN` is visible as an updater entry, opened, accepted by
the standalone parser, or surfaced as an Update option. At the time of this
entry the earlier screen offered only Done and Delete firmware update files;
F-305 records the owner's confirmation that this remains the current result.
Owner report, 2026-10-18; high confidence as a report, not independently
verified. No firmware bytes/dumps.

F-305. The owner confirms the Firmware version screen still offers no Update
option, after clarifying that the camera is reading the card root. This
confirms the candidate is still not offered for installation; it does not
distinguish whether the exact filename is absent from the updater's file list,
the file cannot be opened/read, the parser rejects it, or a later UI gate
filters it. Do not ask the owner to repeat the menu check or attempt install.
The next work is a bounded offline trace of the directory enumeration/open,
parser return, and menu-row construction conditions, limited to finding a
concrete candidate-specific gate or documenting that the updater's runtime
result is required. Owner report, 2026-10-18; high confidence as a report, no
firmware bytes/dumps.

F-306. A fresh bounded decode of callback `0x10594c1c` corrects F-299's
description of the accepted-file path. When the scanner reports an accepted
file, the callback skips the fallback-message helper, but continues into a
second helper at `0x102342a6`, passing it a pointer to a callback-local stack
buffer. That helper runs additional setup calls, populates a descriptor-like
record and returns status; the callback then branches on status before
returning. Thus parser acceptance does not directly establish that the
Firmware-version UI exposes Update. The helper's exact role, descriptor
fields and status meanings are not yet resolved. This identifies a concrete
post-scan menu-record path worth one bounded trace of its input record, return
values and consumer. Hash-verified Thumb control-flow and call-argument decode,
2026-10-18; high confidence in the call/record flow, semantics unconfirmed.
No firmware bytes/dumps.

F-307. The post-scan path is now narrowed to a record-construction helper.
After the accepted-file branch, callback `0x10594c1c` passes a local stack
buffer to `0x102342a6`. The helper has guarded setup calls; on its construction
path it writes a status/type byte at record offset `+4` and copies fixed-size
fields into the record beginning at `+5` and `+0xf`. The callback then checks
the helper's return status through multiple branches. These fields and return
codes are not yet mapped to Firmware-version menu actions, so this does not
identify why Update is absent. Next, trace those record fields/status values
to their consumer, bounded to finding whether a UI eligibility check can hide
an otherwise accepted standalone EG. Hash-verified Thumb call-context and
write-offset analysis, 2026-10-18; high confidence in offsets and control
flow, semantic mapping unknown. No firmware bytes/dumps.

F-308. The callback's status consumer has been decoded one step further. After
`0x102342a6` returns, `0x10594c1c` reads the first word of the local record
and distinguishes values 1, 2, 4 and 8. Value 1 writes callback result 4;
values 2, 4 and 8 take separate branches; all other values write result 3
and use a common reporting helper. This confirms the post-scan record controls
distinct callback outcomes, but the meanings of those outcomes and their
visible Firmware-version menu effects remain unknown. The next bounded step
is to trace the record's producer and the callback's result consumer to a menu
action/label or prove that the chain remains runtime-only. Hash-verified Thumb
branch/field flow, 2026-10-18; high confidence in tested values and assignments,
semantics unknown. No firmware bytes/dumps.

F-309. An exact pointer-reference scan finds the callback pointer for
`0x10594c1c` once, inside a contiguous five-entry Thumb callback table. The
surrounding descriptor includes property key `0xc181a0d8`; four neighboring
callbacks are at `0x10594bf4`, `0x10594c3e`, `0x10594cb4`, and `0x10594ce2`.
This places the callback in a registered callback family, but does not by
itself identify the property's meaning or the Firmware-version menu consumer.
Exact direct references to the table's nearby addresses were not found, so
the registration-table owner remains unresolved. Next trace the table's
dispatcher/registration path once; if it does not connect to a menu action,
stop the static updater branch and retain runtime visibility as the unresolved
issue. Hash-verified pointer-table read and exact-reference scan, 2026-10-18;
high confidence in table membership, semantic role unknown. No firmware
bytes/dumps.

F-310. Reviewing the actual private auto-arm source found that candidate 01
was explicitly a diagnostic variant: it omitted the native status-copy bridge
after action 45. F-271 shows that bridge `0x101925b0` copies the AF pair into
the context bytes used by the tracking path, and F-273 shows the normal
producer is event-driven rather than a per-frame refresh. A separate private
candidate 02 now copies configuration bytes `+0x38/+0x39` to an aligned
two-byte stack pair and calls that bridge after action 45 succeeds. The
candidate was rebuilt from the verified original with four exact spans;
independent builder read-back reports unchanged length (33,939,514 bytes),
254 changed bytes, valid native CRC, and candidate SHA-256
`f5a392d3e347f5afdb111cec55f7fc5fedc5ed26e5d94e94752f74ded176abd1`. A
separate static check verifies all three hook branch destinations and the
bridge/config literals. The targeted QEMU call timed out
without usable observations, so it does not show whether the bridge or action
completed in that run. Candidate 02 is private and has not been copied to the
SD card; the owner's latest no-Update report predates it and is not acceptance
evidence for candidate 02. It is not ready for installation or a camera test,
and it does not establish reticle/acquisition behavior. Build/audit output and
bounded QEMU attempt, 2026-10-18; high confidence in the exact edit and static
checks, no runtime conclusion. No firmware bytes/dumps.

F-311. Static ABI review of candidate 02's native status bridge call confirms
that its argument and alignment match the stock caller. The candidate saves
`r4-r6,lr` (16 bytes), reserves an aligned 8-byte local area, copies the
configuration pair from `0xc259ff0c+0x38/+0x39`, and passes that area's address
in `r0`. Native bridge `0x101925b0` saves `r4,lr` (8 bytes), calls the same
pre-copy helper used by the stock caller, copies the two bytes to tracking
context `+0x61/+0x62`, restores `r4,lr`, then branches to its stock cleanup
helper. The native action's observed plain Auto-area route adds a 24-byte
action frame, a 24-byte state-operation frame, a 16-byte state-helper frame,
and a 32-byte event/state helper frame. Its conditional continuation reaches
additional 8-byte helper frames on separate branches. The live-view callback
itself saves 48 bytes. On the bridge path, the pre-copy helper tail-branches
to an 8-byte synchronization frame and then calls a native dispatcher; the
post-copy cleanup helper tail-branches to another native dispatcher. Candidate
wrappers preserve their saved registers and keep SP 8-byte aligned at calls.
One decoded event-helper branch returns through `0x1022fbf4` into
`0x10225012`, whose explicit frame is 48 bytes; with the candidate and live
callback frames, this gives a 224-byte lower bound along that possible
action/state route, before its indirect callee and other omitted frames. The
bridge path separately reaches native synchronization dispatchers. These
observations do not bound the transitive native event/state and synchronization
helpers or the complete callback peak against APPLV's requested 8 KiB stack.
Static disassembly cannot establish that peak, and the focused QEMU attempt
remains inconclusive. Candidate 02
therefore remains NO-GO for a camera test pending a defensible full call-chain
stack bound or a specifically accepted stack-risk waiver. Hash-verified
original Thumb disassembly and private candidate source review, 2026-10-18;
high confidence in local ABI/frame observations, incomplete peak-stack proof.
No camera access or firmware bytes/dumps.

F-312. The bounded stack trace reaches an indirect dispatch on the native
Auto-area action path. State helper `0x10230832` calls owner-check helper
`0x1019596e`; a conditional continuation calls `0x1022fbf4` with a pointer to
a two-word record. On its accepted branch, `0x1022fbf4` loads both words and
tail-branches to `0x10225012`. That routine makes an indirect call through a
register derived from the supplied record. The dispatch frame itself saves
48 bytes, producing a 224-byte explicit-frame lower bound when combined with
the candidate, live-view callback, action and observed state frames. The
record's runtime producer and indirect callee are not resolved in the static
trail, so the callee's frame and further call depth cannot be bounded from
these observations. This is the specific remaining stack-analysis blocker;
candidate 02 stays NO-GO for a camera test under the current readiness gate.
Hash-verified original Thumb disassembly and call-argument trace, 2026-10-18;
high confidence in the argument and indirect-call flow, unknown runtime
callback target. No camera access or firmware bytes/dumps.

F-313. Corrects F-312's interpretation of the action-path record. Caller
`0x10230832` explicitly stores zero to both words of its local record before
passing it to `0x1022fbf4`; on the accepted owner branch, `0x10225012` receives
zero and branches around its initial indirect callback at `0x1022502c`.
It then continues into a table-driven event-processing body with
state-dependent direct calls across `0x102250a6`–`0x1022568a`. Thus the
record's callback producer is not missing on this path; the callback is
intentionally null. The remaining stack question is the exact event-dispatch
branch and its transitive callees under the live-view task context. The body
has many direct calls and conditional table routes; a complete peak bound is
not established here. This preserves the NO-GO status but narrows the next
static task to the zero-record event-dispatch path. Hash-verified original
Thumb disassembly and argument flow, 2026-10-18; high confidence in the zero
record and skipped first callback, event branch and peak stack unresolved. No
camera access or firmware bytes/dumps.

F-314. The zero-record dispatcher path is gated by a runtime mask word.
After `0x10225012` skips its null initial callback, it calls `0x10066714`,
which returns 0 and takes the early-exit branch when word `0xc18a7540` is
nonzero; zero returns 1 and enters event processing. Helpers `0x1006670a` and
`0x100666f8` set and clear bits in this word using OR/AND operations, and the
full image contains direct callers with masks including `0x1`, `0x2`, `0x4`,
`0x8`, `0x10`, `0x20`, `0x80`, `0x100`, `0x200` and `0x400`. This is a shared
runtime bitfield, not a pointer. The branch in the candidate's live-view
context depends on which operations currently hold bits; that runtime value
and its feature-level meaning are unknown. Candidate 02 remains NO-GO because
the zero-mask event path's transitive stack is not bounded. Hash-verified
original Thumb disassembly, helper caller scan and exact global-word
reference scan, 2026-10-18; high confidence in bit operations and observed
caller masks, unknown runtime mask and semantics. No camera access or firmware
bytes/dumps.

F-315. One action-45 state-handler branch reaches the zero-record event
dispatcher. Handler `0x1045a1ae` calls `0x10230832` after clearing an
AF-related object field and before posting its internal event. `0x10230832`
checks the AF-record type and service state, then passes a zeroed pair through
`0x1022fbf4` to `0x10225012`; that dispatcher gates its large event body on
the shared mask word `0xc18a7540`. Observed callers of `0x1045a1ae` include
`0x10368bc6` (event-code route) and `0x10458dfe` (record-callback route).
Neither this helper nor those caller slices directly set or clear the mask.
Thus the gate's runtime value remains ambient and unresolved; this trace
neither proves the deep body is skipped nor bounds its stack. This is the
action/state chain, distinct from candidate 02's separate status-copy bridge
`0x101925b0`, whose synchronization calls also remain unbounded. Candidate 02
remains NO-GO. Hash-verified full Thumb disassembly and direct-call
comparison, 2026-10-18; high confidence in reviewed direct edges and lack of
local mask mutation, unknown ambient state. No camera access or firmware
bytes/dumps.

F-316. A bounded structural scan of the event-processing body in
`0x10225012` (`0x102250a6`–`0x1022568a`) found 103 direct call sites to 70
distinct routines. No register-indirect call or table-branch instruction is
present in that body range, but the direct callees' transitive call paths are
not bounded by this scan. The previously measured dispatcher/candidate local
frames therefore do not establish peak stack use against APPLV's 8 KiB
allocation. Candidate 02 remains NO-GO absent a transitive bound or a named
owner waiver. Hash-verified full Thumb disassembly, call-instruction scan,
2026-10-18; high confidence in the bounded body-level count, no inference
about transitive stack use. No camera access or firmware bytes/dumps.

F-317. The two synchronization calls in candidate 02's separate status-copy
bridge resolve to fixed ARM-mode service stubs. Bridge `0x101925b0` calls
`0x10197c76`, which tail-branches through `0x10199bc6` to ARM entry
`0x100361e8`; after copying the AF pair, its cleanup helper reaches
`0x10199baa` and the ARM entry `0x100364e0`. Each stub saves `r4` and `lr`
(8 bytes total), issues SVC #6, restores them, and returns; neither stub makes
a further firmware call. This bounds the visible firmware-side wrapper frames
on this bridge path, but not the implementation or stack behavior behind SVC
#6. It does not resolve the separate action-45 state-handler path through
`0x10225012`, whose deep event body remains unbounded. Candidate 02 remains
NO-GO. Hash-verified module disassembly in ARM mode, 2026-10-18; high
confidence in stub instructions and local frames, SVC internals unresolved.
No camera access or firmware bytes/dumps.

F-318. The zero-mask event body's completion path has a conditional runtime
callback beyond its 70 direct callees. After the event loop, `0x10225012`
calls `0x10062a6a` with value `0x3f` at `0x10225670`. That helper checks bit
63 in a related runtime bitset via `0x100624d2`; when set, it clears the bit,
then may invoke the callback pointer stored at runtime address `0xc23a63b4`
through `bx r12`. Neither the bit state nor pointer value is established by
static contents. Thus the dispatcher has a live state-dependent tail whose
callee frame/depth is not bounded by F-316; this does not prove the callback
is taken on the camera. Trace the bit-63 setter and callback-slot producer if
they are statically recoverable. Candidate 02 remains NO-GO. Hash-verified
full Thumb disassembly and direct data-flow trace, 2026-10-18; high confidence
in the condition and indirect branch, runtime state/target unknown. No camera
access or firmware bytes/dumps.

F-319. Correction to F-318: `0xc23a63b4` is passed to the synchronization
service at `0x10199bc6` with timeout `0x3e8`; it is not the callback slot.
When `0x10062a6a` finds bit 63 set, it loads the callback pointer from the
runtime field at `0xc18a748c` (derived from the singleton address
`0xc18a74a8`) and invokes it indirectly through `bx r12`. The tested bitset
uses the data pointer field at `0xc18a74a4`. The generic set-bit helper
`0x1006248e` has one direct call site, in `0x10062998`; that routine loops
over byte IDs supplied at runtime and sets them in a different bitset based
at `0xc18a74b0`. Static evidence does not show that this list includes 63 or
that it writes the tested bitset. The callback field's producer and runtime
value remain unknown, so the transitive stack remains unbounded and candidate
02 remains NO-GO. This supersedes F-318's identification of the callback
address. Hash-verified full Thumb disassembly and local data-flow/xref review,
2026-10-18; high confidence in the corrected address arithmetic and direct
call-site count, runtime list and callback unresolved. No camera access or
firmware bytes/dumps.

F-320. A full-image static word-reference scan finds only the helper's own
literal reference to singleton base `0xc18a74a8`; it finds no absolute word
reference to computed callback-field address `0xc18a748c`. The generic
set-bit wrapper `0x10062998` likewise has no direct call-site or static
function-pointer reference in the linked image; its entry path and the
runtime byte list it consumes are unresolved. This narrows the missing
producer to a computed/pointer-based registration or runtime initialization
path, but does not exclude aliases or indirect dispatch. No static callback
target or peak-stack bound is established; candidate 02 remains NO-GO. The
next useful static pass is to follow the registered callback-table/initializer
path for this synchronization domain once, then pivot away if its runtime
registration cannot be identified. Private linked-image xref scan and
hash-verified disassembly, 2026-10-18; high confidence for exact absolute-word
and direct-call xref absence, no conclusion about computed references. No
camera access or firmware bytes/dumps.

F-321. The conditional callback in F-319 has a statically recoverable
initializer and bounded target path. Initialization routine `0x1006516c`
loads callback target `0x1006499b` and calls setter `0x100628de`; the setter
stores that value in field `0xc18a748c`. The same initializer passes the
callback to registration helper `0x10060e6a`. On the `0x10062a6a` dispatch
path, `r0` is loaded from the fixed literal at `0x10062bfc` and `r1` receives
the bit index. The callback entry `0x1006499a` copies `r0` to its selector,
initializes the return value to zero, and returns immediately for selectors
at least 5; the fixed selector on this path exceeds that limit. It makes no
call and allocates no stack, so this conditional callback adds no target-frame
depth. This corrects F-319/F-320's unresolved callback-producer/target
assessment. The action path's remaining direct callees and peak stack are
still unbounded by F-316, so candidate 02 remains NO-GO. Hash-verified full
Thumb disassembly and literal/data-flow review, 2026-10-18; high confidence
in registration, fixed selector and early-return path. No camera access or
firmware bytes/dumps.

F-322. Corrects F-321's callback-target decode. The initializer literal points
to Thumb target `0x10064a9b` (entry `0x10064a9a`), not `0x1006499b`. At the
`0x10062a6a` call site, the fixed first argument is `0x04100004`; the target
transforms it to selector 3 and enters switch case 3 at `0x10064aee`. That
case saves 16 bytes and calls `0x10060ecc`, `0x10060cde`, `0x10061aa6`, and
`0x100660f2`, so its transitive stack is unresolved. F-321's claim of a
no-call, zero-frame callback is withdrawn; candidate 02 remains NO-GO. This
also corrects F-319/F-320's set-bit helper accounting: `0x1006248e` has two
static call sites (`0x100628a0` and `0x100629b6`); `0x1006289a` tail-branches
to it for fixed IDs, while `0x10062998` loops over a runtime byte list. The
tested bitset and that list consumer use different bases. Hash-verified full
Thumb disassembly and literal/case data-flow review, 2026-10-18; high
confidence in target, selector and direct callees, transitive stack unresolved.
No camera access or firmware bytes/dumps.

F-323. Traces the actual selector-3 callback branch found in F-322. Its local
path is: `0x10064a9a` (16-byte frame), table mapper `0x10060ecc` (selector
and event byte 63; returns without a call), `0x10060cde` (receives byte 4 and
takes its state-check path), `0x10061aa6` (8-byte frame, calls `0x10061930`),
then `0x100660f2` (24-byte frame). The last helper loops over a runtime
listener count at `0xc18a74d5` and function-pointer entries beginning at
`0xc18a7520`; each entry is called through `0x10061072`, which tail-dispatches
the generated event code. The table/count have no statically decoded contents,
so subscriber callback frames and total peak remain unknown. The 40-byte local
frame in `0x10061930` is on a preceding registration/service call path, not
simultaneous with the later listener loop. This gives a precise unresolved
callback risk rather than treating the whole 70-callee body as opaque.
Candidate 02 remains NO-GO. Hash-verified Thumb control-flow and global-base
trace, 2026-10-18; high confidence in call order, local frames and runtime
table accesses; dynamic listener contents unresolved. No camera access or
firmware bytes/dumps.

F-324. Continued the F-323 listener-table trace by following the shared base
`0xc18a74d4` through its literal-pool references. The broadcast helper
`0x100660f2` itself is read-only with respect to the listener count and
pointer array: it uses the count byte at `+1`, then reads pointers from `+0x4c`
and dispatches them. The first-pass base-reference sweep did not identify a
statically traceable subscriber-registration writer; the other inspected
references belong to adjacent state/configuration paths. This does not prove
there is no computed or external registration path, so callback stack depth
remains unresolved. Stop this listener-table branch and pivot to a direct
AF-ready/reticle hook search. Candidate 02 remains NO-GO. Hash-verified
Thumb disassembly and bounded base-reference review, 2026-10-18; high
confidence in the broadcast's read-only behavior, moderate confidence in the
bounded search disposition. No camera access or firmware bytes/dumps.

F-325. Reviewed candidate 02's private source against the owner's persistent
auto-arm behavior. Its helper requires the native live-view-ready flag, base
AF-area mode 6, and People/Animal submode 1 or 2. The submode-setter hook calls
that helper after the native setter when live view is already active; the
live-view-ready hook calls it when that transition occurs after the AF mode
selection. The mode hook clears the one-shot latch when leaving mode 6. On an
eligible transition, the helper skips a duplicate action when its latch or
the copied AF status byte says tracking is already armed; otherwise it calls
native action 45, copies the native AF status pair through `0x101925b0`, then
sets the latch on success. This source-level structure covers the two
transition orderings in the requested behavior, so no new trigger point was
identified in this pass. It does not prove correct native timing, completed
dispatch, reticle visibility, or half-press acquisition; the focused QEMU call
timed out, and dynamic callback stack remains unresolved. Candidate 02 stays
NO-GO. Private source review, 2026-10-18; high confidence in stated branch
structure, no runtime conclusion. No camera access or firmware bytes/dumps.

F-326. A stock pinned-QEMU startup populated the runtime event-listener table
with one stable callback target, Thumb entry `0x1022adee` (three consecutive
samples). Static control flow from the action-45 state-handler selector-3
case emits event `0xB5` through the shared broadcast, which passes the event
code and payload to that listener list. The listener's frame is 88 bytes
(28-byte saved-register frame plus 60 bytes of locals); its `0xB5` switch arm
reaches setting/value translation helpers and a further native notification
helper. This replaces the prior claim that the listener target itself was
unknown, but does not establish that a normal QEMU action-45 run completed
this callback or bound the helper/SVC tail. The complete transitive stack,
reticle visibility, half-press acquisition, and candidate behavior remain
unverified; candidate 02 stays NO-GO. Runtime table sampling plus
hash-verified Thumb control-flow trace, 2026-10-18; high confidence in the
sampled target and static branch, moderate confidence that this closes the
runtime dispatch target under normal table stability. No camera access or
firmware bytes/dumps.

F-327. Followed F-326's target through the actual stock event path in pinned
QEMU: after standard assisted startup, a diagnostic call to the native
selector handler with selector event `0x04100004` and payload 1 emitted
`0xB5`, entered listener `0x1022adee`, and returned to the diagnostic
sentinel. Breakpoints across the branch observed a lowest SP of
`0xc2bacf30` from an entry SP of `0xc2bacfe0` (176 bytes sampled). The
conditional nested notification callback at `0x1022c4b8` and its dispatch
site `0x10062344` were not reached; their enable mask was zero at ordinary
post-startup. This closes callback completion for this constructed payload
and QEMU context, but 176 bytes is not a worst-case bound and the diagnostic
ran on InitTask, not the candidate's APPLV worker. It does not establish
candidate action completion, reticle visibility, or half-press acquisition.
Candidate 02 remains NO-GO. Read-only stock-QEMU trace, 2026-10-18; high
confidence for the observed event, return and sampled stack delta; no claim
about other payloads, worker context or camera behavior. No camera access or
firmware bytes/dumps.

F-328. Re-audited the QEMU callback's alleged missing AF-object context.
`0x101885e8` is a generic linked-list pop-front helper: it reads the head
node's payload, unlinks the node, decrements the list count, and returns that
payload. In `0x10074492`, the list at `0xc259e920+0x70` is first checked for
emptiness; when nonempty, its head is inspected, popped, and moved to a second
list at `0xc259e920+0x90`. Thus the QEMU observation that `r4 == 0` at
`0x1007450e` means the first queue was empty in that fixture. It does not
mean an AF object lookup failed, and `0x101885e8` is not evidence of an
AF-object registry. This supersedes the object-lookup interpretation in
F-280/F-282/F-283 and retires the proposed search for a constructor or
registration feeding `0x101885e8`. The queue's producer and semantic relation
to tracking remain unknown; continue with the direct AF-ready/reticle hook or
the producer only if its identification can change that hook decision.
Hash-verified Thumb decode and direct call-site review, 2026-10-18; high
confidence in the list operation and empty-queue interpretation, no claim on
queue purpose or tracking behavior. No camera access or firmware bytes/dumps.

F-329. A pinned-QEMU probe set AF-area values 601 and 602 through native
setter `0x1042b2d8`; property getters read back base mode 6 with People
submode 1 and Animal submode 2. The action-45 state mapper still returned
state 5 in both cases. A synthetic enable of the separate boolean gate at
`0xc23a51a8+5` did not change the mapper result or reach any state-operation
helper; the source pair remained `(0,0)`. The mapper's snapshot is copied from
the AF context by `0x104b9348`/`0x101925ce`, and its `+0x61/+0x62` bytes are
the pair copied by bridge `0x101925b0` from the source pair at
`0xc259ff0c+0x38/+0x39`. Thus ordinary QEMU mode selection does not populate
the native AF state required for action 45, even when the separate boolean
gate is enabled. This does not show that the same rejection occurs on the
camera or disprove the auto-arm design; it means QEMU cannot verify candidate
activation from this setup. The camera-side reticle and half-press behavior
remain unverified. Read-only pinned-QEMU probe plus hash-verified Thumb data
flow, 2026-10-18; high confidence in property readback, state-5 return, and
snapshot copy path; no claim about real-camera state or UI behavior. No camera
access or firmware bytes/dumps.

F-330. Hash-verified static Thumb tracing narrowed the source-pair transition
layer. Routine `0x1007756e`, reached by a tail-dispatch entry at `0x10162f14`,
passes the native lock gate and, when the source state byte at
`0xc259ff0c+0x10` is exactly 1, writes state 4, source pair `(1,1)` at
`+0x38/+0x39`, and related status fields. Sibling entry `0x10162f18` reaches
`0x100775c6`, which has separate state-dependent clearing paths. This is a
concrete candidate for the native state transition layer, but static code
does not identify the dispatch entries as the Auto-area tracking command or
prove that calling `0x1007756e` produces the reticle or half-press acquisition.
The known `(1,0)` writer `0x10078aa0` remains on an event-driven callback path
through `0x1007445c`; its relation to the `(1,1)` transition is unresolved.
Next trace the dispatcher input/registration and the observed half-press
consumer before selecting a call site. Candidate 02 remains NO-GO. No camera
access or firmware bytes/dumps. High confidence in the decoded writes and
branch targets; no confidence claim on user-visible tracking semantics.

F-331. Follow-up control-flow analysis connects F-330 to action 45. Native
pair `(1,1)` with Auto-area base-mode byte 6 maps through `0x1044dc5a` to
state 3. The principal action-45 selector routes states 2/3 through
`0x1045a21c`, which calls bridge `0x10230866`; that bridge calls dispatch
entry `0x10162f18` and thus `0x100775c6`. In its current-source-state-4 case,
`0x100775c6` clears the source state and pair to zero. Therefore, after
`0x1007756e` has established source state 4 and `(1,1)`, replaying action 45
can follow a native clear transition. This is consistent with a toggle/cancel
path and makes action 45 a poor direct substitute for the desired persistent
ready state. It does not establish reticle visibility, shutter half-press
acquisition, or the semantic label for source state 4. Next trace the actual
native entry that first reaches `0x1007756e` in camera control flow and its
caller conditions. Read-only hash-verified static decode; high confidence in
the call chain and state-dependent writes, no claim about UI behavior. No
camera access or firmware bytes/dumps.

F-332. The only branch to the F-330 arming transition traces through a
native AF callback. `0x1028f200` calls the local return-only request stub
with code `0x33`, then tail-branches to `0x102bdbb4`. That routine
copies the AF context and calls `0x1045a1e6` with argument 1 only when the
snapshot has Auto-area base byte `+0x44 == 6`, source pair `+0x61/+0x62 ==
(1,0)`, and byte `+0x415 == 0`. The downstream `0x1007756e` transition also
requires source state byte `0xc259ff0c+0x10 == 1`; state 0 takes its no-write
branch. With state 1, `0x1045a1e6 -> 0x10230856 -> 0x10162f14 ->
0x1007756e` sets source state 4 and pair `(1,1)`. This is a real
mode-conditioned native path into the pair/state already observed to map to
action-45 state 3. The extra byte's meaning and the runtime registration or
trigger for `0x1028f200` remain unknown; no evidence says it runs on AF-mode
selection or produces the visible reticle. Next trace the runtime callback
dispatch or a statically recoverable caller that controls this AF method.
Hash-verified static Thumb review; high confidence in the guard and call
chain, no claim on trigger timing or UI behavior. No camera access or
firmware bytes/dumps.

F-333. A pinned stock-QEMU probe corrected F-330's overly broad state gate and
executed the native callback with synthetic context. The state initializer
`0x100774f4` moved source state 0 to state 1 and pair `(1,0)`. With that
state, the wrapper `0x1028f200` left the pair unchanged for wrong Auto-area
mode, wrong AF-context pair, or nonzero context byte `+0x415`. For mode 6,
context pair `(1,0)`, byte `+0x415 == 0`, and source state 1, the callback
reached `0x1045a1e6 -> 0x10230856 -> 0x10162f14 -> 0x1007756e` and returned
with source state 4 and pair `(1,1)`. An earlier case with source state 0 did
not transition, confirming `0x1007756e` writes only from state 1. The original
firmware hash and QEMU checkout were unchanged. This validates the native
state transition and guards under constructed QEMU state only; it does not
prove that state 1 displays the reticle, that the wrapper is the physical
half-press callback, or that real camera timing supplies these values. The
next patch decision is to produce ready state 1 on Auto-area activation while
preserving the native guarded state-4 transition for half-press. High
confidence in the observed QEMU state changes and guard behavior, no claim on
camera UI behavior. No camera access or firmware bytes/dumps.

F-334. Candidate generation was premature relative to the evidence and the
project's camera-readiness gate. Candidate 02 did not establish the requested
Auto-area People/Animal ready state on a camera, visible reticle, or
half-press acquisition; the camera displayed no Update action and did not
begin installation. The candidate remains NO-GO and must not be presented as
ready to install or test. F-333's QEMU result validates only native state
writes under constructed conditions. Continue with hook selection and
behavior evidence; do not make another installable image until the hook and
all project gates are resolved. Review of current handoff and camera report,
2026-10-18; high confidence in candidate status, no claim on updater's exact
rejection reason. No camera access or firmware bytes/dumps.

F-335. A full-image direct-Thumb-call and exact-word-reference sweep using
the private read-only xref tool found two direct callers of Auto-area setter
`0x1042b2d8` (`0x1042bac2`, `0x10430c6c`), and two direct callers of ready
helper `0x1045a1ae` (`0x10368bc6`, `0x10458dfe`). The state-1 writer
`0x100774f4` is reached by tail branch `0x10162f10`; the guarded state-4
writer `0x1007756e` is reached by tail branch `0x10162f14`. The wrapper
`0x1028f200` has no direct branch or exact literal-pointer reference in this
sweep; its only observed branch is its tail to `0x102bdbb4`. This leaves the
wrapper's trigger indirect or runtime-registered and does not prove a physical
half-press connection. The setter is a better candidate reconciliation point
because its two known callers centralize mode writes, but its full ABI,
return-time context and unobserved indirect callers still require review.
Read-only xref scan of the hash-verified local original, 2026-10-18; high
confidence in the bounded call/reference results, no completeness claim for
computed dispatch. No camera access or firmware bytes/dumps.

F-336. A pinned stock-QEMU sequence used synthetic Auto-area AF context to
establish native state 1/pair `(1,0)`, copy that pair into the AF context,
and run the guarded callback into state 4/pair `(1,1)`. Reapplying native
ready helper `0x1045a1ae` after that transition completed its normal helper
chain but left source state 4 and pair `(1,1)` unchanged. This shows that the
helper does not reset those source bytes when repeated after the constructed
active transition; it does not prove that its other side effects preserve
camera tracking, that state 4 means acquisition is active, or that the
callback is driven by shutter half-press. The QEMU firmware identity and
checkout remained unchanged. Read-only pinned-QEMU probe with constructed
state, 2026-10-18; high confidence in the sampled state bytes and call chain,
no claim about reticle or camera behavior. No camera access or firmware
bytes/dumps.

F-337. After standard simulated shooting-view setup, native setter calls with
encodings 601 and 602 returned successfully and standard properties read back
base mode 6 with submodes 1 and 2. The AF context at `0xc237c7b4` still had
base-mode byte `+0x44 == 0` and pair `+0x61/+0x62 == (0,0)` after each setter
call. This repeats the known simulator disconnect between property selection
and the AF snapshot in a read-only context sample; it does not prove the real
camera's context remains stale or that setter continuation is unsafe. Stop
repeating this QEMU setup. The real-firmware question is which AF-context
producer populates base mode and what native callback follows that update.
Pinned stock-QEMU property setter/readback and guest-memory observation,
2026-10-18; high confidence in the sampled simulator values, no claim about
camera context. No camera access or firmware bytes/dumps.

F-338. A follow-up pinned-QEMU test captured the actual stack snapshot used
by guarded callback `0x1028f200`, without writing the AF-context mode byte.
For both native setter encodings 601 and 602, the property getters returned
base mode 6 and submode 1/2. Native ready helper `0x1045a1ae` plus bridge
`0x101925b0` established source/context pair `(1,0)`, and the extra guard byte
was zero; however, the callback's constructed snapshot at stack offsets
`+0x44`, `+0x61/+0x62`, and `+0x415` was `(0, (1,0), 0)`. It therefore did
not call `0x1045a1e6`, and source state remained 1 for both People and Animal.
This directly confirms that the stock QEMU property setter does not produce
the mode byte required by this callback through the exercised setup. It does
not show the camera has the same context gap. This refines F-337: the global
context sample was not itself the callback snapshot; the stack snapshot is
the decisive observation. Trace the actual AF-context producer and its event
ordering rather than retrying this setter sequence. Original firmware hash
and simulator checkout remained unchanged. Read-only pinned-QEMU test with
synthetic state and stack sampling, 2026-10-18; high confidence in sampled
snapshot and control path, no claim about real-camera behavior. No camera
access or firmware bytes/dumps.

F-339. Static tracing of the callback snapshot builder identifies the source
of its mode guard. `0x101925ee` copies a 0x6c-byte range from the live AF object
at `*(root + 0x144) + 0x40` into the constructed context at `+0x44`; this
supplies the byte later tested by the callback at snapshot offset `+0x44`.
The same builder reads the live object's `+0x40` field in a mode-dependent
branch. By contrast, Auto-area setter `0x1042b2d8` decomposes its encoded input
and writes public properties `0x0c2b` and, for base modes 4/6, `0x0c3c` or
`0x0c3d`; it has no direct write to the live AF object or the copied context.
This explains why the exercised QEMU setter path can read back People/Animal
properties while the callback snapshot mode byte remains zero, and weakens the
public setter as an immediate ready-state hook unless the downstream AF-object
update has already completed. The next useful trace is the writer/update path
for live AF-object offset `+0x40`, then the timing of its context snapshot.
This is static data-flow evidence only: it does not prove real-camera timing,
reticle visibility, or half-press acquisition. Hash-verified Thumb decode,
2026-10-18; high confidence in the copy source/destination and setter property
writes, no claim about camera behavior. No camera access or firmware
bytes/dumps.

F-340. The Auto-area setter's generic property-write path is synchronous
through a runtime observer dispatcher. Setter `0x1042b2d8` calls property
writer `0x10465990`, which tail-routes to `0x1021a0c6`; after storing the
property, that routine calls `0x10132f8c` with the property ID and new value
before returning. The dispatcher searches runtime callback records and invokes
a matching function pointer when present; if its cached target is empty, it
uses a resolver path. Thus a post-return hook could run after a property
observer has updated AF state, but the callbacks for `0x0c2b` and `0x0c3d`
and any write they make to live AF-object `+0x40` remain unidentified. This
qualifies F-339: the setter has no direct object write, while its downstream
observer path may still update the object synchronously. Next trace the
registration/resolution path for these property IDs and determine whether its
handler populates the live AF object's mode field. Hash-verified Thumb decode
and bounded callback-dispatch review, 2026-10-18; high confidence in the
setter-to-dispatch call chain and indirect callback mechanism, no resolved
observer target or camera behavior. No camera access or firmware bytes/dumps.

F-341. A focused pinned-QEMU probe observed property IDs `0x0c2b` (base mode)
and `0x0c3d` (People/Animal submode) enter dispatcher `0x10132f8c` after
native setter encodings 601/602. The dispatcher did not reach its indirect
callback-call site or its fallback resolver for either property in this
shooting-view fixture. Property getters still returned base mode 6 and
submodes 1/2. Thus this QEMU setup has no observed callback route that updates
the live AF-object mode field; this refines, but does not replace, F-337/F-338.
It does not show that the real camera lacks these runtime registrations. The
original firmware hash and pinned simulator checkout remained unchanged. A
new probe recorded only setter/dispatcher registers and did not call the ready
helper or tracking callback; 2026-10-18, high confidence in the observed
QEMU path and property readback, no claim about camera registrations or UI
behavior. No camera access or firmware bytes/dumps. Next trace the property
observer registration/initialization path statically and find the AF-object
`+0x40` writer.

F-342. Static review of both direct callers of Auto-area setter
`0x1042b2d8` found no direct call to the ready/action helpers or the AF-context
builder after the property write. Caller `0x1042bac2` returns immediately
after the setter. Caller `0x10430c6c` continues through property-to-menu
mapping helper `0x10430b46` and selection-adjustment helper `0x1042d6de`, then
returns success; these caller slices do not write live AF-object `+0x40`.
Together with F-340/F-341, this makes the setter a clear property-selection
boundary but not a proven AF-object update or tracking-ready hook. The object
update may occur through dynamic observers or another AF lifecycle path. Next
trace the producer/writer for AF-object `+0x40` outside these two setter
callers, and identify when it becomes visible to builder `0x101925ee`.
Hash-verified Thumb call-chain review, 2026-10-18; high confidence in the two
direct caller continuations, no completeness claim for indirect dispatch and
no camera behavior. No camera access or firmware bytes/dumps.

F-343. Reviewed the hash-verified Thumb consumer at `0x10489832`, one of the
static readers of Auto-area base property `0x0c2b`. It branches on the base
mode, reads `0x0c3d` for People/Animal when base mode is 6, maps those values
to menu-label identifiers, and emits the corresponding UI updates. This path
does not write the live AF-object mode byte or build the tracking callback
context, so it is a display/menu consumer rather than the missing AF-context
producer. The direct writer for live AF-object `+0x40` and the runtime update
ordering remain unresolved; broad `STRB [register,#0x40]` matches cannot be
identified as that field without proving the base pointer. Hash-verified
Thumb decode, 2026-10-18; high confidence in this consumer's property reads
and UI mapping, no claim about the camera's runtime observer or tracking
behavior. No camera access or firmware bytes/dumps.

F-344. Followed the only direct caller of snapshot builder `0x101925ee` at
`0x101613b2`. It belongs to handler entry `0x1016139e`, which is referenced
as a Thumb callback pointer in the static table at `0x10161a44`. On the
handler's matching branch it passes the live-view context at `[r1+0x428]` to
the snapshot builder, then reads AF-object fields including `+0x40` for
subsequent decisions; the reviewed caller slice contains no store to that
field. This identifies an event-driven snapshot consumer, not the missing
AF-object mode producer, and leaves the callback's dispatcher/event meaning
unresolved. Hash-verified Thumb decode and direct-call/reference review,
2026-10-19; high confidence in the call/data flow, no claim about runtime
event delivery or camera behavior. No camera access or firmware bytes/dumps.

F-345. Followed the Auto-area base-property notification path one layer past
the setter. Property-batch processor `0x104579a0` passes each changed property
ID to classifier `0x104575d0`; the `0x0c2b` case returns mask `0x04000000`.
The processor then obtains the shared notification context and posts event
`0x56` with that mask through `0x10462894` and the native queue helper. This
proves Auto-area base-property changes enter a specific asynchronous
notification route, but does not identify its receiver or show a write to
live AF-object `+0x40`, tracking-ready state, or reticle state. Continue from
the event-`0x56` receiver/queue consumer and determine whether it updates the
AF object before the registered snapshot callback runs. Hash-verified
Thumb-only static trace, 2026-10-19; high confidence in the property-to-mask
and event-post path, no runtime timing or camera conclusion. No camera access
or firmware bytes/dumps.

F-346. Correction to F-345: the `0x56` argument at `0x104628c8` is passed
to `0x1046296e`, which is a return stub; it is not the queued notification
event. After that call, `0x10462894` loads the shared handle and mask and
tail-calls wrapper `0x10199e04`, which forwards them to platform primitive
`0x10036334`. Thus the established edge is that Auto-area base-property
changes set mask `0x04000000` on a shared event-flag-like object. The waiting
consumer and its relationship to live AF-object `+0x40` remain unknown. Trace
the handle initialization/wait path to identify that consumer before choosing
a patch hook. Hash-verified Thumb call/data-flow review, 2026-10-19; high
confidence in the stub and handle/mask path, no runtime timing or camera
conclusion. No camera access or firmware bytes/dumps. Supersedes F-345's
description of `0x56` as a queued event.

F-347. Traced the shared-handle initialization reached from the mode-3 branch
at `0x10595840`. It creates three synchronization objects through
`0x10462840`, `0x1046285e`, and `0x1046287c`; their returned handles are stored
in adjacent slots based at `0xc181e4e4`. That same initializer then registers
seven callbacks through `0x101e1c04`, including targets in `0x104650f8` and
`0x104bd422`–`0x104bd4da`. The callback implementations update separate
bit-packed/shared state records, but this trace does not associate their
registration keys or effects with Auto-area property mask `0x04000000`, the
live AF-object `+0x40` byte, or the snapshot callback `0x1016139e`. The image
contains many generic wait-wrapper call sites; the bounded direct-call review
did not identify a unique consumer for these three handles. This rules out
the simple local waiter-xref route, not indirect consumers or runtime
registration. Next inspect the callback registry keys and the callers of the
registered targets, then connect only a proven key/state update to the AF
snapshot path. Hash-verified Thumb decode and direct-call review, 2026-10-19;
medium confidence in the initialization and callback target list, no runtime
timing or camera conclusion. No camera access or firmware bytes/dumps.

F-348. Decoded the registration wrapper used by the F-347 initializer.
`0x101e1c04` swaps the caller's key pointer and callback pointer before
entering `0x101e1b86`; that routine hashes a zero-terminated key (rejecting
keys longer than 16 bytes), selects a bucket, compares existing keys, and
stores a callback pointer, an auxiliary value, and the caller's opaque
pointer in the registration record. At the seven call sites, the key pointer
comes from a nearby address and the callback pointer from a literal pool;
their key contents have not been semantically identified. This establishes
that the F-347 registrations are keyed callback subscriptions, not proof that
they consume the Auto-area event mask. Next map the seven key contents to
other key producers/dispatch sites and follow only a matching callback toward
AF-object `+0x40` or snapshot handler `0x1016139e`. Static Thumb review,
2026-10-19; high confidence in the local argument and record flow, no
runtime delivery or camera conclusion. No camera access or firmware
bytes/dumps.

F-349. Connected registered handler `0x1016139e` to its runtime callback
filter and snapshot event. Initialization stores its Thumb pointer in shared
callback slot `0xc1885f30`; dispatcher `0x1021dfa0`/`0x1021dee4` can route into
that slot. The generic `0x041a0040` dispatch branch does not satisfy the
handler's event filter. The handler proceeds to snapshot live-view AF context
`[r1+0x428]` only for event ID `0x0002fe3d`; another accepted ID takes a
separate path. The `0x0002fe3d` route is therefore a concrete event-to-AF-
snapshot edge, but its producer is not yet linked to Auto-area property
`0x0c2b`/submode `0x0c3d` or to the tracking-ready helper. Next trace the
producer of `0x0002fe3d` and test whether its ordering follows the AF-context
update; only then can this callback be evaluated as an auto-arm hook.
Hash-verified Thumb and literal-pool data-flow review, 2026-10-19; high
confidence in the local callback filter and snapshot call, no runtime timing,
reticle, or camera conclusion. No camera access or firmware bytes/dumps.

F-350. Bounded the visible static source chain for F-349's callback. The
outer callback `0x1021dfa0` is installed in a shared callback slot and its two
located indirect call sites supply event ID `0x041a0081`; the AF handler
`0x1016139e` rejects that ID before building the AF snapshot. A full-image
literal search found no occurrence of accepted snapshot event `0x0002fe3d`.
Thus the visible static caller chain does not explain the accepted snapshot
event or link it to Auto-area changes. This does not exclude runtime-generated
IDs, indirect producers outside the located slot, or an event whose value is
assembled from fields. The callback is not a selected hook. Pivot to the live
AF-context producer/event ordering and retain the snapshot callback only if a
new source link is found. Full-image Thumb disassembly, literal-reference and
byte-pattern scans, 2026-10-19; medium confidence in the bounded static
inventory, no runtime or camera conclusion. No camera access or firmware
bytes/dumps.

F-351. Reviewed the strongest offset-only candidates from a bounded scan for
stores near the live AF object's `+0x40` field. `0x135762` allocates and
initializes the object whose pointer is installed at root `+0x144`; its stores
to object `+0x40` are zero-initialization. `0x143718` is a reusable reset
routine that clears the same object fields, including `+0x40`. The other
matches write either a stack-built record, a separate global record, or
nested components reached through unrelated offsets. None is evidence of the
Auto-area People/Animal mode producer. This rules out these prominent
offset-only matches, not every possible indirect or byte-sized writer. The
next useful static step is to trace non-initialization readers and writers
from the root `+0x144` object using the exact pointer provenance; if that does
not reveal a mode update, report the static hook unresolved and require a
runtime AF-context observation before another patch. Thumb disassembly and
bounded candidate classification, 2026-10-19; medium confidence in the
classified sites, no runtime or camera conclusion. No camera access or
firmware bytes/dumps.

F-352. Correction to F-339/F-351: rereading snapshot builder
`0x101925ee` at the instruction level shows its copied context input in `r5`;
the mode byte used by its mode-6 guard is loaded from `[r1 + 0x40]` after
`r1 = [r5]`. Thus the relevant mode object is the pointer at context offset
`+0`, plus `+0x40`. The separate pointer at context `+0x144` supplies other
snapshot fields and is not the direct source of this mode byte. The earlier
`0x135762` and `0x143718` offset-only candidates therefore were not shown to
initialize/reset the mode object; F-351's claimed AF-object classification is
withdrawn. A bounded instruction-level taint scan from `ldr reg,[base,#0x144]`
found no immediate same-register byte writer to `+0x40`; one word store at
`0x307bec` targets that different `+0x144` subobject. Next trace the pointer
stored at context `+0` and its own `+0x40` writers from the callback's actual
context root. No hook or patch is established. Hash-verified Thumb review,
2026-10-19; high confidence in the local source-pointer correction, no runtime
or camera conclusion. No camera access or firmware bytes/dumps. Supersedes
F-339's pointer expression and F-351's object classification.

F-353. The corrected context-pointer search finds a concrete writer family at
section offsets `0x1d84c28` and `0x1e0a9f4` (duplicated code paths). Each takes
a state record, loads its first pointer, scans eight four-byte table entries,
derives a 0/1 value from entry flags/counts, and stores that byte at pointed
object `+0x40`; the first variant then sends the inverse value to a follow-up
helper. Located callers of `0x1d84c28` include `0x1d86396`, `0x1d86528`,
`0x1d86a6c`, and `0x1d87abe`; reviewed call sites include a zero second
argument and are within a larger AF-like event-processing routine. This is a
real writer to the pointer-at-context-`+0` field but writes a table-derived
boolean, not the Auto-area mode value 6, and no reviewed guard ties it to
properties `0x0c2b`/`0x0c3d` or the native ready helper. Treat it as a state
consumer/update path, not the auto-arm hook. Next identify the table's producer
and the event/registration semantics of the callers; stop if no Auto-area or
ready-state link appears. Hash-verified Thumb review, 2026-10-19; high
confidence in the local dataflow, low confidence in feature semantics, no
runtime or camera conclusion. No camera access or firmware bytes/dumps.

F-354. Followed the table input one edge upstream. In the nearby state-update
path, caller record fields are copied into a local five-word tuple; its
third/fourth fields are then installed at state-record offsets `+0x268` and
`+0x26c` (store sites `0x1d6cde`/`0x1d6cd6`, with a parallel path at
`0x1d6d6c`/`0x1d6d64`). In the first path, the `+0x26c` value originates
from `[r5 + 8]` in the caller-provided record. That is the pointer later
scanned by the `+0x40` boolean writer family in F-353. The bounded slice does
not identify the record's producer or event type, and does not link it to
Auto-area properties or tracking readiness. Next trace the caller-provided
record from update entry `0x1d6ba30` and its call path; stop unless it reaches
AF-area selection or the native ready helper. Thumb dataflow review,
2026-10-19; medium confidence in local field provenance, no feature/runtime/
camera conclusion. No camera access or firmware bytes/dumps.

F-355. Correction to F-354's proposed next address: section offset `0x1d6ba30`
is inside a ring-buffer helper beginning at `0x1d6ba22` (it scans indexed
records and updates a cursor); it is not the caller-record producer or the
state-update entry described in F-354. The cited `0x1d6cd6` region also
decodes as unrelated counter/table iteration, so the previous address list
does not establish stores to state-record `+0x268/+0x26c`. Withdraw F-354's
specific store-site and producer-address claims pending revalidation. Keep
only the earlier F-353 finding that a table-derived boolean is written
through the context-first pointer at `+0x40`; the table provenance is
unresolved. Pivot to the direct callers of native ready helper `0x1045a1ae`
(section offsets `0x348bc6` and `0x438dfe`) and trace their enclosing
dispatcher/input sources before assigning button or tracking semantics.
Hash-verified Thumb re-decode, 2026-10-19; high confidence that the proposed
`0x1d6ba30`/`0x1d6cd6` interpretation is unsupported, no feature/runtime/
camera conclusion. No camera access or firmware bytes/dumps. Supersedes
F-354's store-site and next-address claims.

F-356. Inspected the two direct callsites of native ready helper
`0x1045a1ae`. The callsite at section offset `0x348bc6` is reached from an
event-like handler that switches on incoming codes `0x0b`, `0x19`, `0x1b`,
`0x28`, `0x2c`, and `0x2d`; for code `0x1b`, result values 0/1 call the ready
helper with byte 0, value 2 calls clear helper `0x1045a1e6`, and value 3 calls
active-transition helper `0x1045a21c` before possibly looping to ready. Other
branches use the same helper family, but their event-code producer and
semantics are unresolved. The second callsite at `0x438dfe` is inside a
record-driven dispatcher: it checks input flags, property/key `0x188c`,
record byte `+4` equal to 2 or 3, and successful returns from helpers
`0x1045a258`/`0x1045a21c` before calling ready with byte 1. These are real
ready-state routes, but neither local slice links its input to Auto-area
People/Animal selection, OK, Fn1, or the requested automatic behavior. Next
trace the outer dispatchers and source records for these two paths; stop if
no AF-area or tracking-state connection appears. Hash-verified Thumb
disassembly, 2026-10-19; high confidence in local control flow, no confidence
in feature semantics, no runtime or camera conclusion. No camera access or
firmware bytes/dumps.

F-357. Traced the ready-helper callers one level into their surrounding
dispatch. The event-like caller `0x348b6e` is reached from configurable-action
helpers that query settings including `0x1170`, `0x1141`, `0x1173`, and
`0x1144`, then branch on action values such as `0x19`, `0x2a`, and `0x4d`.
The known AE-L/AF-L stills assignment is setting `0x1184`, so these local
reads do not identify the AE-L/AF-L input or Auto-area transition. The other
ready-helper caller remains guarded by generic record fields and key
`0x188c`, with no AF-area link. Treat both routes as unassigned generic
state/action machinery, not as the automatic-arm hook. The key `0x188c` and
setting IDs have not been mapped to named AF properties. Resume from the
Auto-area base/submode notification consumer or another proven AF-context
producer, and evaluate whether it can call the idempotent ready-state path
without routing through toggle action 45. Hash-verified Thumb call-chain
review and cross-check against the named setting table, 2026-10-19; high
confidence in the local call paths and setting-ID distinction, no feature
semantics or runtime/camera conclusion. No camera access or firmware
bytes/dumps.

F-358. Bounded the event-source follow-up for F-353's table-derived AF-context
writer. The writer at `0x1d84c28` is called from the processing routine at
`0x1d85b44`; that routine has four direct callers at section offsets
`0x1d8551a`, `0x1d860c4`, `0x1d86302`, and `0x1d87570`. The reviewed call
slices pass internal object/record pointers into the same processing family,
but do not expose Auto-area properties `0x0c2b`/`0x0c3d`, the setter
`0x1042b2d8`, or ready helper `0x1045a1ae`. This does not rule out a dynamic
event producer or computed dispatch, but the bounded static caller path does
not connect this writer to the requested arm behavior. Stop extending this
branch absent a new cross-reference. Resume with the Auto-area notification
consumer only through a candidate event/dispatcher that can be tied to the
three initialized handles; generic wait-wrapper enumeration alone has not
identified a consumer. Hash-verified Thumb disassembly and direct-call sweep,
2026-10-19; high confidence in the listed direct callers and local data flow,
no feature/runtime/camera conclusion. No camera access or firmware
bytes/dumps.

F-359. Resolved the semantic domain of the callback registrations made by
initializer `0x10595840`. Its seven key strings name GUI debug/log controls:
debug logging, interface logging, category/task selection, log skipping, and
debug-mode get/set. The property-batch processor's Auto-area case signals the
second of the three handles initialized by this routine through the shared
flag setter. This ties the `0x0c2b` notification to a GUI/property-notification
route, but the registered debug-command callbacks are not evidence of an AF
context consumer or tracking-ready transition. Retire the callback-key branch;
do not infer tracking behavior from this shared GUI notification mechanism.
Next find the AF engine's application/update path from the Auto-area setter or
another positively identified AF lifecycle callback. Hash-verified Thumb
disassembly and local key-string classification, 2026-10-19; high confidence
in the registered key domain and slot usage, no proof of runtime receiver,
reticle, half-press, or camera behavior. No camera access or firmware
bytes/dumps.

F-360. Reviewed a candidate property handler at `0x1008955c` because it
compares Auto-area base/submode IDs `0x0c2b`, `0x0c3c`, and `0x0c3d`. Its
local effect is to gather property values into a change record and pass that
record to `0x1008945c`, which merges it into a generic cached-property table.
It does not locally call the native ready helper, write the AF-context mode
byte, or invoke the tracking action. A bounded direct-call and literal-pointer
scan found no static registration/reference to this entry, so its role as an
observer callback is unproven; computed or runtime registration remains
possible. Do not use this routine as the auto-arm hook. The useful next step
is to identify the actual AF-application callback reached after setter
`0x1042b2d8`, or a runtime observer resolver target for `0x0c2b`/`0x0c3d`,
and follow it to the live context and ready-state writer. Hash-verified Thumb
review and bounded xref sweep, 2026-10-19; high confidence in the local
property-record behavior and absence of direct static references, no proof of
runtime reachability or AF semantics. No camera access or firmware
bytes/dumps.

F-361. The generic property observer dispatcher `0x10132f8c` scans a
200-record registration table initialized by `0x10132eac`. Initialization
copies each record's fixed property ID from the static table at `0x115db4ec`
into runtime table storage, then performs the record's service setup. A
bounded scan of all 200 static IDs found no entries for Auto-area base
property `0x0c2b` or submode properties `0x0c3c`/`0x0c3d`. The dispatcher's
remaining local fallback branches also do not match these IDs. The resolver
`0x10132e66` is directly called only from this table initializer and from the
dispatcher when a matching record lacks a cached handler; neither path
supplies a static Auto-area registration. Therefore this observer system is
not the missing AF-application callback on the reviewed static path. Runtime
code outside these direct paths could still affect AF context, so this does
not prove that no AF update occurs elsewhere. Retire the generic resolver
branch and trace AF-specific application/lifecycle code. Hash-verified
original-module Thumb decode, static-table scan, and bounded direct-call
sweep, 2026-10-19; high confidence for the fixed table contents and reviewed
dispatch paths, no claim about other runtime mechanisms or camera behavior.
No camera access or firmware bytes/dumps.

F-362. Followed the AF-like configuration callback at `0x1036c066` because
it queries Auto-area properties through helper `0x1036bff0` and reaches
`0x1045a47e`. The helper's selectors read properties `0x0c2a`/`0x0c2b`
(or alternate IDs `0x56c`/`0x56d`) to build generic property records; the
callback compares two configuration structures and updates cached status
bytes. Its call to `0x1045a47e` is a status query: that wrapper returns the
boolean from `0x102240ac`, which reads a global state byte, and performs no
ready-state write or tracking action. The branch is gated by an internal
configuration byte equal to 5, with no proven mapping to Auto-area
People/Animal or the requested ready state. This is an AF-adjacent
configuration reconciler, not the auto-arm hook. It narrows the search but
does not identify a patch point; resume at a proven live-context mode writer
or a native ready-state caller whose source is tied to Auto-area. Hash-
verified Thumb dataflow review, 2026-10-19; high confidence in the local
property reads, cached-state writes, and status-query contract, no runtime,
feature-semantic, reticle, or camera conclusion. No camera access or firmware
bytes/dumps.

F-363. Re-traced the live-view snapshot consumer `0x101925ee` from its
registered caller `0x1016139e`. Before the extended mode-specific snapshot
path, it reads byte `+0` and mode byte `+0x40` from the object pointer at
context `+0`; that path runs only when the bytes are respectively 1 and 6
and local snapshot flags at output `+0x364`/`+0x365` are clear. It then builds
additional snapshot data through `0x101914ae` and continues copying fields
from the separate context `+0x144` object. The reviewed builder reads these
mode/context fields and writes its snapshot output; it does not set the
source object's mode byte or enter the native ready helper. This is a
downstream consumer gate, not an auto-arm hook, and it establishes only that
the snapshot has a mode-6-specific branch. Next trace the producer that
installs the object pointer at live-view context `+0` and updates its
`+0x40` byte before this callback. Hash-verified Thumb review, 2026-10-19;
high confidence in the local gate and snapshot-copy path, no proof of runtime
event ordering, tracking semantics, reticle, half-press, or camera behavior.
No camera access or firmware bytes/dumps.

F-364. Resumed F-243's open search for callback `0x10302220`'s registration.
A full-image Thumb-pointer scan finds one static function pointer to that
callback at file offset `0x1f8af58`, in a table whose neighboring entries
are other callbacks in the same configurable-function subsystem. The callback
itself gates entry through `0x10485b50`, accepts only input codes `0x1a`,
`0x1b`, or `0x1c`, and then invokes dispatcher `0x10301f36`. The dispatcher's
first table routes those inputs to handlers other than AE-L/AF-L handler
index 13; the setting-`0x1184` check inside handler `0x10369468` therefore
does not establish physical AE-L/AF-L delivery to that route. This confirms
the callback's static-table presence but does not identify its table
initializer or a physical-key source. Do not use this dispatcher as the
one-button tracking hook. The physical input edge remains unresolved under
offline-only project rules. Hash-verified Thumb decode and full-image
pointer scan, 2026-10-19; high confidence in the pointer occurrence, callback
gate, and input-code routing, no physical-input or camera conclusion. No
camera access or firmware bytes/dumps.

F-365. Rechecked the proposed Auto-area setter boundary and native action
entry using the hash-verified original. Setter `0x1042b2d8` decodes its input
as base mode and submode, writes `0x0c2b`, then writes the People/Animal
submode to `0x0c3d` when base mode is 6; it returns without calling the
tracking-ready helper. Its two known callers are a setting-commit path
(`0x1042bac2`) and a mode-table application path (`0x10430c6c`), not a proven
AF-context lifecycle callback. Native ready helper `0x1045a1ae` takes a
pointer to a byte, clears a shared state word, and delegates through
`0x10230832` to state/configuration logic; its call alone is not evidence of
a visible reticle. Selector 45 (`0x10368b6e`) first maps a live AF snapshot and
chooses different helpers for mapped states 0/1 versus 2/3, so an unconditional
selector-45 call on every property update is not a safe auto-arm design. This
narrows the build question: a setter hook could catch explicit mode changes,
but the startup/live-view trigger and a People/Animal-ready precondition remain
unresolved. Next evaluate a disposable QEMU-only setter-hook prototype for
native state side effects, while separately tracing the AF-context lifecycle
needed when Auto-area is already selected. Candidate 02 remains NO-GO; no
camera access or installation workflow. Hash-verified Thumb decode and
caller-path review, 2026-10-19; high confidence in the local setter and helper
contracts, no proof of reticle, half-press behavior, natural context ordering,
or camera behavior. No firmware bytes/dumps.

F-366. Built a throwaway setter-hook overlay in `/private/tmp`, booted the
verified stock image in the pinned QEMU, then applied only the hook and stub
to guest RAM. Diagnostic calls to setter `0x1042b2d8` with encoded values 601
and 602 traversed the new tail-call stub, called native ready helper
`0x1045a1ae`, and reached the downstream state write with value 6. Value 600
traversed the stub but did not call the ready helper. The sampled AF-context
window around mode byte `+0x40` remained unchanged in all three cases. This
proves the prototype's local branch and native helper path in constructed
QEMU calls only; it does not show a natural menu selection reaching the hook,
that byte 6 produces the intended reticle, or half-press acquisition. It also
shows the public setter plus helper does not populate the sampled live AF
context in this simulator fixture. Next trace the AF-context producer and
view-entry lifecycle; keep the setter hook as a partial mode-change path, not
a complete auto-arm implementation. Candidate 02 remains NO-GO. Pinned-QEMU
guest-RAM overlay, 2026-10-19; high confidence in the observed branch,
helper-call, and state-write values, no natural event, camera, reticle, or
half-press conclusion. No firmware bytes/dumps in the repository and no
camera access.

F-367. Follow-up xrefs do not connect the pair accessors near AF status root
`0xc237c7b4` to the live-view mode object used by snapshot builder
`0x101925ee`. Getter `0x10197828` reads root bytes `+0x414/+0x415`; setter
`0x10197c3c` writes those bytes, with the located setter caller at
`0x102222aa`. They are separate from the live-view callback's context pointer
at `[r1+0x428]`, whose pointed object supplies mode byte `+0x40`. A read-only
stock-QEMU boot sample found context-root `+0` null at the InitTask checkpoint;
this is before simulated stills-view entry and says nothing about camera-time
state. A full-image displacement scan for `#0x428` produced many unrelated
structures and only re-observed the known callback loads at `0x101613ac` and
`0x101613b8`; it did not identify a unique object installer. Retire the
`+0x414/+0x415` accessor as a tracking-hook lead. Next trace the owner and
initializer of the live-view event context passed to `0x1016139e`, then its
context `+0` object and mode `+0x40` writer. Candidate 02 remains NO-GO. This
is static Thumb review plus a simulator boot-state read only; no camera,
reticle, or half-press conclusion. 2026-10-19; high confidence in the local
accessor offsets and sampled boot value, no feature-level conclusion. No
firmware bytes/dumps in the repository.

F-368. Continued the callback-owner trace from F-367. The short routine at
`0x10161642` passes two ADR-derived data addresses near the static callback
data to queue setup helper `0x1021cce8`; a separate nearby registration at
`0x101617e4` calls keyed registry `0x101e1c04`. These local setup calls do not
identify an AF-context installer. Generic event dispatcher `0x1021dee4`
receives a payload pointer, reads payload fields `+0x42c` and `+0x428`, then
uses the context pointer at `payload+0x428` (including its byte `+0xe`) before
forwarding an event ID and payload to the registered callback. Its ordinary
event `0x041a0040` does not pass the AF handler's `0x0002fe3d` filter. A
full-image Thumb scan found neither `MOVW #0xfe3d` nor `MOVT #2`; computed or
table-derived sources remain possible. This confirms the handler is an
event consumer, not a demonstrated Auto-area mode-object installer or arm
hook. Stop extending this callback branch absent a newly identified producer
for the accepted event. Return to the live AF object's context `+0`
installation and `+0x40` writer, correlating the pointer by proven data flow
rather than the `+0x428` displacement alone. Candidate 02 remains NO-GO.
Hash-verified Thumb and relative-table review, 2026-10-19; high confidence in
the local dispatcher and setup edges, no accepted-event source, reticle,
half-press, or camera conclusion. No firmware bytes/dumps in the repository.

F-369. Ran the project's standard pinned-QEMU stills-view setup with a
breakpoint on AF snapshot callback `0x1016139e`. Setup completed, but the
callback was never reached and status-root `0xc237c7b4 + 0` remained null.
This fixture therefore cannot expose the camera-time AF context producer;
do not repeat the same simulated view-entry sequence. A separate full-image
Thumb scan found no simple same-register sequence that moves immediate 6
directly into a `STRB [register,#0x40]` within the preceding 12 decoded
instructions. This does not exclude loaded constants, register copies,
indirect stores, or computed values. Continue static work on the proven
live-object pointer and writer; do not infer a hook from displacement-only
matches. Candidate 02 remains NO-GO. Pinned-QEMU diagnostic and targeted
Thumb scan, 2026-10-19; high confidence in the bounded observations, no
camera or feature-behavior conclusion. No firmware bytes/dumps in the repo.

F-370. Re-decoded setter caller `0x10430c6c` in its enclosing routine
`0x10430baa`. That routine reads the current AF base/submode properties
`0x0c2b` and `0x0c3d`, maps the selected AF-area table entry, calls setter
`0x1042b2d8`, then updates selection state and menu UI through
`0x10430b46`/`0x1042d6de`. It is the explicit AF-area menu-selection path,
not a stills-view entry or live AF-object lifecycle callback. Thus a setter
hook covers a user changing AF-area in the menu but cannot by itself arm
tracking when Auto-area was already selected on entry. Keep searching for the
stills-view/AF-application path that has the live context pointer. Candidate
02 remains NO-GO. Hash-verified Thumb decode of the enclosing caller,
2026-10-19; high confidence in local menu dataflow, no reticle, half-press,
or camera conclusion. No firmware bytes/dumps in the repository.
