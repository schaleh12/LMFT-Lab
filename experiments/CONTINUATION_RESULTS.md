# Fresh learning after correction and restart — results

Evaluated 2026-10-12 under the frozen [protocol](CONTINUATION_PROTOCOL.md).
[Commands and implementation](../docs/CONTINUATION_EXPERIMENT.md). Complete inputs, source/config
snapshots, checks, halted states and traces are retained in `outputs/continuation-001/`.

**Corrected judgments remained revisable after actual restart.** The existing outcome
admission/projection mechanism already supported continuation. Production changes were
limited to an opt-in, birth-pinned control that freezes new outcome admission after an
accepted correction. Correction policy, fixture, numerical rules, seed, routes, migration,
teacher configuration and historical reports were unchanged. No models were invoked.

## Exact results

All values below are shielded branch values; counts exclude the separate unshielded branch.
Each slash separates score and independent count, not a new formula. Expected values were
specified as rational numbers independently of the implementation. Observed values matched
at every stage, including the inclusive +1/5 and -1/5 thresholds.

| Scenario | Initial score; count | After correction | Subsequent independent evidence: expected = observed |
| --- | --- | --- | --- |
| Crossing (o2) | -1/3; 1 | +1/3; 1, success | failure: 0; 2, abstain → failure: -1/5; 3, failure → success: 0; 4, abstain |
| Same category (o12) | 0; 2 | 1/2; 2, success | failure: 1/5; 3, still success |
| Unresolved (o4) | 1/3; 4 | 0; 4, abstain | failure: -1/7; 5, abstain → success: 0; 6, abstain |

The corrected original event always contributed once. Its old version and accepted
replacement remained immutable, with the same head/parent/root ancestry. New events were
unused registered IDs (o8/event-1, o9/event-1, o3/event-2 as specified); each added exactly
one independent contribution. These are registered instrument-log reports under the existing
admission policy, not newly established sensor truth or teacher assertions. The experiment
reuses their common batch/procedure/branch; scenario prefixes are event identities, not
additional learned contexts. In particular, o8/o9 originals are themselves correctable
reports in the historical fixture. This study uses their admitted negative outputs without
new reference validation; it establishes responsiveness to eligible reports, not that those
new reports are objectively accurate. Subsequent repair of them remains possible.

| Condition, three scenarios each | New admitted outcomes | Final independent outcomes | Ledger versions | Rejected input deliveries |
| --- | ---: | ---: | ---: | ---: |
| Corrected LMFT, restarted | 9 | 19 | 22 | 9 |
| Corrected LMFT, uninterrupted | 9 | 19 | 22 | 9 |
| Ordinary memory, restarted | 9 | 19 | 22 | 9 |
| Corrected LMFT, later learning frozen | 0 | 10 | 13 | 33 |

Nine new outcomes comprise six shielded and three unshielded events across scenarios.
Every condition accepted the same three corrections and retained their ancestry. The frozen
control retained corrected scores/counts (+1/3,1), (1/2,2), (0,4). Its extra rejections include
new-ID deliveries of events it never learned; those cannot be labeled evidence duplicates.
The first five exact-message redeliveries per scenario still deduplicated in every condition.

## Lifecycle, identity, scope and questions

**387 regression tests passed**, including 16 new continuation cases; the improved manifest
control test and all 16 continuation cases also passed in a targeted rerun. **450/450
preregistered experiment checks passed.** All 12 individuals halted. No evaluated failure,
criterion change, post-result numerical tuning or hidden model execution occurred.

Restarted LMFT, memory and frozen control each halted after correction, performed a no-input
restart/halt with exact state equality, then restarted before receiving new evidence.
Uninterrupted LMFT had no intermediate halt. Final LMFT judgments, questions and semantic
outbox records matched exactly between restarted and uninterrupted runs (timestamps excluded).
Memory matched effective evidence, questions and all semantic outgoing responses. Its simpler
projection omits LMFT's derived replay traces, so full raw judgment representation differs.
Both share the same correction/storage infrastructure. All live access stayed within deliberate
outbox and lifecycle acknowledgments; full inspection was refused until halt.

Five exact plus five new-message-ID repetitions of the first new outcome per scenario added
no effective evidence or recomputation. Conflicting content under the corrected original ID
rejected without restoring it. An attempted new evidence-ID alias for that original event
was unregistered and rejected. Every rejected input remains in inbox/receipt history. These
checks are bounded identity handling, not general provenance or anti-fraud validation.

An unused unshielded success raised only that branch from 1/3 with one sample to 1/2 with two;
its target shielded branch and cached target response stayed unchanged. A modified batch-2
report was rejected as unregistered. This demonstrates accepted branch isolation and rejection
of unsupported scope, **not** accepted learning across arbitrary batch scopes.

Eligible new target evidence invalidated its warm cache; immediate repeat evaluations hit.
Duplicate/conflict/scope rejection preserved semantic target results. Unshielded caches changed
only when unshielded evidence was admitted. Fresh wording reflected the current score/count,
category and support references, not a saved pre-correction sentence.

