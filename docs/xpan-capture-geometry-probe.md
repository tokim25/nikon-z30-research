# A centered 65:24 capture-geometry result

Date: 2026-10-15. Two offline simulator runs, original firmware file unchanged.

The stock geometry routine `0x101d5b36` returned a centered 5200 by 1920
rectangle after temporary geometry-data changes in the guest. The ratio is
exactly 65:24. This closes the earlier unrun geometry-sensitivity test; it
does not show a captured image, a saved RAW crop or physical-camera support.

## Controlled comparison

Both runs used area 4, large size, mode 0. Five known geometry-data pairs
were changed only inside a disposable simulator process. No firmware
instruction or original file was changed. This is a sufficient tested set,
not proof that every changed pair is necessary.

| Phase | Area size | Area origin | Rectangle coordinates | Derived rectangle size |
| --- | --- | --- | --- | --- |
| Original | 3728 by 3728 | 936, 0 | 8, 8 to 3720, 3720 | 3712 by 3712 |
| Temporary data | 5216 by 1936 | 192, 896 | 8, 8 to 5208, 1928 | 5200 by 1920 |
| Restored | Identical to original | Identical to original | Identical to original | Identical to original |

The surrounding readout remained 5600 by 3728. The changed origin centers
the new area inside that readout. The chosen synthetic dimensions give an
exact ratio with aligned dimensions; they are not a claim about the largest
supported camera crop. DX and 16:9 results stayed identical throughout.

The origin comes from a separate table read through `0x1020c072`; the
geometry function does not infer it from the new dimensions. The test
therefore supplied a matching origin as well as size data. The agreement
with half the readout-minus-area difference in the original baseline was
an observed relationship, not a general arithmetic contract in this routine.

Confidence is high for these observed return values and unchanged controls.
There was no exposure, SD image, NEF output, image-quality check or tracking
test. The simulator's optional functional ISP is not evidence that this
new geometry is supported by the real capture pipeline.

## Reproduce privately

Use the owner-confirmed WORK and a fresh directory:

```sh
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex_agent_geometry_data_probe_private.py" \
  --output "$WORK/private-inputs/codex-geometry-reproduce-01"
```

Successful runs: `codex-agent-raw-geometry-probe-02` and independent
`codex-root-geometry-probe-01`. The helper checks original identity and the
clean pinned simulator, uses a thread-aware call helper, records original /
changed / restored results, and restores the temporary data before closing.
Private run details and the data edit list stay outside Git.

Next: trace the geometry descriptor's consumers into capture/save requests,
NEF dimensions or crop metadata, and storage writes. A geometry return value
alone cannot satisfy the saved-RAW requirement.

Written by Codex in collaboration with Tony Kim; experiment and independent repeat performed by Codex agents.
