# Context-dependent measurement interpretation — results

Evaluation 2026-10-12; handoff 2026-10-13. **Completed; awaiting independent review.** Primary and independent
ordinary memory matched exactly. One fixed calibration opportunity increased correct
support decisions from **192 to 352 of 2,688**, with no wrong or unsafe resolutions.
Of the 160 additional correct decisions,96 were at the newly calibrated context and
**64 were at genuinely unobserved contexts**. Original-context behavior was unchanged.
Only 8 of 48 arms identified one hypothesis;40 remained ambiguous. No seed/propagation
participation, accepted-global-belief revision or architectural superiority is shown.

## Frozen contract and implementation

The parent approved the [original draft](CONTEXT_APPLICABILITY_PROTOCOL_DRAFT.md),
SHA-256 `33d7dfcc5daee064b8508f0d02b2cd99a35cfe658493e8e4310c263d5d51b8b2`.
It remains byte-identical. [Final protocol v1](CONTEXT_APPLICABILITY_PROTOCOL.md)
was pinned at **2026-10-12T23:43:27.950000+00:00**, before evaluation:
`8b16c1e2f43d5593dea56de3bfc0f25c761ba461d3d5490cb3e636defb0223a2`.
Pin: `outputs/context-applicability-prework-001/protocol-pin.json`.
This is local recorded provenance, not an external timestamp/authentication service.

Six supplied mappings `{0,1,c0,not c0,c1,not c1}`, two neutral context bits, six
private wiring worlds, four fixed schedules and two value flips produce 48 arms.
Every arm receives initial calibration at 00 and one subsequent opportunity at 10,
11,00, or unavailable at 10. No adaptive selection, retries or family repair.
Calibration constrains `v XOR h(c)=z`. The reference is a commanded synthetic bit;
separately configured wiring supplies raw v. Stable noiseless wiring and a correct
reference are fixture assumptions, not demonstrated real-world independence.
First-measurement orientation, family, evidence gates and budget are authored.
Only candidate elimination/applicability is learned from admitted calibration.

All production source/configuration stayed byte-identical. New experiment-local files:

| File | Role |
| --- | --- |
| [contract](context_applicability_contract.py) | Public family, strict schema, shared support gates and pins |
| [primary](context_applicability_primary.py) | Explicit expression evaluation, filtering and consensus |
| [ordinary memory](context_applicability_memory.py) | Independent truth tables, bit-mask filtering and voting |
| [engine](context_applicability_engine.py) | Admission journal, witnesses, phase/budget checks and replay validation |
| [worker](context_applicability_worker.py) | Fresh-process lifecycle and parent-pipe reference verification |
| [private device](context_applicability_device.py) | Commanded reference, wiring and fixed evaluation cases |
| [runner](run_context_applicability.py) | Matrix, comparisons, archives and outcome scoring |
| [tests](../tests/test_context_applicability.py) |115 boundary, realizability, independence and restart cases |

Memory never calls primary filtering/evaluation/prediction; poisoning those functions
does not break memory. Shared schema, admission, support sufficiency gate and storage
are intentional and disclosed. Workers receive no wiring/world/relevant-cue labels or
registry paths. Verification requests get a strict Boolean registry response. Hidden
assignment stays with the coordinator. Import restrictions/dataflow tests enforce the
intended local boundary; they are not a hostile-filesystem security sandbox.

## Outcomes and denominators

Each controller/stage has 48 arms x 56 support cases =2,688 cases. The56 comprise
four contexts x two targets x seven fixed templates. Complete and duplicate-complete
templates are resolvable under the correct mapping; the other five intentionally
exercise disagreement, contradiction or missing/foreign support. Identity-renamed
copies and integrity probes are excluded from these denominators. Duplicated records
do not count as independent evidence; symmetry/template cases are not independent
statistical replications. Abstention is never counted as correct.

| Controller | Stage | Correct | Wrong | Abstained | Unsafe resolutions |
| --- | --- | ---: | ---: | ---: | ---: |
| Primary / independent memory (each) | Before |192 |0 |2,496 |0 |
| Primary / independent memory (each) | After |352 |0 |2,336 |0 |
| Frozen pre-follow-up | Before / after |192 |0 |2,496 |0 |
| Constant equality | Before / after |384 |192 |2,112 |192 |
| Global replacement | Before / after, aggregate |512 |128 |2,048 |128 |

