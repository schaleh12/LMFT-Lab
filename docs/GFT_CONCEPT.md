# GFT Concept — Research Specification Scaffold

This document organizes the conceptual definition of GFT before implementation.
It is not a complete architecture or authorization to implement the topics below.

**Status labels:** Established decisions are supported by [AGENTS.md](../AGENTS.md),
[README.md](../README.md), or the explicit scope of this scaffold. Tentative
interpretations are vocabulary aids, not accepted theory or tested hypotheses.
Open questions and decisions not yet made remain unresolved. The
[documentation index](INDEX.md) describes how research documents are treated.

## 1. Research Vision

**Purpose:** State what the project investigates and the qualities it seeks.

**Established:** GFT-Lab investigates Genetic Fuzzy Tree architectures for
inspectable, evolvable artificial intelligence. The research goal is reasoning
whose internal decision structures can be inspected, traced, mutated, crossed
over, and evolved. Transparency, simplicity, reproducibility, and scientific
validity take priority over production-scale engineering.

**Open:** What evidence will demonstrate useful reasoning and inspectability?
These goals are not claims of demonstrated capabilities.

## 2. GFT Individual

**Purpose:** Clarify what counts as one GFT reasoning system and one individual
in evolutionary research.

**Established:** GFT decision structures are intended to be inspectable and
evolvable; their concrete representation has not been selected.

**Open:** What defines an individual's identity, boundaries, and continuity?
What belongs to the individual, and what belongs to its environment? No specific
tree or node representation is defined here.

## 3. Concept

**Purpose:** Reserve a definition for what a GFT can treat as a concept.

**Experimental hypothesis:** [Conceptual Geometry](CONCEPTUAL_GEOMETRY.md) records
the current detailed experimental hypothesis for conceptual representation. It
is not an established architecture or a selected computational representation.

**Open:** A concept's identity, meaning, and relationship to fuzzy reasoning
remain unsettled. How are concepts distinguished and related? The linked
hypothesis's theoretical and implementation questions remain open.

## 4. Conceptual Workspace

**Purpose:** Clarify the intended meaning and scope of a conceptual workspace.

**Tentative interpretation:** A workspace may describe the context in which
concepts are available for consideration. This is informal vocabulary, not a
decision about memory, data structures, or execution.

**Open:** What is available in that context, how does it change, and is it
individual, shared, or both? Its relationship to internal state remains undefined.

## 5. Orientation

**Purpose:** Reserve space to define what orientation means in GFT research.

**Open:** The current documentation supplies no definition. What would an
orientation describe, and how would it differ from state, goals, or behavior?
No personality categories, including Good/Evil personalities, are defined.

## 6. Internal State

**Purpose:** Clarify what, if anything, persists or changes within an individual
during reasoning.

**Established constraint:** Any eventual account must respect the project's
commitment to transparent, inspectable algorithms and data structures.

**Open:** What constitutes state, how does it change, and what is its relationship
to decision structure, workspace, and inheritance? No state variables or update
rules have been chosen.

## 7. Contemplation

**Purpose:** Reserve a conceptual account of what the term contemplation is
intended to describe.

**Tentative interpretation:** It may refer informally to internal consideration
of concepts. This does not specify a reasoning procedure or imply subjective
experience.

**Open:** Does the term describe something distinct from reasoning generally?
What initiates it, what can change through it, and how could it be inspected?
No iterative process, scheduling rule, or stopping criterion is established.

## 8. External Events / Perception

**Purpose:** Clarify how events outside an individual relate conceptually to
what that individual can consider.

**Open:** What counts as an external event or perception? How does an event
relate to a concept or to internal state? Existing documents do not select input
types, interpretation rules, or a perception mechanism.

## 9. Shared Conceptual Environment

**Purpose:** Clarify what a conceptual environment shared by GFTs would mean.

**Established research direction:** Multiple GFT individuals may coexist relative
to a shared conceptual environment. The environment can provide common conceptual
referents while each GFT retains its own individual internal state, orientation,
interpretation, or other individual properties that may later be defined. This
states a research direction, not an implementation decision or a definition of
those individual properties.

**Established scope for this scaffold:** “Shared consciousness” is an informal
research description of a shared conceptual workspace unless later specified
otherwise. It does not assert literal phenomenal consciousness.

**Open:** What constitutes a common conceptual referent, and where are the
boundaries between shared referents and individual properties? How would different
interpretations coexist? The relationship between this environment and an
individual's workspace is unresolved. No representation or sharing mechanism is
selected.

## 10. Multiple GFTs / Coexistence

**Purpose:** Identify the questions raised by studying more than one GFT.

**Established research goal:** The README includes developing co-evolving GFT
architectures. This is a research direction, not a decided interaction model.

**Open:** What does coexistence mean, how might individuals affect one another,
and what would co-evolution involve? Communication, cooperation, competition,
and shared access are not established requirements or mechanisms.

## 11. Evolution

**Purpose:** State the research commitments governing evolutionary change.

**Established:** Decision structures should be amenable to mutation, crossover,
and evolution. Evolutionary functionality must preserve ancestry and lineage.
Experiments must preserve seeds, configurations, fitness definitions, and relevant
results. Fitness definitions are part of research design and must not be changed
merely to obtain success. Historical results must not be modified or deleted to
produce cleaner outcomes.

**Open:** What is inherited, what can vary, and what constitutes a valid change?
Selection procedures, operators, and fitness functions remain undefined here.

## 12. Language / LLM Boundary

**Purpose:** Preserve the distinction between GFT reasoning and a possible
language interface.

**Established:** An LLM may later serve as a language or translation interface;
it is not the GFT reasoning engine and must not silently replace GFT
decision-making. No LLM integration is selected or introduced by this document.

**Research principle:** An LLM should not assign meaning to arbitrary internal
GFT structures merely by producing a plausible interpretation. Semantic
interpretation should ultimately be grounded in observable relationships, traces,
events, state changes, or behavior and remain testable and revisable. The grounding
and validation procedures remain unresolved; see
[Conceptual Geometry](CONCEPTUAL_GEOMETRY.md#13-meaning-through-grounding).

**Open:** How could translation preserve meaning and make the boundary between
translation and decision-making inspectable? Interface contracts and evaluation
procedures have not been decided.

## 13. Open Research Questions

**Purpose:** Keep gaps visible rather than treating vocabulary as settled theory.

**Unresolved:** What operational meanings should be assigned to individual,
concept, workspace, orientation, state, contemplation, and perception? How do
these notions relate without presupposing an architecture? What observations
could support or challenge future hypotheses about reasoning, sharing, and
co-evolution? How should inspectability be assessed?

No answers or experimentally supported hypotheses for these questions are
established by the current project documents. Tentative interpretations above
must not be treated as findings.

## 14. Decisions Not Yet Made

**Purpose:** Identify decisions that require further research specification
before implementation.

**Undecided:** Concrete tree/node representation; concept representation;
reasoning and fuzzy semantics; workspace boundaries; state and change rules;
the meaning of orientation and contemplation; perception; shared-environment
semantics; interaction among individuals; inheritance and evolutionary operators;
fitness definitions; and any future language-interface contract.

These gaps are intentional. This scaffold introduces no neural networks,
embeddings, vector databases, agent frameworks, or LLM-based reasoning. Naming
a topic here does not approve a feature or resolve a research question.
