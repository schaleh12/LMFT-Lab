# Relationship ambiguity — evaluated results

Evaluated 2026-10-12 under [preregistration v1](AMBIGUITY_PROTOCOL.md).
Protocol SHA256: `9708cdfb393bdfdd19b727e26659995d79e069c0d9171b9f744196cfeb6b2ffc`.
Inspected clean starting commit: `0ae2461f078757c2cb2b0300a4591f327aaff381`.
Complete evaluated run: `outputs/ambiguity-001/` (ignored by Git).

One verified informative observation resolved the ambiguity; equally equipped
ordinary memory matched exactly. Non-informative, unavailable and no-evidence
controls retained uncertainty. No fuzzy propagation or LMFT advantage was established.

## Implementation and evidence

[Study module](../src/lmft_lab/ambiguity.py), [harness](run_ambiguity.py),
[tests](../tests/test_ambiguity.py). This is an isolated file-backed study using the
existing atomic Store and canonical constructor; it does not add a mode to the
supervised inbox/outbox runtime. LMFT stores the unchanged 40-node scaffold and
ordinary memory omits it. All scientific mechanisms and opportunities are shared.
Existing counters, activation, propagation, migration and model configurations are
unchanged. Zero model calls, including mocks; no Jev or teacher integration.

Supplied by the developer: six-candidate comparison vocabulary, exact features,
deterministic noiseless bounded-write verifier, split registration, disagreement
score, ordered tie policy, one-observation budget, all-survivor validation gate,
consensus/abstention policy and persistence harness. Learned from evidence: which
supplied hypotheses remain consistent. There is no autonomous feature discovery.
The numerical/fuzzy seed contributes nothing to selection or prediction; removing
the birth record in a test leaves predictions identical.

All conditions retained `lt` and `le` after the four non-equality training outcomes.
In the full candidate pool, q1=(0,2) and q4=(7,6) scored 0; q2=(5,5) and q3=(6,6)
scored 1. q2 won the declared-order tie, before any candidate outcomes were obtained.
The verifier reported success, eliminating lt and retaining le. Non-informative
selection spent its one observation on q1 and eliminated neither hypothesis.
The unavailable pool contained only q1,q4, so no informative request was possible;
it spent zero observations. The no-evidence control also spent zero.

Four fresh non-equality validation records checked EVERY surviving hypothesis.
They never selected or filtered hypotheses. Every retained set passed, including
the ambiguous sets. Facts remain separate registered outcomes; hypotheses remain
explicit comparison representations. Acceptance failure is tested to reject the
entire set without fallback, rather than using validation to break a tie.

## Quality and unresolved results

Each row applies identically to LMFT and ordinary memory. Accuracy is among
decisions; no equality decision means undefined accuracy, rather than zero.

| Policy | Resolved | Verified observations | Equality correct/decided (coverage) | Non-equality correct/decided (coverage) | Overall coverage / accuracy |
| --- | --- | ---: | --- | --- | --- |
| Disagreement | Yes: le | 1 | 4/4 (100%) | 4/4 (100%) | 100% / 100% |
| Non-informative q1 | No: lt,le | 1 | 0/0 (0%; accuracy undefined) | 4/4 (100%) | 50% / 100% |
| Informative observation unavailable | No: lt,le | 0 | 0/0 (0%; accuracy undefined) | 4/4 (100%) | 50% / 100% |
| No new evidence | No: lt,le | 0 | 0/0 (0%; accuracy undefined) | 4/4 (100%) | 50% / 100% |

All conditions abstained on the out-of-scope probe. The controls' four equality
abstentions are substantive negative resolution results, preserved as expected.
Overall performance is not a claim that all cases were answered correctly.
The candidate family already contains the correct rule, and the simulator is
noiseless. Accuracy does not establish semantic understanding, real-world sensor
trust, broad extrapolation or calibrated uncertainty.

## Verification and exact artifacts

**433 tests passed**; **109/109 integrity checks** and **24/24 quality checks** passed.
Eight study conditions each have a restarted and uninterrupted reference. Restart
loads the persisted checkpoint in a distinct Python process and computes fresh
predictions there. Process IDs, restored state digest, predictions and checkpoint
hash invariance are recorded; uninterrupted states and predictions match exactly.
The entire eight-condition prediction table was frozen before held-out labels
were executed. Evaluation does not write the checkpoint or alter evidence,
hypotheses, acceptance, counters or seed. Source/config/protocol/archive guards pass.

Exact training repeats and acquired-outcome repeats are deduplicated without
spending budget. Conflicting identities, wrong source, malformed/executable proposals,
held-out admission and unselected/second acquisitions are rejected. Tests cover
invalid types/features, false outcomes, closed phases, changed training, whole-set
validation failure, source/config/archive drift, checksum corruption, feature-only
selection with oracle disabled, seed independence and actual subprocess persistence.

Under `outputs/ambiguity-001/`:

- `archive-manifest.json`, `archive/`: exact evaluated source, tests, config and protocol snapshots/hashes.
- `configuration.json`, `provenance.json`: cases, policies, budget, hypothesis space, scope, seed, Python/source identity and zero calls.
- `frozen-predictions.json`, `results.json`: all predictions followed by separate per-group scoring/checks.
- `<mode>-<policy>/checkpoint.json`: persisted birth (LMFT only), verified split evidence, initial/final hypotheses, acquisition votes/scores/selection, admission/rejection/filter traces, validation checks and acceptance.
- `<mode>-<policy>/restart-result.json`: actual restarted process PID, restored state digest, fresh predictions and checkpoint-invariance result.
- `<mode>-<policy>/uninterrupted-state.json`, `uninterrupted-predictions.json`: full reference execution for equivalence.

Modes are `lmft`, `memory`; policies are `disagreement`, `noninformative`,
`unavailable`, `no-evidence`. Checkpoints are 24,767–26,803 bytes for LMFT and
9,863–11,899 bytes for memory. The 14,904-byte difference is the inert scaffold,
not evidence of a computational or cognitive advantage. Timing was not a target.
Archives are local and ignored by Git; no external backup was verified.

## Reproduce and next proposal

PowerShell, repository root:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/ambiguity-regression-002
.\.venv\Scripts\python.exe experiments/run_ambiguity.py --output outputs/ambiguity-001
```

Those paths record the completed commands. Choose NEW output and test-temp paths
when reproducing; the study refuses existing output directories. The initial focused
test invocation using sandbox-default temp storage failed three atomic-replacement
checks with Windows permission errors (16 passed); a fresh writable-checkout temp
run passed all 19 then-current tests. After focused trace/training-guard additions,
the complete 433-test run passed. No protocol or quality criterion changed.

One proposed next experiment: a separately preregistered misspecified-family task
where verified training eliminates all six candidates; compare matched memory and
LMFT rejection/abstention across restart without broadening the vocabulary after
seeing outcomes. This is proposed only; no follow-on experiment was dispatched.
