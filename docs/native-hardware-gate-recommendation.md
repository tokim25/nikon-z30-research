# Hardware-gate recommendation

Owner-reported result, 2026-10-17: steps 1–5 of the selected method below
are reported complete. The camera firmware display was reported as “1.2,”
consistent with the project's C 1.20 target; the exact display formatting
was not independently captured. macOS reports **NIKON DSC Z 30**, manufacturer
NIKON, vendor ID `0x04b0`, product ID `0x0452`, USB product version `0x0120`
and a 480 Mb/s link. Serial number, location identifier and full report are
not copied into the repository. No unexpected activity was reported, but
this is not proof of zero writes or a hash verification of installed code.
The owner has not yet reported step 6 (idle shutdown/disconnection) complete.
Codex performed no camera operation. Lifecycle condition 1 remains unmet by
the owner's explicit choice; modified-firmware testing remains NO-GO.

Current update, 2026-10-17: the session manager conveyed explicit owner
authorization for the narrow owner-operated read-only connection. The owner
then asked Codex to choose the method. Separately, the owner directly chose
to keep lifecycle condition 1 unmet. The historical missing-approval wording
below is superseded for the read-only scope only; modified firmware remains
NO-GO. No camera has been accessed by Codex.

2026-10-17. Recommendation only. No connection, camera operation, firmware
load or hardware-state change is authorized or performed by this document.

## 1. Read-only connection first

Recommend a separately approved, owner-operated read-only identity/version
connection before considering a modified-firmware test. Its purpose would
be limited to identifying the camera and its installed firmware through a
supported interface. No settings changes, firmware loading, updater entry,
memory dumping or test-code execution belong in that scope.

The intended risk is lower because this step would not replace camera
firmware. It is not risk-free or certified safe. A connection is an active
interaction; calling a tool “read-only” does not prove its requests avoid
writes or other camera operations. The exact tool, interface and requests
must be reviewed before the owner uses them. A method that needs writes or
code execution falls outside the proposed read-only step.

A modified-firmware test carries substantially greater potential impact:
it changes the code the camera depends on to start and operate. A failure
could leave it unusable, with no verified way to restore it at home.

## 2. Gates before each step

[AGENTS.md](../AGENTS.md) requires a separate, explicit go-ahead even to
connect the camera, also says analysis is offline and never to touch the
camera, and leaves hardware operation to the owner under
[build-phase-gate.md](build-phase-gate.md). The current rules do not grant
an automatic read-only exception. The proposed distinction below requires
an explicit owner authorization; this recommendation does not amend either
file or mark the camera ready.

For a read-only connection, require all of the following:

- A written, bounded identity/version-only scope and a reviewed tool/interface
  whose requests stay inside that scope. **Unmet:** no concrete method has
  been validated for this step in the reviewed record.
- A stop rule: stop if the method requests an update, a settings change,
  write access, test-code execution or anything outside the approved reads.
  Any collected information stays local; proprietary data is not published.
- The owner operates the camera and explicitly approves this particular
  session immediately before connection, including a narrow exception to
  the current offline/no-camera restriction. **Unmet:** no such approval
  has been given here.

Feature simulator tests and a patch package are not technical prerequisites
for reading identity/version information. However, because the existing gate
uses “any hardware step” wording, that narrower read-only scope must be
expressly authorized rather than assumed to bypass the gate.

Before a modified-firmware test, all six existing build-gate conditions
remain applicable:

| Gate | Current state |
| --- | --- |
| Simulator behavior and relevant state transitions | Unmet: native startup, menu return, playback and warning coverage remain unverified. Any exception must be explicit; diagnostic passes are not lifecycle acceptance. |
| Exact original and only planned changes | Exact original identities and offline verification tools exist. Unmet for a final modified camera package: no such package is accepted; the native digest still has missing input. |
| Layout, instruction mode, branches, registers, stack and returns reviewed | Bounded F-148/F-160 contracts pass. Global exact-build review and the relevant eligibility/lifecycle guarantees remain incomplete. |
| Offline original backup and recovery/risk record | The verified original is preserved locally. The concrete test record must bind its backup and explicit service-or-total-loss acceptance to the exact build; a working recovery route is unverified. |
| Hardware-readiness record names the exact build/test and says READY FOR AN EXPERIMENTAL HARDWARE TEST | Unmet: current status remains NO-GO. |
| Owner approval immediately before that concrete hardware test | Unmet. Read-only approval would not satisfy this separate approval. |

## 3. Recovery basis: accepted service-or-total-loss risk

For planning, record the requested recovery disposition as **accepted
service-or-total-loss risk**, explicitly **not safe** and **not a verified
recovery path**. General personal-use hardware risk acceptance is already
recorded in the project. This disposition does not establish that service
will repair the camera or that the owner can restore the original.

The [recovery plan](recovery-plan.md) must continue to say that a verified
independent recovery method is absent. A preserved original is not proof
that a camera which no longer starts can load it. Recovery may require
Nikon service, may be refused or unsuccessful, or may be impossible.

