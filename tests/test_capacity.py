"""Finite relationship induction, validation boundaries and historical-rule reuse."""
from copy import deepcopy
import json
import pytest
from lmft_lab import capacity as c, capacity_fixture as f, capacity_relations as r
from lmft_lab.runtime import initial_state, software_manifest, advance
from lmft_lab.runtime_store import Store,digest


def message(mid,op,record):
    return {"schema_version":1,"id":mid,"sender":"fixture-operator","source":f.SOURCE,"type":"observation",
            "content":{"text":"Registered capacity evidence or bounded control.","operation":op,"record":deepcopy(record)}}


def step(state,m):return advance(state,(state["cursor"]+1,m,None,json.dumps(m)),None)


def prepared(mode="capacity-lmft",accepted=True):
    state=initial_state("capacity",True,software_manifest(None,"fixture"),mode)
    for eid in f.TRAIN:state=step(state,message(eid,"outcome",f.outcome(eid,"train")))
    state=step(state,message("select","select",{}))
    for eid in f.VALIDATION:state=step(state,message(eid,"outcome",f.outcome(eid,"validation")))
    if accepted:state=step(state,message("accept","accept",{}))
    return state


@pytest.mark.parametrize("mode",c.MODES)
def test_prediction_conditions_and_unchanged_counter(mode):
    state=prepared(mode);current=state["judgment"]
    assert current["coarse"]["score"]==0 and len(current["coarse"]["evidence"])==6
    assert len(current["evidence"]["validation"])==4
    for eid in f.HELD:
        result=c.predict(current,f.case(eid))
        if eid=="x1":assert result["decision"]=="out_of_scope";continue
        if mode=="capacity-aggregate" or mode=="capacity-lookup" and eid not in f.SEEN:
            assert result["decision"]=="abstain"
        else:assert (result["decision"]=="success")==f.execute(*f.HELD[eid])
    if mode in c.LEARNERS:
        assert current["selection"]["selected"]["op"]=="le"
        assert len(current["selection"]["consistent"])==1
        assert current["accepted_relationship"]["validation"]["accepted"]
    else:assert current["accepted_relationship"] is None


@pytest.mark.parametrize("bad",[{}, {"code":"print(1)"}, {"version":r.VERSION,"left":"length","op":"__import__","right":"capacity"},
    {"version":r.VERSION,"left":"capacity","op":"le","right":"length"},
    {"version":r.VERSION,"left":"length","op":[],"right":"capacity"}])
def test_malformed_relationships_never_execute(bad):
    assert not r.valid(bad)
    with pytest.raises(ValueError):r.evaluate(bad,f.case("h1"))
    state=prepared();before=deepcopy(state["judgment"]["accepted_relationship"])
    state=step(state,message("bad","proposal",bad))
    assert state["receipts"][-1]["status"]=="rejected"
    assert state["judgment"]["accepted_relationship"]==before


@pytest.mark.parametrize("update",[{"length":True},{"length":-1},{"length":9},{"capacity":None},{"procedure":"other"},{"fits":True}])
def test_scope_limits(update):
    case={**f.case("h1"),**update};state=prepared()
    assert c.predict(state["judgment"],case)["decision"]=="out_of_scope"
    with pytest.raises(ValueError):r.evaluate(r.candidates()[1],case)


def test_ambiguous_training_is_not_disambiguated_with_validation():
    train={eid:f.outcome(eid,"train") for eid in ("t1","t2","t4","t5")}
    selected=r.select(train)
    assert [x["op"] for x in selected["consistent"]]==["lt","le"]
    assert selected["selected"] is None
    validation=r.validate(selected,{eid:f.outcome(eid,"validation") for eid in f.VALIDATION})
    assert not validation["accepted"] and validation["checks"]==[]


def test_failed_validation_does_not_fallback():
    selection=r.select({eid:f.outcome(eid,"train") for eid in f.TRAIN})
    validation={eid:f.outcome(eid,"validation") for eid in f.VALIDATION}
    validation["v1"]["success"]=False
    result=r.validate(selection,validation)
    assert not result["accepted"]
    assert selection["selected"]["op"]=="le"
    assert sum(c["predicted"]!=c["observed"] for c in result["checks"])==1


