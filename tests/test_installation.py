"""Invented components/addresses only; no real firmware or target manifests."""

from dataclasses import replace
import hashlib
import unittest

from test_package_container import seal
from nikon_z30_research.installation import (
    AddressRange, InstallationModelError, InstallationPolicy, model_installation,
)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.component = seal(b'invented-data')
        self.policy = InstallationPolicy('synthetic-main', 0x1000, 32, 8,
                                          (AddressRange(0, 0x1000),))

    def test_exact_payload_crc_exclusion_and_padding_hash(self):
        report = model_installation(self.component, self.policy)
        expected = self.component[:-2] + bytes([255]) * (32 - len(self.component) + 2)
        self.assertEqual(report.expected_span_sha256, hashlib.sha256(expected).hexdigest())
        self.assertEqual(report.component_sha256, hashlib.sha256(self.component).hexdigest())
        self.assertEqual(report.payload_sha256, hashlib.sha256(self.component[:-2]).hexdigest())
        self.assertEqual(report.payload_size, 13)
        self.assertEqual(report.padding_size, 19)
        self.assertEqual(report.excluded_crc_bytes, 2)
        self.assertEqual(report.target_end, 0x1020)
        self.assertEqual(report.scope, 'static_installation_model')

    def test_chunk_order_and_bounds(self):
        report = model_installation(self.component, self.policy)
        erase = [report.chunk(i, phase='erase') for i in range(4)]
        program = [report.chunk(i, phase='program') for i in range(4)]
        self.assertEqual([r.start for r in erase], [0x1000, 0x1008, 0x1010, 0x1018])
        self.assertEqual([r.start for r in program], [0x1008, 0x1010, 0x1018, 0x1000])
        self.assertEqual(set(erase), set(program))
        self.assertTrue(all(0x1000 <= r.start < r.end <= 0x1020 for r in program))

    def test_single_chunk_and_no_padding(self):
        report = model_installation(seal(b'abcdefgh'), replace(self.policy, capacity=8))
        self.assertEqual(report.padding_size, 0)
        self.assertEqual(report.chunk(0, phase='erase'), report.chunk(0, phase='program'))
        self.assertEqual(report.expected_span_sha256, hashlib.sha256(b'abcdefgh').hexdigest())

    def test_small_and_oversized_components_rejected(self):
        for data in (b'', bytes(2), seal(b'x' * 33)):
            with self.subTest(length=len(data)):
                with self.assertRaisesRegex(InstallationModelError, 'payload length'):
                    model_installation(data, self.policy)

    def test_crc_corruption_and_mutable_input_rejected(self):
        for data, message in ((self.component[:-1] + bytes([self.component[-1] ^ 1]), 'CRC'),
                              (bytearray(self.component), 'immutable')):
            with self.assertRaisesRegex(InstallationModelError, message):
                model_installation(data, self.policy)

    def test_bad_bounds_alignment_and_policy_types(self):
        policies = [None, replace(self.policy, target_start=-1),
                    replace(self.policy, target_start=True), replace(self.policy, capacity=False),
                    replace(self.policy, capacity=0), replace(self.policy, capacity=31),
                    replace(self.policy, chunk_size=0), replace(self.policy, chunk_size=6),
                    replace(self.policy, chunk_size=2), replace(self.policy, target_start=0x1001),
                    replace(self.policy, target_start=(1 << 32) - 16),
                    replace(self.policy, component_name=''),
                    replace(self.policy, protected_ranges=[])]
        for policy in policies:
            with self.subTest(policy=policy):
                with self.assertRaises(InstallationModelError):
                    model_installation(self.component, policy)

    def test_protected_boundaries_and_full_span_overlap(self):
        # Overlap only in padding must still be rejected.
        for region in (AddressRange(0x1018, 0x1020), AddressRange(0x1000, 0x1001),
                       AddressRange(0xfff, 0x1030)):
            with self.assertRaisesRegex(InstallationModelError, 'overlaps protected'):
                model_installation(self.component, replace(self.policy, protected_ranges=(region,)))
        model_installation(self.component, replace(self.policy,
            protected_ranges=(AddressRange(0, 0x1000), AddressRange(0x1020, 0x2000))))

    def test_invalid_protected_ranges(self):
        for regions in ((AddressRange(1, 1),), (AddressRange(-1, 1),), (None,),
                        (AddressRange(10, 20), AddressRange(15, 25))):
            with self.assertRaises(InstallationModelError):
                model_installation(self.component, replace(self.policy, protected_ranges=regions))

    def test_chunk_access_rejected_outside_model(self):
        report = model_installation(self.component, self.policy)
        for step in (-1, 4, True, 1.5):
            with self.assertRaises(InstallationModelError):
                report.chunk(step, phase='erase')
        with self.assertRaises(InstallationModelError):
            report.chunk(0, phase='execute')

    def test_streamed_padding_crosses_hash_chunk_boundary(self):
        policy = replace(self.policy, capacity=2 * 1024 * 1024, chunk_size=8)
        report = model_installation(self.component, policy)
        expected = self.component[:-2] + bytes([255]) * (policy.capacity - 13)
        self.assertEqual(report.expected_span_sha256, hashlib.sha256(expected).hexdigest())


if __name__ == '__main__':
    unittest.main()
