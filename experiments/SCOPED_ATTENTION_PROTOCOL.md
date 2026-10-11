# Scoped verified support — preregistration v1

Frozen before implementation/evaluation. Preserve ATTENTION_RESULTS and all historical
outputs. Deterministic, zero inference calls, one additional request per case. No new
seed nodes, core equations, counter update or migration changes. Authored mappings are
experimental conventions, not discovered concepts or calibrated confidence.

## Fixture, evidence and prediction
Seven fresh cases q1..q7. Each has two decision-relevant questions: shielded and
payload_valid, with candidate IDs 1-shielded and 2-payload_valid; both use route B.
All conditions start each primary case from the same neutral seed, previously learned
fixed route weights A=.25/B=.75/D=.5, and eight verified contextual prior outcomes
s1..u4 (conditional scores +1/3,-1/3, existing update/threshold rules).
No new route learning. Fixed weights are an explicit imported experimental initial
condition, not newly learned in this study.

Evidence has immutable ID, case_id, scope, question, part, Boolean value and source.
Applicable means exact case and scope and known question/part; eligibility means exact
registered synthetic record including types. Preserve provenance even if inapplicable.
Unverified assertions are attributed reports only, regardless of certainty wording.
Shielded requires two distinct parts (check1/check2) with one consistent Boolean value
across all applicable records. Payload_valid requires one part (check1), also consistent.
Any eligible opposite value retains both observations and makes the question unresolved;
no majority vote, recency replacement or fabricated reconciliation. Duplicate IDs cannot
add evidence. Two different IDs for one part are not two independent required parts.
Resolution is this ordinary evidence policy, never inferred from seed activation.

Prediction requires both questions resolved and payload_valid=true. It then uses the
existing conditional orientation for shielded. Otherwise abstain (including payload
invalid, outside this declared valid-payload scope). Held-out outcomes never revise
judgments. Verification returns registered parts only for the selected question; it
cannot inspect unselected answers for selection. Evaluator reads final outcome after halt.

## Authored mapping and influence ablations
Use the prior attention pathway constants and synchronous two passes/gain .25 unchanged.
For each candidate: Novelty=1 and Theory=.5 for its two independent conflicting attributed
reports, Salience=1, Clarity=0. These inputs remain the same when verified evidence exists:
there is no hidden resolved-state reduction of these inputs. Fact is the fraction of
required parts with nonconflicting applicable evidence (0,.5,1); Confidence direct input
is 1 iff the full evidence requirement is satisfied, otherwise 0. Cross-part disagreement
also forces unresolved, even if individual parts are nonconflicting. Trace both raw facts
and sufficiency separately from these named leaf activations/numeric node fields.

Preserve edges Novelty->Theory .5, Salience->Clarity B=.75, Theory->Clarity .5,
Fact->Confidence 1, Confidence->Clarity -1. Add separately authored Fact->Clarity -1
as direct support attenuation; it does not alter seed geometry or propagation equations.
Choose highest final Clarity >0, ascending candidate ID ties; otherwise no request.
No additional resolved-state gate for conceptual conditions. Trace the positive-score
eligibility rule and one-request budget as external procedural gates. No fallback request
on zero scores. Removing edges never removes evidence access or the decision policy.

Conditions: full; no-fact (disable Fact->Confidence AND Fact->Clarity only);
no-confidence (disable Confidence->Clarity only); neither (all three off);
memory (explicit unresolved-only gate, same evidence/weights, ascending ID ties, no propagation).
The baseline gate is intentionally explicit and competent. No tuning after evaluation.
For a fully resolved question, full score clamps to 0; either single ablation leaves
.015625; neither leaves .265625. Unresolved with no evidence scores .265625. Thus single
ablations can still prioritize unresolved over resolved; fully resolved cases diagnose
whether either remaining inhibition alone suffices to suppress a request. These are
wiring predictions from an authored circuit, not evidence of inherent cognitive necessity.

## Frozen fresh cases
All initial payload_valid values below are true where known; all scopes are batch-1.
All questions retain conflicting attributed reports, including when evidence resolves them.

| Case | Initially available verified information | Selected reply | Actual success |
| --- | --- | --- | --- |
| q1 | shielded check1/check2=true; payload unknown | payload=true | true |
| q2 | shielded check1=true only; payload=true | shielded both=true | false |
| q3 | payload=true; confident teacher assertion shielded=true only | shielded both=false | false |
| q4 | shielded both=true and payload=true; deliver shielded check1 twice | any selected question repeats known values | false |
| q5 | payload=true; shielded=true records for other case and old scope | shielded both=true in current scope | true |
| q6 | shielded check1/check2=true plus eligible check1=false; payload=true | shielded both=true, conflict remains | true |
| q7 | shielded both=false and payload=true | any selected question repeats known values | false |

Primary cases use independent individuals, never carry evidence/budgets between cases.
Expected full/memory requests: payload for q1; shielded for q2,q3,q5,q6; none q4,q7.
Single/both ablations may redundantly select shielded on q4/q7 but must not be artificially
blocked from acting. All conditions use the same initial evidence and verifier policy;
only selected replies differ. q6 stays unresolved despite reconsideration: explicitly
report this negative limitation. Expected primary final decisions six, correct four,
abstention one for full, either single ablation and memory. With neither influence,
q1 ties and selects already-resolved shielded, leaving payload unknown: five decisions,
three correct and two abstentions. No saved-call-to-accuracy improvement claim.

## Sequential reopening and persistence
Separate q6 individual: deliver all initial evidence except contrary record, inspect via
deliberate evaluate response (full/memory no request), halt/restart, deliver new eligible
contrary record, evaluate again. Its unchanged case budget permits the first request;
selected reply cannot erase the contradiction. Compare an uninterrupted full run with
identical message sequence and question references. No new budget on repeated evaluation.
Repeat accepted evidence five new message IDs plus five exact deliveries and a barrier;
no ledger, activation trace, revision or request growth from duplicates. Receipts remain.

## Acceptance and metrics
Require scope isolation, partial evidence remaining unresolved, no fact from assertions,
dedup, contradiction reopening, unchanged route weights/seed/counter scores, no hidden
truth access in select/predict, actual restart equality and uninterrupted equivalence.
Test malformed evidence/replies, budget exhaustion and atomic commit interruption too.
Measure per-case initial/final resolution, chosen question, redundant requests (question
already resolved), appropriate requests, inappropriate suppression (unresolved relevant
question but no request), calls saved relative to neither, decisions/correct/abstained,
model calls=0, timing, record counts and storage. Report accuracy among decisions separately
from coverage and resolution. No significance/population inference from seven authored cases.
Stop after fixed seven cases x five conditions plus sequential tests, 420s per exchange.

During runtime use only deliberate inbox/outbox and lifecycle acknowledgments; full state
inspection only after halt. Snapshot protocol, config, all sources/tests/harness and hashes
before evaluated run. Fresh outputs directory, preserve failures, never overwrite history.

Pre-evaluation arithmetic correction: a unit test exposed the q1 tie when BOTH outgoing
influences are removed. The original expected-count sentence overlooked ID tie-breaking.
Corrected expectations above; mappings, cases, evidence, rules and acceptance requirements
are unchanged. No evaluated run has occurred. Also report missed unresolved opportunities
separately from literal no-request suppression, to distinguish wasting a budget from abstention.
