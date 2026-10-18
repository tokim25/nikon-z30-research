"""Synthetic manifests and headers only. No firmware content or real patch manifests."""

import hashlib
import unittest

from nikon_z30_research.edit_policy import (
    EditPolicyError, HeaderFieldPolicy, PreviewSize,
    check_edit_categories, check_header_field, check_preview_sizes,
)
from nikon_z30_research.patch_audit import ExactEdit


def digest(data):
    return hashlib.sha256(data).hexdigest()


XPAN = frozenset({'bars', 'label', 'geometry', 'preview'})


class CategoryTests(unittest.TestCase):
    def setUp(self):
        self.edits = tuple(ExactEdit(f'edit {n}', n * 4, 2, digest(b'ab'), digest(b'cd'))
                           for n in range(4))
        self.categories = {'edit 0': 'bars', 'edit 1': 'label',
                           'edit 2': 'geometry', 'edit 3': 'preview'}

    def test_complete_manifest_counts_each_category(self):
        counts = check_edit_categories(self.edits, self.categories, XPAN)
        self.assertEqual(counts, {'bars': 1, 'label': 1, 'geometry': 1, 'preview': 1})

    def test_missing_required_category_rejected(self):
        partial = dict(self.categories)
        partial['edit 3'] = 'bars'  # no preview edit left
        with self.assertRaisesRegex(EditPolicyError, 'preview'):
            check_edit_categories(self.edits, partial, XPAN)

    def test_unknown_category_rejected(self):
        bad = dict(self.categories)
        bad['edit 0'] = 'nonsense'
        with self.assertRaisesRegex(EditPolicyError, 'unknown edit category'):
            check_edit_categories(self.edits, bad, XPAN)

    def test_category_mapping_must_match_labels_exactly(self):
        for categories in ({k: v for k, v in self.categories.items() if k != 'edit 3'},
                           {**self.categories, 'extra': 'bars'}):
            with self.assertRaisesRegex(EditPolicyError, 'exactly one category'):
                check_edit_categories(self.edits, categories, XPAN)

    def test_required_must_be_known_frozenset(self):
        for required in ({'bars'}, frozenset({'unknown'})):
            with self.assertRaisesRegex(EditPolicyError, 'required categories'):
                check_edit_categories(self.edits, self.categories, required)

    def test_extra_optional_category_allowed(self):
        edits = self.edits + (ExactEdit('edit 4', 99, 2, digest(b'ab'), digest(b'cd')),)
        categories = {**self.categories, 'edit 4': 'crc'}
        counts = check_edit_categories(edits, categories, XPAN)
        self.assertEqual(counts['crc'], 1)


