# Caller search for the getter at 0x10354350

2026-10-17. Static analysis of the original firmware image only. No simulator,
no QEMU, no firmware change, no camera. Only addresses and descriptions appear
here. Follows [lane2-filename-trace.md](lane2-filename-trace.md) (F-131,
F-132 on the unmerged lane 2 branch).

**Verdict: not found.** No route from any part of the image reaches the getter
at `0x10354350`. Every route class below returned zero matches. Confidence is
high for direct and literal-pool references, and medium overall because
computed-address dispatch is not modelled (see Limits).

## Target

The getter `0x10354350` is the first filename table's selector getter from the
lane 2 note. It is a Thumb function that returns one of the four filename
template pointers. Its body was not re-decoded here; only its entry address
matters for this search.

## Method

1. A helper script lives outside the repository, in the session scratch
   directory, and is not committed. It reads the private firmware input
   read-only, at base `0x10020000`, through the analysis environment's
   capstone. It prints route names, addresses and short descriptions only.
2. Route classes, each scanned over the whole image:
   - Thumb wide branches: `bl`, `blx` immediate, `b.w`, and conditional
     `b<cc>.w`, each with its own offset formula.
   - Thumb short branches: `b` and conditional `b<cc>`.
   - ARM branches: `b`/`bl` (4-byte aligned) and `blx` immediate.
   - Raw 32-bit words equal to the target with and without the Thumb bit. This
     covers literal-pool words, function-pointer tables, callback tables and
     vector tables.
   - `movw`/`movt` pairs that build the target, in Thumb and ARM forms,
     within 16 bytes.
   - `adr` (Thumb form) producing the target address.
   - Table-branch sites (`tbb`/`tbh`): each site's first 128 table entries are
     checked for a target equal to the getter. These are candidates only.
   - Fall-through into the entry: the instruction before the entry is checked
     for a non-returning transfer.
3. Validation. The scanner was run on the known getter `0x10360bba`. It finds
   498 direct Thumb call sites, the same count the lane 2 note reports. It was
   also run on three neighbouring entries, `0x10354376`, `0x1035437c` and
   `0x10354388`. Each has direct callers, so the scanner works in this region.

## Results for 0x10354350

| Route class | Matches | What it is |
| --- | --- | --- |
| Thumb wide branches (`bl`, `blx`, `b.w`, `b<cc>.w`) | 0 | No direct call or tail branch. |
| Thumb short branches (`b`, `b<cc>`) | 0 | No short branch. |
| ARM `b`/`bl`/`blx` immediate | 0 | No ARM-mode reference. |
| Raw words equal to the target (either Thumb bit) | 0 | No literal-pool, pointer-table, callback-table or vector-table entry holds the address. |
| `movw`/`movt` construction (Thumb and ARM) | 0 | No code builds the address. |
| `adr` producing the target | 0 | No PC-relative address calculation reaches it. |
| `tbb`/`tbh` table candidates | 0 | No bounded table entry decodes to it. |
| Fall-through into the entry | 0 | The instruction before the entry is a return, so control cannot fall through. |

**Routes found: none.** The table of routes above is the full list of classes
checked; each one is empty.

## Table-dispatched callbacks

The question asked whether the address could sit in a callback table reached
by an indexed indirect call. A table holding the address would appear in the
raw-word route, and that route is empty. So no table entry holds the getter,
and no indexed indirect call can reach it through a stored pointer.

## Limits

- Computed addresses are not modelled. A pointer built by arithmetic on a
  base register, or read from a table of base-relative offsets (not absolute
  addresses), would not show up in the raw-word route. Such a table was not
  searched.
- Block copies of the first table's structure would not show a
  slot-specific load and would not show a call to the getter. The lane 2
  note already flags this.
- Indirect calls through a register whose value comes from a call result
  are not followed.
- The `tbb`/`tbh` route was bounded to 128 entries per site and treated as
  candidates. None matched.

## Consequence for the filename-table route

The getter has no reachable caller found by any static route in this image.
The lane 2 note's next step was to check indirect calls through tables; that
check is now done and came back empty for the getter. The lane 2 note
recommended marking the filename-table route low priority if this came back
empty, which it did. Under AGENTS.md's priority rule, the next work should be
the real file-creation boundary (the card-write path), not further tracing of
this getter.

Hardware remains NO-GO.
