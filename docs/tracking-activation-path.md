# Tracking activation path: AE-L/AF-L to subject tracking (static, partial)

Date: 2026-10-17. Read-only static analysis of verified firmware C1.20.
SHA-256 of the scratch module was checked before decoding and matched the
value already recorded in [tracking-input-chain.md](tracking-input-chain.md).
Addresses and descriptions only; no firmware bytes, dumps or patches are
recorded here. Private helpers and their output stay outside Git.

Inputs read: [tracking-input-chain.md](tracking-input-chain.md) (main). The
two Lane 3 documents named in the task, `lane3-family-search.md` and
`lane3-stack-placement-check.md`, are not on main. They exist on branch
`claude/lane3-family-search-2ded1d` (commits `b23a7ff` and `dfad2ef`), so this
pass used them from that branch.

## Verdict

**Path NOT traced end to end.** The press-to-tracking chain is not closed.
The posting side of property `0x2021` is traced. The receiver side is not:
no function was shown to consume `0x2021` and start tracking.

## Traced so far

| Address | Observed behavior (static decode) |
| --- | --- |
| `0x10475d8c` | Allow-list. Returns 1 for ids `0x2000`..`0x2009`, `0x200a`, and `0x2020`, `0x2021`, `0x2083`, `0x2087` (offset tests). |
| `0x10475ecc` | Shared post primitive. Calls the allow-list first. On success it may check a gate (`0x104a22ac`, reads a global flag). It then allocates a 0x2c-byte record, stores the id at record +0x24 and the payload pointer at +0x28, and either enqueues it (`0x104a1d00`) or builds a stack record and calls `0x104a223e`. |
| `0x104a1d00` | Enqueue. Passes the record to a message-send helper (`0x1021157c`) on a fixed global object. |
| `0x104a223e` | Ring insert into a 32-slot array. Index is a halfword global, wrapped with `and 0x1f`. Calls `0x10199e0a` and `0x1021157c`. |
| `0x104a1d4e` | Receiver dispatcher. Indexes a table by a key in `r0` (`ldr r4,[r1,r0,lsl #2]`). Calls a per-receiver callback at object +0x50 and a second callback at +0x60. |
| `0x103a341a` | Handler for event `0x2021` (from dispatcher `0x1037aae2`). Posts `0x2021` through `0x10475ecc`. A poster, not a reader. |

Earlier-note context (not re-verified here): `0x2021` is written from at least
three sites and never compared as a literal. The family-search note
(branch `claude/lane3-family-search-2ded1d`) found the consumer is not reached
by a literal compare. Its single next step is the receiver table behind
`0x10475ecc`. That is the step this pass started.

## Open link

Not yet established:

1. Which key `0x104a1d4e` receives for id `0x2021`. The key is `r0`. Its
   callers and the table it indexes are not yet mapped.
2. Whether the receiver whose callback runs for `0x2021` ever starts tracking.
   The callback targets are not yet named.
3. Whether event `0x2021` is the AE-L/AF-L press. Not shown. The event
   `0x2021` is posted by sub-codes of `0x103a341a` and is not tied to a
   physical switch.

The tracking path that is known separately is the queued route via event
`0x2083` (handler `0x103a3d14`, logical input id 41, mask `0x2000`). Its
connection to `0x2021` and to a button is not shown.

## OK-button tracking entry point

**Not established.** The closest documented OK chain is the menu candidate in
[tracking-input-chain.md](tracking-input-chain.md) (record field +0x18 with
candidate `0x1b`, translated to event `0x27e` by `0x1045933e`) and the key
dispatcher `0x103ce96e`, which receives the OK key in the simulator. Neither
is shown to reach a tracking entry. No OK-button tracking routine was found.

## Simulator checks

Installed: QEMU 10.2.4 at the pinned revision `0ba0c3547ccbec09e7c861eaca35db8e82795f15`,
clean checkout, binary present. **No simulator run was made in this pass.**
The earlier breakpoint test on `0x10475ecc` (F-117) never saw a post during
menu and key navigation, so a probe needs a way to trigger the input first.
That is a separate step, and it should follow the static link above.

## Single next step

Find the callers of the receiver dispatcher `0x104a1d4e`, and the key it
receives for id `0x2021` and for `0x2083`. Then name the callback at +0x50 for
that key. This names the receiver to hook. Do not add simulator probes first.

## Limits

- Static Thumb decode only. Literal-pool and register-passed table keys are
  not fully resolved. A callback reached through a stored pointer is not
  covered.
- Table base and receiver registration were not decoded. A "receiver" here is
  an inference from the dispatch shape, not a verified object.
- No hardware, no camera, no flashing. No firmware changes.

Written by Claude (Haiku 5.5) in collaboration with Tony Kim.

## Simulator reachability of the AE-L/AF-L press (first result)

**The simulator cannot deliver an AE-L/AF-L press.** Read-only check of
the pinned simulator's input path (`tools/gui.py`): the only keys sent are
up, down, left, right, OK and back, mapped to event codes `0x253`, `0x254`,
`0x257`, `0x258`, `0x27e` and `0x255`. The browser and keyboard handlers
accept only those. No AE-L/AF-L, shutter, i-menu or info key exists in the
map, matching the recorded key-set limit (facts F-097 note).

A raw diagnostic injection into the key dispatcher `0x103ce96e` is possible
in principle, but it would post a synthetic event code, not a press. No code
for AE-L/AF-L is established, so that would not be a test of the button.
No simulator run was made.

### On-camera test item (not simulator-verifiable)

- Press and hold AE-L/AF-L on a real Z30 running stock C 1.20 with a
  subject in view. Record whether the reticle tracks the subject, the
  release behavior, and whether a second press cancels. Requires the real
  camera. Not run here; no camera contact was made.
