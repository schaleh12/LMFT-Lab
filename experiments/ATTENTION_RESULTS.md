# Attention-guided verification — results

Recorded 2026-10-11. [Preregistered protocol](ATTENTION_PROTOCOL.md),
[implementation and commands](../docs/ATTENTION_EXPERIMENT.md).

## Finding

Propagated activation now causally ranks concrete verification requests. Two verified
training experiences change separately stored association weights and later choices,
including after an actual process restart. **LMFT matches the competent ordinary-memory
baseline; it does not outperform it.** Prior propagation-equivalence findings remain
unchanged for their earlier, uncoupled mechanisms.

Archive: `outputs/attention-001/`. **70/70 experiment checks and 223/223 tests passed**
(206 preexisting tests plus 17 new parameterized cases). All execution is deterministic;
zero SLM calls and zero mock inference. No model-assisted comparison was performed.
No evaluated run failed. A development test initially matched the word fixture in a
comment; its brittle source-text assertion was removed, retaining the test that fails
on verifier/outcome access during selection. A pre-evaluation mapping review reduced
Theory's direct input to .5 to avoid saturating its Novelty input; this was recorded
before the evaluation. No mapping or criterion changed after held-out evaluation.

## Causal and learned changes

All candidates contain attributed conflicting reports. Exact repeated reports retain
identity/source and add no independent conflict. Color is an irrelevant distractor;
shielded is the authored relevant condition. With equal .5 weights, initial Clarity
priority is .203125 for routes A/B and .078125 for D; ties choose A. The disabled
fallback chooses D by public candidate ID. This is a controlled wiring demonstration,
not a fair claim that arbitrary fallback order represents the strongest alternative.

Initial p1 selects A and remains unresolved in both LMFT and ordinary memory. Its
verification does not train. Training t1's unavailable A reply reduces A .5 -> .25.
Training t2 then selects B, whose verified Boolean resolves the condition and raises
B .5 -> .75. All later association learning is frozen. Fresh h1..h5 select B in the
learning conditions, A with frozen associations, and D with the disabled pathway.
The ordinary-memory relevance-first rule gets identical route statistics and matches.

These are candidate-specific sidecar Salience -> Clarity weights, not founding node
changes or independently discovered meanings. The unchanged counter score and thresholds
supply conditional predictions after verified information selects a branch. Propagation
changes **what is investigated**, not the judgment equation or factual acceptance gate.
Novelty/Theory and Salience contribute numerically to the priority; relevance and route
weight drive the observed ranking differences. Fact/Confidence distinguish verified
support in post-verification frames. They are zero before initial selection, and no
separate causal selection benefit from them is demonstrated by this one-request fixture.
Clarity is explicitly interpreted here as need for clarification, not measured achieved
intelligibility. None of these activations is calibrated probability or semantic understanding.

## Held-out results

Five fresh cases, same public reports/menu, one request each. Replies differ only because
selectors request different routes from the same verifier. No unselected truth is fetched
for selection. Prediction never reads held-out outcomes; quality scoring happens after halt.

| Condition | Relevant requests | Resolved | Decisions / cases | Correct / decisions | Abstentions | Unnecessary requests |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| LMFT learning | 5/5 | 4/5 | 4/5 | 2/4 | 1 | 1 |
| Frozen associations | 5/5 | 0/5 | 0/5 | Undefined | 5 | 5 |
| Pathway disabled | 0/5 | 0/5 | 0/5 | Undefined | 5 | 5 |
| Ordinary memory | 5/5 | 4/5 | 4/5 | 2/4 | 1 | 1 |

Unnecessary means irrelevant or unable to resolve this decision, assessed retrospectively;
it is not a claim that unavailability was knowable before querying. All conditions first
abstain without a verified condition. h1/h2 are predicted correctly; h3/h4 deliberately
violate the conditional tendency and are wrong even after successful verification. h5
cannot be resolved by either relevant route. n1 supplies no independent conflict and
causes no request. Improving resolution increases coverage to 80%, with only 50% accuracy
among predictions. No population-level or broad generalization claim follows.

## Persistence, validation and boundaries

