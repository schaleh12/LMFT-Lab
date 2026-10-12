# LMFT-Lab — current project state

Snapshot: **2026-10-12**. Action-aware correction starting HEAD:
`e61372e86e2b804ab53012d6de006ed7a401663b`, preserving seven dirty seed-study/handoff
files in a complete prework archive. Both experiments and handoff changes remain uncommitted.
Earlier evaluation starting commits remain in their original reports/archives; no
provenance was rewritten. Recheck actual Git status.

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
- New opt-in passive runtime modes: [guide](docs/PASSIVE_RELATIONSHIP_RUNTIME.md),
  [handler](src/lmft_lab/passive_relationship.py), [runtime](src/lmft_lab/runtime.py),
  [protocol](experiments/PASSIVE_RELATIONSHIP_PROTOCOL.md), [results](experiments/PASSIVE_RELATIONSHIP_RESULTS.md).
  Real inbox/outbox/receipts/checkpoints, pinned scenario policy, persisted candidate sets,
  separate support/validation status, rejection/dedup invariance and zero-call consensus.
- Explicit preservation contexts: [verification contract](experiments/PRESERVATION_VERIFICATION_CONTRACT.md),
  [results](experiments/PRESERVATION_VERIFICATION_RESULTS.md),
  [capture/audit CLI](experiments/verify_preservation.py),
  [current helper](src/lmft_lab/preservation_context.py). Nonempty complete current-source
  baselines for behavioral tests; separate original-byte historical audit, no fallback
  after missing/changed current contexts and no altered scientific criteria.
- Opt-in one-request acquisition: [guide](docs/ACTIVE_RELATIONSHIP_RUNTIME.md),
  [handler](src/lmft_lab/active_relationship.py),
  [protocol v1.2](experiments/ACTIVE_ACQUISITION_PROTOCOL_V1_2.md),
  [results](experiments/ACTIVE_ACQUISITION_RESULTS.md). Real clarification requests,
  pending budget/questions across restart, strict correlated synthetic verification,
  separate acquisition evidence and effective hypothesis filtering; no teacher calls.
- Optional receiver-attempt accounting: [protocol](experiments/RECEIVER_BUDGET_PROTOCOL.md),
  [results](experiments/RECEIVER_BUDGET_RESULTS.md), [tests](tests/test_receiver_budget.py).
  Explicit strict budget0..8; omission preserves unlimited default. Committed attempts
  survive restart and exhaustion denies later replies without false resolution.
  Physical rollback can repeat computation; no crash-proof physical cap is claimed.

## Latest completed milestone

The [action-aware correction study](experiments/ACTION_CORRECTION_RESULTS.md) separates
missing-part gathering from eligible verified replacement, reusing protected production
machinery unchanged. v2 adds the unchanged original selector after owner review;
v1 remains archived. Full/memory: 6 requests, 2 non-resolving, 6 decisions/4 correct;
original: 9 requests, 8 non-resolving (6 unresolved contradiction gathers), 4 decisions/3
correct. Exact scalar memory matches; combined action/eligibility policy benefit is
not a seed advantage. **565/565 integrity**, **630 full tests**, actual pending child
reload passed. Work/admissions/preparation costs are separate. Final archive
`outputs/action-correction-002/`; D016. Stopped for coordinator review.

The [seed-contribution study](experiments/SEED_CONTRIBUTION_RESULTS.md) reuses unchanged
Clarity wiring and its existing ablation. Intact resolved 4 new questions versus 7
ablated (three hurts/zero helps); all final decisions tie, four decided/three correct.
Exact scalar-memory scores/actions/predictions match. **222/222 integrity checks**,
actual standalone process reload and **588 checkout tests** passed. No production
code, seed, numerics, model configuration or migration changed. Two earlier attempts
remain preserved; final archive `outputs/seed-contribution-003/`. Full regression
artifact reuse is disclosed in the report; current raw artifacts are the second run.
See D015.

