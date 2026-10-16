# Personal Z30 feature work

Date: 2026-10-15. The owner asked Codex to continue both features and approved
taking over the guide and RAW-crop files. This plan records the requested
result and the evidence still needed. It is not an installation procedure.

The requested result is a personal firmware build with centered 65:24 XPan
framing in live view, the matching crop in saved RAW files, and one press of
AE-L/AF-L to activate the camera's subject tracking. A guide drawn on screen
does not satisfy the RAW requirement. A menu OK event does not satisfy the
tracking requirement.

| Work | Proven so far | Required before calling the feature complete |
| --- | --- | --- |
| Live-view framing | Native guide drawing with a debugger in the simulator. | A repeatable hook that runs without the debugger; correct placement and cleanup through supported state changes. |
| RAW crop | Stock capture-geometry outputs for existing image areas. | A traced path from crop settings through capture requests and saved RAW dimensions or crop metadata; evidence showing how RAW software applies it. |
| AE-L/AF-L tracking | Named switch mask and portions of input decoding. | A proven physical press/release path to the tracking reticle; one activation per press, cancellation, mode checks and rejection behavior. |
| Combined build | Exact-original EG hash gate and host tests. | Versioned private build provenance, feature coexistence, failure containment and recovery evidence. |

The RAW goal is to make the saved file carry the intended crop. Whether the
camera stores fewer sensor pixels or records a crop over a full sensor image
is unresolved; neither behavior has been demonstrated. Existing geometry
calculations cannot settle it because this simulator has no image processor.
If that missing component prevents a required check, record the gap rather
than claiming a RAW feature works.

The build gate is open for personal, non-distributed work. Camera access is
still closed: [hardware-readiness.md](hardware-readiness.md) says NO-GO, and
there is no demonstrated recovery path. Do not describe the version check as
a recovery method or assume the update menu can restore a failed camera.

## Ownership and handoff

Codex now owns `docs/native-*`, `docs/guide*`, `docs/image-area-tables.md` and
`docs/capture-geometry-baseline.md`, in addition to the tracking files.
The lane configuration records this user-approved transfer. Simulator
infrastructure retains its existing assignment. Claude can resume from
[handoff-codex.md](handoff-codex.md), the facts ledger and the pull requests;
file ownership must be agreed again before concurrent edits.

Publish a small PR for each finding or working feature, with observed
behavior, limits and a reproduction command. Keep private helpers, original
and modified firmware, logs and screenshots outside Git. Never merge our own
PRs or push main. No camera connection, flash or installation steps are
authorized in this session.

## Next milestone

Establish the source and destination of the AE-L/AF-L input. The latest
[bit-13 trace](tracking-mask-namespaces.md) narrows two candidate fields but
does not identify either as the physical switch. Resolve that evidence gap
before choosing a tracking remap.

Written by Codex in collaboration with Tony Kim; continues Claude's simulator and capture research.
