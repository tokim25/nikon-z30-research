# ael_ok: AE-L/AF-L to OK (draft, untested)

SD module for Wonder Lantern's research module host. See
[the plan](../../docs/one-button-tracking-plan.md#update-2026-11-17-upstream-pr-36).

Status: compiles with `arm-none-eabi-gcc` and passes the build script's
position-independence check. It has not run in any emulator or on a camera.

    sh build.sh ael_ok.bin            # log only
    sh build.sh ael_ok.bin -DREMAP    # also send OK on each AE-L/AF-L press

The header and linker script are copied from WonderLantern/wonder-lantern-z30
(MIT). Built `.bin` files stay out of Git.
