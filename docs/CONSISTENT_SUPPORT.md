# Consistent support before suppressing investigation

This versioned experiment preserves the earlier scoped mapping and compares it with a
revised circuit, three outgoing-edge ablations and ordinary memory. Read the
[preregistered protocol](../experiments/CONSISTENT_SUPPORT_PROTOCOL.md) and
[results](../experiments/CONSISTENT_SUPPORT_RESULTS.md). The historical failure remains
reproducible through the old modes and archived sources.

## Reproduce

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_consistent_support.py --output outputs/my-consistent-support-run
```

Use a fresh directory. The harness refuses overwrite, snapshots exact sources/tests/
configuration/protocol, and retains failed attempts. It uses actual separate runtime
processes, zero inference calls, no downloads, tokens or new dependencies. Nine fresh
cases, one known counterexample and seven old regression cases are scored separately
across six modes. Six sequential restart runs and an uninterrupted reference are additional.

Runtime modes: `consistent-historical`, `consistent-full`, `consistent-no-clarity`,
`consistent-no-fact`, `consistent-no-confidence`, `consistent-memory`. Use `--mode fixture`
with the existing [start/submit/receive/stop commands](INTERACTIVE_RUNTIME.md). Halt before
probe/inspect. Restart without --new using the same experiment/mode and original sources.
All route weights stay fixed, including under --learning-disabled; this study does not
learn associations. No autonomous scheduling or code modification is added.

## Explicit task policy versus numerical use

`consistent_fixture.py` registers public cases, evidence, selected-question replies and
separate evaluator-only outcomes. `consistent_attention.py` normalizes scoped observations,
computes coverage and consistency, and applies the versioned mapping. Exact evidence
validation, identity, attribution, atomic commit and question budgets follow the existing
supervised pattern. Operations remain outcome/evidence/evaluate/verification/barrier.

The ordinary external task rule is explicit: equal-property checks must agree; a declared
complement-property second check is inverted before comparison. Different raw values can
therefore be compatible. Raw evidence remains intact; normalized part values and evidence
IDs are traced. Coverage counts required parts with observations. Inconsistency means
both normalized Boolean values occur. Sufficiency requires full coverage and no conflict.
A fluent or confident assertion is not verified evidence. Contradictions are not erased
by later corroboration, and an unavailable resolution is retained as uncertainty.

The shared relevance gate excludes questions outside the declared pending decision.
The shared prediction gate requires sufficient relevant support and a valid payload
before using the unchanged prior conditional judgment. These gates and the task relation
are ordinary code, not abilities discovered by fuzzy geometry.

Revised inputs: Fact=coverage, Confidence=sufficiency, Clarity=unresolved inconsistency.
The Fact->Confidence inference is removed. Existing Novelty/Salience/Theory inputs feed
a temporary Execution priority readout, with negative Fact/Confidence edges and a positive
Clarity edge. Every coefficient and selection rule is frozen in the protocol. Positive
final priority determines eligibility; conceptual selection has no resolved-state override.
Outgoing ablations disable exactly one specified edge, retaining inputs, evidence and
other edges. Execution is an authored numerical readout, not an external action.
Named leaf activations are not changes to numeric confidence fields or founding principles.

The historical condition calls the original scoped-full selector unchanged. On fresh
cases it receives the same relevance/normalization adapter as all other conditions;
old equality cases are identity-transformed. Ordinary memory explicitly tracks insufficient
questions and prioritizes inconsistency before missing information using the same task rule.
Thus a causal edge effect demonstrates use of an authored result, not semantic discovery.

## Compatibility and archives

New developmental ledgers/case traces are separate from the canonical 40 nodes. No change
to activation/propagation equations, judgment updates, legacy migration, or previous source
modules occurs. The runtime adds only opt-in dispatch. Older checkpoints still require
their archived software because the source-hash restart check is unchanged; no silent
conversion exists. All live access is deliberate outbox/lifecycle communication, with
internal traces inspected only after halt. Raw outputs are ignored by Git and need separate
backup; selected results and the protocol are retained as repository documentation.