def test_verifier_is_inaccessible_during_selection_validation_and_prediction(monkeypatch):
    state=prepared(accepted=False)
    monkeypatch.setattr(f,"execute",lambda *a:pytest.fail("hidden procedure accessed"))
    monkeypatch.setattr(f,"verify",lambda *a:pytest.fail("verifier accessed outside admission"))
    selected=r.select(c.records(state["judgment"],"train"))
    assert selected==state["judgment"]["selection"]
    before=digest(state)
    assert c.predict(state["judgment"],f.case("h1"))["decision"]=="abstain"
    assert digest(state)==before
    state=step(state,message("accept","accept",{}))
    prior=digest(state)
    assert c.predict(state["judgment"],f.case("h1"))["decision"]=="success"
    assert digest(state)==prior


def test_training_heldout_split_gate_precedes_execution(monkeypatch):
    state=prepared();before=deepcopy(state["judgment"]["accepted_relationship"])
    monkeypatch.setattr(f,"execute",lambda *a:pytest.fail("held-out execution during admission"))
    for split in ("heldout","train","validation"):
        record={"evidence_id":"h1","split":split,"procedure":f.PROCEDURE,"length":1,"capacity":4,"success":True}
        state=step(state,message("leak-"+split,"outcome",record))
        assert state["receipts"][-1]["status"]=="rejected"
        assert not f.verify(record)
    assert state["judgment"]["accepted_relationship"]==before


def test_duplicate_and_conflicting_evidence_and_proposals():
    state=prepared();before=deepcopy(state["judgment"])
    state=step(state,message("t1","outcome",f.outcome("t1","train")))
    assert state["receipts"][-1]["status"]=="duplicate"
    state=step(state,message("copy","outcome",f.outcome("t1","train")))
    assert state["judgment"]==before
    changed=f.outcome("t1","train");changed["success"]=False
    state=step(state,message("conflict","outcome",changed))
    assert state["receipts"][-1]["reason"]=="conflicting evidence identity"
    state=step(state,message("external","proposal",r.candidates()[1]))
    assert state["receipts"][-1]["status"]=="rejected"
    assert state["judgment"]["accepted_relationship"]==before["accepted_relationship"]


def test_validation_never_changes_training_candidates_or_counter():
    state=prepared(accepted=False);selection=deepcopy(state["judgment"]["selection"]);counter=deepcopy(state["judgment"]["coarse"])
    state=step(state,message("accept","accept",{}))
    assert state["judgment"]["selection"]==selection and state["judgment"]["coarse"]==counter
    state=step(state,message("again","select",{}))
    assert state["receipts"][-1]["status"]=="rejected"


def test_memory_gets_identical_induction_access():
    a=prepared()["judgment"];b=prepared("capacity-memory")["judgment"]
    assert a["selection"]==b["selection"] and a["accepted_relationship"]==b["accepted_relationship"]


def test_bad_source_and_premature_acceptance():
    state=initial_state("capacity",True,software_manifest(None,"fixture"),"capacity-lmft")
    m=message("spoof","outcome",f.outcome("t1","train"));m["source"]="untrusted"
    state=step(state,m);assert not state["judgment"]["evidence"]["train"]
    state=step(state,message("early","accept",{}));assert state["receipts"][-1]["status"]=="rejected"
    assert state["judgment"]["accepted_relationship"] is None


@pytest.mark.parametrize("point",["before_replace","after_replace"])
def test_atomic_relationship_acceptance(tmp_path,point):
    state=prepared(accepted=False);store=Store(tmp_path);store.commit(state)
    m=message("accept","accept",{});changed=step(state,m)
    def fault(where):
        if where==point:raise RuntimeError("interrupted")
    with pytest.raises(RuntimeError):store.commit(changed,fault=fault)
    restored=store.inspect();assert digest(restored)==digest(state if point=="before_replace" else changed)
    if point=="before_replace":restored=step(restored,m)
    assert restored["judgment"]==changed["judgment"]
    assert step(restored,m)["judgment"]==changed["judgment"]
