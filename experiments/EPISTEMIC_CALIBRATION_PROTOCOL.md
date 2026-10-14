# Epistemic Modesty & Adversarial Noise Calibration Protocol (Phase 3)

## 1. Research Question & Purpose
Can we mathematically formalize and calibrate the decision boundary between active speaking postures and *Neutral Observant Silence* to guarantee a 0.0% false-positive rate across noisy distractors and adversarial out-of-domain text without compromising recall on valid contextual anchors?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator; require byte-for-byte evaluation parity.
- **Pareto Optimality:** Identify the optimal threshold $\tau^*$ that maximizes recall while keeping false-positive rate strictly at $0.0\%$.
- **Zero Runtime LLM Calls:** All alignments and classification decisions must be computed deterministically offline.

## 3. Benchmark Dataset Structure (16 Instances)
1. **Exact Matches (4 instances):** Full token alignment ($S = 1.00$).
2. **High Partial Collocations (4 instances):** Core anchor embedded in extended natural syntax ($S \in [0.60, 0.85]$).
3. **Noisy Distractor Sentences (4 instances):** Sentences sharing single incidental tokens but lacking the target polysemous sense ($S \in [0.25, 0.50]$).
4. **Adversarial Out-of-Domain Sentences (4 instances):** Scientific, geological, or historical text completely unrelated to the target domains ($S = 0.00$).

## 4. Evaluation Criteria
- Zero false positives ($FP = 0$, $FPR = 0.0\%$).
- 100% honest abstention on all distractors and adversarial text.
- 100% precision on fired cases.
- Exact byte-for-byte state parity against the ordinary memory comparator.
