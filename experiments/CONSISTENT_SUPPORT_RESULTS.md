# Consistent support before suppression — results

Recorded 2026-10-11. [Preregistration](CONSISTENT_SUPPORT_PROTOCOL.md),
[implementation and commands](../docs/CONSISTENT_SUPPORT.md).
The prior [scoped results](SCOPED_ATTENTION_RESULTS.md) and their counterexample remain unchanged.

## Finding

The revised authored mapping investigates the known disagreement and avoids premature
closure in all nine fresh cases, matching ordinary memory. **Clarity changes prioritization,
not prediction quality; Fact and Confidence each suppress redundant requests in this circuit.**
The historical failure is reproduced exactly. No fuzzy superiority, discovered semantics,
or improved prediction accuracy is demonstrated.

Final archive: `outputs/consistent-support-002/`. **260/260 tests passed** (240 previous,
20 new parameterized cases), **475/475 experimental integrity checks passed**, and **11/11
preregistered research checks passed**. Research and integrity checks are recorded separately
so a negative research result would not be repaired merely to obtain an integrity pass.
102 primary individuals plus six sequential and one uninterrupted reference used actual
runtime processes; all 109 halted. All conditions made zero model or mock-inference calls.

Failed attempt preserved: `outputs/consistent-support-001/failure.json`. The harness initially
passed the alias known to the verifier instead of the emitted request's case ID q6. The
56 individuals from that attempt are halted and their data retained. Only verifier routing
in the harness was corrected; the protocol, mapping, cases and criteria were unchanged.
A development unit test also required canonical JSON comparison because persistence converts
tuples to lists; no scientific state change was needed. No evaluated mapping was tuned.

## Exact historical failure and revised mechanism

The old trace has normalized check1=false and check2=true, each individually nonconflicting.
The ordinary policy correctly says unresolved, but part coverage gives Fact=1. Direct
Confidence is 0, yet Fact->Confidence raises its propagated value to .25. Pass 1 Clarity
is zero; pass 2 input sum is .75+.3125-.25-1=-.1875, giving -.046875 after gain .25 and
clamping to zero. The selector therefore makes no request. The new historical condition's
complete selection trace equals the preserved post-hoc trace, not just its chosen action.

The new `consistent-support-1` circuit separately records verified observations, required
part coverage, normalized inconsistency and sufficiency. An ordinary external task rule
handles equality versus complementary-property measurements. It is that rule, not geometry,
that identifies disagreement. All conditions, including memory, receive the same information.
Raw observations retain their original values, scope, identities and provenance.

The revised mapping removes Fact->Confidence. Fact encodes coverage; direct Confidence
encodes complete consistent support; Clarity encodes unresolved inconsistency. Their outgoing
edges contribute to an existing Execution leaf used only as a temporary request-priority
readout. Existing propagation equations are unchanged. The positive-score readout, one-request
budget, ID tie-break and shared task-relevance exclusion are named external rules. Conceptual
selection has no blanket resolved-state override. The shared prediction eligibility gate is
ordinary code and is not credited to propagation.

Route weights remain A=.25/B=.75/D=.5, with both relevant candidates using B. Existing prior
outcomes recreate +1/3,-1/3 judgments; neither routes nor judgments learn from fresh outcomes.
The historical condition calls the original selector unchanged. On new tasks it receives
the shared relevance/normalization adapter; old equality regressions are identity-transformed.

## Fresh evidence: nine cases only

| Condition | Requests | Redundant | Useful unresolved | Premature suppression | Correct / predictions | Abstentions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Historical mapping | 4 | 0 | 4 | 1 | 4/6 | 3 |
| Revised full | 5 | 0 | 5 | 0 | 4/6 | 3 |
| No Clarity influence | 5 | 0 | 5 | 0 | 4/6 | 3 |
| No Fact influence | 9 | 4 | 5 | 0 | 4/6 | 3 |
| No Confidence influence | 9 | 4 | 5 | 0 | 4/6 | 3 |
| Ordinary memory | 5 | 0 | 5 | 0 | 4/6 | 3 |

