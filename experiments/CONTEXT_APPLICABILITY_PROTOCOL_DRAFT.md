# Context-dependent measurement interpretation — draft protocol

Status: **DRAFT FOR PARENT REVIEW; implementation/evaluation not authorized by this file.**
Prepared 2026-10-12 after D024 demo retirement. Sequential session ceiling:
2026-10-13 02:40 UTC (2026-10-12 22:40 America/New_York). Each completed task
returns for review; unused time is not authorization to start another task.

## 1. Question and scope

Can finite-family evidence elimination learn where to complement a measurement,
retain its previously useful interpretation, and transfer to an unobserved context?
The existing `consistent_attention.normalized` receives an authored `relation` field;
this experiment removes that applicability shortcut in a NEW isolated contract.
See [consistent-support findings](CONSISTENT_SUPPORT_RESULTS.md),
[binding findings](ATTRIBUTE_BINDING_RESULTS.md), and
[seed-contribution negative results](SEED_CONTRIBUTION_RESULTS.md).

This is narrowing uncertainty within a supplied family, **not revision of a
previously accepted global belief**, concept discovery, or evidence for seed utility.
No propagation, acquisition-policy learning, runtime integration, philosophical
naming, teacher, model call, new dependency, or demo. Existing source, seed,
numerical mechanisms, model configuration, protocols and results stay unchanged.

## 2. Public family and independent calibration

Context is exactly two strict bits `c=(c0,c1)` in `{0,1}^2`. Values below are strict
integer bits; Boolean substitutes, missing/extra fields and unknown contexts reject
at admission. An evaluation with unknown context abstains without state changes.
First-measurement orientation is a **supplied assumption**, not learned.
Second-measurement normalization is `v XOR h(c)`. The fixed ordered family is:

`H = [0, 1, c0, not c0, c1, not c1]`.

An admitted calibration contains public context `c`, raw second measurement `v`,
and independently referenced target `z`. It imposes exactly:

`v XOR h(c) = z`.

The synthetic device uses a commanded binary reference source. Its reference
channel reports the commanded bit `z`; a separately configured measurement channel
passes or inverts that signal according to its wiring. Six coordinator-private
worlds have wiring: always pass; always invert; invert when c0=1; invert when c0=0;
invert when c1=1; invert when c1=0. These correspond to the six public hypotheses,
but the device/reference implementation must not call learner evaluation/filtering
or derive a target from whichever normalization creates agreement. Both reference
and raw channel values are generated before admission/learning. The commanded
target and schedule are independent of wiring. Reference observations legitimately
provide information; sending a wiring label would instead leak the answer.

Assumptions: noiseless, stable wiring in primary worlds; correct commanded reference;
trusted local fixture registry binding the actual paired observations to context,
scope and acquisition slot. This is an authored synthetic truth source, not a test
of sensor reliability, causal discovery, cryptographic authentication, or hostile
filesystem isolation. Real disagreement alone supplies no calibration constraint.

## 3. Exact matrix and schedule

Evaluate all six worlds, four schedules below, and two value flips `b=0,1`:
**48 distinct public calibration histories before controller comparisons**.
No additional cue permutation arms: c0/c1 and their complements already occur as
worlds. They are symmetry checks, not independent replications.

Every arm starts with exactly one calibration at `c=00`, reference `z=b`.
It has one fixed subsequent opportunity, reference `z=1-b`, with no retries:

| Schedule | Follow-up context | Delivery |
| --- | --- | --- |
| P10 | 10 | valid paired observation |
| P11 | 11 | valid paired observation |
| P00 | 00 | valid paired observation |
| U10 | 10 | unavailable; no calibration admitted |

Raw `v` comes from the private device, never from learner selection. Scheduling,
reference values, opportunity timing and unavailable status are the same for every
world. An opportunity is charged once even when unavailable. No budget increase,
alternative query, hypothesis expansion, family repair or retuning after scoring.

Analytic examples (mapping bit is `v XOR z`, not supplied as a label): equality at
00 retains `{0,c0,c1}`. Complement at10 leaves `{c0}`; complement at11 leaves
`{c0,c1}`; equality at10 leaves `{0,c1}`. Therefore one follow-up does not identify
all worlds. P00 adds no new context information; U10 supplies no new constraint.
The complementary first-observation cases are equally mandatory, not discarded.

## 4. Admission and information boundary

