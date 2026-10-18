"""Synthetic integrity controls, with no firmware bytes or derived keys."""

import hashlib
import unittest

from nikon_z30_research.package_digest import PackageDigestError, verify_package_digests


class PackageDigestTests(unittest.TestCase):
    def setUp(self):
        self.original = b'synthetic original body with trailer'
        self.candidate = b'synthetic changed body with trailer'
        self.suffix = b'TESTONLY'
        self.arguments = dict(
            original_digest=hashlib.sha1(self.original + self.suffix).digest(),
            candidate_digest=hashlib.sha1(self.candidate + self.suffix).digest(),
            suffix=self.suffix,
        )

    def verify(self, **changes):
        return verify_package_digests(self.original, self.candidate,
                                      **(self.arguments | changes))

    def test_valid_pair_has_bounded_report_without_secret(self):
        report = self.verify()
        self.assertEqual(report.original_body_sha256, hashlib.sha256(self.original).hexdigest())
        self.assertEqual(report.candidate_body_sha256, hashlib.sha256(self.candidate).hexdigest())
        self.assertEqual(report.hardware_readiness, 'not_established')
        self.assertNotIn(self.suffix.decode(), repr(report))

    def test_missing_wrong_size_and_mutable_suffix_rejected(self):
        for value in (None, b'', b'short', b'too long suffix', bytearray(self.suffix)):
            with self.subTest(value=value), self.assertRaises(PackageDigestError):
                self.verify(suffix=value)

    def test_wrong_suffix_rejects_original_first(self):
        with self.assertRaisesRegex(PackageDigestError, 'original package digest mismatch'):
            self.verify(suffix=b'WRONGKEY', candidate_digest=b'')

    def test_old_digest_cannot_pass_changed_candidate(self):
        with self.assertRaisesRegex(PackageDigestError, 'candidate package digest mismatch'):
            self.verify(candidate_digest=self.arguments['original_digest'])

    def test_trailer_is_covered(self):
        with self.assertRaisesRegex(PackageDigestError, 'candidate package digest mismatch'):
            verify_package_digests(self.original, self.candidate[:-1] + b'!', **self.arguments)

    def test_digest_length_and_type_rejected(self):
        for field in ('original_digest', 'candidate_digest'):
            for value in (b'', b'x' * 19, b'x' * 21, bytearray(b'x' * 20)):
                with self.subTest(field=field, value=value), self.assertRaises(PackageDigestError):
                    self.verify(**{field: value})

    def test_body_type_and_empty_body_rejected(self):
        for value in (b'', bytearray(self.original), None):
            for original, candidate in ((value, self.candidate), (self.original, value)):
                with self.subTest(original=original, candidate=candidate):
                    with self.assertRaises(PackageDigestError):
                        verify_package_digests(original, candidate, **self.arguments)


if __name__ == '__main__':
    unittest.main()
