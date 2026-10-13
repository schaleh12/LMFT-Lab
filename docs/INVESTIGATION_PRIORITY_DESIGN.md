# Investigation priority: design review of existing evidence

2026-10-13. Design only; no new execution, simulation, learning rule or runtime
integration. Read the actual x1-x3 and r9 archived traces and current policy.
**Recommendation: do not implement a learned priority study yet.** There is a
specific structural limitation left by eligibility, but the existing evidence does
not supply a context-dependent utility target that requires learning.

## What the existing cases establish

Sources: [seed contribution report](../experiments/SEED_CONTRIBUTION_RESULTS.md),
`outputs/seed-contribution-003/results.json` and frozen inputs;
[action correction report](../experiments/ACTION_CORRECTION_RESULTS.md),
`outputs/action-correction-002/results.json` and `frozen-inputs.json`.

| Case | Archived choice and consequence | What current eligibility would settle |
| --- | --- | --- |
| x1 | Intact gathers shield evidence despite complete contradictory support; no resolution or coverage gain. Ablation resolves missing payload. Both abstain finally. | A missing-parts-only gather offer for shield has no missing parts and is rejected. Learning to reject it would duplicate the gate. |
| x2 | Shield check1 already contains both values; check2 is missing. Intact gathers shield: coverage +0.5, no resolution. Ablation resolves payload: coverage +1. Both abstain finally. | **Not settled:** gathering exactly missing check2 still passes. It cannot remove the contradiction in check1. A structural feasibility rule can recognize this without learned context. |
| x3 | Intact gathers contradictory payload; no resolution or coverage gain. Ablation resolves missing shield. Both abstain finally. | Complete contradictory payload has no missing parts; the gather gate rejects it. |
| r9 | Full/memory chooses permitted shield correction; ablation/gather-only chooses payload gathering. Each resolves one question with one request; both final decisions abstain. | Both offers are legitimately eligible. Permission alone cannot prefer either, and this trace gives neither a resolution-count nor final-decision advantage. |

The x rows are observations under the OLD question selector. They contain no
action-offer/permit interface. The right column is a code-inspection inference
assuming equivalent available scoped gather offers, **not a rerun of x1-x3 through
the current adapter**. No automatic cross-case correction service is assumed.

r9 is also a tie-breaking example: full/memory scores both eligible actions
0.265625, then chooses `correct-c1-a` by action ID. Ablation scores correction
0.015625 versus gather 0.265625. Correction adds zero part coverage; gathering adds
one. Neither coverage nor the existing Clarity contribution measures expected
decision utility. The unchanged original selector gathers shield and resolves zero.

## Narrow candidate contract, conditional on the owner's objective

Keep five quantities separate:

1. **Eligibility:** existing scope, availability, exact-target and permit checks
   remain binding. A priority estimate cannot authorize evidence or a correction.
2. **Attainable information benefit:** distinguish part coverage, complete consistent
   question resolution, and enabling a final decision. For append-only gathering,
   an existing within-part contradiction makes one-step resolution impossible.
   Other eligible actions are only *potentially* resolving; missing replies and
   rejected corrections can still prevent it. Do not label that potential a probability.
3. **Cost:** current evidence gives logical requests, service attempts and receiver
   checks, not a calibrated latency/CPU/money cost. Preserve the lifetime budget.
4. **Error risk:** verified support is not guaranteed world truth. r4's permitted
   repair fails verification; r8's accepted repair enables a wrong decision. A
   resolution reward alone must never be reported as improved correctness.
5. **Abstention:** retain the final support gate and allow spending no request.
   Whether partial resolution is worth a request when final abstention is inevitable
   is a task objective, not something the seed's node names decide.

If useful subquestion resolution is the agreed objective, the smallest next
implementation would be an experiment-local feasibility annotation and direct
ranking rule over already eligible actions. Demote structurally impossible
one-step resolution before any speculative learned preference; keep explicit stable
ties and an abstain option. x2 is a concrete regression target. This is a proposed
authored policy, not learned knowledge, and is not approved or implemented here.
If the objective is only enabling an immediate final decision, x1-x3 and r9 do
not justify spending either request: the other unresolved question remains. A
cost-sensitive no-action baseline is then essential. Longer-horizon information
value would require an explicit later-use task absent from these traces.

## Where context learning could matter, and what is missing

After structural filtering, two permitted, potentially useful actions could differ
in observed success or cost across contexts. Prior verified episodes could then
change which action is worth its cost. That would be nonredundant with permission.
These archives do not contain such comparable context-conditioned service histories
or a chosen benefit/cost objective. The accepted applicability study learns how to
interpret evidence; it does not establish investigation utility or action reliability.
Do not invent services, rewards, seed weights or a synthetic success reversal merely
to manufacture a positive learning result.

An eventual preregistration must define public pre-action context and action
metadata; record the choice and budget before calling any service; then record the
receiver's verification result, support transition and work counts. Independent
task outcomes, where legitimately observable, arrive after prediction freeze and
are scored separately. Never read the selected future reply, unselected reply,
held-out outcome or scenario ID as a selection label. Selection-only feedback is
biased; unchosen action success is unknown unless an independently authorized
evaluation design supplies it. Evaluation counterfactuals must stay outside training.

## Hooks, controls and authority

[action_policy.preflight/select/request/receive](../src/lmft_lab/action_policy.py)
already separates eligibility, ranking, the charged pending request and admission.
[consistent_attention.support/predict](../src/lmft_lab/consistent_attention.py)
provides inspectable support and final abstention. The archived harness's
`finish` records before/after resolution and work; its evaluation freezes predictions
before outcome scoring. These are sufficient inspection hooks; no new runtime
state or model service is needed for the proposed structural diagnostic.

The competent baseline is an ordinary controller with the same eligibility,
feasibility, history, information and budget, direct ranking and no-action option.
If learning is later justified, independent structured memory must learn from the
same feedback and persist across restart. Compare a frozen pre-learning policy too.
Existing scalar memory only proves equivalence to the present circuit; it is not
a stronger utility baseline. The existing Clarity-edge ablation removes one edge,
not propagation as a whole. A meaningful propagation-disabled comparator must
retain the full eligibility/learning/support pipeline and make its direct choice
from the same utility evidence; simply zeroing execution activation and disabling
all action would create an artificially weak control.

The founding geometry, protection/revision rules, receiver authority and numerical
mechanisms stay unchanged. Eligibility and any objective/feasibility rule are
authored. Future estimates learned from admissible feedback would be separately
versioned, inspectable, revisable developmental state. Propagation would at most
propose a priority among permitted actions; it would not override authorization,
budget, verification or support abstention. No literal philosophical arrows or
arbitrary new seed weights follow from this design.

A positive structural test would establish a better authored selector on its
specified objective, not learning or seed advantage. Future learning could show
useful remembered feedback only against frozen and competent memory controls;
parity would support the mechanism without tree superiority. No benefit over the
structural baseline, loss of calibration/retention, or extra errors would be valid
negative findings. Do not retune the objective after seeing outcomes.

## Decision needed before implementation

**When one permitted check cannot enable a final decision, should LMFT spend it
to resolve a useful subquestion, or preserve its budget and abstain?** x2 and r9
make that choice concrete. If partial resolution matters, define its later use;
if only immediate correct decisions matter, the abstain baseline is the next
starting point. No nonredundant learned-utility test is presently justified by
these archives. Stop for parent/owner review; no experiment is dispatched.
