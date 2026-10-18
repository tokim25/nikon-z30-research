# Firmware static map, C 1.20 (2026-10-17)

Deeper cross-reference results and the full hardware-switch map are in the
companion [firmware-map-deep-2026-10-17.md](firmware-map-deep-2026-10-17.md).


A consolidated address-and-description map of the owner's verified C 1.20
package, assembled for Codex. It is a reference map only: addresses, call
chains and confidence levels. It contains no firmware bytes, no hex or base64
dumps, no extracted component data, no raw table listings and no patch. The
extracted component files and any byte-level listings stay outside the
repository, per AGENTS.md.

Provenance: the package identity matches the recorded original in
[milestone-1-recovery.md](milestone-1-recovery.md). The component layout was
re-derived locally with the recovered verifier's decoder and re-checked with
this repo's `validate_container`; all three component hashes matched the
recorded values. The mappings below draw on verified notes already in the
repo ([facts.md](facts.md), [tracking-input-chain.md](tracking-input-chain.md),
[tracking-entry-research.md](tracking-entry-research.md),
[native-dispatch-chain.md](native-dispatch-chain.md),
[display-refresh-path.md](display-refresh-path.md),
[image-area-tables.md](image-area-tables.md),
[native-updater-digest-inputs.md](native-updater-digest-inputs.md)) plus a new
static cross-reference pass over the decoded EG module. No new firmware
decoding beyond extraction. No hardware, QEMU or camera contact.

Confidence: **confirmed** = observed static code/data link, independently
checked. **likely** = inferred, medium. **unknown** = not established. Every
"reached from" link is a static branch/literal/pointer reference, not a
runtime trace; prologue (function-start) detection is heuristic.

## Components

Names are abbreviated as in [milestone-1-recovery.md](milestone-1-recovery.md).

| # | Component | Offset in file | Size (bytes) | Load address | Confidence |
|---|---|---|---|---|---|
| 0 | EX | 176 | 524,290 | unknown | confirmed (extracted, validated) |
| 1 | TPJ | 524,466 | 32,802 | unknown | confirmed (extracted, validated) |
| 2 | EG (main) | 557,268 | 33,939,514 | 0x10020000 | confirmed |

Container shape: 32-byte prefix, 48-byte header, 3 × 32-byte directory
entries, the three components, 16-byte trailer. Package and component
SHA-256 values are in [milestone-1-recovery.md](milestone-1-recovery.md).

## Mapped items for the owner's user stories

