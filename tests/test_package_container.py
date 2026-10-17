"""Invented component names and payloads only; no firmware fixtures."""

import binascii
import hashlib
import struct
import unittest

from nikon_z30_research.package_container import (
    ComponentSpec, ContainerValidationError, validate_container,
)


def seal(payload):
    return payload + binascii.crc_hqx(payload, 0).to_bytes(2, 'big')


def fix_container_crc(data):
    data[-16:-14] = binascii.crc_hqx(data[:-16], 0).to_bytes(2, 'big')
    return bytes(data)


def fixture(payloads=(b'invented main payload', b'invented auxiliary payload')):
    components = [seal(payload) for payload in payloads]
    names = ('synthetic-main', 'synthetic-extra')
    end = 48 + 32 * len(components)
    directory = bytearray()
    specs = []
    cursor = end
    for name, component in zip(names, components):
        directory.extend(struct.pack('>16s4I', name.encode(), cursor, len(component), 0, 0))
        specs.append(ComponentSpec(name, len(component), hashlib.sha256(component).hexdigest()))
        cursor += len(component)
    body = b' ' * 32 + struct.pack('>4I', len(components), end, 0, 0) + directory + b''.join(components)
    return seal(body) + bytes(14), tuple(specs)


class ContainerTests(unittest.TestCase):
    def setUp(self):
        self.data, self.specs = fixture()

    def reject(self, data, message, specs=None):
        with self.assertRaisesRegex(ContainerValidationError, message):
            validate_container(data, self.specs if specs is None else specs)

    def test_valid_container_reports_hashes_without_mutation(self):
        before = self.data
        report = validate_container(self.data, self.specs)
        self.assertEqual(report.sha256, hashlib.sha256(before).hexdigest())
        self.assertEqual(report.size, len(before))
        self.assertEqual(tuple(c.sha256 for c in report.components),
                         tuple(s.unchanged_sha256 for s in self.specs))
        self.assertTrue(all(c.unchanged_checked for c in report.components))
        self.assertEqual(self.data, before)

    def test_every_truncation_and_appended_bytes_rejected(self):
        for length in range(len(self.data)):
            with self.subTest(length=length):
                self.reject(self.data[:length], 'length')
        self.reject(self.data + b'x', 'length')

    def test_header_prefix_and_trailer_rejected_even_with_valid_crc(self):
        for offset, message in ((0, 'prefix'), (35, 'header'), (39, 'header'),
                                (43, 'header'), (47, 'header'), (-1, 'trailer')):
            with self.subTest(offset=offset):
                data = bytearray(self.data)
                data[offset] ^= 1
                self.reject(fix_container_crc(data), message)

    def test_directory_bounds_reserved_and_wrong_sizes(self):
        for field, values, message in ((16, (0, 111, 113, 0xffffffff), 'layout'),
                                       (20, (0, 1, 0xffffffff), 'layout'),
                                       (24, (1,), 'reserved'), (28, (1,), 'reserved')):
            for value in values:
                with self.subTest(field=field, value=value):
                    data = bytearray(self.data)
                    struct.pack_into('>I', data, 48 + field, value)
                    self.reject(fix_container_crc(data), message)
        data = bytearray(self.data)
        struct.pack_into('>I', data, 80 + 16, 112)
        self.reject(fix_container_crc(data), 'layout')

    def test_names_order_duplicates_and_padding(self):
        for replacement in (b'unknown', b'synthetic-extra', b'synthetic-main\0x', b'\xff'):
            data = bytearray(self.data)
            data[48:64] = replacement.ljust(16, b'\0')
            self.reject(fix_container_crc(data), 'name/order')

    def test_component_corruption_detected_after_container_crc_repair(self):
        data = bytearray(self.data)
        data[112] ^= 1
        self.reject(fix_container_crc(data), 'component 0 CRC')

    def test_component_crc_bytes_corruption(self):
        data = bytearray(self.data)
        data[112 + self.specs[0].size - 1] ^= 1
        self.reject(fix_container_crc(data), 'component 0 CRC')

    def test_outer_crc_corruption(self):
        data = bytearray(self.data)
        data[-16] ^= 1
        self.reject(bytes(data), 'container CRC')

    def test_valid_crcs_cannot_hide_change_to_pinned_component(self):
        changed, _ = fixture((b'Invented main payload', b'invented auxiliary payload'))
        self.reject(changed, 'unchanged digest')
        unpinned = (ComponentSpec(self.specs[0].name, self.specs[0].size), self.specs[1])
        report = validate_container(changed, unpinned)
        self.assertFalse(report.components[0].unchanged_checked)
        self.assertTrue(report.components[1].unchanged_checked)

    def test_second_component_is_also_pinned(self):
        changed, _ = fixture((b'invented main payload', b'Invented auxiliary payload'))
        self.reject(changed, 'component 1 unchanged digest')

    def test_swapped_directory_entries_rejected(self):
        data = bytearray(self.data)
        data[48:80], data[80:112] = data[80:112], data[48:80]
        self.reject(fix_container_crc(data), 'name/order')

    def test_wrong_expected_size_and_name_are_rejected(self):
        self.reject(self.data, 'length',
                    (ComponentSpec(self.specs[0].name, self.specs[0].size + 1), self.specs[1]))
        self.reject(self.data, 'name/order',
                    (ComponentSpec('different-name', self.specs[0].size), self.specs[1]))

    def test_invalid_policy_and_mutable_input(self):
        self.reject(bytearray(self.data), 'immutable')
        policies = ((), list(self.specs), (None,),
                    (ComponentSpec('', 2),), (ComponentSpec('a\0b', 2),),
                    (ComponentSpec('nonascii\u2603', 2),), (ComponentSpec('x' * 17, 2),),
                    (ComponentSpec('a', True),), (ComponentSpec('a', -1),),
                    (ComponentSpec('a', 0x100000000),),
                    (ComponentSpec('a', 2, 'invalid'),),
                    (ComponentSpec('a', 2), ComponentSpec('a', 2)))
        for policy in policies:
            with self.subTest(policy=policy):
                self.reject(self.data, 'expected|specification|ASCII|invalid|duplicate', policy)

    def test_errors_do_not_echo_payload_or_candidate_name(self):
        data = bytearray(self.data)
        data[48:64] = b'secret-candidate'
        try:
            validate_container(fix_container_crc(data), self.specs)
        except ContainerValidationError as error:
            self.assertNotIn('secret', str(error))
        else:
            self.fail('invalid name accepted')


if __name__ == '__main__':
    unittest.main()
