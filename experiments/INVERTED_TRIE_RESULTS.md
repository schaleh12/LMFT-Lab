# Inverted Lemma Index & Context Trie Scalability Results (Phase 1)

## Experiment Summary
- **Protocol:** [INVERTED_TRIE_PROTOCOL.md](INVERTED_TRIE_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/inverted_trie.py`](../src/lmft_lab/inverted_trie.py)
- **Harness:** [`experiments/inverted_trie.py`](inverted_trie.py)
- **Outputs:** `outputs/inverted-trie-benchmark-corpus1000-20261014-001/inverted-trie-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. 63.0x Speedup Over Linear Scan
- Across 1,000 capacity rules:
  - Average Linear Scan Latency: **4.221 ms** per sentence.
  - Average Inverted Trie Latency: **0.067 ms** (67 microseconds) per sentence.
  - Latency speedup factor: **63.0x faster**.
  - Total index construction time for 1,000 rules: **5.64 ms**.

### 2. 100.0% Decision Equivalence (Zero Divergence)
- Across all multi-target and negative distractor sentences, the inverted trie matched the exact rule sets returned by the exhaustive linear scan.
- Zero false negatives (no missed rules) and zero false positives.

### 3. Matched Ordinary-Memory Baseline Parity (Rule D004)
- Matched ordinary structured-memory comparator running parallel evaluations produced 100% identical decision digests.

### 4. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
