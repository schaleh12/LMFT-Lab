# Experiments

This area holds LMFT experimental protocols and reproducibility records.
[Experiment 001](EXPERIMENT_001_PERSISTENT_REVISION.md) is a draft persistent-revision
protocol; its broader developmental study has not been executed. A narrow
[interactive fixture protocol](INTERACTIVE_REVISION_PROTOCOL.md) now has
[mechanical and actual-model results](INTERACTIVE_REVISION_RESULTS.md).
Numerical unit tests are not a completed
developmental experiment. Genetic search is optional future research only.

Each future experiment should preserve enough information to reproduce and
interpret its results:

- The research question or hypothesis and complete configuration.
- Random seeds and the random generators to which they apply.
- Acceptance criteria, evidence/update rules, parameters, and evaluation procedures.
- Model/prompt/schema versions or explicit mocked/absent LLM status.
- Evidence provenance, accepted/rejected revisions, traces, and restart/replay results.
- Software information: code revision, relevant local changes, Python and
  dependency versions, and relevant platform or numerical-library details.
- Relevant inputs, results, and the commands or procedure used to obtain them.
- Ancestry and lineage information when evolutionary functionality is introduced.

Evaluation definitions are part of the research design. Fitness definitions and
lineage remain required if genetic research is later explicitly introduced. Do not change them merely
to make an experiment succeed. Never modify or delete historical results to
obtain cleaner results; preserve the original record when documenting corrections
or subsequent runs.

The repository currently ignores directories named `outputs/` and `logs/`.
Ignored files are not a durable experimental record: preserve results needed for
reproducibility in tracked files or a documented durable archive. The supervised runner uses a versioned JSON checkpoint for short experiments;
no archival service is selected.


The immediate target is a small traceable change of mind that survives restart
and retains its reasons and behavioral consequence. Later comparisons should
include learning-disabled and propagation-disabled controls and an LLM with
ordinary structured memory under matched evidence/model/resource conditions.
Distinguish better explanation from stronger evidence; record unsuccessful
revisions and constitutional/prompt-injection test failures as well as successes.


[Local-model smoke run](LOCAL_MODEL_SMOKE.md) records actual CUDA and offline
proposal-path execution, separate from mocked tests and from the unexecuted
persistent-revision experiment.

[Comparative procedure reliability](COMPARATIVE_RELIABILITY_PROTOCOL.md) is the
second grounded fixture, with [results](COMPARATIVE_RELIABILITY_RESULTS.md) and
[commands](../docs/COMPARATIVE_RELIABILITY.md). It compares the current counter with
and without propagation and an independent structured-memory recount. Original
interactive results remain historical records.

The [contextual protocol](CONTEXTUAL_PROTOCOL.md) and [results](CONTEXTUAL_RESULTS.md)
test conditional judgments, linked clarification and reduced retransmission overhead
against conditional and aggregate memory.
