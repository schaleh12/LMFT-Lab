# Correction without erasure — evaluated results

Evaluated 2026-10-11 under the frozen [protocol](CORRECTION_PROTOCOL.md).
Implementation and commands: [correction guide](../docs/CORRECTION_EXPERIMENT.md).
Raw evidence, checkpoints, configuration, source snapshots, hashes and results are retained
in ignored `outputs/correction-001/`. Historical studies and their failures remain unchanged.

## Outcome

All **286 tests** passed (including 26 correction tests); **595/595 evaluated checks** passed.
The evaluated run used 36 primary individuals (12 cases × three conditions) and three
uninterrupted chain controls. Actual processes halted and restarted; no model was called.
No evaluated failure prompted a change to the protocol, mapping or acceptance criteria.

Correction-enabled LMFT and ordinary structured memory produced identical acceptance,
prediction and request results. Effective evidence repair caused behavioral changes;
this study provides no measurable advantage for fuzzy propagation. Propagation consumes
the repaired support through the unchanged consistent-support mapping; it does not authorize,
verify or apply corrections. The canonical seed, numerical equations, fixed routes,
migration behavior and prior outcome counters were preserved.

## What was corrected

Initial admission certifies a registered instrument log, which deliberately contains errors;
it does not certify objective truth. This new fixture policy does not weaken historical
truth-based verifiers. Trusted configuration permits exact correction payloads. Sender and
payload must match that permit; eligibility then requires an active target, exact digest
and unchanged scope/coordinate. Independent reference verification checks the proposed
replacement only. Some permitted proposals deliberately fail those later checks.

Original observations remain immutable. An accepted correction appends a replacement and
an audit event, advances the root's active head and retains ancestry, source, reasons and
before/after references. The effective view contains one head per independent root.
Across each enabled condition, 36 original scoped roots remain 36 roots, while stored
observations grow to 47 through 11 accepted replacements. Two-step chains do not add samples.
There are separately eight unchanged prior outcome samples per individual (96 per condition).

Only scoped observations are correctable. Repair selects or withholds an existing conditional
judgment; it does not revise the prior outcome counters. Their scores remain ±1/3 under
sum(signs)/(n+2). Outcome-evidence correction remains unimplemented.

## Matched comparisons

All conditions received identical evidence and correction batches, authority policy,
verification procedure and one-request lifetime budget per case. Routes remained
A=.25/B=.75/D=.5. Memory uses the existing transparent selector instead of propagation.
The disabled control validates proposals but refuses acceptance. Later chain targets can
therefore be nonexistent in that control; this is a consequence of disabling the first repair.
Model settings and budgets are identical: zero calls.

| Measure across 12 cases | LMFT | Correction disabled | Ordinary memory |
| --- | ---: | ---: | ---: |
| Accepted / rejected correction attempts | 11 / 8 | 0 / 19 | 11 / 8 |
| Decisions / correct / abstentions | 7 / 6 / 5 | 3 / 1 / 9 | 7 / 6 / 5 |
| Accuracy on decided cases | 85.7% | 33.3% | 85.7% |
| Coverage | 58.3% | 25.0% | 58.3% |
| Verification requests / redundant | 10 / 0 | 9 / 0 | 10 / 0 |
| Questions closed / still pending | 5 / 5 | 0 / 9 | 5 / 5 |
| Effective scoped roots / stored observations | 36 / 47 | 36 / 36 | 36 / 47 |

These authored cases cover different decision subsets; percentages are not population
accuracy estimates. A useful request means a relevant unresolved question was identified,
not that an answer was obtained. No additional measurement was available for these requests;
corrections close some questions, while others properly remain pending. Corrections do not
refund spent requests. Enabled c2 adds the tenth request by exposing a new contradiction.

| Case | Enabled LMFT and memory: initial → final | Accepted / rejected | Interpretation |
| --- | --- | ---: | --- |
| c1 | abstain → success | 1 / 0 | Conflict removed; pending question closed |
| c2 | success → abstain | 1 / 0 | Conflict exposed; question reopened |
| c3 | success → failure | 2 / 0 | Both checks repaired; other conditional judgment selected |
| c4 | abstain → abstain | 1 / 0 | Missing second check still prevents closure |
| c5 | abstain → abstain | 0 / 1 | Claimed authority is insufficient |
| c6 | abstain → abstain | 0 / 2 | Authorized wrong value and malformed replacement rejected |
| c7 | abstain → abstain | 0 / 2 | Wrong scope and nonexistent target rejected |
| c8 | abstain → success | 1 / 0 | Repeated delivery adds no learning |
| c9 | abstain → success | 1 / 1 | Conflicting ID rejected; prediction nevertheless wrong |
| c10 | abstain → success | 1 / 2 | Competing inactive target and stale digest rejected |
| c11 | abstain → success | 2 / 0 | Two-event ancestry, same independent root |
| c12 | success → success | 1 / 0 | Irrelevant color repair leaves prediction/cache unchanged |

