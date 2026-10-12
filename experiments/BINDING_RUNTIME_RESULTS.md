# Persistent binding in the supervised runtime — results

**Review status:** the initial integration below was **blocked** by independent
review for checksum-valid nested configuration and request-history inconsistencies.
Original results/archives remain intact. The owner-authorized [narrow restart fix](BINDING_RESTART_FIX_RESULTS.md)
passed writer-run corrective verification and was subsequently independently accepted. Earlier
passing counts below did not establish the missing consistency properties.

2026-10-12. Two opt-in fixture-only modes now use learned neutral-channel bindings
to determine actual supervised-runtime outbox decisions. Informative evidence
changes12 abstentions into12 correct decisions after restart. An explicit frozen
pre-acquisition control admits the same evidence and spends the same budget but
retains those abstentions. Independent ordinary memory matches throughout.

This integrates a finite numeric comparison family. It does not establish tree
superiority, philosophical-seed usefulness, semantic understanding or a causal world
model. The fixed40-node birth state remains unchanged and is not the mechanism
responsible for this result. No model calls, teachers, new dependencies or UI.

## Protocol, chronology and review provenance

[Protocol v1](BINDING_RUNTIME_PROTOCOL.md) and its acceptance matrix were frozen
before production implementation/evaluation. SHA256:
`9bc68f69b135890e64cdc56ec4321c0a35d75fc4aa4d434166cfccdf56ffe13e`.
`outputs/binding-runtime-prework-001/protocol-pin.json` records16:25:17 UTC and the
session tool sequence establishes the ordering; this is not an external timestamp
authority. Starting HEAD: `341b4c8281847fcf676e9aa5fa9f837de159065b`.
The preceding attribute-binding work and handoff were already uncommitted.

The accepted [isolated binding study](ATTRIBUTE_BINDING_RESULTS.md) remains intact.
Its independent reviewer reproduced20 focused tests,248 review checks and30 actual
subprocess stages with30 identical checkpoints for permutation4. The reviewer used
unchanged stage functions because Git-scoped CLI preflight was blocked. Its full778
test XML,1,125 recorded checks,1,121 artifact hashes and210 source hashes were
inspected; the778-test suite was **not independently rerun** at that gate.

This integration's first focused run retained27 passes and one failure: complete
state comparison treated in-memory birth tuples as different from JSON lists.
Diagnostic comparison localized the difference to birth and confirmed equality after
JSON normalization. The harness comparison was corrected, without changing scientific
criteria. Original failed outputs/XML and exact219-file source snapshot remain in
`binding-runtime-targeted-001` / `binding-runtime-targeted-source-001`.
Focused002 passed28 tests in16.24s; focused003, with additional real-inbox probes,
passed28 in17.18s. Exact snapshots for both are retained. No failed evaluated primary
study was overwritten. Negative admission tests and expected compatibility rejection
are intentional checks, not silently discarded failures.

## Production contract and exact call path

[Runtime guide](../docs/BINDING_RUNTIME.md). Existing entry point:
`python -m lmft_lab.runtime --root ... start --mode fixture --experiment binding-primary`
or `binding-memory`, with explicit `--binding-registry` and optional
`--binding-condition`. Both modes reject local-model execution and missing registry.

`runtime.main -> run -> initial_state -> Store.next_input -> runtime.advance ->
binding_runtime.handle -> binding predictor -> runtime.emit -> Store.commit`.
Restart uses `Store.read`, unchanged full manifest comparison and binding-state
validation. These are the existing supervised queue, deduplication, outbox and atomic
checkpoint mechanisms, not a separate demo or recommendation wrapper.

Only pre-existing implementation file changed: [runtime.py](../src/lmft_lab/runtime.py)
(registration, pinned controls, dispatch, restart validation and halt-only probe).
New production modules:

- [binding_contract.py](../src/lmft_lab/binding_contract.py): fixed neutral-binding-1
  family/scope,36 representations/18 behavioral classes and deterministic query pool.
- [binding_primary.py](../src/lmft_lab/binding_primary.py): explicit comparisons,
  elimination, disagreement selection and consensus.
- [binding_memory.py](../src/lmft_lab/binding_memory.py): independently computed
  truth-table masks, filtering and votes; no primary decision-function calls.
