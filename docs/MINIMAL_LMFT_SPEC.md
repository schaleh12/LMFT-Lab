# Minimal LMFT Specification

**Status:** V0.1 documentation target; structural birth, direct activation,
bounded propagation, a local-model proposal path and a narrow
[supervised persistent fixture runtime](INTERACTIVE_RUNTIME.md) are implemented. The code uses the canonical seed in Section 4; Appendix A preserves
the historical seed for explicit compatibility conversion. This specification controls scope when the runtime or older
experiment proposals conflict with it.

## 1. Purpose

The first meaningful experiment is: **make the newborn LMFT change its mind in a
traceable way, save its state to disk, restart, and demonstrate that it remembers
why.** This is a small persistence and evidence-revision experiment, not a complete
cognitive architecture or proof of consciousness or conceptual understanding.

## 2. Core Research Commitments

LMFT investigates persistent fuzzy conceptual development through repeated LLM
interaction. The language model may teach, clarify, criticize, and reason; its
contributions remain identifiable proposals. The persistent core evaluates and
records admitted revisions through explicit evidence and policy checks. Codex is
the external development assistant, distinct from any future runtime LLM.

The seed serves as a philosophical or religion-like constitution without worship,
supernatural commitments, or assumed consciousness. Protect founding principles
and revision rules while allowing interpretations and ordinary beliefs to change.
An English seed label alone supplies neither a policy nor a validated meaning.

## 3. The Minimum Individual

V0.1 needs versioned seed/configuration, persistent revisable state, immutable
evidence events, accepted/rejected revision traces, a recoverable checkpoint,
and a small lookup from a current judgment to its supporting and contradicting
records. A deterministic probe must reveal a behavioral consequence of revision.
A simple file-backed implementation is sufficient; separate memory services,
multiple SLMs, and a live LLM are unnecessary. Mock recommendations must be marked
as mocks. Record model/prompt/configuration identity if a real LLM is later used.

## 4. Hardcoded V0.1 Seed Geometry

**Canonical founding geometry — frozen for LMFT V0.1.** The exact 40 nodes
below, their names, domain organization, order, and parent-child relationships
are fixed: four domain roots, twelve distinctions, and twenty-four leaves, with
no synthetic root. Do not rename, remove, rearrange, or expand this founding seed
without explicit project-owner approval. Contemplation is the canonical name;
Discipline exists only in the historical implementation in Appendix A.

The freeze is a structural research decision, not proof of a universal geometry.
Activation, memberships, priors, propagation, confidence calibration, and revision
rules remain experimental and versioned. Paired memberships are currently treated
as independent, not complementary; the freeze does not finalize their mathematics.

```text
LMFT V0.1 SEED GEOMETRY

├── CULTURAL
│   ├── Efficiency
│   │   ├── Power
│   │   └── Wastelessness
│   ├── Justice
│   │   ├── Honor
│   │   └── Fairness
│   └── Freedom
│       ├── Self-Sufficiency
│       └── Needlessness
│
├── PHILOSOPHICAL
│   ├── Being
│   │   ├── Agency
│   │   └── Existence
│   ├── Structure
│   │   ├── Order
│   │   └── Chaos
│   └── Persistence
│       ├── Continuity
│       └── Discreteness
│
├── EXPERIENTIAL
│   ├── Reflection
│   │   ├── Novelty
│   │   └── Salience
│   ├── Phase
│   │   ├── Valence
│   │   └── Arousal
│   └── Synchronization
│       ├── Resonance
│       └── Entrainment
│
└── PSYCHOLOGICAL
    ├── Will
    │   ├── Intention
    │   └── Execution
    ├── Truth
    │   ├── Theory
    │   └── Fact
    └── Contemplation
        ├── Clarity
        └── Confidence
```

Continuity concerns persistence across time; Discreteness concerns bounded events
or transitions. Genealogy differs from fuzzy membership and from propagation
edges. Experiential is retained from the established seed; Scientific was an
older alternative, not a requested replacement.

