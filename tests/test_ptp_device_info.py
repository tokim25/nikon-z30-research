import ctypes
import struct
import unittest

from nikon_z30_research.ptp_device_info import (
    DeviceInfo,
    PTPError,
    _ContainerReader,
    decode_container,
    make_get_device_info_command,
    parse_device_info,
)


def ptp_string(value):
    encoded = value.encode("utf-16-le") + b"\x00\x00"
    return bytes([len(encoded) // 2]) + encoded


def device_info_dataset(operations):
    return (
        struct.pack("<HIH", 100, 0x0000000A, 100)
        + ptp_string("Nikon extension")
        + struct.pack("<HI", 0, len(operations))
        + struct.pack(f"<{len(operations)}H", *operations)
        + struct.pack("<IIII", 0, 0, 0, 0)
        + ptp_string("Nikon Corporation")
        + ptp_string("Z 30")
        + ptp_string("1.20")
        + ptp_string("synthetic serial")
    )


class PTPDeviceInfoTests(unittest.TestCase):
    def test_command_is_the_single_read_only_get_device_info_request(self):
        self.assertEqual(
            make_get_device_info_command(),
            struct.pack("<IHHI", 12, 1, 0x1001, 0),
        )

    def test_device_info_extracts_identity_and_supported_operations_only(self):
        operations = (0x1001, 0x1002, 0x9201, 0x9203)
        info = parse_device_info(device_info_dataset(operations))
        self.assertEqual(
            info,
            DeviceInfo(100, 0x0A, 100, "Nikon extension", 0, operations,
                       "Nikon Corporation", "Z 30", "1.20"),
        )
        self.assertFalse(hasattr(info, "serial_number"))

    def test_truncated_string_is_rejected(self):
        data = struct.pack("<HIH", 100, 0x0A, 100) + b"\x02A"
        with self.assertRaises(PTPError):
            parse_device_info(data)

    def test_unreasonable_operation_count_is_rejected(self):
        data = (
            struct.pack("<HIH", 100, 0x0A, 100)
            + ptp_string("")
            + struct.pack("<HI", 0, 4097)
        )
        with self.assertRaises(PTPError):
            parse_device_info(data)

    def test_container_parser_checks_length_and_returns_payload(self):
        payload = b"synthetic"
        packet = struct.pack("<IHHI", 12 + len(payload), 2, 0x1001, 0) + payload
        self.assertEqual(decode_container(packet), (2, 0x1001, 0, payload))
        with self.assertRaises(PTPError):
            decode_container(packet[:-1])

    def test_container_reader_preserves_adjacent_containers(self):
        data = struct.pack("<IHHI", 13, 2, 0x1001, 0) + b"x"
        response = struct.pack("<IHHI", 12, 3, 0x2001, 0)
        stream = bytearray(data + response)

        class FakeUSB:
            def libusb_bulk_transfer(self, _handle, _endpoint, buffer, length,
                                     transferred, _timeout):
                chunk = stream[:length]
                del stream[:len(chunk)]
                ctypes.memmove(buffer, bytes(chunk), len(chunk))
                ctypes.cast(
                    transferred, ctypes.POINTER(ctypes.c_int)
                ).contents.value = len(chunk)
                return 0

        reader = _ContainerReader(FakeUSB(), None, 0x81)
        self.assertEqual(reader.read(), data)
        self.assertEqual(reader.read(), response)


if __name__ == "__main__":
    unittest.main()
