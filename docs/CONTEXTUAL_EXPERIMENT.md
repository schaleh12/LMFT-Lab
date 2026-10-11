# Context-dependent learning and clarification

See the [preregistered protocol](../experiments/CONTEXTUAL_PROTOCOL.md) and
[results](../experiments/CONTEXTUAL_RESULTS.md). Historical
[propagation-equivalence findings](../experiments/COMPARATIVE_RELIABILITY_RESULTS.md)
remain unchanged: diagnostic activations did not cause revision.

## Mechanism

The explicitly authored Boolean feature is `shielded`. Registered transmission
outcomes are verified by executing the procedure. Both feature values have successful
and failed outcomes. LMFT retains a separate judgment for each value using the existing
sum(signs)/(n+2) helper and thresholds. The current case selects exactly one branch.
Independent conditional-memory and aggregate recounts provide comparisons.

This is ordinary conditional lookup, not fuzzy reasoning or feature discovery. No
propagation ablation is relevant: propagation does not participate. Existing Fact,
Execution and Confidence concepts can describe these records, but no founding nodes,
weights, numerical equations or migration rules change. The feature is authored;
its outcome association is retained from evidence. All deterministic conditions get
the same evidence, cases and replies, and make zero model calls.

The live interface remains outbox communication plus lifecycle acknowledgments.
Inspection and probes are permitted only after halt. This is an interface boundary,
not protection against a filesystem owner. See [the runtime guide](INTERACTIVE_RUNTIME.md).

## Structured operations

Context modes use the existing version-1 envelope, sender/source, observation or
teacher_reply type, ID and reply_to. Content is exactly text, operation and record:

| operation | record | effect |
| --- | --- | --- |
| outcome | evidence_id, procedure, payload, shielded, disturbance, output | Verify registered outcome and revise selected counter |
| evaluate | case_id, procedure, payload, shielded (Boolean or null) | Select branch or ask for missing condition |
| condition | evidence_id `condition/<case_id>`, case_id, Boolean shielded | Verify linked reply and resolve that pending case |
| barrier | Empty object | Deliberate completion response; no learning/model call |

A missing condition is never supplied automatically from the registry. A linked reply
must match the open request and registered case/value. Irrelevant, malformed or false
answers leave it pending. Condition evidence retains source, record, message and request
references; it selects a judgment but is not a successful/failed trial. One question
per pending case is emitted; waiting or retransmitting a missing query cannot cause
repeated calls/questions. Scope exclusions receive no prediction or clarification.

The registry provides synthetic verification, not real-world factual authority. The
validator can access registered condition truth; evaluation does not silently use it
to fill missing input. This is controlled information withholding, not an assertion
that the entire program lacks access to the registry. A teacher message cannot modify
seed, permissions, code or policy. Pure probes return scores/evaluations without learning.

## Identity and storage

Message ID identifies delivery. Evidence ID plus canonical full JSON payload (including
types) identifies an outcome. Equal text is not identity: distinct registered events
with identical text count separately. Conflicting reuse of an accepted evidence ID
is rejected, never overwritten. Under a new message ID, the same accepted evidence
adds only a lightweight receipt with source, hash, original-message reference and
current version; no repeated revision, model trace or outgoing result is produced.
Exact delivery duplicates retain the original receipt behavior. Raw inbox files and
checkpoint writes remain, so growth is reduced rather than eliminated. Rejected or
learning-disabled outcomes are not in the accepted ledger; repeats can retain small
rejection records, without model calls.

Outcome deduplication never replays a score. Evaluation caches are separate and keyed
by complete available case, judgment version, comparison mode, policy and accepted
condition evidence/provenance. Source/model settings are frozen at birth. Unchanged
contexts can reuse a checked rendering; new evidence increments the version and forces
fresh evaluation. A model failure uses an explicit authored fallback, cached for that
context; no automatic retry loop exists. Pending requests and accepted replies survive
the existing atomic checkpoint commit/recovery process.

Histories, raw inbox files, cache entries and whole-history writes still grow. No broad
consolidation, autonomous contemplation or major infrastructure is introduced. Earlier
checkpoints require their archived code/config to restart; no automatic conversion is
performed. The original channel and reliability fixture paths remain available.

## Reproduce on Windows

Run from the repository root with the existing Python environment:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_contextual.py --output outputs/my-contextual-study
.\.venv\Scripts\python.exe experiments/run_contextual.py --local --output outputs/my-contextual-wording
```

Use fresh output directories. The first experiment runs aggregate, conditional memory,
LMFT, a learning-disabled control, process restart and an uninterrupted comparison.
The second is real offline inference using the existing pinned model/backend cache;
see [model setup](LOCAL_MODELS.md). Sources, tests, config and protocol are archived
before each run. Raw outputs remain ignored by Git; back them up separately.

## Manual supervised exchange

In terminal 1:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson start --new context-lesson --experiment context-lmft --mode fixture
```

In terminal 2, publish the eight registered outcomes with intentionally identical text:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -c "from lmft_lab.contextual import outcome; from lmft_lab.runtime_store import Store; [print(Store('outputs/context-lesson').submit({'schema_version':1,'id':'outcome-'+k,'sender':'codex','source':'registered-transmission-fixture','type':'observation','content':{'text':'Recorded fixture information.','operation':'outcome','record':outcome(k)}})) for k in ('s1','s2','s3','s4','u1','u2','u3','u4')]"
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson receive
@{
  schema_version=1; id='missing-m1'; sender='codex'; source='registered-transmission-fixture'; type='observation'
  content=@{ text='The shielding condition is not supplied.'; operation='evaluate'
    record=@{ case_id='m1'; procedure='transmit-1'; payload=9; shielded=$null } }
} | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 outputs/context-question.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson submit --file outputs/context-question.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson receive --after 8
```

Read the actual clarification ID. For exactly this new individual and eight outcomes
it is `out-9`; substitute the returned ID if the history differs:

```powershell
@{
  schema_version=1; id='answer-m1'; sender='codex'; source='registered-transmission-fixture'; type='teacher_reply'; reply_to='out-9'
  content=@{ text='Registered m1 is shielded.'; operation='condition'
    record=@{ evidence_id='condition/m1'; case_id='m1'; shielded=$true } }
} | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 outputs/context-answer.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson submit --file outputs/context-answer.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson receive --after 9
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson stop
```

Wait for `halted` in terminal 1, then inspect or restart:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson probe
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson inspect > outputs/context-diagnostics.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/context-lesson start --experiment context-lmft --mode fixture
```

Other modes are `context-memory` and `context-aggregate`; creation and restart must
match. Use `--learning-disabled` consistently for the control. Use `--mode local
--offline` consistently instead of fixture for the real constrained wording path.

## What local wording establishes

Only a new evaluation or targeted question may call the model. It selects one of two
complete verified renderings via JSON enum grammar. Exact membership is independently
checked before emission. Both include prediction or missing-input abstention, evidence
references and uncertainty. Outbox `wording_origin` distinguishes authored,
model-constrained and authored-fallback text. Diagnostics retain exact requests,
responses, model/backend pins, latency and server PID, inspectable after halt only.

This is genuine inference with constrained formulation, not unrestricted prose or
independent semantic verification. No comparative model-assisted superiority claim is
made. No genetics, visual processing, robotics, new seed branches or automatic Codex
bridge are included.
