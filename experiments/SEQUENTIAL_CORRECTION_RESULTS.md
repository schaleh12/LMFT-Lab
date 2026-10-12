# Correction, later contrary evidence and chained restart - results

2026-10-12. The action-aware correction sequence now has bounded standalone evidence
for an accepted correction, a later separately identified conflicting report, and
another actual process restart. Later conflict restored abstention; equally equipped
scalar memory matched exactly. This is persistent evidence handling, not improved
truth finding, further autonomous correction, seed understanding or LMFT superiority.

Review follow-up: strict late-report schema enforcement now rejects numeric Boolean
aliases. Fresh run002 retains all original findings; **109 targeted /697 full tests**
and **126/126 study checks** pass. See the defect disclosure below; original run001
and its source, results and tests remain preserved.

## Frozen contract and implementation

[Protocol v1](SEQUENTIAL_CORRECTION_PROTOCOL.md), SHA256
`f62d1145da8db35b54ad12d7d3801df6a2281680eabd8a94a5b583b653298fc5`, was written
before the first targeted test/evaluation. Starting HEAD was
`90c1b84a4092f5f82a76debbf2e637d7da092fe9`, with a clean working tree.
Prior reports' historical starting commits and results remain unchanged.

[Harness](run_sequential_correction.py) imports the existing action-aware v2 adapter
without editing it. Two existing cases, r1/c1 and r8/c9, each start with three
instrument roots and one permitted correction. The late report has a fresh root,
the same shielded/check1 coordinate and value false. Its frozen identity is
`late/<case>/shielded/check1`. The two-entry study registry certifies report identity,
not truth or statistical independence. It does not replace the correction reference.

The only production change is the optional keyword `evidence_registry` on
[correction.handle](../src/lmft_lab/correction.py). It selects the registration
predicate for evidence admission; the default remains the existing fixture, and
the original source check remains required. No payload can select this argument.
The unchanged handler writes the existing ledger. Correction authority, exact
permits, replacement verification, lineage and dedup remain unchanged. No direct
study ledger insertion, second truth store, new runtime mode or silent migration.
Existing source-wide runtime manifests consequently differ: historical checkpoints
still require archived source/configuration, as before.

## Results

Two cases x two selectors x three conditions = twelve trajectories per pass.
Every pending trajectory abstains. Accepted correction retains three roots and
increases stored records from three to four. Both cases then predict success;
c1 is correct, while c9 retains its known wrong prediction.

| Condition, identical for full and scalar memory | After correction | After late stage and final restart | Final roots / stored records per case | Final coverage / accuracy among decisions |
| --- | --- | --- | --- | --- |
| Admit later contrary report | success, success | abstain, abstain | 4 / 5 | 0% / undefined |
| No later report | success, success | success, success | 3 / 4 | 100% / 50% |
| Freeze admission after correction | success, success | success, success | 3 / 4 | 100% / 50% |

After correction, every condition has 100% coverage and 50% accuracy. The late
report restores inconsistent shielded support without overwriting the accepted
replacement. All original records remain present; the corrected original root
still points to its replacement and the late report supplies a distinct root.
Retransmission adds no root or record. Reduced coverage is not established truth
improvement: the authored later report is not independently verified ground truth.

The frozen control explicitly withholds the envelope in the experiment driver and
records that fact. It does not claim that runtime `learning=false` blocks evidence.
The no-later control sends no report. Memory uses the same ledger, receiver, predictor,
evidence and budget, with the existing exact scalar action-ranking reduction.
Actions, scalar/circuit scores, final full judgment state, support and predictions match.
No learned hypothesis family or validation-set acceptance exists in this predictor;
those fields are explicitly null, not inferred successes.

## Restart, identity and rejection evidence

Primary archive: `outputs/sequential-correction-001/`. Three distinct interpreter
PIDs **16716 -> 34028 -> 19688** load pending, corrected and late snapshots in turn.
Each child exits after saving its stage. `process-*.json` records loaded input hashes,
digests and interpreter/parent PIDs; `launch-*.json` records the Windows venv launcher
PID and orchestrator PID15444. The final child therefore loads evidence admitted
by the preceding child, rather than starting again from initial inputs.

