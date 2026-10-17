# Saved-crop restart: initialized table mappings

2026-10-17. F-149. Read-only original-image analysis and RAM reads after the
usual assisted startup of unmodified firmware in the simulator. No crop
patch, capture attempt, updater or camera access occurred.

F-110/F-111 searched the stored ROM addresses of two filename-pointer tables
without finding their consumers. F-141/F-142's startup-copy evidence supplies
a different search target: their initialized RAM addresses. This is a new
bounded search, not a retry of the retired crop-builder caller or SD-model
threads.

## Mapping and runtime cross-check

The checked initialized-data copy maps source `0x11f81c94` to destination
`0xc1800000`, length `0xf8258`. Both pointer tables lie inside that source.

| Stored table | Initialized RAM address | Startup comparison |
| --- | --- | --- |
| F-110 first filename-pointer table, `0x1204d280` | `0xc18cb5ec` | All four pointer words match the initialized source. |
| F-110 second filename-pointer table, `0x1204d440` | `0xc18cb7ac` | All four pointer words match the initialized source. |
| F-112 geometry header | `0xc18c7de8` | All eight checked words match the initialized source. |

These 64 bytes were compared in private; no table contents or byte excerpts
are reproduced here. This verifies these particular mappings after assisted
startup, not all initialized data or later mutation behavior.

## References found, with limits

A full-image aligned-word search for each RAM table address and offsets
within 64 bytes on either side finds three nearby literal references for
the first table and five for the second. None is an exact-base reference.
Adjacent references are candidate module anchors, not demonstrated reads
of the filename-pointer fields.

One first-table anchor resolves through literal pool `0x10360b98` to
`0xc18cb5d4`, 24 bytes before the pointer table. Bounded Thumb decode verifies
readers `0x10360876`, `0x103608c6` and `0x103608fa`; their accesses are
halfword-indexed lookups in nearby format/flag data. This establishes a
native lookup connection but does not show a filename-pointer load or file
creation. A separate nearby anchor is used by mutable state getters/setters;
that alone is also insufficient to identify a save operation.

No new saved-crop path is established. In particular, sharing an initialized
data neighborhood with filename templates does not establish that a function
serializes a photo or uses crop dimensions. F-106's rejected record-builder
interpretation remains rejected; F-114's seven-caller trace and the retired
SD-card simulator thread were not resumed.

## Reproduction and next step

The newly written private helper reruns the original-input/mapping audit,
searches the RAM targets and compares the three bounded RAM blocks:

```sh
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-save-table-ram-audit-private.py" --tag 02
```

Recorded run: fresh private tag `01`. Firmware, raw tables and logs stay
outside Git. This experiment leaves the original firmware unchanged.

Single next step: trace accesses to the filename-pointer fields themselves
using these verified RAM addresses and candidate module anchors. Require an
actual pointer-field load before treating an anchor as a filename consumer;
then follow its request toward a real RAW/JPEG serialization or file-creation
boundary. A neighboring flag lookup is not enough to choose a crop patch.

No saved cropped RAW or JPEG has been produced. Hardware remains NO-GO.
