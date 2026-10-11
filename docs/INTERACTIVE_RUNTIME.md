# Supervised persistent runtime

This implements the narrow [frozen mechanical protocol](../experiments/INTERACTIVE_REVISION_PROTOCOL.md),
not the complete developmental architecture. The existing 40-node seed, legacy birth
migration, activation and propagation equations are unchanged. A separate learned
judgment has evidence and accepted/rejected revisions. Codex remains an external
teacher/developer. No API bridge or continuously listening VS Code assistant is installed.

## Start and communicate on Windows

From the repository root in PowerShell, use the existing Python 3.12 environment.
[Local model setup](LOCAL_MODELS.md) covers installation, verified downloads and cache.
Open two terminals in the same repository. In **each** terminal set:

```powershell
$env:PYTHONPATH = 'src'
```

In terminal 1, start a new individual (foreground so Ctrl+C is available):

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson start --new lesson --mode local
```

The first processed input downloads the pinned assets if needed. After download,
add `--offline` to prevent any asset network access. For the deterministic mechanical
experiment, use `--mode fixture` instead: its three role proposals are explicitly
mocked, and no model is loaded. Always restart with the original mode and control.
The startup line is a lifecycle acknowledgment, not an LMFT utterance.

In terminal 2, submit an observation:

```powershell
@{
  schema_version = 1; id = 'lesson-1'; sender = 'codex'; source = 'supervised-session'
  type = 'observation'; content = @{ text = 'Does the synthetic channel agree with its reference?' }
} | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 outputs/lesson-observation.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson submit --file outputs/lesson-observation.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson receive
```

`submit` acknowledges queue publication only. Repeat `receive` after processing
finishes; it is read-only. The first cycle emits a response and clarification `out-2`.
Read actual IDs rather than assuming that number in an existing individual.
Submit a reply linked to that clarification:

```powershell
@{
  schema_version = 1; id = 'lesson-2'; sender = 'codex'; source = 'supervised-session'
  type = 'teacher_reply'; reply_to = 'out-2'
  content = @{
    text = 'The authored fixture lists sample-a as channel 3 and reference 3.'
    evidence = @{ sample_id = 'sample-a'; channel = 3; reference = 3 }
  }
} | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 outputs/lesson-reply.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson submit --file outputs/lesson-reply.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson receive --after 2
```

This is an example Codex exchange: observation → LMFT's authored request for eligible
evidence → attributed teacher reply → LMFT's rule-based response. The teacher can
supply or discuss evidence; a message cannot change code, seed, permissions, or rules.
Do software development separately, after halting the individual.

Request graceful stop in terminal 2, then wait for `halted` in terminal 1:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson stop
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson probe
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson inspect > outputs/lesson-diagnostics.json
```

