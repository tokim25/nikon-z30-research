# Claude research handoff: path to a real-camera test build

2026-10-17. Owner requested pausing Codex and handing research to Claude.
No camera access, simulator run, patch encoding, firmware output, commit,
push or PR occurred during this handoff investigation. Earlier local changes
remain uncommitted; preserve them. This is a new lead, not a READY decision.

## Consolidated session status

Publication update: main 512e6b3 now records later owner waivers for lifecycle,
still-photo guard and byte-exact installed identity in session-manager-brief.md
and test-readiness-2026-10-17.md. They supersede this packet's earlier
retained-gate wording; they are not successful measurements or permission to
flash. Current task authorizes commits/PRs for review, with no merge, hardware
or firmware encoding. Local findings formerly F-150--F-155 are now F-156--F-161;
merged F-135--F-155 are preserved. No new research was performed for this update.

| Session | Completed | Stopping point |
| --- | --- | --- |
| Firmware/XPan, primary checkout | Original decode/round trip, container/exact-edit/installation models; F-148 corrected bars hooks; bounded pixel/cycle/ABI controls; digest arithmetic verification; public-repository triage and standalone-EG static lead below. | No complete XPan image. Still-photo eligibility/exclusion guard unresolved: stack-empty/selector-1 is not proof. Camera-ready NO-GO. Label, capture/preview edits, final review and retained lifecycle gate remain open. |
| Tracking, isolated checkout | Candidate assembled/linked privately; menu selection through native keys stores assignment 77; actual target-task allocation grows by 1024 to 11264; constructed admission/rejection/cleanup and seven record-copy controls pass; bounded normal-decoder pointer-lifetime review completed. | No installable image or natural tracking activation. Actual queued-edge delivery, action/decision/request-state and asynchronous lifecycle remain open. |

Tracking's authoritative current reports are in the separate checkout:

- [Tracking handoff](/Users/tonykim/.codex/worktrees/tracking-assignment-menu/nikon-z30-research/docs/tracking-claude-handoff.md)
- [Candidate review, especially its final two sections](/Users/tonykim/.codex/worktrees/tracking-assignment-menu/nikon-z30-research/docs/tracking-candidate-review.md)
- [Storage/ABI audit, final revisions supersede earlier offsets](/Users/tonykim/.codex/worktrees/tracking-assignment-menu/nikon-z30-research/docs/tracking-storage-abi-audit.md)

Tracking storage is a **16-byte decision state + 400-byte owned record** in
a **424-byte outer frame**, including alignment/return bookkeeping. Actual
added simultaneous stack depth is **472 bytes** with wrappers, within a
funded **1024-byte** increment, leaving 552 bytes. Capacity/placement audit:
964 code bytes occupy 972 of 1408 checked candidate bytes; 952 menu-data
bytes fit the reviewed 968-byte data capacity; 45 disjoint spans and 24
relocations checked. No XPan interval was taken. Bounded mapping/reference
and decoded stack checks are not global ownership, interrupt or concurrency
proof. Final private source SHA-256:
`8d90d7a808e5d513f901f686e61bcdf1bcd1a7803d23f35031207b027e06819f`.
Menu/allocation runs preceded the final unlock-entry flag correction;
constructed copy tests and rerun static checks include it. Do not describe
the earlier runs as full execution of that final revision.

For XPan, a proven still-photo predicate would close the guard's semantic
gap; none is established. This is a NO-GO for a certified stills-only or
camera-ready implementation, not proof of observed harm in every state.
The owner's explicit stills scope removed movie-predicate research as a
prerequisite for the offline prototype. Preserve both qualifications.

Saved RAW/JPEG correctness is an **on-camera test item, not a feature-work
or simulator blocker**. Simulation need not prove everything: stop fidelity
loops, retain measurable checks and state residual risks honestly. This does
not silently reverse the owner's explicit retained lifecycle gate.

## Hardware recommendation and exact approval boundary

Current recommendation: **no hardware action**. Stock identity/version reads
were owner-reported through step 5; shutdown/disconnection closure is still
unreported. They authorize neither collection of missing digest bytes nor a
modified update. Recovery is unverified; service or permanent loss remains
possible. Planning risk acceptance is not exact-test approval.

