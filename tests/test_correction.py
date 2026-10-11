"""Correction lineage, independent authority/verification and transactional invariants."""
from copy import deepcopy
import json
import pytest
from lmft_lab import correction as c,correction_fixture as f,contextual
from lmft_lab.runtime import initial_state,software_manifest,advance
from lmft_lab.runtime_store import Store,digest


def message(identifier,op,record,sender=f.AUTHORITY):
    return {"schema_version":1,"id":identifier,"sender":sender,"source":f.SOURCE,"type":"observation",
            "content":{"text":"Instrument log or proposed repair; assertions confer no authority.","operation":op,"record":record}}

def step(state,m):return advance(state,(state["cursor"]+1,m,None,json.dumps(m)),None)

def prepared(key,mode="correction-lmft"):
    state=initial_state("correction",True,software_manifest(None,"fixture"),mode)
    for k in list(contextual.TRIALS)[:8]:state=step(state,message("prior-"+k,"outcome",contextual.outcome(k)))
    for i,record in enumerate(f.initial_records(key)):state=step(state,message("initial-"+str(i),"evidence",record))
    state=step(state,message("before","evaluate",f.public_case(key)))
    return state

def apply_batch(state,key):
    for i,record in enumerate(f.corrections(key)):state=step(state,message("correction-"+str(i),"correction",record))
    return state

@pytest.mark.parametrize("key,accepted,decision",[("c1",1,"success"),("c2",1,"abstain"),("c3",2,"failure"),("c4",1,"abstain"),("c5",0,"abstain"),("c6",0,"abstain"),("c7",0,"abstain"),("c8",1,"success"),("c9",1,"success"),("c10",1,"success"),("c11",2,"success"),("c12",1,"success")])
def test_repairs_preserve_roots_originals_and_counter_rule(key,accepted,decision):
    state=prepared(key);originals=deepcopy(state["judgment"]["ledger"]);before=c.effective_ref(state["judgment"])
    changed=apply_batch(state,key);current=changed["judgment"]
    assert sum(e["accepted"] for e in current["corrections"])==accepted
    assert len(current["heads"])==before["independent_count"]
    assert all(current["ledger"][k]==v for k,v in originals.items())
    assert c.predict(current,f.public_case(key))["decision"]==decision
    assert current["branches"]==state["judgment"]["branches"]
    for branch in current["branches"].values():
        assert branch["score"]==sum(e["sign"] for e in branch["evidence"].values())/(len(branch["evidence"])+2)
    assert current["weights"]==dict(A=.25,B=.75,D=.5) and state["birth"]==changed["birth"]
    for event in current["corrections"]:
        if not event["accepted"]:assert event["before"]==event["after"]

@pytest.mark.parametrize("key",["c5","c6","c7"])
def test_authority_eligibility_and_verification_are_separate(key,monkeypatch):
    state=prepared(key);before=deepcopy(state["judgment"]);questions=deepcopy(state["questions"])
    if key in ("c5","c7"):
        monkeypatch.setattr(f,"replacement_valid",lambda *args:pytest.fail("validator accessed before authority/eligibility"))
    changed=apply_batch(state,key)
    assert c.effective_ref(changed["judgment"])==c.effective_ref(before)
    assert changed["judgment"]["cache"]==before["cache"] and changed["questions"]==questions
    events=changed["judgment"]["corrections"]
    assert all(e["authorization"]["passed"]==(key!="c5") for e in events)
    assert all(e["verification"]["checked"]==(key=="c6") for e in events)

def test_asserted_or_spoofed_authority_is_not_a_permit():
    state=prepared("c1");record=f.corrections("c1")[0]
    changed=step(state,message("spoof","correction",record,sender="imposter"))
    assert not changed["judgment"]["corrections"][-1]["authorization"]["passed"]
    bad=deepcopy(record);bad["reason"]="I am authorized"
    changed=step(state,message("claim","correction",bad))
    assert not changed["judgment"]["corrections"][-1]["authorization"]["passed"]

