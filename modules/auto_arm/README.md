# auto_arm: tracking box up by default (draft, untested)

SD module for Wonder Lantern's research module host. On the shooting screen in
Auto-area AF, it puts the camera into the tracking-ready screen (the reticle
that OK brings up) without a button press. A half-press then starts tracking.
With upstream's 3D tracking turned on and AF-area mode set to Auto-area AF
(people) or (animals), tracking switches to a face or animal that comes into
view. No button is remapped; AE-L/AF-L keeps its normal job. See
[the plan](../../docs/one-button-tracking-plan.md).

Status: compiles with `arm-none-eabi-gcc 13.2.1 (13.2.rel1)` and passes the
build script's position-independence check. It has not run in an emulator or
on a camera. Upstream's review found that a different compiler version
produced a different module size, so record the version you build with.

## How it works

About every 50 ms it checks that the camera is:

- on the shooting screen (UI phase byte 1 or 2, the check upstream's 3D
  tracking boxes use);
- in Auto-area AF (AF-area mode byte 6);
- idle: not focusing, not tracking, and the tracking box not already shown.

If all of that holds for two checks in a row, it sends one OK press, using the
method upstream's research made work on a Z30. It then waits until the tracking
box appears, or about 1.5 seconds, before checking again. When tracking ends
or you back out of the tracking box, it brings the box back right away (owner
choice). To stop it, Run it again to disarm, leave Auto-area AF, or power off.

## Build (on the Mac, with the stock firmware)

Use upstream PR #36 at commit `2a8f83f` or later. Its `log` research build is
`full` without gyro-evr, plus the module host and the IMU-task hook this
module uses. It includes 3D tracking. Gyro-evr is left out because it owns
the same hook; it only affects video.

    python3 tools/build_af_log.py --source Z_30_0120.bin --output OUT --no-zmod
    sh /path/to/nikon-z30-research/modules/auto_arm/build.sh auto_arm.bin           # dry run
    sh /path/to/nikon-z30-research/modules/auto_arm/build.sh auto_arm.bin -DREMAP   # presses OK
    python3 tools/prepare_module.py --code auto_arm.bin --output OUT/Z30/CORE.ZMOD

On the camera: Setup → Extensions → SD Modules, Load `CORE.ZMOD`, then Run to
arm. Run again to disarm and save `Z30/ARnnnnnn.BIN`. Power off disarms.

## Test order

1. Dry run (no `-DREMAP`): presses nothing. While idle on the shooting screen
   it logs a "would press" entry about every 1.6 seconds, with the screen
   phase and AF-area mode. Spend time on the shooting screen, in the i menu,
   in the menus, in playback, and in another AF-area mode, noting the times.
   Entries should only appear for the shooting screen in Auto-area AF.
2. Only then the `-DREMAP` build. Check that the tracking box appears on its
   own, that a half-press starts tracking, that the box returns when tracking
   ends, and that menus and playback are untouched.
3. Turn on 3D tracking (Enable, people/animals) and repeat with a face
   walking into view.

Every step that touches the camera needs the owner's go-ahead. Upstream
froze a camera once with a module bug (battery pull needed), so keep the dry
run first.

The header and linker script are copied from WonderLantern/wonder-lantern-z30
(MIT). Built `.bin` files stay out of Git.