| # | Item | Address | What it does | Call chain | Confidence |
|---|---|---|---|---|---|
| 1 | Input map table | 0x1073b400 | 179 rows × 8 bytes: input code → UI-event code (event at row +4) | read by 0x1045933e | confirmed |
| 2 | Input 0x1b → event 0x27e | row 32 of 0x1073b400 | Menu OK key | 0x1045933e → 0x103ce96e | confirmed |
| 3 | Nav inputs 0x3/0x4/0x5/0x6/0x8 → 0x255/0x253/0x254/0x257/0x258 | 0x1073b400 | d-pad/navigation (role likely) | table | confirmed table |
| 4 | Nav inputs 0x15/0x17/0x1a/0x1c/0x1f → 0x24e–0x252 | 0x1073b400 | Navigation handlers | → dispatcher 0x10462970 | likely |
| 5 | Navigation guards | 0x1045fb10/20/24/50 | Gate codes 0x24f–0x251, 0x26d–0x270 | UI-event rows | confirmed guards; role likely |
| 6 | Named switch table | 0x1072e3b0 | 40-byte slots (name, mask) | pointer at 0x1072e304 | confirmed |
| 7 | ID_SW0_AEAF_LOCK | slot 10, mask 0x2000 | AE-L/AF-L bit | table at 0x1072e3b0 | confirmed name; physical source unknown |
| 8 | ID_SW0_AEAF_LOCK_VPOS | slot 11, mask 0x1000 | Vertical-position twin | table at 0x1072e3b0 | confirmed name |
| 9 | Custom-function strings | — | eDSID_Setting_FuncAeAfLockButtonShooting / ...Movie | — | confirmed string; code path unknown |
| 10 | Key dispatcher | 0x103ce96e | Screen-stack dispatcher; per-screen key table (16-byte rows) | top of stack at 0xc181e4f0; 7 callers; 1 literal ref 0x104759e8 | confirmed |
| 11 | Key filter (0x27e → live view) | 0x104e2cbc → 0x102f1e10 | Diverts OK to live-view routine for some screens | reached from dispatcher (0x103ce884, 0x103ce94c) | confirmed |
| 12 | Live-view routine | 0x102f1e10 | Central live-view handler | 34 callers | confirmed; role likely |
| 13 | Live-view key table | not found | Why OK does nothing in live view | — | unknown |
| 14 | Live-view input type 3 | 0x102f7448 (fn 0x102f7398) | Live-view input entry | caller 0x102f760a | likely |
| 15 | Packet decoder (snapshot) | 0x1030705a → 0x102f0d14 | 5-byte packet → mask words and signed deltas | registered in pointer table ~0x115ce0cc..0x115ce148 (base 0x115ce1f4) | confirmed data flow; source likely |
| 16 | Mask-group-1 bit 0 → code 0x1b | decoder 0x102f0e38 | Maps the bit to internal code 0x1b (→ 0x27e) | loop at 0x102f101a; callers 0x102f1dbc, 0x102f28fa | confirmed |
| 17 | Touch/drag event ring | 0xc2008ea0 (writer 0x102f0a36) | 60-byte typed events; not button presses | — | confirmed |
| 18 | Mask 0x2000 structured-record path | selector 5 at 0x1008ad26 → staging 0xc1811e74 | Sets/clears AE-L/AF-L bit from state | → setter 0x101e383a → cache 0xc181182c+0x30 | confirmed; sender unknown |
| 19 | Input-cache setter | 0x101e383a | Copies staging word into cache | 3 callers: 0x1008ad6e, 0x103a3e88, 0x103a400c | confirmed |
| 20 | Queued input bank | handler 0x103a3d14 (code 0x2083); query 0x103a3cb0 | Maps queued ID byte to mask | reached via 0x10379a68 ← 0x10379b3e; publishers 0x103a400c/0x103a3e88; shared core 0x103a3b9c | confirmed; physical source unknown |
| 21 | Queued-bank row for ID 41 | row 11, mask 0x2000 | Associates logical ID 41 with AE-L/AF-L mask | consumer 0x103a3f9e | confirmed |
| 22 | Queued-input module registration | registrar fn 0x10379fc0; record at 0x1037a2c4 | Handler fn 0x10379d5a registered as callback; per-code handler table at 0x1037a2d0..0x1037a2f4; config descriptor at 0x115c685c (not a name) | init/task path: task entry fn 0x1059c2c8 → fn 0x1035b750 → 0x10379fc0 | confirmed refs; task-entry inferred |
| 23 | Router DRAM work area | ~0x20022000 | Queued-input/property router working memory (from descriptor) | referenced at 0x1002c69c (literal pool) and 0x115c6868 | confirmed reference; writer unknown |
| 24 | Tracking candidate entry | 0x11cf4e90 / 0x11cf4ea0 | Candidate subject-AF activation entries | → 0x11cf4986 / 0x11cf5774 | likely (candidate) |
| 25 | Tracking slot matcher | 0x11cf5248 | Matches 12-bit identifiers across 4 slots; returns slot or 0xffff | called by 0x11cf4986, 0x11cf5774 | confirmed |
| 26 | Tracking event dispatcher | 0x11cf5774 | Dispatches on leading event byte (0x13 branch) | ← 0x11cf4ea0, 0x11cf3e60/3e94 | likely |
| 27 | Inert text stub | 0x11d6f7b8 | Immediate return; reporting hypothesis dropped | — | confirmed |
| 28 | AF-area label lead | 0x103edc2e → text 0x103eddfc | Label selection for AF area; no prologue found | — | unknown |
| 29 | Image-area menu text | "Choose image area" | Menu label; setting Setting_ImageSize | — | confirmed text; entry point unknown |
| 30 | Menu translator | 0x1045933e | Maps menu candidate 0x1b to 0x27e | → table 0x1073b400 (literal refs 0x10459344..0x10459376) | confirmed |
| 31 | Image-area writer | 0x1008d38c (store at 0x1008d3fc) | Writes the image-area choice record | caller 0x1008a146 in fn 0x10089682; reached through subsystem function table at 0x11f9a4dc | confirmed chain; dispatcher unknown |
| 32 | Image-area function table | 0x11f9a4d8..0x11f9a518+ | vtable-shaped run of 0x10058xxx/0x1005dxxx function pointers; top fn 0x10058a82 at 0x11f9a4dc | indexed from a computed base (not located) | confirmed table; index unknown |
| 33 | Stock refresh chain | 0x10453d14 → 0x104b74f4 → 0x104b740a → 0x103c3810 → 0x103c3568 → 0x103c0bc0/0x103c0ac2/0x103c05d2 → 0x103c1b54 | Refresh request to render setup; no pixel write | — | confirmed (static) |
| 34 | Display refresh candidate | 0x1032427e–0x10324358; literal 0x10324648 → 0x10453ac3 | Conditional refresh request; links to menu redraw | 0x1030b596/0x1030b59e → predicate 0x10369ad0 | likely |
| 35 | Image-area ratio table | 0x10750658–0x1075080f | Retouch Trim crop sizes, not live view | ratio code 0x10597440 hard-codes 5 ratios; callers 0x105979a4, 0x10597bae | confirmed (not XPan live view) |
| 36 | Live-view bar hook sites | 0x102f5810 (fn 0x102f57e2), 0x102355f4 (fn 0x102355c6), 0x102355c0 (fn 0x10235576) | Documented bar hook points, seated in their functions | screen fan-out fn 0x10595844 calls four activation fns (incl. 0x102355c6) via adjacent BLs 0x10595850..0x1059585c | confirmed refs; fan-out entry unknown |
| 37 | XPan writer boundary | 0x1008d3fe / caller 0x1008a14a | Flash-write boundary (simulator-observed) | — | confirmed (simulator only) |
| 38 | Updater digest-input header reader | 0x101d5900 | Encoded-format flag path (not user-facing) | → 0x101d5ab2 → 0x101cf858 | confirmed (static) |
| 39 | Digest 8-byte suffix source | 0x10000088 | Unmapped digest input, outside EG | setup 0x101d7026 | unknown |

