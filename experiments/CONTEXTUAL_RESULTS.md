# Context-dependent learning and clarification — results

Recorded 2026-10-11 UTC. [Preregistration](CONTEXTUAL_PROTOCOL.md),
[implementation and exact commands](../docs/CONTEXTUAL_EXPERIMENT.md).

**LMFT retained and applied conditional judgments, but matched ordinary conditional
memory rather than outperforming it.** Selection used an authored feature and ordinary
lookup. Propagation did not participate. The historical [comparative result](COMPARATIVE_RELIABILITY_RESULTS.md)
is preserved and remains no evidence of a fuzzy-tree advantage.

## What was implemented

Two separately stored transmission judgments condition on an explicitly authored
observable `shielded` flag. The existing bounded score equation and thresholds are
unchanged. Outcomes are admitted only after registered procedure execution verifies
the recorded payload, feature, disturbance and output. Successes and failures are
stored with original attributed evidence and supporting/contradicting revision reasons.
The feature was supplied, not independently discovered; counting verified outcomes
learns the fixture association, not the feature's meaning.

A missing feature causes a targeted pending question, not an aggregate fallback.
A correctly linked, registered condition reply resolves only that case. It is not
outcome evidence or constitutional authority. Persistent question IDs and resolution
sources survive restart. Invalid and irrelevant answers leave the question pending.

Evidence IDs are distinct from delivery IDs. Identical text across independent events
counts normally; accepted evidence retransmissions are lightweight receipts, not new
revisions or model processing. Conflicting ID reuse is rejected. Evaluation caching
uses complete available case, policy/mode, revision version and resolved-condition
provenance. Fresh evidence forces re-evaluation instead of replaying stale wording.
Global version invalidation is conservative: unrelated branch changes can also cause
a fresh evaluation; no claim of optimal caching is made.

## Predefined checks

Final deterministic run: `outputs/contextual-002/`, **11.940 seconds**.
**73/73 experiment checks and 206/206 tests passed**. The 197 prior tests still pass.
Deterministic comparisons use no model calls or mock inference. The separate offline
wording smoke passed **9/9 checks**. No evaluated run failed; the earlier successful
`contextual-001` archive is retained. The final deterministic harness also includes
the single-case smoke reply path used by the local run. Criteria were not changed.

| Check | Observed outcome |
| --- | --- |
| Initial state | All counters 0; known cases abstain |
| Registered training | Both conditions have successes and failures; scores +1/3 and -1/3 |
| Aggregate comparison | Four successes/four failures yield 0 |
| Missing condition | Two pending requests; no unsupported prediction |
| Irrelevant/malformed replies | Both rejected, request remains pending |
| Verified linked replies | Both requests resolve, original source and reply references retained |
| Waiting | 0.3-second idle interval adds no output, receipts, diagnostics or calls |
| Actual process restart | Judgments, evidence, reasons and both pending references retained |
| Restarted versus uninterrupted | Exact final contextual state/question equality |
| Read-only probes | No learning, version or communication changes |
| Evidence repetition | No added accepted evidence/revisions/model diagnostics |
| Evidence-ID conflict | Rejected without overwriting original |
| Changed context | Contrary evidence invalidates prior h1 evaluation |
| Learning-disabled control | No learned evidence, both counters stay 0 |
| Recovery tests | Injected interruption before/after replacement preserves one committed resolution |
| Interface | Live full inspection refused; full diagnostics read after halt |

The existing seed constructor, activation/propagation equations, migration and pinned
model backend remain unchanged. No new seed nodes, learned graph edges or automatic
code modification were added. Older checkpoints still require their archived source
versions; none were silently converted or overwritten.

## Prediction and clarification quality

All three conditions had identical evidence, available features, cases, teacher
contributions and zero deterministic model-call budgets. The aggregate condition has
access to the feature but uses one counter by definition; all conditions share the
missing-input gate and verification policy. Conditional memory independently recounts
the same scoped records. Shared verifier/communication/storage infrastructure is a
common assumption, not an optimized minimal-memory benchmark.

| Stage / condition | Known decisions | Correct known decisions | Withheld | Accuracy among decisions |
| --- | ---: | ---: | ---: | ---: |
| Initial, all | 0/6 | 0 | 6 | Not defined |
| After training, aggregate | 0/6 | 0 | 6 | Not defined |
| After training, conditional memory | 6/6 | 4 | 0 | 66.7% |
| After training, LMFT lookup | 6/6 | 4 | 0 | 66.7% |
| After contrary evidence, all learning conditions | 6/6 | 3 | 0 | 50% |
| Learning disabled, all stages | 0/6 | 0 | 6 | Not defined |

The feature enabled covered judgments where aggregate evidence cancelled, but did not
remove exceptions: one shielded failure and one unshielded success were mispredicted.
Abstentions are not counted as correct or as zero-percent accuracy. Two scope exclusions
were correctly excluded in all conditions. These are six preregistered new cases,
not a generalization benchmark over all possible transmissions.

Both missing cases had **0/2 decisions before clarification**. After verified answers,
LMFT and conditional memory made **2/2 correct decisions**; aggregate and the learning-
disabled control still abstained because their scores supplied no preference.
Clarification selected the applicable learned counter without changing its score.
This demonstrates withholding unsupported decisions and information use, not a measured
advantage over baselines with the same clarification access. No guessing control was
used and no claim about how many wrong guesses were prevented is made.