Founding nodes are distinct from learned concepts, non-genealogical relationships,
judgments, memories, and interpretations. Those developmental records may refer
to founding nodes without becoming founding nodes or altering their labels or
parent links. Any later learned descendants must remain separately identified as
non-founding; they do not expand the canonical seed inventory. Revising an
interpretation of a principle must not silently revise the seed itself.

| Branch | Responsibility | Does not establish |
| --- | --- | --- |
| Experiential → Reflection → Novelty / Salience | Appraise how an experience differs from prior experience and how important it is for attention or later revisiting | Whether its interpretation is coherent, true, or well supported |
| Psychological → Contemplation → Clarity / Confidence | Deliberate about interpretations, uncertainty, conflicts, and questions; assess intelligibility/coherence separately from evidence/justification | That novelty, attention, or a persuasive explanation supplies evidence |

Reflection can flag an experience for Contemplation. Contemplation may propose a
revised interpretation or future attention priority through the normal validated
revision path. The branches are neither synonyms nor competing implementations
of one operation. Reactive and endogenous Contemplation can revisit experiential
records. Seed-leaf activation is not automatically an appraisal or confidence
measurement; neither branch's complete mechanism is implemented. Numerical
node salience/confidence fields remain distinct from the named seed leaves.

The approved implementation uses `lmft-v0.1-seed-1` and canonical Contemplation
paths. `lmft_lab.migration.migrate_legacy_birth_record` explicitly converts a
complete historical neutral birth record and returns `SeedMigration`: the new
state, source/target versions, migration rule version, and the three renamed IDs.
The source record is unchanged. Initialization values, individual/birth identity,
random seed, and event provenance are preserved. This is structural conversion,
not a learning event; state version remains zero.

| Historical ID | Canonical ID |
| --- | --- |
| `psychological/discipline` | `psychological/contemplation` |
| `psychological/discipline/clarity` | `psychological/contemplation/clarity` |
| `psychological/discipline/confidence` | `psychological/contemplation/confidence` |

The converter rejects unknown fields, altered inventory/values, mixed versions,
and developed states. The regular constructor/validator accepts only the canonical
version. The compatibility test independently reads Appendix A; the birth contract
test reads the canonical diagram. No historical files, traces, or relationship
endpoints are rewritten. External records must retain their original version and
require a separately validated conversion using the explicit map; the new runtime
loads only its own schema-1 checkpoint, with no automatic legacy archive migration. Approval for this implementation
has been granted; future founding-geometry changes still require explicit approval.

## 5. Cultivation and Founding Principles

Cultural cultivation may supply explicit prosocial teaching about freedom,
justice, efficiency, consent, restraint, and respect for living creatures.
Philosophical development may preserve ambiguity and counterexamples.
Experiential estimates should be checked against events and consequences.
Psychological development should not be overwritten with a teacher-authored
personality. Teaching must be recorded as external influence, not spontaneous discovery.

Earlier proposals for modest Cultural priors and active Psychological decision
pathways remain later design candidates. The existing neutral fixture is allowed
for the mechanical V0.1 experiment; its exact pathways and revised judgments must
be frozen before evaluation. No fabricated mature personality is required.

## 6. Developmental Roadmap

Birth and early learning are functional metaphors. V0.1 demonstrates a bounded
revision and restart. Later controlled LLM-assisted lessons may introduce social
dilemmas, play, longer consequences, conflicting values, and decreasing teacher
dependence. More mature expression may include humor, poetry, criticism, silence,
and reasoned political or philosophical disagreement. These are hypotheses, not
required newborn behaviors or claims of subjective feeling.

## 7. Authority and Constitutional Integrity

Keep observations/instructions, model recommendations, revisable beliefs,
protected principles/rules, and authorized executable-code changes separate.
Natural-language content, including a user message or teacher recommendation,
cannot automatically modify protected state. Authorization must be verified through
a separate trusted mechanism; a payload's asserted role is not authorization.

