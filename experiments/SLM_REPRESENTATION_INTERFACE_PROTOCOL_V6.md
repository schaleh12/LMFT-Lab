# Local SLM Representation Interface — Protocol 6 (SemCor Batch 2)

**Authoritative Specification — Frozen Protocol (2026-10-13)**

## 1. Scope & Execution Boundary

Protocol 6 applies the verified Protocol 4/5 two-tier representation interface to the remaining **13 development instances of SemCor Development Batch 2** (`stage: development_batch_2`).
- Target lemma: polysemous noun *order* / *orders*.
- Model: Pinned local `Qwen3-4B-Q4_K_M.gguf` via owned loopback llama-server.
- Call limit: Exactly 13 calls; no retries, manual edits, or parameter tweaking.
- Prompt Contract:
  1. Pure JSON output complying with schema version 1.
  2. Exactly one concise reading (`status: one_reading`).
  3. Literal text quotation (`context_quote`) of contiguous non-target context.
  4. Negative lexical constraint: strictly zero occurrences of target word (`order`/`orders`) in `gloss`.
  5. Python runtime deterministically resolves contiguous token slice `[start:end]` in `tokens`.
- Baseline Requirement (Rule D004): Matched ordinary structured-memory comparator must verify identical record digests under separate process restart.
- Seed Invariant (Rule D001): 40 canonical founding nodes remain 100% frozen.
