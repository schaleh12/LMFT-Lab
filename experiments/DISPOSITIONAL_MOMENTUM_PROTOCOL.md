# Persistent Dispositional State Vector & Momentum Drift Protocol (Phase 4)

## 1. Research Question & Purpose
Can the LMFT maintain a persistent dispositional state vector across sequential interactions (an ongoing temporal "mood" or baseline) for all 24 canonical leaves in `birth.py`, using exponential moving average (EMA) momentum drift and gentle equilibrium relaxation, and serialize cleanly with Rule D001 seed invariant enforcement?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant. The dispositional vector tracks continuous activations across the 24 canonical leaf nodes. Any imported state with a mismatched seed fingerprint must be rejected with `ValueError`.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator performing identical EMA updates, drift steps, and export serializations; require 100% byte-for-byte evaluation digest parity.
- **Continuous Momentum Formulation:**
  $$\vec{D}_t = (1 - \gamma) \vec{D}_{t-1} + \gamma \vec{S}_t$$
  where $\gamma \in [0.05, 0.95]$ (default $\gamma = 0.35$).
- **Equilibrium Relaxation:**
  $$\vec{D}_{\text{drift}} = \vec{D} + \mu \cdot (0.50 - \vec{D})$$
  where $\mu \in [0.01, 0.50]$ (default $\mu = 0.05$).
- **Zero Runtime LLM Calls:** All trajectory transitions and persistence operations must be computed deterministically offline.

## 3. Benchmark Dataset Structure (4-Turn Trajectory + Drift + Serialization)
- Turn 1: Authoritative directive stimulus (high Power, Order, Intention).
- Turn 2: Unexpected chaotic disruption (high Chaos, Novelty, Arousal).
- Turn 3: Epistemic contemplation and fairness (high Fairness, Clarity, Continuity).
- Turn 4: Neutral pause (Order=0.50, Power=0.50) demonstrating dispositional momentum preservation.
- Idle Phase: 5 consecutive equilibrium drift steps relaxing toward $0.50$.
- Persistence Phase: Export to atomic state dictionary, integrity validation, simulated restart restoration, and tampered seed rejection.

## 4. Evaluation Criteria
- Observable temporal continuity: Turn 4 retains elevated Order ($>0.55$) rather than dropping instantaneously to $0.50$.
- Smooth equilibrium relaxation across idle steps.
- 100% round-trip restoration fidelity and 100% detection of forged seed fingerprints.
- Exact byte-for-byte evaluation digest parity against ordinary memory comparator.
