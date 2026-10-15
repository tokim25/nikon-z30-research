# From histogram state to a refresh request

Date: 2026-10-15. Follow-up to the [first display trace](display-path-trace.md).

## What changed

We found a static path from display-element flags to the same refresh-request
mechanism used by the upstream custom menus. This narrows the search: the known
histogram code participates in a shared display system rather than exposing
an independent rectangle-drawing function.

The useful next boundary is the refresh mechanism itself. We have not shown how
it creates pixels, where a new overlay would be registered, or when calling it
would be safe.

## Evidence and interpretation

These are original summaries of local inspection, not an instruction listing.
Addresses identify research landmarks, not callable APIs.

| Landmark | Observed behavior | Interpretation and limit |
| --- | --- | --- |
| 0x10369d88–0x10369e00 | The reached part of the shared routine updates a selected descriptor and child-record flags; it calls a small property-dependent predicate. | State management, not demonstrated pixel output. Earlier table-controlled branches remain incompletely understood. |
| 0x1030664a | Reads stored state and a property through the established property-reader address, producing a boolean-shaped result. | The property meaning is not independently established; this is not a drawing primitive. |
| 0x1036999e, 0x10369a2c, 0x10369a60 | Iterate 66 descriptor slots and their child records, clearing selected flags. Child records use a 48-byte stride. | Shared lifecycle/reset machinery; actual scheduling and field names remain unknown. |
| 0x10369a96, continuing at 0x10369ad0 | Tests child flags across the same entries, returns early on a nonzero flag, and otherwise finishes with zero. | An aggregate state predicate, informally “any child flagged”; this name is an inference, not a recovered symbol. |
| 0x1030b596 and 0x1030b59e | Both call that aggregate predicate; nearby branches can lead to 0x1032427e. A subsequent path calls the flag-clearing routine. | A conditional update/refresh sequence. Not proof that the entire caller runs every frame or that every path requests refresh. |
| 0x1032427e–0x10324358 | Checks additional state and can call 0x10453fac using the code-pointer value resolved from a literal. | A refresh-request candidate with extra gates; not a direct drawing API. |
| Literal at 0x10324648 | Resolves to 0x10453ac3, matching the code-pointer value supplied by the upstream menu redraw path. | A concrete link between the examined native path and the known menu-refresh mechanism. The pointer's low bit encodes Thumb state. |

The corresponding upstream menu call is in
[sound_ui.py, line 168](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/src/z30_extensions/features/sound_ui.py#L168).
This comparison establishes the same destination and code-pointer value, not
identical timing, ownership, or display behavior.

The histogram descriptor's child count is one in the original image. Its child
record was inspected locally; no callable drawing pointer was established from
that inspection. Fields that resemble coordinates remain unclassified.

## How the evidence was obtained

The official package was checked and decoded in memory with the recovered
verifier on each run. Capstone 5.0.6 translated bounded Thumb instruction
windows. Known branches were followed around literal data rather than treating
the entire surrounding region as instructions.

Aligned table-pointer matches and potential direct calls were used only as
search leads. Candidate calls to the aggregate predicate were checked in their
surrounding instruction flow. Other scan matches remain unvalidated; a byte
pattern matching a pointer or call does not establish reachable code.

Raw descriptor words and disassembly are stored outside Git in the chat
workspace's private-inputs directory. No camera instructions were executed,
no patched image was generated, and no hardware was connected.

## Next bounded investigation

Inspect the refresh service and its code-pointer target to determine whether
they dispatch, queue, or directly perform rendering. Follow supported branches
only, and label unknown arguments and indirect calls explicitly.

Before attempting XPan integration, we still need evidence for drawing
coordinates, clipping, registration, allowed execution context, update timing,
and cleanup. The current evidence supports continued read-only research, not
camera-specific code or a claim that an overlay is ready.