The [receiver accounting study](experiments/RECEIVER_BUDGET_RESULTS.md) adds an
opt-in acquisition-verifier cap, preserving old omitted-option behavior. Twenty-eight
actual runtime individuals (both modes, seven fixed sequences, restart/reference)
all halted; **618/618 integrity**, **84/84 quality**, **574 full current-checkout tests**
passed, including 22 receiver tests. Historical audit and all 3,043 original archive/
failure bytes still pass. Source/context archive: `outputs/receiver-budget-001/`.

Finite flood cap2 uses two committed/normal-process checks, then blocks the later
valid reply and remains ambiguous (50% coverage/75% decision accuracy). Finite
valid-first/false-valid/last-valid resolve within budget (100%/75%). A finite
legacy replay of six false replies plus valid uses seven checks and resolves.
Bad claims can therefore deny legitimate evidence: this tradeoff is explicit.
Memory matches exactly; no seed/numerical/model/migration changes or model calls.

Crucial scope: attempts are CHECKPOINT-accounted, not a hard physical bound. A real
child-process before-replace fault/replay makes two physical calls while final
committed attempts remain1 (budget1); after-replace replay makes one. Raw append-only
call markers and state/PID traces preserve this negative result. Durable pre-computation
reservation/recovery is NOT implemented; arbitrary ingress CPU/storage/network costs
remain outside the cap. Changed-budget restart rejects without checkpoint changes.

### Prior active acquisition milestone

Active relationship-acquire-lmft/memory modes connect nonempty ambiguity to the
existing runtime investigation transport. Generic predicted disagreement chooses
q2 before outcome access; one charged request survives pending restart, a verified
reply retains le, and reserved validation precedes predictions. Ordinary memory
matches exactly. Noninformative q1 does not resolve ambiguity; unavailable, unique
and unsupported families issue zero requests. Original training derivation is intact.

[Evaluated v1.2](experiments/ACTIVE_ACQUISITION_RESULTS.md): **540/540 integrity**,
**60/60 quality**, **34 targeted tests**, **552 full current-checkout tests**.
Twenty main individuals plus disabled control all halted. Coverage/decision accuracy:
informative and supported 100%/75%; noninformative/unavailable 50%/75%; unsupported
0%/undefined. Held-out fault errors remain. No fuzzy/LMFT advantage or model calls.
Archive `outputs/active-acquisition-001/`; complete 161-file current context and
separate historical audit passed. All 3,043 original archive/failure bytes are intact.

Requests, admitted facts and verification executions are DISTINCT: requesting
episodes have one request/unit, one acquisition/service observation, two acquisition
receiver checks (failed label plus valid); every condition has four training admissions
but five training checks, and four validation admissions/checks. v1/v1.1 remain;
v1.2 fixed cost naming and outcome-dependent expectation selection BEFORE reevaluation.
The earlier v1.1 harness/failed unit attempts are preserved, not rewritten.

That unlimited default still permits repeated eligible receiver work. The explicit
receiver option above adds only committed-attempt accounting; there is no timeout
or crash-proof physical reservation. The original active v1.2 result is unchanged.

### Preservation verification milestone

The focused verification correction separates current behavioral regression from
historical preservation (D012). Both harness defaults keep their historical prework
behavior; end-to-end tests EXPLICITLY use complete nonempty current contexts. Copied
contexts are pinned, checked before/after runs, and missing/changed contexts reject
at restart. No core learner/runtime behavior, source settings or scientific criteria changed.

Historical read-only audit passed **83 archived source entries / 134 protected entries**,
including **56 omitted source entries resolved from pinned historical Git bytes**;
the full 137-file original tree matches. Current-context studies retained original
**137/137 + 18/18** insufficiency and **274/274 + 36/36** passive checks. The first
full CURRENT CHECKOUT suite passed **516 tests**; two further process-restart context
tests bring focused coverage to 32. The final full current-checkout suite passed
**518 tests** under `outputs/preservation-full-regression-002/`, without skips or an
alternate checkout; exact commands/results are in the follow-up report.

