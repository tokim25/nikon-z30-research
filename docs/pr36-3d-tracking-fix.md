# Proposed fix for PR #36's 3D tracking regression

Date: 2026-11-17. Written by Claude from this repository's findings and the
PR's code at `2a8f83f`. Nothing here has been built or run: building needs
the stock firmware, which this session does not have.

## The regression

PR #36 revision 6 (`2a8f83f`) only sets the touch-start flag when a
people/animal check passes. To make that check, it calls the stock settings
getter `0x10465984` with key `0x58B`, or `0xC3C` when AF display block
`+0x3FD` is set, and accepts 1 (people) or 2 (animals). On a camera in
Auto-area AF (people), the handover stopped working. The reviewer
(RealCaCl2) suspects the key choice and a missing `uxtb`.

## What this repository found

The stock AF-area mode setter `0x1042b2d8` maps the three Auto-area menu
choices (encodings 600, 601 and 602) to base mode 6 in property `0x0c2b` and
submode 0, 1 or 2 in property `0x0c3d` (F-215, F-231,
F-329). Plain Auto-area is submode 0, people is 1 and
animals is 2. The stock menu consumer `0x10489832` reads `0x0c3d` for the
people/animal label when base mode is 6 (F-343).

So the Auto-area people/animal setting looks like key `0x0C3D`. The PR reads
`0x0C3C` or `0x058B`, one off and a different key. That fits the camera
result: the check never sees 1 or 2, so the flag is never set.

Unverified: that the PR's getter `0x10465984` uses the same key space as these
properties. The keys are in the same range, but this repository never traced
that getter.

## Proposed change

In `src/z30_extensions/features/tracking3d.py`, replace the two lines that
pick the key and call the getter with one fixed key, and truncate the result
to a byte as the reviewer suggested:

```diff
-DETECT_SELECT = AF_DISPLAY + 0x3FD   # 0x1039CC18: non-zero -> setting 0xC3C, else 0x58B
-DETECT_KEYS = (0x58B, 0xC3C)
+AUTO_SUBMODE = 0xC3D            # Auto-area submode: 0 plain, 1 people, 2 animals
 GET_SETTING = 0x10465984        # stock settings getter (r0 = key)
```

```diff
-        {c('r1',DETECT_SELECT)}ldrb r1,[r1];{c('r0',DETECT_KEYS[0])}cmp r1,#0;beq detect_key;{c('r0',DETECT_KEYS[1])}
-        detect_key:{invoke(GET_SETTING)}subs r0,#{PEOPLE};cmp r0,#{ANIMALS - PEOPLE};bhi out;
+        {c('r0',AUTO_SUBMODE)}{invoke(GET_SETTING)}uxtb r0,r0;subs r0,#{PEOPLE};cmp r0,#{ANIMALS - PEOPLE};bhi out;
```

The build report's `detection_keys` entry also needs to become
`hex(AUTO_SUBMODE)`. The Unicorn test in `tests/test_tracking3d.py` stubs the
getter by key, so it needs the new key too.

## How to check it

1. Build `full` from the patched branch and run upstream's tests.
2. On a camera, in Auto-area AF (people), start tracking on an object and let
   a face walk into the box. It should switch, as `c01e7ca` did.
3. In plain Auto-area AF, the same test should keep stock behavior (no
   switch). This is the case revision 6 was added for.

If step 2 fails, use the reviewer's fallback: keep only the AF-area mode 6
check, which brings back the plain Auto-area problem.

## Draft comment for PR #36

> Possible cause for the revision 6 regression, from separate research on the
> same firmware (not built or run here): the stock AF-area setter `0x1042b2d8`
> stores the Auto-area choice as base mode 6 in property `0x0C2B` and submode
> 0 / 1 / 2 (plain / people / animals) in property `0x0C3D`, and the stock menu
> code `0x10489832` reads `0x0C3D` for the people/animal label when the base
> mode is 6. Revision 6 reads `0x0C3C` or `0x058B`. If `0x10465984` takes the
> same keys, reading `0x0C3D` (with `uxtb`) may fix it. I haven't confirmed
> that the getter uses the same key space.

Written by Claude in collaboration with Tony Kim.
