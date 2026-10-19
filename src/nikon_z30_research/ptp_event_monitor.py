"""Bounded PTP event-endpoint monitor for a Nikon Z 30.

This tool opens one standard PTP session, listens only on the USB interrupt-IN
event endpoint for a bounded interval, then closes that session. It does not
send vendor operations, set properties, capture images, or transfer objects.
The current 8-byte-endpoint and zero-length-poll handling completed two
bounded camera runs (F-266/F-267). The owner approved this bounded method;
before each 15-second window, warn the owner and wait for their explicit
start signal.
"""

from __future__ import annotations

import argparse
import ctypes
import json
import struct
import time

from .ptp_device_info import (
    PTPError,
    PTP_CONTAINER_COMMAND,
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

PTP_OPEN_SESSION = 0x1002
PTP_CLOSE_SESSION = 0x1003
PTP_CONTAINER_EVENT = 4
PTP_SESSION_ID = 1
PTP_INITIAL_TRANSACTION_ID = 0
PTP_CLOSE_TRANSACTION_ID = 1
LIBUSB_ERROR_TIMEOUT = -7
MAX_EVENT_PARAMETERS = 3
MAX_EVENT_PACKET = 12 + MAX_EVENT_PARAMETERS * 4


def make_open_session_command() -> bytes:
    return struct.pack("<IHHII", 16, PTP_CONTAINER_COMMAND,
                       PTP_OPEN_SESSION, PTP_INITIAL_TRANSACTION_ID,
                       PTP_SESSION_ID)


def make_close_session_command() -> bytes:
    return struct.pack("<IHHI", 12, PTP_CONTAINER_COMMAND,
                       PTP_CLOSE_SESSION, PTP_CLOSE_TRANSACTION_ID)


def parse_event_container(packet: bytes) -> dict[str, object]:
    kind, event_code, transaction_id, payload = decode_container(packet)
    if kind != PTP_CONTAINER_EVENT:
        raise PTPError("interrupt endpoint did not return a PTP event container")
    if len(payload) % 4 or len(payload) > MAX_EVENT_PARAMETERS * 4:
        raise PTPError("invalid PTP event parameter area")
    parameters = struct.unpack(f"<{len(payload) // 4}I", payload) if payload else ()
    return {
        "event_code": f"0x{event_code:04x}",
        "transaction_id": transaction_id,
        "parameters": [f"0x{value:08x}" for value in parameters],
    }


def _find_ptp_interface(config: _ConfigDescriptor) -> tuple[int, int, int, int, int]:
    """Return interface, bulk-IN, bulk-OUT and interrupt-IN endpoint details."""
    matches = []
    for i in range(config.interface_count):
        interface = config.interfaces[i]
        for j in range(interface.alternate_count):
            alt = interface.altsettings[j]
            if (alt.alternate_setting != 0 or alt.interface_class != 6 or
                    alt.interface_subclass != 1 or alt.interface_protocol != 1):
                continue
            bulk_in = [alt.endpoints[k].address for k in range(alt.endpoint_count)
                       if alt.endpoints[k].attributes & 0x03 == 2 and
                       alt.endpoints[k].address & 0x80]
            bulk_out = [alt.endpoints[k].address for k in range(alt.endpoint_count)
                        if alt.endpoints[k].attributes & 0x03 == 2 and
                        not alt.endpoints[k].address & 0x80]
            event_endpoints = [alt.endpoints[k] for k in range(alt.endpoint_count)
                               if alt.endpoints[k].attributes & 0x03 == 3 and
                               alt.endpoints[k].address & 0x80]
            event_in = [endpoint.address for endpoint in event_endpoints]
            if len(bulk_in) == len(bulk_out) == len(event_in) == 1:
                packet_size = event_endpoints[0].max_packet_size & 0x07ff
                if packet_size < 1:
                    continue
                matches.append((alt.interface_number, bulk_in[0], bulk_out[0],
                                event_in[0], packet_size))
    if len(matches) != 1:
        raise PTPError("expected one default PTP interface with one event-IN endpoint")
    interface, bulk_in, bulk_out, event_in, packet_size = matches[0]
    return interface, bulk_in, bulk_out, event_in, packet_size


def _open_and_claim(lib, device, interface_number: int) -> ctypes.c_void_p:
    handle = ctypes.c_void_p()
    if lib.libusb_open(device, ctypes.byref(handle)) != 0:
        raise PTPError("could not open the Z 30; no transfer was sent")
    if lib.libusb_claim_interface(handle, interface_number) != 0:
        lib.libusb_close(handle)
        raise PTPError("PTP interface is busy; no driver detach or reset was attempted")
    return handle


def _send_command(lib, handle, endpoint_out: int, response_reader: _ContainerReader,
                  command: bytes, operation: int, transaction: int) -> None:
    sent = _bulk_transfer(lib, handle, endpoint_out, command, 0, 5000)
    if sent != len(command):
        raise PTPError("short PTP command transfer")
    response = response_reader.read()
    kind, code, response_transaction, payload = decode_container(response)
    if (kind, code, response_transaction) != (
            PTP_CONTAINER_RESPONSE, PTP_RESPONSE_OK, transaction):
        raise PTPError(
            f"PTP session operation 0x{operation:04x} was not acknowledged "
            f"(kind=0x{kind:04x}, code=0x{code:04x}, "
            f"transaction={response_transaction})"
        )
    if payload:
        raise PTPError("unexpected PTP session response parameters")


def _interrupt_transfer(lib, handle, endpoint: int, packet_size: int,
                        timeout_ms: int) -> bytes | None:
    libusb = lib.lib
    libusb.libusb_interrupt_transfer.argtypes = [
        ctypes.c_void_p, ctypes.c_ubyte, ctypes.POINTER(ctypes.c_ubyte),
        ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_uint,
    ]
    libusb.libusb_interrupt_transfer.restype = ctypes.c_int
    # PTP event containers can be 12-24 bytes. The libusb transfer length is
    # a maximum; libusb abstracts packet boundaries and collects packets into
    # the transfer buffer.
    buffer = (ctypes.c_ubyte * MAX_EVENT_PACKET)()
    transferred = ctypes.c_int()
    result = libusb.libusb_interrupt_transfer(
        handle, endpoint, buffer, len(buffer), ctypes.byref(transferred), timeout_ms
    )
    if result == LIBUSB_ERROR_TIMEOUT:
        return None
    if result != 0:
        raise PTPError(f"libusb interrupt-IN transfer failed ({result})")
    return bytes(buffer[:transferred.value])


def _decode_event_poll(packet: bytes | None) -> dict[str, object] | None:
    """Return no event for timeout/zero-length USB transfers."""
    if packet is None or packet == b"":
        return None
    return parse_event_container(packet)


def monitor_z30_events(duration_seconds: float = 15.0) -> dict[str, object]:
    """Open a standard PTP session and report event codes/parameters only."""
    if not 1.0 <= duration_seconds <= 30.0:
        raise PTPError("monitor duration must be between 1 and 30 seconds")
    usb = _LibUSB()
    lib = usb.lib
    lib.libusb_interrupt_transfer.argtypes = [
        ctypes.c_void_p, ctypes.c_ubyte, ctypes.POINTER(ctypes.c_ubyte),
        ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_uint,
    ]
    lib.libusb_interrupt_transfer.restype = ctypes.c_int
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
        interface_number, bulk_in, bulk_out, event_in, packet_size = (
            _find_ptp_interface(config.contents)
        )
        handle = _open_and_claim(lib, device, interface_number)
        claimed_interface = interface_number
        response_reader = _ContainerReader(lib, handle, bulk_in)

        # The only PTP commands are standard OpenSession and CloseSession.
        _send_command(lib, handle, bulk_out, response_reader,
                      make_open_session_command(), PTP_OPEN_SESSION,
                      PTP_INITIAL_TRANSACTION_ID)
        session_open = True
        events = []
        started = time.monotonic()
        deadline = started + duration_seconds
        while time.monotonic() < deadline:
            remaining_ms = max(1, int((deadline - time.monotonic()) * 1000))
            packet = _interrupt_transfer(
                usb, handle, event_in, packet_size, min(250, remaining_ms)
            )
            event = _decode_event_poll(packet)
            if event is None:
                continue
            if len(packet) > MAX_EVENT_PACKET:
                raise PTPError("oversized PTP interrupt-IN packet")
            event["elapsed_seconds"] = round(time.monotonic() - started, 3)
            events.append(event)
            if len(events) >= 128:
                break
        return {"session_opened": True, "events": events,
                "event_limit_reached": len(events) >= 128}
    finally:
        if session_open and handle:
            try:
                _send_command(lib, handle, bulk_out, response_reader,
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
    parser.add_argument("--listen-events", action="store_true",
                        help="open one PTP session and listen on event-IN")
    parser.add_argument("--seconds", type=float, default=15.0)
    args = parser.parse_args()
    if not args.listen_events:
        parser.error("explicitly pass --listen-events to monitor the event endpoint")
    try:
        result = monitor_z30_events(args.seconds)
    except PTPError as exc:
        parser.exit(2, f"PTP event monitor stopped: {exc}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
