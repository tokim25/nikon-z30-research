# Recovery plan (draft)

Status: draft, written 2026-10-16. This is condition 2 of the
[build-phase gate](build-phase-gate.md). It is **not yet a credible plan**:
it lists what a plan must answer and what is still unknown. Nothing here
authorizes touching a real camera. The owner does any hardware step alone.

## The risk in plain words

A camera that fails to start after a firmware change may not be fixable by
the owner at home. The ordinary firmware-update menu lives inside the same
firmware that would be broken, so it cannot be counted on as the way back.

## What is known

- The owner's exact original is identified: 33,939,514 bytes, SHA-256
  beginning `8a99ced2` ([milestone-1-recovery.md](milestone-1-recovery.md)).
  The hash gate refuses anything else (`verified_firmware.py`).
- That original stays on the owner's machine only. It is never in this
  repository, even a private one.
- The simulator can show whether the new code behaves; it cannot show what
  happens when a real camera loses power or fails halfway.

## What is not known (each must be answered with evidence)

1. **Is there a startup path that does not depend on the main firmware?**
   Unknown. Nothing in this repository shows one, and none may be assumed.
2. **Can the owner put the original back after a failed start?** Unknown.
   Having the original file is not the same as having a way to load it.
3. **Does a modified image pass the camera's own integrity checks?** Unknown.
   A rejected image is the safe failure; a half-accepted one is not.
4. **What does the camera do if power drops mid-update?** Unknown. The
   simulator does not model this.
5. **Does Nikon service accept a camera in this state?** Unknown, and a
   modified camera may be refused or charged. The owner should expect to
   carry this cost, and should decide in advance whether they accept it.

## Public sources checked (2026-10-16)

- Nikon's published update guide for a different camera, the COOLPIX P500
  ([PDF](https://nikonimglib.com/europe/Firmware/P500/v1.1/Sc/Updating_Camera_Firmware(Windows).pdf)),
  says power loss during an update can damage the camera, and that an
  inoperable camera should go to a Nikon-authorized service representative.
  That is a different model, so for the Z30 it is **unverified**, though
  Nikon guides for other models read the same way. It points to service as
  the official way back, not a home procedure. This bears on unknowns 1, 2
  and 5 but answers none of them.
- A search for an official Nikon Z-series recovery page found none. Forum
  reports describe only retrying an update or resetting the camera, which
  applies to a camera that still starts.

## What a credible plan must contain before the gate counts it as met

- A written, step-by-step way back to the verified original that does not
  use the update menu, with a source for each step (not a guess).
- Proof the way back was checked on something other than the owner's only
  camera, or a clear statement that it was not and the owner accepts that.
- A stop rule: the exact conditions under which the owner abandons a try.
- Fully charged battery and stable power as written preconditions.
- A copy of the verified original kept offline, with its hash written down
  next to it.
- A plain statement of the worst case: the camera may not recover.

## Rules that already apply

- Only the exact verified original may be patched (hash gate).
- No Nikon bytes, dumps or patched images go in the repository or anywhere
  public.
- Hardware access also needs [hardware-readiness.md](hardware-readiness.md)
  to stop saying NO-GO, and the owner's separate, explicit go-ahead.

## Next

Collect sources for the five unknowns above, labelling each answer observed,
inferred or unverified in [facts.md](facts.md). Until items 1 and 2 have
evidence, this condition stays unmet.

Written by Claude (Opus 5.5) in collaboration with Tony Kim.