All **3,043** original files across six archive/failure roots remain unchanged, including
the original **485-pass/1-failure** result. That historical failure is preserved, not
reclassified; no no-prework snapshot is used by corrected current tests. Derivative
audits/current studies are in fresh outputs. See [results/commands](experiments/PRESERVATION_VERIFICATION_RESULTS.md).

### Passive integration milestone

Passive relationship sets now use the supervised runtime in new opt-in
relationship-set-lmft/memory modes. The unchanged insufficiency learner/fixture supplies
registered evidence, finite selection and validation; new runtime wrapping persists
provenance/message links and returns explicit unvalidated/supported/ambiguous/unsupported
states. No active acquisition requests, teacher calls or numerical changes were added.
Twelve real runtime individuals plus a disabled/compatibility control all halted.
Standalone, memory and uninterrupted/restarted scientific state/behavior match.

Evaluated [run](experiments/PASSIVE_RELATIONSHIP_RESULTS.md): **274/274 integrity**,
**36/36 quality** checks. Quality is unchanged: unsupported 0% coverage, supported
100% coverage/75% accuracy, ambiguous 50% coverage/75% accuracy among decisions.
All 139 prior protected files match except the explicitly excluded runtime/handoff edits.
Archive: `outputs/passive-runtime-001/`; prework: `outputs/passive-runtime-prework-001/`.

**486 tests passed in an identical clean source snapshot**. The ordinary working-checkout
full suite had **485 passed/1 failed** because the historical insufficiency harness loads
an old local preservation manifest requiring runtime.py to be unchanged. That one
preservation failure is retained; no behavior check failed and old criteria/code were
not weakened. Snapshot/full-test paths, two earlier focused failure fixes and exact
reproduction instructions are in the report. That was the pre-correction outcome;
the explicit-context follow-up above now makes current behavioral tests independent
of the old local preservation directory, while default historical runs remain guarded.
Old checkpoints require archived source/configuration; there is no silent migration.

### Previous insufficiency milestone

The [insufficiency protocol](experiments/INSUFFICIENCY_PROTOCOL.md) and
[results](experiments/INSUFFICIENCY_RESULTS.md) test a NEW deterministic device fixture
that refuses length-two payloads. Verified training contradicts all six comparisons:
the learner retains `[]`, records `no_supported_hypothesis` and abstains on all eight
fresh in-scope cases. Supported le and ambiguous lt/le controls prevent blanket
abstention: respective coverage 100%/50%, accuracy among decisions 75%/75%.
Their preregistered device-fault errors are preserved. Ordinary memory matches exactly.
The new task does not change historical capacity truth. An empty set does not identify
why the family is insufficient or establish real-world theory invalidation.

Verified in the preceding insufficiency cycle: **461 tests pass**, primary and fresh reproduction each
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

Active implementation work: **passive, preservation, active acquisition and one receiver
accounting follow-up, bounded seed-contribution and action-aware correction experiments
complete; stopped for coordinator review** (D011–D016). No later task is dispatched.
Coordinator owns sequencing toward 2026-10-12 12:00 UTC (08:00 America/New_York);
this task stops safely at the review gate. Old source manifests, synthetic
verifier authority and phase isolation/deduplication remain material limits; current
versus historical preservation context is now explicitly separated and fail-closed.
Pinned Git/archives and the local historical trust anchor are required for the audit.
Next concrete limitation to assess is durable pre-computation reservation/recovery if a
hard PHYSICAL call bound is needed; it must address lost-result/admission tradeoffs and
cannot be inferred from the current logical cap. No redesign is implemented/dispatched.
Accepted-set revision and arbitrary-ingress receipt/storage growth remain outside scope.