In o12, the initial consistency question closed at correction, then reopened on o8/event-1,
even though the score still predicted success at +.2. The spent question budget was not
refunded. o4 remained unresolved; no new evidence forced closure. Enabled conditions ended
with nine open questions (warm plus two fresh cases for each scenario). Frozen control had
three open questions in o4, one retained closed question in o12, and none in o2.
Atomic fault tests before/after new-outcome checkpoint replacement recovered the complete
old/new transaction, preserving correction ancestry and question state without double learning.

## Prediction quality is a separate result

The two fresh payloads31/47 per scenario were absent from admitted evidence and warm20 probes.
Their labels remained evaluator-only. As in the prior fixture, the two authored labels are
opposites within each supplied branch; branch-constant predictions cannot get both right.

| Condition | Correct / decided | Abstentions | Accuracy among decisions | Coverage |
| --- | ---: | ---: | ---: | ---: |
| Restarted LMFT | 1 / 2 | 4 | 50% | 33.33% |
| Uninterrupted LMFT | 1 / 2 | 4 | 50% | 33.33% |
| Ordinary memory | 1 / 2 | 4 | 50% | 33.33% |
| Frozen subsequent learning | 2 / 4 | 2 | 50% | 66.67% |

Continued revision decreased coverage, with unchanged conditional accuracy. Correct evidence
handling produced appropriate uncertainty under the fixed rule; it did not improve prediction.
No propagation participates here and no fuzzy advantage is demonstrated. Six synthetic probes
per condition cannot support broader generalization claims.

## Resources and preservation

| Condition | Measured processing seconds | Final checkpoint bytes | Growth since corrected checkpoint |
| --- | ---: | ---: | ---: |
| Restarted LMFT | 0.100995 | 268,224 | 116,528 |
| Uninterrupted LMFT | 0.094991 | 268,231 | no interim snapshot |
| Ordinary memory | 0.094099 | 243,430 | 105,039 |
| Frozen control | 0.102165 | 253,839 | 102,016 |

Times sum transition computation only, excluding checkpoint writes and lifecycle waits;
these single runs are not performance benchmarks. Timing fields explain small byte differences
between restarted/uninterrupted checkpoints. Per-stage counts and individual-directory bytes
are in results.json. Repetition adds receipts/inbox storage even with no learning. Zero model
calls in every condition. Whole-history storage limitations and cooperative-host assumptions
remain; no consolidation, production authentication or power-loss durability was added.

Protocol SHA256: `37697f99898fc0f918f26c1284dbc4f8a34202676cb9fbf2f23b5287f0ce3def`.
All source/config/protocol snapshot hashes matched after execution, before documentation
completion. Raw runs are ignored by Git under `outputs/continuation-001/`; preserve the complete
halted directory for durable replay. Historical results were not overwritten. The harness
refuses existing output paths and records failures without changing criteria.

## Next substantive bottleneck and one proposed experiment

The current predictor pools all eligible observations in a supplied branch and emits one
judgment regardless of payload. It retains payloads but does not condition on a property
that explains different outcomes within the branch. The deliberately opposite held-out labels
expose that limit; they do not establish that a particular missing physical cause has been
identified. More reliable ancestry or stronger activation cannot supply absent predictive
information or discover semantics by itself.

The earlier [contextual study](CONTEXTUAL_RESULTS.md) showed that an authored relevant condition
can improve over aggregation while matching competent conditional memory. The
[consistent-support study](CONSISTENT_SUPPORT_RESULTS.md) showed that external task relations
identify conflicts and activation can prioritize questions, without establishing improved
prediction. Together these results justify testing a relevant within-branch distinction,
not further bookkeeping as a proxy for learning.

Propose one bounded capacity experiment: a deterministic transmission simulator succeeds
only when payload length fits an independently recorded buffer capacity. Supply both observable
measurements and an explicitly authored `fits_capacity` distinction; learn success/failure
judgments from balanced verified outcomes within the same shielded branch. Keep the counter
and thresholds fixed. Compare branch-only LMFT, feature-conditioned LMFT and competent ordinary
conditional memory, with identical feature access, evidence, clarification budgets and zero
model calls. Include nuisance identifiers independent of outcome.

Preregister train/test splits with new payload contents and unseen length/capacity combinations
on both sides of the boundary, matched sample counts, restart checks, accuracy/coverage and
abstentions. A missing verified capacity should trigger bounded clarification or abstention,
not oracle access. Freeze the executable simulator and evaluator labels before training.
Feature-conditioned improvement over branch-only on those fresh cases would show the value
of the supplied predictive distinction; equal conditional-memory performance would again show
no LMFT advantage. Failure to improve or transfer must remain a negative result. Because the
distinction is authored, this would test conditional learning, not autonomous feature discovery.
This additional experiment is recommended only and has not been implemented.