First eventual test stays one named **XPan stills + saved RAW/JPEG crop**
build, without tracking, then tracking alone, then combined features. Before
hardware, finish exact-original/edit/integrity and applicable format checks,
exact-build review, backup/risk binding, disposition of the retained lifecycle
gate, and a named READY record. Then obtain the owner's separate immediate
approval identifying **the final artifact SHA-256, bounded owner-performed
test, stop rules, and accepted service-or-total-loss risk**. No accepted
artifact hash or such approval exists yet; this handoff requests neither
flashing nor a generic repeat waiver. See
[readiness report](native-real-camera-readiness.md) and
[read-only result](native-hardware-gate-recommendation.md).

## Claude permissions-parity checklist

Verify permissions in Claude's actual session; do not assume Codex access
transfers. Record a missing capability before dependent work. This checklist
does not grant access or change settings.

- [ ] Read the same primary project at
  `/Users/tonykim/Documents/GitHub/nikon-z30-research`, branch
  `codex/firmware-preflight-plan`, currently HEAD `cf9aca2`; confirm write
  access to permitted files while preserving all local changes and lanes.
- [ ] Read the tracking checkout above, branch `codex/tracking-menu-contract`;
  confirm separate write access only if resuming that lane. Do not switch,
  reset or merge the two working directories to make them appear identical.
- [ ] Run shell/terminal commands, Python, Git reads and permitted file edits.
  Codex has verified shell execution and primary-repo/temp writes. Private
  WORK inputs are readable; this session has no blanket write permission
  there. Verify Claude's exact private-input/tool paths and output permissions.
- [ ] Read network/GitHub sources, including the private project as needed.
  Codex used connected GitHub reads when direct web fetching failed; shell
  network is restricted. A successful public web read does not establish
  private-repo authentication or Git write permission.
- [ ] If the owner later authorizes publication, verify ability to create/
  update the intended lane branch and open/update PRs. Those mutations are
  not verified by this handoff and are not authorized now. Never push main,
  merge one's own PR, change visibility or repository settings.
- [ ] Run the validation commands below in the correct checkout, with its
  actual dependencies. Verify the private analysis Python/Capstone separately
  if static firmware inspection needs them; do not install or run external
  source merely because it is accessible.
- [ ] Keep vendor bytes, tables, private code/objects/images and raw reports
  outside Git. Neither session may connect to, operate or flash the camera
  without separate explicit owner approval; approved hardware steps remain
  owner-operated only. Automation capability is not hardware authorization.

