# Local-SLM representation interface check — protocol 1

2026-10-13. Separate, bounded DEVELOPMENT interface inspection after the completed
negative lexical study. Maximum FOUR attempts, no retries/repairs/replacement cases
or prompt changes after outputs. No held-out efficacy claim; the prior 14-case
evaluation is consumed and is neither input nor tuning material here.

## Frozen inputs and calls

Verify approved development export SHA256
`77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`.
Sort the published sense keys actually present; take the first four, and select
the lexicographically first example ID for each. Include both development batches
in selection. Freeze these four IDs, original-record hashes, source hashes,
exact request JSON hashes and prompt/schema/source/config hashes BEFORE calls.
Sense labels serve selection only; never include them, document IDs, example IDs,
prior cues or evaluation results in a model request. User message contains only
indexed original surface tokens and the given target span/quotation. Compound
surface tokens remain single indexed tokens, including embedded spaces.

Use only `LocalModels.generate('interpretation', request, ..., validator)` with
explicit existing cache `C:\Users\schal\AppData\Local\LMFT-Lab\cache`, offline
mode and the unchanged `config/local_models.json`: Qwen3-4B Q4_K_M, revision
bc640142c66e1fdd12af0bd68f40445458f3869b, model SHA256
7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5,
llama.cpp b11429/CUDA12.4; context8192, output1024, temperature0, seed42,
timeout120 seconds. Verify existing model, backend archives AND extracted files
before invocation; stop if anything is absent/different. No download, extraction
repair, configuration/seed/equation changes, new dependencies or external services.
Do not invoke process_observation, production activation or other roles.

Start at most one owned local server and reuse it. Count and persist attempt intent
before every generate invocation. Contract rejection consumes its attempt and is
retained; the validator returns an explicit admissibility report so the transport
can continue without restarting a healthy server. `trace.status=validated` in this
API means the validator returned its REPORT, not that a proposed interpretation
passed: only report.admissible controls that distinction. Transport/startup/timeout
failure or loss of the owned process stops remaining attempts, with unattempted
cases recorded. Never restart or replace a server/model. Close only the owned server
in finally; preserve logs without exposing API credentials. No automatic resumption
of a partially run directory.

## Neutral proposal contract, not a learned state

The frozen JSON schema and fixed system prompt are generated from the contract
module and archived before calls. Exact output fields: integer schema_version=1,
status, target anchor, readings, uncertainties. Status `one_reading` requires one
reading; `alternatives` requires two; `insufficient_context` requires zero readings
and at least one uncertainty. Maximum three uncertainty strings, each1..240 chars.
No numeric memberships, seed-node mapping, sense-key classification, permission,
truth/confidence score or automatic action/admission.

Each reading has a concise gloss, 1..2 source anchors, 0..2 target-relative relations
and 0..2 conditions. Each relation/condition has concise text and1..2 anchors.
Every text is1..240 characters. An anchor is exactly integer start/end plus quote;
indices are zero-based, start inclusive/end exclusive, within original surface
tokens. Quote equals the exact space-join of that token slice. Output target must
equal the supplied target span/quote. Every reading must cite at least one
non-target context token. Overlapping spans are permitted and do not imply
independent support; duplicate identical ranges within one anchor list are rejected.
Alternative readings may share anchors. Empty, Boolean/float/out-of-range anchors,
wrong quotations, unknown fields, invalid statuses/counts or malformed JSON reject.

Quotation/schema validity proves attribution only. It does not establish whether
the proposed relation, gloss, condition or uncertainty is semantically justified.
Validated records remain `unverified_proposal`; rejected records retain exact raw
response and failure. Immutable source tokens/target, source hash, original input
hash and external original-export provenance remain associated with each record.
Keep the model/author, exact request/generation identity and trace digest. No output
is a verified fact, accepted permanent meaning or canonical philosophical relation.

One shared neutral record is available to both primary-facing and ordinary-memory
consumers using the identical read-only retrieval contract. Avoid duplicate wrappers
or extra inference. Test exact retrieval/digest equality and nonmutation across
actual subprocess restart; no claim of seed benefit follows from identical access.
Reuse Store/checksum/atomic JSON and a tiny experiment-local append/retrieve path,
not a new generic ledger/runtime. Exact duplicate record IDs/content are no-ops;
conflicting IDs fail without mutation. Pins remain strict, with type-sensitive state
validation. Synthetic tests cover all contract boundaries independently of corpus.

## Preregistered inspection and technical criteria

For each of the four fixed cases report attempted/unattempted, transport completion,
finish reason/token limit, elapsed time/usage, JSON/schema/anchor admissibility,
proposal status and counts, and exact source/request/response/trace hashes. Retain
all failures. No resampling or corrective prompts. Technical checks: assets/pins,
call cap, allowed inputs/settings/role, failed-response retention, source-anchor
validation, duplicate/conflict behavior, faithful equal consumer retrieval, actual
restart/nonmutation and appropriate regressions. Interface rejection is a recorded
negative natural result, not grounds to loosen validation.

Cautious human inspection separately asks: does the captured output express a
target-specific reading or relation beyond generic word co-occurrence; do its
anchors locate relevant context; are relations/conditions plausible, unsupported
or unclear from the supplied source; are alternatives/insufficient-context claims
honest? Use descriptive judgments with uncertainty, not semantic gold, calibrated
accuracy or independent benchmark scores. A meaningful gloss with bad anchors is
still inadmissible. A valid quotation with an unsupported interpretation is still
semantically unverified. Four development examples and potentially pretrained
material cannot establish efficacy, generalization or persistent cognition.

## Storage, recovery and stop

Raw corpus, frozen requests, responses, traces and checkpoints stay in a fresh
nonpublished child of
`C:\Users\schal\AppData\Local\LMFT-Lab\research-archives`, beside the existing
recovery archive without overwriting it. Preserve README/LICENSE/use notices.
SemCor/Brown licensing ambiguity remains; no publication or corpus text in repo,
source archives or result prose. Repo may retain source, synthetic tests, counts,
opaque IDs and hashes. Archive before editing, preserve all prior work/negative
results, update handoffs after completion. No commits/push/discard. Stop for
independent parent review, including if assets/server access blocks execution.
