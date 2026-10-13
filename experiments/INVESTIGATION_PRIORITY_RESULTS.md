# Investigation priority — engineering comparison results

2026-10-13. Awaiting independent review. This bounded comparison makes a provisional
policy choice inspectable; it does not learn a policy, choose a permanent default,
measure longer-term information value or establish a seed advantage.

Current and target-resolution-oriented selection behave identically on the six
executable cases. Final-support-gate-oriented selection saves the r9 request but
leaves its shield question unresolved. No controller improves final decisions or
correctness. The x2 decision-only probes expose information that a resolution
preference would forgo. These findings do not select a universal winner.

## Frozen method and meaning of feasibility

[Protocol v1](INVESTIGATION_PRIORITY_PROTOCOL.md) was pinned before implementation,
tests and evaluation at `outputs/investigation-priority-prework-001/protocol-pin.json`.
SHA-256: `1a3cd48bb1351f7307373c139404a189b8bbc30f24f867d8bd8b50139b541f1a`.
[Comparison and annotator](run_investigation_priority.py) are experiment-local.
All existing production, seed/numerical/model configuration and dependencies stay
unchanged. No model calls, learning, runtime integration, new service or default.

Existing preflight, positive priorities and action-ID ties apply to all selectors.
Target selection additionally requires a target-resolution witness. Final selection
requires a witness satisfying both support prerequisites (including payload true)
and an existing downstream branch judgment that actually produces a decision.
The direct/scalar counterpart of each selector receives identical information and
matches its selections and outcome vectors exactly.

The annotator enumerates the public Boolean EFFECT ENVELOPE: all assignments to
missing gathered parts, or either Boolean value at the one active correction
target. It uses effective scoped heads and the existing equal/complement relation.
Other heads and coordinates stay fixed. This is an overapproximation of admissible
replies, not enumeration of actual authorized payloads. Exact opaque permits and
private verification may admit only one value or reject the operation entirely.
No proposal, actual replacement, verification or outcome helper is accessed by
annotation/selection, and no payload hash is inverted.

`possible` means a structural witness conditional on admission; admission remains
`unknown`. `ruled_out` means even this complete Boolean envelope contains no witness,
for this snapshot and operation. Unsupported domains/operators/relations return
`unknown`, not a proof of impossibility. No primary eligible case needed that fallback.
Neither information gain nor success is guaranteed. Actual rejected or unavailable
actions remain possible and do not count as successful-effect witnesses.

## Executable cases: controller-by-case results

Each cell applies equally to circuit and scalar selection. C=current, T=target,
F=final. One lifetime request per case, no refund/retry. Preparation is shared.

| Case | C / T action | F action | New coverage; admitted records | Newly resolved questions C/T/F | Final result, all controllers | Remaining uncertainty |
| --- | --- | --- | --- | --- | --- | --- |
| r2 | Gather shield check2 | Same | +0.5; 1 | 1 / 1 / 1 | success, correct | Both questions resolved |
| r4 | Correct shield check1 | Same | 0; 0 | 0 / 0 / 0 | abstain | Repair rejected; shield conflict remains |
| r8 | Correct shield check1 | Same | 0; 1 | 1 / 1 / 1 | success, **wrong** | Support resolved, but not reliable world truth |
| r9 | Correct shield check1 | No request | C/T: 0; 1. F: 0; 0 | 1 / 1 / 0 | abstain | C/T: payload missing. F: payload missing and shield conflict |
| r10 | No request | Same | 0; 0 | 0 / 0 / 0 | inherited success, **wrong** | Resolved support does not establish correctness |
| r12 | Gather shield check2 | Same | +0.5; 1 | 0 / 0 / 0 | abstain | New part known, shield conflict now present |

All actual non-no-op actions target one question, so target-resolution counts equal
new-question counts here. Full per-coordinate values, remaining missing parts,
inconsistency, selection traces, receipts and immutable evidence are in `results.json`.

r9's two eligible offers both have score 0.265625. C/T chooses correction by action
ID; payload gathering is also annotated target-possible. Neither action alone can
meet final prerequisites. The tie-sensitivity test renames an action and obtains
gather selection; the main evaluation does not execute that renamed counterfactual.
r4 demonstrates possible effect versus failed verification. r12 could structurally
resolve if check2 matched check1; the actual contrary arrival does not. F cannot
avoid these failures without future information. r8 retains the known wrong answer.

