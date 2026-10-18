# Offline XPan build architecture

Codex engineering proposal, 2026-10-17. This describes a private build and
validation design for the owner's Z 30 C 1.20 only. It is not an updater
procedure and does not authorize camera contact.

## Chosen artifact

Build a standalone `EG209020.BIN` from the verified C 1.20 EG component, not a
rewrapped outer `Z_30_0120.bin`. The project's static decode shows native
discovery type 2 takes the EG CRC route; the unresolved outer-container digest
is selected for type 4. The pinned WonderLantern build documentation also
describes emitting the standalone EG without rebuilding the outer package and
reports a C 1.20 camera test. That is format corroboration, not validation of
this project's artifact.

## Same-camera implementation comparison

The current Wonder Lantern Z30 C 1.20 source now documents an implemented
65:24 profile with still-size geometry, capture-specific embedded-preview
dimensions, and user-reported camera validation. Its geometry follows the
native area-2 path (L/M/S 5568×2056, 4176×1544, 2784×1024), rather than this
plan's proposed area-4 crop (5200×1920, 3900×1440, 2600×960). It also uses a
profile selection/configuration and native grid reference, not this project's
stored-1:1 choice and black-bars overlay.

This is not a drop-in baseline for the requested build: its multi-profile
setting changes the native image area to 2 and draws a grid reference, while
our feature replaces the stored 1:1 choice in area 4 and requires independent
black bars. Its source is only a same-firmware reference; no code is copied.

Source: [public aspect-profile implementation and reported validation](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/aspect-profiles.md),
[standalone-EG build contract](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/build.md).

## Candidate contents

The private experimental candidate has been built as a standalone EG from the
verified C 1.20 original. It replaces the stored 1:1 slot (value 1), includes
the F-148 bars edits, area-4 L/M/S geometry, localized menu/size strings, and
four area-4 preview-table edits. It excludes tracking and changes to updater
validation. The binary and manifest stay in owner-only storage outside Git;
the handoff records retention requirements without exposing their path.

## Concrete patch shape

Treat the feature as a data-only change to the existing image pipeline.
Preserve the native sensor/readout path and stock RAW/JPEG encoders; reuse the
existing 1:1 menu slot and its stored value `1`. The approved patch scope
changes only the four preview dimensions in area-4 table slot 4. The owner
waived the still-photo guard and accepted that reduced area-4 previews may
also affect playback, movies or warnings. This side effect is a residual
risk, not a measured behavior or hardware-readiness claim.

The area-4 record set is internally consistent at all three sizes: L
5200×1920, M 3900×1440, S 2600×960. F-165 validates the crop descriptors
through the native builder. F-198's table-only preview edit supersedes the
previous caller-scoped proposal:
For this candidate, edit only area-4 slot 4 in both the generic getter and
direct-buffer dimension tables; the native constructors bypass the getters.
The values become 480×176 and 1080×400. Each table's other four area slots
remain byte-for-byte stock, as do row strides 960/2160 and the fixed
120×120 thumbnail. The edit affects any consumer selecting area 4. The owner
accepted possible playback/movie/warning effects, so capture-caller hooks and
code veneers are unnecessary for this offline candidate. Upstream area-2
values 640×236 and 1920×708 are not used.

F-169 identifies three direct pixel-buffer constructors and five possible
hook sites. The candidate uses no code hooks; it edits their backing slot.
F-170 synthetically executes all three constructors with the replacement
dimensions and confirms the fixed thumbnail fields remain unchanged. That
proves the values flow into native output records, but not full camera
lifecycle or preview pixels.

F-170's area-0 control changed when the shared table was replaced for its
probe. The candidate instead edits only slot 4; an independent byte audit
confirms slots 0–3 and both stride tables are unchanged. Area-4 playback and
other contexts remain within the accepted guard-waiver risk.

F-171 shows the `0x10142d86` constructor is reached through shared wrapper
`0x10142f5e` from preview-slot creation and current-record rebuild paths.
Those paths explain why the candidate's accepted area-4 side effects remain a
real risk; they do not change the four-table-edit scope.

## Historical hook-layout exploration (not used by F-198)

Earlier code-hook proposals considered a small appended payload in the native EG plus a
nearby branch veneer, if layout checks confirm the updater's loaded address
range. The same-version upstream builder documents adding code at the EG tail
before its CRC; this is a useful format precedent, not proof for our payload.
The EG parser has about 9 MB of capacity headroom, while a Thumb branch from
the preview constructors to the file tail may exceed direct branch range. A
local veneer can keep each hook branch in range and transfer through an
absolute Thumb-tagged pointer to the appended stub. Verify the exact relocated
address, instruction mode, trailer movement, loaded extent and return ABI
before adopting this layout. Keep the appended payload minimal and include it
as an exact manifest region.

For the verified original, the two-byte CRC begins at virtual address
`0x1207e038`; code inserted immediately before it would begin at that address
and use Thumb entry pointer `0x1207e039`. The parser's `0x2940000`-byte write
span ends at `0x12960000`, leaving more than 9 MB beyond the original payload.
These calculations establish bounds only; the module's executable mapping and
the actual copied range still require verification.

