# Terminal interrupt follow-up - protocol v1

Frozen 2026-10-12 before implementation evaluation. Scope is the existing demo's
console interrupt path only. ACTION_DEMO_PROTOCOL.md scientific checks are unchanged.
Preserve prior source and all demo artifacts, including failed PTY trials, under
action-interrupt-prework-001. Diagnostic probes are not acceptance evidence.

The hosted PowerShell signal probe catches SIGINT but is terminated during cleanup.
A raw-input probe receives Ctrl+C as character3 and completes cleanup/restoration.
Implement a temporary Windows console input reader while the demo owns the terminal;
restore its original mode after child shutdown. No persistent OS/security settings,
host termination, new learner, new command, dependency or runtime transaction change.
Ctrl+C requests exit at the wrapper's next command boundary. An in-flight command
can finish before the key is consumed; it never interrupts checkpoint replacement.
Repeated keys during shutdown cannot escalate into forced child termination. Do not
promise protection against process kills, console closure or external signal injection.
Non-console/script input retains the existing input path. Quit/EOF/stop/resume remain.

Acceptance: actual hosted PTY Ctrl+C with a pending request, after correction/later
evidence, repeated Ctrl+C, and during a command where observable. Require return0,
runtime halted acknowledgment in transcript, persisted halted lifecycle, released
runtime lock, valid checkpoint and a waited/reaped owned child. Resume must preserve
one-request budget, request identity, evidence and scientific state. Verify original
console mode restoration. Distinguish commands buffered before a Ctrl+C from commands
proven in flight; do not claim timing coverage merely from sending them together.
Test reader invalid/oversized input, backspace, CR/LF, Ctrl+Z EOF and Ctrl+C; retain
existing wrapper/direct-runtime/memory parity and actual quit/EOF smoke. Run targeted
and full regression with unique paths and source/context archives. Preserve every
failed attempt. If a host limitation remains, report acceptance incomplete. Stop for
review; no subsequent task.
