# Payload length / buffer capacity — preregistration v1

2026-10-12. Deterministic primary study; zero teacher/model calls. Preserve seed, activation,
propagation, sum(signs)/(n+2), +/-0.2 thresholds, migration and historical results. New accepted
relationships and validation records are separate developmental data, never seed mutations.

## Task and frozen splits

Procedure capacity-transmit-1: noiseless, empty buffer, one write per payload unit, no draining,
compression, framing overhead or concurrent writer. Verifier simulates bounded writes. Success
means all units transmitted; equality succeeds. Predictors receive only case ID, procedure,
integer length and integer capacity, no fits flag or outcome. Declared scope: both integers
0..8 inclusive and exactly this procedure. Missing/Boolean/out-of-range inputs abstain as
out-of-scope. ID is provenance, not a predictive feature. No model sees any of this task.

Training t1..t6 in order: (1,3), (2,4), (3,3), (4,2), (3,1), (2,1).
Validation v1..v4: (1,1), (4,4), (1,2), (4,3).
Held-out seen-combination new events s1..s4: (1,3), (3,3), (4,2), (2,1).
Held-out unseen combinations h1..h6: (1,4), (2,2), (2,3), (3,2), (3,4), (4,1).
Modest range shift r1..r6: (5,6), (6,5), (6,6), (8,5), (5,8), (8,8).
Out-of-scope x1: (9,8), separately excluded from in-scope quality denominators.
Training/validation pair sets are disjoint. Every h value occurs individually in training;
none of its pairs do. r uses new values5..8. Seen-combination results must not be called
combination transfer. All labels are produced by the verifier/evaluator, not predictor logic.

## Candidate language, selection and acceptance

capacity-comparison-1: exact schema {version, left:"length", op, right:"capacity"}; op in
fixed order [lt, le, eq, ge, gt, ne]. No constants, code, nesting, new features or arbitrary
expressions. Six total candidates; authored inductive bias. Evaluate each on training only.
A candidate is consistent iff it predicts every verified training outcome. Select only when
exactly one is consistent, after at least four examples with both labels (runtime additionally
requires all six registered training events). Ties retain uncertainty and no selected rule;
validation cannot break ties, and failed validation cannot trigger selection of another rule.

Training closes before validation. All four registered validation outcomes must match the
selected candidate for acceptance. Store all candidate errors/refs, training digest, selected
representation/version, validation per-case results/refs, applicability, acceptance reason
and supporting provenance. One selection/acceptance lifecycle per individual; no retry/tuning.
Rejected/unsupported external proposals never install a rule. Testing malformed syntax and
ambiguous training is separate from primary performance; no arbitrary code execution.

Training and validation are separate verified outcome records (operational facts). Candidate
comparisons are explanations under test. Theory/Fact nodes are not activated and do not cause
inference. The supplied simulator defines task truth; the candidate chosen by evidence is
learned selection within an authored family, not learned understanding of transmission.

## Matched conditions

Five modes: capacity-aggregate, capacity-lookup, capacity-lmft, capacity-memory, capacity-authored.
Every mode receives identical inputs, verified train/validation records and control operations.
Aggregate retains the existing global counter and thresholds. Lookup uses an exact (length,
capacity) counter, same equation; unknown pair abstains, no backoff or smoothing beyond +2.
Counters learn training only. Validation labels are available to all, but reserved for acceptance,
not fitted into aggregate/lookup counters or hypothesis selection. Four seen-pair probes test
lookup versus aggregation; six unseen pairs test transfer separately.

LMFT and ordinary relation-memory use the IDENTICAL deterministic candidate selector, DSL,
training and validation policy. Sharing these mechanisms prevents withholding induction from
memory; this experiment does not compare independent implementations. Authored diagnostic
explicitly applies length<=capacity without learning; report separately. All retain the coarse
counter. Accepted relation predictions are direct Boolean evaluations with no invented confidence
score: a new explicit predictor, not a change to the evidence-counter equation. Trace inputs,
relationship reference, result and coarse counterfactual on every prediction.

## Execution, metrics and acceptance

Five restarted individuals and five uninterrupted references = ten. Admit train; redeliver t1
five exact and five new-ID copies; conflicting t1 rejects. Attempt a registered held-out outcome
as learning: reject before executing hidden truth. Reject malformed executable and well-formed
external relationship proposals. Select using train only, admit validation, accept once. Probe
one fresh case BEFORE acceptance (relationship conditions abstain) using no labels. Halt/restart
before held-out evaluation, with exact no-input restart equality; controls never halt midstream.
Only inbox/outbox/lifecycle while live; full inspection after halt. No waiting cognition.

Check seed/counter preservation, evidence deduplication, train/validation/held-out separation,
unique training-selected le candidate, five rejected inconsistent candidates, one accepted
relationship in each relation mode, four successful validation checks, explicit provenance,
read-only probe invariance, unsupported/scope rejection, actual restart/uninterrupted accepted
state and semantic response equality. Tests also exercise ambiguous training, malformed DSL,
validation failure, changed source/split, and no hidden verifier access from selection/prediction.

Report accuracy among decisions, coverage and abstentions for seen-pair, unseen-pair, range-shift,
and equality-boundary subsets separately. Predictions are frozen before held-out labels are
executed for scoring. Expected aggregate: score0 (three successes/three failures), all abstain.
Lookup: four seen pairs correct, unseen/shift abstain. Both learned relationships and authored
reference: all sixteen in-scope predictions correct/covered for this noiseless family. Scope x1
must abstain in every mode. These are falsifiable expected results, not criteria to tune toward.

Measure transition time, bytes, evidence/candidate/validation/accepted/rejected record counts,
zero calls. Snapshot source/config/protocol, messages, full halted states, evaluations and failures
in a new outputs path. Do not overwrite previous studies. Stop after the fixed suite; no teacher
integration or additional experiment implementation. Distinguish mechanism checks from quality
results, retaining negative outcomes even when execution succeeds.
