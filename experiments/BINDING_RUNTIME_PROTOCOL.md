# Binding in the supervised runtime — protocol v1

Frozen before implementation evaluation on 2026-10-12. Owner-approved scope:
two new fixture-only modes, binding-primary and binding-memory. Existing modes,
40-node seed, numerical rules, model configuration and teachers are unchanged.
No model calls, generated code, dependencies or runtime family expansion.

## Contract and information boundary

Use the existing inbox -> runtime.advance -> binding handler -> pure predictor ->
outbox -> atomic checkpoint path. Promote the neutral-binding-1 public family and
two independent kernels without importing experiments. Preserve 36 representations,
18 truth-vector classes, a/b/c integer channels0..3, query domain0..2, budget1,
class disagreement selection and lexicographic ties. Evidence changes survivors;
predictions read the persisted survivors, not a recommendation or authored binding.

New state binding-runtime-state-1 is separate from existing capacity state. Outer
checkpoint schema1 and exact software_manifest checks remain unchanged. Resume
validates fixed configuration/catalog, evidence derivation and episode invariants.
Unknown versions, changed private verifier registry, sources or controls fail closed.
No migration. Exact pre-change source/config and prior output hashes were archived
before production edits, with the owner's demo manifest matched against all44
current source files. Compatibility tests use a copy, never the owner's directory.

The harness alone owns the world mapping and unchanged bounded-write oracle. It
creates a private immutable registry of canonical neutral training/query records.
A receiver-invoked fixed verifier subprocess checks exact record membership and
returns the canonical observation. Its registry contains no explicit mapping,
includes a random nonce and opaque identity, and stays outside learner state and
messages. Receiver adapter source and opaque registry fingerprint are pinned;
private path and contents are never copied into checkpoint, receipt or outbox.
Private registry possession/configuration is trusted operator authority. A sender's
source string, supplied digest or supplied verification assertion cannot authorize
admission. This is a local trusted fixture boundary, not an OS security sandbox.
No oracle labels are available through the predictor or selection kernels.

Strict public commands: train(record), select({}), reply(record) as a correlated
teacher_reply, close({}), evaluate({id,channels}), barrier({}). Text is inert.
Training records use tNNN and acquisition qNNN; all values are strict typed.
Only registered training and the outstanding selected query may enter evidence.
Training closes once; selection charges at most one lifetime request. Close requires
the charged reply to have been admitted. Evaluation is allowed after training
closes, including while pending. It rejects labels and changes no learning state;
cursor/receipt/outbox bookkeeping may advance. Disagreement or an empty candidate
set abstains, while nonempty consensus may decide without a unique binding.

Five conditions retain the accepted study definitions: informative, no-acquisition,
noninformative, unavailable (diagonal query pool), already-supported (27 training
points). A sixth informative-frozen control admits the same acquired observation
and spends the same budget but uses the persisted pre-acquisition survivor snapshot
for prediction. The control is explicit in the manifest and result provenance.
No forced singleton or held-out-label-based acceptance. No separate validation.

## Frozen acceptance matrix

Run both independent kernels under all six channel permutations and all six
conditions (72 arms), unless safely stopped at the18:40 UTC session ceiling.
Partial evidence cannot be presented as full acceptance. Each arm uses actual
runtime processes: train/select, stop with pending request, restart/admit/close,
stop/restart/evaluate. Compare deterministic learning state and predictions with
continuous direct transitions receiving exactly the same inputs. Actual process
outputs/checkpoints remain archived. Freeze every arm's pre/post predictions before
accessing held-out scoring labels. Hold out37 triples containing a3.

| Gate | Required result |
| --- | --- |
| Informative | 2->1 classes;25->37 decisions/37;all decided correct;budget1 |
| No acquisition/noninformative/unavailable | 2->2;25 decisions,12 abstentions;budgets0/1/0 |
| Supported | 1->1;37 correct decisions;budget0 |
| Frozen | Same admitted reply/budget as informative;25 decisions/12 abstentions; prediction snapshot unchanged |
| Memory | Independent filtering, voting and prediction; equal normalized science, choices and outcomes |
| Restart | Pending request and spent budget survive; post-reply reload yields same learning state and emitted decisions |
| Causal path | Held-out outbox decisions equal kernel predictions from saved state; informative differs from frozen on exactly12 cases |
| Immutable evaluation | Binding-state digest unchanged before/after evaluation; labels rejected |
| Gates | Malformed/Boolean aliases, forged digest, wrong source/query/phase, unregistered label, ID conflicts rejected; duplicates no learning/recharge |
| Empty/ambiguous | Contradictory trusted unit fixture yields empty family and abstention; ambiguous disagreement abstains and consensus decides |
| Isolation | Paired indistinguishable histories have equal learning state/selection, excluding opaque verifier identity; no mapping in public schema/state |
| Compatibility | Copy of old demo resumes under matching archive; modified source rejects its manifest; owner originals unchanged |
| Preservation | All captured prior files and protected source/config unchanged; new outputs never overwrite earlier runs |

Unit fixtures testing an insufficient family are explicitly separate from the
noiseless primary oracle. Rejected events and failed runs are retained. Full pytest,
targeted tests and a fresh-output permutation rerun are separate reported evidence.
Six permutations are symmetry checks, not independent scientific replications.

## Claims and stop

Permitted claim: integrated persistent finite-family learned operand binding affects
real supervised runtime decisions. Memory parity is expected and forbids tree,
semantic understanding or causal world-model superiority claims. The philosophical
seed is present as existing birth state, not credited as the mechanism.
Archive final source/context, results, preservation checks and update handoff; stop
for independent review without dispatching another task.
