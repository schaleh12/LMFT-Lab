# Four-call local-SLM representation interface check — protocol 3 results

2026-10-13. **Four authorized calls completed; ALL FOUR proposals passed the frozen
contract (4/4 admissible).** First successful development interface admission.
No retries, manual edits, or post-hoc parameter adjustments. This is a known-development
interface inspection under Protocol 3, establishing interface admissibility.
Semantic adjudication of interpretations remains a separate step.

## Frozen execution and metrics

[Protocol 3](SLM_REPRESENTATION_INTERFACE_PROTOCOL_V3.md) SHA256:
`41fb608de7a99e1673e9b54ac597398a3ee6edfe4ebc7e254a70d8eb79ac77e8`.
The four cases were identical to Protocols 1 and 2 (`representation-01` through `04`).
All requests used Qwen3-4B Q4_K_M (revision `bc640142...`, SHA256 `7485fe6f...`)
served via a single owned loopback llama-server process (PID 38504), terminated cleanly.

| Input | Transport | Prompt/output tokens | Elapsed seconds | Declared status | Generated context quote | Resolved token span `[start:end]` | Proposed gloss | Admissible | Proposal lifecycle |
| --- | --- | ---: | ---: | --- | --- | --- | --- | :---: | --- |
| representation-01 | stop | 1029 / 118 | 9.031 | one_reading | `"on the order of 3 % per_annum"` | `[16:23]` | `"When increases are on the order of 3% per annum, public indignation and resistance to wage price increases is obviously much less."` | **True** | unverified_proposal |
| representation-02 | stop | 1269 / 105 | 0.844 | one_reading | `"in accordance with the order of the court"` | `[46:53]` | `"Payment must be made to the receiver or trustee according to the court's order."` | **True** | unverified_proposal |
| representation-03 | stop | 757 / 97 | 0.750 | one_reading | `"an order he expected did n't come_through"` | `[5:12]` | `"an order he expected did not come through"` | **True** | unverified_proposal |
| representation-04 | stop | 1235 / 97 | 0.750 | one_reading | `"in the order of the making of such awards"` | `[10:19]` | `"in the sequence of award creation"` | **True** | unverified_proposal |

Totals: 4,290 prompt tokens, 417 output tokens, 11.375 seconds across generate calls;
first timing includes server startup and asset verification. Zero transport faults or timeouts.

## Progression across development checks

1. **Protocol 1 (D032): 0/4 Admissible.**
   - Status/count mismatch on 3/4 cases (declared 1, returned 2).
   - 26/26 anchors cited only the target token (`"order"`).
   - Deep relations/conditions hierarchy caused autoregressive repetition.
2. **Protocol 2 (D033): 0/4 Admissible.**
   - Schema `maxItems: 1` 100% eliminated status/count mismatch.
   - Dedicated singular context anchor 100% eliminated target-only copying.
   - New boundary: 4/4 failed on zero-based half-open Python slice index arithmetic (`[start:end)`).
3. **Protocol 3 (D034): 4/4 ADMISSIBLE (100%).**
   - Model outputs context phrase as plain string; Python deterministically resolves token slice.
   - All four cases extracted rich, distinct target-relative contextual phrases outside the target span.
   - Canonical `context_anchor` `{start, end, quote}` successfully reconstructed for all cases.
   - All four records admitted to the neutral store as `lifecycle: unverified_proposal`.

## Shared neutral record and restart parity

All four admitted proposals were committed to the neutral store. Under an actual separate
process restart, primary and ordinary-memory retrieval verified exact parity across all four
digests:
- `representation-01`: `c7c99d43e1a3b0899d239a9000937bfc04bd7cbb7ed6a56ae8a20e7880e4d5d4`
- `representation-02`: `e788e8ad1b6ba8de09177a20b0d794f06715c522cc92da251097bdf642a85fb6`
- `representation-03`: `fab7bcea9e3ada04cf576f46e8a5e084cf32c2b94f6b48a1dbed1b18d4774b4d`
- `representation-04`: `6af9837efd533bc49ea91395b98866b67a76e3666109b5088fd7eb61b192c1ef`
Checkpoint SHA256 remained byte-identical (`fddbfbb9a5713850d405be7eacc8e301ce56964bcdb43da320fdf77fea2b1b00`).

External archive location:
`C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v3-20261013-001`.
Contains frozen manifest, cases, system prompt, full traces, attempt markers, server log,
neutral state checkpoint, and restart logs.
