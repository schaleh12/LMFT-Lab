# Comparative procedure reliability — preregistration v1

Recorded before implementation and evaluated runs. Preserve the previous interactive
protocol/results and output archives. This is a synthetic, verifiable procedure study,
not a real-world reliability estimate or a new cognitive theory.

## Target, evidence and existing rule

Separate target `fixture/one-pass-sort-reliability`: whether a single left-to-right
adjacent compare/swap pass returns a fully ascending list, for lists of exactly three
integers in [0,9]. Each adjacent pair is visited once (indices 0 and 1). The verifier
executes that procedure and independently compares the result with Python sorted.
Accepted records must match an authored trial ID, procedure version, recorded input,
and actual output. A teacher's claimed success or a model interpretation cannot
replace verification. Held-out inputs are never accepted as training records.

The canonical seed and all existing equations remain unchanged. Reuse the current
judgment equation sum(signs)/(n+2), initial 0, success +1 and failure -1, once per
trial ID. Support >=0.2, oppose <=-0.2, otherwise undetermined. This is an evidential
orientation score, not calibrated confidence/probability. Proposed scope is an
experimental convention, not a claim that six cases establish reliability.

Authored conceptual references: Psychological/Truth/Fact for measured results,
Psychological/Will/Execution for the procedure, and Psychological/Contemplation/
Confidence for evidential questions. Diagnostic edges Fact -> Execution -> Confidence
have weight 1, confidence .1, plasticity .5, provenance `reliability-fixture-1`.
These are illustrative associations, not learned meanings. Authored interpretation
activates Fact .8; default two passes/gain .25 gives Execution .2 and Confidence .05.
The score never consumes any activation, including the Confidence leaf.

## Frozen sequence and probes

Start with a question and no evidence; require an outbox clarification. A linked
teacher reply supplies t1. An unsupported assertion with unknown trial ID must be
rejected. Then t2 supplies a second success. Halt and restart the actual process,
verify original evidence/reasons, then deliver contrary evidence t3..t6:

| Trial | Input | Observed one-pass output | Sign |
| --- | --- | --- | --- |
| t1 | [1,3,2] | [1,2,3] | +1 |
| t2 | [2,1,3] | [1,2,3] | +1 |
| t3 | [3,2,1] | [2,1,3] | -1 |
| t4 | [2,3,1] | [2,1,3] | -1 |
| t5 | [4,3,2] | [3,2,4] | -1 |
| t6 | [5,4,3] | [4,3,5] | -1 |

Expected score sequence: 0, 1/3, unchanged after unsupported assertion, 1/2,
1/5, 0, -1/7, -1/4. Final decision oppose. Probe is read-only, no inference or
learning. In scope: support means `trial_with_verification`, oppose means
`use_full_sort`, uncertainty means `request_more_evidence`; these are returned labels,
not autonomous execution. Out-of-scope procedure/input always returns `out_of_scope`.

Frozen held-out cases: one-pass [0,2,1] (actual success), [9,7,8] (actual success),
[8,9,6] (actual failure), [4,1,0] (actual failure); four-element input and a different
procedure are out of scope. Probe applies the aggregate judgment without peeking at
held-out outcomes. At final oppose it predicts failure for all four in-scope cases:
expected accuracy 2/4, coverage 4/4; two scope exclusions. Report initial/post-success/
final predictions, coverage, accuracy and action labels. This deliberately exposes
the limited aggregate scope rather than engineering a perfect held-out result.

## Conditions, controls and budget

A: same persistent revision with authored edges/default propagation.
B: identical input/proposals/edges, passes=0.
C: structured-memory ledger; same validator, independent transparent recount of
successes/failures with the same equation, no activation or model calls. Reuse runtime
communication/storage infrastructure to match delivery/restart semantics; unused birth
metadata remains storage overhead, so this is not a minimal-memory speed benchmark.
A/B use three deterministic mocked role calls per eligible envelope, C none; actual
SLM calls are zero for every deterministic condition. Same messages/teacher sources.
A learning-disabled control uses A's processing but accepts no evidence. An additional
uninterrupted A comparison checks checkpoint/restart equivalence.

After contrary evidence, submit the exact t6 message five times, then the same t6
record under five new message IDs. End each batch with a valid unsupported marker
message to establish completion through the outbox, not a live state reader. Markers
are separately counted. No repeat may add evidence, accepted revisions or score.
Expect original implementation overhead: exact duplicates add receipts only; new IDs
add rejected revision records, responses, and processing diagnostics. Measure rather
than consolidate these costs. No confidence-increase claim is possible: no learned
confidence field exists. Limit repeats to ten and never schedule idle contemplation.

## Acceptance, measurements and stopping

Require exact score/probe equality across A/B/C, evidence/reason retention after restart,
unsupported/duplicate rejection, unchanged seed, read-only probes and refused live
inspection. Verify propagation actually changes diagnostic activations A vs B; expect
no behavioral advantage because no score coupling exists. Controls remain score 0.
Measure per-stage wall time (includes process/delivery/polling), internal cycle compute
time, actual and mock role calls, receipts, revisions (accepted/rejected), evidence,
outbox and diagnostics counts, checkpoint bytes and total individual-directory bytes.
Capture before/after repetition differences. Exclude archived source copies from size
comparisons. Timing is descriptive, one run per condition, no speed significance test.

Stop after the fixed sequence/batches, max 420 seconds per exchange/process boundary.
Record checks as pass/fail, preserve all failures; do not tune criteria to outcomes.
Only inspect full checkpoints after halt. While running use deliberate outbox and
lifecycle acknowledgments only. Freeze source/config/protocol hashes and archive exact
sources before running. No automatic conversion of earlier checkpoints.

After deterministic evaluation, run a separate offline actual-SLM smoke using A:
question, linked t1 reply, unsupported assertion, t3 contrary outcome (four inputs,
at most twelve calls). Same pinned existing model/config; no model-assisted comparative
claim. Halt, verify actual calls, server reuse, rejection and resulting score 0.
Check each authored outgoing response against its committed revision and probe,
selected evidence IDs, and uncertainty wording. Fluent model proposals are internal;
no model-generated utterance or improved learning is claimed. Failures remain results.
