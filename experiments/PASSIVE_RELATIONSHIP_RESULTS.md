# Passive runtime integration — evaluated results

2026-10-12, [frozen protocol v1](PASSIVE_RELATIONSHIP_PROTOCOL.md).
Protocol SHA256 `7a0e0092de474676975734ffbfc2046ff760043471e563fd413a5e7ecdad4b4b`.
Actual clean starting commit `186c586348482eee19dc2fc8e31e9b552866eee7`;
previous insufficiency work had been committed before this cycle. New integration
changes remain uncommitted. No competing source writer was used.

**Relationship sets now run through the real supervised runtime. State, predictions
and semantic communication match uninterrupted execution, the standalone learner
and equally equipped memory. No active acquisition was added.**

## Implementation and contracts

[Handler](../src/lmft_lab/passive_relationship.py),
[runtime registration/routing](../src/lmft_lab/runtime.py),
[harness](run_passive_relationship.py), [tests](../tests/test_passive_relationship.py),
[usage/compatibility guide](../docs/PASSIVE_RELATIONSHIP_RUNTIME.md).

Two new opt-in modes: relationship-set-lmft and relationship-set-memory. Both wrap
the UNCHANGED insufficiency learner and registered blocked-length-two fixture.
The original capacity mode, standalone algorithms, six candidates, founding geometry,
numerical equations/thresholds, model configuration and migration behavior are unchanged.
Both comparators share the existing runtime's inert 40-node birth scaffold. Its
presence is common runtime packaging; neither selection nor prediction uses activation,
propagation or founding node labels. No LMFT/fuzzy advantage follows.

New manifests pin integration rule, scenario and the exact task/verifier/candidate/scope
configuration. JSON-normalized policy identity survives persistence. Fixture operation
is mandatory, so local-model setup is rejected before configuration/model loading.
The new handler dispatches before model processing. Calls, including mocks: **zero**.

The learner lives separately under judgment, with six authored candidates, registered
evidence/provenance, retained set and derivation/validation trace. Accepted evidence
also has source/sender/message/cycle links. Receipt/inbox records retain rejected
inputs and reasons, outside the learner. Copy-before-admission means rejection and
evidence duplicates leave the ENTIRE judgment unchanged; runtime message duplicates
and conflicts retain their existing behavior.

Support status distinguishes untrained, supported, ambiguous and no_supported_hypothesis;
validation status separately distinguishes unvalidated, validated, validation_rejected
and empty-family rejection. Unvalidated supported rules abstain. Empty sets have no
votes and cannot pass vacuously. Ambiguous accepted sets predict only on unanimity.
evaluate writes a deliberate response/receipt but changes no learner state or evidence;
pure predictions and halted CLI probes also preserve checkpoint bytes.

This is a noiseless synthetic registration/verifier contract, not source authentication
or real-world truth. Unsupported does not distinguish missing vocabulary/context from
erroneous evidence. The full candidate vocabulary and policies are developer-authored;
the evidence determines their retained subset. No teacher or feature repair is involved.

## Frozen run, parity and quality

Evaluated archive: `outputs/passive-runtime-001/`.
Six conditions each have restarted and uninterrupted references = twelve actual
runtime individuals, plus one learning-disabled/compatibility individual. All thirteen
are halted. Restarted conditions each used five real process lifetimes: initial
training, exact no-input training restart, validation continuation, exact no-input
accepted-state restart, and evaluation. Six uninterrupted references used one lifetime
each. All scientific judgments, birth and semantic receipts/outbox messages match,
excluding timestamps/processing time. Live inspection was refused.

**274/274 integration integrity checks** and **36/36 quality checks** passed.
All twelve runtime learner states/predictions match the independent standalone path,
and LMFT/memory access, provenance links and semantic communication match exactly.
Both models received identical registered/invalid inputs, splits, phases and policies.
There were no questions, inference diagnostics or automatic observation requests.

Quality remains exactly the prior insufficiency fixture's negative results:

