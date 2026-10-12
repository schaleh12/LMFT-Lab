# Passive supervised relationship sets

The new opt-in modes `relationship-set-lmft` and `relationship-set-memory` use the
existing supervised inbox/outbox, receipts, locks, atomic checkpoints and lifecycle.
The [frozen integration protocol](../experiments/PASSIVE_RELATIONSHIP_PROTOCOL.md)
and [results](../experiments/PASSIVE_RELATIONSHIP_RESULTS.md) distinguish integration
correctness from prediction accuracy. There are no observation requests or model calls.

## Start a new individual

PowerShell, repository root:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-passive start --new passive --mode fixture --experiment relationship-set-lmft --relationship-scenario ambiguous
```

Use `relationship-set-memory` for the equally equipped comparator. Registered
scenarios are unsupported, supported and ambiguous. The scenario/task policy is
pinned in the manifest; restart with exactly the same mode/scenario/control and
omit `--new`. The new modes require fixture operation and reject `--mode local`
before loading model configuration. Existing model configuration is unchanged.

The fixture is `capacity-blocked-two-1`: a noiseless bounded-write device with a
known synthetic length-two refusal fault. It is separate from capacity-transmit-1.
Source identifiers are attributed registration labels, not authentication. Exact
simulation verification is not a general real-world evidence validator.

## Operations and observable behavior

Submit the existing observation envelope (schema_version,id,sender,source,type,content).
Content must contain exactly text,operation,record. Example eligible first outcome:

```json
{
  "schema_version": 1,
  "id": "train-1",
  "sender": "fixture-operator",
  "source": "registered-insufficiency-1",
  "type": "observation",
  "content": {
    "text": "Registered synthetic outcome; verify before learning.",
    "operation": "outcome",
    "record": {
      "evidence_id": "t1", "scenario": "ambiguous", "split": "train",
      "procedure": "capacity-blocked-two-1", "length": 1, "capacity": 3,
      "success": true
    }
  }
}
```

The verifier checks registration, procedure, scenario, phase, strict value types,
features and simulated label before admitting evidence. Receive deliberate responses
with the existing `receive` command; inspect/probe remain unavailable while live.
The [fixture](../src/lmft_lab/insufficiency_fixture.py) and
[original protocol](../experiments/INSUFFICIENCY_PROTOCOL.md) define all registered splits.

- `outcome`: admit verified training/validation evidence, retaining source/record and message links.
- `select`, empty record: require all four training events, close training and retain all consistent hypotheses with candidate error refs.
- `accept`, empty record: require all four reserved validation events, check the retained set without filtering/resurrection; empty sets cannot pass.
- `evaluate`, observable case record: emit a prediction/consensus trace and scientific/provenance digests; update only communication metadata.
- `barrier`, empty record: acknowledge processing completion.

Teacher replies, proposals, requests and acquisition operations reject. No autonomous
loop or waiting computation exists. A new-ID copy of already recorded evidence gets
a duplicate response without learning; exact message replay uses existing runtime
deduplication and emits no new response. Conflicting identities preserve originals.
Rejected inputs are retained in receipts/inboxes, outside learner evidence/trace.
`--learning-disabled` rejects outcome/select/accept before verification; evaluation
and barriers remain available without scientific revisions.

The persisted learner distinguishes untrained, one supported hypothesis, multiple
supported hypotheses (ambiguous) and an explicitly empty set (no_supported_hypothesis).
Validation status is separate: not_validated, validated, validation_rejected or
no_supported_hypothesis. Unvalidated predictions abstain. Accepted multiple hypotheses
decide only on unanimous votes; disagreement abstains with hypothesis_disagreement.
An empty set abstains without votes and does not diagnose why the vocabulary fails.

After a graceful stop, `probe` returns the hypothesis-set summary without modifying
the checkpoint. `inspect` returns the complete halted state. Existing runtime shutdown,
read-only receive and atomic state/output/cursor commit contracts apply unchanged.

## Compatibility and limitations

No silent migration is implemented. Existing checkpoint manifests pin ALL package
source files, so adding the new mode changes software identity even for old modes.
Use archived software/configuration to resume old individuals; do not edit their
manifests or checkpoints. Original capacity behavior still has regression coverage
under the new source but historical manifests are not automatically compatible.

The learner/fixture, founding seed, numerical equations, thresholds and migration
code remain unchanged. Both runtime modes inherit the same inert scaffold; ordinary
memory does not use it for inference. This integration does not make fuzzy propagation
causal or establish general understanding. Supported-by-training rules can still be
wrong on held-out context/fault cases; those negative results remain in the report.

Reproduce the fixed integration in a fresh output path:

```powershell
.\.venv\Scripts\python.exe experiments/run_passive_relationship.py --output outputs/my-passive-integration
```

Preserve the complete local output archive; outputs are ignored by Git. No active
acquisition is implemented in this priority.
