# Binding restart consistency — corrective result

2026-10-12. **Initial binding-runtime integration acceptance was blocked by independent
review.** Its passing tests did not cover nested configuration and request-history
consistency. The owner authorized only this narrow fix. Corrective writer-run checks
passed; independent re-review subsequently accepted this narrow fix. No new study or feature was added.

## Review findings and preserved reproduction

Readable reviewer evidence:
`C:/Users/schal/Documents/Codex/2026-10-12/task/binding-runtime-review-audit-001/`
(`results.json`, `correlation-finding.json`). Exact copies are preserved in
`outputs/binding-restart-fix-prework-001/reviewer-*.json`; originals remain unchanged.

The reviewer independently reproduced28 tests,250 targeted checks,36 runtime
processes,36 state matches,4 compatibility checks and102,090 historical hashes.
They inspected806 full-test XML,1,530 primary checks,8,313 artifacts and220 source
hashes. **Runtime CLI worked during this review.** The earlier standalone study's
Git-scoped CLI preflight limitation is distinct.

| Checksum-valid copied-state inconsistency | Pre-fix actual restart | Consequence |
| --- | --- | --- |
| Nested informative -> frozen; manifest/launch still informative | Accepted |37 decisions became25 |
| Nested primary -> memory; outer configuration still primary | Accepted | Kernel mismatch accepted |
| request_id -> missing-outbox-request | Accepted | Real-request reply rejected; nonexistent-request reply admitted |

These are internal consistency defects, not inbox exploits. After freezing the fix
criteria, the writer reproduced all three on fresh pre-fix checkpoint copies. Each
started and halted; original checkpoints were untouched. Results, copied states and
reply transitions remain in `outputs/binding-restart-prefixed-probes-001/`.
The original positive integration evidence and negative review probes are preserved.

## Frozen criteria and narrow implementation

[Acceptance protocol](BINDING_RESTART_FIX_PROTOCOL.md) SHA256:
`8d267ebddff39d295d9212c5d4c458f0bd6e22f1e3cb4bbcb195905fe12519cf`.
The prework pin records16:52:19 UTC, before baseline reproduction and fixed-code
evaluation.222 source/config/document files were archived before production changes;
119,159 prior output files were hash-pinned. Starting HEAD remains
`341b4c8281847fcf676e9aa5fa9f837de159065b`; existing uncommitted work is preserved.

Only two production files changed:

- [binding_runtime.py](../src/lmft_lab/binding_runtime.py): `applies` recognizes binding
  identity at any existing layer; `check_runtime` checks the complete runtime context
  around the existing nested validator. Nested mode must match outer experiment and
  manifest; exact binding policy/condition and fixture rule/mode must agree.
- [runtime.py](../src/lmft_lab/runtime.py): read-only preflight before locks, verifier
  construction or lifecycle publication; repeat checking under the lock and against
  launch controls; guard direct input transitions, binding handler entry, resulting
  state and halt-only probe. Full software_manifest checks remain unchanged.

A selected request must uniquely resolve to an emitted clarification with matching
schema, ID/position/sequence, sender/source, cycle, query/payload and reply-to. It
links to the unique accepted selection receipt and processed message identity.
Training/no-query states reject orphan history. Admitted acquisition must match its
accepted correlated reply, evidence reference, record, source and later cycle.
Closure must follow selection and any reply and match its accepted close command.
Pending-with-admitted-reply remains valid; closed state retains historical links.
Duplicates and rejections add no new accepted history.

There are no new serialized fields, migrations, learning rules or authentication
mechanisms. Persisted evidence is not reverified against the registry. Two existing
unit-fixture setups now supply consistent outer mode/manifest identity; acceptance
criteria were not weakened. New tests:
[test_binding_restart_consistency.py](../tests/test_binding_restart_consistency.py).
Kernels, family, seed, numerical mechanisms, model/config and teachers are unchanged.

## Corrective verification

**103 focused tests passed in46.57s**: existing28 binding tests plus75 regressions.
Artifacts: `outputs/binding-restart-fix-targeted-001/` and matching XML.

- 29 actual subprocess rejection cases: nested/outer/manifest/launch mismatches;
  missing/duplicate/wrong-type requests; wrong query/text/source/sender/sequence/
  budget/correlation/cycle; missing selection/reply/closure; wrong evidence/reply
  linkage or closure order; pending-with-closure; training/no-query orphan requests.
  Every copied individual's entire file inventory and bytes stayed identical.
  No started lifecycle was emitted; each process exited.
