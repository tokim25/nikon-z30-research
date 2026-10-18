# Native standalone EG route for an XPan build

2026-10-17. F-163. Read-only decode of the verified Z 30 C 1.20 EG with
Capstone 5.0.6. This resolves native validation-path selection for the
standalone format. It does not build an EG, execute the updater, or establish
camera acceptance. Hardware remains NO-GO.

## Current offline candidate status (F-198/F-199)

A private 176-span standalone-EG candidate now exists. Revalidation against the
known verified original confirms exact planned edits, unchanged protected
fields and file length, parser-capacity fit, native CRC, and the area-4 table
layout. This resolves the offline artifact checks described below; it does
not establish that Nikon's updater accepts this candidate. Lifecycle
condition 1 remains unmet, so hardware status remains NO-GO. The binary and
firmware-derived manifest are retained in owner-only storage outside Git.

## Decision

The native standalone-EG route is the best candidate format for the eventual
XPan build. It does **not** enter the unresolved 20-byte outer-package digest
path. The digest condition is restricted to body-package discovery type 4;
the standalone EG is discovery type 2. Type 2 takes the native file-CRC path,
then hands execution type 3 to the shared main-firmware updater. This is a
statically traced path through the verified original, not a camera acceptance
claim.

This corrects the older reading in
[xpan-build-decision.md](xpan-build-decision.md) that the standalone route
reaches the digest. The digest remains unresolved for the full outer body
package; it is not a reason to block a standalone-EG candidate.

## Native route

1. The firmware-management discovery table has a standalone-EG row with type
   2 and a filename pattern matching `EG209020.BIN`. Its parser dispatches to
   `0x101cd3cc`.
2. The parser checks that file length does not exceed a configured capacity.
   It seeks to offset `0x10`, reads four bytes, and compares them with a
   selected four-byte compatibility field. It then seeks to `0x24`, reads
   eight metadata bytes, and passes them to the execution-type-3 metadata
   formatter. Success records execution type 3 and one selected component.
3. The selector at `0x101cf8cc` returns the encoded-header flag only when the
   selected **discovery type is 4**. For type 2 it returns zero. Caller
   `0x10234440` therefore branches to `0x101ce324`, not digest checker
   `0x101ce518`.
4. `0x101ce324` loads the selected file and checks native CRC residue. For
   execution type 3, the two CRC trailer bytes are then removed from the
   length passed to the updater. The dispatcher reaches shared updater
   `0x101ce89e`.

By contrast, the original encoded outer body package is discovery type 4;
its parsed encoded flag is 1, so the caller enters `0x101ce518` and the
additional SHA-1 check described in
[native-updater-digest-inputs.md](native-updater-digest-inputs.md). That
branch's eight-byte input at `0x10000088` remains unknown. No flag or native
check is changed on either route.

## Remaining native-acceptance limits

The branch selection is resolved and the offline candidate checks are done.
The remaining limits concern native acceptance and any future hardware test:

- The initialized standalone-file capacity is confirmed as `0x2940000`
  bytes by a read-only pinned-QEMU startup; it matches the upstream C 1.20
  platform constant. The verified original EG is 33,939,514 bytes, below the
  limit. Keep the candidate exactly the original length and still check that
  exact length in the independent preflight; F-198/F-199 confirm this.
- The parser's four-byte compatibility field at file offset `0x10` is
  compared with the currently loaded module's four-byte field at the same
  offset. Preserve those original bytes exactly; do not edit this header
  field.
- The eight bytes at offset `0x24` are copied and formatted for execution
  type 3. They are preserved exactly; their downstream version-policy
  consumer and any later compatibility gate remain unverified.
- F-198/F-199 confirm native CRC coverage, trailer order, and exact output
  length for this offline artifact. The checks do not execute the updater.
- The updater's physical write, recovery behavior and acceptance of this
  project's candidate have not been executed or established here.

The pinned Wonder Lantern C 1.20 build guide independently documents a tool
that emits standalone `EG209020.BIN` without rewrapping the outer package. Its
verification page reports that its maintainer installed that project's
standalone module on a Z 30 C 1.20. This corroborates the format route, but
does not validate our edits or artifact:
[build guide](https://github.com/WonderLantern/wonder-lantern-z30/blob/f6630588810f6ecb9363bc7881fccb47e4fdb87b/docs/build.md),
[verification record](https://github.com/WonderLantern/wonder-lantern-z30/blob/f6630588810f6ecb9363bc7881fccb47e4fdb87b/docs/verification.md).

## F-198 offline XPan stills candidate

The private candidate contains XPan stills only, replacing the existing 1:1
slot, with no tracking changes:

- **Choice and label:** preserve the menu choice and callback, key all edits
  off the verified stored value 1, and replace its localized label and
  displayed size text without changing string lengths or neighboring labels.
- **Capture geometry:** update the area-4 readout, output-size and crop tables
  as a consistent set. For the scoped large mode, the checked rectangle is
  exactly 5200 by 1920. Its rectangle uses group 3/index 19 dimensions, group
  5/index 29 margin, group 6/index 34 inset, and the separately read area
  origin. F-164 maps the normal-context medium/small crop pairs (3/5) and
  candidate outputs 3900×1440 and 2600×960. F-165 exercises all three through
  the full native builder with synthetic guest records. See
  [all-size contract](native-xpan-all-sizes-preview-contract.md).
- **Embedded previews:** F-198 changes only area-4 slot 4 in the small/large
  getter and direct-buffer dimension tables to 480×176 and 1080×400. Slots
  0–3 and the five-entry stride tables are unchanged; the fixed thumbnail is
  not edited. The owner's still-photo-guard waiver accepts unmeasured
  area-4 playback/movie/warning side effects. F-170's synthetic constructor
  run used the same dimensions, but did not load this exact candidate.
- **Live-view bars:** the candidate includes the F-148 bars hook/template and
  its tested callback contracts. This is separate from capture geometry and
  does not add movie-specific behavior. The still-photo-guard waiver accepts
  possible playback/movie/warning side effects; lifecycle condition 1 remains
  unmet. Neither decision replaces exact-build checks or immediate test
  approval.

The offline artifact proof is recorded in F-198/F-199: exact-original
identity, complete manifest, exact changes, protected fields, unchanged
length, parser capacity, native CRC and preview-table layout. Nikon updater
acceptance, natural lifecycle transitions, saved RAW/JPEG crop behavior, and
the remaining Retouch Trim scope have not been established. Lifecycle
condition 1 remains unmet; no hardware test is ready or authorized.

No installable patch or camera procedure is specified here. The generated EG
and all firmware-derived details stay outside Git.
