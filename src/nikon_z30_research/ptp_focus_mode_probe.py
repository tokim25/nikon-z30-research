"""Read only the standard PTP FocusMeteringMode descriptor from a Z 30.

This proposed probe sends OpenSession, one GetDevicePropDesc request for
property 0x501c, and CloseSession. It never sends a property-set, vendor,
object, capture, or firmware operation. Do not run on a camera until this
exact method is reviewed and approved.
"""

from __future__ import annotations

import argparse
import ctypes
import json
import struct

from .ptp_device_info import (
    PTPError,
    PTP_CONTAINER_COMMAND,
    PTP_CONTAINER_DATA,
    PTP_CONTAINER_RESPONSE,
    PTP_RESPONSE_OK,
    Z30_PRODUCT_ID,
    Z30_VENDOR_ID,
    _ConfigDescriptor,
    _ContainerReader,
    _DeviceDescriptor,
    _LibUSB,
    _bulk_transfer,
    decode_container,
)
from .ptp_event_monitor import (
    PTP_CLOSE_SESSION,
    PTP_OPEN_SESSION,
    _find_ptp_interface,
    _open_and_claim,
    _send_command,
    make_open_session_command,
)

PTP_GET_DEVICE_PROP_DESC = 0x1014
PTP_FOCUS_METERING_MODE = 0x501C
PTP_DESC_TRANSACTION_ID = 1
PTP_CLOSE_TRANSACTION_ID = 2
PTP_DTC_UINT16 = 0x0004
PTP_FORM_NONE = 0
PTP_FORM_ENUM = 1
MAX_SUPPORTED_VALUES = 256
MAX_DESCRIPTOR_SIZE = 4096


def make_get_focus_mode_desc_command() -> bytes:
    """Build the one read-only property request; the code is fixed here."""
    return struct.pack(
        "<IHHII", 16, PTP_CONTAINER_COMMAND, PTP_GET_DEVICE_PROP_DESC,
        PTP_DESC_TRANSACTION_ID, PTP_FOCUS_METERING_MODE,
    )


def make_close_session_command() -> bytes:
    return struct.pack("<IHHI", 12, PTP_CONTAINER_COMMAND,
                       PTP_CLOSE_SESSION, PTP_CLOSE_TRANSACTION_ID)


def parse_focus_mode_descriptor(data: bytes) -> dict[str, object]:
    """Parse the expected UINT16 enum descriptor without retaining raw data."""
    if len(data) > MAX_DESCRIPTOR_SIZE or len(data) < 10:
        raise PTPError("invalid FocusMeteringMode descriptor size")
    property_code, data_type = struct.unpack_from("<HH", data, 0)
    if property_code != PTP_FOCUS_METERING_MODE:
        raise PTPError("camera returned a different property descriptor")
    if data_type != PTP_DTC_UINT16:
        raise PTPError("FocusMeteringMode descriptor is not UINT16")
    get_set = data[4]
    if get_set not in (0, 1):
        raise PTPError("invalid PTP GetSet field")
    default_value, current_value = struct.unpack_from("<HH", data, 5)
    form_flag = data[9]
    offset = 10
    supported_values: tuple[int, ...] = ()
    if form_flag == PTP_FORM_ENUM:
        if offset + 2 > len(data):
            raise PTPError("truncated FocusMeteringMode enumeration")
        count = struct.unpack_from("<H", data, offset)[0]
        offset += 2
        if count > MAX_SUPPORTED_VALUES or offset + count * 2 > len(data):
            raise PTPError("invalid FocusMeteringMode enumeration")
        supported_values = struct.unpack_from(f"<{count}H", data, offset) if count else ()
        offset += count * 2
    elif form_flag != PTP_FORM_NONE:
        raise PTPError("unsupported FocusMeteringMode descriptor form")
    if offset != len(data):
        raise PTPError("unexpected trailing FocusMeteringMode descriptor data")
    return {
        "property": "FocusMeteringMode",
        "property_code": f"0x{property_code:04x}",
        "data_type": "UINT16",
        "get_set": "get/set" if get_set else "get-only",
        "factory_default": f"0x{default_value:04x}",
        "current_value": f"0x{current_value:04x}",
        "supported_values": [f"0x{value:04x}" for value in supported_values],
    }


