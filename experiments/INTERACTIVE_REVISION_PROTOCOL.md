# Interactive revision fixture v1 — frozen protocol

This preregistration precedes evaluated execution. It implements a narrow mechanical
subset of Experiment 001; it does not execute that document's broader developmental
study. No change to founding nodes or existing activation/update equations is made.

## Target and rule

The separate judgment `fixture/channel-agreement` estimates agreement in an authored
synthetic measurement table. Initial score is 0. This is not a moral disposition,
a probability, or the founding Confidence node. Clarity is not numerically learned.

Frozen measurements: `sample-a` = channel 3, reference 3; `sample-b` = 4, 5;
`sample-c` = 7, 7; `sample-d` = 8, 9. These are simulated ground truth, not
external observations validated by an LLM. Incoming evidence must exactly match a
sample ID and its two integer measurements. Teacher identity or persuasive wording
cannot make another record eligible. Each sample ID contributes at most once.
Supporting evidence has sign +1, contradicting evidence -1. For n accepted samples,
score = sum(signs)/(n+2), bounded in [-1,1]. Read-only probe returns `support` for
score >= 0.2, `oppose` for score <= -0.2, otherwise `undetermined`. No decay,
confidence calibration, or fuzzy-propagation benefit is claimed. This fixture rule
is separate from the provisional node-baseline equations, which remain unchanged.

Reject mismatched, unknown, repeated evidence or evidence in an invalid reply;
record reasons and before/after scores. Learning-disabled mode rejects otherwise
eligible evidence without changing the judgment. Model judgment strings are
retained as proposals and have no acceptance authority.

## Communication and acceptance

One authored clarification is emitted for the initial lack of eligible evidence;
one further issue type is possible when supporting and contrary evidence coexist.
At most one question remains open, and an issue type is never asked twice. A linked
teacher reply closes the addressed question, even if its evidence is rejected.
Unanswered questions persist without scheduled inference or repeated output.
Responses expose only the selected probe, acceptance reason, and evidence IDs.
Model wording is not needed for this fixture; all outgoing wording is authored.

Freeze software/config hashes in each individual. Evaluation uses mocked roles,
not live inference. Initial probe must be undetermined; an observation without
evidence must emit a clarification; a linked reply carrying sample-a must yield
1/3 and support. Stop and restart the actual process; persisted evidence and reason
must remain exactly equal. Compare an uninterrupted individual with the same
messages. Duplicate delivery must add neither evidence nor outgoing messages;
new message IDs carrying sample-a must also leave score unchanged. Sample-b alone
must yield -1/3 and oppose; a learning-disabled control must remain 0. Comparisons
are exact Python float equality for this deterministic rule, excluding timestamps,
PIDs, and storage metadata. Adding sample-b after sample-a must yield 0 and preserve
both support and contrary evidence. No criteria may be changed after evaluation.

Automated checks must cover malformed/conflicting messages, invalid linked replies,
failed models, single-writer locking, post-halt-only inspection, idle behavior,
read-only probes, partial unpublished inbox/checkpoint writes, and failures both
before and after the checkpoint replacement. Local filesystems are assumed;
power-loss durability and hostile host access are not guaranteed.

Run a separate actual cached local-SLM smoke after mechanical evaluation. Require
validated completion of three roles per input, messages through the outbox, and
reuse of the same model-server process across two cycles. No exact wording or
learning outcome is required from the model. Preserve failure results separately.
