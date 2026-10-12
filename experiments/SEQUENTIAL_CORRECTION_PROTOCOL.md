# Sequential correction and later contrary evidence - protocol v1

Frozen before evaluation, 2026-10-12. This standalone deterministic study extends
the action-aware v2 sequence, not its criteria or historical results. Starting HEAD
90c1b84a4092f5f82a76debbf2e637d7da092fe9; complete tracked-source prework and five
prior study output hash inventories are in outputs/sequential-correction-prework-001.

## Mechanism and scope

Reuse run_action_correction.prepare/request/receive/select and correction.correct.
Cases r1/c1 and r8/c9 preserve one known correct and one known wrong post-repair
prediction. Each starts with three registered instrument roots, an inconsistent
shielded question, existing historical counters and an exact permitted correction.
No preparation correction, new permits, weights, equations, seed or model changes.

After the authorized correction, deliver a separately identified instrument report
at shielded/check1 with value false, same case and batch-1, ID late/<case>/shielded/check1.
Its source is registered-instrument-log-1. These two exact authored reports form
a study-only registry extension: registration proves report identity, NOT truth.
Their distinct roots model independent observations; statistical independence and
real-world correctness are not established. Existing receiver reference remains
unchanged. No second truth store or learned hypothesis family is introduced.

Minimal opt-in production seam: correction.handle accepts an optional fixture for
instrument registration; default runtime behavior remains unchanged. The study
calls that existing handler with this frozen registry for late evidence only.
It cannot write ledger records directly. No live runtime mode is added.

## Conditions and identity

Full action circuit and equally equipped exact scalar memory each receive identical
inputs, offers, replies, admissions and one lifetime charged action request. For
each, run late-conflict, no-later-evidence and frozen-after-correction controls.
The frozen control receives the same late envelope but records withheld admission
in the experiment trace without calling the receiver. It is an explicit experiment
control, not a claim that runtime learning=false currently blocks evidence.

One episode persists through every stage. Recalling request must not reset/recharge
it. Replaying its reply is a no-op. A fresh transport ID with an identical evidence
ID is a retransmission, never another root. Conflicting reuse of that evidence ID
is rejected. A new correction operation ID requires its own existing exact permit;
no new operation is authorized by this protocol. Closed episode cannot repair the
later conflict. Read-only prediction/selection never admits evidence or sends requests.

## Stages, challenges and checkpoints

Persist pending action, accepted correction, late-evidence/control and final states.
Run uninterrupted and a chained restart trajectory: fresh child loads pending,
corrects and saves; a second fresh child loads corrected, admits/withholds late
evidence and saves; a third fresh child loads late state, probes and processes
replays/rejections. Compare semantic state at each boundary, excluding ONLY outbox
wall-clock timestamps; retain raw copies, PIDs and input digests. Hash and pin full
source/config/protocol context and input snapshots; reject changed restart inputs.

Challenges after the last restart: identical late-report retransmission (late
condition only), conflicting evidence identity, identical accepted correction under
fresh transport ID, unauthorized new correction ID, malformed correction envelope,
and original correction ID with altered payload. All must retain effective evidence,
heads, prediction, weights and original ledger bytes; rejection history may grow.
Separately exercise existing c10-a followed by permitted c10-b stale-target and
c10-c stale-digest operations through the unchanged receiver; neither may verify
or replace stale evidence. This companion is receiver validation, not extra action
budget or an additional action-policy success case.

## Frozen measurements and interpretation

Record stage effective heads/digest/root count, stored records, support part values,
resolved/inconsistent flags, prediction, correction lineage and rejection reasons.
Surviving hypotheses and validation-set acceptance are not applicable to this
counter-based predictor; do not invent them. Record requests, service proposals,
correction verifier executions, admitted reports/replacements, rejected corrections,
duplicate admissions, registration checks and preparation work separately. Receiver
challenge operations are separate from policy costs; no physical-cost cap claim.

Expected mechanical transitions: abstain -> success -> abstain with late conflict;
no-later/frozen remain success. These are testable expectations, not forced success.
Report decision coverage and accuracy separately by stage, across the two cases;
c9's success remains wrong. Freeze all predictions before fixture.actual_success
is called for scoring. False reports may reduce coverage; the study does not
establish that accepting the late report improves truth or that LMFT beats memory.

Required checks: exact memory action/score/prediction/ledger parity, actual chained
process restart parity, append-only originals, same-root accepted replacement,
one additional late root only, no replay inflation, nonmutating probes, unchanged
episode charge and protected source/config hashes. Preserve failed attempts, use
fresh study/context/pytest temp/XML paths every invocation, targeted and full actual
checkout regression. Version protocol changes before reevaluation. Stop for review.
