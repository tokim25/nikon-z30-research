# XPan stills: build decision on the standalone-EG route

## Current offline candidate status (F-198/F-199)

A private 176-span standalone-EG candidate now passes exact manifest, byte-
diff, protected-field, length/capacity, native-CRC and preview-table layout
checks. It remains outside Git with its firmware-derived manifest in
owner-only storage. No exact-candidate native updater acceptance, natural
lifecycle coverage, or camera behavior is claimed; hardware remains NO-GO.

## Codex correction: standalone EG avoids the outer digest (F-163)

The earlier route verdict below is superseded on this point. Static decode of
the verified original shows that the extra 20-byte digest is selected only
for discovery type 4 with its encoded-header flag set. The native standalone
EG is discovery type 2; the same selector returns zero, so the caller takes
the native file-CRC path at `0x101ce324` and then dispatches execution type 3
to the shared updater. The missing eight-byte digest input therefore does
not block a standalone-EG candidate. It still blocks any candidate sent
through the encoded outer-body path. No check was disabled or changed.

The standalone route is the selected candidate format. Parser capacity,
compatibility-field preservation, all-size crop/preview edits and exact
candidate byte/layout/CRC checks have since been completed for the offline
artifact. Version-policy semantics and Nikon updater acceptance remain
unverified. See
[native-standalone-eg-route.md](native-standalone-eg-route.md).

## Earlier route analysis (historical; corrected by F-163 and F-198)

2026-10-17. Claude, read-only static review. No simulator run, no patch
encoding, no camera access, no installation workflow. Hardware remains
**NO-GO**. The native-claude-build-research-handoff.md named in the request
does not exist on `main`; this review proceeds from handoff.md,
handoff-codex.md, project-status.md, and the native and XPan notes.

## Build decision

**Route verdict: not verified end to end.** The native standalone-EG path is
traced statically up to its digest check. The decoded-container checks,
CRC coverage, header handling and installation span are established against
the verified original. The 20-byte digest branch cannot be reproduced because
one eight-byte input has no verified source ([native-updater-digest-inputs.md](native-updater-digest-inputs.md),
F-140; [native-boot-mapping-boundary.md](native-boot-mapping-boundary.md),
F-141). Until that input is resolved, a candidate EG cannot be claimed
acceptable by the camera.

**Top gap:** the digest's eight-byte metadata input at `0x10000088`. Startup
mappings and scatter copies do not cover it, and literal searches are
exhausted ([native-boot-mapping-boundary.md](native-boot-mapping-boundary.md)).

**Next step for Codex:** decide whether those eight bytes are derived from
package content (then reproducible offline) or from device or boot state (then
an unresolvable gap for this route). Do this by tracing the inputs to the
metadata transform at `0x101d3f14` and its callback chain from the setup
helper, not by searching the address again.

## What the route establishes (static, verified original)

| Item | Status | Evidence |
| --- | --- | --- |
| Body-package discovery and parser | Traced | [native-updater-validation.md](native-updater-validation.md), F-139 |
| Encoded-format flag and selected-record restore | Traced; branch predicted, not executed | [native-updater-digest-inputs.md](native-updater-digest-inputs.md), F-140 |
| Decoder masks and CRC primitive | Equivalent to recovered tooling | F-139 |
| Container header, component bounds, CRC coverage | Checked | [native-container-validator.md](native-container-validator.md), F-136 |
| Exact-edit comparison, combined preflight | Checked; baseline zero changed bytes | F-137, F-138 |
| Installation span and capacity | 43,253,760 bytes; payload 33,939,512 excluding CRC; 9,314,248 bytes of 0xFF tail | [native-install-span.md](native-install-span.md), F-142, F-143 |
| Updater relocation and handoff | Mapped to verified EG bytes; not executed | [native-boot-mapping-boundary.md](native-boot-mapping-boundary.md), F-141 |
| 20-byte digest comparison | **Unresolved input** | F-140, F-141 |
| Compatibility, version and downgrade policy | **Not established** | F-139 scope note |
| Authentication or acceptance by the camera | **Not established** | F-136, F-138 scope notes |

Nothing in this table licenses an install, a flash, or an assertion that a
candidate would pass the camera's checks.

## Reconciliation with WonderLantern (contradiction to resolve)