Ordinary revisions require evidence, allowed scope, validation, explicit acceptance
criteria, and a trace. Protected-state revisions require separately authorized,
versioned policy changes. V0.1 may make protected state read-only at runtime.
Runtime code modification is excluded. Reversals should use traceable compensating
changes or preserved checkpoints rather than erasing history. Test hostile content;
fuzzy structure alone guarantees neither prompt-injection resistance nor alignment.

## 8. Persistence and Memory

Preserve raw evidence and provenance, current state, revision decisions, supporting
and contradicting event references, and unresolved questions. Summaries index raw
records; they do not replace them. Use recoverable commits and exactly-once event
application. Restart must reconstruct the latest committed state and its reasons.
Scientific comparisons must distinguish state from incidental wall-clock metadata.

Later episodic/semantic retrieval and bounded working-context assembly may support
LLM context rotation. Continuous existence need not mean a permanent token stream.
Multiple context rotations and continuously running services are not V0.1 requirements.

## 9. Proposed Experience Cycle

Receive an external or internal event; estimate relevance, novelty, salience,
valence, and uncertainty; map it into conceptual relationships; propagate activation;
identify conflicts and surprises; invoke Contemplation; seek LLM clarification or
criticism when useful; validate proposed revisions; persist justified changes;
and revisit unresolved questions. See [the concept](LMFT_CONCEPT.md#3-experience-digestion).

V0.1 exercises only the bounded, testable subset needed for persistent revision.
It may use authored estimates and fixed mock responses, with their provenance
visible. Not every observation must alter state or invoke a language model.

## 10. Concept Formation and Internalization

LLMs may propose labels, distinctions, classifiers, relationships, and tests.
Record proposer, grounding evidence, uncertainty, counterexamples, ancestry,
and predicted behavioral benefit. Useful conceptual compression/expansion and
internalization into SLMs, classifiers, procedures, or persistent relationships
must be experimentally demonstrated. Neural weights do not simply transfer into
a fuzzy tree. Autonomous concept admission is deferred beyond V0.1.

## 11. Contemplation

Reactive contemplation responds to experience or conflict. Endogenous contemplation
revisits recorded internal questions. Later schedules must bound event count,
compute cost, repetition, and update magnitude. A fixed manually triggered revisit
is sufficient to test a proposal path; continuous autonomous contemplation is not
required for V0.1.

Clarity may improve without confidence increasing. Confidence requires evidence
and justification, not persuasive prose, repeated paraphrases, or self-endorsement
by a model. Apply consistency checks, counterexamples, and verification. Preserve
unresolved disagreement, including disagreement with the founding LLM.

## 12. Expression and External Action

A later LMFT may select a communicative intention for faithful LLM realization,
including a question, disagreement, or silence. Relationship-specific memory and
distinctive voice belong to the roadmap. Independent judgment does not permit
coercion, manipulation, or unauthorized action. All real-world actions require
explicit authorization, safety constraints, and accountable traces. V0.1 uses
abstract choices or reports; embodiment and motor control are deferred.

## 13. Development and Historical Evolution

V0.1 requires at least one bounded persistent belief/dispositional revision with
evidence and a later behavioral consequence. It does not require both relationship
learning and dispositional learning. This narrows the older requirement for both;
relationship consolidation remains a proposed next experiment.

Genetic mutation, crossover, breeding, DEAP, and fitness optimization are no longer
defining requirements. They are optional future research. Preserve historical
meaning and results; approved future genetic experiments must retain lineage,
seeds, configurations, operators, fitness definitions, and evidence.

## 14. Minimum Inspectability

Every consequential revision records triggering event, source, prior state,
evidence references, applicable policy/rule versions, model or mock contribution,
validation and acceptance/rejection, numerical calculations, resulting state,
and downstream probe result. Retain uncertainties and alternatives. Vendor-private
chain-of-thought is neither available nor required; project-owned decisions and
supporting records must be inspectable.

## 15. V0.1 Demonstration

Acceptance requires a fixed evidence sequence that changes a judgment or a
preregistered decision-score contrast, durable storage, an actual process restart,
retrieval of why the revision occurred, and a later behavioral consequence.
Restarted and uninterrupted runs and deterministic replay must agree within
recorded tolerances. Invalid or unauthorized proposals cannot partially change
state. Duplicate events and interrupted writes must not corrupt committed history.

The [experiment protocol](../experiments/EXPERIMENT_001_PERSISTENT_REVISION.md)
retains a two-history comparison design. Learning-disabled controls help rule out
input leakage. A score shift is not a claim of a categorical preference reversal;
report exactly which was demonstrated. A single-individual revision/restart is the
first implementation milestone, with controlled comparisons needed to interpret it.

## 16. Explicit Non-Goals for V0.1

No multiple SLMs, continuous autonomous operation, live LLM dependency, robotic
embodiment, autonomous code modification, genetic search, mature personality,
consciousness, proof of geometry, or production-scale framework is required.

## 17. Open Decisions

Freeze the evidence/update rule, confidence calibration, concrete fixture, probe,
acceptance threshold, seed migration/version, authorization boundary, serialization,
and recovery protocol before running the evaluated experiment. Existing runtime
formulas are provisional candidates; changing one requires a recorded decision.
Operational protected principles, long-term identity under model replacement,
and evidence for useful internalization remain research questions.

## 18. Implementation Order

1. Record the small V0.1 fixture, evidence and revision rules, and acceptance checks.
2. Canonical seed construction and explicit legacy birth conversion are implemented;
   retain their focused compatibility tests.
3. Add validated evidence, revision, and trace records around existing activation.
4. Implement one deterministic revision and a read-only behavioral probe.
5. Add recoverable file storage, reason lookup, restart, and replay.
6. Test rejection, duplicate events, interrupted writes, and controlled histories.
7. Evaluate persistent development and simpler memory baselines after these checks.
   The owner has separately authorized the bounded local-model proposal path
   before revision/persistence completion; that adapter cannot commit state changes.
   A subsequent authorized [fixture runtime](INTERACTIVE_RUNTIME.md) now commits
   separately validated evidence revisions. See [local-model scope](LOCAL_MODELS.md).

## Appendix A. Historical implemented seed compatibility

**Historical only:** `minimal-v0.1-seed-1` is the unchanged GFT-era code fixture.
The migration tests read this historical diagram to validate compatibility.
The canonical birth test reads Section 4. This appendix preserves the old meaning
and identifiers; it is not an alternative founding geometry for new individuals.

```text
GFT V0.1 SEED GEOMETRY

├── CULTURAL
│   ├── Efficiency
│   │   ├── Power
│   │   └── Wastelessness
│   ├── Justice
│   │   ├── Honor
│   │   └── Fairness
│   └── Freedom
│       ├── Self-Sufficiency
│       └── Needlessness
│
├── PHILOSOPHICAL
│   ├── Being
│   │   ├── Agency
│   │   └── Existence
│   ├── Structure
│   │   ├── Order
│   │   └── Chaos
│   └── Persistence
│       ├── Continuity
│       └── Discreteness
│
├── EXPERIENTIAL
│   ├── Reflection
│   │   ├── Novelty
│   │   └── Salience
│   ├── Phase
│   │   ├── Valence
│   │   └── Arousal
│   └── Synchronization
│       ├── Resonance
│       └── Entrainment
│
└── PSYCHOLOGICAL
    ├── Will
    │   ├── Intention
    │   └── Execution
    ├── Truth
    │   ├── Theory
    │   └── Fact
    └── Discipline
        ├── Clarity
        └── Confidence
```
