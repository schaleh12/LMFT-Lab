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
post-hoc tuning of the completed study. D009 records the isolated ambiguity follow-up;
this original capacity policy remains unchanged.

## D008: Evolution-first GFT direction

**Status: superseded by [D002](#d002-persistent-development-separate-from-founding-state).** Population breeding, crossover, mutation and evolutionary
fitness are no longer defining requirements; genetic work remains optional future research.
Rationale: the project now investigates persistent LMFT development through evidence and
language-model interaction. Historical research and legacy compatibility records retain meaning.
Sources: [migration decisions](docs/INDEX.md#migration-decisions-and-compatibility), [AGENTS](AGENTS.md).
Revisit only as a separately scoped research proposal with a demonstrated need, not an implied
prerequisite for current implementation.

## D009: One informative equality observation

**Status: experimental — implemented and evaluated in an isolated study.** Retain every
training-consistent hypothesis; choose at most one observation by predicted disagreement,
with declared-order candidate ties and no request when scores are zero. Fresh validation
checks the entire retained set without filtering; consensus predicts and disagreement abstains.
Matched memory, non-informative, unavailable and no-evidence controls share the same mechanisms.
Rationale: test evidence-driven disambiguation beyond the uniquely identifiable capacity task.
The informative observation resolved lt/le; controls did not; ordinary memory matched exactly.
The canonical seed is inert and no numerical/runtime architecture changes follow.
Sources: original [proposal](experiments/CAPACITY_RESULTS.md#limits-and-smallest-next-experiment),
[frozen ambiguity protocol](experiments/AMBIGUITY_PROTOCOL.md),
[results](experiments/AMBIGUITY_RESULTS.md), [study code](src/lmft_lab/ambiguity.py).
Revisit noise, misspecification or further acquisition only through a separate preregistration;
never use held-out truth or validation to select surviving hypotheses.

## D010: Explicit unsupported hypothesis family

**Status: experimental — implemented and evaluated in an isolated study.** Preserve an
explicit empty surviving set and `no_supported_hypothesis`, distinct from ambiguity.
Accept only a nonempty set that passes whole-set validation; consensus requires actual
votes. Rejected/unverified inputs never count as candidate contradictions. No fallback,
resurrection, vocabulary expansion or teacher repair. Matched memory shares the policy.
Rationale: recognizing insufficient support must survive restart without claiming to
diagnose vocabulary, context or evidence faults. Exact elimination relies on this
noiseless registered synthetic verifier; it is not a general real-world evidence rule.
Sources: [frozen protocol](experiments/INSUFFICIENCY_PROTOCOL.md),
[results](experiments/INSUFFICIENCY_RESULTS.md), [study](src/lmft_lab/insufficiency.py).
All candidates were contradicted in the unsupported condition; controls made predictions
and preserved known held-out errors. Ordinary memory matched; seed/propagation were inert.
Revisit evidence assumptions or accepted-set revision only under a separate explicit contract.

## D011: Passive supervised relationship-set integration

**Status: experimental — passive integration implemented and evaluated.** New opt-in
relationship-set-lmft/memory modes use existing runtime transactions for verified outcomes,
explicit selection, whole-set validation and consensus probes, retaining empty versus
ambiguous support reasons and separate validation status. Preserve original capacity semantics
and old archives. Rejected/duplicate inputs leave judgment unchanged, with reasons in receipts.
Rationale: connect the isolated capacity/ambiguity/insufficiency mechanisms to an existing
inspectable lifecycle before adding autonomous acquisition. Request/reply verification
and atomic one-observation budgeting are a later step; no teacher or numerical overhaul.
Sources: original [assessment](experiments/INSUFFICIENCY_RESULTS.md#smallest-supervised-runtime-integration-step--assessment-only),
[frozen integration protocol](experiments/PASSIVE_RELATIONSHIP_PROTOCOL.md),
[results/limitations](experiments/PASSIVE_RELATIONSHIP_RESULTS.md),
[handler](src/lmft_lab/passive_relationship.py). All runtime/standalone/memory parity checks pass;
prediction accuracy remains the prior negative result. No acquisition is implemented yet.
Compatibility remains explicit: source-wide manifests reject historical checkpoints under
new code; keep archived source/config rather than migrate silently. Policy is JSON-normalized
and source/scenario/control changes reject. Fixture identifiers are not authentication.
Historical local prework preservation tests must use their original source context; current
behavioral regressions also pass in a clean matching source snapshot. Active acquisition
requires a separately frozen contract and coordinator sequencing.

## D012: Separate current regression from historical byte preservation

**Status: experimental — explicit verification contexts implemented and evaluated.**
Historical harness defaults and scientific criteria remain unchanged. Current behavioral
tests supply a frozen NONEMPTY complete source baseline, enforced before/after each run,
archived and pinned through restart. Added/missing/changed source or context rejects.
Historical audit resolves all original protected bytes from archived source and the exact
pinned Git revision, never from later working files or an absent context.
Rationale: an authorized later runtime edit must not be mislabeled as historical preservation,
and old output-specific prework must not conflate historical audits with current behavior.
The earlier 485/1 failure and original archive bytes remain preserved.
Sources: [separate contract](experiments/PRESERVATION_VERIFICATION_CONTRACT.md),
[historical anchor](experiments/INSUFFICIENCY_HISTORICAL_CONTEXT.json),
[verification results](experiments/PRESERVATION_VERIFICATION_RESULTS.md).
Audit requires original archive and pinned local Git evidence; exact CRLF checkout-byte
reconstruction is accepted only when it matches the original hash. This is an inspectable
local anchor, not authentication/backup. No scientific criterion or runtime algorithm changed.

## D013: One explicit active relationship investigation

**Status: experimental — implemented and evaluated in new opt-in modes.** After
complete training, investigate can issue at most one clarification_request for a
nonempty ambiguous set. Reuse generic feature-only disagreement selection and
declared-order ties; predefined noninformative control deliberately bypasses the
positive-score gate. Empty/unique/no-positive-score conditions close without request.
Persist episode/request/charged unit/question/output atomically; validate exact reply
source/correlation/schema/features with the synthetic device before admitting/filtering.
Original training evidence stays separate; whole-set validation never resurrects.
No reset or automatic episode replacement; cancellation never refunds a request.
Sources: [protocol v1.2](experiments/ACTIVE_ACQUISITION_PROTOCOL_V1_2.md),
[results and protocol history](experiments/ACTIVE_ACQUISITION_RESULTS.md),
[handler](src/lmft_lab/active_relationship.py). v1/v1.1 and early test outputs remain;
cost/expectation corrections were frozen in v1.2 before its reevaluation.
Rationale: persistent request/reply acquisition should be inspectable and equally
available to ordinary memory. Informative evidence resolved ambiguity; controls
did not; seed/propagation were inert and known fault errors remained.
Request cost, admitted facts and receiver executions are distinct. The original
unlimited default has no receiver-attempt cap; D014 adds only an explicitly opt-in
logical cap. Do not interpret one request as bounded total computation. Timeouts,
physical reservation and accepted-set revision need separate explicit contracts.

## D014: Opt-in checkpoint-accounted receiver attempts

**Status: experimental — implemented and evaluated.** Optional strict budget0..8
charges each eligible acquisition check in its computed checkpoint transaction,
including false labels. Committed charges persist; final false/zero-budget denial
closes exhausted, retains uncertainty and blocks later evidence. Last-valid succeeds.
Cheap malformed/unrelated/duplicate/conflicting inputs do not consume/check. Omission
retains the original unlimited policy/state; budget drift refuses restart.
Rationale: bound committed receiver work without falsely claiming a physical bound
or redesigning the transaction engine. False claims can exhaust resources and deny
legitimate evidence; memory has the identical policy and shares the outcome.
Sources: [frozen protocol](experiments/RECEIVER_BUDGET_PROTOCOL.md),
[results and physical counterexample](experiments/RECEIVER_BUDGET_RESULTS.md),
[fault child](experiments/receiver_fault_worker.py). Budget1 before-replace replay
made two physical calls/final logical1; after-replace replay made one. No durable
pre-computation reservation or ingress CPU/network/storage defense is established.
Revisit a HARD physical guarantee only through an explicit reservation/recovery
contract and its lost-result tradeoff; do not silently strengthen this logical claim.
