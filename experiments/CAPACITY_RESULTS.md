# Payload length and buffer capacity — evaluated results

Evaluated 2026-10-12 under the frozen [protocol](CAPACITY_PROTOCOL.md).
[Implementation and commands](../docs/CAPACITY_EXPERIMENT.md). Complete archived sources/configs,
original inputs, candidate evaluations, acceptance records, halted states, predictions and
results remain in `outputs/capacity-001/`. Historical studies and prior continuation work remain.

**A training-selected, separately validated relationship transferred to fresh combinations.
LMFT matched equally capable ordinary memory exactly. Seed activation had no causal role.**

## Supplied versus learned

Supplied: a deterministic noiseless bounded-write simulator; numerical length/capacity
observations; fixed train/validation/held-out splits; the six-candidate comparison language;
unique-consistency selection; all-four-validation acceptance; applicability 0..8; and an
explicitly authored <= reference baseline. No precomputed fits flag was supplied to predictors.

Learned: selection of `length <= capacity` from the six candidates using verified training
outcomes. Candidate evaluations, evidence IDs/digests and validation traces remain inspectable.
The selected rule was not installed from fixture code or a teacher statement. The hypothesis
family and supplied features are strong authored inductive biases containing the simulator's
true relation; this is not independent discovery of the feature vocabulary or learned semantic
understanding of transmission.

The immutable 40-node birth state is separate from `accepted_relationship`. No activation,
propagation or Theory/Fact node causes inference. Operationally, facts are verified outcome
records; theories are comparisons evaluated against them. Model calls, including mock inference:
**zero**. The current teacher adapter/profile/configuration were read but not changed or used.

## Evidence and relationship acceptance

Six training events had three successes and three failures, so the unchanged coarse counter
remained **0/(6+2) = 0**, abstaining throughout. Exact-pair counters had one training sample
each and scores +/-1/3. Four validation events were reserved for acceptance in every condition;
they were not fitted into counters or used to rank candidates.

| Candidate | Training disagreement references |
| --- | --- |
| length < capacity | t3, the equality case |
| length <= capacity | none |
| length == capacity | t1, t2 |
| length >= capacity | t1, t2, t4, t5, t6 |
| length > capacity | all six |
| length != capacity | t3, t4, t5, t6 |

Both learned conditions selected the unique consistent `le` candidate before validation.
All four validation checks matched; each accepted one relationship. Five candidates were
filtered as training-inconsistent, and zero selected relationships failed validation in the
primary run. The tests separately retained ambiguity between lt/le when equality evidence
was omitted and rejected a validation mismatch without selecting a fallback.

Each accepted artifact contains `capacity-comparison-1`, explicit operands/operator, bounded
applicability, the complete derivation and training references/digest, validation references/
digest/checks, acceptance message and reason. It survives restart. In the explicit fresh h1
trace (length1, capacity4), the learned predictor changed from abstain before acceptance to
success afterward, using `capacity-relationship-1`; the coarse counterfactual remained abstain
at score0. Relation prediction is direct Boolean evaluation with score=null, not a modification
to the counter formula or a confidence probability.

Every individual also rejected one conflicting evidence identity, one held-out learning attempt,
one malformed executable proposal and one well-formed external relationship proposal. The
last two are rejected inputs, not candidates considered by the internal induction policy.
Five exact and five reattributed training deliveries added no evidence or counter revisions.

## Prediction quality by split

Cells show correct/decided, followed by abstentions. Accuracy is correct among decisions;
where no decision exists it is undefined, not zero. Seen-combination probes are new events
at previously trained pairs; they are explicitly not evidence of combination transfer.

| Condition | Seen pairs (4) | Unseen combinations (6) | Range shift (6) |
| --- | --- | --- | --- |
| Aggregate counter | 0/0; 4 abstain | 0/0; 6 abstain | 0/0; 6 abstain |
| Exact-pair conditional memory | 4/4; 0 abstain | 0/0; 6 abstain | 0/0; 6 abstain |
| LMFT accepted relationship | 4/4; 0 abstain | 6/6; 0 abstain | 6/6; 0 abstain |
| Ordinary relation-learning memory | 4/4; 0 abstain | 6/6; 0 abstain | 6/6; 0 abstain |
| Authored <= diagnostic | 4/4; 0 abstain | 6/6; 0 abstain | 6/6; 0 abstain |

Across sixteen disjoint in-scope probes, aggregate coverage was 0%; exact-pair memory coverage
was 25%, with 100% accuracy on its four decisions; each relation condition/reference had 100%
coverage and 100% accuracy. The lookup comparison shows improved correct decisiveness on known
pairs relative to aggregation, but no transfer to unknown pairs. Relation-learning memory is
the competent induction comparator; exact lookup is not presented as the strongest memory.