Worker calibration records have only version, evidence ID, scope, context, raw value,
reference value and slot (`initial` or `followup`). A fixed source ID identifies
the fixture, never a world. The receiver validates against its trusted registered
observation for the slot; a sender-computable digest alone is not verification.
Verification returns accept/reject plus the paired observation, not hidden wiring.
Only accepted calibration can eliminate hypotheses. Raw support records, request
priority, agreement gains and evaluation scores cannot do so.

No relation field, world ID, relevant-cue label, wiring parameter, rule identity,
oracle trace or equivalent metadata reaches learner inputs/state. Use identical
evidence IDs (`cal-0`, `cal-1`), scope (`calibration`), source and schema across arms.
Learner hypothesis IDs enumerate the public family, never identify the true member.
No timestamps, world-dependent record order, receipt tokens or descriptive paths.
Public schedules are fixed; their names/contents reveal no hidden world.
Allocate opaque work roots before world assignment, independent of world identity;
store world associations and evaluation targets only in coordinator-private outputs.
Workers receive a local root and explicit public inputs, not oracle paths/config.
Restrict imports and audit the dataflow; do not claim an OS confidentiality boundary.

Paired indistinguishable-history checks group arms by their complete admitted public
history and schedule prefix, excluding only external process/path metadata. Their
canonical learned state, receipts, rejection witnesses and all predictions must
match exactly, even if hidden worlds imply different later targets. Before follow-up,
the three equality-at00 worlds must be indistinguishable. After complement at11,
c0/c1 must remain indistinguishable and abstain where they disagree. Publish the
grouping/check results, not just an assertion that the boundary holds.

## 5. Learning, support and abstention

Primary learner retains all and only hypotheses satisfying every admitted
calibration, plus the evidence IDs rejecting each eliminated hypothesis. Prediction
requires a NONEMPTY surviving set and unanimous mapping at the given context.
An empty family is `unsupported`, never vacuous consensus. Mixed mapping votes are
`mapping_ambiguous`. Neither condition may be resolved by looking at support agreement.

Keep three independent fields: mapping status/votes; within-part contradiction;
cross-part disagreement under each surviving mapping. Raw part values, identities,
source and scope remain immutable. Normalize a copied view only. Complementing
`{0,1}` still gives `{0,1}` and cannot remove its within-part contradiction.
Only applicable records count; duplicate evidence never adds independent support.
A support decision requires a known context, unanimous mapping, both parts present,
no within-part contradiction, and agreement of the oriented first measurement with
the normalized second. Otherwise abstain with separate reasons. No majority rule.
No existing correction permissions or truth gates are broadened.

## 6. Exact read-only evaluation grid

At both pre-follow-up and post-follow-up stages, evaluate every context in
`[00,01,10,11]` and reference target `z in [0,1]`. The coordinator creates raw second
value `v` with the private device. `z` is NOT in support input; it is revealed to
the scorer only after predictions have been written and hashed. The oriented first
measurement below is observable evidence, not a separate hidden label field.

For each of these eight context/value combinations, use these seven templates:

| Template | Applicable first-part values | Applicable second-part values |
| --- | --- | --- |
| complete | `{z}` | `{v}` |
| cross disagreement | `{1-z}` | `{v}` |
| within-part contradiction | `{z}` | `{v,1-v}` |
| second absent | `{z}` | empty |
| first absent | empty | `{v}` |
| duplicate complete | same exact first record twice | same exact second record twice |
| foreign second | `{z}` | empty; `{v}` record supplied with foreign scope |

That is **56 support cases per stage/controller/arm**; no target-dependent filtering.
Also record mapping-only predictions for all four contexts. Render the complete grid
twice with a fixed one-to-one neutral evidence/case ID renaming; duplicates within
each rendering remain exact duplicates. Require identical scientific predictions;
report identity invariance separately, do not double statistical denominators.
The two `b` arms and both evaluation targets provide value-flip invariance checks.

Freeze support features and all stages' predictions before outcome scoring. Evaluation
never changes evidence, survivors, counters, opportunity charge or rejection witnesses.
Explicit categories, not a pooled transfer claim:

- Retention: context00 on fresh records, both target values, after follow-up.
- Calibration-context application: the delivered follow-up context, if different.
- Genuine unobserved-context transfer: contexts absent from admitted calibrations;
  P10 => `{01,11}`, P11 => `{01,10}`, P00/U10 => `{01,10,11}`.
- Value/identity invariance: separate symmetry checks, not new learned distinctions.

## 7. Comparators and causal controls

