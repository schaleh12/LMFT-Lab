# Local synthetic terminal demonstration

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -m lmft_lab.action_demo --scenario r1
```

This creates and prints a unique session directory under `outputs`. Choose r1 or r8
for correction followed by a later conflicting report, or r2 for missing evidence
gathering. Add `--mode memory` for the equally equipped scalar baseline. There is
no language model, freeform chat, network service or new learning rule. Registered
synthetic reports can be wrong; typed claims never become verified evidence.

Try these commands, one per line:

```text
inspect
request
stop
resume
reply
late
inspect
stop
provenance
quit
```

For r1, the explicit synthetic reply permits a success prediction. The later report
restores conflict and abstention, while the historical request remains resolved.
r8 retains the known wrong post-correction prediction before later conflict. r2 has
no registered later report. Each session has one lifetime request, including across
restart; there is no reset or automatic second request.

`inspect` displays public current support, evidence IDs, prediction/abstention,
remaining budget and historical closure. `reply` fetches only the registered fixture
reply to the existing request; the runtime checks it independently. `late` submits
only the registered later report. `repeat` retransmits the last message with its
same ID to exercise deduplication. `help` lists commands. Full internal provenance
is available only after `stop`, with retained originals, current heads, sources and
verification metadata. The append-only `demo-transcript.jsonl` is an audit, not a
second truth store.

Explicit fresh paths must not exist, even as empty directories:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.action_demo --root outputs/my-new-demo --scenario r2
.\.venv\Scripts\python.exe -m lmft_lab.action_demo --resume outputs/my-new-demo
```

Resume uses the stored mode/scenario and refuses overrides. `--script commands.txt`
feeds the same command interface from a UTF-8 file. Unknown/oversized commands do
not submit evidence. The wrapper owns its child runtime and uses the existing
inbox/outbox/checkpoints; it does not edit scientific state directly.

Use `quit`, EOF (Windows Ctrl+Z), or Ctrl+C to exit the interactive Windows console.
These paths were verified in a real hosted terminal. Ctrl+C is read as an exit key:
the current command finishes, then the wrapper requests a normal stop and reaps its
child. Repeated keys do not force termination. Temporary console input flags are
restored after shutdown, and abandoned queued keys are discarded before returning
to the shell. No persistent OS setting changes. External signals, script-mode
interrupts, console closure and forced termination are outside this guarantee.
The [interrupt follow-up](../experiments/ACTION_INTERRUPT_RESULTS.md) records the
fix, real PTY evidence and preserved earlier failures.

Older checkpoints require their archived source/configuration because the existing
source manifest includes the new wrapper module. There is no silent migration.
See [protocol](../experiments/ACTION_DEMO_PROTOCOL.md) and
[initial results and evidence](../experiments/ACTION_DEMO_RESULTS.md).
