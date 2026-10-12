# Learning a payload-length / capacity relationship

The bounded [protocol](../experiments/CAPACITY_PROTOCOL.md) and
[results](../experiments/CAPACITY_RESULTS.md) separate aggregate counting, conditional lookup,
relationship induction and an authored diagnostic rule. Predictors receive length and capacity,
not a fits flag. No teacher/model calls or seed activation occur.

## Supplied task and learned artifact

`capacity_fixture` defines a noiseless empty buffer with no draining, compression, overhead or
concurrent writer. Its evidence verifier simulates bounded writes for registered train/validation
samples. Held-out labels are executed only after the evaluator saves all predictions. Incoming
assertions are never sufficient to install facts or relationships. This synthetic verifier is
not production sensor authentication.

`capacity_relations` supplies six authored hypotheses: length lt/le/eq/ge/gt/ne capacity.
`capacity-comparison-1` has an exact four-field JSON schema (version, left, op, right). Its small
operator dispatcher accepts no code, nesting, constants or other operands. Scope is the fixed
procedure and strict integer values 0..8; Boolean/missing/out-of-range values are out of scope.
The range is declared applicability, not proof that every possible input was validated.

Selection requires a uniquely zero-error training candidate, with both labels and at least four
examples. The runtime also requires all six preregistered training events. Ambiguity retains no
selected candidate; validation cannot break the tie. Four fixed validation outcomes must all
match before acceptance. A failed validation does not select another candidate or retry.
Training closes before validation; held-out outcomes never enter either set.

Accepted state stores representation/version, training references/digest, all six candidate
error lists, validation checks, applicability and acceptance reason. This is a revisable
interpretation stored under the experimental judgment, separate from founding nodes. The
current study has one selection/acceptance lifecycle; later relationship revision is not yet
implemented. External proposals, even well-formed ones, cannot install/select a relationship.
The existing local teacher adapter remains available but unchanged and unused.

Operational facts are verified outcomes; explanations are candidate comparisons. Truth/Theory
and Fact node names do not participate in selection and no decorative activation was added.
What is learned is which member of an authored family fits supplied evidence, not autonomous
feature discovery or understanding of buffer semantics.

## Conditions and predictions

- `capacity-aggregate`: unchanged sum(signs)/(n+2) counter with existing +/-0.2 thresholds.
- `capacity-lookup`: the same counter per exact (length,capacity) pair; unknown pairs abstain.
- `capacity-lmft`: direct Boolean evaluation of an accepted relationship; abstain before acceptance.
- `capacity-memory`: identical induction, evidence and acceptance access, using the same code.
- `capacity-authored`: explicit diagnostic length<=capacity, not a learned condition.

Every mode retains the same verified splits, coarse counter and lookup records for comparison.
Validation is reserved, not fitted into counters. The relation predictor is new and explicit:
it has no counter-derived score or calibrated confidence. Prediction traces name the accepted
relationship, inputs, result and unchanged coarse counterfactual. Sharing induction with memory
means this is a representation/transfer check, not an implementation-performance contest.

Runtime operations use the existing observation envelope with text/operation/record. `outcome`
admits exact verified split records; `select` closes training; `accept` validates once; `evaluate`
records deliberate communication; `proposal` rejects external installation; `barrier` acknowledges.
The pure `predict` function is read-only. The same atomic checkpoint persists artifacts, evidence,
acceptance and output together. Inspect only after halt; use outbox/lifecycle while running.

## Reproduce

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_capacity.py --output outputs/my-capacity-study
```

The harness refuses existing output paths. Five restarted individuals and five uninterrupted
references receive identical messages and split access. It snapshots source/config/protocol,
preserves evidence/candidate/acceptance traces, and writes `frozen-predictions.json` before
held-out scoring. Raw outputs remain ignored by Git; copy the complete halted run for durable
external retention. No inference assets, network access or new dependencies are needed.

Inspect the completed LMFT relationship:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-capacity-study/restarted/capacity-lmft/individual probe
```

Historical modes and equations remain available. Old checkpoints still need their archived
source/config under the existing manifest guard; no migration or in-place conversion is added.
Prior uncommitted continuation work was preserved.
