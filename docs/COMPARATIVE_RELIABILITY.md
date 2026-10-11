# Comparative procedure-reliability experiment

This second fixture compares the existing persistent evidence counter with and without
activation propagation and with a simpler structured-memory implementation. It does
not add activation-to-learning coupling. See the frozen
[protocol](../experiments/COMPARATIVE_RELIABILITY_PROTOCOL.md) and
[results](../experiments/COMPARATIVE_RELIABILITY_RESULTS.md).
The [original interactive study](../experiments/INTERACTIVE_REVISION_RESULTS.md) is unchanged.

## What changed

`reliability.py` defines a registered adjacent compare/swap procedure, six synthetic
trial records, executable outcome validation, held-out probes, authored associations
and a transparent independent memory recount. The shared revision helper retains
sum(signs)/(n+2) and the original thresholds exactly. Only verified distinct trials
count. Teacher claims, invented outputs, held-out inputs relabeled as training, and
repeated sample IDs are rejected. The original channel fixture remains the default.

The new judgment estimates aggregate procedure reliability over three integers in
[0,9]; it cannot identify which individual input will fail. It references existing
Fact, Execution and Confidence nodes through authored diagnostic associations. It
does not modify their identities, meanings, genealogy or numerical update equations.
Seed Confidence activation is not learned evidential confidence. No confidence field
or automatic truth authority has been added.

Three `--experiment` settings select the comparison:

| Setting | Processing | Revision |
| --- | --- | --- |
| `reliability` | Authored edges, existing two-pass propagation | Existing bounded evidence counter |
| `reliability-no-propagation` | Same edges/memberships, zero passes | Same counter |
| `reliability-memory` | No activation or model calls | Independent success/failure recount with same equation |

All use the same validated messages, evidence eligibility and file-backed runtime.
The memory condition retains unused birth metadata and the same audit infrastructure;
its costs are not those of an optimized minimal memory store. Deterministic A/B role
proposals are mocks with identical outputs; their contexts differ in activation. C
makes no mock calls. All actual SLM budgets in the deterministic comparison are zero.
The separate real SLM run is a communication smoke, not a model-assisted comparison.

The runner adds internal per-cycle compute timing, excluding checkpoint serialization
and commit. Windows checkpoint reads/replacements now retry transient PermissionError
at 25 ms intervals for at most 0.5 seconds; other errors remain errors. This small
storage fix arose from the preserved first comparative run. The atomic replacement
commit point and previous durability limitations remain unchanged.

## Reproduce on Windows

From the repository root, with the existing environment and cached model for the
optional offline smoke:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_comparative.py --output outputs/my-comparison
.\.venv\Scripts\python.exe experiments/run_comparative.py --local --output outputs/my-comparison-local
```

Use fresh output directories. The harness archives exact source files, tests, model
configuration and protocol before execution. Completed and failed runs are retained.
Raw messages, checkpoints and model traces remain under ignored outputs. The tracked
results report preserves selected measurements; archive local results separately.

The deterministic harness runs all three conditions, a learning-disabled control,
and an uninterrupted comparison. It halts before inspecting internal state, verifies
an actual restart, and uses outbox completion markers for repetition batches. It
records scope probes, timings, calls, counts and storage growth. No idle cognitive
loop, broad consolidation or automatic Codex bridge is implemented.

## Manual supervised exchange

The existing [interactive commands](INTERACTIVE_RUNTIME.md) also support the new
fixture. In one terminal:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson start --new procedure-lesson --mode fixture --experiment reliability
```

In a second terminal:

```powershell
$env:PYTHONPATH = 'src'
@{
  schema_version = 1; id = 'question'; sender = 'codex'; source = 'registered-procedure-trials'
  type = 'observation'; content = @{ text = 'Does one adjacent pass reliably sort three integers?' }
} | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 outputs/procedure-question.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson submit --file outputs/procedure-question.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson receive
```

After reading the clarification, use its actual ID (normally `out-2` for this new
individual) in the reply:

```powershell
@{
  schema_version = 1; id = 'trial-1'; sender = 'codex'; source = 'registered-procedure-trials'
  type = 'teacher_reply'; reply_to = 'out-2'
  content = @{
    text = 'Registered trial t1 ran one adjacent pass on [1,3,2] and returned [1,2,3].'
    evidence = @{ sample_id = 't1'; procedure = 'adjacent-pass-1'; input = @(1,3,2); output = @(1,2,3) }
  }
} | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 outputs/procedure-reply.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson submit --file outputs/procedure-reply.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson receive --after 2
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson stop
```

Wait for `halted` in the first terminal before diagnostics:

```powershell
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson probe
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson inspect > outputs/procedure-diagnostics.json
.\.venv\Scripts\python.exe -m lmft_lab.runtime --root outputs/procedure-lesson start --mode fixture --experiment reliability
```

Restart must specify the same condition, mode and learning-control flag. Use
`--learning-disabled` at both creation and restart for that control. To use the real
cached model, select `--mode local --offline` instead of fixture at creation/restart.

The live teacher-facing boundary remains deliberate outbox messages and lifecycle
acknowledgments only. Full state and probe access remain gated until halt. Response
wording is authored from the accepted judgment, evidence counts and uncertainty;
SLM-generated text is retained internally as proposals. This is an interface boundary,
not protection against a host filesystem owner.

## Compatibility and limits

No previous checkpoints or historical results are rewritten. Source hashes changed,
so previous experimental individuals still require their original archived code to
restart; no automatic migration is performed. The historical seed migration module
is unchanged. New comparative states explicitly identify their experimental condition.

Successes and failures are grounded in executing an authored software fixture, not
independently observed real-world events. The shared evidence validator is a common
assumption across conditions. The experiment does not establish factual grounding in
general, calibrated confidence, learned conceptual associations or useful geometry.
The score ignores propagated activation. The model path can reject malformed model
responses before revision, but no such failure is manufactured as a propagation benefit.
