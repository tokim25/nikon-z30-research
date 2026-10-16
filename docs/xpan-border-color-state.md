# A persistent color input for stock border drawing

Date: 2026-10-16. Static analysis and three offline simulator runs.

Native setter `0x104540ee` stores its second argument as a retention flag at
`0xc1820134` and its first argument as color at `0xc1820138`. The refresh
builder copies a nonzero color into request `+0x168`. With retention zero,
it then clears the stored color; nonzero retention leaves it available.

The reviewed chain carries that value into render-context `+0x44`, then the
fifth argument of producer `0x103c1b54`, and into rectangle request color
`+0x10`. The setter is a fully read leaf routine, not a guessed callback.

| Diagnostic setting | First explicit refresh | Second explicit refresh |
| --- | --- | --- |
| Synthetic white, retention 1 | White stored and passed to producer | White still stored and passed |
| Synthetic white, retention 0 | White passed; stored color becomes zero | Zero passed |

The retention-1 result was independently repeated. Every run restored the
original two-word state, preserved the module hash and left the pinned
simulator checkout clean. Confidence is high for the selected data flow and
observed two-refresh behavior. Longer operation and other modes were not tested.

This does not show visible guides. The baseline border extents are still zero,
and no new geometry was supplied in these tests. A persistent color property
does not establish persistent drawing, a safe new object, or debugger-free
startup. The earlier observation of zero-colored border requests describes
the tested state; color is not hard-coded to zero on this reviewed path.

## Reproduce privately

Use confirmed WORK and fresh output directories:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex-guide-border-color-verify-private.py" \
  --output "$WORK/private-inputs/codex-border-color-reproduce-01"
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex-guide-border-color-observe-private.py" --retention 1 \
  --output "$WORK/private-inputs/codex-border-color-reproduce-02"
```

Repeat the second command with `--retention 0` and another fresh directory
for the one-shot control. Successful runs include
`codex-guide-border-color-observation-01`,
`codex-guide-border-color-observation-one-shot-02` and independent
`codex-root-border-color-run-20261016-01`. Logs and memory remain private.

Next: establish the matching clip-geometry ownership and whether the stock
border commands survive composition. No firmware instruction was changed.

Written by Codex in collaboration with Tony Kim; native color behavior independently repeated by Codex agents.
