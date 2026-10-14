# Closed-Loop Supervised Clarification Bridge Protocol (Phase 4)

## 1. Research Question & Purpose
Can the runtime outbox clarification request mechanism be bridged directly to local model candidate proposals and deterministic validation gates to autonomously resolve epistemic ambiguity and missing evidence without human supervisory latency, while preserving the non-authoritative boundary (Rule D003) and frozen seed geometry (Rule D001)?

## 2. Invariants & Guardrails
- **Rule D001 (Frozen Founding Seed):** The canonical 40 founding nodes in `birth.py` must remain completely invariant.
- **Rule D003 (Model Proposals Require Independent Acceptance):** Model outputs are treated strictly as candidate proposals. Evidence is validated against frozen ground truth before constructing a `teacher_reply`. Invalid or hallucinated proposals must fail at the gate and never mutate state.
- **Rule D004 (Matched Ordinary-Memory Baseline):** Evaluate against a matched structured-memory comparator; require byte-for-byte state parity.
- **Envelope & Schema Integrity:** All emitted replies must follow JSON schema version 1 and explicitly link to open question IDs (`reply_to`).

## 3. Interaction Protocol & Benchmark Sequence
1. **Cycle 1 (Missing Evidence):** Submit observation without evidence $\rightarrow$ runtime emits `clarification_request` (`issue: "missing-evidence"`).
2. **Bridge Execution 1:** Bridge scans outbox, drafts candidate proposal for `sample-a`, passes validation gate, constructs and submits `teacher_reply`. Runtime closes question (`answered_by`) and updates score ($0 \rightarrow 1/3$, `support`).
3. **Cycle 2 (Conflicting Evidence):** Submit contradictory measurement (`sample-b`) $\rightarrow$ runtime detects conflict and emits `clarification_request` (`issue: "conflicting-evidence"`).
4. **Bridge Execution 2:** Bridge scans outbox, drafts third eligible sample (`sample-c`), validates, and submits reply. Runtime resolves conflict and updates score ($0 \rightarrow 0.2$, `support`).

## 4. Evaluation Criteria
- 100% resolution of open clarification requests.
- Complete rejection of hallucinated or out-of-table samples at the validation gate.
- Zero runtime LLM calls during unassisted test execution.
- Exact byte-for-byte state parity against the ordinary memory comparator.
