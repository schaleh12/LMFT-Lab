# Preservation context correction — verification results

2026-10-12. [Separate verification contract v1](PRESERVATION_VERIFICATION_CONTRACT.md)
was frozen before evaluation. SHA256:
`98fd67289006ce2d65c9702a1022cd37706b2ffa7f5ae44eb6a2387d4b52274c`.
This is Priority 1 verification follow-up ONLY: no runtime/learner algorithm,
scientific protocol/case/criterion, seed, numerical mechanism, model setting,
migration behavior or acquisition change. Earlier passive work remains uncommitted
and was preserved before these additional narrow edits.

## Corrected separation

[Current context helper](../src/lmft_lab/preservation_context.py),
[historical audit/capture CLI](verify_preservation.py),
[historical anchor](INSUFFICIENCY_HISTORICAL_CONTEXT.json),
[focused tests](../tests/test_preservation_context.py).

Both end-to-end behavioral tests now EXPLICITLY capture a complete nonempty
current-source baseline and pass --preservation-context to their harness. The
existing [insufficiency harness](run_insufficiency.py) and
[passive harness](run_passive_relationship.py) retain their historical default
prework behavior and original 137/18 and 274/36 criteria. No preservation check
is skipped and no empty/absent context is used to claim current preservation.

Current context covers every non-bytecode source/spec/config/fixture/test/report
file in the contract's fixed inventory, plus the specified root files. Its root,
kind, exact path set, file hashes and inventory digest are strict. All context
files are archived, and the exact context-file hash is recorded in provenance.
Added/missing/changed source fails before/after evaluation. The current context is
copied into the run; deletion or byte changes reject rather than selecting legacy
behavior. The insufficiency restart identity includes the pinned context hash;
the passive harness checks its original pin before EVERY start/restart and at
completion. Genuine runtime checkpoint source/config guards remain unchanged.

This verifies current source was unchanged DURING the run. A context cannot be
reused after later source/test/document edits; capture a new one for a new run.
It does not assert that current source equals a historical baseline. That claim
belongs to the separate historical audit, never to behavioral regression.

## Historical audit — reproduced from historical bytes

`outputs/preservation-historical-audit-001.json` passed. Read-only audit checked:

- ALL **83** archived source/config/protocol entries and the complete **137-file** original tree.
- ALL **134** protected baseline entries: **78** from archived exact bytes; **56** from the pinned Git revision.
- Of those 56 versioned omissions, **4** used exact Git blob bytes; **52** reconstructed Windows LF-to-CRLF checkout bytes. EVERY resulting hash equals the original protected hash; expected hashes were not normalized or changed.
- Original config/provenance/protocol/manifests/result bytes, with recorded science totals **137/137 integrity, 18/18 quality**.

Pinned historical source commit:
`5e45ab365688c7b0b0ac246fd8e7db558e509704`.
Original protocol remains unchanged:
`1cb49361efc3d33249f75aaa01d40b0d06836aefd4bbd350f2ec710182852369`.
Historical context SHA256:
`fd4acfb71f0dd5749647f550be03c25db1945b5ebeda99c75a99ba10a8f72647`.
Original full-tree inventory digest:
`3b9793756d913c00c2c77c1aa23e83c71b09373886446f653635ad3c45551c84`.

The audit never uses current working bytes to substitute for historical evidence.
Missing/tampered archived bytes/manifests/context, wrong historical revision and
missing/changed Git evidence reject. A missing archived entry cannot be rescued
by Git fallback; versioned resolution is only for explicitly omitted protected
paths. The frozen context is a local inspectable trust anchor, not authentication,
a signature or proof of an external backup. Pinned local Git history is required.

## Current source behavioral results

Explicit current baseline `outputs/current-regression-context-001.json` covered
**154 files**. SHA256:
`141338bb6070dae6b885ad00a6cd93e63c33da78dea069fc433c4c6579aec4e2`.
This baseline belongs to these completed runs, captured before later test/report
additions; do not reuse it against later source.

