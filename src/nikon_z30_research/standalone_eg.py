"""Private-use standalone-EG composition checks using exact reviewed spans.

This module never reads or writes paths and never communicates with a device.
Callers must keep firmware input, plans, payloads and composed artifacts
outside the repository. Real build code must first pass the verified-original
gate in :mod:`verified_firmware`.
"""

from dataclasses import dataclass
import binascii
import hashlib
import json
import re

from .verified_firmware import VERIFIED_EG_SHA256, VERIFIED_EG_SIZE


class EgBuildError(ValueError):
    """A standalone-EG build plan or candidate violates its exact policy."""


@dataclass(frozen=True)
class EgEdit:
    """One exact, same-length edit expressed in original file coordinates."""

    label: str
    offset: int
    expected: bytes
    replacement: bytes


@dataclass(frozen=True)
class EgBuildPolicy:
    """Exact original, edit list and optional payload inserted before CRC."""

    original_size: int
    original_sha256: str
    edits: tuple[EgEdit, ...]
    payload: bytes = b""
    payload_sha256: str | None = None
    capacity: int | None = None


@dataclass(frozen=True)
class EgAuditReport:
    original_sha256: str
    candidate_sha256: str
    policy_sha256: str
    original_size: int
    candidate_size: int
    edit_count: int
    changed_bytes: int
    payload_size: int
    crc_valid: bool


