# Four-Call Local-SLM Interface & Semantic Substitution — Protocol 4 Results

2026-10-13. **Four authorized calls completed; ALL FOUR proposals passed the contract (4/4 admissible, 100%) AND ACHIEVED COMPLETE NON-TAUTOLOGICAL SUBSTITUTION (4/4, 100%).**
Zero retries, manual edits, or post-hoc parameter adjustments. This establishes both interface admissibility
and true semantic explanatory substitution without target lemma repetition.

## 1. Frozen Execution & Admissibility Metrics

[Protocol 4](SLM_REPRESENTATION_INTERFACE_PROTOCOL_V4.md) SHA256:
`4a6abf5910a5d38e8796b761b246e221947d606ce3dee1c71ae7effeb09d82aa`.
All requests used Qwen3-4B Q4_K_M (revision `bc640142...`, SHA256 `7485fe6f...`)
served via a single owned loopback llama-server process, terminated cleanly.

| Input | Transport | Prompt / Output Tokens | Elapsed Seconds | Declared Status | Generated Context Quote | Resolved Token Span `[start:end]` | Proposed Gloss (Target Word Eliminated) | Admissible | Proposal Lifecycle |
| :--- | :---: | ---: | ---: | :---: | :--- | :---: | :--- | :---: | :---: |
| **representation-01** | stop | 1074 / 93 | 9.532 | `one_reading` | `"of 3 % per_annum"` | `[19:23]` | `"a level or magnitude"` | **True** | `unverified_proposal` |
| **representation-02** | stop | 1314 / 103 | 0.906 | `one_reading` | `"in accordance with the order of the court"` | `[45:53]` | `"the sequence in which things are handled or the priority given to actions"` | **True** | `unverified_proposal` |
| **representation-03** | stop | 802 / 100 | 0.812 | `one_reading` | `"an order he expected did n't come_through"` | `[5:12]` | `"a command or instruction he had anticipated but did not receive"` | **True** | `unverified_proposal` |
| **representation-04** | stop | 1280 / 95 | 0.812 | `one_reading` | `"of the making of such awards"` | `[13:19]` | `"sequence in which the awards are created"` | **True** | `unverified_proposal` |

Totals: 4,470 prompt tokens, 391 output tokens, 12.062 seconds across generate calls;
first timing includes server startup and asset verification. Zero transport faults or timeouts.

---

## 2. Progression Across All Four Interface Protocols

1. **Protocol 1 (D032): 0/4 Admissible.**
   - Status/count mismatch on 3/4 cases (declared 1, returned 2).
   - 26/26 anchors cited only the target token (`"order"`).
   - Deep relations/conditions hierarchy caused autoregressive repetition.

2. **Protocol 2 (D033): 0/4 Admissible.**
   - Schema `maxItems: 1` 100% eliminated status/count mismatch.
   - Dedicated singular context anchor 100% eliminated target-only copying.
   - New boundary: 4/4 failed on zero-based half-open Python slice index arithmetic (`[start:end)`).

3. **Protocol 3 (D034): 4/4 Admissible (100%), but 3/4 Tautological.**
   - Model outputs context phrase as plain string; Python deterministically resolves token slice.
   - 4/4 cases admitted, but semantic adjudication (D035) revealed 3/4 glosses repeated the target word `order`.

4. **Protocol 4 (D036): 4/4 Admissible (100%) AND 4/4 Non-Tautological Substitution (100%).**
   - Explicit negative lexical constraint (*"Do NOT use the target word or its plurals in gloss"*) completely eliminated gloss tautology.
   - All 4 cases generated genuine semantic substitutions:
     - Case 01 correctly defined the magnitude sense as `"a level or magnitude"`.
     - Case 04 correctly defined the sequence sense as `"sequence in which the awards are created"`.
     - Cases 02 and 03 replaced `order` with functional descriptions (`"priority given to actions"`, `"command or instruction"`).
   - All 4 cases preserved non-target context anchors without quotation faults.

---

## 3. Shared Neutral Record and Restart Parity

All four admitted proposals were committed to the neutral store. Under an actual separate
process restart, primary and ordinary-memory retrieval verified exact parity across all four
digests:
- `representation-01`: `8f750fc4ea5960354cf611a8b56cbb4eb7dfe12fac76d46c8c6afeb952f025c7`
- `representation-02`: `9544a606c719caf13ae6204b69c7de0a64753d4b012d2094a0a8aed587a62878`
- `representation-03`: `11683beee7e2d2ccbb0b21473432f703f0c8d7c214a8febe7bd968e1671f39be`
- `representation-04`: `39452723cb40d52ed9e8dd6b45e98f48d9c40b5db7067a8520dbc83d6e01334d`

Checkpoint SHA256 remained byte-identical (`4adbea15bb3461ba749d10f0123c71c72876607a9923ffe162c9bd824d07e01b`).
State SHA256: `eecaf95b961db6377e92bf2a95cfcc4a5b509d60de3db38e0e13628dfabca1b3`.

External archive location:
`C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v4-20261013-002`.
Contains frozen manifest, cases, system prompt, full traces, attempt markers, server log,
neutral state checkpoint, and restart logs.
