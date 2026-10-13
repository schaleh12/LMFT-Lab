# Linguistic application Phase B: negative result and bounded diagnosis

2026-10-13. **The preregistered improvement criterion failed.** All 14 held-out
examples in 11 documents have now been used. This split is consumed: it must never
be presented as fresh evaluation for a revised learner. No tuning, new experiment,
model call or classifier change was performed for this report.

## Result and evidence boundary

The independent evaluator accepted the type-validation correction before Phase B,
committed predictions before joining gold, and retained four fresh held-out worker
processes (two stages, original and repeat). Repeated predictions agree, primary
and independently computed memory agree, and checkpoints were not mutated.

| Stage/controller | Correct singleton | Wrong singleton | Abstain | Ambiguous | Wrong label inclusions | Gold exclusions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Stage 1 primary/memory/frozen | 0 | 0 | 14 | 0 | 0 | 14 |
| Stage 2 primary/memory | 0 | 3 | 10 | 1 | 5 | 14 |
| Stage 2 frozen batch 1 | 0 | 0 | 14 | 0 | 0 | 14 |
| Majority, either stage | 7 | 7 | 0 | 0 | 7 | 7 |

Zero strict-correct gains and zero strict-correct losses **do not mean no harm**:
case-0001, case-0003 and case-0014 changed from abstention to wrong singletons;
case-0006 changed to an ambiguous set containing two wrong labels and excluding
gold. Singleton coverage rose from 0/14 to 3/14, entirely through errors. Majority's
7/14 correct labels outperform the learned rule system's 0/14 on strict accuracy;
the experiment does not assign utility weights to its additional wrong choices.

Gold denominators: `order%1:10:03::` 7, `order%1:07:01::` 3,
`order%1:26:00::` 2, `order%1:14:00::` 1 and `order%1:14:02::` 1.
The last is unseen in development at both stages (case-0013): primary/memory/frozen
abstained and majority was wrong. It is retained in all denominators. Training
categories and corpus annotations are supplied, not newly discovered meanings or
semantic truth; neither ambiguity nor abstention establishes a natural semantic label.

Reviewer independently reproduced 91 focused tests, rejection of all 10 original
bad-checkpoint inspect/predict probes, eight development worker processes with
identical results, and the held-out captures/independent metric recount. The 1,254
full-suite passing XML was inspected, **not independently rerun**. This documentation
task verified evaluator artifact/source hashes and performed trace joins; it did
not rerun learning, prediction, evaluation or tests.

## Observed trace evidence

Every held-out rule firing came from three stage-2 conjunctions below. These brief
tokens are included solely to identify the failure mechanism; no natural passages
or token arrays are copied into the repository. Rule IDs below are unique prefixes;
full IDs/counts are in `outputs/linguistic-phase-b-diagnosis-20261013-001/trace-diagnosis.json`.

| Rule prefix | Cue | Supplied sense | Positive examples / distinct documents | Admitted counterexamples | Firing cases |
| --- | --- | --- | --- | ---: | --- |
| `4620c42e29f8` | `a` + `by` | `order%1:10:00::` | 2 / 2 | 0 | 0001, 0003, 0006, 0014 |
| `f038e42fd66c` | `and` + `by` | `order%1:10:00::` | 2 / 2 | 0 | 0006 |
| `d9485da2c3ba` | `be` + `was` | `order%1:10:03::` | 2 / 2 | 0 | 0006 |

All three existed in stage 1 but were rejected for only one positive document.
The second batch supplied their second supporting document, making them eligible
under the frozen rule. The first two have exactly the same two positive witnesses;
their co-firing is not independent corroboration. Distinct document IDs are verified;
source-family independence is not established. Individual component words occur
in other-sense development examples: respectively 11/3, 15/3 and 1/3 negative
examples. Their *joint* absence from negative development examples admitted the
pairs. Witness counts and identities were checked against retained training records.

No active gold-sense cue matched any of the 14 cases. Specifically:

- `order%1:26:00::` has five development examples across four documents but no
  active cue. Its two held-out cases are 0001 and 0006. They match 10 and 24 of its
  rejected candidates; every such candidate has a development counterexample.
- `order%1:07:01::` has one active cue, which matches none of its three held-out
  cases. Each matches nine rejected gold candidates, all with counterexamples.
- `order%1:14:00::` has eight active cues, none matching its one held-out case;
  17 matching gold candidates were rejected with counterexamples.
- `order%1:10:03::` has 17 active cues, none matching its seven held-out cases.
  Matching rejected candidates have counterexamples and/or too few supporting
  documents. In erroneous case-0014, all 18 matching gold candidates have
  counterexamples. Other cases also expose insufficient-document candidates.
- The unseen `order%1:14:02::` has no supplied development interpretation at all.