The stop request finishes the active cycle and leaves pending inputs for restart.
`probe` and `inspect` fail until the runtime has released its lock. Inspection includes
original evidence, reasons, proposals and traces. Probe does not learn, decay or call a model.
Restart the same individual in terminal 1, without `--new`:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/lesson start --mode local --offline
```

To replay a delivery, submit the exact same message file. The original outbox IDs
remain retrievable; duplicates emit no new utterance. A new message ID carrying the
same sample is a new attributed proposal, rejected as repeated evidence.

## Protocol and boundary

Incoming JSON schema version 1 requires `id`, `sender`, `source`, `type`, `content`.
IDs/source labels are 1–96 ASCII letters/digits/underscore/dot/colon/hyphen (first
character alphanumeric). Types are `observation` and `teacher_reply`; only the latter
requires `reply_to`. Content has `text` and optionally `evidence`. Unknown envelope
or content fields are rejected. An optional string `timestamp` is metadata only.
Evidence is an attributed proposal, validated separately against the frozen table.
Total input is limited to 30,000 UTF-8 bytes; text to 6,000 characters; serialized
model input must also fit 6,000 characters or the cycle records a rejection.

Queue sequence is allocated under a short exclusive lock, independent of timestamps.
The runtime processes published files sequentially at cycle boundaries. Outgoing
records have version, stable ID, sender, authored source, type (`response` or
`clarification_request`), selected content, reply reference, cycle and output sequence.
`receive --after N` returns only deliberately emitted records with sequence > N.
Reading does not consume them; receivers deduplicate by output ID or keep a cursor.

While running, the teacher-facing interface exposes only outbox messages, plus
separate lifecycle/queue acknowledgments. It has no live state/probe endpoint,
activation stream, raw prompt dump or diagnostic feed. `inspect` and `probe` acquire
the same exclusive lock as the runner and refuse while it runs. This is an interface
boundary, **not filesystem security** against a host owner or code importing internal
storage functions. Keep private runtime directories out of shared/cloud-synchronized
locations when confidentiality matters; no access-control system is implemented.

Outgoing wording is entirely authored in this milestone. Clarification refers to
recorded missing eligible evidence or conflicting accepted signs; at most one
question is open, and each of these two issue types is asked once per lifetime.
A valid linked reply closes a request even if evidence is rejected. Invalid/closed
reply references cannot revise the judgment. Unanswered questions persist; waiting
causes no inference, learning, repeat question or checkpoint. The local SLM still
performs interpretation, digestion and bounded contemplation through the existing
processing path. Its suggested wording/judgments remain internal proposals.
Reflection's broader novelty/salience and Contemplation's clarity/confidence research
roles remain distinct; this fixture does not implement their full mechanisms.

## Revision and provenance

The [protocol](../experiments/INTERACTIVE_REVISION_PROTOCOL.md) freezes the four samples,
score equation, probe thresholds and acceptance criteria. The new judgment is
`fixture/channel-agreement`, not a seed node. Its score is not calibrated confidence.
Every unique eligible sample is verified against authored simulated ground truth,
counts once, and retains original content/source/message, sign and validation reason.
All evaluated proposals record accepted/rejected status, before/after and supporting/
contradicting IDs. No general real-world evidence verifier is implied.

Source file hashes, model configuration, mode, Python version and rule version are
frozen at birth. Restart refuses changed software/configuration or learning-control
flags. This format has no automatic upgrade: retain original code/config to resume,
or start an explicitly separate experiment. Existing legacy birth conversion is
unchanged; this runner does not import old birth JSON or one-shot diagnostic traces.
No preexisting persistent runtime schema was migrated.

The internal processing trace retains exact prompts, validated proposals, activation,
model pins, request hashes and failures. The legacy standalone trace field
`not_applied_revision_engine_not_implemented` remains for compatibility and describes
that proposal-only function; the enclosing runtime diagnostic has the actual separate
fixture revision. Model prose never supplies acceptance authority or evidence weight.

## Commit and recovery

`checkpoint.json` is the sole authoritative scientific record. It contains the fixed
birth/config, judgment/history, processed identities, inbox cursor/receipts, all
committed outbox records, questions and diagnostics, with a SHA256 integrity checksum.
A cycle computes privately, writes a new temporary file, flushes/fsyncs it, then
replaces the checkpoint. Replacement is the commit point: input receipt, evidence,
revision and outgoing messages become visible together. One OS lock prevents two
runners; the same lock gates inspection. The runtime retains one model adapter across
cycles, reusing its server when roles share the same model.

An interrupted pre-replacement calculation is retried from the last committed cursor;
this can repeat a model call (and produce different live text), but cannot duplicate a
committed revision/output. An interruption after replacement resumes past that input.
Unpublished `.partial` inbox/checkpoint files are ignored and retained for diagnosis.
Queued originals are retained. Files must not be manually removed/reordered/edited.
Malformed published JSON becomes a rejected receipt and generic outgoing response;
the original file remains. Same ID/different content becomes a conflict rejection;
identical redelivery, ignoring timestamp metadata, gets a duplicate receipt and no
new model call/output. Invalid CLI submissions fail before publication, so callers
must correct and resubmit. Model failures commit a visible rejection and retained
failure trace; retry requires a new message ID. Unexpected errors halt without
committing the active cycle. Ctrl+C may abort the uncommitted cycle; use `stop` to
finish it gracefully.

Assumptions: one host, local filesystem with atomic replacement, cooperative clients.
No multi-file transaction is claimed. Inbox publication and scientific acceptance
are separate. No power-loss/directory-flush durability, hostile tamper resistance,
cloud-sync conflict recovery, or distributed exactly-once delivery is claimed.
Checksums detect accidental alteration, not malicious re-signing. Corrupt checkpoints
fail closed; there is no automatic backup rollback. Copy the halted directory for
backups. Lifecycle JSON is advisory and may be stale after a crash; the OS lock is
what prevents a second runner. A force-killed parent may leave an orphaned model
server; the preexisting backend limitation remains.

## Bounds and reproduction

Each valid new message runs at most three bounded model calls. Existing configured
startup/request timeouts apply per operation (downloads retain the asset layer's
behavior); no recursive contemplation or retry loop is added. Waiting polls files
at 0.1 seconds and never calls a model. A single model stays resident until halt,
role switch, or failure. Histories, messages, traces and backend logs grow without
consolidation. Whole-history checkpoints use O(history) space/read/write per cycle
and O(history-squared) cumulative write volume: suitable only for short supervised
experiments. Stop and archive instead of treating this as an unlimited service.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe experiments/run_interactive.py --output outputs/my-mechanical-run
.\.venv\Scripts\python.exe experiments/run_interactive.py --local --output outputs/my-local-smoke
```

