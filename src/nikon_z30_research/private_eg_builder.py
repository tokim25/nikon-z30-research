"""Write an audited standalone-EG candidate outside the repository.

This module is a private build primitive, not an installation workflow. The
caller must supply the SHA-256 of the exact manifest they reviewed. Firmware,
manifest, payload, and output paths must all resolve outside the project tree;
the output is created with owner-only permissions.
"""

from pathlib import Path
import hashlib
import os

from .standalone_eg import (
    EgAuditReport,
    EgBuildError,
    audit_standalone_eg,
    compose_standalone_eg,
    policy_from_complete_manifest,
)
from .verified_firmware import require_verified_eg_module


DEFAULT_PARSER_CAPACITY = 0x2940000
_REPO_ROOT = Path(__file__).resolve().parents[2]


def _outside_repository(path: Path, repo_root: Path) -> Path:
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(repo_root)
    except ValueError:
        return resolved
    raise EgBuildError("firmware build paths must be outside the repository")


def build_private_eg_candidate(
    *,
    original_path: str | Path,
    manifest_path: str | Path,
    output_path: str | Path,
    reviewed_manifest_sha256: str,
    payload_path: str | Path | None = None,
    repository_root: str | Path = _REPO_ROOT,
) -> EgAuditReport:
    """Build and independently re-open an exact candidate in a private path.

    The function refuses incomplete plans through the manifest parser,
    requires the user-supplied digest of the reviewed plan, never overwrites
    an output, and removes a partial output if post-write audit fails.
    """
    if (not isinstance(reviewed_manifest_sha256, str)
            or len(reviewed_manifest_sha256) != 64
            or any(c not in "0123456789abcdef" for c in reviewed_manifest_sha256)):
        raise EgBuildError("reviewed manifest SHA-256 must be 64 lowercase hex characters")

    root = Path(repository_root).resolve(strict=True)
    original_file = _outside_repository(Path(original_path), root)
    manifest_file = _outside_repository(Path(manifest_path), root)
    payload_file = (_outside_repository(Path(payload_path), root)
                    if payload_path is not None else None)

    if not original_file.is_file() or not manifest_file.is_file():
        raise EgBuildError("original and manifest must be regular files")
    if payload_file is not None and not payload_file.is_file():
        raise EgBuildError("payload must be a regular file")

    output_input = Path(output_path)
    if output_input.is_symlink():
        raise EgBuildError("candidate output must not be a symlink")
    output_parent = output_input.parent.resolve(strict=True)
    output_file = _outside_repository(output_parent / output_input.name, root)
    if output_file.exists():
        raise EgBuildError("candidate output already exists")

    # Identity validation happens before any composition or output creation.
    source_report = require_verified_eg_module(original_file)
    original = original_file.read_bytes()
    manifest_bytes = manifest_file.read_bytes()
    actual_manifest_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
    if actual_manifest_sha256 != reviewed_manifest_sha256:
        raise EgBuildError("reviewed manifest SHA-256 mismatch")
    if payload_file is not None and payload_file.stat().st_size > (
            DEFAULT_PARSER_CAPACITY - source_report.size_bytes):
        raise EgBuildError("payload exceeds standalone-EG parser capacity")
    payload = payload_file.read_bytes() if payload_file is not None else b""
    policy = policy_from_complete_manifest(
        manifest_bytes,
        payload=payload,
        capacity=DEFAULT_PARSER_CAPACITY,
    )
    candidate, report = compose_standalone_eg(original, policy)

    # Exclusive creation prevents accidental replacement of an existing file.
    created = False
    descriptor = None
    try:
        descriptor = os.open(
            output_file,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        created = True
        os.fchmod(descriptor, 0o600)
        stream = os.fdopen(descriptor, "wb")
        descriptor = None
        with stream:
            stream.write(candidate)
        written = output_file.read_bytes()
        independent = audit_standalone_eg(original, written, policy)
        if (independent.candidate_sha256 != report.candidate_sha256
                or independent.policy_sha256 != report.policy_sha256):
            raise EgBuildError("post-write candidate audit identity mismatch")
        return independent
    except Exception:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
        if created:
            try:
                output_file.unlink(missing_ok=True)
            except OSError:
                pass
        raise
