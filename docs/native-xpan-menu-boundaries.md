# Stills menu-confirmation boundaries

2026-10-17. F-157. Bounded follow-up to
[the stills controls](native-xpan-stills-controls.md), using the exact F-148
private overlay. No overlay encoding or hook was changed.

## Observed results

| Run | Confirmation | Boundary evidence |
| --- | --- | --- |
| Stock, coarse observations | Returned | Writer changes image-area choice from 0 to 1 |
| Candidate, same coarse observations plus overlay entries | Unexpected stop | Reaches writer wrapper and guard; mask not reached |
| Candidate, finer observations | Returned | Guard skips mask with stack count 3 and returns through original caller |

The stock and first candidate have identical r0–r15/CPSR and ten stack words
at the original writer return boundary, `0x1008d3fe`. The choice is already
1 at that point in both. No state/close/live-ready hook is observed during
these confirmation calls.

The unsuccessful candidate stops with debugger reply `T02thread:01;`, not
a deadline timeout. Its device log identifies an unmodeled simulated flash
write at `0x10000aaa`, with execution stopped at `0xc2b1065c`. The two earlier
F-156 candidate failures have the same stop PC and are also not timeouts.
This corrects the interpretation of “hung”: the diagnostic call failed to
return because the simulator stopped. It does not identify why this path
was reached or establish that the firmware itself deadlocked.

In the finer candidate trace, the native count getter returns 3. The guard
skips mask application, preserves NZCVQ, restores its frame and reaches the
writer's original caller at `0x1008a14a`. Returned r0–r8 match the native
working frame; SP advances by its original 40 bytes and the saved return
target matches. Scratch LR differs, as already recorded in F-148. This
trace adds real menu-call evidence to those earlier diagnostic ABI checks;
it does not certify the whole caller chain or scratch LR's later liveness.

The finer observation set also stops in the shared count routine on the
other virtual CPU. Breakpoint stepping changes execution scheduling. One
successful finer trace cannot establish a fix, eliminate a patch defect,
or prove which observation changed the result. No guard bypass, arbitrary
register repair or simulated device response was introduced.

## Build decision and bounded next step

Keep menu acceptance open. The mask is not called in either candidate
confirmation trace, so these observations do not implicate mask drawing.
Do not rewrite the guard or dismiss the failure as simulator fidelity on
this evidence alone.

Next bounded control: repeat the coarse stock/candidate comparison with
only the writer-branch redirection omitted from the candidate loader
manifest. Preserve every other overlay and all observation/input settings.
This tests whether this added writer path is necessary for the observed
stop and informs whether that hook should remain in the stills build.
A mixed result remains inconclusive; do not start an open-ended flash-device
model investigation. Movie transitions and saved-crop tracing remain outside
this experiment.

## Private reproduction and limits

WORK helper: `codex-xpan-menu-boundary-private.py`, modes `stock` and
`candidate`, numeric tags, `--detail coarse` or `--detail fine`. Tag 01 used
the coarse observations; candidate tag 02 adds post-getter, guard-return
and original-caller observations. Exact point sets are retained in each
private session audit. Reports: `codex-xpan-menu-boundary-stock-01`,
`codex-xpan-menu-boundary-candidate-01` and `02`, and
`codex-xpan-menu-boundary-comparison-01.json`.

All overlay files matched the pinned manifest before loading and loaded
memory matched their hashes. Original firmware and pinned QEMU checkout
remained unchanged. Assisted startup and diagnostic GUI-event injection
remain prerequisites: natural startup/menu-return acceptance is unproved.
All sessions closed. Raw traces, decodes and frames remain outside Git;
no image, publication or camera access. Hardware remains NO-GO.

## Writer-hook isolation control, F-158

The owner approved exactly one control: omit only the writer-branch
redirection, preserving the eleven other F-148 overlay entries, pinned
simulator, nine coarse candidate observation points, assisted startup,
navigation inputs, timing requests and zero requested repeat cycles.
The original writer instruction was verified in loaded memory; retained
overlays matched their hashes. This changed loader selection only, with no
patch encoding or production-candidate modification.

Control loader manifest SHA-256:
`76e12866fd9f018412d72b09613c9642a685ba0da6e57171a2ad6e0810108c9e`.
Reference F-148 manifest SHA-256:
`5a933892e98effb0ba114adc1ad0e3a4be40daf2cac021df73e8bc1661ef37c9`.

The confirmation still failed to return: `T02thread:01;`, PC
`0xc2b1065c`, and the same unmodeled simulated flash write at
`0x10000aaa`. The writer boundary was reached once with choice 1 and
registers/CPSR/ten stack words equal to the prior stock boundary. Neither
the added writer wrapper nor guard was observed during confirmation.

The menu mask remained off: flag 0 before confirmation and at both observed
writer boundaries, with screen-stack count 3. This is the expected menu
exclusion state. Confirmation failure prevented the existing subsequent
diagnostic live activation, so this control does **not** establish post-menu
bars correctness. Extra read-only pixel snapshots were startup refreshes;
their private stage labels were corrected accordingly. F-156's separate
callback-rendering result remains unchanged, not extended by this test.

Comparison: stock/coarse returned; candidate/coarse and writer-disabled/
coarse both stopped at the same simulated access; candidate/fine returned.
The writer redirection is therefore not necessary for this observed stop.
This single control does not establish another hook as the cause, explain
the mixed instrumentation result, or certify a writer-disabled feature build.

Decision: removing the writer hook is not an established remedy. Leave the
patch unchanged and menu acceptance open. Stop this checkpoint here; no
additional control, lifecycle expansion or flash-model investigation was
performed. Further work needs a separately selected bounded decision.

Private reproduction: helper `codex-xpan-menu-boundary-private.py`,
`--mode writer-disabled --detail coarse --tag 01`; evidence directory
`codex-xpan-menu-boundary-writer-disabled-01`, including
`isolation-result.json`. Loader metadata is in
`codex-xpan-writer-disabled-loader-01`; all raw evidence stays private.
Original firmware and pinned QEMU checkout remained unchanged; session
closed. No camera access, commit, push, merge or PR.

## Stop provenance, F-159

A read-only check of the verified original maps the stopped helper at
`0xc2b10656` to a cached flash identity/geometry initializer at
`0xc2b1012c`. The recorded LR in both the coarse candidate and writer-disabled
stop is `0xc2b1013f`, matching that initializer's helper call. After the
helper, the native code reads identity fields, derives capacity/block
geometry and sets its initialized flag. These later instructions were
decoded statically; successful completion was not observed.

The initializer is shared. An information-getter wrapper calls it, and
erase/program wrappers call it before their respective operations. Thus the
stop establishes attempted discovery commands, not an identified payload
erase/program operation. It also does not prove that an update could not
follow: the outer caller is absent from the retained current-stack evidence.
Do not label this a firmware-install attempt, ordinary setting persistence,
or patch-induced control-flow corruption without that missing evidence.

This resolves the local helper's role, not the mixed confirmation result.
Keep the patch unchanged and menu acceptance open. Retire further work on
explaining the simulator's flash response here, per the real-build priority.
The useful next build task is the remaining close/live-ready hook contract
review; the stop does not justify weakening the state/writer ABI checks or
removing an otherwise needed hook.

Private helper `codex-xpan-stop-provenance-private.py` verifies selected
semantic landmarks and the two existing stop contexts, producing
`codex-xpan-stop-provenance-01.json`. It uses F-141's relocated-block mapping
and the pinned original hash. No new simulator run, firmware modification,
device model change or hardware access occurred. Raw decodes remain private.
