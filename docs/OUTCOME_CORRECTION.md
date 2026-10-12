# Outcome correction experiment

The opt-in `outcome-lmft`, `outcome-disabled`, and `outcome-memory` modes extend the
existing correction transaction to synthetic outcome reports. See the frozen
[protocol](../experiments/OUTCOME_CORRECTION_PROTOCOL.md) and
[results](../experiments/OUTCOME_CORRECTION_RESULTS.md).

## Policy and implementation

`outcome-instrument-log-1` admits exact registered instrument reports, which can be
wrong. Admission authenticates fixture-log membership, not objective truth. These
reports are provisionally scored; ordinary teacher assertions are not eligible.
`registered-outcome-reference-1` independently verifies a proposed correction for
the same event. This is a separately authored synthetic reference, not a real sensor
or a model judgment. Historical truth-based verifiers are unchanged.

`config/outcome_correction_authority.json` supplies the existing exact-payload hash
and named-authority permits. Runtime pins this policy in the birth manifest. A
matching sender and full operation permit are required, followed separately by
eligibility and content verification. These public fixture permits are replayable
capabilities under the existing cooperative single-host assumptions; sender names
are not cryptographic authentication. Authorization does not establish truth.

Eligible targets are active outcome heads with the exact expected digest. The
replacement must preserve event ID, kind, scope, branch, procedure and payload;
only outcome output and version/provenance may change. Boolean values do not pass
integer outcome validation. Replacement IDs are `replacement/<correction_id>`.
First correction-ID disposition is terminal, including rejection; conflicting reuse
and stale targets reject. A chain must name its current head and digest explicitly.

`correction.correct` remains the sole authorization/identity/lineage transaction.
Its optional trusted-code hooks supply outcome eligibility, verification, before/after
snapshots and recomputation. They are not fields selectable by an inbox message.
The default historical scoped-observation behavior is unchanged.

The original and every accepted ancestor remain in the ledger. Each independent root
has one active head. `outcome_correction` projects all eligible heads per branch through
unchanged `judgment.apply_validated`; the baseline independently recounts the same
signs. Score remains `sum(signs)/(count+2)` with thresholds +0.2 and -0.2. Stored
replacement count is distinct from independent outcome count. Derived replay revisions
are a projection, not extra learning events. Correction audits retain before/after
scores, counts, supporting/contradicting root and head references, and reasons.

The fixed routes remain A=.25, B=.75, D=.5 and are unused here. No activation propagation,
inference, teacher bridge or autonomous loop participates. Scores are not calibrated
confidence probabilities. Memory shares ledger/authorization infrastructure, while
using a simpler arithmetic projection; this comparison does not isolate those shared
infrastructure costs.

## Caches, questions and persistence

Probe caches depend on the case and effective branch records. Relevant new heads
invalidate them, even when the sign stays the same; unrelated branch caches survive.
Outgoing wording is generated from current semantic results. The read-only `predict`
function does not register cases or alter state; inbox `evaluate` deliberately records
communication and may ask a question.

The new fixture's preregistered `outcome_consistency` question is resolved only by
nonempty effective evidence with one sign. Mixed signs remain unresolved even with
a categorical judgment. This is a bounded experimental convention, not a modification
to historical question criteria. Each case has one request budget. Corrections can
close or reopen an existing question without refunding it. No unanswered request is
silently converted into verification.

The existing atomic checkpoint commits replacement, active head, projection, cache,
questions and acknowledgment together. During execution use only inbox submission,
outbox reception and lifecycle acknowledgments. Full inspection/probing is available
only after halt. Historical individuals are not migrated: the existing source/config
manifest guard still requires their original archived code. Use fresh individuals for
these modes. Seed IDs, migration policy, teacher profiles and models are unchanged.

## Reproduce

Run from the repository root in PowerShell, with the existing virtual environment:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_outcome_correction.py --output outputs/my-outcome-correction
```

The harness refuses an existing output directory. It freezes source/config/protocol
snapshots, uses zero model calls, and preserves original messages, complete halted
checkpoints, result checks and any evaluated failure. It runs 36 primary individuals
and six uninterrupted controls. No Hugging Face access or model installation is needed.

To inspect a completed individual (after the harness has halted it):

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-outcome-correction/outcome-lmft/o12/individual probe
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-outcome-correction/outcome-lmft/o12/individual inspect
```

Raw runs remain under ignored `outputs/`, following existing archive conventions;
copy the complete halted directory to durable backup if retaining it outside this
workspace. The protocol, implementation, tests and human-readable report are repository
artifacts. No power-loss, hostile-host, distributed-delivery or cloud-sync guarantee
is inferred from the atomic fault tests.

The subsequent [continuation experiment](CONTINUATION_EXPERIMENT.md) reuses this mechanism for new independent events after correction and restart. An opt-in pinned control freezes only subsequent outcome learning; historical defaults and this study remain unchanged.
