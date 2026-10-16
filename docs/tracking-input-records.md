# Input records: two ring writers

Date: 2026-10-15. Read-only static analysis of the verified C1.20 EG module.
No simulator input calls or firmware edits were made for this finding.

## Result

F-021's claim that only one routine writes the ring is incorrect. At least
two routines write records into the store at `0xc2008ea0`, using the index
state at `0xc182004c`. Their input sizes differ. This matters because treating
every ring entry as a 60-byte event would hide another input path.

| Routine | Observed static behavior |
| --- | --- |
| `0x102f0a36` | Copies 60 bytes into a cleared 400-byte slot and forces the leading kind word to 1 at `0x102f0c02`. |
| `0x102f1844` | Clears a 400-byte slot and copies 396 bytes from its input at `0x102f1946`. A conditional path advances the index modulo 16. |
| `0x102f1412` | Mode 0 selects the ring with a 400-byte stride. Mode 1 selects the separate record at `0xc200a7a0`. |

These are observed code and data links, with high confidence. They do not
show that either path ran in the simulator or that a record came from a
physical button. This report corrects the exclusive-writer and universal
record-size claims; it does not reassess every other claim in F-021.

## Links to input decoding

The paired-record builder `0x102f199a` calls the larger writer at
`0x102f1a4a` and `0x102f1aa0`, after calls to `0x102f0d14`. Its field helper
`0x101dd502` stores two masks and their changed, first-only and second-only
bits. Interpreting this as logical transition construction is inference.
Press and release meaning remains unverified.

A separate static chain agrees with the earlier menu-OK candidate:
getter `0x101dd616` reads record field `+0x18`; decoder `0x102f0e38` uses
that field in its loop at `0x102f101a`. Table row `0x1073be50` associates
mask 1 with candidate `0x1b`. Menu translator `0x1045933e` maps `0x1b` to
event `0x27e` through row 32 of table `0x1073b400`.

Candidate creation is insufficient to prove input delivery. Later decoder
branches can clear all three output words, including the path at
`0x102f1404` to `0x102f140c`. No physical OK bit, AE-L/AF-L mapping or
tracking entry point is established by this chain.

The live-view callback also has a call to the larger writer at
`0x102f2fd0`, followed conditionally by a flag-2 signal at `0x102f2fdc`.
The preceding gates, task context and successful runtime delivery remain
unresolved. None of these addresses is an approved call interface.

## Reproduce privately

Use the WORK path confirmed by the owner. The helper is private because it
reads the original module and saves detailed decode output. It checks the
module hash, pinned simulator revision and clean simulator checkout, then
asserts the selected instruction and table relationships. Use a fresh output
folder each time:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex_input_record_verify_private.py" \
  --output "$WORK/private-inputs/codex-input-record-review-02"
```

The successful session output is `codex-input-record-resume-01`. An
independent reviewer decoded the writer and reader paths again in
`codex-agent-producer-resume-01`. All detailed output stays outside Git.
The private helper's earlier range ended halfway through an instruction;
that analysis-tool error was corrected before its assertions passed.

Repository checks pass: 54 unit tests, the tracked-artifact check and the
encoded-data check. Those checks validate the repository, not camera behavior.

## Next step

Trace the named AE-L/AF-L switch's bit-13 reader and its event destination.
Keep the switch-name table separate from the logical record masks until an
actual code path connects them.

Written by Codex in collaboration with Tony Kim; independently checked by a Codex subagent.
