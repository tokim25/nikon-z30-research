# First read-only display-path trace

Date: 2026-10-15. Input: the verified Z30 C 1.20 package described in
[Milestone 1 recovery](milestone-1-recovery.md).

## Plain-language result

We connected the known histogram checks to shared display-state routines.
One of those routines uses the same table and histogram entry that the earlier
research verified. This is a useful connection, not a new drawing feature.

The inspected code appears to decide whether existing display elements should
be active. We have not identified the code that turns a new rectangle into
pixels, nor shown how to add an independent overlay safely.

## Method and boundaries

The recovered verifier checked the original package, decoded its main module
in memory, and checked its identity and integrity before inspection. Capstone
5.0.6 decoded selected ARM Thumb instruction windows locally. No camera
instructions were executed. No upstream patch builder was run.

The decoder dependency is installed only in the chat workspace's isolated
analysis environment; the repository and its CI remain dependency-free at
runtime. The local script and disassembly report remain outside Git.

Six bounded windows were inspected: the known display gate, widget gate,
two downstream routine entries, and two branch-chain points. A separate
four-byte literal lookup and table-entry lookup tied the shared routine to
the known histogram descriptor. All reads stayed within the fixed image.

This was not a complete control-flow analysis. Linear decoding can mistake
embedded data for instructions. In particular, a table branch inside the
larger shared routine was encountered; following linear output over its
table was not treated as executable evidence. Unresolved branches and
indirect calls remain unresolved.

## Evidence map

Addresses are research landmarks, not callable APIs or patch instructions.
Only original summaries and metadata are published, not instruction listings.

| Location | Observation | Confidence and limit |
| --- | --- | --- |
| Known gate at 0x1044ff70 | Beyond the DISP check, it reads properties and checks additional routines before forming a boolean-like result. | Static observation. Property meanings and all downstream conditions remain unverified. |
| Widget path starting 0x1036e8b4 | A reachable branch within this bounded path calls the known gate at 0x1044ff70. The path also updates bytes in an existing widget-related object. | Static link established; byte meanings and actual runtime reachability were not tested. |
| Path near 0x1036e8fe | Passes index 31 to 0x10369c88, then transfers to 0x10369c54 with the same index. | Direct calls/transfers observed. Neither target is established as a drawing service. |
| Routine at 0x10369c54 | Uses its input to select a descriptor, inspects child-record state, and can set a descriptor flag. | Consistent with state propagation; naming it a renderer would go beyond the evidence. |
| Literal at 0x10369f10 | Resolves to descriptor table 0x1073f830; entry 31 resolves to 0xc1826714. | Independently read from the decoded image in this phase; agrees with recovered histogram landmark. |
| Routine at 0x10369c88 | Starts with property/state checks and branches based on the supplied index. | Partial inspection only. Table branches and paths outside the window prevent a complete role assignment. |

The upstream source identifies the existing histogram descriptor and gates in
[liveview_dual.py at the pinned revision](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/src/z30_extensions/features/liveview_dual.py#L7).
Its [gate checker](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/tools/verify_liveview_gates.py#L1)
stops before downstream services. This new inspection extends the static map;
it does not extend the upstream execution tests or establish hardware behavior.

## Decision and next step

Continue read-only analysis of descriptor consumers: find which functions read
the state flags and eventually request drawing. Keep eligibility checks,
state updates, and actual rendering separate.

Before calling anything a usable XPan drawing service, establish coordinate
units, clipping, refresh timing, object ownership, and cleanup when leaving
live view. The next pass should follow control flow around branch tables
rather than interpreting a larger linear listing as a complete function.

No firmware was modified, no extracted binary was written, and no hardware was
connected. The source and decoded-module identities still match the recovery
report. No new claim about subject tracking follows from this display trace.
