# Affective Plasticity Regulation Protocol (Phase 2)

## 1. Research Question & Purpose
Can learning plasticity ($\alpha$), habituation decay ($\lambda$), and contradiction damping ($\delta$) be dynamically modulated as a continuous function of live `Experiential` (Novelty, Arousal, Valence, Retention) and `Psychological` (Contemplation Clarity, Confidence) states such that surprise accelerates adaptation while mastery protects established associations, without mutating or expanding the frozen 40-node founding seed (Rule D001)?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant. Affective plasticity regulates dynamic rate coefficients; it does not add or rename seed nodes.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator running identical dynamic rate calculations and weight transitions; require 100% byte-for-byte evaluation digest parity.
- **Continuous Parameter Boundedness:** 
  - Dynamic learning rate: $\alpha^* \in [0.05, 0.45]$
  - Dynamic decay rate: $\lambda^* \in [0.01, 0.15]$
  - Dynamic damping penalty: $\delta^* \in [0.20, 0.60]$
  - Weight values: $w \in [0.10, 1.00]$
- **Zero Runtime LLM Calls:** All rate evaluations and weight modulations must be computed deterministically offline.

## 3. Benchmark Dataset Structure (6 Conditions)
1. `high_novelty_high_arousal_surprise`: High surprise (Novelty=0.95, Arousal=0.90, Clarity=0.20, Confidence=0.20) testing $\alpha > 0.28$.
2. `high_clarity_high_confidence_mastery`: High mastery (Clarity=0.95, Confidence=0.95, Novelty=0.10) testing $\alpha < 0.15$.
3. `high_retention_positive_valence_preservation`: High retention (0.95) and positive valence (0.90) testing slowed decay ($\lambda < 0.035$).
4. `low_retention_negative_valence_volatility`: Low retention (0.10) and negative valence (0.10) testing accelerated decay ($\lambda > 0.055$).
5. `high_arousal_low_confidence_contradiction`: High arousal and low confidence testing intensified contradiction penalty ($\delta > 0.40$).
6. `neutral_equilibrium_baseline`: Baseline $0.50$ coordinates testing reproduction of standard baseline rates ($\alpha=0.20, \lambda=0.05, \delta=0.35$).

## 4. Evaluation Criteria
- Observable regime separation: Hyper-Adaptive under surprise vs. Protected Mastery under certainty.
- 100% adherence to rate and weight bounds across all transitions.
- Exact byte-for-byte state digest parity against ordinary memory baseline comparator.
