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
