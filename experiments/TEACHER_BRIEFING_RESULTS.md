# Bounded teacher briefing follow-up â€” results

2026-10-11. [Preregistered comparison](TEACHER_BRIEFING_PROTOCOL.md).
New study: ignored `outputs/teacher-briefing-001/`. Historical replay, with zero inference:
`outputs/teacher-historical-replay-002/`. The original [teacher result](TEACHER_RESULTS.md),
its raw exchange and all prior research results remain unchanged.

## Outcome and stopping point

Completed the four allocated offline calls, with **no retries, replacements or extra calls**.
The clarified briefing produced one accepted B=.75 proposal in the beneficial situation.
Its retained route preference changed fresh investigation choices after restart. Ordinary
memory matched LMFT. Both briefings appropriately proposed no change in the already-sufficient
situation. Appropriate action did not guarantee an entirely supported explanation.

The study is complete. Teacher communication remains optional; the next development task is
[one outcome-sample correction](../docs/EVIDENCE_LEARNING_HANDOFF.md), not more teacher tuning.
That experiment was documented but not implemented here.

## What the original archive establishes

The archive contains the exact system/user messages, raw model response, parsed proposal,
validation, model/config/profile provenance and settings. The original system told the teacher
that A/B investigate shielded, D investigates irrelevant color, a usable measurement differs
from a correct prediction, weights are limited to .25/.5/.75, and two training IDs are required.
The user context contained A unavailable/B available calibration, current .5 weights and
conditional judgment summaries. It did not explain weight effects on selection, tie-breaking,
the one-request consequence, or a clear schema-compatible no-change convention.

The observed rejection was an unchanged A=.5 proposal and zero validation improvement.
The phrase "available evidence entries" is ambiguous: it may refer to records existing,
not usable measurements. It does not prove the model believed the false availability flags
were true. Insufficient model size or definite misunderstanding cannot be inferred from
that one response. Incomplete briefing was a testable hypothesis.

The original request specified `enable_thinking=false` and `/no_think`; it used 745 prompt
and 82 output tokens under an 8192 context and 1024 output ceiling. Finish reason was `stop`,
JSON parsing succeeded and the raw response matches the recorded proposal. The original backend log also confirms `n_ctx_slot=8192` and `truncated=0`;
it is copied into the follow-up archive. There was no observed truncation. The new historical-briefing beneficial call reproduced the same proposal
and wording. This strengthens reproducibility for this setting, not a causal diagnosis.

## Exact briefing changes and unchanged mechanisms

V1 profile/config text is preserved. V2 retains the same stable boundary, capability description
and reply schema, with generic guidance to interpret availability literally, explain operational
consequences, and express justified no change using an evidenced route's current weight.
This convention does not make a no-op an accepted update.

`config/teacher_briefing.json` supplies scoped operational context:

- A/B are equally relevant alternative requests for shielded; D requests irrelevant color.
- `available=true` means a usable measurement was returned; false means none was returned.
  Record presence, shielded's Boolean value and prediction correctness are separate matters.
- Higher weight raises preference among equally relevant conflicting candidates; ties select
  A before B. One route is tried; unavailable measurement leads to abstention, not another try.
- Registered evidence supports the direction of a change; fixed validation must strictly
  improve resolution without increasing irrelevant requests. Current validation count and
  its two-case maximum are supplied, without validation case answers.
- Future availability and predictive success are unknown. No desired route/weight is stated.

System profile contains the stable role/boundary/schema; current routes/evidence/state/question
are task context. This is a bundled briefing comparison, not isolation of one wording change.
The lesson schema, `teacher.assess`, validation and selection functions, core numerical
modules, model configuration and backend lifecycle were unchanged. No held-out answers were
supplied to the teacher or acceptance policy.

Both briefings received the same four calibration records and eight prior outcomes, with the
same validation conditions. New individuals used A=B=D=.5 in the beneficial situation and
A=.25/B=.75/D=.5 in the no-change situation. These are explicit experiment initializations,
not secretly learned changes. Pre-inference enumeration using training/validation only found
exactly two accepted edits for beneficial (A=.25 or B=.75) and none for no-change, already at
2/2 validation resolutions. Finite-set optimality is not universal optimality.

