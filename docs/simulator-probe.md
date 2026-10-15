# Repeatable stock-display probe

This original wrapper runs a bounded diagnostic experiment against the separately
obtained, reviewed WonderLantern simulator. It neither decodes firmware nor
generates patches. It does execute original firmware inside the simulator;
the synthetic unit tests do not.

## Prerequisites

- A clean checkout of WonderLantern/z30-qemu at
  `0ba0c3547ccbec09e7c861eaca35db8e82795f15`, outside this repository.
- Its locally built simulator and `.local/build-manifest.json`. Follow the
  [pinned build instructions](https://github.com/WonderLantern/z30-qemu/tree/0ba0c3547ccbec09e7c861eaca35db8e82795f15).
  The wrapper checks the binary and source hashes against that local manifest;
  this is a consistency check, not independent binary authentication.
- The original verified C1.20 extracted EG module, kept outside this repository.
  The wrapper rejects any other size or digest. Obtain this only through the
  separately reviewed local recovery workflow; no firmware is distributed here.
- Permission for the simulator's loopback-only debugger connection. No camera
  connection, SD device, patched image, or host-version override is used.

## Run

From the repository root, substitute absolute paths to private local inputs:

```sh
PYTHONPATH=src python3 -m nikon_z30_research.simulator_probe \
  --simulator /absolute/private/z30-qemu \
  --firmware /absolute/private/eg2090_0120a0.bi \
  --output /absolute/private/new-run-directory \
  --profile worker
```

The output directory must not exist and must be outside both repositories.
Inherited `Z30_` environment switches are rejected to prevent accidental
variation in diagnostic fixtures. The reviewed simulator still supplies its
explicit live-view startup fixtures and synthetic color bars.

Profiles `refresh`, `worker`, and `render` observe different bounded sets of
known addresses while requesting the same stock refresh. They do not invoke
those observed addresses directly or replace guest instructions. Hardware
breakpoints and diagnostic argument registers are simulator interventions;
this is not passive boot evidence.

## Interpret results

Raw upstream audits include registers and memory-derived fields. Frames include
native firmware graphics. **Keep the entire output directory private and out
of Git, issues, and release attachments.** Review a prose summary separately.

`summary.json` records observed addresses, completed-call status, unchanged
input identity, and a frame hash. An empty observation list is not success for
an expected branch. A frame hash does not measure correctness or stability:
the scene contains moving color bars, so whole-frame equality is not a valid
guide-cleanup criterion.

Feature and hardware-readiness fields intentionally stay false/unestablished.
A stock refresh cannot prove native XPan guides, tracking, or coexistence.

Tests cover private-path boundaries (including symbolic links), output reuse,
and honest summary semantics with synthetic inputs only. They are separate
from the manually run simulator experiment and need no firmware in CI.
