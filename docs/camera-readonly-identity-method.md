# Read-only camera identity and operation inventory

2026-10-18. The bounded identity probe is implemented in
[`ptp_device_info.py`](../src/nikon_z30_research/ptp_device_info.py) and
tested with synthetic PTP datasets. It successfully completed the identity
query on the connected camera using host USB access (F-258).
Modified-firmware hardware testing remains
**NO-GO** ([hardware-readiness.md](hardware-readiness.md)).

## Scope

The probe reports manufacturer, model, device-version string, vendor
extension information, and the operation codes the camera advertises. This
may reveal whether the camera advertises a candidate read operation, but the
probe does not invoke it. PTP DeviceInfo does not expose runtime TTBR0 memory
or verify the installed firmware byte for byte.

## Exact request and invocation

- One standard PTP GetDeviceInfo operation (`0x1001`, transaction ID zero)
  is sent over USB. [CIPA's PTP-IP specification](https://cipa.jp/std/documents/e/DC-X005.pdf)
  permits transaction ID zero for GetDeviceInfo before a session is open;
  the probe therefore sends no OpenSession or CloseSession request.
- The exact command, with the camera connected in normal shooting mode, is:
  `PYTHONPATH=src python3 -m nikon_z30_research.ptp_device_info --read-device-info`
- No additional Python package is needed. The probe uses Python's standard
  library and the already installed `libusb-1.0` runtime.
- It selects only USB ID `04b0:0452`, inspects the active USB configuration's
  default Still Image PTP interface, and sends the single standard request.
  It does not set a USB configuration or alternate setting, detach a kernel
  driver, reset the device, or try another command if the read fails. If the
  interface is busy or unavailable, it stops without taking it from another
  app.
- No object, image, device property, event, or Nikon vendor operation is
  requested. The serial field is parsed only to validate response bounds and
  is discarded; it is never printed or saved.

## Operation review and limits

The command builder emits only operation `0x1001`, with no parameters and no
data-out phase. The response parser accepts only the matching DeviceInfo data
and success response containers. The module has no API for any other PTP
operation. Its only bulk-OUT transfer is that GetDeviceInfo command; it does
not call libusb's configuration, alternate-setting, reset, control-transfer,
or detach-driver APIs. It stores no response file and omits the serial number
from output.

Synthetic tests cover the emitted request, bounded parsing of identity and
advertised operation codes, truncated data, and container lengths. The
hardware identity run succeeded with host USB access; the serial was omitted.
If the host cannot claim the interface, the probe stops; it does not fall
back to `gphoto2`.

The `ctypes` definitions for libusb device, endpoint, interface,
alternate-setting and configuration descriptors were compared with the
installed libusb C header using the local C compiler. Their sizes and the
field offsets read by the probe match on this host. This removes a host ABI
layout uncertainty but does not test camera-specific descriptors, interface
claim behavior or PTP responses.

**Host transport result, 2026-10-18:** macOS IORegistry listed the connected
Z 30 (`04b0:0452`), while sandboxed Python and native C libusb 1.0.30
enumeration returned zero devices. The exact probe initially stopped before
opening a handle or sending a command. With host USB access, the same reviewed
probe then sent only GetDeviceInfo and returned model Z 30 and device version
V1.20 (F-258). It also returned the advertised operations, with serial omitted.
The USB descriptor release `0x0120` is separate metadata; the firmware
version comes from the PTP response. Unknown operation `0x9535` is not
authorized for invocation.

The probe is not a live-memory reader. An advertised Nikon vendor operation
would require a separate source review, exact-method review, and approval
before any use. Do not send guessed vendor commands.

## Comparison and handling

- Compare the reported firmware version with the identity in
  [milestone-1-recovery.md](milestone-1-recovery.md). This is a version-level
  check only.
- No serial number, camera-derived hash, firmware bytes, or response dump is
  written to the repository.
- Read-only Z 30 identity is pre-approved under [AGENTS.md](../AGENTS.md);
  that authorization does not extend to live-memory access, firmware
  readback, or camera writes.

Nothing in this method authorizes a vendor command, live-memory read, byte
dump, flashing, or any write to the camera.

**Owner update, 2026-10-18:** the owner has since authorized read/write
experiments in principle and identified reinstalling stock firmware as the
recovery plan for a future camera write. This identity method remains limited
to GetDeviceInfo. Any additional camera operation still needs its own exact
method review and method-specific approval; the recovery route has not been
independently verified.
