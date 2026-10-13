# Interpretation handoff protocol v2 — specified, not recommended for execution

2026-10-13. Documentation-only revision of the assessment's proposed protocol.
This supersedes its section 4 wherever they differ. No protocol pin, implementation,
evaluation or approval to execute is implied. The assessment now recommends a
philosophical-contribution operationalization prerequisite instead: this handoff
largely duplicates accepted binding/action-runtime capabilities.

## 1. Identity, sources and information boundary

Use unchanged synthetic `context_applicability_device.measure`, `calibrations` and
`evaluation`. Wiring is stable within each of 48 histories: six worlds × four
schedules × two flips. Allocate opaque bench/history IDs before world assignment;
pin that association only in the coordinator. Controller copies share the same
bench/history observations but have distinct execution roots. IDs are routing keys,
never predictor features. A new bench is a distinct history, not a context change.

Every proposed envelope has exact fields `version="bench-envelope-1"`, `bench_id`,
`history_id`, `event_id`, positive integer `sequence`, `kind`, `payload`. A trusted
launch manifest pins identities, controller, family, source/configuration hashes,
issuer registries and event schema. No message may select a different registry.
Kinds have separately versioned, exact payload schemas:

| Kind | Payload and scope |
| --- | --- |
| context | `context_id`, `context_version`, strict two-bit `context`; same history, increasing version per context ID |
| calibration | `context_id`, `context_version`, original strict calibration record and slot; record context must match referenced context |
| observation | `observation_id`, `context_id`, `context_version`, original support-case record, observation digest |
| permission | `permission_version`, `observation_id`, strict Boolean `allow_release`, issuer `coordinator-policy-1` |
| intent | `intent_id`, observation/context references, calibration revision and evidence digest, permission version, computed support/mapping and proposed release/hold reason |
| disposition | `disposition_id`, `intent_id`, all source versions/digests, current permission version, committed release/hold or aborted-stale status |
| evaluation_receipt | `receipt_id`, `disposition_id`, observation/context references, bit `counterfactual_reference`, provenance `synthetic-evaluator-1` |

Calibration slots and observation situations use distinct context IDs; a calibration
context event cannot rebind an earlier observation. Observations retain their exact
context/version reference. A newer version of that observation context invalidates
its outstanding intent, but never rewrites its original evidence.

The permission issuer is a separately trusted coordinator control channel/registry,
not merely an accepted source string. Validate exact registered permission events
against that pinned registry before updating authority. This trusts local setup;
it supplies no cryptographic or real-world identity guarantee. Calibration uses the
existing coordinator verification pipe: bind each worker to its immutable launch
history, validate outer identity/context, then verify the unchanged inner record
against that history's `device.calibrations` registry. Do not add identities to the
strict existing kernel record schema or let caller-supplied IDs choose the registry.

Only initial/follow-up calibration records reach hypothesis filtering. Observation
records are support evidence, not calibration. The future wiring, reference bits
and receipt store are absent from selector inputs. Hypothesis IDs enumerate the
public family, not the true member. Record fields, versions and IDs must be validated
without coercing Boolean/integer aliases or malformed domain values.

## 2. Transaction states and rejection behavior

Per `(history, stage, observation, permission-arm)`, progression is:
`ready -> intent_saved -> disposition_committed -> receipt_recorded`.
A stale intent terminates as `aborted_stale`; it cannot be silently recomputed or
executed. Reissuing requires a fresh intent ID, outside the main matrix and recorded
as a separate probe. Command IDs are distinct from evidence IDs.

Saving an intent atomically records exact context, observation, calibration and
permission versions. Immediately before disposition, the same external boundary
for EVERY controller rechecks history, active observation/context, calibration
revision and current permission. A new calibration revision makes the intent stale
even if the resulting hypothesis set happens to match. A changed observation or
context also rejects the old intent. Valid context changes never discard existing
generalized hypotheses; a new intent queries the same admitted history at its new
context. No resetting to make a desired relation fit.

Permission revocation after saving intent prohibits release. Coordinated control
uses the new permission; the stale-permission intervention submits its old intent.
The identical external boundary still refuses unauthorized release. Record a denied
attempt or mandated hold, not a successful unauthorized simulated execution. This
intervention is named **stale permission**, not stale context.

Exact event replay is an idempotent receipt lookup: no version/budget/disposition
increment. Reusing an ID with changed payload rejects unchanged. Non-next sequence,
unknown issuer, wrong history/context/observation, stale target or digest, and receipt
before a committed disposition reject before changing scientific state. Rejected
transport diagnostics may be retained separately. A duplicate commit returns the
original disposition. Conflicting receipt IDs or a second differing receipt for
one disposition reject; no last-write-wins. Unknown future sequence is rejected,
not silently reordered or buffered into a different scientific history.

Actual process boundaries for every controller/history/stage:
worker A saves the batch of intents and exits; worker B reloads, receives any probe
revocation/calibration update, checks current versions, commits dispositions and
exits; worker C reloads and accepts the receipt batch. Thus restarts straddle saved
intent/revocation and committed disposition/receipt. The next stage retains the
same calibration history and charged opportunity. Copy/checksum/config/version
validation precedes mutation; no software-manifest relaxation or old-state migration.

## 3. What the receipts mean

