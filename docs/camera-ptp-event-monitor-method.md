# Bounded PTP event-endpoint monitor

Status: the revised procedure has completed two 15-second camera runs after
the owner was warned and gave an explicit start signal each time. Four
AE-L/AF-L presses coincided with four `DevicePropChanged` events for property
`0x501c` in the first run; three presses coincided with two such events in the
second. Standard PTP references identify `0x4006` as DevicePropChanged and
`0x501c` as FocusMeteringMode. The event count is not a reliable key-press
count, and the event does not report the property's new value. The owner says
the same bounded event-monitor method does not need renewed approval, but
each run still needs a pre-run warning and explicit start signal. Any new
property-query method is a separate method and requires its own review and
approval. The owner authorized read/write experiments in principle and named
stock-firmware reinstallation as the recovery plan.

## Purpose

Check whether the Z 30 exposes any event containers over its PTP USB
interrupt-IN endpoint while the owner presses AE-L/AF-L or a control assigned
to Subject tracking. A reported event could connect a physical action to a
camera-visible event. No event is an inconclusive result: Nikon may not expose
physical button events through PTP, or may require a different interface.

## Exact method

Run the bounded monitor for 15 seconds while the owner performs a known
button sequence:

```sh
PYTHONPATH=src python3 -m nikon_z30_research.ptp_event_monitor --listen-events --seconds 15
```

The probe selects only USB ID `04b0:0452`, reads the active configuration,
requires one default still-image PTP interface with one bulk-IN, one bulk-OUT
and one interrupt-IN endpoint, then opens and claims that interface only if
available. It does not detach a driver, reset the camera, change the USB
configuration or select another alternate setting. If the interface is busy,
it stops without a transfer.

The only camera commands are standard PTP OpenSession (`0x1002`, session ID
1) and, after monitoring, CloseSession (`0x1003`). The probe performs no
vendor operation, property query or write, image capture, object transfer,
firmware read, or storage operation. During the 15-second window it issues
only USB interrupt-IN transfers on the event endpoint. The endpoint may have
an 8-byte maximum packet size; libusb is asked to collect enough packets for
one PTP event container of at most 24 bytes. The parser accepts only one
12-24-byte event container with up to three numeric parameters per transfer.
Timeouts and successful zero-byte transfers count as no event and continue
within the overall time bound; malformed nonempty packets stop the run.
The libusb API treats transfer length as a maximum and abstracts packet
boundaries, so a host transfer may collect multiple USB packets ([synchronous
I/O](https://libusb.sourceforge.io/api-1.0/group__libusb__syncio.html),
[packet handling](https://libusb.sourceforge.io/api-1.0/libusb_packetoverflow.html)).
The Still Image Capture Device definition specifies a 12-byte event header
and up to three 4-byte parameters in interrupt data ([USB class definition,
section 7.3](https://ptacts.uspto.gov/ptacts/public-informations/petitions/1556893/download-documents?artifactId=qE6lQbkSUyn1aAIncLWSD6nUr_OnLV3FWaze2meY3tyyUVYK-wsaW4w)).
It prints decoded PTP event codes and numeric parameters only; it does not print serial numbers,
raw packets, images or object content. It caps the duration at 30 seconds and
the output at 128 events. A successful OpenSession is followed by one
best-effort CloseSession even if event parsing fails; then the interface is
released and the handle is closed.

## Review and recovery

The implementation is isolated in
[`ptp_event_monitor.py`](../src/nikon_z30_research/ptp_event_monitor.py).
Synthetic tests cover exact session command containers and event-container
parsing. Source review shows no camera data-out transfer other than the two
standard session commands; no PTP vendor code is invoked. The event queue may
be consumed, and opening a session can conflict with tethering software, so
run only when no other host application is using the camera. A claim failure
is a hard stop.

The owner states that stock-firmware reinstallation is the recovery plan for
a camera write. This method does not write firmware or persistent settings;
the stock reinstall procedure has not been independently verified. If the
camera or USB session behaves abnormally, stop, disconnect USB and let the
owner recover the camera using their stated route. Do not retry automatically.

## Approval boundary

The earlier preflight and zero-byte failures are recorded as F-263 through
F-265. The successful windows and count mismatch are F-266/F-267. The code's
finally path attempts standard CloseSession, but its acknowledgement is not
exposed after another failure. The descriptor-only inspection is documented
in `camera-usb-descriptor-method.md`. The bounded procedure treats zero-byte
transfers as idle polls. Before another 15-second run, warn the owner and wait
for the explicit start signal; do not start the window before then. No
firmware bytes or raw event dumps were retained.
