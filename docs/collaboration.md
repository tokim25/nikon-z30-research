# How Claude and Codex work in parallel

Two AI sessions work on this project at the same time. The owner decides
what merges. Hard limits stay in [AGENTS.md](../AGENTS.md).

## Lanes

Each lane owns a set of files, listed in `.github/lanes.json`. CI fails a
pull request from a `claude/*` or `codex/*` branch that edits the other lane's
files. Shared files are open to both.

- Claude: simulator drawing and display work, `docs/native-*`, `docs/guide*`.
- Codex: tracking entry-point research, static analysis tooling, tests.
- Shared: `docs/facts.md`, `docs/roadmap.md`, `AGENTS.md`, `.github/`.

## Rules

1. Branch from `main` as `claude/<topic>` or `codex/<topic>`. Never push to
   `main`, and never merge your own pull request.
2. Open small pull requests. Each states what was observed, what was
   inferred, and the command that reproduces it.
3. Record each finding as a line in [facts.md](facts.md). Append only. To
   correct an entry, add a new one that supersedes it.
4. Keep your handoff file current: `docs/handoff.md` for Claude,
   `docs/handoff-codex.md` for Codex.
5. Work tracked in GitHub issues carries a `lane:` label. Anything that needs
   the owner is labeled `status:needs-user`; stop and wait.
6. Restricted inputs stay outside the checkout. Never search the disk for
   firmware, and never publish raw output.

## Convergence

Research ends in feature specs: hook point, arguments, preconditions, and the
simulator test that proves it. Turning specs into a build is a separate
phase, described in [build-phase-gate.md](build-phase-gate.md), and it needs
the owner's explicit approval.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
