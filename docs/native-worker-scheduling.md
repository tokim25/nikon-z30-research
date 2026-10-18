# Lane 0: worker creation and passive scheduling

Date: 2026-10-17. Offline, pinned simulator only; unchanged original firmware.
This answers whether the dormant-worker observations justify changing the
machine model before pursuing natural live-view lifecycle coverage.

## Step 1: the live-view task is created

A reset-to-InitTask trace observed 249 calls to native task wrapper
`0x10219876`, without reaching the observer's 256-hit limit. It constructs
the native task request, calls ARM service stub `0x10035fdc`, and starts
the resulting task through `0x10219870`. Its task trampoline is
`0x1021986c`. This bounded inspection explicitly handles ARM service code;
it does not assume that the image is entirely Thumb.

The trace captured these creation requests, followed by allocated kernel
task records at the first service checkpoint, before diagnostic startup:

| Task | Object argument | Requested task entry | Kernel task record |
| --- | --- | --- | --- |
| APPLV | `0xc1821d44` | `0x10235577` | `0xc2b7a498` |
| APPMENU | `0xc182e688` | `0x10235577` | `0xc2b7a2e8` |
| APP_OBS | `0xc1f923f4` | `0x103577a5` | `0xc2b7a720` |

The kernel record's `+0x0c` field is the argument, not the entry point.
The entry at `+0x14` is the common trampoline. Among the 256 inspected
slots, 254 had nonzero state and two had zero state; preassigned nonzero
IDs alone must not be counted as successful task creation.

The live-view object stores worker pointer `0x102f2ca9` at `+0x40`.
The generic screen task calls that field at `0x102355b4`; the worker's
loop calls payload builder `0x102f2ad2` at `0x102f2cd8`. This connects
the named APPLV task to the actual worker rather than guessing from its name.

**Limit:** the task that produces property events `0x2006`/`0x2087` has
not been identified. APP_OBS exists, but calling it that producer would
be an inference without a verified connection. No missing-worker finding
was established for that route. Its separate property-dispatch research
branch was not changed.

## Step 2: the worker runs without a diagnostic call in flight

After the existing `liveview_session.start` fixture returned, a new
40-second window used `Session.run_to` with observation breakpoints and
an otherwise unused existing ROM address as its timeout target. The
expected timeout was handled as the end of the window. No diagnostic call,
register redirection or debugger state write was in flight during it.

The 40.005-second wall-time window recorded **196 payload-builder entries**:
all had return link `0x102f2cdd`, stack pointer `0xc56e2ff0`, and incoming
flags `0x4`. The observer never reached its limit. These entries are
ordinary iterations inside the running worker, not repeated diagnostic
calls. The worker entry itself need not fire again: its loop branches to
an internal address after the entry prologue.

No observation occurred at the bit-16 type-2 dispatch `0x102f2c0a`,
live-view-ready `0x102f57e2`, dispatcher `0x10459d80`, property
state-machine step `0x10379d5a`, event dispatcher `0x1037aae2`,
`0x2087` handler `0x103a341a`, or shared post primitive `0x10475ecc`.
Flag 4 does not contain the bit 16 that the known live-view-enter branch
tests. This explains that branch's non-execution for the sampled iterations;
it does not establish why the required event signal was absent.

A separate trigger-only 40-second window, omitting the repeated worker
breakpoints, is recorded in the private `codex-lane0-free-rare-01` run.
It completed after 40.004 wall seconds with zero observations and no cap.
The model's 48 MHz counter advanced by approximately 189.959 seconds of
virtual time. There were no breakpoint stops before the timeout interrupt.
This is a longer emulated window as well as a longer host wait; it still
does not prove that every required upstream stimulus was present.

## Step 3: not entered

The worker ran, so the prerequisite for investigating a general scheduler
stall did not hold. No MMIO shortcut was changed and no machine-model C
source was edited. Presence of a GIC or a QEMUTimer is not by itself proof
of scheduler progress; the native worker observations supply that evidence.

There is also a source-selection correction: `Session` initially builds
assisted command arguments but replaces the machine with
`nikon-z30-display`. That machine uses `nikon-z30-display.c`'s recovery/
platform setup, including its GICv1 hypothesis, rather than the separate
`nikon-z30-assisted` implementation in `nikon-z30.c`. Any future device
investigation must start from the actual recorded command and device options.

## Interpretation and next step

Update for PR #155 reconciliation: the next-step proposal below is historical.
The owner subsequently directed against simulator-completeness loops and
recorded lifecycle/guard waivers. Preserve these observations; follow the
current session-manager brief before authorizing any new investigation.

F-019 and F-117 remain valid descriptions of their bounded observations.
They do not establish that APPLV was absent or that the RTOS could not run
it. The stronger common explanation, a globally dormant scheduler, is now
contradicted for this fixture. A missing event or prerequisite is still
possible; it is not yet a confirmed MMIO bug, nor a physical-input finding.

Next: observe the existing live-view event object's signal/wait boundary
and connect the missing bit-16 signal to a real firmware producer, using
the running APPLV context. The target decision is whether the bars can pass
natural live-view/menu lifecycle checks. Do not resume unrelated SD-model
fidelity work or infer property-producer identity from this result.

## Private reproduction and integrity

Use the owner-confirmed WORK directory and a fresh output name:

```sh
"$WORK/analysis-env/bin/python" -B "$WORK/codex-lane0-workers-private.py" \
  creation --name codex-lane0-creation-reproduce
"$WORK/analysis-env/bin/python" -B "$WORK/codex-lane0-workers-private.py" \
  free --name codex-lane0-free-reproduce
"$WORK/analysis-env/bin/python" -B "$WORK/codex-lane0-workers-private.py" \
  free --rare --name codex-lane0-free-rare-reproduce
```

Successful creation trace: `private-inputs/codex-lane0-creation-02`.
Worker trace: `private-inputs/codex-lane0-free-01`. Earlier exploratory
`creation-01` observed an IRQ configuration routine, not task creation;
it is not evidence for the creation conclusion. The corrected trace uses
the verified wrapper and allocated records.

The helper checks the original hash and pinned simulator revision, clean
checkout, binary manifest hash and recorded source hashes before and after
runtime tests. All helpers, task dumps, raw decode, registers, run logs and
images remain under WORK, outside the research repository. No overlay was
generated. These private commands are not self-contained CI evidence.

Publication validation: all 54 repository unit tests, the restricted-artifact
check and the encoded-byte check passed. The full staged prose diff and
publication file list were reviewed; no private helper or raw output is staged.

Confidence: high for the positive task-creation and worker-execution
observations; bounded negative for the listed trigger addresses. Hardware
remains NO-GO. This does not satisfy the complete feature's lifecycle checks
or change build-phase conditions 2 through 4, risk acceptance, or the
requirement for separate owner approval immediately before any hardware step.

Written by Codex in collaboration with Tony Kim.
