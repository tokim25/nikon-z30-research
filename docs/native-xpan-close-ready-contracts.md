# Close and live-ready hook contracts

2026-10-17. F-160. Bounded static review and four paired diagnostic calls
using stock firmware and the exact F-148 private overlay. All eight calls
returned. No patch modification was needed for these checked contracts.

## Results

| Case | Candidate mask | Checked result |
| --- | ---: | --- |
| Ready, target 1:1 stand-in | 1 | Native inputs, selector result, aligned stack and return checks pass |
| Phase-3 notification, target | 1 | Native callback inputs and return checks pass |
| Ready, DX | 0 | Native inputs, selector result, aligned stack and return checks pass |
| Phase-3 notification, DX | 0 | Native callback inputs and return checks pass |

Each pair uses assisted startup, the stock image-area callback, seeded
diagnostic registers and three invented caller-stack words. The stock
functions are `0x104b9116` and `0x10235560`; the candidate wrappers are
`0x1027f468` and `0x1002d7b4`. Register arguments r0–r12 match at native
function entry. All observed helper stacks are eight-byte aligned. All
calls preserve r4–r11 and the bounded caller-stack words, restore incoming
SP and reach the diagnostic return target/mode. Full return CPSR matches
stock in all four pairs. Ready's original r0 result is preserved.

The runtime-registered live callback is `0x10058dff`, with context 3, in
both processes. It receives the same r0–r12 values in both close cases.
Static review follows its tail transfer to the phase dispatcher: the
phase-3 path builds its own outgoing stack arguments in its own frame,
rather than reading incoming caller-stack arguments.

These wrappers call the stock functions with an eight-byte temporary frame
and remove it on return. For these reviewed register-input routines that
is an aligned normal call. It is distinct from F-145's state-kernel tail
transfer, whose exact incoming caller-stack view must be preserved. That
checker was not relaxed or applied to an incompatible contract.

## Return differences and native continuation

The calls are not identical in every volatile register:

| Case | Differing return registers |
| --- | --- |
| Ready, target | r2, LR |
| Phase 3, target | r0, r1, r2, LR |
| Ready, DX | r1, LR |
| Phase 3, DX | r0, r1, LR |

At the actual ready continuation, `0x102f5814` replaces r1, then replaces
r0 and calls `0x1044e68c`, replacing LR. That callee's first instruction
replaces r2 before reading it. At the actual phase-3 continuation,
`0x102355c4` branches to `0x1023558e`; r2, r1 and r0 are replaced before
the next call replaces LR. The checked differences are therefore not
consumed as inputs by these native continuations. No difference in r3 or
r12 was measured in these cases.

## Acceptance boundary

The bounded contracts pass; retain the existing wrappers. This does not
certify all callbacks registered on other objects, every possible color
helper output, concurrency, all guard outcomes or global build-gate
condition 3. The phase-3 diagnostic is not proof that the whole close/menu
lifecycle cleans up correctly: with an empty screen stack and selector 1,
the guard reapplies the selected mask, as its code specifies.

F-156 retains rendering and repeated-setting evidence. F-157/F-158 still
leave native menu return unresolved. No pixel, saved-file, movie,
power-cycle or physical-camera acceptance was added here. Hardware remains
NO-GO. Further flash-device explanation is retired per F-159; this review
does not reopen it or justify a hook rewrite.

## Private reproduction

Manifest SHA-256:
`5a933892e98effb0ba114adc1ad0e3a4be40daf2cac021df73e8bc1661ef37c9`.
All overlay files matched before loading and their loaded hashes matched.
The original firmware and pinned QEMU checkout remained unchanged.

WORK helper `codex-xpan-close-ready-audit-private.py`, run once each with
`--mode stock --tag 01` and `--mode candidate --tag 01`; comparison helper
`codex-xpan-close-ready-compare-private.py` checks the retained tag-01 pair
and selected original continuation landmarks. Private reports are
`codex-xpan-close-ready-stock-01`, `codex-xpan-close-ready-candidate-01`
and `codex-xpan-close-ready-comparison-01.json`. Both sessions closed.
Raw evidence and concrete overlays stay outside Git. No publication or
hardware access.