- [binding_runtime.py](../src/lmft_lab/binding_runtime.py): strict admission,
  lifecycle, persisted learning state and emitted decisions.
- [binding_verifier.py](../src/lmft_lab/binding_verifier.py): receiver-invoked trusted
  private-registry subprocess. Production imports no experimental modules.

Outer checkpoint schema1 remains unchanged; nested `binding-runtime-state-1` pins
mode, condition, family digest, evidence/provenance, recomputable survivor analysis,
pre-acquisition prediction snapshot, query, request identity, phase and spent budget.
Support is inspectable from survivor count and per-case consensus/reason. Unknown
versions, altered family/derivation or invalid episode invariants are rejected.
There is no capacity-checkpoint conversion, family expansion or forced singleton.

Training and the correlated selected reply can filter survivors. External proposals
cannot install a relationship; language text has no learning authority. Predictions
use saved survivors (or the explicitly pinned frozen snapshot). Empty families
abstain; ambiguous disagreement abstains; nonempty consensus may decide without a
unique class. Feature-only evaluation leaves the complete binding state unchanged;
normal cursor, receipt and outbox bookkeeping continues. No held-out labels filter
candidates or validate deployment. This remains a one-episode synthetic experiment.

## Trust and information boundaries

The harness alone owns the hidden channel mapping and executes the unchanged
bounded-write oracle. It prepares canonical neutral training/query observations in
an operator-owned private registry. The receiver invokes a fixed verifier subprocess
to compare an incoming record with that registry, checks the returned canonical
record and persists provenance. A supplied digest, source string or verification
assertion alone cannot authorize evidence. Registry identity and salted byte hash
are pinned; its private path, contents and hidden mapping are absent from learner
state and deliberately emitted messages. The learner sees only admitted records.

This trusts the operator's registry construction and local process/filesystem. The
receiver authenticates membership in that synthetic registry; it does not establish
independent real-world truth or re-execute a physical device for each admission.
Random opaque identities/paths contain no channel permutation. Strict kernels have
no mapping/oracle interface. Existing runtime fixture imports are not an OS sandbox;
arbitrary malicious local code could read private files. Rejected inbox contents
remain untrusted audit data and cannot change binding state.

The budget is one selected information request. Registry preparation precomputes
query outcomes; direct-reference replay repeats verification. Neither a physical
oracle-call cap nor crash-proof exactly-once verification is claimed.

## Results and denominators

Each row holds for **both kernels in each of six permutations**. Permutations are
symmetry checks, not independent replications. All72 arms froze pre/post predictions
before held-out scoring.37 held-out triples contain a3 and are excluded from admission.

| Condition | Classes before -> after | Request budget spent | Decisions before -> after /37 | Correct/decided after | Abstentions after |
| --- | --- | ---: | --- | --- | ---: |
| Informative | 2 -> 1 | 1 | 25 -> 37 | 37/37 | 0 |
| No acquisition | 2 -> 2 | 0 | 25 -> 25 | 25/25 | 12 |
| Noninformative | 2 -> 2 | 1 | 25 -> 25 | 25/25 | 12 |
| Unavailable | 2 -> 2 | 0 | 25 -> 25 | 25/25 | 12 |
| Already supported | 1 -> 1 | 0 | 37 -> 37 | 37/37 | 0 |
| Informative, prediction frozen | 2 -> 1 | 1 | 25 -> 25 | 25/25 | 12 |

Wrong decisions:0 in every condition at both stages. Informative coverage rises
67.57% ->100%; accuracy among decisions stays100%, not an accuracy improvement.
The frozen control retains the two-class prediction snapshot despite its evidence
analysis becoming unique. Same admitted evidence/budget plus exactly12 changed outbox
decisions identifies the causal role of updating the persisted prediction basis.

**1,530/1,530 checks**,72 arms and216 actual runtime processes passed in
`outputs/binding-runtime-001`. Every arm stopped with persisted selection, restarted
for reply/closure, and restarted again for evaluation. All three stages match
continuous direct transitions. Checks include live-inspection exclusion, actual
inbox rejection/dedup, immutable evaluation, outbox/kernel parity, zero calls,
birth invariance, memory parity and30 paired indistinguishable-history comparisons.
Unit tests separately exercise an empty family from explicitly contradictory trusted
fixture records; such records are not primary noiseless oracle data.

