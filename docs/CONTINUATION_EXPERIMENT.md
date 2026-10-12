# Continued outcome learning after correction

The [frozen protocol](../experiments/CONTINUATION_PROTOCOL.md) and
[results](../experiments/CONTINUATION_RESULTS.md) test whether corrected judgments remain
revisable after actual restart. Three small sequences compare restarted/uninterrupted LMFT,
ordinary memory and a control retaining correction while blocking subsequent outcomes.

The existing [outcome mechanism](OUTCOME_CORRECTION.md) already admits unused registered events,
recomputes from one effective version per root, invalidates caches and updates questions.
No new fixture, numerical equation, correction authorization rule or predictive architecture
was needed. Experiment inputs reuse unused records from the same procedure/batch/branch.
Registered log membership is not an independent truth guarantee.

The only production addition is `--freeze-outcomes-after-correction`, valid for outcome modes.
It pins a Boolean in the birth manifest. Once a correction is accepted, new eligible outcome
admissions reject; initial learning and correction acceptance still work. Existing identity
checks run first. Exact delivery duplicates remain duplicates; reattributed unlearned outcomes
remain blocked. This flag cannot be changed on restart or by an inbox instruction. It differs
from `outcome-disabled`, which disables correction acceptance, and does not repurpose the
existing generic learning flag. Defaults and historical migration behavior are unchanged.

Run from the repository root in PowerShell:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_continuation.py --output outputs/my-continuation
```

Use a fresh path; the harness refuses overwrites. It uses actual runtime processes and zero
model calls, archives source/config/protocol, and retains original inbox messages, complete
halted state, result checks and failures. During runtime only deliberate outbox messages and
lifecycle acknowledgments are exposed. Full inspection is after halt:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-continuation/restarted/same-category/individual probe
```

For manual frozen-control runs, use the flag on both initial start and every restart with
`--experiment outcome-lmft --mode fixture`. Existing historical individuals still require
their archived source/config due to the existing manifest guard; no checkpoints are migrated.
Raw experiments remain under ignored outputs/ and need a durable external copy if required.

The experiment establishes mechanical continued revision and uncertainty, not prediction
improvement. The report proposes a separate bounded predictive-feature comparison against
competent ordinary memory; that follow-up is not implemented here.