| Per six-case controller | Requests | Gather attempts / returned records / checks | Correction attempts / proposals / checks | Admitted records | Newly covered parts / summed coverage | Questions resolved | Correct / wrong / abstain |
| --- | ---: | --- | --- | ---: | --- | ---: | --- |
| Current | 5 | 2 / 2 / 2 | 3 / 3 / 3 | 4 | 2 / 1.0 | 3 | 1 / 2 / 3 |
| Target | 5 | 2 / 2 / 2 | 3 / 3 / 3 | 4 | 2 / 1.0 | 3 | 1 / 2 / 3 |
| Final | 4 | 2 / 2 / 2 | 2 / 2 / 2 | 3 | 2 / 1.0 | 2 | 1 / 2 / 3 |

Scalar counterparts reproduce these vectors. Across six controllers there are 36
case executions and 28 logical requests, with 12 gather and 16 correction checks.
The r2 preparation correction/check/replacement is executed once in shared bundle
construction and excluded from action totals. These are logical authored work
counts, not CPU/latency costs or independent statistical samples. Verification may
reuse the pure fixture service helper. There is no composite utility score.

## x2: decision-only information-sacrifice probe

Original archived initial observations and public case/prior are read from
`outputs/seed-contribution-003/`. New descriptors advertise only the missing parts;
no correction permit, x2 service, receiver execution or incompatible reply replay
is introduced. `x2-decision-only-input.json` records this explicit construction.

| Offers | Current | Target | Final |
| --- | --- | --- | --- |
| Shield check2 and payload check1 | Shield gather | Payload gather | No request |
| Shield check2 only | Shield gather | No request | No request |

Shield check1 already has false and true. Adding any value for check2 cannot resolve
shield, but can reveal its missing value. Payload can potentially resolve, while
shield remains conflicted. No observed x2 action metrics or outcomes are reported:
these are annotation/decision probes only. The shield-only perturbation demonstrates
that resolution preference can forgo missing-part information. Its possible later
use is unmeasured, so the gather is not called universally useless.

## Validation, chronology and preservation

First focused run: **179 passed**, including **137 new tests**. Independent annotation
validation covers all 64 empty/singleton/conflicting assignments to the three parts
under both equal/complement relations (128 cases), comparing every eligible gather
and active-target replacement against a separate list-based Boolean truth table.
That oracle does not call production support/predict/normalization or the annotator;
it independently checks payload truth and branch thresholds. Other tests cover
superseded heads, multiple roots, foreign scope, undetermined branches, duplicates,
ordering, unknown relation, future-access rejection, genuine ID ties, receiver
preservation and pending/closed budget reuse. Shared annotation across scalar
controllers alone is not treated as annotation validation.

Primary `outputs/investigation-priority-001/`: **331/331 integrity checks** pass.
All selections are persisted before selected service calls; predictions are persisted
before existing outcome labels are scored. **1,113 full regression tests pass in
220.23 seconds**. No failed focused, primary or full run occurred in this comparison.
The terminal demo remains retired; its 20 retired tests are not reintroduced.

Prework archive: 232 exact files. Evaluated archive: 234 exact files. All 232 existing
prework source/config hashes matched before reporting. Preservation reverified
135,271 prior-output hashes and 10,564 context-study artifact hashes, with no mismatch
(`outputs/investigation-priority-preservation-001.json`). Later handoff edits are
separately archived; historical results, wrong outcomes and failures are unchanged.
Starting/current HEAD: `583071f857a9912c83ac06429dca0fe9d67e8aa1`; no commit made.
Outputs are Git-ignored local recovery evidence, not an external backup. Old
checkpoints still require their matching archived production/config snapshot;
no manifest relaxation or migration occurred.

Evaluated source-manifest SHA-256:
`7336177faba35ac3c0de4be7214a408ed9ffc933d09e17430b6722e23b456453`.
Results SHA-256:
`cab6bcecf7a786e819e660e1d8177b56ec936129c802c1643d32786eb4e5818a`.

## Reproduction and decision boundary

From the repository root with Python 3.12, choose a genuinely fresh output path:

```powershell
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
.\.venv\Scripts\python.exe experiments/run_investigation_priority.py --output outputs/investigation-priority-reproduction-001 --protocol-pin outputs/investigation-priority-prework-001/protocol-pin.json
```

The CLI rejects an existing output directory and a changed protocol pin. It requires
the preserved x2 archive. Newly generated wall-clock provenance may differ; compare
selection/annotation and outcome vectors, not entire runtime-state byte equality.

The user's provisional preference is now expressed as a reversible comparison,
not a changed default. Current/target parity on known executable cases and the
x2 information sacrifice do not justify a learned selector or permanent policy.
No held-out or longer-term benefit was measured. Stop for independent review;
no next experiment, implementation or task is dispatched.

## Corrective addendum v1 — guard unsupported values before support (2026-10-13)

