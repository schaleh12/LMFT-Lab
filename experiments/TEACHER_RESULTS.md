# First local teacher connection — results

2026-10-11. [Frozen protocol](TEACHER_PROTOCOL.md), [implementation/setup](../docs/LOCAL_TEACHER.md).
Actual run: ignored `outputs/teacher-001/`. Final-code deterministic replay:
`outputs/teacher-replay-001/`. Historical studies remain unchanged.

## Communication succeeded; transfer did not

One actual offline Qwen3-8B Q4_K_M exchange completed, with no fallback and no retry.
LMFT emitted a deliberate teaching question; the adapter passed its scoped context to the
local teacher, published the actual structured response into the inbox, and LMFT retained
its rejected disposition. No developmental weight was accepted. Fluency and retained prose
did not establish understanding or improved learning.

The selected profile was `foundational-teacher` version 1, CLI selector
`foundational-teacher-v1`. It proposed one bounded existing route preference with evidence
references and uncertainty. The real reply proposed:

```json
{
  "route": "A",
  "weight": 0.5,
  "supporting_evidence": ["train-A1", "train-A2"],
  "reason": "Route A has two available evidence entries, indicating a consistent calibration observation, which supports a reusable route preference.",
  "uncertainty": "The limited scope of available evidence may affect the reliability of the preference."
}
```

Both cited records actually reported `available: false`; their presence was not evidence
of route success. More decisively, the proposal left A at its existing .5 weight and
resolved zero of two validation cases both before and after. It failed the fixed grounded
change/strict-improvement policy. The recorded reason was
`unsupported direction or no strict validation improvement`. Prose was not treated as Fact.
No second inference was used to search for a favorable proposal; the prompt, schema and
acceptance criteria were not revised after this result.

## Actual model, assets and offline execution

