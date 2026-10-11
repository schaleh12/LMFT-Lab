# Consistent support before suppression — preregistration v1

Recorded before implementation/evaluation. Preserve all prior experiments and their failures.
Zero models, no route learning, no new seed nodes or core numerical/judgment/migration changes.
Fixed imported route weights A=.25/B=.75/D=.5; eight prior contextual outcomes s1..u4
recreate existing conditional scores +1/3,-1/3 independently for every primary individual.

## Established historical failure
The preserved posthoc-cross-part trace has check1=false/check2=true. Each part singly
consistent gives Fact=1, while external resolution=false and direct Confidence=0.
Pass1: Confidence=.25 through Fact->Confidence, Clarity=0. Pass2 Clarity input sum
.75+.3125-.25-1=-.1875, gain .25 yields -.046875, clamped 0. This is premature closure
from coverage-driven inhibition and unearned propagated Confidence, not a faulty external
unanimity test. Reproduce this known case separately, not as fresh held-out evidence.

## Evidence relation, applicability and scope
Keep exact registered evidence validation, immutable IDs, scope/case/part provenance,
no majority overwrite, and at most one selected-question verifier request per case.
Questions: shielded (check1/check2) and payload_valid (check1), both relevant to prediction.
A diagnostic color question may be offered but is explicitly outside the decision scope.
Its exclusion is a named shared relevance gate, never credited to propagation.

Equality task: both shielded checks measure the same Boolean, so normalized values must
agree. Complement task f9: check2 measures the opposite property; invert its raw Boolean
before comparison. False/true is compatible there. Differences between different questions
are also compatible. The declared relation is observable, not inferred from truth. All
conditions use the same ordinary normalization/applicability rule. Raw evidence is never
rewritten; normalized views and supporting IDs are traced. Unverified reports do not
participate in consistency, even if expressed confidently. Missing checks cannot resolve.
Coverage is fraction of required parts having any eligible applicable observation.
Consistency fails if the union of normalized applicable values contains both Booleans,
including contradictions within a part. Empty/partial evidence can be nonconflicting
without being sufficient. Sufficient = full coverage AND no inconsistency.
Prediction requires both relevant questions sufficient and payload_valid=true, then uses
the unchanged shielded orientation counter. Otherwise abstain. No held-out outcome learning.

## Revised circuit and controls
Version consistent-support-1, two synchronous passes, gain .25, unchanged clamping.
Candidate direct inputs: Novelty=1 (independent attributed report conflict), Salience=1
(after shared relevance gate), Theory=.5, Fact=coverage, Confidence=1 iff sufficient,
Clarity=1 iff applicable normalized evidence is inconsistent; Execution=0.
Edges: Novelty->Theory .5; Salience->Execution route B=.75; Theory->Execution .5;
Fact->Execution -1; Confidence->Execution -1; Clarity->Execution +1.
Execution is a temporary authored request-priority readout, not autonomous action.
Clarity represents detected lack of coherence here, not achieved intelligibility. The
external relation rule detects inconsistency; propagation only uses that result.
No Fact->Confidence link and no external resolved gate in conceptual selection.
Select positive final Execution descending, ascending candidate ID ties; otherwise none.
These are explicit external readout/budget/tie rules. Do not change them after evaluation.

Six conditions: historical (call unchanged scoped-full selector on the common normalized
view); revised full; revised no-clarity (disable only Clarity->Execution); revised no-fact
(disable only Fact->Execution); revised no-confidence (disable only Confidence->Execution);
ordinary memory (same relevant scoped facts and relation, explicit insufficient-only gate,
inconsistency first, then fixed route weight, then ID). Historical numerical mapping and
its old part-based Fact input remain unchanged. Historical comparison receives the same
normalization/relevance adapter on fresh tasks; old equal-relation regression inputs are
identity-transformed. Match evidence, budgets, routes and teacher/verifier policy.

Predicted scores: no support .265625; half coverage .140625; full consistent 0; full
inconsistent .265625. No-clarity still gives full inconsistent .015625, so it may remain
eligible. Both other single ablations give full consistent .015625, permitting redundant
requests. A matched two-uncertainty case can expose Clarity's priority influence without
assuming it is necessary for every reopening. Equality or failure is acceptable.

