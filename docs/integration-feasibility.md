# Can these features reach the camera?

Reviewed 2026-10-15 at WonderLantern commit
`10e7335977d613075e4e5feed1e3ac331ba90a8a`. This is a source review,
not a camera test or a firmware execution result.

## Plain-language result

The existing project gives us a useful starting point, but neither feature is
ready to put on the camera. It changes when an existing histogram appears and
adds menu pages. That does not yet give us a way to draw our own framing guide
over the live picture or start subject tracking from a new button action.

The add-on interface supports short actions selected from a menu. Keeping an
add-on in memory does not make it run in the background.

**Decision:** continue read-only display research; do not implement camera
integration yet. Tracking needs a verified entry point before implementation.
This does not establish that either feature is impossible.

## Evidence map

All links below pin the reviewed revision. References identify source locations;
no firmware bytes or copied patch code are included.

| Requirement | Evidence | What remains missing |
| --- | --- | --- |
| Run our framing or tracking logic through an add-on | [Interface declaration, lines 10–19](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/examples/modules/z30_module_api.h#L10) offers property reads, short text output, and registration of a run handler. | No declared drawing, tracking-start, event subscription, or cancellation service. |
| Run repeatedly while composing a photo | [Interface restrictions, lines 1–3](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/examples/modules/z30_module_api.h#L1) and [module limits, lines 99–103](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/docs/modules.md#L99) limit the supported model to synchronous menu work. | A supported repeated-call mechanism, ownership rules, and cleanup on mode changes or shutdown. |
| Show graphics during live view | [Histogram feature, lines 38–75](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/src/z30_extensions/features/liveview_dual.py#L38) changes existing display gates and visibility masks. | A verified way to create a new graphic, its coordinate system, update timing, and display-mode behavior. |
| Draw custom menu content | [Menu rendering, lines 110–131](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/src/z30_extensions/features/sound_ui.py#L110) binds text to menu controls and refreshes a menu. | Evidence that these services can be used safely in live view; menu rendering is not a general live-view drawing contract. |
| Start tracking with one press | [Menu routing, lines 188–202](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/src/z30_extensions/features/sound_ui.py#L188) handles activation for owned menu pages and forwards other cases. | Physical-button mapping, the live-view tracking transition, eligibility checks, and a verified start/cancel operation. Numeric menu events are not established shutter or tracking events. |
| Match the mock tracking model's success, failure, and timeout states | [Module run, lines 193–200](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/src/z30_extensions/features/module_host.py#L193) calls the registered handler synchronously and records its return status. | Actual tracking-state notifications. Module success is not autofocus acquisition success. |
| Prove the guide renders correctly | [Gate checker, lines 1–5](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/tools/verify_liveview_gates.py#L1) explicitly stops before downstream drawing and eligibility services. | Evidence of live-view pixels, bounds, orientation, and cleanup. Existing gate tests do not provide this. |

## Limits of the review

Read: the complete public tree listing; module interface header; module
documentation; selected module host sections; live-view histogram feature;
sound menu routing/rendering; text-resource support; platform image mapping;
UI verification notes; and the live-view gate checker. Public sources were read
through GitHub's contents API at the pinned revision.

No tracking entry was identified in that scope. This is not a claim that the
entire Nikon firmware lacks one. Text labels and numeric event IDs alone cannot
prove a usable autofocus implementation. The platform mapping helper validates
and reads an image; it does not supply an autofocus interface.

The upstream UI notes describe menu experiments and clearly qualify their
[test scope near line 170](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/docs/ui-qemu.md#L170).
We did not reproduce those experiments. No upstream builder, checker, or module
was executed. The local firmware was neither decoded nor modified in this phase.
The prior milestone ZIP is still unavailable.

## Next steps and stop conditions

1. Trace the histogram's existing display path using source references first.
   Record where it leads, what each function is believed to do, and what evidence
   would disprove that interpretation. Stop before claiming arbitrary drawing.
2. Recover the earlier research ZIP before repeating its decoded analysis.
   Inspect its contents locally; import only reviewed original tools and notes.
   Do not import firmware, extracted bytes, or installable patches.
3. If source evidence is insufficient, define a separate read-only firmware
   analysis plan with identity checks and local-only intermediate data. Record
   unknowns instead of guessing function signatures or reusing menu event IDs.

Proceed to camera-specific implementation only after documenting the required
calls, allowed execution context, display or input ownership, and cleanup.
Hardware work and installable outputs remain outside this project's scope.
