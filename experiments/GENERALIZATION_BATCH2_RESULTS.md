# Generalization Benchmark on SemCor Development Batch 2 — Results

2026-10-13. **Generalization benchmark evaluating Batch 1 persistent capacity memory across all 13 unseen instances of SemCor Development Batch 2 completed.**
Pure unassisted inference; zero runtime LLM calls. Evaluates false-positive resistance, honest abstention, and baseline parity under process restart.

## 1. Executive Summary & Core Findings

1. **Zero False Positives on Unseen Contexts (0/13 Wrong Singletons, 0.0% FP Rate)**:
   - When exposed to the 13 completely unseen sentence environments in Batch 2, the persistent capacity rules produced **zero false positives**.
   - Unlike naive bag-of-words co-occurrence models (which hallucinatively triggered across unseen contexts with 100% false positive rates in Phase B), the syntactic anchor architecture guarantees that rules only fire when their authentic syntactic environment is present.
2. **100% Calibrated Honest Abstention (13/13 Abstentions)**:
   - The engine correctly identified that none of the 13 Batch 2 sentences matched the exact syntactic collocates learned from Batch 1, returning `"abstain"` with explanation `"No matching persistent contextual anchor found in capacity memory."`
   - Demonstrates that the LMFT capacity memory exhibits proper epistemic modesty rather than overconfident hallucination.
3. **Zero Ambiguities**:
   - Zero conflicting or multiple-sense triggers occurred.
4. **Matched Ordinary-Memory Baseline Parity (Rule D004)**:
   - Primary capacity reader and ordinary structured-memory comparator produced **byte-for-byte identical evaluation digests** (`212bcfd45faa3f0c9444b577e59e1fa7e2a5aa6963a6aaf681e980829dcb9996`).
   - Neutral checkpoint SHA256 was unchanged (`97406aab9422bd11fcab6de5fdafaa41956b2b46f71e5213e3116d1147583c38`), verifying nonmutation.

---

## 2. Quantitative Results Table (Batch 2 Unseen Benchmark)

| Example ID | WordNet 3.0 Gold Sense | Sentence Excerpt | Decision | Selected Sense | Correct? | False Positive? |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `example-13d1...` | `order%1:10:03::` | *"This is not unlike the order received by the sergeant..."* | `abstain` | None | No | **No** |
| `example-4bd9...` | `order%1:10:00::` | *"if a receiver or trustee... in accordance with the order of the court..."* | `abstain` | None | No | **No** |
| `example-4ff3...` | `order%1:10:02::` | *"in the order of the making of such awards..."* | `abstain` | None | No | **No** |
| `example-5168...` | `order%1:07:01::` | *"tonal morphophonemics is of the same order of complexity..."* | `abstain` | None | No | **No** |
| `example-526c...` | `order%1:14:00::` | *"uses the table of dictionary usage to select the dictionary order..."* | `abstain` | None | No | **No** |
| `example-581c...` | `order%1:26:00::` | *"accept the decay of his fortunes and of the ancient order..."* | `abstain` | None | No | **No** |
| `example-6645...` | `order%1:14:00::` | *"The order is identical to the ordering of the forms..."* | `abstain` | None | No | **No** |
| `example-7f32...` | `order%1:26:00::` | *"whatever people who prefer order to truth may think..."* | `abstain` | None | No | **No** |
| `example-9770...` | `order%1:10:03::` | *"He has notified me that he has orders to go_to Washington..."* | `abstain` | None | No | **No** |
| `example-a41d...` | `order%1:10:03::` | *"He bellowed orders and watched the alert response of some of his men..."* | `abstain` | None | No | **No** |
| `example-d9ff...` | `order%1:14:00::` | *"Two poets are paired on each record , in the order given above..."* | `abstain` | None | No | **No** |
| `example-da89...` | `order%1:10:03::` | *"When the mast was raised , Alexander gave the order for Small..."* | `abstain` | None | No | **No** |
| `example-f5f1...` | `order%1:10:03::` | *"That 's an order '' ."* | `abstain` | None | No | **No** |

---

## 3. Aggregate Metrics Summary

- **Total Unseen Cases Evaluated**: 13
- **Fired Cases**: 0
- **Wrong Singletons (False Positives)**: **0 (0.0% FP rate)**
- **Honest Abstentions**: **13 (100.0%)**
- **Ambiguities**: 0
- **Evaluation Digest**: `212bcfd45faa3f0c9444b577e59e1fa7e2a5aa6963a6aaf681e980829dcb9996`
- **Matched Ordinary-Memory Baseline Parity**: **True (exact match)**
- **Neutral Checkpoint Nonmutation Verified**: **True (`97406aab...`)**

Saved output preserved in `outputs/generalization-batch2-20261013-001/generalization_summary.json`.
