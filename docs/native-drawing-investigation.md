# Native rectangle interface: bounded investigation

Date: 2026-10-15. Offline analysis of the unmodified EG image and the existing
QEMU render-trace report. Addresses below are evidence landmarks, not approved
entry points. All names are descriptive inferences, not recovered symbols.

## Result

A defensible route now exists for investigating native 65:24 guides: follow
the stock renderer's border-rectangle submissions into the 28-byte request
wrappers at **0x10477af2** and **0x10477596**. A related zero-color operation is
at **0x10477a5c**. These are materially narrower candidates than the large
render-state objects passed through 0x103c0ac2.

This establishes a static rectangle interface candidate, not functioning
guides. None of these newly identified functions was invoked. The supplied
runtime report observes their upstream caller, 0x103c1b54, but does not record
entry into these rectangle wrappers or their input memory. Pixel attribution,
execution context, clipping, ownership, and refresh persistence remain open.

## Evidence chain

| Landmark | Concrete evidence | Limit |
| --- | --- | --- |
| 0x103c3568 | Iterates five categories; obtains or reuses objects, prepares category-specific state, then can call 0x103c1b54. | Categories are not independently named display layers. |
| 0x103c0bc0 | Builds a compact selector and obtains object pointers through 0x1036454c. | This is object acquisition, not a rectangle constructor. |
| 0x103c0ac2 | Dispatches by category; categories 1 and 2 reach 0x103c0930 or 0x103c05d2. | Different categories have different layouts. |
| 0x103c0930 | Initializes two four-halfword geometry records from zero origins and object dimensions before calling 0x103c05d2. | End-coordinate versus extent semantics are not established for every record. |
| 0x103c05d2 | Sets scaling flags, geometry, buffer-related pointers, and multiple records in the category-1/2 object. | Not a general line-drawing routine. It also mutates incoming geometry. |
| 0x103c1b54 | Computes centered image bounds and constructs left/right/top/bottom rectangle requests from the surrounding region. | The observed runtime entry alone does not prove every conditional border call executes. |
| 0x10477af2, 0x10477596, 0x10477a5c | Copy 28 bytes into local storage; obtain current surface dimensions; replace the second coordinate with surface height minus that coordinate minus rectangle height. | Explicit vertical-origin conversion; active surface and orientation still require runtime measurement. |
| 0x10477a88, 0x10477528, 0x104779f4 | Select a context-dependent request/dispatch path or a direct rendering path. | Queue ownership and completion contracts have not been resolved. |
| 0x104773c6 | Uses the first four request words as geometry, configures color/state, and calls 0x1050aad6 on one branch. | Lower backend and actual scanout effects were not traced in this pass. |

The supplied session has two observation groups: one during a checkpoint and
one attached to the explicit stock refresh. In the explicit-refresh group,
the object supplied in r2 at 0x103c0ac2 and 0x103c05d2 is the same pointer
supplied in r0 at 0x103c1b54. Category argument r1 is 1 at the first two
entries; category argument r2 is 1 at the final entry. The earlier checkpoint
group uses a different object address. This supports a shared object flow,
and argues against treating one observed object address as permanent.

## Two distinct representations

The category-1/2 render-state object contains ten 76-byte record slots starting
at offset 8, followed by a count at 0x300. The ten-slot interpretation follows
both the clear loop and the population loop in 0x103c05d2. Each populated slot
contains flags, buffer-related pointers, dimensions and geometry. Object
offsets 0x320 and 0x324 supply dimensions; 0x328 and 0x32c supply buffer-related
values. Scale flags at 0x309 and 0x30c encode powers of two. Geometry handling
includes signed halfword comparisons and vertical even-alignment adjustments.
This is evidence for a composite render description, not ten arbitrary guide
rectangles. Ownership and the complete allocation size remain unresolved.

The smaller rectangle request is a separate representation:

| Offset | Supported interpretation |
| --- | --- |
| 0x00, 0x04 | 32-bit horizontal and vertical origin candidates. Border construction and the wrapper's vertical transform support this interpretation. |
| 0x08, 0x0c | 32-bit width and height candidates. Border callers calculate remaining widths/heights by subtraction. |
| 0x10 | Packed color input on the 0x10477af2 path; a downstream helper extracts byte components. Channel ordering and alpha behavior remain unverified. |
| 0x14 | Mode-dependent alternate-path parameter; zero selects a simpler backend path in 0x104773c6. Do not assume it is opacity or line thickness. |
| 0x18, 0x19 | Byte-sized state selectors forwarded into rendering-state setup. Meanings remain unresolved. |
| 0x1a–0x1b | Included in the 28-byte copy; semantic use not established. |

The related 0x10477a5c path reaches a backend that temporarily sets four color
components to zero. It should not be presumed to draw visible black guides:
zero may have transparency/clearing implications. The two colored candidates
also differ in their downstream behavior and are not interchangeable APIs.

## Bounded next experiment for the parent trace tooling

Use passive entry observations during the already-established stock refresh,
without introducing calls to any new address:

1. Observe 0x10477af2, 0x10477596 and 0x10477a5c. Record caller, task/context,
   r0, and exactly 28 bytes of pointed-to request memory in private evidence.
2. Observe their downstream direct/dispatch decision and the surface-dimension
   helper 0x103bd330. Associate observations with the same refresh sequence.
3. Compare requests with native image bounds and resulting frames. Separate
   border clearing from visible colored drawing. If no wrapper executes, report
   that result rather than forcing a branch or invoking the service.
4. Establish coordinate units, surface selection, color semantics, clipping,
   completion, and redraw ordering before considering a guide experiment.

For a measured active image rectangle (x, y, W, H), the intended centered guide
height is W × 24 / 65, and its upper boundary is y + (H − W × 24 / 65) / 2.
This assumes that height fits inside H. Two thin horizontal rectangles are a
reasonable eventual representation. Rounding and thickness must respect the
measured native coordinate scale; the current evidence does not justify using
the simulator window size as the image rectangle or assuming one logical unit
is one output pixel. Guides must be resubmitted at an established point after
stock clears and removed through the normal redraw lifecycle.

## Reproducibility and limits

The private tool `work/drawing-investigation/inspect_windows.py` reads the
specified unmodified image, records its SHA-256 and Capstone version, bounds
each requested window to at most 4096 bytes, and merges local instruction
windows into a private report. It neither executes firmware nor writes the
input. Raw listings remain outside the repository.

Linear windows include embedded literal pools and branch tables. Conclusions
above follow explicit branch destinations and contiguous instruction sequences;
decodings across those data islands are not executable evidence. This pass
does not claim a complete control-flow graph or independently verify the
upstream package extraction. The existing session report is evidence supplied
by the parent investigation, not a fresh run performed here.

No hardware, firmware edits, installable patches, host-drawn guide mockups,
tracking analysis, or publication actions were involved. Current readiness:
**native rectangle candidate identified; passive runtime validation pending;
65:24 guide rendering not demonstrated**.
