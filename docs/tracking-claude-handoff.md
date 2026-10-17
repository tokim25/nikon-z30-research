# Lane 3 pickup for Claude

Prepared 2026-10-16 at the owner's request to hand off near the Codex
usage limit. This is the AE-L/AF-L subject-tracking lane, not the drawing
or saved-crop lanes. Read AGENTS.md's Priority section, the Lane 3 section
of handoff-codex.md, then tracking-protect-button.md's dated continuations.
The latest two sections contain the current trail; earlier BLE hypotheses
were explicitly retired and must not be revived.

## Exact repository state

- Checkout: `/Users/tonykim/Documents/GitHub/nikon-z30-research`.
- Branch: `codex/tracking-property-dispatch`.
- Starting HEAD: `3264c5e4c3a52fb70d22759a5b35c4c7cece5c43`.
- The owner subsequently authorized committing and pushing this Lane 3
  checkpoint on the existing branch. Read `git log -1` for its final hash.
- Checkpoint files: `docs/corrections.md`, `docs/handoff-codex.md`,
  `docs/project-status.md`, `docs/tracking-input-chain.md`.
- New checkpoint files: `docs/tracking-protect-button.md` and this handoff.
- All six files belong to this Lane 3 session. Preserve this checkpoint;
  do not reset or replace it to start over. No pull request was requested.

No firmware or private reports are in the checkout. The owner authorized
the branch commit and push after this handoff was prepared. Continue on
this branch unless directed otherwise; no merge is authorized. The
Codex branch's lane rules already cover the tracking documents. Keep the
other lane's simulator infrastructure untouched.

## What is established

1. The original property cluster is BLE control/authentication machinery.
   Its generic lookup, subscriber and dispatcher were resolved and two
   bounded menu probes completed. This is a retired physical-button lead.
2. The Protect clue identifies separate shooting and playback assignments:
   `0x1184` and `0x1186`; mode 1 uses `0x1187`. Preserve playback Protect.
3. Subject tracking is native assignment value 77, label index 1561.
   Four other configurable-button handlers dispatch it to `0x10368b6e`.
   AE-L/AF-L handler `0x10369468` omits that case, and the helper itself
   rejects logical input `0x0d`. A menu-only change is insufficient.
4. Native request candidates reach `0x100774f4` / `0x100775c6` and
   real tracking state. The status bridge, numerical start/stop gates and
   native exclusion predicate are traced. Handler return means handled,
   not acquired. No runtime tracking start/stop or acquisition was tested.
5. The AF-ON branch tests held state. Snapshot `+0x10` carries press
   edges. A 32-call stock-decoder probe confirms press and hold both
   produce the same logical id; release outputs zero. Chord arbitration
   and the return-register/output distinction are documented.
6. A separate six-call stock FIFO probe confirms that `r5` retains the
   exact popped record across `0x102f1dbc` -> `0x102f1dc0`, with its
   press edge intact. `r4` is the decoded-output destination. This is a
   candidate worker-side boundary, not an installed or validated hook.

## Single next step

Trace the real AE-L/AF-L assignment-menu option rows, selected-value
mapping and setter callbacks around `0x103d4222` / `0x103d9898`.
Produce a coordinated change plan covering value-77 visibility, action
dispatch, same-record edge gating and existing native completion cleanup.
Account for both direct calls to `0x10369468`, including the combined
input path. Preserve stock context checks, native eligibility and chord
arbitration. Do not substitute a newer global snapshot, invoke tracking
in the input callback, or treat a held logical id as a fresh press.

The complete address/ABI details and limits are in tracking-protect-button.md.
No adapter or installable patch exists. All work remains offline and
simulator-only; never touch the owner's camera. Hardware remains NO-GO.

## Private reproduction

Confirmed WORK:
`/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work`.
Do not search the disk for firmware. The original hash and pinned QEMU
revision are checked by each live helper, and remained unchanged/clean.

- `codex-protect-button-route-private.py`: initial switch/menu/action links.
- `codex-tracking-native-contract-private.py`: extended static assertions,
  status bridge, AF-area table consumers and synthetic arithmetic checks.
- `codex-tracking-input-semantics-private.py`: completed decoder run in
  `private-inputs/codex-tracking-input-semantics-01`.
- `codex-tracking-queued-edge-private.py`: completed FIFO run in
  `private-inputs/codex-tracking-queued-edge-01`.

Run scripts with WORK's `analysis-env/bin/python`. Live scripts require
`--output` naming a new private directory, never an existing report or a
path inside the repository. Raw audits, frames and firmware-derived
material remain private; publish only descriptive addresses and findings.

## Validation and publication boundary

Final validation on 2026-10-16: all 54 standard unit tests passed, both
artifact scripts and `git diff --check` passed, and both untracked documents
passed direct encoded-data scans. The full local research diff and the
new documents were manually reviewed. The static verifier and both new
diagnostic runs also passed. Both disposable QEMU processes were closed.
No research process or automatic continuation is left running.

Before publication after further edits, rerun the three standard checks and
review all local prose, including both untracked files; the tracked-file
scanners do not cover those automatically.
No fact number was allocated; findings were appended to tracking documents
as the owner allowed. The later owner instruction authorizes committing and
pushing this checkpoint; it does not authorize merging it.

The owner requested stopping Codex research at 7% or less five-hour usage
remaining, reserving the end for handoff. This is an explicit session handoff,
not a recurring task or automatic continuation promise.
