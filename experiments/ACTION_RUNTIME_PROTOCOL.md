# Supervised fixed-command action adapter - protocol v1

Frozen 2026-10-12 before evaluation. Starting HEAD90c1b84; existing dirty work and
25,975 prior output-file hashes preserved in outputs/action-runtime-prework-001.
This is synthetic supervised interaction, not freeform chat or autonomous agency.

## Reuse and interface

Extract existing action-policy functions into a shared source module, preserving
experiment imports/default semantics. Extract the strict late-report registry into
a shared source module. Keep correction.correct, equations, seed40, authority
permits and model settings unchanged. New opt-in action-command-lmft/memory modes
use existing runtime.advance, Store, inbox/outbox, receipts and atomic checkpoints.
Fixture mode only; no model/mock completion calls. Existing modes retain defaults.

Fixed commands in content.text: initialize r1 / initialize r8 / initialize r2,
inspect, request, reply, evidence, barrier. No arbitrary text interpretation.
Commands have exact content keys; replies/evidence add record. Fixed input bounds
and short rejection strings apply; existing envelope/inbox byte limits remain.
Initialization is one explicit synthetic setup, reusing prepare: three cases with
the same registered initial evidence, historical counter replay and (r2 only)
existing preparation correction. Store its complete setup receipts/provenance;
do not represent authored history as new autonomous learning. No second truth store.

initialize/request require fixture-operator / action-command-1. Replies/evidence
require fixture-curator / registered-instrument-log-1 plus exact registered data,
scope and correlation. These are synthetic local capabilities, not authentication.
Text or source labels alone never verify arbitrary claims. Inspect/barrier return
only deliberate fixed JSON summaries and cannot modify judgment or action budget.
Transport receipts/outbox metadata may grow; internal inspection remains halt-only.
Learning-disabled refuses setup/admission/request; inspect/barrier remain available.

One episode per individual, one lifetime charged policy request, no reset/refund.
`request` applies the unchanged action selector; it may request correction (r1/r8)
or eligible missing-part gathering (r2). Persist request outbox ID, episode ID,
selected operation ID, charge and selection trace atomically. Reply is teacher_reply
transport only, with matching reply_to and exact record keys episode_id/request_id/
operation_id/payload. Strict real Boolean schemas precede substantive verification.
Unrelated/malformed envelopes are rejected without closing a pending request;
well-formed correlated operations reaching the existing receiver retain its closure
semantics even when rejected. Repeated request never resets or issues another.
Identical reply under fresh transport ID is a no-op; different late reply is rejected.

Late `evidence` is allowed only after the request closes, for the initialized c1/c9
case and exact existing two-entry registry. New identity means a new registered
root; repeated identity is retransmission. Conflicting reuse and integer0/1 reject.
Read-only inspect returns current support/prediction AND historical request closure
separately; later conflict must not falsely reopen/recharge the old request.

## Frozen evaluation

Cases r1/c1, r8/c9 and r2/c4, both circuit/scalar selectors, uninterrupted/restarted
runtime individuals = twelve individuals. Start empty; explicit initialize, inspect,
request, pending checkpoint restart (restarted arm), malformed/uncorrelated inputs,
valid reply, inspect, late evidence for r1/r8, inspect, second restart, replay and
identity-conflict challenges, inspect, halt. Actual restart must preserve complete
checkpoint state before further messages. Compare full semantic final state after
excluding only outbox timestamps and receipt processing durations. Retain both raw
states, process identities, lifecycle, input/outbox/receipt/checkpoint traces.

Compare equivalent standalone prepare/request/receive/late-admission inputs using
the shared mechanism: same effective records/heads, branch counters, weights,
selected actions, support, predictions and costs. Circuit/memory share evidence,
capabilities, interface and budget; score/action equality required. No-later controls
are the already frozen standalone results and before-late live probes; do not infer
a novel frozen-runtime control. Initial all abstain; after reply all predict success.
c9 remains wrong. After late evidence c1/c9 abstain, r2 stays success. Freeze all
predictions before scoring unchanged fixture outcomes; report coverage and accuracy
separately, not improvement from abstention. No surviving-hypothesis or validation-set
claim applies to this predictor.

Rejections: unknown text, wrong sender/source, nonmatching episode/request/operation,
wrong envelope reply_to, malformed record, integer Boolean alias, unrelated late
scope/case, conflicting evidence/message identity, stale/closed operation. Test
valid-but-unverified correlated correction separately since closure consumes the
one opportunity. Test live inspection denial, read-only probe, duplicate no-op,
learning-disabled, option/mode and manifest mismatch without checkpoint changes.

Real child-process interrupted commits use existing Store fault injection before
and after replace on a queued valid reply, then resume with the actual runtime.
Before-replace leaves the pending checkpoint; after-replace retains the accepted
reply; recovery must have exactly one committed admission/charge. Preserve partial
files and negative physical-work result: pre-commit retry can repeat verification;
do not claim physical work cap, crash-proof external side effects or power-loss safety.

## Measurement, preservation and stop

Record policy requests, returned reply kind, admitted gather/replacement/late records,
correction verifier calls (action versus setup), gather checks, registry checks,
duplicate admissions, rejection receipts, stage roots/stored records, support and
prediction. Physical fault verification markers are separate from logical counters.
Historical setup outcomes/admissions remain separate from action costs. Whole-history
checkpoint/inbox/outbox growth is not bounded by the one-request limit.

Pinned source/config/protocol snapshots and fresh output/temp/JUnit paths each run;
preserve failures. Targeted and full actual-checkout regressions, historical audit,
prior-output hash checks. New source-wide manifest rejects old checkpoints; retain
archived source/config, no silent migration. Protocol changes before reevaluation.
No teacher, model calls, new nodes, major dependencies, demo polish or next task.
Update handoff and stop for coordinator review.
