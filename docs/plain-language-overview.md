# The project in plain language

This is a guide for anyone who is not an engineer. It explains what the
project is, where it stands, and what the rules are. The detailed technical
notes live in the other files; this one is the map.

## What we are trying to do

A Nikon Z30 is a camera. Like most cameras, it runs a small built-in program
called firmware. Firmware is the software that tells the camera how to focus,
how to show a picture on its screen, and how to save a photo.

The owner wants to add two features to their own camera by changing its
firmware:

1. **XPan framing.** A very wide, letterbox-shaped photo, like old panoramic
   film cameras. On screen, black bars at the top and bottom would show the
   wide frame while you shoot.
2. **Subject tracking.** The camera follows a moving subject to keep it in
   focus, started by a button on the back of the camera.

## How the work is done, and why it is slow

Changing a camera's firmware is risky. A bad change can turn the camera into a
brick that no longer turns on. So almost all of the work happens on a regular
computer, never on the camera.

Two things make it painstaking:

- **The firmware is like a locked machine with no manual.** Nobody outside
  Nikon has the instructions. Progress means reading the camera's own program,
  one piece at a time, and working out what each piece does. The notes are
  full of numbers like `0x101cd3cc`; each one is an address, a location inside
  the program, the way a house has a street number.
- **A simulator stands in for the camera.** A simulator is a program that
  imitates the camera's hardware, so the camera's firmware can run on a plain
  computer. It is close, but not a perfect copy. Some things the real camera
  does cannot be tested in the simulator at all.

Two assistants do this work in parallel, called Claude and Codex. The owner,
Tony, reviews and approves everything. Neither assistant is allowed to change
the real camera.

## Where things stand today

Nothing is ready to put on a camera. There is no finished, installable
version of either feature. The camera is marked **NO-GO**, meaning no
modified firmware may be installed on it.

What exists so far is research and partial pieces:

- The on-screen black bars for XPan have been built and tested in the
  simulator, but only the bars, not the rest of the feature.
- The parts that read and check a firmware package have been built and tested
  with made-up data.
- Subject tracking has a draft design, but no way to start it has been proven.

The main things still blocking a real build:

- **Proving the preview path.** When the camera saves a wide photo, it also
  saves a small preview image inside the file. That preview has to match the
  new shape, and the work to prove this has only just been identified, not
  finished.
- **One unresolved checksum input.** When the camera accepts a firmware
  update, it checks a kind of fingerprint. Eight bytes that feed one of those
  checks have not been located. Until they are, a changed firmware package
  cannot be shown to pass the camera's own checks.
- **Lifecycle gate.** Nobody has yet shown, start to finish in the simulator,
  that the camera starts up, enters and leaves menus, and plays back photos
  normally with the change in place.

## The rules that never bend

These come from the project's contributor rules and the owner's decisions:

- **Never touch the real camera** without the owner's separate, explicit
  go-ahead for that exact step. Read-only identification of the camera is the
  one thing already allowed.
- **No firmware in the project files.** The camera's firmware belongs to
  Nikon. It, and anything pulled out of it, stays on the owner's own computer
  and never goes into the shared repository.
- **The owner approves everything.** The assistants propose; Tony decides and
  merges. Neither assistant merges its own work.

A note on "waivers": the owner has accepted certain risks in writing, such as
not being able to verify every byte of the installed firmware. Accepting a
risk is not the same as a step being proven safe, and it is never permission
to install anything. The camera stays NO-GO.

## Where to read more

- Current state and blockers: `session-manager-brief.md` (read first).
- Open work and merge order: `project-status.md`.
- The rules for touching hardware: `build-phase-gate.md`.
- Every recorded finding, in order: `facts.md`.

Written by Claude in collaboration with Tony Kim.
