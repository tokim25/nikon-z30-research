# Offline research roadmap

This is a new scaffold plan, not a reconstruction of missing milestone code. Source evidence and qualifications are in [research.md](research.md). Public-source reading is permitted; all experiments run locally on original synthetic data. No firmware modification, extracted-byte publication, installable patch, camera connection, or flashing is in scope.

## Milestone 0 — Evidence and reproducibility

Deliver a source register with access dates, upstream-report labels, known limitations, and firmware hash attribution. Pin an upstream commit before any revision-dependent source comparison; until then record the unresolved revision. Preserve the distinction between Nikon documentation, upstream claims, and project proposals. The current research document records the coordinator's independent package size/hash match against the upstream report; authenticity and decoded-module checks remain unverified.

Exit criteria: reviewers can trace every factual capability claim to a source; unknowns remain explicit; repository content contains no firmware or extracted payload. Earlier milestones are labeled unavailable rather than silently replaced.

## Milestone 1 — XPan live-view composition model

Implement the original host-side geometry and synthetic overlay demo described in [the XPan issue](issues/001-xpan-live-view-framing.md). Declare a 65:24 target, viewport coordinate convention, orientation behavior, rounding rule, and display-only status.

Exit criteria: all listed geometry and non-mutation tests pass offline; generated examples demonstrate bounds and centering; the report clearly states that camera rendering remains unverified.

## Milestone 2 — One-step subject-tracking interaction model

Implement an original mock state machine described in [the tracking issue](issues/002-one-step-subject-tracking.md). Specify eligibility, acknowledgement, failure, cancellation, mode changes, and repeated inputs. Keep desired interaction behavior separate from Nikon's documented behavior.

Exit criteria: deterministic event traces and tests cover every transition without Nikon bytes, camera services, or autofocus claims. No menu string is accepted as proof of 3D tracking.

## Separate research track — Native panoramic capture

Not a dependency for the framing overlay and not authorized implementation work. First produce a documentation-only evidence-gap report covering encoded dimensions, RAW/JPEG semantics, metadata, playback, and whether any source supports a native mode. Keep host cropping separate. Do not claim that an overlay changes saved files, and do not implement a firmware patch to investigate it.

Exit criterion: a sourced feasibility assessment or an explicit unresolved finding, not an installable artifact. Hardware validation remains outside this project's authorized scope.

## Publication and handoff

The two reviewed bodies under `docs/issues/` were published on 2026-10-15 in the private repository as open implementation issues: [#1: XPan-style framing](https://github.com/tokim25/nikon-z30-research/issues/1) and [#2: one-step subject tracking](https://github.com/tokim25/nikon-z30-research/issues/2). Their acceptance criteria remain future work. Completion of a simulated model demonstrates only that model; record tests actually run separately from planned acceptance criteria.
