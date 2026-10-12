# Existing Clarity contribution under competing questions — results

The unchanged Clarity->Execution contribution changed question ranking, but reduced
newly resolved questions in three of ten authored cases. Final decisions tied in
every case. An equally equipped scalar-memory comparator matched exact scores,
actions and predictions. This establishes a bounded causal ranking effect and a
utility limitation; it provides no evidence of semantic understanding or advantage
over ordinary structured memory.

## Frozen scope and method

[Protocol v1](SEED_CONTRIBUTION_PROTOCOL.md) was frozen before evaluation, including
all cases, outcomes and expected limitations. Protocol SHA256:
`ccc04722d6b00986fc671e9d8a4eb151af993de68255f214e24153e57cce3950`.
Starting HEAD: `e61372e86e2b804ab53012d6de006ed7a401663b`; checkout initially clean.
Only experiment code, tests and handoff documentation were added/edited. Production
code, canonical seed40, numerical parameters, model configuration and migration
were unchanged. No inference, model/mock calls, dependencies or fresh learning.

[Harness](run_seed_contribution.py) reuses existing consistent_attention selection,
support, prediction and its existing no-Clarity mode. The ablation disables only
the existing Clarity->Execution edge; direct activations and every other edge match.
Existing initializer weights A=.25/B=.75/D=.5 remain frozen. Eight existing authored
contextual outcomes reconstruct historical branch counters +1/3 and -1/3; this is
explicit replay, not an imported learned checkpoint or new association learning.

Each case permits at most one selected-field verification. Accepted contradictory
records remain append-only and unresolved; added corroboration cannot repair them.
All forty predictions freeze before any outcome scoring. Child PID3136 loaded
the persisted prior and explicitly ordered public-case snapshot, producing exact
canonical-JSON parity with uninterrupted evaluation. This is standalone process
reload, not a supervised inbox/outbox runtime integration.

The scalar baseline applies identical public inputs, support/conflict/relevance
gates, tie rule, reply budget and final predictor. Exact circuit reduction:
`clamp(.25*(w+.3125-coverage-resolved+inconsistent),0,1)`; ablation removes only
`inconsistent`. The .3125 term follows the existing two-pass Theory contribution.
Names such as Clarity and Fact do not establish learned meanings. Features, route
weights and candidate IDs are authored experimental inputs.

## Results

Each condition covers ten scenarios with two relevant questions each and at most
one query per scenario; eight requests were issued per condition. Newly resolved
questions count false-to-true transitions of complete consistent support, separately
from decision correctness.

| Condition | Requests | Newly resolved questions | Sum of part-coverage gains | Decisions / correct | Decision coverage / accuracy |
| --- | ---: | ---: | ---: | --- | --- |
| Intact circuit | 8 | 4 | 4.5 | 4 / 3 | 40% / 75% |
| Existing Clarity ablation | 8 | 7 | 7 | 4 / 3 | 40% / 75% |
| Scalar memory, intact | 8 | 4 | 4.5 | 4 / 3 | 40% / 75% |
| Scalar memory, ablated | 8 | 7 | 7 | 4 / 3 | 40% / 75% |

In x1/x2 the intact selector prioritizes inconsistent shield evidence over missing
payload evidence; x3 provides the symmetric payload-conflict case. These requests
do not resolve the conflict, whereas ablation resolves the competing question.
Thus three utility hurts and zero helps occur. x4 verification is non-resolving in both conditions;
x5 tests a tie; x6/x8 test useful replies; x9 is already resolved; x10 lacks the
independent-conflict gate. x7 retains an incorrect inherited success prediction.
No acceptance criteria, outcomes, contradiction policy or score were changed to
improve these results. Part-coverage gain measures acquired information, separately
from decision coverage. Neither ranking changes nor additional resolved questions
changed final decisions here; those require both relevant questions resolved.

## Verification and preserved attempts

Final `outputs/seed-contribution-003/`: **222/222 integrity checks** passed, including
frozen case expectations, unchanged weights/counters/prior records, contradiction
retention, one-query bounds, action parity, actual process reload and complete
171-file source/config/context archive checks. **588 checkout tests passed**,
including 14 new experiment tests. Tests check exact scores, single-edge ablation,
oracle isolation, attainable support combinations across all three existing
weights, downstream results and explicit persisted case ordering.

Two full-suite invocations accidentally reused the same `--basetemp
outputs/seed-contribution-full-regression-001` and XML path. First command record
`exec-8f4e5de7`: 588 passed in 132.33s. Second `exec-21838678`: 588 passed in
136.35s. Both command/summary records remain in task history. Pytest clears reused
basetemp and overwrites XML; the CURRENT raw artifact tree and
`outputs/seed-contribution-full-regression-001.xml` belong to the second run.
Separate copies of the first full-suite raw artifacts were not retained. No further
rerun or reconstruction was made. This limitation does not affect the three distinct
primary experiment archives below.

Attempt001 passed 222 checks but reconstructed child case inputs rather than loading
the persisted public snapshot. Coordinator implementation review identified that
scope gap; it remains preserved and is superseded by003. Attempt002 loaded persisted
inputs but JSON lexical key order placed x10 before x2; exact restart comparison
failed (221/222). Its failure remains preserved. Explicit case_order fixed execution
order without changing scientific cases or expectations. No primary attempt was overwritten.

Separate historical audit `outputs/seed-contribution-historical-audit-001.json`
passed 83 archived sources, 134 protected files and 137 original tree files. All 3,043
files in the prior immutable-archive baseline retain their hashes. Local evidence
is not an external backup or authentication. Existing runtime physical-budget
limitations and previous experiment errors remain unchanged.

Final archive contains configuration/provenance, frozen prior and public inputs,
frozen predictions, full circuit/scalar traces, selected replies, final ledgers,
restart evaluations, results and original source/context. Outputs are ignored by
Git and must be preserved separately. Handoff edits occur after evaluation and
regression; the archived source context describes the evaluated checkout.

## Reproduce

From the repository root, choose fresh output/context paths and unique regression
artifact paths for every invocation:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/seed-context-new.json
.\.venv\Scripts\python.exe experiments/run_seed_contribution.py --output outputs/seed-new --preservation-context outputs/seed-context-new.json
.\.venv\Scripts\python.exe -m pytest -q tests/test_seed_contribution.py
```

This bounded experiment is complete and stopped for coordinator review. No roadmap
step2, chat demo, semantic mechanism, transaction redesign or later task is dispatched.
