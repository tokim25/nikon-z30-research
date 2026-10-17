# Digest input trace and read-tool review

2026-10-17. Claude, static review. No firmware bytes, hashes, or extracted
content in the repo. Restricted archive extracted only to a new scratch
directory outside the repo. Hardware remains **NO-GO**.

## 1. Digest input at 0x10000088: NOT DETERMINED

- The owner's archive (`Nikon-Z30-Firmware-Research-M1.zip`) contains tools,
  reports, a README and a test file. It does not contain the firmware image,
  so the EG module cannot be traced from it.
- A bounded search of the Downloads, Documents and Desktop folders for a
  firmware-sized file found none.
- Required to answer: the decoded EG module at a path the owner supplies, or
  `WORK` set to the private copy. Tracing `0x101d3f14` also needs a
  disassembler. Capstone is not installed here, and this review did not
  install it.
- Answer status: package content or device state is **undetermined**.
  [native-updater-digest-inputs.md](native-updater-digest-inputs.md) remains
  the record.

## 2. Read-tool review: gphoto2 is NOT read-only as shipped

- Candidate reviewed: libgphoto2 `camlibs/ptp2/library.c`, default branch
  fetched read-only. Findings are in
  [camera-readonly-identity-method.md](camera-readonly-identity-method.md).
- Verdict: a `gphoto2 --summary` check cannot be claimed read-only until its
  exact operation log is captured or a reviewed build omits the write calls.
- No other candidate tool has been reviewed. No vendor tool was installed.
- Earlier wording in the identity method called the check read-only. That
  claim is withdrawn.

## Owner decisions

1. Supply the decoded EG module path (or `WORK`) so the digest trace can run.
2. Decide whether the read-only identity check should wait for a pinned,
   reviewed build or an operation-log capture before any connection.
3. Decide whether a byte-level readback is still needed; see
   [camera-byte-readback-method.md](camera-byte-readback-method.md).

## 3. Update 2026-10-17: archive location, hash search, gphoto2 command

- The archive named in the request was not found under a `WORK` folder; no
  `WORK` directory exists in the home directory. A copy is at
  `Downloads/Nikon-Z30-Firmware-Research-M1 (1).zip`. It contains no firmware
  image, so the original image was not matched.
- A search of the home, Volumes and temp folders for files of the pinned
  container size (34,496,798 bytes) or EG size (33,939,514 bytes) found none.
  No hash comparison was possible.
- gphoto2: **none.** No command in libgphoto2 is documented or reviewed to read
  the installed Nikon firmware image. PTP vocabulary in `ptp.h` includes
  firmware-update opcodes for other vendors (Canon, MTP, Leica), and this
  review did not identify the Nikon equivalents. A generic opcode could reach
  an update operation, so no command should be run.
- Top risk: an accidental firmware-update or write operation through a generic
  PTP tool. Do not connect the camera for a readback until a reviewed method
  exists.

## 4. Digest test on the scratch copy: unresolved

- Decoded components of the owner's original: `ex2090_012000.bi` (524,290
  bytes), `_tpj04_v10a5.bin` (32,802 bytes), `eg2090_0120a0.bi` (33,939,514
  bytes). Their offsets and sizes are recorded; no bytes are recorded.
- Plain SHA-1 over the outer prefix-stripped package, the decoded body, and the
  raw package does not equal the expected 20-byte digest. Appending eight bytes
  from the EX or EG components at offset 0x88, or from the decoded body,
  also does not match.
- The expected digest includes the metadata transform at `0x101d3f14` that
  the native checker applies to the eight-byte input. That transform is not
  reproduced here, so the digest is not resolved.
- Conclusion: the digest input at `0x10000088` remains unresolved. No local
  copy is built on this basis.

## 5. Digest source trace (2026-10-17, static, scratch copy)

- Caller found: at `0x101ce590` the literal `0x10000088` is loaded into r0 and
  passed to the setup helper `0x101d7026`, which copies 8 bytes from that
  argument into the checker object (memcpy via `0x10199cf0`, length 8).
- The address is outside the EG payload. The EX component (524,290 bytes) does
  not show an ARM vector-table pattern at its start, so it cannot be assumed to
  be the boot region mapped at flash base `0x10000000`. TPJ shows no such
  pattern either.
- Result: the source is a fixed boot-region address that the decoded package
  does not supply at that offset, which points to device or boot state rather
  than package content. This is a reading, not proof.
- Digest input: **still open**. Build: not started; the readout-record manifest
  depends on this gate.
