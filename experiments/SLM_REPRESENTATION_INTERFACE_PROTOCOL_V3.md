# Local-SLM representation interface check — protocol 3 (deterministic context span resolution)

2026-10-13. Third bounded DEVELOPMENT interface inspection following the D033
findings. Maximum FOUR attempts on the identical four development cases.
No retries, manual edits, or post-hoc parameter adjustments.

## Purpose and interface refinement

Protocol 2 confirmed two major hypotheses:
1. Schema-level `maxItems: 1` 100% eliminated status/reading count mismatches.
2. The dedicated context field 100% eliminated target-only copying (all models
   extracted phrases outside the target).

However, 4/4 cases were rejected on `source quotation mismatch` because the 4B SLM
miscalculated zero-based half-open Python slice indices (`[start, end)`), despite
extracting the correct text phrases (e.g. `"order he expected"`, `"of 3%"`).

Protocol 3 eliminates token-slice arithmetic from the model's responsibility:
- The model outputs `context_quote` as a plain string snippet from the sentence.
- Python deterministically resolves the exact token slice `(start, end)` in `tokens`.
- Python verifies that the resolved span contains non-target context tokens.
- The resolved canonical anchor `{"start": start, "end": end, "quote": quote}` is
  persisted in the neutral store, preserving identical downstream schema and
  matched-memory parity.

## Frozen inputs and calls

1. Use approved SemCor development export SHA256:
   `77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`.
2. Reuse the identical four development cases: `representation-01` through `04`.
3. Offline inference only via Qwen3-4B Q4_K_M on a single owned loopback server.
4. Maximum 4 attempts; any transport fault or rejection consumes its attempt.

## Candidate schema and prompt

### JSON Schema
- `schema_version`: enum `[1]`.
- `status`: enum `["one_reading", "insufficient_context"]`.
- `target`: object with required `start`, `end`, `quote` (copied verbatim from input).
- `readings`: array with `maxItems: 1`, containing reading objects:
  - `gloss`: string (1..240 chars).
  - `context_quote`: string (1..240 chars, exact words from sentence).
- `uncertainties`: array with `maxItems: 2`, containing strings (1..240 chars).

### System Prompt
```text
Given indexed surface tokens and a target span, output JSON conforming to the schema.
1. Copy the target span exactly into target.
2. If the sentence provides sufficient context to interpret target:
   - Set status to "one_reading".
   - In readings, provide exactly one object with:
     * gloss: a concise target-relative reading (1..240 chars).
     * context_quote: an exact phrase of 2 or more words from the sentence (outside target) that informs the reading.
   - CRITICAL: context_quote must be an exact quote from the sentence. Do not quote target alone or generic stop words.
3. If surrounding context is insufficient to determine meaning:
   - Set status to "insufficient_context".
   - Set readings to [].
   - Provide 1..2 concise reasons in uncertainties.
Return valid JSON only. /no_think
```

## Validation rules

1. Parse JSON strictly.
2. Target must match input target exactly.
3. If `one_reading`:
   - `len(readings) == 1` and `len(uncertainties) == 0`.
   - `context_quote` must resolve to an exact contiguous slice `tokens[start:end]`.
   - The resolved slice must contain at least one token outside the target span.
   - Canonical `context_anchor` is constructed from the resolved span.
4. If `insufficient_context`:
   - `len(readings) == 0` and `1 <= len(uncertainties) <= 2`.
5. Neutral store records and process-restart parity remain strictly checked.
