# GFT-Lab Development Rules

These rules apply throughout this repository.

## Research purpose

- This project investigates Genetic Fuzzy Tree (GFT) architectures for inspectable, evolvable artificial intelligence.
- The primary research goal is to build GFT reasoning systems whose internal decision structures can be inspected, traced, mutated, crossed over, and evolved.
- GFT reasoning must remain conceptually separate from LLM reasoning. An LLM may later be used as a language/translation interface, but it must not silently replace the GFT's decision-making.
- Prefer transparent, inspectable algorithms and data structures over opaque substitutes.
- Treat documents describing GFT theory and experimental hypotheses as research specifications, not as invitations to rewrite the theory.

## Scientific validity and reproducibility

- Evolutionary experiments must be reproducible. Preserve random seeds, configuration, fitness definitions, and relevant results.
- Fitness functions are part of the research design and must not be casually changed merely to make tests or experiments succeed.
- Preserve ancestry/lineage information when evolutionary functionality is introduced.
- Never modify or delete historical experimental results merely to obtain cleaner results.

## Development practices

- Write automated tests for important behavior.
- Prefer small, understandable modules over premature complexity.
- Do not add large frameworks, cloud services, databases, agent frameworks, neural networks, or other major dependencies unless they are specifically justified and approved.
- Do not implement speculative features merely because they appear in design documents.
- Do not make large architectural changes without explaining the proposed change first.

## Language and environment

- Python is the primary implementation language.
- The current local environment uses Python 3.12.
- Expected scientific/evolutionary dependencies include NumPy, SciPy, DEAP, scikit-fuzzy, NetworkX, and pytest. This list does not require installing or using all of them immediately.

## Current stage

This is an early-stage experimental repository. Simplicity, inspectability, reproducibility, and scientific validity take priority over production-scale engineering.
