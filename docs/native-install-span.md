# Native main-firmware erase/program span

2026-10-17. F-142. Bounded static trace of original code, never invoked.
No firmware modification, updater execution or hardware access.

## Build decision

The relocated updater contains identifiable erase and programming paths,
status polling and readback comparisons. For the initialized region policy
in the verified original, the main update processes 43,253,760 bytes, not
only the 33,939,512-byte EG payload excluding its two CRC bytes.

The remaining 9,314,248 bytes are filled with `0xFF` before the worker runs.
A concrete patch preflight therefore needs to model that full installation
span and padding as well as the bytes contained in the package.

These are static properties of the checked original and initialized tables.
Actual device geometry, runtime policy changes, physical flash behavior and
recovery are not validated by this trace.

## Worker handoff

The main path prepares the source buffer in `0x101ce89e`. Its call through
the relocated setup entry configures source/state. `0x1011a028`, previously
only called a handoff helper, adjusts a memory-mapping path; it is not the
erase/program worker entry.

The next ARM trampoline `0x1017e378` returns callback `0xc2b10c8b`.
The caller passes that callback to `0x101a27f4`, which stores it in a worker
state field and signals an event. The consumer at `0x101a2594` loads that
same field and calls it at `0x101a2598` when the corresponding event bit is
set. This traces the callback linkage; the task was not executed here.

The callback's Thumb entry at `0xc2b10c8a` runs the erase stage
`0xc2b10d46`, then programming stage `0xc2b10bb0`. It contains a bounded
retry loop and reports the result through its configured callback.

## Erase/program boundaries

The erase stage reaches `0xc2b106e8` via the block-range helper chain.
That primitive issues memory-mapped flash commands, polls completion/error
status and returns an error or success result. No command sequence is
reproduced here and none was sent to a device.

The programming stage reaches `0xc2b10328`, which selects buffered and
halfword programming paths at `0xc2b101e8` and `0xc2b10280`. Those paths
perform actual destination halfword stores, poll device state and compare
readback with source data. The outer worker also performs word-by-word
source/destination comparisons after each programmed chunk.

The high-level loop uses 128 KiB chunks. It erases the leading chunk first,
then the remaining chunks. It programs the later chunks first and the
leading chunk last. Programming the leading chunk last does not make this
an atomic update: it has already been erased if later programming fails.
Retries and readback checks are not proof of power-loss recovery.

## Initialized installation policy

Initializer mapping from F-141 gives the logical-region table at
`0xc1880d2c` and physical-region table at `0xc188087c`. Logical id 2 selects
physical record 2. Native getter `0x101f4eba`, through `0x10212238`, carries
its destination and size into updater state. The initialized alternate
address is zero, so that record describes one target rather than a demonstrated
second bank. Runtime configuration mutation was not exhaustively audited.

| Field | Value from verified initializer / static arithmetic |
| --- | --- |
| Main target start | `0x10020000` |
| Target end, exclusive | `0x12960000` |
| Region capacity | 43,253,760 bytes (`0x02940000`) |
| EG payload excluding component CRC | 33,939,512 bytes |
| Payload end in target mapping | `0x1207e038` |
| Tail fill | 9,314,248 bytes of `0xFF` |
| High-level chunks | 330 chunks of 131,072 bytes |

Preparation helper `0x1021b290` fills the tail from actual payload length
to configured capacity. The worker loop limit comes from that capacity.
The initial allocation request is larger than the region, but this pass did
not prove every allocator/alignment/source-pointer lifetime contract.

For this initialized EG target, the first 128 KiB at flash base `0x10000000`
lies before the region. This does not prove that area is a usable independent
recovery loader, reveal the missing digest bytes there, or establish what
other component updaters may write.

## Reproduction and next step

The newly written private helper verifies selected instructions across the
callback chain, erase/program/readback paths, logical/physical initialized
records, source length and span arithmetic. It reruns the earlier identity,
decode/CRC and unchanged baselines through the private helper chain. It emits
metadata only and does not execute any native updater function.

```sh
PYTHONPATH=src "$WORK/analysis-env/bin/python" -B "$WORK/codex-install-span-audit-private.py"
```

The private verifier passed. No firmware image, native-code dump or extracted
table was written. Original inputs and recovered tools remain unchanged.

F-143 implements the read-only model and integrates it into preflight;
see [native-installation-model.md](native-installation-model.md).
It checks payload/CRC exclusion, padding, chunks and bounds against supplied
independent policy and reports static scope. The extra native digest remains unreproduced because
its eight-byte boot-region source is missing. Hardware remains NO-GO.