Every condition predicts six of nine cases, with four correct: **accuracy 4/6 (66.7%)**
among predictions and **coverage 6/9 (66.7%)**. f2/f6 are wrong despite sufficient support.
Changing investigation does not improve prediction quality in this fixture. Abstentions
are separate, never counted as correct.

Revised full/memory investigate f2 missing support, f3 cross-part disagreement, f4 a new
within-part contradiction, f7 missing support despite duplicates/foreign evidence, and
f8 multiple uncertainties. They make no request for f1 complete support, f5 irrelevant
color disagreement, f6 unverified opposing assertions, or f9 compatible complementary
measurements. Color exclusion comes from the shared declared relevance gate. False/true
in f9 is compatible because check2 measures the opposite property; the selector does not
label arbitrary differing values contradictory.

Historical mapping suppresses investigation entirely on f3. It also selects the missing
payload question on f8 instead of the inconsistent shielded question. It therefore leaves
relevant inconsistency uninvestigated in two cases. No-Clarity leaves inconsistency
uninvestigated in one case (f8); full and memory in zero. Selecting another unresolved
question is recorded separately from literal no-request premature suppression.

The additional full-pathway request is an investigation, not a successful resolution:
f3/f4/f8 remain explicitly uncertain. Full/memory have three unresolved cases after their
budget is spent. Historical has two after spent budgets, plus f3 with an unused budget
and incorrect suppression. No condition silently converts these contradictions into facts.

## Causal attribution and ablations

- **Clarity:** in f8, full priority for inconsistent shielded is .265625, tied with missing
  payload; the unchanged ID tie-break selects shielded. Removing only Clarity->Execution
  reduces shielded to .015625, so payload wins. This is a causal priority contribution.
  Both choices still abstain after one request. Clarity is **not necessary** to keep the
  known counterexample eligible: without it, .015625 remains positive. The removal of
  unearned Fact->Confidence inhibition already prevents that historical zero-score failure.
- **Fact:** removing only Fact->Execution changes complete-support priority from 0 to
  .015625 and causes four redundant fresh requests. No prediction benefit appears.
- **Confidence:** removing only Confidence->Execution likewise causes four redundant
  fresh requests. Its distinct input is sufficiency, not merely having verified records.
- **Ordinary memory:** explicit scoped sufficiency and inconsistency-first ordering matches
  full choices and aggregate results. Its external rule supplies the same task knowledge;
  no architectural superiority can be inferred from this circuit reproducing that policy.

Exact outgoing-edge tests show direct inputs, all other edges, route weights and evidence
are preserved. Each revised ablation disables one edge only. These causal effects depend
on this chosen mapping/threshold; they are not established psychological meanings or an
argument that these named nodes are universally necessary.

## Known historical counterexample — separate regression

The exact previously inspected q6 check1=false/check2=true records, plus valid payload,
are not fresh held-out evidence. Historical mapping makes zero requests and reproduces
improper suppression. All five other conditions request shielded, including No-Clarity.
The reply adds agreeing observations but cannot erase the original disagreement: **all
six conditions abstain**, with zero predictions and undefined accuracy. Reopening the
question is demonstrated; resolving the contradiction is not.

## Previous preregistered cases — separate regression

These are unchanged q1..q7 inputs/policies from the previous study, never pooled with fresh
cases for accuracy or generalization claims.

| Condition | Requests | Redundant | Useful unresolved | Premature suppression | Correct / predictions | Abstentions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Historical mapping | 5 | 0 | 5 | 0 | 4/6 | 1 |
| Revised full | 5 | 0 | 5 | 0 | 4/6 | 1 |
| No Clarity influence | 5 | 0 | 5 | 0 | 4/6 | 1 |
| No Fact influence | 7 | 2 | 5 | 0 | 4/6 | 1 |
| No Confidence influence | 7 | 2 | 5 | 0 | 4/6 | 1 |
| Ordinary memory | 5 | 0 | 5 | 0 | 4/6 | 1 |

Historical, revised full, No-Clarity and memory match the previous five-request result.
Removing Fact or Confidence adds two redundant requests. Every condition has 4/6 accuracy
among predictions and 6/7 coverage. The original negative cross-part finding remains intact.

