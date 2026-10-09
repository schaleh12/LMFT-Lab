# Experiment 001: Persistent Revision

**Status:** Draft mechanical-phase protocol; not yet executed. Updated for the
LMFT direction. Numerical diagnostics now use the `lmft_lab` package; historical seed records remain versioned.

**First milestone:** Make the newborn LMFT change its mind in a traceable way,
save its state to disk, restart, and demonstrate that it remembers why. Show a
later behavioral consequence; fluent explanation alone is insufficient.

**Purpose:** Turn the runtime specification into a small, reviewable first
experiment. Separate established requirements, proposed experimental choices,
and decisions still needed before a scientifically interpretable run.

## 1. Specification authority and scope

The [Minimal LMFT Specification](../docs/MINIMAL_LMFT_SPEC.md) controls where it
conflicts with the [Runtime Specification](../docs/LMFT_RUNTIME_SPEC.md).
Runtime Section 19.1 defines the mechanical-phase requirements. Its numerical
defaults are provisional computational choices, not validated conceptual theory.
The broader [LMFT Concept](../docs/LMFT_CONCEPT.md) and
[Conceptual Geometry](../docs/CONCEPTUAL_GEOMETRY.md) remain research context.

This protocol does not silently amend those specifications. Choices labeled
**proposed** below are for review before implementation or use as acceptance
criteria. Missing choices must be recorded explicitly rather than filled in by
implementation convenience.

The mechanical phase excludes live LLM integration, genetic evolution, autonomous
concept creation, a user interface, and unrestricted self-modification. It is the
small V0.1 target, not the complete long-term hybrid architecture. Mocked LLM
recommendations are permitted when labeled and subjected to evidence checks.
No fitness function is defined or required for this phase.

## 2. Research question and limited hypothesis

Can a fixed-seed LMFT change its persistent disposition through structured
consequences, retain those changes across a process restart, and subsequently
revise them when given contrary evidence?

**Experimental hypothesis:** Different controlled histories can produce
different later action evaluations through inspectable persistent state, and
that state remains revisable rather than becoming a fixed preference.

Passing would demonstrate the specified state-transition and persistence
mechanics. It would not establish semantic understanding, consciousness, the
correctness of the conceptual geometry, or the effectiveness of an LMFT–LLM hybrid.

## 3. Required substrate

### Completed baby step: structural birth

The constructor now implements the canonical Section 4 seed with Contemplation,
Clarity, and Confidence under `lmft-v0.1-seed-1`. The explicit legacy converter
accepts only complete neutral `minimal-v0.1-seed-1` birth records, preserves its
input, and returns new state plus migration metadata. It performs no file writes
or conversion of external traces/relationships. Appendix A preserves the old seed.

Recorded implementation conventions for this step:

- All 40 named entries are records: four domain roots at depth 0, twelve parent
  distinctions at depth 1, and twenty-four leaves at depth 2. There is no synthetic
  root. Lowercase label paths form stable IDs; genealogy is explicit.
- Seed version is `lmft-v0.1-seed-1`; initialization version is
  `neutral-structural-scaffold-1`. The caller supplies individual ID, birth-event
  ID, and random seed. State version is zero. No randomness or clock is consulted.
- Each node has immutable, inspectable numerical values grouped in a `values`
  record: baseline and activation 0, salience and confidence 0.10, plasticity
  0.50, retention 0.70. These are the runtime's provisional neutral defaults.
- This constructor deliberately accepts only that structural initialization;
  it does not expose arbitrary changes to priors as an approved birth policy.
- Parent links have no computational influence yet. No memberships, cross-links,
  action selection, learning, event processing, memory, archive, or checkpoint is
  implemented. Birth-event IDs reserve provenance references; no event is emitted.

**Limitation:** Uniform neutral baselines are a structural test fixture, not a
validated Cultural-prior policy or proof of Psychological participation in
decisions. Those experimental choices remain open in Section 6A. This state
must not be presented as a complete V0.1 newborn or an executed experiment.

The owner's incremental implementation request permits this structural step
before resolving the behavior-related choices below. A neutral baseline fixture
is allowed for the small LMFT mechanical experiment. Numerical fixtures and
acceptance criteria must still be frozen before an evaluated experiment.

### Completed baby step: direct activation inspection

