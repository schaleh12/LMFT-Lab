# Local-SLM Representation Interface & Semantic Substitution — Protocol 4

2026-10-13. Fourth bounded DEVELOPMENT interface inspection following the D034 interface
breakthrough and D035 semantic adjudication findings. Maximum FOUR attempts on the identical
four development cases (`representation-01` through `04`). No retries, manual edits, or post-hoc
parameter adjustments.

## 1. Purpose and Interface Refinement

Protocol 3 achieved 100% interface admissibility (4/4) and D035 demonstrated that the
extracted contiguous context anchors provide 100% discriminative precision (0 false positives).

However, semantic adjudication identified the next scientific boundary:
- 3/4 cases produced **tautological glosses** (repeating the target lemma `order` in the explanation).
- Only 1/4 (`representation-04`) achieved **semantic substitution** (`"in the sequence of award creation"`).

Protocol 4 introduces a strict **Non-Tautological Substitution Constraint**:
1. The prompt contract explicitly instructs the model not to repeat the target lemma (or its plurals)
   in the gloss, requiring an explanatory synonym or definition (e.g. `sequence`, `magnitude`, `decree`, `purchase`).
2. The validator rejects any proposal whose gloss contains the target word (`order` / `orders`) as
   `gloss tautology: target word repeated in gloss`.
3. Deterministic Python token span resolution and schema-level `maxItems: 1` are preserved unchanged.

## 2. Frozen Inputs and Calls

1. Approved SemCor development export SHA256:
   `77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`.
2. Identical four development cases: `representation-01` through `04`.
3. Offline inference only via Qwen3-4B Q4_K_M on a single owned loopback server.
4. Maximum 4 attempts; any transport fault or contract rejection consumes its attempt.

## 3. Schema & System Prompt

### JSON Schema
- `schema_version`: enum `[1]`.
- `status`: enum `["one_reading", "insufficient_context"]`.
- `target`: object with required `start`, `end`, `quote` (copied verbatim from input).
- `readings`: array with `maxItems: 1`, containing reading objects:
  - `gloss`: string (1..240 chars, without target lemma).
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
       CRITICAL: Do NOT use the target word or its plurals in gloss. Define or substitute its meaning using other words (e.g., sequence, magnitude, decree, purchase/requisition).
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
