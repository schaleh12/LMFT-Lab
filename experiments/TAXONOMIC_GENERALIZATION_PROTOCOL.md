# Taxonomic Hypernym Generalization Protocol (Phase 4)

## 1. Research Question & Purpose
Can discrete WordNet sense keys (e.g. fine-grained polysemy labels for *bank* and *order*) be mapped deterministically to higher-level ontological categories via hypernym path traversal, and propagate principled modulation into canonical leaf dials across the 4 canonical founding branches without mutating or expanding the frozen 40-node founding seed (Rule D001)?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant. Hypernym categories do NOT create new seed nodes; they modulate continuous leaf dial activations within the existing 24 canonical leaves.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator performing the identical taxonomic hypernym traversal and dial modulation; require 100% byte-for-byte evaluation digest parity.
- **Continuous Dial Boundedness:** All modulated canonical leaf activations must be strictly bounded within $[0.0, 1.0]$.
- **Graceful Unregistered Handling:** Any unanchored or unregistered sense key must yield `found = False`, apply zero affinities, and preserve base dials without raising unhandled exceptions.
- **Zero Runtime LLM Calls:** All hypernym path resolutions and affinity propagations must be computed deterministically offline.

## 3. Benchmark Dataset Structure (12 Instances)
- 3 senses of *bank*:
  - `bank%1:14:00::` (financial institution $\rightarrow$ `organization`)
  - `bank%1:17:01::` (river bank $\rightarrow$ `geological_formation`)
  - `bank%1:14:01::` (reserve repository $\rightarrow$ `facility_artifact`)
- 8 senses of *order*:
  - `order%1:10:00::` (judicial decree $\rightarrow$ `legal_instrument`)
  - `order%1:10:01::` (commercial purchase $\rightarrow$ `commercial_document`)
  - `order%1:10:02::` (sequence succession $\rightarrow$ `sequence_structure`)
  - `order%1:10:03::` (authoritative command $\rightarrow$ `authoritative_act`)
  - `order%1:14:00::` (sequence ordering $\rightarrow$ `sorting_act`)
  - `order%1:07:01::` (degree magnitude $\rightarrow$ `quantitative_magnitude`)
  - `order%1:26:00::` (social condition $\rightarrow$ `social_condition`)
  - `order%1:26:02::` (systematic arrangement $\rightarrow$ `systemic_arrangement`)
- 1 unregistered out-of-domain control instance (`unregistered%1:00:00::`).

## 4. Evaluation Criteria
- 100% successful hypernym path resolution up to root (`entity`) for all 11 registered senses.
- Identification of 11 unique primary categories.
- 100% adherence to $[0.0, 1.0]$ dial bounds across 33 total leaf modulations.
- 100% honest abstention/preservation on unregistered control sense.
- Exact byte-for-byte evaluation digest parity against the ordinary-memory comparator.
