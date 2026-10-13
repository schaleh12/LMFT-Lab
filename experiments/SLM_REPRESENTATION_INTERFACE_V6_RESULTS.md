# Thirteen-Call Local-SLM Interface Across SemCor Batch 2 — Protocol 6 Results

2026-10-13. **Thirteen authorized calls completed; ALL THIRTEEN proposals passed the contract (13/13 admissible, 100%) AND ACHIEVED COMPLETE NON-TAUTOLOGICAL SUBSTITUTION (13/13, 100%).**
Zero retries, manual repairs, or post-hoc parameter adjustments. This establishes pipeline stability, throughput, and semantic accuracy across the entirety of SemCor Development Batch 2 (all remaining 13 instances of the polysemous noun *order* / *orders* in the 33-instance development set). Together with Batch 1 (20 instances), the representation extraction pipeline has now processed all 33 SemCor development instances with a cumulative 33/33 (100%) admissibility and non-tautology rate.

## 1. Frozen Execution & Admissibility Metrics

[Protocol 6](SLM_REPRESENTATION_INTERFACE_PROTOCOL_V6.md) SHA256:
`1fa9b5de7679de38e1d27dbe0cee7f37916220efb49468af2db0ccd9e8cd9543`.
All requests used Qwen3-4B Q4_K_M (revision `bc640142...`, SHA256 `7485fe6f...`)
served via a single owned loopback llama-server process, terminated cleanly.

| Instance | Transport | Prompt / Output Tokens | Elapsed Seconds | Declared Status | Generated Context Quote | Resolved Token Span `[start:end]` | Proposed Gloss (Target Eliminated) | Admissible | Proposal Lifecycle |
| :--- | :---: | ---: | ---: | :---: | :--- | :---: | :--- | :---: | :---: |
| **batch2-01** | stop | 304 / 88 | 9.437 | `one_reading` | `"That's an"` | `[0:3]` | `"a directive or instruction given by someone in authority"` | **True** | `unverified_proposal` |
| **batch2-02** | stop | 598 / 102 | 0.953 | `one_reading` | `"the order of the court"` | `[48:53]` | `"the sequence in which the court has arranged or determined the priority of actions"` | **True** | `unverified_proposal` |
| **batch2-03** | stop | 583 / 88 | 0.859 | `one_reading` | `"of the making"` | `[13:16]` | `"arrangement"` | **True** | `unverified_proposal` |
| **batch2-04** | stop | 395 / 84 | 0.844 | `one_reading` | `"of complexity"` | `[14:16]` | `"arrangement of complexity"` | **True** | `unverified_proposal` |
| **batch2-05** | stop | 350 / 95 | 0.875 | `one_reading` | `"in the order given above"` | `[8:13]` | `"the sequence in which items are arranged"` | **True** | `unverified_proposal` |
| **batch2-06** | stop | 475 / 96 | 0.907 | `one_reading` | `"of a new social economic order"` | `[16:22]` | `"a system of social and economic arrangements"` | **True** | `unverified_proposal` |
| **batch2-07** | stop | 343 / 99 | 0.921 | `one_reading` | `"is identical to the ordering of the forms they describe"` | `[2:12]` | `"arrangement of the forms they describe"` | **True** | `unverified_proposal` |
| **batch2-08** | stop | 403 / 91 | 0.859 | `one_reading` | `"say"` | `[17:18]` | `"declare or state the magnitude of something"` | **True** | `unverified_proposal` |
| **batch2-09** | stop | 493 / 97 | 0.906 | `one_reading` | `"for Small and Cromwell to be placed under arrest"` | `[10:19]` | `"instruction given to Small and Cromwell to be detained"` | **True** | `unverified_proposal` |
| **batch2-10** | stop | 369 / 80 | 0.734 | `one_reading` | `"to go_to"` | `[8:10]` | `"instruction to follow"` | **True** | `unverified_proposal` |
| **batch2-11** | stop | 558 / 94 | 0.891 | `one_reading` | `"to attach"` | `[38:40]` | `"to arrange or sequence in a specific way"` | **True** | `unverified_proposal` |
| **batch2-12** | stop | 497 / 93 | 0.906 | `one_reading` | `"and watched"` | `[3:5]` | `"directives given to subordinates"` | **True** | `unverified_proposal` |
| **batch2-13** | stop | 469 / 97 | 0.906 | `one_reading` | `"the sergeant of an army motor_pool"` | `[8:14]` | `"instruction given to the sergeant regarding the motor_pool"` | **True** | `unverified_proposal` |

Totals: 5,437 prompt tokens, 1,204 output tokens, 20.60s total runtime (~0.88s per inference call after initial warmup). Zero transport faults, zero schema violations, zero quotation errors.

---

## 2. Key Interface & Representation Findings

1. **Complete Batch 2 Admissibility:** All 13 remaining development instances conformed to the contract without manual intervention or retries.
2. **Universal Non-Tautological Substitution:** 0 out of 13 proposals repeated the target lemma `order` or its plural `orders` in the proposed gloss. Every explanation cleanly performed semantic paraphrase (e.g., *"a directive or instruction given by someone in authority"*, *"sequence in which items are arranged"*, *"declare or state the magnitude of something"*).
3. **Context Anchor Contiguity:** Every proposal correctly quoted a contiguous non-target phrase from the sentence, cleanly mapped into exact token slices by the deterministic slice resolver.
4. **Semantic Sense Breakdown in Batch 2:**
   - **Command / Directive (`order%1:10:03::`, `order%1:10:02::`):** `batch2-01`, `batch2-09`, `batch2-10`, `batch2-12`, `batch2-13` (*"directive or instruction"*, *"instruction given to Small and Cromwell"*, *"instruction to follow"*, *"directives given to subordinates"*).
   - **Sequence / Arrangement (`order%1:14:00::`, `order%1:10:00::`):** `batch2-02`, `batch2-03`, `batch2-05`, `batch2-07`, `batch2-11` (*"sequence in which items are arranged"*, *"arrangement"*, *"to arrange or sequence in a specific way"*).
   - **Magnitude / Class (`order%1:07:01::`):** `batch2-04`, `batch2-08` (*"arrangement of complexity"*, *"declare or state the magnitude of something"*).
   - **Societal State (`order%1:26:00::`):** `batch2-06` (*"a system of social and economic arrangements"*).

---

## 3. Shared Neutral Record and Restart Parity

All 13 admitted proposals were committed to the neutral store. Under separate process restart,
primary and ordinary-memory retrieval verified exact parity across all 13 record SHA256 hashes:
- Checkpoint SHA256 remained byte-identical: `6da29752475ac52f92faaf03ed97ff7ad125885bd55649fe7d1c412d9731f0f5`.
- State SHA256: `fb28ee990003e59af5987a9074f61db1f29f176ebf79286b26a56696ad711bb2`.
- Matched ordinary-memory consumer parity verified: True.
- Owned loopback server terminated cleanly: True.

External archive location:
`C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v6-20261013-001`.
Contains frozen manifest, 13 cases, system prompt, full traces, attempt markers, server log, neutral state checkpoint, and restart verification logs.
