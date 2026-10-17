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