**Initial independent review blocked acceptance on an experiment-local contract
defect. Corrective re-review is pending.** The positive known-domain findings above
remain preserved in Run001 and the exact pre-fix report/source snapshot. Reviewer
independently reproduced 179 focused tests and 331 checks; inspected the 1,113-test
full-suite XML rather than rerunning it; verified 234 evaluated/232 prework sources,
135,271 prior hashes, 10,564 context artifacts and 57 production/config/dependency
files. This did not validate the unsupported-domain boundary.

Reviewer supplied active evidence values `[false]` and `{"value": false}`. Original
`annotate()` reached support's set construction through preflight before checking
the domain, raising TypeError instead of returning unknown. `choose()` likewise
called selection before annotation. Inputs remained unchanged; null, integer zero
and a string reached the later annotation check and returned unknown. The exact
negative probe is retained at
`outputs/investigation-priority-fix-prework-001/reviewer-unsupported-domain-probe.json`.

The correction touches only the experiment runner and its tests. A raw-value guard
now runs before preflight, normalization, support or priority selection. Direct
annotation returns unknown with no witnesses. Selection returns no action, explicit
unknown diagnostics and null scores; it does not invent a zero priority or Boolean
value. The original conservative domain boundary is preserved: every active record
in the current case/scope must be strictly Boolean, including unrelated fields in
that same case/scope. Foreign case/scope records and superseded records remain
outside that effective-domain check. This is a value-domain guard, not a general
validator of arbitrary corrupt ledger/head schemas. Genuine false/true conflicts
remain admissible input to structural analysis and are never coerced or erased.

Fifty added tests cover lists, dictionaries, null, integers 0/1, strings, floats,
missing values, relevant/other-question/same-scope unrelated fields, normalization
coordinates, foreign case/scope and superseded records. Direct annotate and all six
choose variants are exercised; patched support/preflight/selection sentinels prove
malformed active values cannot reach those functions. Inputs stay unchanged.
The original independent Boolean truth table and valid-domain tests remain intact.

**229 focused tests and 1,163 full regression tests pass** (full run 216.47 seconds).
Fresh `outputs/investigation-priority-002/` passes **331/331** checks. Compared with
Run001, predictions, vectors, checks, x2 inputs/decision probes and complete result
rows match exactly, excluding only outbox wall-clock timestamps. No scientific
criterion, valid-domain selection, receiver, budget or production policy changed.
Parity evidence: `outputs/investigation-priority-fix-parity-001.json`. A fresh
five-value direct probe records unknown annotation and all 30 controller choices
with unchanged inputs in `outputs/investigation-priority-fixed-domain-probe-001.json`.

Pre-fix snapshot contains 235 source/config files; Run002 archives 235 evaluated
files. Before handoff changes, only runner and test hashes differed from pre-fix.
Original Run001 result hash and all 234 archived source hashes still verify. No
original successful result, historical failure or reviewer-negative probe was
rewritten. Corrective focused, primary and full runs passed on their first attempts.
The original protocol pin is unchanged; the implementation repair fulfills its
existing unknown-domain contract. No model calls, dependencies, protected changes,
runtime integration, commits or broader work.

Run002 source-manifest SHA-256:
`3c9418272d01aa51de5db5a358f271101ece89cc147ec8532e42d3b08f1191a2`.
Run002 results SHA-256:
`a7dd55f8bef2124fce2e7942aa0396ec0e7f0fdf87e1a6b2e27ec2447ff18a55`.
Runner SHA-256:
`6a6dc76385889eb63828358298285f97138197b4987f471b576869648894329a`.
Focused test source SHA-256:
`c984998ed15a5faf27aeaf6718bbf31ab9c3c3770e0dc1017c903a928f00f943`.

Use the same reproduction command above with another fresh output path. Final
handoff and the retained read-only r8/r10 diagnosis are at
`outputs/investigation-priority-fix-handoff-001/`. That diagnosis found no prediction
code/contract inconsistency: r8 retains a limited historical branch's exception;
r10 admits fallible agreeing reports and refuses an audit because support is already
resolved. It does not authorize retuning, new labels or another controller. Stop
for independent re-review; no follow-on implementation is dispatched.


## Accepted independent corrective review (2026-10-13)

Parent accepted the comparison and narrow domain-guard fix. Independent reviewer
reproduced 35 direct malformed-domain probes with sentinel guards, 229 focused tests
and 331 comparison checks; known-case outputs remained unchanged except timestamps.
Reviewer verified pre-fix, original evaluated and corrected source hashes, unchanged
protocol and 57 unchanged production/configuration/dependency files. The 1,163-test
full-suite XML was inspected, not independently rerun. Earlier positive results,
review-blocking negative evidence and corrective chronology above remain preserved.
Acceptance covers the bounded engineering comparison and its repaired contract;
it does not choose a default, establish learned utility or authorize runtime changes.
