# Compose completion is too late for the current guide flush

Date: 2026-10-15. Bounded static analysis and simulator observation.

The selected stock path submits compose job `0x42010019` through adapter
`0x10478f5e`. Dispatcher `0x103bbfac` routes it through `0x103bc1d6` and
`0x103bc4d8` to compose `0x104787f2`. Only after compose returns does the
dispatcher invoke the job's completion callback, `0x10476ea2`, which signals
through `0x10199e04`. That callback cannot insert guides before this compose's
flush. This rejects one candidate hook; it does not exclude other hooks.

Gate helper `0x103bc388` reads a signed 16-bit value at `0xc1808744`.
Zero selects direct compose; nonzero selects the queued path. A passive run
saw eight compose entries alternating preview/UI layers, all with caller
`0x103bc55b` and gate 177. Debugger thread IDs varied and do not identify
native task ownership. Confidence is high for the bounded links and counts.

One additional stock-refresh observation saw producer `0x103c1b54` once,
compose submission twice and compose twice. Candidate object callback
`0x103c3500` had zero hits. Its lifetime-related interpretation remains an
unverified lead, not a usable drawing interface.

Private repro, confirmed WORK and fresh output directories:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex-guide-worker-verify-private.py" \
  --output "$WORK/private-inputs/codex-guide-worker-reproduce-01"
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex-guide-passive-worker-private.py" \
  --output "$WORK/private-inputs/codex-guide-passive-reproduce-01"
```

Independent verification: `codex-guide-worker-root-01` and
`codex-guide-worker-review-input-01`. No firmware changes or new drawing
calls; original hash unchanged and simulator checkout clean. All raw evidence
remains private. Next: trace draw submissions before composition and establish
any callback's ownership/scheduling contract. No debugger-free hook is verified.

Written by Codex in collaboration with Tony Kim; independently reviewed by Codex agents.
