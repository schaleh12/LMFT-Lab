# Linguistic application: Phase A development-only results

2026-10-13. **Implementation and development checks complete; STOP before held-out
execution for parent and independent custodian review.** No evaluation passages or
per-example labels were accessed. This is supervised contextual cue learning over
supplied categories, not new meanings, philosophical weights, seed contribution or
production runtime integration. The cross-cutting geometry remains untested.

## Frozen inputs and implementation

[Protocol](LINGUISTIC_APPLICATION_PROTOCOL.md) was persisted before implementation
and before writer access to development passages. Its unchanged SHA256 is
`00967e14b87adafa06aa0be3935e24621f05e0172f0019966061caba918ab964`.
[Data binding](LINGUISTIC_APPLICATION_DATA_BINDING.json) pins the approved export,
split identity, counts and exact adapter mapping. No other corpus was downloaded
or inspected. The 20 first-batch examples cover 10 documents/18 sentences; the 13
second-batch examples cover 10 other documents/13 sentences. Seven supplied senses
appear in batch 1, eight cumulatively. No observed sense was merged or discarded.

Document/provenance/stage fields never become classifier features. Surface tokens
include punctuation and compounds containing spaces; the entire target token is
excluded before the frozen ASCII lowercase segmentation. No external stop words,
semantic tags, WordNet lookup, numerical memberships or model calls are used.

The primary inverted cue index and ordinary memory's independent candidate/scanning
implementation produce identical rule/witness tables. Both use the same admission
rule, data and application policy. Batch 2 preserves prior evidence and revisions,
adds candidates and invalidates contradicted active cues. Frozen batch 1 and the
lexically tie-broken majority diagnostic are also implemented. All application
requests reject labels and extra metadata; scoring is separate from the worker.

## Development findings — resubstitution only

| Development set and controller | Correct single label | Wrong single label | Abstain | Ambiguous |
| --- | ---: | ---: | ---: | ---: |
| Batch 1, primary/memory/frozen at stage 1 | 7/20 | 0 | 13 | 0 |
| Batch 1, majority at stage 1 | 5/20 | 15 | 0 | 0 |
| Same batch 1, updated primary/memory at stage 2 | 8/20 | 0 | 12 | 0 |
| All development, updated primary/memory | 15/33 | 0 | 18 | 0 |
| All development, frozen batch 1 | 8/33 | 3 | 22 | 0 |
| All development, majority | 10/33 | 23 | 0 | 0 |

On the same original 20 examples, updated primary/memory gained three strict-correct
classifications and lost two; both losses became abstentions. Preserve those
regressions. The other controllers' batch-1 classifications did not change.
Stage 1 has 7,012 candidates: 11 active and 7,001 rejected. Stage 2 adds 3,215
candidates and has 28 active, one invalidated and 10,198 rejected. Counts are
candidate rules, not independent observations or learned concepts. Cumulative
evidence never removes the invalidating counterexample.

Zero wrong inclusions on cumulative training data follows from excluding every
cue with an admitted counterexample; it is not independent semantic validation.
No ambiguity in these natural development outputs does not establish that meanings
are disjoint. Synthetic overlap/unknown cases test mechanics only. Per-sense
denominators, inclusion/exclusion counts, coverage and full comparator metrics are
in `outputs/linguistic-application-phase-a-20261013-001/development-summary.json`.
Passage-bearing predictions and witness traces remain outside the repository.

## Verification and retained failure

- Focused synthetic contracts: **63 passed**. Tests cover distinct-document support,
  independent pair cues, immutable witnesses/revisions, invalidation/no resurrection,
  ambiguity/abstention, exact replay, conflicting IDs/locators, malformed/provenance
  inputs, gold rejection, majority ties, independent-memory construction, exhaustive
  small synthetic labelings, metrics/unseen gold, tampered history/source pins and
  actual subprocess restart with no mutation.
- Full existing plus new regression: **1,226 passed**, zero skipped/errors/failures,
  214.66 seconds (1,163 existing + 63 new). This increment retires no tests.
- Natural development used eight completed fresh worker processes. Repeated
  predictions and exact batch replays preserve checkpoint bytes; primary/memory
  parity and frozen retention hold. Both stage checkpoints and all traces retained.
- Initial focused run: 62 passed/one failed because the sandbox-default pytest
  temporary directory denied atomic checkpoint replacement. Preserve
  `focused-tests-001.xml`. The unchanged code passed with an explicit directory
  under the authorized user Temp root (`focused-tests-002.xml`). No rule/threshold
  or acceptance criterion changed. Full-suite invocation used that same explicit
  Temp-root approach with a new directory.
- Worker check at 02:30:14 UTC found zero matching LMFT/pilot/pytest Python workers.
  Sandbox CIM access first failed; the authorized read-only host query succeeded.
- All 174 previously reviewed executable/configuration/protocol/test files remain
  unchanged. Only new experiment/test files plus handoff documentation were added
  or revised; production, seed, numerical mechanisms, model/config/dependency pins,
  random seeds, prior uncommitted work and historical outputs are preserved.

## Reproduction and evaluator handoff

Python 3.12, existing environment only. Set `PYTHONPATH=src` from repo root.
Focused command: `.venv/Scripts/python.exe -m pytest tests/test_linguistic_application.py -q`
with an explicit fresh writable `--basetemp` and `--junitxml` path. Full command is
the same without the test-path restriction. Recorded commands and XML/log evidence
are in `outputs/linguistic-application-phase-a-20261013-001/`.

