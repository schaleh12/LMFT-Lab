# Supervised fixed-command correction sequence - results

2026-10-12. New opt-in `action-command-lmft` and `action-command-memory` modes connect
the bounded action policy to real runtime inbox/outbox, receipts and atomic
checkpoints. Pending requests and later conflicting evidence survive actual restarts.
Scalar memory matches exactly; known errors and the physical replay limit remain.
This is deterministic synthetic interaction, not freeform chat or autonomous agency.

## Contract, source and compatibility

[Protocol v1](ACTION_RUNTIME_PROTOCOL.md) was frozen before evaluation. SHA256:
`61f707c7bee642f4ad7b354b4f764a12e14a233270f3210766c451e0063bc183`.
Starting HEAD `90c1b84a4092f5f82a76debbf2e637d7da092fe9`; all previous dirty work was
preserved in `outputs/action-runtime-prework-001/`, with 181 source files and
25,975 prior output-file hashes. No scientific criteria or protocol revisions occurred.

Implementation:

- [Shared action policy](../src/lmft_lab/action_policy.py): extracted existing
  prepare/select/request/receive machinery, re-exported by the original experiment.
  Defaults remain unchanged; an optional reply message ID connects accepted runtime
  corrections to the actual incoming message instead of a synthetic fixed ID.
- [Shared later-report registry](../src/lmft_lab/late_evidence.py): extracted the
  reviewed strict Boolean/schema registry, re-exported by the sequential experiment.
- [Fixed-command adapter](../src/lmft_lab/action_runtime.py) and minimal
  [runtime registration/routing](../src/lmft_lab/runtime.py).
- [Usage/command contract](../docs/ACTION_COMMAND_RUNTIME.md),
  [integration harness](run_action_runtime.py),
  [fault worker](action_runtime_fault_worker.py), [tests](../tests/test_action_runtime.py).

The existing correction engine and its evidence-registration seam are unchanged by
this integration. There is no parallel ledger or second truth store. Initialization
explicitly reuses the authored fixture setup and stores its complete setup receipts;
historical outcomes are replayed inputs, not newly learned experiences. Seed40,
equations, weights, thresholds, model configuration, correction permits and migrations
are unchanged. No dependencies or model/mock completion calls were introduced.

Existing passive/active/default algorithms retain their behavior. Adding source files
changes the source-wide manifest, so old checkpoints require their archived source
and configuration, including old modes. This is an explicit compatibility limit, not
silent migration. An actual changed-mode restart was rejected without changing the
checkpoint; the CLI probe was verified read-only after halt.

## Interface and authority boundary

Exact commands: `initialize r1`, `initialize r8`, `initialize r2`, `inspect`, `request`,
`reply`, `evidence`, `barrier`. Command text is capped at 32 characters; serialized
content at 4,096 UTF-8 bytes; existing envelope/inbox bounds remain. Errors have
short fixed reasons. Inspect returns current prediction/support separately from
historical request closure. Raw internal inspection remains refused while live.

Initialization/request require the configured synthetic command sender/source.
Reply/evidence require the synthetic fixture sender/source plus exact references,
scope and episode/request/operation correlation. These labels are not identity
authentication; arbitrary text or a claimed role cannot admit arbitrary records.
Strict schemas reject integer Boolean aliases before substantive receiver execution.
The legacy `teacher_reply` type is transport only; there is no teacher or model call.

One charged request persists for the individual's lifetime. Unrelated/malformed replies
reject without changing pending state. A well-formed correlated proposal reaching the
existing receiver closes the opportunity even if rejected. Identical retransmission
does not admit new evidence; conflicting IDs reject. No reset/refund/retry episode
is added. A later report may restore conflict while the historical request stays
resolved. This separation is visible in deliberate JSON output.

## Primary results

Final archive: `outputs/action-runtime-003/`; earlier runs001/002 remain preserved.
Three scenarios x two modes x uninterrupted/
restarted arms = **12 runtime individuals**, with 36 normal runtime process starts.
Each restarted arm halts at pending and late boundaries, proves an actual reload
retains the complete checkpoint, then resumes. All individuals halt successfully.

