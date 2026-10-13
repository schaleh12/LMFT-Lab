# Protocol: Unified 33-Instance Persistent Capacity Compilation & Unassisted Disambiguation

## 1. Research Question & Hypothesis

Does unifying persistent representations compiled across both SemCor Development Batch 1 (20 instances, Protocol 5) and Batch 2 (13 instances, Protocol 6) enable unassisted, deterministic contextual disambiguation across the complete 33-sentence SemCor development corpus with 100% precision, zero false positives, and zero runtime model calls?

**Hypotheses:**
1. **Full-Corpus Disambiguation Precision:** Persistent contextual rules derived from syntactic anchors will achieve $\ge 95\%$ accuracy and 100% precision on fired cases across all 33 SemCor development instances, completely remedying Phase B's bag-of-words false positive failure.
2. **Mutual Exclusivity & Non-Ambiguity:** Multi-token syntactic context anchors provide sufficient mutual exclusivity such that 0 sentences trigger ambiguous conflicting senses.
3. **Matched Memory Parity (Rule D004):** The primary capacity engine and the matched ordinary structured-memory comparator produce byte-for-byte identical predictions, rule compilations, and evaluation digests.
4. **State Invariance Across Restart:** Checkpoint files remain read-only and unmutated during inference; fresh child process evaluation reproduces the evaluation digest identically.

## 2. Pinned Inputs & Artifacts

- **Batch 1 Checkpoint:**
  `C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json`
  SHA256: `97406aab9422bd11fcab6de5fdafaa41956b2b46f71e5213e3116d1147583c38`.
- **Batch 2 Checkpoint:**
  `C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v6-20261013-001\neutral-state\checkpoint.json`
  SHA256: `6da29752475ac52f92faaf03ed97ff7ad125885bd55649fe7d1c412d9731f0f5`.
- **SemCor Development Export:**
  `C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json`
  SHA256: `77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`.

## 3. Evaluation Rules & Invariants

1. **Unassisted Inference:** Zero LLM calls are permitted during rule matching and inference. Evaluation is pure Python string/token matching against persistent memory state.
2. **Blind Input Contract:** `validate_public_item()` enforces that the evaluator receives only `{id, tokens, target_indices}`. Gold sense keys and stages are strictly withheld during inference and only joined during scoring.
3. **Comparator Parity:** An ordinary structured-memory comparator reads identical JSON records and runs the identical prediction pipeline.
4. **Nonmutation:** Checkpoint SHA256 hashes must be verified before and after evaluation. Any change constitutes a test failure.
