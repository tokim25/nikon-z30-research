# A structure pack is not yet a saved-RAW path

Date: 2026-10-16. Bounded static analysis of the verified module.

Builder `0x101e779c` copies selected halfword fields from source offsets
`+0x208` through `+0x218` into destination `+0x47c` through `+0x48c`.
Caller `0x101ea022` supplies its argument plus `0x1c` as the source and
`0xc233addc` as destination. Later it calls `0x100aa43a`, whose reviewed
path copies 2024 bytes into a per-unit buffer and submits through
`0x100c9f24`.

These are observed selected code/data links, high confidence, independently
checked. The source object has not been connected to the earlier capture
request whose geometry begins near `+0x20a`. Matching offsets alone do not
establish identity or make these fields NEF tags. Complete pointer contracts,
runtime delivery, file serialization and storage writes remain unverified.

The follow-on worker trace led toward hardware-processing configuration,
not verified NEF serialization. It does not show which packed fields reach
particular registers or exclude other save paths. A separate search for
TIFF-like numeric constants failed: reviewed matches were error/UI values,
not proven width/height tag writers.

Private repro, confirmed WORK and fresh directory:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex_agent_geometry_pack_verify_private.py" \
  --output "$WORK/private-inputs/codex-geometry-pack-reproduce-01"
```

Agent run: `codex-agent-geometry-pack-verified-20261016-01`; independent
root repeat: `codex-root-geometry-pack-20261016-01`. The helper verifies
original identity and selected exact instructions/literals, not full control
flow. Worker/interface leads remain private in
`codex-agent-pack-submit-worker-20261016-01` and
`codex-agent-native-output-interface-20261016-01`. No firmware execution,
modification, saved file or hardware was used.

Next: prove source-object identity and the native save boundary before using
this pack as evidence that a crop reaches a RAW file.

Written by Codex in collaboration with Tony Kim; selected structure links independently checked by Codex agents.
