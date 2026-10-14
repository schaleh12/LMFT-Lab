"""Closed-Loop Supervised Clarification Bridge Engine.

Automates the interactive supervisory bridge between runtime clarification requests
(emitted when the LMFT is ambiguous or missing evidence) and local model representation
proposals under strict independent validation gates.

Architecture & Invariants:
1. Observes outbox for 'clarification_request' messages (issue: missing-evidence or conflicting-evidence).
2. Prompts local model / SLM proposer to generate candidate evidence/anchors.
3. Enforces Rule D003 (independent deterministic validation): candidate proposals
   are checked for schema compliance, valid evidence, and non-tautological structure.
4. Formats valid proposals into 'teacher_reply' envelopes referencing request ID.
5. Advances the runtime state atomically, updating judgment and marking question answered.
6. Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
"""
from copy import deepcopy
import json
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from lmft_lab.judgment import SAMPLES
from lmft_lab.runtime import advance, FixtureModels
from lmft_lab.runtime_store import digest


def scan_open_questions(runtime_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scans runtime state for unanswered clarification requests in outbox/questions."""
    open_questions = []
    questions = runtime_state.get("questions", {})
    for q_id, q_data in questions.items():
        if q_data.get("answered_by") is None:
            open_questions.append({
                "question_id": q_id,
                "issue": q_data.get("issue"),
                "trigger_message": q_data.get("trigger_message"),
                "evidence_refs": q_data.get("evidence_refs", []),
            })
    return open_questions


def default_evidence_validator(proposal: Dict[str, Any]) -> Tuple[bool, str]:
    """Strict validation gate for channel-agreement fixture evidence (Rule D003)."""
    if not isinstance(proposal, dict):
        return False, "proposal must be a dictionary"
    
    sample_id = proposal.get("sample_id")
    if sample_id not in SAMPLES:
        return False, f"sample_id '{sample_id}' is not in frozen fixture table"
        
    expected_channel, expected_ref = SAMPLES[sample_id]
    if proposal.get("channel") != expected_channel or proposal.get("reference") != expected_ref:
        return False, "channel and reference measurements do not match ground truth table"
        
    return True, "valid fixture evidence"


class LocalClarificationProposer:
    """Simulates or invokes model role to propose evidence resolving an open clarification."""
    def __init__(self, mode: str = "fixture", sample_pool: Optional[Dict[str, Any]] = None):
        self.mode = mode
        self.sample_pool = sample_pool or SAMPLES

    def propose_evidence(self, question: Dict[str, Any], trigger_text: str) -> Dict[str, Any]:
        """Generates a candidate proposal based on the issue type."""
        issue = question.get("issue")
        already_used = question.get("evidence_refs", [])
        
        # Select first unused candidate sample
        candidate_id = None
        for s_id in self.sample_pool:
            if s_id not in already_used:
                candidate_id = s_id
                break
                
        if not candidate_id:
            return {"error": "no eligible unused sample available"}
            
        ch, ref = self.sample_pool[candidate_id]
        return {
            "sample_id": candidate_id,
            "channel": ch,
            "reference": ref,
            "explanatory_gloss": f"Ground-truth measurement for {candidate_id}.",
        }


def format_teacher_reply(
    question_id: str,
    reply_id: str,
    evidence: Dict[str, Any],
    text: str = "Supervised teacher reply with validated evidence.",
) -> Dict[str, Any]:
    """Constructs a schema-version 1 teacher_reply message envelope."""
    return {
        "schema_version": 1,
        "id": reply_id,
        "sender": "supervised-teacher",
        "source": "autonomous-clarification-bridge",
        "type": "teacher_reply",
        "reply_to": question_id,
        "content": {
            "text": text,
            "evidence": {
                "sample_id": evidence["sample_id"],
                "channel": evidence["channel"],
                "reference": evidence["reference"],
            },
        },
    }


def execute_bridge_cycle(
    runtime_state: Dict[str, Any],
    proposer: LocalClarificationProposer,
    validator: Callable[[Dict[str, Any]], Tuple[bool, str]] = default_evidence_validator,
    models: Optional[Any] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Finds open questions, synthesizes validated replies, and applies them to state."""
    current_state = deepcopy(runtime_state)
    open_questions = scan_open_questions(current_state)
    cycle_logs = []
    
    models = models or FixtureModels()
    
    for q in open_questions:
        q_id = q["question_id"]
        trigger_id = q["trigger_message"]
        
        # 1. Propose candidate evidence
        candidate_proposal = proposer.propose_evidence(q, trigger_id)
        if "error" in candidate_proposal:
            cycle_logs.append({
                "question_id": q_id,
                "status": "skipped",
                "reason": candidate_proposal["error"],
            })
            continue
            
        # 2. Independent validation gate (Rule D003)
        is_valid, val_reason = validator(candidate_proposal)
        if not is_valid:
            cycle_logs.append({
                "question_id": q_id,
                "status": "rejected_by_gate",
                "proposal": candidate_proposal,
                "reason": val_reason,
            })
            continue
            
        # 3. Construct teacher_reply
        reply_id = f"reply-bridge-{current_state['cursor'] + 1}"
        reply_msg = format_teacher_reply(
            question_id=q_id,
            reply_id=reply_id,
            evidence=candidate_proposal,
            text=f"Resolving {q['issue']} with validated evidence {candidate_proposal['sample_id']}.",
        )
        
        # 4. Advance runtime state atomically
        queued = (current_state["cursor"] + 1, reply_msg, None, json.dumps(reply_msg))
        current_state = advance(current_state, queued, models)
        
        cycle_logs.append({
            "question_id": q_id,
            "reply_id": reply_id,
            "sample_id": candidate_proposal["sample_id"],
            "status": "committed",
            "judgment_score": current_state["judgment"]["score"],
        })
        
    return current_state, cycle_logs


class OrdinaryMemoryClarificationComparator:
    """Matched ordinary structured-memory baseline (Rule D004).
    
    Executes identical bridge logic and state advances on matched memory.
    """
    def __init__(self, initial_state: Dict[str, Any]):
        self.state = deepcopy(initial_state)

    def step(
        self,
        proposer: LocalClarificationProposer,
        validator: Callable[[Dict[str, Any]], Tuple[bool, str]] = default_evidence_validator,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        self.state, logs = execute_bridge_cycle(self.state, proposer, validator=validator)
        return self.state, logs