The owner approved the numerical example before attempting a manually interpreted
situation. `src/lmft_lab/activation.py` implements only Runtime Section 9.1 and
the temporary-reset behavior of Section 8. It is not the full event processor.

- A developer-authored input supplies stable node IDs and membership values.
  Agency `0.8` and Existence `0.3` are the first mechanical fixture; they carry
  no asserted semantic interpretation. Paired values are not normalized.
- Each call validates the entire input and returns an immutable activation frame
  for all 40 nodes. Omitted values become zero. Unknown IDs, non-finite values,
  and values outside `[0, 1]` are rejected rather than silently corrected.
- The frame preserves input ID, developer source/version, individual and birth
  IDs, seed/initialization/state versions, and the supplied value or omission
  behind every activation. Its rule version is `direct-only-1`.
- Activation is an ephemeral overlay; the immutable structural birth record and
  its persistent fields remain unchanged. Subsequent inputs start from zero,
  and previously returned frames remain unchanged and inspectable.
- No propagation, timestamps, event sequence enforcement, durable event archive,
  or full runtime event envelope exists yet. Input IDs are caller-supplied, and
  this calculation does not provide stream-wide duplicate detection.

This diagnostic path does not meet the full mechanical-phase acceptance criteria.
Human interpretations of a future imagined situation must be labeled by source;
they would be authored input, not meanings independently inferred by the LMFT.

### Completed baby step: bounded propagation

`src/lmft_lab/propagation.py` now applies Runtime Section 9.2 to explicitly
supplied directed `association` records. The owner authorized this mechanical
step; it does not establish the real seed's association network or semantics.

- Defaults are two synchronous passes and gain 0.25, as specified by the runtime.
  Every pass uses the preceding pass's activation and the original direct input:
  `clamp(direct + gain * sum(source_activation * weight), 0, 1)`.
- Genealogical links do not implicitly propagate. Only supplied active
  associations participate; negative weights reduce relevance, not baseline.
  Confidence and plasticity are recorded but are not extra multipliers in this
  formula. Neither relationships nor persistent node values change.
- Immutable results retain the direct-input frame, configuration, relationship
  records and source, and every pass's source contributions, sum, unclamped
  value, and clamped result. Rule version is `synchronous-association-1`.
- Deterministic summation uses relationship-ID order and `math.fsum`; node
  calculations use stable ID order. Duplicate relationship IDs or directed pairs
  are rejected in this diagnostic path to avoid accidental double-counting.
- The diagnostic API permits 0 through 100 passes and gain in `[0, 1]`; these
  are engineering limits, not validated cognitive properties. Zero passes or
  zero gain leaves direct activation unchanged. Cycles and self-links remain
  bounded by the same fixed pass count.
- Endpoint references and numerical fields are validated before calculation.
  Relationship provenance IDs are recorded as supplied; resolving them against
  an authoritative event archive remains future work.

Synthetic tests use existing node IDs only as numerical addresses. For unit
weights on A -> B -> C, direct A = 0.8 produces B = 0.2 on pass 1 and C = 0.05
on pass 2. This does not assert that the addressed concepts cause, imply, or
support one another. No synthetic edges are installed in the birth constructor.

No action selection, learning, semantic inference, persistence, or full
Experiment 001 execution is provided by this step.

The founding inventory in Minimal Section 4 is now canonical and frozen.
Experimental learning must revise separately identified judgments, relationships,
or interpretations, not seed names or parent-child links. Numerical rules remain
experimental and must be fixed for each evaluated run. The approved canonical seed migration is implemented; future changes to founding
geometry still require explicit approval.

### Requirements for the eventual mechanical experiment

- Instantiate the complete seed from Minimal Section 4, including Cultural,
  Philosophical, Experiential, and Psychological domains.
- Keep genealogy distinct from non-genealogical relationships and memberships.
- Preserve activation, persistent baseline, salience, confidence, plasticity,
  and retention as distinct quantities under the runtime contract.
- Validate finite numbers, declared ranges, identifiers, and references before
  mutation. Record every consequential calculation and persistent change.
- Include at least one bounded persistent belief/dispositional revision.
  Relationship consolidation is optional after this first milestone; the earlier
  requirement to implement both is superseded by Minimal Section 13.
- Preserve immutable events, configuration, provenance, checkpoints, and results.

