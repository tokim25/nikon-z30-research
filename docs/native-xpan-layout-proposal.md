# Corrected state-wrapper layout feasibility

2026-10-17. F-146. Private textual layout review following
[the synthetic call contract](native-call-contract-tests.md), F-145.
No object, replacement overlay, modified firmware or camera package was
created. The proposal and concrete instruction material remain outside Git.

The corrected contract fits the existing 52-byte candidate span together
with its adjacent writer wrapper. This is a layout result; build-gate
condition 3 and the existing-overlay rejection remain open.

## Checked proposal

The proposed state wrapper uses a 32-byte temporary frame to preserve all
argument/scratch registers that its added work may disturb, scratch callee-
saved registers and LR. Both state branches restore that entire frame before
a tail transfer to the original stock service. This removes the saved-LR
word at service entry identified in F-144. The proposed entry-flag policy
remains the explicit non-preserving policy from F-145.

| Item | Reviewed size |
| --- | ---: |
| State wrapper, including alignment and two literals | 40 bytes |
| Adjacent writer wrapper | 8 bytes |
| Combined footprint | 48 bytes |
| Original candidate span | 52 bytes |
| Spare space | 4 bytes |

The state entry stays in place. The writer entry moves four bytes, requiring
its original hook to be retargeted and its own guard call to be re-encoded.
Reusing the old writer address would enter the proposal's literal area.
These dependencies must be included together in any later experimental
overlay; the existing overlays were not changed.

The original span was verified zero again against the pinned EG identity.
F-144's existing-file audit also ran again, preserving its rejected result.
The proposal remains within the checked payload and installation mapping.

## Validation and its limit

Apple clang 21.0.0's integrated assembler accepted fourteen instruction forms
in textual output mode. Captured encoding annotations independently confirmed
the proposed instruction widths, including wide save/restore forms with r12
and LR. Output remained in memory; no object or overlay was emitted to disk.
Six branch distances and two narrow literal displacements passed independent
alignment/range arithmetic. Code/data intervals cover the proposed footprint
without overlaps, and both literals are aligned within the candidate span.

External targets remain symbolic in this textual check. It does not resolve
and inspect final branch encodings or execute the proposed instructions.
Those checks require an actual private experimental overlay. The proposal
does not establish runtime permissions, hidden references, thread/interrupt
context, reentrancy, natural feature transitions or hardware behavior.

An initial assembler no-output experiment with label-width assertions crashed.
The successful check uses textual assembler output and separate layout
arithmetic instead. The crash supplied no acceptance evidence and produced
no object or overlay. The private helper reproduces only the successful path:

```sh
"$WORK/analysis-env/bin/python" -B "$WORK/codex-xpan-layout-proposal-private.py"
```

## Single next step

Test this specific remediation in a throwaway private overlay using only the
pinned QEMU simulator, under AGENTS.md's simulator-only experimentation
exception. Before running it, decode the final instructions and resolved
branches, verify the retargeted writer hook, and bind the evidence to every
overlay file's actual hash. At the stock-service entry, compare registers,
SP/LR, caller stack and return behavior against the unwrapped baseline.
Exercise both state branches and the writer path. This is an ABI-remediation
experiment, not a camera build or natural-lifecycle acceptance result.

No such overlay or run was produced in this review. Missing native digest
input, actual saved crop, natural lifecycle and recovery remain open.
Hardware remains NO-GO.
