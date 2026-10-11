# Scoped verified support — results

Recorded 2026-10-11. [Protocol](SCOPED_ATTENTION_PROTOCOL.md),
[setup and implementation](../docs/SCOPED_ATTENTION.md).
Earlier [attention results](ATTENTION_RESULTS.md) and raw archives remain unchanged.

## Finding and counterexample

**Fact and Confidence each causally affected request suppression in the preregistered
fixture; ordinary memory matched the full pathway. A separate post-hoc counterexample
shows the conceptual mapping can incorrectly suppress a genuinely unresolved question.**
The result supports a narrow authored circuit effect, not a generally reliable evidence
policy or a fuzzy-tree advantage. No mappings were tuned after evaluation.

Primary archive `outputs/scoped-attention-001/`: **232/232 checks passed; 240/240 tests
passed** (223 earlier tests plus 17 new parameterized cases). Thirty-five primary
individuals (seven cases x five conditions), five restarted sequential individuals and
one uninterrupted comparison used actual runner processes. All halted. All conditions
made zero model calls or mock-inference calls. No evaluated run failed; the post-hoc
policy counterexample below is a substantive negative result, separately preserved.

Before evaluation, a unit test exposed an arithmetic oversight in predicted q1 behavior
when both influences are removed: scores tie and the existing ID tie-break selects the
already-resolved question. The protocol records this correction. Cases, mappings,
selection rules and acceptance requirements were not changed to fit evaluated results.

## What changed and what caused behavior

New opt-in scoped modes store exact synthetic observations with case/scope/question/part
identity and attribution. Shielded requires two distinct checks with consistent Boolean
values; payload validity requires one. Repeated records do not add independent checks.
Opposing eligible evidence remains present and unresolved; no overwrite or majority rule.
Different-case/old-scope observations are retained but not applicable. A confident teacher
assertion supplies no verified evidence. This ordinary evidence bookkeeping determines
resolution and the protected prediction eligibility gate; seed activation does not.

Previous route weights A=.25/B=.75/D=.5 are explicit fixed starting assumptions; no new
route learning occurs. Both questions use B. Eight existing contextual prior outcomes
recreate scores +1/3,-1/3 through the unchanged judgment update. Each primary case starts
independently, so evidence/budgets never leak between cases.

The existing attention pathway is extended by one separate Fact -> Clarity inhibitory
association. Applicable nonconflicting part coverage supplies Fact; full scoped sufficiency
supplies direct Confidence. The full propagated final Clarity is the sole conceptual
ranking signal, with positive-score eligibility and a shared one-request budget. Those
external rules are explicitly traced. There is no external resolved-question gate in
conceptual selection. Ordinary memory instead uses that gate explicitly.

A fully resolved question has full priority 0, versus .015625 with either single
influence disabled and .265625 with both disabled. Disabling Fact removes only its two
outgoing edges; disabling Confidence removes only its outgoing edge. Evidence, direct
inputs, other edges, weights and budgets are unchanged. Exact edge-isolation tests pass.
Either single inhibition can still rank an unresolved question above a resolved one,
but neither alone completely suppresses the residual positive score on q4/q7. Both
are necessary for zero requests there under this authored mapping and threshold. This
is numerical complementarity, not a universal claim that these concepts are necessary.

## Primary results: resolution and prediction kept separate

| Condition | Requests | Redundant | Appropriate unresolved | Fully resolved cases | Correct / predictions | Abstentions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Full pathway | 5 | 0 | 5 | 6/7 | 4/6 | 1 |
| Fact outgoing disabled | 7 | 2 | 5 | 6/7 | 4/6 | 1 |
| Confidence outgoing disabled | 7 | 2 | 5 | 6/7 | 4/6 | 1 |
| Both disabled | 7 | 3 | 4 | 5/7 | 3/5 | 2 |
| Ordinary memory | 5 | 0 | 5 | 6/7 | 4/6 | 1 |

Full and memory save two calls versus both-disabled, with identical results. Single
ablations spend two extra calls but have exactly the same final prediction accuracy and
coverage as full. Saving these calls does not improve prediction quality. Full/memory
accuracy is 4/6 (66.7%) among decisions, coverage 6/7 (85.7%). Both-disabled is 3/5 (60%)
with coverage 5/7 (71.4%); the decision subsets differ. Never count abstention as correct.

q1: full/single ablations/memory investigate unknown payload validity, while both-disabled
wastes its request rechecking shielded and misses the unresolved opportunity. q2: partial
verification is insufficient until its second check arrives. q3: confident prose does not
prevent verification. q4: duplicate evidence does not change support. q5: other-case/old-
scope evidence does not resolve current shielded. q6: an eligible contradiction prompts
reconsideration, but another agreeing reply cannot erase it; prediction remains withheld.
q7: full/memory make no request for fully resolved evidence. q2/q4 are deliberately wrong
predictions despite complete uncertainty resolution. The earlier 2/4 attention result is
not replaced or directly comparable to these new cases.

