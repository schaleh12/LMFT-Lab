# Comparative procedure reliability — results

Recorded 2026-10-11 UTC. Preregistered
[protocol](COMPARATIVE_RELIABILITY_PROTOCOL.md); [commands and implementation](../docs/COMPARATIVE_RELIABILITY.md).
Historical [first-fixture results](INTERACTIVE_REVISION_RESULTS.md) remain unchanged.

## Finding

**The three learning conditions produced identical judgments, revisions, evidence and
held-out behavior. Fuzzy propagation supplied no measurable learning benefit.**
The cause of behavioral change was the existing verified-evidence counter and its
fixed thresholds. Propagated activation is not an input to that counter.

The second fixture executes one left-to-right adjacent compare/swap pass, then checks
its recorded output against a full sort. It grounds six synthetic procedure outcomes
in executable verification, unlike the first fixture's fixed measurement equality.
It does not establish real-world factual grounding or procedural understanding.

## Execution and checks

Final deterministic archive: `outputs/comparative-reliability-003/`, total
10.026 seconds across comparisons and uninterrupted run.
**27/27 experiment checks passed; 197/197 tests passed**, including the original
179 tests. Deterministic model proposals were explicit mocks. Actual SLM calls: zero.

| Check | Result |
| --- | --- |
| Initial judgment / probe | 0, undetermined; request more evidence |
| Inbox/outbox | Deliberate clarification, linked teacher outcome, attributed response |
| Two verified successes | 1/3 then 1/2; support; trial with verification |
| Unsupported teacher assertion | Rejected; score/evidence unchanged |
| Actual halt/restart | Exact original evidence and revision reasons retained |
| Four contrary outcomes | 1/5 → 0 → -1/7 → -1/4; final oppose, use full sort |
| Propagation versus zero passes | Execution activation .2 and Confidence .05 versus zero; identical judgments |
| Structured-memory baseline | Exact same learned judgment/evidence/revisions, independently recounted |
| Uninterrupted comparison | Exact learned judgment/revision equality |
| Repeated delivery / reattribution | No extra evidence, accepted revision or score increase |
| Learning-disabled control | Score 0, no accepted evidence; continues to request evidence |
| Live inspection boundary | Refused; full diagnostics read only after halt |
| Seed/equations/migration | Original files byte-equal to archived first-fixture sources |

No acceptance criterion was changed after evaluation. **Failed run retained:**
`outputs/comparative-reliability-001/failure.json` records a Windows PermissionError
while reading a checkpoint during replacement. A bounded sharing-error retry fixed
that infrastructure issue; it did not change the evidence or score rules. The
successful `-002` archive is also retained. Final `-003` strengthens independent
communication auditing; it does not change the scientific comparison.

## Held-out scope and limitations

The probe returns action labels only; it does not execute autonomous actions or
peek at held-out outcomes. It applies one aggregate judgment to all in-scope inputs.

| Held-out input | Actual one-pass outcome | After successes | After contrary evidence |
| --- | --- | --- | --- |
| [0,2,1] | Success | Predict success | Predict failure |
| [9,7,8] | Success | Predict success | Predict failure |
| [8,9,6] | Failure | Predict success | Predict failure |
| [4,1,0] | Failure | Predict success | Predict failure |
| Four-element input | Outside declared scope | Out of scope | Out of scope |
| Different procedure | Outside declared scope | Out of scope | Out of scope |

Initial coverage was 0/4 (undetermined), with no accuracy assigned to abstention.
After successes and after contrary evidence, coverage was 4/4 and accuracy **2/4**
in every learning condition. Two scope exclusions were correct. These were new
inputs, not replayed training cases. The score changed which cases were wrong,
without improving accuracy. No broad generalization or useful concept geometry was
demonstrated; a coarse reliability judgment cannot distinguish individual cases.
The learning-disabled control abstained on all four in-scope cases throughout.

## Costs and record growth

Final metrics include the ten repeats and two explicit completion markers.
Wall seconds sum measured active stage lifetimes, including startup, IPC/polling,
commit and halt; initial birth-only startup is excluded. Core milliseconds are the
sum of internal cycle processing before serialization/commit. Timing has one final
run per condition, no randomized order or confidence interval. It is descriptive,
not a statistically established speed comparison.

| Condition | Final score | Stage wall s | Core ms | Mock / real calls | Checkpoint bytes, initial → final | Final individual bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Propagation | -0.25 | 2.008 | 112.58 | 45 / 0 | 18,067 → 672,141 | 678,468 |
| Zero passes | -0.25 | 1.933 | 78.54 | 45 / 0 | 18,097 → 507,955 | 514,282 |
| Structured memory | -0.25 | 1.683 | 12.25 | 0 / 0 | 18,081 → 58,172 | 64,500 |
| Learning disabled | 0.00 | 2.042 | 110.08 | 45 / 0 | 18,068 → 665,586 | 671,914 |

