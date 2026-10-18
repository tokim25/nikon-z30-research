# AE-L/AF-L tracking control and cycle review

Date: 2026-10-17. Read-only firmware analysis plus a bounded, memory-only
QEMU run of the private tracking candidate. No camera access, firmware image,
or overlay was used.

## Playback Protect separation

The AE-L/AF-L button serves a shooting assignment and the playback Protect
action through separate settings. The candidate's new shooting option stores
77 in assignment `0x1184`; its action adapter requires the shooting context,
mode 0, and that assignment before it can call tracking. It does not change
playback assignment `0x1186`, and other contexts fall through to the stock
handler. Mode-1 setting `0x1187` is outside this candidate's scope. This
resolves the side-control ownership question at the static/menu-routing
level; playback Protect was not exercised in the modified simulator run.

## Start/stop cycle and correction

The earlier cycle fixture manually set the public status pair to `(1, 0)`
before the second action, so it proved the native stop branch but did not
prove that a first request naturally made the next press stop. An unforced
run found the missing synchronization: after the start request, the native
tracking pair at `0xc259ff44` became `(1, 0)`, while the status record read by
the shared helper remained `(0, 0)` through a one-second simulator window.
The next fresh action therefore selected start again. This run had no
physical input or acquired AF target, so it does not show how a real camera's
asynchronous acquisition event will update status.

The native status bridge uses locked setter `0x101925b0` to publish the two
native tracking-pair bytes into the helper's public status record at offsets
`+0x61/+0x62`. The private candidate now calls that same setter after native
completion when the shared helper reports a handled start/stop request. A
bounded candidate-memory QEMU run, without injecting the active status pair,
then produced this sequence:

| Action | Native request reached | Native pair after | Public pair after |
| --- | --- | --- | --- |
| Fresh press from idle | Start `0x100774f4` | `(1, 0)` | `(1, 0)` |
| Held/no-decision record | None | unchanged | unchanged |
| Next fresh press | Stop `0x100775c6` | `(0, 0)` | `(0, 0)` |

The action adapter's decoded frame is now 32 bytes. The maximum additional
simultaneous stack depth is 480 bytes against the candidate's dedicated
1024-byte increment. Assembly/linking and the independent bounded CFG/frame
review passed: 1,000 code bytes, 1,010 occupied bytes including padding,
45 planned spans and 25 checked relocations. No firmware image or overlay
was written.

This closes the **candidate's synthetic request/status cycle** by keeping
the helper's status view synchronized with the native request pair. It does
not prove physical AE-L/AF-L delivery, real AF acquisition, the camera's
asynchronous state transitions, or behavior after native cancellation and
mode changes. The bridge call is not a substitute for a device test. Before
any camera test, still complete the standalone-EG package/integrity contract,
review the updated exact private manifest, and satisfy the project's
readiness and per-step authorization gates. Keep the playback Protect action
and mode-1 assignment unchanged.

Validation performed privately: candidate assembly/link/layout verifier,
independent candidate ABI/frame verifier, and the bounded QEMU cycle
diagnostic. Repository test suite and publication scanners are run before
any PR. Private firmware, source artifacts, and raw diagnostic output remain
outside Git.