- `outputs/insufficiency-current-regression-001/`: unchanged **137/137 integrity, 18/18 quality**.
- `outputs/passive-current-regression-001/`: unchanged **274/274 integrity, 36/36 quality**.
- Full CURRENT CHECKOUT pytest with both explicit contexts: **516 tests passed** under `outputs/preservation-full-regression-001/`, without a no-prework snapshot or skipped tests.
- Added two actual passive halt/restart context-tampering tests afterward; **32 focused tests pass** under `outputs/preservation-tests-003/`. The final full CURRENT CHECKOUT suite passed **518 tests** under `outputs/preservation-full-regression-002/` (39.04 seconds), with no skipped tests or alternate checkout.

Both current studies retain identical cases, hypotheses, evidence, budgets,
negative predictive outcomes and ordinary-memory comparisons. Only preservation
context/provenance and end-to-end test invocation changed. Original protocols
remain frozen; no scientific criterion required revision.

## Failures and original bytes preserved

The earlier **485-pass/1-failure** working-checkout result is still the recorded
historical outcome; its failure.json, 136/137 old run and all original archives
are untouched. Current contexts do not retroactively turn that audit green.
The old default still compares current code to that historical prework and can
fail on legitimate later edits. The new historical audit resolves original bytes
separately instead of weakening or deleting the old manifest.

Before follow-up, inventoried **3,043 files** across six prior archive/failure roots;
their inventories/hashes are stored in
`outputs/preservation-followup-prework-001/immutable-archives.json`. All those
original bytes and path sets remain unchanged. Prior dirty source/handoff copies
and hashes are in the same prework directory.

Initial focused audit tests: 30 passed. A subsequent addition of two passive
process tests first produced 30 passed/2 import-setup failures, retained in
`outputs/preservation-tests-002/`; explicitly adding the experiments import path
to the test harness fixed setup, with no change to verification/scientific criteria.
The two process tests now gracefully halt a real individual, remove/alter only its
ISOLATED test context, and confirm restart is refused before another process starts.
The tests never mutate original evidence. Original passive focused failures and
the 486-test clean-snapshot result remain historically reported without rewriting.

## Reproduce separately

PowerShell, repository root:

```powershell
$env:PYTHONPATH = 'src'
# Read-only historical byte audit; output outside original archive.
.\.venv\Scripts\python.exe experiments/verify_preservation.py audit-historical --run outputs/insufficiency-001 --git-root . --output outputs/my-historical-audit.json

# Fresh complete CURRENT source baseline (capture before each new run).
.\.venv\Scripts\python.exe experiments/verify_preservation.py capture-current --root . --output outputs/my-current-context.json
.\.venv\Scripts\python.exe experiments/run_insufficiency.py --output outputs/my-current-insufficiency --preservation-context outputs/my-current-context.json
.\.venv\Scripts\python.exe experiments/run_passive_relationship.py --output outputs/my-current-passive --preservation-context outputs/my-current-context.json

# Full behavioral suite in the real checkout; tests explicitly capture contexts.
.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/my-current-pytest-temp
```

Use fresh outputs/temp paths. Do not edit covered source during evaluation. Each
new current study contains archive/manifest, current-preservation-context.json,
nonempty protected-hashes.json, labelled provenance/results, all checkpoints,
traces and frozen predictions. Historical audit output includes per-file source
resolution/hash/revision rather than merely a success summary. Standalone default
historical behavior remains available without --preservation-context.

Final full-suite command/output is under `outputs/preservation-full-regression-002/`.
Completed command: `.\.venv\Scripts\python.exe -m pytest -q --basetemp outputs/preservation-full-regression-002`.
Stop after this correction for coordinator review. No Priority 2, active acquisition,
new scientific task, push, publication or archive deletion was performed.
