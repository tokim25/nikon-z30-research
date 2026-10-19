# Proposed read-only FocusMeteringMode descriptor query

Status: reviewed offline after F-266/F-267 linked AE-L/AF-L activity to PTP
property `0x501c`. The owner authorized testing on the camera on 2026-10-18
after review of this bounded method.

## Question

Read the current and default values and the camera-advertised numeric enum for
the specific property that generated the PTP events. This can show whether
the camera exposes an Auto-area/subject-tracking-related focus mode and whether
the value changes after the native Subject-tracking action. It cannot itself
identify a physical button or prove the firmware hook.

## Exact proposed method

Run once per snapshot, before or after an owner-controlled native action:

```sh
PYTHONPATH=src python3 -m nikon_z30_research.ptp_focus_mode_probe --read-focus-mode-descriptor
```

The probe selects only USB ID `04b0:0452`, inspects the active configuration,
and requires the one default Still Image PTP interface already observed on
this camera. It opens and claims that interface only if available; it does not
detach a driver, reset the camera, change configuration, or select another
alternate setting. A busy interface is a hard stop.

The only PTP commands are standard OpenSession (`0x1002`, session 1), one
GetDevicePropDesc (`0x1014`, parameter `0x501c`), and standard CloseSession
(`0x1003`). The standard operation returns a property descriptor from camera
to host; it does not set a property. The command is fixed in code to
`FocusMeteringMode` and cannot accept another property code. The response is
accepted only when it identifies property `0x501c` with type UINT16 and a
bounded enum/no-form descriptor. The output contains only the property name,
access mode, factory default, current numeric value, and supported numeric
values. It stores no raw PTP response or packet. Descriptor container size is
capped at 4 KiB plus the PTP header.

No property-set/reset, Nikon vendor operation, event poll, image capture,
object transfer, storage operation, firmware read, or firmware write is sent.
The code attempts one CloseSession after a successful OpenSession, then
releases the interface and closes the USB handle. If an unexpected operation,
container, property code, or data type is received, it stops without retrying.

## Recovery for a failed read

The method sends only standard PTP session-management and property-descriptor
read operations; it cannot change a camera property or persistent storage.
On a timeout or malformed response, the probe stops and attempts normal PTP
session and USB cleanup. Do not retry in that state. Disconnect USB and
power-cycle the camera normally to restore PTP availability. If the camera
does not return to normal operation after that, stop camera experiments and
use the owner's service/recovery route; firmware reinstallation is not needed
or attempted for this read.

PIMA 15740 defines `0x1014` as GetDevicePropDesc, with one DevicePropCode
parameter and responder-to-initiator data direction. It identifies property
`0x501c` as FocusMeteringMode, a UINT16 enum describing the automatic focus
mechanism. Standard values include generic center-/multi-spot modes; the
camera's returned numeric enum must be observed before assigning Nikon-specific
meaning. See the [PTP operation definition](https://ptacts.uspto.gov/ptacts/public-informations/petitions/1556893/download-documents?artifactId=ZCNYY4cBkARuZdDg7Ckj6pTBmRWMHsb-_mnOanITHL1iqwBuNytzabI) and
[property definition](https://ptacts.uspto.gov/ptacts/public-informations/petitions/1516315/download-documents?artifactId=nOUIu_EuqshngTSjLqqHlDaa5EipPs18x0USP2xSehuFmjsYHrh0LRU).

## Review boundary

Implementation: [`ptp_focus_mode_probe.py`](../src/nikon_z30_research/ptp_focus_mode_probe.py).
Synthetic tests cover command bytes, expected property/type, numeric values,
enum bounds, truncation, response-status reporting, and rejection paths. The
single host-USB query returned `0x200A` (`DeviceProp Not Supported`) for
property `0x501c`; the response did not contain a descriptor. The probe
retained no raw response. No firmware or raw camera data belongs in the
repository.
