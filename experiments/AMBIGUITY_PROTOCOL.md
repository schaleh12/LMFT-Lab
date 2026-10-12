# Relationship ambiguity — preregistration v1

Frozen 2026-10-12 before evaluation. Zero model calls; deterministic seed 42.
This isolated study reuses capacity-comparison-1 and capacity-transmit-1's bounded
write verifier. Existing runtime, counters, numerical mechanisms, seed, migration,
model configuration and historical studies remain unchanged.

## Cases and authored hypothesis space

Six authored operators in order lt, le, eq, ge, gt, ne; length and capacity are
strict integers 0..8. Training: t1=(1,3), t2=(2,4), t3=(4,2), t4=(3,1).
All four verified outcomes are required, with both labels. Expected survivors:
lt and le, both retained; no default or arbitrary hypothesis tie break.

Candidate observations, in order: q1=(0,2), q2=(5,5), q3=(6,6), q4=(7,6).
Predictors receive these features only, never candidate outcomes. Score each by
number of disagreeing unordered surviving-hypothesis pairs (true votes times
false votes). Select maximum positive score, ties by declared candidate order;
if all scores are zero, make no request. No equality-specific selection branch.
Verify at most one selected observation, once, with the bounded-write simulator.
Filter survivors only with training and that verified acquisition. Keep outcomes
and hypotheses in separate records; trace votes, scores, refs and rejection reasons.

Fresh validation: v1=(0,3), v2=(2,5), v3=(5,2), v4=(7,4). These are disjoint
from training, acquisition and evaluation. Validation cannot filter/rank hypotheses.
Accept the retained hypothesis set only if every survivor matches all four records;
otherwise reject the whole set, with no fallback or retry. Non-equality validation
deliberately checks consistency without secretly resolving lt/le.

Held-out equality: h1=(2,2), h2=(3,3), h3=(7,7), h4=(8,8).
Held-out non-equality: h5=(0,1), h6=(4,6), h7=(6,4), h8=(8,7).
Scope probe x1=(9,8) is excluded from quality denominators. Case IDs are provenance.
Consensus means all accepted survivors predict the same Boolean; disagreement
means abstention. No accepted set also means abstention; invalid scope is separate.

## Matched conditions and execution

For BOTH LMFT and ordinary memory run four policies: disagreement on all q cases;
predefined non-informative control requests q1 regardless of score; unavailable
uses only q1,q4 and disagreement selection (thus no request); no-evidence requests
nothing. Ordinary memory uses identical code, space, evidence, candidates, validation,
budgets and opportunities. Only LMFT stores the unchanged canonical birth scaffold;
neither reads activation or propagation for predictions. This is a standalone
file-backed study, not integration into the supervised inbox/outbox runtime.

For each of eight conditions, run restarted and uninterrupted references. The
restarted checkpoint is loaded by a separate Python process after validation,
then fresh predictions are computed without learning. Freeze all predictions
before any held-out outcomes are executed. Evaluation is read-only, including
checkpoint byte/hash invariance. Record actual process identity and restart equality.
Deduplicate exact evidence identities; conflicts, wrong source/schema/split/features,
unselected acquisitions, second requests, external proposals and held-out admission
must reject before verifier execution where possible. Duplicate outcomes consume
no acquisition budget. Preserve all input and rejection traces. Source/config/protocol
hash guard and checkpoint checksum reject incompatible recovery.

## Metrics and frozen acceptance criteria

Report ambiguity resolution (one survivor), verified request count, validation
acceptance, coverage, abstentions, correct/decided and accuracy among decisions
(null when none), separately for equality and non-equality and overall.
Expected disagreement: one request q2, le retained, 100% coverage/accuracy.
Other policies: lt/le remain; equality coverage 0%, non-equality 100%, overall 50%,
accuracy 100% among decisions. Negative unresolved results are valid findings.

Integrity requires initial lt/le, feature-only scored selection, budget <=1,
no validation selection, restart state/prediction equality, deduplication and
rejections, read-only evaluation, seed preservation, exact baseline parity,
and zero calls. Quality expectations above are falsifiable checks, not tuning
targets. Tests exercise validation failure, malformed inputs, source/config drift,
checksum corruption and oracle isolation. Archive protocol/source/config, evidence,
requests, states, predictions, metrics and failures in a fresh directory; never
overwrite a run. Stop after this suite and focused fixes. Deterministic filtering
cannot establish fuzzy propagation, understanding or an LMFT advantage.
