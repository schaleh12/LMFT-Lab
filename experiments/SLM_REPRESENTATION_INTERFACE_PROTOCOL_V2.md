# Local-SLM representation interface check — protocol 2 (context anchor and grammar-enforced count)

2026-10-13. Second bounded DEVELOPMENT interface inspection following the D032
negative result (0/4 admissible). Maximum FOUR attempts, on the identical four
development cases from protocol 1. No retries, prompt tweaks, or post-hoc
relaxations. No held-out efficacy claim; the consumed 14-case evaluation is neither
input nor tuning material here.

## Purpose and smallest remaining gap

Protocol 1 demonstrated that the 4B local SLM stopped normally and generated valid
JSON, but failed contract admissibility due to two structural interface issues:
1. Status/count mismatch (`one_reading` with 2 returned readings) caused by
   schema-grammar decoupling permitting `maxItems: 2` under a plural prompt.
2. Target-only anchors (0/4 non-target context anchors; 26/26 target-only) caused by
   name collision between `target` and `anchors`, plus multi-slice token math overload.

Protocol 2 tests whether pruning recursive relations/conditions, enforcing `maxItems: 1`
in the JSON schema grammar, and replacing the generic `anchors` array with a singular,
disambiguated `context_anchor` produces admissible context representations.
Semantic adjudication remains an independent gap after interface admissibility.

## Frozen inputs and calls

1. Use the approved SemCor noun development export SHA256:
   `77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`.
2. Reuse the identical four mechanically selected development cases from Protocol 1:
   - `representation-01`
   - `representation-02`
   - `representation-03`
   - `representation-04`
3. Request message contains ONLY:
   - Indexed original surface tokens (`tokens`: list of strings).
   - Target token span and quotation (`target`: `{start, end, quote}`).
   - Compound surface tokens remain single indexed tokens.
   - Zero gold sense keys, document IDs, lemma labels, or prior evaluation cues.
4. Offline inference only via `LocalModels.generate('interpretation', request, ..., validator)`:
   - Model: Qwen3-4B Q4_K_M, revision `bc640142c66e1fdd12af0bd68f40445458f3869b`, SHA256
     `7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5`.
   - Backend: llama.cpp b11429/CUDA12.4; context 8192, output 1024, temperature 0, seed 42, timeout 120s.
   - Verify model, backend archives, and extracted files before execution.
   - Exactly ONE owned local server process reused across the 4 attempts, terminated in `finally`.
   - Max 4 attempts: any rejection, transport fault, or invalid output consumes the attempt and halts without retry.

## Candidate schema and prompt contract

### JSON Schema
Constrain generation strictly via grammar sampling:
- `schema_version`: integer enum `[1]`.
- `status`: string enum `["one_reading", "insufficient_context"]`.
- `target`: object with required `start` (int), `end` (int), `quote` (string).
- `readings`: array with `maxItems: 1`, containing reading objects:
  - `gloss`: string (1..240 chars).
  - `context_anchor`: object with required `start` (int), `end` (int), `quote` (string).
- `uncertainties`: array with `maxItems: 2`, containing strings (1..240 chars).
- `additionalProperties: False` across all object definitions.

### System Prompt
```text
Given indexed surface tokens and a target span, output JSON conforming to the schema.
1. Copy the target span exactly into target.
2. If the sentence provides sufficient context to interpret target:
   - Set status to "one_reading".
   - In readings, provide exactly one object with:
     * gloss: a concise target-relative reading (1..240 chars).
     * context_anchor: a token span (start, end, quote) identifying surrounding words that inform the reading.
   - CRITICAL: context_anchor must include tokens outside the target. Never set context_anchor equal to target.
3. If surrounding context is insufficient to determine meaning:
   - Set status to "insufficient_context".
   - Set readings to [].
   - Provide 1..2 concise reasons in uncertainties.
Token spans are zero-based (start inclusive, end exclusive). quote must be the exact space-joined tokens. /no_think
```

## Validation and admissibility rules

The validator evaluates raw output against strict structural and evidence rules:
1. **Schema Integrity:** Exact schema match, parseable JSON, no extra/missing keys, correct versions.
2. **Status/Count Invariant:**
   - If `status == "one_reading"`, `len(readings) == 1` and `len(uncertainties) == 0`.
   - If `status == "insufficient_context"`, `len(readings) == 0` and `1 <= len(uncertainties) <= 2`.
3. **Target Invariant:** `target` must match the input target start, end, and space-joined quotation exactly.
4. **Context Anchor Invariant:**
   - Indices must be valid zero-based indices into `tokens` (`0 <= start < end <= len(tokens)`).
   - `quote` must match `tokens[start:end]` joined by single space.
   - Non-target presence: `set(range(start, end)) - set(range(target_start, target_end))` must NOT be empty. An anchor that only covers target tokens fails immediately.
5. **No Automatic Repair:** Malformed JSON, count violations, out-of-bounds indices, or target-only anchors fail admissibility closed. Rejected responses are recorded with their raw failure message.

## Storage, parity, and governance

1. **Neutral Store Access (D004):** Admitted or rejected proposals are stored in the neutral format. Both primary and ordinary-memory consumers access records via identical read-only retrieval contracts. Parity and nonmutation must hold across process restart.
2. **Frozen Seed Invariant (D001):** The 40 canonical founding nodes remain completely untouched. No proposal can install nodes, relations, or numeric weights into the tree.
3. **Preservation of Prior Evidence (D012):** The D032 negative results and protocol 1 files remain historical evidence and will not be overwritten. Outputs for this run go to a new archive: `outputs/slm-representation-interface-v2-20261013-001/`.
4. **External Raw Data:** Prompts, responses, and traces stay in a separate nonpublished child under `C:\Users\schal\AppData\Local\LMFT-Lab\research-archives`.

## Stop Condition
Execution stops immediately upon completion of the 4 attempts (or earlier if a transport/server fault occurs). A detailed results report (`SLM_REPRESENTATION_INTERFACE_V2_RESULTS.md`) and diagnostic log must be prepared for parent review. No subsequent experiment or code modification is authorized.
