# Linguistic application pilot — protocol 1, Phase A

Frozen before implementation and before writer access to development passages,
2026-10-13. Phase A authorizes development-only implementation/testing and stops
before held-out execution for parent and independent custodian review. This is an
experiment-local supervised contextual cue learner, not production integration,
autonomous meaning discovery, philosophical geometry validation or seed benefit.

## Source, custody and split

Custodian source: official NLTK SemCor 3.0, 47 noun uses of lemma `order` in 31
documents and nine published sense keys. Human-origin annotations were automatically
remapped from WordNet 1.6 to 3.0. Supplied sense categories are not semantic truth,
newly discovered meanings or philosophical definitions. Preserve distributed notices;
underlying licensing remains unresolved. Internal, nonpublished pilot only.

Custodian hash-sorts document identities, assigns first floor(2N/3) documents to
development and the rest to evaluation, then splits development documents into
first floor(Ndev/2) and remainder. No reshuffle or sense merging. The custodian's
split identity/hash and approved development export hashes are pinned separately
before natural development execution; their absence blocks that execution. Writer
must not inspect/download SemCor or read raw/evaluation custody. Separation is
procedural, not a security boundary. Source-family overlap is unverified. Neither
this split nor a tiny corpus establishes statistical generalization.

Corpus passages, tokens, learned cue vocabulary, witness-bearing checkpoints and
development traces remain outside the repository and shareable source archives.
Repository summaries contain counts, opaque identities and hashes only. Source
archives exclude all outputs recursively and include no corpus. Source notices
remain with the custodian export and external working artifacts.

## Exact input and feature contract

Normalized training batch: `{split_id, batch, examples}`; batch is integer 1 or 2.
Each example has exactly `id`, `document_id`, `tokens`, `target_indices`, `sense`,
and `provenance`. Tokens are a nonempty list of nonempty surface strings. Target
indices are a nonempty sorted unique list of in-range integers (never Boolean).
Provenance has exactly nonempty strings `source`, `locator`, `source_sha256`
(64 lowercase hex). ID, document and provenance are lineage only, never features.
The custodian export adapter may translate its documented shape into this exact
schema without selecting examples or changing labels. Adapter mapping and hashes
must be recorded before development execution. Every observed development sense
is retained. No external WordNet lookup, morphology, stop-word resource or model.

Tokenizer: lowercase each non-target surface string, extract ASCII `[a-z]+`
segments, discard segments exactly `order` or `orders` everywhere, then use a set
of remaining segments. No other stop words, stemming, lemmatization, position,
frequency, sense-name features or weighting. Thus apostrophes/hyphens split;
non-ASCII letters are separators. This intentionally limited English surface
representation is frozen, not claimed linguistically optimal. Target positions are
removed before tokenization, including multi-token annotations. Full sentence is
the context; no adaptive window. Candidate cues are every unigram and every
unordered pair of distinct normalized tokens occurring together in a positive
development example. Cue ordering is lexical. No higher-order conjunctions.

Runtime application items have exactly `id`, `tokens`, `target_indices`; no sense,
document, provenance or extra fields. Reject malformed or gold-bearing requests
before application. A nonempty target span is required even when its surrounding
context has no retained tokens; that yields no match. These are supplied target
annotations, not learned target detection. Natural corpus lacks paraphrase-without-
target, overlapping-sense and unknown-sense gold; do not fabricate such labels.

## Learning, revision and rejection

For each observed sense independently, retain every candidate cue with all matching
positive and negative example IDs. Positive means the supplied label equals that
sense; every other supplied development label is a counterexample when the cue
matches. A cue is active iff positives cover at least two distinct documents and
there are zero admitted counterexamples. Otherwise it is rejected with explicit
`counterexample` and/or `insufficient_documents` reasons. All witnesses and original
training records are preserved; no majority fallback in primary.

Batch 2 recomputes from cumulative immutable development evidence, admitting new
cues and invalidating old active cues. Each complete batch creates a numbered,
immutable interpretation revision with supplied sense identity, executable cues,
witnesses, statuses and transitions from the previous revision. Previously active
cues rejected by new evidence are marked invalidated. Evidence is append-only, so
a counterexample cannot disappear and an invalidated cue cannot resurrect under
this protocol. A future new evidence basis would need a separately defined version;
no such recovery is implemented here. Initially insufficient cues can become active
when a second document supports them without contradiction.

Identical example ID/content repeats are idempotent and are recorded as duplicates;
conflicting content under the same ID, conflicting reuse of a source/locator, bad
provenance and cross-batch document reuse reject the entire batch without changing
the checkpoint. Exact replay of a committed batch is a no-op; a different replay
or out-of-order batch fails. Conflict is an input-contract failure, not a discovered
semantic contradiction to relabel. New rejected cues and invalidations are ordinary
scientific outcomes, not technical failures.

