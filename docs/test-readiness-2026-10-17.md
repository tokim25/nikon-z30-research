# On-camera test readiness record

2026-10-17. Preparation only. No camera was connected, flashed or touched.
Hardware remains **NO-GO** (see
[hardware-readiness.md](hardware-readiness.md) and
[build-phase-gate.md](build-phase-gate.md)).

## Latest status addendum, 2026-10-17

The private offline XPan candidate (F-198) has been built and independently
audited; see [handoff-codex.md](handoff-codex.md) for its retention warning
and [facts.md](facts.md) for the audit identity. Exact manifest edits, no
unplanned changes beyond the regenerated CRC
trailer, protected fields, file length/capacity, native CRC and area-4 table
layout pass. Nikon updater acceptance and real-camera behavior are unverified.
The owner's latest answer keeps lifecycle condition 1 **unmet**; earlier
waiver language is superseded. Hardware remains NO-GO. No connection,
write or flash was made or authorized.

**Owner reaffirmation, 2026-10-17 (F-201):** after reviewing that the shared
preview/capture path is not proven specific to new still-image creation, the
owner said to keep the XPan still-photo guard waiver. Possible area-4
preview-table effects in playback, movie or warning contexts remain accepted
and unmeasured. This does not waive lifecycle condition 1 or authorize a
camera write; hardware remains NO-GO.

## Exact-firmware identity: version level only

- Relayed by the session manager (owner update, 2026-10-17): a read-only USB
  identification reports firmware 1.20 (USB version 0x0120). The owner states
  the same firmware is the original file in the private WORK copy.
- Later relay (session manager): a read-only device-info check with
  `gphoto2 --summary` reports model Z 30 and version V1.20. The serial number
  is redacted and not recorded.
- Recorded: identity confirmed at version level (1.20), through the camera's
  own identification (read-only) plus the owner's statement. Not recorded:
  serial number.
- **Byte-exact match is NOT verified.** The camera's installed image cannot be
  read read-only, so the EG hash check has not been run against the camera.
- The private local extracted EG passes `require-verified-eg` at the pinned
  size and SHA-256. This confirms the source for the private manifest only;
  it does not establish the image installed in the camera or a modified
  package's integrity.

## Exact-firmware identity check: extracted EG verified

- Required identities, from [milestone-1-recovery.md](milestone-1-recovery.md):
  - Original package: 34,496,798 bytes, SHA-256
    `1a5449ef505f1f347ed4e066a6a3f588ea542240680e83f4ebcae3b16da3434a`.
  - Main EG module: 33,939,514 bytes, SHA-256
    `8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
- Command run from the repo root against the known private WORK copy; output
  contained only size, hash and verified status:

```bash
PYTHONPATH=src python3 -m nikon_z30_research require-verified-eg /path/to/extracted-eg.bin
```

  Exit code 0 returned. The original remains outside Git. The outer-package
  digest applies only to that alternative route; updater acceptance of the
  modified standalone EG remains unverified.

## Readiness state

| Gate item | State |
| --- | --- |
| Exact original identity (EG) | Verified for private extracted source; installed-code identity remains waived at version level only |
| Digest input at `0x10000088` | Unresolved (F-140, F-141) |
| Native standalone-EG route | Static path and private candidate checks documented; Nikon updater acceptance unverified ([native-standalone-eg-route.md](native-standalone-eg-route.md)) |
| Simulator acceptance, bars and geometry | Not complete |
| Lifecycle gate (condition 1 natural transitions) | **Unmet** by latest owner disposition; natural transitions remain unverified |
| Tracking physical input and activation | Assigned by owner to tracking-patch device test; not verified |
| Backup and recovery decision | Not recorded here; owner decision |
| Owner approval immediately before any hardware step | Not given |

## Owner dispositions at the camera-test stage (2026-10-17)

Recorded as the owner's decisions, not as gates passed. Reason, in the
owner's words: "owner accepted the risks, 2026-10-17".

1. **Lifecycle gate (build-phase-gate condition 1, natural transitions):
   unmet, not waived.** The owner's latest disposition explicitly keeps this
   gate unmet.
2. **XPan still-photo guard: waived.** Without it, XPan crop lines could appear
   during movies, playback or warnings. The owner accepts that outcome.

3. **Byte-exact identity of the installed firmware: waived by the owner (signed).**
   Reported by the session manager as signed on 2026-10-17 (commit `db6a95e`
   draft). Owner's reason, as given: "I assume the risks." Risk accepted: the
   installed image may differ from the original in ways the version-level check
   cannot detect.

4. **Tracking native-entry simulator evidence: assigned to the tracking-patch
   device test by owner direction (2026-10-17).** The simulator does not supply
   the physical AE-L/AF-L press. The owner directs that activation be tested
   with the tracking patch on the real Z 30. The unverified behavior remains
   an explicit test objective; it is not marked as passed. This disposition
   does not waive package/container integrity, exact planned edits, native
   eligibility and cleanup review, backup/risk binding, the test order, or
   separate immediate approval for the exact camera write.

A waiver does not approve any camera step. Local extracted-EG identity is now
verified. Nikon acceptance of the private standalone-EG candidate, recovery
and risk records, readiness promotion, and the owner's separate approval
immediately before any hardware step remain open. Hardware remains **NO-GO**.
No connection or flash was made.

## Tracking patch test disposition

The private tracking design has a coordinated 45-span manifest. Native menu
selection stores assignment 77; task allocation was measured at 11,264 bytes
versus 10,240 stock; constructed guard, cleanup and copy controls pass. The
physical press-to-native-event and start/stop/cancel lifecycle remain
unverified. The owner assigns those behaviors to a later real-device test
with the tracking patch because the simulator cannot produce the button
input. That test belongs after the owner's existing XPan test order and only
after an accepted artifact format, exact-build review, backup/risk record,
and a separate approval naming the exact write. No tracking patch image or
accepted update package currently exists.

Before the tracking patch can be marked ready for that device test, close the
candidate-side control that does not require a physical button: execute the
candidate action adapter in a bounded simulator diagnostic with a constructed
fresh-edge record and observe the native request/state and completion calls.
Include held/repeated input, a fresh second edge, combined input, and
unsupported/ineligible controls. Require one request on the fresh start edge,
no duplicate while held, the expected native stop/cancel transition on the
fresh second edge, and unchanged playback Protect. Distinguish request/state
transition from successful subject acquisition. A constructed adapter call
does not establish natural worker admission or physical press delivery; those
limits must remain explicit. If the candidate-side control cannot be run or
fails, do not transfer that uncertainty to the device-test exception.

For that eventual test, record assignment 77 selected for the shooting
AE-L/AF-L button; one fresh physical press in an eligible still/live-view
context; visible native subject-tracking start; no repeat while held; a fresh
subsequent press and the native stop/cancel result; and unchanged playback
Protect behavior. Stop the bounded test after a failed or ambiguous first
press, any unexpected state change, or loss of normal camera operation. This
acceptance record is not an installation procedure.

## Result

Test readiness is **not achieved**. The private XPan candidate passes exact
offline edit/integrity/layout checks, but Nikon acceptance and lifecycle
condition 1 remain unresolved. Recovery/risk binding, readiness promotion,
the required test order and separate write approval are also outstanding.
