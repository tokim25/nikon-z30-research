"""Read-only exact-edit audit. No patch generation, byte logging or file writes."""

from dataclasses import dataclass
import hashlib
import json
import re


class PatchAuditError(ValueError):
    """Identity, manifest or candidate differs from the independently reviewed plan."""


@dataclass(frozen=True)
class ExactEdit:
    label: str
    offset: int
    size: int
    original_sha256: str
    candidate_sha256: str


@dataclass(frozen=True)
class PatchAuditReport:
    original_sha256: str
    candidate_sha256: str
    manifest_sha256: str
    size: int
    edit_count: int
    changed_bytes: int


def _digest_valid(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def audit_exact_edits(original: bytes, candidate: bytes, *, original_size: int,
                      original_sha256: str, edits: tuple[ExactEdit, ...]) -> PatchAuditReport:
    """Pin the original, hash both sides of each edit, compare all other bytes.

    Supply identities and edits independently of the candidate. Do not derive
    replacement digests by observing a candidate and then claim plan compliance.
    Offsets are file-relative, never runtime addresses. Resizing is forbidden.
    CRC fields receive no exemption: include exact reviewed checksum edits or
    reject them. This function checks neither CRC correctness nor code semantics.
    Reports contain hashes/counts only; concrete manifests stay outside Git.
    """
    if not isinstance(original, bytes) or not isinstance(candidate, bytes):
        raise PatchAuditError('inputs must be immutable bytes')
    if type(original_size) is not int or original_size < 0 or not _digest_valid(original_sha256):
        raise PatchAuditError('invalid original identity policy')
    if len(original) != original_size or hashlib.sha256(original).hexdigest() != original_sha256:
        raise PatchAuditError('original identity mismatch')
    if len(candidate) != original_size:
        raise PatchAuditError('candidate size mismatch')
    if not isinstance(edits, tuple):
        raise PatchAuditError('edits must be an ordered tuple')

    cursor = 0
    labels = set()
    for index, edit in enumerate(edits):
        if not isinstance(edit, ExactEdit):
            raise PatchAuditError(f'edit {index} invalid specification')
        if not isinstance(edit.label, str) or not edit.label.strip() or edit.label in labels:
            raise PatchAuditError(f'edit {index} invalid or duplicate label')
        labels.add(edit.label)
        if (type(edit.offset) is not int or type(edit.size) is not int
                or edit.offset < cursor or edit.size <= 0
                or edit.offset + edit.size > original_size):
            raise PatchAuditError(f'edit {index} bounds/order/overlap mismatch')
        if not _digest_valid(edit.original_sha256) or not _digest_valid(edit.candidate_sha256):
            raise PatchAuditError(f'edit {index} invalid digest')
        if edit.original_sha256 == edit.candidate_sha256:
            raise PatchAuditError(f'edit {index} must describe a change')
        cursor = edit.offset + edit.size

    old_view, new_view = memoryview(original), memoryview(candidate)
    cursor = changed = 0
    for index, edit in enumerate(edits):
        if old_view[cursor:edit.offset] != new_view[cursor:edit.offset]:
            raise PatchAuditError('unexpected change outside planned edits')
        end = edit.offset + edit.size
        old, new = old_view[edit.offset:end], new_view[edit.offset:end]
        if hashlib.sha256(old).hexdigest() != edit.original_sha256:
            raise PatchAuditError(f'edit {index} original digest mismatch')
        if hashlib.sha256(new).hexdigest() != edit.candidate_sha256:
            raise PatchAuditError(f'edit {index} candidate digest mismatch')
        changed += sum(left != right for left, right in zip(old, new))
        cursor = end
    if old_view[cursor:] != new_view[cursor:]:
        raise PatchAuditError('unexpected change outside planned edits')
    # Versioned, deterministic identity for this exact policy, including labels.
    policy = {'schema': 1, 'original_size': original_size, 'original_sha256': original_sha256,
              'edits': [[e.label, e.offset, e.size, e.original_sha256, e.candidate_sha256]
                        for e in edits]}
    encoded = json.dumps(policy, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
    return PatchAuditReport(original_sha256, hashlib.sha256(candidate).hexdigest(),
                            hashlib.sha256(encoded).hexdigest(), original_size, len(edits), changed)
