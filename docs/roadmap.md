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

The two reviewed bodies under `docs/issues/` were published on 2026-10-15: [#1: XPan-style framing](https://github.com/tokim25/nikon-z30-research/issues/1) and [#2: one-step subject tracking](https://github.com/tokim25/nikon-z30-research/issues/2). The original host simulations are implemented, with 24 tests passing in coordinator integration. See [XPan evidence](xpan.md) and [tracking evidence](tracking.md). Completion demonstrates only the simulations, not camera functionality.

## Next session: camera-integration feasibility

The first source audit is complete: [findings and evidence](integration-feasibility.md).
Neither feature has a supported camera integration path yet. The next task is a
read-only trace of the existing display path; tracking needs a verified entry
point. The previous milestone ZIP is now recovered; [its verification results](milestone-1-recovery.md) restore the known display landmarks without importing raw firmware excerpts.

Follow the display landmarks from the recovered analysis and record evidence gaps before camera-specific implementation. Do not run the upstream patch builder, generate installable payloads, or connect hardware. Raw local evidence must be reviewed and summarized before publication.

The [first read-only display trace](display-path-trace.md) now connects the
widget path to shared state routines and confirms their descriptor table link.
Next: trace consumers of those state flags to distinguish refresh decisions
from actual drawing, with branch-table-aware analysis.

The [second trace](display-refresh-path.md) connects an aggregate child-state
check to a shared refresh-request mechanism. Next: inspect the refresh service
and its code-pointer target, keeping dispatch separate from pixel rendering.

## Active milestone — Native XPan guides in the simulator

The user authorized offline simulator work through native guide rendering and
clean on/off behavior. The [native display baseline](simulator-baseline.md)
now runs successfully on macOS using unchanged firmware, assisted startup,
and synthetic color bars. Runtime observations confirm the refresh path.
Native XPan drawing remains incomplete; the baseline is not milestone success.
Follow the acceptance checklist in that report. No hardware or installable
firmware work is authorized by this milestone.
