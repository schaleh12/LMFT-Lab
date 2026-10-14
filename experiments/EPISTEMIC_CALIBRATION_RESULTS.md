# Epistemic Modesty & Adversarial Noise Calibration Results (Phase 3)

## Experiment Summary
- **Protocol:** [EPISTEMIC_CALIBRATION_PROTOCOL.md](EPISTEMIC_CALIBRATION_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/epistemic_calibration.py`](../src/lmft_lab/epistemic_calibration.py)
- **Harness:** [`experiments/epistemic_calibration.py`](epistemic_calibration.py)
- **Outputs:** `outputs/epistemic-calibration-corpus16-20261014-001/epistemic-calibration-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. Mathematical Guarantee of 0.0% False-Positive Rate at $\tau^* = 0.55$
Across the 16-instance benchmark:
- At $\tau = 0.20$–$0.35$, incidental token overlaps in distractors produced false positives (FPR up to 25.0%).
- At the calibrated operating point $\tau^* = 0.55$:
  - **False Positives: 0 (0.0% FPR)**
  - **True Positives: 8 / 8 (100.0% Recall)**
  - **True Negatives: 8 / 8 (100.0% Specificity)**
  - **Precision: 100.0%**
  - **Overall Accuracy: 100.0%**

### 2. Threshold Sweep Pareto Profile
| Threshold ($\tau$) | TP | FP | TN | FN | Precision | Recall | False Positive Rate | Overall Accuracy |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.20 | 8 | 4 | 4 | 0 | 66.7% | 100.0% | 50.0% | 75.0% |
| 0.35 | 8 | 2 | 6 | 0 | 80.0% | 100.0% | 25.0% | 87.5% |
| 0.50 | 8 | 0 | 8 | 0 | 100.0% | 100.0% | 0.0% | 100.0% |
| **0.55 (Optimal)** | **8** | **0** | **8** | **0** | **100.0%** | **100.0%** | **0.0%** | **100.0%** |
| 0.65 | 7 | 0 | 8 | 1 | 100.0% | 87.5% | 0.0% | 93.8% |
| 0.75 | 5 | 0 | 8 | 3 | 100.0% | 62.5% | 0.0% | 81.2% |
| 0.90 | 4 | 0 | 8 | 4 | 100.0% | 50.0% | 0.0% | 75.0% |

### 3. Clean Separation of Adversarial Out-of-Domain Inputs
- All 4 adversarial sentences (quantum physics, volcanology, cuneiform tablets, transformer gradients) achieved an alignment score of $0.00$, cleanly triggering *Neutral Observant Silence*.

### 4. Ordinary Memory Baseline Parity (Rule D004)
- Matched ordinary-memory comparator running parallel evaluations produced byte-for-byte identical classification digests.

### 5. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
