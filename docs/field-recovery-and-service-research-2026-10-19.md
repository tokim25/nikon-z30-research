# Z 30 field recovery and service research

This note records the external recovery investigation after an experimental
candidate left the owner's Z 30 in an early-boot loop. Firmware files, dumps,
private QEMU output, and installable candidates remain outside this repository.

## Observed failure state

- The LCD remains black.
- The rear green activity light and lens initialization occur once at startup.
- The camera repeats that activity approximately every 15 seconds.
- The loop continues with the lens removed and with the SD card removed.
- A Mac USB monitor saw no Nikon PTP, recovery, or alternate USB identity during
  repeated checks across the loop.
- Removing the battery for one minute did not change the behavior.
- Holding `MENU` during startup did not change the behavior.
- Holding `OK` during startup did not change the behavior.

The combined observations are consistent with an early body-boot failure, but
do not identify the failed storage region or hardware component.

## Public recovery research

Nikon's documented Z 30 update procedure requires the camera to reach
`Setup > Firmware version`; it does not document automatic SD-card recovery or
a user-accessible emergency bootloader. The Z 30 online manual describes the
same menu-based update path.

No verified Z 30 button sequence for entering a recovery or service-loader mode
was found. Anecdotal sequences reported for other Z cameras are not evidence
that they apply to the Z 30.

## Service-level path

Nikon publishes a Z 30 repair manual with main-PCB removal and replacement
procedures, but it does not publish a Z 30 SWD/JTAG/UART pinout, factory flash
tool, or service-loader protocol. Therefore, the practical service outcomes
are:

1. Nikon reprograms the existing board with factory service equipment, if the
   board is still recoverable;
2. Nikon replaces the main PCB; or
3. Nikon diagnoses another board-level failure and quotes the repair.

The service request should describe this as an early-boot firmware/main-board
failure, not only as a black LCD. The owner should request an estimate before
authorizing a main-board replacement.

## Non-invasive research boundary

Without opening the camera, the remaining useful measurements are limited to
USB enumeration, external power behavior, SD-card activity, lens/no-lens boot
comparison, and documented button-sequence checks. Identifying flash contents,
debug pads, or a board-level boot protocol requires access to the main PCB and
is outside this non-disassembly path.

## Sources

- [Nikon Z 30 firmware download and update instructions](https://downloadcenter.nikonimglib.com/en/download/fw/556.html)
- [Nikon Z 30 online manual: Firmware version](https://onlinemanual.nikonimglib.com/z30/en/16-01.html)
- [Nikon Z 30 repair manual](https://download.nikonimglib.com/archive7/YzVuP00KpXB106Yrzhr97kms0532/Z30_RM_%28En%2902.pdf)
- [Nikon USA repair portal](https://repair.nikonusa.com/en/)
