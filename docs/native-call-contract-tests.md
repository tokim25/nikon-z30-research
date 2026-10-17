# Synthetic state-wrapper call contract

2026-10-17. F-145. Newly written `call_contract.py` checks supplied boundary
snapshots. `test_call_contract.py` exercises it with an abstract operation
model using invented addresses and values. No firmware inputs, encoded
instructions, private overlays, debugger or device connection are used.

This implements the next contract test from
[the existing-overlay review](native-xpan-contract-review.md), F-144.
It does not approve an actual wrapper implementation or build-gate condition 3.

## Required behavior

The proposed abstract wrapper saves the state that added work may disturb,
performs that work on an aligned temporary frame, restores the full incoming
state, and tail-transfers to the original service. Its frame and saved return
address are removed before service entry. The stock service then returns
directly to the original caller. No post-service wrapper return is needed.

The checker requires:

- The reviewed service address and ARM/Thumb mode.
- Incoming r0-r12, SP, LR and the bounded caller stack view at service entry.
- Eight-byte-aligned incoming SP and every supplied helper-entry SP.
- Entry condition flags when explicitly required by policy.
- A reference return to the original caller with its instruction mode,
  restored SP and preserved r4-r11.
- Complete wrapper/reference return equality, including service results,
  flags, LR, stack view and return target/mode.

Preserving r0-r12 is deliberately conservative here because the complete
native service argument contract has not been established. The stack view
has a required explicit size; passing a short or empty view fails. It is
still a bounded view, not proof about all memory.

Entry flags are an explicit policy choice. The abstract helper changes them;
the normal policy does not claim entry flag preservation. A stricter policy
rejects that trace until the supplied entry evidence also preserves flags.
Return flags always match the independently obtained reference.

## Tests and observations

The test model provides abstract save, restore, helper call and service
transfer operations. It is not an ARM emulator and produces no machine code.
The helper overwrites volatile registers, LR and flags; the invented service
uses both register and stack arguments and produces distinct return values.
The unwrapped reference service starts separately on the original inputs.

Fourteen tests cover both added-work branches, ARM and Thumb caller returns,
argument/scratch-register loss, caller stack corruption, wrong target/mode/LR,
helper misalignment, flag policies, return corruption and malformed input.
Negative cases include an aligned eight-byte stack displacement and the
four-byte residual-frame pattern whose final SP is balanced. Both fail at
service entry. Separate cases check that reference/return agreement cannot
hide a broken callee-save contract, and that legitimate reference service
stack outputs must be preserved on return.

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -p 'test_call_contract.py' -v
PYTHONPATH=src python3 -B -O -m unittest discover -s tests -p 'test_call_contract.py' -v
```

## Evidence boundary and next step

The report explicitly scopes itself to `supplied_call_boundaries_only`.
A caller could supply fabricated snapshots or omit helper entries. These
checks do not establish that a machine-code implementation generated the
evidence, executed the helpers, fits a cave, or preserves state between
boundaries. No instruction decoding, branch encoding, memory protection,
interrupt/lock context or natural feature lifecycle is modeled here.

Single next step: read-only mapping of this abstract contract to a private
instruction-layout proposal, checking actual instruction forms, frame size,
literal placement, branch reach and available insertion space. No new overlay
or camera build is authorized by these synthetic results. An actual private
implementation would need instruction review and execution evidence tied to
its exact bytes before this contract could support its acceptance.

F-144's existing overlays remain rejected on the service-entry stack
contract. Native digest input, saved crop, natural transitions and recovery
remain open. Hardware remains NO-GO.
