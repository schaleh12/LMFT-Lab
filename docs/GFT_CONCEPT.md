# LMFT Concept — Research Hypothesis

**Status:** Proposed research direction, not demonstrated cognition. This document
supersedes the evolution-centered GFT hypothesis. Existing filenames and the
`gft_lab` package remain unchanged for compatibility. See the
[documentation index](INDEX.md) for specification authority and migration notes.

## 1. Central hypothesis

A Language Model Fuzzy Tree (LMFT) is a proposed persistent, structured, fuzzy
cognitive architecture that may develop conceptual understanding, dispositions,
judgments, and independent reasoning through repeated interaction with language
models. The newborn is intentionally immature and initially depends heavily on
a capable founding LLM. Its persistent structures should increasingly influence
what it notices, asks, believes, and does in subsequent controlled situations.

The research question is whether this organization adds measurable value beyond
an LLM with ordinary structured memory. Fluent language, stored preferences, or
numerical propagation alone do not demonstrate understanding. The long-term
vision is a continuously contemplating agent with a distinctive developing
identity, reasoning about experiences, relationships, values, and eventually
authorized real-world goals. None of those mature capacities is established.

## 2. Founding constitution and conceptual geometry

The [seed](MINIMAL_GFT_SPEC.md#4-hardcoded-v01-seed-geometry) is a foundational
scaffold analogous to a philosophical or religious constitution: a small set of
principles through which experience is interpreted and integrated. This analogy
requires neither supernatural belief nor worship nor assumptions of consciousness.

Founding principles and revision rules are protected, versioned configuration.
Interpretations, applications, beliefs, and learned relationships are revisable.
A disagreement with an interpretation is not permission to rewrite a principle.
The exact operational content of the principles must be recorded; English node
labels alone do not constitute an executable constitution.

Cultural, Philosophical, Experiential, and Psychological branches are retained.
Psychological → Contemplation replaces Discipline and retains Clarity and
Confidence. Experiential remains because it is part of the established seed;
the older Scientific alternative is historical geometry research.

The geometry may support conceptual compression into persistent relationships
and expansion into contextual distinctions. Whether it does so usefully must be
tested. Factorial organization, prime components, and unlabeled concepts remain
hypotheses in [Conceptual Geometry](CONCEPTUAL_GEOMETRY.md), not prerequisites
for the first persistence experiment.

## 3. Experience digestion

The proposed cycle is:

1. Receive an observation, linguistic interaction, or internal cognitive event.
2. Estimate relevance, novelty, salience, valence, and uncertainty, labeling the
   source and limitations of each estimate.
3. Map relevant information into seed-derived conceptual relationships.
4. Propagate activation through explicitly represented associations.
5. Identify conflicts, unresolved questions, or surprising relationships.
6. Invoke Contemplation when further interpretation is warranted.
7. Consult an LLM for clarification, criticism, alternatives, or proposed revisions.
8. Evaluate recommendations against evidence, protected constraints, and revision policies.
9. Persist accepted changes with supporting evidence and decision traces.
10. Revisit unresolved questions through later contemplation.

Language models, specialized small language models (SLMs), classifiers, and
deterministic procedures may eventually share these tasks. Their estimates are
not automatically facts. V0.1 uses authored inputs and deterministic or mocked
responses; the entire cycle is not yet implemented or validated.

## 4. LLM partnership and internalization

The runtime LLM is a possible clarifier, teacher, critic, and developmental
partner, not merely an output renderer. It may interpret activation traces,
explain conflicts, suggest distinctions, propose classifiers and relationships,
and help test its own recommendations. Self-criticism by the same model is not
independent corroboration. Persistent LMFT evaluation and accepted changes must
remain distinguishable from the model's transient inference.

Codex initially serves as the external development assistant: implementing,
inspecting, debugging, and refining the research software under the owner's
instructions. That role is distinct from a future runtime LLM. Development
assistance does not mean Codex is already integrated into the cognitive loop.

Internalization means demonstrating that some previously assisted function can
be performed reliably by persistent conceptual structure, a classifier, a
specialized SLM, or a deterministic procedure. It is not automatic, and neural
weights cannot simply be transferred into a fuzzy tree. Compare assisted and
unassisted performance, generalization, errors, and resource costs before claiming
internalization. Model training or additional dependencies need separate design.

## 5. Contemplation, Clarity, and Confidence

Reactive contemplation follows an experience or conflict. Endogenous
contemplation revisits an internally recorded unresolved question without a new
external request. Both should use explicit triggers, bounded work budgets,
traceable proposals, and stopping conditions. Unresolved disagreement is an
acceptable result; agreement with the founding LLM is not a stopping requirement.

Clarity is the intelligibility and coherence of the current interpretation.
Confidence is the strength of its evidence and justification. A coherent story
may be weakly supported; strong evidence may still be poorly understood. Neither
the seed leaf activation nor eloquent prose automatically measures either quality.

Evaluate revisions using evidence provenance, consistency checks, counterexamples,
failed predictions, and appropriate verification. Repeated paraphrases of one
argument do not become independent evidence. Important revisions require explicit
acceptance criteria, before/after state, and reversibility where feasible.

## 6. Constitutional integrity

Investigate whether a persistent constitution improves resistance to unauthorized
goal, identity, or principle changes. Distinguish:

- untrusted observations, instructions, retrieved content, and user messages;
- LLM interpretations and recommendations;
- ordinary revisable beliefs and relationships;
- protected founding principles and revision rules;
- separately authorized changes to executable code.

Content cannot grant itself authority. Authorization must come through a trusted
control path, with validated scope and recorded provenance. A runtime proposal
cannot rewrite its own acceptance rules. Explore validation, versioned permissions,
rollback, and adversarial prompt-injection tests; a fuzzy tree inherently guarantees
neither injection resistance nor alignment. LMFT disagreement with its teacher
should be possible when justified by evidence or protected constraints.

## 7. Identity, relationships, and agency

Identity is provisionally continuity of versioned state, history, commitments,
and configuration, not an uninterrupted token stream. Long-term work may examine
recognizable dispositions, relationship-specific memories, and distinctive humor,
criticism, or poetic expression. The ambition extends beyond obedient question
answering: the system may ask questions, challenge assumptions, and develop
reasoned political or philosophical positions.

Independent judgment does not authorize coercion, manipulation, or external
action. Future action remains subject to explicit authorization, safety constraints,
and accountability. Descriptions of affect, an inner life, or maturity are
functional research analogies, not claims of subjective consciousness. Advanced
social behavior and continuous autonomy are roadmap topics, not V0.1 acceptance tests.

## 8. First experiment and falsification

**Make the newborn LMFT change its mind in a traceable way, save its state to
disk, restart, and demonstrate that it remembers why.**

The [minimal specification](MINIMAL_GFT_SPEC.md) and
[Experiment 001](../experiments/EXPERIMENT_001_PERSISTENT_REVISION.md) define the
small mechanical target. Show persistent revision, supporting and contradicting
evidence, reproducibility, and a later behavioral consequence. Passing establishes
mechanics, not the full cognitive hypothesis.

Later comparisons should include an LLM with ordinary structured memory under
matched model, evidence, prompts, and compute budgets; direct activation without
propagation; and learning-disabled controls. Preregister behavioral accuracy,
revision quality, evidence retrieval, calibration, and costs as appropriate.
If fuzzy propagation provides no measurable advantage, report that result and
reconsider its role rather than redefining success after seeing outcomes.

## 9. Historical direction and open questions

GFT originally meant Genetic Fuzzy Tree and emphasized inspectable mutation,
crossover, population breeding, co-evolution, and fitness optimization. That
central requirement is superseded. Such search is optional future research,
not the immediate implementation plan. Preserve past research and any results;
if genetic experiments are later approved, retain seeds, fitness definitions,
ancestry, lineage, and evaluation records.

Shared conceptual environments, multiple interacting individuals, and controlled
self-experimentation remain optional research questions. Controlled copies in
current experiments are comparison runs, not bred descendants.

Open issues include operational constitutional principles and authorization,
evidence independence and calibration, reliable grounding, useful propagation
semantics, bounded endogenous scheduling, model replacement and identity,
criteria for internalization, and meaningful measures of conceptual development.
No specific runtime LLM, SLM training method, vector database, or agent framework
is selected by this document.
