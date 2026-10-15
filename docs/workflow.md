# Research and integration workflow

## Explicit sessions

Start each Codex session with a concrete objective, the project root, and file ownership. Read `AGENTS.md`, inspect existing changes, and preserve other contributors' work. End with completed work, validation evidence, unresolved questions, and the next actionable step. Sessions do not continue automatically after ending.

Recurring or background work requires separate user authorization and a configured automation with a defined scope and notification policy. Repository creation and publication authorization alone do not authorize automation.

## Offline analysis

Keep analysis offline and use synthetic data for tests. Store any restricted inputs outside this checkout. Never flash hardware or publish firmware, extracted bytes, dumps, or installable patches. The same restrictions apply to encoded strings, screenshots, logs, issue attachments, releases, and Git history.

## Integration gate

1. Each owner completes only their assigned files and reports validation results.
2. The coordinator integrates source, tests, roadmap, and documentation, resolving missing CLI documentation with the tooling owner.
3. The coordinator explicitly declares integration ready before anyone commits or pushes. Do not stage unrelated concurrent changes.
4. Initialize Git only at this project root if needed. Confirm the repository owner and private visibility and inspect the remote before publication.
5. Stage the intended scaffold, then inspect `git diff --cached --stat`, `git diff --cached`, and `git ls-files`. Review any existing commits that would be pushed as well.
6. Run `PYTHONPATH=src python -m unittest discover -s tests -v` and `python .github/scripts/check_artifacts.py`. Confirm discovery includes the intended tests; an empty test run is not meaningful validation.
7. After the coordinator's publication instruction, commit and push the reviewed scaffold. Verify the remote remains private and inspect CI results.
8. Create approved roadmap issues from reviewed text only, checking existing issues to avoid duplicates. Do not attach research inputs or raw analysis output.

## Artifact gate limitations

The automated check restricts tracked files to small UTF-8 source and documentation files, rejects symlinks and restricted directories, and detects null bytes. It does not inspect ignored or untracked files, historical commits, issue content, or semantic provenance. It cannot distinguish safe synthetic text from proprietary bytes encoded as text. Manual review remains mandatory.

CI validates pushed content; it cannot prevent an initial upload. Run checks and content review locally before pushing. CI installs no project dependencies, uploads no artifacts, and uses a read-only repository token. GitHub-hosted CI is scaffold validation, not a place to analyze firmware.

If restricted material is accidentally staged, unstage it and move it outside the checkout. If it has been committed or uploaded, stop further publication and notify the coordinator; deleting it in a later commit does not remove it from history.
