# Multi-Lemma Polysemy Arbiter Protocol (Phase 1)

## 1. Research Question & Purpose
Can the LMFT architecture process natural language sentences containing multiple polysemous target lemmas (e.g. *order* and *bank*) simultaneously without cross-anchor contamination or keyword bleed, while harmonically synthesizing their individual operational postures into a composite multi-lens register?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched dictionary comparator on the exact same token windows; require byte-for-byte decision parity.
- **Zero Unassisted LLM Calls:** All sense resolution and register composition must be computed deterministically offline.
- **Epistemic Honesty:** Unanchored target occurrences and out-of-distribution text must trigger honest abstentions and *Neutral Observant Silence*.

## 3. Benchmark Dataset & Categories
1. **Compound Multi-Target Sentences (5 instances):**
   - Commercial Bank (Financial) + Court Order (Command)
   - River Bank (Embankment) + Placed an Order (Commercial Transaction)
   - Canal Bank (Embankment) + Rank and Order (Sequence)
   - Blood Bank (Reserve Repository) + Emergency Order of Supplies (Commercial Requisition)
   - Investment Bank (Financial) + Order of Magnitude (Degree/Scale)
2. **Single Target Sentences (2 instances):**
   - Commercial Bank Only
   - Court Order Only
3. **Control Sentences (2 instances):**
   - Ambiguous Unanchored Targets (*bank* and *order* present without valid collocation anchors)
   - Out-of-Domain Distractor (clean natural text without any target lemmas)

## 4. Evaluation Criteria
- Precision on fired target occurrences $\ge 0.95$ (target: 1.00).
- False positive rate $\le 0.05$ (target: 0.00).
- 100% honest abstention on control instances.
- Harmonious composite register synthesis without cross-talk.
- Exact byte-for-byte consumer parity against the ordinary memory comparator.