## Sequential reopening, restart and duplicate evidence

A separate f4 run starts fully resolved, halts/restarts, and then receives a new eligible
check2=false observation. Historical, revised full, No-Clarity and memory initially save
their budget and then reopen/request shielded. No-Fact and No-Confidence already spent
their one request redundantly before the contradiction and cannot request again; their
uncertainty state still reopens. No budget is reset. A third evaluation confirms the
spent budget and continued abstention. No accepted contradiction is deleted or outvoted.

All six restarted runs preserve exact state before new input. Restarted revised full and
uninterrupted revised full match scientific state and question references. Five new-ID
redeliveries plus five exact messages add no evidence, accepted changes, propagation traces,
questions or learning. With the barrier they add 11 receipts, 6 processed IDs and one
acknowledgment. Checkpoint growth is 2,628–2,631 bytes; original inbox files also remain.

Tests cover compatible differences, genuine cross/within-part disagreement, partial
support, scope isolation, assertions/duplicates, exact historical values, precise ablations,
reopening, one-request limits, hidden-truth isolation and interrupted commits. Inspection
is refused during runtime. Only deliberate outbox/lifecycle communication is consumed
while running; all internal diagnostics and outcome scoring occur after halt.

## Descriptive costs

Totals below cover nine fresh individuals per condition. Wall time includes startup,
communication and halt; core time excludes checkpoint serialization/commit. Individual
sizes exclude separately saved halted snapshots and source archives. No significance test.

| Condition | Wall s | Core ms | Checkpoint bytes | Individual bytes |
| --- | ---: | ---: | ---: | ---: |
| Historical mapping | 5.078 | 94.98 | 760,992 | 811,426 |
| Revised full | 5.190 | 101.09 | 767,150 | 818,418 |
| No Clarity influence | 5.182 | 100.35 | 763,476 | 814,584 |
| No Fact influence | 5.617 | 107.75 | 775,178 | 829,144 |
| No Confidence influence | 5.711 | 107.02 | 775,359 | 829,327 |
| Ordinary memory | 5.280 | 83.48 | 434,373 | 485,645 |

Memory retains substantially less diagnostic data while matching full behavior. Timings
are descriptive and do not establish a speed ordering. Full-history copy/write costs and
retained inbox files remain; no consolidation or long-running service is introduced.

## Preservation, remaining limits and next experiment

Source/config/protocol/test snapshots, original messages, accepted/rejected records,
complete activation traces, halted states and machine-readable results are preserved in
the new archive. Historical reports and the original counterexample are also snapshotted.
Protocol SHA256: `a97e068a5adfccb2161994817ca3fa54c59cdcf84f946d7af74d7e5e02d78d0a`.
Raw outputs remain ignored by Git and need separate backup. These selected results and
protocol are repository documentation. No previous output or historical report was edited.

The canonical seed, activation/propagation, judgment updates, migration, storage, contextual
and both previous attention implementations match earlier archived bytes. Only new versioned
modules and opt-in runtime dispatch are added. Existing source-manifest compatibility is
unchanged: older individuals require their original archived code, not silent conversion.

No primary revised suppression failure occurred, but accepted contradictions **remain
unresolved**. The evidence policy is append-only with no correction/retraction mechanism;
more corroboration cannot settle them. Useful investigation need not yield useful information.
No-Clarity's alternative f8 request has identical prediction quality, so the benefit of
inconsistency-first priority remains unproved. The experiment assumes authored relevance,
known equality/complement relations, exact synthetic verification and conflicting report
menus; it does not establish open-world grounding, learned semantics, calibrated confidence,
absence of all future counterexamples, or broad autonomous cognitive capability.

**Smallest justified next experiment:** preregister a bounded, explicitly authorized
correction of one erroneous observation, retaining the original and the correction's
provenance. Compare whether contradictions can then be resolved without silently deleting
history, using the unchanged counter and ordinary-memory baseline. Keep budget one and
route weights fixed. That addresses the observed inability to settle accepted conflicts
before adding further conceptual machinery or autonomous contemplation.