| Scenario (both modes) | Retained set | Equality correct/decided | Non-equality correct/decided | Overall coverage / accuracy among decisions |
| --- | --- | --- | --- | --- |
| Unsupported | empty | 0/0; 4 abstain | 0/0; 4 abstain | 0% / undefined |
| Supported control | le | 3/4 | 3/4 | 100% / 75% |
| Ambiguous control | lt,le | 0/0; 4 abstain | 3/4 | 50% / 75% |

The supported control fails the withheld fault cases (2,2) and (2,5); ambiguous
consensus fails (2,5). Their errors were preregistered and preserved. All modes
recognize x1 as out-of-scope, excluded from quality denominators. Integration
correctness is not improved predictive accuracy. Blanket abstention fails controls.
All final predictions were frozen before any held-out label was scored, and no
held-out label can revise accepted state.

Per main individual: 43 receipts, 42 outbox records; four training/four validation
facts; eight accepted message/provenance links; six candidate derivations; one exact
message duplicate, one same-message-ID conflict, two evidence duplicates, fifteen
rejected inputs including one malformed envelope. Rejected cases include false
label BEFORE true evidence, wrong source/type/features, held-out input, executable
proposal, teacher reply, request and closed-phase operations. Rejections/duplicates
before/after acceptance preserve scientific/provenance digests, and full judgment
is identical before versus after held-out communication. Restarted checkpoints
range from 80,042 to 85,642 bytes; these are descriptive history/storage costs.

## Tests, preserved failures and scope of reproduction

25 new passive tests, including eight before/after-replacement atomic-fault cases
for evidence, selection, acceptance and evaluation. These check the scientific state,
cursor, processed identities, receipt and outbox as one old/new commit; replay has
no double learning/output. Fault injection is not a power-loss durability claim.
Other tests cover wrong/malformed/unverified evidence, duplicate/conflicting IDs,
state distinctions, oracle/model isolation, learning-disabled admission, local-mode
refusal, whole-set validation failure and source/manifest incompatibility.

The complete **486-test suite passed** from an identical clean source snapshot at
`outputs/passive-runtime-regression-source-001/`, with temp artifacts retained under
`outputs/passive-runtime-regression-clean-001/`. That snapshot includes all tracked
and new source/tests/config/spec/protocol files and a source-snapshot-hashes.json;
source/config files match the evaluated working checkout. No test was skipped or
modified to change historical acceptance criteria.

Important qualification: the initial complete working-checkout invocation was
**485 passed, 1 failed**. Its sole failed check was the old insufficiency harness's
`protected-files-preserved`: that harness implicitly loads its historical local
prework directory and asserts the runtime source is unchanged. This authorized
integration intentionally changes exactly that protected file (`src/lmft_lab/runtime.py`).
The same old run still passed 136/137 integrity and 18/18 quality checks; no scientific
behavior check failed. The failed run/result/failure.json is retained under
`outputs/passive-runtime-regression-001/test_full_frozen_study_with_ac0/study/`.
The historical harness and preservation criteria were NOT weakened or rewritten.
The matching source snapshot separates all behavioral regression tests from that
preexisting output-context assumption; its old prework evidence is explicitly unavailable.
The main new integration run separately checks all 139 protected prior files against
its own prework manifest, which excludes only authorized runtime/handoff edits.
Rerunning the old full-study test in this working checkout will still report that
historical-source-preservation failure; use a clean matching checkout/snapshot for
the complete behavioral suite, or original archived sources for historical provenance.

Two earlier focused attempts are also retained:

- `outputs/passive-runtime-tests-001/`: 24 tests passed, process test failed on a tuple-versus-JSON-list policy manifest restart mismatch. Normalize the policy at the boundary; frozen protocol/criteria unchanged.
- `outputs/passive-runtime-tests-002/`: process study passed; 24 tests passed and one atomic replay test compared wall-clock timestamps across recalculation. The test now compares the complete semantic transaction excluding timestamps, as already specified by v1; exact old/new checkpoint restoration is still checked before replay.

