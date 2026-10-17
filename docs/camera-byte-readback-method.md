# Byte-level firmware readback from the camera: method status for review

2026-10-17. Written for owner review. Nothing has been run. No camera was
connected, no tool was installed, and nothing was flashed. Hardware remains
**NO-GO** ([hardware-readiness.md](hardware-readiness.md)).

## Status: no read-only method is defined

- The owner approved in principle a full byte-level read of the camera's
  installed firmware. This document cannot yet specify an exact command,
  because no read-only route to the installed image has been identified.
- Standard PTP and the USB device-info query used so far expose identity
  only (see [camera-readonly-identity-method.md](camera-readonly-identity-method.md)).
  They do not return the installed firmware image.
- Any route to the image would use a vendor-specific or updater-mode interface.
  Such an interface is not documented in this repo, and using one is the kind
  of operation that can alter the camera. The owner should not approve a
  readback until the route itself has been reviewed and shown to be
  read-only. This review has not been done.

## What the owner must decide before any method is written

1. Whether a byte-level readback is needed at all. The exact original is
   already held privately, and the owner's own identity check at version
   level is recorded. A readback would only show whether the installed image
   matches that original.
2. Whether a vendor or updater-mode route is acceptable, given that the
   route would have to be reviewed for write paths first.

## Required fields once a route is identified

- Tool, exact version and source checksum.
- Exact command, with the operation log that proves only read operations ran.
- Where the output is stored: outside the repo, on the owner's machine only,
  never committed or attached to an issue.
- Hash-only comparison: SHA-256 and size of the read image compared with the
  original's recorded values in [milestone-1-recovery.md](milestone-1-recovery.md).
  No bytes and no camera-derived hashes go into the repo.
- Partial or failed read: discard the output, record the failure, and do not
  retry in a way that changes camera state.

## Steps that could alter the camera

- Any vendor-specific command, updater-mode entry, or firmware-related USB
  operation whose effect is not documented.
- Any read that puts the camera into a service or update state.
- Interrupting a read partway, which could leave the camera in an unclear state.

## Top risk

A readback route that is not truly read-only could write to or corrupt the
installed firmware. Without a reviewed command list and operation log, the
read cannot be considered safe.

## What the owner must approve

1. Whether a byte-level readback is needed, given the original is held.
2. The route, only after its command set is reviewed and shown read-only.
3. One read-only session with the card removed, with a full recovery plan
   recorded beforehand.

Nothing in this document authorizes a read, a dump, flashing, or any write.