## Fresh cases (independent initial states)
All have conflicting attributed reports for both relevant questions, IDs 1-shielded and
2-payload_valid. Prior evidence below is registered, not teacher assertion. Unless stated,
payload_valid=true is already verified and relation is equality. Replies are only for the
selected question; unselected verification truth is never accessed by selector/predictor.

| ID | Initial evidence | Selected-question verifier policy | Actual success |
| --- | --- | --- | --- |
| f1 | shielded both=true, payload=true | same values | true |
| f2 | shielded check1=true only | both=true | false |
| f3 | shielded check1=false/check2=true | both=true; conflict retained | true |
| f4 | both=true plus new eligible check2=false | both=true; conflict retained | true |
| f5 | shielded both=false; irrelevant color checks false/true | shielded=false or payload=true | false |
| f6 | both=true; confident unverified assertion says false | same verified values | false |
| f7 | check1=true duplicated; full shielded records other-case and old-scope | both=true | true |
| f8 | shielded check1=false/check2=true; payload missing | shielded both=true OR payload=true; one request cannot settle both | false |
| f9 | complementary checks false/true; payload=true | same compatible values | false |

Expected revised/memory: no calls f1/f5/f6/f9; investigate f2/f3/f4/f7/f8. f8 selects
shielded by priority/tie; no-clarity selects payload. This difference need not improve
prediction: both remain unresolved. Revised/memory expected six predictions, four correct,
three abstentions. f2/f6 deliberately defeat the conditional prediction despite resolution.
Do not score no decision as correct or conflate saved calls with improved accuracy.

## Separate regression groups and sequential test
Known counterexample: exact registered q6 records from preserved audit, with check1=false,
check2=true and payload=true. Compare all six modes; require unchanged historical failure
and report each new result separately. Previous preregistered regressions: q1..q7 from
SCOPED_ATTENTION_PROTOCOL, unchanged evidence/reply policy and equality relation. Never
pool these eight known cases with nine fresh cases for accuracy/generalization claims.

Sequential f4, each condition: start with both shielded checks true and payload true;
evaluate; halt/restart; deliver eligible check2=false; evaluate again; answer only any
new selected request; evaluate once more to demonstrate spent budget/retained uncertainty.
No reset of per-case budget. Conditions spending it before contradiction cannot request
again. Compare restarted revised full to uninterrupted identical messages. Repeat one
accepted evidence message five new IDs plus five exact deliveries, barrier for completion;
no evidence, changes, activation traces or requests from repetition. Retain receipts/files.

## Acceptance, metrics and preservation
Research criteria: reproduce historical trace/failure; test whether revised mapping avoids
premature suppression, avoids redundant verification, retains uncertainty on irreconcilable
conflicts, and matches or differs from memory. A failed research criterion is a result,
not permission to tune. Integrity requirements: exact outgoing-only ablations, unchanged
weights/counters/seed, scope/identity/type protection, no hidden truth in selection or
prediction, one request, restart equality, old-results preservation, zero model calls.
Metrics per group: verification count, redundant requests, useful unresolved requests,
no-request suppression of relevant inconsistency, inconsistency left uninvestigated,
reopening vs spent budget, unresolved after budget, prediction accuracy/coverage/abstentions,
wall/core time, record counts and storage. Shared relevance exclusion and prediction gate
must be explicitly attributed to ordinary code. No significance/population-level claims.
Stop at fixed 17 primary cases x 6 modes plus six sequential and one uninterrupted run,
420-second exchange deadlines. Record failures; do not overwrite runs.

Test partial/compatible/incompatible support, scope, duplicates, assertions, exact ablations,
reopening, exhausted budgets, restart and interrupted commits. During execution expose only
deliberate outbox/lifecycle acknowledgments; inspect internals only after halt. Archive
protocol, versioned configuration, all source/tests/harness, hashes and complete traces in
a fresh ignored outputs directory; preserve tracked selected findings separately.