- Actual halt/restart after training retains exact complete state, evidence and reasons.
- Restarted and uninterrupted runs have identical learned state, cases and question links.
- One malformed t1 answer per condition is rejected without closing its request. A valid
  correction uses that same request. Unit tests also reject unselected routes, wrong cases,
  forged source labels, Boolean/type errors and conflicting evidence identity.
- Repeating t1 five new message IDs plus five exact deliveries changes no evidence, weights,
  update records, propagation diagnostics or requests. A repeated case cannot allocate
  a second request, including after an unresolved reply.
- Tests inject failure before/after checkpoint replacement and recover exactly one update;
  bounded updates saturate at 0 or 1. Existing recovery/regression tests remain passing.
- During execution, the harness reads only deliberate outbox messages and lifecycle
  acknowledgments. Live inspection is refused. All diagnostic inspection occurs after halt.
- Seed, activation, propagation, migration, judgment, contextual and storage implementations
  are unchanged against the prior state; existing historical result reports are untouched.

Each final condition stores 8 original training outcomes (8 counter revisions), 8 verified
request replies, 8 association acceptance/rejection records, 9 cases, 8 question records,
38 receipts, 33 processed message IDs, 28 outbox messages and 1 rejected malformed reply.
Learning LMFT/memory accept exactly two association updates; frozen/disabled accept zero.
LMFT/frozen store 16 propagation diagnostic records; memory/disabled store none.

## Costs and storage

Single-run descriptive timing, including process startup/restart, polling and commits in
wall time; core time sums transitions before serialization/commit. No significance test.
Sizes cover each individual, excluding separately retained snapshots and archived sources.
Repeat delta includes the repeated-case budget check and barrier acknowledgment.

| Condition | Wall seconds | Core ms | Checkpoint bytes initial -> final | Final individual bytes | Repeat checkpoint growth |
| --- | ---: | ---: | ---: | ---: | ---: |
| LMFT learning | 4.107 | 166.07 | 18,767 -> 656,303 | 674,207 | 3,843 |
| Frozen associations | 4.086 | 171.34 | 18,773 -> 656,099 | 674,000 | 3,840 |
| Pathway disabled | 3.577 | 30.01 | 18,779 -> 75,615 | 93,457 | 3,850 |
| Ordinary memory | 3.607 | 30.52 | 18,773 -> 75,900 | 93,803 | 3,848 |

The repeat stage adds 12 receipts, 7 processed IDs and 2 deliberate responses, but no
scientific evidence or update records. Original inbox files remain, so storage still grows.
LMFT's full propagation traces cost substantially more storage and compute than ordinary
memory for the same observed behavior. Whole-history checkpoint copying/writing remains
unsuitable for unbounded operation; no consolidation was introduced.

## Preservation, limitations and next step

The ignored archive contains frozen protocol, all source/test files, model configuration,
SHA256 manifest, original inboxes, complete checkpoints, halted snapshots, activation
traces, accepted/rejected update provenance and machine-readable results. Back it up
separately: `outputs/` is outside Git. This report and the protocol preserve selected
findings in version control. Protocol SHA256:
`fa9e849238fb27e649dc98cb77d8dfbcf67e6d19b17c12019da4fdbc13233533`.
Earlier individuals still require their archived software because source-hash compatibility
checks intentionally refuse changed code. No automatic state migration was introduced.

This is a tiny authored fixture with ideal verification, fixed cue classes and known
relevance, not learned concept discovery, secure authentication, real-world epistemology,
autonomous contemplation or general understanding. Source strings alone provide no trust;
acceptance additionally requires exact registered selected-request evidence. Hostile host
access is outside the existing interface boundary. The verification-resolution update is
not prediction-accuracy learning. The baseline shares persistence/validation overhead and
is not a minimal possible memory implementation. Fact/Confidence selection utility remains
untested, and no fuzzy superiority was shown.

**Smallest next experiment:** preregister fresh mixed-availability cases with already
verified partial information, so verified support can suppress redundant investigation
under the same one-request budget. Keep a relevance-and-support ordinary-memory baseline
and the unchanged judgment equation. That tests the currently unexercised support gate
without adding an autonomous loop or tuning this fixture after its results.
