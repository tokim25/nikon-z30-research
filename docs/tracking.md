# Offline subject-tracking interaction model

This newly written host simulation implements the proposal in `issues/002-one-step-subject-tracking.md`. It is not recovered milestone code. It emits immutable mock acquisition requests only: no backend callbacks, capture requests, firmware operations, or camera access exist.

## Proposal contract

`TrackingModel` models photo configurations with focus `AF-S`, `AF-C`, or `AF-A` and area `auto-area`, `auto-area-people`, or `auto-area-animals`. Eligibility is a project policy, not an assertion that a Nikon API supports this operation. A target is a two-element tuple of finite numeric coordinates in the inclusive normalized range 0–1; booleans are rejected. Configure through `configure`, rather than assigning model fields directly.

One input press emits `AcquisitionRequest(request_id, target)`. IDs increase within a model instance and acknowledgements must refer to that same instance. No real object detection or focus calculation occurs. The caller supplies success/failure explicitly. `advance` moves a deterministic integer clock; five ticks is the default timeout, with no relationship to camera timing or wall-clock seconds.

| State | Event | Result and observable effect |
| --- | --- | --- |
| idle, eligible | fresh press | acquiring; exactly one request |
| any | held-key repeat | unchanged; no request |
| acquiring or tracking | release then press | unchanged; no request |
| acquiring | matching success | tracking; timer cleared |
| acquiring | matching failure | idle; `acquisition-failed` |
| acquiring | clock reaches timeout | idle; `timeout`; request invalidated |
| any | mismatched, late, duplicate acknowledgement | unchanged |
| any | release | clears key latch; does not stop tracking |
| any | cancel | idle if eligible, otherwise unavailable; request invalidated |
| any | configure | session invalidated; eligibility reevaluated, even for unchanged settings |
| any | shutdown | permanently unavailable; request invalidated |
| unavailable | press | no request; explicit reason remains |

Unavailable reasons are `unsupported-focus`, `unsupported-area`, `invalid-target`, or `shutdown`, in that precedence after shutdown. Cancellation, failure, timeout, and configuration changes retain the key latch: retry requires release and a fresh press. Tracking ends through explicit cancellation, configuration, or shutdown, not another press. Create a new model after shutdown; do not route old acknowledgements into a new instance.

`trace` returns immutable transition snapshots containing event, resulting state, reason, active request ID, and emitted requests. Example: `press/acquiring → ack-success/tracking → release/tracking`. Failure/retry example: `press/acquiring → ack-failure/idle → repeat/idle → release/idle → press/acquiring`, with a new request ID. These traces describe a simulated interaction only.

## Separate documented baseline

[Nikon's Focus guide](https://onlinemanual.nikonimglib.com/z30/en/05-01.html) documents release ending photo AF-C/AF-A tracking when tracking was initiated by a shutter half-press, restoring the previous focus point. `NikonHalfPressBaselineTests` stores this as a separate documentation fixture and contrasts it with the proposed button release behavior. That fixture does not execute or validate Nikon firmware. The mock never emits a shutter-release action.

## Validation and limitations

Run from the project root:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_tracking.py' -v
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Tests use synthetic targets, explicit acknowledgements, and clock ticks. They cover eligibility, request counts, repeats and fresh edges, success/failure, timeout boundary, stale acknowledgements, session invalidation, shutdown, and the separate release baseline.

Execution on 2026-10-15: all 10 tracking tests passed locally. The coordinator reported that the final integrated suite passed all 24 tests. `python3 .github/scripts/check_artifacts.py` passed its tracked-artifact checks; this does not certify untracked content or replace manual review.

Unresolved integration: real input routing, display coordinates, target acquisition, autofocus accuracy, camera timing, and hardware compatibility. Simulated success and readable menu strings prove no 3D-tracking implementation. 
