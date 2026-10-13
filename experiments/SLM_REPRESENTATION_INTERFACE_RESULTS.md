# Four-call local-SLM representation interface check

2026-10-13. **Four authorized calls completed; zero proposals passed the frozen
contract.** No retries, repairs, replacement inputs or additional calls. This is
a known-development interface inspection, not a held-out semantic benchmark or
a revision of the consumed 14-case linguistic evaluation.

## Frozen execution and result

[Protocol](SLM_REPRESENTATION_INTERFACE_PROTOCOL.md) SHA256:
`1ff969b7de47f344848b4ad79fbc4725faca7f353779c04cf68ff41346666750`.
The four cases were selected mechanically: first example ID in each of the first
four sorted sense keys present in the approved development export. Both batches
were eligible. Exact selection IDs, source/original/request hashes, schema, system
prompt, code/config pins and assets were frozen before invocation. Gold sense keys
and document/example IDs were not in model requests; only indexed source surface
tokens, target span/quote and contract instructions were supplied.

Used existing `LocalModels.generate` interpretation transport only, offline, with
Qwen3-4B Q4_K_M revision `bc640142c66e1fdd12af0bd68f40445458f3869b`, SHA256
`7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5`.
Both llama.cpp b11429/CUDA12.4 archives and all 55 extracted files matched their
verified bytes. No downloads, extraction repairs or model/config changes occurred.
Context8192/output1024/temperature0/seed42/timeout120 seconds stayed unchanged.
Exactly one owned hidden loopback server (PID37016) served all four requests and
was closed afterward. No teacher, digestion, contemplation or activation call.

| Input | Transport | Prompt/output tokens | Elapsed seconds | Declared status / actual readings | First contract failure |
| --- | --- | ---: | ---: | --- | --- |
| representation-01 | stop | 1404 / 447 | 12.078 | one_reading / 2 | status/count mismatch |
| representation-02 | stop | 1630 / 370 | 2.422 | one_reading / 2 | status/count mismatch |
| representation-03 | stop | 1144 / 299 | 1.938 | one_reading / 2 | status/count mismatch |
| representation-04 | stop | 1590 / 424 | 2.875 | one_reading / 1 | no non-target context anchor |

All responses were parseable JSON and finished normally below the output limit.
Totals: 5,768 prompt tokens, 1,540 output tokens, 19.313 seconds across generate
calls; the first timing includes startup/asset verification. No generation timeout
or transport error was reported. No GPU-memory or broader performance claim follows.

The API trace's `validated` status means its validator returned an admissibility
REPORT; it does **not** mean the proposal passed. All four report.admissible values
are false and all four neutral records have lifecycle `rejected`. Returning the
report preserved failures without repairing outputs or restarting a healthy server.

## Attribution audit versus semantic judgment

Read-only inspection of the captured JSON found 26 anchor occurrences (including
target anchors): all quotes/indices match the source, but **all 26 cite only the
target token**. These are repeated occurrences, not 26 independent witnesses.
All four targets were copied exactly; zero readings cited surrounding context.
Thus the three status-mismatch cases also fail the contextual-evidence requirement,
even though the strict validator reported their earlier failure first. No output
was modified to see whether it could pass.

Cautious human inspection, separate from contract validation and without semantic
gold scoring:

- Input01 contains a domain-specific comparison paraphrase, but fails to explain
  the target expression and shifts attention away from the source's main proposition.
  The two readings and their relation/condition texts are duplicates.
- Input02 reflects an institutional directive/payment relationship, but repeats
  clause content rather than isolating a target-relative interpretation. Its two
  readings are duplicates; citing the target alone does not attribute the relation.
- Input03 captures an expected event's nonarrival. The intended kind of event is
  underdetermined from the fragment; the two near-duplicate formulations are not
  meaningful alternatives, and both are declared a single reading.
- Input04 is a long, incomplete near-copy with a mixed-language substitution and
  duplicated conditions. It does not clearly isolate the target's sequencing role.
  The source references needed to assess that interpretation are absent.

Some context-containing paraphrase appeared beyond the earlier failed function-word
co-occurrence cues. This is not evidence of accurate structured interpretation:
none was admissible, relations/conditions mostly repeat prose, and uncertainties
are not calibrated. Exact quotation proves attribution only; here even correct
target quotation did not provide useful contextual support. These judgments are
fallible human review, not independent annotations or model text promoted to truth.

The smallest remaining gap is producing one consistently counted, concise reading
with a genuine non-target source anchor. Semantic adequacy remains a separate gap
after that. Do not add a renderer/self-talk layer, integrate proposals into learning,
or claim seed utility on this evidence. Any narrower future interface/prompt/schema
investigation requires separate parent scope; this task makes no further calls.
The four development cases do not establish efficacy/generalization, and possible
pretraining exposure remains unresolved. The consumed 14-case split stays consumed.

## Shared record and verification

One neutral, explicitly unverified/rejected source-bound contract serves both
primary-facing and ordinary structured-memory consumers. No duplicate learner,
extra inference, philosophical binning or authority was introduced. Both consumers
retrieved identical records/hashes after an actual fresh-process restart; the
checkpoint remained byte-identical. This establishes faithful access to rejection
evidence, not successful interpretations or primary superiority.

**42 synthetic focused tests and 1,296 full tests passed**, zero failures/skips.
The 42 additions cover schema/status counts, integer anchors, exact quotations,
overlapping versus duplicate spans, target/context requirements, malformed responses,
provenance/type corruption, semantic-unverified distinction, duplicate/conflicting
IDs, consumer nonmutation, actual restart and four-attempt/no-resume/no-repair guards.
No synthetic outcomes are presented as natural linguistic gold. Full tests took
223.41 seconds. An initial console inspection hit a Unicode display encoding error;
escaped-JSON reading completed the review without altering any model artifact.

New experiment-local files: `slm_representation.py`, `run_slm_representation.py`,
the protocol/results documents, and `tests/test_slm_representation.py`.
Shared LocalModels/Store, completed cue learner, its scientific protocol, canonical
seed, numerical mechanisms, model/configuration and dependencies remain unchanged.
Final source/configuration archives and verification are in
`outputs/slm-representation-interface-20261013-001/`.

## Exact recovery artifacts and limits

Fresh stable nonpublished folder:
`C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-20261013-001`.
It contains notices, selected original records/source tokens, exact frozen requests,
schema/prompt, all raw responses/traces, attempt marker/count, owned-server log,
neutral checkpoint and restart evidence. Existing research archives were untouched.
No raw corpus, prompt containing corpus or model response was copied into repository
source archives or result prose. Repository copies contain counts, opaque IDs and
hashes; system instructions/schema are also recoverable from pinned source.

Neutral checkpoint SHA256:
`8ca59c990dc2242651edca622c8fbb0634deb1e53e8707524d8a7e9c5a0e22b4`.
Contract source SHA256:
`594218f50ab9c26be1437531c2a6c0567a344c1708f7b1af3b1fed9bc0ba19a5`.
Runner source SHA256:
`1ab612bba28de5bc293d9dbcec2d89db628e7a23f121b5ab78cad2c1b1c930ca`.
`frozen-manifest.json` and `run-summary.json` in the repository output directory
record all four exact input/request/output hashes; final verification pins external
artifacts and both source snapshots. A run-started marker prevents resuming/repeating
this four-attempt scope. Original outputs require matching source pins; no migration.

SemCor/Brown licensing ambiguity remains; the folder is local/nonpublished, not
permission to redistribute. No model-generated content became fact, accepted meaning,
permission, numerical membership or canonical philosophy. No commits/push/discard.
**Stop for independent parent review; no follow-on task started.**
