# Scoped evidence and bounded investigation

The [protocol](../experiments/SCOPED_ATTENTION_PROTOCOL.md) freezes a seven-case study
of whether verified partial information suppresses redundant verification while leaving
unresolved questions eligible. The [results](../experiments/SCOPED_ATTENTION_RESULTS.md)
include matched ordinary-memory performance and a separate **negative cross-part conflict
audit**. This is an experimental fixture; the current mapping is not generally reliable.

## Reproduce from PowerShell

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_scoped_attention.py --output outputs/my-scoped-run
.\.venv\Scripts\python.exe experiments/audit_scoped_cross_part.py --output outputs/my-cross-part-audit.json
```

Use fresh output paths. No downloads, credentials, model installation or new dependencies
are needed; all comparisons make zero inference calls. The main harness runs 35 independent
primary individuals, five restarted sequential individuals and one uninterrupted reference.
The separate audit is a pure-function counterexample, excluded from primary metrics.

Optional runtime modes: `scoped-full`, `scoped-no-fact`, `scoped-no-confidence`,
`scoped-neither`, `scoped-memory`, all with `--mode fixture`. Use the normal
[supervised runtime commands](INTERACTIVE_RUNTIME.md) for start/submit/receive/stop.
Restart with the same experiment/mode, omitting --new. Inspect or probe only after halt.
The post-halt probe shows fixed imported route weights. Detailed scoped evidence and
selection traces are available through halted inspection. No background work occurs.

## Evidence, selection and trace boundaries

`scoped_attention.py` stores a separate scoped ledger, accepted-evidence audit entries,
cases, questions and selection traces. `scoped_fixture.py` contains registered initial
observations, selected-question verification and evaluator-only outcomes. Selection and
prediction read only supplied reports and accepted ledger entries; the harness obtains
verification only after receiving a concrete deliberate request.

New modes use the existing version-1 envelope with exact `text`, `operation`, `record`.
Operations: `outcome` for the unchanged eight prior judgments; `evidence` for registered
scoped observations; `evaluate` for public cases; linked `verification` for the selected
question; and `barrier` for a completion acknowledgment. The harness supplies exact JSON
examples. Message/evidence identity remain separate. Original records and their source
attribution survive restart. A source label alone never makes an arbitrary assertion
eligible; it must match the complete registered synthetic record, including types.

Resolution requires explicit matching case/scope/question/part evidence, complete required
parts and unanimous values. All conflicting observations remain available. Prediction has
an explicit ordinary eligibility gate: both questions resolved and payload valid before
using the existing conditional score. This gate is shared by every condition and is not
a seed capability. There is no equivalent external resolved gate in conceptual selection:
that uses positive final Clarity with the unchanged propagation equation and ID tie-break.
The competent memory baseline explicitly selects only unresolved questions.

Fact encodes nonconflicting part coverage; direct Confidence encodes full sufficiency.
These are authored temporary leaf activations, not modified founding names or numerical
confidence fields, nor calibrated probability. The exact additional sidecar edge and
outgoing-only ablations are specified in the protocol. Route weights stay fixed; disabling
learning changes nothing in this study. No automatic constitutional changes are possible.

## Compatibility and known limitation

Existing attention and other modes are unchanged. Only new scoped individuals use this
separate developmental layout. Source-manifest compatibility still rejects older runtime
checkpoints under changed software: use their original archived sources. No implicit
migration, seed modification, new equations or new judgment rule was introduced.

Within-part contradiction is handled in the registered cases, but cross-part disagreement
can yield Fact=1 despite unresolved support, causing improper suppression in the full
pathway. Ordinary memory avoids this error. The preserved post-hoc audit reproduces it;
no fix was silently tuned into the reported evaluation. Do not use this selector as a
general real-world evidence policy. Raw archives remain in ignored outputs/ and require
separate backup. Complete traced checkpoints impose additional storage cost.
