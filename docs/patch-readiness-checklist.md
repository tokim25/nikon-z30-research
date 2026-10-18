# Minimal patch-readiness checklist

Use this checklist to decide whether a concrete patch can be built. Do not
start another research loop until the next item is identifiable and bounded.

## Simulator patch essentials

- [ ] Exact hooks and native input boundaries are identified for each included
  feature. Tracking is conditional and stays out until its native entry point
  is verified.
- [ ] Each hook has a defined trigger, guard, cleanup, and return behavior.
- [ ] Reserved space, instruction mode, branches, literals, registers, stack,
  flags, and return paths pass an ABI/layout audit.
- [ ] Every intended change is in an exact edit manifest; firmware bytes and
  patched images stay outside the repository.
- [ ] A private overlay loads in the pinned simulator without debugger writes.

## Simulator acceptance essentials

- [ ] Native lifecycle passes: startup, menu return, relevant state changes,
  repeated transitions, cleanup, recovery, and target/non-target behavior.
- [ ] Stock-versus-patched comparisons pass, followed by an independent
  ABI/layout review. If tracking is included, also cover eligibility, chord
  arbitration, press edges, completion cleanup, and playback protection.

## Publication check

- [ ] Before authorized publication, run unit, artifact, encoded-data, and
  whitespace/diff checks, then manually review the complete file set and fact
  numbering. These checks validate publication, not feature acceptance.

## Hardware gates

Current owner waivers are recorded in session-manager-brief.md and
test-readiness-2026-10-17.md. Apply those named waivers to the camera-test
decision without labelling missing measurements as passes. No hardware
approval follows from this publication task.

The simulator essentials must be satisfied first, unless an explicit owner
deviation is recorded.

- [ ] Verify the exact original firmware identity offline.
- [ ] Run read-only preflight allowing only the planned edits and policy.
- [ ] Bind the build to its exact manifest and bounded test scope.
- [ ] Document the original backup and recovery decision, including service or
  total-loss risk if recovery cannot be verified.
- [ ] Mark `hardware-readiness.md` **READY FOR AN EXPERIMENTAL HARDWARE TEST**
  with the exact build, scope, evidence, and residual risks.
- [ ] Obtain the owner's separate approval immediately before hardware access.

## Scope notes

Saved RAW/JPEG crop is an owner-approved on-camera test item, not a simulator
checkbox or feature-work blocker. Tracking patch design is deferred until the
authorized breakpoint checkpoint establishes a native entry point. Hardware
remains **NO-GO**.

The owner subsequently narrowed XPan work to stills only. Movie-transition
coverage and a still/movie exclusion predicate do not block that simulator
candidate; movie behavior remains unvalidated. This scope clarification does
not relax the ABI checker or the stills lifecycle acceptance requirements.