Experiential remains the fourth-domain choice in all current specifications;
Scientific is preserved only as a historical alternative geometry hypothesis.

## 4. Proposed experimental design

The first implementation can use one individual and one read-only before/after
probe across revision and restart. The two-history design below remains the
controlled evaluation target; it does not require simultaneous agents or breeding.
Select in advance whether “change of mind” means a categorical reversal or a
specified judgment/score contrast. Retrieve the supporting and contrary evidence
after restart, not merely the saved score or an authored summary.

Use two independently identified individuals, A and B, with the same complete
birth configuration and recorded random seed. Use authored structured events
and abstract action identifiers; no language model interprets situations or
assigns conceptual meaning. Memberships and predicted effects are explicit
experimental inputs, not evidence that the system discovered their semantics.

**Proposed sequence:**

1. **Birth:** Validate and checkpoint both individuals. Evaluate a common probe
   to establish equal initial numerical results.
2. **Different histories:** Present matched structured dilemmas and separately
   recorded consequences. Change only the preregistered consequence evidence
   between A and B; hold event counts, candidate actions, and other inputs fixed.
3. **Persistence:** Commit a checkpoint, terminate the process, restore, and
   continue. Compare against an uninterrupted execution of each same history.
4. **Common probe:** Evaluate identical memberships and action candidates for
   both individuals. Compare baseline contributions, action scores, and choice.
5. **Revision:** Continue A with a fixed contrary-evidence sequence. Compare it
   with a controlled copy receiving a matched continuation of the original
   evidence. Preserve the branching checkpoint and source-history references.
6. **Final probe and replay:** Repeat the common probe, then independently replay
   each recorded history from birth and compare its numerical results.

Controlled copies are comparison runs, not evolutionary descendants produced by
mutation or selection. Their provenance must identify the common starting state.

Probe evaluation is proposed to be read-only: calculate activation and scores
on a temporary state without learning or persistent decay. Archive the probe
inputs and results separately. This prevents repeated measurement from itself
becoming unreported developmental experience.

The contrary-evidence sequence has a fixed length chosen before the run. Do not
continue adding events until an expected reversal appears. If the specified
revision does not occur, preserve and report that outcome.

## 5. Proposed mechanical conventions

These choices reduce engineering ambiguity without claiming new LMFT theory:

- Use deterministic evaluation mode for all mechanical trials; no exploration.
  Record the random seed even if the selected path consumes no randomness.
- Traverse nodes and relationships in stable identifier order. Break equal
  action scores by stable action identifier. Record the rule in configuration.
- Commit a dilemma before processing its separate consequence event. A
  consequence explicitly references the originating event and selected action.
- Use existing dependencies and standard-library file storage. JSON birth and
  runtime configuration is proposed instead of the runtime's example YAML files,
  avoiding an additional parser dependency.
- Treat the durable transaction commit record as authoritative. Recovery must
  distinguish committed work from incomplete writes and must never apply an
  event twice. Snapshot replacement alone is not a multi-file transaction.
- Keep event timestamps and run identity as provenance, not numerical inputs.
  Compare scientific state separately from differing wall-clock metadata.

The concrete persistence layout and recovery algorithm must be documented and
tested before any run is considered recoverable.

## 6. Decisions needed before the first run

Three bounded decision groups remain. They are not authorization to invent
answers in code.

### A. Birth and active pathways

Use the complete Section 4 target inventory, stable IDs, parent links, and
depths 0–2 with no synthetic root; record the new seed version and migration map. Freeze per-node initial values, Cultural
priors (or the explicitly neutral mechanical fixture), memberships, and initial association directions and weights.

Specify which Psychological pathways the experiment actually exercises. Full
psychological participation at birth is a later developmental target. The action
formula multiplies by baseline, so zero baseline produces zero direct score
contribution. Do not manufacture a mature personality to hide this issue.
Specify whether genealogy has any activation effect; it is not automatically a
weighted association.

### B. Learning and evidence

Define which activation is credited by a later consequence: the earlier dilemma's
recorded activation, newly supplied evidence, or another explicitly approved rule.
Freeze the meaning and source of evidence confidence and consequence strength,
the confidence-counter update and per-event caps. Association eligibility is
needed only if the optional relationship-consolidation experiment is included.