`continuous-{corrected,late,final}.json` and `restarted-{corrected,late,final}.json`
match over complete JSON semantic state. Only outbox wall-clock timestamps are
excluded; raw copies are retained. Python tuples become JSON arrays on both sides.
Source/config/protocol context is pinned before/after child execution, and the
expected snapshot hash is checked before loading. All stage predictions are frozen
in `frozen-predictions.json` before outcome labels are accessed for scoring.

One lifetime action episode persists. Recalling request does not reset or recharge;
replaying its selected reply is a complete state no-op. Fresh transport IDs carrying
the same evidence/correction identity do not create support or another correction.
Conflicting evidence identity is rejected. Unauthorized new operation, malformed
envelope and conflicting correction-ID payload append rejection history while
leaving effective evidence, heads, questions, prediction and counters unchanged.
This is handler-level transport identity testing, not a new runtime transport mode.

The separate `stale-companion.json` reuses existing c10-a preparation and the exact
permitted c10-b/c10-c operations. Both are rejected at eligibility (stale head and
stale digest), before replacement verification. No new permit is created.

The original action question stays `resolved_by_correction` after new evidence
reintroduces conflict. That field records the historical request outcome, not current
support. The live read-only predictor abstains. No automatic reopening, new episode,
extra action budget or further repair is implemented. There is no crash/power-loss
test, live inbox/outbox integration, hostile-host authentication or physical-cost cap.

## Costs and denominators

Per selector/condition, across its two cases and ONE evaluation pass: two charged
policy requests, two returned correction proposals, two correction verifier calls,
two admitted replacements and six rejected challenge correction events. Challenges
perform no additional replacement verification. Late condition additionally has
two registration checks/two admitted reports; controls have zero. Duplicate
admissions are zero. No gather requests or preparation corrections occur in these
twelve primary trajectories.

Each trajectory's challenges include one correction retransmission plus three
rejected operations, distinct from its policy request. Late trajectories additionally
receive one evidence retransmission and one conflicting-ID rejection; those bypass
registration. All envelopes/receipts/reasons are retained in state and audit traces.
The replay helper reconstructs the identical authored reply payload locally; this
is not another policy request or replacement verifier execution. These are logical
operation counts, not measurements of all CPU/helper calls.

Uninterrupted and chained passes each execute twelve policy corrections and four
late registrations: **24 correction verifier calls and eight late registrations**
across both passes. The separate stale companion adds one preparation verifier call
and zero challenge verifier calls. Initial preparation constructs two shared case
bundles (six original instrument admissions and sixteen historical outcome messages),
then clones them into conditions; it is not fresh outcome learning. The companion
separately constructs its existing c10 bundle. Tests are additional work, excluded
from these primary-study costs. No model or mock-LLM calls occur.

## Verification, preserved failure and provenance

Primary study: **126/126 integrity checks**. Targeted final run: **63 passed** (21
new sequence tests plus 42 existing action-aware tests). Full actual working-checkout
regression: **651 passed in137.90s**, with no failures or skips. JUnit artifacts:
`outputs/sequential-correction-targeted-003.xml` and
`outputs/sequential-correction-full-regression-001.xml`.

The first targeted run retained **20 passed/1 failed**. Its restart check incorrectly
required the interpreter's direct parent to be the orchestrator on Windows, and
compared in-memory tuples against reloaded arrays. The stored stage JSON already
matched. The fix verifies the launched interpreter or its venv-launcher parent and
compares JSON-native values, preserving the timestamp-only exclusion. No evidence,
acceptance policy or expected scientific outcome changed. That run's source archive,
failure, stages and JUnit remain under `outputs/sequential-correction-targeted-001/`.
The next targeted run passed21; final targeted run003 follows a cost-counting cleanup.

The primary archive contains180 source/config/protocol files, all hash-verified.
Prework copied177 tracked files; before handoff edits, only correction.py differed.
All907 files across prior action001/002 and seed001/002/003 study directories retain
their captured bytes. All3,043 older archive-baseline files remain unchanged.
Separate historical audit passed83 archived-source /134 protected /137 tree checks,
including56 entries resolved from pinned Git. Artifacts:
`outputs/sequential-correction-preservation-001.json` and
`outputs/sequential-correction-historical-audit-001.json`.

