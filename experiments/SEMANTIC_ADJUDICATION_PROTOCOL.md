# Semantic Adjudication Protocol — Evaluation of Admitted Context-Anchored Representations

2026-10-13. Formal preregistered protocol for evaluating the semantic validity,
explanatory informativeness, and discriminative utility of the four admitted local-SLM
representations from Protocol 3 (`representation-01` through `04`).

## 1. Research Purpose & Invariants

Protocol 3 established **interface admissibility**: the 4B SLM reliably emits valid JSON
with non-target context quotes, and Python deterministically reconstructs contiguous token
slices without index math faults (100% admissible, 4/4).

However, in accordance with [AGENTS.md](../AGENTS.md) and [DECISIONS.md](../DECISIONS.md) D003:
**syntactic admissibility is not semantic truth or cognitive capability.**
We must not conflate a valid schema response with successful semantic disambiguation.

This protocol defines the formal criteria for **Semantic Adjudication**:
1. Evaluating whether the proposed glosses provide genuine semantic explanation or tautological restatement.
2. Assessing concordance between the proposals and WordNet 3.0 gold sense definitions.
3. Quantifying the discriminative power and precision of the extracted context anchors across the full development dataset (33 examples), directly contrasting them with the failed Phase B bag-of-words rules.
4. Enforcing the matched ordinary-memory baseline (Rule D004) under identical deterministic evaluation and restart verification.

## 2. Frozen Evaluation Inputs

1. **Admitted Neutral Checkpoint**:
   `C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v3-20261013-001\neutral-state\checkpoint.json`
   SHA256: `d156a8125d6aa8028557345a597bcb648fdab78d982ecb7bbee54beab096d25e`.
   Contains the 4 admitted proposals: `representation-01`, `02`, `03`, `04`.

2. **Approved Development Export**:
   `development.json` (SHA256: `77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`).
   Contains 33 development examples across 8 WordNet sense keys for lemma `order`.

3. **Ground Truth WordNet 3.0 Definitions**:
   - `order%1:07:01::`: degree / magnitude ("(often followed by 'of') a degree in a continuum of size or quantity").
   - `order%1:10:00::`: judicial decree / authoritative command ("a formal legal document issued by a court or authority").
   - `order%1:10:01::`: commercial purchase order ("a commercial document requesting that a supplier provide merchandise or services").
   - `order%1:10:02::`: sequence / arrangement ("the arrangement of things in succession; succession").

## 3. Adjudication Dimensions & Metrics

### Dimension A: Gloss Informativeness (Tautology vs Substitution)
- **Tautology Check**: Does the gloss repeat the target lemma (`order` / `orders`)?
  - A gloss that contains `order` without explaining its meaning is flagged as *tautological / clause-copy*.
  - A gloss that substitutes the target lemma with an explanatory synonym or concept (e.g. `sequence`) is scored as *informative substitution*.
- **Metrics**:
  - `tautology_present`: Boolean.
  - `target_substituted`: Boolean (`not tautology_present`).
  - `gloss_char_length`: Integer.
  - `gloss_token_count`: Integer.

### Dimension B: WordNet Gold Sense Concordance
- **Semantic Alignment**:
  - Does the proposal identify the core semantic distinction of the target sense key?
  - Evaluated on a 3-point scale:
    - `concordant` (2): correctly captures the specific meaning (e.g. sequence for `order%1:10:02::`).
    - `partially_concordant` (1): captures general context or situational setting, but relies on unclarified target usage.
    - `discordant` (0): contradicts or misidentifies the sense.

### Dimension C: Context Anchor Discriminative Power (Cross-Example Matching)
- **Matching Rule**:
  Extract the non-target phrase pattern from `context_anchor`.
  Apply the pattern across all 33 examples in `development.json`.
- **Metrics Recorded**:
  - `true_positives` (TP): matches examples annotated with the identical gold sense.
  - `false_positives` (FP): matches examples annotated with a different sense.
  - `false_negatives` (FN): examples with the identical sense that were not matched.
  - `precision`: $TP / (TP + FP)$ if $(TP + FP) > 0$ else $0.0$.
  - `recall`: $TP / (TP + FN)$.
  - `false_positive_rate`: $FP / (33 - \text{gold\_count})$.
  - Comparison against Phase B: Compare FP rate of these contiguous syntactic anchors against the catastrophic Phase B function-word pairs (`a` + `by` had 4 false positives, 0 true positives).

### Dimension D: Matched Ordinary-Memory Baseline Comparison (Rule D004)
- Run identical adjudication metrics independently through:
  1. Primary LMFT capacity record reader.
  2. Ordinary structured-memory comparator reader.
- Parity requirement: Both readers must produce byte-for-byte identical metric records and SHA256 digests.
- Nonmutation requirement: The neutral store checkpoint must remain unmodified.

## 4. Execution Protocol

- Zero additional LLM calls; pure deterministic Python evaluation.
- All evaluation logic implemented in `experiments/semantic_adjudication.py`.
- Automated test coverage in `tests/test_semantic_adjudication.py`.
- Results published to `experiments/SEMANTIC_ADJUDICATION_RESULTS.md`.
- Consequential choices recorded in `DECISIONS.md` (D035) and `PROJECT_STATE.md`.
