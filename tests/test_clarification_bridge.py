"""Unit tests for Closed-Loop Supervised Clarification Bridge Engine.

Verifies:
1. Automated discovery of open clarification requests in runtime outbox.
2. Independent validation gate checks (Rule D003) admitting valid evidence and blocking invalid proposals.
3. Closed-loop state advancement: question marked answered, judgment score updated.
4. Immunity to model hallucinations: rejected proposals never mutate runtime state.
5. Matched ordinary-memory baseline parity (Rule D004).
6. Invariance of canonical 40 founding nodes in birth.py (Rule D001).
"""
import json
import pytest
from lmft_lab.birth import _inventory
from lmft_lab.judgment import probe, newborn, SAMPLES
from lmft_lab.runtime import advance, initial_state, software_manifest, FixtureModels
from lmft_lab.clarification_bridge import (
    scan_open_questions,
    default_evidence_validator,
    LocalClarificationProposer,
    format_teacher_reply,
    execute_bridge_cycle,
    OrdinaryMemoryClarificationComparator,
)
from lmft_lab.runtime_store import digest


def make_test_state():
    return initial_state("test-indiv", True, software_manifest(None, "fixture"))


def trigger_clarification(state):
    """Submits an initial observation without evidence, prompting a clarification request."""
    item = {
        "schema_version": 1,
        "id": "obs-trigger-1",
        "sender": "operator",
        "source": "authored-fixture",
        "type": "observation",
        "content": {"text": "Evaluate the channel measurement."},
    }
    queued = (state["cursor"] + 1, item, None, json.dumps(item))
    return advance(state, queued, FixtureModels())


def test_open_question_scanning_and_resolution():
    """Verifies that an open question is scanned and cleanly resolved by the bridge."""
    state = trigger_clarification(make_test_state())
    open_q = scan_open_questions(state)
    assert len(open_q) == 1
    assert open_q[0]["issue"] == "missing-evidence"
    
    proposer = LocalClarificationProposer()
    advanced_state, logs = execute_bridge_cycle(state, proposer)
    
    assert len(logs) == 1
    assert logs[0]["status"] == "committed"
    assert logs[0]["sample_id"] == "sample-a"
    
    # Verify question is now marked answered
    q_id = open_q[0]["question_id"]
    assert advanced_state["questions"][q_id]["answered_by"] == logs[0]["reply_id"]
    
    # Verify judgment revised to support
    assert advanced_state["judgment"]["score"] == 1/3
    assert probe(advanced_state["judgment"])["decision"] == "support"
    
    # Verify no open questions remain
    remaining = scan_open_questions(advanced_state)
    assert len(remaining) == 0


def test_validation_gate_rejects_hallucinations():
    """Verifies that invalid proposals are rejected by the gate and do not mutate state (Rule D003)."""
    state = trigger_clarification(make_test_state())
    
    # Proposer that proposes an invented, non-fixture sample
    fake_pool = {"invented-sample": (3, 4)}
    bad_proposer = LocalClarificationProposer(sample_pool=fake_pool)
    
    advanced_state, logs = execute_bridge_cycle(state, bad_proposer)
    assert len(logs) == 1
    assert logs[0]["status"] == "rejected_by_gate"
    
    # State remains unmutated
    assert advanced_state["cursor"] == state["cursor"]
    assert advanced_state["judgment"]["score"] == 0
    assert len(scan_open_questions(advanced_state)) == 1


def test_ordinary_memory_baseline_parity():
    """Verifies byte-for-byte evaluation parity with the matched ordinary-memory comparator (Rule D004)."""
    init_state = trigger_clarification(make_test_state())
    comparator = OrdinaryMemoryClarificationComparator(init_state)
    proposer = LocalClarificationProposer()
    
    p_state, p_logs = execute_bridge_cycle(init_state, proposer)
    c_state, c_logs = comparator.step(proposer)
    
    assert digest(p_state) == digest(c_state)
    assert digest(p_logs) == digest(c_logs)


def test_frozen_seed_invariant_preserved():
    """Verifies that the canonical 40 founding nodes in birth.py remain strictly invariant (Rule D001)."""
    inventory = list(_inventory())
    assert len(inventory) == 40
    domains = {item[2] for item in inventory}
    assert domains == {"cultural", "philosophical", "experiential", "psychological"}
