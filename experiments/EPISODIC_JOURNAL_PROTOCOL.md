# Dual-Coded Episodic Saliency Journal Protocol (Phase 2)

## 1. Research Question & Purpose
Can the LMFT maintain an autobiographical identity through a bounded ring buffer of dual-coded experiences (combining 24-leaf continuous activations under `Truth/Fact` with natural English narrative reflections) gated by experiential salience ($\text{Salience} \ge 0.65$, $\text{Novelty} \ge 0.70$, or explicit conflict), without mutating or expanding the frozen 40-node founding seed (Rule D001)?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant. The journal operates as persistent experiential memory under `Experiential/Retention` and `Philosophical/Truth/Fact`.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator performing identical ring buffer admission, dual-coding, and precedent recall; require 100% byte-for-byte evaluation digest parity.
- **Saliency Admission Gating:**
  - Events are admitted if $\text{Salience} \ge 0.65$, or $\text{Novelty} \ge 0.70$, or $\text{is\_conflict} = \text{True}$.
  - Sub-threshold mundane events are rejected to prevent context bloat.
- **Zero Runtime LLM Calls:** All narrative reflection sentences and mathematical snapshots are synthesized deterministically offline.

## 3. Benchmark Dataset Structure (5 Interaction Episodes)
1. `sovereign_financial_action`: High salience ($0.85$), Authoritative & Chivalrous posture. Target: *bank*.
2. `mundane_ambient_observation`: Sub-threshold ambient event (salience $0.45$, novelty $0.40$). Target: *leaf*.
3. `cognitive_conflict_disruption`: Contradictory input with low clarity ($0.25$) and high arousal ($0.80$). Target: *order*.
4. `river_collocation_discovery`: High novelty ($0.85$), Communal & Reassuring posture. Target: *bank*.
5. `tactical_order_execution`: High salience ($0.78$), Methodical & Pragmatic posture. Target: *order*.

## 4. Evaluation Criteria
- Saliency gate admits 100% of high-salience, high-novelty, and conflict scenarios, and rejects 100% of mundane sub-threshold events.
- Admitted records contain dual-coded representations (24-leaf affective state + natural English narrative reflection).
- Reverse-chronological precedent recall recovers target lemmas with 100% accuracy.
- Exact byte-for-byte state digest parity against ordinary memory comparator.
