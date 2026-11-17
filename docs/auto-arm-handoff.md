# Auto-arm dry run: handoff for a local session

Date: 2026-11-17. For a Claude Code session on the owner's Mac. Read this,
then `AGENTS.md`, then `modules/auto_arm/README.md`.

## The goal

With Auto-area AF selected, the camera should sit in the tracking-ready screen
(the reticle OK brings up) without a button press. A half-press then starts
tracking, and upstream's 3D tracking switches it to a face or animal that comes
into view. No button is remapped.

`modules/auto_arm` does this as an SD add-on for Wonder Lantern's module host.
It sends one OK press whenever the camera is idle in photo live view in
Auto-area AF. The dry-run build presses nothing; it logs when it would have
pressed. The full background is in `docs/one-button-tracking-plan.md`.

## Where things stand

- The add-on compiles and packages. It has not run on an emulator or a camera.
- Its base firmware is upstream PR #36 at `8715c25` or later, which is also
  not yet confirmed on a camera. Upstream's earlier PR #36 builds ran on
  Z30s, including the pieces the add-on reuses.
- The owner decided to run the dry run now, without waiting for the PR
  reviewer to confirm `8715c25`.

## What the session does

1. Ask the owner for the full path to `Z_30_0120.bin`. Never search the disk
   for firmware (`docs/collaboration.md`, rule 6).
2. Check that `arm-none-eabi-gcc` is installed. If not, ask the owner to run
   `brew install --cask gcc-arm-embedded`.
3. Run, from this repository's root:

       sh modules/auto_arm/prepare_mac.sh /path/to/Z_30_0120.bin

   It checks the firmware's hash, fetches PR #36 into `~/z30-auto-arm`, runs
   upstream's unit tests, builds the research firmware and the dry-run
   add-on, and prints the output hashes. Everything stays in
   `~/z30-auto-arm`, outside this repository.
4. Report to the owner: the PR commit used, the upstream test result, the
   compiler version, and the two output hashes. If anything failed, stop and
   explain; do not work around a failed check.
5. Walk the owner through "On the camera" below. The owner does every camera
   and card step. The session never connects to the camera.
6. When the owner has the log, run the reader (below) and explain the result.

## Rules that apply

- `AGENTS.md` governs. In particular: firmware, built images and logs never
  enter this repository; no camera contact by the session; any camera write
  needs the owner's go-ahead for that exact step.
- Installing the research firmware is a camera write. Before step 5, show
  the owner the EG hash and get an explicit go-ahead.
- Recovery: keep `Z_30_0120.bin`. Upstream says stock firmware can be
  reinstalled from Setup → Firmware version as long as that screen opens.
  This repository has not verified that (`docs/hardware-readiness.md`).

## On the camera (owner)

1. Charged battery; card formatted in the camera.
2. Copy `~/z30-auto-arm/OUT/EG209020.BIN` to the card root, and the folder
   `~/z30-auto-arm/OUT/Z30` (with `CORE.ZMOD`) to the card root.
3. Setup → Firmware version → Update. Wait for it to finish.
4. Set AF-area mode to Auto-area AF (people).
5. Setup → Extensions → SD Modules → Load CORE.ZMOD, then Run module. The
   screen should say "Auto-arm dry run, Run=save". Timing starts here.
6. Follow this sequence, noting roughly when you switch:

   | Time | Do this |
   | --- | --- |
   | 0–20 s | Photo live view, press nothing |
   | 20–35 s | Open the i menu and leave it open |
   | 35–50 s | MENU, browse |
   | 50–65 s | Playback |
   | 65–80 s | Live view with AF-area mode Single-point |
   | 80–95 s | Video mode live view |
   | 95–110 s | Photo live view, Auto-area AF (people) |

7. SD Modules → Run module again. The screen should say "Saved, presses N".
8. Copy `Z30/ARnnnnnn.BIN` from the card to the Mac.

If the camera freezes, pull the battery. Power off also disarms the add-on.

## Reading the log

From this repository's root:

    PYTHONPATH=src python3 -m nikon_z30_research.auto_arm_log /path/to/ARnnnnnn.BIN

Pass: entries about every 1.6 s during 0–20 s and 95–110 s, none in between,
no UNEXPECTED lines. Each line shows the UI phase, UI state, photo backend
and AF-area mode it read.

## After the dry run

- Pass: next is the version that presses OK. Build it with
  `sh modules/auto_arm/prepare_mac.sh /path/to/Z_30_0120.bin --remap`. It
  keeps the installed firmware and rebuilds only `CORE.ZMOD`. Copy the new
  `Z30` folder to the card. No firmware update is needed. Checks: the
  tracking box appears by itself in Auto-area AF, a half-press starts
  tracking, the box comes back when tracking ends, and nothing happens in
  menus, playback, video or other AF-area modes. Needs the owner's go-ahead.
- UNEXPECTED entries: do not build the pressing version. Record which screen
  produced them, from the owner's timings, and work out which state value
  failed to exclude it.

## Recording results

Summarize results in prose in `docs/one-button-tracking-plan.md` and append
a finding to `docs/facts.md` (next free F-number per `docs/project-status.md`).
Never commit the log, firmware or build outputs. Commit to a `claude/` branch
and open a PR only if the owner asks.

## Kickoff prompt

Paste this into a new Claude Code session started in this repository on the
Mac, on branch `claude/beautiful-johnson-uvcfn6`:

> Read docs/auto-arm-handoff.md and follow it. I want to run the auto-arm dry
> run today. Ask me for the firmware path first.

Written by Claude in collaboration with Tony Kim.
