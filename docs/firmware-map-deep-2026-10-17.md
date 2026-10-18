# Firmware static map — deeper cross-reference pass (2026-10-17)

Companion to [firmware-map-2026-10-17.md](firmware-map-2026-10-17.md). This
pass added a static branch/literal/pointer cross-reference index over the
decoded EG module (base 0x10020000) and read several on-image data tables
directly. Addresses and descriptions only: no firmware bytes, no hex/base64
dumps, no raw table listings, no patch. Extracted components and raw table
dumps stay outside the repository per AGENTS.md.

Every "reached from" link is a static reference, not a runtime trace.
Function-start (prologue) detection is heuristic. Confidence: **confirmed** =
observed static code/data link; **likely** = inferred; **unknown** = not
established.

## Method and its one hard limit

The index covers Thumb and ARM BL/BLX/B branches and literal-pool pointer
loads. It does **not** resolve addresses the code builds with MOVW/MOVT
immediate pairs or from a base register. That gap is load-bearing: three of
the most useful remaining leads below dead-end precisely on MOVW/MOVT-built
addresses, and resolving them needs an index pass this work did not do. (In
this project that pass belongs to the Codex lane.)

## Confirmed call chains

| Target | References | Role | Confidence |
|---|---|---|---|
| 0x102f1e10 | 34 branch refs | Central live-view routine | confirmed ref; role likely |
| 0x103ce96e | 7 branch refs; literal at 0x104759e8 | Key dispatcher (screen-stack) | confirmed |
| 0x104e2cbc | from 0x103ce884, 0x103ce94c | Key filter: diverts OK (0x27e) to live view | confirmed |
| 0x101e383a | from 0x1008ad6e, 0x103a3e88, 0x103a400c | Input-cache setter; all 3 documented callers reached | confirmed |
| 0x103a3d14 | via 0x10379a68 ← 0x10379b3e | Queued-input handler for code 0x2083 | confirmed |
| 0x102f0d14 | 7 branch refs | Input-snapshot writer | confirmed ref |
| 0x102f0e38 | from 0x102f1dbc, 0x102f28fa | Mask decoder (bit → internal code 0x1b) | confirmed |
| 0x1008d38c | from 0x1008a146 (in fn 0x10089682) | Image-area writer | confirmed ref |
| 0x10597440 | from 0x105979a4, 0x10597bae | Crop-table ratio function | confirmed ref |
| 0x1073b400 | 4 literal refs (0x10459344..0x10459376) | Input-map table | confirmed |

## Three subsystem results

### Live-view bars — screen fan-out driver
The documented bar hook sites are instruction points inside functions, not
entries. Seating them: 0x102f5810 is in fn 0x102f57e2; 0x102355f4 is in
activation fn 0x102355c6; 0x102355c0 is in fn 0x10235576. Four
screen-activation functions (0x102afd24, 0x102f2910, 0x103ce4d8, 0x10565218)
all enter fn 0x102355c6, and all four are invoked from one block inside
**fn 0x10595844** by a run of adjacent calls. That driver is the natural point
where a screen-open event reaches the live-view path — the hook candidate for
turning bars on/off per screen. Its own entry is indirect (not located).

### Crop / image area — a function-pointer table
The image-area writer 0x1008d38c is reached through a vtable-shaped table of
same-subsystem function pointers at **0x11f9a4dc** (run 0x11f9a4d8..0x11f9a518+,
all into the 0x10058xxx/0x1005dxxx cluster; the writer's top function 0x10058a82
is one entry). So the writer is dispatched through this table, not called
directly from a menu. The dispatcher that indexes the table uses a computed
base and is not yet located.

### AE-L/AF-L — a registered queued-input router
The queued-input handler resolves to a registered input module: handler
fn 0x10379d5a is installed as a callback by registrar fn 0x10379fc0 (pointer
stored in a registration record at 0x1037a2c4, alongside a per-code handler
table at 0x1037a2d0..0x1037a2f4 and a config descriptor at 0x115c685c). The
registrar runs from a task-init path topped by entry fn 0x1059c2c8. The
descriptor at 0x115c685c is a config block (flags plus DRAM work-area pointers
around 0x20022000), not a name — so this is the generic queued-input/property
router (codes 0x2082/0x2083), not an AE-L/AF-L-specific module. AE-L/AF-L
passes through it as logical ID 41 → mask 0x2000. The module receives input via
its callback rather than reading a button, which is why the physical transport
is not a static branch inside EG.

## Named hardware-switch table (0x1072e3b0)

The firmware holds a full named-switch table: 40-byte slots (a name, then a
32-bit mask), covering three input registers. Summary by register (bit values
in parentheses for the controls that matter to the user stories):

- **SW0 (shooting register):** the d-pad (eight directions) and CENTER; FUNCTION
  (0x4000); **AEAF_LOCK (0x2000)** and AEAF_LOCK_VPOS (0x1000); EXP_MODE,
  EXP_CORRECT, MAIN, ILLUMINATE, BRACKET, FLASH; **AF_ON (0x200000)** and
  AF_ON_VPOS; F_MIN; RELEASE_HALF / RELEASE_ON (with VPOS and 10PIN variants);
  and unused ("BLANK") bits.
- **SW1 (playback/menu register):** INFO, HELP, PROTECT, **LIVEVIEW (0x10)**,
  ZOOM, THUMBNAIL, PLAY, **OK (0x1)**, **MENU (0x8000)**, DELETE,
  **MOVIE (0x2000)**, PICTURE_CONTROL, **I (0x400, the "i" quick menu)**,
  CENTER_VPOS; a second run of *_VPOS d-pad copies; and the front-dial
  functions QUALITY, WB, ISO, AF_MODE, RELEASE_MODE, AE_MEASURE_MODE,
  FUNCTION_VPOS, FUNCTION_10PIN.