No protocol-changing fix or v2 criterion revision occurred. No failed attempt was
deleted. Original evaluated sources for every attempt remain in its fresh archive.
The final integration run and clean-snapshot full suite used the corrected implementation.

## Reproduce and artifact paths

Completed working-root commands (PowerShell):

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/passive-runtime-regression-001
.\.venv\Scripts\python.exe experiments/run_passive_relationship.py --output outputs/passive-runtime-001
```

The first command has the one historical-context failure described above. For the
passing full-suite reproduction, working directory was the preserved source snapshot:

```powershell
$env:PYTHONPATH = 'src'
& 'C:\Users\schal\OneDrive\Desktop\LMFT based general AI\LMFT-Lab\.venv\Scripts\python.exe' -m pytest -q --basetemp 'C:\Users\schal\OneDrive\Desktop\LMFT based general AI\LMFT-Lab\outputs\passive-runtime-regression-clean-001'
```

Choose fresh output/temp paths when repeating commands. The targeted passive test
file can be run directly in the working checkout. No second standalone scientific
study was dispatched; full-suite executions contain their own fixed harness checks.

Under `outputs/passive-runtime-001/`:

- `archive-manifest.json`, `archive/`, `configuration.json`, `provenance.json`, `protected-hashes.json`: exact evaluated source/tests/config/protocol, hashes, pinned policies, Git/Python identity and preservation evidence.
- `frozen-predictions.json`, `results.json`: all twelve frozen predictions followed by separate group scoring/integrity results.
- `<branch>/<mode>-<scenario>/training-halted.json`, `accepted-halted.json`: restarted states before exact no-input recovery checks (restarted branch only).
- `<branch>/<mode>-<scenario>/final-halted.json`, `integration-checks.json`, `standalone-state.json`, `frozen-predictions.json`: complete final state, process PIDs/checks, independently constructed learner and prediction set.
- `<branch>/<mode>-<scenario>/individual/checkpoint.json`, `inbox/*.json`, `lifecycle.json`: real atomic runtime state, raw messages and final halted lifecycle.
- `control-compatibility/`: halted disabled individual, changed-scenario/control refusal stderr/returncodes and checks.

Branches restarted,uninterrupted; modes relationship-set-lmft,relationship-set-memory;
scenarios unsupported,supported,ambiguous. Pre-change source/handoff copies and
protected hashes: `outputs/passive-runtime-prework-001/`. Outputs are local/ignored
by Git; no external backup was verified.

## Compatibility and next boundary

New software identity rejects old checkpoint manifests; no historical checkpoint
was migrated or altered. Resume old individuals with archived software/configuration.
The original capacity behavior retains regression coverage under the new source.
New scenario/control drift and source incompatibility reject before checkpoint changes;
local inference mode also rejects before model setup. Existing migration behavior
and model pins remain unchanged.

Passive integration is complete. The next authorized priority belongs to coordinator
review/sequencing: explicit bounded acquisition linked to outbox request identity,
independent verification, phase closure and atomic one-observation budget. It is
NOT implemented here. Stop at this boundary; no automatic request, new experiment,
teacher expansion, push, publication or further dispatch occurred.

## Verification follow-up — 2026-10-12

The original outcomes/failures above remain unchanged historical records. A later
focused [verification contract](PRESERVATION_VERIFICATION_CONTRACT.md) and
[results](PRESERVATION_VERIFICATION_RESULTS.md) now separate current behavioral
regression from historical byte preservation explicitly. End-to-end tests provide
complete NONEMPTY current contexts to both harnesses; default historical prework
and original 137/18 and 274/36 scientific criteria remain unchanged. Current-context
deletion/tampering rejects at restart, and historical audit verifies all 83 archived
and 134 protected entries against archived/versioned original bytes. No no-prework
snapshot is needed for the corrected full current-checkout suite. Earlier 485/1,
failed run and original archives are preserved byte-for-byte. This follow-up changes
verification only, with no active acquisition or runtime algorithm change.
