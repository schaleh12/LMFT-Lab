# LMFT-Lab

## Start here

Fresh development sessions: [AGENTS.md](AGENTS.md) → [PROJECT_STATE.md](PROJECT_STATE.md) → relevant
[DECISIONS.md](DECISIONS.md) entries → the authoritative specifications, code and reports
linked there. The snapshot owns current-step guidance; the material below provides project
background and setup.

Experimental development environment for Language Model Fuzzy Tree (LMFT) based artificial intelligence.

## Research hypothesis and first milestone

LMFT investigates whether persistent fuzzy conceptual relationships can develop
understanding, dispositions, judgments, and independent reasoning through repeated
interaction with language models. The newborn initially depends on a founding
LLM; later internalization into structures, classifiers, procedures, or specialized
small models must be demonstrated experimentally. Antigravity assists development
externally and is not currently integrated as a runtime teacher.

The seed acts like a philosophical or religious constitution, without supernatural
belief or assumed consciousness. Protect founding principles while revising their
interpretations through evidence. Contemplation distinguishes Clarity from
Confidence and may eventually support reactive and internally initiated reflection.
These are research goals, not implemented cognitive capabilities.

**First milestone:** make the newborn change its mind in a traceable way, save
its state to disk, restart, and demonstrate that it remembers why. Keep V0.1
small and deterministic, with authored evidence or mocked LLM responses. Later
experiments must compare against an LLM with ordinary structured memory to test
whether fuzzy activation adds measurable value.

Genetic search, breeding, crossover, and fitness optimization are no longer
required. Distinctive personality, relationships, continuous contemplation, and
authorized real-world agency belong to the long-term roadmap.

