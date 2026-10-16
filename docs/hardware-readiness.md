# Hardware-readiness checkpoint

Reviewed 2026-10-16. **NO-GO for hardware testing or installation.**
Personal build-phase authorization does not grant permission to connect,
flash or install on the owner's camera. No installable firmware was produced.

| Requirement | Evidence | Remaining gap |
| --- | --- | --- |
| Live-view framing | Prior native guide lines; PR #43 adds persistent native black masks after diagnostic setup. | Natural startup and supported state lifecycle. |
| Display reliability | PR #48 repeats two clean on/off cycles. Mask remains over audited menu entry. | Menu cleanup, verified return to live view, focus graphics and reboot. |
| RAW crop | PR #37 changes capture geometry to centered 5200 by 1920 in a disposable guest. | Actual capture, saved NEF dimensions/metadata and compatibility. |
| RAW output path | PR #47 verifies a selected structure pack and processing submission. | Source-object identity and native serialization/storage boundary. |
| AE-L/AF-L tracking | PRs #44/#45 trace a queued bank mapping; physical identity remains unresolved. | Verified button press/release, tracking entry point, reticle and cancellation. |
| Combined features | Neither complete feature is available. | Concurrent display/input behavior, rejection in unsupported states and recovery. |
| Failure containment | Exact original identity gate exists. | Timing, power behavior, compatibility and a credible recovery plan. |

The masked preview leaves 720 by 266 visible pixels, rounded to 65:24.
It hides UI outside that strip as well. The test uses one diagnostic guest
clip-flag write and native geometry/color setup; it is not an automatic
firmware feature. The audited live-view entry after menu entry leaves the
screen stack populated, so it does not establish natural menu exit.

Assisted startup and synthetic preview input do not establish sensor,
physical input or save-pipeline readiness. An empty screen stack also does
not mean the live-view mode object is uninitialized (PR #46). The simulator
has functional ISP support (PR #41), but that alone does not prove it can
validate a complete RAW capture/save path.

Tracking research has resumed by owner request; earlier paused-lane wording
is stale. No physical-button input or tracking activation is verified.
Matching a logical input mask to the named hardware switch is insufficient.

All new observations are bounded in the milestone PRs listed in
[the current handoff](handoff-codex.md). Original firmware files/instructions
and the pinned simulator remain unchanged; runtime data was restored before
each disposable process was discarded. No hardware was used.

Next: establish native clip-state lifecycle across menu entry and a verified
return to live view. Complete the remaining simulator evidence and containment
work before proposing a separate, concrete hardware plan for owner approval.

Written by Codex in collaboration with Tony Kim; updates Claude's earlier checkpoint with the new simulator findings and their limits.
