# Persistent Capacity Memory Decay & Reinforcement Results (Phase 2)

## Experiment Summary
- **Protocol:** [CAPACITY_DECAY_PROTOCOL.md](CAPACITY_DECAY_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/capacity_decay.py`](../src/lmft_lab/capacity_decay.py)
- **Harness:** [`experiments/capacity_decay.py`](capacity_decay.py)
- **Outputs:** `outputs/capacity-decay-benchmark-20261014-001/capacity-decay-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. Controlled Asymptotic Reinforcement
- Learned rules reinforced across consecutive interaction cycles demonstrated smooth asymptotic convergence towards the ceiling ($1.00$).
- Rules with repeated confirmation (`rule-bank-com`) advanced from baseline $0.50 \rightarrow 0.60 \rightarrow 0.68 \rightarrow 0.744 \dots \rightarrow 0.6692$ (factoring in scheduled idle periods).

### 2. Monotonic Habituation Decay
- Idle rules unvisited during inactive epochs exhibited gradual, monotonic decay ($0.50 \rightarrow 0.475 \rightarrow 0.451 \dots$) without dropping below the defined stability floor ($0.10$).
- Prevents unused or transient associations from monopolizing memory capacity over extended operational lifespans.

### 3. Immediate Contradiction Damping
- Conflicting feedback (`rule-order-mag`) triggered an immediate proportional penalty drop ($-35\%$), reducing the weight from $0.528 \rightarrow 0.3432$ in a single epoch, effectively quarantining suspected associations until subsequent independent re-verification.

### 4. Ordinary Memory Baseline Parity (Rule D004)
- Matched ordinary structured-memory comparator running parallel transitions achieved 100% byte-for-byte state digest parity across all 10 epochs.

### 5. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