The machine-readable diagnosis retains every opaque case's counts and rejection
reason combinations. These are post-result explanations of fixed decisions, not
evidence admitted to the learner. No rejected cue was reinstated using evaluation.

## Interpretation, distinct from observation

The evidence points to inadequate context representation and sparse supervised
support, rather than a newly demonstrated contract defect. All observed firing
cues satisfy the specified two-document/no-counterexample rule; recorded matches,
witnesses, lifecycle changes and independent memory outputs are consistent. This
bounded audit does not prove the entire implementation bug-free. The previously
found numeric-type bug was corrected before these pinned predictions and does not
explain their label errors.

All three firing pairs consist of common function words. The learner searches many
unigram/pair candidates (10,227 cumulatively) and treats lack of a counterexample
in 33 training examples as sufficient admission. Whole-sentence sets discard order,
distance, syntax, target-relative roles and conditions. A conjunction can therefore
be perfectly consistent in this small sample without expressing the target's sense.
Accidental sample co-occurrence is a supported explanation, not a proven causal
linguistic account of every passage. Removing these particular words or adjusting
support thresholds now would tune against the exposed 14-case evaluation and would
not establish a general solution. No such changes were made.

The experiment validates inspectable supervised evidence/revision machinery and
exposes this representation's failure on this sample. It does not validate meaning
acquisition, general language understanding, philosophical seed benefit or the
owner's intended cross-cutting contextual geometry. That intent is not six-bin
dictionary sorting and remains a separate, untested architectural hypothesis.

## One proposed next capability step — separate authorization required

Propose a **bounded context-representation contract using the existing local SLM**,
with target-relative relations/roles, conditions, alternative readings and explicit
insufficient-context output anchored to source evidence. Model output would remain
a versioned proposal, distinguishable from admitted persistent evidence and from
independent evaluation. This targets information discarded by bag-of-word pairs;
more hand-tuned lexical exclusions would primarily patch the observed symptoms.

The repository already pins `qwen3_4b` (Qwen3-4B Q4_K_M) in `config/local_models.json`
and provides a proposal-only local transport. That is an available implementation
direction, not evidence of successful contextual extraction or a reason to activate
the existing seed-membership/propagation pipeline for this purpose. Reuse of the
model transport would need separately authorized experiment-local work; no new
teacher/model/dependency or configuration change is proposed here. No model was
called, loaded or downloaded for this assessment.

Before any future run, independently select a new lawful dataset/split, freeze the
representation and adjudication criteria before its gold is exposed, and match the
same SLM/information/budget in an ordinary structured-memory comparator. Distinguish
fresh SLM inference from persistent application/revision; extraction errors and
pretraining contamination are additional limitations, not solved by a richer output
schema. The consumed split can illustrate known failures only. This proposal is one
capability prerequisite, not an approved experiment or promise of improvement.

## Honest status view already supported by evidence

Existing records can expose revision/source identity, candidate lifecycle, matched
rule IDs, deduplicated supporting-document counts, observed counterexamples,
rejection reasons, and application status `abstain`/`single`/`ambiguous`. That is
enough for a small factual uncertainty view without a generative self-talk layer.
For case-0006 it would report two matching interpretations, three rules but only
two distinct supporting witness sets, and no selected sense. It must not label a
singleton "confident", equate no observed counterexamples with reliability, or
claim abstention identifies novelty. Gold correctness belongs only in the separate
evaluator view. No renderer or new status mechanism was implemented.

## Provenance, preservation and stop

Evaluated protocol SHA256:
`00967e14b87adafa06aa0be3935e24621f05e0172f0019966061caba918ab964`.
Evaluated learner SHA256:
`cf7249dc7b5d954d4cfa63880bfb5b6cd8f4dfa5739626e179b797131ccd4acd`.
Evaluator aggregate SHA256:
`e2cb6bb72b0eac5d7d693152e663510ca4678a1e00e8a1f9cf8f1a65c52be78f`.
Prediction commit SHA256:
`753c1e7f767b11e3606556a7f3699c70a3022e767ab687c1ee121a36df8ae78a`.

Original evaluator artifacts remain external at
`C:\Users\schal\AppData\Local\Temp\lmft-linguistic-gated-evaluation-c_98o9jq`.
Only numerical aggregates, sense/rule identities and hashes enter the report archive;
raw corpus/custody/checkpoints remain external with notices. Licensing is unresolved,
custody was procedural, and document separation does not prove source-family
independence. Temp retention is not durable backup or publication permission.

`outputs/linguistic-phase-b-diagnosis-20261013-001/` records prework/final source
snapshots, evaluator hashes, aggregate results, sanitized trace diagnosis and final
verification. Executable/configuration/protocol/test files remain byte-identical;
prior negatives, checkpoints and uncommitted work are preserved. No commit/push,
model call, new experiment, stop-word addition, threshold change or rule pruning.
**Stop for parent review; no follow-on task has been started.**
