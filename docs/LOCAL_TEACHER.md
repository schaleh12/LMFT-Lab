# Bounded local teacher connection

The teacher connection is implemented, with versioned developmental briefings and one unchanged lesson format.
[Preregistration](../experiments/TEACHER_PROTOCOL.md) and
[actual results](../experiments/TEACHER_RESULTS.md) distinguish communication, retained
proposals and transfer. The first real reply was rejected; no transfer was demonstrated.

## Setup and reproduce

From the repository root in PowerShell, using the existing environment:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
# First provision downloads missing assets through the existing verified cache workflow:
.\.venv\Scripts\python.exe -m lmft_lab.teacher_adapter --provision --config config/teacher_models.json --profile foundational-teacher-v1
# Verify assets without network access:
.\.venv\Scripts\python.exe -m lmft_lab.teacher_adapter --provision --offline
# Fresh output directory; actual teacher call is offline, evaluation is deterministic:
.\.venv\Scripts\python.exe experiments/run_teacher.py --output outputs/my-teacher-study
```

The harness creates three individuals, supplies registered priors/calibration through the
inbox, invokes the teacher once, replays its actual reply into the controls, halts/restarts,
and tests six fresh cases without teacher assistance. It archives all experimental inputs
before the call. At most one explicitly requested retry follows an inference failure;
a valid but rejected proposal is not retried. Failed runs and negative results are retained.

To replay archived messages with **zero inference**, use a new output directory:

```powershell
.\.venv\Scripts\python.exe experiments/replay_teacher.py --source outputs/teacher-001 --output outputs/my-teacher-replay
```

See [local-model setup](LOCAL_MODELS.md) for environment installation and NVIDIA/Windows
requirements. No new packages, frameworks, service installation or credentials are needed.

## Model and configuration

[Official Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) is a post-trained, instruction-capable
8.2B model supporting non-thinking generation. The official
[GGUF Q4_K_M](https://huggingface.co/Qwen/Qwen3-8B-GGUF/blob/7c41481f57cb95916b40956ab2f0b139b296d974/Qwen3-8B-Q4_K_M.gguf)
is 5,027,783,488 bytes (about 4.68 GiB), Apache-2.0. This is a practical larger teacher
than the existing 4B interpreter while leaving room for context and CUDA buffers on the
measured RTX 4080. Quantization/model size does not establish teaching competence.

`config/teacher_models.json` separately maps `teacher` to the 8B model; interpretation,
digestion and contemplation remain mapped to Qwen3-4B. The original local_models.json
is unchanged. Roles may be explicitly configured to share a compatible model, but this
study actually used the separate 8B teacher. Existing LocalModels manages one hidden
loopback server at a time; switching models closes the previous server. In this study
runtime mode `fixture` invokes no student inference and only the adapter starts a server.
Do not manually keep another large server resident unnecessarily.

Pinned teacher assets/settings:

- Repository: `Qwen/Qwen3-8B-GGUF`
- Revision: `7c41481f57cb95916b40956ab2f0b139b296d974`
- Filename: `Qwen3-8B-Q4_K_M.gguf`
- SHA256: `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`
- Quantization/license: Q4_K_M / Apache-2.0
- Backend: existing official Windows CUDA 12.4 llama.cpp `b11429`; archive hashes remain
  pinned in model_assets.py. Actual server fingerprint: `b11429-d81235049`.
- Context 8192, output ceiling 1024, temperature 0, seed 42, non-thinking, timeout 120s.

The observed machine had 16,376 MiB total VRAM, about 14,043 MiB free immediately before
the study, and 32,635,796 KiB total / 16,969,792 KiB free RAM. These are snapshots, not
peak inference memory measurements. The actual call took 13.14s including verification,
startup and inference; steady-state latency was not benchmarked. The 8B weight file is
larger than the 4B file, so cold load/checksum work also increases.

Assets remain outside Git in `%LOCALAPPDATA%\LMFT-Lab\cache` (or LMFT_CACHE_DIR).
Existing downloads verify pinned SHA256, publish atomically and reuse verified files.
HF_TOKEN is optional for another gated/private model; never put tokens in profiles/config
or Git. `--offline` disables asset downloads; inference uses local loopback. Offline-ready
means provisioned and callable, not guaranteed availability despite process/hardware failures.

## Profile and one-question command

The historical `foundational-teacher-v1` remains the default. Its file is
`config/teacher_profiles/foundational-teacher-v1.json`: profile ID `foundational-teacher`,
version `1`, stable boundary, current capabilities/limits, developmental guidance and reply
schema. It encourages evidence-backed reusable preferences and explicit uncertainty.
All prompt text stays in configuration; there is no speculative stage selection framework.

For an existing eligible pending teaching question:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.teacher_adapter --root outputs/my-individual --config config/teacher_models.json --profile foundational-teacher-v1 --offline
```