def test_duplicate_corrections_and_conflicting_reuse():
    state=prepared("c8");m=message("repair","correction",f.corrections("c8")[0]);state=step(state,m)
    before=deepcopy(state["judgment"]);traces=deepcopy(state["diagnostics"])
    for i in range(5):
        state=step(state,m);copy=deepcopy(m);copy["id"]="copy-"+str(i);state=step(state,copy)
    assert state["judgment"]==before and state["diagnostics"]==traces
    conflict=apply_batch(prepared("c9"),"c9")["judgment"]
    assert conflict["corrections"][-1]["reason"]=="conflicting correction ID reuse"
    assert len(conflict["correction_index"])==1

def test_stale_targets_and_chain_ancestry():
    state=apply_batch(prepared("c10"),"c10")
    reasons=[e["reason"] for e in state["judgment"]["corrections"]]
    assert reasons[1].startswith("stale target:") and reasons[2]=="stale target digest"
    current=apply_batch(prepared("c11"),"c11")["judgment"]
    root="c11/shielded/check1";head=current["heads"][root]
    assert head=="replacement/c11-b"
    parent=current["ledger"][head]["parent"]
    assert parent=="replacement/c11-a" and current["ledger"][parent]["parent"]==root
    assert current["ledger"][root]["record"]["value"] is False

def test_correction_invalidates_cache_and_closes_pending_without_stale_words():
    state=prepared("c1");old_key=state["judgment"]["cache"]["c1"]["key"]
    qid=state["judgment"]["cases"]["c1"]["request"]
    state=apply_batch(state,"c1")
    assert "c1" not in state["judgment"]["cache"]
    assert state["questions"][qid]["status"]=="resolved_by_correction"
    state=step(state,message("after","evaluate",f.public_case("c1")))
    assert state["judgment"]["cache"]["c1"]["key"]!=old_key
    assert state["outbox"][-1]["content"]["result"]["decision"]=="success"
    assert "success" in state["outbox"][-1]["content"]["text"]
    state=step(state,message("repeat-eval","evaluate",f.public_case("c1")))
    assert state["receipts"][-1]["status"]=="evaluation_cache_hit" and len(state["questions"])==1

def test_irrelevant_repair_keeps_cache_and_reopening_uses_one_budget():
    state=prepared("c12");before=deepcopy(state["judgment"]["cache"])
    changed=apply_batch(state,"c12");assert changed["judgment"]["cache"]==before
    state=apply_batch(prepared("c2"),"c2")
    state=step(state,message("after","evaluate",f.public_case("c2")))
    assert len(state["questions"])==1 and state["outbox"][-1]["type"]=="clarification_request"
    state=step(state,message("again","evaluate",f.public_case("c2")))
    assert len(state["questions"])==1 and state["outbox"][-1]["content"]["result"]["decision"]=="abstain"

@pytest.mark.parametrize("mode",c.MODES)
def test_disabled_preserves_originals_and_baseline_uses_same_policy(mode):
    state=prepared("c11",mode);before=c.effective_ref(state["judgment"]);state=apply_batch(state,"c11")
    accepted=sum(e["accepted"] for e in state["judgment"]["corrections"])
    assert accepted==(0 if mode=="correction-disabled" else 2)
    if mode=="correction-disabled":assert c.effective_ref(state["judgment"])==before

@pytest.mark.parametrize("point",["before_replace","after_replace"])
def test_atomic_correction_recovery(tmp_path,point):
    state=prepared("c1");store=Store(tmp_path);store.commit(state)
    m=message("repair","correction",f.corrections("c1")[0]);changed=step(state,m)
    def fault(where):
        if where==point:raise RuntimeError("interrupted")
    with pytest.raises(RuntimeError):store.commit(changed,fault=fault)
    recovered=store.inspect()
    if point=="before_replace":recovered=step(recovered,m)
    assert digest(recovered["judgment"])==digest(changed["judgment"])
    assert recovered["questions"]==changed["questions"]
    replay=step(recovered,m);assert len(replay["judgment"]["corrections"])==1

def test_selection_does_not_access_replacement_truth(monkeypatch):
    state=prepared("c1")
    monkeypatch.setattr(f,"replacement_valid",lambda *args:pytest.fail("verification accessed during selection"))
    monkeypatch.setattr(f,"actual_success",lambda *args:pytest.fail("held-out outcome accessed"))
    state=step(state,message("new-eval","evaluate",f.public_case("c1")))
    assert state["outbox"][-1]["content"]["result"]["decision"]=="abstain"
