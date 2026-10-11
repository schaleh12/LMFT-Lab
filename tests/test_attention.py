"""Deterministic causal selection, attribution, learning and commit recovery."""
from copy import deepcopy
import json
import pytest
from lmft_lab import attention as a, attention_fixture as f
from lmft_lab.runtime import initial_state, advance, software_manifest
from lmft_lab.runtime_store import Store, digest

def message(identifier,op,record,reply=None):
    result={"schema_version":1,"id":identifier,"source":"registered-attention-1","sender":"teacher",
        "type":"teacher_reply" if reply else "observation","content":{"text":"Attributed fixture input.","operation":op,"record":record}}
    if reply: result["reply_to"]=reply
    return result

def step(state,m):
    return advance(state,(state["cursor"]+1,m,None,json.dumps(m)),None)

def state(mode="attention-lmft"):
    return initial_state("attention",True,software_manifest(None,"fixture"),mode)

def request(current,key):
    current=step(current,message("case-"+key,"case",f.public_case(key)))
    out=current["outbox"][-1]
    return current,message("reply-"+key,"verification",f.verify(key,out["content"]["candidate"]),out["id"])

def test_selection_causality_and_no_hidden_truth(monkeypatch):
    monkeypatch.setattr(f,"verify",lambda *args:pytest.fail("selector accessed verifier"))
    monkeypatch.setattr(f,"actual_success",lambda *args:pytest.fail("selector accessed outcome"))
    case=f.public_case("p1")
    current=a.newborn("attention-lmft");before=digest(current)
    selected,traces=a.select(current,case)
    assert selected["route"]=="A" and digest(current)==before
    assert a.select(a.newborn("attention-disabled"),case)[0]["route"]=="D"
    score=next(t["score"] for t in traces if t["candidate"]["route"]=="A")
    assert score==.203125
    assert a.frame(selected,False,True,.5)[0] < score

def test_reports_are_attributed_and_duplicates_not_independent():
    current=state();initial=deepcopy(current["judgment"])
    current,reply=request(current,"p1")
    assert not current["judgment"]["evidence"]
    assert current["judgment"]["cases"]["p1"]["result"]["decision"]=="abstain"
    case=f.public_case("n1")
    assert a.select(initial,case)[0] is None
    case=f.public_case("p1");case["reports"][-1]["value"]=True
    with pytest.raises(ValueError,match="identity"):a.select(initial,case)
    rejected=step(state(),message("conflict","case",case))
    assert rejected["receipts"][-1]["status"]=="rejected"

@pytest.mark.parametrize("kind",["type","wrong_case","unselected","source","assertion"])
def test_bad_verification_leaves_pending(kind):
    current,reply=request(state(),"t1");bad=deepcopy(reply);bad["id"]="bad"
    if kind=="type":bad["content"]["record"]["value"]="true"
    if kind=="wrong_case":bad["content"]["record"]["case_id"]="t2"
    if kind=="unselected":bad["content"]["record"]=f.verify("t1",f.CANDIDATES[2])
    if kind=="source":bad["source"]="teacher-assertion"
    if kind=="assertion":bad["type"]="observation";bad.pop("reply_to")
    current=step(current,bad)
    assert current["questions"][reply["reply_to"]]["answered_by"] is None
    assert current["judgment"]["weights"]["A"]==.5
    current=step(current,reply)
    assert current["judgment"]["weights"]["A"]==.25

@pytest.mark.parametrize("mode",a.MODES)
def test_learning_controls_and_heldout_freeze(mode):
    current=state(mode)
    for key in ("t1","t2"):
        current,reply=request(current,key);current=step(current,reply)
    expected={"A":.25,"B":.75,"D":.5} if mode in ("attention-lmft","attention-memory") else dict(A=.5,B=.5,D=.5)
    assert current["judgment"]["weights"]==expected
    current,reply=request(current,"h1");current=step(current,reply)
    assert current["judgment"]["weights"]==expected
    assert not current["judgment"]["updates"][-1]["accepted"]

def test_budget_dedup_and_conflicting_evidence():
    current,reply=request(state(),"t1");current=step(current,reply)
    before=deepcopy(current["judgment"]);traces=len(current["diagnostics"])
    for i in range(5):
        copy=deepcopy(reply);copy["id"]="copy-"+str(i);current=step(current,copy)
        current=step(current,reply)
    assert current["judgment"]==before and len(current["diagnostics"])==traces
    current=step(current,message("again","case",f.public_case("t1")))
    assert len(current["questions"])==1 and current["receipts"][-1]["status"]=="budget_exhausted"
    bad=deepcopy(reply);bad["id"]="changed";bad["content"]["record"]["value"]=True
    current=step(current,bad)
    assert current["receipts"][-1]["reason"]=="conflicting evidence identity"
    assert current["judgment"]["weights"]==before["weights"]

@pytest.mark.parametrize("resolved",[True,False])
def test_bounded_weight_updates(resolved):
    value=.5
    for _ in range(100): value=a.updated_weight(value,resolved);assert 0<=value<=1
    assert value==(1 if resolved else 0)

@pytest.mark.parametrize("point",["before_replace","after_replace"])
def test_attention_commit_recovery(tmp_path,point):
    current,reply=request(state(),"t1");store=Store(tmp_path);store.commit(current)
    changed=step(current,reply)
    def fault(where):
        if where==point:raise RuntimeError("interrupted")
    with pytest.raises(RuntimeError):store.commit(changed,fault=fault)
    recovered=store.inspect()
    if point=="before_replace":recovered=step(recovered,reply);store.commit(recovered)
    assert recovered["judgment"]==changed["judgment"]
    replay=step(recovered,reply)
    assert len(replay["judgment"]["updates"])==1

def test_existing_judgment_rule_and_verified_decision():
    current=state()
    for key in list(f.contextual.TRIALS)[:8]: current=step(current,message(key,"outcome",f.training_record(key)))
    assert [b["score"] for b in current["judgment"]["branches"].values()]==[1/3,-1/3]
    for key in ("t1","t2","h3"):
        current,reply=request(current,key);current=step(current,reply)
    assert current["judgment"]["cases"]["h3"]["result"]["decision"]=="success"
    assert not f.actual_success("h3")  # Resolution is not correctness.
