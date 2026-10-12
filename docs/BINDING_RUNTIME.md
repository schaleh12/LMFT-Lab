# Supervised neutral binding runtime

The opt-in `binding-primary` and `binding-memory` modes learn operand binding within
a fixed numeric comparison family. They use the existing supervised inbox/outbox,
checkpoints and restart. This is a bounded fixture experiment, not a conversational
interface, general concept learner or demonstration of seed/fuzzy superiority.

Start a fresh individual with a trusted operator-provided private registry:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-binding-individual start --new my-binding --mode fixture --experiment binding-primary --binding-condition informative --binding-registry PATH_TO_PRIVATE_REGISTRY
```

Use `binding-memory` for the independent truth-table comparator. Conditions:
`informative`, `no-acquisition`, `noninformative`, `unavailable`, `already-supported`,
`informative-frozen`. Controls are manifest-pinned and cannot change during resume.
The reproducible [harness](../experiments/run_binding_runtime.py) constructs private
registries using the unchanged oracle; registry authoring is trusted setup, not inbox
learning. An untrusted caller cannot authorize an outcome by attaching a digest.

Messages retain the existing schema1 envelope. Content is exactly `text`, `operation`,
`record`. Text is inert. Operations:

| Operation | Record | Effect |
| --- | --- | --- |
| train | Strict registered neutral observation | Admit verified training evidence |
| select | Empty object | Close training; persist query and charge at most one request |
| reply | Strict selected observation; teacher_reply correlated to emitted request ID | Receiver verifies and admits acquisition |
| close | Empty object | Close acquisition after the selected reply, if any |
| evaluate | `{id, channels: [a,b,c]}` | Emit success/failure/abstain without changing learning state |
| barrier | Empty object | Acknowledge processed input boundary |

Evidence fields: `version: neutral-binding-1`, `id: tNNN/qNNN`,
`split: training/acquisition`, `channels`, Boolean `outcome`,
`source: registered-binding-observation-1`. Envelope source must match.
Admission channels are strict integers0..2. Prediction allows0..3; held-out outcomes
and extra fields are rejected. External proposals cannot install hypotheses.
Learning can affect predictions only through the fixed18-class family and admitted
evidence. No model inference occurs.

Use existing `submit --file`, `receive`, `stop` and halt-only `inspect`/`probe` commands.
Resume with the same start options and private registry, omitting `--new`.
An empty family abstains. Multiple survivors decide only when they agree on the
case. The explicit frozen control uses its pre-acquisition snapshot for decisions.
Evaluation changes normal queue/receipt/outbox bookkeeping, never binding evidence,
survivors, phase or budget.

Nested binding-state version is `binding-runtime-state-1`; outer checkpoint version
remains1. Source/config/registry changes fail closed. Old checkpoints require their
matching archived source: do not run the owner's existing demo under modified code.
The [report](../experiments/BINDING_RUNTIME_RESULTS.md) records the verified archive
and copied-checkpoint recovery check. No automatic migration is provided or required.

Initial integration acceptance was blocked by review for inconsistent nested controls
and request references. The [narrow fix](../experiments/BINDING_RESTART_FIX_RESULTS.md)
checks outer/manifest/nested/launch agreement and actual selection/request/reply/close
history before startup and transitions. Independent re-review accepted the correction
within trusted local finite-fixture scope. This adds consistency validation, not checkpoint authentication.

See the [frozen protocol](../experiments/BINDING_RUNTIME_PROTOCOL.md),
[results/reproduction](../experiments/BINDING_RUNTIME_RESULTS.md), and
[tests](../tests/test_binding_runtime.py). The session is closed at the accepted
checkpoint; extensions need a separately agreed decision contract.