| Scenario, identical in both modes | Selected action | Before | After reply | After later stage/restart | Final scoped roots / stored records |
| --- | --- | --- | --- | --- | --- |
| r1 / c1 | verified correction | abstain | success, correct | abstain after conflict | 4 / 5 |
| r8 / c9 | verified correction | abstain | success, wrong | abstain after conflict | 4 / 5 |
| r2 / c4 | missing-part gather | abstain | success, correct | success; no later report | 3 / 4 |

After reply, each mode has **100% coverage and 66.7% accuracy** (2/3 correct).
Finally each has **33.3% coverage and 100% accuracy among the one remaining decision**.
These different denominators do not establish improved truth finding. The wrong c9
prediction is retained in pre-late output, and the later instrument report is registered
evidence, not independently proven ground truth. No seed/fuzzy advantage is claimed.

Every runtime individual matches its equivalent standalone reference on effective
evidence, full scoped ledger/root lineage, counters, weights, correction events,
selected action, budget and prediction. Circuit/memory scores and scientific state
match. Restarted/uninterrupted full semantic states match, excluding only outbox
timestamps and receipt processing durations; raw values remain archived. All stage
predictions were frozen before unchanged fixture labels were accessed for scoring.

Replay and invalid-input checks preserve effective support and budget. Numeric
replies/late reports, unknown text, wrong sender/source/correlation, unrelated late
case, conflicting evidence/message IDs and closed stale operations are rejected.
Repeated request does not spend again; identical replies and late reports add zero
records. The initial question remains historically resolved while c1/c9 current
support is inconsistent and prediction abstains. No automatic reopening or re-repair.

## Logical costs and interrupted commits

Per primary individual:

| Scenario | Policy requests | Action correction verifier calls / accepted replacements | Setup correction checks | Gather checks / admitted records | Late registration checks / admitted reports |
| --- | ---: | --- | ---: | --- | --- |
| r1, r8 | 1 | 1 / 1 | 0 | 0 / 0 | 1 / 1 |
| r2 | 1 | 0 / 0 | 1 | 1 / 1 | 0 / 0 |

Across 12 primary individuals: **12 requests**, 8 action correction checks and
accepted replacements, 4 setup correction checks/replacements, 4 gather checks/
admissions and 8 late registration checks/admissions. There are 168 rejection
receipts (15 per r1/r8 individual, 12 per r2); these include pre-receiver and transport
rejections, not 168 replacement verifications. Initial setup separately admits 32
instrument roots and replays 96 historical outcome messages. Final scoped inventory
is 44 roots /56 stored records. No replay adds an admission or another charge.

Standalone reference construction repeats equivalent operations: another 8 action
and 4 setup correction checks, 4 gather checks and 8 late registration checks.
Authored service payload generation/reconstruction is separate from requests and
receiver checks; these logical counts are not calibrated CPU measurements. Tests
perform additional work and are not included in primary-study costs.

Two actual fault children terminate with exit17 around Store's existing replace
boundary on a valid queued correction. Before-replace leaves the checkpoint byte
identical to pending; actual runtime recovery recomputes and admits once. Append-only
physical markers show **two verifier calls, one committed correction and one charge**.
After-replace retains the accepted correction; restart does not recompute it:
**one physical verifier call, one committed correction and one charge**.
Both fault roots retain interrupted/recovered checkpoints, queue envelope, physical
PID markers, lifecycle and any partial files. They add three physical correction
checks beyond primary/reference work. They do not issue a new policy request.

Normal runs, two recovery runtime starts and two abrupt fault workers are distinct
from the 12 primary individuals. This tests controlled process interruption, not
hostile storage, power loss or exactly-once external effects. Whole-history receipts,
inbox and outbox still grow; one request is not a total physical-work/storage cap.

## Verification and preservation

**229/229 study integrity checks**, **150 targeted tests** and **738 full actual-checkout
tests in148.73s** passed, with no final failures or skips. The targeted suite combines
41 new adapter tests with all 109 existing action/sequential tests. CLI checks are
saved separately in `outputs/action-runtime-cli-checks-001.json`.

