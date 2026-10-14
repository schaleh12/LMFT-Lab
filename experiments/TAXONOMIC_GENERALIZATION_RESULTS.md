# Taxonomic Hypernym Generalization Results (Phase 4)

## Experiment Summary
- **Protocol:** [TAXONOMIC_GENERALIZATION_PROTOCOL.md](TAXONOMIC_GENERALIZATION_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/taxonomic_generalization.py`](../src/lmft_lab/taxonomic_generalization.py)
- **Harness:** [`experiments/taxonomic_generalization.py`](taxonomic_generalization.py)
- **Outputs:** `outputs/taxonomic-generalization-corpus12-20261014-001/taxonomic-generalization-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. 100% Hypernym Path Resolution Across 11 Fine-Grained Senses
- Successfully resolved complete hypernym ancestry paths up to root `entity` (path depths ranging from 5 to 7 steps) across all 11 registered senses for *bank* and *order*.
- Extracted 11 distinct primary taxonomic categories: `organization`, `geological_formation`, `facility_artifact`, `legal_instrument`, `commercial_document`, `sequence_structure`, `authoritative_act`, `sorting_act`, `quantitative_magnitude`, `social_condition`, and `systemic_arrangement`.

### 2. Principled Canonical Leaf Modulation (33 Activations)
- Applied 33 continuous dial modulations across the 24 canonical leaves in `birth.py` without mutating or expanding the founding scaffold (Rule D001).
- Every modulated activation satisfied the $[0.0, 1.0]$ dial bound condition.
- Cross-lemma conceptual convergence was demonstrated: senses from distinct lemmas sharing institutional or structural traits (e.g. `bank%1:14:00::` and `order%1:26:00::`) reinforced common canonical leaves (`philosophical/structure/order` and `cultural/justice/fairness`).

### 3. Calibrated Handling of Unregistered Controls
- The out-of-domain control instance (`unregistered%1:00:00::`) was cleanly detected (`found = False`), applied 0 affinities, and left all canonical leaf dials at baseline without error.

### 4. Matched Ordinary-Memory Baseline Parity (Rule D004)
- An ordinary structured-memory comparator performing parallel taxonomic traversal and dial modulation produced an exact byte-for-byte evaluation digest match across all 12 instances (`c30f37f8b47b4104da9495df089db56f28e1efe3ad6f19955bee9890fc468ccf`).

### 5. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
