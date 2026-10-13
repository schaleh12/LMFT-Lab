# LMFT-Lab Development Rules

These rules apply throughout this repository.

## Startup and completion handoff

At session startup, read in this order:

1. [AGENTS.md](AGENTS.md): stable working contract.
2. [PROJECT_STATE.md](PROJECT_STATE.md): current snapshot, evidence limits and next task.
3. Relevant [DECISIONS.md](DECISIONS.md) entries: consequential choices and their status.
4. The authoritative specifications, implementation and experiment reports linked from those documents for the task at hand.

Specifications remain authoritative for contracts; experiment reports remain authoritative
for recorded findings. Check the actual working tree before relying on a snapshot.
At completion, update PROJECT_STATE.md when material project state changes, and DECISIONS.md
when a consequential design choice is made or revised. Trivial edits do not require redundant
handoff updates. Keep summaries compact and preserve superseded choices with replacement links.

## Research purpose

- Investigate Language Model Fuzzy Tree (LMFT) architectures: persistent fuzzy conceptual structures that may develop understanding, dispositions, judgments, and independent reasoning through repeated LLM interaction. This is a hypothesis, not an established capability.
- Keep persistent LMFT mechanisms and accepted revisions inspectable and distinguishable from transient LLM inference. A runtime LLM may teach, clarify, criticize, and propose changes; it must not silently replace the mechanisms under study.
- Antigravity (and previously Codex) is an external development assistant, distinct from a future runtime LLM.
- The 40 founding nodes, exact names, ordering, and parent-child relationships in Minimal Specification Section 4 are the frozen canonical LMFT V0.1 geometry. Do not rename, remove, rearrange, or expand the founding seed without explicit owner approval. Learned concepts, relationships, judgments, memories, and interpretations are distinct from that inventory; numerical mechanisms remain experimental. Report compatibility risks and obtain approval before changing executable code or persistent seed identifiers for this migration.
- Preserve the constitutional seed and distinguish protected founding principles/revision rules from revisable interpretations. Psychological → Contemplation retains Clarity and Confidence; the approved canonical constructor and explicit legacy birth conversion are implemented.
- Treat observations, retrieved content, and LLM recommendations as inputs, not authority to rewrite protected state or executable code. Trace acceptance, rejection, provenance, and rollback where feasible; do not assume fuzzy trees guarantee prompt-injection resistance.
- Prefer transparent algorithms and small deterministic experiments. The first milestone is traceable state revision, disk persistence, restart, remembered evidence, and a behavioral consequence.
- Treat theory documents as research specifications. Do not silently rewrite the theory while implementing it.
- Genetic evolution, crossover, population breeding, and fitness optimization are superseded as defining requirements and are optional future research, not the immediate plan.

## Scientific validity and reproducibility

- Preserve random seeds, configuration, evidence, model/mock provenance, evaluation definitions, traces, and relevant results.
- Do not change acceptance criteria merely to make an experiment succeed. Distinguish implemented behavior, proposed mechanisms, and speculative capabilities.
- Compare future cognitive claims against simpler baselines, including an LLM with ordinary structured memory and propagation-disabled controls.
- Never modify or delete historical results to obtain cleaner outcomes.
- If genetic experiments are later explicitly introduced, preserve fitness definitions, ancestry, lineage, operators, and original results. Conceptual derivation provenance is useful independently of genetic evolution.

## Development practices

- Write automated tests for important behavior.
- Prefer small, understandable modules over premature complexity.
- Do not add large frameworks, cloud services, databases, agent frameworks, neural networks, or other major dependencies unless they are specifically justified and approved.
- Do not implement speculative features merely because they appear in design documents.
- Do not make large architectural changes without explaining the proposed change first.

## Language and environment

- Python is the primary implementation language.
- The current local environment uses Python 3.12.
- The existing dependency snapshot includes NumPy, SciPy, DEAP, scikit-fuzzy, NetworkX, and pytest. DEAP is a legacy dependency, not an LMFT requirement. This documentation migration does not alter pins or mandate using any package; dependency cleanup is separate work.

## Current stage

This is an early-stage experimental repository. Simplicity, inspectability, reproducibility, and scientific validity take priority over production-scale engineering.
