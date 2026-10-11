# Outcome correction without double counting — preregistration v1

Freeze before evaluated execution. Zero teacher/model calls; keep seed, equations, thresholds,
fixed routes, migrations and historical verifiers/results unchanged. Extend the existing
correction transaction with fixture-specific eligibility/recomputation, not a second ledger.

## Admission, authority and replacement

New outcome-instrument-log-1 admits exact registered instrument LOG records, not objective
truth. A logged payload/output can be erroneous. A separate registered outcome reference
checks the proposed replacement of a specific event only. This policy does not weaken old
outcome verifiers. event_id is stable; evidence_id identifies a stored version. Sign is +1
when output equals payload, otherwise -1. One untouched unshielded success per scenario tests
branch isolation. o7 additionally retains a non-outcome maintenance annotation, ineligible
for outcome correction/scoring.

Trusted config/outcome_correction_authority.json uses the existing exact full-payload hash
and named authority permit policy. Sender must match fixture-curator AND an exact configured
permit; an assertion of authority is insufficient. o5 is unpermitted. Some invalid replacements
are deliberately permitted to separate authorization, eligibility and verification. This is
synthetic operation authorization, not production identity authentication.

Targets must be active ledger heads with exact expected digest and kind=outcome. Preserve
stable event_id, kind, scope, branch, procedure and payload; only output and provenance/version
change. Replacement schema/types and output must match the independent reference. No cross-
branch/scope movement. Reuse first-ID terminal ordering, including rejected IDs; identical
payload redelivery is a receipt-only no-op; conflicting ID reuse rejects. Stale target/digest
rejects without rebasing. Chains must target the latest head explicitly. Originals/ancestors
remain immutable and each root contributes exactly one effective sign.

## Equation, caches and uncertainty

For every branch, recompute ALL eligible active outcome heads using sum(signs)/(count+2)
and existing ±.2 decision thresholds. LMFT replays effective samples through unchanged
judgment.apply_validated into a derived branch; memory independently recounts the same signs.
Ledger/audit history is not erased. Store before/after branch scores, root/head supporting and
contradicting references, counts and reasons in correction/recomputation traces. Replacements
do not increment the independent event count. Fixed A=.25/B=.75/D=.5 routes remain unused;
propagation is not causal in this counter experiment.

Cache semantic probe results by case and effective branch evidence, never saved prose. Accepted
changes invalidate affected branch caches, including same-sign new provenance. Other-branch
caches remain. Pending outcome-consistency questions use a fixed declared criterion: nonempty
eligible evidence with only one sign. Mixed signs remain unresolved even if the score predicts
success/failure. Each case may ask once; correction may close/reopen that existing question
without refunding budget. A categorical prediction is not proof of consistency or certainty.
Rejecting corrections cannot alter effective evidence, counters, caches or questions; audits grow.

## Twelve independent scenarios

Each has the additional unchanged unshielded success. Listed counts/scores are shielded only.

| Case | Initial signs | Correction and intended result |
| --- | --- | --- |
| o1 | + | success→failure; +1/3→-1/3, category changes |
| o2 | - | failure→success; -1/3→+1/3, category changes |
| o3 | ++++ | first +→-; 2/3→1/3, still success but now mixed/unresolved |
| o4 | +++- | first +→-; 1/3→0, conflicting evidence remains, abstain |
| o5 | - | unauthorized -→+ rejects |
| o6 | - | authorized wrong output and Boolean output both reject verification |
| o7 | - | nonexistent, moved-branch and non-outcome targets reject eligibility |
| o8 | - | valid -→+, five exact plus five new-ID duplicate correction deliveries |
| o9 | - | valid -→+ then conflicting correction-ID reuse rejects |
| o10 | - | valid -→+, then inactive original target and active-head stale digest reject |
| o11 | - | -→+ then same-value reference attestation at new head; two ancestors, one root |
| o12 | -+ | first -→+; 0→1/2, consistency question closes; restart and fresh response |

Enabled expected 10 accepted and 9 rejected attempts; disabled 0/19. There are 31 independent
outcome events across 12 scenarios (19 shielded +12 unshielded), unchanged by corrections;
o7's annotation is one additional ledger root but is NOT an outcome event.

## Comparisons and fresh cases

Modes outcome-lmft, outcome-disabled, outcome-memory. Same messages/order/reference access;
disabled validates but never accepts. Later stale/chain rejection reasons may differ because
an earlier head was never installed. Memory shares authorization/ledger policy but uses
transparent independent arithmetic, not propagation. No extra model-assisted condition.

Before correction, evaluate warm payload20 twice and other-branch payload53 twice. Correct,
halt/restart with exact state check, then warm/repeat and two held-out payloads31/47. Fresh-case
branch labels are supplied fixture conditions; there is no learned context discovery. Outcomes
are evaluator-only: fresh-1 succeeds except o1; fresh-2 is the opposite. Thus one of two fresh
predictions is wrong whenever the same branch judgment decides both. Repair correctness is
independent of generalization, and coverage/accuracy must be reported separately.

Enabled expected 22/24 fresh decisions, 11 correct, 2 abstentions (o4). Disabled expected
22/24 decisions, 11 correct, 2 abstentions (o12). Equal aggregates conceal case-level changes;
report those. Do not claim prediction improvement or fuzzy advantage from successful repair.

## Checks, repetitions and stopping

Actual processes: 12 cases ×3 modes, plus uninterrupted o11/o12 in each mode (42 individuals).
Every primary run halts/restarts after correction and compares exact retained state, then
checks fresh responses/cache wording. Compare uninterrupted judgment/questions and semantic
outbox responses (ignore lifecycle timing) with restarted counterparts. Inspect diagnostics
only after halt; live interface is deliberate outbox/lifecycle.

o8 duplicates add no roots, ledger entries, corrections, recomputations, confidence or questions;
receipts/raw inbox storage can grow. Record before/after counts and bytes. Test atomic faults
before/after checkpoint replacement, rejection invariance, direction changes, both branch
isolation and scope constraints, stale targets, chains and exact arithmetic. Run regressions,
including historical correction compatibility. Snapshot source/config/protocol/messages/traces
before evaluation and preserve failed runs. No tuning after seeing outcomes. Stop after the
finite suite; no teacher work or next experiment implementation.
