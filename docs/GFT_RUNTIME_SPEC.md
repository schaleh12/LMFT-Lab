# GFT Runtime Specification

**Status:** V0.1 provisional computational design  
**Depends on:** `MINIMAL_GFT_SPEC.md`  
**Purpose:** Convert the developmental GFT design into a small, transparent,
testable runtime without prematurely claiming that its first numerical choices
are final.

If this document conflicts with the Minimal GFT Specification, the Minimal GFT
Specification controls.

## 1. Runtime Goal

The V0.1 runtime must support one persistent developmental individual whose
later decisions can be measurably influenced by earlier experience without
depending on one permanent LLM token chain.

The runtime is successful only if it can show the causal path:

```text
event and retrieved memory
          ↓
inspectable GFT activation
          ↓
bounded persistent state change
          ↓
later GFT evaluation
          ↓
historically explainable difference in behavior
```

The runtime does not attempt to simulate an entire brain. It implements the
smallest stateful fuzzy system capable of development, continuity, reflection,
choice, and controlled interaction with an LLM.

## 2. Design Status

This specification distinguishes three levels of commitment:

- **Required:** necessary to conform to the Minimal GFT Specification.
- **V0.1 default:** the recommended first implementation, replaceable only by a
  documented design change.
- **Open:** intentionally requires experiment or owner judgment.

The formulas below are V0.1 defaults. Their purpose is to make the first
experiment runnable and falsifiable. They are not claims that these equations
are psychologically or philosophically final.

## 3. Runtime Components

The runtime consists of small modules with explicit boundaries:

1. **GFT core** — owns nodes, relationships, activation, evaluation, and
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

The GFT core must be usable in tests without an LLM. Deterministic structured
events must be sufficient to exercise activation, learning, choice, persistence,
and replay.

## 4. Structural Representation

### 4.1 V0.1 representation

**V0.1 default:** represent the GFT as a typed directed graph containing a fixed
seed hierarchy plus learnable cross-links and descendant concepts.

The hierarchy preserves conceptual genealogy. Cross-links represent fuzzy
participation and learned relationships. Keeping these separate prevents a
concept's birthplace from being mistaken for its complete meaning.

```text
seed hierarchy / genealogy:  parent → child
fuzzy conceptual geometry:   node ↔ node weighted relationships
developmental history:       event → state delta → resulting version
```

This is called a GFT because the seed and conceptual ancestry remain tree-like.
The runtime graph is not required to be a pure tree once fuzzy cross-membership
and learned association are represented.

### 4.2 Node record

Every node must contain:

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
- **retention** controls how slowly accumulated salience and orientation decay.

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

### 6.2 Provisional baseline policy

**Accepted V0.1 policy:** initialize most node baselines to `0.0`, confidence
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
enter the GFT through an immutable event envelope.

```yaml
event_id: stable identifier
individual_id: target individual
sequence: monotonically increasing integer
timestamp: recorded wall-clock time
kind: observation | dilemma | outcome | feedback | reflection | memory_recall
source: environment | teacher | llm | gft | developer
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

LLM-produced fields are proposals. The GFT core computes internal activation,
salience, orientation, and selection. The LLM may not send direct node mutation
commands through this contract.

## 8. Runtime Event Cycle

The supervisor processes one event transaction at a time:

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
14. Request LLM expression only for a GFT-selected communicative intention.

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

One event therefore cannot normally flip a mature, confident, retained
orientation. Repeated grounded evidence can still change it.

### 10.5 Confidence update

Confidence rises slowly when independent consequences repeatedly support the
same orientation and falls when credible evidence contradicts it. V0.1 should
implement this as a bounded evidence counter rather than ask the LLM to choose a
confidence value.

### 10.6 Relationship consolidation

When two nodes repeatedly activate in the same consequential episodes, the
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

## 11. Candidate Actions and GFT Selection

The environment or LLM may propose candidate actions. Each candidate must be
represented as predicted effects rather than persuasive prose:

```yaml
action_id: stable local identifier
description: human-readable inspection text
predicted_effects:
  node_id_a: float [-1, 1]
  node_id_b: float [-1, 1]
