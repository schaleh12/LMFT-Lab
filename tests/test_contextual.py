"""Authored-feature learning, clarification and identity; no live model calls."""
from copy import deepcopy
import json
from types import SimpleNamespace

import pytest

from lmft_lab import contextual as c
from lmft_lab.context_wording import formulate
from lmft_lab.runtime import advance, initial_state, software_manifest
from lmft_lab.runtime_store import Store, digest


def message(identifier, operation, record, reply=None):
    result = {"schema_version": 1, "id": identifier, "source": "registered-fixture", "sender": "teacher",
              "type": "teacher_reply" if reply else "observation",
              "content": {"text": "Recorded fixture information.", "operation": operation, "record": record}}
    if reply: result["reply_to"] = reply
    return result


def state(mode="context-lmft"):
    return initial_state("context", True, software_manifest(None, "fixture"), mode)


def step(current, item):
    return advance(current, (current["cursor"]+1, item, None, json.dumps(item)), None)


def trained(mode="context-lmft"):
    current = state(mode)
    for identifier in list(c.TRIALS)[:8]:
        current = step(current, message(identifier, "outcome", c.outcome(identifier)))
    return current


def test_authored_feature_improves_coverage_without_fuzzy_advantage():
    predictions = []
    for mode in c.MODES:
        current = trained(mode)
        probes = [c.probe(current["judgment"], c.case(f"h{i}")) for i in range(1,7)]
        predictions.append(probes)
        if mode != "context-aggregate":
            assert [v["score"] for v in probes] == [1/3]*3 + [-1/3]*3
            assert [v["decision"] for v in probes] == ["success"]*3 + ["failure"]*3
        else:
            assert all(v["decision"] == "abstain" for v in probes)
        assert current["birth"] == state()["birth"]
    assert predictions[0] == predictions[1]


def test_missing_and_malformed_clarification_remain_pending():
    current = step(trained(), message("missing", "evaluate", c.case("m1", True)))
    question = current["outbox"][-1]["id"]
    assert current["outbox"][-1]["type"] == "clarification_request"
    for identifier, value in [("m2", False), ("m1", "true"), ("m1", False)]:
        current = step(current, message("bad-"+str(value), "condition",
            {"evidence_id": "condition/"+identifier, "case_id": identifier, "shielded": value}, question))
        assert current["questions"][question]["answered_by"] is None
    before = len(current["outbox"])
    current = step(current, message("repeat-question", "evaluate", c.case("m1", True)))
    assert len(current["outbox"]) == before
    current = step(current, message("answer", "condition",
        {"evidence_id": "condition/m1", "case_id": "m1", "shielded": True}, question))
    assert current["questions"][question]["answered_by"] == "answer"
    assert current["outbox"][-1]["content"]["evaluation"]["decision"] == "success"
    assert len(current["judgment"]["evidence"]) == 8


def test_duplicate_identity_not_text_and_conflicting_reuse():
    current = state()
    first = message("delivery-1", "outcome", c.outcome("s1"))
    current = step(current, first)
    current = step(current, message("delivery-2", "outcome", c.outcome("s2")))
    assert len(current["judgment"]["evidence"]) == 2  # same text, different event
    before = deepcopy(current["judgment"])
    for i in range(5): current = step(current, message(f"copy-{i}", "outcome", c.outcome("s1")))
    assert current["judgment"] == before and current["diagnostics"] == []
    assert "message" not in current["receipts"][-1]
    changed = c.outcome("s1"); changed["shielded"] = 1
    current = step(current, message("conflict", "outcome", changed))
    assert current["receipts"][-1]["reason"] == "conflicting reuse of evidence ID"
    assert current["judgment"]["evidence"]["s1"]["record"]["shielded"] is True


def test_cache_invalidates_on_contrary_evidence_and_probe_is_read_only():
    current = trained()
    current = step(current, message("query", "evaluate", c.case("h1")))
    current = step(current, message("query-again", "evaluate", c.case("h1")))
    assert current["receipts"][-1]["status"] == "evaluation_cache_hit"
    for identifier, expected in zip(("c1","c2","c3","c4"), (1/7,0,-1/9,-1/5)):
        current = step(current, message(identifier, "outcome", c.outcome(identifier)))
        assert current["judgment"]["branches"]["shielded"]["score"] == expected
    current = step(current, message("after", "evaluate", c.case("h1")))
    assert current["receipts"][-1]["status"] == "evaluated"
    assert current["outbox"][-1]["content"]["evaluation"]["decision"] == "failure"
    before = digest(current)
    assert c.probe(current["judgment"], c.case("x1"))["decision"] == "out_of_scope"
    assert c.probe(current["judgment"], c.case("x2"))["decision"] == "out_of_scope"
    assert digest(current) == before


@pytest.mark.parametrize("point", ["before_replace", "after_replace"])
def test_pending_request_and_reply_recover_atomically(tmp_path, point):
    store = Store(tmp_path)
    original = step(trained(), message("missing", "evaluate", c.case("m1", True)))
    store.commit(original)
    question = original["outbox"][-1]["id"]
    item = message("answer", "condition", {"evidence_id":"condition/m1", "case_id":"m1", "shielded":True}, question)
    store.submit(item)
    # Queue sequence must follow already committed receipts in this unit fixture.
    queued = (original["cursor"]+1, item, None, json.dumps(item))
    changed = advance(original, queued, None)
    def interrupt(stage):
        if point == stage: raise OSError("injected interruption")
    with pytest.raises(OSError): store.commit(changed, interrupt)
    recovered = store.read()
    if recovered["cursor"] == original["cursor"]: store.commit(advance(recovered, queued, None))
    assert store.read()["judgment"] == changed["judgment"]
    assert store.read()["questions"][question]["answered_by"] == "answer"
    assert len(store.receive()) == len(changed["outbox"])


def test_wrong_mode_and_control_cannot_teach():
    current = state();current["learning"] = False
    current = step(current, message("s1", "outcome", c.outcome("s1")))
    assert not current["judgment"]["evidence"]
    assert current["receipts"][-1]["reason"] == "learning disabled control"


@pytest.mark.parametrize("invalid", [True,False])
def test_constrained_wording_validates_actual_response_and_falls_back(invalid):
    class Models:
        config={"roles":{"contemplation":"test"},"models":{"test":{"repo_id":"mock"}},
                "generation":{"temperature":0,"seed":42,"max_tokens":1024,"timeout_seconds":10}}
        offline=True
        process=SimpleNamespace(pid=123)
        def _start(self, name): pass
        def close(self): pass
        def _request(self, endpoint, request, timeout):
            allowed=request["response_format"]["schema"]["properties"]["text"]["enum"]
            return {"choices":[{"finish_reason":"stop","message":{"content":json.dumps({"text":"I guarantee success" if invalid else allowed[1]})}}]}
    result=c.probe(trained()["judgment"], c.case("h1"))
    text, trace=formulate(Models(),result)
    assert "guarantee success" not in text
    assert trace["status"] == ("rejected" if invalid else "validated")
    assert "Limited synthetic evidence" in text
