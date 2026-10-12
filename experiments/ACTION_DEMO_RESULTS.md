# Thin local terminal demonstration - results

Follow-up: [actual hosted Ctrl+C correction](ACTION_INTERRUPT_RESULTS.md) supersedes
the unresolved keyboard-exit limitation below. This initial report and its failed
trials remain historical evidence; their original findings are not reclassified.

2026-10-12. A standard-library terminal wrapper now exposes the existing synthetic
action runtime for r1/r8/r2, in circuit and matched-memory modes. Direct runtime
replay and scientific memory parity pass. Real terminal request, reply, later report,
stop/resume, provenance, quit and EOF work. **Acceptance is incomplete for graceful
hosted-terminal Ctrl+C shutdown**; both failed trials are retained below. No new
learner, model calls, network service, dependencies or protected mechanism changes.

## Frozen contract and implementation

[Protocol v1](ACTION_DEMO_PROTOCOL.md) was frozen before evaluation; SHA256
`76b1a1aaf50803cc626cb82f3b9c478672fd44e0eb81c926a1ade57a1650497a`.
Starting HEAD: `90c1b84a4092f5f82a76debbf2e637d7da092fe9`.
Existing dirty sequential/runtime work was preserved in the 190-file source archive
and 45,224 prior-output hash inventory at `outputs/action-demo-prework-001/`.

[Wrapper](../src/lmft_lab/action_demo.py), [harness](run_action_demo.py),
[tests](../tests/test_action_demo.py), [launch guide](../docs/ACTION_TERMINAL_DEMO.md).
Only a new production module was added; all 190 prior source/config/document files
matched their captured hashes before this final documentation handoff. The existing
runtime, seed, equations, models, permits, migration and correction mechanisms are
unchanged in this task. The new module changes the existing source-wide manifest:
older individuals require archived source, not silent checkpoint migration.

The wrapper launches an owned fixture child, submits exact messages plus completion
barriers, reads deliberate public outbox messages, and stops through the existing
checkpoint-boundary protocol. It never writes scientific state. Explicit fresh roots
reject any existing path; default roots are unique. Explicit resume uses persisted
mode/scenario and scans inbox IDs to avoid collisions. Live output distinguishes
current support from historical closure. Internal provenance is read only after halt.
The transcript is append-only audit data, not recovery authority. Typed claims are
rejected commands; synthetic labels are not real-world identity authentication.

## Evaluation and denominators

Final scripted archive `outputs/action-demo-002/`: **116/116 integrity checks**,
three scenarios x two modes. Six wrapper individuals each use one logical request;
the direct replay creates six additional reference individuals with equivalent
requests. Wrapper submissions total32 envelopes per r1/r8 case and28 per r2 case,
including barriers and deliberate retransmissions. Six requests is not a claim
about the total physical work of running both wrapper and reference evaluations.

Each wrapper executes fresh, collision rejection and explicit resumed invocations,
with pending and post-evidence process restarts, malformed commands, exact replay,
exhausted request/reply attempts and provenance boundaries. Every submitted envelope
is replayed with identical IDs through a separate actual runtime. Complete semantic
state matches, excluding only outbox wall-clock timestamps and receipt processing
durations. Matched memory scientific states/actions/predictions agree in all three
scenarios. Repeated inspection/resume leaves scientific state and budget unchanged.

r1/r8 finish abstaining on later conflict, with historical request still
`resolved_by_correction`; r2 finishes success and `resolved_by_gather`. The known
r8 post-correction prediction error is retained. This is interface/persistence
equivalence, not a new scientific benefit or fuzzy-tree superiority. Zero model calls.

Both targeted invocations passed **9 tests** (15.27s then16.28s); final full checkout
passed **747 tests in166.32s**, no failures/errors/skips. Targeted tests use actual
children for wrapper/direct comparisons, unique paths, collisions, invalid script,
foreign/override resume and EOF/KeyboardInterrupt cleanup. The latter inject Python
exceptions at input; they do not simulate host-level console termination.

## Real terminal evidence and disclosed failure

`outputs/action-demo-interactive-001/` used an actual PTY: inspect/request,
stop/resume pending, reply, late, inspect, stop/provenance, resume and Ctrl+C.
Public output showed abstain -> success -> abstain, budget0 and retained originals.
Ctrl+C recorded `KeyboardInterrupt`, then the host terminated with exit
`-1073741510` before a halted acknowledgment; lifecycle remained `running`.

The only implementation follow-up isolated the child with Windows process-group
flags (or a separate session on other platforms) so a normally handled wrapper
interrupt can request orderly child shutdown. Final source was frozen into context002
and archive002 before reevaluation. Trial `action-demo-interactive-002/` still failed
under hosted PowerShell PTY Ctrl+C with the same exit/lifecycle outcome. The exact
host termination mechanism was not independently diagnosed. No clean Ctrl+C claim
or all-acceptance-passed claim follows from the unit tests or process-group change.
Protocol/criteria were not weakened or rewritten.

`action-demo-interactive-003/` completed the same actual prompt walkthrough using
quit, then a separate explicit --resume invocation, inspect and Windows EOF. Both
exited0 with halted lifecycle acknowledgments; current conflict, historical closure
and budget persisted. `action-demo-interactive-evidence-001/results.json` records
the observed command sequences, snapshots, exit observation and checkpoint/transcript
hashes. Full submitted/received messages are in each session transcript; the console
interaction itself is recorded in the Codex tool transcript. Failed original sessions
remain untouched. A copy of failed002 in the evidence directory resumed and quit
successfully with identical scientific snapshot, establishing recovery of that copy,
not graceful interruption or a general forced-termination guarantee.

Use quit/EOF for the demonstrated safe exit. Ctrl+C handling in this host is the
remaining review limitation; do not silently promote this demo to a general shell.

## Reproduction and preservation

From the repository root, using fresh output paths each time:

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/action-demo-context-002.json
.\.venv\Scripts\python.exe -m pytest -q tests/test_action_demo.py --basetemp outputs/action-demo-targeted-002 --junitxml outputs/action-demo-targeted-002.xml
.\.venv\Scripts\python.exe experiments/run_action_demo.py --output outputs/action-demo-002 --preservation-context outputs/action-demo-context-002.json
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/action-demo-full-regression-001 --junitxml outputs/action-demo-full-regression-001.xml
.\.venv\Scripts\python.exe experiments/verify_preservation.py audit-historical --output outputs/action-demo-historical-audit-001.json
```

These are the recorded commands and already-used paths; choose NEW names to rerun.
Final evaluated context SHA256:
`42ec475248cd15078fdd183bb694df3758e00fe8b27f223f421838008a70bb8a` (194 files).
Both scripted runs001/002 passed116 checks and their source archives remain.
Original context001 SHA256:
`fda3ff210bbbe4e47cc170e62446aad2a2c0f92cdbfc74578269b19e7bdea564`.
The guide/results/handoff were written after regression; evaluated source is archived.

`action-demo-preservation-001.json` confirms all45,224 captured prior outputs and
3,043 historical files unchanged. Separate historical audit passed83 source entries,
134 protected entries (56 resolved from pinned Git), and137 original tree files.
No historical evidence, failed attempt or prior dirty work was discarded. No push,
publication, dependency installation or later task. Stop for coordinator review.
