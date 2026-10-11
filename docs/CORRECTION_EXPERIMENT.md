# Correction without erasing evidence

This bounded study adds a versioned correction ledger around the unchanged consistent-support
mapping. Read the [protocol](../experiments/CORRECTION_PROTOCOL.md) and
[results](../experiments/CORRECTION_RESULTS.md) for exact scope, comparisons and limits.

## Reproduce

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe experiments/run_correction.py --output outputs/my-correction-run
```

Use a fresh directory. The harness retains failed runs and snapshots protocol, source,
tests, config, original messages, full lineage and traces before evaluation. It runs actual
processes with halt/restart and uninterrupted controls. No downloads, models, credentials,
new dependencies or background cognition are required. Raw outputs remain ignored by Git.

Modes: `correction-lmft`, `correction-disabled`, `correction-memory`, with `--mode fixture`.
Use the normal [supervised lifecycle commands](INTERACTIVE_RUNTIME.md). The inherited
--learning-disabled flag also disables correction acceptance. Fixed prior outcome judgments
and route weights remain available in all modes. While running, use only deliberate outbox
messages/lifecycle acknowledgments; inspect full lineage and diagnostics after halt.

## Separate authority, eligibility and truth checks

`config/correction_authority.json` is trusted deployment input, included in the restart
manifest and frozen into new individuals. It permits exact correction payload hashes under
a named authority. Both the sender name and entire payload must match; a message's assertion
of authority cannot change the policy. Changing policy requires explicitly new experimental
state; the existing source/config compatibility check prevents silent restart changes.

This is a synthetic public operation allowlist, not human authentication. Exact permitted
messages are replayable bearer capabilities, and a hostile host can edit files. No secret or
production authentication is claimed. Some deliberately invalid replacements are authorized
in the fixture, demonstrating that permission is distinct from eligibility and verification.

The validator first checks authority, then an active target with exact digest and matching
case/scope/question/part. Only then can it consult the registered reference for the submitted
replacement coordinate. Replacement schema/types and content must match that independent
reference. A malformed, unverifiable, wrong-scope, nonexistent or stale target is rejected.
The original logged report is never rewritten. Earlier truth-based fixture verifiers remain
unchanged: this separately versioned initial admission certifies an instrument LOG entry,
which can be erroneous, rather than certifying objective truth.

## Lineage and effective evidence

Operations use the existing version-1 envelope and exact text/operation/record content:
`outcome`, `evidence`, `evaluate`, `correction`, `barrier`. The harness provides exact payloads.
A correction specifies correction_id, authority, target_id, expected_digest, reason and a
replacement observation. Each attempt records provenance, separate stage results, acceptance
reason and before/after effective head maps, digest and independent count.

Immutable ledger records include originals and replacements. A root has one active head;
a verified replacement inherits its root and points to its parent. The derived effective
view supplies only heads to the unchanged selector/predictor. Replacing an observation does
not add an independent root. Chains must explicitly target the current head and its digest.
Competing old-target corrections cannot overwrite later accepted state. No last-write-wins.

First use of a correction ID is terminal, including rejection. Same payload redelivery adds
only a receipt; conflicting reuse appends a rejected attempt without replacing the original
result. A corrected rejected proposal needs a new correction ID and an appropriate permit.
This simple public-ID policy is not denial-of-service resistant; it is a fixture convention.
Source attribution on every original and correction remains inspectable after halt.

Only scoped observations are correctable here. Prior outcome samples are not eligible targets;
the existing sum(signs)/(n+2) equation still operates on the unchanged eight eligible outcome
roots. Condition repair can select a different existing conditional judgment, without adding
outcome samples or changing the numerical rule. Correcting outcome evidence is future work.

## Caches, questions and persistence

Evaluation caches hold semantic results/selection keyed by public case, relevant effective
records, fixed routes/mode and prior judgments. Relevant accepted corrections invalidate the
affected cache; rejection/irrelevant correction preserves it. Fresh outgoing wording comes
from the current result, never stale saved prose. Traces distinguish cache invalidation,
effective-evidence changes and numerical selection.

Pending requests close only if their question becomes sufficient, retaining the closing
correction reference. Closed requests and spent budgets remain in history. Reopening does
not allocate a second request after the one-request lifetime budget is spent. The study's
additional verification requests have no new measurement available and remain pending unless
a correction settles the question; no fabricated response is supplied.

One existing atomic checkpoint commits lineage, heads, correction index, cache invalidation,
question updates and output together. Tests exercise failure before and after replacement.
No prior record, seed node or historical result is deleted. Existing checkpoints still need
their archived code/config; no new automatic migration or production durability claim exists.
