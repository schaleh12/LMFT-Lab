# Unsupported hypothesis family — results and runtime assessment

Evaluated 2026-10-12 under the [frozen protocol](INSUFFICIENCY_PROTOCOL.md).
Protocol SHA256: `1cb49361efc3d33249f75aaa01d40b0d06836aefd4bbd350f2ec710182852369`.
Actual clean starting commit `5e45ab365688c7b0b0ac246fd8e7db558e509704`; the existing
ambiguity work had been committed before this cycle. The handoff snapshot still
described it as uncommitted, so actual Git/source provenance takes precedence.
This insufficiency study is uncommitted. Prior handoff/ambiguity files were copied
into `outputs/insufficiency-prework-001/`; all 134
protected prior file hashes still match, including the previous ambiguity implementation,
protocol/results, seed, numerical mechanisms, migration and model configuration.
Handoff documents were updated separately; their pre-cycle versions are in prework.

**The learner retained an explicitly empty set when verified training contradicted
every comparison. It distinguished that from ambiguity and abstained across restart.
Equally equipped ordinary memory matched exactly.** There were zero model/mock calls,
zero acquisition requests, no teacher repair and no additions to the candidate space.

## Authored mechanism and evidence assumptions

[Fixture](../src/lmft_lab/insufficiency_fixture.py),
[study](../src/lmft_lab/insufficiency.py), [harness](run_insufficiency.py),
[regression tests](../tests/test_insufficiency.py).

The new procedure `capacity-blocked-two-1` refuses length-two payloads, otherwise
using the original bounded-write simulation. The original capacity-transmit-1 task
and its findings are unchanged. The six comparison operators and numeric features
are unchanged; no fault/context feature is introduced. Their numerical dispatch is
reused under an explicitly separate scope, not by mislabeling new device evidence
as historical capacity evidence. Case/scenario IDs are provenance, never inputs
to the comparison function. Neither selection nor prediction can call the verifier.

The developer authored the task, case registration/splits, vocabulary, exact verifier,
zero-error filtering, validation gate, support-status vocabulary, consensus policy,
persistence and tests. Evidence determines the retained subset. All accepted facts
retain source, record digest and verification reason separately from hypotheses.
All rejected submissions retain their original record/source and reason.

The verifier is authoritative only inside this noiseless synthetic task. Its exact
observations may eliminate these deterministic candidates. This does not establish
that real-world contradictions always invalidate theories. An empty set identifies
no supported member of this supplied family; it does not identify inadequate
vocabulary, missing context or erroneous evidence as the cause. The fault is known
to the external experiment author, not inferred or represented by the learner.

## Training elimination and invalid-input isolation

Unsupported training labels for t1=(1,3), t2=(4,2), t3=(2,4), t4=(3,3) were
true, false, false, true. Every candidate has at least one recorded error:

| Candidate | Verified training contradiction refs |
| --- | --- |
| lt | t3, t4 |
| le | t3 |
| eq | t1 |
| ge | t1, t2 |
| gt | t1, t2, t4 |
| ne | t2, t3, t4 |

The surviving set is exactly `[]`, with support status `no_supported_hypothesis`.
Fresh validation is recorded but cannot restore a rejected rule; acceptance is
false with the same reason, not vacuously true over zero checks. Predictions contain
no votes and abstain with that explicit reason. Ambiguous controls retain lt/le and
use `hypothesis_disagreement` where votes differ; supported controls retain le.

Before true training, every condition rejected a false asserted label, wrong source,
Boolean/non-Boolean schema violations, wrong features, executable proposal,
held-out attempt and wrong scenario. None entered evidence or candidate errors.
After true training, a conflicting identity rejected while preserving the original.
Each final state contains nine rejected inputs, two duplicates, four training facts,
four validation facts, eight provenance records and six candidate derivations.
Exact repeats count once; rejection traces are not treated as evidence.

## Quality, including expected negative results

Each row applies identically to LMFT and ordinary memory, which share all evidence,
space, policy and validation. Only LMFT stores the unchanged inert 40-node birth.

| Scenario | Surviving set | Validation acceptance | Equality correct/decided | Non-equality correct/decided | Overall coverage | Accuracy among decisions |
| --- | --- | --- | --- | --- | --- | --- |
| Unsupported | empty | No | 0/0; 4 abstain | 0/0; 4 abstain | 0% | Undefined |
| Supported control | le | Yes | 3/4 | 3/4 | 100% | 75% (6/8) |
| Ambiguous control | lt,le | Yes | 0/0; 4 abstain | 3/4 | 50% | 75% (3/4) |

The supported control is supported by its admitted evidence, not proven to explain
the entire device. It fails h2=(2,2) and h5=(2,5). Ambiguous consensus also fails h5.
Those errors were preregistered and preserved. Held-out outcomes were scored only
after all six prediction sets were frozen, and never enter learning or acceptance.
All conditions return out_of_scope on x1. Blanket abstention fails both controls.
No fallback, teacher repair, candidate resurrection or post-hoc criteria change occurred.
Seed activation and fuzzy propagation have no causal role and no LMFT advantage is claimed.

## Verification, inspection and reproduction

