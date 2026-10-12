# Neutral attribute binding - results

2026-10-12. A bounded learner selected which neutral numeric channels to compare
after one informative observation separated two initially viable operand bindings.
Coverage rose from25/37 to37/37 held-out cases; accuracy among decisions stayed100%.
An independently implemented ordinary-memory learner matched all scientific state,
query choices and predictions. This removes an authored operand-binding assumption
within a supplied finite family. It is not linguistic category acquisition, causal
understanding, autonomous concept admission or evidence of a seed/fuzzy-tree advantage.

## Frozen scope and implementation

[Protocol v1](ATTRIBUTE_BINDING_PROTOCOL.md) was frozen and hashed before evaluation:
`b1724989ab0c92bf6d78050f056702c3e811d96dfd9ac829d4e6a3bde48f40e7`.
Starting HEAD `341b4c8281847fcf676e9aa5fa9f837de159065b`, initially clean. This follows
the owner's foundations-first instruction; session ceiling18:40 UTC, then stop for
independent coordinator review. No later task is dispatched.

Existing capacity learning hardcodes length/capacity operands and chooses an operator.
This isolated schema exposes a,b,c in0..3 and supplies36 representations: six ordered
distinct operand pairs x six comparison operators. Grouping by complete candidate
prediction vectors gives18 behavioral classes, each with two reversed equivalents.
Those vectors are candidate predictions, not oracle evaluation labels. Class IDs,
query order, evidence IDs, public metadata and learner directories contain no world
mapping. Class voting counts equivalents once. The fixed seed is not used in this
experiment; no decorative activation is credited as a cause.

Files:

- [Public schema/family/pools](attribute_binding_contract.py).
- [Primary explicit-relation learner](attribute_binding_primary.py).
- [Independent ordinary-memory comparator](attribute_binding_memory.py): comparison
  signs produce truth-table masks; bit constraints filter candidates, and independent
  table-voting code selects queries and predicts. It never calls primary evaluation,
  elimination, selection or prediction functions. Shared schema, admission, storage
  and lifecycle are disclosed; this is not two names for one decision implementation.
- [Strict admission/checkpoints](attribute_binding_engine.py),
  [coordinator-only oracle/evaluator](attribute_binding_oracle.py),
  [restricted-import worker](attribute_binding_worker.py),
  [study/reproduction entry point](run_attribute_binding.py),
  [focused tests](../tests/test_attribute_binding.py).

Production contracts and all existing source files were unchanged before final
documentation handoff. New modules are confined to experiments/tests. The independent
device outcome comes from unchanged capacity_fixture.execute. No model calls, teachers,
new seed nodes, numerical changes, model configuration changes, dependencies or servers.

## Identifiability and information boundaries

Four training events make distractor=length, while including equality and both
outcomes. Thus strict operators are already eliminated but either of two channels
can be the operand compared with capacity. The mapping is held only by the coordinator
oracle/evaluator; workers receive neutral observations and verified outcomes. The six
permutations are symmetry checks, not six independent replications.

The full query pool is every neutral triple in0..2, lexicographically ordered without
mapping or outcome access. Query score is true-class-votes * false-class-votes; ties
use the first maximum-positive point. A selected request immediately spends the one
lifetime budget. Noninformative control explicitly chooses the first zero-score point;
unavailable control offers only diagonal triples; no-acquisition requests nothing.
Already-supported control trains on all27 neutral0..2 triples and needs no query.

Training and the one authorized acquisition can eliminate candidates. There is no
separate validation phase and no production acceptance/deployment in this diagnostic.
Evaluation never filters or invalidates a family. All pre/post predictions across
all60 arms were frozen to disk before any held-out scoring; pre-acquisition predictions
were also stored before the selected reply was obtained. Held-out features are the37
triples in0..3 containing at least one3, disjoint from all training/query features.

Strict worker requests reject hidden mapping/evaluation-label fields, including nested
evidence extras, before producing a checkpoint. Oracle imports are blocked in workers.
Admission rejects malformed values, Boolean/integer aliases, unverified records,
wrong source/phase/query, conflicting IDs, and held-out features even with a synthetic
receipt. Duplicates add audit receipts, but no evidence, learning or budget charge.
Synthetic receipts are trusted local digest attestations, not cryptographic identity
authentication against a hostile process with filesystem access. This is an inspected
information-flow boundary, not an OS sandbox or claim that arbitrary malicious learner
code could not read coordinator files.

