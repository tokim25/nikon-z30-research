# Remaining work across the research lanes

Reviewed 2026-10-17 at the owner's request, against main through F-120
and Lane 0's F-127 observations. This is a gap review, not a claim that
the other lanes' experiments were rerun. Hardware remains NO-GO.

| Lane | What the evidence supports | Work still needed | Concrete next result |
| --- | --- | --- | --- |
| 0: natural trigger delivery | APPLV is created and its worker runs passively; a general scheduler stall is not supported. The sampled worker flags were 4, without the live-view-enter bit. | Identify the missing event/precondition. The actual property-event producer task is still unidentified. | Trace the live-view signal/wait boundary in the running task and establish a real producer for bit 16; stop if the result only explains unrelated simulator fidelity. |
| 1: live-view bars | F-101's private hooks pass diagnostic area controls and ten signal cycles. F-115 fixes two audit findings and reaches the guard/mask during a direct close-handler call. | Natural startup/menu return with the worker active; actual mask flip from off to on on the admitted close path; immediate area change through the i menu; playback/movie rejection; focus graphics/readouts inside the strip; reboot persistence and cleanup. The shared activation helper may clear bars for legitimate overlays. | Exercise the guarded lifecycle from a real firmware event in the running APPLV context, with an initially off mask and controls for DX/16:9 and non-live-view closes. Follow with the remaining design checklist. |
| 2: saved RAW/JPEG crop | F-113/F-114 resolve the crop descriptor; F-118 confirms its geometry math at runtime; F-119 reads the ROM-backed size table via its initialized RAM pointers. | A verified capture/save consumer, native serialization/storage boundary, RAW metadata dimensions, JPEG dimensions and actual cropped content. Finish table-index mapping and identify other square assumptions where they affect a real save. | Identify a real save-path boundary independent of the retired record-builder chain, then connect the crop descriptor and file dimensions to it. A display formatter or shots-remaining estimate is insufficient. |
| 3: AE-L/AF-L tracking | Queued-bank mapping and a non-Bluetooth event cluster exist. F-116/F-117 found no verified property-2021 consumer. | Physical press/release identity, producer/consumer connection, native tracking activation, reticle, cancellation and unsupported-state behavior. | Let the independent codex/tracking-property-dispatch work establish its consumer result; this branch neither changes it nor assumes it depends on Lane 0. |
| Integration and readiness | Personal, non-distributed build work is authorized; hardware access is separately gated. | Exact-original patch policy and only-planned-edits proof; integrity/authentication coverage; final instruction-mode/ABI/layout review; offline original backup; verified recovery or explicit service/total-loss risk acceptance; combined feature checks. | Record a reviewable exact build and test scope, close the measurable gate checks, then obtain the owner's separate hardware decision. |

The highest-impact unresolved feature gap for the owner's first planned test
remains **saved RAW and JPEG cropping**, because that test combines bars and
saved crop. A scheduler result cannot substitute for saved-file evidence.
Tracking remains a separate second test; combined operation follows both.

The menu/data scope also remains incomplete: replace the existing 1:1 slot
rather than add a choice; use the final stored choice byte's actual mapping;
verify the label and size text, all three output sizes, retained selection,
and unchanged DX/16:9 behavior. F-080's successful builder experiment is not
proof that image processing or either saved file accepts those dimensions.

## Evidence hygiene and stale status

Several summary documents predate later facts. Read their historical claims
alongside the current handoff, rather than restarting completed searches:

- `roadmap.md` still describes bars covering menus and tracking as unstaffed;
  F-101/F-115 and the independent tracking branch supersede those summaries.
- `user-stories.md` still calls menu construction unresearched in its early
  status, despite its later replace-not-add decision and F-072 through F-101.
- `xpan-replace-1to1-plan.md` retains the older callback value 4 and the
  superseded F-081 through F-087 state chain. The final stored byte is 1
  for 1:1; use F-093/F-101 and the current bars design.
- The old Lane 3 handoff says its two options were untried. F-116/F-117
  already tried them, with the limits recorded in `tracking-input-chain.md`.
- F-120 confirms ARM code exists. Recheck instruction mode at real boundaries;
  it does not justify redoing every exhausted caller search without a lead.

The shared original checkout was on `codex/firmware-preflight-plan` with
uncommitted preflight work, rather than clean main. It was preserved. This
review does not validate or publish that work, and those local fact numbers
are not merged evidence. F-127 avoids its local F-121 through F-126 numbers.

## Owner decisions

No machine-model source change was needed, so there is no C-source commit
decision in this PR. The owner still decides any explicit deviation from
the natural-lifecycle requirement, and later whether to accept the concrete
recovery and residual risks for an exact experimental build. Neither decision
has been inferred here. Conditions 2 through 4 remain untouched by Lane 0.

Sources: [worker evidence](native-worker-scheduling.md),
[bars design](xpan-bars-design.md),
[hook audit](native-xpan-liveview-hook-audit.md),
[tracking evidence](tracking-input-chain.md),
[facts](facts.md), [readiness](hardware-readiness.md), and
[build gate](build-phase-gate.md).

Written by Codex in collaboration with Tony Kim.
