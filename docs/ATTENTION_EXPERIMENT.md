# Bounded attention and verification experiment

This optional runtime experiment connects authored fuzzy propagation to a concrete
verification choice and learns one bounded class of separate association weights.
Read the [preregistration](../experiments/ATTENTION_PROTOCOL.md) for every mapping,
edge, update, case, budget and acceptance criterion, and the
[results](../experiments/ATTENTION_RESULTS.md) for measured equivalence and limitations.
The canonical seed, existing equations, conditional counter rule and migration are unchanged.

## Reproduce

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_attention.py --output outputs/my-attention-run
```

Choose a fresh output directory; the harness refuses overwrite. No download, token,
network or model installation is required. The harness starts actual separate runtime
processes, communicates through inbox/outbox, halts before inspection, and compares
four conditions plus an uninterrupted run. Exact sources/config/protocol/tests are
snapshotted before execution. Complete raw archives remain ignored by Git.

Manual lifecycle commands for a separate individual:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-attention start --new attention --experiment attention-lmft --mode fixture
# In another terminal, submit a prepared JSON envelope:
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-attention submit --file outputs/attention-message.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-attention receive
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-attention stop
# Wait for halted before these commands:
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-attention probe
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-attention inspect
# Restart without --new, with the same experiment and mode:
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-attention start --experiment attention-lmft --mode fixture
```

Other modes: `attention-frozen`, `attention-disabled`, `attention-memory`. The existing
`--learning-disabled` flag also freezes **association** updates in these modes; the
matched eight prior outcome judgments still initialize from verified evidence. This is
an association-learning control, unlike earlier all-judgment-learning controls.
Use fixture mode: this study performs no model inference even if a local adapter exists.

## Implementation and protocol

`attention.py` owns the separate state, candidate appraisal, selection, conditional
probe and bounded weight update. Selection and prediction do not import/query hidden
truth. `attention_fixture.py` separates public cases from the selected-request verifier
and evaluator-only outcomes. `run_attention.py` retrieves truth only for the concrete
outbox request; outcome accuracy is computed after halt. The ordinary-memory mode uses
explicit relevance then the same learned route statistics and ID tie-break; no propagation.

New modes reuse the existing version-1 envelope, exact `text`, `operation`, `record`
content and linked `teacher_reply` mechanism. Operations are `outcome` (registered prior
training), `case` (public reports/menu), `verification` (selected linked reply), and
`barrier` (empty record, completion acknowledgment). The harness provides exact examples.
Cases cannot be silently replaced or exceed their one-request budget. Repeated evidence
is identified by canonical payload plus evidence ID, independently of delivery ID.
Unverified reports never select a judgment branch. A matching unavailable verification
is still evidence that the route failed to resolve this case; it is not a false fact.

Each candidate uses a temporary birth-based frame and explicit sidecar edges; no new
founding nodes or automatic genealogical links exist. Final Clarity activation is the
priority consumed by LMFT selection. Learned weights are stored by route, with separate
accepted/rejected before/after records and complete verified-reply provenance. Trace
edge metadata identifies the authored template; the update ledger, not template event
labels, identifies the experience that changed a route weight. Seed leaf activations
are distinct from the birth node's numeric salience/confidence fields.

Verification resolution and prediction correctness are separate. Existing validated
counter updates supply +1/3 and -1/3 conditional orientations, unchanged throughout
held-out evaluation. The read-only decision function consumes only accepted condition
information and those counters. No speculation from teacher/model text becomes a fact.

## Compatibility and limits

Existing modes retain their prior behavior. Historical checkpoints are not converted;
the existing source-manifest restart check requires their original archived sources.
Only explicitly new attention individuals use this new separate state layout.
One checkpoint atomically commits selection/questions and later evidence/updates/output.
There is no background cognition, new dependency, autonomous code modification or seed edit.

The owner communication boundary remains [the supervised runtime boundary](INTERACTIVE_RUNTIME.md):
only deliberate messages and lifecycle acknowledgments while running; internal state and
traces only after halt. This is an interface convention, not hostile-host filesystem isolation.
The registered verifier supplies synthetic validation, not external source authentication.
Full traces increase storage considerably without improving results over ordinary memory.
