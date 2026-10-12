# Opt-in receiver attempts — evaluated results

2026-10-12, [frozen protocol v1](RECEIVER_BUDGET_PROTOCOL.md), SHA256
`ed3cb3c53c5f7a9ca5bd70471de1c095d69fcb98af12d7ac0c28f84f9df548c6`.
Starting HEAD `c92d213beab89568e10bac7f121c6c7a59c1f17b`, with four dirty
handoff/report documents preserved before editing. Source/dirty copies and hashes:
`outputs/receiver-budget-prework-001/`. No reset/discard or archive rewrite occurred.

**The opt-in cap bounds checkpoint-accounted acquisition checks. It does not bound
physical verifier work across pre-commit rollback.** Valid evidence within budget
is admitted; false claims can exhaust the budget and block a later legitimate
reply. Equally equipped ordinary memory matches in every condition. Old unlimited
default behavior remains available unchanged when the option is omitted.

## Narrow implementation and ordering

[Handler](../src/lmft_lab/active_relationship.py),
[runtime option/policy](../src/lmft_lab/runtime.py), [harness](run_receiver_budget.py),
[tests](../tests/test_receiver_budget.py), [physical fault child](receiver_fault_worker.py).

Optional --receiver-attempt-budget accepts strict integers 0..8; None/omission
retains the original policy and episode schema. Finite options add a pinned rule,
limit, committed-attempt counter and exhaustion state, not new hypotheses/nodes.
The source-wide manifest and exact budget refuse changed-budget restart; no silent
checkpoint migration. Non-active modes reject the option before checkpoint creation.
The unchanged passive/active-default/current regression tests still run.

Ordering is envelope/message identity, learning gate, source/transport, exact
episode/request correlation, strict selected-case schema/features, accepted-fact
duplicate/conflict, pending phase/question, remaining budget, charge, verifier,
verdict. Malformed/unrelated inputs and exact duplicates/conflicts do not execute
the verifier or consume attempts. Failed claims do not become facts; a fresh-ID
copy of an eligible false claim costs another attempt while pending.

A false verdict on the final allowed attempt closes receiver_budget_exhausted;
late valid replies cannot compute, learn or reset it. A valid final attempt is
admitted successfully, with zero remaining budget but no denial/exhaustion outcome.
Budget0 still permits the existing request; its first eligible reply closes exhausted
without a verifier call. Cancellation retains all committed charges. Evaluation
never spends/checks/adopts or issues requests. Source identifiers remain synthetic
registration, not authentication, and no ingress-wide defense is claimed.

## Frozen runtime results and cost/coverage tradeoff

`outputs/receiver-budget-001/`: seven fixed sequences, both modes, restarted and
uninterrupted = **28 real runtime individuals**, all halted. Each issues one
request/unit; admissions remain <=1. All cases use the unchanged ambiguous
training/validation/held-out fixture and disagreement selector. Table applies
identically to LMFT and ordinary memory:

| Sequence | Limit | Eligible checks | Committed / normal physical checks | Admissions | Exhausted | Coverage / decision accuracy |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| zero | 0 | 1 | 0 / 0 | 0 | Yes | 50% / 75% |
| valid-first | 2 | 1 | 1 / 1 | 1 | No | 100% / 75% |
| false-valid | 2 | 2 | 2 / 2 | 1 | No | 100% / 75% |
| exhausted-late | 2 | 2 | 2 / 2 | 0 | Yes | 50% / 75% |
| fresh-ID-flood | 2 | 2 | 2 / 2 | 0 | Yes | 50% / 75% |
| last-valid | 1 | 1 | 1 / 1 | 1 | No | 100% / 75% |
| legacy-flood | None | 7 | 7 / 7 | 1 | No | 100% / 75% |

Eligibility includes the still-pending gate; zero's first eligible reply is denied
at the remaining-budget gate. Later exhausted/closed replies are phase-ineligible.
Normal physical counts are receiver call-site instrumentation in completed no-fault
runs, not a crash-proof physical upper bound. Legacy's committed count comes from
receipt execution totals; its episode retains the old schema without a cap/counter.

The flood is EXACTLY six distinct false reply IDs plus one valid reply, not arbitrary
traffic. Every individual handled 40–49 messages, below the frozen100-message bound.
Flood finite2 denies five later replies; exhausted-late denies the one valid later
reply. This is the explicit denial-of-service tradeoff: hostile but structurally
eligible claims can spend budget before legitimate evidence arrives. The legacy
reference resolves with seven checks; the capped case remains lt/le after two.
There is no claim to defend CPU, network or memory against arbitrary ingress.

Effective le cases answer8/correct6 (equality3/4, non-equality3/4); ambiguous cases
answer4/correct3, abstaining on all four equality cases. Accuracy among decisions
is75% in both. Original length-two fault errors remain, x1 is out-of-scope, no
held-out result learns or repairs hypotheses. Expectations are keyed to fixed
sequence fields, not observed resolution. All28 predictions were frozen before
any held-out label was scored.

Across main individuals: 28 requests/units,16 admitted acquisitions and60 receiver
checks. These normal-run counts are separate from reserved evidence verification
and the deliberately faulted physical-call tests. No teacher/model/mock calls,
seed activation, propagation or fuzzy advantage. Vocabulary, numerical equations,
thresholds, seed geometry, model configuration and migrations are unchanged.

## Physical rollback counterexample — retained negative result

