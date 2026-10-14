# Comparative Baseline Benchmark Results

## 1. Executive Summary
Preregistered [Comparative Baseline Protocol](COMPARATIVE_BASELINE_PROTOCOL.md) completed across the complete 33-instance SemCor development corpus (`development.json`, *order* / *orders*). Evaluated unassisted LMFT capacity representation against two conventional baselines: Baseline A (Exact Key-Value Dictionary Lookup) and Baseline B (Naive Bag-of-Words Matcher).

Zero runtime LLM calls during inference. Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity) enforced throughout.

---

## 2. Comparative Performance Matrix

| Metric | LMFT Capacity Engine | Baseline A: Key-Value Store | Baseline B: Bag-of-Words Matcher |
| :--- | :---: | :---: | :---: |
| **Accuracy (Overall)** | **1.0000 (33/33)** | **1.0000 (33/33)** | 0.9394 (31/33) |
| **Precision on Fired Cases** | **1.0000 (33/33)** | **1.0000 (33/33)** | 1.0000 (31/31) |
| **False Positive Rate** | **0.0000 (0/33)** | **0.0000 (0/33)** | 0.0000 (0/33) |
| **Ambiguity Rate** | **0.0000 (0/33)** | **0.0000 (0/33)** | 0.0606 (2/33) |
| **Abstention Rate** | 0.0000 (0/33) | 0.0000 (0/33) | 0.0000 (0/33) |
| **Continuous Leaf Dials (24)** | **Yes (100% active)** | No (0 dials) | No (0 dials) |
| **Harmonic Concordance ($H$)** | **0.893 (average)** | N/A | N/A |
| **Speaking Register Actuation** | **4 Distinct Registers** | None | None |
| **Execution Latency** | ~0.0002s | ~0.0001s | ~0.0006s |

---

## 3. Scientific Findings & Hypotheses Verification

1. **H1 Confirmed (Classification Accuracy Parity)**:
   Baseline A (Key-Value Store) achieved **100% classification accuracy (33/33)**, perfectly matching the LMFT capacity engine. This confirms that for discrete sense labeling alone, an ordinary dictionary lookup table is fully sufficient and computationally trivial.
2. **H2 Confirmed (Bag-of-Words Ambiguity)**:
   Baseline B (Naive Bag-of-Words) suffered from an **ambiguity rate of 6.06% (2 instances)** where token co-occurrences overlapped across conflicting senses (`order%1:10:00::` vs `order%1:10:03::`), validating why Phase B's bag-of-words approach originally failed.
3. **H3 Confirmed (Continuous Stance & Register Differentiation)**:
   The unique empirical capability of the LMFT architecture does *not* reside in superior discrete classification over an exact dictionary, but in:
   - Populating all 24 canonical leaf nodes across Cultural, Philosophical, Experiential, and Psychological domains.
   - Dynamic homeostatic regulation (counter-balancing dyadic skews via shadow damping).
   - Multi-lens prismatic alignment into calibrated speaking registers and actionable social exchange strategies.
4. **H4 Confirmed (Rule D004 Matched Baseline Parity)**:
   The primary capacity store and matched ordinary structured-memory comparator produced identical evaluation digests (`5c2c7c4c...`). Checkpoints verified unmutated before and after inference.

---

## 4. Persisted Outputs
- Output directory: `outputs/comparative-baseline-corpus33-20261014-001/`
- Summary file: `comparative-benchmark-summary.json`
- Tests: 3 unit tests in `tests/test_comparative_baseline.py`
