# Final Codex handoff for Claude

Updated 2026-10-15. Research stopped to honor the owner's 8% remaining-usage
cutoff. No agents continue working. Personal build work is open; hardware
access remains closed. No installable firmware was produced.

The owner resumed tracking and approved Codex taking over guide/native and
RAW-crop documents. PR #35 records the exact ownership/test changes.
Read this handoff before older paused-lane notes. Agree ownership before
concurrent edits; simulator infrastructure retains its previous assignment.

## GitHub integration

All work starts from main `32a9da5`. Nothing was merged by Codex.
The owner merges. Preserve all append-only facts and use this final handoff
when resolving ledger/handoff conflicts:

| PR | Fact | Result |
| --- | --- | --- |
| #34 | F-025 | Two input-ring writers, correcting F-021. |
| #35 | F-026 | Distinct bit-13 fields; file transfer and feature plan. |
| #36 | F-027 | Structured control into input cache, physical source unknown. |
| #37 | F-036 | Two successful centered 65:24 geometry A/B/A runs. |
| #38 | F-029 | Assisted live-view screen stack empty; menu control populated it. |
| #39 | F-028 | One candidate input route parses numeric commands. |
| #40 | F-035 | Selected completion callback runs after compose; too late for current guide flush. |
| Current branch | F-037 | Functional ISP exists; saved-RAW pipeline remains unverified. |

Current branch: `codex/final-claude-handoff`, in dedicated worktree
`work/codex-tracking-resume`. The primary checkout remains on main.
Merge in the listed order and retain every report; these branches share a
base, not an integration history. Do not replace the ledger with one branch's
copy. F-025 to F-037 are now allocated; next free fact is F-038, subject to
checking main/open PRs.

## Single next step

Inspect independent cache-setter calls at `0x103a3e88` and `0x103a400c`
for a physical input source. The numeric-command route is not evidence of an
AE-L/AF-L press. No tracking entry point or normal input delivery is verified.

Other resumable leads, not established interfaces:

- RAW: geometry descriptors reach request field `+0x20a` at candidate
  callers `0x1015382a`, `0x1015f978`, `0x1016238e`; the latter continues
  through `0x1015336c`. Trace toward NEF metadata/storage. No writer contract
  was verified. Filename anchors are not writer evidence.
- Guides: trace draw submissions before `0x103c2232` queues composition.
  Object callback `0x103c3500` had zero hits in one stock refresh; its
  lifetime interpretation remains unverified. No debugger-free hook exists
  in the evidence so far.
- Input fixture: establish stock shooting-screen initialization. A synthetic
  preview can render with an empty menu/screen stack; avoid guessed key calls.
- Snapshot/cache-pair link from the earlier linear symbolic script remains
  unreviewed; do not rely on it without checking branches and register flow.

## Private reproduction and checks

Confirmed WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Keep existing inputs unchanged. New helpers and outputs are codex-prefixed
outside Git. Every report supplies private repro commands with fresh output
directories. Runtime imports disable bytecode writes; each simulator uses
its own local debugger port and absolute private output path.

Successful geometry runs: `codex-agent-raw-geometry-probe-02` and
`codex-root-geometry-probe-01`. Temporary guest data produced centered
5200 by 1920 geometry; DX/16:9 controls were unchanged and restoration exactly
recovered baseline. Original firmware files and instructions were untouched.
This did not capture or save a RAW image.

Unreviewed NEF leads remain in private `codex-agent-raw-geometry-context-01`
and `codex-agent-raw-format-anchor-xrefs-01`. Guide producer observations
are in `codex-guide-producer-observation-01`. Do not import raw memory,
firmware, screenshots, logs or extracted listings into Git.

All publication branches passed 54 local unit tests and artifact/encoded-data
checks. CI results must be checked on GitHub for the latest heads. The
original module hash and pinned clean simulator were checked. No patch
builder, hardware access, original firmware edit or installation workflow
was used. The only firmware-data experiment was inside a disposable guest.

Hardware readiness stays NO-GO: debugger-free guides, saved RAW behavior,
physical-button tracking, failure containment and recovery remain unresolved.

Written by Codex in collaboration with Tony Kim; continues Claude's research and includes independent Codex agent reviews.
