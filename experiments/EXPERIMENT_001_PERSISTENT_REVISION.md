# Experiment 001: Persistent Revision

**Status:** Draft mechanical-phase protocol; not yet executed.

**Purpose:** Turn the runtime specification into a small, reviewable first
experiment. Separate established requirements, proposed experimental choices,
and decisions still needed before a scientifically interpretable run.

## 1. Specification authority and scope

The [Minimal GFT Specification](../docs/MINIMAL_GFT_SPEC.md) controls where it
conflicts with the [Runtime Specification](../docs/GFT_RUNTIME_SPEC.md).
Runtime Section 19.1 defines the mechanical-phase requirements. Its numerical
defaults are provisional computational choices, not validated conceptual theory.
The broader [GFT Concept](../docs/GFT_CONCEPT.md) and
[Conceptual Geometry](../docs/CONCEPTUAL_GEOMETRY.md) remain research context.

This protocol does not silently amend those specifications. Choices labeled
**proposed** below are for review before implementation or use as acceptance
criteria. Missing choices must be recorded explicitly rather than filled in by
implementation convenience.

The mechanical phase excludes GPT/LLM integration, genetic evolution, autonomous
concept creation, a user interface, and unrestricted self-modification. It is a
precursor to the hybrid demonstration, not a claim to implement all of V0.1.
No fitness function is defined or required for this phase.

## 2. Research question and limited hypothesis

Can a fixed-seed GFT change its persistent disposition through structured
consequences, retain those changes across a process restart, and subsequently
revise them when given contrary evidence?

**Experimental hypothesis:** Different controlled histories can produce
different later action evaluations through inspectable persistent state, and
that state remains revisable rather than becoming a fixed preference.

Passing would demonstrate the specified state-transition and persistence
mechanics. It would not establish semantic understanding, consciousness, the
correctness of the conceptual geometry, or the effectiveness of a GFT–LLM hybrid.

## 3. Required substrate

### Completed baby step: structural birth

The project owner approved the exact Minimal Specification Section 4 hierarchy
as the first experimental starting point. `src/gft_lab/birth.py` now constructs
that hierarchy in memory; it does not implement the full runtime birth contract.

Recorded implementation conventions for this step:

- All 40 named entries are records: four domain roots at depth 0, twelve parent
  distinctions at depth 1, and twenty-four leaves at depth 2. There is no synthetic
  root. Lowercase label paths form stable IDs; genealogy is explicit.
- Seed version is `minimal-v0.1-seed-1`; initialization version is
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

**Limitation:** Uniform neutral baselines are a structural test fixture, not the
accepted Cultural-prior policy or proof of Psychological participation in
decisions. Those experimental choices remain open in Section 6A. This state
must not be presented as a complete V0.1 newborn or an executed experiment.

The owner's incremental implementation request permits this structural step
before resolving the behavior-related choices below. Numerical fixtures and
acceptance criteria must still be frozen before an evaluated experiment.

### Completed baby step: direct activation inspection

The owner approved the numerical example before attempting a manually interpreted
situation. `src/gft_lab/activation.py` implements only Runtime Section 9.1 and
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
they would be authored input, not meanings independently inferred by the GFT.

### Requirements for the eventual mechanical experiment

- Instantiate the complete seed from Minimal Section 4, including Cultural,
  Philosophical, Experiential, and Psychological domains.
- Keep genealogy distinct from non-genealogical relationships and memberships.
- Preserve activation, persistent baseline, salience, confidence, plasticity,
  and retention as distinct quantities under the runtime contract.
- Validate finite numbers, declared ranges, identifiers, and references before
  mutation. Record every consequential calculation and persistent change.
- Include bounded relationship consolidation as well as dispositional updates;
  Minimal Section 13 requires a minimal form of both for development.
- Preserve immutable events, configuration, provenance, checkpoints, and results.

The Scientific domain in Conceptual Geometry's candidate seed does not replace
the Experiential domain required by the controlling Minimal Specification.
This precedence does not resolve the broader theoretical comparison.

## 4. Proposed experimental design

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

These choices reduce engineering ambiguity without claiming new GFT theory:

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

Record the complete node inventory, stable IDs, parent links, depth convention,
and whether a synthetic root exists. Freeze per-node initial values, Cultural
priors, memberships, and initial association directions and weights.

Specify how Psychological nodes participate in decisions at birth. The action
formula multiplies by baseline, so zero baseline produces zero direct score
contribution. Do not manufacture a mature personality to hide this issue.
Specify whether genealogy has any activation effect; it is not automatically a
weighted association.

### B. Learning and evidence

Define which activation is credited by a later consequence: the earlier dilemma's
recorded activation, newly supplied evidence, or another explicitly approved rule.
Freeze the meaning and source of evidence confidence and consequence strength,
the confidence-counter update, association eligibility, and per-event caps.

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
failures. Record LLM use as absent rather than inventing model metadata.

Use a new run location for each attempt. Never overwrite historical evidence to
improve the result. Files under ignored `outputs/` or `logs/` directories are
not sufficient preservation by themselves; keep the required record in tracked
artifacts or a documented durable archive.

## 9. Small implementation sequence

1. Resolve and record the three decision groups above; freeze the protocol and
   numerical fixtures without running an outcome-driven calibration loop.
2. Implement validated state/event/configuration records and seed initialization.
3. Implement deterministic activation, scoring, bounded learning, association
   updates, and the minimal historical lookup required by novelty.
4. Implement traces, recoverable commits, checkpoints, and replay.
5. Run unit/recovery checks, then the fixed-history experiment and controls.

Report which checks passed, failed, or could not be evaluated. A successful
mechanical run permits discussion of the next research phase; it does not by
itself authorize GPT integration or expansion of the architecture.
