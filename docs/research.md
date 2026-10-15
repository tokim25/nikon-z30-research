# Nikon Z30: source evidence and offline research boundaries

Reviewed: 2026-10-15. This is newly written research, not recovered milestone code. Prior milestone files were unavailable. No earlier implementation, test result, address, or feasibility claim is accepted as established without independently inspectable evidence.

## Method and evidence labels

Public web access was used only to read primary-source documentation. Analysis and proposed validation are offline: no camera connection, firmware download, extraction, modification, patch generation, or hardware flashing. Publish only original source, synthetic fixtures, documentation, and non-payload evidence. Never publish Nikon firmware, extracted bytes, or installable patches.

- **Documented fact:** directly supported by Nikon documentation; not a hardware test here.
- **Upstream report:** directly observed in WonderLantern documentation; execution and hardware claims remain the author's reports.
- **Coordinator-measured result:** local verification performed by the coordinating session and reported on 2026-10-15; not rerun by this documentation session.
- **Proposal:** a requirement or inference for this new project, not demonstrated camera functionality.
- **Inherited/unverified:** statements about previous milestones or unavailable artifacts.

## Primary-source register

| ID | Source | Version or revision | What it supports |
| --- | --- | --- | --- |
| N1 | [Nikon Z30 download center](https://downloadcenter.nikonimglib.com/en/products/603/Z_30.html) | Listed C 1.20, released 2025-05-07 | Firmware listing as observed on review date |
| N2 | [Nikon C 1.20 release notes](https://downloadcenter.nikonimglib.com/en/download/fw/556.html) | C 1.20 | Filename and official change description |
| N3 | [Nikon: Choose image area](https://onlinemanual.nikonimglib.com/z30/en/09-03-05.html) | Live HTML; immutable revision unavailable | Documented still-image areas |
| N4 | [Nikon: Still images](https://onlinemanual.nikonimglib.com/z30/en/07-02.html) | Live HTML; immutable revision unavailable | Image dimensions |
| N5 | [Nikon: Focus](https://onlinemanual.nikonimglib.com/z30/en/05-01.html) | Live HTML; immutable revision unavailable | Subject-tracking controls and restrictions |
| W1 | [WonderLantern repository README](https://github.com/WonderLantern/wonder-lantern-z30) | Mutable `main`; commit SHA not resolved | Declared project scope, presets, input identity |
| W2 | [WonderLantern build documentation](https://github.com/WonderLantern/wonder-lantern-z30/blob/main/docs/build.md) | Mutable `main`; commit SHA not resolved | Reported source and decoded-module identities; offline validation boundaries |

The initial browser review did not resolve a revision. A subsequent GitHub API check on 2026-10-15 resolved `main` to [10e7335977d613075e4e5feed1e3ac331ba90a8a](https://github.com/WonderLantern/wonder-lantern-z30/commit/10e7335977d613075e4e5feed1e3ac331ba90a8a), committed 2026-10-13. The coordinator read [build.md at that revision](https://github.com/WonderLantern/wonder-lantern-z30/blob/10e7335977d613075e4e5feed1e3ac331ba90a8a/docs/build.md) and confirmed both reported identities below. Other initial browser claims have not all been re-audited at that revision; this is not an atomic audit of the entire source tree. No upstream code was executed.

## Verified documentation and upstream reports

**Nikon:** N1 lists C 1.20. N2 names `Z_30_0120.bin`; its 1.11-to-1.20 change is a fix for a rare startup hang involving monitor opening and enabled wireless connectivity. These release notes do not announce XPan capture or 3D tracking.

N3 lists DX, square, and 16:9 still-image areas; it does not list a 65:24 option. N4 lists the large DX image as 5568 × 3712 pixels. A panoramic composition guide therefore does not establish native panoramic capture support.

N5 documents subject tracking under the three auto-area variants. J enables the reticle; another J starts tracking; J ends tracking and W (Q) exits the mode. Fn controls can be assigned subject tracking. Touch AF can select and track a subject without releasing the shutter. For photo AF-C/AF-A tracking started by half-press, releasing the shutter button ends tracking. This is documented subject tracking, not proof of a separate 3D-tracking implementation.

**WonderLantern:** W1 describes an experimental Z30 C 1.20 project. Its listed live-view feature combines histogram and level displays; that is not an XPan mask. The listed presets do not demonstrate either requested feature. W1 reports hardware experience for some features, but explicitly limits its validation claims. Those reports are not reproduced here.

### Source identity: upstream report and local measurement

W1 and W2 report the accepted original package identity:

- Name: `Z_30_0120.bin`
- Size: 34,496,798 bytes
- SHA-256: `1a5449ef505f1f347ed4e066a6a3f588ea542240680e83f4ebcae3b16da3434a`

W2 separately reports a decoded EG identity:

- Size: 33,939,514 bytes
- SHA-256: `8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`

On 2026-10-15, the coordinator independently measured the recovered attachment locally using the new verify CLI: size 34,496,798 bytes and SHA-256 `1a5449ef505f1f347ed4e066a6a3f588ea542240680e83f4ebcae3b16da3434a`. Both match the upstream-reported original package identity. This establishes identity consistency with that report, not authenticity or trusted provenance. It is not a Git commit hash or an independently verified Nikon-published checksum.

The decoded EG size and digest remain upstream reports only; decoded-module checks have not been independently verified. W2 distinguishes offline checks from complete camera behavior; matching the package identity cannot establish display or autofocus correctness on hardware. Recovery of this attachment does not constitute recovery of prior milestone code.

## Proposed research questions

### XPan-style framing

Use 65:24 as an explicit project design choice. Build a host-side composition overlay over synthetic images, with no claim that the camera can render it. The initial continuous/subpixel proposal for active-image viewport `(x, y, W, H)` fits the largest centered rectangle: width `min(W, H × 65/24)`, height `width × 24/65`, followed by a documented pixel-rounding rule.

The current geometry scaffold instead uses exact integer multiples: `k = min(floor(W/65), floor(H/24))`, with guide dimensions `65k × 24k`. This preserves the exact ratio but can trim additional edge pixels compared with the continuous or rounded proposal. These are distinct geometry policies; the proposal is not a description of the scaffold. For a 1300 × 900 viewport, both yield a 1300 × 480 guide with 210-pixel top and bottom margins.

Keep three outcomes distinct: display-only guide, host-side crop of user-owned imagery, and native camera capture. This milestone covers only the first. Native JPEG/NEF dimensions, metadata, sensor readout, and capture-pipeline behavior remain unknown and outside implementation scope.

### One-step subject tracking

Define a host-side state-machine experiment: one deliberate press requests acquisition at an already selected target from an eligible idle state. A mock success acknowledgement moves to tracking. This is a proposed button workflow, not an assertion about a Nikon callback or algorithm. Existing touch behavior is a useful documented baseline, not evidence that an equivalent button operation is exposed internally.

Readable strings, menu names, symbol guesses, or a successful simulated transition do not prove executable 3D tracking. Any inherited claim of hidden tracking support requires independently attributable implementation and reachability evidence; none has been supplied. Public deliverables must not include extracted instructions or firmware payloads.

## What remains unverified

No recovered milestone code; no complete source audit at the pinned upstream revision; no independently verified decoded-module checks or firmware authenticity; no camera rendering hook, event API, autofocus integration, or native panoramic capture path; no hardware reproduction of upstream results. The coordinator's local package size/hash measurement establishes the identity consistency described above. The roadmap and issue acceptance criteria are specifications, not evidence that all their tests have passed.
