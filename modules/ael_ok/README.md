# ael_ok: AE-L/AF-L acts as OK (draft, untested)

SD module for Wonder Lantern's research module host. With it loaded, one
press of AE-L/AF-L on the shooting screen counts as one press of OK. In
Auto-area AF, OK starts Subject tracking. With upstream's 3D tracking turned
on and AF-area mode set to Auto-area AF (people) or (animals), that tracking
also switches to a face or animal that comes into view. See
[the plan](../../docs/one-button-tracking-plan.md).

Status: compiles with `arm-none-eabi-gcc 13.2.1 (13.2.rel1)` and passes the
build script's position-independence check. It has not run in an emulator or
on a camera. Upstream's review found that a different compiler version
produced a different module size, so record the version you build with.

## When it sends OK

All of these must hold for a new AE-L/AF-L press:

- The module was built with `-DREMAP` and armed with Run.
- The camera is on the shooting screen (UI phase byte 1 or 2, the check
  upstream's 3D tracking boxes use).
- AF-area mode is Auto-area (mode byte 6, the check upstream added in its
  review revision).

Without `-DREMAP` it only logs. Each logged press records the AF-area mode and
the UI phase, so a log-only run also shows whether both checks read correctly.

## Build (on the Mac, with the stock firmware)

Use upstream PR #36 at commit `2a8f83f` or later. Its `log` research build is
`full` without gyro-evr, plus the module host and the IMU-task hook this
module uses. It includes 3D tracking. Gyro-evr is left out because it owns
the same hook; it only affects video.

    python3 tools/build_af_log.py --source Z_30_0120.bin --output OUT --no-zmod
    sh /path/to/nikon-z30-research/modules/ael_ok/build.sh ael_ok.bin           # log only
    sh /path/to/nikon-z30-research/modules/ael_ok/build.sh ael_ok.bin -DREMAP   # sends OK
    python3 tools/prepare_module.py --code ael_ok.bin --output OUT/Z30/CORE.ZMOD

On the camera: Setup → Extensions → SD Modules, Load `CORE.ZMOD`, then Run to
arm. Run again to disarm and save `Z30/AEnnnnnn.BIN`. Power off disarms.

## Test order

1. Log-only build. On the shooting screen in Auto-area AF, press AE-L/AF-L a
   counted number of times, then save. The log's press count should match.
2. Only then the `-DREMAP` build. Check that each press acts like OK, and that
   nothing happens in menus, playback, or other AF-area modes.
3. Turn on 3D tracking (Enable, people/animals) and repeat with a face
   walking into view.

Every step that touches the camera needs the owner's go-ahead. Upstream
froze a camera once with a module bug (battery pull needed), so keep the
log-only step first.

The header and linker script are copied from WonderLantern/wonder-lantern-z30
(MIT). Built `.bin` files stay out of Git.