The disabled condition retained every initial prediction. Its c2/c3 successes were wrong;
c12 was correct. In the enabled conditions c9 remains a deliberate held-out failure:
correct evidence repair does not establish that the selected judgment predicts every outcome.
c3 corrections were batched before reevaluation; intermediate states remain in the audit.

## Integrity, communication and persistence

Passing checks cover original preservation, root counts, separate validation stages,
rejection invariance, stale targets/digests, conflicting IDs, chains, cache freshness,
question closure/reopening, fixed counters/routes and seed preservation. Rejection invariance
means effective evidence, cache and questions stay unchanged; rejection audits still grow.
First use of a correction ID is terminal, including rejection. Identical redelivery does not
create another correction; conflicting reuse records a rejected attempt.

Relevant accepted corrections invalidate affected semantic caches. Rejected and irrelevant
corrections preserve them. Fresh deliberate output reflects the current decision and
uncertainty; no saved prose is reused. Closed questions retain their closing correction ID
and spent budget. No inappropriate closure occurred, including after partial repair.

The live interface exposed deliberate outbox messages and lifecycle acknowledgments only;
live full-state inspection was refused. State and diagnostics were read after halt.
Every primary run had an exact-state restart check. The three uninterrupted c11 controls
matched restarted judgment and question state. Atomic-commit fault tests before and after
replacement recovered the appropriate complete state without partially applied corrections.
These deterministic fault tests are not a general hardware-durability guarantee.

## Cost and bounded repetition

Totals across the 12 primary individuals per condition, excluding the three uninterrupted
controls and archive copies. Wall time includes process/lifecycle overhead; core time is
instrumented processing. Single runs support descriptive comparisons only.

| Cost | LMFT | Correction disabled | Ordinary memory |
| --- | ---: | ---: | ---: |
| Wall seconds | 14.780 | 14.796 | 14.323 |
| Core processing milliseconds | 311.580 | 272.589 | 219.422 |
| Final checkpoint bytes | 1,574,556 | 1,259,891 | 835,032 |
| Final individual-directory bytes | 1,697,386 | 1,382,716 | 957,861 |
| SLM calls | 0 | 0 | 0 |

In c8, five new-ID deliveries plus five exact redeliveries and a barrier added 11 receipts,
six processed IDs and one barrier outbox acknowledgment per condition. They added zero
corrections, indexed correction IDs, observations, heads, questions, diagnostics or caches.
Judgments, evidence and request budgets were unchanged: no confidence or sample inflation.
Checkpoint growth was 2,673 bytes for LMFT and 2,674 each for disabled and memory.
Raw inbox and receipt retention still consume storage; no consolidation was implemented.
Per-stage counts, storage and timings are retained in `results.json`.

## Limits and next experiment

The public synthetic permit list is an exact-operation bearer capability, not human identity
authentication. Someone able to replay a permitted message can exercise it. First-use public
IDs are not denial-of-service resistant. Host edits are outside the boundary. New authority
policy requires new experimental state under the pinned source/config compatibility check;
this is not live permission administration.

Verification is a bounded synthetic reference lookup, not discovery of real-world truth.
No model communication, autonomous contemplation or broad generalization was tested.
Authority and effective-view bookkeeping are ordinary algorithms and work equally in memory.
The evidence supports correction integrity and these particular behavioral consequences,
not fuzzy superiority or independently acquired cognitive ability.

The smallest next experiment is to correct one mistaken prior outcome sample, then recompute
the unchanged judgment equation from effective outcome roots. Compare ordinary memory again,
checking changed score, reasons, cache and restart without counting a replacement twice.
That extension is explicitly outside this implementation.

## Frozen inputs

Protocol SHA256: `290b2ff0d17a9fc22e5acc279ba0b874fb1e7ac21c8042ce3e8d972e7c9b224f`.
Authority policy SHA256: `20233d4cfc3460d91ae0dd15d3293b853d1cebb348a14c4e45aa56e740ac99cc`.
`archive-manifest.json` records the remaining source, tests, configuration and historical
result hashes. The evaluated archive is retained locally under `outputs/correction-001/`.