Before any modified-firmware test, the owner must explicitly accept those
consequences for the exact named build/test under condition 4. This planning
record does not manufacture that final consent or waive the remaining gates.
It also does not turn the proposed read-only step into a safe operation.

## 4. Effect of the unresolved feature paths

The XPan still-photo eligibility guard is not proven. Empty screen stack
plus live-view selector 1 is a UI-state check, not a guarantee that bars stay
out of every excluded state. This does **not** block the proposed identity/
version-only connection, because that step would run no patch. It remains
unresolved evidence for modified XPan firmware; the owner must retain the
applicable acceptance gate or explicitly accept the named coverage gap.
The later stills-only prototype scope does not reintroduce movie-transition
research as a prerequisite, and does not prove movie exclusion.

The AE-L/AF-L tracking entry path is also unverified. It does **not** block
an identity/version-only connection or a bars-only candidate that contains
no tracking edits. It blocks acceptance of a tracking-enabled modified build.
Keep tracking out of the first candidate, following the owner's existing
XPan-first test order. Neither unresolved feature path is permission to
connect the camera today.

## 5. Exact owner decision needed for the first step

Choose whether to authorize the bounded read-only route while keeping every
modified-firmware test NO-GO. The proposed decision is:

> I authorize one owner-operated, read-only connection to identify my Z30
> and read its installed firmware version, after the exact tool/interface
> and requests have been reviewed to stay within that scope. This is a
> narrow exception to the offline/no-camera restriction. It does not
> authorize settings changes, firmware loading, memory dumping, test code
> or modified-firmware testing. I will give the session-specific go-ahead
> immediately before the connection.

That decision would permit preparation of the specified read-only step;
actual connection still waits for the method review and immediate owner
go-ahead. It would not mark the feature simulator-accepted or the camera
ready for modified firmware. No such decision is inferred from a general
“Go,” prior risk acceptance, or the request to write this recommendation.

## Selected method and owner-operated steps

Use the camera's own firmware-version display for the installed version,
and Apple's built-in System Information for host-side USB identification.
Local application metadata, read without probing connected devices, identifies
System Information 11.0, build 915, on this Mac. No camera-control utility,
custom script, camera command or firmware tool is selected.

The method review is limited to these documented informational functions;
it is not a USB traffic audit or proof that macOS/background software issues
no writes. Closing camera applications and seeing no update prompt are scope
checks, not proof of zero writes. No firmware/setting write is requested by
these steps. If strict proof of zero writes is required, the connection is
not certified to that standard.

1. Have a charged battery, the preserved verified original offline, and a
   known-working USB data cable. Close camera-control, transfer, import,
   sync and update applications before connection. Do not change camera or
   computer settings for this check.
2. With USB disconnected, view camera **MENU → Setup (wrench) → Firmware
   version**. Record the displayed **C** version; do not select an update.
   If it is not C 1.20, stop and report the mismatch with this project's
   original rather than trying to change the camera version.
3. Exit the display. Turn the camera off, connect directly to a Mac USB
   port with the data cable, then turn it on. Do not use an update utility,
   start a transfer or change USB settings.
4. On the Mac, hold **Option** and open **Apple menu → System Information**.
   Select **Hardware → USB**, then the Nikon/Z30 entry if present. Record
   only the displayed device identity and vendor/product identifiers.
   A USB descriptor labelled “Version” is not evidence of the Nikon C
   firmware version; use the camera display from step 2.
5. Confirm no other camera application starts or acts, no transfer is
   running, and the camera shows no update/write/progress screen. Record
   date/time, camera C version, Mac/tool version and a private screenshot
   of the selected device. Keep serial numbers and full system reports
   private. Record any unexpected activity; do not call the session verified
   read-only if it occurred.
6. Finish only when idle and no transfer/access operation is in progress:
   turn the camera off before disconnecting its USB cable. Do not interrupt
   an unexpected ongoing operation or force a reset; stop issuing requests
   and report its state instead.

Stop immediately if an update, format/initialize, settings/sync action or
unexpected transfer is offered or starts, if another camera application
launches, if the camera is not identified, or if an error/unexpected screen
appears. Do not troubleshoot by changing settings or trying commands.
These are owner instructions; Codex does not operate the camera.

Sources reviewed for this method:
[Nikon firmware-version display](https://onlinemanual.nikonimglib.com/z30/en/16-01.html),
[Nikon USB connection precautions](https://onlinemanual.nikonimglib.com/z30/en/11-01.html),
[Apple System Information](https://support.apple.com/guide/system-information/system-information-syspr35536/mac).
Only the informational display/connection parts are used; image-transfer
and update procedures are outside the selected method.

This is **not safe or guaranteed recoverable**. Recovery remains the
accepted **service-or-total-loss risk** described above. No hardware action
was performed, and no modified-firmware gate was waived.
