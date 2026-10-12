# Unsupported hypothesis family — preregistration v1

Frozen 2026-10-12 before evaluation. Zero model/mock calls, seed 42, no teacher,
new hypotheses, repair, acquisition or runtime integration. Preserve all previous
uncommitted work and historical findings. Isolated file-backed study.

## Evidence assumptions and task

New procedure `capacity-blocked-two-1`: an empty noiseless bounded-write buffer
as in the previous task, with a deterministic device fault that refuses ALL
payloads of length 2. Other lengths use the existing bounded-write simulation.
This is a NEW synthetic fixture, not a revision of capacity-transmit-1's truth.
Strict integer length/capacity 0..8 and a procedure identifier are observable;
no fault feature is added to the learner's vocabulary. The registered simulator
is authoritative ONLY within this synthetic study. Exact verified labels can
eliminate deterministic candidates under these noiseless assumptions. Real-world
contradictions need not invalidate a theory. An empty set cannot diagnose inadequate
vocabulary versus missing context versus erroneous evidence.

The six PREEXISTING comparison representations remain lt,le,eq,ge,gt,ne in that
order. Their numerical operator dispatch is reused under the explicitly new task
scope; original capacity scope and predictor remain unchanged. No code generation.

## Registered splits and controls

Each scenario has t1..t4, with pair values below and independently simulated labels:

- unsupported: (1,3), (4,2), (2,4), (3,3), labels true,false,false,true.
- supported: (1,3), (4,2), (3,3), (5,1), labels true,false,true,false.
- ambiguous: (1,3), (4,2), (3,5), (5,1), labels true,false,true,false.

Complete training is required. Retain EVERY zero-error hypothesis. Expected sets:
unsupported=[], supported=[le], ambiguous=[lt,le]. Store each candidate's full
training error refs and predictions; unsupported is explicit `no_supported_hypothesis`,
distinct from `ambiguous`, `supported` and `untrained`. No tie breaking/fallback.

Fresh validation v1..v4: (0,3),(3,6),(6,1),(7,4), labels true,true,false,false.
Validation checks every retained candidate, never filters/resurrects candidates.
Acceptance requires a NONEMPTY set and every validation check matching; empty
remains rejected for `no_supported_hypothesis`, never passes vacuously.
Validation mismatch rejects the whole nonempty set without fallback.

Held-out equality h1..h4: (1,1),(2,2),(4,4),(6,6).
Held-out non-equality h5..h8: (2,5),(1,4),(6,3),(8,7).
x1=(9,8) tests scope, excluded from quality denominators. All held/validation pairs
are absent from every scenario's training; validation and evaluation are disjoint.
Case IDs/scenario metadata are provenance, never predictive features.

## Admission, prediction and persistence

Only exact registered outcome schema, source, scenario, phase, features and
Boolean label verified by the simulator enter evidence. Rejected malformed,
wrong-source, wrong-feature, unregistered, false-label, external proposal and
held-out inputs remain traced but do not count as training contradictions.
Exact evidence duplicates count once; conflicting identities reject and preserve
the original. Selection reads only admitted training, not the verifier/validation.

Empty set: abstain with `no_supported_hypothesis`, no votes. Multiple hypotheses:
consensus only when all accepted hypotheses agree; otherwise `hypothesis_disagreement`.
One validated hypothesis: its prediction. Untrained/unvalidated/validation-rejected
states abstain with distinct reasons. There is no calibrated confidence claim.

LMFT and ordinary memory receive identical evidence, candidate space, selection,
validation, invalid attempts and policies; only LMFT persists the unchanged 40-node
scaffold. Neither uses seed activation or propagation. Six conditions total.
For each, checkpoint immediately after selection and after validation; load BOTH
in distinct Python processes, record PID/state digest/hypotheses/rejection trace,
and compute predictions without writes to scientific state. Compare uninterrupted
references. Freeze ALL final predictions before executing ANY held-out labels.
Evaluation must preserve state digest and exact checkpoint bytes/hash.

## Metrics and frozen criteria

Report support status, surviving candidates, admission/rejection/duplicate counts,
validation acceptance, coverage, accuracy among decisions (null at zero decisions),
abstentions and per-case/group correctness. Expected final unsupported coverage=0%,
8 abstentions, accuracy=null. Supported coverage=100%, correct=6/8, accuracy=75%
(fault cases h2,h5 fail). Ambiguous equality coverage=0%; non-equality=100%,
correct=3/4, accuracy=75%; overall coverage=50%, correct=3/4. THESE negative
control errors are frozen expectations, not permission to repair from held-out data.
Both controls must make specified decisions, so blanket abstention fails.

Integrity requires explicit empty/ambiguous/supported distinctions, six candidate
derivations, no rejected-input contamination or resurrection, validation preserving
the selected set, duplicate/conflict handling, actual two-stage restart parity,
identical ordinary-memory results, unchanged seed/protected sources/history,
read-only evaluation, source/config/protocol/hash/checksum guards and zero calls.
Tests cover malformed/unverified inputs, no vacuous consensus/acceptance, closed
phases, validation failure, oracle isolation and checkpoint/manifest drift.

Fresh archives capture prior dirty source identity, prework preservation hashes,
all source/tests/config/protocol, evidence and rejected inputs, training/final
states, predictions, results and failures. Do not overwrite/delete previous runs
or change criteria after outcomes. Reproduce the SAME fixed study once in a fresh
output directory; distinguish reproduction from inspection. Then stop, assess
the smallest supervised-runtime integration step and risks in documentation only;
do not recommend/dispatch another standalone study or implement integration.
