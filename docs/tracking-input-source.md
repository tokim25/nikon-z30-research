# A structured-control path into the input cache

Date: 2026-10-15. Read-only static analysis of verified firmware C1.20.

The reviewed path can produce bit 13 without directly reading a hardware
switch. It receives a structured record, chooses a mask from a selector,
updates a staging word and passes that word to an input-cache setter.
This establishes one producer path, not the physical identity of its input.

| Landmark | Observed bounded behavior |
| --- | --- |
| `0x1008ad26` | Reads selector at record `+0x04`; an unsigned check admits values below 6 to the branch table at `0x1008ad2c`. |
| `0x1008ad4a` | Selector 5 chooses mask `0x2000`. |
| `0x1008ad50` onward | Reads state at record `+0x08`. State 1 sets the mask in staging word `0xc1811e74`; state 0 clears it. Other values skip that staging update. |
| `0x1008ad6e` | Transfers to setter `0x101e383a` with the staging-word address, including when the state skipped the update. |
| `0x101e383a` | Reads its pointed-to input word and stores it at cache `0xc181182c + 0x30`, at `0x101e3840`; then continues pending-state handling. |
| `0x101e3858` | A separate setter copies its pointed-to word to the same cache's `+0x38`, at `0x101e385e`. |

Confidence is high for these observed code and data links. Upstream
reachability, the record sender, transport, selector meaning and physical
SW0 relationship remain unverified. State values 1 and 0 resemble on/off
control, but calling them physical press and release would be inference.
Neither path has been shown to activate tracking or even to run during the
simulator's normal refresh.

The staging address needs care: the literal is `0xc1811e70`, then the code
adds 4 before accessing and passing the word. The accessed word is therefore
`0xc1811e74`. Also, an unrecognized state does not imply no cache side
effects: the setter still runs. Independent review caught both errors in
the draft analysis before publication.

## Reproduce privately

With confirmed WORK and a fresh output folder:

```sh
"$WORK/analysis-env/bin/python" \
  "$WORK/codex-input-field-source-verify-private.py" \
  --output "$WORK/private-inputs/codex-input-field-source-review-04"
```

The private helper checks the original module hash and selected instruction,
literal and branch-table relationships. Independent inspection in
`codex-agent-field-source-review-01` checked surrounding branches and
register flow. These are bounded static checks, not a complete proof of
execution. Private outputs and all firmware content stay outside Git.

No firmware changes, simulator calls or hardware access were used. None of
these addresses is an approved call or patch interface. Next: identify the
sender and meaning of the structured records before assigning a button name.

Written by Codex in collaboration with Tony Kim; independently checked by Codex subagents.
