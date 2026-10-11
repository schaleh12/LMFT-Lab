# Local foundational teacher — preregistration v1

Frozen before any actual teaching call or evaluated run. One profile:
foundational-teacher v1 in config/teacher_profiles/foundational-teacher-v1.json.
One existing route A/B/D may be set to .25, .5 or .75, with at least two exact
registered training IDs for that route, a reason and uncertainty. No other edit.
Full profile/schema, model config and source are archived before execution.

## Architecture and independent acceptance

Use the original attention selector and propagation equations with initial A=B=D=.5,
and the unchanged eight contextual outcome priors. The recent correction ledger is
not extended. Ordinary memory uses the original attention-memory priority rule.
Teacher state and dispositions are separate from existing experience updates.
Four off-policy calibration records (train-A1/A2 unavailable, train-B1/B2 available)
are supplied as registered evidence, not online selected-resolution rewards. They
therefore do not trigger the existing experience-based update; that mechanism remains
unchanged and available in its original modes. No teacher assertion is admitted as Fact.

LMFT deliberately asks for one route lesson after retaining all four calibration records.
The outbox question supplies those records, weights and supported judgment summaries,
plus the frozen profile's capability description. No validation answers, held-out values,
fixture tables, internal diagnostics or complete checkpoint go to the teacher adapter.
The adapter reads only the outbox. It writes an attributed linked reply through the inbox.
Prompt guidance is not enforcement: exact schema, profile/config/request linkage and
registered evidence are checked in code. Prose is retained but not executed or scored.

Acceptance requires two distinct matching evidence IDs for the proposed route, both
supporting its direction (available -> increase; unavailable -> decrease), and strict
improvement in relevant resolved investigations on fixed validation v1/v2 without more
irrelevant requests. Each validation has conflicting reports, routes A unavailable and B
available. It tests route utility, not outcome accuracy. Unchanged/no-improvement edits
reject. Developmental changes need learning enabled; all attempts retain disposition,
before/after, validation, evidence and model attribution. No change to seed or equations.

## Calls, retry and profile policy

Teacher: official Qwen3-8B-GGUF Q4_K_M, exact revision/checksum in teacher_models.json,
Apache-2.0, existing llama.cpp b11429 backend. 8192 context, 1024 output tokens,
temperature 0, seed 42, non-thinking, 120-second backend timeout. No small-model calls.
Provision first, then call offline. One successful exchange maximum, one inference per
explicit adapter command; at most two attempts, with --retry required after failure.
No retry after a completed reply; schema/acceptance rejection is a negative result.
Interrupted attempt counts toward the budget. Never synthesize a successful reply.
CLI profile selection is trusted configuration, pinned per individual and exchange.
Inbox text cannot select another profile. Public provenance does not authenticate a
human; acceptance remains independent of claimed model authority.

## Three matched conditions and fresh evaluation

teacher-lmft, teacher-none (same LMFT with lesson acceptance disabled), teacher-memory.
All receive the SAME actual teacher reply and equivalent training/validation access;
only teacher-lmft owns the model call. Controls receive replay attributed to that exchange,
not fabricated model executions. Identical weights/outcomes/cases before teaching.

After disposition: halt, restart without input, compare full retained state, then evaluate
six fresh e1..e6 with teacher disabled (no adapter commands). Each has at most one selected
verification, using a registered verifier after the question commits. e1: B available,
shielded=true, actual success; e2: B available, shielded=false, actual failure;
e3: B available, shielded=true, actual failure (counterexample); e4: neither A nor B
available; e5: A available but B unavailable (scope reversal); e6: no independent conflict.
A unavailable except e5. D is irrelevant. Outcomes remain evaluator-only; teacher and
acceptance cannot access them. e6 has no verification and abstains. Evaluate after halt.

Measure selected routes, useful/irrelevant/unresolved verification, predictions, accuracy
on decided cases, coverage and abstentions. Improved route choice on v1/v2 establishes
only validation utility. Fresh transfer requires more relevant resolutions than the
no-lesson control, not just stored prose. Record counterexamples and ordinary-memory
equivalence. Do not tune prompts/criteria after seeing outcomes.

## Checks, archive and stopping

Routine tests use mocks: profile/version pin, exact reply linkage, schema bounds,
unsupported/unauthorized fields, evidence/validation isolation, model failure, duplicate
adapter invocation/reply, retry limits, lesson-disabled control and checkpoint restart.
Actual offline experiment uses real processes. During runtime expose only outbox/lifecycle;
full state inspection only after halt. Repeated exact and new-ID lesson replies must not
apply a second update. Preserve source/config/profile/prompts/raw responses/messages,
dispositions, initial/final checkpoints, model provenance, costs and failures. Compare
post-restart behavior with a halted read-only evaluation of the same retained state.
Report model latency/calls separately from deterministic evaluation time and storage.
Stop after three conditions × six fresh cases, at most two actual inference attempts.
Communication, retained proposal and measured transfer are separate success criteria;
a rejected proposal is a valid result. No fallback to an authored lesson.
