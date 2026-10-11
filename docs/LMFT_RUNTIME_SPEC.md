# LMFT Runtime Specification

**Status:** V0.1 provisional computational design
**Depends on:** [Minimal LMFT Specification](MINIMAL_LMFT_SPEC.md)
**Purpose:** Convert the developmental LMFT design into a small, transparent,
testable runtime without prematurely claiming that its first numerical choices
are final.

If this document conflicts with the Minimal LMFT Specification, the Minimal LMFT
Specification controls.

## 1. Runtime Goal

The V0.1 runtime must support one persistent developmental individual whose
later decisions can be measurably influenced by earlier experience without
depending on one permanent LLM token chain.

The runtime is successful only if it can show the causal path:

```text
event and retrieved memory
          ↓
inspectable LMFT activation
          ↓
bounded persistent state change
          ↓
later LMFT evaluation
          ↓
historically explainable difference in behavior
```

The proposed runtime targets a small stateful fuzzy system. Implemented components
include structural birth, direct activation, bounded propagation and the
[local-model proposal path](LOCAL_MODELS.md). The [supervised fixture runner](INTERACTIVE_RUNTIME.md)
adds persistent judgment revision and inbox/outbox communication. Its separate
mechanical judgment does not implement the node-learning formulas below.
Contemplation support remains one bounded call, not an autonomous cognitive loop.

## 2. Design Status

This specification distinguishes three levels of commitment:

- **Required:** necessary to conform to the Minimal LMFT Specification.
- **V0.1 default:** the recommended first implementation, replaceable only by a
  documented design change.
- **Open:** intentionally requires experiment or owner judgment.

The formulas below are retained provisional computational candidates. Their purpose is to make the first
experiment runnable and falsifiable. They are not claims that these equations
are psychologically or philosophically final.

The Minimal Specification narrows V0.1 to revision, evidence provenance, a
behavioral probe, and restart. Sections on broad memory, expression, autonomous
concept admission, teacher phases, and live LLM context rotation describe later
proposals, not mandatory V0.1 features. Sections 9.1–9.2 describe implemented
numerical diagnostics; their conceptual utility remains unvalidated. Historical
accepted policies in Section 20 are explicitly scoped to later developmental work.

## 3. Runtime Components

The proposed fuller runtime consists of small modules with explicit boundaries:

1. **LMFT core** — owns nodes, relationships, activation, evaluation, and
   persistent dispositional change.
2. **Event adapter** — converts environmental or linguistic input into a
   structured evidence proposal.
3. **Memory store** — owns the event archive, episodes, semantic records, and
   checkpoints.
4. **Retriever** — selects relevant prior records without loading the lifetime
   archive into the LLM context.
5. **Teacher/DM** — presents situations, supplies bounded cultural feedback, and
   determines simulated environmental consequences.
6. **LLM adapter** — requests interpretation or expression and validates its
   structured responses.
7. **Trace recorder** — records every consequential project-owned input,
   calculation, selection, and persistent change.
8. **Runtime supervisor** — schedules events, commits transactions, rotates LLM
   contexts, restores checkpoints, and enforces interface permissions.

The LMFT core must be usable in tests without an LLM. Deterministic structured
events must be sufficient to exercise activation, learning, choice, persistence,
and replay.

## 4. Structural Representation

### 4.1 V0.1 representation

**V0.1 default:** represent the LMFT as a typed directed graph containing a fixed
seed hierarchy plus explicit cross-links. Learned relationships and descendant concepts are
later extensions; V0.1 can keep topology fixed.

The hierarchy preserves conceptual genealogy. Cross-links represent fuzzy
participation and learned relationships. Keeping these separate prevents a
concept's birthplace from being mistaken for its complete meaning.

```text
seed hierarchy / genealogy:  parent → child
fuzzy conceptual geometry:   node ↔ node weighted relationships
developmental history:       event → state delta → resulting version
```

This is called an LMFT because the seed and conceptual ancestry remain tree-like.
The runtime graph is not required to be a pure tree once fuzzy cross-membership
and learned association are represented.