Experiment files:

- `linguistic_application.py`: strict contract, primary induction, versioned state,
  application and separate metrics.
- `linguistic_application_memory.py`: independently computed ordinary memory rules.
- `linguistic_application_worker.py`: one-request CLI using existing Store/atomic
  persistence and locks, pinned source/protocol and full history reconstruction.
- `linguistic_application_development.py`: exact approved export adapter and
  development-only subprocess runner; it cannot locate or load held-out custody.
- `tests/test_linguistic_application.py`: synthetic contracts; no corpus fixtures.

CLI consumes one JSON object on stdin. `train --state-dir PATH` takes the exact
protocol batch schema, creates stage 1 or reloads for stage 2. `predict --state-dir
PATH` takes exactly `{"items": [{"id": "opaque-id", "tokens": [...],
"target_indices": [0]}]}` and returns `pid`, `stage`, `state_digest`, and predictions
for primary/memory/frozen/majority. Each controller output includes sorted `labels`,
`status`, singleton `selected` or null, and matched rule IDs. `inspect --state-dir
PATH` reports stage/count/pins/hash only. Gold stays with the evaluator and must not
be included in application input. Prediction does not commit any state. Exact
source/protocol pins are mandatory; no migration/fallback is provided.

External retained working directory:
`C:\Users\schal\AppData\Local\Temp\lmft-linguistic-phase-a-20261013-001`.
`state/checkpoint.json` is stage 2; `batch-1-checkpoint.json` preserves stage 1.
`development-trace.json` holds development outputs; original export, normalized
requests and README/LICENSE/use notices remain beside them. This is temporary
local storage, not a durable backup or permission to redistribute. Source archives
cannot alone reconstruct corpus-bearing checkpoints; recovery also needs the exact
approved export/notices or preserved external artifacts. Do not inspect other
custodian directories. Shared-filesystem separation is procedural, not security
isolation; aggregate evaluation distribution may be inferable from disclosed counts.
Source-family independence is unverified and licensing remains unresolved.

The source-only prework archive contains all 238 original files, preserving the
dirty working tree. `pre-development-source-hashes.json` pins all seven pilot files
before natural learning. Final `source/` and `source-manifest.json` archive source,
configuration, protocol and handoff without corpus; `verification.json` records
preservation, evidence and final Git state. Historical outputs are not recursively
copied. No commits, pushes, publication, teacher expansion or model calls occurred.

Parent/custodian review of frozen protocol, code, export mapping and these limits
is the next gate. **No held-out execution or next implementation task performed.**


## Corrective addendum: strict cached-state types (2026-10-13)

Parent review blocked held-out execution after five checksum-valid substitutions
were accepted by both inspect and predict: Boolean/float schema version, Boolean
revision version, and Boolean/float cached target indices. Original requests were
unchanged. Python equality treated these values as equal to the expected integers.
Substantive cue/document/provenance corruption was already rejected. The original
results, source, checkpoints and reviewer negative evidence remain preserved.

Narrow correction: require `type(schema_version) is int` and compare the entire
reconstructed/persisted state through sorted JSON serialization with nonfinite
numbers rejected. This distinguishes Boolean, integer and floating-point values
throughout cached evidence, interpretation versions and batch history. Shared Store,
scientific protocol, tokenizer, thresholds, comparators and data binding are unchanged.

Added 28 actual-process inspect/predict tests covering the five reported cases,
related revision/memory/batch numeric types and already-rejected stage/request
cases. Before the fix these reproduced **20 failed/8 passed** (63 deselected);
`prefix-reproduction.xml` and `.log` preserve that failure. After correction:
**91 focused and 1,254 full tests passed**. No tests skipped or criteria relaxed.

Fresh development checkpoints were recreated from the same approved export, without
migration. Every development prediction and report is identical; traces differ only
in process IDs/state digests and both checkpoint states differ only in source pins.
The original three gains/two losses and all other scientific outcomes remain.
No held-out examples/labels or models were accessed.

Corrected external directory (corpus/notices remain outside repository):
`C:\Users\schal\AppData\Local\Temp\lmft-linguistic-phase-a-type-fixed-20261013-001`.
Use its `state/checkpoint.json` with corrected code. Old checkpoints require the
matching original source; pins were not relaxed.

SHA256 identities:

- Corrected `linguistic_application.py`:
  `cf7249dc7b5d954d4cfa63880bfb5b6cd8f4dfa5739626e179b797131ccd4acd`.
- Corrected `test_linguistic_application.py`:
  `d3f1aa4f03c8f18fe127bed771e5d258ddb468ab5853bf9df3c2aa36053b6b4e`.
- Corrected `batch-1-checkpoint.json`:
  `42d28fc6dc9ab407cc66b1ff58349d8a3702d32a346efff2e9edec739407aba1`.
- Corrected `state/checkpoint.json`:
  `123e3fd3a8af02ca16f92de02a99b3ba0973c16006afce8d4c53b3bb83858838`.

Correction archive: `outputs/linguistic-application-type-fix-20261013-001/` includes
246-file prework recovery, corrected source, full final source/configuration snapshot,
test/failure logs, development parity and verification manifests. Reviewer evidence
at `C:\Users\schal\AppData\Local\Temp\lmft-linguistic-phase-a-review-vf5lpvro`
remains in place, with hashes only in the repo to avoid copying corpus-bearing data.
Parent/custodian re-review remains the gate; STOP before held-out execution.
