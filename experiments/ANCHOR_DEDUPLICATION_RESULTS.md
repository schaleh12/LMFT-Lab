# Anchor Normalization & Deduplication Results (Phase 2)

## Experiment Summary
- **Protocol:** [ANCHOR_DEDUPLICATION_PROTOCOL.md](ANCHOR_DEDUPLICATION_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/anchor_deduplication.py`](../src/lmft_lab/anchor_deduplication.py)
- **Harness:** [`experiments/anchor_deduplication.py`](anchor_deduplication.py)
- **Outputs:** `outputs/anchor-deduplication-benchmark-corpus20-20261014-001/anchor-deduplication-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. 60.0% Redundancy Elimination (20 $\rightarrow$ 8 Rules)
- The normalization pipeline stripped extraneous articles (*the*, *a*, *an*), possessives (*their*, *its*), and trailing punctuation.
- Condensed 20 raw candidate proposals into **8 unique, canonical capacity rules**, merging 12 redundant variants (memory compression ratio: **40.0%**).

### 2. Witness Union and Richest Gloss Retention
- Merged rules preserved complete observational provenance by taking the set union of all witness IDs.
- For each cluster, the longest and most informative explanatory gloss was retained.

### 3. Progressive Confidence Reinforcement
- Each duplicate observation acted as independent empirical confirmation:
  - 1 confirmation: $w = 0.50$
  - 3 confirmations: $w = 0.6387$
  - 4 confirmations: $w = 0.6929$

### 4. Matched Ordinary-Memory Baseline Parity (Rule D004)
- Matched ordinary structured-memory comparator running parallel deduplication produced byte-for-byte identical rule sets and summary digests.

### 5. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
