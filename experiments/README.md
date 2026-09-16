# Experiments

This area will hold controlled evolutionary experiments and their configurations.
No experiment is defined or run by this scaffold.

Each future experiment should preserve enough information to reproduce and
interpret its results:

- The research question or hypothesis and complete configuration.
- Random seeds and the random generators to which they apply.
- Fitness definitions, including parameters and evaluation procedures.
- Software information: code revision, relevant local changes, Python and
  dependency versions, and relevant platform or numerical-library details.
- Relevant inputs, results, and the commands or procedure used to obtain them.
- Ancestry and lineage information when evolutionary functionality is introduced.

Fitness definitions are part of the research design. Do not change them merely
to make an experiment succeed. Never modify or delete historical results to
obtain cleaner results; preserve the original record when documenting corrections
or subsequent runs.

The repository currently ignores directories named `outputs/` and `logs/`.
Ignored files are not a durable experimental record: preserve results needed for
reproducibility in tracked files or a documented durable archive. No storage
format, experiment framework, or archival service is selected here.