Counter charge, verdict, question, receipt, output and cursor are computed before
one atomic checkpoint replacement. Computation already happened when replacement
fails. Two independent child processes and an append-only marker OUTSIDE the
scientific checkpoint record actual completed simulator calls:

| Budget1 false-reply fault | First recovered committed attempts | Physical calls after replay | Final committed attempts | Admission |
| --- | ---: | ---: | ---: | ---: |
| Before replacement | 0 | 2 | 1 | 0 |
| After replacement | 1 | 1 | 1 | 0 |

Before-replace replay exceeds the physical budget while the logical committed
counter remains1. No physical work is undone/refunded. After-replace recovery
retains spent/exhausted state and processed identity, so replay is a cheap duplicate.
Both final states are exhausted and retain ambiguity. These tests explicitly
DISPROVE a hard physical-at-most-budget claim. No reservation-first protocol,
durable execution journal or transaction redesign was implemented.

Exact full-suite fault traces:

- `outputs/receiver-full-regression-001/test_actual_child_process_atom0/physical-calls.jsonl`: two completed calls with different PIDs; before-replace failure/replay state files.
- `outputs/receiver-full-regression-001/test_actual_child_process_atom1/physical-calls.jsonl`: one completed call; after-replace failure/replay state files.
- In each: `individual/checkpoint.json`, `input.json`, `worker-before_replace.json` or `worker-after_replace.json`, and `worker-replay.json` preserve restored digests and process identity.

The worker marker is test-only, never production accounting. The finite guard gives
no crash-proof bound on physical work; repeated pre-commit failures could repeat
the same computation. A stronger guarantee needs a separately specified durable
pre-computation reservation/recovery policy, with its own evidence-loss tradeoff.

## Verification, preservation and accurate state

**618/618 integrity** and **84/84 quality** checks passed. Pending counters and
exhausted closure survive actual no-input process restart; final scientific state,
questions and semantic responses match uninterrupted references and memory. Direct
standalone cap references and retained hypotheses match. Full current checkout:
**574 tests passed** (130.93 seconds), including **22 receiver tests**. A prior
targeted receiver invocation passed 20; two explicit compatibility tests were added,
then 21 mechanism tests passed and all 22 passed within the complete suite.

Changed-budget actual restart (2->3) was refused before checkpoint changes; exact
budget2 restart subsequently recovered the pending state unchanged. Refusal stderr:
`outputs/receiver-full-regression-001/test_actual_restart_budget_cha0/changed-budget-refusal.json`.
Non-active rejection, invalid/zero budgets, last-valid success, cancellation/no refund,
cheap duplicates/conflicts and pure evaluation are covered. No failed evaluated
attempt or scientific criterion revision occurred in this follow-up.

Current-source context covers 167 files, SHA256:
`27a2fe645f940229d6261da63cf44c3a87187a4c458c6c1f9a91db39fc928fa9`.
Context and every archived source/config/protocol file matched at run completion.
This context precedes final report/handoff edits; recapture rather than reuse it
against later source. All regression studies use legitimate nonempty contexts,
without skipped tests or a no-prework snapshot.

Separate historical audit passed again (83 archived source entries, 134 protected
entries including 56 versioned omissions, full original 137-file tree). All 3,043
previously inventoried historical/failure files remain byte-for-byte unchanged.
Prior four dirty handoff/report files and source snapshots were preserved before
the narrow active/runtime edits. HEAD remains c92d213 at report preparation;
receiver implementation and handoff changes are uncommitted. All28 main lifecycle
records are halted; fault workers exit normally after controlled fault/replay.

Coordinator separately reported19 mechanism tests and exact omitted-option parity
against preserved prework for nine policies/eighteen states, plus unchanged prior
archive groups. These are attributed review evidence, distinct from the tests run
by this task. No source/configuration settings were changed to obtain the result.

## Commands and exact artifact layout

Completed PowerShell, repository root:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest tests/test_receiver_budget.py -q --basetemp outputs/receiver-targeted-tests-001 --junitxml outputs/receiver-targeted-tests-001.xml
.\.venv\Scripts\python.exe -m pytest tests/test_receiver_budget.py -q -k 'not real_receiver_budget_study' --basetemp outputs/receiver-unit-tests-002 --junitxml outputs/receiver-unit-tests-002.xml
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/receiver-current-context-001.json
.\.venv\Scripts\python.exe experiments/verify_preservation.py audit-historical --output outputs/receiver-historical-audit-001.json
.\.venv\Scripts\python.exe experiments/run_receiver_budget.py --output outputs/receiver-budget-001 --preservation-context outputs/receiver-current-context-001.json
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/receiver-full-regression-001 --junitxml outputs/receiver-full-regression-001.xml
```

Choose fresh paths and a newly captured context for reproduction. Under
`outputs/receiver-budget-001/`: archive/manifest, configuration.json, provenance.json,
current-preservation-context.json, frozen-predictions.json, results.json, then
`<branch>/<mode>-<sequence>/pending-halted.json`, `replied-halted.json` (restarted),
`final-halted.json`, `case-results.json`, `standalone-reference.json`,
`frozen-predictions.json`, and `individual/checkpoint.json`, `inbox/*.json`,
`lifecycle.json`. Branches restarted/uninterrupted; modes relationship-acquire-lmft/
memory; seven sequence names are in the frozen table. Raw messages/costs, questions,
budget counters, closure and legacy schema remain inspectable.

Stop after this follow-up for coordinator review. No subsequent task dispatch,
push, publication, archive deletion, teacher expansion or major dependency was
performed. Outputs remain local/ignored by Git; no external backup is claimed.
