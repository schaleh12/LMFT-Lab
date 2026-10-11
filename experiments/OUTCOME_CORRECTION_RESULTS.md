# Outcome correction — evaluated results

Evaluated 2026-10-11 under the frozen [protocol](OUTCOME_CORRECTION_PROTOCOL.md).
[Implementation and commands](../docs/OUTCOME_CORRECTION.md). Raw source/config snapshots,
original messages, complete halted states, results and hashes remain in
`outputs/outcome-correction-001/`. This is a zero-inference deterministic study.
Historical reports, verifiers, teacher configurations, seed, equations and migrations
were not changed.

## Repair result

**371 tests passed**, including 47 new outcome tests and all 26 historical correction
tests. **766/766 experiment checks passed**, with 36 primary individuals and six
uninterrupted controls. All 42 individuals halted. No evaluated failure or criterion
change occurred. During test development, two atomic assertions compared in-memory
birth tuples to JSON lists; canonical JSON comparison fixed the tests without changing
storage behavior or acceptance criteria.

Enabled LMFT and ordinary structured memory produced identical effective evidence,
correction dispositions, scores, questions and semantic outgoing responses. The
existing ledger/authorization transaction is shared; only the numerical projection
implementation differs. LMFT replays active roots through `judgment.apply_validated`,
while memory independently sums their signs. Neither uses propagation in this study.
The result demonstrates remembered evidence repair and consequent behavior, not a
fuzzy-reasoning advantage, prediction improvement or an LLM teaching effect.

| Primary condition (12 scenarios each) | Accepted / rejected | Effective outcomes | Stored ledger records | Changed scores / categories |
| --- | ---: | ---: | ---: | ---: |
| LMFT correction enabled | 10 / 9 | 31 | 42 | 9 / 8 |
| Correction disabled | 0 / 19 | 31 | 32 | 0 / 0 |
| Ordinary structured memory | 10 / 9 | 31 | 42 | 9 / 8 |

The 31 independent outcomes comprise 19 shielded and 12 unshielded events. One
additional non-outcome annotation in o7 makes 32 original ledger roots. It never
contributes to score or outcome count. Each accepted replacement adds one immutable
stored version and zero independent events. Ten accepted corrections affect nine
roots; o11's second correction is a same-sign reference attestation on the latest
head. Its ancestry is original → replacement/o11-a → replacement/o11-b, with one
active contribution throughout.

## Exact correction policy and cases

Originals are exact members of a separately versioned instrument LOG, which permits
measurement error. They are provisionally scored reports, not independently proven
facts. Full operation hashes in `config/outcome_correction_authority.json` authorize
the named curator; the submitted role name alone grants nothing. Eligibility requires
an existing active outcome head and matching digest, stable event/scope/branch/procedure/
payload, and a fresh replacement identity. Independent registered reference data then
checks the replacement schema, exact integer types and output. Invalid proposals may
have authorization yet fail eligibility or verification. There is no rebasing or
last-write-wins policy. Rejections retain their inputs and reasons without changing
effective evidence, caches or questions.

| Scenario | Enabled shielded score | Behavioral result |
| --- | --- | --- |
| o1, success → failure | +1/3 → -1/3 | success → failure |
| o2, failure → success | -1/3 → +1/3 | failure → success |
| o3, score-only repair | 2/3 → 1/3 | remains success; now conflicting/unresolved |
| o4, residual conflict | 1/3 → 0 | success → abstain; conflict remains |
| o5, unauthorized | -1/3 unchanged | rejected before reference lookup |
| o6, wrong or Boolean output | -1/3 unchanged | two authorized verification rejections |
| o7, missing / moved-branch / annotation target | -1/3 unchanged | three eligibility rejections |
| o8, duplicate deliveries | -1/3 → +1/3 once | ten repeats add no learning |
| o9, conflicting correction ID | -1/3 → +1/3 once | conflicting second payload rejected |
| o10, stale target and digest | -1/3 → +1/3 once | two stale proposals rejected |
| o11, valid chain | -1/3 → +1/3 → +1/3 | all ancestors retained; no extra event |
| o12, restart and fresh cases | 0 → 1/2 | abstain → success; consistency request closes |

Every untouched unshielded branch remains at +1/3. Disabled acceptance retains all
original scores. Its later stale/chain rejection reasons can differ because no prior
replacement was installed; inputs and authority/reference access were matched.

## Caches, uncertainty and persistence

Affected warm caches invalidated; other-branch caches and subsequent cache hits remained
valid. Semantic results, rather than cached prose, determined outgoing wording. o12's
warm question closed only after both effective signs became positive. o4 remained
mixed and unresolved. o3 became mixed despite still predicting success. Enabled
conditions each ended with six open questions (warm and two fresh cases for o3/o4)
and one closed question (o12); disabled ended with six open questions (o4/o12), none
closed. This is at most one request per case, not one per scenario.