For each of four ambiguous policies and both implementations, swapping hidden length
and distractor produces identical serialized training requests. All24 paired checks
produced identical complete learner state, query selection and predictions before
informative evidence. The acquired labels then separate the appropriate bindings.
Directory UUIDs are opaque and have no semantic encoding; science is deterministic.

## Results and denominators

The following counts hold separately for **each of the six permutations and both
implementations**. Full per-arm classes, selected query, before/after wrong and abstained
IDs, denominators and metrics are in `outputs/attribute-binding-001/results.json`;
the60 detailed subset evaluations are in `evaluator/scores.json`.

| Condition | Classes before -> after | Charged queries | Decisions before -> after /37 | Correct/decided after | Wrong after | Abstentions after |
| --- | --- | ---: | --- | --- | ---: | ---: |
| Informative | 2 -> 1 | 1 | 25 -> 37 | 37/37 | 0 | 0 |
| No acquisition | 2 -> 2 | 0 | 25 -> 25 | 25/25 | 0 | 12 |
| Noninformative | 2 -> 2 | 1 | 25 -> 25 | 25/25 | 0 | 12 |
| Unavailable | 2 -> 2 | 0 | 25 -> 25 | 25/25 | 0 | 12 |
| Already supported | 1 -> 1 | 0 | 37 -> 37 | 37/37 | 0 | 0 |

Informative coverage is67.57% ->100%; the three ambiguous controls remain67.57%.
Already-supported coverage stays100%. Accuracy is100% on the decided subset at both
stages in every arm: **this is increased coverage, not an accuracy improvement**.
The12 abstentions in each ambiguous control are retained negative outcomes for full
identification; no tie was secretly resolved. Blanket abstention would fail both the
supported control and the25 consensus cases available before acquisition.

Represent each behavioral class by its <= member; its reversed >= member remains
in the archived public class catalog. The acquired classes are:

| Oracle permutation index (evaluator only) | Initial classes | Informative query channels / ID | Final class |
| ---: | --- | --- | --- |
| 0 | a<=b, c<=b | [0,0,1] / q001 | a<=b |
| 1 | a<=c, b<=c | [0,1,0] / q003 | a<=c |
| 2 | b<=a, c<=a | [0,0,1] / q001 | b<=a |
| 3 | a<=c, b<=c | [0,1,0] / q003 | b<=c |
| 4 | b<=a, c<=a | [0,0,1] / q001 | c<=a |
| 5 | a<=b, c<=b | [0,0,1] / q001 | c<=b |

Both implementations give exactly this table. Controls retain the initial classes;
already-supported starts with the final class. Noninformative always queries q000
[0,0,0], repeating a training feature point with a separate event ID and no new
distinguishing information. No-acquisition/unavailable/supported select nothing.

Every informative/supported arm correctly decides all7 equality cases, all22 success
cases and all15 failure cases. For seven held-out length/capacity pairs, all four
distractor values are present and decisions are invariant. Nine remaining pairs have
only one held-out distractor value; no within-pair invariance claim rests on those
singletons. The fixed family contains the noiseless simulator's rule; zero errors
here do not establish robustness to sensor noise, misspecification or new concepts.

## Persistence, comparison and tests

Primary run: **1,125/1,125 integrity checks**,60 arms,180 actual worker subprocesses.
Each arm checkpoints after training/query selection, restarts to admit acquisition,
then restarts again for read-only evaluation. Complete states match uninterrupted
transitions, including evidence, class counterexamples, rejection reasons, selected
query and spent budget. Evaluation checkpoints are unchanged. All worker return codes
are0 and per-arm child PIDs differ from one another and the coordinator. No model calls.

There are24 charged worker-arm queries:12 informative and12 noninformative. The
uninterrupted comparison separately replays the same transitions and observations;
it does not obtain extra oracle information. The targeted reproduction has4 charged
queries. These are per-arm logical observation budgets, not physical computation caps.

