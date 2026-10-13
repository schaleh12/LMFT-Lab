# Retired local synthetic terminal demonstration

Retired on 2026-10-12 at the owner's request. The fixed-command terminal wrapper,
its console reader, two dedicated test files (20 collected cases), scripted demo
harness and interrupt probe are no longer active supported entrypoints.
The shared [action runtime](ACTION_COMMAND_RUNTIME.md), capacity/binding learning,
and shared regression infrastructure remain available and unchanged.

Historical [demo protocol](../experiments/ACTION_DEMO_PROTOCOL.md),
[results and failures](../experiments/ACTION_DEMO_RESULTS.md), and
[interrupt follow-up](../experiments/ACTION_INTERRUPT_RESULTS.md) remain evidence
of the implementation at that time. Their source links and reproduction commands
refer to archived versions, not current launch instructions.

## Recovery and checkpoint compatibility

The exact pre-cleanup checkout (225 files, including source, configuration, tests
and original guide) is saved at `outputs/terminal-demo-retirement-20261012-001/source/`.
`source-hashes.json` records SHA-256 hashes of the original working bytes.
Git HEAD `583071f857a9912c83ac06429dca0fe9d67e8aa1` also retains the retired files;
the archive is preferred for exact checkout bytes and line endings.

The original owner session `outputs/action-demo-20261012T150026-75a8489b` remains
untouched. Its matching old executable/config snapshot remains
`outputs/binding-runtime-prework-001/source/`; later binding fixes remain archived
in `outputs/session-closeout-20261012-001/source/`. The new pre-cleanup archive is
not a substitute for an older checkpoint's matching software manifest.

Removing modules changes the source-wide runtime manifest. Existing checkpoints
must use their exact matching source/config in an isolated recovery checkout, with
a COPY of the checkpoint/session. Do not overlay retired files on current source,
relax the manifest, silently migrate, or reopen the original owner session.
All archives under `outputs/` are local and Git-ignored; no external backup was
verified. No historical results, failures or output files were pruned.