**461 tests passed** (28 new insufficiency tests). Primary run and separate local
reproduction each passed **137/137 integrity checks** and **18/18 quality checks**.
Six conditions checkpoint after training selection and after validation; all twelve
stage checkpoints per run are loaded in distinct Python processes. Validation
continues from the persisted training checkpoint, not solely an in-memory object.
Full state digests, explicit sets/statuses, all rejection reasons and predictions
match uninterrupted references. Evaluation preserves exact checkpoint hashes/bytes.
Tests cover rejection before oracle access, verifier mismatch, duplication, nonvacuous
acceptance, immutable selected sets, validation failure, closed/incomplete phases,
oracle isolation, source/config/archive/checksum guards, read-only probes and seed
independence. The complete suite also runs historical behavior regression tests.

After the primary run, inspected the protocol, source, per-candidate derivations,
all six result groups, unsupported admission/rejection records and provenance. Then
reran the SAME fixed deterministic study in `outputs/insufficiency-reproduction-001/`.
This is a fresh local reproduction by this assistant, not an independent investigator.
A separate archive inspection checked all 24 checksummed stage states across both
runs; scientific states and frozen predictions match exactly across runs. Both
source/config/protocol/archive guards and all 134 protected-file hashes pass.
The coordinator's independent review/reproduction remains separately attributable.

Completed commands (PowerShell, repository root):

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest tests/test_insufficiency.py -q --basetemp outputs/insufficiency-tests-001
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/insufficiency-regression-001
.\.venv\Scripts\python.exe experiments/run_insufficiency.py --output outputs/insufficiency-001
.\.venv\Scripts\python.exe experiments/run_insufficiency.py --output outputs/insufficiency-reproduction-001
```

The targeted invocation passed all 28 tests. The full 461-test run followed a focused
harness improvement to continue validation from persisted training. No frozen criterion
or task changed. Choose fresh output AND test-temp paths when reproducing; study
outputs refuse reuse. Test runs also retain their isolated study archives under temp
directories. No evaluated failure occurred. Raw outputs are ignored by Git and no
external backup was verified.

Exact paths beneath EACH completed run directory:

- `archive-manifest.json`, `archive/`: evaluated source/tests/config/protocol and hashes.
- `configuration.json`, `provenance.json`, `protected-hashes.json`: frozen cases/space/scope, Python/Git/working-tree identity, protocol hash, zero calls and preservation evidence.
- `frozen-predictions.json`, `results.json`: all frozen predictions, followed by per-case/groups scoring and all checks.
- `<mode>-<scenario>/training/checkpoint.json`: selected sets, six error derivations, verified training provenance and all nine rejection reasons.
- `<mode>-<scenario>/final/checkpoint.json`: persisted validation, same selected set/status, acceptance and evidence/provenance/trace.
- `<mode>-<scenario>/<stage>/restart-result.json`: actual restart PID, state digest, explicit sets/statuses, rejection trace, fresh predictions and checkpoint-invariance check.
- `<mode>-<scenario>/<stage>/uninterrupted-state.json`, `uninterrupted-predictions.json`: complete reference state/behavior.

Modes: lmft,memory. Scenarios: unsupported,supported,ambiguous. Stages: training,final.
No existing archive, previous study or uncommitted implementation was overwritten.

## Smallest supervised-runtime integration step — assessment only

The [capacity handler](../src/lmft_lab/capacity.py) already receives explicit
`outcome/select/accept/evaluate` operations through [runtime](../src/lmft_lab/runtime.py),
with envelope/message deduplication, atomic checkpoints, learning control, outbox
communication and post-halt inspection. Its original policy stores only a uniquely
selected accepted relationship. [Ambiguity](../src/lmft_lab/ambiguity.py) adds a retained
set and feature-driven one-observation selection, but is currently a standalone harness.
This study adds explicit empty-family reasons and nonvacuous consensus/acceptance.

The smallest useful integration is a NEW opt-in supervised relationship-set mode,
initially passive: registered verified outcomes, explicit training close, retained
set with derivation/status, all-set validation, then read-only consensus probes and
outbox explanations of unsupported versus ambiguous evidence. Store it only under
the existing separate developmental judgment. Reuse the existing runtime lifecycle
and transaction boundary; keep original capacity mode/archive semantics intact.
Do not begin with an autonomous loop, a teacher repair path or numerical changes.

That step would require bounded changes to mode registration/initialization,
operation-envelope routing, the handler and CLI/probe dispatch. Freeze a task/verifier
policy in the software manifest, honor learning-disabled controls, and test atomic
state/output/cursor commits and restart under runtime messages. After this passive
boundary is established, ambiguity's acquisition could become an explicit outbox
verification request linked to a selected feature record; replies would need exact
request identity, one-observation budget, independent admission and phase closure.
That request bridge is a later integration step, not part of the proposed minimum.

Risks: existing source-wide manifests reject new-source restarts, so old individuals
must retain archived software rather than silently migrate; direct fixture source
labels are not real-world authentication; accepted sets do not guarantee a correct
family or complete context; ambiguity and unsupported states must not be collapsed
into one generic uncertainty string; unverified replies must not filter hypotheses;
validation/evaluation must not become fallback training; delivery/message versus
evidence deduplication and budget commits must stay atomic; accepted-set revision
needs a separately specified lifecycle. Shared memory parity and inert seed results
still apply. No integration code was changed and no additional study was dispatched.
