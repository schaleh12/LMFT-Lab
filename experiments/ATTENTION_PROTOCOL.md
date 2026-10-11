# Attention and verification â€” preregistration v1

Frozen before implementation/evaluation. Synthetic fixture only; historical studies remain unchanged.

## Task and evidence
Each case contains conflicting attributed reports for shielded (decision relevant) and
color (irrelevant). Two shielded verification routes A/B and one color route D are offered.
A repeated report keeps its original report ID/source and supplies no independent evidence.
Reports are never facts. All conditions receive identical public records and the same
selected-request verifier policy. Counterfactual unselected replies are never fetched.
Verifier truth is isolated from selection/prediction. Only the selected route can be
validated; a reply must match that registered request, exact types and source provenance.
This is an ideal synthetic verifier, not authentication or real-world grounding.

Reuse the previous eight registered transmission outcomes s1..u4 and existing validated
counter update: shielded +1/3, unshielded -1/3. Verified shielded selects that branch;
existing support/oppose thresholds predict success/failure. No verified condition means
abstain. No held-out outcome revises these counters. Verification resolution is a separate
learning target from prediction correctness.

## Authored pathway
One fresh frame per candidate. Leaf inputs: Novelty=1 for unique independent conflict,
Salience=1 for shielded / 0 for color, Theory=.5 for conflicting unverified reports,
Fact=0 until a verified Boolean is available, Clarity=0, Confidence=0. No implicit tree
edges. Edges Novelty -> Theory (.5), Salience -> Clarity (route weight w),
Theory -> Clarity (.5), Fact -> Confidence (1), Confidence -> Clarity (-1).
Existing synchronous propagation: two passes, gain .25, unchanged clamping equation.
Rank final Clarity descending, candidate ID ascending ties; require an independent
conflict and positive score. Clarity here is an authored *need for clarification* signal,
not achieved intelligibility. Confidence encodes verified support only, not persuasive
language or probability. Post-verification frames record Fact=1 and Theory=0 when
resolved; no second request is allowed. Seed leaf names do not change numeric node fields.
All edges are sidecar interpretations; only Salience -> Clarity route weights learn.
Initial weights A=B=D=.5. Update selected relevant route w := clamp(w + .25*(2r-1),0,1),
where r=1 iff the validated reply supplies a Boolean shielded value, otherwise 0.
Irrelevant verifications do not update weights. Freeze all association learning after t2.
Store before/after, verified evidence identity, attribution and explicit eligibility reason.

## Conditions and fixed sequence
LMFT learns; frozen LMFT uses same propagation with no weight updates; disabled pathway
uses an actionable fallback: independent conflict candidates in ID order (D=0,A=1,B=2),
without relevance propagation or learned weights. Ordinary memory uses explicit relevance
first, then same learned route weight, then ID; no propagation. It learns on t1/t2 equally.
Budget exactly one request per case, zero model calls. No conflict -> abstain/no request.

Pre-learning fresh p1: shielded=true, actual success; A unavailable, B available, D available.
Training t1: true/success, A unavailable, B available; t2: false/failure, A unavailable,
B available. p1 is evaluation only. t1 penalizes A .5 -> .25; t2 selects B and rewards
B .5 -> .75. Learning frozen thereafter. Halt/restart after t2, compare uninterrupted.
Held-out h1: true/success; h2: false/failure; h3: true/failure; h4: false/success;
A unavailable/B available for h1..h4. h5: true/success, both routes unavailable.
All have color=true, independent color conflict. h3/h4 deliberately test exceptions to
conditional orientation; no perfect accuracy expected. Training/held-out case IDs differ.
No-conflict n1 offers only repetitions of a single shielded assertion; no request.
Truth fields are evaluator/verifier-only. The protocol is public to developers, never
an input to selector/predictor. Diagnostic p1: propagation selects A, fallback selects D.
This is wiring evidence, not superiority. Predicted held-out LMFT/memory: 4/5 coverage,
2/4 accuracy, one unresolved; frozen/fallback: 0/5 coverage. Report unfavorable p1 too.

## Acceptance, robustness and costs
Require causal counterfactual, exact eligible weight changes, no fact from assertions,
no learning on p1/held-out, baseline equivalence, restart/uninterrupted learned-state
and decision equality, one request/case, no second request after unresolved answer.
Malformed/forged replies leave request pending; corrected same request may be accepted
without extra budget. Duplicate evidence under same/new message IDs adds no update,
verification, or propagation trace. Repeat accepted t1 reply five new IDs plus five exact
deliveries; record lightweight receipt/storage overhead. Conflicting evidence ID rejects.
Test bounds, attribution conflict, malformed replies, budget exhaustion, dedup, restart,
and faults before/after atomic commit. Stop at fixed cases/repeats, 420 seconds per wait.

Measure relevant/irrelevant selections, resolved/unresolved, correct/decided/abstained,
unnecessary requests (irrelevant or unresolved), model calls=0, timing, persistent counts,
checkpoint/directory bytes and repeat growth. Timing descriptive; no population inference.
Only deliberate outbox/lifecycle during runtime; inspect internals after halt. Archive
protocol/config/source/tests/traces/hashes before evaluation, results in a fresh ignored
outputs directory. No tuning after held-out evaluation. Existing seed, equations, judgment
rules, migration and historical reports must remain byte-identical.

Pre-evaluation implementation review: Theory input is .5, leaving headroom so the
Novelty edge contributes rather than saturating at 1. No evaluated cases have run.
