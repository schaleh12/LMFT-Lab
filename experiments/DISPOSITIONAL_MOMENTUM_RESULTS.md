# Persistent Dispositional State Vector & Momentum Drift Results (Phase 4)

## Experiment Summary
- **Protocol:** [DISPOSITIONAL_MOMENTUM_PROTOCOL.md](DISPOSITIONAL_MOMENTUM_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/dispositional_momentum.py`](../src/lmft_lab/dispositional_momentum.py)
- **Harness:** [`experiments/dispositional_momentum.py`](dispositional_momentum.py)
- **Outputs:** `outputs/dispositional-momentum-benchmark-20261014-001/dispositional-momentum-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. Temporal Dispositional Continuity Across Interactions
- **Living Momentum:** In Turn 1, an authoritative stimulus raised Order from $0.50$ to **$0.6050$**. In Turn 4, after chaotic disruption and philosophical contemplation, a neutral pause ($0.50$ stimulus) did **not** reset Order back to baseline; it retained an ongoing elevated disposition of **$0.5682$**.
- **Equilibrium Relaxation Half-Life:** Across 5 consecutive idle drift steps, elevated Order relaxed smoothly from $0.5682$ toward equilibrium ($0.50$), arriving at **$0.5528$** without discontinuous snapping.

### 2. 100% Round-Trip Restoration Fidelity & Seed Guardrails
- The 24-leaf dispositional state serialized to an atomic state structure and was restored into a fresh instance with 100% field and digest parity (`1762c7793f537b28...`).
- A tampered payload simulating a mutated 41-node seed geometry triggered immediate rejection (`ValueError: Seed geometry violation`), strictly safeguarding Rule D001.

### 3. Matched Ordinary-Memory Baseline Parity (Rule D004)
- An ordinary structured-memory comparator performing parallel EMA updates, drift steps, and state exports matched the primary engine byte-for-byte across all turns (`1762c7793f537b28...`).

### 4. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
