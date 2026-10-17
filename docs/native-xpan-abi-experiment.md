# Corrected-wrapper pinned-QEMU experiment

2026-10-17. F-147. Disposable private loader overlays and diagnostic calls in
the pinned simulator only. Original EG and the simulator checkout remained
unchanged. No camera, installable package or combined firmware image was used.

The stack correction works at the measured service boundary, but the proposed
wrapper **does not pass the full F-145 contract**: the other-screen branch
returns different condition flags. Build-gate condition 3 remains open.

## Exact input and final instructions

The experimental overlay implements F-146's layout and retains the later
revision's close/guard alignment fixes. It has eleven files; three differ
from that earlier revision: state wrapper, relocated writer wrapper and writer
hook. Each file is hashed, checked before loading and compared with simulated
memory before CPU startup. The private manifest identity for the final paired
run is
`9dd7b2453fa81c86a914d053303f9efc609295b8721b0fce3f9757fa227b549d`.

Final code sections decoded completely. All six changed/proposed branch
targets matched the reviewed addresses, including the writer relocation.
The state save and restore lists agree, the stock-service transfer is a tail
branch, and the writer replays the original return instruction. Overlay spans
do not overlap and remain within verified EG payload bounds. Concrete bytes,
scripts, manifests, register/stack captures and output remain private.

## Paired fixture

The final `03` run uses separate baseline and corrected simulator processes.
Both use pinned revision `0ba0c3547ccbec09e7c861eaca35db8e82795f15` and the
existing assisted startup. A stock 1:1 callback is allowed to settle for two
seconds; the stored area byte is verified as 1 before the state tests.

Calls run at the existing InitTask diagnostic checkpoint with seeded scratch
registers and three invented caller-stack words on an aligned temporary
stack. The test restores the diagnostic task context afterward. Observations
are filtered to the diverted thread and the expected fixture SP, excluding
background service calls. This is deliberately assisted execution, not a
natural startup or physical-input test.

Two earlier fixtures also returned, but were insufficient controls. Direct
writer inputs did not select 1:1; invoking the asynchronous callback without
waiting did not establish a settled choice. They are not bars-on acceptance
evidence. The final paired fixture resolves that ambiguity.

## Observed results

| Case | Result |
| --- | --- |
| Live-view state, stored choice 1 | Original r0-r12, SP, LR and three caller-stack words reach the stock service. Helper entry is aligned. Mask flag becomes 1. F-145 return comparison passes for this fixture. |
| Other-screen state, stored choice 1 | Same service-entry register/stack checks pass. Mask flag becomes 0. Return registers, SP/LR, target/mode and stack match, but NZCV differs: original 8, corrected 6. F-145 rejects the return. |
| Writer with input one | Relocated wrapper, guard and mask helper are reached. Original return-frame contents, r0-r12/SP results, saved return target and caller-stack words match the baseline. Helper entry alignment passes. |
| Writer with input zero | The same frame, result, stack, target and alignment checks pass. Scratch LR and condition flags differ from the baseline; no broad transparency claim is made. |

All eight final paired diagnostic calls completed. These tests read the mask
flag; they do not establish rendered-pixel correctness, saved-file cropping
or natural transition behavior.

The writer's frame needs care: the original function uses part of its saved
r0-r3 slots as working/output data. Comparing its eventual pop against the
initial argument registers would be the wrong reference. The experiment
compares the actual original frame with the corrected frame, verifies its
preserved r4-r8/LR portion and checks that each return consumes the observed
frame. The return PC is correct even when scratch LR differs.

The public call-contract checker was applied without relaxing its flag rule.
Its successful live-view case and rejected other-state case are recorded in
the private comparison report. Process completion and the corrected SP alone
are not acceptance of the entire wrapper.

## Reproduction and next step

The helpers are newly written, private simulator experiment tools:

```sh
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-xpan-abi-experiment-private.py" --tag 04
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-xpan-abi-compare-private.py" --tag 04
```

Use a fresh numeric tag; existing outputs are never overwritten. New runs
must be judged on their actual comparison results, not assumed to reproduce
the final `03` case's coincident live-view flag equality. No simulated updater
or flash worker is called by these tools.

Single next step: develop a flags-preserving simulator-only remediation,
checking its insertion-space and branch consequences before execution, then
repeat the strict baseline comparison on both state branches and the writer
return. Do not weaken the checker to turn the observed mismatch into a pass.

Condition 1's natural lifecycle gap, native package digest input, actual saved
RAW/JPEG crop and recovery remain open. Hardware remains NO-GO.
