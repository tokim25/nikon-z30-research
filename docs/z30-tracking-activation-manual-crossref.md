# Subject tracking on the Z30: manual vs. our firmware route (cross-reference)

2026-10-18. Claude, read-only. Manual lookup plus a read of the repo's existing
static analysis. No simulator run (the simulator is on the owner's machine, not
in this session, and the record shows it cannot press these buttons or start
tracking). No firmware bytes. This note is a lead for the Codex/local session;
it is uncommitted and is not a research finding in `facts.md`.

## Headline: the activation input in our tracking lane may not exist on the Z30

Our tracking research is built around an **AE-L/AF-L button** press as the
activation input. The Z30 manual and Z30 owner reports indicate the camera has
**no dedicated AE-L/AF-L button**. If that holds, the native way a user starts
subject tracking is a different control, and part of the tracking lane has been
tracing the wrong input. This is a lead to verify against the firmware, not a
proven overturn: the manual pages were read through search snippets that were
partly garbled, the owner reports are anecdotal, and no firmware was read here.

## What the manual says a user does today

Observed, from Nikon's Z30 Reference Guide:

- Subject tracking runs when **AF-area mode is set to Auto-area AF** (or
  Auto-area AF people / animals); the camera tracks the subject in the focus
  point. ([Focus, 05-01](https://onlinemanual.nikonimglib.com/z30/en/05-01.html))
- In other AF-area modes, the user **presses OK** to start tracking: the focus
  point becomes a targeting reticle and the display switches to a
  subject-tracking view. ([g2 Custom controls, 09-05-47](https://onlinemanual.nikonimglib.com/z30/en/09-05-47.html))
- In an Auto-area mode the OK button **only** starts subject-tracking AF,
  whatever role it is otherwise assigned. ([g2, 09-05-47](https://onlinemanual.nikonimglib.com/z30/en/09-05-47.html))
- AF-area mode is changed from the **i menu** or the shooting menu, or by
  default by **holding Fn2 and turning the sub-command dial**. ([05-01](https://onlinemanual.nikonimglib.com/z30/en/05-01.html))
- The OK button's default role is Zoom on/off, so tracking-on-OK is the
  auto-area behavior, not the global default. ([Defaults, 09-01](https://onlinemanual.nikonimglib.com/z30/en/09-01.html))

Z30 physical controls that can take a role: **Fn1** (default white balance),
**Fn2** (default focus / AF-area mode), **OK**. Owner reports say AF-L / back-
button AF is not offered on the Z30, while Fn1/Fn2 are.
([Camera controls, 02-02](https://onlinemanual.nikonimglib.com/z30/en/02-02.html);
[DPReview, Z30 AE-L/AF-L reassignment](https://www.dpreview.com/forums/thread/4738871))

## What our firmware route has, from existing static analysis

From `firmware-map-deep-2026-10-17.md` and `tracking-activation-path.md` (no new
decode here):

- Subject tracking is the **AF-area-mode subsystem**, 3D-TRACKING mode. Label
  table `0x103edda0`, 3D-TRACKING label `0x103eddfc`; settings `AfAreaMode*`,
  `AfTrackingSensitivity*`.
- The traced AE-L/AF-L input path (detection side): handler `0x103a3d14`
  (mask `0x2000` to logical ID 41), dispatcher `0x103a3b9c` (reads SW-bank word
  `0x115c694c`), consumer `0x103a3f9e`, setter `0x101e383a`, structured record
  `0xc1811e74`. Governed by `eDSID_Setting_FuncAeAfLockButtonShooting`.
- The press-to-tracking chain is not closed. Event `0x2021`'s posting side is
  traced, its consumer is not, and no OK-button tracking routine was found.

## Why the two do not line up

The firmware's switch table names an AE-L/AF-L bit (`SW0` bit `0x2000`) because
it is a shared EXPEED/platform table used across Nikon bodies, many of which do
have that button. A bit existing in that table is not proof the Z30 exposes the
physical button. The manual says the Z30 user starts tracking through Auto-area
AF and the OK button, and our own trace never connected the AE-L/AF-L event to a
tracking start, nor found an OK-button tracking routine. Both point the same
way: the AE-L/AF-L framing is probably not the Z30's real activation route.

## Suggested next trace (for the session that has the firmware)

Aim the static trace and any simulator breakpoint at the OK / auto-area route,
not the AE-L/AF-L button:

1. From the AF-area label table `0x103edda0` and the 3D-TRACKING label
   `0x103eddfc`, resolve the **AF-area-mode set function** (what writes the
   current AF-area mode when the i menu or Fn2 changes it).
2. Find where an **Auto-area AF** selection arms subject tracking, and where the
   **OK/J key** starts tracking in the non-auto modes. The OK key dispatcher
   `0x103ce96e` is already noted as receiving OK in the simulator; follow it
   toward the tracking entry rather than treating AE-L/AF-L as the trigger.
3. The i menu is drivable in the simulator, so a breakpoint on the AF-area-mode
   set function is a more promising probe than a button press, which the
   simulator cannot deliver.

## Limits

- No firmware read, no simulator run, no camera contact in this note.
- Manual detail came from search snippets, partly garbled; confirm on the camera
  or the full manual before relying on exact option names.
- Owner-report claims about the missing AE-L/AF-L button are anecdotal.
- Tracking is the Codex lane; this note is a manual-side cross-reference for
  that session to act on, not a change to the tracking research itself.

Written by Claude in collaboration with Tony Kim.
