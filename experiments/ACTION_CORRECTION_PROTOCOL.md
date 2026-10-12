# Action-aware missing evidence versus verified correction — protocol v1

Frozen before evaluation. One bounded standalone experiment, no runtime registration,
production edits, protected seed/numerical changes, model calls or fresh learning.
Reuse correction.correct, configured existing authority permits and coordinate verifier;
reuse consistent_attention support/predict/circuit ranking. Ordinary memory receives
the same information, action policy, budget and correction machinery; its ranking
uses the exact existing two-pass scalar reduction, not a weaker memory heuristic.

## New external action policy

For each declared relevant unresolved question, offer gather ONLY for missing parts
with an available scoped observation service. For an inconsistent question, offer
correction ONLY for advertised existing permitted operations targeting an active
head with exact digest and unchanged scoped coordinate, unused correction ID and
matching authority/permit metadata. Resolved/irrelevant questions get no action.
Missing and inconsistent are separate properties; both actions can coexist.
Metadata declares a possible operation, not replacement truth or guaranteed repair.
Never read replacement value or outcome before selection. Receiver authorization,
eligibility and independent replacement verification remain decisive after request.

Rank eligible actions by unchanged question circuit score, positive-score gate,
then lexicographic action ID. Only action availability/eligibility filtering is new.
No new learned policy or node meaning is claimed. Correction preflight reads policy
metadata, target identities/digests and scope only; the full payload is checked again
by the unchanged correction receiver. One shared request per scenario, including
rejected replies. No retry, fallback, refund or automatic reset. Persist pending
request before reply and verify exact reload before processing it.

Conditions: action-aware full circuit; equally equipped exact scalar memory;
action-aware existing Clarity-edge ablation; gather-only full-circuit control.
Scalar score clamp(.25*(w+.3125-coverage-resolved+inconsistent),0,1), ablation removes
only inconsistent. Existing weights A=.25/B=.75/D=.5 and historical eight-outcome
counter replay +/-1/3 remain frozen. All conditions use identical authored inputs.
No corrections to outcome counters, source/config policy or founding inventory.

## Cases and fixed expectations

Reuse correction_fixture public cases and admitted instrument records (which are
not guaranteed truth). Preparation c4-a and c10-a are existing verified corrections,
applied identically BEFORE action-budget evaluation and counted separately. r9
omits payload admission to create competing missing/conflicted questions. Gather
service supplies authored scoped missing parts=true, with exact receiver matching;
it never supersedes roots. Public offers exclude all replacement values. Rejected
offers appear in selection traces; no trusted policy is rewritten to admit them.

| Scenario | Existing case / preparation | Offered action | Full / scalar / ablated / gather-only | Final enabled decision |
| --- | --- | --- | --- | --- |
| r1 | c1 conflict | c1-a correction | correction / correction / correction / none | success |
| r2 | c4, prepared c4-a | missing check2 gather | gather in all | success |
| r3 | c5 conflict | unpermitted c5-a | none in all | abstain |
| r4 | c6 conflict | permitted wrong-value c6-a | correction / correction / correction / none | abstain, verification rejected |
| r5 | c7 conflict | permitted wrong-scope c7-a | none in all | abstain |
| r6 | c10, prepared c10-a | inactive-target c10-b | none in all | success |
| r7 | c12 resolved | irrelevant color c12-a | none in all | success |
| r8 | c9 conflict | valid c9-a | correction / correction / correction / none | success, incorrect |
| r9 | c1, payload absent | c1-a and payload gather | correction / correction / gather / gather | abstain |
| r10 | c3 resolved | c3-a | none in all | success, incorrect |
| r11 | c4, prepared c4-a | unavailable gather | none in all | abstain |
| r12 | c4, no preparation | missing check2 gather | gather in all | abstain, new conflict |

Truth uses unchanged fixture.actual_success for each case ONLY after all48 final
predictions freeze. Full/scalar/ablated:6requests,6decisions/4correct,50% coverage,
2/3 accuracy,4 newly resolved questions. Full/scalar3accepted/1rejected action
corrections; ablated2accepted/1rejected. Gather-only3requests,4decisions/3correct,
1/3 coverage,3/4 accuracy,2 newly resolved questions. Twelve scenarios, two relevant
questions each. Newly resolved means false-to-true complete consistent support,
not correctness. Record part-coverage gain separately. r12 adds coverage but exposes
inconsistency; r9 exposes action ranking differences without final-decision benefit.

## Integrity and stopping rule

Required: exact circuit/scalar scores/actions; existing single-edge ablation only;
selection oracle isolation and state purity; original-record immutability; correction
lineage/same-root replacement; gather new roots only at requested missing coordinates;
separate authorization/eligibility/verification traces; rejected replies preserve
effective support/cache/questions; duplicate replies no additional semantic effect;
stale digest/scope/target, spoofed sender and budget tests; pending actual-process
restart parity with uninterrupted execution; fixed weights/counters/birth; complete
nonempty current source context and prework protected hashes unchanged.

Archive frozen input/order/prior/pending snapshots, exact permits, selected replies,
full traces, final ledgers, prediction freeze, metrics, PID/source/config/context
hashes and any failures to fresh output roots. Full regression uses unique basetemp
and XML paths, never reused. Preserve historical archives and existing dirty work.
Standalone harness output is not real-runtime transport, a physical computation cap,
general authentication, repair of all conflicting roots or evidence of fuzzy superiority.
Stop after this experiment and review; no step2, demo or further work.