Literal inappropriate suppression (no request despite unresolved relevant information) is
zero in the seven primary cases for all modes. Both-disabled nevertheless misses one
unresolved opportunity by spending its budget on a resolved question; this is counted
separately. Seven authored cases do not establish population-level generalization.

## Reopening, persistence and repetition

Sequential q6 first contains consistent evidence, then receives an additional eligible
opposing record after an actual halt/restart. Full/memory preserve their unused budget,
then reopen and request shielded verification. Single/both ablations already spent their
one request redundantly before the contradiction, so they correctly enforce the spent
budget afterward. Their evidence policy still becomes unresolved; they cannot issue a
second request. Every condition retains the contradiction and abstains at the end.

Restart preserves exact full state before new input. Restarted full and uninterrupted
full have identical scientific state and question references. Five reattributed evidence
messages plus five exact redeliveries add no evidence, changes, traces or requests.
Including the explicit barrier, each repeat stage adds 11 receipts, 6 processed IDs and
one acknowledgment; checkpoint growth is approximately 2,630 bytes, plus retained inbox
files. No consolidation or autonomous loop was introduced.

Tests cover scope isolation, partial support, assertions/type rejection, duplicate and
conflicting IDs, outgoing-edge isolation, one-request budgets, invalid selected replies,
reopening, persistence, hidden-truth isolation and failures before/after atomic replacement.
During execution only deliberate outbox/lifecycle data is read; inspection is refused
while running. Original seed, activation/propagation equations, migration, judgment,
contextual, storage and prior attention files match the previous archive byte-for-byte.

## Post-hoc negative diagnostic — outside the preregistered score

After the primary run, audit the existing q6 registered observations with only check1=false
and check2=true (plus known valid payload). Each individual check is internally consistent,
but the checks disagree with each other. Ordinary bookkeeping correctly reports unresolved.
Fact nevertheless becomes 1 from complete per-part coverage, while direct Confidence is 0.
Fact -> Clarity and Fact -> Confidence -> Clarity together suppress priority to zero.
**Full propagation makes no request; ordinary memory selects shielded. This is inappropriate
suppression.** No new hidden truth or invented eligible observation is needed for the audit.

Preserved separately in `outputs/scoped-attention-001/posthoc-cross-part.json`, with exact
reproduction source and SHA256 under `posthoc-source/`. This is a static selector/policy
audit, not a new process-based primary trial, and is not included in the 232 checks.
No repair was folded into the evaluated source. The frozen mapping remains limited to
this research fixture and should not be treated as a generally correct investigation gate.
The finding limits the apparent primary success and gives ordinary memory an advantage
on this counterexample. It also distinguishes within-part contradictions (tested in q6)
from between-part disagreement (missing from the primary preregistration).

## Descriptive costs

Totals across seven primary individuals per condition. Wall time includes startup,
file exchange and halt; core time excludes checkpoint serialization/commit. Sizes exclude
separately retained snapshots and source archives. These are single-run descriptive values.

| Condition | Wall s | Core ms | Checkpoint bytes total | Individual bytes total |
| --- | ---: | ---: | ---: | ---: |
| Full pathway | 4.193 | 67.59 | 584,406 | 622,685 |
| Fact outgoing disabled | 4.515 | 69.82 | 585,425 | 625,053 |
| Confidence outgoing disabled | 4.329 | 70.12 | 587,820 | 627,448 |
| Both disabled | 4.355 | 68.37 | 583,834 | 623,630 |
| Ordinary memory | 4.094 | 54.52 | 326,823 | 365,106 |

Full propagation retains larger traces for the same primary behavior as memory. Sequential
runs additionally cost about 1.7 seconds each. There is no statistical speed claim.
Full-history checkpoint write/copy costs remain; no large-system durability is claimed.

## Preservation and smallest next experiment

The original primary archive freezes source, tests, model configuration, experiment
configuration, protocol, hashes, all inboxes/checkpoints, halted snapshots and traces.
Protocol SHA256: `d695a63d5ee8a1a2b5171fe4139aa577b0b49e86db5140795ff0707415ee2bf1`.
Raw outputs and the separate audit archive remain ignored by Git; back them up separately.
The tracked protocol/report preserve selected results. Prior individuals require their
archived software under the unchanged source-manifest restart rule; no migration occurred.

Limitations: ideal registered verifier, authored relevance/parts/edges, fixed weights,
uncalibrated activations, narrow prediction scope, seven cases and the documented improper
suppression counterexample. No general evidence grounding, autonomous contemplation,
semantic understanding or fuzzy superiority was established.

**Smallest next experiment:** preregister cross-part disagreement alongside within-part
conflict and coherent partial support, then test a revised consistent-support mapping
against the frozen mapping and ordinary memory. Require unresolved conflict never to be
silently suppressed. Preserve this counterexample and explicitly attribute any external
safety gate rather than crediting it to propagation. Do not add route learning or a loop.
