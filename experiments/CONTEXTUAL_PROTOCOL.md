# Context-dependent transmission — frozen protocol v1

Preregistered before implementation/evaluation. Historical comparative findings remain:
propagation changed diagnostics, not revision; no fuzzy advantage was demonstrated.
This study uses ordinary lookup on one authored observable feature, not feature discovery.
The owner request authorizes conditional records, clarification and deduplication.
New fixture conventions below do not change seed, protected rules or existing equations.

## Fixture and frozen data

Procedure `transmit-1` copies an integer payload in [0,9]. Feature `shielded` is Boolean.
With disturbance 0, transmission succeeds in either condition; with disturbance 1 it
succeeds only when shielded; with disturbance 2 it fails in either condition. Failure
returns (payload+1)%10. Validate registered trials by executing this procedure and
comparing output to payload. These are synthetic observed outcomes, not teacher truth.

Initial evidence in order (ID: payload, shielded, disturbance):
s1: 0,true,0; s2: 1,true,1; s3: 2,true,0; s4: 3,true,2;
u1: 4,false,1; u2: 5,false,2; u3: 6,false,1; u4: 7,false,0.
Both conditions contain successes and failures. Contrary sequence:
c1: 4,true,2; c2: 5,true,2; c3: 6,true,2; c4: 7,true,2.
All records contain evidence ID, procedure, payload, shielded, disturbance and output.
Initial score 0; reuse sum(signs)/(n+2), success +1/failure -1, support >=.2,
oppose <=-.2, otherwise abstain. No learned confidence probability is introduced.

LMFT stores two separate judgments with evidence/reasons and chooses exactly the
known-condition branch. The conditional-memory baseline independently recounts the
same branch evidence. Aggregate memory uses all outcomes and ignores the available
feature for counting, but gets the same cases and answers. All share scope and
missing-input policy. References to existing Fact/Execution/Confidence are descriptive
metadata; no nodes, edges, weights or propagation coupling are added. No propagation
ablation is useful here because propagation does not participate.

## Evaluation cases and clarification

Known held-out cases (ID: payload, shielded, disturbance; disturbance is evaluator-only):
h1: 8,true,0; h2: 9,true,1; h3: 8,true,2;
h4: 8,false,1; h5: 9,false,2; h6: 8,false,0.
Missing-condition cases m1: 9,true,0 and m2: 9,false,1 initially omit shielded.
Scope exclusions: x1 has procedure other-1; x2 has payload 10.
None is admitted as training evidence. A query supplies case_id, procedure, payload,
and shielded true/false/null. No runtime auto-completion from the fixture registry:
null always withholds evaluation and emits one question per pending case.

A linked condition reply supplies evidence_id `condition/<case_id>`, case_id, shielded.
It must match the immutable registered case and the open question. Record attribution,
input and resolution reference. Irrelevant case, wrong value, malformed Boolean, or
unknown question leaves the question pending and changes no learned judgment.
Only validated replies resolve missing information; they are not outcome evidence.

Probe is read-only. With known condition, support predicts success, oppose predicts
failure, uncertainty withholds. Missing condition withholds even in aggregate mode;
scope exclusions never request clarification. Before evidence all conditions abstain.
After initial evidence: conditional scores +1/3 and -1/3, aggregate 0. Expect LMFT
and conditional memory 4/6 correct known decisions, coverage 6/6; aggregate coverage
0/6. Missing cases: 0/2 decisions before answers, conditional 2/2 correct afterward;
aggregate remains undetermined. Report abstention separately, never as correctness.
After contrary sequence, shielded score 1/7,0,-1/9,-1/5; unshielded stays -1/3;
aggregate becomes -2/7. Both conditional branches then oppose, known accuracy 3/6.
These small-case results do not establish broad generalization.

## Fixed run and comparisons

Run aggregate, conditional memory and LMFT with identical messages, features and
teacher contributions; deterministic mode makes zero model calls in every condition.
1. Record initial held-out probes after halt.
2. Supply s1..s4,u1..u4 and evaluate known/scope cases through inbox/outbox.
3. Submit missing m1 and m2; halt with both requests pending. Restart the actual
   process; verify retained judgments, evidence/reasons and pending references.
4. Deliver one irrelevant and one malformed linked reply to m1. Neither resolves it.
   Idle for 0.3 seconds; no calls or repeat requests. Deliver valid answers for both.
5. Repeat s1 under five new message IDs and deliver the original s1 message five times;
   finish with an explicit barrier. Same outcome text for distinct s1/s2 must count both.
   Conflicting reuse of s1 ID is rejected, never overwritten. No repeat may increase
   evidence, revisions, model calls or large diagnostics; lightweight receipts remain.
6. Query h1 twice before and once after c1..c4 to exercise versioned evaluation caching.
   A stale pre-contrary result must not be replayed. Record final held-out probes.
Compare restarted LMFT with an uninterrupted execution of the same messages. Add a
learning-disabled control. Stop after this sequence, max 420 seconds per wait.

## Identity, costs, acceptance and recovery

Message ID identifies a delivery; evidence ID plus canonical complete payload identifies
an event. Identical text is irrelevant to identity. A conflicting payload under an
existing evidence ID is rejected. Outcome duplicates never teach again, even after
state changes; they do not replay a saved score. Evaluation cache keys include complete
available case, judgment revision version, mode, policy and resolved-condition evidence.
Changed context is evaluated anew. Cache hits retain a delivery and selected outbox
response but no new model trace. Pending questions are keyed by case, not message ID.
Rejected input is retained compactly; no broad consolidation or autonomous loop.

Require correct frozen score sequences, independent conditional-baseline equivalence,
correct retrieval of supporting/contrary source evidence, no unsupported missing-case
decision, invalid replies pending, exact restart/uninterrupted state equivalence
(excluding timing/lifecycle), preserved seed and post-halt-only diagnostic boundary.
Tests include interrupted writes, evidence conflicts, duplicate context, stale-cache
invalidation, new events with identical wording and faithful-renderer rejection.
Measure known/missing accuracy and coverage, clarification resolution/usefulness,
retrieval correctness, core/wall time, calls, receipts/revisions/diagnostics/outbox counts,
checkpoint and individual-directory bytes; compare repetition deltas. Timings descriptive.
Archive source/config/protocol before each evaluated run; preserve failed runs.

## Separate actual offline wording smoke

After deterministic checks, run local Qwen/llama.cpp with the existing pinned settings.
Train eight outcomes without LLM calls; evaluate h1, missing m1, then a valid linked
answer; retransmit old evidence under new IDs; re-evaluate unchanged h1; apply contrary
sequence and evaluate h1 again. Four new evaluation/clarification contexts permit at
most four model calls; repeated context/evidence and idle periods permit none.
The model selects between two complete faithful renderings generated from accepted
facts, via a JSON enum grammar. Independently validate exact membership before using
text; on failure retain diagnostic and use explicit authored fallback. This is
constrained formulation, not a claim of general free-form semantic faithfulness.
Verify actual calls, same server reuse, wording/uncertainty/evidence alignment, cache
behavior and costs. No comparative model-assisted superiority claim is made.
