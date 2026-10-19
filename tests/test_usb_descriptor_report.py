import unittest
from types import SimpleNamespace

from nikon_z30_research.usb_descriptor_report import summarize_interface


class USBDescriptorReportTests(unittest.TestCase):
    def test_summary_contains_only_interface_and_endpoint_metadata(self):
        endpoints = [
            SimpleNamespace(address=0x81, attributes=2, max_packet_size=512,
                            interval=0),
            SimpleNamespace(address=0x02, attributes=2, max_packet_size=512,
                            interval=0),
            SimpleNamespace(address=0x83, attributes=3, max_packet_size=16,
                            interval=4),
        ]
        alt = SimpleNamespace(interface_number=1, alternate_setting=0,
                              interface_class=6, interface_subclass=1,
                              interface_protocol=1, endpoint_count=len(endpoints),
                              endpoints=endpoints)
        self.assertEqual(
            summarize_interface(alt),
            {
                "interface_number": 1, "alternate_setting": 0,
                "class": 6, "subclass": 1, "protocol": 1,
                "endpoints": [
                    {"address": "0x81", "direction": "in",
                     "transfer_type": "bulk", "max_packet_size": 512,
                     "interval": 0},
                    {"address": "0x02", "direction": "out",
                     "transfer_type": "bulk", "max_packet_size": 512,
                     "interval": 0},
                    {"address": "0x83", "direction": "in",
                     "transfer_type": "interrupt", "max_packet_size": 16,
                     "interval": 4},
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
