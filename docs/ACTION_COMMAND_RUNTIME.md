# Supervised synthetic action commands

This opt-in adapter accepts fixed commands and registered fixture records. It is
not freeform chat, an autonomous agent or a source of verified real-world facts.
The circuit and exact scalar memory use the same interface and one lifetime request.

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/my-action-individual start --new action-demo --mode fixture --experiment action-command-lmft
```

Use `action-command-memory` for the matched scalar selector. In another terminal,
submit a saved JSON envelope with the ordinary runtime `submit --file` command.
Start with an explicit authored setup, choosing r1, r8 or r2:

```json
{"schema_version":1,"id":"initialize","sender":"fixture-operator","source":"action-command-1","type":"observation","content":{"text":"initialize r1"}}
```

The setup retains registered instrument reports, historical outcome replay and
their receipts. It does not represent a newly learned history. r1/r8 offer correction;
r2 offers missing-part gathering after an existing preparation correction.
Initialization rejects a setup whose permits differ from the policy pinned at launch.

| Fixed text | Additional content | Effect |
| --- | --- | --- |
| initialize r1 / initialize r8 / initialize r2 | none | One explicit fixture setup |
| inspect | none | Current prediction/support and historical request closure |
| request | none | At most one eligible correction or gather request |
| reply | record | Correlated synthetic reply; independently checked by existing receiver |
| evidence | record | Exact registered later report after episode closure |
| barrier | none | Completion acknowledgment and current summary |

For commands, content has exactly `text`; reply/evidence have exactly `text` and
`record`. Text is at most32 characters and serialized content at most4096 UTF-8 bytes.
Existing runtime envelope/inbox limits also apply. Errors use short fixed reasons;
arbitrary input text is not interpreted as policy, authority or evidence.

Initialization/request require sender `fixture-operator`, source `action-command-1`.
Reply/evidence require sender `fixture-curator`, source `registered-instrument-log-1`.
These strings are synthetic local registration, not secure identity authentication.
Correct labels alone do not admit an arbitrary record: exact permits/references,
scope, real Boolean types and correlation checks remain necessary.

The `clarification_request` outbox message supplies episode_id, operation_id and its
own request ID. A reply uses type `teacher_reply` with `reply_to` equal to that ID;
its record has exactly episode_id, request_id, operation_id and payload. The payload
is the existing registered correction proposal or selected gather records. The
name `teacher_reply` is transport only; no teacher/model is called. Inspect the
[protocol](../experiments/ACTION_RUNTIME_PROTOCOL.md) and study harness for exact
synthetic service examples. Do not fabricate a reply from its narrative description.

The late registry contains only `late/c1/shielded/check1` and
`late/c9/shielded/check1`, value Booleanfalse, batch-1, registered-instrument-log-1.
Only the initialized case is eligible. A registered instrument report can be wrong;
admission establishes identity/provenance, not truth. Integer0 is not Booleanfalse.

Use `receive --after N` for deliberate live outbox messages. Internal `inspect` and
CLI `probe` are refused while running; send the fixed inspect command for a live
public support summary. It separately labels `current` and `historical_request`.
Later conflict can make current prediction abstain while the old request remains
historically resolved. Repeating request never replenishes its budget. Malformed or
unrelated replies reject before receiver execution; a correlated valid-schema reply
that reaches the receiver closes the one opportunity even if acceptance fails.
Gather verification accounting includes rejected well-formed replies; replay does
not add another verification or admission.

Stop with the runtime `stop` command. Resume using the same start command without
`--new`, retaining mode and options. Code/config/control changes reject restart;
use archived source for old checkpoints, with no silent conversion. Initialization
cannot be repeated. Read-only inspect/predict do not revise judgment, although normal
transport receipts and outbox history grow. One request is not a global storage or
physical computation bound, especially across an interrupted pre-commit calculation.

This interface is intentionally small. No model downloads, new dependencies,
freeform conversation, automatic re-correction or new action episode are provided.
