"""Report only active USB interface and endpoint descriptors for a Z 30."""

from __future__ import annotations

import argparse
import ctypes
import json

from .ptp_device_info import (
    PTPError,
    Z30_PRODUCT_ID,
    Z30_VENDOR_ID,
    _ConfigDescriptor,
    _DeviceDescriptor,
    _LibUSB,
)


TRANSFER_TYPES = {0: "control", 1: "isochronous", 2: "bulk", 3: "interrupt"}


def summarize_interface(alt) -> dict[str, object]:
    endpoints = []
    for index in range(alt.endpoint_count):
        endpoint = alt.endpoints[index]
        endpoints.append({
            "address": f"0x{endpoint.address:02x}",
            "direction": "in" if endpoint.address & 0x80 else "out",
            "transfer_type": TRANSFER_TYPES[endpoint.attributes & 0x03],
            "max_packet_size": endpoint.max_packet_size & 0x07ff,
            "interval": endpoint.interval,
        })
    return {
        "interface_number": alt.interface_number,
        "alternate_setting": alt.alternate_setting,
        "class": alt.interface_class,
        "subclass": alt.interface_subclass,
        "protocol": alt.interface_protocol,
        "endpoints": endpoints,
    }


def inspect_z30_usb_descriptors() -> dict[str, object]:
    """Read active descriptors only; never open or claim the camera."""
    usb = _LibUSB()
    lib = usb.lib
    context = ctypes.c_void_p()
    if lib.libusb_init(ctypes.byref(context)) != 0:
        raise PTPError("libusb initialization failed; no device was opened")
    devices = ctypes.POINTER(ctypes.c_void_p)()
    config = ctypes.POINTER(_ConfigDescriptor)()
    try:
        count = lib.libusb_get_device_list(context, ctypes.byref(devices))
        if count < 0:
            raise PTPError("USB enumeration failed; no device was opened")
        matches = []
        for index in range(count):
            device = devices[index]
            descriptor = _DeviceDescriptor()
            if lib.libusb_get_device_descriptor(device, ctypes.byref(descriptor)) == 0 and (
                descriptor.vendor_id, descriptor.product_id
            ) == (Z30_VENDOR_ID, Z30_PRODUCT_ID):
                matches.append(device)
        if len(matches) != 1:
            raise PTPError(f"expected one Z 30 USB device, found {len(matches)}")
        if lib.libusb_get_active_config_descriptor(matches[0], ctypes.byref(config)) != 0:
            raise PTPError("could not read active configuration descriptors")
        interfaces = []
        active = config.contents
        for interface_index in range(active.interface_count):
            interface = active.interfaces[interface_index]
            for alt_index in range(interface.alternate_count):
                interfaces.append(summarize_interface(interface.altsettings[alt_index]))
        return {"interfaces": interfaces}
    finally:
        if config:
            lib.libusb_free_config_descriptor(config)
        if devices:
            lib.libusb_free_device_list(devices, 1)
        lib.libusb_exit(context)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inspect-descriptors", action="store_true",
                        help="read and print active interface/endpoint descriptors")
    args = parser.parse_args()
    if not args.inspect_descriptors:
        parser.error("explicitly pass --inspect-descriptors")
    try:
        result = inspect_z30_usb_descriptors()
    except PTPError as exc:
        parser.exit(2, f"USB descriptor inspection stopped: {exc}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
