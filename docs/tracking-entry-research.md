# Tracking entry research — bounded static findings

Reviewed 2026-10-15. This sidecar investigated tracking only; it did not trace
the display worker, execute firmware controls, modify firmware, or test hardware.

**Decision after falsification:** reject the caller convergence lead at
`0x11cf4e90` / `0x11cf4ea0` as a subject-autofocus activation entry. Its callees
process Bluetooth/HCI packets and connection handles. The separate
subject-text lead is regulatory wording. No verified native subject-tracking
entry remains from these text leads. Hardware readiness is not established.
These addresses are research landmarks, not callable interfaces or proposed
patch locations.

## Follow-up: caller conditions and subsystem attribution

The follow-up read original code and text in local memory; detailed inspection
is retained only in `work/tracking-investigation/private-inspection.json`.
`falsify.py` reproduces the bounded inspection and writes `falsification.json`.
Do not import the private inspection into the repository: it contains restricted
instruction listings and text. The following is a newly written semantic summary.

| Location | Resolved behavior | Consequence |
| --- | --- | --- |
| `0x11cf4e7e`–caller neighborhood | Compares a queue's first pointer with its head; the nonempty path obtains a node through `0x11cd9502`. That helper unlinks a first node by updating forward/back links. | This is queue processing, not a demonstrated camera-button dispatcher. |
| `0x11cf4e90` | Repeats `0x11cf4986` while its return is zero. Once nonzero, tests bit 1 of the node's byte at offset `0x10`; only that branch passes the node to `0x11cf5774`. Subsequent branches test bits 2 and 3. | Convergence represents packet-class dispatch after another processing step; the return must not be called AF acquisition success. |
| `0x11cf4986` | Manipulates queues and packet flags; reads a two-byte value through `0x11cd947a` and passes it to `0x11cf5248`. Its tracking text explicitly identifies Bluetooth packets. | Attribute this neighborhood to packet bookkeeping. Full scheduling semantics and the return-value contract were not reconstructed. |
| `0x11cf5248` | Masks its input to 12 bits, checks four enabled records for matching masked identifiers, and returns slot 0–3 or `0xffff` on miss. No stores or calls occur within this bounded leaf routine. | Connection-handle lookup in this context, not tracking activation or an AF target-coordinate operation. |
| `0x11cd947a` | Combines two adjacent bytes into an unsigned little-endian 16-bit value. | Provides structural support for packet-field parsing independently of the tracking labels. |
| `0x11cf5774` | Reads a payload pointer at node offset `0x0c`, checks payload length against a length byte, and dispatches on a leading event byte. One branch selects `0x13`, reads an entry count, then handle/count pairs; it performs the shared lookup and completion bookkeeping. | Together with explicit HCI receive-buffer and completed-packet text, this identifies protocol-event processing rather than subject acquisition. |
| `0x11d6f7b8` | Immediately returns to its caller, without modifying state or formatting text. | The earlier reporting-helper hypothesis is narrowed to an inert stub in this image. Calling it cannot supply acquisition notifications. |
| `0x104d2410` | The subject keyword belongs to a regulatory sentence; the code passes consecutive lines to repeated text-processing calls. | Reject the subject-text lead as an AF candidate. |
| `0x103edc2e` | Selects an AF-area label, supplies length 16 and a stack destination, then joins neighboring label cases at a common call. | A label-selection/output path remains; it does not establish that the named mode can be activated. The common callee's exact contract was not established. |

Bluetooth attribution is a static conclusion supported by both explicit
protocol vocabulary and queue/handle/event structure. No external protocol
specification was consulted and no camera or emulator controls were executed.
The analysis does not exclude a separate AF implementation elsewhere in the
image, or claim that all callers of these helpers have been recovered.

### Concrete blocker and stop decision

The recovered text leads now resolve to packet processing, regulatory text,
property metadata, and label output. None supplies a native live-view input
dispatcher, an AF acquisition call, or its state/argument contract. The only
available GUI input route substitutes display refresh for live-view key events.
Consequently there is no evidenced event path or known-safe native operation
with which to conduct milestone 3. Guessing a call address or interpreting mock
acknowledgements as firmware acquisition would not close that gap.

This completes falsification of the convergence lead and reaches an evidence
blocker, rather than leaving that lead as a proposed next step. The separate
research needed to unblock activation is to establish stock live-view input
routing from an independent input landmark. The menu dispatcher is not such a
landmark without a proven live-view connection. No hardware work is justified
by the current results.

## Initial-pass evidence and reproducibility

The initial candidate map below is retained for provenance. Its AF candidacy
is superseded by the falsification above; it is not the current recommendation.