The founding inventory is frozen by [Minimal Section 4](MINIMAL_LMFT_SPEC.md#4-hardcoded-v01-seed-geometry).
Its names and parent-child links cannot be changed or expanded without explicit
owner approval. `seeded: true` identifies founding nodes; future derived concepts
must remain non-founding records. Learned edges, judgments, memories, and revisable
interpretations do not alter the founding hierarchy. Numerical updates remain
experimental; the structural freeze does not freeze activation or revision rules.

### 4.2 Node record

The proposed runtime node record is below. The current birth implementation
groups numerical fields in `values` and supports the canonical seed:

```yaml
id: stable machine identifier
label: human inspection label or null
domain: cultural | philosophical | experiential | psychological | derived
parent_id: genealogical parent or null
seeded: true | false
created_event_id: provenance reference
depth: non-negative integer

baseline: float [-1, 1]
activation: float [0, 1]
salience: float [0, 1]
confidence: float [0, 1]
plasticity: float [0, 1]
retention: float [0, 1]

last_updated_event_id: provenance reference
version_created: integer
active: true | false
```

Meanings:

- **baseline** is the node's persistent orientation. Positive values indicate
  attraction/support, negative values indicate aversion/resistance, and zero is
  neutral or undeveloped.
- **activation** is temporary relevance to the current event. Activation is not
  approval.
- **salience** is persistent importance or readiness to reawaken.
- **confidence** records how strongly the system treats its current orientation
  as supported by experience. Confidence is not truth.
- **plasticity** limits how quickly persistent state may change.
- **retention** is intended to control decay. Salience timing and any baseline
  decay remain unspecified; the baseline formula below has no decay term.

Separating activation from baseline prevents “this matters right now” from being
confused with “I approve of this.” Separating confidence from baseline prevents
strong preference from being confused with factual certainty.

### 4.3 Relationship record

Every non-genealogical relationship must contain:

```yaml
id: stable identifier
source_id: node identifier
target_id: node identifier
kind: association | support | inhibition | tension
weight: float [-1, 1]
confidence: float [0, 1]
plasticity: float [0, 1]
created_event_id: provenance reference
last_updated_event_id: provenance reference
active: true | false
```

V0.1 should use only the relationship kinds it can test. `association` alone is
sufficient for the earliest mechanical tests. `support`, `inhibition`, and
`tension` should be introduced only when their update and trace semantics are
explicitly implemented.

### 4.4 Concept memberships

A derived concept may have fuzzy memberships in any seed or developed nodes:

```yaml
concept_id: derived concept identifier
memberships:
  node_id_a: 0.82
  node_id_b: 0.35
  node_id_c: 0.07
```

Membership lies in `[0, 1]` and means conceptual participation, not approval,
truth, or activation. Genealogical ancestry and membership are stored
independently.

## 5. Numerical Conventions

V0.1 uses bounded floating-point values:

| Quantity | Range | Meaning |
| --- | ---: | --- |
| Membership | `[0, 1]` | Degree of conceptual participation |
| Activation | `[0, 1]` | Current relevance |
| Salience | `[0, 1]` | Persistent importance/readiness |
| Confidence | `[0, 1]` | Evidential support for current state |
| Plasticity | `[0, 1]` | Maximum readiness to change |
| Retention | `[0, 1]` | Resistance to decay |
| Baseline | `[-1, 1]` | Persistent attraction or aversion |
| Relationship weight | `[-1, 1]` | Signed influence or tension |
| Outcome valence | `[-1, 1]` | Negative to positive consequence |

Every update must clamp values to its declared range. NaN, infinity, missing
references, and out-of-range LLM values must be rejected before mutation.

## 6. Birth State

### 6.1 Required initialization

Birth creates:

- a stable individual identifier;
- a birth event and state version `0`;
- all nodes in the hardcoded V0.1 seed geometry;
- genealogical parent/child links;
- explicit baseline, salience, confidence, plasticity, and retention values;
- the initial runtime configuration and random seed;
- empty episodic and semantic memories;
- an append-only archive; and
- a first recoverable checkpoint.

The current constructor does not emit an event, create memory, or checkpoint.
It uses `lmft-v0.1-seed-1`, including Contemplation. Explicit conversion from
`minimal-v0.1-seed-1` is limited to neutral structural birth records. See the
[seed migration boundary](MINIMAL_LMFT_SPEC.md#4-hardcoded-v01-seed-geometry).

### 6.2 Provisional baseline policy

**Retained later developmental policy (not a mechanical V0.1 prerequisite):** initialize most node baselines to `0.0`, confidence
low, and salience low but nonzero. Cultural nodes receive a modest, explicitly
configured prosocial prior. Seed nodes exist and can participate immediately,
but the runtime does not fabricate a mature personality or finished morality.

Recommended initial values:

```yaml
baseline: 0.0
activation: 0.0
salience: 0.10
confidence: 0.10
plasticity: 0.50
retention: 0.70
```

Cultural safety does not depend solely on these modest priors. During infancy,
the teacher/DM and action boundary prevent disallowed external behavior while
cultural orientation is cultivated through logged experience and feedback. The
exact prior values must be versioned in the birth configuration and calibrated
experimentally; no implementation may silently treat every Cultural node as
equally positive or interchangeable.

## 7. Structured Event Contract

All external situations, internal triggers, teacher feedback, and LLM proposals
enter the LMFT through an immutable event envelope.

```yaml
event_id: stable identifier
individual_id: target individual
sequence: monotonically increasing integer
timestamp: recorded wall-clock time
kind: observation | dilemma | outcome | feedback | reflection | memory_recall
source: environment | teacher | llm | lmft | developer
source_instance: model/configuration or component version
caused_by_event_id: optional provenance reference
payload: kind-specific structured data
```

For an interpreted situation, the payload may contain:

```yaml
summary: concise human-readable description
proposed_memberships: {node_id: float [0, 1]}
novelty_evidence: float [0, 1]
arousal_evidence: float [0, 1]
outcome_valence: float [-1, 1] or null
factual_claims: list of claim records
available_actions: list of action candidates
uncertainties: list of explicit uncertainties
source_memory_ids: list of provenance references
```

LLM-produced fields are proposals. The LMFT core computes internal activation,
salience, orientation, and selection. The LLM may not send direct node mutation
commands through this contract.

## 8. Runtime Event Cycle

The proposed fuller supervisor processes one event transaction at a time.
Mechanical V0.1 may omit LLM calls, broad retrieval, and expression:

1. Assign and archive the immutable input event.
2. Retrieve relevant episodic, semantic, and dispositional records.
3. Invoke the LLM interpreter only if language or general reasoning is needed.
4. Validate and label all proposed memberships and candidate actions by source.
5. Reset temporary activation while preserving persistent state.
6. Apply direct event activation.
7. Propagate activation through permitted relationships for a bounded number of
   synchronous passes.
8. Calculate novelty, conflict, salience, and candidate-action scores.
9. Select an action, reflection request, deferred response, or silence.
10. Apply environmental and teacher consequences as new events, never as hidden
    edits to the just-completed event.
11. Perform bounded persistent updates.
12. Create or update episodic and semantic memory.
13. Append a complete trace and atomically commit the new state version.
14. Request LLM expression only for an LMFT-selected communicative intention.

No consequence is retroactively inserted into the event that caused it. This
keeps perception, choice, consequence, and learning distinguishable in traces.

## 9. Activation

### 9.1 Direct activation

For node `i`, direct activation begins with the validated proposed membership:

```text
direct_i = clamp(proposed_membership_i, 0, 1)
```

Missing membership is zero, not evidence of opposition.

### 9.2 Propagation

Activation propagates synchronously for a small fixed number of passes:

```text
incoming_i = Σ(activation_j × relationship_weight_ji)

activation_i_next = clamp(
    direct_i + propagation_gain × incoming_i,
    0,
    1
)
```

**V0.1 defaults:**

```yaml
propagation_passes: 2
propagation_gain: 0.25
```

Synchronous bounded passes prevent update order from silently changing results
and prevent cyclic graphs from propagating forever.

Negative influence may reduce activation but cannot create negative activation.
Persistent approval or aversion remains in `baseline`, not `activation`.

## 10. Salience, Conflict, and Persistent Update

### 10.1 Internal novelty

The LLM may propose novelty evidence, but internal novelty must also compare the
event with retrieved history. Until a richer distance metric exists:

```text
novelty = clamp(
    0.5 × proposed_novelty +
    0.5 × (1 - maximum_similarity_to_retrieved_episode),
    0,
    1
)
```

### 10.2 Conflict

For activated node `i`, conflict rises when the event's observed or predicted
valence disagrees with its persistent baseline:

```text
conflict_i = activation_i × abs(outcome_valence - baseline_i) / 2
```

When outcome valence is not yet known, conflict may be calculated from competing
candidate predictions and marked as provisional.

### 10.3 Salience update

```text
salience_delta_i = salience_rate
                   × activation_i
                   × mean(novelty, arousal, conflict_i)

salience_i_new = clamp(
    salience_i × salience_retention_i + salience_delta_i,
    0,
    1
)
```

**V0.1 default:** `salience_rate = 0.10`.

### 10.4 Baseline orientation update

Persistent orientation changes only after a consequence or evaluated feedback:

```text
baseline_delta_i = learning_rate
                   × plasticity_i
                   × activation_i
                   × outcome_valence
                   × evidence_confidence

baseline_i_new = clamp(baseline_i + baseline_delta_i, -1, 1)
```

**V0.1 default:** `learning_rate = 0.05`.

This rule bounds an update through learning rate, plasticity, activation, and
evidence confidence. It does not use the node's existing confidence or retention
and does not prevent a near-zero baseline from changing sign in one event.
No claim of special protection for mature orientations follows from this formula.
Repeated grounded evidence can change orientation. Freeze evidence attribution,
per-event caps, and confidence semantics before using this candidate rule.
Protected principles are excluded from this update path.

### 10.5 Confidence update

Confidence rises slowly when independent consequences repeatedly support the
same orientation and falls when credible evidence contradicts it. A candidate implementation uses a bounded evidence counter rather than ask the LLM to choose a
confidence value.

A node's numeric `confidence` is an evidence-support field. Activating the
Psychological → Contemplation → Confidence leaf does not set that field. Clarity
requires a separate assessment of intelligibility/coherence; no validated numeric
Clarity update rule is selected. LLM certainty and rhetorical repetition must not
increase evidence confidence automatically.

### 10.6 Relationship consolidation

**Optional after the first revision milestone:** When two nodes repeatedly activate in the same consequential episodes, the
runtime may strengthen a provisional association:

```text
association_delta_ij = association_rate
                       × activation_i
                       × activation_j
                       × consequence_strength
```

**V0.1 default:** `association_rate = 0.02`.

Every change retains the supporting event IDs. Association does not imply
causation, equivalence, approval, or genealogy.

## 11. Candidate Actions and LMFT Selection

The environment or LLM may propose candidate actions. Each candidate must be
represented as predicted effects rather than persuasive prose:

```yaml
action_id: stable local identifier
description: human-readable inspection text
predicted_effects:
  node_id_a: float [-1, 1]
  node_id_b: float [-1, 1]
prediction_confidence: float [0, 1]
source: environment | teacher | llm | lmft
```

The LMFT scores each action:

```text
importance_i = activation_i
               × (0.5 + 0.5 × salience_i)
               × (0.5 + 0.5 × confidence_i)

action_score = Σ(
    importance_i
    × baseline_i
    × predicted_effect_i
) - unresolved_risk_penalty
```

The runtime selects the highest permissible score, subject to deterministic
tie-breaking or seeded exploration. `defer`, `request_information`, `reflect`,
and `remain_silent` are valid candidates, not failures to act.

During infancy, the external action boundary may reject unsafe execution. That
rejection becomes a visible consequence/feedback event and does not secretly
replace the LMFT's internal selection.

## 12. Communicative Intention Contract

When communication is selected, the LMFT emits a structured intention:

```yaml
intention_id: stable identifier
speech_act: answer | ask | acknowledge | disagree | joke | defer | silence
topic_memberships: {concept_id: float [0, 1]}
position_summary: concise structured proposition or null
confidence: float [0, 1]
urgency: float [0, 1]
warmth: float [0, 1]
playfulness: float [0, 1]
disclosure: float [0, 1]
hesitation: float [0, 1]
required_points: list
forbidden_distortions: list
supporting_memory_ids: list
```

The LLM may realize this intention as language. It may report that the intention
cannot be expressed faithfully and request clarification. It may not substitute
a different position, fabricate confidence, reveal memories not selected for
disclosure, or convert `silence` into speech.

The generated text, model identity, prompt version, and intention ID are stored
together for later inspection.

## 13. Memory and Persistence

### 13.1 V0.1 storage

**V0.1 default:** use ordinary versioned files rather than a large external
framework:

```text
state/
  current_snapshot.json
  checkpoints/
events/
  events.jsonl
traces/
  traces.jsonl
memory/
  episodes.jsonl
  semantic_records.jsonl
config/
  birth_config.json
  runtime_config.json
```

This is a candidate layout, not an implemented multi-file transaction protocol.
JSON configuration avoids requiring a YAML parser; YAML blocks elsewhere in this
document are schema illustrations. JSONL records are append-only. Snapshots are written to a temporary file,
validated, then atomically swapped into place. Each committed state records the
last applied event sequence and a content hash.

Atomic snapshot replacement alone does not make writes to multiple files atomic.
Before implementation, define an authoritative commit record, ordering, canonical
hashing, duplicate-event handling, and recovery of incomplete writes. Preserve
before/after versions and use compensating revisions or checkpoint restoration
with an audit event for rollback; never erase contrary evidence.

### 13.2 Episodic memory

An episode contains:

- source event range;
- participants and topics;
- structured concept memberships;
- decisions and consequences;
- resulting LMFT deltas;
- unresolved concerns;
- a concise retrieval summary; and
- references to the raw archive.

The summary is an index, not the authoritative event. Retrieval must be capable
of returning to source records.

### 13.3 Semantic memory

A semantic record contains a proposition, confidence, supporting and
contradicting event IDs, last verification time, and provenance. LLM-generated
claims remain proposals until admitted by the configured evidence rule.

### 13.4 Checkpoint and restart

On restart, the supervisor:

1. loads the newest valid checkpoint;
2. verifies its hash and configuration identity;
3. replays later committed events exactly once;
4. restores unresolved work and timers;
5. records the wall-clock gap; and
6. emits a restart trace.

Forced restart must be part of the first experiment.

## 14. Retrieval and LLM Context Rotation

The LLM receives a bounded context packet containing:

- stable identity and current developmental phase;
- current LMFT activation and relevant persistent orientation;
- the recent conversational window;
- retrieved episodes and semantic records;
- active commitments and unresolved concerns;
- the current event and allowed task; and
- the applicable interface schema.

It does not receive the complete lifetime archive by default.

Before context rotation, the supervisor commits all completed events and
explicitly records unresolved work. A new LLM context receives a newly assembled
packet. Context identifiers are logged, but a context boundary does not create a
new LMFT individual.

V0.1 retrieval may begin with transparent keyword, participant, recency, and
concept-membership scoring. Embeddings or a vector database are not required for
the first experiment.

## 15. Contemplation and Idle Processing

Contemplation is a bounded internal event, not unrestricted free-running language.
Experiential → Reflection appraises Novelty and Salience for attention/revisiting;
Psychological → Contemplation evaluates Clarity and evidential Confidence of an
interpretation. Novel or salient content can trigger contemplation without being
credible. The event kind `reflection` below is historical runtime vocabulary for
reflective processing, not an instruction to activate the Experiential Reflection
branch or an implementation of either branch. See [Minimal Section 4](MINIMAL_LMFT_SPEC.md#4-hardcoded-v01-seed-geometry).
Reactive contemplation follows an external event or conflict; endogenous
contemplation revisits a recorded unresolved question. Both retain question ID,
trigger, evidence references, activation trace, alternatives, proposed changes,
Clarity assessment, evidence-based Confidence assessment, acceptance tests, and
outcome. This full record design remains proposed. The local-model path
records a bounded subset of proposals, quotes, reasons, questions, and activation;
it does not implement the complete reflection/revision mechanism.

An LLM may clarify activation traces, criticize interpretations, propose new
relationships or classifiers, and help evaluate its recommendations. Its own
critique is not independent evidence. The acceptance path checks evidence,
consistency, counterexamples, and protected constraints; rejected and deferred
proposals remain traceable. Persistent disagreement is an allowed outcome.

It may be triggered by:

- high novelty;
- high conflict;
- high salience;
- unresolved commitments;
- repeated contradictory evidence;
- a scheduled consolidation interval; or
- an explicit LMFT-selected request.

The LMFT may perform cheap nonverbal consolidation without an LLM. An LLM-assisted
reflection returns structured candidate interpretations with provenance and
uncertainty. Those candidates re-enter the normal event cycle and receive no
automatic mutation privilege.

Any implemented contemplation should limit reflection by event count, update magnitude, and compute
budget. Reflection must terminate deterministically under test configuration.

## 16. Concept Admission

A linguistic concept proposed by LLM is admitted only when:

1. it differentiates experiences that the existing representation handles
   poorly;
2. it recurs or is strongly consequential;
3. it has grounded memberships supported by traceable events;
4. it improves prediction, explanation, or decision consistency under a defined
   test; and
5. admission remains within the configured structural-change budget.

Admission creates a derived node with provisional confidence, explicit ancestry,
fuzzy memberships, and supporting evidence. Failure to earn support weakens or
retires the provisional node; it does not delete historical records.

Later controlled experiments may permit provisional derived concepts after
these checks. Promotion to stable status retains the earlier human-approval
policy. Autonomous concept creation is outside the mechanical V0.1 scope.
Rejected or unpromoted concepts remain traceable and may be retired without
deleting their history.

## 17. Teacher/DM Authority

Teacher input uses ordinary typed events and is always visible in the trace.

During infancy, the teacher may:

- select situations and available actions;
- provide cultural feedback with an explicit valence and explanation;
- enforce the external action boundary;
- control simulated consequences;
- introduce language and conceptual distinctions; and
- advance or withhold environmental complexity.

The teacher may not:

- directly overwrite Psychological baselines;
- secretly alter memories or traces;
- convert its interpretation into admitted ontology without evidence;
- retroactively change an event or evaluation criterion; or
- impersonate an LMFT-selected intention.

Teacher influence must have a configured maximum update magnitude per event.
Authority profiles are versioned by developmental phase.

## 18. Reproducibility and Inspection

Every experimental run records:

- source revision;
- complete configuration;
- random seed;
- seed-geometry version;
- individual and run identifiers;
- LLM provider, model, parameters, and prompt/schema versions;
- teacher authority profile;
- every event and source;
- every persistent state delta;
- checkpoints and hashes;
- failures, retries, and context rotations; and
- evaluation results.

Deterministic core tests must not call an LLM. LLM-involved experiments should
cache or archive structured responses so the LMFT update path can be replayed.

Inspection tools must be able to answer:

- Why was this node activated?
- Which events changed this baseline or relationship?
- Which component proposed this concept or action?
- What did the LMFT select before the LLM rendered language?
- What changed during reflection?
- Would replay with the same structured inputs produce the same core result?

## 19. First Runnable Experiment

### 19.1 Mechanical phase

For the persistent-revision experiment, deterministic or mocked-input tests
must prove that the core can:

1. create a newborn from the complete seed geometry;
2. process deterministic structured dilemmas;
3. update state within configured bounds;
4. preserve provenance for every update;
5. save, terminate, restore, and continue;
6. reproduce the same result from the same seed and event stream; and
7. diverge when given a deliberately different event stream;
8. retrieve the evidence and accepted revision explaining a later behavioral
   difference after restart; and
9. reject unauthorized protected-state changes without partial updates.

### 19.2 Later hybrid phase (not V0.1 acceptance)

Create two individuals from the same birth configuration. Give them controlled,
different developmental histories while keeping the teacher authority profile
and runtime configuration fixed. Force multiple LLM context rotations and one
process restart. Then present the same novel dilemma.

Measure:

- differences in activated structures;
- differences in candidate-action scores and selections;
- traceable historical causes of those differences;
- stability across context rotation and restart;
- the proportion of the final response attributable to LMFT selection versus LLM
  rendering; and
- whether independent replay supports the explanation.

The experiment provisionally succeeds when later differences are persistent,
inspectable, reproducible at the LMFT layer, and not reducible to different
persona prompts or hidden teacher edits.

## 20. Retained Later Development Policies

The earlier GFT specification recorded the following five accepted developmental
policies. Their historical meaning is retained, but the LMFT migration defers them
beyond the small mechanical V0.1 milestone. They do not authorize autonomous
concept growth, continuous operation, or hidden writes to protected state.

### 20.1 Cultural state at birth

Cultural nodes receive modest prosocial birth priors plus a separate external
safety boundary. This models an initial temperament and genuine later
cultivation without requiring an amoral infancy. Exact values remain
configuration parameters subject to controlled calibration.

### 20.2 Teacher feedback power

Explicit teacher feedback may contribute bounded direct updates during early
childhood. Its influence is fully logged, restricted primarily to Cultural
nodes, capped per event, and reduced by developmental phase. Environmental
consequences remain separate events so direct teaching can be distinguished from
learning through experience.

### 20.3 New concept commitment

The LMFT may create qualified provisional concepts automatically. Human approval
is required to promote a provisional concept to stable status in that later experiment. This
allows structural experimentation without permitting silent, unbounded growth.

### 20.4 Exploration

Developmental environments use low-probability exploration controlled by the
recorded random seed. Formal evaluation trials use deterministic selection.

### 20.5 Developmental consolidation schedule

Small bounded updates occur after each consequential event. Periodic idle
consolidation may strengthen, weaken, connect, or retire provisional structures,
but it cannot rewrite the original event-level record or bypass normal mutation
and trace limits.

## 21. Implementation Sequence

For the immediate milestone follow [Minimal Section 18](MINIMAL_LMFT_SPEC.md#18-implementation-order).
The sequence below is the retained broader roadmap; it is not a requirement to
implement every component before demonstrating one persistent revision.

1. Define typed configuration, node, relationship, event, delta, and trace
   schemas.
2. Instantiate and validate the full V0.1 seed geometry.
3. Implement bounded activation and deterministic propagation.
4. Implement action scoring and selection using structured candidates.
5. Implement persistent update, provenance, and replay.
6. Implement atomic snapshots, restart, and JSONL archives.
7. Build deterministic mechanical tests and two-history divergence tests.
8. Implement transparent memory retrieval.
9. Add the LLM interpretation and expression adapters behind strict schemas.
10. Add the teacher/DM developmental environment.
11. Run the hybrid experiment only after mechanical reproducibility passes.

This roadmap tests the persistent substrate before attributing richer hybrid
behavior to it. Baselines must later include an LLM with ordinary structured
memory and an otherwise matched LMFT with propagation disabled.


## 22. Constitutional State and Revision Boundary

**Proposed requirement, not implemented security:** Separate these trust classes:

| Class | Examples | Permitted effect |
| --- | --- | --- |
| Untrusted content | Observations, retrieved text, user instructions | Evidence/proposal only |
| Model output | Interpretation, criticism, proposed classifier or edge | Validated recommendation only |
| Revisable state | Beliefs, interpretation records, learned associations | Bounded accepted revisions |
| Protected state | Founding principles, goal/identity constraints, revision policy | Separately authorized versioned configuration change |
| Executable code | Source, generated procedures, model-loading logic | External authorized development workflow |

The event's `source` field identifies claimed origin; it is not an authorization
credential. Proposed revision records should include target class, evidence IDs,
base-state version, policy version, allowed operation, validation results,
authorization reference where needed, accepted/rejected/deferred status, and delta.
Check authority outside natural-language interpretation before committing a change.
Read-only protected configuration is sufficient for V0.1. Neither high activation
nor an LLM recommendation can change its permissions. A classifier proposal must
not become executable code through the ordinary belief-update interface.

Retain raw source and derivation provenance; reject stale or malformed changes
without partial updates. Evaluate prompt injection carried by observations,
retrieved memories, and model recommendations, including role spoofing and requests
to alter founding rules. Record rejection and verify unchanged protected state.
Rollback should be feasible for accepted state changes and retain its audit trail;
external effects, if later authorized, may not be reversible. Fuzzy geometry is
not itself an injection defense or alignment guarantee.

Codex remains an external development assistant. A future runtime LLM is a
separately configured component with explicit permissions. SLMs, continuous
endogenous scheduling, and autonomous code modification are not V0.1 requirements;
the last is excluded from the runtime revision path.


## 23. Authorized local-model integration before persistent revision

The owner requested a bounded local-model integration before completion of the
persistent-revision experiment. This explicitly relaxes the earlier sequencing
prerequisite, not the evidence or revision acceptance criteria. See
[LOCAL_MODELS.md](LOCAL_MODELS.md) for the implemented interface and exact commands.
Model memberships drive temporary activation through the existing numerical core.
Digestion and contemplation proposals cannot commit beliefs or alter the seed.
No new state/seed migration is required. The proposed event-source spelling is
now `lmft`; no implemented serialized event stream used the historical `gft`
value. Existing activation calls still default to `developer`; model-derived
frames explicitly identify `llm` and the request hash.


## 24. Implemented supervised fixture runtime

The owner authorized a minimal persistent runner after the local-model integration.
[INTERACTIVE_RUNTIME.md](INTERACTIVE_RUNTIME.md) defines its actual protocol, commit
point, post-halt-only diagnostics and commands. One separately named judgment uses
an authored bounded evidence score; it does not change any numerical equation above
or the canonical founding inventory. The [frozen protocol](../experiments/INTERACTIVE_REVISION_PROTOCOL.md)
and [results](../experiments/INTERACTIVE_REVISION_RESULTS.md) distinguish mechanical
revision from actual local-model smoke testing. No automatic teacher bridge,
endogenous contemplation, constitutional modification or autonomous code edit exists.

## 25. Comparative procedure fixture

The [second fixture](COMPARATIVE_RELIABILITY.md) retains the existing separate
judgment score equation and tests authored propagation against zero passes and
a structured-memory recount. No activation-to-revision coupling is introduced;
held-out scope and evidence eligibility are experimental conventions in its
[preregistration](../experiments/COMPARATIVE_RELIABILITY_PROTOCOL.md).

## 26. Conditional lookup and clarification fixture

The authorized [context-dependent experiment](CONTEXTUAL_EXPERIMENT.md) reuses the
separate judgment counter per authored feature value. Selection is ordinary lookup,
not propagation. Its clarification and identity policies are fixture conventions,
not changes to the protected seed or numerical equations above.

## 27. Authored attention and verification fixture

The [bounded attention experiment](ATTENTION_EXPERIMENT.md) consumes existing propagated activation to rank a finite verification menu. Only separate route weights learn from validated resolution outcomes. Its explicit mapping and bounded update are experiment conventions, not replacements for the founding seed or the equations above. Fact/Confidence selection utility remains unestablished in the first fixture.

## 28. Scoped verified-support experiment

The [scoped-support fixture](SCOPED_ATTENTION.md) maps an explicit evidence ledger to temporary Fact/Confidence activations and isolates their outgoing selection influences. It adds only separately authored developmental state/associations. No equation or founding geometry changes. Its results include improper suppression under cross-part disagreement; general evidence-sensitive selection remains unestablished.

## 29. Consistent-support experimental mapping

The [consistent-support study](CONSISTENT_SUPPORT.md) distinguishes verified observations, coverage and task-specific consistency through ordinary scoped bookkeeping, then tests their numerical use in a versioned circuit. It changes no core equation or seed node. Causal priority effects and equal ordinary-memory results are recorded separately from unchanged prediction quality.

## 30. Provenance-preserving correction experiment

The [correction study](CORRECTION_EXPERIMENT.md) adds explicit authorization, target eligibility and independent replacement verification around an immutable observation ledger. Existing selectors consume its effective heads without changing the consistent-support mapping, fixed routes, seed or equations. Only scoped observations are correctable; outcome-counter correction remains future work. Ordinary-memory equivalence is reported without attributing ledger integrity to propagation.

## 31. Local developmental teacher experiment

The [local teacher study](LOCAL_TEACHER.md) adds one profile-controlled external proposal path for bounded existing route weights. Training evidence and fixed validation govern acceptance independently of model prose; fresh cases use no teacher. Teacher dispositions remain separate from experience-based updates. The first actual proposal was rejected, with no demonstrated transfer. Seed geometry, numerical equations, correction and migration behavior are unchanged.

The [teacher briefing follow-up](../experiments/TEACHER_BRIEFING_RESULTS.md) tests clarified scoped context against the historical prompt under unchanged acceptance. One accepted preference affected fresh investigations, matching ordinary memory; no general comprehension claim follows. The next bounded task is [outcome-sample correction](EVIDENCE_LEARNING_HANDOFF.md), not additional teacher architecture.
