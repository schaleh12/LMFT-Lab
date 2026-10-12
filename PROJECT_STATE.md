# LMFT-Lab — current project state

Snapshot: **2026-10-12**. Inspected source commit:
`c097c987f221703b856e29d2f0c76a3935087c84`.
The working tree was clean before this documentation-only handoff. This identifies the
inspected state, not a future documentation commit. Recheck Git status in each session.

Read [AGENTS.md](AGENTS.md), this snapshot, then relevant [DECISIONS.md](DECISIONS.md)
entries. These files summarize; [Minimal Specification](docs/MINIMAL_LMFT_SPEC.md) controls
V0.1 contracts, [Runtime Specification](docs/LMFT_RUNTIME_SPEC.md) describes numerical and
runtime proposals, and dated experiment reports own their findings. Use the
[documentation index](docs/INDEX.md) for topic-specific sources.

## Purpose and stage

LMFT investigates persistent conceptual structures developing through evidence and language-model
interaction. This is an early experimental hypothesis, not demonstrated general cognition.
The owner-approved 40-node seed is frozen; developmental judgments and relationships remain
separate. See [concept](docs/LMFT_CONCEPT.md) and decisions D001–D004.

## Implemented capabilities

- Canonical birth, explicit limited legacy conversion, direct activation and bounded propagation:
  [birth](src/lmft_lab/birth.py), [migration](src/lmft_lab/migration.py),
  [activation](src/lmft_lab/activation.py), [propagation](src/lmft_lab/propagation.py).
- Supervised inbox/outbox, atomic checkpoints, deduplication, restart and post-halt inspection:
  [runtime guide](docs/INTERACTIVE_RUNTIME.md), [runner](src/lmft_lab/runtime.py),
  [store](src/lmft_lab/runtime_store.py). While live, expose only deliberate outbox messages
  and lifecycle acknowledgments; inspect internal state after halt.
- Fixture judgments, contextual lookup, bounded attention/route experiments, correction lineage
  and continued outcome learning: [index](docs/INDEX.md), [contextual code](src/lmft_lab/contextual.py),
  [correction](src/lmft_lab/correction.py), [outcome projection](src/lmft_lab/outcome_correction.py).
  [Continuation results](experiments/CONTINUATION_RESULTS.md) show revision after correction/restart,
  not improved prediction. Some admitted instrument logs remain revisable, not independently proven truth.
- Pinned local model assets and proposal processing: [setup](docs/LOCAL_MODELS.md),
  [asset layer](src/lmft_lab/model_assets.py). The supervised
  [teacher adapter](src/lmft_lab/teacher_adapter.py) and independent
  [lesson assessment](src/lmft_lab/teacher.py) exist. The
  [teacher briefing report](experiments/TEACHER_BRIEFING_RESULTS.md) records one accepted constrained
  route lesson after four offline calls, with ordinary-memory equivalence. Broader teacher
  reliability and general understanding remain unproven.
- Bounded relationship induction: [capacity guide](docs/CAPACITY_EXPERIMENT.md),
  [state/acceptance code](src/lmft_lab/capacity.py),
  [finite language/selector](src/lmft_lab/capacity_relations.py). No generated executable proposals.

## Latest completed milestone

The [capacity protocol](experiments/CAPACITY_PROTOCOL.md) and
[results](experiments/CAPACITY_RESULTS.md) record training selection of `length <= capacity`
from six predefined candidates, followed by separate validation before acceptance.
The accepted relationship transferred to six unseen combinations and six evaluated range-shift
cases; all sixteen in-scope probes were correct. Exact-pair lookup answered only four seen pairs;
the balanced aggregate counter abstained. Equally equipped ordinary memory matched LMFT.
Seed activation had no causal role; the experiment used **zero model calls**.

**Reported results, not rerun for this handoff:** 413 passing tests, 155/155 integrity checks,
40/40 quality checks; restarted and uninterrupted states/predictions matched.
The supplied vocabulary and hypothesis family contain the correct rule. This is finite
hypothesis selection, not autonomous feature discovery, general understanding or fuzzy superiority.

## Limits and next task

No autonomous contemplation loop, general constitutional enforcement, calibrated confidence,
or broad real-world agency is established. The capacity study is noiseless and tightly scoped;
it has one selection/acceptance lifecycle, no interactive acquisition of missing evidence and
no revision of an already accepted relationship. Ambiguity handling is unit-tested, not yet
an interactive result. Whole-history checkpoints grow with history; old individuals require
archived source/config under the existing manifest guard.

Active implementation work: **none recorded**; this handoff is documentation-only.
Next concrete task (**proposed, not implemented**, D009): preregister training that leaves
`<` versus `<=` ambiguous, then test selection and use of at most one verified equality
observation. Match evidence/request budgets with equally equipped memory and a no-new-evidence
control; reserve fresh validation and held-out equality/non-equality cases. Do not default to
`<=` or use held-out labels to break ties. See the capacity report's next-experiment rationale.

## Verification and local evidence

From the repository root in PowerShell, when implementation verification or a new run is needed:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_capacity.py --output outputs/my-capacity-study
```

Use a fresh output path. Model setup/reproduction is separately documented in
[LOCAL_MODELS.md](docs/LOCAL_MODELS.md) and [LOCAL_TEACHER.md](docs/LOCAL_TEACHER.md).

Reports locate complete local runs under `outputs/`, notably `capacity-001/`, `continuation-001/`,
`outcome-correction-001/` and `teacher-briefing-001/`. This handoff checked those directories,
results summaries, manifest-file presence and checkpoint counts; it did **not** verify every
archive file/hash or reproduce the experiments. No external backup was verified.
[.gitignore](.gitignore) excludes outputs, logs, virtual environments, local caches, weights
and credential files; these are not conveyed by a Git checkout. Default model cache is
`%LOCALAPPDATA%/LMFT-Lab/cache`; its assets were not inspected in this task.

Checks run for this handoff: source/report review, Git status/commit inspection, local archive
presence/summary checks, changed-document link validation and documentation diff review.
No tests, inference, downloads or experimental runs were performed.
