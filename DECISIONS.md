# LMFT-Lab — consequential decisions

A compact, retrospective index of repository-supported choices, not new approvals or a second
specification. **Adopted** means the working constraint/policy; **experimental** means a scoped
implementation choice, not an established cognitive law. **Proposed** is unimplemented;
**superseded** retains historical meaning. Only explicitly documented owner constraints are
identified as such. Keep IDs stable; when replacing a choice, retain it and link its successor.
Current findings and next work belong in [PROJECT_STATE.md](PROJECT_STATE.md).

## D001: Frozen founding seed

**Status: adopted — explicit owner constraint.** Preserve the canonical 40 nodes, names, order
and parent-child geometry, including Contemplation. Keep learned concepts outside that inventory.
Rationale: a stable founding scaffold permits interpretable developmental comparisons.
Sources: [AGENTS](AGENTS.md), [Minimal Section 4](docs/MINIMAL_LMFT_SPEC.md#4-hardcoded-v01-seed-geometry).
Revisit only with explicit owner approval and an explicit compatibility/migration plan; current
numerical defaults do not inherit the seed's frozen status.

## D002: Persistent development separate from founding state

**Status: adopted — research/specification direction.** Store judgments, memories, relationships,
interpretations and provenance separately from the seed; pursue bounded, evidence-backed
persistent development rather than mandatory genetic search (replaces D008).
Rationale: changes must be traceable without silently redefining founding principles.
Sources: [concept](docs/LMFT_CONCEPT.md), [Minimal Specification](docs/MINIMAL_LMFT_SPEC.md),
[capacity state](src/lmft_lab/capacity.py), [correction ledger](src/lmft_lab/correction.py).
Revisit storage representations when demonstrated needs justify a scoped migration; changing
founding geometry still requires D001 approval.

## D003: Model proposals require independent acceptance

**Status: adopted — working boundary; specific validators are experimental.** LLM/SLM output
can propose or clarify, but prose/role claims do not authorize belief, seed or code changes.
The teacher route fixture checks evidence and strict validation improvement before acceptance.
Rationale: persuasiveness is not evidence; permission and truth are distinct.
Sources: [AGENTS](AGENTS.md), [model guide](docs/LOCAL_MODELS.md),
[teacher assessment](src/lmft_lab/teacher.py), [teacher findings](experiments/TEACHER_BRIEFING_RESULTS.md).
Revisit task-specific criteria with new preregistered evidence; one accepted lesson does not
justify general trust or bypassing validation.

## D004: Matched ordinary-memory comparisons

**Status: adopted — research convention.** Give competent ordinary memory the same relevant
inputs, induction access and budgets; distinguish authored references from learned conditions.
Report equivalence/negative results and test propagation causally before crediting it.
Rationale: avoid manufacturing LMFT wins through weaker baselines.
Sources: [AGENTS](AGENTS.md), [capacity protocol](experiments/CAPACITY_PROTOCOL.md),
[capacity results](experiments/CAPACITY_RESULTS.md).
Revisit a comparator when capabilities/task scope change, documenting any remaining mismatch.

## D005: Reproducible local model assets

**Status: experimental — current deployment choice.** Use configured roles, full model revision
and checksum pins, a pinned llama.cpp backend, cached reuse and explicit offline failure on
missing/corrupt assets. Credentials come from environment, never committed tokens.
Rationale: reproducibility and practical Windows/RTX 4080 operation without a large framework.
Sources: [local model setup](docs/LOCAL_MODELS.md), [asset implementation](src/lmft_lab/model_assets.py),
[teacher setup](docs/LOCAL_TEACHER.md), [.gitignore](.gitignore).
Revisit for measured capability, hardware or backend needs; update pins and provenance explicitly.
These are implementation choices, not permanent owner-approved model selections.

## D006: Supervised communication and recoverable state

**Status: adopted — runtime boundary; single-file storage is experimental.** While running,
expose deliberate outbox messages and lifecycle acknowledgments; inspect full state only after
halt. Persist evidence, dispositions and outputs together, and reject incompatible restart
manifests. Preserve originals through correction lineage rather than overwriting evidence.
Rationale: accountable observation and reproducible recovery.
Sources: [runtime contract](docs/INTERACTIVE_RUNTIME.md), [store](src/lmft_lab/runtime_store.py),
[outcome guide](docs/OUTCOME_CORRECTION.md).
Revisit storage for demonstrated scale/durability needs; no distributed, hostile-host or
power-loss guarantee follows from the current atomic-replacement tests.

## D007: Bounded deterministic relationship induction

**Status: experimental — capacity fixture only.** Select one uniquely consistent comparison
from six authored candidates using training only; separate validation precedes acceptance.
Retain uncertainty on ties, forbid arbitrary code, and keep held-out labels outside selection.
Relation evaluation is a new explicit predictor, not a change to the existing counter equation.
Rationale: inspectable transfer with an equally capable memory comparator; no decorative activation.
Sources: [capacity guide](docs/CAPACITY_EXPERIMENT.md), [selector](src/lmft_lab/capacity_relations.py),
[protocol](experiments/CAPACITY_PROTOCOL.md).
Revisit for ambiguity, misspecification or new scoped evidence through a new protocol, not
post-hoc tuning of the completed study. D009 proposes the next test, not a replacement yet.

## D008: Evolution-first GFT direction

**Status: superseded by [D002](#d002-persistent-development-separate-from-founding-state).** Population breeding, crossover, mutation and evolutionary
fitness are no longer defining requirements; genetic work remains optional future research.
Rationale: the project now investigates persistent LMFT development through evidence and
language-model interaction. Historical research and legacy compatibility records retain meaning.
Sources: [migration decisions](docs/INDEX.md#migration-decisions-and-compatibility), [AGENTS](AGENTS.md).
Revisit only as a separately scoped research proposal with a demonstrated need, not an implied
prerequisite for current implementation.

## D009: One informative equality observation

**Status: proposed — not implemented.** Leave `<`/`<=` ambiguous, then test selection and use
of one verified equality observation against equally equipped memory and a no-new-evidence
control, with reserved validation/held-out cases.
Rationale: test evidence-driven disambiguation beyond the completed uniquely identifiable task.
Source: [capacity report](experiments/CAPACITY_RESULTS.md#limits-and-smallest-next-experiment).
Revisit during preregistration if scope, budgets or acceptance cannot isolate that question;
never use held-out truth to choose the hypothesis.
