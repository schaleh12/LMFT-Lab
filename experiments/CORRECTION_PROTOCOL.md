# Correction without erasure — preregistration v1

Before implementation/evaluation. No changes to founding seed, consistent-support-1 mapping,
fixed A=.25/B=.75/D=.5 routes, judgment equation, migration or historical outputs. Zero models.

## Scope, initial admission and independent verification
Fresh c1..c12 use equality shielded checks plus known payload_valid=true. Initial admission
under correction-fixture-1 verifies what an instrument LOG reported, not whether the report
was true. Erroneous logged observations are deliberate fixture data. This separately versioned
policy does not weaken any historical exact-truth verifier. Corrections target only scoped
observations, including irrelevant color; prior eight outcome samples s1..u4 are ineligible.
The unchanged sum(signs)/(n+2) rule still applies to the same eight eligible outcome roots.
Effective condition evidence selects which existing conditional judgment applies; correcting
prior outcome counters is deferred. This small scope requires no protected numerical change.

Replacement verification uses a separate registered reference lookup by case/question/part;
it can check only the explicitly proposed replacement, not unrequested case truth. Selector
and predictor cannot call this lookup or held-out outcomes. Values are Boolean, exact schema,
case, scope, question and part must match target, and replacement ID is replacement/<correction-id>.
The reason must be nonempty; the original evidence remains immutable. References describe
synthetic calibration checks, not real-world truth discovery or production authentication.

## Authority and transaction policy
Separately trusted config/correction_authority.json contains authority plus full correction
payload SHA256 permits, frozen in each individual's manifest/policy. A message saying it is
authorized is insufficient. The sender must match the named permitted authority and the exact
payload must match a configured permit. This public synthetic allowlist authorizes specific
operations; anyone able to replay an exact permitted message has a bearer capability. It does
not authenticate a human, resist hostile host edits, or keep secrets. No tokens are needed.
Some invalid replacements are deliberately PERMITTED to demonstrate authority is not truth.
Authorization, target eligibility and replacement verification are separately traced.

A correction has correction_id, authority, target_id, expected_digest, reason, replacement.
Accept only a current active head and matching digest. Record root ancestry and append a new
replacement record; update head pointer, never delete or overwrite original content. The
replacement occupies the same independent root, not a new sample. A second correction may
explicitly target the active replacement with its exact digest. Maximum tested chain: two.
Competing corrections against an inactive target reject; no last-write-wins. Stale digest
also rejects. No implicit target rebasing. A chain's second replacement can corroborate the
same value with a new attestation without adding independent evidence.

First correction ID use is terminal, including rejection. Identical payload redelivery is
a no-op (receipt only), regardless of new delivery ID. Different payload with same correction
ID is a rejected conflict attempt and cannot replace the original indexed result. Every new
attempt gets a unique audit event ID and retains proposed correction, sender/source, separate
stage outcomes, verification result, acceptance/reason and before/after effective head maps,
digests and independent counts. Rejections may add audit records but never change effective
evidence, cached evaluations or questions. Ordinary exact message duplicates use existing guard.

## Effective view, cache, requests and controls
The immutable record store contains originals and replacements. Derived view includes only
current head per root. Reuse existing consistent select/predict unchanged on that view.
Do not credit effective-view or authorization capabilities to propagation. Three conditions:
correction-lmft; same circuit correction-disabled (validate but reject acceptance, preserve
originals); correction-memory using the existing competent memory selector with identical
correction policy/effective access. No new seed ablation is needed.

Cache only semantic evaluation/selection, keyed by the complete public case, relevant effective
records and fixed mode/routes/counters. Emit fresh wording from that result. An accepted relevant
correction invalidates affected cached evaluation; rejected or irrelevant correction does not.
Trace invalidation separately from propagation. Pending questions close only when their own
question becomes sufficient, with explicit closing correction reference; retain question history
and spent budget. Reopening never resets one-request lifetime budget per case. Evaluate both
before and after correction batches to demonstrate changed behavior rather than stale wording.
Requests remain pending in the primary fixture: the additional verifier has no new measurement
available. No request returns invented corroboration. Correction validation is separately
bounded to submitted replacements, identical across conditions. No calls while idle.

## Fresh case sequence and fixed outcomes
All start with payload=true. Unless stated, shielded check1=false/check2=true, thus uncertain.
Every initial record is an admitted instrument report. Actual success is evaluator-only.
Initial evaluate, repeated evaluate (cache hit), correction batch, final evaluate, repeated
final evaluate, barrier. Same messages and ordering across conditions. At most one request.

| Case | Correction batch | Expected enabled behavior | Actual success |
| --- | --- | --- | --- |
| c1 | check1 false -> true | contradiction removed, closure, success | true |
| c2 | initially true/true; correct check1 -> false | expose contradiction, reopen, abstain | false |
| c3 | initially true/true; correct both checks -> false (two events) | success -> failure, same roots | false |
| c4 | check1=false only; correct -> true | still missing check2, abstain | true |
| c5 | unpermitted correction claiming authority | reject, unchanged uncertainty | true |
| c6 | two permitted attempts: wrong Boolean value; missing value | reject unverifiable/malformed | true |
| c7 | two permitted attempts: wrong scope; nonexistent target | reject eligibility | true |
| c8 | valid check1 correction, five new-ID plus five exact repeats | one correction, closure | true |
| c9 | valid correction then conflicting reuse of its ID | preserve first, reject conflict | false |
| c10 | valid correction; competing old-target correction; active-target bad digest | reject both stale attempts | true |
| c11 | valid false->true, then active replacement -> true attestation | retain two-event ancestry, one root | true |
| c12 | initially true/true; irrelevant color false -> true | prediction/selected question/cache unchanged | true |

Enabled LMFT/memory expected seven decisions, six correct, five abstentions. c9 is a deliberate
prediction failure despite repair. Disabled expected three decisions, one correct, nine
abstentions. These are different covered subsets, not a population accuracy comparison.
Initial unresolved cases consume their one request before correction. Enabled c2 reopens and
requests once; c3's two corrections occur as a batch before reevaluation (intermediate states
remain in correction audit). Predicted total requests enabled=10, disabled=9, no redundant
requests. Corrections need not save requests already spent. Final enabled c2/c4 and rejected
c5/c6/c7 remain uncertain. No false closure from rejected or partial repairs.

## Persistence, integrity and measurements
Every case uses a new individual with eight original outcome priors. Halt after initial cached
evaluation with any questions pending; restart, compare exact state, apply correction batch,
evaluate, halt. Compare separate uninterrupted c11 runs for all conditions with identical
messages. c8 repetition stage gets its own halted before/after metrics; no additional correction
events, independent roots, requests, cache invalidations or traces from repeats. Receipts grow.

Test policy spoofing, unauthorized and authorized-invalid content, wrong scope/target, digest
checks, ID reuse, chains, original immutability, effective count, cache/wording freshness,
rejection invariance, closure/reopening and atomic faults before/after correction replacement.
Snapshot source/config/protocol/hashes before evaluated run. During runtime only deliberate
outbox/lifecycle communication; diagnostics and outcomes inspected after halt. Preserve failures.
Stop after 12 cases x 3 conditions plus three uninterrupted chain runs; 420s per exchange.

Report accepted/rejected/duplicate corrections, lineage/supersession, effective root counts,
inappropriate closure, correct reopening, useful/redundant requests, prediction accuracy and
coverage/abstention, storage/repeat growth, timing and zero model calls. Require original
preservation, rejection invariance, no independent inflation, cache correctness and restart
identity. Research equivalence/failure is a result, never grounds to tune criteria afterward.