- **SW2 (sub-selector / Fn register):** sub-selector directions and center,
  FN2/FN3/FN4, WIFI, MAP, ACTION, DISP, FEATURE, and unused bits.

The table pointer is stored at 0x1072e304. Consequences for the user stories:

- **AE-L/AF-L is SW0 bit 0x2000**, a dedicated bit distinct from every d-pad
  direction and from AF_ON. This agrees with two other paths already in the
  repo — the queued-bank route maps logical ID 41 → mask 0x2000, and the
  structured-record selector-5 path stages mask 0x2000 at 0xc1811e74 and
  caches it at 0xc181182c+0x30. Three independent places now concur.
- **The "i" button is SW1 bit 0x400 (ID_SW1_I)**; LIVEVIEW, MENU, MOVIE and OK
  are all named SW1 bits. This names the controls behind Story 1's "i"-menu
  route and the live-view/menu transitions.

This table maps control name → hardware bit. It does **not** map a hardware bit
to an input code in 0x1073b400; the firmware scans the SW registers to produce
input codes elsewhere, and that scan — plus the code that writes the SW
register words — is still being traced.

## SW-register read path and the live scan

- The named-switch table is consumed only by an isolated registrar/naming
  module (fn 0x1033ce76): debug naming, not the live input scan.
- The live read path for AE-L/AF-L, by confirmed index edges: handler
  0x103a3d14 (maps mask 0x2000 → logical ID 41) → dispatcher 0x103a3b9c (reads
  the SW-bank word at 0x115c694c) → consumer 0x103a3f9e → setter 0x101e383a →
  structured record 0xc1811e74. The mask→ID-41 step relies on the prior repo
  fact; that handler body is MOVW/register-indirect and was not re-decoded.
- The input-map consumer (fn 0x10459342, map 0x1073b400) is a parallel
  translator whose junction with this path is not established.
- **Cleanest AE-L/AF-L hook candidate:** the ID-41 handler/dispatcher pair
  operating on the SW-bank word 0x115c694c.
- Writers: fn 0x103a3df6 only initializes the bank pointer (store at
  0x103a3e58), not the bits. The bit-source writer was not found via plain
  literal/pointer references; the live bits arrive through register-indirect
  or MOVW-built addresses, so it is a Codex lead.

## Action half: tracking-activation subsystem (corrected)

"One-button tracking" needs an **action** target (what starts subject tracking)
to wire the AE-L/AF-L detection hook to. This pass corrected which subsystem
that is.

- **The earlier "tracking candidate" cluster is Bluetooth, not AF tracking.**
  The functions 0x11cf4e90 / 0x11cf4ea0 / dispatcher 0x11cf5774 / matcher
  0x11cf5248 belong to Bluetooth HCI packet handling: nearby strings are
  "Tracking BtPacket" (0x11cf4dbc), "Tracking HCI Rx Buffer" (0x11cf51d0),
  "Bluetooth" (0x11cc70d0), "Read Remote Features", "Remote name request".
  The word "Tracking" there means tracking Bluetooth packets. This cluster is
  **ruled out** as the one-button-tracking action target, and its registration
  is not relevant to tracking.
- **On-camera subject tracking is the AF-area-mode subsystem.** The AF-area
  mode label table is at 0x103edda0: PINPOINT, SINGLE-POINT, WIDE-AREA(S),
  WIDE-AREA(L), DYNAMIC-AREA, **3D-TRACKING** (label 0x103eddfc), AUTO-AREA.
  The label routine is at 0x103edc2e. AF settings sit near 0x11c9b.. (e.g.
  AfAreaMode*, AfTrackingSensitivityMovie). Subject tracking is the
  3D-TRACKING AF-area mode (with subject detection in Wide/Auto modes).
- **The AE-L/AF-L button's behavior is governed by**
  `eDSID_Setting_FuncAeAfLockButtonShooting` (and `...Movie`).
- The AF-area label table and the 3D-TRACKING string have **no plain
  branch/literal/pointer references** — they are reached through MOVW/computed
  addresses, so the AF-area-mode consumer/set function and the button
  option→action dispatch need the address-building pass (Codex lane).

Revised action-half questions for the Codex lane:
1. Resolve the AF-area-mode consumer/set function from label table 0x103edda0 /
   label routine 0x103edc2e.
2. Resolve the `eDSID_Setting_FuncAeAfLockButtonShooting` option→action
   dispatch: whether an option engages 3D-TRACKING / AF-ON-with-tracking — the
   hook that turns an AE-L/AF-L press into subject tracking.

**Bottom line for one-button tracking:** the detection hook is confirmed
(ID-41 / SW-bank word 0x115c694c); the action target is now correctly located
(AF-area 3D-TRACKING mode), replacing the mistaken Bluetooth candidate; the
exact set function and the button-option mapping remain for the Codex address
pass.

## Open leads, by weight

1. **AE-L/AF-L transport (largest).** Mask 0x2000 is firmly placed (SW0 bit,
   logical ID 41). What remains is the SW-register reader (bit → input code)
   and the writer that fills the SW0 word — and where that word's source is
   (hardware/driver read vs. decoded packet, likely below EG in the RTOS
   layer). The reader/writer trace is in progress.
2. **Crop dispatcher.** What indexes the image-area function table at
   0x11f9a4dc (computed base).
3. **Bars fan-out entry.** How screen fan-out fn 0x10595844 is entered
   (indirect).

Leads 2 and 3, and the SW-register writer in lead 1, all require resolving
MOVW/MOVT-built or base-register addresses — the one pass this work did not do
and which belongs to the Codex lane.