Every learning condition ended with **6 evidence records, 15 revision records
(6 accepted / 9 rejected), 20 receipts, 15 processed IDs, 15 diagnostics and 17
outgoing messages**. The control had 0 evidence, 15 rejected revisions and 16 outgoing
messages; the other receipt/diagnostic counts matched. Initial counts were zero.
The extra control difference is the absent conflict clarification, since no outcome
was admitted. The memory baseline uses the same audit/store shell, including unused
birth metadata; it is simpler computationally but not a minimal possible data store.
A/B used identical mock output and settings with different activation context; memory
used no mock adapter. All deterministic actual-model call budgets were equally zero.

Repetition results (each batch includes one separately counted unsupported marker):

- Five exact duplicate deliveries: five extra receipts, no model/mock calls,
  revisions, diagnostics or utterances attributable to those duplicates. The marker
  added one rejected revision/diagnostic/response and three mock calls in A/B/control.
- Five new message IDs with the same t6 evidence: five rejected revisions,
  diagnostics and responses, plus 15 mock calls in A/B/control. The marker added one
  more of each record and three calls. Memory made no calls.
- Every batch retained six accepted samples and score -1/4 in learning conditions.
  No evidential inflation occurred. There is no learned confidence field to inflate.

| Condition | Checkpoint growth: duplicates + marker (bytes) | Reattributions + marker (bytes) |
| --- | ---: | ---: |
| Propagation | 43,313 | 260,005 |
| Zero passes | 32,367 | 194,318 |
| Structured memory | 2,751 | 14,325 |
| Learning disabled | 43,196 | 258,595 |

The overhead is a negative engineering finding: repeat processing under new IDs
retains expensive no-op diagnostics. No consolidation or pre-inference optimization
was quietly introduced. Whole-history checkpoints also amplify copy/write cost.
The memory baseline achieved the same learning with much less diagnostic storage.
Totals above cover the individual directory only, excluding source snapshots and
separately retained halted-state snapshots used for experiment preservation.

## Real offline SLM communication smoke — separate result

Archive: `outputs/comparative-reliability-local-002/`. Actual pinned Qwen3-4B Q4_K_M,
llama.cpp b11429 CUDA, offline cached assets, same existing configuration. Total
wall time **43.575 seconds**. **6/6 checks passed**: twelve validated
calls across four inputs, one reused server PID, rejected unsupported assertion,
verified final score 0 from one success and one failure, faithful outgoing messages,
and refused live inspection. Six outbox messages passed independent checks of
historical score/decision, evidence counts/references, acceptance reasons and limited
uncertainty wording. Checkpoint: 328,503 bytes; individual directory:
329,810 bytes. Records: 2 evidence, 4 revisions (2 accepted/2 rejected),
4 receipts, 4 diagnostics, 6 outgoing messages. All inspection occurred after halt.

Outgoing wording is **authored from state**, not generated by the SLM. For example,
after success plus contrary evidence it reports undetermined, one verified success,
one verified failure, and requests more evidence without guaranteeing success.
This smoke verifies model integration and truthful presentation of the accepted
judgment. It does not demonstrate more capable learning or reliable free-form model
expression. A model-assisted three-condition comparison was not conducted.

Earlier local `-001` is preserved. Its `metrics.wall_seconds` field was the sum of
model-call durations, mislabeled as wall time; its `total_wall_seconds` is valid.
Final `-002` corrects that measurement label and independently audits message content
rather than using the wording producer as the test oracle. Learning criteria remained
unchanged. All runtime processes from these runs halted successfully.

## Reproducibility, open questions and next step

Each archive contains exact source/test/config/protocol copies, a SHA256 archive
manifest, original inbox files, complete halted state, evidence/revision reasons and
model traces where applicable. Local outputs remain ignored by Git; back up those
archives separately. This tracked report preserves the selected results and failures.
Protocol SHA256: `b7c1e20ea8f6037b5aa6308b979d676a66252315a87b3dddbf8c2db3067c7f50`.
Final runtime source-map SHA256: `8a452e8b79c1b5dc782939adfcaf6d89c4f0d495d2f6e869a09b389191040f3f`.
No historical experiment was overwritten. Older individuals require their original
archived runtime sources because existing source-hash restart checks remain enforced.

Inconclusive or unsupported: a benefit from fuzzy geometry beyond diagnostics,
semantic generalization, calibrated confidence, learned associations, autonomous
contemplation, real-world evidence validation and statistical timing superiority.
The numerical equality is expected from the current uncoupled architecture; it does
not refute every possible future use of activation.

**Smallest next learning experiment:** preregister one authored input distinction
(e.g. whether the smallest element is last), compare two scoped ordinary-memory
counters against the current aggregate counter using fresh held-out inputs, and
retain the same verification/update rule. This tests whether conditional evidence
addresses the observed 2/4 limitation before adding any activation-to-learning coupling.
Any later coupling needs its own explicit proposal and controls; this result supplies
no justification for manufacturing one merely to make LMFT win.
