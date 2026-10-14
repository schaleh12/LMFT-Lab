# Second Lemma Generalization Protocol: Polysemous Noun *Bank*

## 1. Research Purpose & Hypotheses
Following the successful full-corpus evaluation across the polysemous noun *order* / *orders* (D044–D053), this study investigates cross-lemma generalization (Phase 2). It evaluates whether the unassisted LMFT capacity representation, homeostatic regulation across all 24 canonical leaves, Tripartite Psychological Funnel, and Kaleidoscopic Prism generalize to a completely distinct polysemous noun: **"bank"**.

### Senses Under Study (WordNet 3.0)
1. **Financial Institution (`bank%1:14:00::`)**:
   *"A financial establishment that invests money deposited by customers, pays it out when required, makes loans at interest, and exchanges currency."*
2. **River / Waterway Embankment (`bank%1:17:01::`)**:
   *"Sloping land adjoining a body of water (especially beside a river or stream)."*
3. **Reserve Repository (`bank%1:14:01::`)**:
   *"A supply or stock held in reserve for future use (e.g. data bank, blood bank, memory bank)."*

### Preregistered Hypotheses
1. **Zero False Positives & Precision on Fired Cases (H1)**: Context-anchored capacity rules will achieve **100% precision on all fired cases** (0 wrong singletons, 0.0% false positive rate) across all 3 senses.
2. **Honest Calibrated Abstention on Ambiguous/Unseen Contexts (H2)**: On unanchored sentences (e.g., *"He walked toward the bank."*) or non-target sentences, the system will honestly abstain (decision: `abstain`, zero guesses), triggering *Neutral Observant Silence*.
3. **Cross-Lemma Psychological Funnel & Prismatic Actuation (H3)**: The 3 distinct senses will project into distinct, coherent speaking registers:
   - Financial bank $\rightarrow$ *Methodical & Pragmatic* (quantized fiscal transactions).
   - River bank $\rightarrow$ *Communal & Reassuring* / *Foundational Anchor* (natural ontological boundary).
   - Reserve bank $\rightarrow$ *Authoritative & Chivalrous* / *Scientific* (protective stewardship of life/data reserves).
4. **Matched Ordinary-Memory Baseline Parity (H4 / Rule D004)**: Primary capacity storage and matched ordinary structured-memory comparator will yield byte-for-byte identical evaluation digests.

---

## 2. Benchmark Corpus
The evaluation corpus consists of 11 standardized test instances:
- 4 instances of Financial Bank (`bank%1:14:00::`)
- 3 instances of River Embankment (`bank%1:17:01::`)
- 2 instances of Reserve Repository (`bank%1:14:01::`)
- 1 unanchored ambiguous context instance (*"He walked toward the bank without further explanation."*)
- 1 non-target out-of-distribution instance (*"A gentle breeze blew across the open meadow."*)

Inference is 100% unassisted and offline with zero runtime model invocations.
