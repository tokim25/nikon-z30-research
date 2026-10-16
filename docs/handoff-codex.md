# Final Codex handoff for Claude

Updated 2026-10-16. Offline research is finished for this session; the owner
requested an 8% remaining-usage cutoff. No agents continue working. No
installable firmware was produced. Personal build work is open; hardware
access remains closed.

The owner resumed tracking and approved Codex taking over guide/native and
RAW-crop documents. PR #35 records that transfer. Older paused-lane notes
are stale. Agree ownership before concurrent edits; simulator infrastructure
retains its previous assignment.

## GitHub integration

All milestone branches start from main `32a9da5`, rather than from each
other. The dedicated worktree is `work/codex-tracking-resume`; the primary
checkout remains on main. Codex has merged nothing. Owner or Claude should
retain every report and append-only fact during integration, then use THIS
handoff instead of older branch copies. The owner approves merges.

| PR | Fact | Result |
| --- | --- | --- |
| [34](https://github.com/tokim25/nikon-z30-research/pull/34) | F-025 | Two input-ring writers correct F-021. |
| [35](https://github.com/tokim25/nikon-z30-research/pull/35) | F-026 | Separate bit-13 namespaces; approved document transfer. |
| [36](https://github.com/tokim25/nikon-z30-research/pull/36) | F-027 | Structured numeric control reaches the cache; physical source unknown. |
| [37](https://github.com/tokim25/nikon-z30-research/pull/37) | F-036 | Centered 5200 by 1920 capture geometry, two A/B/A runs; no saved RAW. |
| [38](https://github.com/tokim25/nikon-z30-research/pull/38) | F-029 | Empty assisted live-view screen stack; populated menu control. |
| [39](https://github.com/tokim25/nikon-z30-research/pull/39) | F-028 | Registered candidate input route parses numeric commands. |
| [40](https://github.com/tokim25/nikon-z30-research/pull/40) | F-035 | Compose completion callback is too late for the current flush. |
| [41](https://github.com/tokim25/nikon-z30-research/pull/41) | F-037 | Simulator has functional ISP support; no verified saved-RAW path. |
| [42](https://github.com/tokim25/nikon-z30-research/pull/42) | F-040 | Retained native border color survives multiple refreshes. |
| [43](https://github.com/tokim25/nikon-z30-research/pull/43) | F-042 | Stock native masks persist after diagnostic setup; independent repeat. |
| [44](https://github.com/tokim25/nikon-z30-research/pull/44) | F-038 | Bank-mapped queued input reaches cache; physical source unresolved. |
| [45](https://github.com/tokim25/nikon-z30-research/pull/45) | F-043 | Selected bank maps logical ID 41 to mask 0x2000; identity unresolved. |
| [46](https://github.com/tokim25/nikon-z30-research/pull/46) | F-041 | Mode selector initializes despite empty screen stack; bounded registry lookup. |
| [47](https://github.com/tokim25/nikon-z30-research/pull/47) | F-039 | Geometry-like structure pack reaches processing submission, not proven NEF. |
| [48](https://github.com/tokim25/nikon-z30-research/pull/48) | F-044 | Two mask toggle cycles pass; mask remains over audited menu entry. |

Merge earlier facts before their follow-ups, preserving all entries. All
PRs #34 through #48 had successful checks on their published heads when
reviewed this session. This final handoff branch carries no new finding.
F-025 through F-044 are allocated; next free is F-045 after rechecking
main and open PRs.

## Single next step

Establish native clip-state cleanup on menu entry and a verified return to
live view. Start with the config ownership around initializer `0x104b5fd4`,
which copies the flag/bounds from config offsets `+8/+0xc`. It also performs
surface initialization: do not call it as though it were a clip-only setter.
Audit its callers and complete argument contract before a new runtime test.

The strongest result is F-042. Native geometry setter `0x104b7976` with
bounds (-1, 106, 721, 374), color setter `0x104540ee` with opaque black and
retention 1, plus ONE diagnostic guest-data clip flag at
`0xc1d87838 + 0x2c`, produces persistent stock black borders. No per-cycle
drawing calls or queue-gate override were used. At 720 pixels wide, rows
107 through 372 remain visible: 266 rows, a rounded 65:24 display crop.

Two independent calibrated runs pass autonomous refresh and three explicit
refreshes. Earlier bounds (0, 107, 720, 373) FAILED calibration: only 264
visible rows and unwanted side borders. F-044 adds two on/off cycles and
an independent repeat. Off restores baseline pixels outside the animated
band. The mask remains after audited menu entry and can cover menu graphics.
Calling live-view entry afterward leaves two screen-stack entries; it
does not prove natural menu exit. This is still diagnostic setup, not
automatic startup, saved-image cropping or a finished camera feature.

## Other trails to preserve

Tracking: F-038 selects rows by
`0xc18c9a7c + 128 * BYTE(0xc18c9a64) + 8 * row`, at most 16 rows.
The selector is a BYTE; earlier provisional relative-pointer/word readings
were rejected. Query `0x103a3cb0` selects bank 1. Logical ID 41 maps to
mask 0x2000 there, but this does not establish physical SW0 AE-L/AF-L identity.
Property event 0x2083 at `0x103a3d14` queues a record whose ID is byte
`+0x11` and operation byte `+0x10`; upstream is
`0x10379f00 -> 0x10379a68 -> 0x103a3d14`.
Trace that producer toward transport and press/release semantics. No tracking
entry point, reticle transition or physical-button delivery is verified.

F-041 separates state systems: assisted live-view object's selector
`+0x74` changes 4 to 1 while screen-stack count stays zero. Do not infer
that an empty stack means the mode object never initialized. Registry
getter `0x104571fe` computes base + 44 * ID after checking group < 7;
it does not validate ID bounds or a null base. Do not guess IDs.

RAW: F-039 builder `0x101e779c` packs source halfwords `+0x208..+0x218`
into `+0x47c..+0x48c`. Caller `0x101ea022` uses argument + 0x1c and
destination `0xc233addc`; later `0x100aa43a` copies 2024 bytes before
submission `0x100c9f24`. Source identity with earlier capture requests is
unproven. The follow-on worker can reach processing configuration on selected
paths, not verified NEF serialization. TIFF-like constant matches reviewed were error/UI values.
Do not call this a metadata writer or claim each field reaches hardware.

Private follow-on source-buffer leads: pointer `0xc1885da8`, allocation
`0x101e7430`, getter `0x101ea1ee`, exposure `0x10317d94`, consumer
`0x10318160`. They may belong to a supplied transfer context rather than
ordinary capture. This remains a lead, not an established capture contract.
Private windows: `codex-agent-pack-submit-worker-20261016-01` and
`codex-agent-native-output-interface-20261016-01`.

## Private reproduction

Confirmed WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Inputs and existing helpers are immutable. New codex-prefixed helpers and
outputs stay outside Git. Each report gives a command using a fresh output
directory. Runtime helpers disable bytecode writes, use absolute private
output paths and choose their own debugger ports.

| Result | Private helper | Independent root run |
| --- | --- | --- |
| Persistent mask | `codex-guide-clip-mask-private.py` with `--bounds -1 106 721 374` | `codex-root-clip-mask-20261016-01` |
| Mask toggles/menu | `codex-guide-mask-reliability-private.py` | `codex-root-mask-reliability-20261016-01` |
| Packed structure | `codex_agent_geometry_pack_verify_private.py` | `codex-root-geometry-pack-20261016-01` |
| Queued route | `codex-agent-queued-input-verify-private.py` | `codex-root-queued-input-20261016-01` |
| Selected bank | `codex-agent-input-bank-verify-private.py` | `codex-root-input-bank-20261016-01` |
| Mode/registry | `codex_mode_object_20261016_private.py --menu-control` | `codex-mode-object-20261016-run-01` |

Run with `"$WORK/analysis-env/bin/python" "$WORK/HELPER" --output "$WORK/private-inputs/codex-FRESH"`.
Use the report for complete arguments. Raw listings, pixels, logs and
firmware remain private. Unpublished root live-view windows
`codex-liveview-type3-20261016-08` and
`codex-liveview-type3-filter-20261016-09` are incomplete leads, not findings.
Linear windows can cross literal pools; validate branches and register flow.

All publication branches passed 54 synthetic tests, artifact and encoded-data
checks. Fact allocation was checked across main and all 15 milestone branches;
each pending fact has one source branch. Before publishing new work, run:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 .github/scripts/check_artifacts.py
python3 .github/scripts/check_byte_dumps.py
```

The verified
original module and pinned clean simulator were checked by runtime helpers.
No patch builder, original instruction change, hardware or installation
workflow was used. Restore owned guest fields, then discard each process.

Hardware readiness stays NO-GO: natural startup and mode cleanup, saved RAW
behavior, physical-button tracking, combined feature checks, containment and
recovery remain unresolved.

Written by Codex in collaboration with Tony Kim; continues Claude's research and includes independent Codex agent experiments and reviews.
