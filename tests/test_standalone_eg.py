"""Synthetic standalone-EG composition and exact-layout checks only."""

import binascii
import hashlib
import json
import unittest

from nikon_z30_research.standalone_eg import (
    EgBuildError,
    EgBuildPolicy,
    EgEdit,
    audit_standalone_eg,
    compose_standalone_eg,
    policy_from_complete_manifest,
)


def valid_synthetic_eg(size=96):
    body = bytearray((index * 37 + 11) & 0xFF for index in range(size))
    body[-2:] = binascii.crc_hqx(body[:-2], 0).to_bytes(2, "big")
    return bytes(body)


def policy_for(original, edits=(), payload=b"", *, capacity=None):
    return EgBuildPolicy(
        original_size=len(original),
        original_sha256=hashlib.sha256(original).hexdigest(),
        edits=tuple(edits),
        payload=payload,
        payload_sha256=hashlib.sha256(payload).hexdigest() if payload else None,
        capacity=capacity,
    )


class StandaloneEgTests(unittest.TestCase):
    def parse_manifest(self, original, value, *, payload=b"", capacity=None):
        return policy_from_complete_manifest(
            json.dumps(value).encode(), payload=payload, capacity=capacity,
            expected_source_size=len(original),
            expected_source_sha256=hashlib.sha256(original).hexdigest(),
        )

    def complete_manifest(self, original, payload=b""):
        old, new = original[48:50], b"XY"
        entry = {
            "kind": "synthetic-table",
            "file_offset": 48,
            "length": 2,
            "expected_hex": old.hex(),
            "expected_sha256": hashlib.sha256(old).hexdigest(),
            "replacement_hex": new.hex(),
            "replacement_sha256": hashlib.sha256(new).hexdigest(),
        }
        value = {
            "schema": "z30-private-exact-span-manifest-v1",
            "status": "COMPLETE_REVIEWED_PLAN",
            "source_size": len(original),
            "source_sha256": hashlib.sha256(original).hexdigest(),
            "load_base": "0x10020000",
            "edit_count": 1,
            "edits": [entry],
        }
        if payload:
            value["append"] = {
                "file_offset": len(original) - 2,
                "length": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        return value

    def test_unchanged_original_round_trip_and_crc(self):
        original = valid_synthetic_eg()
        candidate, report = compose_standalone_eg(original, policy_for(original))
        self.assertEqual(candidate, original)
        self.assertEqual(report.candidate_sha256, hashlib.sha256(original).hexdigest())
        self.assertTrue(report.crc_valid)
        self.assertEqual(report.changed_bytes, 0)

    def test_complete_manifest_load_checks_span_hashes_and_composes(self):
        original = valid_synthetic_eg()
        payload = b"synthetic payload"
        manifest = self.complete_manifest(original, payload)
        policy = self.parse_manifest(original, manifest, payload=payload, capacity=128)
        candidate, report = compose_standalone_eg(original, policy)
        self.assertEqual(candidate[48:50], b"XY")
        self.assertEqual(report.payload_size, len(payload))
        self.assertTrue(report.crc_valid)

    def test_incomplete_manifest_and_bad_replacement_hash_rejected(self):
        original = valid_synthetic_eg()
        manifest = self.complete_manifest(original)
        manifest["status"] = "DATA_ONLY_INCOMPLETE_NOT_A_FIRMWARE_CANDIDATE"
        with self.assertRaisesRegex(EgBuildError, "not marked complete"):
            self.parse_manifest(original, manifest)

        manifest = self.complete_manifest(original)
        manifest["edits"][0]["replacement_sha256"] = "0" * 64
        with self.assertRaisesRegex(EgBuildError, "digest mismatch"):
            self.parse_manifest(original, manifest)

    def test_manifest_append_location_length_hash_and_payload_are_bound(self):
        original = valid_synthetic_eg()
        payload = b"payload"
        manifest = self.complete_manifest(original, payload)
        manifest["append"]["file_offset"] -= 1
        with self.assertRaisesRegex(EgBuildError, "append record/payload mismatch"):
            self.parse_manifest(original, manifest, payload=payload)

        manifest = self.complete_manifest(original, payload)
        with self.assertRaisesRegex(EgBuildError, "append record/payload mismatch"):
            self.parse_manifest(original, manifest, payload=b"wrong")

        manifest = self.complete_manifest(original)
        with self.assertRaisesRegex(EgBuildError, "no append record"):
            self.parse_manifest(original, manifest, payload=payload)

    def test_manifest_must_target_pinned_z30_original_by_default(self):
        original = valid_synthetic_eg()
        manifest_bytes = json.dumps(self.complete_manifest(original)).encode()
        with self.assertRaisesRegex(EgBuildError, "does not target"):
            policy_from_complete_manifest(manifest_bytes)

    def test_exact_edit_and_payload_append_before_recomputed_crc(self):
        original = valid_synthetic_eg()
        edit = EgEdit("synthetic-table", 48, original[48:50], b"XY")
        payload = b"synthetic-thumb-code"
        policy = policy_for(original, (edit,), payload, capacity=128)
        candidate, report = compose_standalone_eg(original, policy)

        insertion = len(original) - 2
        self.assertEqual(len(candidate), len(original) + len(payload))
        self.assertEqual(candidate[48:50], b"XY")
        self.assertEqual(candidate[insertion:insertion + len(payload)], payload)
        self.assertEqual(candidate[0x10:0x14], original[0x10:0x14])
        self.assertEqual(candidate[0x24:0x2C], original[0x24:0x2C])
        self.assertEqual(binascii.crc_hqx(candidate[:-2], 0), int.from_bytes(candidate[-2:], "big"))
        self.assertEqual(binascii.crc_hqx(candidate, 0), 0)
        self.assertEqual(report.edit_count, 1)
        self.assertEqual(report.payload_size, len(payload))

    def test_wrong_original_identity_rejected(self):
        original = valid_synthetic_eg()
        policy = policy_for(original)
        with self.assertRaisesRegex(EgBuildError, "identity mismatch"):
            compose_standalone_eg(original[:-1] + b"!", policy)

    def test_invalid_original_crc_rejected(self):
        original = valid_synthetic_eg()
        corrupted = original[:-1] + bytes([original[-1] ^ 1])
        policy = policy_for(corrupted)
        with self.assertRaisesRegex(EgBuildError, "CRC"):
            compose_standalone_eg(corrupted, policy)

    def test_header_and_metadata_edits_rejected(self):
        original = valid_synthetic_eg()
        for offset in (0x10, 0x24):
            edit = EgEdit("protected", offset, original[offset:offset + 1], b"Z")
            with self.subTest(offset=offset), self.assertRaisesRegex(EgBuildError, "protected"):
                compose_standalone_eg(original, policy_for(original, (edit,)))

    def test_overlap_unsorted_or_size_changing_edit_rejected(self):
        original = valid_synthetic_eg()
        a = EgEdit("a", 48, original[48:51], b"abc")
        overlap = EgEdit("b", 50, original[50:52], b"de")
        with self.assertRaisesRegex(EgBuildError, "bounds, order or length"):
            compose_standalone_eg(original, policy_for(original, (a, overlap)))
        with self.assertRaisesRegex(EgBuildError, "bounds, order or length"):
            compose_standalone_eg(original, policy_for(original, (overlap, a)))
        resized = EgEdit("resize", 48, original[48:50], b"long")
        with self.assertRaisesRegex(EgBuildError, "bounds, order or length"):
            compose_standalone_eg(original, policy_for(original, (resized,)))

    def test_wrong_expected_span_rejected(self):
        original = valid_synthetic_eg()
        edit = EgEdit("wrong-source", 48, b"xx", b"yy")
        with self.assertRaisesRegex(EgBuildError, "expected bytes mismatch"):
            compose_standalone_eg(original, policy_for(original, (edit,)))

    def test_payload_hash_and_capacity_are_hard_gates(self):
        original = valid_synthetic_eg()
        payload = b"bounded synthetic payload"
        policy = EgBuildPolicy(len(original), hashlib.sha256(original).hexdigest(), (),
                               payload, "0" * 64, 128)
        with self.assertRaisesRegex(EgBuildError, "payload identity mismatch"):
            compose_standalone_eg(original, policy)
        with self.assertRaisesRegex(EgBuildError, "parser capacity"):
            compose_standalone_eg(original, policy_for(original, payload=payload, capacity=97))

    def test_independent_audit_rejects_unlisted_changes_and_wrong_payload(self):
        original = valid_synthetic_eg()
        edit = EgEdit("one-span", 48, original[48:49], b"Z")
        policy = policy_for(original, (edit,), b"payload")
        candidate, _ = compose_standalone_eg(original, policy)

        changed = bytearray(candidate)
        changed[60] ^= 1
        changed[-2:] = binascii.crc_hqx(changed[:-2], 0).to_bytes(2, "big")
        with self.assertRaisesRegex(EgBuildError, "outside the edit plan"):
            audit_standalone_eg(original, bytes(changed), policy)

        changed = bytearray(candidate)
        changed[len(original) - 2] ^= 1
        changed[-2:] = binascii.crc_hqx(changed[:-2], 0).to_bytes(2, "big")
        with self.assertRaisesRegex(EgBuildError, "payload mismatch"):
            audit_standalone_eg(original, bytes(changed), policy)

    def test_audit_rejects_length_and_crc_errors(self):
        original = valid_synthetic_eg()
        policy = policy_for(original)
        candidate, _ = compose_standalone_eg(original, policy)
        with self.assertRaisesRegex(EgBuildError, "length mismatch"):
            audit_standalone_eg(original, candidate + b"x", policy)
        broken_crc = candidate[:-1] + bytes([candidate[-1] ^ 1])
        with self.assertRaisesRegex(EgBuildError, "CRC"):
            audit_standalone_eg(original, broken_crc, policy)


if __name__ == "__main__":
    unittest.main()
