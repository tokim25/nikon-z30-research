# Native XPan live-view hook research

Date: 2026-10-16. Firmware C1.20, offline assisted simulator only. No camera
was used, and this work does not produce an installable firmware image.

## Result

A private QEMU loader overlay proved that a small native hook can make the
existing screen-layer mask follow the stored image-area choice. The overlay
loads synthetic code and data before the CPU starts. The debugger does not
write the hook, the mask flag, the mask bounds, the color or the image-area
choice during the run.

With 1:1 selected as the stand-in for XPan, the mask was on in live view and
off while a menu was active. DX and 16:9 kept the mask off. Ten alternating
menu/live-view signal cycles passed without changing the mask bounds or the
screen-stack count.

A follow-up tested the final menu-close path. Two stock internal events
closed the last screen-stack entry, but both requested mode `0x10000` rather
than the live-view target `0x100000`. The resulting simulated screen was not
a verified live-view return. An early close wrapper enabled the mask there,
so that version was rejected.

The final private overlay guards the close path. That path applies the mask
only when the screen stack is empty and the live-view object selector is 1.
The same non-live-view close control then kept the mask off. Direct area
changes and ten menu/live-view signal cycles still passed.

This establishes usable instruction space and a working trigger layout in
the simulator. It does not establish that the same locations are safe on
camera hardware.

## Image-area writer

The property callback for image-area property `0x501` reaches a function at
`0x1008d38c`. Its store at `0x1008d3fc` updates the record whose choice byte
is at `0xc1811d90`. The stored values observed in the simulator are:

| Choice | Stored byte |
|---|---:|
| DX | 0 |
| 1:1, used as XPan | 1 |
| 16:9 | 2 |

This corrects the older design note that treated 4 as the stored XPan value.
Four is an argument used by the 1:1 property callback, not the final byte at
`0xc1811d90`.

The setter return is the earliest tested point where the new choice is
available. The menu's first callback return is too early: the confirmed
choice byte still has its old value there.

## Candidate instruction space

Read-only static scans found four zero-filled spans that can hold the small
wrappers used by the prototype:

| Range | Size | Boundary evidence |
|---|---:|---|
| `0x1002d78c..0x1002d7bf` | 52 bytes | The prior ARM function returns before the span; its two literals follow the span. |
| `0x1002d80c..0x1002d83f` | 52 bytes | The prior ARM delay loop returns at `0x1002d808`; the next ARM function starts at `0x1002d840`. |
| `0x1002d860..0x1002d87f` | 32 bytes | The prior ARM function and its literals end before the span. |
| `0x1027f468..0x1027f47f` | 24 bytes | The prior ARM wrapper returns at `0x1027f464`; the next Thumb function starts at `0x1027f480`. |

No aligned literal or table reference into these spans was found. A
conservative mixed-mode branch scan reported apparent references caused by
decoding ARM instructions as Thumb, or Thumb instructions as ARM. Manual
review in the surrounding function's actual mode rejected those hits.

The simulator maps the firmware region as executable ROM, and all four spans
executed there. Hardware execution permissions, hidden references and
loader behavior remain inferred. Confidence is high for the simulator and
medium for the static insertion-space assessment.

## Trigger layout tested

The final private prototype used six small routines:

1. A mask helper reads `0xc1811d90`. It enables the existing mask flag only
   when the choice is 1 and sets the retained layer color when enabling it.
2. A screen-state wrapper runs at the generic screen activation tail. It
   calls the mask helper for the live-view object and clears the flag for
   other screen objects.
3. A guard checks that the screen stack is empty and that the live-view
   object's selector byte at `0xc1821db8` is 1.
4. An image-area setter wrapper runs after the store at `0x1008d3fc`, then
   calls the guard.
5. A live-view-ready wrapper runs at `0x102f5810`, where the firmware sets
   the live-view object selector to 1, then calls the guard.
6. A screen-close wrapper runs after the stock phase-3 close callback at
   `0x102355c0`, then calls the guard.

The hook sites were the screen activation tail at `0x102355f4`, the close
callback at `0x102355c0`, the live-view-ready selector call at `0x102f5810`,
and the image-area setter return at `0x1008d3fe`. The screen-state path
distinguishes the live-view signal object at `0xc1821d64` from other screen
objects.

The screen-stack check is important. A real menu pick changes the stored
choice before the menu has closed. Updating the mask unconditionally at the
setter return would draw bars over the menu, which violates the design.

## Simulator evidence

These checks used the private loader overlay:

