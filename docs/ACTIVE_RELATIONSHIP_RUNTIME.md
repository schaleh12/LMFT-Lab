# One-request relationship investigation

New opt-in modes relationship-acquire-lmft and relationship-acquire-memory use the
existing supervised inbox/outbox, questions, receipts, locks and atomic checkpoints.
See [frozen protocol v1.2](../experiments/ACTIVE_ACQUISITION_PROTOCOL_V1_2.md) and
[results](../experiments/ACTIVE_ACQUISITION_RESULTS.md). Passive modes remain passive.

PowerShell, repository root:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-active start --new active --mode fixture --experiment relationship-acquire-lmft --relationship-scenario ambiguous --acquisition-policy disagreement
```

Restart with identical scenario/policy/mode/control, omitting --new. The source/config
manifest refuses drift or silent migration; old individuals require archived software.
Model configuration is unchanged; active modes refuse local operation before model setup.

## Explicit operations and existing investigation transport

Use the existing observation envelope with exactly text/operation/record. Training
and validation outcomes use the [registered insufficiency fixture](../src/lmft_lab/insufficiency_fixture.py),
which models a bounded buffer that refuses length-two payloads. This synthetic
verification authority is not authentication or a real-world sensor guarantee.

After all four training outcomes, send select with an empty record, then investigate
with an empty record. Nonempty ambiguous hypotheses are scored using the unchanged
ambiguity selector and an explicit numeric-scope adapter. Policy disagreement selects
the largest positive predicted disagreement, ties by declared order. Policy unavailable
offers only noninformative candidates and makes no request. The predefined control
noninformative deliberately requests q1 at score zero. Unique and empty families make
no request; empty reports no_supported_hypothesis without inventing candidates.

A selected observation produces a clarification_request in the deliberate outbox
and a matching entry in state.questions. Its episode/request identity and single
spent request unit persist together. Read the actual outbox ID; do not guess it.
The episode is local to the addressed individual directory, not a global authenticated ID.

Return the existing teacher_reply envelope as TRANSPORT ONLY; no teacher inference
occurs. Set reply_to to that outbox request ID and content.operation to verification.
The record must be exactly:

```json
{
  "episode_id": "active:relationship-episode-1",
  "request_id": "out-actual-id",
  "evidence": {
    "evidence_id": "q2", "scenario": "ambiguous", "split": "acquisition",
    "procedure": "capacity-blocked-two-1", "length": 5, "capacity": 5,
    "success": true
  }
}
```

Source must be registered-insufficiency-1. The outer request/episode/envelope IDs,
selected candidate features, strict schema/types and independent synthetic label
verification must ALL match. Rejected replies leave the question pending, hypotheses
unchanged and request budget spent. Correct a rejected submission with a new message
ID referencing the SAME request; conflicting reuse of a message ID is rejected.
Duplicate accepted evidence gets no new admission/filtering/verifier execution.

Only one episode/request exists per new individual. No reset or new episode operation
is available. A pending investigation can be explicitly cancelled using
close_investigation with an empty record; that never refunds its request unit.
Late replies then reject. Validation admission is blocked until investigation closes.
All four reserved validation outcomes and accept are required before predictions
use the effective hypothesis set. Original training evidence/derivation remains intact;
verified acquisition and its filtering/provenance are separate.

evaluate emits a prediction but never investigates, spends budget or learns. Pure
predictors and halted CLI probe preserve state/checkpoint bytes. While live, use
only outbox/lifecycle; full inspect/probe is refused until graceful halt.

## Counts and current limits

Request issuance costs one unit BEFORE any reply. Admitted acquisition count is
at most one. Receiver verification executions are separate: the frozen study has
one rejected false label plus one valid label, so two acquisition checks per
requesting episode. Its reserved intake has five training checks/four admissions
and four validation checks/four admissions. These are measured scripted counts.

There is NO cap on repeated eligible false-reply verification attempts under fresh
message IDs while pending. They cannot cause more requests/admissions or reset the
bank, but can consume more receiver computation and receipt storage. No automatic
timeout exists; cancellation is explicit. Do not interpret the one-request budget
as a bound on ALL computation. This limit is documented, not repaired in this priority.

Both modes share selection/filtering/validation and the inert scaffold. No numerical
propagation or LMFT advantage is claimed. Supported rules can still fail withheld
fault cases. Reproduce using a fresh complete current preservation context:

```powershell
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/my-active-context.json
.\.venv\Scripts\python.exe experiments/run_active_relationship.py --output outputs/my-active-study --preservation-context outputs/my-active-context.json
```

Keep source unchanged during a run; recapture after edits. Preserve complete local
outputs, which are ignored by Git.

## Optional checkpoint-accounted receiver cap

The unlimited behavior above remains the default. To opt in, add
`--receiver-attempt-budget 2` when creating an active individual, then use the
same value on restart. Strict values0..8 are supported. Budget0 can issue the
existing request, but its first eligible reply is denied without verification.
After source changes, archived software is still required for old checkpoints.

Each eligible acquisition check consumes a committed attempt, including a false
label. Malformed/unrelated/duplicate/conflicting replies remain cheap. A false
final attempt closes exhausted and blocks later valid evidence; a valid final
attempt succeeds. Cancellation does not refund, and no reset operation exists.

This cap bounds CHECKPOINT-accounted work, not physical calls across pre-commit
rollback. Computation can happen before a failed checkpoint write; replay can
compute again. It also does not bound arbitrary ingress parsing/receipt storage.
See [frozen receiver contract](../experiments/RECEIVER_BUDGET_PROTOCOL.md) and
[results with physical counterexample](../experiments/RECEIVER_BUDGET_RESULTS.md).
No durable pre-computation reservation or broader transaction redesign is added.
