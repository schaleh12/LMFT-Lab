# Dual-Speed Memory Consolidation Protocol ("Sleep / Replay") (Phase 3)

## 1. Research Question & Purpose
Can the LMFT mirror biological hippocampal-neocortical memory consolidation by replaying episodic records during offline sleep phases, promoting recurring patterns ($N \ge \text{min\_confirmations}$) into persistent capacity rules with habituated weights and structured provenance while pruning transient buffer noise, without mutating or expanding the frozen 40-node founding seed (Rule D001)?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant. Consolidated long-term rules exist strictly outside the founding seed as persistent capacity associations.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator executing identical replay, promotion, reinforcement, and pruning routines; require 100% byte-for-byte evaluation digest parity.
- **Pattern Graduation Threshold:**
  - A candidate pattern must be witnessed $N \ge 2$ times across episodes to graduate into a persistent long-term capacity rule.
  - Sub-threshold singletons ($N = 1$) are pruned to prevent memory and token bloat.
  - Unresolved cognitive conflict episodes are preserved in the buffer for waking resolution.
- **Zero Runtime LLM Calls:** All replay and consolidation computations are executed deterministically offline.

## 3. Benchmark Dataset Structure (2 Consecutive Sleep Cycles)
- **Initial Rule:** `rule-order-cmd-01` (*court order*, weight $0.50$).
- **Sleep Cycle 1 (5 Episodes):**
  - Episodes 1 & 2: *national bank* (financial, 2 occurrences).
  - Episode 3: *court order* (decree, 1 occurrence matching existing rule).
  - Episode 4: *wandering sparrow* (bird, 1 singleton occurrence).
  - Episode 5: *contradictory order* (conflict, 1 occurrence with `is_conflict = True`).
- **Sleep Cycle 2 (3 Episodes):**
  - Episode 6: *national bank* (financial, 3rd occurrence across cycles).
  - Episodes 7 & 8: *river bank* (landscape, 2 occurrences).

## 4. Evaluation Criteria
- 100% promotion of patterns meeting $N \ge 2$ threshold.
- Progressive fuzzy reinforcement of recurring existing rules ($w \rightarrow 0.60 \rightarrow 0.68$).
- Clean pruning of transient singletons and retention of conflict episodes.
- Exact byte-for-byte state digest parity against ordinary memory comparator.
