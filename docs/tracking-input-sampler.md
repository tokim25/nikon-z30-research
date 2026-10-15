# Bounded MMIO sampling lead

Reviewed 2026-10-15. Static analysis only; no guest control calls or hardware.

Candidate routines at `0x1029d8aa` and `0x1029d8ea` read a byte from
`0x2016c010`. Their bounded control flow supports a single-bit output and a
four-bit output. Their callers, device purpose and connection to live-view
input remain unknown. Neither address is a verified tracking entry point.

## Source lead and failed hypotheses

The clean simulator checkout was at revision
`0ba0c3547ccbec09e7c861eaca35db8e82795f15`. Its
[MMIO source](https://github.com/WonderLantern/z30-qemu/blob/0ba0c3547ccbec09e7c861eaca35db8e82795f15/qemu/nikon-z30-display.c#L3031-L3036)
returns zero for recovery-profile byte reads at `0x2016c010`. That is observed
source behavior, not a measured external input. The accompanying comment
labels the all-low value an unmeasured hypothesis.

The comment attributes bit sampling to `0x102595de` and `0x1025961e`.
Bounded decoding at those addresses in the verified module did not reproduce
the stated sampling sequence. Adding `0x20000` did not repair the attribution:
the resulting windows contained byte reads but did not establish the claimed
MMIO sampling. Both address hypotheses failed. The cause of the comment's
address discrepancy remains unknown; no simulator source was changed.

Searching for the MMIO base constant, then checking bounded PC-relative
references to it, supplied the independent landmarks below. The search was
limited to the confirmed private module. It was not a search for new firmware.

## Static observations and interpretation

The module is 33,939,514 bytes, mapped at `0x10020000`, with SHA-256
`8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
The hash and size were checked before analysis. Capstone 5.0.6 decoded Thumb
instructions. Detailed decode output stays outside this repository.

| Landmark | Observed in bounded static decode | Interpretation and confidence |
| --- | --- | --- |
| `0x1029d8aa`–`0x1029d8e9` | A stack-save start, preservation of the incoming second argument as a destination, a PC-relative load at `0x1029d8c2` through `0x1029dbbc`, addition of 16, and a byte read at `0x1029d8c6`. The literal value is the MMIO base `0x2016c000`. | High confidence in a byte read from `0x2016c010` within this window. Reachability from stock live view is unverified. |
| Same window | The sampled byte is shifted left by 30; sign-dependent branches choose zero or one and store a byte through the preserved destination. | Static inference, high confidence: destination byte represents sampled bit 1. No button identity follows. |
| `0x1029d8ea`–`0x1029d94f` | The incoming second argument is preserved as a destination. A PC-relative load at `0x1029d902` uses the same literal, adds 16 and reads a byte at `0x1029d906`. | High confidence in another byte read from `0x2016c010`. |
| Same window | Shifts by 27, 26, 25 and 24 feed sign-dependent branches. The destination is cleared, then conditionally receives output bits 0–3. | Static inference, high confidence: sampled bits 4–7 form the destination's low nibble. Device and input semantics remain unknown. |

The windows also call helpers before and after sampling. Their contracts,
locking requirements, side effects and error handling have not been established.
The stack-save starts and adjacent tail branches support candidate routine
boundaries; a full control-flow graph and all incoming references have not been
reconstructed. No address in this report is approved for a diagnostic call.

The existing GUI limitation was rechecked in source: its live-view worker
refreshes instead of passing a key event, the HTTP input allowlist accepts only
`refresh` in live-view mode, and page construction disables keyboard forwarding.
The menu route's `0x103ce96e` therefore supplies no demonstrated connection to
these samplers. This is source inspection, not a browser or guest execution test.

## Reproduce privately

Use the owner-confirmed workspace. The verifier is newly written research
code, not recovered code. It checks identity and bounded decode structure,
creates a new output directory and keeps detailed output private. Choose a
fresh `codex-` output name on each run.

```sh
WORK=/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work
"$WORK/analysis-env/bin/python" "$WORK/codex_input_sampler_verify_private.py" \
  --output "$WORK/private-inputs/codex-input-sampler-review-01"
git -C "$WORK/z30-qemu" rev-parse HEAD
git -C "$WORK/z30-qemu" status --porcelain
```

The reproduction depends on private files confirmed by the owner; it is not
self-contained CI evidence. Do not upload the verifier's raw decode or private
run folders. The reported run used `codex-input-sampler-verified-01`; all bounded
checks passed. The simulator checkout remained clean. No simulator was started,
no firmware instruction was changed, and no restricted artifact was added here.

## Single next step

Trace static callers of `0x1029d8aa` and `0x1029d8ea` and identify their output
consumers. Establish the peripheral's purpose before calling either a button
sampler or a live-view route. Tracking activation remains unverified.

Written by Codex in collaboration with Tony Kim, with source review by Codex subagents.