- 27 direct-transition checks reject inconsistent state before mutation.
- 1 ordering check forbids verifier construction and confirms rejection before any
  worker construction or runtime.lock creation.
- 18 actual valid resumes cover both kernels, informative/frozen/no-acquisition and
  pending/replied/closed stages. Replies, duplicates, closure and emitted predictions
  match direct transitions; evaluation leaves learning state unchanged; all halt.

Each copied fixture retains `rejection-result.json` or `resume-result.json` evidence.
Summary: `outputs/binding-restart-fix-focused-summary-001.json`. The existing binding
test also exercises three actual runtime stages. Informative valid resumes retain
37/37 decisions; frozen/no-acquisition retain25/37 and12 abstentions. These are
regressions of the existing fixture, not new scientific results.

**881 full checkout tests passed in212.90s**, no failures/errors/skips:
`outputs/binding-restart-fix-full-001.xml`. This is writer-run verification, separate
from the reviewer's inspection-only806-test evidence. No fixed-code test run failed.
The initial integration's tuple/list comparison failure and the pre-fix inconsistent
restart probes remain preserved. No new primary matrix was run.

## Archives, preservation and reproduction

Evaluated source: `outputs/binding-restart-fix-source-001/`,224 files. Context:
`outputs/binding-restart-fix-context-001.json`, SHA256
`82316979de001c83fa833f1f0cc477d3585d4bb85f227f6ce963770a5b336a8c`;
source inventory digest
`340b46582e7d5e227414776312b5263f87bcd3045e3fe4916e4786e088bba323`.
Source remained unchanged throughout focused/full evaluation.

All119,159 captured prior output files and both reviewer originals are unchanged.
This includes the owner's19 demo files and exact44-file matching runtime under
`outputs/binding-runtime-prework-001/source`. The old session was never reopened;
its archived recovery route and all earlier artifacts remain intact.

Final handoff is separately saved in
`outputs/binding-restart-fix-handoff-context-001.json` and
`outputs/binding-restart-fix-handoff-source-001/`.
`outputs/binding-restart-fix-final-checks-001.json` records final source/preservation/
lifecycle checks; `outputs/binding-restart-fix-artifact-hashes-001.json` pins corrective
artifacts. The prework archive retains exact pre-fix source/config and reviewer files.

Reproduce only with fresh output names:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q tests/test_binding_runtime.py tests/test_binding_restart_consistency.py --basetemp outputs/binding-restart-fix-review-tests-001 --junitxml outputs/binding-restart-fix-review-tests-001.xml
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/binding-restart-fix-review-full-001 --junitxml outputs/binding-restart-fix-review-full-001.xml
```

No new study, commits, pushes, publication, discards or further task dispatch.
Session closed after independent acceptance, early before18:40 UTC. The authored finite family and
synthetic trusted evidence remain foundational limits; no tree/semantic superiority.

## Accepted independent re-review and session closeout

2026-10-12. The parent relayed independent acceptance of the narrow fix within trusted
local finite-fixture scope. Reviewer reproduced103 focused tests,29 actual rejected
restarts with copied bytes unchanged and18 valid resumes. All three original
inconsistency probes and two Boolean substitutions fail closed before lock/startup.
Reviewer verified224 evaluated source hashes,225 handoff source hashes,8,597
corrective artifact hashes and119,159 prior hashes, and found no active checked
runtime PIDs. The881-test full suite was inspected through XML, **not independently
rerun**. Writer execution and independent inspection remain distinct evidence.

Parent decision: stop this session early at the useful accepted checkpoint, before
18:40 UTC. No further engineering, studies, chat/demo work or monitoring is dispatched.
The read-only foundational reassessment found no more valuable small engineering
step justified within the remaining time. Binding learns evidence-dependent selection
within an authored finite family; query scoring, admissibility and episode policy
are authored. Binding modes retain the canonical seed but do not consult seed
activation/propagation for selection or predictions. Ordinary memory matches; no
useful seed advantage is demonstrated. Earlier Clarity influence changed rankings
without improved final decisions and with recorded utility harms.

The next recommended discussion is a discriminating propagation decision contract:
what decision propagation may influence, its authority relative to verified evidence,
and a falsifiable benefit against equally equipped memory and propagation-disabled
controls. This is an architectural choice requiring review, not authorization for
automatic wiring or another fixture study. No protected mechanism change is proposed.

Documentation-only closeout archive and evidence:
`outputs/session-closeout-20261012-001/`. Earlier archives and findings are retained.
