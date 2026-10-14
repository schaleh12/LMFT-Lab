# Second Lemma Generalization Benchmark (*Bank*) Results

## 1. Executive Summary
Preregistered [Second Lemma Generalization Protocol](SECOND_LEMMA_BANK_PROTOCOL.md) completed across the 11-instance evaluation benchmark for the polysemous noun **"bank"**. Evaluated unassisted cross-lemma capacity representation, homeostatic regulation across all 24 canonical leaves, Tripartite Psychological Funnel, and Kaleidoscopic Prism rotation.

Zero runtime LLM calls during unassisted evaluation. Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity) enforced throughout.

---

## 2. Benchmark Performance Matrix

| Metric | Target Instances (9) | Control Instances (2) | Cumulative Total (11) |
| :--- | :---: | :---: | :---: |
| **Correct Singletons** | **9 / 9 (100.0%)** | N/A | 9 / 11 (81.8%) |
| **Honest Abstentions** | 0 / 9 (0.0%) | **2 / 2 (100.0%)** | 2 / 11 (18.2%) |
| **Wrong Singletons (FP)** | **0 / 9 (0.0%)** | **0 / 2 (0.0%)** | **0 / 11 (0.0% FP rate)** |
| **Precision on Fired Cases** | **100.0% (9 / 9)** | N/A | **100.0% (9 / 9)** |
| **Ambiguity Rate** | 0.0% (0 / 9) | 0.0% (0 / 2) | 0.0% (0 / 11) |
| **Consumer Parity (Rule D004)** | Verified | Verified | **Verified (`consumer_parity: True`)** |

---

## 3. Register & Funnel Differentiation (H3 Confirmed)

All 3 senses mapped cleanly into coherent, differentiated speaking registers:
- **Financial Bank (`bank%1:14:00::`) — 4 instances**:
  - Dials: High Order (0.85), High Discreteness (0.80), High Execution (0.78).
  - Register: **Methodical & Pragmatic**
  - Exemplar: *"Taking this step by step: organizing 'a financial institution for deposits, loans, and commercial transactions' allows us to advance without wasted effort."*
- **River Embankment (`bank%1:17:01::`) — 3 instances**:
  - Dials: High Existence (0.85), High Continuity (0.80), Low Arousal (0.30).
  - Register: **Communal & Reassuring**
  - Exemplar: *"Let us anchor our discussion in the shared foundation: maintaining 'sloping natural land bordering a river or stream' protects us all."*
- **Reserve Repository (`bank%1:14:01::`) — 2 instances**:
  - Dials: High Agency / Stewardship (0.85), High Order (0.80), High Honor (0.90).
  - Register: **Authoritative & Chivalrous**
  - Exemplar: *"Under clear authority, we proceed as directed: 'a critical medical reserve repository of blood supplies for transfusion' must be fulfilled with precision and honor."*
- **Controls (Unanchored & Out-of-Distribution) — 2 instances**:
  - Register: **Neutral Observant Silence**
  - Exemplar: *"I observe the context, but reserve judgment until further evidence arrives."*

---

## 4. Scientific Verification & Invariants

1. **H1 Confirmed (Zero False Positives & 100% Precision)**:
   Context-anchored rules generalized across all 3 senses of *bank* without a single classification error.
2. **H2 Confirmed (Calibrated Honest Abstention)**:
   Unanchored target sentences (*"He walked toward the bank."*) and OOD sentences (*"A gentle breeze blew..."*) cleanly abstained with zero hallucinations.
3. **H3 Confirmed (Cross-Lemma Prismatic Differentiation)**:
   The Tripartite Funnel and Kaleidoscopic Lenses accurately refracted the 3 senses into 3 distinct communicative registers matching their semantic profiles.
4. **H4 Confirmed (Rule D004 Matched Parity)**:
   Primary capacity storage and matched ordinary structured-memory comparator produced identical evaluation digests. Checkpoints unmutated.

---

## 5. Persisted Outputs
- Output directory: `outputs/second-lemma-bank-corpus11-20261014-001/`
- Summary file: `second-lemma-bank-summary.json`
- Tests: 4 unit tests in `tests/test_second_lemma_bank.py`
