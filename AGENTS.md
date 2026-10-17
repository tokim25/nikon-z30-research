# Contributor instructions

This directory is the project root. Never initialize Git in a parent directory.

## Start here

Before anything else, read [docs/session-manager-brief.md](docs/session-manager-brief.md) for the current project state, owner rules, and blockers. Then read your lane's handoff file. It records the current
state, the single next step, and how to resume after a stalled session.

- Codex: [docs/handoff-codex.md](docs/handoff-codex.md), tracking research.
- Claude: [docs/handoff.md](docs/handoff.md), simulator drawing work.

Then read [docs/project-status.md](docs/project-status.md) for open pull
requests, merge order, sessions in flight and reserved fact numbers, followed
by [docs/collaboration.md](docs/collaboration.md) and
[docs/facts.md](docs/facts.md). If your handoff file is out of date, fix it
first. Update it before you stop, even when a session ends early.

## Priority: stay hyper-focused on the real build

Owner direction, 2026-10-16: this project exists to test modded firmware on
the owner's own real camera (personal, non-distributed, risk explicitly
accepted — see [docs/build-phase-gate.md](docs/build-phase-gate.md)). Before
starting or continuing any research thread, in either lane, ask: **does this
lead toward a concrete patch, hook point, or build decision for the real
firmware, or is it only explaining a limit of this project's own simulator?**

- Tracing real firmware logic (what a function does, what it calls, what
  format it uses) is in scope even when read entirely through static
  decode, because it describes the actual firmware and transfers to
  hardware.
- Tracing *why the simulator itself* fails to model something (an
  unimplemented peripheral, an event that never fires under QEMU's generic
  device model, a card the simulator can't make the firmware accept) is
  **low priority** unless it is the one thing blocking a specific, named
  build decision. A simulator-fidelity dead end is worth one fact
  documenting it, then dropping — not a multi-session trace.
- When a thread's next step is ambiguous between "keep tracing what the
  simulator can't do" and "trace what the real firmware would need for the
  feature," take the second. If genuinely unsure which a next step is,
  say so in the handoff file rather than picking by default.
- This applies retroactively: if an open thread in a handoff file doesn't
  clearly lead to a buildable artifact or an informed patch decision,
  mark it low priority or drop it there, don't just keep extending it.

## Scope and collaboration

- Respect explicit exclusive file ownership assigned by the coordinating session. Do not modify another agent's files or revert unrelated changes.
- Use `apply_patch` for edits. Read applicable nested instructions before editing.
- This is a new scaffold. Milestone 1 originals were recovered and verified locally; see docs/milestone-1-recovery.md. Never describe newly written code as recovered code. Keep the recovered tools and raw reports outside Git because some include firmware excerpts.
- Parallel work follows [docs/collaboration.md](docs/collaboration.md): file lanes in `.github/lanes.json`, branches named `claude/<topic>` or `codex/<topic>`, and findings appended to [docs/facts.md](docs/facts.md). The owner approves and merges every pull request.
- Commit to your own lane branch and open a pull request when the owner has asked you to publish work. Never push to `main`, never merge your own pull request, and never open issues or change repository settings without the owner's say-so.
- A build phase is open, for the owner's personal, non-distributed camera only. See [docs/build-phase-gate.md](docs/build-phase-gate.md) for its scope and for what still gates actual hardware access. Never flash or connect a real camera without the owner's separate, explicit go-ahead at that step, even under this authorization.

## Research and publication

- All analysis is offline. Never flash hardware or create an installation
  workflow. **Never touch the owner's real camera**, in any form.
- Local, simulator-only experimentation is allowed for testing a hypothesis:
  you may try code or byte changes in a throwaway local copy of the firmware
  and run it only in the pinned QEMU simulator on this machine. This does not
  open the build phase. A modified copy, its diff, or anything derived from
  it stays outside the repository and is never committed, pushed, or
  attached to an issue; summarize the result in prose instead.
- Never publish Nikon firmware, extracted bytes, dumps, installable patches, credentials, or proprietary artifacts in any repository surface.
- Use synthetic fixtures only. Do not embed real bytes as hex, base64, strings, or generated test data.
- Keep restricted inputs outside the repository. `.gitignore` and automated checks are defense in depth, not publication permission.
- Keep the GitHub repository private unless the user separately authorizes a visibility change.

## Validation

- Keep Python code under `src/` and standard-library unittest tests under `tests/`.
- Run `PYTHONPATH=src python -m unittest discover -s tests -v` and `python .github/scripts/check_artifacts.py` before publication.
- Review the full staged diff, file list, and any history being pushed. Automated checks cannot reliably detect encoded firmware or sensitive prose.
- Codex work occurs in explicit sessions. Recurring or background work requires separate user authorization and an actual configured automation; never promise automatic continuation.

## Owner-approved camera rules (2026-10-17)

The owner approved revised camera-contact rules on 2026-10-17. See
[docs/proposed-rules-2026-10-17.md](docs/proposed-rules-2026-10-17.md).
Read-only identification of the Z 30 is pre-approved. Any write to the camera
still needs the owner's approval for that exact step, given in one reply.
Firmware bytes stay on the owner's local machine and never enter the repository.
