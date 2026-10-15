# Model one-step subject-tracking activation offline

## Problem and evidence

Explore one physical-button action to request tracking at an already selected target. Nikon's [Focus guide](https://onlinemanual.nikonimglib.com/z30/en/05-01.html) documents a reticle-then-start J workflow and direct touch selection. A new button interaction needs its own specification; documentation alone does not expose a callable camera implementation.

This is an original host simulation. Strings such as “3D tracking,” menus, or guessed symbols are not proof of an implemented, reachable 3D-tracking algorithm. No such functionality is claimed.

## Proposed model

Define `idle`, `acquiring`, `tracking`, and `unavailable` states. In a declared eligible auto-area configuration with a valid selected target, a single press emits exactly one mock acquisition request and enters `acquiring`. A matching success acknowledgement enters `tracking`; failure returns to idle with a reason. Cancellation ends the session. Specify this as proposed behavior, not Nikon's internal state machine.

## Offline acceptance criteria

- [ ] Publish a transition table defining states, eligible modes, target validity, input events, and observable effects; cite documented behavior separately from project choices.
- [ ] From eligible idle, one press emits one acquisition request for the selected target without a second confirmation; no shutter-release or capture request is emitted.
- [ ] Success for the active request enters tracking; failure or a deterministic simulated timeout returns to idle with an error reason.
- [ ] Repeated key-down/autorepeat during acquisition emits no duplicate requests. Define and test release/repress behavior and cancellation while tracking.
- [ ] Missing target, manual-focus configuration, and unsupported AF-area configurations emit no acquisition request and expose an unavailable reason.
- [ ] Cancel, mode change, and simulated shutdown invalidate pending requests; late or mismatched acknowledgements cannot restart tracking.
- [ ] Maintain a separate baseline fixture for Nikon's documented photo AF-C/AF-A half-press release behavior; do not silently apply it to all proposed button workflows.
- [ ] Use synthetic targets and a mock backend only. Tests run without firmware, network, camera, USB, or SD access and include deterministic event traces plus actual test results.
- [ ] Document that simulated acquisition success proves neither autofocus accuracy nor hardware compatibility nor 3D tracking.

## Exclusions and completion evidence

No camera callbacks, firmware changes, extracted byte sequences, installable patches, or hardware flashing. Deliver original model code, transition coverage, test command/results, and an unresolved integration list. Earlier milestone artifacts remain unavailable; this work must not be labeled recovered code.