The fixed contrary sequence reduced shielded scores through **1/7, 0, -1/9, -1/5**;
unshielded stayed -1/3. Aggregate ended -2/7. Known-case accuracy fell from 4/6 to 3/6
in both conditional conditions. This negative result is preserved: the selected
contrary history shifted the aggregate orientation, not a mechanism that detects
which individual case is exceptional.

## Costs, storage and retransmission

Times are descriptive from one final run, not statistically established differences.
Stage wall times include process startup, polling, commit and halt; initial birth and
the isolated idle/restart check are not included in the summed stage figures. Core
time excludes serialization/commit. Total run time above includes all conditions and
uninterrupted execution. Individual bytes exclude source copies and separate archived
halted-state snapshots. Deterministic calls/large model diagnostics were zero throughout.

| Condition | Summed stage wall s | Core ms | Checkpoint bytes initial → final | Final individual bytes |
| --- | ---: | ---: | ---: | ---: |
| Aggregate memory | 1.884 | 27.27 | 18,455 → 70,286 | 83,174 |
| Conditional memory | 2.067 | 28.59 | 18,590 → 70,097 | 82,985 |
| LMFT lookup | 1.886 | 29.30 | 18,584 → 77,576 | 90,462 |
| Learning disabled | 1.955 | 24.77 | 18,585 → 64,277 | 77,165 |

The learning conditions finish with **12 evidence records, 12 accepted revisions,
2 condition records, 2 retained question references, 13 cached contexts, 41 receipts,
36 processed message IDs, 3 compact rejection records, 31 outbox messages and no model
diagnostics**. The control retains no accepted outcomes/revisions; it has 20 compact
rejections, 12 cached contexts and 36 outgoing messages. It still resolves both
condition records, which are not learning events.

The bounded repetition batch contained five new delivery IDs carrying accepted s1,
five exact original-message duplicates, and one explicit completion barrier. In all
learning conditions the ten repeats added no revision, cached result, diagnostic,
model call or repeated utterance; the barrier added one response. Eleven lightweight
receipts and six new processed IDs remain. All original inbox files remain too.

| Condition | Checkpoint growth for repeats + barrier (bytes) | Individual growth (bytes) | Added revisions | Added model diagnostics |
| --- | ---: | ---: | ---: | ---: |
| Aggregate memory | 3,539 | 7,064 | 0 | 0 |
| Conditional memory | 3,538 | 7,064 | 0 | 0 |
| LMFT lookup | 3,538 | 7,062 | 0 | 0 |
| Learning disabled | 6,537 | 10,061 | 0 | 0 |

This addresses the earlier redundant processing, but does not eliminate journal
or whole-checkpoint write costs. The learning-disabled control's unaccepted samples
are not in the accepted-evidence ledger; retransmissions can add compact rejection
records/responses, without large diagnostics or model calls. Cache/history growth
remains unbounded outside the finite experiment. No broad consolidation was implemented.
Previous experiments used different paths and workloads; these timings are not a
matched speedup estimate against their model-processing costs.

## Actual offline constrained-wording smoke

Archive: `outputs/contextual-local-001/`. Existing pinned Qwen3-4B Q4_K_M/llama.cpp
CUDA backend, offline assets, unchanged model settings. **Four actual validated calls**
used one server PID. Total wall time **11.041 seconds**; per-call
latencies were **8.672, 0.238, 0.406, 0.326 seconds** (first includes cold startup).

Calls covered a known-case judgment, the targeted missing-condition question, its
verified answer, and a fresh judgment after contrary evidence. Repeated evidence,
an unchanged known-case query, and idle waiting caused no additional calls. The
last query changed from success to failure using new evidence; stale cached wording
was not replayed. All emitted evaluation wording matched score, uncertainty and
supporting evidence references in the selected result.

Final smoke records: 12 verified outcomes/revisions, 1 condition record, 1 retained
question, 4 cached contexts, 28 receipts, 23 processed IDs, 18 outgoing messages and
4 private model traces. Checkpoint: **71,021 bytes**;
individual directory: **80,023 bytes**.

The model genuinely ran, but could only select between two complete preverified
renderings under an enum grammar. Exact output membership was validated independently;
unit tests rejected an invented guarantee and verified explicit authored fallback.
The smoke establishes faithful **constrained formulation**, not arbitrary natural-
language generation or independent semantic verification. No model-assisted
three-condition superiority comparison was conducted. All model traces were inspected
only after halt; no automatic bridge or live diagnostic feed exists.

## Preservation, limits and next experiment

Each new archive contains original inputs, checkpoints, evidence/reasons, source/test/
config/protocol snapshots and SHA256 manifests. Full local outputs are ignored by Git;
back them up separately. This report preserves selected results. Historical results
and failed attempts from prior studies are untouched.
Protocol SHA256: `7a5c7e638be36aeeeac5674a38ee2a3b213a367e2733a4fc443c8e25b3da1e5e`.

Not established: a fuzzy-tree advantage, feature discovery, open-world evidence
validation, calibrated confidence, unrestricted faithful prose, mature personality,
autonomous contemplation or broad generalization. The perfect registry-backed
clarification verifier and manually supplied feature are substantial experimental
assumptions. Statistical timing superiority is inconclusive, and the held-out set
is too small to estimate population accuracy.

**Smallest justified next experiment:** keep the same conditional-memory comparison,
but provide two conflicting attributed condition observations and require a bounded
independent verification step before resolution. Preregister fresh cases and the
acceptance policy. That tests the current idealized clarification boundary rather
than adding propagation solely to produce a difference.
