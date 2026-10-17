# Lane 2: tracing loads of the filename-pointer fields

2026-10-17. F-151, F-152. Read-only static analysis of the original firmware
image. No simulator, no QEMU, no firmware change, no camera. Only addresses
and descriptions appear here.

**Verdict: not found.** One real consumer of the first table's pointer slots
exists (a small selector getter at `0x10354350`), but it has no static caller,
and the second table has no pointer-slot load at all. No path from either
table to file creation or RAW/JPEG serialization was reached. Hardware
remains NO-GO.

## Correction to F-129's field addresses

F-110 describes each table as five header words followed by four filename
pointers (then, for the first table, two property ids). F-129 compared and
searched 16 bytes starting at the table base, so those 16 bytes were header
words, not the pointers. The pointer slots are 0x14 bytes later:

| Table | Stored pointer slots | Initialized RAM pointer slots |
| --- | --- | --- |
| First | `0x1204d294`-`0x1204d2a3` | `0xc18cb600`-`0xc18cb60f` |
| Second | `0x1204d454`-`0x1204d463` | `0xc18cb7c0`-`0xc18cb7cf` |

Both tables' four slots point into F-110's filename-template table at
`0x11c9a5fc`, in F-110's order (slot 0 the `.JPG` entry, 1 `.NEF`, 2 `.NDF`,
3 `.TIF`). The F-129 RAM-to-source mapping itself is unaffected; only the
field offsets inside it change. F-129's anchor findings (three and five
references within 64 bytes) were centered on the wrong offset, so this pass
redid the anchor search.

## Method

1. Helper script kept outside the repository. It reuses the existing private
   verified-image loader (the same one earlier helpers use), so reads come
   from the checked decoded module. It never starts the simulator.
2. Anchor search: every aligned 32-bit literal in the image whose value lies
   within 84 bytes either side of each pointer block (repeated at 260 bytes).
   Exact-block references do not exist; all are nearby anchors.
3. For each anchor literal, find the PC-relative `ldr` instructions that load
   it (Thumb and ARM forms), then follow the register forward with simple
   propagation (`adds`, `mov`), recording every load whose effective address
   falls in the pointer block, classified by width and offset.
4. Re-ran without the control-flow cutoff over a 96-byte window so loads that
   sit after a `bx lr` branch target in a small switch-style function are not
   missed.
5. For every real load found, scan the whole image for callers: Thumb `bl`,
   `blx`, `b.w`, short `b`/conditional `b`, ARM branches, raw 32-bit
   function pointers (with and without the Thumb bit), and `movw`/`movt`
   pairs that build the function or slot addresses. The caller scanner was
   validated on a known getter (`0x10360bba`, 498 call sites).

## Loads found

Anchor `0xc18cb5f8`, literal at `0x10354634`, is 8 bytes before the first
table's pointer slots. It has 23 load sites in the `0x10354350`-`0x1035462c`
cluster. Only one of them reaches the pointer slots.

| Address | What it reads |
| --- | --- |
| `0x1035436a` | First-table slot 0 (`0xc18cb600`) |
| `0x1035436e` | First-table slot 1 (`0xc18cb604`) |
| `0x10354372` | First-table slot 3 (`0xc18cb60c`) |
| `0x10354366` | First-table slot 2 (`0xc18cb608`) |

All four are word loads inside one function, `0x10354350`. It takes a small
selector in r0 (0, 1, 2, 3 select slots 0, 1, 3, 2) and returns the selected
pointer in r0, returning zero for other selectors. In F-110's template order
that is selector 0 `.JPG`, 1 `.NEF`, 2 `.TIF`, 3 `.NDF`. This is a getter:
it returns a filename-template pointer and does nothing with it.

Other loads relative to the same anchors were not pointer-slot loads:

- `0x10354388`-`0x10354506` byte loads/stores at anchor offsets covering the
  header bytes: state flags, not pointers.
- `0x103544fa` and `0x10354500`: word loads of the two trailing property ids
  after the first table's pointers.
- `0x103545d8`, `0x103545e6`, `0x103545f6`: word loads just past the block.
- `0x10360878`, `0x103608ca`: indexed halfword lookups (F-129's readers),
  confirmed again as format/flag lookups.

Second table: anchors exist at `0xc18cb7d4` and others, but every load
through them lands past the pointer block (offsets 20 and 24 and beyond,
i.e. the next structure). There is no word load of a second-table pointer
slot, no exact reference and no `movw`/`movt` construction.

## Consumers

| Candidate | Result |
| --- | --- |
| Getter `0x10354350` (first table) | Real field loads, but no consumer found: no `bl`/`blx`/`b.w`, short branch, ARM branch, raw pointer or `movw`/`movt` reference to it anywhere in the image. Its neighbours (`0x10354376`, `0x1035437c`, `0x10354388`, `0x10354394`, `0x1035439a`, `0x103543a0`, `0x103543ac`, `0x103543b8`) all have many callers, so this is an unreferenced entry, not a scanner gap. |
| Second table | No pointer-slot load. Ruled out as reachable by these methods. |
| Anchor-relative readers of F-129 (`0x10360876`, `0x103608c6`, `0x103608fa`) | Not filename consumers (halfword format/flag lookups). Ruled out. |

## Interpretation and limits

- The first table has exactly one reader, and it is statically orphaned. Likely
  explanations, not tested: it is dead code in this build; it is reached
  through a computed address (a table of offsets or an address built some way
  this scan does not model); or the filename pointers are consumed through a
  copy of the block made elsewhere. A block copy of the whole structure was
  not excluded: a `memcpy`-style reader would not show a slot-specific load.
- The scan models Thumb literal loads with `adds`/`mov` propagation and a
  96-640 byte window. It does not model indirect jumps or loads where the base
  comes from a call result.
- Whoever builds the real file name today is therefore not identified. The
  filename-template table at `0x11c9a5fc` may be read directly rather than
  through the two pointer tables; F-110/F-111 found no code consumer of the
  template strings beyond these two tables.
- This does not choose a crop patch. Nothing here shows where saved
  dimensions or a crop region are chosen.

## Next step (single)

Trace the pointer data one level out: search the image for direct references
to the template strings (`0x11c9a5fc`-`0x11c9a63c`), including the individual
entry addresses at `0x11c9a60c`, `0x11c9a61c` and `0x11c9a62c`, and for loads
of the first table's whole 40-byte structure by block copy, and check callers
of `0x10354350` through indirect `blx` registers loaded from tables. If those
also come back empty, mark the filename-table route low priority and return to
the real file-creation boundary by another door (the card-write path that
real firmware must use), per AGENTS.md's priority rule.
