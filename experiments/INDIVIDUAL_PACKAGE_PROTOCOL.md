# Standalone Individual Packaging & Migration Protocol (Phase 3)

## 1. Research Question & Purpose
Can an active, trained LMFT individual (including its birth identity, frozen founding seed, dynamic judgment state, capacity rules, and clarification ledgers) be serialized into an atomic, standalone `.lmft.json` package that guarantees:
1. Complete fidelity across independent export and import round-trips.
2. Cryptographic SHA-256 integrity verification that rejects any payload tampering.
3. Strict enforcement of Rule D001 (frozen 40-node seed geometry) rejecting mutated founding seeds upon import.
4. Byte-for-byte state parity against a matched ordinary structured-memory baseline comparator (Rule D004).

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant. The package must store a canonical seed fingerprint computed over all 40 paths in canonical alphabetical order. Any package with a mismatched fingerprint must be rejected with `ValueError`.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against an ordinary structured-memory package comparator running an identical serialization/deserialization routine; require byte-for-byte state parity after stripping transient filesystem provenance.
- **Tamper Protection:** The package must embed an SHA-256 digest computed across all payload fields except the signature itself. Any post-export mutation to any field (e.g. cycle count, capacity rules) must fail integrity checks.
- **Zero Runtime LLM Calls:** All export, verification, and import routines must be computed deterministically offline.

## 3. Benchmark Dataset Structure
- Full trained individual state (`migratable-individual-alpha`):
  - Birth state with canonical 40-node founding seed.
  - Newborn/trained judgment state.
  - Multi-lemma capacity rules (`bank`, `order`) with empirical weights.
  - Open/resolved clarification questions.
  - Cycle and cursor pointers at 12.

## 4. Evaluation Criteria
- 100% round-trip fidelity between original state and restored state.
- Tamper detection rate: 100% on modified payload fields.
- Seed invariant rejection rate: 100% on forged or altered seed fingerprints.
- Exact byte-for-byte digest parity against ordinary memory comparator.