Fresh permutation4 rerun: **250/250 checks**,12 arms/36 runtime processes in
`outputs/binding-runtime-rerun-001`. Main and rerun learning-state snapshots compare
without removing scientific fields; full state comparisons normalize JSON, timestamps,
processing duration and the random opaque verifier pin. Exact comparison evidence:
`outputs/binding-runtime-rerun-comparison-001.json`.
Its77/77 checks include36 identical learning-state digests and36 normalized full-state
comparisons, score parity and both source/artifact manifest verifications. Main and
rerun artifact manifests pin8,313 and1,573 files respectively, excluding themselves.

Full checkout regression: **806 passed in194.27s**, no failures/errors/skips,
`outputs/binding-runtime-full-regression-001.xml`. This is separate from the preceding
reviewer's inspection-only778-test evidence.

## Preservation, archives and compatibility

Before any production edit, all44 runtime source hashes exactly matched the owner's
demo manifest.211 source/config/document files were copied under
`outputs/binding-runtime-prework-001/source`; source inventory digest:
`89ad87fd7ffac6d3c3c460a912afc7fe2d013eb9ba05ffcecdbb7410b322d487`.
All102,090 prior output files were pinned (inventory digest
`95d39d6ab8817f4b14ff9b6aa9678e8b62794ce87989c3caacae8f2a35d490ed`)
and verified unchanged, including all19 files of
`outputs/action-demo-20261012T150026-75a8489b` and previous studies/archives.
Separate historical audit passes83 archived sources,134 protected resolutions,
56 Git-backed resolutions and137 tree files.

Evaluated context004 SHA256:
`2729113bd7aa77471d1a2b80fe81e1c595a382e09163c1a6bc6d3007bf910b77`;
220-file source inventory:
`eccc5abcd05747c3c2d5516c005cc106552d3f7f5e1c4f8ca0aabf9943bf1acd`.
Both main and rerun contain the complete evaluated source/config archive and artifact
hash manifests. Main frozen predictions SHA256:
`cff7e65777b4ac319dece58b17c89a0d1ef64d56163d698c0b2a7ca9c4f3e03e`.
Documentation handoff is captured separately after evaluation in
`outputs/binding-runtime-handoff-context-001.json` and
`outputs/binding-runtime-handoff-source-001/`. Final preservation/source/lifecycle
checks are recorded in `outputs/binding-runtime-final-checks-001.json`.

Compatibility checks in `outputs/binding-runtime-compatibility-001/results.json`
pass4/4: source match, modified-code rejection, archived-code startup/halt preserving
the copied checkpoint exactly, and unchanged original demo. The test used a fresh
checkpoint-only copy and did not replay the user's inbox. It establishes a matching
archived-code recovery route; it does not claim complete queued-work recovery.
The original session was never reopened. Old sessions **cannot resume under the
modified current checkout**: full software_manifest checks were not relaxed.
No surprise migration or user action is required to preserve the existing session.

## Reproduction and stop

Use new output names every time. Current-context capture is required after handoff
documentation changes; context004 belongs to the evaluated pre-handoff source set.

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/binding-runtime-review-context-001.json
.\.venv\Scripts\python.exe experiments/run_binding_runtime.py --output outputs/binding-runtime-review-001 --preservation-context outputs/binding-runtime-review-context-001.json --permutation 4
.\.venv\Scripts\python.exe -m pytest -q tests/test_binding_runtime.py --basetemp outputs/binding-runtime-review-tests-001
```

Omit `--permutation 4` for the complete matrix. Scientific outputs are deterministic;
process IDs, timing, random private registry identity/nonce and directory names are
not. [Compatibility checker](check_binding_compatibility.py) accepts a fresh `--output`
and explicit `--archive` / `--demo`; defaults identify the preserved checkpoint and
pre-change source. It never writes into the demo directory.

No commits, pushes, publication, discards or next task. The original gate stopped for
review; the narrow fix was subsequently independently accepted. The parent closed
the session early, before18:40 UTC. This integration does not authorize broader
learning, conversational work, seed changes or additional experiments.