The device provides evaluator counterfactual references, **not observed physical
consequences of release**. Name every output `evaluation_receipt`; never claim
actuation, repair success, consequence-driven learning or a discovered world model.
After ALL dispositions in a stage have been committed and hashed, deliver one such
receipt for every release AND hold. An aborted transaction has no committed action
to score; record its rejection separately. Equal delivery/timing across controllers
prevents selective outcome visibility from creating a learning advantage.

Store receipts outside calibration and decision inputs. They affect reporting only.
An isolated diagnostic copy may substitute the retained receipt reference after
commit, explicitly marked as a reporting intervention rather than valid new evidence.
Its metrics may change, but replayed hypotheses and all subsequent dispositions must
remain identical. Do not alter the original run. A forged live receipt still fails
registry checks. These checks establish record linkage and information isolation,
not learning from consequences.

## 4. Exact roster and denominators

Each controller receives 48 histories × 2 stages × 56 existing support cases ×
2 permissions = **10,752 committed main dispositions**. Five controllers yield
53,760. They are repeated conformance observations, not independent replications.
Both permission arms use identical raw observations with distinct transaction IDs.
Permission is balanced independently of target/wiring; source messages contain no
template label or world ID for selection. Preserve all seven existing templates.

Full roster, included before scoring:

1. Coordinated applicability primary: current survivor consensus, existing support
   gate and current permission; release iff supported prediction is 1 and permitted.
2. Ordinary conditional memory/direct control: independent truth-table kernel,
   exactly the same support/permission rule, events, verifier, timing, costs, source
   boundaries and restarts. No graph propagation is introduced in either, so this
   is also the relevant direct/no-propagation comparator.
3. Frozen interpretation: admits the same events and spends the same opportunity,
   but decisions use pre-follow-up survivor state. It still honors current authority.
4. Stale permission: coordinated interpretation but uses saved-intent permission
   after revocation in probes; the unchanged external authority boundary still
   blocks invalid execution. Main-matrix behavior should otherwise match primary.
5. First-channel diagnostic: validate record/schema/scope/context, then release iff
   the applicable first channel has exactly the distinct value 1 and permission
   allows it; hold for value 0, absent/conflicting first evidence, invalid input or
   denial. Ignore second-channel agreement/mapping for the choice. Still receive
   the same calibration/events, costs, receipt timing and restarts. Report separately
   where this violates the authored two-channel gate despite a factually correct bit.

All histories receive one initial calibration, counted separately from the single
charged follow-up opportunity. Follow-up costs one opportunity whether informative,
repeated-context or unavailable; duplicate delivery costs none. Log receiver checks,
records returned and denied/duplicate work separately. No reward-weighted score or
assumed equality of CPU, latency and logical work.

Report separate, potentially overlapping categories: false committed release
(reference 0); unsupported release (shared two-channel gate not met); unauthorized
release attempt and committed unauthorized release; authorized foregone opportunity
(hold, permission allowed, reference 1); mandated hold (permission denied); supported
not-ready hold; uncertain hold. Count denied stale attempts separately from committed
dispositions. Do not credit mandated holds as correct diagnosis or penalize them as
authorized missed opportunities. Correct truth alone does not imply task compliance.

## 5. Separate intervention probes

For each of 48 histories and five controllers, use fresh copies of the pre-stage
state and fixed case e007 (first-context ready=1 complete support, both permission
and interpretation initially sufficient). No outcome-based case selection. Twelve
probe recipes, **2,880 separate probe copies**, excluded from 53,760 main dispositions:

1. Replay exact context/calibration/observation/permission events; verify no change.
2. Reuse an event ID with changed payload; reject unchanged.
3. Supply a different bench/history identity; reject unchanged.
4. Deliver a receipt before disposition; reject unchanged.
5. Advance calibration after saved intent; reject stale intent, retain new hypotheses.
6. Change context after intent; reject old intent, preserve generalized hypotheses.
7. Revoke permission between workers A/B; no committed unauthorized release.
8. Replay a committed disposition; no second commit or cost.
9. Supply an unregistered permission issuer; reject unchanged.
10. Deliver non-next sequence; reject before scientific mutation.
11. Substitute retained receipt reference in an isolated diagnostic projection;
    hypotheses/subsequent dispositions unchanged, reporting may differ.
12. Duplicate receipt then conflict its payload; duplicate no-op, conflict rejected.

Each controller gets the same intervention and process boundaries. Probe-specific
valid events remain schema-correct and are pinned before execution; a changed
calibration is an existing permitted follow-up, not an invented contradiction or
extra budget. For unavailable schedules, delivering the opportunity advances the
calibration-state revision even without admitting a record. Revision therefore means
validated calibration lifecycle revision, distinct from hypothesis-set revision.

## 6. Acceptance and limits

Require exact primary/memory scientific parity, independent truth-table support
validation, restart equivalence, complete immutable lineage, strict source/version
and budget checks, and all receipt-isolation interventions. No outcome access before
stage freeze. Report differences against frozen interpretation and diagnostic truth/
compliance costs even when they favor the simpler diagnostic. Never retune the gate
or denominator. Any unsupported or unauthorized action, lost context history, hidden
label dependence or unmatched comparator opportunity invalidates that claim.

This could validate an applicability-specific versioned disposition interface. It
would not validate seed coordination, learned audit utility, a philosophical leaf,
physical consequences, or improvements beyond already accepted inference. No code
is proposed for production. See the assessment's revision discussion for why this
fully specified bookkeeping comparison is not the recommended next task.
