"""Compose decoded-container and exact-edit checks on the same immutable inputs."""

from dataclasses import asdict, dataclass, replace
import hashlib
import json

from .package_container import ComponentSpec, ContainerReport, validate_container
from .patch_audit import ExactEdit, PatchAuditReport, audit_exact_edits
from .installation import InstallationPolicy, InstallationReport, model_installation


class PreflightError(ValueError):
    """A preflight policy is incomplete or grants changes outside its scope."""


@dataclass(frozen=True)
class PreflightReport:
    policy_sha256: str
    original: ContainerReport
    candidate: ContainerReport
    edits: PatchAuditReport
    scope: str = 'decoded_container_only'
    hardware_readiness: str = 'not_established'
    installation: InstallationReport | None = None


def preflight_decoded(original: bytes, candidate: bytes, *, original_size: int,
                      original_sha256: str, components: tuple[ComponentSpec, ...],
                      changed_components: tuple[str, ...],
                      edits: tuple[ExactEdit, ...],
                      installation: InstallationPolicy | None = None) -> PreflightReport:
    """Return a report only after all checks pass; accept no precomputed results.

    All original component hashes are mandatory. changed_components explicitly
    names the components whose hashes may differ; their exact changes are still
    pinned by edits. Every edit must fit inside one such component or the two
    container-CRC bytes. Header/directory changes and resizing are forbidden.
    Original identity and policy must be independently trusted. Encoded-package
    decoding, outer prefix, runtime mapping and camera acceptance are not tested.
    An optional installation policy models one validated component's expected
    full target span. None means no installation model was checked. Modeled
    padding/hash/chunk order do not establish physical writes or recovery.
    """
    edit_report = audit_exact_edits(original, candidate, original_size=original_size,
                                    original_sha256=original_sha256, edits=edits)
    old_report = validate_container(original, components)
    if any(spec.unchanged_sha256 is None for spec in components):
        raise PreflightError('all original component hashes must be pinned')
    if (not isinstance(changed_components, tuple)
            or any(not isinstance(name, str) for name in changed_components)
            or len(set(changed_components)) != len(changed_components)):
        raise PreflightError('changed components must be a tuple of unique names')
    known = {spec.name for spec in components}
    if not set(changed_components) <= known:
        raise PreflightError('unknown changed component')
    permitted = [(item.offset, item.offset + item.size) for item in old_report.components
                 if item.name in changed_components]
    # Exact-edit hashes pin the new CRC bytes; CRC validation checks correctness.
    permitted.append((len(original) - 16, len(original) - 14))
    for index, edit in enumerate(edits):
        if not any(start <= edit.offset and edit.offset + edit.size <= end
                   for start, end in permitted):
            raise PreflightError(f'edit {index} crosses or exceeds permitted component/CRC scope')
    candidate_specs = tuple(replace(spec, unchanged_sha256=None)
                            if spec.name in changed_components else spec for spec in components)
    new_report = validate_container(candidate, candidate_specs)
    for old, new in zip(old_report.components, new_report.components):
        if old.name in changed_components and old.sha256 == new.sha256:
            raise PreflightError('declared changed component is unchanged')
    install_report = None
    if installation is not None:
        if not isinstance(installation, InstallationPolicy):
            raise PreflightError('invalid installation policy')
        selected = next((item for item in new_report.components
                         if item.name == installation.component_name), None)
        if selected is None:
            raise PreflightError('installation component not in validated container')
        install_report = model_installation(
            candidate[selected.offset:selected.offset + selected.size], installation,
        )
    # Include every comparison policy, not just the edit plan, in this identity.
    policy = {'schema': 1, 'scope': 'decoded_container_only',
              'edit_manifest_sha256': edit_report.manifest_sha256,
              'components': [[s.name, s.size, s.unchanged_sha256] for s in components],
              'changed_components': sorted(changed_components)}
    if installation is not None:
        policy['schema'] = 2
        policy['installation'] = asdict(installation)
    encoded = json.dumps(policy, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
    return PreflightReport(hashlib.sha256(encoded).hexdigest(), old_report, new_report, edit_report,
                           installation=install_report)
