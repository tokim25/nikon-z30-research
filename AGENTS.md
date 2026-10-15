# Contributor instructions

This directory is the project root. Never initialize Git in a parent directory.

## Start here

Before anything else, read your lane's handoff file. It records the current
state, the single next step, and how to resume after a stalled session.

- Codex: [docs/handoff-codex.md](docs/handoff-codex.md), tracking research.
- Claude: [docs/handoff.md](docs/handoff.md), simulator drawing work.

Then read [docs/collaboration.md](docs/collaboration.md) and
[docs/facts.md](docs/facts.md). If your handoff file is out of date, fix it
first. Update it before you stop, even when a session ends early.

## Scope and collaboration

- Respect explicit exclusive file ownership assigned by the coordinating session. Do not modify another agent's files or revert unrelated changes.
- Use `apply_patch` for edits. Read applicable nested instructions before editing.
- This is a new scaffold. Milestone 1 originals were recovered and verified locally; see docs/milestone-1-recovery.md. Never describe newly written code as recovered code. Keep the recovered tools and raw reports outside Git because some include firmware excerpts.
- Parallel work follows [docs/collaboration.md](docs/collaboration.md): file lanes in `.github/lanes.json`, branches named `claude/<topic>` or `codex/<topic>`, and findings appended to [docs/facts.md](docs/facts.md). The owner approves and merges every pull request.
- Commit to your own lane branch and open a pull request when the owner has asked you to publish work. Never push to `main`, never merge your own pull request, and never open issues or change repository settings without the owner's say-so.
- A build phase is closed. See [docs/build-phase-gate.md](docs/build-phase-gate.md). Do not create installable output, patched images, or hardware steps unless the owner opens that phase in this file.

## Research and publication

- All analysis is offline. Never flash hardware or create an installation workflow.
- Never publish Nikon firmware, extracted bytes, dumps, installable patches, credentials, or proprietary artifacts in any repository surface.
- Use synthetic fixtures only. Do not embed real bytes as hex, base64, strings, or generated test data.
- Keep restricted inputs outside the repository. `.gitignore` and automated checks are defense in depth, not publication permission.
- Keep the GitHub repository private unless the user separately authorizes a visibility change.

## Validation

- Keep Python code under `src/` and standard-library unittest tests under `tests/`.
- Run `PYTHONPATH=src python -m unittest discover -s tests -v` and `python .github/scripts/check_artifacts.py` before publication.
- Review the full staged diff, file list, and any history being pushed. Automated checks cannot reliably detect encoded firmware or sensitive prose.
- Codex work occurs in explicit sessions. Recurring or background work requires separate user authorization and an actual configured automation; never promise automatic continuation.
