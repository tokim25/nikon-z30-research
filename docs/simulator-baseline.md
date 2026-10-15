# Native display simulator baseline

Date: 2026-10-15. Status: baseline verified; native XPan milestone incomplete.

## Result

The pinned WonderLantern Z30 simulator built locally on macOS and executed
the original C1.20 display code. Local frame inspection showed simulated color
bars with native touch controls, information-button graphics, and focus-frame
graphics. A second run successfully refreshed the display with debugger
observations enabled. No host-drawn XPan overlay was used.

This is assisted execution, not natural camera boot. The simulator supplies
diagnostic startup state and synthetic processed preview buffers. It does not
demonstrate a working sensor, autofocus, RAW processing, or physical camera.
The native XPan guides and their on/off lifecycle are not demonstrated yet.

## Reproducibility and boundaries

- Simulator source: [WonderLantern/z30-qemu at the tested revision](https://github.com/WonderLantern/z30-qemu/tree/0ba0c3547ccbec09e7c861eaca35db8e82795f15).
- QEMU version: 10.2.4. The upstream build tool verified its archive checksum.
- Local build: six jobs; isolated Python build tools; existing Homebrew GLib
  and Pixman. The pinned device-tree dependency required a separate fetch
  after an initial network-restricted attempt left its checkout incomplete.
- Firmware: the recovered verifier extracted the unchanged EG module from
  the original verified package; its expected SHA-256 matched before and
  after saving the simulator input. See [recovery evidence](milestone-1-recovery.md).
- Startup: upstream `liveview_session.start` with its documented diagnostic
  options, followed by a refresh request. The debugger listens on loopback.
- Firmware, extracted module, build products, raw session logs, and native
  screenshots remain outside this repository. No patches or hardware access.

The upstream session helper supplies diagnostic calls at the InitTask service
checkpoint and restores the caller context after completed calls. This
establishes a tested simulator context, not safe call timing on a real camera.

## Refresh trace

A bounded runtime observation during an explicit call to `0x1032427e`
recorded, in order, `0x10453fac`, `0x10453ac2`, and `0x10453d14`.
The call completed. The alternative observed address `0x10453e2e` was not
visited during that particular call; this does not rule out other states.

Static inspection clarifies that `0x10453ac2` returns a state-dependent
boolean-shaped value. It is a gate, not an established draw callback.
The reached `0x10453d14` prepares a request structure and calls `0x104b74f4`,
whose entry branches to `0x104b740a`. That downstream path still needs runtime
tracing. Neither address is an established rectangle API.

## Remaining milestone acceptance checks

- Identify a native drawing operation and validate its arguments, ownership,
  clipping, and execution context without modifying firmware instructions.
- Draw centered 65:24 guides through native code, with no host pixel overlay.
- Verify guide placement against the actual image viewport, not assumed LCD
  dimensions; distinguish synthetic scene pixels from UI pixels.
- Toggle off, refresh, and verify removal; repeat to check stale graphics.
- Verify unrelated UI stays intact and the firmware input hash is unchanged.
- Publish only original tooling, synthetic tests, and reviewed summaries.

Next investigation: follow the observed request into its downstream display
worker and identify how existing native drawing objects are rendered. The
baseline removes simulator setup as an obstacle; drawing integration remains
research, not a finished feature or a promised hardware capability.