Runtime configuration for a new compatible individual is explicit:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-individual start --new teacher-subject --experiment teacher-lmft --mode fixture --teacher-config config/teacher_models.json --teacher-profile foundational-teacher-v1
```

In another terminal, the supervised owner must submit registered calibration observations
and an `ask_teacher` operation through the existing inbox; the reproducible harness shows
those exact messages. No eligible question means a clear error and zero calls. Ordinary
clarification requests are not automatically sent to the LLM. Supported controls are
`teacher-none` (lesson acceptance disabled) and `teacher-memory` (ordinary selection).

The adapter reads only deliberate outbox messages, chooses one pending teaching request,
and sends only its scoped context. That context contains registered calibration evidence,
current weights, supported judgment summaries and capabilities. Hidden answers, validation
outcomes, held-out evidence and internal diagnostics are excluded. While runtime is active,
use `receive` and lifecycle acknowledgments; `inspect`/`probe` require halt.

A successful structured reply is published into the existing inbox with stable message ID,
reply linkage, exchange ID, exact profile/text/hash/version, full model configuration,
request text/hash/context, raw response and backend provenance. Runtime independently
checks linkage/config/schema and records a disposition. The teacher never writes state.

## Lesson and independent validation

The only lesson fields are `route`, `weight`, `supporting_evidence`, `reason`, `uncertainty`.
Route is A, B or D; proposed weight is .25, .5 or .75. At least two distinct registered
training IDs must support that route and direction. No arbitrary nodes, graph edits,
code, facts, correction authority or protected changes are representable.

Acceptance additionally requires strictly more relevant resolutions on fixed v1/v2
validation cases without increased irrelevant requests. No-op changes fail. No held-out
outcomes are used. Reasons/uncertainty are retained as attributed prose, not interpreted
by another model or converted into confidence. Prompt guidance is not the enforcement layer.

Four off-policy calibration observations do not constitute new online selected-resolution
rewards. The existing experience-based update implementation stays unchanged; this opt-in
study retains teacher changes in a separate `lessons` ledger with before/after weights,
evidence, validation and reasons. Fresh evaluation does not update either set of weights.
Ordinary memory receives the same actual proposal and equivalent validation access.

## Failure, duplicate and compatibility behavior

One command makes at most one inference attempt. The existing lock/atomic-file primitives
journal an attempt before inference; an interrupted attempt consumes budget. Explicit
`--retry` permits one further attempt after failure, never more than two. Malformed output,
truncation, missing assets, timeout or backend failure leave a failure trace and publish
no fabricated reply. A schema-valid rejected lesson remains a negative result.

The journal saves the complete inbox message before publication. Recovery can redeliver
its stable ID without another call; existing inbox deduplication prevents another update.
A completed/disposed question triggers zero calls. A new message ID answering an already
disposed question cannot apply another lesson. First lesson disposition is terminal for
that question, including malformed or rejected content. The journal lock is nonblocking;
concurrent adapters receive a busy error rather than starting two calls.

Public provenance fields are attribution/integrity checks, not cryptographic authentication
of a human or trusted model. Independent validation supplies acceptance authority. Host
filesystem tampering and general prompt-injection resistance are not solved by this study.

No checkpoint conversion is performed. Existing source/config manifest checks intentionally
refuse restarting old individuals under changed code or profiles; use their archived
source/config to inspect/reproduce them, or create a new individual. The original real-run
snapshot and the final hardened-code replay snapshot are both retained. No persistent
seed identifiers, equations or historical records were migrated or changed.

## Bounded briefing follow-up and roadmap handoff

`foundational-teacher-v2` is the explicit clarified alternative. It preserves the stable
boundary and lesson schema, while scoped route/availability/selection descriptions come
from config/teacher_briefing.json. Choose it with adapter `--profile foundational-teacher-v2`
and matching runtime `--teacher-profile foundational-teacher-v2`. Profile/config remain
frozen per individual; inbox replies cannot select another version.

For the registered comparison only, runtime `--teacher-study beneficial` initializes
A=B=D=.5, and `--teacher-study no-change` initializes A=.25/B=.75/D=.5. These are fresh study
states using separate b1..b6 evaluation cases. Default `--teacher-study historical` preserves
the original experiment. They do not migrate or rewrite existing individuals.

The [four-call study](../experiments/TEACHER_BRIEFING_RESULTS.md) accepted one clarified
beneficial proposal and observed bounded transfer matching ordinary memory. Both briefings
appropriately retained state in the no-change situation; one explanation remained unsupported.
The unchanged independent acceptance policy remains essential.

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe experiments/run_teacher_briefing.py --output outputs/my-briefing-study
```

This harness uses four fixed offline calls and no retries. Do not extend the budget to chase
acceptance. Teacher work now hands back to [outcome evidence correction](EVIDENCE_LEARNING_HANDOFF.md).
The teacher stays available as a separate optional supervised capability; further prompt or
model work is not a prerequisite for that deterministic experiment.
