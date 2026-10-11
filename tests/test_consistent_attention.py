"""Relation-aware support, exact ablations and known failure preservation."""
from copy import deepcopy
import json
import pytest
from lmft_lab import consistent_attention as c,consistent_fixture as f,scoped_attention as old
from lmft_lab.runtime import advance,initial_state,software_manifest
from lmft_lab.runtime_store import Store,digest


def message(identifier,op,record,reply=None):
    m={"schema_version":1,"id":identifier,"source":f.SOURCE,"sender":"teacher",
       "type":"teacher_reply" if reply else "observation","content":{"text":"Registered experiment input.","operation":op,"record":record}}
    if reply:m["reply_to"]=reply
    return m

def step(current,m):return advance(current,(current["cursor"]+1,m,None,json.dumps(m)),None)

def prepared(key,mode="consistent-full",contrary=True):
    current=initial_state("consistent",True,software_manifest(None,"fixture"),mode)
    for i,r in enumerate(f.initial_records(key,contrary)):
        current=step(current,message("evidence-"+str(i),"evidence",r))
    return current

@pytest.mark.parametrize("key,resolved,inconsistent,coverage",[("f1",True,False,1),("f2",False,False,.5),("f3",False,True,1),("f4",False,True,1),("f7",False,False,.5),("f9",True,False,1)])
def test_relation_coverage_consistency_are_distinct(key,resolved,inconsistent,coverage):
    current=prepared(key);before=digest(current)
    support=c.support(current["judgment"],f.public_case(key),"shielded")
    assert (support["resolved"],support["inconsistent"],support["coverage"])==(resolved,inconsistent,coverage)
    assert digest(current)==before
    if key=="f9":assert support["value"] is False

@pytest.mark.parametrize("mode",c.MODES)
def test_known_failure_and_fresh_priority(mode):
    known=prepared("known",mode);selected,traces=c.select(known["judgment"],f.public_case("known"))
    assert (selected is None)==(mode=="consistent-historical")
    current=prepared("f8",mode);selected,_=c.select(current["judgment"],f.public_case("f8"))
    assert selected["field"]==("payload_valid" if mode in ("consistent-historical","consistent-no-clarity") else "shielded")
    assert current["judgment"]["weights"]==dict(A=.25,B=.75,D=.5)

def test_historical_select_is_exact_old_function_result():
    current=prepared("known","consistent-historical")["judgment"];case=f.public_case("known")
    chosen,traces=c.select(current,case)
    view=c.normalized(current,case);view["mode"]="scoped-full"
    old_choice,old_traces=old.select(view,case)
    assert chosen==old_choice and traces[0]["historical_selection"]==old_traces
    assert old_traces[0]["support"]["fact_fraction"]==1
    final={e["node_id"]:e for e in old_traces[0]["propagation"]["passes"][-1]}
    assert final[c.C]["unclamped"]==-.046875 and final[c.C]["activation"]==0
    assert final[c.Q]["activation"]==.25

def test_ablation_removes_only_specified_outgoing_edge():
    def trace(mode):
        _,traces=c.select(prepared("f3",mode)["judgment"],f.public_case("f3"))
        return traces[1]["propagation"]
    full=trace("consistent-full")
    for mode,node in (("consistent-no-clarity",c.C),("consistent-no-fact",c.F),("consistent-no-confidence",c.Q)):
        ablated=trace(mode)
        assert ablated["direct_frame"]==full["direct_frame"]
        differences=[]
        for edge,original in zip(ablated["relationships"],full["relationships"]):
            assert {k:v for k,v in edge.items() if k!="active"}=={k:v for k,v in original.items() if k!="active"}
            if not edge["active"]:differences.append(edge["source_id"])
        assert differences==[node]

def test_irrelevant_difference_and_unverified_claim_do_not_reopen():
    for key in ("f5","f6"):
        current=prepared(key)
        chosen,traces=c.select(current["judgment"],f.public_case(key))
        assert chosen is None
        if key=="f5":assert traces[0]["adapter"]["excluded"][0]["field"]=="color"

def test_scope_duplicate_and_bad_claims():
    current=prepared("f7");case=f.public_case("f7")
    support=c.support(current["judgment"],case,"shielded")
    assert support["coverage"]==.5 and len(support["evidence_refs"])==1
    before=deepcopy(current["judgment"]);r=f.initial_records("f7")[1]
    for i in range(5):current=step(current,message("copy-"+str(i),"evidence",r))
    assert current["judgment"]==before
    bad={**r,"value":"certain"};current=step(current,message("bad","evidence",bad))
    assert current["receipts"][-1]["status"]=="rejected"

def test_reopening_restart_and_exhausted_budget(tmp_path):
    current=prepared("f4",contrary=False)
    current=step(current,message("before","evaluate",f.public_case("f4")))
    assert not current["questions"]
    store=Store(tmp_path);store.commit(current);assert digest(store.inspect())==digest(current)
    current=step(store.inspect(),message("late","evidence",f.initial_records("f4")[-1]))
    current=step(current,message("after","evaluate",f.public_case("f4")))
    request=current["outbox"][-1];assert request["type"]=="clarification_request"
    reply=message("answer","verification",f.verify("f4","shielded"),request["id"])
    current=step(current,reply)
    assert c.predict(current["judgment"],f.public_case("f4"))["decision"]=="abstain"
    current=step(current,message("again","evaluate",f.public_case("f4")))
    assert current["receipts"][-1]["status"]=="budget_exhausted" and len(current["questions"])==1

def test_no_hidden_truth_in_selector_or_prediction(monkeypatch):
    current=prepared("f9");case=f.public_case("f9")
    def forbidden(*args):pytest.fail("accessed hidden truth")
    monkeypatch.setattr(f,"verify",forbidden);monkeypatch.setattr(f,"actual_success",forbidden)
    assert c.select(current["judgment"],case)[0] is None
    assert c.predict(current["judgment"],case)["support"]["shielded"]["resolved"]

@pytest.mark.parametrize("point",["before_replace","after_replace"])
def test_interrupted_contradiction_commit(tmp_path,point):
    current=prepared("f4",contrary=False);store=Store(tmp_path);store.commit(current)
    m=message("late","evidence",f.initial_records("f4")[-1]);changed=step(current,m)
    def fault(where):
        if where==point:raise RuntimeError("interruption")
    with pytest.raises(RuntimeError):store.commit(changed,fault=fault)
    recovered=store.inspect()
    if point=="before_replace":recovered=step(recovered,m)
    assert recovered["judgment"]==changed["judgment"]
    assert step(recovered,m)["judgment"]==changed["judgment"]
