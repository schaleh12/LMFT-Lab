# Affective Plasticity Regulation Results (Phase 2)

## Experiment Summary
- **Protocol:** [AFFECTIVE_PLASTICITY_PROTOCOL.md](AFFECTIVE_PLASTICITY_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/affective_plasticity.py`](../src/lmft_lab/affective_plasticity.py)
- **Harness:** [`experiments/affective_plasticity.py`](affective_plasticity.py)
- **Outputs:** `outputs/affective-plasticity-benchmark-20261014-001/affective-plasticity-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. Dynamic Plasticity Adaptation Across Affective Regimes
- **Surprise-Driven Hyper-Adaptation:** Under high novelty ($0.95$) and arousal ($0.90$), learning plasticity spiked from baseline $0.20$ to **$\alpha = 0.358$** ($+79.0\%$ boost), moving rule weight from $0.50$ to **$0.679$** in a single observation.
- **Mastery-Driven Knowledge Protection:** Under high contemplation clarity ($0.95$) and confidence ($0.95$), learning plasticity was throttled down to **$\alpha = 0.089$** ($-55.5\%$ reduction), preventing noisy fluctuations from disturbing established memory.
- **Affective Memory Retention Modulation:** High retention and positive valence slowed habituation decay to **$\lambda = 0.0278$**, whereas volatile, ungrounded contexts accelerated decay to **$\lambda = 0.061$**.
- **Contradiction Penalty Amplification:** Intense arousal under epistemic uncertainty increased damping penalty from standard $0.35$ up to **$\delta = 0.4375$**.

### 2. Strict Baseline Reproduction under Neutral State
- When initialized at default $0.50$ coordinates, the engine reproduced the standard rates identically ($\alpha = 0.2000$, $\lambda = 0.0500$, $\delta = 0.3500$).

### 3. Matched Ordinary-Memory Baseline Parity (Rule D004)
- An ordinary structured-memory comparator performing parallel rate calculations and weight transitions matched the primary engine byte-for-byte across all 6 benchmark conditions (`61b76a2375566abf...`).

### 4. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
