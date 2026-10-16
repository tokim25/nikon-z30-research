# Selecting a populated input-map bank

Date: 2026-10-16. Read-only static analysis of verified C1.20.

Query `0x103a3cb0` selects bank 1 with a byte store at `0x103a3cdc` into
`0xc18c9a64`. That selects initialized bank `0xc18c9afc` for the queued
input lookup. Zero-based row 11, at `0xc18c9b54`, associates logical ID 41
with mask `0x2000`; its initialized-data origin is `0x1204b7e8`. The root
also checked that this ID has no earlier duplicate in the 16-row bank.

The query emits each row's first two bytes as tag/ID pairs through property
code `0x2082` at `0x103a3d06`. This supplies a concrete selection path for
a populated bank, rather than assuming the initially empty bank 0 is the
only available mapping.

Confidence is high for these bounded code/data links. Actual query execution,
incoming transport, the ID's physical meaning and tracking remain unverified.
The matching mask is insufficient to identify AE-L/AF-L: the named hardware
SW0 table and this logical input bank are not proven to share a namespace.

Private repro, confirmed WORK and fresh directory:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex-agent-input-bank-verify-private.py" \
  --output "$WORK/private-inputs/codex-input-bank-reproduce-01"
```

Agent run: `codex-agent-input-bank-verify-01`; independent root repeat:
`codex-root-input-bank-20261016-01`. Original identity and selected instructions,
copy mapping and row values are checked; detailed evidence stays outside Git.
No firmware execution, modification or hardware was used.

Next: identify the sender/meaning of incoming event IDs before calling
logical ID 41 a physical button.

Written by Codex in collaboration with Tony Kim; selected mapping independently checked by Codex agents.
