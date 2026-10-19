import struct
import unittest
from unittest.mock import patch

from nikon_z30_research.ptp_device_info import PTPError, _ContainerReader
from nikon_z30_research.ptp_focus_mode_probe import (
    PTP_CONTAINER_COMMAND,
    PTP_FOCUS_METERING_MODE,
    PTP_GET_DEVICE_PROP_DESC,
    PTP_CONTAINER_DATA,
    PTP_CONTAINER_RESPONSE,
    _get_descriptor,
    make_close_session_command,
    make_get_focus_mode_desc_command,
    parse_focus_mode_descriptor,
)


def focus_descriptor(current=0x8001, supported=(0x0001, 0x0002, 0x8001)):
    return (struct.pack("<HHBHHBH", PTP_FOCUS_METERING_MODE, 0x0004,
                        1, 0x0001, current, 1, len(supported)) +
            struct.pack(f"<{len(supported)}H", *supported))


class PTPFocusModeProbeTests(unittest.TestCase):
    def test_command_targets_only_standard_focus_mode_descriptor(self):
        self.assertEqual(
            make_get_focus_mode_desc_command(),
            struct.pack("<IHHII", 16, PTP_CONTAINER_COMMAND,
                        PTP_GET_DEVICE_PROP_DESC, 1,
                        PTP_FOCUS_METERING_MODE),
        )

    def test_close_session_uses_the_next_transaction_id(self):
        self.assertEqual(
            make_close_session_command(),
            struct.pack("<IHHI", 12, PTP_CONTAINER_COMMAND, 0x1003, 2),
        )

    def test_container_reader_enforces_property_response_bound(self):
        header = struct.pack("<IHHI", 20, 2, 0x1014, 1)
        with patch("nikon_z30_research.ptp_device_info._bulk_transfer",
                   return_value=header):
            reader = _ContainerReader(object(), object(), 0x81, 16)
            with self.assertRaises(PTPError):
                reader.read()

    def test_get_descriptor_reports_numeric_response_status_without_raw_data(self):
        data = struct.pack("<IHHI", 14, PTP_CONTAINER_DATA,
                            PTP_GET_DEVICE_PROP_DESC, 1) + b"xx"
        rejected = struct.pack("<IHHI", 12, PTP_CONTAINER_RESPONSE,
                               0x2005, 1)
        with patch("nikon_z30_research.ptp_focus_mode_probe._bulk_transfer",
                   return_value=16) as transfer, patch(
                       "nikon_z30_research.ptp_focus_mode_probe._ContainerReader"
                   ) as reader_type:
            reader_type.return_value.read.side_effect = [data, rejected]
            with self.assertRaisesRegex(PTPError, "code=0x2005"):
                _get_descriptor(object(), object(), 1, 0x81)
            self.assertEqual(transfer.call_count, 1)

    def test_descriptor_reports_numeric_current_and_supported_values(self):
        self.assertEqual(parse_focus_mode_descriptor(focus_descriptor()), {
            "property": "FocusMeteringMode",
            "property_code": "0x501c",
            "data_type": "UINT16",
            "get_set": "get/set",
            "factory_default": "0x0001",
            "current_value": "0x8001",
            "supported_values": ["0x0001", "0x0002", "0x8001"],
        })

    def test_read_only_descriptor_with_no_form_is_supported(self):
        data = struct.pack("<HHBHHB", PTP_FOCUS_METERING_MODE, 0x0004,
                           0, 0x0001, 0x0002, 0)
        result = parse_focus_mode_descriptor(data)
        self.assertEqual(result["get_set"], "get-only")
        self.assertEqual(result["current_value"], "0x0002")
        self.assertEqual(result["supported_values"], [])

    def test_wrong_property_or_type_is_rejected(self):
        wrong_property = struct.pack("<HHBHHB", 0x501B, 0x0004,
                                     1, 1, 2, 0)
        wrong_type = struct.pack("<HHBHHB", PTP_FOCUS_METERING_MODE, 0x0006,
                                 1, 1, 2, 0)
        for data in (wrong_property, wrong_type):
            with self.subTest(data=data):
                with self.assertRaises(PTPError):
                    parse_focus_mode_descriptor(data)

    def test_truncated_oversized_and_unexpected_descriptor_forms_are_rejected(self):
        truncated = struct.pack("<HHBHHB", PTP_FOCUS_METERING_MODE, 0x0004,
                                1, 1, 2, 1) + b"\x02"
        too_many = struct.pack("<HHBHHBH", PTP_FOCUS_METERING_MODE, 0x0004,
                               1, 1, 2, 1, 257)
        unsupported_form = struct.pack("<HHBHHB", PTP_FOCUS_METERING_MODE,
                                       0x0004, 1, 1, 2, 2)
        trailing = struct.pack("<HHBHHB", PTP_FOCUS_METERING_MODE, 0x0004,
                               1, 1, 2, 0) + b"\x00"
        for data in (truncated, too_many, unsupported_form, trailing, b"\x00" * 9):
            with self.subTest(data_length=len(data)):
                with self.assertRaises(PTPError):
                    parse_focus_mode_descriptor(data)


if __name__ == "__main__":
    unittest.main()
