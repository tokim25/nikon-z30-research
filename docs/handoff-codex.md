# Codex continuation handoff

Updated 2026-10-16. The owner resumed work until 8% remaining account usage.
No hardware approval was given. Personal build work is open; hardware stays
NO-GO. All 54 baseline tests and artifact checks pass.

Current branch: `codex/xpan-persistent-native-mask`, from main `32a9da5`,
in `work/codex-tracking-resume`. The primary checkout remains on main.
PRs #34 through #42 remain open. Preserve every fact/report and use the latest
handoff when resolving integration conflicts; the owner merges, never Codex.
PR #35 records the user-approved guide/RAW document takeover.

F-042 and [the mask report](xpan-persistent-native-mask.md) establish persistent
native black crop masks after one diagnostic clip-flag write and native
geometry/color setup. Two calibrated runs leave rows 107–372 visible, survive
three refreshes and restore cleanly. No per-cycle rectangle injector or queue
gate override is used. This is not natural startup or an installable feature.

Single next guide step: establish the current mode's native clip-enable and
startup ownership before using the surface initializer `0x104b5fd4`.
It is an unverified lead, not a clip-only setter. Menus, focus overlays,
repeated toggles, reboot persistence and saved RAW remain untested.

Other work awaiting publication: a bank-mapped queued input route (F-038),
separate bank selection/ID mapping (F-043), and registry/mode-object state
(F-041). No physical AE-L/AF-L input or tracking entry is verified. RAW
structure packing has not been identified as NEF metadata; preserve its
private leads without promoting field-offset matches to file evidence.

Confirmed WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Existing inputs are immutable. New codex-prefixed helpers/output stay outside
Git; detailed logs, pixels, memory and extracted listings never enter Git.
Each report gives a fresh-directory repro. Disable bytecode writes and use
isolated debugger ports. Original hash and pinned clean simulator are checked.
No original firmware file/instruction or hardware was changed.

Written by Codex in collaboration with Tony Kim; continues Claude's work with independent Codex agent checks.