The larger teacher was successfully provisioned through the existing external asset cache,
not substituted with the existing 4B model. Official
[Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) supports instruction following and non-thinking
operation. The official [Q4_K_M GGUF](https://huggingface.co/Qwen/Qwen3-8B-GGUF/blob/7c41481f57cb95916b40956ab2f0b139b296d974/Qwen3-8B-Q4_K_M.gguf)
uses Apache-2.0 and occupies 5,027,783,488 bytes. Its larger capacity did not guarantee a
useful lesson in this run.

- Repository/revision: `Qwen/Qwen3-8B-GGUF` / `7c41481f57cb95916b40956ab2f0b139b296d974`.
- File/hash: `Qwen3-8B-Q4_K_M.gguf` /
  `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`.
- Backend: existing llama.cpp Windows CUDA 12.4 b11429; actual fingerprint b11429-d81235049.
- Settings: 8192 context, 1024 output ceiling, temperature 0, seed 42, non-thinking,
  120-second timeout. Exact configuration and backend archive hashes are in the exchange.
- Hardware snapshot: RTX 4080, 16,376 MiB VRAM / 14,043 MiB free, driver 610.88;
  RAM 32,635,796 KiB total / 16,969,792 KiB free. No peak memory claim.
- One actual call, 13.141 seconds end-to-end including cached asset verification/startup.
  Backend reported 745 prompt tokens, 82 completion tokens, 114.601ms prompt processing
  and 766.536ms generation. Those backend timings exclude most startup overhead.
- Offline mode verified cached assets and used loopback inference; no model downloads were
  needed during the call. No student model calls and no simultaneous student server.

## Teacher-disabled fresh cases

All three conditions began with A=B=D=.5, the same eight unchanged outcome priors and four
registered route-calibration records. All received the same actual teacher reply, identical
training evidence and equivalent validation access. Only the LMFT adapter performed
inference; controls replayed that attributed exchange. They did not generate new replies.

| Condition | Accepted lessons | Resolved investigations | Correct / decided | Abstentions | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: |
| LMFT after exchange | 0 | 1 | 1 / 1 | 5 | 16.7% |
| LMFT without lesson acceptance | 0 | 1 | 1 / 1 | 5 | 16.7% |
| Ordinary structured memory | 0 | 1 | 1 / 1 | 5 | 16.7% |

Each made five relevant verification requests: one resolved, four inconclusive, zero
irrelevant requests. Inconclusive verification costs are reported separately from irrelevant
requests; four calls failed to supply useful condition evidence. Accuracy was 100% on a
single decided case, not evidence of broad reliability.

All selected A for e1..e5 and no route for e6. A was unavailable in e1..e4, so all abstained.
The scope-reversal e5 made A available and yielded the one correct success prediction.
e6 lacked independent conflict and abstained without verification. The e3 held-out failure
was never predicted because the relevant condition remained unavailable. No teacher-assisted
fresh answers or outcome access influenced acceptance.

There was no behavioral change attributable to a lesson, because none was accepted.
The unchanged route tie-break and existing conditional judgment caused these behaviors.
Fuzzy propagation provided no measured advantage over ordinary memory. The lesson-disabled
control was equivalent here; its ability to refuse an otherwise valid lesson was tested
with mocks, not exercised by the real rejected proposal.

## Persistence and integrity

The actual process study passed **40/40 checks**, including exact restart state, retained
exchange/rejection, unchanged counters/seed, duplicate handling and post-restart behavior.
All three individuals halted. Runtime exposed only deliberate outbox/lifecycle information;
full state inspections occurred after halt. The adapter itself read only the outbox.

Repeated adapter invocation made zero additional calls. Exact and new-ID lesson redelivery
left one disposition, unchanged weights and no experience updates. The exchange ledger and
profile/request/model/raw-response provenance persisted through restart. Accepted state was
exercised by mocked tests only; this real run retained a rejection.

The final suite passed **319 tests**, including 33 teacher-specific mocked checks. After the
actual run, adversarial response-envelope tests found four non-object response-choice forms
that could raise AttributeError. Final code rejects them cleanly and uses type-exact profile,
configuration and request comparisons. These were input-hardening fixes, not prompt, lesson
or evaluation changes. The original evaluated source remains archived. A separate final-code
process replay used the preserved actual inbox messages with **zero inference** and passed
**9/9 checks**, reproducing identical judgment, questions and birth state across all conditions.
The extra tests also cover malformed generated JSON, timeouts, explicit retries and failures
without fabricated inbox replies. An earlier unit-test comparison was normalized for JSON's
tuple-to-list serialization; no storage behavior or experiment criterion was changed.

## Costs

Evaluation costs below exclude the teacher call and include only teacher-disabled fresh-case
processing. Wall time includes queue/checkpoint/halt overhead. These are single-run observations.

| Measure | LMFT | Lesson disabled | Ordinary memory |
| --- | ---: | ---: | ---: |
| Evaluation core processing ms | 50.918 | 53.039 | 12.697 |
| Evaluation wall seconds | 1.434 | 1.444 | 1.305 |
| Final checkpoint bytes | 382,051 | 382,051 | 109,776 |
| Final individual-directory bytes | 460,927 | 428,127 | 155,852 |
| Fresh evaluation LLM calls | 0 | 0 | 0 |

Each final checkpoint retained four calibrations, eight outcome priors, six cases, five
verification records, one rejected lesson, zero experience updates, 28 receipts, 27 outbox
messages and six question records (one teaching plus five verification). LMFT conditions
also retained five propagation diagnostics; memory retained none. The real-calling condition
additionally stored the adapter journal, explaining some directory-size differences.

Duplicate deliveries plus a barrier increased checkpoint size by 13,260 bytes per condition,
with three receipts/two outbox acknowledgments and no extra lesson. Full attributed input
retention still costs storage. No consolidation was introduced. Raw per-stage counters and
costs are in results.json, and duplicate outputs were not counted as new teacher exchanges.

## Limits and smallest next step

This is one model, one profile and one attempted lesson. It establishes an inspectable local
teacher connection with independent rejection, not successful teaching, reasoning transfer
or fuzzy superiority. Calibration, validation and fresh cases are authored synthetic evidence.
The lesson format is limited to one existing route weight; no new concepts, constitutional
changes, outcome corrections or autonomous loop were implemented.

Model/profile provenance is not human authentication. Anyone with local file-write access
can tamper with inputs; independent scope/evidence/validation checks still determine
acceptance. The frozen-source restart policy is unchanged: historical checkpoints require
their original archived code/config, and final-code replays use new individuals.

The smallest justified next step is a preregistered profile-comprehension experiment that
explicitly distinguishes a recorded observation from a successful route measurement, then
uses fresh transfer cases. Preserve this v1 failure and the same independent acceptance
standard. Do not assume a prompt adjustment will produce learning.

## Archive references

Original archive: `outputs/teacher-001/archive/` and archive-manifest.json, plus exact
journal/request/response, inbox messages, halted checkpoints, hardware and results.
Final hardened-code replay archive: `outputs/teacher-replay-001/archive/` with its own hashes.
Both archives verify; protected core/experience/correction modules match the prior study.

- Profile SHA256: `0f1f5e0f593812af793b17047a1c2d7083b0b86b7681a19b6924e40a93497a11`.
- Protocol SHA256: `f5495f7375c49f81d730c7b1938b20bf01a6e30769c3409ff082fe9b1c0b246e`.
- Teacher configuration SHA256: `a19a5f32f657cd1815538d0a16c1ce74c1f586bb9ab4a7e6f0bf728fef8e5e29`.
