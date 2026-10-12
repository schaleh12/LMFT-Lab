# Opt-in receiver attempt accounting — protocol v1

Frozen 2026-10-12 BEFORE evaluation. One bounded follow-up only. Preserve the
unlimited active default and all prior dirty work/archives. Zero model/mock calls,
no teacher/seed/numerical/configuration/migration changes or dependencies.

## Scope and truthful guarantee

Add optional --receiver-attempt-budget to existing NEW active modes. None (omitted)
retains old unlimited receiver behavior/state shape/policy. Explicit strict integer
0..8 enables receiver-attempt-policy-1. Pin it in birth/software policy; changing
budget/control/source on restart rejects. No silent checkpoint migration.

Retain one investigation request and at most one admitted acquisition per episode.
Finite budget counts eligible acquisition-verifier invocations represented by the
COMMITTED checkpoint. Count attempts before calling the verifier in the computed
transition, persist with verdict/phase/question/receipt/cursor in the same commit.
False labels consume attempts; no refund/reset through replay/restart/cancellation.

This is NOT a hard bound on physical process invocations across rollback. Verifier
computation happens before atomic checkpoint replacement. A before-replace failure
can restore an uncharged pending state AFTER computation occurred; replay can compute
again. Physical calls may therefore exceed the checkpoint budget under repeated
pre-commit failures. Do not claim reservation-before-computation, CPU/network/memory
defense or crash-proof physical at-most-once execution. A new transaction design is
outside scope. Report committed logical attempts and independently observed physical
invocations separately, including the deliberately negative rollback result.

## Fixed intake order and exhaustion

Reuse all active v1.2 correlation, syntax, evidence and selection rules unchanged.
Ordering: runtime envelope/message identity dedup/conflict; learning gate; transport
type/source; exact episode/request/reply_to; strict selected evidence schema/features;
accepted-evidence duplicate/conflict; still-pending phase/question; FINITE remaining
attempt gate; charge logical attempt; invoke verifier; handle verdict.

Malformed/unrelated/source/correlation errors and exact message redelivery are cheap:
zero verifier call and zero attempt. Duplicate accepted evidence under a fresh ID
is cheap AFTER source/correlation checks. Conflicting same-message identity and
accepted-evidence identity reject cheaply. A rejected false label is not stored as
a fact; the SAME false claim under fresh IDs is eligible again while pending and
consumes another attempt. Do not silently invent failed-evidence dedup semantics.

If no attempts remain when an otherwise eligible reply arrives (including budget0),
do not invoke verifier; close the episode/question with receiver_budget_exhausted,
preserve hypotheses, and explicitly report exhaustion. A false verdict consuming
the LAST attempt also closes exhausted immediately. A valid verdict on the last
permitted attempt succeeds, closes answered and is NOT a denial/exhaustion outcome.
Budget remaining may be0 after success; report exhaustion reason separately.
After exhaustion, late valid/false replies reject before verifier and cannot reset
budget or resolve hypotheses. Validation may proceed on the retained ambiguous set.

Budget0 still permits the existing single request; its first structurally eligible
reply is denied without verification and closes exhausted. No unsolicited reply
creates a request or counter. Cancellation retains attempts/request charges; no
automatic timeout/reset. Rejections may update cost/closure metadata when consuming
an attempt, but cannot install/filter unverified hypotheses. Exhaustion's intentional
phase/question change is explicit, distinct from cheap-rejection invariance.

## Task, controls and fixed expectations

Use ONLY original ambiguous training/validation/held-out case sets and disagreement
selector from active v1.2. Candidate features and hypotheses unchanged; q2 is selected.
All mode pairs receive identical evidence, attempt/request budgets and policies.
Known length-two fault errors remain; no new hypotheses or repair.

Seven fixed receiver sequences, both LMFT/memory, restarted and uninterrupted:

