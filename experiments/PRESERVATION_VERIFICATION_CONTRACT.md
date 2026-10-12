# Current regression and historical preservation — verification contract v1

Frozen 2026-10-12 BEFORE evaluating this correction. This changes verification
context selection only, not the insufficiency/passive scientific protocols,
cases, evidence assumptions, candidate family, acceptance criteria or findings.
Preserve all original archives and the recorded 485-pass/1-failure outcome.
No active acquisition, new scientific study, model call or runtime behavior change.

## Explicit current behavioral regression

Keep the insufficiency harness's historical DEFAULT preservation behavior. Add
an explicit --preservation-context option for current regression. The pytest
end-to-end behavioral test must explicitly create/use that current context.
Never remove/rename/hide old prework, substitute an empty baseline, skip the
protected-files-preserved check, or change the existing 137 integrity/18 quality
expectations. Default runs still use their historical prework, even if it fails
against legitimate later code changes.

A current context is captured BEFORE the run and must be nonempty, strict-schema,
root-bound and complete for the defined source inventory: all non-bytecode files
under src/tests/config/experiments/docs and root .py/.md/.txt/.json/.toml/.cfg/.ini
files plus .gitignore. Exclude __pycache__, .pyc/.pyo and ignored output directories,
not source files. Exact canonical relative paths and SHA256 values are required.
Verify the inventory and every byte hash before use and after the run; added,
missing or altered source must fail. Copy the context into the new run and bind
it to study identity; changing it cannot silently change a restarted checkpoint.
Archive every context-covered file, not just the previous narrow source set.
Capture and verify the context-file hash as well. Record its kind/root/scope/count
and hash in new provenance/results, distinct from historical preservation.

The current baseline asserts unchanged CURRENT source during the behavioral run.
It does not assert historical source preservation or turn the old failure green.
The current code may legitimately differ from a past baseline; that is separately
audited against historical bytes. Full current-checkout pytest must pass without
using a no-prework source snapshot or skipping any test.

## Separate fail-closed historical audit

Freeze a distinct checked-in historical context for outputs/insufficiency-001,
with original source commit 5e45ab365688c7b0b0ac246fd8e7db558e509704, protocol
hash 1cb49361efc3d33249f75aaa01d40b0d06836aefd4bbd350f2ec710182852369,
all archived-tree file hashes and pinned metadata hashes. This context is an
inspectable local trust anchor, not external authentication or an external backup.
Its creation reads existing evidence only; never rewrite the original archive.

Audit original archive metadata/source/config/protocol against the frozen context.
Normalize Windows/POSIX separators for identity only; reject path escape, duplicate
canonical identities and malformed hashes. Every archive-manifest entry must have
its actual historical file and exact hash; no fallback may hide a missing/tampered
archived file. The full original tree must match its frozen inventory/hash as well.

Audit ALL 134 protected baseline entries, not only the 78 also present in the
83-file source archive. Resolve overlapping entries from archived historical bytes;
resolve the 56 omissions from Git blobs at the EXACT pinned historical commit.
Record the chosen source/revision and resulting hash for each. Historical Windows
checkout line endings may be reconstructed from pinned Git blob bytes using ONLY
the two predefined exact renderings: unchanged blob, or LF-to-CRLF checkout form.
The resulting byte hash MUST equal the ORIGINAL protected hash; never normalize
the expected hash, use current working files, accept arbitrary transformations,
or silently select another revision. This is byte reconstruction, not relaxed
comparison. Missing Git evidence, wrong revision, altered manifests/source/config,
missing historical bytes or an empty/incomplete context must reject.

Current runtime.py may differ while this historical audit passes, because the
audit resolves original historical bytes explicitly. Conversely, current behavioral
regression cannot claim historical preservation. Audit is read-only; derivative
results must be outside the original archive. Preserve the complete original
archive bytes and prior failed run, verified against pre-follow-up inventories.

## Required tests and outcome reporting

Focused tests must prove: current complete/nonempty baseline succeeds, catches
altered/missing/added source and changed context; wrong root/schema fails; historical
audit succeeds with archived/versioned original bytes despite changed current code;
tampered/missing archived files/manifests and wrong historical revision fail;
missing/changed versioned bytes fail; every omitted protected entry is resolved.
Use isolated test copies, never tamper with original artifacts.

Run separate historical audit and full current-checkout behavioral pytest. Retain
exact source/context/protocol hashes, nonempty counts, results/failures and command
outputs. Distinguish unchanged 137/18 science, verification-context checks, full-suite
totals and original failed evidence. Add a separate follow-up report/contract and
handoff updates; append a clearly dated correction note to passive results rather
than rewriting prior outcomes. Stop for parent review; no Priority 2 or dispatch.
