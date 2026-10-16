# A bank-mapped queued route into the input cache

Date: 2026-10-16. Bounded static analysis of verified C1.20.

The independent caller at `0x103a400c` publishes staging word `0xc18c9a68`
through setter `0x101e383a`. Unlike the earlier numeric-command route, its
consumer `0x103a3f9e` obtains a queued record and maps its ID byte (`+0x11`)
to a mask. Operation byte `+0x10` selects set or clear behavior.

The table formula is `0xc18c9a7c + 128 * BYTE(0xc18c9a64) + 8 * row`,
with at most 16 rows. Each row has ID byte `+1` and mask word `+4`.
Operations 0–2 OR the mask; 3–4 clear it. The queued route calls the setter
when staging changes. Separate caller `0x103a3e88` publishes a reset when
the staging word was nonzero.

Handler `0x103a3d14` processes code `0x2083`, builds the ID/operation fields,
queues the record and invokes the consumer path. The reviewed upstream chain
includes `0x10379f00` and `0x10379a68`. Incoming transport, physical SW0
identity, press/release meaning and tracking activation remain unverified.
The same numeric code in an unrelated UI path is not a proven sender.

The bank selector is a byte, not a word. An earlier provisional interpretation
as a relative pointer was wrong: exact subtraction and shift checks establish
the banked formula above. Initial bank 0 is empty; that does not exclude a
later selection of another initialized bank. Confidence is high for these
bounded code/data links, not runtime delivery.

Private repro, confirmed WORK and fresh directory:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex-agent-queued-input-verify-private.py" \
  --output "$WORK/private-inputs/codex-queued-route-reproduce-01"
```

Corrected agent verification: `codex-agent-queued-input-verify-03`;
root repeat: `codex-root-queued-input-20261016-01`. The helper checks original
identity and selected instructions, table branches and copy mapping. Detailed
evidence stays private. No firmware execution or hardware was used.

Next: trace the incoming producer of the property-event record and establish
the meaning of its ID before assigning it a physical button name.

Written by Codex in collaboration with Tony Kim; selected checks independently repeated by Codex agents.
