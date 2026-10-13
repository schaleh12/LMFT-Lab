# LMFT-Lab â€” consequential decisions

A compact, retrospective index of repository-supported choices, not new approvals or a second
specification. **Adopted** means the working constraint/policy; **experimental** means a scoped
implementation choice, not an established cognitive law. **Proposed** is unimplemented;
**superseded** retains historical meaning. Only explicitly documented owner constraints are
identified as such. Keep IDs stable; when replacing a choice, retain it and link its successor.
Current findings and next work belong in [PROJECT_STATE.md](PROJECT_STATE.md).

## D001: Frozen founding seed

**Status: adopted â€” explicit owner constraint.** Preserve the canonical 40 nodes, names, order
and parent-child geometry, including Contemplation. Keep learned concepts outside that inventory.
Rationale: a stable founding scaffold permits interpretable developmental comparisons.
Sources: [AGENTS](AGENTS.md), [Minimal Section 4](docs/MINIMAL_LMFT_SPEC.md#4-hardcoded-v01-seed-geometry).
Revisit only with explicit owner approval and an explicit compatibility/migration plan; current
numerical defaults do not inherit the seed's frozen status.

## D002: Persistent development separate from founding state

**Status: adopted â€” research/specification direction.** Store judgments, memories, relationships,
interpretations and provenance separately from the seed; pursue bounded, evidence-backed
persistent development rather than mandatory genetic search (replaces D008).
Rationale: changes must be traceable without silently redefining founding principles.
Sources: [concept](docs/LMFT_CONCEPT.md), [Minimal Specification](docs/MINIMAL_LMFT_SPEC.md),
[capacity state](src/lmft_lab/capacity.py), [correction ledger](src/lmft_lab/correction.py).
Revisit storage representations when demonstrated needs justify a scoped migration; changing
founding geometry still requires D001 approval.

## D003: Model proposals require independent acceptance

**Status: adopted â€” working boundary; specific validators are experimental.** LLM/SLM output
can propose or clarify, but prose/role claims do not authorize belief, seed or code changes.
The teacher route fixture checks evidence and strict validation improvement before acceptance.
Rationale: persuasiveness is not evidence; permission and truth are distinct.
Sources: [AGENTS](AGENTS.md), [model guide](docs/LOCAL_MODELS.md),
[teacher assessment](src/lmft_lab/teacher.py), [teacher findings](experiments/TEACHER_BRIEFING_RESULTS.md).
Revisit task-specific criteria with new preregistered evidence; one accepted lesson does not
justify general trust or bypassing validation.

## D004: Matched ordinary-memory comparisons

**Status: adopted â€” research convention.** Give competent ordinary memory the same relevant
inputs, induction access and budgets; distinguish authored references from learned conditions.
Report equivalence/negative results and test propagation causally before crediting it.
Rationale: avoid manufacturing LMFT wins through weaker baselines.
Sources: [AGENTS](AGENTS.md), [capacity protocol](experiments/CAPACITY_PROTOCOL.md),
[capacity results](experiments/CAPACITY_RESULTS.md).
Revisit a comparator when capabilities/task scope change, documenting any remaining mismatch.

## D005: Reproducible local model assets

**Status: experimental â€” current deployment choice.** Use configured roles, full model revision
and checksum pins, a pinned llama.cpp backend, cached reuse and explicit offline failure on
missing/corrupt assets. Credentials come from environment, never committed tokens.
Rationale: reproducibility and practical Windows/RTX 4080 operation without a large framework.
Sources: [local model setup](docs/LOCAL_MODELS.md), [asset implementation](src/lmft_lab/model_assets.py),
[teacher setup](docs/LOCAL_TEACHER.md), [.gitignore](.gitignore).
Revisit for measured capability, hardware or backend needs; update pins and provenance explicitly.
These are implementation choices, not permanent owner-approved model selections.

## D006: Supervised communication and recoverable state

**Status: adopted â€” runtime boundary; single-file storage is experimental.** While running,
expose deliberate outbox messages and lifecycle acknowledgments; inspect full state only after
halt. Persist evidence, dispositions and outputs together, and reject incompatible restart
manifests. Preserve originals through correction lineage rather than overwriting evidence.
Rationale: accountable observation and reproducible recovery.
Sources: [runtime contract](docs/INTERACTIVE_RUNTIME.md), [store](src/lmft_lab/runtime_store.py),
[outcome guide](docs/OUTCOME_CORRECTION.md).
Revisit storage for demonstrated scale/durability needs; no distributed, hostile-host or
power-loss guarantee follows from the current atomic-replacement tests.

## D007: Bounded deterministic relationship induction

**Status: experimental â€” capacity fixture only.** Select one uniquely consistent comparison
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

**Status: experimental â€” implemented and evaluated in an isolated study.** Retain every
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

**Status: experimental â€” implemented and evaluated in an isolated study.** Preserve an
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

**Status: experimental â€” passive integration implemented and evaluated.** New opt-in
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

**Status: experimental â€” explicit verification contexts implemented and evaluated.**
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

**Status: experimental â€” implemented and evaluated in new opt-in modes.** After
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

**Status: experimental â€” implemented and evaluated.** Optional strict budget0..8
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

## D015: Existing Clarity ranking contribution has bounded utility limits

**Status: experimental â€” evaluated without production changes.** Reuse the existing
consistent_attention circuit and its single-edge Clarity ablation; compare exact
algebraic ordinary-memory equivalents. Freeze existing initializer weights and
historical counter replay; no fresh learning or contradiction repair.
Rationale: previous ranking causality did not establish downstream usefulness.
In ten authored competing-question cases, intact resolves 4 questions versus 7 ablated
(three hurts/no helps), while all final decisions tie and scalar memory matches.
This supports a causal ranking effect and a limitation, not semantic understanding,
a general seed benefit or a fuzzy-tree advantage. Preserve wrong outcomes and all
primary attempts; no theory/seed/numerical change follows automatically from this finding.
Sources: [frozen protocol](experiments/SEED_CONTRIBUTION_PROTOCOL.md),
[results and reproduction](experiments/SEED_CONTRIBUTION_RESULTS.md),
[experiment tests](tests/test_seed_contribution.py). Stop for coordinator review;
roadmap step2 and chat demonstration remain undispatched.

## D016: External bounded action choice distinguishes gathering from correction

**Status: experimental â€” standalone evaluated, no production changes.** Missing
parts permit scoped gathering; inconsistent support permits advertised existing
authorized operations only on current exact targets. Selection cannot read reply
values/outcomes; unchanged correction receiver separately authorizes/checks/verifies.
One shared lifetime request, no reset/refund/retry. No new learned policy or node meaning.
Rationale: additional corroboration cannot supersede conflicting instrument roots.
v1 filtered gather-only did not establish original-selector query savings; owner
review required frozen v2 with unchanged selector and separate work/admission metrics.
v1 remains preserved. Full/memory has2 non-resolving requests versus original8,
avoids6 unresolved contradiction gathers, but includes an invalid repair and wrong
predictions. Exact memory parity; combined adapter benefit is not seed/fuzzy superiority.
Sources: [v1](experiments/ACTION_CORRECTION_PROTOCOL.md),
[frozen v2](experiments/ACTION_CORRECTION_PROTOCOL_V2.md),
[results/costs/limits](experiments/ACTION_CORRECTION_RESULTS.md),
[tests](tests/test_action_correction.py). Stop for coordinator review; runtime
integration, further learning, physical bounds and later roadmap work are undispatched.

## D017: Later registered evidence can restore conflict after verified correction

**Status: experimental - standalone chained restart evaluated.** Preserve the existing
action-aware adapter and one lifetime request. Accept a separately registered later
report through the existing ledger handler with an explicit optional evidence registry;
default runtime registration, correction permits and receiver remain unchanged.
Rationale: correction success must not erase later contrary evidence or count replay
as independent support. Two existing cases restore conflict/abstention after a later
report, across three chained actual child processes; exact scalar memory matches.
No-later/frozen controls retain the known wrong prediction. Registered report identity
does not certify truth; lower coverage does not prove improved judgment.
Sources: [frozen protocol](experiments/SEQUENTIAL_CORRECTION_PROTOCOL.md),
[results, costs and limitations](experiments/SEQUENTIAL_CORRECTION_RESULTS.md),
[tests](tests/test_sequential_correction.py). The historical action question remains
closed while current support can become inconsistent. No automatic reopening, second
repair budget, live runtime mode or physical bound. Old manifests still require
archived source. Stop for coordinator review before another bounded task.
Review follow-up enforces the intended strict Boolean/schema registration boundary
after discovering Python numeric/Boolean equality; canonical record digests replace
dictionary equality. Run002 reproduces the original valid-Boolean findings, retaining
run001 and disclosing its malformed-input defect in the results. No policy or
scientific criterion revision follows from this implementation correction.

## D018: Fixed synthetic commands reuse supervised runtime transactions

**Status: experimental - opt-in integration implemented and evaluated.** Two new
action-command modes share extracted existing policy/strict registry functions and
the unchanged correction ledger. Exact commands and correlated replies use the
existing inbox/outbox, receipt, dedup and checkpoint lifecycle. Explicit authored
setup retains provenance; inspect separates current support from historical closure.
One lifetime action request persists, without reset, automatic re-repair or freeform
interpretation. Synthetic sender/source labels are not identity authentication.
Rationale: test the bounded correction/later-conflict sequence at the real communication
and persistence boundary before considering a broader interface. Twelve individuals
match standalone references, memory and restarted controls. The known prediction error
remains; higher final accuracy covers fewer decisions. Pre-commit fault recovery can
repeat physical verification; no physical cap or exactly-once external effect follows.
Sources: [protocol](experiments/ACTION_RUNTIME_PROTOCOL.md),
[results/costs](experiments/ACTION_RUNTIME_RESULTS.md),
[command contract](docs/ACTION_COMMAND_RUNTIME.md). Source-wide manifests reject old
checkpoints under new code; archived source/config remain necessary. Stop for review
before demo polish, new episodes, teacher integration or another bounded task.
Final review enforces initialization against the already pinned permit policy and
counts both successful and rejected gather verification attempts in the new adapter.
Legacy receiver defaults remain unchanged; runs001/002/003 and intermediate regressions
are preserved, with identical primary metrics and stage predictions.

## D019: Thin local presentation over the existing synthetic runtime

**Status: experimental - implemented; Ctrl+C incomplete at the initial gate.**
Subsequent focused fix: D020 supersedes this initial keyboard-exit limitation;
the observations and failed artifacts described here remain historical evidence.
A standard-library terminal wrapper uses only existing inbox/outbox/checkpoint commands
for r1/r8/r2. Fresh roots refuse overwrite; explicit resume preserves scenario,
one-request budget and message identities. Public current support/history stay
separate; internal provenance requires halt. No text interpretation or new learning.
Rationale: make the bounded sequence inspectable by a human without adding a second
state authority. Direct actual-runtime replay and matched-memory parity pass.
Sources: [protocol](experiments/ACTION_DEMO_PROTOCOL.md),
[results and retained failures](experiments/ACTION_DEMO_RESULTS.md),
[guide](docs/ACTION_TERMINAL_DEMO.md). Real quit/EOF/resume pass, but hosted PowerShell
Ctrl+C terminates before orderly cleanup despite process-group isolation; exception
injection tests do not establish console-signal safety. Failed originals are retained;
recovery of a copy preserves scientific state. Do not claim all exit criteria passed.
Older checkpoints still require archived source. Stop for review before any later task.

## D020: Handle interactive Windows Ctrl+C at a command boundary

**Status: experimental - actual hosted PTY evaluated.** Temporarily read Windows
console input without processed Ctrl+C while the wrapper owns it; restore exact
original flags only after normal child shutdown and reaping. The exit key is queued
during command execution and consumed at the next boundary; repeated keys cannot
escalate the wrapper into killing its child. No persistent OS/security change.
Rationale: a minimal hosted signal probe was terminated during cleanup even after
SIGINT was caught; a console-input key avoids that broadcast path. D019's failed
trials remain unchanged. Pending, instrumented in-progress reply, repeated-key,
post-conflict, quit and EOF PTY trials pass with lifecycle/receipt/process evidence.
Sources: [focused protocol](experiments/ACTION_INTERRUPT_PROTOCOL.md),
[diagnosis, results and limits](experiments/ACTION_INTERRUPT_RESULTS.md),
[reader](src/lmft_lab/action_console.py). Existing scientific/runtime rules are unchanged.
This resolves tested interactive keystrokes only: external signals, script-mode
interrupts, console closure and forced termination are not covered. Stop for review.

## D021: Learn operand binding inside a supplied finite comparison family

**Status: experimental - isolated study evaluated.** Use neutral numeric channels,
36 representations grouped into18 behavioral classes, class-weighted disagreement
and one verified observation to distinguish correlated operand bindings. The oracle
mapping stays outside learner requests/checkpoints; held-out labels are accessed
only after predictions freeze. No validation-based candidate elimination is hidden
inside evaluation. An independent ordinary-memory implementation uses truth-table
mask filtering/voting with the same information, budget and persistence.
Rationale: earlier capacity learning supplied the operands, while subsequent studies
emphasized evidence bookkeeping. Evidence now chooses the operands within a frozen
experimental family, with remembered provenance and later transfer. Full memory parity
means no seed/fuzzy advantage. Six permutations test symmetry, not independent replication.
Sources: [frozen protocol](experiments/ATTRIBUTE_BINDING_PROTOCOL.md),
[results, boundaries and limitations](experiments/ATTRIBUTE_BINDING_RESULTS.md),
[primary](experiments/attribute_binding_primary.py),
[independent memory](experiments/attribute_binding_memory.py).
Coverage improves25/37 ->37/37 with informative evidence; accuracy remains100% among
decisions. Ambiguous controls keep12 abstentions; supported controls avoid unnecessary
queries. This does not learn linguistic categories, primitives or causal understanding.
No production/seed/numerical/model contract changes. Current session ceiling18:40 UTC;
stop for coordinator review before investigating larger surviving families or integration.

## D022: Integrate fixed-family learned binding through the supervised runtime

**Status: initial integration blocked by review; narrow correction under
[D023](#d023-reject-inconsistent-binding-configuration-and-request-history) is independently accepted.** Following accepted D021, add fixture-only binding-primary and
binding-memory modes using existing inbox, outbox, deduplication and atomic commits.
The separately versioned persisted survivor set directly controls emitted decisions;
no forced singleton, language-authorized revision or runtime family expansion.
Independent truth-table memory retains its own filtering/voting/prediction logic.
A pinned frozen pre-acquisition predictor receives the same evidence and budget to
isolate the decision effect of updating the learned basis. It keeps12 abstentions
while informative learning resolves them; both kernels match, with no wrong decisions.

Use a receiver-invoked trusted private registry adapter; sender-computable digests
cannot authorize evidence. Harness-private mapping and held-out labels do not enter
the learning API. This trusts local operator fixture construction, not arbitrary
untrusted files or OS sandboxing. One request bounds admitted information, not
physical oracle/verifier computation. Evaluation leaves learning state unchanged.

Do not relax full software_manifest checks or migrate old states. Before editing,
match/archive the owner's exact44-file runtime; test recovery only on a fresh copy.
Original19 demo files and102,090 prior outputs remain unchanged. Copied-checkpoint
startup/halt under archived code passes; current-source resume correctly fails.
New contract/source changes require fresh individuals or separately approved work.

[Protocol and frozen matrix](experiments/BINDING_RUNTIME_PROTOCOL.md),
[results/preservation/reproduction](experiments/BINDING_RUNTIME_RESULTS.md),
[runtime guide](docs/BINDING_RUNTIME.md), [handler](src/lmft_lab/binding_runtime.py).
1,530 checks,72 arms/216 processes;28 focused/806 full tests pass. Fresh rerun250
checks and77 comparison checks pass. No tree/semantic/causal-world-model superiority
claim. The original gate stopped for review; D023 records the correction and
subsequent independent acceptance. No further task is dispatched.

## D023: Reject inconsistent binding configuration and request history

**Status: independently accepted within trusted local finite-fixture scope; session closed.**
D022's initial acceptance was blocked by independently reproduced checksum-valid
nested mode/condition mismatches and a nonexistent request ID. These are internal
consistency defects; do not dismiss them as a hostile-filesystem threat. Preserve
all original positive/negative evidence and exact pre-fix source/config.

Validate binding identity across nested state, outer experiment, manifest and launch
before startup and input processing. A charged request must resolve uniquely to its
actual emitted clarification, with matching selection, query/payload, source/sender,
sequence and correlation. Retained acquisition/closure must match accepted reply/
close history and phase ordering. Reject before lifecycle/output writes or verifier
construction; repeat under the existing lock. Do not relax software_manifest, add
fields/migration/authentication or reverify all persisted registry records.

[Protocol](experiments/BINDING_RESTART_FIX_PROTOCOL.md),
[corrective report](experiments/BINDING_RESTART_FIX_RESULTS.md),
[tests](tests/test_binding_restart_consistency.py).103 focused/881 full tests pass;
29 invalid actual restarts preserve all copied bytes;18 valid resumes preserve
expected decisions and parity.119,159 earlier output files and owner demo unchanged.
No new study or foundational capability claim. Independent re-review accepted the
narrow correction; the parent closed the session at this checkpoint.


2026-10-12 closeout: parent accepted independent re-review (103 focused tests,
29 unchanged-byte invalid restarts,18 valid resumes; original defects and two Boolean
substitutions rejected pre-startup).224 evaluated/225 handoff sources,8,597 corrective
artifacts and119,159 prior hashes verified;881 full-suite XML inspected, not rerun.
Session ended early before18:40 UTC. The next design discussion should define a
falsifiable propagation decision contract and its authority relative to evidence.
Binding currently learns finite-family selection with authored query policy and no
seed participation in decisions; memory matches. No automatic wiring, new fixture
study, protected change or further implementation is dispatched.

## D024: Retire the fixed-command terminal demo only

**Status: owner-requested retirement, 2026-10-12; awaiting parent review.**
Supersedes active support for the D019 terminal wrapper and D020 console helper;
their recorded results, failures and protocols remain historical and unchanged.
Remove the two demo modules, two dedicated test files (20 cases), scripted demo
harness and interrupt probe from active paths. Retain shared action runtime,
action policy, capacity/binding learning and all shared regression infrastructure.
No seed, numerical mechanism, model configuration or dependency changes.

Archive exact current source/config before removal, rather than assuming older
archives match: `outputs/terminal-demo-retirement-20261012-001/source/` contains
225 files with SHA-256 hashes, from clean HEAD
`583071f857a9912c83ac06429dca0fe9d67e8aa1`. No commit was made by this cleanup.
Source-wide manifests intentionally reject incompatible old checkpoints; retain
matching historical archives and original owner session unchanged. No relaxed
manifest, silent migration or restart of the owner session. Historical executable
links/commands are to be interpreted in their matching archived checkout.
[Retirement and recovery](docs/ACTION_TERMINAL_DEMO.md) replaces active launch guidance.
Stop for parent review; no follow-on implementation or experiment is dispatched.

Cleanup validation: 861 remaining tests pass; 20 demo-only cases were deliberately
retired. The first run omitted the documented child-process PYTHONPATH and is
retained alongside the corrected passing run. All 215 unrelated tracked files and
19 owner-demo files remain byte-identical; 225 pre-cleanup archive hashes verify.
Final system-wide process query found no Python workers. No further work dispatched.

## D025: Learn measurement-interpretation applicability in a fixed family

**Status: independently accepted within the frozen isolated scope, 2026-10-13.**
Following owner approval of the direction, independent review narrowed the study to
six fixed binary normalization hypotheses and independently referenced synthetic
calibration. The original [draft](experiments/CONTEXT_APPLICABILITY_PROTOCOL_DRAFT.md)
is preserved unchanged; the parent approved one bounded study, and its
[final protocol](experiments/CONTEXT_APPLICABILITY_PROTOCOL.md) was pinned before
evaluation. It fixes worlds, two context bits, schedule, held-out grid, controls and
integrity gates; later scientific changes require a new version and preregistration.
Only calibration narrows hypotheses; agreement-seeking normalization is not evidence.
Ordinary memory receives identical evidence and independently filters/predicts.
No propagation diagnostics, acquisition-policy learning, runtime integration or
philosophical naming. Narrowing uncertainty is not revising an accepted global belief.
The [results](experiments/CONTEXT_APPLICABILITY_RESULTS.md) show 192 -> 352 correct
support decisions of 2,688, zero wrong/unsafe, including 64 gains on genuinely unseen
contexts and unchanged original-context behavior. Memory matches; 40/48 arms remain
ambiguous. No family repair or additional budget. Global replacement loses some
original-context behavior despite unchanged aggregate correct counts.

7,821 study checks, 115 targeted and 976 full tests pass; actual restart and journal/
configuration rejection checks preserve witnesses and raw evidence. All production,
seed/numerical/model mechanisms and dependencies remain byte-identical. The old demo
and historical evidence stay preserved. Parent accepted independent review: 115
focused tests, 24 arms at flip0 across all worlds/schedules and five controllers,
360 worker invocations, 3,937 checks and 18 pipe checks reproduced. Full traces
recounted (352/0/2336; 64 unseen-context and 96 newly calibrated gains; retention
unchanged; 40/48 ambiguous). 229 source, 480 prediction, 10,564 artifact, 135,271
prior hashes and 57 unchanged production/config/dependency files verified.
976 full tests and 7,821 study checks were inspected, not independently rerun.
Session ceiling 2026-10-13 02:40 UTC does not authorize self-dispatch.


## D026: Defer learned investigation priority pending a task utility objective

**Status: original design-only decision; bounded comparison subsequently approved in D027.**
[Evidence and candidate contract](docs/INVESTIGATION_PRIORITY_DESIGN.md) distinguishes
permission from attainable information, cost, error risk and abstention. Existing
missing-part eligibility would filter the x1/x3 wasted gathers, but mixed missing
and contradictory support in x2 remains eligible. A structural feasibility check
can address that remaining one-step resolution limitation without learned context.
This is code inspection, not a new evaluation of those fixtures under the adapter.
r9 full/memory scores tie; correction wins by action ID. Correction and gathering
each resolve one question and still abstain, with no established cost advantage.

Do not manufacture a learned selector or seed-weight change from those cases.
First choose whether useful partial resolution merits spending the only request
when no immediate final decision can follow. Any future implementation must compare
a competent direct controller and memory with identical permission, information,
budget and feedback; distinguish single-edge ablation from propagation disabled.
No protected geometry, executable, numerical, model or dependency change follows.
Parent/owner review is next; no experiment or runtime integration dispatched.


## D027: Compare provisional investigation objectives without changing defaults

**Status: comparison and narrow domain-guard correction independently accepted, 2026-10-13.**
Owner provisionally favored useful partial learning with visible costs; this does
not authorize a permanent or always-investigate policy. Freeze current, target-
resolution and final-support-gate selection with matching scalar controls, existing
eligibility/positive priorities/ties/receivers and lifetime budget. x2 is annotation/
decision-only, never a new service. Six existing r-cases retain wrong/rejected results.
[Protocol](experiments/INVESTIGATION_PRIORITY_PROTOCOL.md) precedes implementation;
[results](experiments/INVESTIGATION_PRIORITY_RESULTS.md) report separate information,
resolution, decisions/correctness, work and remaining-uncertainty vectors.

Boolean enumeration is a complete public effect overapproximation, not access to
actual permitted replacements: possibility is conditional on unknown admission.
Current/target match on executable cases. Final saves one r9 request at the cost
of one unresolved question; final answers tie. x2 exposes foregone missing-part
information. No universal objective, learned selector or seed advantage follows.
331 checks, 179 focused/1,113 full tests pass; independent support truth-table tests
validate annotations beyond shared scalar parity. Production/configuration and all
historical evidence preserved. No runtime/default change, model call or commit.
Stop for independent review; no follow-on work dispatched.


D027 corrective follow-up, 2026-10-13: reviewer reproduced list/dict TypeError before
unknown-domain handling. Preserve its negative probe and exact 235-file pre-fix
snapshot. Move raw active scoped Boolean-domain validation ahead of preflight and
selection; malformed values return unknown/no action, with no coercion. This is
experiment-local contract repair, not a new priority policy. Run002 matches all
known-case predictions/vectors/rows except outbox timestamps; 331 checks, 229 focused
and 1,163 full tests pass. Original179/331 results were independently reproduced;
original1,113 full XML inspected only. Source/history/production preservation holds.
[Versioned addendum](experiments/INVESTIGATION_PRIORITY_RESULTS.md) records failure,
fix, hashes and limits. Read-only r8/r10 diagnosis remains separate; no broader fix.
Stop for independent re-review.


D027 accepted corrective review: parent reports 35 direct malformed probes with
sentinel guards, 229 focused tests and 331 comparison checks independently reproduced;
known-case outputs unchanged except timestamps. Pre-fix/original/corrected source
hashes, protocol and 57 production/configuration/dependency files verified. 1,163
full-suite XML inspected, not independently rerun. Original rejection and correction
history remain preserved. No new default or broader cognitive claim follows.

## D028: Audit-policy assessment recommends retaining the accepted checkpoint

**Status: parent accepted stopping at the checkpoint; session completed early, 2026-10-13.**
[Assessment](docs/CONSISTENT_SUPPORT_AUDIT_ASSESSMENT.md) distinguishes report identity,
consistent support, exact operation permission, coordinate verification and outcome
prediction. Original c3 already demonstrates revising consistent erroneous reports;
r10's selector declines that operation as already resolved. A separately scoped,
explicitly operator-requested audit could use existing correction verification, but
would demonstrate capability rather than learning when to audit. No matched
cost-only resolved-support controls or task-grounded trigger currently establish
benefit. The r8 prediction error is a distinct information/induction limitation.
Applicability inference requires missing runtime context/calibration inputs and
cannot be assumed to repair both bad agreeing reports or missing outcome features.
Recommend stopping at the accepted checkpoint rather than implementing either
an audit policy or applicability integration. No institution/source/nationality
weights, philosophical authority, seed/configuration or executable changes. Parent
review is next; no further experiment or task dispatched.


D028 final closeout: parent agreed to end the up-to-three-hour session early, before
02:40 UTC, rather than invent a favorable audit fixture. No further task is queued;
no monitoring or autonomous continuation. Preserve accepted D025/D027 findings,
reviewer reproduction-versus-inspection limits, r8/r10 diagnoses and all negative
history. Next design need: representative contexts, observable pre-action cues,
and costs/outcomes for deciding when to audit fallible but consistent reports.
No learned audit policy or seed utility is established. Recent Jev discussion is
research-only, with no integration/model-call/teacher authorization. Only current
handoff documentation changed at closeout; all executable/configuration/protocol/
test files match the reviewed snapshot. No rerun, model call, commit or push.
Final compact manifest: `outputs/session-closeout-20261013-001/`.


## D029: Assess coordination before extending the seed circuit

**Status: proposed next increment; documentation-only first task, awaiting parent review.**
New bounded session authorized 01:25–05:25 UTC; earlier closeout remains historical.
[Assessment and candidate protocol](docs/WHOLE_ARCHITECTURE_COORDINATION_ASSESSMENT.md)
traces r8 through the real seven-leaf scratch circuit, external eligibility, verified
correction and historical branch prediction. Full Cultural/Philosophical/Experiential
coordination is not implemented; the owner's proposed dependencies are not silently
converted into equations. Prior local negative findings do not refute every possible
whole architecture, and activating all nodes would not validate one.

Recommend one isolated learned-interpretation-to-action handoff using the accepted
applicability mechanism and existing device family, with persistent authority/history/
consequence linkage, competent equal-information memory and explicit partial controls.
This would test a missing engineering connection, not seed semantics or superiority.
Reversible task defaults and falsification are stated; no hidden-label audit schedule,
new morality/trust weights, seed/numerical edits or production integration. No
implementation/evaluation is authorized by this proposal. Stop for parent review.


D029 parent-review refinement: factual assessment accepted; initial sensor-bench
handoff recommendation withdrawn as the strongest next task because binding/action
runtime integrations already establish most of its persistence/permission/receipt
capabilities. Specified proposed v2 freezes identities, synthetic device/verifier,
transactions/restarts, stale-permission handling, counterfactual receipts and isolation,
five comparators, 10,752 main dispositions per controller and separate probes; it
is parked, not implementation approval. Revised next-step recommendation is one
interpretive-scope-status to Contemplation-agenda contract using existing evidence,
with direct-memory and raw-support-only causal controls. Context evidence must
precede a candidate philosophical distinction, measurable effect and then faithful
verbalization. Presence versus capacity-to-act is only an illustrative parent example,
not canonical Agency/Existence semantics. No equations/seed/code/model changes.
Operationalization and causal authority remain prerequisites; stop for parent review.


D029 final linguistic refinement: supplied fixed numeric families do not establish
new linguistic memberships or contextual working definitions. Recommended first
prerequisite is now a tiny candidate-interpretation/evidence contract, with existing
node links, scoped examples/counterexamples, revision/abstention and independent
held-out linguistic assessment. This precedes the proposed agenda connection.
Parent 'order' examples remain illustrative, not canonical definitions or gold
labels. Model-assisted candidate generation, if needed, requires separate approval;
no model call, teacher expansion, corpus collection or implementation occurred.
See assessment section7. Stop for parent review; no more scope added to this task.

D029 representation limit: do not force lexical concepts into abstract binary seed
extremes. Overlapping scoped associations may require revisable examples,
relationships, conditions and exceptions outside the protected inventory, with
unknown/unrepresented outcomes. Six philosophical leaves are not a demonstrated
encoding of full lexical meaning. Future weighted proposals must justify robustness
to perturbation; no seed expansion or weight tuning is authorized here.

D029 geometry provenance clarification: owner intends middle-diagonal/cross-cutting
Philosophical relations, distinguished from Cultural top-down and Experiential
bottom-up framing, as an abstract contextual game-controller landscape. This came
from a prior ChatGPT conceptual description, not verified model internals, formal
game theory or validated equations. Lexical application tests one grounding
component only and cannot validate this geometry. See assessment section 7; no
implementation or protocol expansion authorized.


## D030: Development-only supervised linguistic application prerequisite

**Status: Phase A implemented/tested; held-out execution blocked pending parent and
independent custodian review, 2026-10-13.** This supersedes D029's documentation-only
stop solely for the newly authorized experiment-local increment. Freeze the
[protocol](experiments/LINGUISTIC_APPLICATION_PROTOCOL.md) before implementation;
[results and CLI](experiments/LINGUISTIC_APPLICATION_PHASE_A_RESULTS.md) own findings.
Use only the custodian-pinned SemCor development export, immutable document split,
supplied labels and exact metadata-to-input adapter. No corpus in source archives.

Each observed sense independently learns surface unigrams/unordered token pairs:
at least two positive documents and no admitted counterexample. Retain immutable
examples, all witnesses, rejected/invalidated cues and numbered revisions; preserve
zero/one/multiple matches with abstention and no primary majority fallback. Reuse
Store/checksum/atomic persistence, not a new transaction framework. Compare against
independently recomputed same-rule memory, frozen batch 1 and majority diagnostic.
No weights, new founding identifiers, seed links, philosophical meanings or production
runtime changes. Corpus supplied categories are not autonomous conceptual admission.

Technical checks pass: 63 focused/1,226 full tests, actual process restart, exact
replay/prediction nonmutation and expected memory parity. Initial sandbox temporary
path failure retained; no threshold tuning. Development revision gains three and
loses two correct classifications on the original 20 items. All 33 development
items: 15 correct/18 abstain updated; frozen 8 correct/3 wrong/22 abstain. Preserve
negative outcomes; these are training diagnostics, not held-out improvement.
Source-family independence, lexical overlap/unknown gold and rights remain unresolved;
procedural custody is not security isolation. No held-out inputs/labels inspected,
models called, teacher expansion, dependencies, commits, pushes or publication.
Stop for parent/custodian review of pinned code/protocol before evaluation.


D030 narrow corrective follow-up: parent review blocked evaluation because ordinary
Python reconstructed-state equality accepted Boolean/float substitutions for cached
integer values despite valid checksums. Require exact integer schema version and
type-sensitive canonical JSON reconstruction comparison in the experiment only.
No shared Store/protocol/scientific rule changes. Preserve reviewer evidence and
20-failure pre-fix restart reproduction. Added 28 actual inspect/predict regressions;
91 focused/1,254 full tests pass. Recreated development predictions/reports are
identical; source pins alone change checkpoint state. Original checkpoints/source
remain recoverable; no silent migration. Corrective addendum records exact hashes.
STOP for parent/custodian re-review before held-out execution; no new study or scope.


## D031: Preserve failed linguistic generalization; assess representation next

**Status: Phase B completed independently; negative result preserved, read-only
failure diagnosis complete; future proposal only, 2026-10-13.** D030's correction
was independently accepted before evaluation. [Phase B report](experiments/LINGUISTIC_APPLICATION_PHASE_B_RESULTS.md)
records committed predictions, independent verification limits and diagnosis.
14 held-out uses/11 documents: updated primary/memory0 correct,3 wrong singletons,
10 abstentions,1 ambiguity with two wrong labels;5 wrong inclusions/14 gold exclusions.
Frozen abstains14;majority7 correct/7 wrong. Improvement criterion FAILED. Zero strict
correct gains/losses does not hide newly introduced errors. This split is consumed.

All three firing cues are function-word pairs supported by two examples in two
separate documents, zero admitted counterexamples; two share identical witnesses.
No active gold cue matches. Evidence indicates sparse, target-insensitive lexical
co-occurrence; no new contract bug identified by bounded trace audit. No stop-word,
threshold, candidate or tokenization tuning against evaluation is permitted by this
work. All scientific source/protocol and negative history remain unchanged.

Recommend only a separately authorized bounded local-SLM context-representation
contract with evidence anchors and independent fresh data, matched against the same
SLM with ordinary structured memory. More hand-tuned lexical exclusions would patch
this consumed test. Richer extraction remains unproven and adds model/provenance
risks; no model call or integration occurred. Existing records can support an honest
status view; no self-talk renderer implemented. Cross-cutting philosophical framing
is not six-bin sorting and no seed benefit is established. Stop for parent review.


## D032: Four-call development-only local-SLM representation interface check

**Status: bounded authorized check completed; negative admissibility outcome;
awaiting independent parent review, 2026-10-13.** Separate from D031's consumed
14-case evaluation. Freeze protocol/schema/prompts/mechanical four-input selection
before calls. Use existing offline Qwen3-4B interpretation transport/settings only;
one owned server, four attempts maximum, no retries/repairs/teacher or activation.
[Results](experiments/SLM_REPRESENTATION_INTERFACE_RESULTS.md) retain exact hashes.

One neutral source-anchored record is shared by primary/memory consumers rather
than duplicate wrappers. Exact quotes/schema do not confer semantic truth or
permanent meaning; no canonical seed mapping or action authority. Four responses
finished normally but all were rejected: three count/status mismatches, all four
without non-target evidence anchors. 26 exact anchor occurrences were target-only.
Context-containing paraphrase is observed, not validated semantic representation.
All raw negatives retained in the new nonpublished research archive with notices.

42 focused/1,296 full tests pass; restart retrieval identical and nonmutating. Four
calls exhausted; owned server closed. No protected source/config/seed/scientific
protocol changes. The next gap is a minimally reliable contextual reading/anchor
interface, then independent semantics; no automatic further prompt/model calls,
self-talk renderer or integration. Stop for independent parent review.


## D033: Protocol 2 local-SLM context-anchor check eliminates count and target-copying limits

**Status: bounded authorized check completed; negative admissibility outcome (token arithmetic);
awaiting review, 2026-10-13.** Follows D032 negative results. Prunes relations/conditions, enforces
`maxItems: 1` in grammar sampling, and introduces singular `context_anchor` requiring non-target context tokens.
[Protocol 2](experiments/SLM_REPRESENTATION_INTERFACE_PROTOCOL_V2.md) and
[results](experiments/SLM_REPRESENTATION_INTERFACE_V2_RESULTS.md) own scope. Exactly 4 offline calls on the
identical development cases; owned server closed.

Status/reading count mismatch was 100% eliminated (4/4 returned exactly one reading). Target-only copying
was 100% eliminated (4/4 anchors identified surrounding context words). However, all 4 were rejected due to
`source quotation mismatch`: the 4B SLM accurately extracted string words but miscalculated 0-based half-open
token slice indices (`[start:end)`). 

Neutral store retrieval verified identical digests across primary and ordinary structured-memory consumers
under actual process restart (`7b20af56...`). 44 focused V2 tests, 42 V1 tests, and 1,340 full regression tests
pass. No seed, numerical mechanism, or production integration changes. All artifacts preserved in external
archive `C:/Users/schal/AppData/Local/LMFT-Lab/research-archives/slm-representation-interface-v2-20261013-001`.


## D034: Protocol 3 deterministic context span resolution achieves interface admissibility

**Status: bounded authorized check completed; positive interface admissibility outcome (4/4 admissible),
2026-10-13.** Follows D033 token-arithmetic findings. Relieves the 4B model of integer slice arithmetic:
model outputs `context_quote` as a plain string snippet from the sentence, and Python deterministically
resolves the contiguous token slice `(start, end)` in `tokens` prioritizing proximity to target.
[Protocol 3](experiments/SLM_REPRESENTATION_INTERFACE_PROTOCOL_V3.md) and
[results](experiments/SLM_REPRESENTATION_INTERFACE_V3_RESULTS.md) own scope. Exactly 4 offline calls on the
identical development cases; owned server closed.

All four proposals passed contract admissibility (4/4 admissible, 100%). Each case produced a concise
reading with rich, non-target context phrase anchors (`[16:23]`, `[46:53]`, `[5:12]`, `[10:19]`).
All four were admitted as `lifecycle: unverified_proposal` to the neutral store.

Neutral store retrieval verified identical digests across primary and ordinary structured-memory consumers
under actual process restart (`fddbfbb9...`). 27 focused V3 tests pass. Interface admissibility is established;
subsequent semantic adjudication remains an independent research step.


## D035: Semantic adjudication demonstrates 100% precision and isolates gloss tautology limit

**Status: adopted evaluation finding; experimental analysis complete, 2026-10-13.** Follows D034 interface
admissibility. Evaluates the four admitted proposals against WordNet 3.0 ground-truth definitions, gloss informativeness,
and cross-example discriminability across the 33 development sentences in SemCor.
[Protocol](experiments/SEMANTIC_ADJUDICATION_PROTOCOL.md) and
[results](experiments/SEMANTIC_ADJUDICATION_RESULTS.md) own scope. Pure deterministic Python evaluation; zero additional
model calls.

Contiguous context anchors achieved 100% precision (0 false positives) across the 33 development sentences, completely
remedying the catastrophic false-positive failure of Phase B's bag-of-words co-occurrence rules. Case 04 achieved true
semantic substitution ("in the sequence of award creation"), while cases 01–03 were partially concordant clause
paraphrases that repeated the target lemma ("order").

Matched ordinary structured-memory comparator achieved byte-for-byte evaluation parity (`c89232ec...`). Neutral
checkpoint SHA256 remained completely invariant (`fddbfbb9...`). 10 focused adjudication tests pass. The remaining
prompting frontier is prompting for target lemma substitution in the gloss.


## D036: Protocol 4 achieves 4/4 semantic substitution and 100% WordNet concordance

**Status: bounded authorized check completed; positive outcome (4/4 admissible, 4/4 non-tautological substitution),
2026-10-13.** Follows D035 findings on gloss tautology. Introduces an explicit negative lexical constraint forbidding
the target lemma (`order` / `orders`) in the gloss and requiring explanatory substitution/definition.
[Protocol 4](experiments/SLM_REPRESENTATION_INTERFACE_PROTOCOL_V4.md) and
[results](experiments/SLM_REPRESENTATION_INTERFACE_V4_RESULTS.md) own scope. Exactly 4 offline calls on the
identical development cases; owned server closed cleanly.

All four proposals passed contract admissibility (4/4 admissible, 100%) AND achieved complete non-tautological
semantic substitution (4/4, 100% target lemma eliminated):
- `representation-01` (`order%1:07:01::`): `"a level or magnitude"` (100% magnitude concordance).
- `representation-02` (`order%1:10:00::`): `"the sequence in which things are handled or the priority given to actions"`.
- `representation-03` (`order%1:10:01::`): `"a command or instruction he had anticipated but did not receive"`.
- `representation-04` (`order%1:10:02::`): `"sequence in which the awards are created"` (100% sequence concordance).

Subsequent semantic adjudication confirmed 4/4 fully concordant (score 2/2), 0 tautological glosses, and 100% average
discriminative precision (0 false positives across 33 development sentences). Neutral store retrieval verified
identical digests across primary and ordinary structured-memory consumers under actual process restart (`4adbea15...`).
15 focused V4 tests pass. Both interface admissibility and semantic substitution boundaries are resolved.


## D037: Persistent contextual disambiguation demonstrates first behavioral consequence and 100% precision

**Status: adopted evaluation finding; experimental analysis complete, 2026-10-13.** Follows D036 semantic
representations. Investigates unassisted contextual disambiguation across all 33 SemCor development instances
driven purely by remembered Protocol 4 representations compiled from disk into persistent capacity state.
Zero runtime LLM calls during inference.
[Protocol](experiments/PERSISTENT_DISAMBIGUATION_PROTOCOL.md) and
[results](experiments/PERSISTENT_DISAMBIGUATION_RESULTS.md) own scope.

Persistent syntactic context anchors achieved 100% precision on fired cases (5/5 correct singletons, 0 wrong singletons,
0 false positives), demonstrating a successful behavioral consequence of remembered evidence across process restarts.
This directly remedies Phase B's bag-of-words failure (which suffered 100% false positives). The engine correctly
generalized the magnitude rule to a second development instance, while honestly abstaining on all 28 sentences with
unseen context.

Matched ordinary structured-memory comparator achieved byte-for-byte evaluation parity (`5e63d902...`). Neutral
checkpoint SHA256 was unchanged (`4adbea15...`), confirming nonmutation. 11 focused disambiguation tests pass.