class HeaderFieldTests(unittest.TestCase):
    def setUp(self):
        self.original = b'0123456789abcdefghijklmnopqrstuvwxyz0123456789ABCDEF'
        self.candidate = bytearray(self.original)
        self.candidate[0x24:0x24 + 8] = b'NEWVALUE'
        self.candidate = bytes(self.candidate)

    def field(self, decision, original=None, candidate=None):
        original = self.original if original is None else original
        candidate = self.candidate if candidate is None else candidate
        return HeaderFieldPolicy('field_0x24', 0x24, 8, decision,
                                 digest(original[0x24:0x24 + 8]),
                                 digest(candidate[0x24:0x24 + 8]))

    def test_replace_decision_binds_changed_field(self):
        identity = check_header_field(self.original, self.candidate, self.field('replace'))
        self.assertEqual(identity, check_header_field(self.original, self.candidate, self.field('replace')))

    def test_preserve_decision_requires_identical_field(self):
        same = self.field('preserve', candidate=self.original)
        self.assertTrue(check_header_field(self.original, self.original, same))
        with self.assertRaisesRegex(EditPolicyError, 'preserve decision'):
            check_header_field(self.original, self.candidate, self.field('preserve'))

    def test_replace_decision_requires_a_change(self):
        with self.assertRaisesRegex(EditPolicyError, 'replace decision'):
            check_header_field(self.original, self.original,
                               self.field('replace', candidate=self.original))

    def test_digest_mismatch_rejected(self):
        wrong = HeaderFieldPolicy('field_0x24', 0x24, 8, 'replace',
                                  digest(b'XXXXXXXX'), digest(self.candidate[0x24:0x24 + 8]))
        with self.assertRaisesRegex(EditPolicyError, 'original digest'):
            check_header_field(self.original, self.candidate, wrong)

    def test_malformed_digest_rejected(self):
        bad = HeaderFieldPolicy('field_0x24', 0x24, 8, 'replace', 'not-a-digest',
                                digest(self.candidate[0x24:0x24 + 8]))
        with self.assertRaisesRegex(EditPolicyError, 'invalid header field digest'):
            check_header_field(self.original, self.candidate, bad)

    def test_candidate_digest_mismatch_rejected(self):
        wrong = HeaderFieldPolicy('field_0x24', 0x24, 8, 'replace',
                                  digest(self.original[0x24:0x24 + 8]), digest(b'OTHER888'))
        with self.assertRaisesRegex(EditPolicyError, 'candidate digest'):
            check_header_field(self.original, self.candidate, wrong)

    def test_invalid_bounds_and_decisions_rejected(self):
        cases = [
            HeaderFieldPolicy('f', -1, 8, 'replace', digest(b''), digest(b'')),
            HeaderFieldPolicy('f', 0, 0, 'replace', digest(b''), digest(b'')),
            HeaderFieldPolicy('f', 50, 8, 'replace', digest(b''), digest(b'')),
            self.field('delete'),
        ]
        for policy in cases:
            with self.subTest(policy=policy):
                with self.assertRaises(EditPolicyError):
                    check_header_field(self.original, self.candidate, policy)

    def test_mutable_input_rejected(self):
        with self.assertRaisesRegex(EditPolicyError, 'immutable bytes'):
            check_header_field(bytearray(self.original), self.candidate, self.field('replace'))


class PreviewSizeTests(unittest.TestCase):
    # 65:24 = 2.7083...
    RATIO = 65 / 24

    def sizes(self):
        return (PreviewSize('small', 480, 176, 640, 360),
                PreviewSize('large', 1080, 400, 1920, 1080))

    def test_in_bounds_aligned_sizes_accepted(self):
        check_preview_sizes(self.sizes(), alignment=4, target_ratio=self.RATIO, tolerance=0.02)

    def test_size_exceeding_stock_allocation_rejected(self):
        oversized = (PreviewSize('small', 700, 176, 640, 360),)
        with self.assertRaisesRegex(EditPolicyError, 'exceeds stock allocation'):
            check_preview_sizes(oversized, alignment=4, target_ratio=self.RATIO, tolerance=0.02)

    def test_misaligned_size_rejected(self):
        odd = (PreviewSize('small', 481, 176, 640, 360),)
        with self.assertRaisesRegex(EditPolicyError, 'aligned'):
            check_preview_sizes(odd, alignment=4, target_ratio=self.RATIO, tolerance=0.02)

    def test_ratio_outside_tolerance_rejected(self):
        wide = (PreviewSize('small', 480, 100, 640, 360),)
        with self.assertRaisesRegex(EditPolicyError, 'ratio'):
            check_preview_sizes(wide, alignment=4, target_ratio=self.RATIO, tolerance=0.02)

    def test_empty_and_invalid_policy_rejected(self):
        with self.assertRaisesRegex(EditPolicyError, 'no preview sizes'):
            check_preview_sizes((), alignment=4, target_ratio=self.RATIO, tolerance=0.02)
        with self.assertRaisesRegex(EditPolicyError, 'invalid preview policy'):
            check_preview_sizes(self.sizes(), alignment=0, target_ratio=self.RATIO, tolerance=0.02)

    def test_nonpositive_dimensions_rejected(self):
        bad = (PreviewSize('small', 0, 176, 640, 360),)
        with self.assertRaisesRegex(EditPolicyError, 'invalid dimensions'):
            check_preview_sizes(bad, alignment=4, target_ratio=self.RATIO, tolerance=0.02)


if __name__ == '__main__':
    unittest.main()
