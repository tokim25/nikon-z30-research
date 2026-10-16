# A numeric-command route into the candidate input handler

Date: 2026-10-15. Bounded static analysis, unchanged firmware.

The structured handler containing `0x1008ad26` has a registered route that
parses numeric text. This is not evidence of a physical AE-L/AF-L reader.
Diagnostic purpose is an inference; the incoming transport remains unknown.

Initializer `0x1008ad72`, on its argument-0-equals-3 path, supplies callback
`0x1008ac2e` through registrar `0x101e1c04`, with word limit 4 and flags 0.
The registration code stores callback, limit and flags at slot offsets
`+0x18`, `+0x1c` and `+0x20`. Duplicate/missing-entry branches mean this
does not prove registration succeeds at runtime.

Consumer `0x101e1c22` uses the flags-zero branch to call parser `0x101e230e`
at `0x101e1c62`, then the registered callback at `0x101e1c6c`. Arguments
are the registration key, a parsed-word array and its count. The parser
splits text at spaces, modifies delimiters in its input, and converts tokens
to words. It initializes radix 10 and can select radix 16; the reviewed
loop can retain that radix for later tokens. Numeric validation is not
established. The private registration label is omitted and provides no
independent physical-switch attribution.

These are observed code/data links, high confidence, independently reviewed.
No execution, switch ownership, normal transport or tracking activation was
verified. Other producers of the same input cache are not excluded.

## Reproduce privately

With confirmed WORK and a fresh output directory:

```sh
"$WORK/analysis-env/bin/python" \
  "$WORK/codex-registered-input-verify-private.py" \
  --output "$WORK/private-inputs/codex-registered-input-review-03"
```

Passing root repeat: `codex-registered-input-root-01`; independent full-block
review: `codex-agent-registered-review-01`. The helper checks original identity
and selected relationships; it is not a complete control-flow proof.
All restricted evidence stays outside Git.

Next: inspect independent cache-setter calls at `0x103a3e88` and
`0x103a400c`, outside this numeric handler, for a physical input source.

Written by Codex in collaboration with Tony Kim; independently reviewed by Codex agents.