Primary/memory coverage rises7.14% ->13.10% over the entire stress grid, at 100%
accuracy among emitted bits. On the 768 oracle-resolvable complete/duplicate cases,
correct coverage is192/768 ->352/768 (25% ->45.83%). This restricted denominator
is reported separately, not substituted for the frozen full grid.
Constant equality emits more answers but only 384/576 (66.67%) are correct; global
replacement512/640 (80%). No loss function was prescribed that trades wrong
answers against abstention, so these numbers do not establish blanket utility
superiority. Their unsafe resolutions occur when the wrong mapping makes an
actually cross-disagreeing pair look consistent. Within-part contradictions remain
unresolved in every controller; complementing `{0,1}` never removes them.

### Retention, genuine transfer and calibrated-context application

Retention tests fresh records at 00 (672 full-grid cases,192 oracle-resolvable).
Primary/memory retain192 correct,0 wrong and 480 abstentions before AND after.
Global replacement changes192/0/480 to 144 correct/24 wrong/504 abstained: aggregate
success conceals original-context losses. Constant equality stays96/48/528; frozen
stays192/0/480. These are actual outcomes, not forced expected control failures.

Genuine transfer excludes every context appearing in admitted calibration: P10
uses01/11; P11 uses01/10; P00/U10 use01/10/11. There are 1,680 full-grid transfer
cases,480 oracle-resolvable cases.

| Controller | Before: correct / wrong / abstained | After: correct / wrong / abstained |
| --- | --- | --- |
| Primary / memory (each) |0 /0 /1,680 |64 /0 /1,616 |
| Frozen |0 /0 /1,680 |0 /0 /1,680 |
| Constant equality |240 /120 /1,320 |240 /120 /1,320 |
| Global replacement |272 /104 /1,304 |272 /104 /1,304 |

Thus primary transfer is64/1,680 full-grid coverage (3.81%), or64/480 (13.33%) of
oracle-resolvable transfer cases, with no wrong decisions. It occurs in the 8 fully
identified arms, not all worlds. The remaining96 additional primary correct
decisions are at the delivered nonzero calibration context (96/336 full-grid cases;
96/96 oracle-resolvable). They are application after calibration, not unseen-context
transfer. Original-context retention contributes none of the 160 gains.

### Non-beneficial and unresolved arms

Mapping-only probes total 192 context predictions per controller/stage. Primary/memory
change from 48 correct/144 ambiguous/0 wrong to 88 correct/104 ambiguous/0 wrong.
Afterward8 arms have one survivor,16 have two,24 have three; none is unsupported in
the realizable primary worlds. The separate contradictory-calibration diagnostic
does become unsupported and remains so after restart.

Below are per-arm post-calibration support counts, each out of 56. Both value flips
and both polarity variants within each world pair have identical counts.

| World pair | Schedule | Survivors | Correct / wrong / abstained |
| --- | --- | ---: | --- |
| Always pass / always invert | P10 |2 |8 /0 /48 |
| Always pass / always invert | P11 |1 |16 /0 /40 |
| c0-high / c0-low switch | P10 |1 |16 /0 /40 |
| c0-high / c0-low switch | P11 |2 |8 /0 /48 |
| c1-high / c1-low switch | P10 or P11 |2 |8 /0 /48 |
| Every world | P00 or U10 |3 |4 /0 /52 |

P00 and U10 have no prediction improvement. In particular, complement at 11 leaves
c0/c1 unresolved; equality at 10 leaves 0/c1 unresolved. No additional request or
reinterpretation rescued those outcomes. Complete per-world/schedule/flip/controller/
stage/category and per-template counts are in `outputs/context-applicability-001/results.json`.

## Integrity, restart, evidence and costs

**7,821/7,821 study integrity checks**, **115 targeted tests**, and **976 full
regression tests** passed. Full regression:225.29s. There are 240 controller
individuals, each with three actual fresh worker processes: **720 invocations**.
Initial and post-opportunity checkpoints match uninterrupted execution; final
read-only reloads preserve every checkpoint byte. All predictions were persisted
and hashed before scoring. Repeated evaluation preserves learning/evidence/budget.

Indistinguishable-history checks record200 controller/schedule/stage/history groups;
160 contain multiple hidden-world arms. All match in scientific state, receipts,
rejection witnesses, mapping predictions and the SAME16 public support probes.
Comparing identical inputs avoids pretending differing raw measurement grids should
produce identical outputs. Calibration value flips, support target flips and fixed
identity renaming pass separately; their repeats do not inflate scientific counts.

The tests include18 checksum-valid inconsistent copied-checkpoint actual restarts
that reject before writes: controller/config/family/source/launch mismatch, Boolean
substitutions, altered evidence, survivors, witnesses, phases and receipts. Both
primary and memory run the two-row empty-family diagnostic through three actual
processes, retaining all rejection witnesses and abstaining. A separate real-pipe
probe passes18/18 checks for malformed and unverified records, duplicate/conflicting
IDs, source/scope rejection, budget exhaustion and restart persistence:
`outputs/context-applicability-boundary-001/`. Its six processes are separate from
the 720 primary-study invocations. Test and diagnostic work is not primary evidence.

