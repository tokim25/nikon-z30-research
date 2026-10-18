# Flag-preserving wrapper: bounded simulator result

2026-10-17. F-148. Private disposable overlay and paired pinned-QEMU runs.
This corrects the measured F-147 flag mismatch. No camera, updater, combined
firmware image or installation package was used.

Both state branches now pass the unchanged F-145 call checker, with entry
flag preservation additionally required. Writer return flags also match the
stock baseline. This is acceptance of these measured diagnostic contracts,
not global build-gate condition 3 or natural-lifecycle acceptance.

## Implementation and review scope

The state wrapper saves application status before its added comparisons and
restores NZCVQ before restoring registers and tail-transferring to the stock
service. The guard likewise preserves application status around its added
work, covering the writer, ready and close callers that share it.

The revision uses only the previously checked insertion spans. The state
routine including its two literals uses 48 bytes; the guard uses 32; the
writer uses eight. Moving the writer into unused live-ready-span capacity
and moving the guard's selector literal into the state span's last four
bytes accommodates the added instructions. Those regions now have no spare
capacity. Concrete layout, instructions and bytes remain private.

All changed/proposed code sections decoded completely. Ten resolved branches,
four status-transfer instructions, the full state save/restore register lists
and all three affected literal loads passed final checks. Insertion spans
were rechecked against the hash-verified original. Twelve overlay files are
individually hashed and matched against simulated memory before startup.
The private experiment manifest SHA-256 is
`5a933892e98effb0ba114adc1ad0e3a4be40daf2cac021df73e8bc1661ef37c9`.

## Paired results

Baseline and corrected processes use the same pinned simulator revision and
settled stock 1:1 callback fixture as F-147. Three invented caller-stack words
and seeded scratch registers make argument/stack corruption observable.

| Case | Observed result |
| --- | --- |
| Live-view state, choice 1 | Service-entry registers, SP/LR, caller stack and NZCV match; complete return registers/CPSR and stack match the original. Strict contract passes. Mask flag is 1. |
| Other-screen state, choice 1 | The same strict checks pass. Original and corrected return NZCV are both 8, resolving F-147's 8-versus-6 mismatch. Mask flag is 0. |
| Writer input one | Original working frame, r0-r12, SP, return PC/mode, full return CPSR and caller stack match. Relocated wrapper reached. |
| Writer input zero | The same writer checks pass, including the condition flags that differed in F-147. |

All eight paired calls completed. Writer scratch LR still differs from the
baseline. It is distinct from the saved return address consumed by the stock
pop: that frame word, actual return target and mode match. This residual is
reported rather than silently excluded from a claim of full transparency.
Writer tests compare the actual stock working frame, not untouched initial
argument slots; the original function changes some of those slots itself.

The state checker was strengthened with `preserve_entry_flags=True`; its
return equality requirement was not relaxed. The writer comparison checks
the complete return CPSR against the baseline. Its comparison of NZCVQ at
the hook versus return accounts for the expected Thumb-to-ARM mode change.

## Limits and reproduction

These are finite diagnostic cases, with assisted startup and debugger-seeded
calling contexts. They do not cover every input flag pattern, concurrent
entry, interrupt/lock context, every guard outcome or a natural menu return.
Mask flags were read; rendered pixels and saved RAW/JPEG were not tested.
Shared guard flag preservation for ready/close paths was reviewed statically,
not separately executed through every lifecycle path in this experiment.
Original firmware and the pinned simulator checkout remain unchanged.

Newly written private tools, with a fresh numeric tag:

```sh
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-xpan-flags-experiment-private.py" --tag 02
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-xpan-flags-compare-private.py" --tag 02
```

The recorded passing paired run is tag `01`; existing outputs are never
overwritten. No firmware or concrete patch material enters the repository.

The measured stack/flag defects are resolved in this prototype. Return to
the saved-crop user stories next: identify a real RAW/JPEG output path or an
evidence-backed patch decision. Native package digest input, natural feature
lifecycle and recovery remain separate gaps. Hardware remains NO-GO.