All five controllers receive identical calibration/support records, gates, schedule,
budget and persistence lifecycle. The primary and ordinary-memory controller each
start with the same six-member family. Memory independently builds/filter truth-table
bit masks and predicts by table voting; it must not call primary hypothesis evaluation,
elimination or prediction. Shared schemas, verification, storage and scoring are disclosed.

Other controls: (1) frozen pre-follow-up survivors, while retaining the follow-up
record and charge but not applying its constraint to decisions; (2) constant equality,
which always uses mapping0; (3) global replacement, which uses the latest admitted
calibration's `v XOR z` as a constant mapping everywhere, retaining its earlier records.
If follow-up is unavailable, global replacement keeps its initial mapping.
These controls use identical completeness, contradiction, context and scope gates;
their deliberately different mapping policy is explicit. Do not force an error:
record actual correct, wrong and abstained outcomes in every world/schedule.
No propagation-ranking or acquisition-policy comparison is included.

## 8. Restart and integrity diagnostics

Use real separate worker processes: initial admission/checkpoint/pre-prediction and
exit; restart from disk for the one opportunity/checkpoint/post-prediction and exit;
final read-only reload. Compare against uninterrupted execution on the same public
events. Preserve exact records, survivor/rejection-witness state, policy/source pins,
opportunity charge, and predictions. Failed checks/attempts remain archived.

Exercise exact duplicate calibration before and after restart: no extra constraint,
charge or independent sample. Conflicting ID reuse, foreign scope, malformed/extra
fields, Boolean aliases, wrong source/slot, unverified observation and extra opportunity
must reject without changing the learned projection; any audit receipt is separate.
Recompute survivor and rejection-witness consistency from admitted evidence on reload;
inconsistent copies fail before writes. No source-manifest relaxation or migration.

One separate empty-family diagnostic uses two registered calibration rows:
`(c=00,v=0,z=0)` then `(c=00,v=0,z=1)`, with distinct evidence IDs and two fixed slots.
This intentionally violates stable/noiseless primary-world assumptions; it is a
trusted-reference inconsistency/family-insufficiency test, not a seventh successful
world. It must retain both rows, reject every hypothesis with witnesses, abstain,
and remain unsupported after restart. Do not repair the family or request more data.
Unknown-context probes and empty-family diagnostics have separate denominators.

## 9. Frozen metrics and acceptance interpretation

For each world/schedule/controller/stage/category report total cases, correct emitted
bits, wrong emitted bits and abstentions (`correct + wrong + abstained = total`).
Correctness compares an emitted target bit with the independent reference target;
abstention is never counted correct. Report coverage and accuracy among emitted bits
with explicit denominators (accuracy undefined when no bit is emitted).
Separately count unsafe resolutions: any emitted bit when oracle-oriented support is
incomplete, contradictory or cross-disagreeing, even if the bit happens to equal z.
Report mapping correctness/ambiguity/unsupported counts and survivor sizes separately.

Report pre/post retention and genuine-transfer deltas, per-case paired differences
versus frozen and memory, symmetry/invariance checks, and initial/follow-up reference
executions, charged opportunities, delivered/admitted calibrations, rejects and duplicate
deliveries. Baselines share the same pre-generated observations; distinguish logical
per-controller charges from physical device executions. No physical crash-proof cap.

Integrity acceptance requires no leakage, correct survivor/witness computation,
independent memory parity, strict admission, no unsafe resolutions by primary/memory,
raw/provenance preservation, immutable evaluation, and actual restart equivalence.
An integrity failure blocks acceptance of scientific claims; retain the failed attempt.

Research outcome: test whether informative observations improve held-out useful
decisions over the frozen learner while preserving context00 behavior. Report cases
with no benefit, persistent ambiguity, false generalization by controls, or no controller
difference without changing criteria. Negative scientific results remain valid.
Memory parity supports finite contextual interpretation learning, not LMFT superiority.
The closed realizable family and reliable reference strongly limit the claim; no
accepted-belief revision, philosophical framing or general understanding follows.

## 10. Approval boundary and prospective files

Parent must approve this draft and its exact matrix before implementation. Then freeze
the approved protocol hash before evaluation. Anticipated work is experiment-local
contract/learner, independent memory, private device/runner and worker modules, focused
tests and results; filenames/module partition may be settled during implementation.
Do not change production contracts or historical files to accommodate the experiment.
Capture exact prework sources/config and preserve all current demo-retirement changes.
No implementation, tests, experiment, model calls or model/config changes were performed
to prepare this draft. Stop for parent review; no subsequent task is self-authorized.
