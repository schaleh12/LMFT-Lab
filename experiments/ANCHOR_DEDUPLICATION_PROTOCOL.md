# Anchor Normalization & Deduplication Protocol (Phase 2)

## 1. Research Question & Purpose
Can automated collocate proposals with diverse surface phrasings (determiner variants, punctuation, whitespace) be deterministically normalized, grouped, and deduplicated into canonical capacity rules with aggregated witnesses and fuzzy reinforcement confidence boosts?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator running identical normalization and merging; require byte-for-byte state parity.
- **Deduplication Invariant:** Non-duplicate rules must never be dropped or conflated across distinct senses or distinct lemmas.
- **Zero Runtime LLM Calls:** All normalization, grouping, and merging must be computed deterministically offline.

## 3. Benchmark Dataset Structure (20 Raw Candidates)
- 4 variants of *commercial bank* (*"the commercial bank"*, *"commercial bank."*, *"a commercial bank"*, *"commercial bank"*)
- 3 variants of *central bank*
- 3 variants of *river bank*
- 4 variants of *court order*
- 3 variants of *rank and order*
- 3 unique non-duplicate rules (*blood bank*, *placed an order*, *order of magnitude*)

## 4. Evaluation Criteria
- 100% normalization of determiners, punctuation, and case.
- Exact consolidation from 20 candidates down to 8 canonical rules (12 duplicates merged).
- Witness union and reinforcement weight boosting on confirmed duplicate hits.
- Exact byte-for-byte state parity against the ordinary memory comparator.
