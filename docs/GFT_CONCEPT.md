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

## 12. GFT / LLM Hybridization Boundary

**Purpose:** Define the research relationship between GFT cognition and the
capabilities supplied by a generative language model without prematurely
assigning all cognitive functions to either component.

**Established constraint:** GFT structures and their persistent changes must
remain inspectable enough to distinguish them from transient LLM inference. An
LLM must not silently replace the GFT mechanisms being studied, and LLM-generated
interpretations must not automatically become GFT ontology merely because the
language model proposed them.

**Research direction:** The intended research subject may be a coupled GFT–LLM
cognitive system rather than a GFT reasoning system with an LLM attached only as
an external translator.

Within such a hybrid, an LLM may contribute capabilities including language
comprehension and generation, learned world knowledge, contextual interpretation,
abstraction, analogy, synthesis, and general-purpose reasoning.

The GFT may contribute capabilities including persistent state and state
transitions, inspectable conceptual relationships, orientation, evolutionary
history, long-term disposition, salience, and other forms of persistent cognitive
structure developed through this research.

Neither component should currently be assumed to constitute the complete
cognitive system independently.

**Tentative hypothesis — persistent cognitive residue:** GFT state transitions
may provide a mechanism through which consequential aspects of previous
interactions with an LLM persist beyond an individual inference episode.

Rather than attempting to preserve a complete LLM reasoning process, the GFT may
preserve some structured consequence of that process: what became salient, which
relationships strengthened or weakened, what remained unresolved, how orientation
changed, or what future situations should provoke renewed consideration.

In this sense, persistent GFT state may function as a form of "instinctual
memory." This term is an informal research analogy and does not establish a
particular memory architecture.

**Tentative hypothesis — recurrent hybrid cognition:** Cognition may occur
through repeated interaction between the two substrates rather than through a
single one-way translation.

A possible conceptual cycle is:

```text
external situation
        |
        v
LLM interpretation / reasoning
        |
        v
GFT interaction and state transition
        |
        v
persistent changes in orientation / salience / relationships
        |
        v
subsequent LLM reasoning conditioned by those consequences
        |
        v
further GFT interaction
        |
       ...
```

Under this hypothesis, the output of the hybrid system may be substantially
generated through the LLM while the selection, persistence, recurrence,
orientation, or contextual significance of its reasoning may be substantially
influenced by the GFT.

The appropriate division of cognitive responsibility remains unresolved.

**Research principle — semantic grounding:** An LLM may propose interpretations
of internal GFT structures, but plausible linguistic interpretation alone does
not establish what those structures mean.

Semantic interpretations should, where possible, remain grounded in observable
relationships, traces, external events, state transitions, behavioral
consequences, developmental history, or other testable evidence.

Interpretations should remain revisable when subsequent observations fail to
support them. See
[Conceptual Geometry](CONCEPTUAL_GEOMETRY.md#13-meaning-through-grounding).

**Research principle — distinguish scaffolding from development:** The project
should attempt to distinguish among:

- transient reasoning performed by the LLM;
- semantic or perceptual structure supplied externally by the LLM;
- persistent structure represented by the GFT;
- changes to GFT structure produced through interaction with the LLM or
  environment;
- higher-order behavior that emerges specifically from recurrent interaction
  between the two systems.

This distinction is necessary because a sophisticated LLM could otherwise supply
an explicit ontology that merely appears to have been developed by the GFT.

Externally supplied conceptual scaffolding is not prohibited. Its influence
should instead be identifiable when the research question depends on whether
conceptual organization emerged within the GFT.

**Research principle — persistent cognitive sovereignty:** Persistent GFT
structure should retain meaningful independence from transient LLM inference.

An LLM may inform, challenge, contextualize, expand, or substantially influence
GFT state, but LLM output should not possess automatic authority over persistent
GFT orientation merely because it is linguistically persuasive, confident,
verbose, repetitive, instruction-conditioned, or prevalent in the model's
training-derived representations.

For purposes of this research, persistent GFT structures may provisionally be
described as an "instinctual" substrate: accumulated relationships, orientations,
salience, tensions, dispositions, and other persistent consequences of
development that survive individual LLM inference episodes. This is an informal
research analogy and does not imply biological instinct or subjective experience.

Persistent disagreement between the GFT and its associated LLM is a permissible
system state. The GFT should not be required to reach agreement with the LLM as
a termination condition for reflection.

Repeated or paraphrased instances of substantially equivalent LLM reasoning
should not automatically receive independent evidential weight. Once an argument
or relationship has been substantively represented, further linguistic
elaboration alone should not compel repeated reconsideration or persistent state
change.

This independence must not make persistent GFT structure immutable. New evidence,
experience, counterexamples, failed predictions, newly discovered relationships,
or other substantively relevant information must remain capable of challenging
and changing persistent GFT state.

A repeated failure of LLM inference to resolve a persistent conflict may instead
be represented as information about the behavior or limitations of that inference
process rather than as additional evidence for the repeated conclusion.

The mechanisms by which the system distinguishes substantive new information
from rhetorical or semantic repetition, models LLM reliability, terminates
unproductive inference loops, and revises persistent state remain open research
questions.

**Tentative research direction — coupled development:** The LLM may participate
in the GFT's conceptual development rather than remaining permanently isolated
from it.

The research does not currently require the GFT to independently rediscover
language, general world knowledge, or every abstraction already available to the
LLM. Hybridization may deliberately use those capabilities where doing so allows
the GFT research to focus on persistent, inspectable, evolvable, or otherwise
complementary cognitive mechanisms.

A particular GFT may therefore develop through repeated interaction with a
particular language model or model lineage. Whether the LLM should remain
interchangeable, whether replacing it changes the identity or behavior of the
hybrid, and whether long-term coupling produces model-specific development are
open research questions.

**Tentative research direction — reflective self-experimentation:** A mature
hybrid may eventually be capable of inspecting its own persistent structures and
proposing experiments concerning possible modifications.

Such proposals should not imply unrestricted self-modification. Experimental
variants may instead be created as descendants or controlled copies, with the
original structure, configuration, lineage, evaluation criteria, and historical
results preserved.

This would permit investigation of whether a hybrid system can reason about
improvements to its own persistent cognitive substrate while retaining
reproducibility and preventing successful outcomes from being manufactured by
silently changing the criteria used to evaluate them.

**Open:** Which cognitive functions should reside primarily in the LLM, primarily
in the GFT, or emerge through recurrent interaction between them? How much
perceptual or semantic seed structure should the LLM provide? How should GFT
state condition subsequent LLM inference? What information should flow in each
direction? At what point does LLM-supplied scaffolding become an externally
supplied ontology rather than GFT development? Can persistent GFT state
meaningfully alter future LLM reasoning without becoming merely a collection of
prompt parameters? How should contributions from each substrate be measured?
What constitutes continuity or identity when either component changes? Can
self-reflective experimentation improve the hybrid without compromising the
integrity of its evaluation? How should the hybrid distinguish genuinely new
evidence from repeated inference? How should persistent disagreement between the
GFT and LLM be represented and resolved without making persistent GFT structure
immutable or giving repeated LLM inference de facto control over it?

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

These gaps are intentional. The hybridization research direction selects no
particular LLM, prompt protocol, context mechanism, memory architecture, or
implementation of LLM-based reasoning. This scaffold adds no neural networks,
embeddings, vector databases, or agent frameworks. Naming a topic here does not
approve a feature or resolve a research question.
