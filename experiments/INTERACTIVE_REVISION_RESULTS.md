# Interactive runtime: mechanical and actual-model results

Recorded 2026-10-11 UTC, Windows / Python 3.12.3, existing RTX 4080 backend.
Protocol: [frozen fixture v1](INTERACTIVE_REVISION_PROTOCOL.md).
Commands: [supervised runtime guide](../docs/INTERACTIVE_RUNTIME.md).

## Mechanical result — authored/mock proposals

Final run: `outputs/interactive-mechanical-003/result.json`, 4.453 seconds.
The harness launched real separate Python runtime processes; inference was explicitly
mocked. Criteria and fixture were recorded before implementation/evaluation.

| Check | Observed result |
| --- | --- |
| Initial read-only probe | score 0, undetermined |
| Observation without evidence | response + clarification through outbox |
| Linked teacher reply with sample-a | accepted, score 1/3, support |
| Graceful halt and actual process restart | exact original measurement, attribution, reason and revision recovered |
| Exact duplicate delivery | duplicate receipt; no new inference, evidence or outgoing message |
| New message ID with same sample | recorded rejection; score unchanged |
| Uninterrupted comparison | learned judgment/evidence/revisions exactly equal |
| Learning-disabled control | score 0, eligible evidence rejected under control |
| Sample-b instead of sample-a | score -1/3, oppose |
| Sample-b after sample-a | score 0; both support and contrary evidence retained |
| Live internal inspection | refused while runtime lock held |

Full suite: **179 tests passed** (159 preexisting, 20 new test cases). New checks
include malformed and conflicting messages, unauthorized reply references, model
failure, single-writer locking, idle invariance, read-only probe, evidence ordering
across restart, and interrupted writes. Fault injection before/after atomic checkpoint
replacement recovered one committed learning/output result. Unpublished partial
inbox/checkpoint files were ignored. These are representative software interruptions,
not destructive power-loss or cloud-sync testing.

## Actual local-SLM smoke — separate result

Final run: `outputs/interactive-local-002/result.json`, 25.438 seconds.
Qwen3-4B Q4_K_M, pinned revision/checksum from `config/local_models.json`, official
llama.cpp b11429 CUDA backend, offline cached assets. Two inputs completed all six
validated role calls. Both post-halt diagnostics recorded the **same model-server
PID**, demonstrating reuse across cycles. The runtime emitted three authored outbox
messages: two responses and one clarification. No eligible evidence was supplied,
so no model-generated claim revised the judgment.

| Call | Role | Seconds (includes startup when applicable) |
| --- | --- | ---: |
| 1 | interpretation | 10.782 |
| 2 | digestion | 2.875 |
| 3 | contemplation | 3.000 |
| 4 | interpretation | 2.500 |
| 5 | digestion | 2.703 |
| 6 | contemplation | 2.844 |

This demonstrates real inference and communication plumbing, not correctness of the
model's interpretations or semantic learning. Outgoing wording is authored; exact
model wording was not an acceptance criterion.

## Preservation and limits

Both final run directories retain complete checkpoints, inboxes, outbox records,
model prompts/responses and results under ignored `outputs/`. Their `source_snapshot/`
folders retain the executed runtime modules, test file, model config, protocol and
harness. Runtime source-map SHA256 (sorted JSON filename-to-hash mapping):
`fb7da118633490cce94c6698c7b36ee5068c7e8c305beeafe61a50858c51abc1`.
The model source/config hashes are also embedded in each checkpoint and result.
Local output archives are not in Git; back up these halted directories separately.
This tracked report preserves the selected findings without publishing raw runtime data.

Earlier successful runs remain intact. A deterministic ordering fix prompted
`*-002` runs; the mechanical `*-003` run also verifies automatic pre-run source
archiving in the harness. Acceptance criteria were unchanged. Development
tests initially exposed a Windows lock initialization issue and JSON tuple/list
comparison differences, both resolved before the reported final evaluation.

The fixture is intentionally equivalent to a small structured evidence counter.
It does **not** establish that fuzzy propagation improves memory or reasoning,
validate general truth assessment, implement node-baseline learning, or demonstrate
consciousness, independent goals, endogenous contemplation or a Codex bridge.
The broader [Experiment 001](EXPERIMENT_001_PERSISTENT_REVISION.md) remains a proposed
study beyond this narrow mechanical subset. Next: define a second grounded evidence
fixture and matched ordinary-memory/propagation-disabled comparisons before making
claims about the benefit of the conceptual geometry.