Each supplied sense has an interpretation record even with no active cues.
Interpretation lifecycle (`active` or `unsupported`) and cue lifecycle are separate
from application status. Application returns sorted matching sense set plus active
cue references: zero matches = `abstain`; one = `single`; multiple = `ambiguous`.
Only a singleton licenses a selected sense. Ambiguity is not broken by frequency.

## Frozen comparators and stage timing

1. Versioned primary: batch-1 snapshot, then cumulative batch-2 snapshot.
2. Ordinary structured memory: independently recompute the SAME unigram/pair rule
   generation and eligibility from identical cumulative examples. Shared schema
   validation/tokenization are permitted; it must not call primary rule generation
   or copy its learned table. Same stages, information, abstention and zero external
   acquisition cost. Expected exact cue/witness/prediction parity is engineering
   correctness, not a baseline expected to lose to LMFT.
3. Frozen batch-1 primary: always apply revision 1, including after batch 2.
4. Development majority diagnostic: cumulative example counts, lexicographically
   smallest exact sense key among tied maxima. Always selects when trained, even
   with empty context; untrained means abstain. Duplicates do not increase counts.

No additional comparators. No permission/action system is introduced: all four
receive the same passages and stage data, no calls or acquisition opportunities.
Preserve batch-1 predictions on batch-1 development examples, then batch-2
predictions on those same examples and the cumulative development set. Mark these
as resubstitution/development diagnostics, never held-out evidence.

## Persistence and evaluator CLI

Reuse existing `runtime_store.Store`, checksum, atomic JSON and lock primitives.
Use one experiment-local checkpoint schema with explicit kind, protocol SHA256,
implementation file hashes, split identity, immutable evidence and revision history.
Resume requires matching source/protocol pins; no silent migration or relaxed
manifest. Checkpoints and requests containing corpus stay outside repo.

CLI `linguistic_application_worker.py train --state-dir PATH` consumes one strict
JSON normalized batch from stdin. Batch 1 creates only a fresh state; batch 2
reloads. Exact replay must leave checkpoint bytes unchanged. `predict --state-dir
PATH` consumes `{items: [...]}` and returns the four controller outputs without
writing state. `inspect --state-dir PATH` returns only counts, stage and hashes.
Output includes process ID for actual fresh-process restart verification. Evaluator
must strip gold fields before predict and score separately; gold is never runtime
input. Phase A must not invoke this CLI on held-out items. Metadata hash pinning
and validation are integrity mechanisms, not protection against a malicious writer.

## Metrics and acceptance frozen before evaluation

For each stage/controller report item-level predicted label sets and singleton
selection. With supplied single gold g, strict correctness is exactly `{g}`;
wrong inclusions count labels in P minus `{g}`; exclusions count items where g is
absent from P. Separately report singleton coverage, zero-match abstention,
multiple-match ambiguity, singleton wrong count and whether g is included in an
ambiguous output. Report per-gold-sense denominators and these same counts,
including evaluation senses unseen during development if any. Count true-to-false
and false-to-true strict-correctness changes on identical development examples,
new/invalidated cue counts and coverage reductions separately. No composite score,
selective easy-sense analysis, imputed overlap gold or post-result threshold tuning.

Technical success: strict schemas/provenance; immutable, complete witnesses; exact
cue eligibility; no resurrection; independently computed memory parity; idempotent
duplicates and rejection without mutation; deterministic output; source/protocol
pin refusal; real process restart equality; predict/evaluation nonmutation; focused
and appropriate full regression success. Synthetic examples test malformed,
conflicting, overlap/unknown and provenance contracts only, not natural semantic
validity. Natural development can yield zero cues or no improvement without failing
technical acceptance. Record all failures and corrections.

Held-out improvement is a separate later authorized descriptive outcome: more
strictly correct items for updated primary than frozen batch 1 on the exact same
fixed evaluation set; also report every worsened item, wrong inclusion/exclusion,
coverage, ambiguity and unseen-sense count. This criterion alone does not establish
net utility or generalization. Equal/negative improvement is retained unchanged.
Primary/memory parity is mandatory and cannot be called seed advantage.

Stop on unapproved/missing export identity, malformed/conflicting data, source pin
mismatch, unexpected evaluation access or failed mechanical checks; preserve failed
evidence. Fix only demonstrable contract bugs before held-out execution, documenting
the correction without changing scientific thresholds. No models, teacher work,
dependencies, seed/configuration/random changes, production integration, commits,
pushes or publication. STOP after Phase A for parent/custodian review.