The competent independent memory implementation matches complete scientific state
and predictions in all30 permutation/control pairs, not just final accuracy. A test
replaces every primary decision function with an exception while memory still learns,
selects and predicts using freshly rebuilt masks. Empty-set behavior is separately
tested with contradictory trusted unit records: no vacuous prediction or query.
Those diagnostic records are not passed off as genuine primary simulator outcomes.

Focused tests passed twice: **20 in2.06s**, then **20 in2.24s** after strengthening
the nested-field worker boundary. The first210-file source snapshot is retained in
`outputs/attribute-binding-targeted-source-001/`; both targeted artifact roots/XMLs
remain. No evaluated study run failed and no scientific protocol criterion changed.
Final full actual-checkout regression: **778 tests passed in166.36s**, no errors,
failures or skips, under `outputs/attribute-binding-full-regression-001/` and its XML.

Targeted reproduction on permutation4: **192/192 checks**,10 arms/30 actual workers,
`outputs/attribute-binding-rerun-001/`. It matches the primary summary and all30 stage
checkpoint files byte-for-byte. The separate comparison passes33/33, including both
complete artifact manifests. This targeted rerun has no paired-world leakage test;
that remains covered by the full six-permutation run and focused actual-worker test.

## Archives, preservation and reproduction

Evaluated source/context:210 files; context002 SHA256
`59cc2d52cd565a8f9b0236244dae2a8ae60f5fe3a83b83a71f9f2a9701a1e568`.
`outputs/attribute-binding-001/` contains the source archive, public configuration,
all36 representations/18 classes, opaque learner directories with requests and three
stage checkpoints, public predictions, process receipts, privileged evaluator mapping
index and post-freeze labels/scores. `artifact-hashes.json` pins1,121 files, excluding
itself. Predictions SHA256:
`e020d923208d4c22cc57cdd3ab163aa20f3a7098da4058856f2e1e9660bd3b15`.

All201 preexisting source files matched prework hashes before final handoff. All59,465
captured prior output files and3,043 historical files remain unchanged. This includes
all19 files in the owner's `outputs/action-demo-20261012T150026-75a8489b/`. Separate
historical audit passed83 archived sources/134 protected/137 tree files, including56
entries resolved from pinned Git. See `attribute-binding-preservation-001.json`,
`attribute-binding-historical-audit-001.json`, and prework source/output manifests.
Original failed historical runs were neither removed nor reclassified. Final report
and handoff edits occur after evaluation; the evaluated source remains archived.

Recorded commands from the repository root (these paths already exist; use new names):

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/attribute-binding-context-002.json
.\.venv\Scripts\python.exe -m pytest -q tests/test_attribute_binding.py --basetemp outputs/attribute-binding-targeted-002 --junitxml outputs/attribute-binding-targeted-002.xml
.\.venv\Scripts\python.exe experiments/run_attribute_binding.py --output outputs/attribute-binding-001 --preservation-context outputs/attribute-binding-context-002.json
.\.venv\Scripts\python.exe experiments/run_attribute_binding.py --output outputs/attribute-binding-rerun-001 --preservation-context outputs/attribute-binding-context-002.json --permutation 4
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/attribute-binding-full-regression-001 --junitxml outputs/attribute-binding-full-regression-001.xml
```

Capture a fresh context for the current source; use the archived evaluated checkout
to reproduce its exact source pin. Existing output roots reject instead of overwriting.
No commits, pushes, publication or production migration were performed.

## Bounded conclusion and next question

The distinction between relevant and proxy operands can be selected from evidence
within this authored comparison family, retained across restart, and applied to new
numeric combinations without an LLM deciding the result. The family, measurement
channels, noiseless verification and training curriculum remain supplied. No language
meaning, novel primitive, learned seed interpretation or useful geometric contribution
was demonstrated; the simple memory solution is equally competent.

The smallest justified question is how much identification relies on training already
reducing uncertainty to exactly two behavioral classes: with more surviving classes,
what useful consensus remains after the same one-bit observation budget? This study
does not answer that question and does not authorize starting it. Stop for review.