_PROTECTED = ((0x10, 0x14), (0x24, 0x2C))
_TRAILER_SIZE = 2
_DIGEST_RE = re.compile(r"[0-9a-f]{64}\Z")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def policy_from_complete_manifest(
    manifest_bytes: bytes, *, payload: bytes = b"", capacity: int | None = None,
    expected_source_size: int = VERIFIED_EG_SIZE,
    expected_source_sha256: str = VERIFIED_EG_SHA256,
) -> EgBuildPolicy:
    """Parse a private complete-plan manifest and verify every declared hash.

    The manifest must explicitly have status ``COMPLETE_REVIEWED_PLAN``.
    Data-only/incomplete manifests are intentionally refused by this builder
    entry point. The returned policy still requires the exact original bytes
    to be supplied to :func:`compose_standalone_eg`.
    """
    if not isinstance(manifest_bytes, bytes):
        raise EgBuildError("manifest must be immutable bytes")
    try:
        manifest = json.loads(manifest_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise EgBuildError("manifest is not valid JSON") from None
    if not isinstance(manifest, dict):
        raise EgBuildError("manifest root must be an object")
    if manifest.get("schema") != "z30-private-exact-span-manifest-v1":
        raise EgBuildError("unsupported manifest schema")
    if manifest.get("status") != "COMPLETE_REVIEWED_PLAN":
        raise EgBuildError("manifest is not marked complete and reviewed")

    source_size = manifest.get("source_size")
    source_sha256 = manifest.get("source_sha256")
    if (type(source_size) is not int or source_size <= _TRAILER_SIZE
            or not isinstance(source_sha256, str)
            or _DIGEST_RE.fullmatch(source_sha256) is None):
        raise EgBuildError("manifest source identity is invalid")
    if (source_size != expected_source_size or source_sha256 != expected_source_sha256):
        raise EgBuildError("manifest does not target the verified Z 30 EG")
    if manifest.get("load_base") != "0x10020000":
        raise EgBuildError("manifest load base mismatch")

    entries = manifest.get("edits")
    if (not isinstance(entries, list) or not entries
            or type(manifest.get("edit_count")) is not int
            or manifest["edit_count"] != len(entries)):
        raise EgBuildError("manifest edit list/count mismatch")

    edits = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise EgBuildError(f"manifest edit {index} is invalid")
        offset = entry.get("file_offset")
        size = entry.get("length")
        expected_hex = entry.get("expected_hex")
        replacement_hex = entry.get("replacement_hex")
        expected_sha = entry.get("expected_sha256")
        replacement_sha = entry.get("replacement_sha256")
        if (type(offset) is not int or type(size) is not int or size <= 0
                or not isinstance(expected_hex, str) or not isinstance(replacement_hex, str)
                or re.fullmatch(r"(?:[0-9a-f]{2})+", expected_hex) is None
                or re.fullmatch(r"(?:[0-9a-f]{2})+", replacement_hex) is None
                or len(expected_hex) != size * 2 or len(replacement_hex) != size * 2
                or not isinstance(expected_sha, str) or _DIGEST_RE.fullmatch(expected_sha) is None
                or not isinstance(replacement_sha, str)
                or _DIGEST_RE.fullmatch(replacement_sha) is None):
            raise EgBuildError(f"manifest edit {index} encoding/length/hash is invalid")
        expected = bytes.fromhex(expected_hex)
        replacement = bytes.fromhex(replacement_hex)
        if _sha256(expected) != expected_sha or _sha256(replacement) != replacement_sha:
            raise EgBuildError(f"manifest edit {index} digest mismatch")
        kind = entry.get("kind")
        if not isinstance(kind, str) or not kind:
            raise EgBuildError(f"manifest edit {index} has no kind")
        label = f"{index}:{kind}:{entry.get('language_index', '')}:{entry.get('string_id', '')}"
        edits.append(EgEdit(label, offset, expected, replacement))

    append = manifest.get("append")
    if append is None:
        if payload:
            raise EgBuildError("payload supplied but manifest has no append record")
        payload_sha = None
    else:
        if not isinstance(append, dict):
            raise EgBuildError("manifest append record is invalid")
        append_offset = append.get("file_offset")
        append_length = append.get("length")
        append_sha = append.get("sha256")
        if (type(append_offset) is not int or append_offset != source_size - _TRAILER_SIZE
                or type(append_length) is not int or append_length <= 0
                or not isinstance(append_sha, str) or _DIGEST_RE.fullmatch(append_sha) is None
                or not isinstance(payload, bytes) or len(payload) != append_length
                or _sha256(payload) != append_sha):
            raise EgBuildError("manifest append record/payload mismatch")
        payload_sha = append_sha

    return EgBuildPolicy(source_size, source_sha256, tuple(edits), payload,
                         payload_sha256=payload_sha, capacity=capacity)


def _validate_policy(original: bytes, policy: EgBuildPolicy) -> None:
    if not isinstance(original, bytes) or not isinstance(policy, EgBuildPolicy):
        raise EgBuildError("invalid immutable input or build policy")
    if (type(policy.original_size) is not int or policy.original_size < 0
            or not isinstance(policy.original_sha256, str)
            or _DIGEST_RE.fullmatch(policy.original_sha256) is None):
        raise EgBuildError("invalid original identity policy")
    if len(original) != policy.original_size or _sha256(original) != policy.original_sha256:
        raise EgBuildError("original identity mismatch")
    if len(original) <= _TRAILER_SIZE:
        raise EgBuildError("standalone EG is too short")
    if not isinstance(policy.edits, tuple):
        raise EgBuildError("edits must be an ordered tuple")
    if not isinstance(policy.payload, bytes):
        raise EgBuildError("payload must be immutable bytes")
    if policy.payload:
        if (not isinstance(policy.payload_sha256, str)
                or _DIGEST_RE.fullmatch(policy.payload_sha256) is None
                or _sha256(policy.payload) != policy.payload_sha256):
            raise EgBuildError("payload identity mismatch")
    elif policy.payload_sha256 is not None:
        raise EgBuildError("payload digest supplied without payload")
    if policy.capacity is not None:
        if type(policy.capacity) is not int or policy.capacity < 2:
            raise EgBuildError("invalid parser capacity")
        if len(original) + len(policy.payload) > policy.capacity:
            raise EgBuildError("candidate exceeds parser capacity")

    # Native EG CRC-16/XMODEM is stored big-endian in the final two bytes.
    if binascii.crc_hqx(original[:-_TRAILER_SIZE], 0) != int.from_bytes(original[-2:], "big"):
        raise EgBuildError("original CRC mismatch")
    if binascii.crc_hqx(original, 0) != 0:
        raise EgBuildError("original CRC residue mismatch")

    cursor = 0
    labels: set[str] = set()
    for index, edit in enumerate(policy.edits):
        if not isinstance(edit, EgEdit):
            raise EgBuildError(f"edit {index} has an invalid specification")
        if not isinstance(edit.label, str) or not edit.label.strip() or edit.label in labels:
            raise EgBuildError(f"edit {index} has an invalid or duplicate label")
        labels.add(edit.label)
        if (type(edit.offset) is not int or edit.offset < cursor
                or not isinstance(edit.expected, bytes)
                or not isinstance(edit.replacement, bytes)
                or not edit.expected or len(edit.expected) != len(edit.replacement)
                or edit.offset + len(edit.expected) > len(original) - _TRAILER_SIZE):
            raise EgBuildError(f"edit {index} has invalid bounds, order or length")
        end = edit.offset + len(edit.expected)
        if any(edit.offset < protected_end and protected_start < end
               for protected_start, protected_end in _PROTECTED):
            raise EgBuildError(f"edit {index} overlaps a protected EG header field")
        if original[edit.offset:end] != edit.expected:
            raise EgBuildError(f"edit {index} expected bytes mismatch")
        if edit.expected == edit.replacement:
            raise EgBuildError(f"edit {index} does not change bytes")
        cursor = end


def audit_standalone_eg(original: bytes, candidate: bytes,
                        policy: EgBuildPolicy) -> EgAuditReport:
    """Check every candidate byte against the reviewed edits, append and CRC."""
    _validate_policy(original, policy)
    if not isinstance(candidate, bytes):
        raise EgBuildError("candidate must be immutable bytes")

    insertion = len(original) - _TRAILER_SIZE
    expected_size = len(original) + len(policy.payload)
    if len(candidate) != expected_size:
        raise EgBuildError("candidate length mismatch")
    if policy.capacity is not None and len(candidate) > policy.capacity:
        raise EgBuildError("candidate exceeds parser capacity")

    old_cursor = new_cursor = changed = 0
    for index, edit in enumerate(policy.edits):
        offset = edit.offset
        if original[old_cursor:offset] != candidate[new_cursor:offset]:
            raise EgBuildError("candidate changes bytes outside the edit plan")
        end = offset + len(edit.expected)
        actual = candidate[offset:end]
        if actual != edit.replacement:
            raise EgBuildError(f"candidate edit {index} does not match the plan")
        changed += sum(a != b for a, b in zip(edit.expected, actual))
        old_cursor = new_cursor = end

    if original[old_cursor:insertion] != candidate[new_cursor:insertion]:
        raise EgBuildError("candidate changes bytes outside the edit plan")
    if policy.payload and candidate[insertion:insertion + len(policy.payload)] != policy.payload:
        raise EgBuildError("candidate payload mismatch")
    candidate_trailer = insertion + len(policy.payload)
    changed += len(policy.payload)
    changed += sum(a != b for a, b in zip(
        original[-_TRAILER_SIZE:], candidate[candidate_trailer:candidate_trailer + _TRAILER_SIZE],
    ))
    if binascii.crc_hqx(candidate[:-_TRAILER_SIZE], 0) != int.from_bytes(candidate[-2:], "big"):
        raise EgBuildError("candidate CRC mismatch")
    if binascii.crc_hqx(candidate, 0) != 0:
        raise EgBuildError("candidate CRC residue mismatch")
    for start, end in _PROTECTED:
        if original[start:end] != candidate[start:end]:
            raise EgBuildError("candidate changes a protected EG header field")

    policy_value = {
        "schema": 1,
        "original_size": policy.original_size,
        "original_sha256": policy.original_sha256,
        "edits": [[e.label, e.offset, len(e.expected), _sha256(e.expected),
                    _sha256(e.replacement)] for e in policy.edits],
        "payload_size": len(policy.payload),
        "payload_sha256": policy.payload_sha256,
        "capacity": policy.capacity,
        "protected": [list(x) for x in _PROTECTED],
        "crc": "crc-16/xmodem-big-endian-trailer",
    }
    policy_json = json.dumps(policy_value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True).encode("ascii")
    return EgAuditReport(policy.original_sha256, _sha256(candidate), _sha256(policy_json),
                         len(original), len(candidate), len(policy.edits), changed,
                         len(policy.payload), True)


def compose_standalone_eg(original: bytes, policy: EgBuildPolicy) -> tuple[bytes, EgAuditReport]:
    """Compose in memory; payload is inserted before the native CRC trailer."""
    _validate_policy(original, policy)
    work = bytearray(original)
    for edit in policy.edits:
        start = edit.offset
        work[start:start + len(edit.expected)] = edit.replacement

    insertion = len(work) - _TRAILER_SIZE
    if policy.payload:
        work[insertion:insertion] = policy.payload
    work[-_TRAILER_SIZE:] = binascii.crc_hqx(work[:-_TRAILER_SIZE], 0).to_bytes(2, "big")
    candidate = bytes(work)
    report = audit_standalone_eg(original, candidate, policy)
    return candidate, report
