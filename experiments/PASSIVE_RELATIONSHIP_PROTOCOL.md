# Passive relationship-set runtime integration — protocol v1

Frozen 2026-10-12 before evaluation. Priority 1 only; zero model/mock calls and
NO observation requests. Existing numerical equations, thresholds, seed, migrations,
model configuration, standalone study code and historical findings remain unchanged.
Use NEW opt-in modes `relationship-set-lmft` and `relationship-set-memory`, with
`--mode fixture` and `--relationship-scenario unsupported|supported|ambiguous`.

## Reused scientific contract and assumptions

Reuse the frozen insufficiency fixture and learner without modifying them: new
procedure capacity-blocked-two-1, existing six comparisons, four registered
training and four reserved validation events per scenario, eight held-out probes
and one excluded out-of-scope probe. Exact cases/labels and limitations are in
[insufficiency protocol](INSUFFICIENCY_PROTOCOL.md). No additional hypotheses,
feature vocabulary, context repair or validation-based selection.

Verified noiseless synthetic observations can eliminate these deterministic
candidates; source names are NOT authentication and this fixture is NOT a
real-world verifier. Empty does not diagnose vocabulary/context/evidence faults.
Both runtime conditions use the SAME existing learner and policy. Both inherit
the runtime's inert 40-node scaffold; it is common packaging, not a mechanism of
ordinary-memory inference or an LMFT advantage. An independent standalone path
receives the identical eligible verified evidence and selection/validation budget.

Persist the full authored candidate space, admitted records, verification provenance,
message/evidence links, derivations and surviving hypotheses separately from birth.
Expose support status untrained/supported/ambiguous/no_supported_hypothesis plus
validation status not_validated/validated/validation_rejected/no_supported_hypothesis.
Unvalidated supported hypotheses abstain; empty sets abstain without vacuous
consensus; multiple validated hypotheses predict only when their votes agree.

## Runtime operations and compatibility

Use the EXISTING strict observation envelope with text/operation/record. Only
outcome, select, accept, evaluate and empty barrier are supported. Teacher replies,
proposals, requests and acquisition operations reject. No automatic messages except
deliberate responses to processed inputs. No idle inference or question generation.

Outcome admits only the exact registered source/schema/scenario/phase/features/label;
copy the learner before admission and commit it only for accepted evidence.
Rejected/unverified inputs and evidence duplicates must not change learner state or
provenance links; receipts retain original input and reason. Runtime message-level
duplicates/conflicts keep the existing policy. Exact message redelivery emits no new
outbox message; a new ID with duplicate evidence receives one duplicate acknowledgment.
Learning-disabled controls reject outcome/select/accept before any verifier call;
evaluation/barriers remain available. select/accept require empty records, complete
eligible splits, one-shot phases and fixed training/set identity.

evaluate uses the pure predictor and writes ONLY delivery/receipt/outbox metadata,
never learning state, accepted hypotheses or evidence; pure probes and halted CLI
probe/inspect preserve scientific state AND exact checkpoint bytes. Distinguish
the communication commit from a read-only pure prediction. Full inspection is
refused while live. Inspect outbox and lifecycle only during execution.

Pin scenario, task/verifier configuration, candidate language, scope and integration
rule version in the existing software manifest, in addition to source/config hashes.
Restart with changed scenario/control/source/config must reject BEFORE changing
the scientific checkpoint. No silent migration; pre-integration checkpoints require
their archived sources/configuration. Existing capacity mode behavior is unchanged
under new software but its old manifests remain guarded. No historical checkpoint
will be opened for modification. New mode requires fixture operation, never creates
LocalModels, and is dispatched before model processing.

## Fixed execution and checks

Six mode/scenario conditions, each restarted and uninterrupted = twelve real runtime
individuals. Use real inbox files, runtime.advance, processed identities, receipts,
outbox, Store atomic commit, locks and start/stop lifecycle. Each restarted individual
halts after select, restarts with no input to verify exact state, then resumes for
validation; halts after accept, restarts with no input, then resumes for evaluation.
All final scientific states and semantic responses must match uninterrupted execution,
excluding timestamp/processing-time metadata. Preserve process PIDs and lifecycle.

Per individual: probe untrained; attempt false label before true evidence, wrong source,
wrong features/types, held-out admission, malformed proposal, teacher reply and request;
admit four training events; redeliver one exact message plus a conflicting same message
ID, a same-evidence new-ID copy and an evidence identity conflict; select; probe before
validation. Admit four validation events, accept, then send invalid post-accept inputs
and duplicates. Compare scientific state before/after rejection/duplicates/evaluation.
Use unique barrier messages for completion, so duplicates need not emit new responses.

Freeze ALL final prediction sets before scoring ANY held-out labels. Expected quality
is EXACTLY the insufficiency study's negative results: unsupported 0% coverage/null
accuracy, supported 100% coverage/75% accuracy (6/8), ambiguous 50% coverage/75%
accuracy (3/4). Equality/non-equality subgroups retain that protocol's denominators.
Blanket abstention fails controls. Quality is reported separately from integration
correctness; held-out labels never drive learning or repair.

Required integrity: standalone scientific/prediction parity, equally equipped memory
parity, real restart/uninterrupted parity, support/validation distinctions, rejection
and dedup invariance, no requests/models/seed mutation, provenance and input retention,
learning-disabled behavior, no scope/phase leakage, read-only probes, live inspection
denial and manifest compatibility refusal. Regression tests inject interruption before
and after atomic replacement for evidence/select/accept/evaluation, covering state,
cursor, processed identity, receipt and outbox as one old/new transaction; replay
must avoid double learning or double output. These are bounded fault injections,
not a power-loss durability guarantee.

## Archive and stop

Freeze source/config/protocol and actual dirty-source Git/Python identity into a fresh
output directory. Preserve complete halted states/inboxes/outboxes, scientific projections,
restart PIDs/equivalence, compatibility/control checks, predictions, metrics and failures.
Guard prior protected file hashes and all evaluated archive hashes. Refuse existing output
paths. Preserve failed attempts; any CHANGE to protocol criteria requires a versioned
revised protocol before reevaluation. Focused implementation fixes that restore this
unchanged contract are documented and reevaluated without changing criteria.

Stop after passive integration, focused fixes and handoff. No active acquisition or
new task dispatch. Finish before the user's 2026-10-12 12:00 UTC deadline; do not
start long stages near it or terminate an atomic write to meet the deadline.
