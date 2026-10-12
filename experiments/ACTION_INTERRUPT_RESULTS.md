# Hosted terminal Ctrl+C follow-up - results

2026-10-12. The interactive Windows console now treats Ctrl+C as an exit key and
finishes the current wrapper command before orderly runtime shutdown. Actual hosted
PTY trials passed for a pending request, a reply observably in progress, repeated
keys and post-correction/later-conflict state. Halt acknowledgments, persisted halted
lifecycle, released locks, reaped children and original console modes were verified.
The previous failures remain preserved; this result supersedes their unresolved
keyboard-exit limitation, not their historical observations.

## Diagnosis and focused change

A minimal signal probe without LMFT caught SIGINT, recorded cleanup step0, then
terminated before step1 (100ms later), with exit -1073741510. This reproduces a host
console-signal limitation outside the runtime. It does not isolate which hosting
component terminated the process. A second probe temporarily disabled processed
console input, read the same real Ctrl+C as character3, completed a one-second cleanup
and restored its original mode with exit0. Evidence:
`outputs/action-interrupt-signal-probe-001/`, `action-interrupt-raw-probe-001/`;
probe source remains in `action-interrupt-prework-001/`.

Windows documents that ENABLE_PROCESSED_INPUT determines whether Ctrl+C is dispatched
as a control signal or retained in the input buffer. See
[Microsoft console modes](https://learn.microsoft.com/en-us/windows/console/setconsolemode).
Python's ordinary SIGINT handler raises KeyboardInterrupt; catching that exception
alone did not prevent this host's later termination. See
[Python signal handling](https://docs.python.org/3/library/signal.html).

[action_console.py](../src/lmft_lab/action_console.py) adds a small standard-library
reader only for interactive Windows console input. It saves the current console
input flags, disables processed Ctrl+C/cooked-line/automatic echo while the demo owns
the terminal, reads bounded command characters, and restores and verifies the exact
original flags after shutdown. Abandoned queued keystrokes are flushed before return
to the shell. No persistent OS/security setting, host process, registry, dependency,
runtime transaction, seed, equation, model or learning mechanism was changed.

[action_demo.py](../src/lmft_lab/action_demo.py) uses that reader and records the
waited child's PID/reaped status. An interrupt key arriving during a command remains
queued until the next input boundary. The wrapper then requests the existing normal
stop and waits for the owned child. Additional keys do not escalate shutdown into
termination. Script/non-console input retains its previous path. No new commands.

The original demo scientific acceptance criteria are unchanged. The focused
[interrupt protocol](ACTION_INTERRUPT_PROTOCOL.md) was frozen after diagnosis and
before implementation evaluation. Exact source/protocol hashes are retained in
`outputs/action-interrupt-smoke-001/provenance.json`; source context002 contains200
files, SHA256 `c53f41f0c589215616c5713fb5ea85e1a064041b60245b1e4e32fd54bd3b72ff`.
Starting HEAD remains `90c1b84a4092f5f82a76debbf2e637d7da092fe9`.

## Actual hosted PTY evidence

| Trial | Real terminal action | Observed outcome |
| --- | --- | --- |
| pending-001, first invocation | request, then three Ctrl+C keys | exit0; pending request retained; halted/reaped; mode restored |
| during-001 | two Ctrl+C keys after real reply submission, before barrier | reply completed after gate release; exit0, halted/reaped; mode restored |
| pending-001, second invocation | explicit resume, inspect pending, reply, late, inspect, Ctrl+C | budget0, conflict/abstention and historical closure retained; exit0 |
| pending-001, third invocation | explicit resume, stop, resume, inspect, Ctrl+Z EOF | same scientific state; exit0; halted/reaped; mode restored |
| quit-001 | memory r2, invalid command, request, reply, quit | invalid input rejected; one gather; exit0; halted/reaped; mode restored |

All roots above are under `outputs/action-interrupt-*`. The in-progress trial uses
[a test-only gate](action_interrupt_probe.py) after Store.submit actually writes the
reply and before the wrapper submits its barrier. The gate announces readiness;
two real PTY Ctrl+C bytes were then sent, followed by a separate release-file action.
No KeyboardInterrupt was injected and no runtime algorithm was mocked. This proves
the key can arrive while the wrapper command is in progress. It does not claim an
interrupt occurred inside the runtime's atomic checkpoint replace.

`action-interrupt-pty-observations-001.json` records tool session IDs, inputs and exit
observations. Session transcripts retain all public inputs/outputs, input endings,
halt receipts and console mode entries/restorations. `action-interrupt-pty-evidence-001.json`
records checkpoint/transcript hashes, valid post-halt snapshots, reaped direct child
PIDs and native Windows process checks: recorded child/runtime PIDs were not running.
Each session retained one request; inspect/resume did not reset its identity or budget.

The three complete real-PTY message histories were also replayed through separate
actual runtimes with identical IDs. All three complete semantic states matched,
excluding only existing outbox timestamps and receipt processing durations.
See `action-interrupt-pty-replay-001/results.json` and the preserved replay driver.
This adds three direct-reference requests to the three interactive individuals;
these counts are not a physical-work bound.

## Regression, smoke and preservation

**20 targeted tests passed in15.67s; 758 full checkout tests passed in171.08s**,
with no failures/errors/skips. The11 new reader tests supplement actual PTY evidence;
they are not the basis for claiming console shutdown works. The original six-case
scripted smoke passed **116/116 checks**, including direct-runtime and circuit/memory
parity, invalid input, dedup, fresh-path protection and explicit resume. Zero model calls.

Recorded commands (paths already exist; choose fresh names for reproduction):

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --output outputs/action-interrupt-context-002.json
.\.venv\Scripts\python.exe -m pytest -q tests/test_action_demo.py tests/test_action_console.py --basetemp outputs/action-interrupt-targeted-001 --junitxml outputs/action-interrupt-targeted-001.xml
.\.venv\Scripts\python.exe experiments/run_action_demo.py --output outputs/action-interrupt-smoke-001 --preservation-context outputs/action-interrupt-context-002.json
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/action-interrupt-full-regression-001 --junitxml outputs/action-interrupt-full-regression-001.xml
```

Interactive launch remains `python -m lmft_lab.action_demo --scenario r1` with this
checkout's Python and PYTHONPATH. For the gated test, run
`experiments/action_interrupt_probe.py --root <fresh-session> --gate <fresh-gate>`,
enter request/reply, wait for its announcement, send Ctrl+C, then create the gate's
`release` file within45s. It is test instrumentation, not a user-facing feature.

The196-file prework archive preserved all prior dirty source. Before final handoff,
the only changed preexisting source was action_demo.py. All7,572 captured demo files,
45,224 older captured outputs and3,043 historical files matched their hashes.
Historical audit passed83 source/134 protected/137 tree files, including56 protected
entries resolved from pinned Git. Original failed PTY sessions remain unchanged.
The evaluated200-file source archive and final handoff context are separate; final
report/guide/handoff edits were made after regression. Nothing was pushed or discarded.

## Scope of the result

This verifies interactive Ctrl+C keystrokes in the tested hosted Windows PTY. It does
not establish safe external SIGINT/CTRL_BREAK delivery, script-mode signal handling,
console closure, forced termination or other operating systems. Interrupt latency
includes the current bounded command; keys do not cancel a partially submitted
operation. Original source-manifest compatibility limits remain. No claim of general
signal safety, exactly-once physical work, or a new cognitive capability. Stop for review.
