# One-button Subject tracking on AE-L/AF-L: build plan

Date: 2026-11-13. Written by Claude from the repository's existing findings,
with no firmware read, no simulator run and no camera contact. This is a plan,
not a finding, so nothing here goes into `facts.md`.

## Owner direction, 2026-11-13

The target is one-button Subject tracking again. The always-armed design is
set aside. This replaces the 2026-10-18 redirect in
[tracking-input-chain.md](tracking-input-chain.md#2026-10-18-owner-redirects-target-to-always-armed-tracking).
The F-268 to F-370 work on arming tracking automatically on Auto-area entry is
no longer the main thread. Work on the live AF object's `+0x40` writer can stop.

Required behavior, matching the stock Fn1 test (F-261):

1. With Auto-area AF selected and AE-L/AF-L assigned to Subject tracking, one
   press of AE-L/AF-L shows the tracking reticle. The reticle stays after release.
2. A shutter half-press starts tracking the subject.
3. A second press of AE-L/AF-L ends tracking.
4. Holding the button counts as one press. A release does nothing.
5. With any other assignment, AE-L/AF-L keeps its stock behavior.

## What already exists

| Part | State | Evidence |
| --- | --- | --- |
| Button identity | Mask `0x2000` maps to logical input 13 and event `0x28b`, labelled "AE-L/AF-L button". | F-229 |
| Native action | Fn1's handler `0x1036957c` calls action 45 (`0x10368b6e`) when setting `0x1150` is 77. | F-226 |
| Gap in stock | The AE-L/AF-L handler `0x10369468` reads `0x1184`/`0x1187`, handles 25 and 42 only, and never calls action 45. | F-226, F-241 |
| Menu entry | Private candidate adds "Subject tracking" to the AE-L/AF-L list and stores 77 in `0x1184`. | F-229 |
| Trigger | Accessor hook at `0x102f14b2` with a worker adapter and a rising-edge guard. The `0x102f0d30` hook was dropped. | F-247 |
| Edge control | Fresh, held, release, fresh gives exactly two action-45 calls in QEMU. | F-230, F-232 |
| Hook ABI | Continuation at `0x102f14b6` preserves registers, flags and SP. | F-248 |
| Press reaches tracking | Four AE-L/AF-L presses on the real body produced four `FocusMeteringMode` events. A second run produced two events for three presses. | F-266, F-267 |

## What is still open

1. **Physical delivery.** No trace shows that a real press produces the ring
   record read at `0x102f14b2` (F-223 to F-225).
2. **Start and cancel.** QEMU has no AF model, so no test shows action 45
   starting tracking from this path or cancelling it on a second press.
3. **Executable placement.** The candidate's code sits in the zero run in VA page
   `0x1002d000`. Nothing shows the camera maps that page as executable (F-233).
4. **Updater acceptance.** The camera offered only Done and Delete for
   candidate 01 (F-305). Candidate 02 was never put on a card.

## Proposed route: build on WonderLantern's builder

Upstream `WonderLantern/wonder-lantern-z30` reports installing standalone EG
modules on a Z30 C 1.20. Features such as photo zebra and date stamp are
reported working on hardware. Its builder appends all hook code to a tail that
starts at the end of the stock payload: `0x10020000 + 33939514 - 2 = 0x1207e038`.
That is the same address F-175 picked for a code append before the CRC.

This would close gaps 3 and 4 without new research:

- For gap 3, put the hook code in that tail instead of the `0x1002d000` zero
  run. Upstream features already run code from there on the camera.
- For gap 4, use upstream's build and CRC path, which produces modules the
  camera installs, instead of our private composer.

Gaps 1 and 2 stay. Both can only be settled by a press on the real camera.

Checked on upstream commit `264d6b0` (2026-11-14): no upstream feature edits
`0x102f14b2`, `0x10369468`, `0x1036957c`, `0x10368b6e` or the `0x10301f36`
dispatcher, so the hooks do not overlap. Each upstream hook uses the same
pattern: check the expected bytes, append Thumb code to the tail, and replace
the site with an 8-byte `ldr.w pc` jump. Our hook fits that pattern.

### Menu choice

Two ways to turn the feature on:

- **A. Native custom-control list (recommended).** Keep candidate 02's menu
  edits so "Subject tracking" appears in the stock AE-L/AF-L assignment list
  and stores 77. This matches how Fn1 works and needs no SD-card settings file.
  The edits already exist privately (45 spans, F-232).
- **B. Upstream Extensions menu.** Add an on/off row to upstream's Extensions
  menu, saved to the SD card. This needs no edits to the stock list, but it adds
  a second place to configure the button and pulls in the shutter-sound framework.

Use A. Fall back to B only if the stock list edits fail when ported.

### Steps

All steps run on the owner's Mac, where the firmware and pinned QEMU live.

1. Fork upstream and add a private preset, for example `ael-tracking`, in a new
   `features/ael_tracking.py`. The preset stays private and is never published,
   because it reads stock bytes at build time like every upstream feature.
2. Port the F-247 accessor hook and edge guard into the tail. Check the expected
   stock bytes at `0x102f14b2` before patching.
3. Port the candidate 02 menu edits (option A) as checked `plan.edit` calls.
4. Build `ael-tracking` alone. Don't combine it with `full` for the first test.
5. Re-run the F-232 fresh, held, release, fresh sequence in QEMU against the new
   image. Expect exactly two action-45 calls.
6. Hardware test, after the owner's go-ahead for that exact image. Install it,
   select Auto-area AF, assign Subject tracking to AE-L/AF-L, and check the five
   behaviors above. To recover, reinstall stock `Z_30_0120.bin` from
   Setup → Firmware version.

## Risks

- If presses don't reach `0x102f14b2`, the button does nothing. That is the
  likeliest failure, and it is safe: tracking just won't start.
- If action 45 fires twice per press, tracking starts and stops at once, so
  the reticle flashes and disappears. Step 5 guards against this before the
  hardware test.
- If the native list edits break the menu, the custom-control page may draw
  badly. Recover by reflashing stock firmware.
- Upstream's recovery note says reflashing works as long as the update page
  opens. That is upstream's claim. This repo has not verified it.

## Correction

[z30-tracking-activation-manual-crossref.md](z30-tracking-activation-manual-crossref.md)
says the Z30 may have no AE-L/AF-L button. The owner pressed it during the PTP
monitor runs (F-266, F-267), so the button exists.

Written by Claude in collaboration with Tony Kim.
