# ael_ok: AE-L/AF-L to OK (draft, untested)

SD module for Wonder Lantern's research module host. See
[the plan](../../docs/one-button-tracking-plan.md#update-2026-11-17-upstream-pr-36).

Status: compiles with `arm-none-eabi-gcc` and passes the build script's
position-independence check. It has not run in any emulator or on a camera.

    sh build.sh ael_ok.bin            # log only
    sh build.sh ael_ok.bin -DREMAP    # also send OK on each AE-L/AF-L press

The OK is sent only in Auto-area AF (AF-area mode byte `0xC237C7F8` = 6),
the gate upstream PR #36 added in its review revision. The log records the
mode for every press, so a log-only run also shows whether the gate reads
correctly.

Built here with `arm-none-eabi-gcc 13.2.1 (13.2.rel1)`. Upstream's review
found a different compiler version produced a different module size, so
record the version you build with.

The header and linker script are copied from WonderLantern/wonder-lantern-z30
(MIT). Built `.bin` files stay out of Git.