Use a fresh output path; the harness refuses to overwrite runs and retains failures.
Mechanical mode uses mocked proposals but actual separate Python runner processes.
Local smoke uses actual pinned offline inference. Both save results and complete
halted checkpoints under ignored `outputs/`. See the
[results report](../experiments/INTERACTIVE_REVISION_RESULTS.md) for what was exercised.
No claim of understanding, autonomous desire, mature personality, or fuzzy-tree
advantage follows from this mechanical persistence result.

## Second fixture and comparison modes

The optional `--experiment` selector now supports a separately registered procedure
fixture and its comparisons. The default remains `channel`. See
[comparative setup](COMPARATIVE_RELIABILITY.md) for exact commands, compatibility,
held-out scope, internal timing and bounded Windows file-sharing retries. The live
teacher boundary and single-checkpoint commit point above remain unchanged.

## Context-dependent experiment

Optional context modes use structured operation/record content, conditional judgments,
verified condition replies and versioned evaluation caches. See
[the contextual guide](CONTEXTUAL_EXPERIMENT.md). Original channel/reliability behavior
remains available; historical records are not converted.

## Attention-guided verification fixture

Optional attention modes use the same inbox/outbox and commit boundary for one-request conflict verification and separately stored route association updates. See the [attention guide](ATTENTION_EXPERIMENT.md). These modes make no model calls and retain existing counter equations.

## Scoped support fixture

The optional [scoped-support modes](SCOPED_ATTENTION.md) reuse the same commit and communication boundaries. They retain fixed route weights and compare outgoing Fact/Confidence influences. The documented cross-part conflict failure limits the selector to experimental use.

## Consistent-support fixture

Optional [consistent-support modes](CONSISTENT_SUPPORT.md) preserve the supervised interface and add a versioned mapping with explicit task relations, fixed routes and outgoing-only ablations. Previous scoped modes and their known failure remain available.

## Correction fixture

Optional [correction modes](CORRECTION_EXPERIMENT.md) preserve the same supervised interface and atomic checkpoint boundary. A pinned authority policy, append-only lineage and effective evidence view support scoped observation correction; prior outcome counters remain unchanged.

## Supervised local teacher connection

Opt-in [teacher modes](LOCAL_TEACHER.md) emit a deliberate teaching request and accept only a bounded, independently validated route proposal through the inbox. An explicit one-question adapter command uses a frozen profile; no background bridge runs. Teacher profile/config selection is pinned at birth and restart, and the existing communication boundary remains unchanged.

The [bounded briefing comparison](../experiments/TEACHER_BRIEFING_RESULTS.md) adds an explicitly selected v2 profile and fresh `--teacher-study beneficial` / `no-change` initializations. Default historical behavior, lesson schema, acceptance policy and communication boundaries remain unchanged. See the [evidence-learning handoff](EVIDENCE_LEARNING_HANDOFF.md) for the next task.
