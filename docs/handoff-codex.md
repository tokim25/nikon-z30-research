# Codex handoff

Updated 2026-10-15. Research stopped near the owner's 8% usage threshold.
The owner resumed both feature tracks and approved the guide/RAW file transfer
recorded in PR #35. Personal build work is open; hardware access is not.

PRs #34 to #39 are open: input-ring correction, ownership/bit-field mapping,
structured input cache, successful 65:24 geometry, screen-stack limitation,
and numeric-command attribution. Preserve every fact when integrating.
All branches start from main `32a9da5`; ledger/handoff conflicts need the
owner's resolution. Never merge our own PRs or push main.

Current branch: `codex/xpan-compose-completion`. F-035 and
[xpan-compose-completion.md](xpan-compose-completion.md) reject the selected
completion callback as a pre-flush hook. The single next guide step is to
trace draw submissions before composition and establish callback ownership.

Confirmed private WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Existing inputs stay unchanged. New private helpers/output use codex prefixes.
Report pages give fresh-directory repro commands. Original hash and pinned,
clean simulator are checked. No raw output enters Git.

Other verified results: temporary guest data produced centered 5200 by 1920
geometry in two A/B/A runs, controls unchanged and restored. This is not saved
RAW evidence. Assisted live-view startup/refresh had empty screen stack; menu
entry control populated it. The candidate structured-input handler has a
numeric-command route; physical AE-L/AF-L input is still unknown.

Remaining unpublished source audit and final cross-track handoff are being
saved next. No agent is doing further research. Hardware readiness stays
NO-GO: debugger-free guides, saved RAW behavior, tracking and recovery remain
unverified. Baseline 54 tests and publication checks pass.

Written by Codex in collaboration with Tony Kim; continues Claude's work and includes independent Codex agent checks.
