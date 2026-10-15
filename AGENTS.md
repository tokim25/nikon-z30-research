# Contributor instructions

This directory is the project root. Never initialize Git in a parent directory.

## Scope and collaboration

- Respect explicit exclusive file ownership assigned by the coordinating session. Do not modify another agent's files or revert unrelated changes.
- Use `apply_patch` for edits. Read applicable nested instructions before editing.
- This is a new scaffold. Prior milestone files have not been recovered; never describe new code as recovered milestone code.
- Do not commit, push, or publish issues until the coordinating session explicitly declares integration ready and authorizes the relevant publication step.

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
