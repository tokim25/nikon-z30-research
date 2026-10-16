# An empty screen stack in the assisted live-view fixture

Date: 2026-10-15. Two offline simulator runs, unchanged firmware.

The screen-stack container reached through `0xc181e4f0` had count zero
before startup, after the known assisted live-view startup, and after one
stock refresh. A second run repeated those results, then the existing
audited menu-entry diagnostic populated two entries (screen IDs 1 and
`0x351`). No direction, OK, AE-L/AF-L or tracking event was injected.

Getter `0x1046109a` uses helper `0x10365ff0`: count is at container `+8`,
stride at `+0`, storage at `+0x0c`; count zero returns no slot. The outer
getter then returns no descriptor. Independent static review confirmed this
layout. The menu control supports the observation method; it does not
identify the shooting screen or its key map.

The fixture can render its synthetic preview with this native stack empty.
A preview alone therefore does not establish the screen state needed by
the menu/screen dispatcher. This does not show that an ordinary camera's
live view has an empty stack, or that the separate live-view worker cannot
process input. Confidence is high for measured counts and bounded getter
behavior, moderate for generalizing to this fixture. Other startup paths
were not tested.

## Reproduce privately

Use confirmed WORK and a fresh directory:

```sh
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex_screen_stack_private.py" \
  --output "$WORK/private-inputs/codex-screen-stack-review-04" --menu-control
```

Runs: `codex-screen-stack-run-02` and `-03`. Independent layout review:
`codex-guide-stack-review-09`. The helper checks original identity, pinned
simulator revision and clean checkout. Detailed memory, logs and frames stay
private; runtime imports disable bytecode writes.

Next: establish stock shooting-screen initialization and its prerequisites
before treating screen-dispatcher events as evidence of tracking activation.

Written by Codex in collaboration with Tony Kim; layout independently checked by a Codex subagent.