The local original EG module is 33,939,514 bytes, mapped at `0x10020000`, with
SHA-256 `8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
Identity matched the recovered milestone report. Analysis used Capstone 5.0.6
in Thumb mode. The new local `work/tracking-investigation/analyze.py` checks
that digest before reading, reproduces five PC-relative references, and emits
address metadata in `evidence.json`. Neither output contains instruction
listings or extracted firmware bytes. Both remain outside this repository.

The scan for incoming branches covers halfword positions before the recovered
initialized-data source at `0x11f81c94`. That interval contains mixed code and
data; pattern matches are candidates, not proof of reachable instructions.
Candidate prologues are the nearest matching stack-save instructions within
2,048 bytes whose linear decode reaches the reference. This is not a complete
control-flow analysis or a function-boundary proof. Calls reported around each
reference come from a bounded linear window, not necessarily one basic block.

| Landmark | Reproduced static evidence | Interpretation and limit |
| --- | --- | --- |
| Prior AF-area label lead | PC-relative reference at `0x103edc2e` resolves to text at `0x103eddfc`. | Moves beyond a bare text hit, but this bounded pass found no qualifying prologue or following call in its short window. It does not prove selectable 3D tracking. |
| Subject-related text | Reference `0x104d2218` resolves to `0x104d2410`; candidate routine `0x104d2166` repeatedly calls the same small set of targets. Incoming candidates occur at `0x104d2698` and `0x104d2728`. | Repetitive text-associated processing is a lower-priority lead than the cluster below. No evidence ties it to target acquisition. |
| First tracking-text reference | `0x11cf4a56` resolves to `0x11cf4dbc`; linear decode from candidate `0x11cf4986` includes calls to `0x11cf5248` and `0x11d6f7b8`. | A concrete code neighborhood to investigate. Text use alone does not identify a start operation. |
| Second tracking-text reference | `0x11cf4f18` resolves to `0x11cf51d0`, followed by a call to `0x11d6f7b8`. | Supports a related neighborhood; no qualifying nearby prologue was found by this heuristic. |
| Third tracking-text reference | `0x11cf589c` resolves to `0x11cf5bc8`; candidate `0x11cf5774` also calls `0x11cf5248` and `0x11d6f7b8`. | Shared targets provide a concrete graph to follow. The common text-adjacent target may be reporting machinery; its semantics are unverified. |
| Caller convergence | Branch-pattern candidates `0x11cf4e90` → `0x11cf4986` and `0x11cf4ea0` → `0x11cf5774`; additional candidates `0x11cf3e60` and `0x11cf3e94` target the latter. | Best next point for caller-side argument and condition analysis. Function boundaries, dispatch ownership, and autofocus attribution remain unknown. |

Exact word-pointer searches did not find references to the starts of those
five text strings; nearby PC-relative decoding did. The earlier movie tracking
sensitivity property text at `0x11c9ba68` has a word reference at `0x1204ee64`.
That is property metadata evidence, not a photo tracking-start service.

## Initial investigation plan — now resolved for this lead

Steps 1–2 below were pursued: subsystem attribution rejected the lead and the
shared helpers were characterized above. Steps 3–4 describe the independent
input evidence still missing, not authorization to invoke guessed addresses.

1. Establish valid instruction boundaries and reachable control flow around
   `0x11cf4e90` / `0x11cf4ea0`, then trace their caller and arguments. Determine
   whether this cluster belongs to autofocus, another tracking subsystem, or
   diagnostics. Reject it as a tracking-activation lead if callers establish an
   unrelated subsystem.
2. Identify the shared `0x11cf5248` callee and distinguish state-changing work
   from text reporting through `0x11d6f7b8`. Do not assume either is acquisition
   or success notification. A text formatter is not a tracking entry point.
3. Only after subsystem attribution, trace backwards to a stock live-view
   input dispatcher and forwards to state transitions. Required evidence is a
   native input-to-state path, eligible camera modes, ownership and arguments,
   cancellation/release behavior, and observable acquisition outcome.
4. If caller analysis fails to connect the cluster to live-view autofocus,
   return to tracing the stock live-view input dispatch independently. Do not
   substitute menu event numbers or the sensitivity property's identifier.

## Simulator limitation and milestones

The local simulator's `tools/gui.py`, lines 83–84, sends live-view key actions
to `liveview_session.refresh(s)`. Only its menu branch passes an event to
`0x103ce96e`. Thus live-view direction, OK, and back clicks do not demonstrate
native live-view key delivery or subject-tracking activation. A changed frame
after such a click is display-refresh evidence only. No arbitrary control calls
were attempted during this investigation.

| Milestone | What this sidecar establishes |
| --- | --- |
| 1 — Framing reliability | Outside this sidecar; no display-worker findings asserted. |
| 2 — Tracking entry | Caller convergence falsified as an AF lead; it belongs to Bluetooth/HCI packet processing. No native acquisition entry established. |
| 3 — Native activation simulation | Blocked by the missing native input/activation contract and GUI refresh substitution. Synthetic acknowledgements are not native acquisition. |
| 4 — Coexistence | Blocked by the missing native tracking path. No evidence yet covers shared input ownership, AF/display scheduling, cancellation, mode transitions, or cleanup. |
| 5 — Hardware readiness | Decision reached: not ready on tracking evidence. Milestones 3–4 have unmet prerequisites; no hardware or installation recommendation follows. |

The existing host model remains useful for proposed interaction behavior.
Its successful mock tests do not validate these addresses, a native AF engine,
hardware timing, or tracking accuracy. The broader integration decision in
`integration-feasibility.md` remains unchanged.
