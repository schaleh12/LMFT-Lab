"""Outcome repair invariants and historical equation reuse."""
from copy import deepcopy
from fractions import Fraction
import json
import pytest
from lmft_lab import outcome_correction as c, outcome_fixture as f
from lmft_lab.runtime import initial_state, software_manifest, advance
from lmft_lab.runtime_store import Store, digest


def message(identifier, op, record, sender=f.AUTHORITY):
    return {"schema_version": 1, "id": identifier, "sender": sender, "source": f.SOURCE, "type": "observation",
            "content": {"text": "Attributed instrument report or proposed correction.", "operation": op, "record": record}}


def step(state, m):
    return advance(state, (state["cursor"]+1, m, None, json.dumps(m)), None)


def prepared(key, mode="outcome-lmft"):
    state = initial_state("outcome", True, software_manifest(None, "fixture"), mode)
    for i, record in enumerate(f.initial_records(key)):
        state = step(state, message("initial-"+str(i), "evidence", record))
    for variant in ("warm", "other"):
        state = step(state, message("before-"+variant, "evaluate", f.public_case(key, variant)))
    return state


def repaired(state, key):
    for i, record in enumerate(f.corrections(key)):
        state = step(state, message("correction-"+str(i), "correction", record))
    return state


@pytest.mark.parametrize("mode", c.MODES)
@pytest.mark.parametrize("key,accepted,score", [("o1",1,-1/3),("o2",1,1/3),("o3",1,1/3),("o4",1,0),
    ("o5",0,-1/3),("o6",0,-1/3),("o7",0,-1/3),("o8",1,1/3),("o9",1,1/3),("o10",1,1/3),("o11",2,1/3),("o12",1,.5)])
def test_projection_originals_counts_and_exact_arithmetic(mode,key,accepted,score):
    before = prepared(key,mode); state = repaired(before,key); current = state["judgment"]
    disabled = mode == "outcome-disabled"
    assert sum(e["accepted"] for e in current["corrections"]) == (0 if disabled else accepted)
    assert current["branches"]["shielded"]["score"] == (before["judgment"]["branches"]["shielded"]["score"] if disabled else score)
    assert current["branches"]["unshielded"] == before["judgment"]["branches"]["unshielded"]
    assert current["cache"][key+"-other"] == before["judgment"]["cache"][key+"-other"]
    assert all(current["ledger"][k] == v for k,v in before["judgment"]["ledger"].items())
    assert len(current["heads"]) == len(before["judgment"]["heads"])
    assert len(current["ledger"]) == len(current["heads"])+(0 if disabled else accepted)
    for name, branch in current["branches"].items():
        samples = list(c.effective_samples(current,name).values())
        signs = [1 if e["record"]["output"] == e["record"]["payload"] else -1 for e in samples]
        assert branch["score"] == float(Fraction(sum(signs),len(signs)+2))
        assert len(branch["evidence"]) == len(samples)
    assert current["weights"] == dict(A=.25,B=.75,D=.5)
    assert state["birth"] == before["birth"]
    for event in current["corrections"]:
        if not event["accepted"]:
            assert event["before"] == event["after"]
            assert event["cache_invalidated"] == event["closed_questions"] == []


@pytest.mark.parametrize("key", ["o5","o6","o7"])
def test_independent_gates_and_rejection_invariance(key,monkeypatch):
    state=prepared(key);before=deepcopy(state)
    if key != "o6":
        monkeypatch.setattr(f,"replacement_valid",lambda *a:pytest.fail("verification before authorization/eligibility"))
    state=repaired(state,key)
    assert c.state_ref(state["judgment"]) == c.state_ref(before["judgment"])
    assert state["questions"] == before["questions"]
    assert state["judgment"]["cache"] == before["judgment"]["cache"]
    assert state["judgment"]["recomputations"] == before["judgment"]["recomputations"]
    for event in state["judgment"]["corrections"]:
        assert event["authorization"]["passed"] == (key != "o5")
        assert event["verification"]["checked"] == (key == "o6")


def test_duplicates_do_not_learn_or_restore_old_head():
    state=repaired(prepared("o8"),"o8");before=deepcopy(state["judgment"])
    for i in range(5):
        state=step(state,message("correction-0","correction",f.corrections("o8")[0]))
        state=step(state,message("new-"+str(i),"correction",f.corrections("o8")[0]))
        state=step(state,message("old-"+str(i),"evidence",f.initial_records("o8")[0]))
    assert state["judgment"] == before