The resolution criterion is the new fixture's frozen nonempty/uniform-sign convention.
It does not establish calibrated confidence or override historical question criteria.
Same-sign chain attestation changes provenance but not score or certainty.

Every primary individual was actually halted and restarted after repair. Exact restored
states matched, including originals, reasons, lineage, counts, caches and questions.
Uninterrupted o11/o12 controls in all three modes matched judgments, question state and
all semantic outbox messages (timestamps excluded). Atomic fault tests before and after
checkpoint replacement recovered the complete old or new transaction, with replay
without double learning. Runtime inspection was refused while live; diagnostics were
read only after halt. No historical checkpoint was rewritten or migrated.

## Prediction quality, separately

Each scenario had two held-out payloads, 31 and 47, distinct from training and warm
inputs. Their authored opposite outcomes deliberately prevent a branch-constant
judgment from being correct on both. Branch labels were supplied; context recognition
was not learned. Hidden outcomes were accessed only by the evaluator.

| Condition | Correct / decided | Abstentions | Accuracy among decisions | Coverage |
| --- | ---: | ---: | ---: | ---: |
| Enabled LMFT | 11 / 22 | 2 | 50% | 91.67% |
| Disabled | 11 / 22 | 2 | 50% | 91.67% |
| Memory | 11 / 22 | 2 | 50% | 91.67% |

Enabled conditions abstain on o4; disabled abstains on o12. Several prediction signs
change, but aggregate accuracy and coverage do not improve. Successful correction
of a recorded event does not establish a better general predictor. These 24 synthetic
cases support no broader generalization claim.

## Time and storage

Totals below cover the 12 primary individuals per condition. Processing time is measured
inside `advance`, excluding checkpoint writes, polling, startup and shutdown. These
single-run timings are descriptive, not performance benchmarks. Model calls: **zero**
in every condition; the handler uses no model and produces authored wording.

| Condition | Processing seconds | Final checkpoint bytes | Individual-directory bytes |
| --- | ---: | ---: | ---: |
| Enabled LMFT | 0.148037 | 735,071 | 821,982 |
| Disabled | 0.143716 | 716,958 | 803,866 |
| Memory | 0.140727 | 693,944 | 780,854 |

From the pre-correction stage to final halt, total checkpoint growth was 235,698 bytes
for LMFT, 217,444 for disabled and 233,473 for memory. Final recomputation audit counts
were 41 / 31 / 41 respectively; all had 194 receipts and 184 deliberate outbox records.

The smaller baseline checkpoints omit LMFT's derived per-sample replay traces. Both
retain full original/accepted/rejected provenance. Stage-by-stage record counts, wall
time and byte counts are in `results.json`; individual-directory totals include inbox
and lifecycle files but exclude the extra archive and halted snapshot copies.

For o8, five exact deliveries plus five new-ID copies of the same correction added no
ledger entries, heads, corrections, recomputations, questions or score increase. Each
condition added 11 receipts, six processed IDs and one outbox message, including the
explicit final barrier. Checkpoint growth was 2,658 bytes in LMFT/memory and 2,659 in
disabled; corresponding individual-directory growth was 10,540 / 10,540 / 10,541 bytes.
Thus scientific state stayed fixed while delivery bookkeeping and raw inputs grew.
This remains a whole-history checkpoint system with unbounded long-run storage cost;
no consolidation was implemented or inferred.

## Limits and next bounded step

All preregistered checks passed. Prediction improvement and fuzzy superiority were not
demonstrated; real-world repair reliability remains untested. The suite uses synthetic
reports/reference data, exact-operation permits and a cooperative single host. It does
not establish production authentication, hostile-host resistance, cross-branch repair,
learned verification criteria, model comprehension, power-loss durability or large-scale
memory efficiency. Teacher capability remains available but unchanged and unused.

The smallest next experiment is one new, independently verified contrary outcome after
a correction and restart. Freeze its expected score/probe beforehand and compare memory:
verify that repaired provenance does not freeze the judgment or prevent later ordinary
evidence from changing it. No new equation or autonomous loop is needed. That follow-up
is proposed, not implemented here.

## Reproduction and preserved evidence

Protocol SHA256: `c7fcf50edbe8baddf28a2e120a2393c0f33967a47424f4ed014699e3d1fa0819`.
Authority config SHA256: `d3ad0c4683668d1169f28eccde8ba730add1107263fc79e137a8795315d8a446`.
All archived source/config/protocol hashes matched evaluated files after the run. The
archive also preserves historical result reports and the pre-completion handoff.
Raw evidence is local under ignored `outputs/outcome-correction-001`; it is not included
in Git or an external archival service. Preserve that full directory for replay.

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_outcome_correction.py --output outputs/my-outcome-correction
```

Use a fresh output path. The runner refuses overwrite and retains failed evaluated runs.
No runtime source/config changed after this evaluated snapshot; only documentation was
completed afterward. Historical reports retain their original claims and dates.
