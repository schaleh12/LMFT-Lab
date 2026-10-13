# Local-SLM Representation Extraction — Protocol 5 (Batch 1 Scaling)

2026-10-13. Fifth bounded DEVELOPMENT interface protocol. Scales the verified
Protocol 4 non-tautological substitution contract across all 20 development instances
in `development_batch_1` from the approved SemCor development export.
Maximum 20 attempts; no retries, manual edits, or post-hoc parameter adjustments.

## 1. Purpose and Scaling Scope

Protocols 1 through 4 solved the representation interface:
- Protocol 3 solved deterministic token span resolution from surface context quotes.
- Protocol 4 solved non-tautological semantic substitution (100% target lemma elimination in glosses).
- Phase C proved that persistent context anchors achieve 100% precision on unassisted contextual disambiguation.

However, Protocols 1–4 only operated on 4 mechanically chosen instances.
Protocol 5 scales this interface across all **20 instances of `development_batch_1`** in SemCor,
spanning 7 WordNet 3.0 senses:
- `order%1:10:03::` (5 instances: authoritative command/directive)
- `order%1:26:02::` (4 instances: condition/state of readiness)
- `order%1:26:00::` (3 instances: state of peace/organization)
- `order%1:07:01::` (3 instances: degree/magnitude)
- `order%1:14:00::` (2 instances: social order/structure)
- `order%1:10:01::` (2 instances: commercial purchase order)
- `order%1:10:00::` (1 instance: judicial decree)

## 2. Frozen Inputs and Calls

1. Approved SemCor development export SHA256:
   `77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`.
2. Exact selection: All 20 rows where `stage == 'development_batch_1'`, sorted lexicographically by `example_id`.
3. Offline inference only via Qwen3-4B Q4_K_M on a single owned loopback server (llama.cpp b11429).
4. Maximum 20 attempts; any transport fault or contract rejection consumes its attempt.

## 3. Schema & System Prompt (Identical to Protocol 4)

### JSON Schema
- `schema_version`: enum `[1]`.
- `status`: enum `["one_reading", "insufficient_context"]`.
- `target`: object with required `start`, `end`, `quote` (copied verbatim from input).
- `readings`: array with `maxItems: 1`, containing reading objects:
  - `gloss`: string (1..240 chars, without target lemma `order` / `orders`).
  - `context_quote`: string (1..240 chars, exact words from sentence).
- `uncertainties`: array with `maxItems: 2`, containing strings (1..240 chars).

### System Prompt
```text
Given indexed surface tokens and a target span, output JSON conforming to the schema.
1. Copy the target span exactly into target.
2. If the sentence provides sufficient context to interpret target:
   - Set status to "one_reading".
   - In readings, provide exactly one object with:
     * gloss: an explanatory paraphrase of target's meaning in this context (1..240 chars).
       CRITICAL: Do NOT use the target word or its plurals in gloss. Define or substitute its meaning using other words (e.g., sequence, magnitude, decree, command, arrangement, purchase).
     * context_quote: an exact phrase of 2 or more words from the sentence (outside target) that informs the reading.
   - CRITICAL: context_quote must be an exact quote from the sentence. Do not quote target alone.
3. If surrounding context is insufficient to determine meaning:
   - Set status to "insufficient_context".
   - Set readings to [].
   - Provide 1..2 concise reasons in uncertainties.
Return valid JSON only. /no_think
```

## 4. Contract Admissibility Rules

A proposal is admissible iff:
1. Valid JSON matching schema version 1.
2. Target span matches supplied source target exactly.
3. Status `one_reading` contains exactly 1 reading and empty uncertainties.
4. `context_quote` resolves to a contiguous token slice containing at least one non-target token.
5. `gloss` does NOT contain the target word or its plurals (`order` / `orders`, case-insensitive).
6. Preserves neutral store commit and exact primary vs ordinary structured-memory parity under separate process restart.
