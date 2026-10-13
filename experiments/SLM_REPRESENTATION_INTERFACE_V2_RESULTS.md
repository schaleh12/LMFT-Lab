# Four-call local-SLM representation interface check — protocol 2 results

2026-10-13. **Four authorized calls completed; zero proposals passed the frozen
contract (0/4 admissible).** No retries, repairs, replacement inputs or additional
calls. This is a known-development interface inspection following Protocol 2, not a
held-out semantic benchmark or a revision of the consumed 14-case linguistic evaluation.

## Frozen execution and metrics

[Protocol 2](SLM_REPRESENTATION_INTERFACE_PROTOCOL_V2.md) SHA256:
`9e83fcc100eae57d884f81f9e93746a2a01452cbd73691826391129a9d093275`.
The four cases were identical to Protocol 1 (`representation-01` through `04`).
All requests used Qwen3-4B Q4_K_M (revision `bc640142...`, SHA256 `7485fe6f...`)
served via a single owned loopback llama-server process (PID 17752), terminated
cleanly upon completion.

| Input | Transport | Prompt/output tokens | Elapsed seconds | Declared status / actual readings | Generated quote | Token slice `[start:end]` | Actual slice quotation | First contract failure |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| representation-01 | stop | 1042 / 133 | 10.750 | one_reading / 1 | `"of 3%"` | `[19:20]` | `"of"` | source quotation mismatch |
| representation-02 | stop | 1268 / 117 | 0.890 | one_reading / 1 | `"the"` | `[50:51]` | `"of"` | source quotation mismatch |
| representation-03 | stop | 782 / 111 | 0.844 | one_reading / 1 | `"order he expected"` | `[6:8]` | `"order he"` | source quotation mismatch |
| representation-04 | stop | 1228 / 120 | 0.875 | one_reading / 1 | `"of the"` | `[13:14]` | `"of"` | source quotation mismatch |

Totals: 4,320 prompt tokens, 481 output tokens, 13.359 seconds across generate calls;
first timing includes server startup and asset verification. No timeouts or transport faults.

## Scientific diagnosis and comparison with Protocol 1

The Protocol 2 candidate contract tested two primary hypotheses:

1. **Elimination of Status/Count Mismatch:**
   - **Result: 100% RESOLVED.** In Protocol 1, cases 01–03 declared `one_reading` but returned 2 readings. Under Protocol 2's grammar constraint (`maxItems: 1`), **4/4 cases returned exactly 1 reading** with `status: "one_reading"` and zero uncertainties.
2. **Elimination of Target-Only Copying:**
   - **Result: 100% RESOLVED.** In Protocol 1, all 26 anchors cited only the target token (`"order"`). In Protocol 2, under the singular `"context_anchor"` prompt and schema, **4/4 cases successfully identified surrounding context words** (`"of 3%"`, `"the"`, `"order he expected"`, `"of the"`). Zero anchors collapsed to the target alone.
3. **The New Failure Boundary — Token Slice Arithmetic:**
   - In all four cases, the model failed on `source quotation mismatch`.
   - The 4B SLM (`enable_thinking: False`) accurately extracted context words in string space, but miscalculated half-open zero-based token indices `[start, end)`:
     - In cases 01 and 04, multi-word quotes (`"of 3%"`, `"of the"`) were assigned single-token slice lengths (`[19:20]`, `[13:14]`).
     - In case 03, the 3-token quote `"order he expected"` (tokens 6, 7, 8) was assigned slice `[6:8]`, treating `end: 8` as inclusive rather than exclusive (`tokens[6:8]` evaluates to `"order he"`).
     - In case 02, the quote `"the"` was assigned `[50:51]` (which is token 50 `"of"`, off by one from token 51 `"the"`).

## Shared neutral record and restart parity

All four rejected responses were preserved as `lifecycle: rejected` records in the
neutral store. Under an actual separate process restart, primary and ordinary-memory
retrieval verified exact parity across all four digests:
- `representation-01`: `6e9ec9bf0146b405daea3c36794e6a326e8b52da8cbe57cbe48f3db17c4c4d9a`
- `representation-02`: `9a23fafd86b43b15b660a833394c5fc98a16de23830b0b3d7b871ed168a907b3`
- `representation-03`: `79b5bedf54398ad142dddcb5ec31b3c557417c3329400537dfa3d761b52825bd`
- `representation-04`: `fc589cd8e4c71d3a5789ffd476c563a88fdb5cb9acd87deba41beb77bbe3339c`
Checkpoint SHA256 remained byte-identical (`7b20af561e31bff7b4ce9d88c4a607c33938d7c4ce3c2e05fe2b5b90a8d23dbd`).

External archive location:
`C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v2-20261013-001`.
Contains frozen manifest, cases, system prompt, full traces, attempt markers, server log,
neutral state checkpoint, and restart logs.
