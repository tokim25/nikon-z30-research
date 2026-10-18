"""Completeness checks layered on an exact-edit manifest. No bytes logged or written.

These run beside audit_exact_edits, not instead of it: that audit proves only
the planned bytes changed; these prove the plan covers what the XPan build
needs, binds a reviewed header-field decision, and keeps preview sizes inside
the stock allocation. All values are supplied by the reviewer, never inferred
from a candidate.
"""

from dataclasses import dataclass
import hashlib
import re

from .patch_audit import ExactEdit

EDIT_CATEGORIES = frozenset({'bars', 'label', 'geometry', 'preview', 'header', 'crc'})


class EditPolicyError(ValueError):
    """The manifest is incomplete or a reviewed policy is not met."""


def _digest_valid(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def check_edit_categories(edits: tuple[ExactEdit, ...], categories: dict[str, str],
                          required: frozenset[str]) -> dict[str, int]:
    """Every edit has a known category and every required category is present.

    Returns the edit count per category. Errors name categories, never labels.
    """
    if not isinstance(required, frozenset) or not required <= EDIT_CATEGORIES:
        raise EditPolicyError('required categories must be a frozenset of known categories')
    labels = [edit.label for edit in edits]
    if set(categories) != set(labels):
        raise EditPolicyError('every edit needs exactly one category entry')
    counts = {}
    for label in labels:
        category = categories[label]
        if category not in EDIT_CATEGORIES:
            raise EditPolicyError('unknown edit category')
        counts[category] = counts.get(category, 0) + 1
    missing = sorted(required - set(counts))
    if missing:
        raise EditPolicyError(f'manifest missing required categories: {", ".join(missing)}')
    return counts


@dataclass(frozen=True)
class HeaderFieldPolicy:
    """A reviewed decision for one file-relative header field, e.g. the 8 bytes at 0x24."""
    name: str
    offset: int
    size: int
    decision: str  # 'preserve' or 'replace'
    original_sha256: str
    candidate_sha256: str


def check_header_field(original: bytes, candidate: bytes, policy: HeaderFieldPolicy) -> str:
    """Bind the field's decision to this exact original and candidate.

    'preserve' requires the candidate field to equal the original's.
    'replace' requires it to differ and match the reviewed candidate digest.
    Returns a digest identifying the policy.
    """
    if not isinstance(original, bytes) or not isinstance(candidate, bytes):
        raise EditPolicyError('inputs must be immutable bytes')
    if (type(policy.offset) is not int or type(policy.size) is not int
            or policy.offset < 0 or policy.size <= 0):
        raise EditPolicyError('invalid header field bounds')
    end = policy.offset + policy.size
    if end > len(original) or end > len(candidate):
        raise EditPolicyError('header field outside input')
    if policy.decision not in ('preserve', 'replace'):
        raise EditPolicyError('header decision must be preserve or replace')
    if not _digest_valid(policy.original_sha256) or not _digest_valid(policy.candidate_sha256):
        raise EditPolicyError('invalid header field digest')
    if policy.decision == 'preserve' and policy.original_sha256 != policy.candidate_sha256:
        raise EditPolicyError('preserve decision must pin identical digests')
    if policy.decision == 'replace' and policy.original_sha256 == policy.candidate_sha256:
        raise EditPolicyError('replace decision must describe a change')
    if hashlib.sha256(original[policy.offset:end]).hexdigest() != policy.original_sha256:
        raise EditPolicyError('header field original digest mismatch')
    if hashlib.sha256(candidate[policy.offset:end]).hexdigest() != policy.candidate_sha256:
        raise EditPolicyError('header field candidate digest mismatch')
    identity = '|'.join([policy.name, str(policy.offset), str(policy.size), policy.decision,
                         policy.original_sha256, policy.candidate_sha256])
    return hashlib.sha256(identity.encode('utf-8')).hexdigest()


@dataclass(frozen=True)
class PreviewSize:
    """A proposed preview size and the stock buffer it must fit in."""
    name: str
    width: int
    height: int
    capacity_width: int
    capacity_height: int


def check_preview_sizes(sizes: tuple[PreviewSize, ...], *, alignment: int,
                        target_ratio: float, tolerance: float) -> None:
    """Each size fits its stock buffer, is aligned, and is near the target ratio.

    Dimension caps come from the reviewed buffer constructor. If that
    constructor allocates by bytes rather than by width and height, this check
    is not sufficient on its own.
    """
    if not sizes:
        raise EditPolicyError('no preview sizes supplied')
    if type(alignment) is not int or alignment <= 0 or target_ratio <= 0 or tolerance < 0:
        raise EditPolicyError('invalid preview policy')
    for index, size in enumerate(sizes):
        values = (size.width, size.height, size.capacity_width, size.capacity_height)
        if any(type(value) is not int or value <= 0 for value in values):
            raise EditPolicyError(f'preview {index} invalid dimensions')
        if size.width > size.capacity_width or size.height > size.capacity_height:
            raise EditPolicyError(f'preview {index} exceeds stock allocation')
        if size.width % alignment or size.height % alignment:
            raise EditPolicyError(f'preview {index} not {alignment}-pixel aligned')
        if abs(size.width / size.height - target_ratio) / target_ratio > tolerance:
            raise EditPolicyError(f'preview {index} ratio outside tolerance')
