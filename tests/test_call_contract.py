"""Invented operation traces, addresses and values; no firmware instructions."""

from dataclasses import replace
import unittest

from nikon_z30_research.call_contract import (
    CallContractError, CallPolicy, CallState, check_call_contract,
)


POLICY = CallPolicy(0x5000, 'thumb', 3)


class ToyMachine:
    """Small abstract save/restore/call model, not an ARM emulator."""

    def __init__(self, lr=0x9001):
        self.regs = list(range(101, 114)) + [0x8000, lr]
        self.pc, self.mode, self.flags = 0x3000, 'thumb', 6
        self.memory = {0x8000 + 4 * i: value for i, value in enumerate((301, 407, 509))}
        self.helpers = []

    def snapshot(self):
        sp = self.regs[13]
        return CallState(tuple(self.regs[:13]), sp, self.regs[14], self.pc,
                         self.mode, self.flags, tuple(self.memory[sp + 4 * i] for i in range(3)))

    def save(self, registers):
        self.regs[13] -= 4 * len(registers)
        for index, register in enumerate(registers):
            self.memory[self.regs[13] + 4 * index] = self.regs[register]

    def restore(self, registers):
        for index, register in enumerate(registers):
            value = self.memory[self.regs[13] + 4 * index]
            if register == 15:
                self.pc, self.mode = value & ~1, 'thumb' if value & 1 else 'arm'
            else:
                self.regs[register] = value
        self.regs[13] += 4 * len(registers)

    def side_effect(self, enabled):
        if enabled:
            self.regs[14], self.pc = 0x3201, 0x6000
            self.helpers.append(self.snapshot())
            for register in (0, 1, 2, 3, 12):
                self.regs[register] = 800 + register
            self.flags = 9
            self.pc = self.regs[14] & ~1
        else:
            self.regs[2], self.flags = 0, 4

    def service(self):
        self.pc, self.mode = POLICY.service_address, POLICY.service_mode
        entry = self.snapshot()
        # Make both register and stack arguments observable in the result.
        self.regs[0] = sum(self.regs[:4]) + self.memory[self.regs[13]]
        self.regs[1], self.regs[2], self.regs[3], self.regs[12] = 17, 19, 23, 29
        self.flags = 11
        self.pc = self.regs[14] & ~1
        self.mode = 'thumb' if self.regs[14] & 1 else 'arm'
        return entry


def trace(*, enabled=True, lr=0x9001, legacy=False, missing_register=None):
    machine = ToyMachine(lr)
    incoming = machine.snapshot()
    reference = ToyMachine(lr)
    reference.service()
    # An independently invented full save/restore, then transparent tail transfer.
    saved = (0, 1, 2, 3, 4, 5, 12, 14)
    if missing_register is not None:
        saved = tuple(6 if r == missing_register else r for r in saved)
    machine.save(saved)
    machine.side_effect(enabled)
    if legacy:
        machine.restore(saved[:-1])
        machine.regs[14] = 0x3401
        entry = machine.service()
        machine.restore((15,))
        # LR is call-clobbered; choose the reference value to isolate the SP bug.
        machine.regs[14] = reference.regs[14]
    else:
        machine.restore(saved)
        entry = machine.service()
    return incoming, entry, reference.snapshot(), machine.snapshot(), tuple(machine.helpers)


