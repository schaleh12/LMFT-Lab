# Persistent Capacity Memory Decay & Reinforcement Protocol (Phase 2)

## 1. Research Question & Purpose
Can learned capacity memory rules undergo continuous, bounded fuzzy habituation and reinforcement dynamics without mutating the canonical 40-node founding seed or violating ordinary-memory parity?

## 2. Mathematical Equations
1. **Fuzzy Asymptotic Reinforcement (Consistent Evidence):**
   $$w_{t+1} = \min(1.0, w_t + \alpha \cdot (1.0 - w_t))$$
   where default learning rate $\alpha = 0.20$. Clamped at ceiling $1.00$ with $\epsilon = 0.0005$ snapping.

2. **Monotonic Habituation Decay (Inactivity Epochs):**
   $$w_{t+1} = \max(0.10, w_t \cdot (1.0 - \lambda))$$
   where default decay rate $\lambda = 0.05$. Clamped at floor $0.10$.

3. **Contradiction Penalty Damping (Conflicting Feedback):**
   $$w_{t+1} = \max(0.10, w_t \cdot (1.0 - \beta))$$
   where default penalty rate $\beta = 0.35$. Clamped at floor $0.10$.

## 3. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The 40 founding nodes in `birth.py` must remain completely invariant.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator running identical equations; require byte-for-byte state parity.
- **Strict Boundedness:** All weights must reside strictly within $[0.10, 1.00]$ across all epochs.
- **Zero Runtime LLM Calls:** All weight transitions must be computed deterministically offline.

## 4. Evaluation Criteria
- 10-epoch multi-rule simulation across reinforcement, decay, and contradiction events.
- Monotonicity and boundary compliance across all rules.
- Exact byte-for-byte digest reproduction against the ordinary memory comparator.
