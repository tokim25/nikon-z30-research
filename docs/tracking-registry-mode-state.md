# Screen registry and mode selector are distinct state

Date: 2026-10-16. Read-only static analysis and assisted simulator observation.

The empty menu/screen stack reported in F-029 does not imply the native
live-view mode object is uninitialized. In the instrumented startup run,
object `0xc1821d44` changed selector `+0x74` from 4 to 1, while the screen
stack remained empty. Stock refresh preserved that combination. The menu
control subsequently selected 1 for menu object `0xc182e688` and populated
two stack entries. These are observed values, not proof of working input.

The separate group registry at `0xc2006594` contained groups 2 and 3 before
the fixture; startup added group 5 at `0xc2017a8c`. Other group slots were
zero at the observed checkpoints. A separate registry-only run agreed.
Static caller `0x10324b60` registers group 5 through `0x104571e8`.

Getter `0x104571fe` accepts group values below 7 and computes registered
base plus 44 times the supplied descriptor ID. It does not guard the ID or
a null registered base on the reviewed path. Do not treat it as a safe
interface for guessed shooting-screen IDs. Registration alone does not put
a descriptor on the active screen stack.

Confidence is high for the bounded code and recorded state, moderate for
generalizing beyond this startup fixture. No shooting-screen key table,
physical event delivery or tracking activation is verified. The separate
type-3 live-view worker remains a relevant path; an empty menu stack alone
does not rule it out.

Private repro, confirmed WORK and fresh directory:

```sh
PYTHONDONTWRITEBYTECODE=1 "$WORK/analysis-env/bin/python" \
  "$WORK/codex_mode_object_20261016_private.py" \
  --output "$WORK/private-inputs/codex-mode-state-reproduce-01" --menu-control
```

Runs: `codex-mode-object-20261016-run-01` and registry-only
`codex-screen-registry-20261016-run-01`. Static selected code is retained in
`codex-screen-group-registration-05` and `codex-screen-group-callers-06`.
Original hash and clean pinned simulator were checked; logs and memory stay
private. The only calls were the established startup, refresh and menu control.

Next: establish the type-3 input contract using the observed selector state;
do not substitute menu key injection into the empty stack.

Written by Codex in collaboration with Tony Kim; extends the prior Codex screen-stack observation.
