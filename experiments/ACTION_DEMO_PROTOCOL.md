# Thin supervised terminal demonstration - protocol v1

Frozen 2026-10-12 before evaluation. Preserve existing dirty work, previous reports,
source and output hashes in outputs/action-demo-prework-001. No new learner/rule.

One standard-library terminal wrapper launches the existing fixture-only runtime as
an owned child, using Store.submit/receive/stop and halt-only Store.inspect. It never
writes checkpoint/scientific state, invents evidence, or interprets freeform claims.
Fresh CLI selects only r1/r8/r2 and lmft/memory. A fresh default root is uniquely named
under outputs; any existing explicitly supplied fresh root rejects, even if empty.
Resume explicitly names a halted compatible initialized session and uses its stored
mode/scenario; reject overrides, foreign modes, running sessions and missing data.
No listener, daemon, installation, external connection or automatic startup.

Banner clearly identifies authored synthetic fixtures, not verified real-world truth
or freeform chat. Commands: help, inspect, request, reply, late, repeat, stop, resume,
provenance, quit. reply explicitly obtains the selected registered synthetic service
payload; late explicitly submits the registered c1/c9 report (unavailable for r2).
No typed payloads, automatic verification of claims, automatic second request or
budget reset. Unknown/oversized commands have helpful bounded errors and no submission.
repeat redelivers the last scientific message with its exact ID; barrier acknowledgment
permits completion even when dedup produces no new outbox message. Request correlation
is recovered from public outbox on resume, not a separate belief store.

Fresh initialization is explicit in CLI scenario choice and recorded through inbox.
Resume never initializes again. inspect sends the existing fixed command while live;
display current support, evidence references, prediction/abstention reason, remaining
budget and historical closure separately. Stop retains all files. Internal provenance
is shown only after halt, with original/head IDs, sources and verification metadata;
requesting provenance while live instructs the user to stop first. Quit, EOF and
KeyboardInterrupt request stop at a commit boundary and wait for the owned child.
No deletion, reset, forced checkpoint overwrite or hidden background process.

An append-only terminal transcript records submitted envelopes and received outbox
messages, plus lifecycle/UI errors; it is an audit, not a truth store or recovery
authority. Resume message IDs avoid existing inbox identities, including queued
unprocessed envelopes. Script mode reads the same commands as interactive stdin.

Acceptance: scripted actual-child runs for all three scenarios and both modes;
repeat/unknown/oversized input; request exhaustion; stop/resume pending and after late
evidence; EOF/interrupt cleanup; root collisions, repeated fresh invocation, explicit
resume and wrong mode. Compare submitted transcript envelopes replayed through a
direct actual runtime with identical IDs, and compare scientific action/state traces
to matched memory. Ignore only outbox timestamps and receipt processing durations.
Read-only inspect does not change judgment/budget; current/historical displays must
remain distinct when later conflict restores abstention. Known c9 error remains.
Also conduct an actual interactive PTY exercise, recording its commands and output.

Freeze source/config/protocol before scripted evaluation; unique output/temp/XML
paths every invocation; targeted and appropriate full current-checkout regression,
source/archive preservation. Retain failed runs and version changed scientific
criteria before reevaluation. Zero model calls/dependencies/protected changes.
Document exact launch and sample walkthrough; update handoff and stop for review.