## Every preregistered call

All four used the existing pinned Qwen3-8B Q4_K_M and llama.cpp b11429, offline, seed42,
temperature0, non-thinking request, 8192 context, 1024 output ceiling and 120s timeout.

| Slot | Briefing / situation | Actual proposal and citations | Disposition | Operationally appropriate | Seconds | Input / output tokens |
| --- | --- | --- | --- | --- | ---: | ---: |
| 1 | V1 / beneficial | A=.5; train-A1/A2 | Reject: no-op, 0â†’0 validation | No | 11.391 | 745 / 82 |
| 2 | V2 / beneficial | B=.75; train-B1/B2 | Accept: grounded increase, 0â†’2 validation | Yes | 11.610 | 1093 / 101 |
| 3 | V1 / no-change | B=.75; train-B1/B2 | Reject as update: no-op, 2â†’2 validation | Yes | 11.625 | 747 / 112 |
| 4 | V2 / no-change | B=.75; train-B1/B2 | Reject as update: no-op, 2â†’2 validation | Yes | 12.079 | 1095 / 165 |

All four replies were schema-valid with eligible, same-route references. Operational
appropriateness is a preregistered task-level proxy: an accepted improvement in beneficial,
or an eligible no-op in no-change. It is separate from acceptance and semantic understanding.
Three update rejections include two appropriate recommendations to retain state.

The accepted reason accurately cited available B measurements and its uncertainty limited
future availability claims to the supplied calibration. No unsupported claim was identified
in that response. V1 reasons used ambiguous "available evidence" phrasing; the no-change
reason also blurred the distinction between task relevance and measurement availability.

V2 no-change correctly described usable B measurements and retained its weight, but its
uncertainty said that lack of additional calibration records limits further increases. That
explanation is unsupported: .75 is already the schema maximum and validation is already 2/2;
more records alone cannot permit an increase. This semantic deficiency was retained. It did
not affect the independently correct no-op disposition. Manual availability classifications
were ambiguous / accurate / ambiguous / accurate; unsupported-claim classifications were
ambiguous / no / ambiguous / yes. The rubric and full audit are stored separately from policy
acceptance in `post-halt-comprehension-audit.json`; no LLM grader was used.

## Teacher-disabled transfer

Each slot used three matched new individuals. Only LMFT invoked the teacher; lesson-disabled
LMFT and ordinary memory received the identical actual proposal and validation access. All
then halted/restarted and evaluated the fresh b1..b6 fixture with zero teacher calls.

| Slot / condition | Resolved / requests | Inconclusive requests | Correct / decided | Abstentions | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1, all three conditions | 1 / 5 | 4 | 1 / 1 | 5 | 16.7% |
| 2, LMFT with lesson | 3 / 5 | 2 | 2 / 3 | 3 | 50.0% |
| 2, lesson-disabled LMFT | 1 / 5 | 4 | 1 / 1 | 5 | 16.7% |
| 2, ordinary memory with same lesson | 3 / 5 | 2 | 2 / 3 | 3 | 50.0% |
| 3, all three conditions | 3 / 5 | 2 | 2 / 3 | 3 | 50.0% |
| 4, all three conditions | 3 / 5 | 2 | 2 / 3 | 3 | 50.0% |

There were zero irrelevant requests in every condition. Inconclusive requests are separately
reported costs, not successful investigations. No-change conditions already started with the
B preference; their performance is not newly acquired transfer.

The accepted B=.75 preference selected B instead of A in b1..b5. It resolved b1..b3; b3 was a
prediction error despite a valid measurement. It abstained on b4 (unavailable) and b5 (only
A available, a scope reversal). The unchanged A preference resolved only b5 correctly. All
conditions abstained on b6 without independent conflict and spent no request there. Consequently
coverage improved in slot 2 while accuracy on the different decided subsets was 2/3 versus
1/1. This is not an accuracy superiority claim.

The change was caused by the accepted route weight being consumed by existing selection,
not by new factual outcomes, altered judgment equations or fluent prose. It demonstrates a
bounded retained preference affecting these fresh cases. Ordinary memory performed identically;
there is no measured fuzzy advantage or evidence of broad conceptual understanding.

