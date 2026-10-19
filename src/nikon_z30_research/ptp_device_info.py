"""Read one standard PTP GetDeviceInfo response over USB.

This module deliberately implements no PTP session setup, vendor operation,
property access, object transfer, or state-changing operation. It is an
identity and capability-inventory probe, not a live-memory reader.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import struct
from dataclasses import asdict, dataclass

PTP_GET_DEVICE_INFO = 0x1001
PTP_CONTAINER_COMMAND = 1
PTP_CONTAINER_DATA = 2
PTP_CONTAINER_RESPONSE = 3
PTP_RESPONSE_OK = 0x2001
Z30_VENDOR_ID = 0x04B0
Z30_PRODUCT_ID = 0x0452
MAX_CONTAINER_SIZE = 1 << 20


class PTPError(RuntimeError):
    """A malformed PTP response or a transport error."""


@dataclass(frozen=True)
class DeviceInfo:
    standard_version: int
    vendor_extension_id: int
    vendor_extension_version: int
    vendor_extension_description: str
    functional_mode: int
    operations_supported: tuple[int, ...]
    manufacturer: str
    model: str
    device_version: str


def _u16(data: bytes, offset: int) -> tuple[int, int]:
    if offset + 2 > len(data):
        raise PTPError("truncated PTP DeviceInfo dataset")
    return struct.unpack_from("<H", data, offset)[0], offset + 2


def _u32(data: bytes, offset: int) -> tuple[int, int]:
    if offset + 4 > len(data):
        raise PTPError("truncated PTP DeviceInfo dataset")
    return struct.unpack_from("<I", data, offset)[0], offset + 4


def _ptp_string(data: bytes, offset: int) -> tuple[str, int]:
    if offset >= len(data):
        raise PTPError("truncated PTP string length")
    count = data[offset]
    end = offset + 1 + count * 2
    if end > len(data):
        raise PTPError("truncated PTP UTF-16 string")
    raw = data[offset + 1 : end]
    try:
        value = raw.decode("utf-16-le")
    except UnicodeDecodeError as exc:
        raise PTPError("invalid PTP UTF-16 string") from exc
    return value.rstrip("\x00"), end


def _u16_array(data: bytes, offset: int) -> tuple[tuple[int, ...], int]:
    count, offset = _u32(data, offset)
    if count > 4096 or offset + count * 2 > len(data):
        raise PTPError("invalid PTP DeviceInfo operation array")
    values = struct.unpack_from(f"<{count}H", data, offset) if count else ()
    return tuple(values), offset + count * 2


def parse_device_info(data: bytes) -> DeviceInfo:
    """Parse identity and advertised operation codes; never return the serial."""
    offset = 0
    standard_version, offset = _u16(data, offset)
    vendor_extension_id, offset = _u32(data, offset)
    vendor_extension_version, offset = _u16(data, offset)
    vendor_extension_description, offset = _ptp_string(data, offset)
    functional_mode, offset = _u16(data, offset)
    operations, offset = _u16_array(data, offset)
    # The intervening event, property, capture-format and image-format arrays
    # are parsed for bounds but intentionally not returned.
    for _ in range(4):
        _, offset = _u16_array(data, offset)
    manufacturer, offset = _ptp_string(data, offset)
    model, offset = _ptp_string(data, offset)
    device_version, offset = _ptp_string(data, offset)
    _serial_number, _ = _ptp_string(data, offset)
    return DeviceInfo(
        standard_version=standard_version,
        vendor_extension_id=vendor_extension_id,
        vendor_extension_version=vendor_extension_version,
        vendor_extension_description=vendor_extension_description,
        functional_mode=functional_mode,
        operations_supported=operations,
        manufacturer=manufacturer,
        model=model,
        device_version=device_version,
    )


def make_get_device_info_command() -> bytes:
    """Return the sole PTP request: GetDeviceInfo, transaction ID zero."""
    return struct.pack("<IHHI", 12, PTP_CONTAINER_COMMAND,
                       PTP_GET_DEVICE_INFO, 0)


def decode_container(packet: bytes) -> tuple[int, int, int, bytes]:
    if len(packet) < 12:
        raise PTPError("short PTP container")
    length, kind, code, transaction = struct.unpack_from("<IHHI", packet)
    if length != len(packet) or length > MAX_CONTAINER_SIZE:
        raise PTPError("invalid PTP container length")
    return kind, code, transaction, packet[12:]


class _DeviceDescriptor(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_uint8), ("descriptor_type", ctypes.c_uint8),
        ("usb_version", ctypes.c_uint16), ("device_class", ctypes.c_uint8),
        ("device_subclass", ctypes.c_uint8), ("device_protocol", ctypes.c_uint8),
        ("max_packet_size", ctypes.c_uint8), ("vendor_id", ctypes.c_uint16),
        ("product_id", ctypes.c_uint16), ("device_version", ctypes.c_uint16),
        ("manufacturer_index", ctypes.c_uint8), ("product_index", ctypes.c_uint8),
        ("serial_index", ctypes.c_uint8), ("configuration_count", ctypes.c_uint8),
    ]


class _EndpointDescriptor(ctypes.Structure):
    pass


_EndpointDescriptor._fields_ = [
    ("length", ctypes.c_uint8), ("descriptor_type", ctypes.c_uint8),
    ("address", ctypes.c_uint8), ("attributes", ctypes.c_uint8),
    ("max_packet_size", ctypes.c_uint16), ("interval", ctypes.c_uint8),
    ("refresh", ctypes.c_uint8), ("synch_address", ctypes.c_uint8),
    ("extra", ctypes.POINTER(ctypes.c_uint8)), ("extra_length", ctypes.c_int),
]


class _InterfaceDescriptor(ctypes.Structure):
    pass


_InterfaceDescriptor._fields_ = [
    ("length", ctypes.c_uint8), ("descriptor_type", ctypes.c_uint8),
    ("interface_number", ctypes.c_uint8), ("alternate_setting", ctypes.c_uint8),
    ("endpoint_count", ctypes.c_uint8), ("interface_class", ctypes.c_uint8),
    ("interface_subclass", ctypes.c_uint8), ("interface_protocol", ctypes.c_uint8),
    ("interface_index", ctypes.c_uint8),
    ("endpoints", ctypes.POINTER(_EndpointDescriptor)),
    ("extra", ctypes.POINTER(ctypes.c_uint8)), ("extra_length", ctypes.c_int),
]


class _Interface(ctypes.Structure):
    _fields_ = [("altsettings", ctypes.POINTER(_InterfaceDescriptor)),
                ("alternate_count", ctypes.c_int)]


class _ConfigDescriptor(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_uint8), ("descriptor_type", ctypes.c_uint8),
        ("total_length", ctypes.c_uint16), ("interface_count", ctypes.c_uint8),
        ("configuration_value", ctypes.c_uint8), ("configuration_index", ctypes.c_uint8),
        ("attributes", ctypes.c_uint8), ("max_power", ctypes.c_uint8),
        ("interfaces", ctypes.POINTER(_Interface)),
        ("extra", ctypes.POINTER(ctypes.c_uint8)), ("extra_length", ctypes.c_int),
    ]


class _LibUSB:
    def __init__(self) -> None:
        path = ctypes.util.find_library("usb-1.0")
        if not path:
            raise PTPError("libusb-1.0 was not found; no camera was contacted")
        self.lib = ctypes.CDLL(path)
        self._declare_functions()

    def _declare_functions(self) -> None:
        lib = self.lib
        lib.libusb_init.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        lib.libusb_init.restype = ctypes.c_int
        lib.libusb_get_device_list.argtypes = [ctypes.c_void_p,
                                               ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))]
        lib.libusb_get_device_list.restype = ctypes.c_ssize_t
        lib.libusb_free_device_list.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_int]
        lib.libusb_get_device_descriptor.argtypes = [ctypes.c_void_p,
                                                      ctypes.POINTER(_DeviceDescriptor)]
        lib.libusb_get_device_descriptor.restype = ctypes.c_int
        lib.libusb_get_active_config_descriptor.argtypes = [
            ctypes.c_void_p, ctypes.POINTER(ctypes.POINTER(_ConfigDescriptor))
        ]
        lib.libusb_get_active_config_descriptor.restype = ctypes.c_int
        lib.libusb_free_config_descriptor.argtypes = [ctypes.POINTER(_ConfigDescriptor)]
        lib.libusb_open.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]
        lib.libusb_open.restype = ctypes.c_int
        lib.libusb_close.argtypes = [ctypes.c_void_p]
        lib.libusb_claim_interface.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.libusb_claim_interface.restype = ctypes.c_int
        lib.libusb_release_interface.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.libusb_release_interface.restype = ctypes.c_int
        lib.libusb_bulk_transfer.argtypes = [ctypes.c_void_p, ctypes.c_ubyte,
                                             ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int,
                                             ctypes.POINTER(ctypes.c_int), ctypes.c_uint]
        lib.libusb_bulk_transfer.restype = ctypes.c_int
        lib.libusb_exit.argtypes = [ctypes.c_void_p]


def _bulk_transfer(lib, handle, endpoint: int, payload: bytes | None,
                   capacity: int, timeout_ms: int) -> bytes | int:
    if payload is None:
        buffer = (ctypes.c_ubyte * capacity)()
        length = capacity
    else:
        buffer = (ctypes.c_ubyte * len(payload)).from_buffer_copy(payload)
        length = len(payload)
    transferred = ctypes.c_int()
    result = lib.libusb_bulk_transfer(handle, endpoint, buffer, length,
                                      ctypes.byref(transferred), timeout_ms)
    if result != 0:
        raise PTPError(f"libusb bulk transfer failed ({result})")
    if payload is not None:
        return transferred.value
    return bytes(buffer[:transferred.value])


class _ContainerReader:
    def __init__(self, lib, handle, endpoint: int,
                 max_container_size: int = MAX_CONTAINER_SIZE) -> None:
        self.lib = lib
        self.handle = handle
        self.endpoint = endpoint
        self.max_container_size = max_container_size
        self.pending = bytearray()

    def read(self) -> bytes:
        while len(self.pending) < 12:
            chunk = _bulk_transfer(self.lib, self.handle, self.endpoint,
                                   None, 65536, 5000)
            if not chunk:
                raise PTPError("empty PTP bulk transfer")
            self.pending.extend(chunk)
        expected = struct.unpack_from("<I", self.pending)[0]
        if expected < 12 or expected > self.max_container_size:
            raise PTPError("invalid PTP container size")
        while len(self.pending) < expected:
            chunk = _bulk_transfer(self.lib, self.handle, self.endpoint,
                                   None, 65536, 5000)
            if not chunk:
                raise PTPError("empty PTP bulk transfer")
            self.pending.extend(chunk)
        packet = bytes(self.pending[:expected])
        del self.pending[:expected]
        return packet


def read_z30_device_info() -> DeviceInfo:
    """Send only PTP GetDeviceInfo to a matching Nikon Z 30 on USB."""
    usb = _LibUSB()
    lib = usb.lib
    context = ctypes.c_void_p()
    if lib.libusb_init(ctypes.byref(context)) != 0:
        raise PTPError("libusb initialization failed; no camera operation sent")
    devices = ctypes.POINTER(ctypes.c_void_p)()
    handle = ctypes.c_void_p()
    claimed_interface = None
    config = ctypes.POINTER(_ConfigDescriptor)()
    try:
        count = lib.libusb_get_device_list(context, ctypes.byref(devices))
        if count < 0:
            raise PTPError("USB enumeration failed; no camera operation sent")
        matches = []
        for index in range(count):
            device = devices[index]
            descriptor = _DeviceDescriptor()
            if lib.libusb_get_device_descriptor(device, ctypes.byref(descriptor)) == 0 and (
                descriptor.vendor_id, descriptor.product_id
            ) == (Z30_VENDOR_ID, Z30_PRODUCT_ID):
                matches.append((device, descriptor))
        if len(matches) != 1:
            raise PTPError(f"expected one Z 30 USB device, found {len(matches)}")
        device, _ = matches[0]
        if lib.libusb_get_active_config_descriptor(device, ctypes.byref(config)) != 0:
            raise PTPError("could not inspect USB descriptors; no operation sent")
        bulk_in = bulk_out = interface_number = None
        config_value = config.contents
        for i in range(config_value.interface_count):
            interface = config_value.interfaces[i]
            for j in range(interface.alternate_count):
                alt = interface.altsettings[j]
                if (alt.alternate_setting != 0 or alt.interface_class != 6 or
                        alt.interface_subclass != 1 or alt.interface_protocol != 1):
                    continue
                ins = [alt.endpoints[k].address for k in range(alt.endpoint_count)
                       if alt.endpoints[k].attributes & 0x03 == 2 and
                       alt.endpoints[k].address & 0x80]
                outs = [alt.endpoints[k].address for k in range(alt.endpoint_count)
                        if alt.endpoints[k].attributes & 0x03 == 2 and
                        not alt.endpoints[k].address & 0x80]
                if len(ins) == len(outs) == 1:
                    bulk_in, bulk_out = ins[0], outs[0]
                    interface_number = alt.interface_number
                    break
            if interface_number is not None:
                break
        if interface_number is None:
            raise PTPError("no default USB PTP bulk interface found; no operation sent")
        if lib.libusb_open(device, ctypes.byref(handle)) != 0:
            raise PTPError("could not open USB device; no operation sent")
        if lib.libusb_claim_interface(handle, interface_number) != 0:
            raise PTPError("could not claim PTP interface; no detach or reset was attempted")
        claimed_interface = interface_number

        # PTP permits transaction ID zero for GetDeviceInfo before a session.
        # No OpenSession or other PTP command is issued.
        command = make_get_device_info_command()
        sent = _bulk_transfer(lib, handle, bulk_out, command, 0, 5000)
        if sent != len(command):
            raise PTPError("short write of the PTP GetDeviceInfo command")
        reader = _ContainerReader(lib, handle, bulk_in)
        data_packet = reader.read()
        kind, code, transaction, payload = decode_container(data_packet)
        if (kind, code, transaction) != (PTP_CONTAINER_DATA, PTP_GET_DEVICE_INFO, 0):
            raise PTPError("unexpected PTP DeviceInfo data container")
        response_packet = reader.read()
        kind, response, transaction, _ = decode_container(response_packet)
        if (kind, response, transaction) != (PTP_CONTAINER_RESPONSE, PTP_RESPONSE_OK, 0):
            raise PTPError(f"GetDeviceInfo failed with response 0x{response:04x}")
        return parse_device_info(payload)
    finally:
        if config:
            lib.libusb_free_config_descriptor(config)
        if handle:
            if claimed_interface is not None:
                lib.libusb_release_interface(handle, claimed_interface)
            lib.libusb_close(handle)
        if devices:
            lib.libusb_free_device_list(devices, 1)
        lib.libusb_exit(context)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--read-device-info", action="store_true",
                        help="send the single standard PTP GetDeviceInfo operation")
    args = parser.parse_args()
    if not args.read_device_info:
        parser.error("explicitly pass --read-device-info to query a connected camera")
    try:
        info = read_z30_device_info()
    except PTPError as exc:
        parser.exit(2, f"PTP identity probe stopped: {exc}\n")
    result = asdict(info)
    result["operations_supported"] = [f"0x{code:04x}" for code in info.operations_supported]
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