| Sequence | Budget | Eligible reply script | Committed/normal physical checks | Admissions | Effective set | Exhaustion | Coverage / decision accuracy |
| --- | ---: | --- | ---: | ---: | --- | --- | --- |
| zero | 0 | valid | 0 | 0 | lt,le | Yes | 50% / 75% |
| valid-first | 2 | valid | 1 | 1 | le | No | 100% / 75% |
| false-valid | 2 | false, valid | 2 | 1 | le | No | 100% / 75% |
| exhausted-late | 2 | false, false, late valid | 2 | 0 | lt,le | Yes | 50% / 75% |
| fresh-ID-flood | 2 | six false under distinct IDs, late valid | 2 | 0 | lt,le | Yes | 50% / 75% |
| last-valid | 1 | valid | 1 | 1 | le | No | 100% / 75% |
| legacy-flood | None | six false under distinct IDs, valid | 7 | 1 | le | No | 100% / 75% |

All28 main individuals issue exactly1 request; admissions <=1. Finite accounted
attempts <= budget; normal crash-free physical executions match committed attempts.
Legacy reference is FINITE scripted replay of old behavior, never unbounded ingress.
Each individual processes at most100 fixture inbox messages; flood contains exactly
six distinct false IDs and one valid ID. Cheap-negative messages and duplicate/conflict
deliveries are predefined separately and do not invoke verifier. Expected ops,
resolution, checks, admissions, exhaustion and quality are keyed ONLY to the frozen
sequence, not observed outcomes. Equality/non-equality denominators remain four/four.

Bad/hostile eligible claims CAN exhaust the cap and block later legitimate evidence:
exhausted-late/flood remain ambiguous while legacy-flood resolves at greater cost.
This denial-of-service tradeoff is a result, not a failure to hide or repair.

## Persistence, atomic faults, metrics and checks

Use real runtime inbox/outbox/questions/receipts/checkpoints. Restart all restarted
conditions while pending BEFORE first reply; exact no-input recovery. Restart again
after scripted reply stage, including exhausted conditions; then validate/evaluate.
Compare uninterrupted scientific state/questions/semantic responses, ordinary memory
and a direct standalone budgeted reference using the same evidence/policy.
Pending attempt counters and exhausted closure must survive actual process restart.
Pure evaluation never attempts verification, issues requests or mutates budgets.
Freeze ALL predictions before any held-out scoring; evaluation outcomes never learn.

Measure request count/units, eligible candidate checks, committed attempts, actual
normal-process verifier calls, admitted observations, exhausted replies/state,
coverage/accuracy separately. Receiver-call instrumentation in no-fault process runs
uses receipt execution counters; independent verifier spies/append-only call markers
in fault tests record computation OUTSIDE the scientific checkpoint.

Before/after-replace fault tests must check atomic budget/verdict/question/evidence/
receipt/output/cursor recovery. Real child-process test, budget1, false reply:
before-replace fault then restarted replay => physical calls2, final committed
attempts1, no admission, exhausted; after-replace fault then restarted replay =>
physical calls1, final committed attempts1, no double execution. Preserve raw call
markers/PIDs and original/recovered states. These tests deliberately disprove a
hard physical bound. No runtime reservation/journal redesign is permitted.

Require malformed/unrelated/cheap duplicate/conflict handling, cancellation/no reset,
zero/invalid budget validation, changed-budget restart refusal, last-valid success,
post-exhaustion late denial, source/model/seed invariance, original passive/unlimited
regression, full ACTUAL checkout suite with complete nonempty current contexts and
separate historical audit. Source/config/protocol/context and raw cost/state traces
go in fresh archives. Preserve all previous outcomes/archives/failed attempts; any
scientific criterion change requires a versioned revised protocol before reevaluation.

Stop after this follow-up and focused fixes for parent review. No further dispatch,
push, publication, archive deletion or scope expansion. 12:00 UTC today is the review
target, not permission to interrupt an atomic write.
