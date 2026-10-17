# Read-only camera identity comparison: method for review

2026-10-17. Written for review only. Nothing here has been run. No camera was
connected, no tool was installed, and nothing was flashed. Hardware remains
**NO-GO** ([hardware-readiness.md](hardware-readiness.md)).

## Scope

This method can confirm identity at the level of the camera's reported
firmware version and device information. It cannot confirm that the camera's
installed image matches our original file byte for byte. That limit is
structural: the installed image is not exposed through a read-only interface
that this method uses. Any byte-level readback would be a different,
non-read-only operation and needs a separate design and approval.

## What it reads

- Standard PTP GetDeviceInfo (operation 0x1001) over USB, if the tool issues
  only that operation. The tool-level check above shows this is not yet proven. It returns the
  device's manufacturer, model, device version string and the vendor
  extension info, which the owner's earlier USB check reported as firmware
  1.20 (USB version 0x0120).
- No object, image, or property data is requested.

## Tool and installation (proposed, not installed)

- `gphoto2` (libgphoto2), installed by the owner from a source they trust, for
  example `brew install gphoto2`. The owner should check the version and
  checksum before use.
- The command, once approved, is `gphoto2 --summary`. It opens a PTP session
  and prints device information.
- Alternative: a small standard-library Python script issuing only
  GetDeviceInfo. This is not written and would need review.

## Proof that it cannot write: NOT MET

Source review of libgphoto2's PTP camlib (`camlibs/ptp2/library.c`, default
branch fetched read-only on 2026-10-17; not pinned to a commit) found
write-capable calls, so `gphoto2` is not read-only as shipped:

- `camera_exit` calls `ptp_nikon_changecameramode(params, 0)` when the control
  mode flag is set.
- `camera_capture_preview` and the Nikon capture path call
  `ptp_nikon_changecameramode(params, 1)` and set the Nikon recording-media
  property. These run only for capture requests, not for `--summary`.
- `fixup_cached_deviceinfo` writes the MTP session-initiator property on a
  vendor-specific branch. Its comment names another vendor, but Nikon
  applicability was not traced.
- The Nikon open/init path was not fully traced, so the summary path's exact
  operation list is unverified.

An operation log is therefore required before any claim of read-only status,
and a read-only check must use a tool or build that omits these calls. This
method is not approved.

## Comparison to our original file

- Compare reported version (1.20) to the identity in
  [milestone-1-recovery.md](milestone-1-recovery.md). This is a version-level
  match only.
- The byte-level comparison stays with the local original: its size and
  SHA-256 are checked with `require-verified-eg` on the owner's file. No
  bytes, hashes of camera content, or serial numbers go into the repo.

## What could go wrong

1. Opening a PTP session during a firmware or update mode could interact with
   an update process. Confirm the camera is in normal shooting mode.
2. A tool with a broader command set could send a write. Mitigated only by
   the operation log described above.
3. USB disconnect during a session could leave the camera in an unclear state.
   Use a stable cable and keep the battery charged; do not power-cycle during
   a session.
4. Connecting the camera while an SD card is inserted could expose card
   contents to the tool. Remove the card for the test.
5. Re-running the command on a changed build could be misread as a result for
   a different firmware. Record the camera's reported version every time.

## What the owner must approve

1. Installing the tool named above, after checking its source and version.
2. Connecting the camera for one read-only session with the card removed.
3. The exact command list and the operation-log capture before the run.

Nothing in this document authorizes a firmware read, a byte dump, flashing,
or any write to the camera.
