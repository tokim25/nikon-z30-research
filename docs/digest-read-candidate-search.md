# Candidate search: read-only access to boot-region bytes at 0x10000088

2026-10-17. Desk review of public PTP vocabulary (libgphoto2 header and
camlib source, fetched read-only). Nothing was run; the camera was not
connected. Hardware remains **NO-GO**.

## Candidates found

| Candidate | Reads | Write-path review | Read-only provable? |
| --- | --- | --- | --- |
| Standard GetDeviceInfo (0x1001) | Identity strings only | Query only | Yes, but gives no memory |
| Nikon GetVendorPropCodes (0x90CA) | Property code list | Query only | Yes, but gives no memory |
| Nikon GetPartialObjectEx / HiSpeed (0x9431, 0x9400) | Stored object (card file) bytes | Query only in its name | Reads files, not device memory |
| Nikon GetObjectSize (0x9421) | Object size | Query only | Reads files, not device memory |
| Nikon GetLiveViewImg and similar (0x9203, 0x9428) | Live-view frames | Starts or depends on live-view state | Not memory |
| Nikon ChangeCameraMode (0x90C2), StartLiveView (0x9201), ResetMenu (0x9436) | Nothing | Changes camera state | No |
| Firmware-update opcodes (for example 0x911F, 0x9812) | Not applicable | Update path | Excluded |

## Result

- No candidate reads boot-region device memory at `0x10000088` through a
  documented, read-only interface.
- The file-oriented reads cannot see device memory by design.
- Candidates that change camera state are excluded; update-mode opcodes are
  excluded by the owner's rule.
- Evidence limit: this review uses header names and gphoto2 source, not
  Nikon's own documentation or runtime observation. It does not prove that no
  undocumented Nikon interface exists.

## Verdict

**None passes review.** The digest input stays open. Owner decision needed: whether
to accept the digest as open at the risk recorded in the readiness record, or
to pursue a different static source for the eight bytes.