Seed40, equations, thresholds, weights, model configuration, migrations and historical
reports are unchanged. No installs, model calls, commits, push, publication or archive
deletion. This report and handoff are written after evaluation; the evaluated180-file
context archives the pre-handoff source. Final handoff context is captured separately.
Git-ignored outputs need separate preservation; no external backup is asserted.

## Exact successful commands

From the Windows repository root, PowerShell:

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -m pytest -q tests/test_sequential_correction.py tests/test_action_correction.py --basetemp outputs/sequential-correction-targeted-003 --junitxml outputs/sequential-correction-targeted-003.xml
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/sequential-correction-context-001.json
.\.venv\Scripts\python.exe experiments/run_sequential_correction.py --output outputs/sequential-correction-001 --preservation-context outputs/sequential-correction-context-001.json
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/sequential-correction-full-regression-001 --junitxml outputs/sequential-correction-full-regression-001.xml
.\.venv\Scripts\python.exe experiments/verify_preservation.py audit-historical --output outputs/sequential-correction-historical-audit-001.json
```

For another run, capture a fresh complete context and use unique output, basetemp
and XML paths. Never reuse the paths above. Stop for coordinator review; no text
demo, new task, autonomous repair loop or runtime integration is dispatched here.

## Review follow-up: strict Boolean admission

Independent review found that `LateRegistry.admitted` used Python dictionary equality,
so integer0 compared equal to Booleanfalse. This violated the intended exact authored
record boundary. A read-only predicate reproduction confirmed integer0 was admitted;
input/result and the pre-fix source are preserved in
`outputs/sequential-schema-prework-001/defect-reproduction.json` and `source/`.

The registry now requires an exact dictionary schema, `type(value) is bool`, string
types for every identity/coordinate/source field, and the existing canonical SHA256
record digest to equal one of the two frozen references. It rejects extra/missing
fields, integers0/1, floats0.0/1.0, null, strings, arrays and objects in the value
field. Invalid coordinate/identity types also reject. Valid Booleanfalse records
remain admissible; Booleantrue is correctly rejected as an unregistered value.
No production code or scientific criterion changed in this fix; the protocol hash
above remains unchanged. No revised protocol or new experiment was introduced.

Forty-six added regression cases cover malformed records/types and exact keys,
receiver-level unchanged support/lineage after numeric rejection, valid Boolean
admission, fresh-transport retransmission, and integer reuse of an admitted Boolean
evidence ID. Existing real process restart tests remain in the targeted suite.
**109 targeted tests passed in6.87s;697 actual-checkout tests passed in137.74s**, with
zero failures/skips. Fresh study `outputs/sequential-correction-002/` passed126/126
checks. Three interpreter PIDs29576 ->29684 ->10668 loaded the chained stages;
complete source archive181 files and full continuous/restarted traces are retained.

All metrics and every stage prediction exactly match run001. Direct inspection of
both final-state archives confirmed that all eight admitted late records across
the two runs contain actual Booleanfalse values. Thus the original valid-Boolean
findings remain supported; the prior registry's malformed-input rejection boundary
was defective and is not retrospectively claimed correct. Memory equivalence,
wrong control prediction, late abstention and all prior limitations remain.

Before updating this report/handoff, only the harness and its tests differed from
the181-file pre-fix source snapshot. All5,788 prior sequential artifact files retained
their hashes, including the original run and every earlier test/failure artifact.
All907 older action/seed files and3,043 historical-baseline files also retain hashes.
Evidence: `outputs/sequential-schema-verification-001.json` and
`outputs/sequential-schema-historical-preservation-001.json`. Prior dirty work was
preserved; HEAD remained90c1b84. No source manifest migration or runtime integration.

Exact commands for this successful follow-up (paths now reserved; use fresh paths
for future runs):

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -m pytest -q tests/test_sequential_correction.py tests/test_action_correction.py --basetemp outputs/sequential-schema-targeted-001 --junitxml outputs/sequential-schema-targeted-001.xml
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/sequential-schema-context-001.json
.\.venv\Scripts\python.exe experiments/run_sequential_correction.py --output outputs/sequential-correction-002 --preservation-context outputs/sequential-schema-context-001.json
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/sequential-schema-full-regression-001 --junitxml outputs/sequential-schema-full-regression-001.xml
```

Stopped for review after the focused fix; no next study or runtime integration began.
