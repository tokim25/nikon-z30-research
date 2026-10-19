import struct
import unittest
from types import SimpleNamespace

from nikon_z30_research.ptp_device_info import PTPError
from nikon_z30_research.ptp_event_monitor import (
    PTP_CLOSE_SESSION,
    PTP_CONTAINER_COMMAND,
    PTP_OPEN_SESSION,
    PTP_SESSION_ID,
    _decode_event_poll,
    _find_ptp_interface,
    make_close_session_command,
    make_open_session_command,
    parse_event_container,
)


class PTPEventMonitorTests(unittest.TestCase):
    def test_open_session_is_one_standard_command(self):
        self.assertEqual(
            make_open_session_command(),
            struct.pack("<IHHII", 16, PTP_CONTAINER_COMMAND,
                        PTP_OPEN_SESSION, 0, PTP_SESSION_ID),
        )

    def test_close_session_is_one_standard_command(self):
        self.assertEqual(
            make_close_session_command(),
            struct.pack("<IHHI", 12, PTP_CONTAINER_COMMAND,
                        PTP_CLOSE_SESSION, 1),
        )

    def test_event_container_returns_only_code_transaction_and_numeric_params(self):
        packet = struct.pack("<IHHIII", 20, 4, 0x4002, 7, 0x1234, 0x5678)
        self.assertEqual(
            parse_event_container(packet),
            {"event_code": "0x4002", "transaction_id": 7,
             "parameters": ["0x00001234", "0x00005678"]},
        )

    def test_non_event_containers_are_rejected(self):
        packet = struct.pack("<IHHI", 12, 3, 0x2001, 0)
        with self.assertRaises(PTPError):
            parse_event_container(packet)

    def test_timeout_and_zero_length_transfers_are_idle_polls(self):
        self.assertIsNone(_decode_event_poll(None))
        self.assertIsNone(_decode_event_poll(b""))

    def test_nonempty_packet_is_still_parsed_as_event(self):
        packet = struct.pack("<IHHI", 12, 4, 0x4002, 7)
        self.assertEqual(_decode_event_poll(packet), {
            "event_code": "0x4002", "transaction_id": 7, "parameters": []
        })

    def test_malformed_event_parameter_area_is_rejected(self):
        misaligned = struct.pack("<IHHI", 13, 4, 0x4002, 0) + b"x"
        oversized = struct.pack("<IHHIIIII", 28, 4, 0x4002, 0, 1, 2, 3, 4)
        for packet in (misaligned, oversized):
            with self.subTest(packet_length=len(packet)):
                with self.assertRaises(PTPError):
                    parse_event_container(packet)

    def test_eight_byte_interrupt_endpoint_is_accepted(self):
        endpoints = [
            SimpleNamespace(address=0x81, attributes=2, max_packet_size=512),
            SimpleNamespace(address=0x02, attributes=2, max_packet_size=512),
            SimpleNamespace(address=0x83, attributes=3, max_packet_size=8),
        ]
        alt = SimpleNamespace(
            alternate_setting=0, interface_class=6, interface_subclass=1,
            interface_protocol=1, endpoints=endpoints, endpoint_count=3,
            interface_number=0,
        )
        interface = SimpleNamespace(altsettings=[alt], alternate_count=1)
        config = SimpleNamespace(interfaces=[interface], interface_count=1)
        self.assertEqual(_find_ptp_interface(config), (0, 0x81, 0x02, 0x83, 8))

    def test_missing_interrupt_endpoint_is_rejected(self):
        endpoints = [
            SimpleNamespace(address=0x81, attributes=2, max_packet_size=512),
            SimpleNamespace(address=0x02, attributes=2, max_packet_size=512),
        ]
        alt = SimpleNamespace(
            alternate_setting=0, interface_class=6, interface_subclass=1,
            interface_protocol=1, endpoints=endpoints, endpoint_count=2,
            interface_number=0,
        )
        interface = SimpleNamespace(altsettings=[alt], alternate_count=1)
        config = SimpleNamespace(interfaces=[interface], interface_count=1)
        with self.assertRaises(PTPError):
            _find_ptp_interface(config)


if __name__ == "__main__":
    unittest.main()