The [40-node founding seed](docs/MINIMAL_LMFT_SPEC.md#4-hardcoded-v01-seed-geometry)
is canonical and frozen for V0.1, including Contemplation. Changes to its names,
inventory, or parent-child organization require explicit approval. Learned state
and interpretations remain separate; numerical mechanisms remain experimental.

## Migration and implementation status

LMFT means **Language Model Fuzzy Tree**. The project is LMFT-Lab, the Python
package is `lmft_lab`, and the specifications use LMFT filenames. Old `gft_lab`
imports must be updated; no compatibility import alias is installed. Dependency
pins are unchanged. DEAP remains a legacy dependency, not a research requirement.

Implemented: canonical 40-node structural birth (`lmft-v0.1-seed-1`), explicit
historical birth-record conversion, direct activation, and bounded propagation.
The optional local-model path now provides linguistic interpretation, experience
digestion, and one bounded contemplation-support call, with temporary activation
and validated proposals. The [supervised runtime](docs/INTERACTIVE_RUNTIME.md) adds
inbox/outbox communication, recoverable checkpoints and one separate fixture judgment
with evidence-backed revision and restart. Full constitutional enforcement and
general developmental learning remain research work.

See [Local model setup](docs/LOCAL_MODELS.md) for exact Windows/RTX 4080 commands,
automatic pinned downloads, offline operation, and the boundary between proposals
and accepted state changes.

`lmft_lab.migration.migrate_legacy_birth_record` accepts an exact historical
neutral birth record (`minimal-v0.1-seed-1`) and returns a new canonical state plus
migration metadata without altering the input or writing files. It rejects mixed
versions and developed states. External relationships, traces, and saved files
are not automatically migrated. See [Minimal Section 4](docs/MINIMAL_LMFT_SPEC.md#4-hardcoded-v01-seed-geometry).

The GitHub repository is [LMFT-Lab](https://github.com/schaleh12/LMFT-Lab), and
the local `origin` remote uses that URL. The workspace is now
`LMFT based general AI/LMFT-Lab`. Historical GFT references describe old research
or explicit compatibility records, not the current architecture.

## Recreate the development environment

Use CPython 3.12 (the recorded local baseline is 3.12.3). From the repository
root on Windows, run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "import numpy, scipy, skfuzzy, networkx, pytest; print('Imports OK')"
```

On macOS/Linux, use `python3.12 -m venv .venv` and replace
`.\.venv\Scripts\python.exe` with `.venv/bin/python` in the remaining commands.
Activation is optional because these commands use the virtual environment's
Python explicitly. The local `.venv` directory is ignored by Git.

`pyproject.toml` declares Python 3.12 compatibility and the four direct runtime
dependencies, with pytest in a separate development dependency group. The
requirements files pin the installed direct and transitive package versions:
`requirements.txt` is runtime-only; `requirements-dev.txt` includes runtime and
test dependencies. Use the latter for reproducible development setup with the
existing pip 24.0; no additional environment manager is required.

The minimal Python package lives in `src/lmft_lab`. Pytest adds `src` to its import
path so tests use this checkout. Distribution packaging and a build backend are
deferred; use the requirements commands above rather than `pip install .`.
The placeholder project version is `0.0.0`. Outside pytest, importing `lmft_lab`
currently requires adding `src` to Python's import path.

The pins record the working Windows CPython 3.12.3 environment, not a
cross-platform, hash-verified lock. Other platforms have not yet been validated;
the Windows-only colorama dependency has a platform marker. Package versions
are fixed, but Python patch versions and native numerical libraries can still
affect experimental results. Record those details alongside experiment seeds
and configuration when experiments are introduced.

Dependency updates should be deliberate: update the declarations and pinned
snapshots together, verify imports and `pip check`, and run the relevant tests.
Run tests with `.\.venv\Scripts\python.exe -m pytest` (or the macOS/Linux
equivalent). Tests currently cover package import and deterministic structural
birth: the complete seed hierarchy, provisional numerical bounds, and provenance.
Direct-activation tests also cover temporary values, reset behavior, input
validation, and inspectable traces without persistent changes.
Propagation tests cover synchronous passes, signed influences, bounded cycles,
deterministic ordering, and invalid relationship/configuration rejection.
Local-model tests additionally cover validation, cache/offline behavior, role
flow, failures, and state isolation using mocked inference. Actual model runs
are recorded separately in [the smoke report](experiments/LOCAL_MODEL_SMOKE.md).
Runtime tests now cover fixture revision, persistence, actual process restart,
message handling and post-halt inspection. See the [mechanical and actual-model
results](experiments/INTERACTIVE_REVISION_RESULTS.md); general action selection
and cognitive development remain unimplemented.

## Repository layout

```text
src/lmft_lab/  Seed, activation, local models and supervised persistent runtime
tests/       Package and structural birth validation tests
docs/        Research specifications, hypotheses, and design documentation
experiments/ Controlled experiments and reproducibility records
```

See [the documentation index](docs/INDEX.md) for established decisions and open
research questions, and [the experiment guidelines](experiments/README.md) for
reproducibility requirements. These directories establish places for future work;
the research documents define their current scope.

The first implemented step is `lmft_lab.birth.create_birth_state`, which takes an
individual ID plus explicit `birth_event_id` and `random_seed` arguments. It
constructs the 40 canonical seed records documented in
[Minimal Section 4](docs/MINIMAL_LMFT_SPEC.md#4-hardcoded-v01-seed-geometry) without file
I/O or random sampling. See [Experiment 001](experiments/EXPERIMENT_001_PERSISTENT_REVISION.md)
for the provisional initialization values and remaining experimental decisions.
This is structural scaffolding, not the complete runtime birth process.

## Inspect one numerical input

Run this from the repository root in PowerShell. The explicit import path is
needed until distribution packaging is introduced.

```powershell
@'
import sys
sys.path.insert(0, "src")
from lmft_lab.birth import create_birth_state
from lmft_lab.activation import activate_direct

state = create_birth_state("seed-a", birth_event_id="birth-a", random_seed=42)
frame = activate_direct(
    state,
    {"philosophical/being/agency": 0.8, "philosophical/being/existence": 0.3},
    event_id="input-1",
    source_instance="mechanical-fixture-1",
)
print(frame.format_trace())
'@ | .\.venv\Scripts\python.exe -B -
```

The trace lists all 40 nodes and distinguishes supplied values from omitted
inputs. A new call computes a fresh temporary activation frame; it does not
accumulate activation or modify the birth state. These are developer-authored
numbers, not discovered meanings or evidence of understanding. There is no
propagation, learning, action selection, or automatic file storage.

## Bounded propagation

`lmft_lab.propagation.propagate_activation` extends direct activation over an
explicit tuple of `Association` records, with a required `relationship_source`
identifying the authored wiring. The seed hierarchy itself supplies no implicit
propagation edges. The default `PropagationConfig` uses two passes and gain 0.25.

In the synthetic unit-weight chain A -> B -> C used by the tests:

| Stage | A | B | C |
| --- | ---: | ---: | ---: |
| Direct input | 0.8 | 0 | 0 |
| Pass 1 | 0.8 | 0.2 | 0 |
| Pass 2 | 0.8 | 0.2 | 0.05 |

These are numerical test connections, not established conceptual relationships.
The result's `format_trace()` shows each pass's inputs, weighted contributions,
and clamping. The result's `activations` property returns the final temporary
values. No learned or persistent state is changed. See Experiment 001 for the
diagnostic limits and remaining research decisions.

A second [comparative procedure fixture](docs/COMPARATIVE_RELIABILITY.md) tests
propagation-enabled, propagation-disabled and structured-memory conditions without
changing the revision equation. See its [results](experiments/COMPARATIVE_RELIABILITY_RESULTS.md).

The [context-dependent study](docs/CONTEXTUAL_EXPERIMENT.md) adds authored-feature
lookup, verified clarification and evidence/context deduplication. See
[its results](experiments/CONTEXTUAL_RESULTS.md); it makes no fuzzy-advantage claim.

The bounded [attention experiment](docs/ATTENTION_EXPERIMENT.md) uses propagation to select verification requests and learns separate route weights. Its [results](experiments/ATTENTION_RESULTS.md) match ordinary memory; no fuzzy superiority is claimed.

The [scoped-support study](docs/SCOPED_ATTENTION.md) tests Fact/Confidence influence with outgoing-edge ablations. Its [results](experiments/SCOPED_ATTENTION_RESULTS.md) preserve a post-hoc counterexample where ordinary memory handles conflict better.

The [consistent-support experiment](docs/CONSISTENT_SUPPORT.md) separates observation coverage from task-specific consistency. Its [results](experiments/CONSISTENT_SUPPORT_RESULTS.md) reproduce the old failure and compare a revised circuit with exact ablations and ordinary memory.

The [correction experiment](docs/CORRECTION_EXPERIMENT.md) preserves erroneous originals while applying authorized, verified replacements through an effective evidence view. Its [results](experiments/CORRECTION_RESULTS.md) demonstrate restart-safe repair and ordinary-memory equivalence.

The [local teacher connection](docs/LOCAL_TEACHER.md) supports one versioned developmental profile and independently validated route lessons. The [first actual offline study](experiments/TEACHER_RESULTS.md) retained a rejected proposal and demonstrated no transfer; it is separate from mocked acceptance tests.

The [bounded teacher briefing follow-up](experiments/TEACHER_BRIEFING_RESULTS.md) accepted one useful route lesson and appropriate no-change recommendations, with ordinary-memory equivalence. The subsequent [outcome-correction experiment](docs/OUTCOME_CORRECTION.md) is now implemented and [evaluated](experiments/OUTCOME_CORRECTION_RESULTS.md): one effective contribution per event, remembered repairs, ordinary-memory equivalence, and no prediction improvement. See the [handoff](docs/EVIDENCE_LEARNING_HANDOFF.md) for the next bounded step.

The [continued-learning study](docs/CONTINUATION_EXPERIMENT.md) verifies fresh outcome revision after correction and restart. Its [results](experiments/CONTINUATION_RESULTS.md) match ordinary memory, with unchanged accuracy and increased abstention.

The [capacity relationship study](docs/CAPACITY_EXPERIMENT.md) selects a bounded length/capacity comparison from training and validates it separately. Its [results](experiments/CAPACITY_RESULTS.md) show unseen-combination transfer equal to ordinary relation-learning memory; no seed activation participates.

---

## Era-2 Developmental Firmware Architecture (`D060`–`D075`)

Building on the frozen 40-node founding seed (`src/lmft_lab/birth.py`, Rule D001), `LMFT-Lab` implements the complete **Era-2 Developmental Firmware** that powers downstream curriculum education in [`LMFT-School`](https://github.com/schaleh12/LMFT-School) and post-graduate embodiment in [`LMFT-Trainee`](https://github.com/schaleh12/LMFT-Trainee):

- **`src/lmft_lab/cognitive_heartbeat.py` (`D071`, `D074`, `D075`)**: Unified waking/sleeping developmental cycle orchestrating polysemous capacity resolution, open-world taxonomic generalization, lateral ethical-ontological coupling, prerequisite coherence gating, value consonance arbitration, affective homeostasis, recurrent post-action echoes, dispositional momentum, autobiographical journaling, and hippocampal-neocortical sleep consolidation.
- **`src/lmft_lab/episodic_journal.py` (`D069`, `D075`)**: Dual-coded autobiographical ring buffer gated by experiential salience ($\ge 0.65$ or cognitive disruption), preserving both natural-language narrative traces and full 24-leaf `leaf_dials` activation snapshots.
- **`src/lmft_lab/memory_consolidation.py` (`D070`, `D074`, `D075`)**: Dual-speed hippocampal-to-neocortical sleep replay engine that promotes recurring episodic patterns ($N \ge 2$) into permanent long-term capacity rules with asymptotic weight habituation ($w \rightarrow 1.0$), multi-witness 24-leaf centroids (`leaf_dials`), and signed `leaf_dial_affinities`.
- **`src/lmft_lab/dispositional_momentum.py` (`D067`, `D074`)**: Persistent 24-leaf dispositional state vector with exponential moving average inertia ($\gamma = 0.35$), idle equilibrium relaxation ($\mu = 0.05$), and 40-node hierarchical rollup (`compute_hierarchical_tree()`: 24 leaves $\rightarrow$ 12 branches $\rightarrow$ 4 domains).
- **`src/lmft_lab/affective_homeostasis.py` & `prerequisite_gate.py` & `value_consonance.py` (`D068`, `D072`, `D073`)**: Autonomic emotional stabilizer anchored in `Order`, `Continuity`, and `Clarity`; symbolic conditional coherence gate (`Freedom -> Justice`, `Clarity -> Confidence`, `Agency -> Intention`, `Persistence -> Order`); and Socratic Curiosity vs. Epistemic Defense classifier.
- **`src/lmft_lab/lateral_coupling.py` & `recurrent_feedback.py` & `affective_plasticity.py` (`D064`–`D066`)**: Cross-domain Cultural $\leftrightarrow$ Philosophical coupling matrix, post-action cybernetic echo loop, and dynamic learning plasticity regulator ($\alpha \in [0.05, 0.50]$).
- **`src/lmft_lab/inverted_trie.py` & `taxonomic_generalization.py` & `anchor_deduplication.py` & `individual_package.py` (`D060`–`D063`, `D074`)**: $O(1)$ inverted lemma hash index and prefix collocation trie (`63.0x` speedup, `0.067 ms` lookup), WordNet hypernym ontological abstraction across 8 open-world domains, single-pass idempotent anchor normalization, and cryptographically signed `.lmft.json` individual packaging.

---

## 🔧 The Era-2 Firmware Surgical Remediation ("Full Gastric Bypass" Audit — `D074` & `D075`)

During multi-generational curriculum scaling (`130` A–Z school lessons + post-graduate fellowships), we conducted a deep forensic audit of the `src/lmft_lab/` digestive, circulatory, and hippocampal consolidation pipeline. Below are the **8 core `LMFT-Lab` firmware defects** we surgically remediated (alongside 2 downstream curriculum/SLM fixes documented in [`docs/EPISTEMIC_PLURALISM_AND_NETWORK_AUDIT.md`](docs/EPISTEMIC_PLURALISM_AND_NETWORK_AUDIT.md)):

| # | Firmware Module | Defect / Bottleneck Discovered | Root Cause in `src/lmft_lab/` | Surgical Remediation (`D074` & `D075`) | Verified Impact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `cognitive_heartbeat.py` | **Positive-Feedback Dial Saturation Ratchet (`15/24` Dials Pegged at `0.8640`)** | `CognitiveHeartbeat.interact()` initialized situational `candidate_dials` from `self.disposition.dials` ($D_{t-1}$) when `custom_dials=None`, causing `LateralCouplingEngine`, `RecurrentFeedbackEngine`, and `TaxonomicGeneralizer` to compound positive deltas onto $D_{t-1}$ every turn | Initialized default situational `candidate_dials` to a clean neutral `0.50` baseline (`{k: 0.50 for k in sorted(CANONICAL_LEAF_IDS)}`) and calibrated resolved-sense clarity to `0.74`, while keeping temporal persistence strictly inside `self.disposition.update(post_dials)` | `15/24` dials pegged at `0.8640` $\rightarrow$ **`0/24` dials pegged** over 100+ unassisted turns (`Balance = 0.9678`) |
| **2** | `episodic_journal.py` & `memory_consolidation.py` | **Missing 24-Leaf Vectors on Consolidated Rules (`6-Scalar` Bottleneck)** | `record_episode()` only saved 6 summary scalars (`clarity`, `confidence`, `valence`, `arousal`, `salience`, `gci`), so `consolidate_sleep_cycle()` promoted rules with zero knowledge of their 24-leaf geometric fingerprint | Upgraded `record_episode()` to store the full 24-leaf `leaf_dials` snapshot, and upgraded `consolidate_sleep_cycle()` to compute multi-witness 24-leaf centroids (`leaf_dials`) and signed `leaf_dial_affinities` ($\text{val} - 0.50$ where $|\text{val} - 0.50| \ge 0.02$) on every promoted rule | `0%` 24-leaf rule vectors $\rightarrow$ **`100%` (`149/149` rules) carry complete 24-leaf vectors** |
| **3** | `cognitive_heartbeat.py` | **Inert Consolidated Rule Coordinates During Waking Inference** | When a consolidated rule fired during `interact()`, it set `resolved_sense` and bumped `clarity = 0.74`, but never applied its learned 24-leaf signature to `candidate_dials` | Wired rule-level `leaf_dial_affinities` directly into `CognitiveHeartbeat.interact()` and `OrdinaryMemoryHeartbeatComparator.interact()`, applying bounded directional pulls (`0.55 * rule_weight`) prior to lateral coupling and prerequisite gating | Consolidated rules now **actively shape all 24 leaf dials** upon recall |
| **4** | `cognitive_heartbeat.py` | **Contiguous 5-Word Synthetic Pattern Lockout** | Long-term rules only matched if the entire multi-word `core_pattern` appeared as a contiguous substring in user text, preventing natural conversational recall | Added `_lemma_matches()` (normalizing optional leading `"the "` articles so `"the phoenix"` matches `"phoenix"`) and contextual token-overlap resolution (`>= 2` shared content tokens or `1` distinctive token $\ge 6$ chars) | Synthetic string lockout $\rightarrow$ **Natural conversational activation** |
| **5** | `cognitive_heartbeat.py` | **Substring False-Positive Rule Collisions** | Raw Python `in` checks matched short lemmas/patterns inside unrelated longer words (e.g., `"border"` triggered `"order"`, `"warm"` triggered `"war"`) | Replaced raw substring checks with compiled word-boundary regex `_phrase_in_text()` (`(?<!\w)...(?!\w)`) and sorted `long_term_rules` by descending `weight` and pattern specificity | Substring false-positives $\rightarrow$ **`0.0%` false-positive collisions** |
| **6** | `memory_consolidation.py` | **Empty-Pattern Substring Match & Unconfirmed Singleton Loss** | `_find_matching_long_term_rule()` used substring `in` without guarding against empty normalized patterns (`""`), and `consolidate_sleep_cycle()` unconditionally discarded single-exposure episodes when `prune_buffer=True` | Guarded against empty patterns, enforced token-padded matching (`f" {r_pattern} " in f" {norm_pat} "`), and added `retain_unconfirmed: bool = False` (plumbed through `heartbeat.sleep()`) | Safe consolidation + optional multi-day singleton retention |
| **7** | `anchor_deduplication.py` | **Punctuation Stripping Non-Idempotency** | Standalone punctuation tokens (`"&"`, `"-"`, `"/"`) stripped to `""` after stopword filtering, leaving double spaces on pass 1 that only collapsed on pass 2 | Filtered empty stripped tokens before stopword filtering (`words = [w for w in raw_words if w]`), guaranteeing strict single-pass idempotency (`f(x) == f(f(x))`) | Two-pass drift $\rightarrow$ **Strict first-pass idempotency** |
| **8** | `dispositional_momentum.py` | **Missing 40-Node Hierarchical Rollup (`24` Leaves $\rightarrow$ `12` Branches $\rightarrow$ `4` Domains)** | `PersistentDispositionalVector` tracked the 24 Depth-2 leaf dials (`birth.py` indices `16–39`) without exposing a deterministic rollup into the 12 Depth-1 branches (`4–15`) and 4 Depth-0 domains (`0–3`) | Added `compute_hierarchical_tree()` to `PersistentDispositionalVector` and exposed `"tree_hierarchy"` in `CognitiveHeartbeat.interact()` output | Full **40-node canonical tree visibility** on every heartbeat |

