# Dual-Coded Episodic Saliency Journal Results (Phase 2)

## Experiment Summary
- **Protocol:** [EPISODIC_JOURNAL_PROTOCOL.md](EPISODIC_JOURNAL_PROTOCOL.md)
- **Engine Implementation:** [`src/lmft_lab/episodic_journal.py`](../src/lmft_lab/episodic_journal.py)
- **Harness:** [`experiments/episodic_journal.py`](episodic_journal.py)
- **Outputs:** `outputs/episodic-journal-benchmark-20261014-001/episodic-journal-summary.json`
- **Execution Date:** 2026-10-14
- **Runtime LLM Calls:** 0 (completely unassisted deterministic evaluation)

## Key Findings

### 1. Saliency Admission Gate & Anti-Bloat Filtration
- Evaluated 5 interaction episodes:
  - **4/4 Salient / Disrupted Events Admitted:**
    - High salience ($0.85$): admitted (`ep-0001-001`).
    - Disruption / conflict ($0.25$ clarity, $0.80$ arousal): admitted (`ep-0003-002`).
    - High novelty ($0.85$): admitted (`ep-0004-003`).
    - High salience ($0.78$): admitted (`ep-0005-004`).
  - **1/1 Mundane Event Filtered Out:**
    - Sub-threshold ambient event (salience $0.45$, novelty $0.40$, no conflict) was cleanly rejected (`admitted = False`, `episode = None`), preserving buffer capacity and preventing memory bloat.

### 2. Dual-Coded Narrative Synthesis
- Each admitted episode recorded:
  1. **Factual Anchor:** Exact input sentence, target lemma, resolved sense.
  2. **Affective Snapshot:** 24-leaf dials (arousal, valence, novelty, salience, clarity, order).
  3. **Actuation Record:** Emitted speaking register and action bid.
  4. **English Narrative Reflection:** Coherent first-person retrospective prose.
     - E.g. Normal resolution: *"Cycle 1: I resolved 'bank' (bank as depository_financial_institution) in context 'The national bank issued an executive financial guarantee for the treasury.'. My structural order harmonized with Authoritative & Chivalrous, stabilizing clarity at 0.90."*
     - E.g. Cognitive conflict: *"Cycle 3: I faced a cognitive conflict regarding 'order' in sentence 'The contradictory edict commanded immediate retreat while demanding holding ground.'. My cognitive arousal was elevated (0.80) and clarity dropped to 0.25. I enacted an alarmed posture while seeking clarification."*

### 3. Precedent Retrieval
- `recall_precedents` successfully retrieved relevant historical episodes ordered reverse-chronologically:
  - Query for `bank`: retrieved 2 episodes (Cycle 4 *river bank* and Cycle 1 *financial bank*).
  - Query for `order`: retrieved 2 episodes (Cycle 5 *tactical sequence* and Cycle 3 *contradictory edict*).

### 4. Matched Ordinary-Memory Baseline Parity (Rule D004)
- Primary journal engine and matched ordinary structured-memory comparator achieved byte-for-byte evaluation digest parity across all episodes (`e639b9646bb3b9f9...`).
- Export payloads matched identically.

### 5. Frozen Founding Seed Invariant (Rule D001)
- The canonical 40 founding nodes in `birth.py` were verified strictly unmutated.
