# Local-model smoke run — 2026-10-11

**Status:** Actual local model execution succeeded; this is not Experiment 001
and does not demonstrate persistent judgment revision.

## Environment and pinned artifacts

- Windows 11 x64, Python 3.12.3.
- NVIDIA RTX 4080, 16,376 MiB VRAM, driver 610.88.
- Qwen/Qwen3-4B-GGUF, Q4_K_M, commit
  `bc640142c66e1fdd12af0bd68f40445458f3869b`.
- llama.cpp b11429, official Windows x64 CUDA 12.4 binaries and CUDA DLLs.
- SHA256 pins are in [the model configuration](../config/local_models.json) and
  [asset bootstrap](../src/lmft_lab/model_assets.py).
- [Hardware evidence](local_model_runs/hardware.json) records the source base
  commit and the LMFT server PID reported by NVIDIA. WDDM reported per-process
  memory as unavailable. Total GPU use while loaded was 5,245 MiB, including other
  applications; this is not a model-only memory measurement.
- [Final source manifest](local_model_runs/source_manifest.json) records hashes
  of the uncommitted implementation/configuration used for the final run.
  Earlier traces predate the explicit offline provenance field; they are retained.

The initial asset preparation used the same ensure_model/ensure_backend functions
that the runtime calls automatically on a cache miss. It downloaded and verified
the model and both backend archives before the first timed processing run.
Reported processing durations therefore exclude network download time.

## Procedure

From the repository root, with `$env:PYTHONPATH = 'src'`:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab --config config/local_models.json --event-id actual-local-001 --observation "I found a mistake in my explanation and corrected it after checking the original measurement." --trace experiments/local_model_runs/actual-local-001.json

.\.venv\Scripts\python.exe -m lmft_lab --offline --event-id actual-offline-002 --observation "I found a mistake in my explanation and corrected it after checking the original measurement." --trace experiments/local_model_runs/actual-offline-002.json

.\.venv\Scripts\python.exe -m lmft_lab --offline --event-id actual-offline-final-003 --observation "I found a mistake in my explanation and corrected it after checking the original measurement." --trace experiments/local_model_runs/actual-offline-final-003.json
```

These files already exist; reproduction must use new event IDs and filenames.
The CLI deliberately refuses to overwrite a run. The final run includes explicit
offline=true provenance for all three role calls. Full requests, outputs, input
state, and numerical activation traces are in:

- [First real run](local_model_runs/actual-local-001.json)
- [Offline verification](local_model_runs/actual-offline-002.json)
- [Final offline run](local_model_runs/actual-offline-final-003.json)

## Observed result

All runs completed interpretation, digestion, and contemplation support. Model
output passed independent LMFT validation. The interpretation proposed relevance
0.8 for Psychological and 0.6 for Philosophical, with exact observation quotations
and reasons. These values entered the existing deterministic activation and
propagation code. No association network was supplied, so propagation did not
invent edges or change direct relevance.

The broad domain-level memberships are model suggestions, not validated semantic
grounding. The model suggested self-correction and accuracy as interpretations.
That plausible explanation does not prove the observation true or justify a
persistent confidence increase. All traces contain an empty persistent_changes
list and explicitly state that the revision engine is not implemented.

| Run | Interpretation (includes startup/cache verification) | Digestion | Contemplation |
| --- | ---: | ---: | ---: |
| First real run | 11.375 s | 2.547 s | 2.672 s |
| Offline verification | 10.625 s | 2.609 s | 2.688 s |
| Final offline run | 10.500 s | 2.547 s | 2.625 s |

The first run's server-reported generation rates were approximately 163–170
tokens/second, with 386–398 generated tokens per role. This is a single short
fixture, not a benchmark across tasks. Offline and online-mode proposals matched
for this fixture; no general bitwise reproducibility claim follows.
The owned llama-server processes were confirmed stopped after completed runs.

## Automated checks versus actual execution

**159 pytest checks passed.** The existing 117 checks continue to pass. New checks
use mocked inference/downloads and verify the real LMFT activation path, role
context flow, unchanged input state, explicit model provenance, schema validation,
malformed/truncated outputs, timeout handling, immutable cache placement,
checksum/offline behavior, credential redaction/redirect handling, and process reuse.

The three runs above actually executed the downloaded model on the local CUDA
backend. No mocked responses were used in those run artifacts.

## Limits and next step

No founding node, persistent seed identifier, prior value, propagation equation,
or migration rule changed. The only existing activation API extension is an
optional source tag whose default remains developer; model-driven frames say llm.

There is no automatic judgment acceptance, persistent learning, checkpoint/restart,
autonomous contemplation scheduling, or general prompt-injection guarantee.
The next step is to specify and implement one evidence-backed judgment revision
with explicit acceptance criteria, reason retention, and recoverable persistence.
The current model proposals can become inputs to that path; they must never bypass it.