## Inference, persistence, tests and costs

All four response stop reasons were `stop`. Every request recorded `enable_thinking=false`
and `/no_think`; responses contained structured content without a separate reasoning field.
All context totals were far below 8192 and output counts below 1024. Archived backend logs
confirm `n_ctx_slot=8192` and `truncated=0` for each call. These observations establish the
requested generation mode and observed output behavior, not visibility into internal cognition.
The backend repeated a control-token-type override warning across all calls; no associated
parse/truncation failure was observed. No model replacement/download or configuration tuning
occurred. Model pin and checksum remain those in [the original report](TEACHER_RESULTS.md).

Four actual calls took 46.705 seconds total including cache verification/startup/inference;
model latency is separate from evaluation below. Historical replay used zero calls.

| Slot | Evaluation core ms: LMFT / disabled / memory | Evaluation wall s: LMFT / disabled / memory | Final checkpoint bytes: LMFT / disabled / memory |
| --- | --- | --- | --- |
| 1 | 47.869 / 46.344 / 13.578 | 1.423 / 1.432 / 1.315 | 371448 / 371445 / 99166 |
| 2 | 47.305 / 47.367 / 11.987 | 1.419 / 1.420 / 1.306 | 377512 / 377361 / 105242 |
| 3 | 47.277 / 51.637 / 11.694 | 1.419 / 1.447 / 1.296 | 372106 / 372104 / 99836 |
| 4 | 47.640 / 53.538 / 12.610 | 1.415 / 1.462 / 1.322 | 379401 / 379405 / 107130 |

Single-run timing is descriptive. LMFT archives propagation traces that memory does not;
this contributes storage/processing differences. Complete per-stage counts and directory
sizes are in results.json. No consolidation or additional learning loop was introduced.

**324 tests passed**, including five tests for materially changed briefing/initialization
behavior. **120/120 experiment checks passed**. All 12 individuals halted. Exact restart
retained exchange, proposal disposition and accepted state where present; post-restart
choices matched read-only predictions. Core counter, seed and experience-update invariants
held. A separate historical-message replay passed **9/9 checks** with zero inference.
The adapter/storage/backend mechanisms were reused; no acceptance failures were repaired
or substituted. Runtime observation stayed limited to outbox/lifecycle until halt.

## Adequacy, limits and handoff

Qwen3-8B demonstrated the ability to provide one useful constrained lesson and an appropriate
no-change action under the clarified briefing. Reliability remains inconclusive: one call per
cell, one fixed seed, a bundled briefing change, synthetic evidence and a remaining unsupported
explanation do not establish robust comprehension. The evidence does not justify replacing the
model, expanding teacher infrastructure or continuing retries in this task.

Proceed next with [one mistaken outcome-sample correction](../docs/EVIDENCE_LEARNING_HANDOFF.md):
retain the original, validate an authorized replacement, project one effective record per root,
and recompute the unchanged score equation without double counting. Compare ordinary memory,
verify behavioral consequence and restart, and leave teacher assistance optional. No genuine
teacher/hardware blocker is known; outcome eligibility/projection is the remaining implementation
work. No outcome-sample correction was implemented here.

## Reproducibility

The run archives source/config/profile snapshots, exact requests, model responses, inbox/outbox,
feasibility enumeration, per-call allocation, dispositions and halted states. Backend logs and
manual comprehension audit were added after halt without changing evaluated snapshots/results.

- V2 profile SHA256: `fbb01e494358c1eecd8fde359477a39a66947c7a4aa5cb120c04dc5108289eb6`.
- Context/study config SHA256: `fb856a661935740fbcfb768872e2a506dbfc92eea8493f1cba5d1d8b022f33f7`.
- Protocol SHA256: `517fb1620a1cccd9bfc7ad8fc64caee9619e5afcc4ec8a257ad7fc568f64d864`.

Run from the repository root in PowerShell with a fresh output directory:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_teacher_briefing.py --output outputs/my-briefing-study
```

The harness permits four fixed slots, no retries, offline only. Reproduction is a new study
run, not permission to extend the completed task's four-call budget.