class CallContractTests(unittest.TestCase):
    def check(self, states, **kwargs):
        incoming, entry, reference, returned, helpers = states
        return check_call_contract(incoming, entry, reference, returned,
                                   policy=kwargs.pop('policy', POLICY),
                                   helper_entries=kwargs.pop('helper_entries', helpers), **kwargs)

    def test_tail_transfer_preserves_arguments_stack_and_both_return_modes(self):
        for enabled in (False, True):
            for lr in (0x9000, 0x9001):
                with self.subTest(enabled=enabled, lr=lr):
                    report = self.check(trace(enabled=enabled, lr=lr))
                    self.assertEqual(report.checked_stack_words, 3)
                    self.assertEqual(report.checked_helper_entries, int(enabled))
                    self.assertEqual(report.scope, 'supplied_call_boundaries_only')

    def test_balanced_final_stack_does_not_hide_service_entry_displacement(self):
        for enabled in (False, True):
            states = trace(enabled=enabled, legacy=True)
            self.assertEqual(states[0].sp, states[3].sp)
            self.assertEqual(states[1].sp, states[0].sp - 4)
            self.assertNotEqual(states[1].stack_words, states[0].stack_words)
            with self.assertRaisesRegex(CallContractError, 'service-entry SP changed'):
                self.check(states)

    def test_argument_and_scratch_register_loss_is_detected(self):
        for register in (0, 1, 2, 3, 12):
            with self.subTest(register=register):
                with self.assertRaisesRegex(CallContractError, 'registers changed'):
                    self.check(trace(missing_register=register))

    def test_aligned_stack_displacement_still_fails(self):
        incoming, entry, reference, returned, helpers = trace()
        with self.assertRaisesRegex(CallContractError, 'service-entry SP changed'):
            self.check((incoming, replace(entry, sp=entry.sp - 8), reference, returned, helpers))

    def test_stack_corruption_without_displacement_fails(self):
        incoming, entry, reference, returned, helpers = trace()
        with self.assertRaisesRegex(CallContractError, 'caller stack changed'):
            self.check((incoming, replace(entry, stack_words=(999, 407, 509)), reference, returned, helpers))

    def test_wrong_target_mode_and_return_address_fail(self):
        states = trace()
        for changes, message in (({'pc': 0x5004}, 'target'), ({'mode': 'arm'}, 'target'),
                                 ({'lr': 0x3401}, 'return address')):
            with self.subTest(changes=changes):
                with self.assertRaisesRegex(CallContractError, message):
                    self.check((states[0], replace(states[1], **changes), *states[2:]))

    def test_helper_alignment_is_checked_even_if_service_entry_is_correct(self):
        states = trace()
        helper = replace(states[4][0], sp=states[4][0].sp - 4)
        with self.assertRaisesRegex(CallContractError, 'helper-entry SP'):
            self.check(states, helper_entries=(helper,))

    def test_entry_flags_are_explicit_and_return_flags_always_checked(self):
        states = trace()
        self.check(states)
        with self.assertRaisesRegex(CallContractError, 'service-entry flags'):
            self.check(states, policy=replace(POLICY, preserve_entry_flags=True))
        with self.assertRaisesRegex(CallContractError, 'wrapper return'):
            self.check((*states[:3], replace(states[3], flags=0), states[4]))

    def test_return_values_and_callee_saved_corruption_fail(self):
        states = trace()
        for register in (0, 1, 2, 3, 4, 8, 11, 12):
            values = list(states[3].registers)
            values[register] += 1
            with self.subTest(register=register):
                with self.assertRaisesRegex(CallContractError, 'wrapper return'):
                    self.check((*states[:3], replace(states[3], registers=tuple(values)), states[4]))

    def test_wrong_reference_cannot_establish_return_contract(self):
        states = trace()
        for changes in ({'pc': 0x9004}, {'mode': 'arm'}, {'sp': 0x7ff8}):
            with self.subTest(changes=changes):
                with self.assertRaisesRegex(CallContractError, 'reference'):
                    self.check((*states[:2], replace(states[2], **changes), *states[3:]))

    def test_explicit_flag_preservation_can_pass(self):
        states = trace()
        entry = replace(states[1], flags=states[0].flags)
        report = self.check((states[0], entry, *states[2:]),
                            policy=replace(POLICY, preserve_entry_flags=True))
        self.assertTrue(report.entry_flags_checked)

    def test_service_stack_outputs_are_compared_to_reference(self):
        states = trace()
        reference = replace(states[2], stack_words=(601, 607, 613))
        self.check((*states[:2], reference, reference, states[4]))
        with self.assertRaisesRegex(CallContractError, 'wrapper return'):
            self.check((*states[:2], reference, states[3], states[4]))

    def test_shared_bad_reference_and_return_cannot_hide_callee_saved_loss(self):
        states = trace()
        registers = list(states[2].registers)
        registers[4] = 999
        bad = replace(states[2], registers=tuple(registers))
        with self.assertRaisesRegex(CallContractError, 'reference violates caller preservation'):
            self.check((*states[:2], bad, bad, states[4]))

    def test_malformed_states_and_policy_are_rejected(self):
        states = trace()
        for changes in ({'registers': (1,)}, {'registers': (False,) * 13}, {'sp': True},
                        {'pc': 0x5001}, {'flags': 16}, {'stack_words': ()},
                        {'stack_words': [301, 407, 509]}, {'mode': 'other'},
                        {'sp': (1 << 32) - 4}):
            with self.subTest(changes=changes):
                with self.assertRaises(CallContractError):
                    self.check((replace(states[0], **changes), *states[1:]))
        for policy in (None, replace(POLICY, stack_word_count=0),
                       replace(POLICY, stack_word_count=True), replace(POLICY, service_address=0x5001),
                       replace(POLICY, preserve_entry_flags=1)):
            with self.subTest(policy=policy):
                with self.assertRaises(CallContractError):
                    self.check(states, policy=policy)
        with self.assertRaises(CallContractError):
            self.check(states, helper_entries=[])


if __name__ == '__main__':
    unittest.main()