## Verification and local evidence

From the repository root in PowerShell, when implementation verification or a new run is needed:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_capacity.py --output outputs/my-capacity-study
.\.venv\Scripts\python.exe experiments/run_ambiguity.py --output outputs/my-ambiguity-study
.\.venv\Scripts\python.exe experiments/run_insufficiency.py --output outputs/my-insufficiency-study
.\.venv\Scripts\python.exe experiments/run_passive_relationship.py --output outputs/my-passive-runtime-study
```

Use a fresh output path. Model setup/reproduction is separately documented in
[LOCAL_MODELS.md](docs/LOCAL_MODELS.md) and [LOCAL_TEACHER.md](docs/LOCAL_TEACHER.md).
For current standalone/passive behavioral reproduction, capture a fresh nonempty
context and supply --preservation-context; historical-default commands above retain
old preservation checks and can legitimately reject later source. Separate historical
audit and current regression commands are in [verification results](experiments/PRESERVATION_VERIFICATION_RESULTS.md#reproduce-separately).
Active harness requires --preservation-context explicitly; [active report](experiments/ACTIVE_ACQUISITION_RESULTS.md#reproduce-and-exact-artifacts)
records full current-checkout commands and fresh context/archive paths.

Reports locate complete local runs under `outputs/`, notably `capacity-001/`, `continuation-001/`,
`outcome-correction-001/` and `teacher-briefing-001/`. This handoff checked those directories,
results summaries, manifest-file presence and checkpoint counts; the previous handoff did
**not** verify every historical archive/hash or reproduce historical experiments. This session
verified the ambiguity archive hashes, checkpoint invariance and actual restarts. This
preceding cycle inspected and reproduced insufficiency with exact states/predictions, all stage
checksums, protocol/source/config guards and prior protected-file preservation.
This cycle verified actual passive runtime restarts, standalone/memory parity,
source/config/protocol archives, pure-probe/checkpoint invariance and all 139 protected files.
No external backup was verified.
[.gitignore](.gitignore) excludes outputs, logs, virtual environments, local caches, weights
and credential files; these are not conveyed by a Git checkout. Default model cache is
`%LOCALAPPDATA%/LMFT-Lab/cache`; its assets were not inspected in this task.

Checks in the passive cycle: handoff/spec/insufficiency/runtime review, actual Git/prework preservation,
frozen passive integration protocol, 25 new tests including eight atomic-fault cases,
real-runtime suite, 486-test clean-source snapshot suite, compatibility/disabled controls,
archive/protected hashes and halted-process checks. Failed focused/working-root attempts
remain in fresh outputs and are documented. No inference, downloads, pushes, publication,
discards, archive deletion or active acquisition. Only runtime registration/routing and
a new opt-in handler changed executable behavior; numerical/seed/model/migration code is intact.
Verification follow-up changed only context capture/audit and harness/test context selection.
It preserved the prior passive dirty work and original archives, ran separate historical
audit/current-context studies and full checkout tests; original scientific protocols are intact.
Active priority extended runtime registration/routing with a NEW handler, reused existing
numeric selector and investigation transport, and passed 552 current-checkout tests plus
540 integration/60 quality checks and historical audit. Prior passive/preservation dirty
work remains preserved; no active process, push, publication, teacher expansion or later dispatch.
Receiver follow-up passed 574 checkout tests plus 618 integration/84 quality checks,
actual pending/exhausted restarts and child-process physical rollback counterexamples.
Omitted-option default policy/state parity is preserved; optional budgets are pinned.
The subsequent owner-authorized bounded seed-contribution experiment passed 588 tests
and 222 integrity checks. Historical audit and all 3,043 baseline archive files still
pass. No transaction redesign, roadmap step2, chat demo or later task was dispatched.
Owner-authorized action-aware correction v2 subsequently passed 630 full tests and
565 integrity checks, preserving v1 and prior dirty work. No production changes.
