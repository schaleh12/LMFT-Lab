# Bounded relationship acquisition in the runtime — protocol v1.2

Frozen 2026-10-12 BEFORE evaluation. Priority 2 only, zero model/mock calls.
NEW opt-in modes relationship-acquire-lmft/memory, --mode fixture, with pinned
--relationship-scenario and --acquisition-policy. Preserve prior dirty work,
seed, numerical mechanisms, model configuration, migrations and old findings.

## Task, vocabulary, splits and fixed conditions

Reuse insufficiency's registered capacity-blocked-two-1 device and six comparisons.
Four training/four reserved validation records, eight held-out cases and x1 are
EXACTLY those in [insufficiency protocol](INSUFFICIENCY_PROTOCOL.md). Nonempty
ambiguous training retains lt/le; supported retains le; unsupported retains [].
No new hypotheses, context feature, teacher repair or automatic episode reset.
Synthetic source registration/simulation is NOT authentication or real-world truth.
An empty set does not identify why the supplied family fails.

Candidate observation features, declared order: q1=(0,2), q2=(5,5), q3=(7,7),
q4=(7,6), under capacity-blocked-two-1. All candidate pairs are absent from
training/validation/held-out. Reuse ambiguity.choose's generic true-votes times
false-votes score (unordered disagreeing hypothesis pairs), maximum POSITIVE score,
declared-order ties. Adapter projects numerical inputs into its comparison scope,
then returns the selected ORIGINAL task observation. Record adapter, votes/scores,
features and selection. No equality-specific branch or verifier/outcome access.

Policies: disagreement uses all candidates; predefined noninformative control
selects q1 irrespective of score; unavailable uses q1,q4 and disagreement selection.
Nonempty ambiguity is the gate for ANY request, including the control. Unique or
empty families issue none. Disagreement selection (including the unavailable pool)
issues no request when no candidate has a positive score. The preregistered
noninformative control explicitly overrides that score gate and requests q1 even
though its score is zero; its request budget and verification gates are identical. Ten fixed conditions: both modes for ambiguous
under all three policies, supported/disagreement and unsupported/disagreement.
Each has restarted and uninterrupted execution (20 actual runtime individuals).
Both modes receive identical space/evidence/candidates/budget/policy/validation;
the shared runtime scaffold is inert packaging, not an inference advantage.

## Episode, request and verified reply contract

One episode per NEW individual, ID <individual_id>:relationship-episode-1, pinned
at birth. Phases: unselected -> ready after complete training selection -> pending
or closed after explicit investigate -> closed on one valid reply or explicit
close_investigation. No new episode/reset/retry request operation. Investigate is
an explicit incoming observation operation, not autonomous idle work.

For a selected candidate, emit the EXISTING clarification_request and register it
in state.questions. Request contains episode ID, selected observable case, expected
source/procedure, request_count=1 and budget_remaining=0. Outbox ID is request ID.
Persist selection/episode/request_count/pending question/outbox/cursor/receipt in
ONE atomic runtime commit. Spend the ONE request unit on issuance, BEFORE a reply,
never refund it. Invalid replies cannot reopen selection or restore budget.

Use the existing teacher_reply envelope as transport only (no teacher/model call),
reply_to equal to request ID, operation verification, and EXACT record:
{episode_id,request_id,evidence:{evidence_id,scenario,split,procedure,length,capacity,success}}.
Evidence ID equals selected q ID; split=acquisition; scenario/procedure/features
must match the pinned episode/candidate, success is strict Boolean, source is
registered-insufficiency-1. Source/schema/correlation/eligibility checks precede
device simulation. Independently check the label with the unchanged synthetic
verifier. Only verified matching evidence filters CURRENT surviving hypotheses;
keep acquisition facts/provenance/filter trace separate from original training
records and derivation. Validation checks the effective retained set, never
filters/resurrects. Preserve support versus validation distinctions.

Reject unrelated/malformed/wrong-source/wrong-episode/wrong-candidate/unverifiable
replies, early validation, changed message/evidence identity and closed-phase
operations. Rejections preserve judgment/questions/pending request/budget; receipts
retain inputs/reasons. Exact message duplicates use runtime dedup and emit no new
message; a new message ID with the SAME correlated verified evidence is a duplicate
acknowledgment, no verifier execution, filtering or question revision. A conflicting
reuse rejects. Duplicate detection must NOT bypass source/correlation checks.

Pending can await a later valid reply to the SAME request after a rejection/restart;
this is not another request. close_investigation cancels explicitly without budget
refund and allows validation, preserving hypotheses; later replies reject. No timeout,
automatic close or reset. Unique/unsupported/unavailable close with explicit reasons,
zero requests, zero acquired observations. Empty reports insufficiency, invents none.

