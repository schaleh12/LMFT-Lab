# Persistent Contextual Disambiguation Protocol — Phase C Behavioral Consequence

2026-10-13. Formal preregistered protocol for evaluating the unassisted, persistent
behavioral consequences of remembered Protocol 4 representations on contextual word-sense
disambiguation across the 33 SemCor development instances.

## 1. Research Purpose & Invariants

In accordance with [AGENTS.md](../AGENTS.md), the core hypothesis under study is whether
Language Model Fuzzy Tree (LMFT) architectures can exhibit:
> *"traceable state revision, disk persistence, restart, remembered evidence, and a **behavioral consequence**."*

Protocol 4 established that the local SLM can emit 100% admissible, non-tautological semantic
substitutions with contiguous context anchors into the neutral store.

This protocol investigates the **behavioral consequence**:
1. Ingests admitted representation records from disk into persistent capacity state.
2. Compiles persistent, inspectable disambiguation rules linking context anchors to semantic interpretations.
3. Evaluates target words in context **unassisted** (zero runtime LLM calls during inference).
4. Demonstrates whether persistent syntactic anchors solve the catastrophic false-positive failure
   of the Phase B bag-of-words rule system (where `a` + `by` suffered 100% false positives).
5. Enforces strict matched ordinary-memory comparison ([Rule D004](../AGENTS.md)) under independent process restart.

## 2. Frozen Evaluation Inputs

1. **Admitted Neutral Checkpoint**:
   Protocol 4 external archive:
   `C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v4-20261013-002\neutral-state\checkpoint.json`
   SHA256: `4adbea15bb3461ba749d10f0123c71c72876607a9923ffe162c9bd824d07e01b`.
   Contains 4 admitted non-tautological proposals: `representation-01` through `04`.

2. **Approved Development Dataset**:
   `development.json` (SHA256: `77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`).
   Contains 33 development instances across 8 WordNet 3.0 sense categories for lemma `order`.

3. **Frozen Founding Seed Geometry (Rule D001)**:
   The canonical 40 nodes and parent-child tree remain completely untouched. All learned rules
   reside in persistent capacity memory outside the seed.

## 3. Evaluation Interface & Decision Rules

### Input Schema (No Gold Exposed)
Each evaluation item contains:
- `id`: string example identifier.
- `tokens`: list of surface token strings.
- `target_indices`: list of integer indices defining the target word.
Neither gold sense keys, document IDs, nor training provenance are provided to the predictor.

### Decision Rules
For each evaluation sentence:
- **`single`**: Exactly one persistent interpretation matches. The engine outputs the selected
  sense key, the remembered explanatory gloss, and traceable witness references.
- **`abstain`**: Zero persistent interpretations match. The engine honestly abstains without guessing.
- **`ambiguous`**: Multiple competing interpretations match with distinct sense keys. The engine
  flags ambiguity and reports the competing witness sets.

### Matching Strategies
1. **Exact Anchor Match**: The exact contiguous context quote from the proposal appears in the sentence.
2. **Core Collocational Anchor Match**: The core syntactic pattern (e.g., `on the order of`, `order of the court`,
   `order he expected`, `order of the making`) matches within distance $k=3$ of the target token.

## 4. Evaluation Metrics & Baseline Comparison

- **Strict Accuracy**: Correct singletons / total evaluation instances (33).
- **Precision on Fired Cases**: $TP / (TP + FP)$ on non-abstained cases.
- **False Positive Rate**: $FP / \text{non-gold instances}$.
- **Abstention Rate**: Abstentions / total instances.
- **Comparison against Phase B**: Compare FP rate directly against Phase B's bag-of-words co-occurrence
  learner (which had 4 false positives, 0 true positives on evaluated rules).
- **Matched Memory Baseline (Rule D004)**: Compare primary LMFT capacity predictor against an ordinary
  structured-memory comparator under identical deterministic inputs and rules. Verify byte-for-byte prediction parity.

## 5. Execution Safeguards

- Zero runtime model calls; deterministic Python inference only.
- Neutral checkpoint nonmutation verified under process restart.
- Complete automated pytest coverage in `tests/test_persistent_disambiguation.py`.
- Results published in `experiments/PERSISTENT_DISAMBIGUATION_RESULTS.md`.