## Call-graph results from the new pass

- **Screen fan-out (bars).** Four screen-activation functions (0x102afd24,
  0x102f2910, 0x103ce4d8, 0x10565218) all enter activation fn 0x102355c6, and
  all four are invoked from one block inside fn 0x10595844 by a run of
  adjacent calls. That driver is the natural point where a screen-open event
  reaches the live-view path; it has no direct callers (entered indirectly).
- **Crop / image area.** The image-area writer is reached through a
  vtable-shaped function table at 0x11f9a4dc, not a direct menu call. The
  dispatcher that indexes that table uses a computed base and is not yet
  located.
- **AE-L/AF-L router.** The queued-input handler resolves to a registered
  input module (callback + per-code handler table at 0x1037a2c4), set up
  during task init from entry fn 0x1059c2c8. Its descriptor at 0x115c685c is a
  config block, not a name; the module is the generic queued-input/property
  router (codes 0x2082/0x2083), and AE-L/AF-L passes through it as logical ID
  41 → mask 0x2000. The module receives input via its callback rather than
  reading a button, so the physical transport is not expressed as a static
  branch inside EG.

## Open gaps, by weight

1. **AE-L/AF-L physical trigger (largest).** Mask 0x2000 is confirmed in the
   input path, but the sender is not. The module receives through a registered
   callback; the physical transport likely sits in the RTOS message/queue
   layer, outside EG's static call graph, and may not be recoverable from this
   image by static call-graph tracing alone. The next concrete step is RAM
   data-flow into the router work area (~0x20022000), not more branch tracing.
2. **Crop dispatcher.** What indexes the image-area function table at
   0x11f9a4dc (computed base) is not located.
3. **Bars fan-out entry.** How screen fan-out fn 0x10595844 is entered
   (indirect) is not located.
4. Live-view OK key: the live-view screen's key table is not found.
5. Menu entry for "Choose image area" and the XPan menu route: entry point
   unknown.
6. Updater digest input at 0x10000088: unmapped and off the user-facing path.

A recurring limit: three of the open leads (crop dispatcher, bars fan-out
entry, router writer) all require resolving addresses the code builds with
MOVW/MOVT or a base register, which this pass did not index.