- Direct calls to the stock image-area callbacks produced the sequence 1:1,
  DX, 1:1, 16:9. The stored byte became 1, 0, 1, 2 and the mask flag became
  on, off, on, off.
- A real menu pick changed DX to 1:1 while the mask stayed off over the menu.
  An audited live-view activation then enabled it. Screen rows 0 through 106
  and 373 through 479 were black; rows 107 through 372 were not fully black.
  Ten menu/live-view signal cycles alternated the flag correctly.
- A 16:9 control kept the flag off in the menu and after live-view
  activation. No full-width black mask rows appeared.
- The guarded build repeated the direct 1:1, DX, 1:1, 16:9 sequence and all
  four expected mask states passed. Ten menu/live-view signal cycles also
  passed.
- A final-screen control used stock event `0x250`. It removed the last stack
  entry but left the live-view selector at 4. The guard kept the mask off.
  The rejected unguarded version had turned it on in the same non-live-view
  state.

The original firmware hash remained
`8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`, and
the pinned QEMU checkout remained clean.

## Limits

The successful menu test used an audited screen-activation call after the
pick. A true return from the menu to live view has not been observed. The
simulator's exposed Back key cannot close the last menu screen. Internal
events `0x24e` and `0x250` close it, but both request mode `0x10000` and do
not reach the live-view-ready transition. Their physical-button identities
are unknown. The assisted fixture also bypasses the natural caller of
`0x102f57e2`, so the hook at its selector-1 call is statically checked but
not observed through that caller.

The simulator exposes no `i` button. The immediate-update test therefore
called the exact stock row callbacks while live view remained active; it did
not drive the camera's real `i`-menu path.

One earlier hypothesis failed. A later menu notification callback was not a
general image-area-change trigger: direct stock property callbacks changed
the choice without reaching it. The final prototype uses the exact writer
instead. QEMU write watchpoints also failed a self-test on a known direct
store, so they were not used as evidence.

This work satisfies the instruction-space and native-execution part of
build-gate condition 1 in the assisted simulator. The unsafe broad close
trigger was found and rejected, and the guarded replacement passed its
available controls. It does not make the hardware gate pass. Natural
transition coverage and hardware safety remain open, and
[hardware-readiness.md](hardware-readiness.md) still controls any camera
work.

## Reproduction

These commands use the confirmed private `WORK` directory. They create only
fresh `codex-` output under that directory. The scripts, loader overlay and
run output stay private and must never enter Git.

```sh
WORK=/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-linker-gaps-private.py" --firmware "$WORK/private-inputs/eg2090_0120a0.bi" --output "$WORK/private-inputs/codex-linker-gaps-reproduce-01" --minimum 12
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-choice-module-trace-private.py" --output "$WORK/private-inputs/codex-choice-module-trace-reproduce-01"
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-xpan-hook-build-private.py" --firmware "$WORK/private-inputs/eg2090_0120a0.bi" --output "$WORK/private-inputs/codex-xpan-hook-overlay-reproduce-01"
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-xpan-hook-run-private.py" --overlay "$WORK/private-inputs/codex-xpan-hook-overlay-reproduce-01" --output "$WORK/private-inputs/codex-xpan-hook-direct-reproduce-01" --direct-only
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-xpan-hook-run-private.py" --overlay "$WORK/private-inputs/codex-xpan-hook-overlay-reproduce-01" --output "$WORK/private-inputs/codex-xpan-hook-menu-reproduce-01" --downs 1 --cycles 10
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-xpan-guarded-hook-build-private.py" --firmware "$WORK/private-inputs/eg2090_0120a0.bi" --output "$WORK/private-inputs/codex-xpan-guarded-overlay-reproduce-01"
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-xpan-hook-run-private.py" --overlay "$WORK/private-inputs/codex-xpan-guarded-overlay-reproduce-01" --output "$WORK/private-inputs/codex-xpan-guarded-direct-reproduce-01" --direct-only
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" "$WORK/codex-xpan-menu-event-return-private.py" --overlay "$WORK/private-inputs/codex-xpan-guarded-overlay-reproduce-01" --exit-event 0x250 --output "$WORK/private-inputs/codex-xpan-guarded-close-reproduce-01"
```

The simulated OK press sometimes hangs. If that happens, stop the disposable
process and rerun with a new output directory.

## Single next step

Find a simulator input path that reaches the live-view-ready transition at
`0x102f57e2` after the menu closes, then confirm that the guarded hook restores
the mask without an audited activation call.

Written by Codex in collaboration with Claude and Tony Kim.