The first nearby zero-run audit rules out using all of
`0x1002d884–0x10030006`: many existing direct pointers target addresses within
it. A 1,642-byte aligned subspan at `0x1002d996–0x1002e000` has no
direct-pointer, scanned Thumb branch, or detected Thumb MOVW/MOVT references,
so it remains a candidate for the nearby veneer only. Section boundary,
computed/base-relative references, executable mapping and every exact veneer
span still require proof before placement.

F-174 establishes candidate four-byte windows near the five direct-buffer
hook areas and confirms that a register-preserving eight-byte literal veneer
can reach an appended Thumb stub; all five windows are within range of the
small zero subspan. The veneer region is not yet proven executable, and each
window's displaced instructions and capture guards remain unapproved.

The menu should continue to use the existing 1:1 choice and availability
logic, while its label and displayed dimensions are replaced with same-length
localized strings. F-176 now records 144 such spans across 36 languages in a
private text-only manifest, with same-length UTF-16 replacements. This maps
space and byte spans but still needs a visual language review. Geometry and
preview data remain private in the exact edit manifest. Preserve the standalone header compatibility field at `0x10` and
the eight bytes at `0x24` until their downstream version semantics are
closed; do not edit those fields to influence version selection.

F-178's 160-span text/geometry manifest was an intermediate plan, later
superseded by the complete private F-198 candidate manifest.

F-189 added the F-148 bars spans to an intermediate 172-span plan. F-198
supersedes it with the complete 176-span candidate manifest and a private
candidate that passed independent read-back checks.

## Offline candidate checks and remaining gates

The private writer accepted only the verified original and exact reviewed
manifest; an independent read-back audit confirmed each listed edit, no
unplanned changes beyond the regenerated two-byte CRC trailer, protected
header/metadata, dimensions, unchanged non-target slots/strides, file length,
capacity, CRC and owner-only mode. This is a testable offline candidate, not
validated camera acceptance: lifecycle condition 1 remains unmet, native
modified-file acceptance is unproven, and camera access/write remains NO-GO.
The candidate and manifest stay outside Git.

F-198/F-199 now provide a reviewable offline data-only candidate. F-170 ran
the native constructors synthetically with the same preview dimensions, but
did not load the exact candidate. The owner's guard waiver permits this
table-only shape while accepting unmeasured area-4 playback/movie/warning
effects. Lifecycle condition 1 remains unmet; native updater acceptance and
the `0x24` downstream version-policy behavior remain unverified. No camera
write is authorized.

The private writer starts from the exact verified original and rejects a
wrong source hash, malformed or incomplete manifest, mismatched expected
bytes, overlap, out-of-range edits, unlisted changes, protected-field edits,
and incorrect CRC. The current F-198 plan has no payload append or code hooks.
The generic composer also supports a hash-pinned payload before the CRC for
future separately reviewed uses; that capability is not used by this
candidate.

The repository now contains a standard-library-only in-memory composer and
read-back auditor in `src/nikon_z30_research/standalone_eg.py`. Its manifest
parser requires a declared `COMPLETE_REVIEWED_PLAN` status, the pinned Z 30
source identity and load base, and exact hashes for each edit and optional
payload. That marker is a plan assertion and still requires independent human
review. The composer validates
the original CRC before edits, applies same-length exact spans, optionally
inserts a hash-pinned payload before the two-byte trailer, regenerates the
CRC-16/XMODEM trailer, and checks every unchanged region plus the protected
header/metadata fields and parser capacity. Fourteen tests exercise only
synthetic fixtures. The separate private writer in
`src/nikon_z30_research/private_eg_builder.py` requires the caller's SHA-256
for the exact reviewed manifest, rejects firmware/plan/payload/output paths
inside the repository and existing output files, verifies the original before
composition, independently re-opens and audits the result, creates the file
with owner-only permissions, and removes a partial output on audit failure.
Synthetic filesystem tests cover these controls. F-198 subsequently ran the
private writer against the verified original and complete reviewed 176-span
manifest. It produced the candidate described in the handoff; an independent
read-back audit passed. Earlier F-178/F-189 in-memory plans are superseded.

The independent F-198/F-199 preflight checks exact source and candidate
identity, all manifest spans, unchanged bytes outside those spans and the
regenerated CRC trailer, protected fields, expected length, parser capacity,
CRC residue, geometry and preview-table layout. It confirms there is no
payload append. The pinned simulator has tested the geometry builder and
preview constructors with synthetic inputs, but has not loaded this exact
candidate. Nikon updater acceptance and complete lifecycle behavior remain
unverified. Keep the firmware candidate, manifest and raw reports in
owner-only storage outside Git.

## Build gates

The standalone-EG route is the selected offline candidate format. The native
parser capacity, compatibility-field preservation, exact manifest and CRC
checks pass for the private artifact. F-165 tests all-size geometry in pinned
QEMU with synthetic guest RAM; F-170 tests the same preview dimensions in
synthetic constructors, not by loading the candidate file. The `0x24`
downstream version-policy consumer, native modified-file acceptance and full
lifecycle remain unverified. Lifecycle condition 1 remains unmet; hardware is
NO-GO and building the private file does not authorize camera contact or
write.
