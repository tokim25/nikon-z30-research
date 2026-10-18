"""Read-only body-plus-suffix digest checks; contains no vendor key material."""

from dataclasses import dataclass
import hashlib
import hmac


class PackageDigestError(ValueError):
    """Digest inputs are absent, malformed, or fail the baseline/candidate check."""


@dataclass(frozen=True)
class PackageDigestReport:
    original_body_sha256: str
    candidate_body_sha256: str
    scope: str = 'supplied_decoded_bodies_and_header_digests_only'
    hardware_readiness: str = 'not_established'


def verify_package_digests(original_body: bytes, candidate_body: bytes, *,
                           original_digest: bytes, candidate_digest: bytes,
                           suffix: bytes | None) -> PackageDigestReport:
    """Check SHA1(body || suffix), baseline first, without generating a package.

    Callers supply the complete decoded body after the outer 32-byte prefix,
    including its trailer, and the first 20 outer-header bytes separately.
    The eight-byte suffix must come from independently justified evidence.
    Matching one baseline checks consistency; it does not establish provenance,
    native branch execution, decoding, CRCs, patch scope or camera acceptance.
    This function never discovers, guesses, logs or returns the suffix.
    """
    if not isinstance(suffix, bytes) or len(suffix) != 8:
        raise PackageDigestError('verified eight-byte suffix required')
    for label, body, expected in (
        ('original', original_body, original_digest),
        ('candidate', candidate_body, candidate_digest),
    ):
        if not isinstance(body, bytes) or not body:
            raise PackageDigestError(label + ' body must be nonempty immutable bytes')
        if not isinstance(expected, bytes) or len(expected) != 20:
            raise PackageDigestError(label + ' digest must contain twenty bytes')
        digest = hashlib.sha1(body)
        digest.update(suffix)
        if not hmac.compare_digest(digest.digest(), expected):
            raise PackageDigestError(label + ' package digest mismatch')
    return PackageDigestReport(hashlib.sha256(original_body).hexdigest(),
                               hashlib.sha256(candidate_body).hexdigest())
