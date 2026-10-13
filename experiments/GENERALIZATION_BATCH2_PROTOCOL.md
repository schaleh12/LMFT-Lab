# Generalization Benchmark on SemCor Development Batch 2 — Protocol

**Authoritative Specification — Milestone 4 (2026-10-13)**

## 1. Purpose and Hypotheses

This protocol establishes a frozen, deterministic generalization benchmark evaluating persistent contextual capacity rules compiled from SemCor Development Batch 1 against the 13 unseen instances of SemCor Development Batch 2.

### Research Questions:
1. **Zero Runtime LLM Dependence:** Can persistent capacity memory compiled from disk evaluate completely unseen sentences unassisted with zero inference-time LLM calls?
2. **False Positive Prevention:** Does syntactic context anchoring prevent spurious guesses on unseen syntactic environments, maintaining 0 false positives and high honest abstention?
3. **Cross-Batch Cross-Talk:** Do any Batch 1 syntactic patterns generalize to Batch 2 instances that share context idioms (e.g. magnitude `"of the same order of complexity"` or succession `"in the order of the making of such awards"`)?
4. **Baseline Parity (Rule D004):** Does an ordinary structured-memory comparator produce byte-for-byte identical evaluation digests?
5. **Neutral Store Nonmutation (Rule D001):** Does the neutral state checkpoint SHA256 remain invariant under evaluation?

---

## 2. Benchmark Architecture

- **Training Corpus (Batch 1):** 20 development instances of the polysemous noun *order* / *orders* from SemCor.
- **Evaluation Corpus (Batch 2):** 13 unseen development instances of *order* / *orders* from SemCor (`stage: development_batch_2`).
- **Memory Source:** Neutral checkpoint `C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json`.
- **Inference Mode:** Deterministic Python execution; zero runtime LLM calls.
- **Decision Taxonomy:**
  - `single`: Exactly one persistent capacity rule matched. Evaluated against ground-truth WordNet gold sense key.
  - `abstain`: Zero persistent rules matched the surface context. Honest abstention on unseen contexts.
  - `ambiguous`: Competing rules with discordant sense keys matched.

---

## 3. Matched Ordinary-Memory Baseline

Under Rule D004, the benchmark must run across two distinct consumers:
1. **Primary Consumer:** Reads neutral checkpoint state via `Store.read()`.
2. **Matched Memory Consumer:** Reads identical records via deep-copied raw JSON dictionary.
Both consumers must produce identical prediction records, identical decision counts, and identical SHA256 evaluation digests.
