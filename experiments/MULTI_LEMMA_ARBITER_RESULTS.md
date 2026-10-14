# Multi-Lemma Polysemy Arbiter Results (Phase 1)

## Experiment Summary
- **Protocol:** [MULTI_LEMMA_ARBITER_PROTOCOL.md](MULTI_LEMMA_ARBITER_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/multi_lemma_arbiter.py`](../src/lmft_lab/multi_lemma_arbiter.py)
- **Harness:** [`experiments/multi_lemma_arbiter.py`](multi_lemma_arbiter.py)
- **Outputs:** `outputs/multi-lemma-arbiter-corpus9-20261014-001/multi-lemma-arbiter-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. 100.0% Precision on Fired Target Occurrences (12/12)
Across all 5 compound sentences and 2 single-target sentences (12 active target occurrences of *order* and *bank*):
- Every single target occurrence was resolved to its exact gold sense without a single misclassification.
- Zero wrong singletons were produced (**0.0% false-positive rate**).

### 2. Complete Elimination of Cross-Anchor Contamination
In sentences containing both targets:
- Financial collocate anchors around *bank* did not cause *order* to falsely trigger commercial senses when it was a judicial command.
- Embankment/canal collocate anchors around *bank* did not distort *order* when it referred to methodical sequence (*rank and order*).
- Local context window bounding ($\pm 4$ tokens) successfully prevented lexical bleed across clauses.

### 3. Calibrated Honest Abstentions on Controls (2/2)
- In the ambiguous sentence (*"He walked past the bank thinking about an order he had heard about"*), both targets were detected, but neither possessed verified collocation anchors; the arbiter honestly abstained on both (0 false guesses).
- In the out-of-domain distractor sentence, zero targets were detected, triggering calibrated *Neutral Observant Silence*.

### 4. Harmonic Multi-Register Compound Synthesis
Compound sentences produced clean blended speaking registers reflecting both constituent postures:
- Commercial Bank + Court Order $\rightarrow$ **Authoritative & Methodical Synthesis**
- River/Canal Bank + Commercial/Sequence Order $\rightarrow$ **Communal & Methodical Synthesis**
- Blood Bank + Emergency Supply Order $\rightarrow$ **Authoritative & Methodical Synthesis**
- Investment Bank + Order of Magnitude $\rightarrow$ **Equilibrated & Methodical Synthesis**

### 5. Ordinary Memory Baseline Parity (Rule D004)
Primary capacity arbiter and the matched ordinary structured-memory comparator achieved byte-for-byte evaluation parity across all 9 benchmark sentences and 14 target occurrences.

### 6. Frozen Founding Seed Invariant (Rule D001)
The 40 founding nodes in `birth.py` were verified strictly unmutated.
