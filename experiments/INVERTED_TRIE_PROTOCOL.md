# Inverted Lemma Index & Context Trie Scalability Protocol (Phase 1)

## 1. Research Question & Purpose
Can an inverted token hash map coupled with a longest-prefix collocation trie eliminate $O(N)$ linear rule search, providing sub-millisecond query evaluation across 1,000+ capacity rules with 100% decision equivalence?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator running linear scans; require 100% parity across matched rule IDs.
- **Equivalence Invariant:** The inverted trie index must return the exact same rule set as a full linear scan (zero false positives, zero false negatives).
- **Zero Runtime LLM Calls:** All index construction and retrieval must be computed deterministically offline.

## 3. Benchmark Dataset Structure
- 1,000 capacity rules (11 ground-truth base rules across *order* and *bank* plus 989 synthetic distractors).
- 6 multi-target benchmark queries (compound financial/command, commercial/river, sequence/embankment, reserve/magnitude, and negative distractor).

## 4. Evaluation Criteria
- 100% decision equivalence with linear scan.
- Speedup factor $\ge 10\times$ (target: $>50\times$).
- Query latency $< 0.5$ ms per sentence.
- Exact byte-for-byte evaluation parity against the ordinary memory comparator.