Define episode similarity and empty-history novelty, unknown-valence conflict,
and the risk penalty used in action scoring. Decide whether a mechanical-only
restriction to known outcomes and zero modeled risk is appropriate; do not
silently substitute those values for unspecified behavior.

Clarify whether `salience_retention` is the node's `retention` field, when decay
occurs, and whether baseline decay is part of this phase. The current baseline
equation supplies no such decay and does not use existing node confidence or
retention to resist change. Preserve the published equation unless a documented
design decision changes it.

### C. Fixed fixtures and comparison rules

Freeze the concrete event streams, node memberships, predicted effects,
consequence values, history lengths, restart point, and probe inputs. Specify
the expected direction of revision and minimum meaningful score difference
before execution. Do not select these thresholds after inspecting results.

Specify floating-point tolerances, state fields included in comparison, canonical
serialization/hash rules, duplicate-event behavior, and crash-recovery cases.
Record the final resolved configuration alongside this protocol's version.

## 7. Proposed acceptance checks

- **Birth:** The full configured seed is present and structurally valid.
- **Bounds:** All updates obey configured limits; invalid input cannot partially
  mutate scientific state.
- **Attribution:** Every baseline and relationship change has source evidence
  and a recorded calculation. No direct hidden state edits are permitted.
- **History effect:** A and B differ beyond the predefined tolerance on the same
  probe's action scores because their persistent state differs. Distinct selected
  actions are recorded, but are not required merely to manufacture a stronger claim.
- **Revision:** Contrary evidence moves A's preregistered probe-score contrast
  in the specified direction relative to the matched continuation control.
  A complete preference reversal is not required unless separately preregistered.
- **Continuity:** Restarted and uninterrupted executions agree under the frozen
  comparison rules; replay reproduces the same scientific state and decisions.
- **Reasons:** After restart, retrieve original evidence and accepted revision
  records that explain the changed probe result.
- **Authority:** Untrusted instructions and mock recommendations cannot rewrite
  protected founding configuration or execute code; rejected proposals are traced.
- **Recovery:** Interrupted writes and duplicate delivery cannot corrupt committed
  state or apply learning twice.

Include a learning-disabled comparison from the same birth state, explicitly
labeled as an experimental control rather than a conforming developmental runtime.
If the same claimed historical effect appears without persistent updates,
investigate leakage or measurement effects before attributing it to development.

These are mechanical acceptance criteria, not an evolutionary fitness function.
They must be finalized before the first evaluated run.

## 8. Evidence to preserve

Each run preserves its protocol/configuration version and hashes, source revision
and relevant uncommitted changes, Python/dependency/platform versions, seed,
individual/run IDs, full authored inputs, event/transaction records, deltas,
intermediate scores, checkpoints, restart/recovery records, comparisons, and
failures. Record LLM use as absent or mocked, with mock fixture/version when applicable;
do not invent real model metadata.

Use a new run location for each attempt. Never overwrite historical evidence to
improve the result. Files under ignored `outputs/` or `logs/` directories are
not sufficient preservation by themselves; keep the required record in tracked
artifacts or a documented durable archive.

## 9. Small implementation sequence

1. Resolve and record the three decision groups above; freeze the protocol and
   numerical fixtures without running an outcome-driven calibration loop.
2. Implement validated state/event/configuration records and seed initialization.
3. Reuse implemented activation/propagation, then add a deterministic probe,
   one bounded revision rule, and minimal evidence lookup. Association learning
   and richer novelty retrieval may follow as separately scoped experiments.
4. Implement traces, recoverable commits, checkpoints, and replay.
5. Run unit/recovery checks, then the fixed-history experiment and controls.

Report which checks passed, failed, or could not be evaluated. A successful
mechanical run permits discussion of the next research phase; it does not by
itself authorize LLM integration or expansion of the architecture.


## 10. Later comparisons and limits

Compare propagation-enabled and propagation-disabled runs, and later an LLM with
ordinary structured memory using matched evidence, model settings, and budgets.
Measure judgment revision, evidence retrieval, calibration, generalization, and
cost as appropriate; preregister metrics rather than selecting favorable ones.
A passing mechanical protocol does not demonstrate useful conceptual compression,
SLM internalization, autonomous contemplation, personality, or injection resistance
outside the tested cases. Clarity/coherence and evidence-based Confidence must be
evaluated separately; persuasive model output is not independent evidence.
