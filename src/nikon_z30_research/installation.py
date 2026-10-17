"""Static native-installation model; no image construction or device interface."""

import binascii
from dataclasses import dataclass
import hashlib


class InstallationModelError(ValueError):
    """Input or independently reviewed installation policy is inconsistent."""


@dataclass(frozen=True)
class AddressRange:
    start: int
    end: int


@dataclass(frozen=True)
class InstallationPolicy:
    component_name: str
    target_start: int
    capacity: int
    chunk_size: int
    protected_ranges: tuple[AddressRange, ...] = ()


@dataclass(frozen=True)
class InstallationReport:
    component_name: str
    component_sha256: str
    payload_sha256: str
    expected_span_sha256: str
    component_size: int
    excluded_crc_bytes: int
    payload_size: int
    padding_size: int
    padding_byte: int
    target_start: int
    target_end: int
    capacity: int
    chunk_size: int
    chunk_count: int
    scope: str = 'static_installation_model'

    def chunk(self, step: int, *, phase: str) -> AddressRange:
        """Describe one chunk in modeled order; never invokes an operation."""
        if type(step) is not int or not 0 <= step < self.chunk_count:
            raise InstallationModelError('chunk step out of bounds')
        if phase == 'erase':
            index = step
        elif phase == 'program':
            index = (step + 1) % self.chunk_count
        else:
            raise InstallationModelError('unknown modeled phase')
        start = self.target_start + index * self.chunk_size
        return AddressRange(start, start + self.chunk_size)


def model_installation(component: bytes, policy: InstallationPolicy) -> InstallationReport:
    """Hash the expected payload-plus-FF span without building or writing it.

    CRC-16 is checked on the supplied component, then its trailing two bytes
    are excluded from the payload. Every remaining byte of target capacity is
    modeled as FF. Policy must be pinned independently of candidate bytes.
    Chunk sizes describe the reviewed high-level loop, not detected hardware
    geometry. Runtime state, allocation, digest authentication and recovery are
    outside this model. The expected span hash is not physical readback.
    """
    if not isinstance(component, bytes):
        raise InstallationModelError('component must be immutable bytes')
    if not isinstance(policy, InstallationPolicy):
        raise InstallationModelError('invalid installation policy')
    if (not isinstance(policy.component_name, str) or not policy.component_name
            or '\0' in policy.component_name):
        raise InstallationModelError('invalid policy component name')
    for value in (policy.target_start, policy.capacity, policy.chunk_size):
        if type(value) is not int:
            raise InstallationModelError('installation bounds must be integers')
    if (policy.target_start < 0 or policy.capacity <= 0
            or policy.target_start + policy.capacity > 1 << 32):
        raise InstallationModelError('installation target exceeds address bounds')
    if (policy.chunk_size < 4 or policy.chunk_size & (policy.chunk_size - 1)
            or policy.target_start % policy.chunk_size or policy.capacity % policy.chunk_size):
        raise InstallationModelError('installation chunk alignment mismatch')
    if not isinstance(policy.protected_ranges, tuple):
        raise InstallationModelError('protected ranges must be an ordered tuple')
    last_end = 0
    target_end = policy.target_start + policy.capacity
    for region in policy.protected_ranges:
        if (not isinstance(region, AddressRange) or type(region.start) is not int
                or type(region.end) is not int or not 0 <= region.start < region.end <= 1 << 32
                or region.start < last_end):
            raise InstallationModelError('invalid/overlapping protected ranges')
        if policy.target_start < region.end and region.start < target_end:
            raise InstallationModelError('installation target overlaps protected range')
        last_end = region.end
    if len(component) <= 2 or len(component) - 2 > policy.capacity:
        raise InstallationModelError('payload length outside target capacity')
    if binascii.crc_hqx(component, 0) != 0:
        raise InstallationModelError('component CRC mismatch')

    payload = memoryview(component)[:-2]
    payload_digest = hashlib.sha256(payload)
    span_digest = payload_digest.copy()
    padding_size = policy.capacity - len(payload)
    # Bounded temporary padding chunk; never allocate the complete target image.
    remaining = padding_size
    padding = bytes([255]) * min(remaining, 1024 * 1024)
    while remaining:
        count = min(remaining, len(padding))
        span_digest.update(memoryview(padding)[:count])
        remaining -= count
    return InstallationReport(
        policy.component_name, hashlib.sha256(component).hexdigest(), payload_digest.hexdigest(),
        span_digest.hexdigest(), len(component), 2, len(payload), padding_size, 255,
        policy.target_start, target_end, policy.capacity, policy.chunk_size,
        policy.capacity // policy.chunk_size,
    )