prediction_confidence: float [0, 1]
source: environment | teacher | llm | gft
```

The GFT scores each action:

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
replace the GFT's internal selection.

## 12. Communicative Intention Contract

When communication is selected, the GFT emits a structured intention:

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
  birth_config.yaml
  runtime_config.yaml
```

JSONL records are append-only. Snapshots are written to a temporary file,
validated, then atomically swapped into place. Each committed state records the
last applied event sequence and a content hash.

### 13.2 Episodic memory

An episode contains:

- source event range;
- participants and topics;
- structured concept memberships;
- decisions and consequences;
- resulting GFT deltas;
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
- current GFT activation and relevant persistent orientation;
- the recent conversational window;
- retrieved episodes and semantic records;
- active commitments and unresolved concerns;
- the current event and allowed task; and
- the applicable interface schema.

It does not receive the complete lifetime archive by default.

Before context rotation, the supervisor commits all completed events and
explicitly records unresolved work. A new LLM context receives a newly assembled
packet. Context identifiers are logged, but a context boundary does not create a
new GFT individual.

V0.1 retrieval may begin with transparent keyword, participant, recency, and
concept-membership scoring. Embeddings or a vector database are not required for
the first experiment.

## 15. Reflection and Idle Processing

Reflection is an internal event, not unrestricted free-running language.

It may be triggered by:

- high novelty;
- high conflict;
- high salience;
- unresolved commitments;
- repeated contradictory evidence;
- a scheduled consolidation interval; or
- an explicit GFT-selected request.

The GFT may perform cheap nonverbal consolidation without an LLM. An LLM-assisted
reflection returns structured candidate interpretations with provenance and
uncertainty. Those candidates re-enter the normal event cycle and receive no
automatic mutation privilege.

V0.1 should limit reflection by event count, update magnitude, and compute
budget. Reflection must terminate deterministically under test configuration.

## 16. Concept Admission

A linguistic concept proposed by GPT is admitted only when:

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

V0.1 permits the GFT to create provisional derived concepts automatically after
the admission checks above. Promotion to stable status requires human approval.
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
- retroactively change an event or fitness criterion; or
- impersonate a GFT-selected intention.

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
cache or archive structured responses so the GFT update path can be replayed.

Inspection tools must be able to answer:

- Why was this node activated?
- Which events changed this baseline or relationship?
- Which component proposed this concept or action?
- What did the GFT select before the LLM rendered language?
- What changed during reflection?
- Would replay with the same structured inputs produce the same core result?

## 19. First Runnable Experiment

### 19.1 Mechanical phase

Before using GPT, tests must prove that the core can:

1. create a newborn from the complete seed geometry;
2. process deterministic structured dilemmas;
3. update state within configured bounds;
4. preserve provenance for every update;
5. save, terminate, restore, and continue;
6. reproduce the same result from the same seed and event stream; and
7. diverge when given a deliberately different event stream.

### 19.2 Hybrid phase

Create two individuals from the same birth configuration. Give them controlled,
different developmental histories while keeping the teacher authority profile
and runtime configuration fixed. Force multiple LLM context rotations and one
process restart. Then present the same novel dilemma.

Measure:

- differences in activated structures;
- differences in candidate-action scores and selections;
- traceable historical causes of those differences;
- stability across context rotation and restart;
- the proportion of the final response attributable to GFT selection versus LLM
  rendering; and
- whether independent replay supports the explanation.

The experiment provisionally succeeds when later differences are persistent,
inspectable, reproducible at the GFT layer, and not reducible to different
persona prompts or hidden teacher edits.

## 20. Accepted V0.1 Development Policies

The project owner has accepted the following five policies for the initial
runtime and hybrid developmental experiment.

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

The GFT may create qualified provisional concepts automatically. Human approval
is required to promote a provisional concept to stable status in V0.1. This
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

This order establishes that the GFT works as a stateful decision substrate before
asking GPT to help it understand or express anything.