def _get_descriptor(lib, handle, endpoint_out: int, endpoint_in: int) -> bytes:
    command = make_get_focus_mode_desc_command()
    sent = _bulk_transfer(lib, handle, endpoint_out, command, 0, 5000)
    if sent != len(command):
        raise PTPError("short GetDevicePropDesc command transfer")
    reader = _ContainerReader(
        lib, handle, endpoint_in, MAX_DESCRIPTOR_SIZE + 12
    )
    first = reader.read()
    kind, code, transaction, payload = decode_container(first)
    if transaction != PTP_DESC_TRANSACTION_ID:
        raise PTPError("wrong transaction ID in GetDevicePropDesc response")
    if kind == PTP_CONTAINER_RESPONSE:
        if payload:
            raise PTPError("unexpected GetDevicePropDesc error parameters")
        raise PTPError(f"GetDevicePropDesc failed (response 0x{code:04x})")
    if (kind, code) != (PTP_CONTAINER_DATA, PTP_GET_DEVICE_PROP_DESC):
        raise PTPError("unexpected data container for GetDevicePropDesc")
    if len(payload) > MAX_DESCRIPTOR_SIZE:
        raise PTPError("FocusMeteringMode descriptor exceeds the read bound")
    response = reader.read()
    response_kind, response_code, response_transaction, response_payload = (
        decode_container(response)
    )
    if (response_kind, response_code, response_transaction) != (
            PTP_CONTAINER_RESPONSE, PTP_RESPONSE_OK, PTP_DESC_TRANSACTION_ID):
        raise PTPError(
            "GetDevicePropDesc response mismatch "
            f"(container=0x{response_kind:04x}, code=0x{response_code:04x}, "
            f"transaction={response_transaction})"
        )
    if response_payload:
        raise PTPError("unexpected GetDevicePropDesc response parameters")
    return payload


def read_focus_mode_descriptor() -> dict[str, object]:
    """Read one standard property descriptor in one PTP session."""
    usb = _LibUSB()
    lib = usb.lib
    context = ctypes.c_void_p()
    if lib.libusb_init(ctypes.byref(context)) != 0:
        raise PTPError("libusb initialization failed; no camera operation sent")
    devices = ctypes.POINTER(ctypes.c_void_p)()
    handle = ctypes.c_void_p()
    config = ctypes.POINTER(_ConfigDescriptor)()
    claimed_interface = None
    session_open = False
    try:
        count = lib.libusb_get_device_list(context, ctypes.byref(devices))
        if count < 0:
            raise PTPError("USB enumeration failed; no camera operation sent")
        matches = []
        for index in range(count):
            device = devices[index]
            descriptor = _DeviceDescriptor()
            if lib.libusb_get_device_descriptor(device, ctypes.byref(descriptor)) == 0 and (
                    descriptor.vendor_id, descriptor.product_id) == (
                        Z30_VENDOR_ID, Z30_PRODUCT_ID):
                matches.append(device)
        if len(matches) != 1:
            raise PTPError(f"expected one Z 30 USB device, found {len(matches)}")
        device = matches[0]
        if lib.libusb_get_active_config_descriptor(device, ctypes.byref(config)) != 0:
            raise PTPError("could not inspect active USB descriptors; no operation sent")
        interface, bulk_in, bulk_out, _event_in, _packet_size = (
            _find_ptp_interface(config.contents)
        )
        handle = _open_and_claim(lib, device, interface)
        claimed_interface = interface
        _send_command(lib, handle, bulk_out, bulk_in,
                      make_open_session_command(), PTP_OPEN_SESSION, 0)
        session_open = True
        descriptor_data = _get_descriptor(lib, handle, bulk_out, bulk_in)
        return parse_focus_mode_descriptor(descriptor_data)
    finally:
        if session_open and handle:
            try:
                _send_command(lib, handle, bulk_out, bulk_in,
                              make_close_session_command(), PTP_CLOSE_SESSION,
                              PTP_CLOSE_TRANSACTION_ID)
            except PTPError:
                pass
        if handle:
            if claimed_interface is not None:
                lib.libusb_release_interface(handle, claimed_interface)
            lib.libusb_close(handle)
        if config:
            lib.libusb_free_config_descriptor(config)
        if devices:
            lib.libusb_free_device_list(devices, 1)
        lib.libusb_exit(context)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--read-focus-mode-descriptor", action="store_true")
    args = parser.parse_args()
    if not args.read_focus_mode_descriptor:
        parser.error("explicitly pass --read-focus-mode-descriptor")
    try:
        result = read_focus_mode_descriptor()
    except PTPError as exc:
        parser.exit(2, f"PTP property probe stopped: {exc}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
