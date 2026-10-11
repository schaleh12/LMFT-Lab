"""Scoped evidence, precise ablations and persistence boundaries."""
from copy import deepcopy
import json
import pytest
from lmft_lab import scoped_attention as s, scoped_fixture as f, attention
from lmft_lab.runtime import advance,initial_state,software_manifest
from lmft_lab.runtime_store import Store,digest


def message(identifier,op,record,reply=None):
    m={"schema_version":1,"id":identifier,"source":f.SOURCE,"sender":"teacher",
       "type":"teacher_reply" if reply else "observation","content":{"text":"Attributed scoped fixture information.","operation":op,"record":record}}
    if reply:m["reply_to"]=reply
    return m

def step(current,m):return advance(current,(current["cursor"]+1,m,None,json.dumps(m)),None)

def state(mode="scoped-full"):
    return initial_state("scoped",True,software_manifest(None,"fixture"),mode)

def prepared(key,mode="scoped-full",contrary=True):
    current=state(mode)
    for i,r in enumerate(f.initial_records(key,contrary)):
        current=step(current,message("initial-"+str(i),"evidence",r))
    return current

@pytest.mark.parametrize("mode",s.MODES)
def test_scoped_choices_and_fixed_weights(mode):
    for key in f.IDS:
        current=prepared(key,mode);before=digest(current)
        selected,traces=s.select(current["judgment"],f.public_case(key))
        expected="payload_valid" if key=="q1" and mode!="scoped-neither" else None if key in ("q4","q7") and mode in ("scoped-full","scoped-memory") else "shielded"
        assert (selected["field"] if selected else None)==expected
        assert digest(current)==before
        assert current["judgment"]["weights"]==dict(A=.25,B=.75,D=.5)
        assert current["birth"]==state()["birth"]

def test_only_outgoing_edges_differ():
    traces={}
    for mode in s.MODES[:-1]:
        _,trace=s.select(prepared("q7",mode)["judgment"],f.public_case("q7"))
        traces[mode]=trace[0]["propagation"]
    base=traces["scoped-full"]
    for mode,trace in traces.items():
        assert trace["direct_frame"]==base["direct_frame"]
        for actual,original in zip(trace["relationships"],base["relationships"]):
            assert {k:v for k,v in actual.items() if k!="active"}=={k:v for k,v in original.items() if k!="active"}
            disabled=(original["source_id"]==s.F and mode in ("scoped-no-fact","scoped-neither") or
                      original["source_id"]==s.Q and mode in ("scoped-no-confidence","scoped-neither"))
            assert actual["active"] is not disabled

@pytest.mark.parametrize("key,fraction,resolved",[("q1",1,True),("q2",.5,False),("q3",0,False),("q5",0,False),("q6",.5,False)])
def test_scoped_partial_assertion_and_conflict_policy(key,fraction,resolved):
    current=prepared(key)
    result=s.support(current["judgment"],f.public_case(key),"shielded")
    assert result["fact_fraction"]==fraction and result["resolved"] is resolved
    if key=="q5":assert result["evidence_refs"]==[] and len(current["judgment"]["ledger"])==5

def test_claim_and_malformed_evidence_are_not_fact():
    current=state();valid=f.initial_records("q1")[0]
    for i,change in enumerate(({"value":"true"},{"value":1},{"scope":"forged"},{"source":"teacher"})):
        invalid={**valid,**change};current=step(current,message("bad-"+str(i),"evidence",invalid))
        assert current["receipts"][-1]["status"]=="rejected"
    assert not current["judgment"]["ledger"]

def test_duplicate_and_conflicting_identity():
    current=prepared("q1");before=deepcopy(current["judgment"])
    record=f.initial_records("q1")[0]
    for i in range(5):current=step(current,message("copy-"+str(i),"evidence",record))
    assert current["judgment"]==before and not current["diagnostics"]
    bad={**record,"value":False};current=step(current,message("conflict","evidence",bad))
    assert current["receipts"][-1]["reason"]=="conflicting evidence identity"

def test_reopening_and_one_request_budget(tmp_path):
    current=prepared("q6",contrary=False)
    current=step(current,message("before","evaluate",f.public_case("q6")))
    assert not current["questions"]
    store=Store(tmp_path);store.commit(current);current=store.inspect()
    current=step(current,message("contrary","evidence",f.initial_records("q6")[-1]))
    current=step(current,message("after","evaluate",f.public_case("q6")))
    request=current["outbox"][-1];assert request["type"]=="clarification_request"
    reply=message("reply","verification",f.verify("q6","shielded"),request["id"])
    bad=deepcopy(reply);bad["id"]="bad";bad["content"]["record"]=f.verify("q6","payload_valid")
    current=step(current,bad);assert current["questions"][request["id"]]["answered_by"] is None
    current=step(current,reply)
    assert not s.support(current["judgment"],f.public_case("q6"),"shielded")["resolved"]
    current=step(current,message("again","evaluate",f.public_case("q6")))
    assert len(current["questions"])==1 and current["receipts"][-1]["status"]=="budget_exhausted"

def test_selection_and_prediction_do_not_read_hidden_truth(monkeypatch):
    current=prepared("q2");case=f.public_case("q2")
    def forbidden(*args):pytest.fail("hidden fixture access")
    monkeypatch.setattr(f,"verify",forbidden);monkeypatch.setattr(f,"actual_success",forbidden)
    assert s.select(current["judgment"],case)[0]["field"]=="shielded"
    assert s.predict(current["judgment"],case)["decision"]=="abstain"

@pytest.mark.parametrize("point",["before_replace","after_replace"])
def test_scoped_commit_interruption(tmp_path,point):
    current=prepared("q6",contrary=False);store=Store(tmp_path);store.commit(current)
    m=message("contrary","evidence",f.initial_records("q6")[-1]);changed=step(current,m)
    def fault(where):
        if where==point:raise RuntimeError("interrupted")
    with pytest.raises(RuntimeError):store.commit(changed,fault=fault)
    recovered=store.inspect()
    if point=="before_replace":recovered=step(recovered,m)
    assert recovered["judgment"]==changed["judgment"]
    assert step(recovered,m)["judgment"]==changed["judgment"]
