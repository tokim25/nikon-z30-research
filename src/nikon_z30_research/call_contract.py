"""Compare supplied call-boundary snapshots; no instruction or device execution."""

from dataclasses import dataclass


class CallContractError(ValueError):
    """A supplied boundary does not preserve the reviewed call contract."""


@dataclass(frozen=True)
class CallState:
    registers: tuple[int, ...]  # r0 through r12
    sp: int
    lr: int
    pc: int
    mode: str
    flags: int  # abstract NZCV nibble, not a complete processor status word
    stack_words: tuple[int, ...]  # bounded view beginning at this snapshot's SP


@dataclass(frozen=True)
class CallPolicy:
    service_address: int
    service_mode: str
    stack_word_count: int
    preserve_entry_flags: bool = False


@dataclass(frozen=True)
class CallContractReport:
    checked_stack_words: int
    checked_helper_entries: int
    entry_flags_checked: bool
    scope: str = 'supplied_call_boundaries_only'


def _word(value):
    return type(value) is int and 0 <= value < 1 << 32


def _state(state, count):
    if not isinstance(state, CallState):
        raise CallContractError('invalid call state')
    if (not isinstance(state.registers, tuple) or len(state.registers) != 13
            or not all(_word(v) for v in state.registers)):
        raise CallContractError('invalid register view')
    if not all(_word(v) for v in (state.sp, state.lr, state.pc)):
        raise CallContractError('invalid address')
    if (state.mode not in ('arm', 'thumb') or state.pc % (4 if state.mode == 'arm' else 2)
            or state.sp % 4):
        raise CallContractError('invalid mode or address alignment')
    if type(state.flags) is not int or not 0 <= state.flags < 16:
        raise CallContractError('invalid abstract flags')
    if (not isinstance(state.stack_words, tuple) or len(state.stack_words) != count
            or not all(_word(v) for v in state.stack_words)
            or state.sp + 4 * count > 1 << 32):
        raise CallContractError('invalid stack view')


def check_call_contract(incoming: CallState, service_entry: CallState,
                        reference_return: CallState, wrapper_return: CallState, *,
                        policy: CallPolicy, helper_entries: tuple[CallState, ...] = ()) -> CallContractReport:
    """Require a transparent transfer to the service and an equivalent return.

    The reference return must come from the unwrapped service on the same
    inputs. All r0-r12, SP, LR and the bounded caller stack view must reach
    service entry unchanged. Entry flags are policy-controlled; return flags
    always match the reference. Helpers must receive eight-byte-aligned SP.
    This compares evidence supplied by a caller: it cannot prove the evidence
    came from machine code, that a helper was not omitted, or full execution.
    """
    if (not isinstance(policy, CallPolicy) or not _word(policy.service_address)
            or policy.service_mode not in ('arm', 'thumb')
            or policy.service_address % (4 if policy.service_mode == 'arm' else 2)
            or type(policy.stack_word_count) is not int or not 1 <= policy.stack_word_count <= 1024
            or type(policy.preserve_entry_flags) is not bool):
        raise CallContractError('invalid call policy')
    if not isinstance(helper_entries, tuple):
        raise CallContractError('helper entries must be a tuple')
    for state in (incoming, service_entry, reference_return, wrapper_return, *helper_entries):
        _state(state, policy.stack_word_count)
    if incoming.sp % 8:
        raise CallContractError('incoming SP is not eight-byte aligned')
    if (service_entry.pc, service_entry.mode) != (policy.service_address, policy.service_mode):
        raise CallContractError('service target or instruction mode changed')
    if service_entry.sp != incoming.sp:
        raise CallContractError('service-entry SP changed')
    if service_entry.lr != incoming.lr:
        raise CallContractError('service-entry return address changed')
    if service_entry.registers != incoming.registers:
        raise CallContractError('service-entry registers changed')
    if service_entry.stack_words != incoming.stack_words:
        raise CallContractError('service-entry caller stack changed')
    if policy.preserve_entry_flags and service_entry.flags != incoming.flags:
        raise CallContractError('service-entry flags changed')
    for state in helper_entries:
        if state.sp % 8:
            raise CallContractError('helper-entry SP is not eight-byte aligned')
    return_mode = 'thumb' if incoming.lr & 1 else 'arm'
    if (reference_return.pc, reference_return.mode) != (incoming.lr & ~1, return_mode):
        raise CallContractError('reference did not return to original caller')
    if (reference_return.sp != incoming.sp
            or reference_return.registers[4:12] != incoming.registers[4:12]):
        raise CallContractError('reference violates caller preservation')
    if wrapper_return != reference_return:
        raise CallContractError('wrapper return differs from reference service')
    return CallContractReport(policy.stack_word_count, len(helper_entries), policy.preserve_entry_flags)
