# Draft: owner waiver for byte-exact camera identity

2026-10-17. Draft for the owner to review, edit and sign. Not in effect until
the owner waives it by name. A waiver does not approve any camera step.
Hardware remains **NO-GO**.

## Readback route: not proposed

Claude will not propose or specify a method for reading the camera's installed
firmware. No read-only route to the image has been identified. The candidate
PTP tool reviewed (libgphoto2) has write-capable calls on exit and capture
paths, and firmware-update opcodes exist in the PTP vocabulary. A dump method
built against an unidentified update or service interface is not a read-only
procedure. The owner can choose to skip the readback entirely, with the waiver
below.

## Gate waived

**Byte-exact identity of the camera's installed firmware** against the owner's
original EG module (SHA-256 `8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`).
Recorded so far: version-level identity, firmware 1.20, from the camera's own
read-only device-info check and the owner's statement.

## Owner's reason (owner to write in their own words)

[Owner: state why the byte-level check is not needed or cannot be performed.]

## Risk accepted

- The camera's installed image may differ from the original in ways the
  version-level check cannot detect.
- A flash based on an unverified installed image may fail, leave the camera
  unusable, or require Nikon service.
- The digest input at `0x10000088` remains unresolved and is not covered by
  this waiver.

## Not covered by this waiver

- Local byte-exact check of the owner's EG file with `require-verified-eg`.
- The unresolved digest input.
- The owner's separate final approval immediately before any hardware step.
- Any connection, flash or write to the camera.

## Signature

Owner name: ____________________
Date: ____________________
Waiver text as written by owner: ____________________
