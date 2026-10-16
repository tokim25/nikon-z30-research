# What the simulator can establish about RAW processing

Date: 2026-10-15. Source audit at pinned revision
`0ba0c3547ccbec09e7c861eaca35db8e82795f15`.

Earlier notes saying the simulator has no image processor are too broad.
It has an opt-in functional ISP model in `qemu/nikon-z30-isp.h`. The source
explicitly treats pixel layouts and algorithms as hypotheses. It consumes
guest RAW buffers and writes processed NV12-like output; this is not proof
of Nikon processing fidelity or a saved RAW file.

The modeled transaction requires specific control state and an exact traced
RAW geometry. Processed outputs are limited to even dimensions up to 1920
by 1280, with stride no greater than 2048. Unsupported descriptors produce
no completion. These constraints do not prove that 65:24 fails in every
path or on the physical camera. Source presence also does not prove a given
binary/run enabled this model.

SD transport and a snapshot-backed card option exist, but they do not establish
a native NEF serializer. The simulator README places photo/movie recording
outside its supported scope. No saved-RAW capture pipeline was verified.
There is also no basis to claim NEF-writing code is absent from the firmware.

Sources inspected: pinned `qemu/nikon-z30-isp.h`,
`qemu/nikon-z30-display.c`, `tools/run.py` and `README.md`. Confidence is
high for these source-level capabilities and declared limits, not runtime
or hardware behavior.

Private repro, confirmed WORK and fresh output directory:

```sh
python3 "$WORK/codex_agent_raw_model_source_audit_private.py" \
  --output "$WORK/private-inputs/codex-raw-model-reproduce-01"
```

Independent root repeat: `codex-raw-model-root-01`. The helper checks pinned
revision, clean checkout, source hashes and selected patterns. Detailed
evidence remains outside Git. Next: trace native geometry-request consumers
into saved NEF dimensions/crop metadata and storage writes; synthetic raster
output alone cannot satisfy the owner's RAW-crop requirement.

Written by Codex in collaboration with Tony Kim; source audit independently repeated by Codex agents.
