# Proposed read-only USB descriptor inspection

Status: approved and run on 2026-10-18. It found the expected standard PTP
interface with an 8-byte interrupt-IN endpoint. See F-264.

## Purpose

The event monitor could not identify exactly one default PTP interface with
the expected interrupt-IN endpoint. This method would report the active USB
interface and endpoint descriptors to determine why the event monitor's
preflight did not match. It sends no PTP command and reads no camera state.

## Exact method

Run with host USB access while the Z 30 is connected:

```sh
PYTHONPATH=src python3 -m nikon_z30_research.usb_descriptor_report --inspect-descriptors
```

The tool selects USB ID `04b0:0452`, reads the active configuration descriptor,
and prints each interface's number, alternate setting, class, subclass,
protocol, and endpoint address, direction, transfer type, maximum packet size,
and interval. It does not open or claim a device handle, detach a driver,
change configuration or alternate setting, reset the camera, or transfer any
PTP data. It omits manufacturer, product, serial, and raw descriptor bytes.
It exits if zero or multiple matching cameras are found.

## Approval boundary

The owner approved this exact descriptor-only diagnostic. It does not
authorize another event-monitor attempt, another PTP command, a property
read/write, live-memory access,
firmware readback, or any camera write. The owner identifies stock-firmware
reinstallation as a recovery route for a future write; that route remains
unverified and is irrelevant to this read-only descriptor method.
