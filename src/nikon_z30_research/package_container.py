"""Read-only validation of decoded containers; no decoding or firmware writes.

Passing establishes layout/checksum consistency against caller-supplied policy.
It does not establish provenance, permitted edits, or camera acceptance.
"""

import binascii
from dataclasses import dataclass
import hashlib
import re
import struct


class ContainerValidationError(ValueError):
    """An input or its validation policy is invalid; messages contain no payload."""


@dataclass(frozen=True)
class ComponentSpec:
    name: str
    size: int
    unchanged_sha256: str | None = None


@dataclass(frozen=True)
class ComponentReport:
    name: str
    offset: int
    size: int
    sha256: str
    unchanged_checked: bool


@dataclass(frozen=True)
class ContainerReport:
    size: int
    sha256: str
    components: tuple[ComponentReport, ...]


def validate_container(data: bytes, expected: tuple[ComponentSpec, ...]) -> ContainerReport:
    """Validate one immutable decoded container against independently trusted specs.

    Specs must come from the verified original or a reviewed build manifest,
    never from the candidate being checked. Pin a digest for every component
    required to stay unchanged. Unpinned components receive structural/CRC
    checks only; a separate change-span audit is required for their edits.
    The encoded package's outer prefix is outside this API's scope.
    """
    if not isinstance(data, bytes):
        raise ContainerValidationError('container must be immutable bytes')
    if not isinstance(expected, tuple) or not expected or len(expected) > 0xffffffff:
        raise ContainerValidationError('expected components must be a nonempty tuple')
    names = set()
    for spec in expected:
        if not isinstance(spec, ComponentSpec) or not isinstance(spec.name, str):
            raise ContainerValidationError('invalid component specification')
        try:
            name = spec.name.encode('ascii')
        except UnicodeEncodeError:
            raise ContainerValidationError('component names must be ASCII') from None
        if not 1 <= len(name) <= 16 or b'\0' in name or spec.name in names:
            raise ContainerValidationError('invalid or duplicate expected component name')
        names.add(spec.name)
        if type(spec.size) is not int or not 2 <= spec.size <= 0xffffffff:
            raise ContainerValidationError('invalid expected component size')
        if spec.unchanged_sha256 is not None and (
            not isinstance(spec.unchanged_sha256, str)
            or re.fullmatch(r'[0-9a-f]{64}', spec.unchanged_sha256) is None
        ):
            raise ContainerValidationError('invalid expected component digest')

    directory_end = 48 + 32 * len(expected)
    expected_size = directory_end + sum(spec.size for spec in expected) + 16
    if len(data) != expected_size:
        raise ContainerValidationError('container length mismatch')
    if data[:32] != b' ' * 32:
        raise ContainerValidationError('container prefix mismatch')
    count, declared_end, reserved0, reserved1 = struct.unpack_from('>4I', data, 32)
    if (count, declared_end, reserved0, reserved1) != (len(expected), directory_end, 0, 0):
        raise ContainerValidationError('container header mismatch')
    trailer = len(data) - 16
    if data[trailer + 2:] != bytes(14):
        raise ContainerValidationError('container trailer mismatch')

    reports = []
    view = memoryview(data)
    cursor = directory_end
    for index, spec in enumerate(expected):
        raw_name, start, size, reserved0, reserved1 = struct.unpack_from(
            '>16s4I', data, 48 + 32 * index,
        )
        if raw_name != spec.name.encode('ascii').ljust(16, b'\0'):
            raise ContainerValidationError(f'component {index} name/order mismatch')
        if reserved0 or reserved1:
            raise ContainerValidationError(f'component {index} reserved field mismatch')
        if start != cursor or size != spec.size or start + size > trailer:
            raise ContainerValidationError(f'component {index} layout mismatch')
        component = view[start:start + size]
        if binascii.crc_hqx(component, 0) != 0:
            raise ContainerValidationError(f'component {index} CRC mismatch')
        digest = hashlib.sha256(component).hexdigest()
        if spec.unchanged_sha256 is not None and digest != spec.unchanged_sha256:
            raise ContainerValidationError(f'component {index} unchanged digest mismatch')
        reports.append(ComponentReport(spec.name, start, size, digest,
                                       spec.unchanged_sha256 is not None))
        cursor += size
    if cursor != trailer:
        raise ContainerValidationError('component coverage mismatch')
    if binascii.crc_hqx(view[:trailer], 0) != int.from_bytes(data[trailer:trailer + 2], 'big'):
        raise ContainerValidationError('container CRC mismatch')
    return ContainerReport(len(data), hashlib.sha256(data).hexdigest(), tuple(reports))
