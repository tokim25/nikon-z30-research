# Existing XPan overlay: static contract review

2026-10-17. F-144. Read-only review of the existing private F-101 overlay,
its later private revision and the hash-verified original EG. No overlay,
firmware image or package was built or changed; no firmware was executed.

The review does **not pass build-gate condition 3**. Both existing revisions
retain a changed stack contract at the screen-state wrapper's stock-service
call. Passing assisted simulator observations do not resolve that defect.

## Scope and identity

The private audit reads `codex-xpan-guarded-hook-overlay-01` and
`codex-guarded-hook-fixed-01` under the confirmed private WORK inputs. Each
contains eleven entries. It records each entry's hash separately: their
manifest files are identical, but three code entries differ. Manifest identity
alone therefore cannot identify the actual executable overlay.

Original EG identity is checked before review and reread afterward. The audit
checks original hook instructions, complete Thumb decoding of the existing
overlay code sections, twenty direct branches and five literal loads per
revision. It reads existing files only; no builder is imported or invoked.

## Checked layout and control flow

All eleven spans are nonoverlapping, lie in the verified EG payload before
its component CRC, and map inside F-142's initialized installation target.
The four insertion spans remain zero in the original. The six small routines
fit those spans, with their literal pools outside the decoded code portions.
The adjacent ARM-function boundaries described in
[native-xpan-liveview-hook.md](native-xpan-liveview-hook.md) were checked
again. This does not establish absence of all hidden references, runtime
execution permissions or ownership by an external loader.

The four original hooks each replace one complete four-byte Thumb instruction:
the state tail branch, close callback call, live-ready call and writer return.
The existing replacement branches decode to the intended Thumb instruction
boundaries; no entry into an IT block was found in the checked hook contexts.
Literal loads remain within the existing overlay spans. The stock service at
`0x10199e04` retains its original interworking route: it branches to a Thumb
veneer at `0x10036334`, which switches to ARM before the kernel entry. Decoding
that veneer entirely as ARM would give a false instruction interpretation.

The state hook receives an already adjusted pointer. The stock activation
function adds `0x20` before its tail branch; the comparison constant names
that member of the live-view object, not the object base. These agree. The
live-ready selector store uses the object base plus `0x74`, also consistent
with the guard's selector address. No pointer correction is indicated here.

## Register, stack and return findings

| Path | Original overlay | Later private revision | Review result |
| --- | --- | --- | --- |
| State wrapper before mask call | Saves r0, r1, r4 and LR. | Saves r0-r4 and LR. | Later revision preserves all four argument registers across the added work; original does not. |
| State wrapper before stock service | Saves 16 bytes, restores 12. | Saves 24 bytes, restores 20. | Both leave four bytes on the stack at the stock call. Unresolved contract failure. |
| Close and guard wrappers | Save only LR, four bytes. | Save r4 and LR, eight bytes. | Later revision fixes their relative alignment, given aligned incoming SP. |
| Writer return | Replays the original ten-register return after the guard. | Same. | Matches the original 40-byte saved frame and restores r0-r8 and the caller's return address. |
| Live-ready wrapper | Saves r4/LR and retains the stock setter's r0 across the guard. | Same. | Balanced eight-byte frame; subsequent stock code resets r0/r1 before use. |
| Mask helper | Saves/restores r4 and LR. | Same. | Balanced eight-byte frame; r0-r3 and flags are scratch across the added work. |

The critical state call is at `0x1002d822`. The original activation tail
transfers to the stock service without changing SP. Both overlays instead
retain a saved LR word, call that service, then remove the word on return.
Balanced SP at the wrapper's final return does not preserve the contract
*at the intervening service entry*.

For an incoming SP divisible by eight, the service now receives SP modulo
eight equal to four. Independently of alignment, its incoming stack position
has moved. The ARM kernel veneer explicitly captures its entry stack pointer
in r4 before the SVC. A saved LR now precedes any caller stack arguments.
The precise service argument contract and whether it consumes stack arguments
were not established; this is not evidence of an observed hardware crash.
It is enough to withhold calling-contract approval. The later revision's
extra argument-register saves do not fix the residual stack word.

Condition flags are changed by the new helpers and are not restored. The
checked surrounding stock instructions do not establish a flag-preservation
requirement across these function calls. Whole-program dependence, interrupt
context, locking and reentrancy were not proved. No broad transparency claim
is made for either revision.

## Reproduction and next build decision

The newly written private helper contains the checks and emits metadata only:

```sh
"$WORK/analysis-env/bin/python" -B "$WORK/codex-xpan-contract-audit-private.py"
```

The structural checks passed on both existing inputs. The result explicitly
reports the residual state-call contract failure; successful execution of
the audit is not overlay acceptance. Original input remained unchanged.

Single next step: define and test a corrected state-wrapper contract using
synthetic instructions and invented addresses, including original argument
registers, caller stack arguments, service-entry SP/alignment and return
behavior. Require the contract before any private simulator rebuild. No
corrected overlay or feature package is produced by this review.

The missing native digest input, natural lifecycle coverage and actual saved
RAW/JPEG crop remain separate open gates. Hardware remains NO-GO.
