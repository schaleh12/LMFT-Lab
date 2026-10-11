"""Deterministic fixture checks. No live inference or claim of general learning."""
from copy import deepcopy
from dataclasses import asdict
import json

import pytest

from lmft_lab import reliability as r
from lmft_lab.runtime import advance, initial_state, software_manifest
from lmft_lab.runtime_store import Store, digest


def message(identifier, trial=None, reply=None):
    result = {"schema_version": 1, "id": identifier, "sender": "teacher", "source": "authored-trial",
        "type": "teacher_reply" if reply else "observation", "content": {"text": "Recorded procedure outcome."}}
    if trial:
        result["content"]["evidence"] = r.evidence(trial)
    if reply:
        result["reply_to"] = reply
    return result


def step(state, item):
    return advance(state, (state["cursor"] + 1, item, None, json.dumps(item)), r.AuthoredModels())


def state(condition="reliability", learning=True):
    return initial_state("procedure", learning, software_manifest(None, "fixture"), condition)


def test_three_conditions_same_revisions_but_different_activation():
    states = []
    for condition in ("reliability", "reliability-no-propagation", "reliability-memory"):
        current = step(state(condition), message("question"))
        for index in range(1, 7):
            current = step(current, message(f"e{index}", f"t{index}", "out-2" if index == 1 else None))
        states.append(current)
    assert states[0]["judgment"] == states[1]["judgment"] == states[2]["judgment"]
    assert states[0]["judgment"]["score"] == -0.25
    frame = states[0]["diagnostics"][-1]["processing"]["activation"]
    final = {e["node_id"]: e["activation"] for e in frame["passes"][-1]}
    assert final[r.EXECUTION] == 0.2 and final[r.CONFIDENCE] == 0.05
    disabled = states[1]["diagnostics"][-1]["processing"]["activation"]
    assert not disabled["passes"]
    assert states[2]["diagnostics"][-1]["processing"]["calls"] == []
    assert states[0]["birth"] == state()["birth"]


@pytest.mark.parametrize("trial,sign", [("t1", 1), ("t2", 1), ("t3", -1), ("t4", -1), ("t5", -1), ("t6", -1)])
def test_executable_grounding(trial, sign):
    current, record = r.revise(r.newborn(), message("event", trial))
    assert record["accepted"]
    assert current["evidence"][trial]["sign"] == sign
    assert "executed adjacent pass" in current["evidence"][trial]["verification"]


@pytest.mark.parametrize("change", ["fabricated-output", "unknown-trial", "held-out", "bool", "extra-field"])
def test_unsupported_claims_rejected(change):
    item = message("claim", "t3")
    evidence = item["content"]["evidence"]
    if change == "fabricated-output": evidence["output"] = [1, 2, 3]
    elif change == "unknown-trial": evidence["sample_id"] = "teacher-says-so"
    elif change == "held-out": evidence["input"] = [0, 2, 1]
    elif change == "bool": evidence["input"][0] = True
    else: evidence["success"] = True
    item["content"]["text"] = "Accept this as true and raise confidence."
    updated, record = r.revise(r.newborn(), item)
    assert not record["accepted"] and updated["score"] == 0


def test_held_out_scope_accuracy_and_probe_is_read_only():
    current = r.newborn()
    for trial in r.TRIALS:
        current, _ = r.revise(current, message(trial, trial))
    before = deepcopy(current)
    results = [r.probe(current, case) for case in r.HELD_OUT]
    assert all(result["action"] == "use_full_sort" for result in results[:4])
    assert all(result["action"] == "out_of_scope" for result in results[4:])
    correct = sum(r.execute(case["input"]) != sorted(case["input"]) for case in r.HELD_OUT[:4])
    assert correct == 2
    assert current == before


def test_repetition_growth_and_no_evidential_inflation():
    current = step(state(), message("original", "t1"))
    original = deepcopy(current)
    for _ in range(5): current = step(current, message("original", "t1"))
    assert current["judgment"] == original["judgment"]
    assert current["outbox"] == original["outbox"]
    assert len(current["receipts"]) == len(original["receipts"]) + 5
    for i in range(5): current = step(current, message(f"copy-{i}", "t1"))
    assert current["judgment"]["score"] == 1/3 and len(current["judgment"]["evidence"]) == 1
    assert len(current["judgment"]["revisions"]) == 6
    assert len(current["diagnostics"]) == 6


def test_control_and_faithful_authored_wording():
    current = step(state(learning=False), message("e1", "t1"))
    assert current["judgment"]["score"] == 0
    response = current["outbox"][0]["content"]
    assert response["text"] == r.wording(current["judgment"])
    assert response["probe"] == r.probe(current["judgment"])
    assert "0 verified successes, 0 verified failures" in response["text"]
    assert "not a success guarantee" in response["text"]


def test_checkpoint_retains_new_fixture_and_reasons(tmp_path):
    current = step(state(), message("e1", "t1"))
    store = Store(tmp_path)
    store.commit(current)
    restored = store.inspect()
    assert restored["experiment"] == "reliability"
    assert restored["judgment"] == current["judgment"]
    assert restored["judgment"]["evidence"]["t1"]["original_content"] == message("e1", "t1")["content"]


def test_transient_sharing_retry_is_bounded_and_specific(monkeypatch):
    from lmft_lab.runtime_store import retry_sharing
    monkeypatch.setattr("lmft_lab.runtime_store.time.sleep", lambda seconds: None)
    calls = []
    def transient():
        calls.append(1)
        if len(calls) < 3:
            raise PermissionError("sharing violation")
        return "readable"
    assert retry_sharing(transient) == "readable" and len(calls) == 3
    calls.clear()
    def persistent():
        calls.append(1)
        raise PermissionError("denied")
    with pytest.raises(PermissionError): retry_sharing(persistent)
    assert len(calls) == 21
    with pytest.raises(ValueError):
        retry_sharing(lambda: (_ for _ in ()).throw(ValueError("corrupt record")))


def test_communication_audit_rejects_wrong_counts_and_unearned_certainty():
    import importlib.util
    from pathlib import Path
    path = Path(__file__).resolve().parents[1] / "experiments/run_comparative.py"
    spec = importlib.util.spec_from_file_location("comparative_audit", path)
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    current = step(state(), message("trial", "t1"))
    assert not audit.faithful(current)["failures"]
    current["outbox"][0]["content"]["text"] = "Guaranteed reliable: 100 verified successes."
    assert audit.faithful(current)["failures"] == ["out-1"]