Standard checks in each affected checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 .github/scripts/check_artifacts.py
PYTHONDONTWRITEBYTECODE=1 python3 .github/scripts/check_byte_dumps.py
git diff --check
```

Scan new/untracked reports explicitly too: tracked-only scanners omit them.
Primary suite has 130 tests; tracking's separate checkout reports 54 tests.
Do not interpret those different suites as one combined integration check.

## Priority finding: native standalone EG route

Our digest investigation assumed rebuilding the outer Nikon body package.
Current upstream Wonder Lantern instead reports standalone EG installation
on the same Z30 C 1.20. Its current revision, obtained through the GitHub API,
is `f6630588810f6ecb9363bc7881fccb47e4fdb87b`. Cached web pages sometimes
show older content; use that pinned revision for further review.

- [Build documentation](https://github.com/WonderLantern/wonder-lantern-z30/blob/f6630588810f6ecb9363bc7881fccb47e4fdb87b/docs/build.md)
- [Current aspect-profile findings](https://github.com/WonderLantern/wonder-lantern-z30/blob/f6630588810f6ecb9363bc7881fccb47e4fdb87b/docs/aspect-profiles.md)
- [Aspect geometry source](https://github.com/WonderLantern/wonder-lantern-z30/blob/f6630588810f6ecb9363bc7881fccb47e4fdb87b/src/z30_extensions/features/aspect_geometry.py)

Bounded original-code inspection independently confirms these landmarks:

| Stage | Evidence in our verified original |
| --- | --- |
| Firmware menu discovery | `0x10594c1e` supplies zero to `0x10234274`; its preserved argument reaches `0x101ce206`. The zero-argument discovery table includes eleven rows. |
| Standalone filename discovery | Row `0x11570f3c` has discovery type 2 and no row callback gate. Its filename pattern matches upstream's standalone EG filename. The type-2 jump-table destination is `0x101ce2ac`, calling `0x101cd3cc`. |
| Standalone parser | `0x101cd3cc` checks length against a configured capacity, seeks/reads four bytes at offset `0x10` for a conditional comparison with running-image data, then reads eight bytes at `0x24`. Its success path clears/copies metadata and stores execution type 3 at `0x101cd498`, count 1 at `0x101cd4a0`. The conditional comparison's complete ctype/model semantics and version policy remain to be reviewed. |
| Validation selection | Getter `0x101cf8cc` returns zero for discovery types other than 4. Native caller `0x10234448` then selects `0x101ce324` at `0x10234458`. No flag or instruction was modified. |
| Standalone integrity path | `0x101ce324` loads the selected file with `0x101ce1a4`, calls native CRC at `0x101ce374`, and rejects nonzero residue. Execution type 3 subtracts two CRC bytes at `0x101ce3b4`. Discovery type 2 takes the default pointer/length setup at `0x101ce498`. |
| Main-firmware handoff | Execution type 3's dispatcher reaches `0x101ce89e` at `0x10233e04`, the previously traced main updater. Existing F-142/F-143 installation bounds remain relevant. |

This is strong static evidence for a native alternative format, not proof of
physical acceptance. Finish the complete parser, compatibility/version and
buffer/length contracts before adopting it. If verified, the missing
outer-package digest input need not block a standalone-EG candidate. Keep
the outer-package digest explicitly unresolved; do not call it recovered,
change its flag or weaken any loader check.

## Critical patch-scope correction

F-148 is twelve hashed overlays totaling 188 covered bytes. It implements
the bars hooks/template only; the stock 1:1 selection is a stand-in. It does
**not** itself contain the label or saved-crop geometry changes needed for
the owner's full XPan story. Do not simply combine those overlays and call
the result a completed XPan firmware build.

Original table pointers were re-read as metadata, correcting any temptation
to infer offsets from neighboring tables. Table base `0x12049a7c`, group
stride five pointers; area 4 is the stock 1:1 capture slot:

| Group | Area-4 target |
| --- | --- |
| 0, padded geometry | `0x115a4d9c` |
| 1, L/M/S output sizes | `0x115a4dd8` |
| 2, second padded geometry | `0x115a4e14` |
| 3, six crop variants | `0x115a4e80` |
| 4, edge/margin variants | `0x115a4ef8` |
| 5, second edge variants | `0x115a4f10` |
| 6, additional variants | `0x115a4f88` |

These addresses are verified pointers, not an approved edit list. Upstream's
independent geometry experiment modifies area 2, not area 4. Its current
runtime aspect feature also uses area 2 and native property `0x501`.
Blindly transplanting those offsets would violate our replace-1:1 scope.
Upstream reports main-image/embedded-preview mismatches, subsequent preview
fixes, and a v8 area-sync fix; these are concrete risks for a naive size-only
patch. Its black-mask feasibility document still distinguishes reference
lines from black bars. Its reported camera results do not validate ours.

## Other requested repository triage

Read-only GitHub API inspection was used where web cache failed. No foreign
code was installed or executed, and no repository was cloned.

| Blocker | Repository evidence | Actionable value / next step |
| --- | --- | --- |
| Stills guard / lifecycle | [z30-qemu README](https://github.com/WonderLantern/z30-qemu/blob/0ba0c3547ccbec09e7c861eaca35db8e82795f15/README.md) identifies assisted startup and incomplete live-view/menu round trips. Remote tree revision exactly matches our pinned `0ba0c3547ccbec09e7c861eaca35db8e82795f15`. | No new lifecycle or still-photo predicate proof. Do not rerun existing simulator limits. |
| Static hook references | Same repository's `tools/rom_xrefs.py` scans Thumb BL/optional B.W plus literal words; `tools/stock_disasm.py` provides bounded Thumb decode and PC-relative literal annotations. | Reusable reading aids already in the pinned source; not control-flow proof. Reference scan stops at `0x650000`; missing results do not prove global nonuse. Decoder output includes firmware bytes and must remain private. |
| Tracking storage/capacity | Neither inspected repository supplies verified ownership/lifetime/capacity for our tracking state. | No demonstrated placement solution; keep tracking outside the first test. |
| Hardware gates | [bullton/nikon](https://github.com/bullton/nikon/tree/0c7653a9bd26da6af00dba58e46c03f8cb789f11) README/CONTEXT describe extraction and an external gphoto2/NAS relay; CONTEXT admits no real-camera testing of the relay. | No patch acceptance, recovery or native-guard evidence. Do not deploy or connect it. |
| Decoder reuse | That repository's `analysis/nikon_extract.py` embeds tables, writes outputs and prints raw windows; it lacks our exact original/component identity and integrity contract. | No benefit over the existing verified decoder; do not execute or import its tables. Its claim that EG needs inner decryption is not evidence against our already decoded native instructions. |

## Current state and single next research task

Validate the standalone-EG route end to end statically, against the exact
original, and produce a minimal proposed artifact contract: format, preserved
headers, compatibility/version predicates, CRC coverage, size/capacity,
payload mapping, and which remaining checks truly apply. If that route is
sound, specify the minimum complete XPan edit set, explicitly separating bars,
menu label, capture geometry and embedded previews. Stop tracing simulator
fidelity or saved-file serialization: saved RAW/JPEG correctness is already
an owner-approved on-camera test item.

Codex can implement/build after the static contract is concrete. Do not
encode patches or run a simulator/hardware for this Claude research handoff.
Do not publish vendor bytes, tables, modified images or concrete patches.

Lifecycle condition 1 remains unproved; the later owner waiver is recorded
in the current brief/readiness record, not inferred from a general Go. Recovery is
unverified, with service-or-total-loss risk accepted for planning only.
Exact-build review, risk binding, a named READY record and immediate separate
owner approval remain necessary before any camera operation. No camera
collection is authorized or requested to resolve the digest.

Known private paths, original identities and F-148 manifest are in
`handoff-codex.md` and linked native reports. Private digest arithmetic helper
is temporary under `/private/tmp/z30-digest-20261017`; its source identity
and limits are recorded in `native-digest-arithmetic-verification.md`.

Documentation checks only for this handoff; no new fact number allocated.
The former F-150 collision is resolved for publication by renumbering only
unmerged local entries. The complete previous code suite last passed 130 tests.

## Transfer cleanup record

Primary branch remains `codex/firmware-preflight-plan`, HEAD `cf9aca2`.
All eleven previously untracked files were inspected and retained: nine
research/handoff/readiness reports plus `package_digest.py` and its synthetic
test file. Existing tracked research, owner-direction/checklist changes and
fact additions are intentionally uncommitted. No file was staged, no branch
was switched, and no commit, push, merge or PR was made.

Only 28 ignored generated `.pyc` cache files under `.github/scripts`,
`src/nikon_z30_research` and `tests` were removed, with their empty cache
directories. No restricted input, private evidence, source, report, test,
worktree or branch was deleted or quarantined. Historical handoffs/checkpoints
were retained and labelled so their obsolete next steps do not supersede
this packet. The readiness report now points here before its older
outer-package-only digest plan. Two pre-existing AGENTS.md links in the Codex
handoff were corrected to their parent-relative path.

Fact-number audit: F-081 and F-110 each appear twice already on current
local main. Local additions F-156 through F-161 introduce no further
duplicate within this checkout. Claude branch `claude/sharp-bartik-ed4fb7`
has F-150, now merged on main; our formerly colliding finding is now F-156.
Both findings and their links are preserved. The tracking branch adds
no colliding fact IDs relative to main in this check. Append-only facts were
not rewritten. No remote refresh was performed for this local-state audit.

Seven registered worktrees were inspected read-only and preserved: primary,
tracking-assignment-menu, and Claude's funny-fermi, infallible-herschel,
sharp-bartik, vigilant-bose and xpan-stills-route checkouts. Their distinct
branches/heads are intentional; do not reset or remove them as clutter.
Tracking's eight local doc changes remain in its own checkout, not copied
or silently merged into the primary branch. Its historical main-based notes
must be interpreted using its latest dated sections.

Validation with bytecode generation disabled: primary 130 tests and tracking
checkout 54 tests pass separately; both artifact/byte-dump scanners and diff
checks pass in both checkouts. All eleven untracked primary files also pass
direct artifact/encoded-data scans. Transfer/status local links resolve after
the two link repairs. No generated caches returned. This cleanup does not
represent an integrated tracking/XPan test or hardware acceptance.
Single next Claude step remains the bounded standalone-EG contract review,
after checking permissions. Research remains paused until that pickup.