Unseen combinations used familiar individual values 1..4 but pairings absent from both training
and validation. Range-shift cases used values 5..8 and are reported separately, within declared
scope. These six successes do not establish arbitrary extrapolation. The equality subset
(overlapping the table's splits) contained four probes: learned relationships/reference got 4/4;
lookup answered one correctly and abstained on three (25% coverage); aggregate abstained on all.
Every condition returned out_of_scope on (9,8), excluded from accuracy/coverage denominators.

All five conditions received identical observables and eligible evidence. LMFT and ordinary
relation memory shared exactly the same candidate language, selector and acceptance policy.
Their accepted artifacts and semantic responses matched, excluding only the explicit predictor
condition label. This demonstrates useful representation and transfer in the defined task,
not an LMFT or fuzzy-tree advantage. The authored diagnostic's perfect result is not learning.

## Persistence, isolation and regression verification

**413 tests passed**, including 26 new capacity tests. **155/155 integrity checks and 40/40
preregistered quality checks passed** across ten actual runtime individuals (five restarted,
five uninterrupted). All halted. No evaluated failure or criterion change occurred.

Each restarted individual halted after acceptance, underwent an exact no-input restart/halt
check, and restarted before held-out evaluation. Scientific judgments, accepted state, seed and
semantic responses matched uninterrupted execution. Pure probes caused no learning; inbox
evaluation recorded communication only. Held-out evaluation did not alter train/validation,
coarse/lookup counters, selection, validation or accepted relationship.

The complete prediction set was written before any held-out outcome was executed for scoring.
Tests prevent verifier/simulator access during selection, acceptance over already verified
records, and prediction. Held-out learning attempts reject before executing hidden outcomes.
Malformed DSL, Boolean/missing/out-of-range inputs, unsupported proposals, source/split errors,
ambiguous selection, duplicate/conflicting evidence and validation mismatch are covered.
Atomic acceptance faults before/after replacement recover the complete old/new transaction.
Live inspection was refused; only deliberate outbox and lifecycle communication was inspected
while processes ran. No historical checkpoint was rewritten.

## Costs

Measured values below are restarted individuals. Processing time covers transitions, excluding
checkpoint writes, process lifecycle and waiting. These single-run timings are descriptive only.

| Condition | Processing seconds | Final checkpoint bytes | Individual-directory bytes | Post-acceptance checkpoint growth |
| --- | ---: | ---: | ---: | ---: |
| Aggregate | 0.030804 | 82,952 | 97,614 | 28,939 |
| Exact lookup | 0.031982 | 81,675 | 96,336 | 27,761 |
| LMFT relation | 0.036218 | 90,942 | 105,604 | 32,748 |
| Memory relation | 0.034786 | 91,020 | 105,683 | 32,816 |
| Authored rule | 0.033434 | 86,325 | 100,987 | 32,118 |

Each stored six training/four validation records, six coarse revisions, 44 receipts, 34 outbox
records and 18 evaluation traces (one pre-acceptance plus 17 held-out/scope probes). Each learner
additionally stored six candidate evaluations and one accepted relationship with four validation
checks. Every condition retained the coarse and pair counters for matched inspection; this is
not a minimal-memory cost contest. No model diagnostics or questions were generated. Whole-
history checkpoint/storage limitations remain, and duplicate deliveries still consume receipts
and inbox bytes. Full uninterrupted timing/counts are in results.json.

## Limits and smallest next experiment

The candidate family contains the correct rule; measurements are exact; all task conditions
are fixed and explicitly declared. This is a small deterministic family-selection result, not
robust causal learning, noisy-measurement handling, free-form theory creation, calibrated
confidence or open-ended generalization. There is no runtime mechanism here for revising an
already accepted relationship or autonomously obtaining missing evidence. Scope includes 0,
though zero-valued inputs were not in the evaluated split. The primary suite had no ambiguous
selection; that safety behavior was unit-tested, not established through an interactive study.

The smallest next experiment is a deliberately ambiguous training set without equality cases,
leaving lt/le both viable, followed by at most one independently verified equality observation.
Freeze an explicit evidence-request budget and acceptance lifecycle in a new protocol. Compare
no-additional-evidence abstention, LMFT and equally capable memory given the same new observation,
then test untouched equality and non-equality pairs plus a fresh reserved validation set. If
uncertainty resolves only after informative evidence and both systems transfer equally, credit
the evidence and finite hypothesis elimination. Do not default to <=, let held-out labels break
the tie, or claim a fuzzy advantage. This proposed follow-up is not implemented here.

## Reproduction and archive

Protocol SHA256: `a6df7d13906bd4f76b922ef3009641798681019adbacb5fba602832cbbcb00ec`.
All archived source/config/protocol hashes matched after the evaluated run, before documentation
completion. `outputs/capacity-001/` contains complete evidence and traces; it is ignored by Git
and not an external archival service. Preserve a durable copy of the complete halted directory.
Prior dirty workspace work was preserved; its key files were snapshotted under
`outputs/capacity-prework/` before implementation.

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_capacity.py --output outputs/my-capacity-study
```

Use a fresh output path; failures are retained and existing results cannot be overwritten.
