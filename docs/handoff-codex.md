# Codex continuation handoff

Updated 2026-10-16. The owner resumed offline work until 8% remaining usage.
Research has stopped for publication and handoff. No hardware approval was
given. Original firmware and simulator checkout remain unchanged.

PRs #34 through #47 contain the prior milestones. Current branch
`codex/xpan-mask-menu-lifetime` adds F-044: two diagnostic mask toggle cycles
pass, independently repeated, but the mask persists over audited menu entry.
The subsequent live-view entry left the stack at two entries, so it did not
establish natural menu exit. See [the report](xpan-mask-menu-lifetime.md).

PR #43 is the strongest display result: persistent stock black crop masking
after diagnostic clip-state setup. It does not crop a saved RAW. PR #47
traces a structure pack but does not establish source identity or NEF
serialization. Physical AE-L/AF-L routing and a tracking entry point remain
unverified. Next: establish native clip-state cleanup across menu entry and
a verified return to live view.

Branches start from main `32a9da5`. Preserve every appended fact while
resolving conflicts and prefer the final session handoff over this interim
copy. Owner merges; Codex never merges. Private helpers/output stay under
the user-confirmed WORK outside Git; reports give fresh-directory repros.
Original inputs are immutable. Local baseline: 54 synthetic tests pass.

Written by Codex in collaboration with Tony Kim; continues Claude's work and the prior Codex handoff.