def test_stale_and_chain():
    state=repaired(prepared("o10"),"o10")
    reasons=[e["reason"] for e in state["judgment"]["corrections"]]
    assert reasons[1].startswith("stale target:") and reasons[2]=="stale target digest"
    current=repaired(prepared("o11"),"o11")["judgment"]
    assert current["heads"]["o11/event-1"] == "replacement/o11-b"
    assert current["ledger"]["replacement/o11-b"]["parent"] == "replacement/o11-a"
    assert current["ledger"]["replacement/o11-a"]["parent"] == "o11/event-1"
    assert len(current["branches"]["shielded"]["evidence"]) == 1
    assert current["corrections"][1]["before"]["branches"]["shielded"]["score"] == 1/3


def test_consistency_closure_cache_and_fresh_wording():
    state=prepared("o12");qid=state["judgment"]["cases"]["o12-warm"]["request"]
    state=repaired(state,"o12")
    assert state["questions"][qid]["status"] == "resolved_by_correction"
    assert "o12-warm" not in state["judgment"]["cache"]
    state=step(state,message("after","evaluate",f.public_case("o12")))
    assert state["receipts"][-1]["status"] == "evaluated"
    assert "success" in state["outbox"][-1]["content"]["text"]
    assert state["outbox"][-1]["content"]["result"]["score"] == .5
    assert len(state["questions"])==1
    mixed=repaired(prepared("o4"),"o4")
    assert all(q["status"]=="open" for q in mixed["questions"].values())
    assert c.snapshot(mixed["judgment"])["shielded"]["decision"]=="abstain"
    same_category=repaired(prepared("o3"),"o3")
    same_category=step(same_category,message("after","evaluate",f.public_case("o3")))
    assert same_category["outbox"][-1]["type"]=="clarification_request"
    assert same_category["outbox"][-1]["content"]["result"]["decision"]=="success"


@pytest.mark.parametrize("point", ["before_replace","after_replace"])
def test_atomic_commit_recovery(tmp_path,point):
    original=prepared("o12");store=Store(tmp_path);store.commit(original)
    m=message("repair","correction",f.corrections("o12")[0]);changed=step(original,m)
    def fault(where):
        if where==point:raise RuntimeError("simulated interruption")
    with pytest.raises(RuntimeError):store.commit(changed,fault=fault)
    recovered=store.inspect()
    assert digest(recovered) == digest(original if point=="before_replace" else changed)
    if point=="before_replace":recovered=step(recovered,m)
    assert recovered["judgment"]==changed["judgment"] and recovered["questions"]==changed["questions"]
    assert step(recovered,m)["judgment"]==changed["judgment"]


def test_no_truth_or_inference_access_during_projection(monkeypatch):
    monkeypatch.setattr(f,"actual_success",lambda *a:pytest.fail("held-out leakage"))
    monkeypatch.setattr(f,"replacement_valid",lambda *a:pytest.fail("reference queried without correction"))
    state=prepared("o2");before=digest(state)
    assert c.predict(state["judgment"],f.public_case("o2","fresh-1"))["decision"]=="failure"
    assert digest(state)==before


def test_spoofed_authority_and_global_acceptance_gate():
    state=prepared("o2");record=f.corrections("o2")[0]
    bad=step(state,message("spoof","correction",record,sender="imposter"))
    assert not bad["judgment"]["corrections"][-1]["authorization"]["passed"]
    state["learning"]=False
    disabled=step(state,message("repair","correction",record))
    assert disabled["judgment"]["corrections"][-1]["reason"]=="correction acceptance disabled"
    assert c.state_ref(disabled["judgment"])==c.state_ref(state["judgment"])


def test_structured_memory_matches_every_semantic_projection():
    for key in f.IDS:
        a=repaired(prepared(key),key);b=repaired(prepared(key,"outcome-memory"),key)
        assert c.state_ref(a["judgment"])==c.state_ref(b["judgment"])
        assert a["questions"]==b["questions"]
        assert a["judgment"]["corrections"]==b["judgment"]["corrections"]