WonderLantern/wonder-lantern-z30 at `f6630588810f6ecb9363bc7881fccb47e4fdb87b`
(read via GitHub, not executed) builds a standalone EG module, not a rebuilt
outer package. Its `docs/verification.md` and `docs/modules.md` say a
standalone EG "can be installed through the camera update flow" and report
that maintainer's camera testing. This is an upstream claim, not validation
here. It also conflicts with F-140: an original-style encoded container is
predicted to take the extra digest branch, and an edited EG would then
mismatch that digest unless the path differs or the check is not reached.
Their installer procedure and outer wrapper are not documented in the files
read, so the contradiction cannot be settled from their sources. It is the
clearest reason to keep the digest gap open rather than assume the route.

WonderLantern's install claim is a lead to test against our traced branch,
not a shortcut past it.

## Minimum XPan edit set (proposed; nothing applied)

Owner decisions carried in: replace 1:1 (not add), saved-file correctness is
an on-camera test item, tracking excluded, lifecycle gate still open.

**1. Choice and stored state**
- The 1:1 choice keeps its menu item and availability code. Reconcile the
  stored value: [xpan-replace-1to1-plan.md](xpan-replace-1to1-plan.md) says
  value 4, but F-093 and F-101 record the final stored byte at `0xc1811d90` as
  **1** for 1:1 (0 DX, 2 for 16:9). Every later edit must key off the verified
  byte, not the callback value.

**2. Labels and resources**
- String 1454 and the size lines beside the labels (F-062 to F-065), in each
  language that shows 1:1. Keep string lengths; the image-area strings carry
  no terminator (F-063).

**3. Size records and lists (area 4 slot)**
- Per-area table entries at indices 4, 9, 14, 19, 24, 29, 34 (F-054;
  [image-area-tables.md](image-area-tables.md)).
- Shared size-list square entries in the 1:1 slot (F-055).
- Crop-window builder inputs (F-056, F-080). Simulator-only evidence gives a
  65:24 window of 5208 by 1928 from replacement records, and an exact 5200 by
  1920 rectangle from temporary geometry data
  ([xpan-capture-geometry-probe.md](xpan-capture-geometry-probe.md)). Pick one
  geometry; do not mix them.

**4. Embedded previews (must not be skipped)**
- WonderLantern found that XPan captures kept 16:9 embedded previews (640 by
  360 and 1920 by 1080) until its capture-call preview sizes were changed
  (640 by 236 and 1920 by 708, 4-pixel aligned, within the stock buffer
  limit) ([aspect-profiles.md](https://github.com/WonderLantern/wonder-lantern-z30/blob/f6630588810f6ecb9363bc7881fccb47e4fdb87b/docs/aspect-profiles.md)).
  This is their area-2 evidence and does not transfer to area 4.
  Our edit set needs the area-4 preview records and the capture-path
  preview selector, checked by the same full-table buffer test.

**5. Live-view bars (new code, hook)**
- Paper design: [xpan-bars-design.md](xpan-bars-design.md). Trigger on area
  change while live view is active, on live-view start, and on menu return
  (F-101). Read byte `0xc1811d90`; equal to 1 means bars on. The F-148 overlay
  is the bars hook only; it is not crop, label or preview work.
- Known open items: the true return path is unobserved; focus points and
  frame lines need clipping or hiding (owner decision).
- WonderLantern's 65:24 choice does not show black bars; its reference frame
  uses the native grid. It is not a model for this mask.

**6. Square assumptions outside capture (decide, do not ignore)**
- Retouch Trim forces width equal to height for the 1:1 slot in its table
  (table A; function `0x10597440`, [image-area-tables.md](image-area-tables.md)).
  Either exclude Retouch Trim from the first build with an explicit owner
  note, or add it. This review does not decide that.

**Not in the first build (owner-excluded):** saved RAW/JPEG serialization,
NEF default-crop markers, tracking.

## Required checks before any Codex implementation step

- Verified original identity and unchanged decoded-container baseline, from
  the existing preflight.
- Exact-edit manifest covering every item above, with the policy bound to the
  candidate.
- Simulator acceptance for the bars trigger set in
  [xpan-bars-design.md](xpan-bars-design.md), and for the four geometry and
  preview records. Simulator runs stay with Codex, not this review.
- Lifecycle gate: still open. Not waived here.

## Limits of this review

- Read-only; the WonderLantern commit was read through the GitHub API, not
  cloned, built or executed.
- The WonderLantern installer procedure beyond `docs/verification.md` and
  `docs/modules.md` was not available in the files read.
- No new fact number is assigned; numbering stays with the owner and Codex.
