# auto_arm: tracking box up by default (working on a camera as an SD add-on)

SD module for Wonder Lantern's research module host. On the shooting screen in
Auto-area AF, it puts the camera into the tracking-ready screen (the reticle
that OK brings up) without a button press. A half-press then starts tracking.
With upstream's 3D tracking turned on and AF-area mode set to Auto-area AF
(people) or (animals), tracking switches to a face or animal that comes into
view. No button is remapped; AE-L/AF-L keeps its normal job. See
[the plan](../../docs/one-button-tracking-plan.md).

Status, 2026-11-17: the `DIRECT` build works on the owner's Z30 with upstream
PR #36 `8715c25`. The box appears about 0.4 s after the shooting screen opens,
and the add-on leaves the i menu, menus, playback, video and other AF-area
modes alone (F-380, F-381). Built with `arm-none-eabi-gcc` 15.3.1 (Arm GNU
Toolchain 15.3.Rel2); it was first written against 13.2.1. Upstream's review
found that compiler versions change the module size, so record yours.

## How it works

About every 50 ms it checks that the camera is:

- in photo live view with nothing open over it: UI phase 1 or 2, UI state 0
  (the i menu sets it to 3) and the photo backend active. Upstream's portrait
  UI and aspect mask use this same check, confirmed on a camera;
- in photo, not video: byte `0xC237CBB1` is 0. On the owner's Z30 the photo
  backend word stays 1 in video, so it cannot tell them apart;
- in Auto-area AF (AF-area mode byte 6; Wide-area AF (L-people) reads 4);
- idle: not focusing, not tracking, and the tracking box not already shown.

If all of that holds for two checks in a row (six after coming back from
another screen, about 300 ms), the `DIRECT` build calls the stock function
the OK button uses to enter the tracking mode, `0x1045A1AE`. Builds without
`DIRECT` send a synthetic OK instead, which brought the box up only about 1
time in 10 on the camera. It then waits until the tracking box appears, or
about 1.5 seconds, before checking again. When tracking ends
or you back out of the tracking box, it brings the box back right away (owner
choice). To stop it, Run it again to disarm, leave Auto-area AF, or power off.

## Build (on the Mac, with the stock firmware)

Use upstream PR #36 at `8715c25` or later. That commit reads the Auto-area
submode from `0xC3D` to fix the 3D tracking regression in `2a8f83f`, but the
fix has not been confirmed on a camera yet. The module itself does not
depend on 3D tracking working, so a dry run can go ahead either way. Its `log` research build is
`full` without gyro-evr, plus the module host and the IMU-task hook this
module uses. It includes 3D tracking. Gyro-evr is left out because it owns
the same hook; it only affects video.

    python3 tools/build_af_log.py --source Z_30_0120.bin --output OUT --no-zmod
    sh /path/to/nikon-z30-research/modules/auto_arm/build.sh auto_arm.bin           # dry run
    sh /path/to/nikon-z30-research/modules/auto_arm/build.sh auto_arm.bin -DREMAP   # presses OK
    python3 tools/prepare_module.py --code auto_arm.bin --output OUT/Z30/CORE.ZMOD

On the camera: Setup → Extensions → SD Modules, Load `CORE.ZMOD`, then Run to
arm. Run again to disarm and save `Z30/ARnnnnnn.BIN`. Power off disarms.

## Reading the log

    PYTHONPATH=src python3 -m nikon_z30_research.auto_arm_log ARnnnnnn.BIN

Run from the `nikon-z30-research` root. It lists each entry with its state
values and marks any entry outside photo live view in Auto-area AF as
UNEXPECTED (exit code 1).

## Test order

1. Dry run (no `-DREMAP`): presses nothing. While idle on the shooting screen
   it logs a "would press" entry about every 1.6 seconds, with the UI phase,
   UI state, photo backend and AF-area mode. Spend time on the shooting screen, in the i menu,
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
