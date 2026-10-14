# Fuzzy Prerequisite Coherence Gate Results (Phase 1)

## Experiment Summary
- **Protocol:** [PREREQUISITE_GATE_PROTOCOL.md](PREREQUISITE_GATE_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/prerequisite_gate.py`](../src/lmft_lab/prerequisite_gate.py)
- **Harness:** [`experiments/prerequisite_gate.py`](prerequisite_gate.py)
- **Outputs:** `outputs/prerequisite-gate-benchmark-20261014-001/prerequisite-gate-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. 100% Distortion Detection & Authentic Score Attenuation
- **Coerced Compliance Flagged:** Nominal Justice ($0.90$) asserted under crushed Freedom ($0.10$) was unmasked and damped by **$-54.0\%$** to an authentic score of **$0.4140$**, cleanly triggering `Coerced Compliance Distortion`.
- **Dogmatic Hallucination Flagged:** Nominal Confidence ($0.95$) asserted under near-zero Clarity ($0.05$) was attenuated by **$-66.5\%$** to **$0.3182$**, cleanly triggering `Dogmatic Hallucination Distortion`.
- **Unanchored Volition Flagged:** Nominal Intention ($0.85$) asserted under low Agency ($0.15$) was attenuated by **$-51.0\%$** to **$0.4165$**, triggering `Unanchored Volition Distortion`.
- **Ephemeral Symmetry Flagged:** Nominal Order ($0.90$) asserted without Persistence ($0.10$) was attenuated by **$-54.0\%$** to **$0.4140$**, triggering `Ephemeral Symmetry Distortion`.

### 2. High Coherence Verification on Genuine Virtues
- In `authentic_harmonic_virtue`, where all virtues satisfied their necessary prerequisites (Freedom $\ge 0.90$, Clarity $\ge 0.90$, Agency $\ge 0.90$, Persistence $\ge 0.90$), the system achieved a **Global Coherence Index of $0.9429$**, zero distortions, and verified `is_authentic = True`.

### 3. Matched Ordinary-Memory Baseline Parity (Rule D004)
- An ordinary structured-memory comparator performing parallel gating calculations matched the primary engine byte-for-byte across all 6 benchmark scenarios (`4676efb1432b5bd2...`).

### 4. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
