# LMFT-Lab — current project state

Snapshot: **2026-10-12**. Clean starting source commit:
`5e45ab365688c7b0b0ac246fd8e7db558e509704`.
Ambiguity work was committed before this cycle; insufficiency implementation/handoff
changes remain uncommitted. The pre-cycle snapshot's uncommitted description was stale.
This identifies the starting state, not a future implementation commit. Recheck Git status.

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
- Isolated ambiguity study: [protocol](experiments/AMBIGUITY_PROTOCOL.md),
  [study code](src/lmft_lab/ambiguity.py), [results](experiments/AMBIGUITY_RESULTS.md).
  Retained hypothesis sets, one feature-selected verified observation, validation without
  tie breaking and read-only consensus predictions across actual process restart.
- Isolated hypothesis-family insufficiency: [protocol](experiments/INSUFFICIENCY_PROTOCOL.md),
  [study](src/lmft_lab/insufficiency.py), [results/runtime assessment](experiments/INSUFFICIENCY_RESULTS.md).
  Explicit empty versus ambiguous sets, no vacuous acceptance/consensus, traced rejected
  inputs outside evidence, two-stage actual restart and equally equipped memory parity.

## Latest completed milestone

The [insufficiency protocol](experiments/INSUFFICIENCY_PROTOCOL.md) and
[results](experiments/INSUFFICIENCY_RESULTS.md) test a NEW deterministic device fixture
that refuses length-two payloads. Verified training contradicts all six comparisons:
the learner retains `[]`, records `no_supported_hypothesis` and abstains on all eight
fresh in-scope cases. Supported le and ambiguous lt/le controls prevent blanket
abstention: respective coverage 100%/50%, accuracy among decisions 75%/75%.
Their preregistered device-fault errors are preserved. Ordinary memory matches exactly.
The new task does not change historical capacity truth. An empty set does not identify
why the family is insufficient or establish real-world theory invalidation.

Verified this cycle: **461 tests pass**, primary and fresh reproduction each
**137/137 integrity** and **18/18 quality** checks. Inspected 24 checksummed stage
states across both runs, with exact scientific-state/prediction parity; all 134
protected prior file hashes match. Zero calls; no seed/numerical/model/runtime edits.
Archives: `outputs/insufficiency-001/`, `outputs/insufficiency-reproduction-001/`;
pre-cycle handoff/ambiguity preservation copies/hashes: `outputs/insufficiency-prework-001/`.

### Previous ambiguity milestone

The [ambiguity protocol](experiments/AMBIGUITY_PROTOCOL.md) and
[results](experiments/AMBIGUITY_RESULTS.md) record lt/le surviving non-equality training.
Predicted disagreement selected one informative observation before outcome access; its
verified success retained le. LMFT and equally equipped ordinary memory matched exactly:
100% coverage/accuracy on eight fresh probes. Non-informative, unavailable and no-evidence
controls remained ambiguous: 0% equality coverage, 100% non-equality coverage, 50% overall
coverage and 100% accuracy among decisions. Validation checked sets without eliminating ties.
The seed was preserved and inert; **zero model calls**. This standalone file-backed study
does not integrate acquisition into the supervised runtime or change numerical mechanisms.

Verified in the prior ambiguity cycle: **433 passing tests**, **109/109 integrity checks**, **24/24 quality
checks**; eight distinct restarted processes matched uninterrupted state/predictions.
Complete source/config/protocol/evidence/restart traces: `outputs/ambiguity-001/`.
These are deterministic finite-family results, not fuzzy superiority or general cognition.

### Previous capacity milestone

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
its supervised runtime has one selection/acceptance lifecycle and no revision of an already
accepted relationship. The isolated ambiguity follow-up demonstrates bounded acquisition
and persistent hypothesis sets, not an autonomous runtime acquisition loop. Whole-history
checkpoints grow with history; old individuals require
archived source/config under the existing manifest guard.

Active implementation work: **none remaining in the authorized bounded cycles** (D009–D010).
The proposed misspecified-family study is now completed. Before another standalone study,
review the [supervised-runtime integration assessment](experiments/INSUFFICIENCY_RESULTS.md#smallest-supervised-runtime-integration-step--assessment-only):
smallest step is a NEW opt-in passive relationship-set mode using existing verified
outcome/select/accept/probe transactions, explicit empty/ambiguous status and atomic outbox
communication. Acquisition/request bridging comes later. This is assessment only;
no integration or further experiment was implemented/dispatched. Old source manifests,
verifier authority, phase isolation, deduplication and atomic budgets remain material risks.

## Verification and local evidence

From the repository root in PowerShell, when implementation verification or a new run is needed:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_capacity.py --output outputs/my-capacity-study
.\.venv\Scripts\python.exe experiments/run_ambiguity.py --output outputs/my-ambiguity-study
.\.venv\Scripts\python.exe experiments/run_insufficiency.py --output outputs/my-insufficiency-study
```

Use a fresh output path. Model setup/reproduction is separately documented in
[LOCAL_MODELS.md](docs/LOCAL_MODELS.md) and [LOCAL_TEACHER.md](docs/LOCAL_TEACHER.md).

Reports locate complete local runs under `outputs/`, notably `capacity-001/`, `continuation-001/`,
`outcome-correction-001/` and `teacher-briefing-001/`. This handoff checked those directories,
results summaries, manifest-file presence and checkpoint counts; the previous handoff did
**not** verify every historical archive/hash or reproduce historical experiments. This session
verified the ambiguity archive hashes, checkpoint invariance and actual restarts. This
cycle inspected and reproduced insufficiency with exact states/predictions, all stage
checksums, protocol/source/config guards and prior protected-file preservation.
No external backup was verified.
[.gitignore](.gitignore) excludes outputs, logs, virtual environments, local caches, weights
and credential files; these are not conveyed by a Git checkout. Default model cache is
`%LOCALAPPDATA%/LMFT-Lab/cache`; its assets were not inspected in this task.

Checks run for this cycle: handoff/spec/runtime/ambiguity review, actual Git/prework preservation,
frozen insufficiency protocol, 28 targeted tests, 461-test regression suite, primary run
and fresh reproduction (each 137 integrity/18 quality checks), state/trace/hash inspection.
The earlier ambiguity cycle's initial sandbox-temp permission errors remain recorded in
its report; this cycle used fresh writable-checkout test-temp paths. No inference,
downloads, pushes, publication, discards or runtime integration.