## Counts, costs and read-only evaluation

Report distinct request_count/request_cost_units (one per committed request),
acquired_observation_count (0 or1 admitted acquisition), and receiver verification
executions (one per eligible label check, including a failed label). Admitted training and
reserved validation facts are four each. Receiver reserved verification executions
are reported separately: FIVE training checks (one deliberately false registered
t1 allegation before true training, then four admitted outcomes) and FOUR validation
checks in every condition. Failed training verification is receipt metadata only,
never a training contradiction or scientific revision.
The scripted service produces at most ONE actual observation per requested episode;
one deliberately false correlated allegation tests failed receiver verification,
not an admitted observation. Malformed/unrelated/duplicate replies cost zero
receiver simulation checks; rejection never changes the scientific state.

Expected requesting conditions: request1, acquired1, ACQUISITION receiver checks2
(one false label plus one valid label); other conditions have all acquisition
counts0. RESERVED costs remain five training/four validation executions, with
four/four admitted facts, in ALL conditions. Report service observation count1
separately from receiver checks, not as two acquisitions. Atomic faults restore either
old unspent/no-request or new spent/pending/request together; valid-reply faults
restore pending/no-admission or closed/admitted/filter/question/output together.
Replay cannot double spend or double admit.

Evaluate/pure predict/halted CLI probes never issue requests, spend budget, filter,
validate, admit or mutate judgment/questions. Communication evaluation commits only
receipts/outbox/delivery metadata. Freeze ALL predictions before scoring ANY held-out
label; no held-out admission or post-evaluation repair. Before validation even a
resolved single hypothesis abstains; accepted consensus decides and disagreement
abstains. Preserve explicit empty-family reason and validation-rejection behavior.

## Fixed execution, metrics and acceptance

Every requesting restarted individual halts while pending, exact no-input restart,
then receives invalid replies and a valid correlated reply; halts after reply,
exact no-input restart, resumes validation. Every other restarted condition also
restarts at the post-investigate and pre-validation stages. Uninterrupted references
receive identical queued inputs. Invalid attempts include malformed envelope/reply,
wrong correlation/source/candidate/episode, false label, duplicate deliveries and
identity conflict, repeated investigate/reset attempts, and evaluation injection.
Use barriers for completion. Live inspection refused; only outbox/lifecycle while live.

Expected quality (same in both modes, prior fixture errors preserved): ambiguous
disagreement resolves to le, 100% coverage/75% accuracy (6/8); supported le same.
Noninformative/unavailable remain lt/le, 50% coverage/75% accuracy among decisions
(3/4); unsupported remains empty, 0% coverage/null accuracy. Equality versus
non-equality metrics use original four/four denominators. Resolution, abstention,
coverage, accuracy, requests and verification costs are SEPARATE metrics.

Required integrity: actual pending/reply restarts, exact question/budget/state recovery,
uninterrupted/memory/standalone parity, score/feature-only selection, eligibility gate,
at-most-one request/admission, immutable original training trace, valid provenance,
rejection/dedup/correlation safety, no resets, validation separation, read-only
evaluation, no model/numerical/seed changes, complete source/context/archives and
historical byte preservation. Tests inject before/after atomic replacement at
request/reply/cancellation/accept/evaluate; scope/disabled/manifest controls and
all state distinctions are tested. Distinguish fault injection from power-loss proof.

Use fresh directories and nonempty complete current preservation contexts for actual
checkout regression; run the separate historical audit. Archive source/config/protocol,
raw inbox/outbox/question/budget/provenance states, PIDs/restarts, cost/results and
failures. Preserve prior archives byte-for-byte. Do not change criteria after outcomes;
scientific protocol changes require a versioned revised protocol BEFORE reevaluation.
Stop after this priority/necessary focused fixes and report for coordinator review.
No later task dispatch, push, publication or broad refactor.

## Pre-evaluation clarification

v1.1 clarifies the already-preregistered noninformative-control exception to the
positive-score gate. Original v1 is retained unchanged; no experiment or outcome
had been evaluated before this clarification. Expected request/control counts,
cases and scientific criteria are unchanged.

## Pre-acceptance correction v1.2

A first v1.1 harness test completed before acceptance review and is retained. It
misnamed four admitted training facts as four verifier calls although its extra
false-training allegation caused a fifth call. v1.2 pins five actual training
checks plus four admissions, with receipt-only instrumentation. Quality and
effective-survivor/resolution expectations must be keyed ONLY to the frozen
scenario/policy, never achieved resolution. Scientific case labels/predictions,
request budgets and acquisition criteria are unchanged. No v1.1 result is
retroactively rewritten; v1.2 is frozen before its reevaluation.