The first targeted run retained **144 passed/1 failed**: the pre-replace assertion
compared an in-memory tuple-containing state against JSON-reloaded arrays. The
checkpoint was preserved and recovery/physical markers already passed. The check
now compares exact checkpoint bytes before/after interruption. No acceptance criterion
or scientific expected outcome changed. Failed test artifacts and the corresponding
188-file source snapshot remain in `outputs/action-runtime-targeted-001/` and
`outputs/action-runtime-targeted-source-001/`. Intermediate targeted run002 passed
145 tests in15.68s; final targeted run004 passed150 in16.21s.

The final archive has 190 hash-verified source/config/protocol files (run001 has189).
Before final
handoff edits, only runtime.py and the two experiment files delegating to shared
modules differed from the prework source snapshot; all other previous source bytes,
including correction.py, remained unchanged. All **25,975** captured prior output
files and **3,043** historical-baseline files retain their hashes. Separate historical
audit passed83 archived-source /134 protected /137 original-tree checks, including56
pinned-Git entries. Evidence: `outputs/action-runtime-preservation-001.json` and
`outputs/action-runtime-historical-audit-001.json`. No external backup is asserted.

Final review added two bounded fixes before handoff. Initialization now rejects a
prepared setup whose freshly read permits differ from the policy pinned in the
individual at launch; otherwise a mid-run permit-file change could replace that
authority during setup. A regression test confirms unchanged judgment/session on
rejection. Two additional tests prohibit service, verifier and held-out truth access
during circuit/memory request selection and inspection. This version produced
run002:229 checks,148 targeted and736 full tests in148.24s. Original run001 and its
733-test regression remain preserved.

A separate accounting reproduction found a well-formed false gather reply was
correctly rejected/closed but recorded zero gather checks, because the legacy
receiver flags successful gathering only. The new runtime adapter now records the
attempted exact-reference check for both acceptance and rejection, after strict
schema/correlation validation. It does not change the legacy default receiver.
Full/memory regression tests prove one check, zero admissions, one closed charge
and no extra work on replay. Before/after evidence is in
`outputs/action-runtime-gather-accounting-before-001.json` and
`outputs/action-runtime-final-verification-001.json`. The primary runs only used
valid gathering, so their recorded counts were unaffected. Final run003 reproduces
every metric and stage prediction from001/002. All three source archives verify;
no scientific criterion/protocol revision was required for these enforcement fixes.

Relevant raw artifacts within the primary directory:

- `provenance.json`, `archive-manifest.json`, `current-preservation-context.json`, `archive/`.
- Per individual: real `individual/inbox/`, `checkpoint.json`, `lifecycle.json`,
  `pending-halted.json`, `late-halted.json` for restarted arms, `final-halted.json`,
  `frozen-predictions.json`, `standalone.json`, `result.json`.
- `fault-before_replace/`, `fault-after_replace/`, aggregate `results.json` and
  `frozen-predictions.json`. Results record actual interpreter PIDs for every launch.

## Exact successful commands and review boundary

PowerShell at the repository root; use new paths for any subsequent run:

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -m pytest -q tests/test_action_runtime.py tests/test_action_correction.py tests/test_sequential_correction.py --basetemp outputs/action-runtime-targeted-004 --junitxml outputs/action-runtime-targeted-004.xml
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/action-runtime-context-003.json
.\.venv\Scripts\python.exe experiments/run_action_runtime.py --output outputs/action-runtime-003 --preservation-context outputs/action-runtime-context-003.json
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/action-runtime-full-regression-003 --junitxml outputs/action-runtime-full-regression-003.xml
.\.venv\Scripts\python.exe experiments/verify_preservation.py audit-historical --output outputs/action-runtime-historical-audit-001.json
```

Protocol and evaluated source archive precede this report/handoff; final handoff
context is captured separately. Changes remain uncommitted; no push, publication,
deletion, model call, seed/numerical change or settings change occurred. Stop for
coordinator review before demo polish or any next bounded task.
