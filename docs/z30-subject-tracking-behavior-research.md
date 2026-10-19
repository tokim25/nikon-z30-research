# How Z30 subject tracking activates today: behavioral research

2026-10-18. Claude, public-source research (Nikon's Z30 Reference Guide and
corroborating sources). No simulator run, no firmware read, no camera contact.
This defines the on-camera behavior the firmware trace must match. It is a
manual-side research note, not a firmware finding, and it is not in `facts.md`.

## The short version

A Z30 user starts subject tracking by **selecting an Auto-area AF mode and
pressing OK**, or by **half-pressing the shutter in AF-C/AF-A**. There is no
AE-L/AF-L or AF-ON button on the body to do it. So the firmware entry point to
find is an **OK/J key press combined with the current AF-area-mode state**, not
a dedicated tracking button.

## AF-area modes and which ones track

The Z30 has ten AF-area modes. Pinpoint and dynamic-area are photo-only.
([Focus, 05-01](https://onlinemanual.nikonimglib.com/z30/en/05-01.html);
[Specifications, 15-08](https://onlinemanual.nikonimglib.com/z30/en/15-08.html))

| AF-area mode | Tracks a moving subject? |
| --- | --- |
| Pinpoint (photo only) | No, stationary |
| Single-point | No, stationary |
| Dynamic-area (photo only) | Follows motion using surrounding points if the subject leaves the point |
| Wide-area (S) / (L) | Holds focus on subjects in the area; wide-L has people and animal variants |
| Auto-area, Auto-area (people), Auto-area (animals) | Yes, the camera tracks the subject in the selected focus point |

Subject detection (faces, eyes, animals) applies in the wide-area and auto-area
families. The exact Z30 subject-detection list was not confirmed from these
sources. ([Focus, 05-01](https://onlinemanual.nikonimglib.com/z30/en/05-01.html))

## How a user starts and stops tracking

The manual describes two routes.

The first is Auto-area AF plus OK. With Auto-area AF (or its people/animals
variants), pressing the control turns the focus point into a targeting reticle
and switches the monitor to a subject-tracking display. The user positions the
reticle and presses OK to lock onto the subject; the box then follows it across
the frame. To stop, the user presses the control again or presses the Q / trash
button. ([Focus, 05-01](https://onlinemanual.nikonimglib.com/z30/en/05-01.html);
[g2 Custom controls, 09-05-47](https://onlinemanual.nikonimglib.com/z30/en/09-05-47.html))

The second is a half-press in AF-C or AF-A. If tracking is initiated by a
half-press of the shutter in those focus modes, the camera tracks only while
the shutter stays half-pressed, and releasing it ends tracking.
([Focus, 05-01](https://onlinemanual.nikonimglib.com/z30/en/05-01.html))

Focus modes on the Z30 are AF-S, AF-C, AF-A (photo only), AF-F (video only), and
MF. AF-S locks focus on a half-press (point turns red to green); AF-C adjusts
continuously while half-pressed; AF-A auto-switches between them.
([Focus, 05-01](https://onlinemanual.nikonimglib.com/z30/en/05-01.html))

Related tuning: Custom Setting **a3 (focus tracking with lock-on)** sets how
quickly focus reacts when something crosses between subject and camera in
AF-C/AF-A; **g4 (AF tracking sensitivity)** applies in video.
([a3, 09-05-04](https://onlinemanual.nikonimglib.com/z30/en/09-05-04.html);
[g4, 09-05-50](https://onlinemanual.nikonimglib.com/z30/en/09-05-50.html))

## Where the control choice is set

- AF-area mode is changed from the **i menu** or the shooting menu, or by
  default by **holding Fn2 and turning the sub-command dial**.
- Custom Setting **g2 (Custom controls)** assigns roles to Fn1, Fn2, and OK. The
  OK button's default role is **Zoom on/off**. Whatever role OK is given, in an
  Auto-area AF mode the button **only** starts subject-tracking AF.
  ([g2, 09-05-47](https://onlinemanual.nikonimglib.com/z30/en/09-05-47.html);
  [Defaults, 09-01](https://onlinemanual.nikonimglib.com/z30/en/09-01.html))
- The Z30 body has no dedicated AE-L/AF-L or AF-ON button; owners report AF-L
  and back-button AF are not offered, while Fn1/Fn2 are.
  ([Camera controls, 02-02](https://onlinemanual.nikonimglib.com/z30/en/02-02.html);
  [DPReview, Z30 AE-L/AF-L reassignment](https://www.dpreview.com/forums/thread/4738871))

## What this means for the firmware hook

The activation is a state plus a key event, not a dedicated button. The state is
that the current AF-area mode is an Auto-area variant (or the focus mode is
AF-C/AF-A, for the half-press route). The event is an OK/J key press, or a
shutter half-press. The transition enters the subject-tracking display with the
reticle on and the subject locked, and it exits on OK-again or the Q/trash key.

So the firmware entry point to locate is the branch where the OK/J key handler,
gated by the AF-area-mode value, enters subject tracking, together with the stop
branch on OK-again or the Q/trash key. The existing static map already
has the AF-area label table (`0x103edda0`), the 3D-TRACKING label
(`0x103eddfc`), and an OK-key dispatcher noted as receiving OK in the simulator
(`0x103ce96e`); those are the threads to follow. The AE-L/AF-L path
(`0x103a3d14` and the SW-bank word `0x115c694c`) is most likely not the Z30's
route, because the body has no such button.

## Open questions for the firmware session

1. In the firmware, which AF-area-mode value marks "Auto-area," and where is it
   read when the OK/J key is handled?
2. Does the OK/J handler branch into subject tracking only when that state
   holds? That branch is the activation hook.
3. What is the stop path (OK-again / Q-trash key), for a clean enable/disable
   pair?
4. Is the half-press-in-AF-C route a separate entry, or the same tracking state
   reached through the shutter handler?

## Limits

- Public sources only; several Z30 manual pages were read through search
  snippets that were partly garbled, so confirm exact option names on the camera
  or the full manual.
- Owner reports of the missing AE-L/AF-L button are anecdotal but consistent.
- No firmware was read and no simulator was run; the hook-point section is a
  direction for the firmware session, not a traced result.

Written by Claude in collaboration with Tony Kim.