Per controller in one primary pass:48 initial admissions,48 charged follow-up
opportunities,36 follow-up admissions,12 unavailable opportunities and 132 duplicate
deliveries (zero added evidence/checks). Across the five controllers the actual
workers make420 reference-registry checks; uninterrupted comparison makes another420.
Calibration is generated once per shared arm:48 initial and 36 follow-up reference/
raw pairs. These calibration counts exclude evaluation-fixture construction/scoring,
tests and supplemental diagnostics. Logical requests, registry checks, fixture
generation and physical external sensing are different; no physical crash-proof
bound or real sensor execution is claimed. **Zero model inference calls.**

## Preservation, versions and reproduction

Starting HEAD `583071f857a9912c83ac06429dca0fe9d67e8aa1`; the terminal-demo retirement
and draft/handoff were already uncommitted. No discard, commit, push or publication.
Prework archived220 files. Before results/handoff edits, all 220 matched and all
**135,271 pre-existing output files** retained their hashes, including the owner's
original19 demo files. All 57 production/config/dependency files are unchanged.
Evidence: `outputs/context-applicability-preservation-001.json` and prework hashes.
No historical protocol, failure or result was edited or deleted. No external backup
was verified; local `outputs/` archives are Git-ignored.

Primary evaluated archive: `outputs/context-applicability-001/`,229 source files.
Source-hash manifest SHA-256:
`8129b21a8ec646a90fc81c8c8cc82269e2a1bb1b73d78822e1882f0be1888f25`.
Prediction-hash manifest SHA-256:
`28b9af447550ae8c5ac1100aeab798c78979a12fb9229cd3110271a656f8834b`.
Results SHA-256:
`e82411e9a99a68c7bb400e99ce6390a17d1f5cfcd89881da03f34fd9350d3700`.
Every file's exact source hash is in `source-hashes.json`; checkpoints pin relevant
experiment and production/parser sources, configs/dependencies and Python version.
Handoff edits follow evaluation and are archived separately; they are not retroactively
part of the evaluated229-file snapshot.

No evaluated attempt failed in this study. Targeted001/002/003 each passed 115 tests;
001/002 sources remain separately archived. Before primary evaluation,002 expanded
dependency pins;003 separated within-part contradiction from cross-part disagreement
in diagnostics and added explicit support-value symmetry checking. Frozen scientific
cases, family, criteria and protocol were unchanged. The final matrix and full suite
use the 003 implementation. All earlier targeted outputs remain present.

From the repository root in PowerShell, use unused paths exactly once:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
.\.venv\Scripts\python.exe experiments/run_context_applicability.py --output outputs/context-applicability-reproduction-001 --protocol-pin outputs/context-applicability-prework-001/protocol-pin.json
.\.venv\Scripts\python.exe -m pytest -q tests/test_context_applicability.py --basetemp outputs/context-applicability-review-targeted-001 --junitxml outputs/context-applicability-review-targeted-001.xml
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/context-applicability-review-full-001 --junitxml outputs/context-applicability-review-full-001.xml
```

The matrix is deterministic in public evidence and scientific state; opaque worker
directory nonces and OS PIDs vary and are not scientific inputs. The runner refuses
an existing output directory. Independent rerun has not yet been performed; the
reported restart/continuous comparison is writer-run evidence.

Final read-only system-wide CIM check at 23:57:17 UTC found no Python workers:
`outputs/context-applicability-worker-final-check-001.json`.
Stop for independent review. No further task is dispatched. The supplied six-member
family, reliable synthetic reference, finite contexts and shared support gates remain
major limitations; no general meaning learning, belief repair, propagation benefit,
philosophical interpretation, authentication or autonomous investigation is established.


## Accepted independent review (2026-10-13)

Parent accepted the study within its frozen scope. Independent reviewer reproduced
115 focused tests and 24 arms covering all worlds/schedules at flip0, five
controllers and 360 worker invocations: 3,937 checks plus 18 pipe checks. Reviewer
recounted the full traces: 352 correct/0 wrong/2,336 abstentions, 64 gains on
unobserved contexts and 96 on newly calibrated contexts, unchanged original-context
retention and 40/48 ambiguous arms. Verified 229 source hashes, 480 prediction
hashes, 10,564 artifact hashes, 135,271 prior hashes and 57 unchanged production/
configuration/dependency files. The full 976-test suite and 7,821-check study run
were inspected, not independently rerun. This acceptance does not establish seed
advantage, broader generalization, learned acquisition utility or runtime integration.
The evaluated archive and all earlier evidence remain unchanged; this section is
a subsequent handoff annotation.
