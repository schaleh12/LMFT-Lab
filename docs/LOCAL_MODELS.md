# Local models: Windows / RTX 4080

## Implemented scope

This is a bounded, proposal-only processing path, not an autonomous agent or the
persistent-revision experiment. It runs three configured roles in sequence:

1. Linguistic interpretation proposes relevance memberships for canonical seed nodes.
2. The existing deterministic core computes temporary activation and bounded propagation.
3. Experience digestion receives the interpretation and activation values.
4. Contemplation support critiques the interpretation and proposes questions/judgments.

Roles can share one model (the default), or point to different pinned models.
Only one server/model is resident at a time. Sharing reuses the loaded model;
switching unloads the prior process. Separate roles are not independent witnesses.

The seed, numerical update equations, legacy migration, and existing developer
activation defaults are unchanged. Digestion/contemplation output is recorded as
a proposal, never committed as a belief, confidence update, or constitutional edit.
There is no implemented judgment-revision engine to call yet. Its future acceptance
path must retain evidence/reasons and explicit policies. JSON trace files are
diagnostic records, not restored cognitive state or a transactional event store.

## Model and backend choice

The initial model is the official
[Qwen3-4B-GGUF](https://huggingface.co/Qwen/Qwen3-4B-GGUF) Q4_K_M file:
4 billion parameters, approximately 2.50 GB on disk (2.33 GiB), Apache-2.0.
It offers instruction-following and non-thinking operation suitable for short
interpretation tasks. It is not a reliable factual authority; quantization,
small model size, and prompt sensitivity can affect judgments.

The backend is official [llama.cpp](https://github.com/ggml-org/llama.cpp/releases/tag/b11429)
Windows x64 CUDA 12.4, pinned to b11429. CUDA DLLs and binaries are downloaded
from the official release and checksum-verified. No CUDA toolkit/compiler,
PyTorch, Hugging Face Python library, or new Python framework is required.
Use a compatible NVIDIA driver and Windows x64; other platforms are not supported
by this bootstrap. If Windows reports a missing Visual C++ runtime, install
Microsoft's official x64 Visual C++ Redistributable.

An RTX 4080 has 16 GB VRAM; this machine reported 16,376 MiB, with about 1.7 GiB
already occupied at inspection. We request all model layers on GPU and an 8,192
token context. Weight size is not total VRAM use: KV cache, scratch buffers,
CUDA, and other apps need additional memory. This leaves more headroom than
loading a large model. Non-thinking output, a 1,024-token ceiling, and a single
shared process reduce latency. Cold startup includes download, checksum, and load
time. Consult the smoke-run report for measured rather than estimated latency.

## Exact setup and run commands

Run from the renamed LMFT-Lab repository root in PowerShell:

```powershell
# Only if the environment does not exist:
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m lmft_lab --config config/local_models.json --event-id local-001 --observation "I found a mistake in my explanation and corrected it after checking the original measurement." --trace outputs/local-001.json
```

The first call downloads the pinned GGUF (~2.50 GB) and two backend archives
(~656 MB combined). Allow additional disk space for extracted binaries. A hidden
llama-server binds only to 127.0.0.1 on a dynamically selected port, with a
per-process API key. The CLI stops it on completion or failure; no service is
installed. A forced kill of the parent process may require manually stopping its
orphaned llama-server process.

Run again with a new trace filename to reuse the cache without any downloads:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m lmft_lab --offline --event-id local-002 --observation "I found a mistake in my explanation and corrected it after checking the original measurement." --trace outputs/local-002.json
```

`--offline` or `HF_HUB_OFFLINE=1` disables asset downloads. Loopback inference
still works. If an asset is missing or corrupted, fail clearly instead of
fetching a substitute. Cached content is checksum-verified, including offline.
Offline runs do not consult Hugging Face or GitHub.

Default cache: `%LOCALAPPDATA%\LMFT-Lab\cache`, outside the repository.
Set `LMFT_CACHE_DIR` to a dedicated cache directory if needed. Avoid concurrent
first-time backend installation into the same cache; this small implementation
does not provide cross-process installation locking. Interrupted downloads use
temporary files and do not become valid cache entries; rerun to retry from the
beginning. Corrupted completed assets fail verification; move the reported asset
aside and rerun online to replace it. Never move or erase historical experiment
results as part of cache repair.

## Reproducibility and authentication

`config/local_models.json` pins the HF repository, full commit SHA, single GGUF
filename, and SHA256. Branch names such as `main` are rejected. The initial pin is:

- Repository: `Qwen/Qwen3-4B-GGUF`
- Revision: `bc640142c66e1fdd12af0bd68f40445458f3869b`
- File: `Qwen3-4B-Q4_K_M.gguf`
- SHA256: `7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5`

Changing models is an explicit config edit, including a reviewed new revision
and checksum. Use single-file GGUF models supported by this llama.cpp build;
multimodal, sharded, or remotely executable model code is not supported.
Backend release URLs and archive checksums are pinned in `model_assets.py`.

The default public model needs no token. For gated/private models, provide
`HF_TOKEN` through your process environment or credential manager after obtaining
repository access. Never put a token in config, a command committed to Git,
a trace, or source. Tokens are sent only to the HF download request, stripped
on redirects, and removed from the model server's environment. The adapter does
not read Hugging Face CLI credential files. No login or token creation is needed
for the default demo.

Git ignores model weights, local cache/model directories, partial downloads,
and .env files. Keep credentials out of Git even if using another filename.
The existing dependency pins are untouched; DEAP remains a historical installed
dependency, not part of this integration.

## Validation and provenance

The backend receives a JSON schema. LMFT independently rejects malformed JSON,
duplicate keys, unknown fields/IDs, duplicate memberships, booleans used as numbers,
nonfinite/out-of-range relevance, excessive lists, or invented/missing quotations.
Every membership includes a reason and an exact observation excerpt. This checks
attribution only; it does not establish the excerpt's truth or the model's reasoning.

Proposals have summary, memberships, uncertainties, questions, and optional
proposed_judgment. They have no mutation/code/authorization field. Input text and
previous model outputs are untrusted even when they claim authority. This restricted
interface prevents this adapter from writing constitutional state; it does not
claim general prompt-injection resistance or semantic correctness.

Each trace stores event and individual identity, seed/state versions, state hash,
observation, each role's model/revision/hash, backend pin, prompt/schema and
generation settings, exact request, raw response, validation outcome, duration,
proposed reasons/quotes, activation calculations, and an explicit empty
persistent_changes list. Failure traces preserve completed calls plus the failed
call where available. Output truncation, timeouts, backend failure, and invalid
responses fail the run with a nonzero exit code; no silent fallback or auto-repair
is performed.

Generation uses temperature 0 and seed 42. GPU/platform/backend differences may
still change text. Archived structured responses support deterministic replay of
the core activation path; identical future live text is not promised.

Traces contain the observation and generated text, so treat them as potentially
private. The CLI requires an explicit destination and refuses to overwrite it.
Ignored outputs are convenient diagnostics, not durable experimental evidence.
Preserve selected sanitized experimental records with their configuration/source
revision in a documented archive or tracked experiment directory.

## Tests and current limitations

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Unit tests mock downloads and inference; they require neither GPU nor model files.
A real run is demonstrated separately in
[the local-model smoke report](../experiments/LOCAL_MODEL_SMOKE.md).
The CLI is not a checkpoint loader, live conversation service, autonomous
contemplation loop, or the persistent judgment-revision experiment. All three
roles run once per observation; no recursive thought scheduling is implemented.
