"""Request accounting, correlation, safe revision and real runtime regression."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import pytest
from lmft_lab import active_relationship as a, insufficiency_fixture as f, insufficiency as s, ambiguity
from lmft_lab.runtime import advance, initial_state, software_manifest, run
from lmft_lab.runtime_store import Store, atomic_json, digest


def message(mid, op, record, reply_to=None, source=f.SOURCE):
    item = {"schema_version":1,"id":mid,"sender":"fixture-operator","source":source,"type":"teacher_reply" if reply_to else "observation",
            "content":{"text":"Registered active relationship operation.","operation":op,"record":deepcopy(record)}}
    if reply_to: item["reply_to"]=reply_to
    return item


def step(state,item):
    class NoModels:
        def complete(self,*args): pytest.fail("active mode called model")
    return advance(state,(state["cursor"]+1,item,None,json.dumps(item)),NoModels())


def new(scenario="ambiguous",policy="disagreement",mode=a.MODES[0],learning=True):
    manifest=software_manifest(None,"fixture"); manifest["active_relationship_policy"]=a.policy(scenario,policy)
    return initial_state("active",learning,manifest,mode)


def selected(scenario="ambiguous",policy="disagreement",mode=a.MODES[0]):
    state=new(scenario,policy,mode)
    for eid in f.TRAIN[scenario]: state=step(state,message(eid,"outcome",f.outcome(scenario,eid,"train")))
    return step(state,message("select","select",{}))


def pending(scenario="ambiguous",policy="disagreement",mode=a.MODES[0]):
    return step(selected(scenario,policy,mode),message("investigate","investigate",{}))


def valid_reply(state,mid="valid"):
    current=state["judgment"]; record=a.verification_record(current)
    return message(mid,"verification",record,record["request_id"])


def accepted(scenario="ambiguous",policy="disagreement",mode=a.MODES[0]):
    state=pending(scenario,policy,mode)
    if state["judgment"]["episode"]["phase"]=="pending": state=step(state,valid_reply(state))
    for eid in f.VALIDATION: state=step(state,message(eid,"outcome",f.outcome(scenario,eid,"validation")))
    return step(state,message("accept","accept",{}))


@pytest.mark.parametrize("scenario,policy,selected_id,ops",[("ambiguous","disagreement","q2",["le"]),
    ("ambiguous","noninformative","q1",["lt","le"]),("ambiguous","unavailable",None,["lt","le"]),
    ("supported","disagreement",None,["le"]),("unsupported","disagreement",None,[])])
def test_gates_resolution_consensus_and_memory_parity(scenario,policy,selected_id,ops):
    l,r=accepted(scenario,policy),accepted(scenario,policy,a.MODES[1])
    assert a.scientific(l["judgment"])==a.scientific(r["judgment"])
    ep=l["judgment"]["episode"]
    assert ep["request_count"]==ep["verified_observations"]==int(selected_id is not None)
    assert len([o for o in l["outbox"] if o["type"]=="clarification_request"])==int(selected_id is not None)
    assert [h["op"] for h in l["judgment"]["survivors"]]==ops
    if selected_id: assert ep["selection"]["selected"]["case_id"]==selected_id
    assert ep["phase"]=="closed" and l["judgment"]["acceptance"]["accepted"]==bool(ops)
    for eid,pair in f.HELD.items(): assert a.predict(l["judgment"],s.case(eid,pair))==a.predict(r["judgment"],s.case(eid,pair))
    assert l["birth"]==r["birth"] and len(l["birth"]["nodes"])==40
    assert not l["diagnostics"]


def test_request_spends_before_reply_and_rejected_label_cost_is_receipt_only():
    state=pending(); current=deepcopy(state["judgment"]); questions=deepcopy(state["questions"])
    item=valid_reply(state,"false"); item["content"]["record"]["evidence"]["success"]=False
    result=step(state,item)
    assert result["judgment"]==current and result["questions"]==questions
    assert result["receipts"][-1]["verification_executions"]==1
    assert result["receipts"][-1]["status"]=="rejected"
    assert current["episode"]["request_count"]==1 and not current["acquired"]
    result=step(result,valid_reply(result)); assert result["judgment"]["episode"]["request_count"]==1
    assert result["judgment"]["episode"]["verified_observations"]==1
    assert sum(r.get("verification_executions",0) for r in result["receipts"])==2


def test_reserved_verifier_cost_counts_failed_checks_without_scientific_revision(monkeypatch):
    state=new(); record=f.outcome("ambiguous","t1","train"); before=deepcopy(state["judgment"])
    original=f.execute; calls=[]
    def counted(*args): calls.append(args); return original(*args)
    monkeypatch.setattr(f,"execute",counted)
    state=step(state,message("false-training","outcome",{**record,"success":False}))
    assert state["judgment"]==before and len(calls)==1
    assert state["receipts"][-1]["reserved_verification_executions"]==1 and state["receipts"][-1]["verification_split"]=="train"
    state=step(state,message("true-training","outcome",record)); assert len(calls)==2
    state=step(state,message("copy-training","outcome",record)); assert len(calls)==2
    assert sum(r.get("reserved_verification_executions",0) for r in state["receipts"])==2
    assert len(state["judgment"]["learner"]["evidence"]["train"])==1


def test_frozen_quality_expectations_ignore_observed_resolution(monkeypatch):
    import importlib.util
    monkeypatch.syspath_prepend(str(Path("experiments").resolve()))
    spec=importlib.util.spec_from_file_location("active_harness","experiments/run_active_relationship.py")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    assert module.quality_expectations({"scenario":"ambiguous","policy":"disagreement","resolved":False})["overall"]==(8,6)
    assert module.quality_expectations({"scenario":"ambiguous","policy":"noninformative","resolved":True})["overall"]==(4,3)


@pytest.mark.parametrize("mutation",["source","episode","request","envelope","candidate","type","schema"])
def test_unrelated_malformed_replies_do_not_learn_or_check_or_close(monkeypatch,mutation):
    state=pending(); item=valid_reply(state); current=deepcopy(state["judgment"]); questions=deepcopy(state["questions"])
    record=item["content"]["record"]
    if mutation=="source": item["source"]="external"
    elif mutation=="episode": record["episode_id"]="other-episode"
    elif mutation=="request": record["request_id"]="out-other"
    elif mutation=="envelope": item["reply_to"]="out-other"
    elif mutation=="candidate": record["evidence"]["length"]=7
    elif mutation=="type": record["evidence"]["success"]=1
    else: record["extra"]="unpermitted"
    monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("ineligible reply reached verifier"))
    result=step(state,item)
    assert result["judgment"]==current and result["questions"]==questions
    assert result["receipts"][-1]["status"]=="rejected" and not result["receipts"][-1].get("verification_executions")


def test_duplicates_conflicts_require_source_and_correlation_before_dedup(monkeypatch):
    state=pending(); item=valid_reply(state); state=step(state,item)
    before=deepcopy(state["judgment"]); questions=deepcopy(state["questions"]); outbox=deepcopy(state["outbox"])
    monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("duplicate verification"))
    state=step(state,item); assert state["receipts"][-1]["status"]=="duplicate" and state["outbox"]==outbox
    conflict=deepcopy(item); conflict["content"]["record"]["evidence"]["success"]=False
    state=step(state,conflict); assert state["receipts"][-1]["status"]=="id_conflict"
    copy=deepcopy(item); copy["id"]="copy"; state=step(state,copy); assert state["receipts"][-1]["status"]=="duplicate_evidence"
    bad=deepcopy(copy); bad["id"]="wrong-source"; bad["source"]="external"; state=step(state,bad)
    assert state["receipts"][-1]["status"]=="rejected"
    bad=deepcopy(copy); bad["id"]="wrong-correlation"; bad["reply_to"]="out-other"; state=step(state,bad)
    assert state["receipts"][-1]["status"]=="rejected"
    conflict["id"]="evidence-conflict"; state=step(state,conflict)
    assert state["receipts"][-1]["reason"]=="conflicting acquisition evidence identity"
    assert state["judgment"]==before and state["questions"]==questions


def test_immutable_training_effective_set_and_validation_distinctions():
    state=pending(); derivation=deepcopy(state["judgment"]["learner"]["derivation"])
    assert a.predict(state["judgment"],s.case("fresh",(1,4)))["reason"]=="not_validated"
    state=step(state,valid_reply(state)); current=state["judgment"]
    assert current["learner"]["derivation"]==derivation
    assert [h["op"] for h in current["learner"]["survivors"]]==["lt","le"]
    assert [h["op"] for h in current["survivors"]]==["le"]
    assert a.predict(current,s.case("fresh",(1,4)))["reason"]=="not_validated"
    for eid in f.VALIDATION: state=step(state,message(eid,"outcome",f.outcome("ambiguous",eid,"validation")))
    state=step(state,message("accept","accept",{})); assert a.predict(state["judgment"],s.case("fresh",(4,4)))["decision"]=="success"
    assert current["learner"]["derivation"]==derivation


def test_repeated_investigation_reset_early_validation_and_cancellation():
    state=pending(); before=deepcopy(state["judgment"]); questions=deepcopy(state["questions"])
    for op,record in (("investigate",{}),("reset_episode",{}),("select",{}),("accept",{}),
                      ("outcome",f.outcome("ambiguous","v1","validation"))):
        state=step(state,message("repeat-"+op,op,record)); assert state["judgment"]==before and state["questions"]==questions
    reply=valid_reply(state)
    state=step(state,message("cancel","close_investigation",{})); before=deepcopy(state["judgment"])
    state=step(state,reply); assert state["judgment"]==before and state["receipts"][-1]["status"]=="rejected"
    assert state["judgment"]["episode"]["request_count"]==1
    state=step(state,message("again","investigate",{})); assert state["judgment"]==before


def test_choose_filter_and_predict_no_oracle_or_decorative_activation(monkeypatch):
    state=selected(); monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("oracle outside admission"))
    monkeypatch.setattr(ambiguity,"outcome",lambda *args:pytest.fail("old oracle accessed"))
    result=a.choose(state["judgment"]); assert result["selected"]["case_id"]=="q2"
    assert [r["score"] for r in result["scored"]]==[0,1,1,0]
    assert a.predict(state["judgment"],s.case("fresh",(3,3)))["decision"]=="abstain"
    state["birth"]=None; assert a.choose(state["judgment"])==result


def test_learning_disabled_never_requests_or_verifies(monkeypatch):
    state=new(learning=False); before=deepcopy(state["judgment"])
    record=f.outcome("ambiguous","t1","train")
    monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("disabled oracle"))
    for op,data in (("outcome",record),("select",{}),("investigate",{}),("accept",{})):
        state=step(state,message(op,op,data)); assert state["judgment"]==before
        assert state["receipts"][-1]["reason"]=="learning disabled"
    assert not state["questions"] and not any(o["type"]=="clarification_request" for o in state["outbox"])


def test_evaluation_read_only_questions_budget_and_verifier(monkeypatch):
    state=accepted(); before=deepcopy(state["judgment"]); questions=deepcopy(state["questions"])
    monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("evaluation executed verifier"))
    for eid,pair in f.HELD.items(): state=step(state,message("probe-"+eid,"evaluate",s.case(eid,pair)))
    assert state["judgment"]==before and state["questions"]==questions


@pytest.mark.parametrize("point",["before_replace","after_replace"])
@pytest.mark.parametrize("operation",["investigate","verification","close_investigation","accept","evaluate"])
def test_atomic_episode_request_reply_and_replay(tmp_path,point,operation):
    if operation=="investigate": state=selected(); item=message("act",operation,{})
    elif operation=="verification": state=pending(); item=valid_reply(state,"act")
    elif operation=="close_investigation": state=pending(); item=message("act",operation,{})
    elif operation=="accept":
        state=pending(); state=step(state,valid_reply(state))
        for eid in f.VALIDATION: state=step(state,message(eid,"outcome",f.outcome("ambiguous",eid,"validation")))
        item=message("act",operation,{})
    else: state=accepted(); item=message("act",operation,s.case("fresh",(4,4)))
    store=Store(tmp_path); store.commit(state); changed=step(state,item)
    def fault(where):
        if where==point: raise RuntimeError("injected interruption")
    with pytest.raises(RuntimeError): store.commit(changed,fault=fault)
    restored=store.inspect(); assert digest(restored)==digest(state if point=="before_replace" else changed)
    if point=="before_replace": restored=step(restored,item)
    def semantic(value):
        result=deepcopy(value)
        for out in result["outbox"]: out.pop("timestamp",None)
        return result
    assert digest(semantic(restored))==digest(semantic(changed))
    replay=step(restored,item); assert replay["judgment"]==restored["judgment"] and replay["questions"]==restored["questions"] and replay["outbox"]==restored["outbox"]
    assert replay["judgment"]["episode"]["request_count"]<=1


def test_validation_failure_and_no_resurrection():
    state=accepted("ambiguous","noninformative"); current=state["judgment"]
    current["learner"]["phase"]="validation"; current["learner"]["evidence"]["validation"]["v1"]["success"]=False
    retained=deepcopy(current["survivors"]); a.accept(current)
    assert not current["acceptance"]["accepted"] and current["survivors"]==retained
    assert a.predict(current,s.case("fresh",(1,4)))["reason"]=="validation_rejected"


def test_local_mode_rejected_before_model_setup(tmp_path,monkeypatch):
    import lmft_lab.runtime as runtime
    monkeypatch.setattr(runtime,"load_config",lambda *args:pytest.fail("model config loaded"))
    with pytest.raises(ValueError,match="require --mode fixture"): run(tmp_path,individual="active",mode="local",experiment=a.MODES[0])


def test_real_active_runtime_suite(tmp_path):
    from lmft_lab.preservation_context import capture_current
    context=tmp_path/"context.json"; atomic_json(context,capture_current(Path.cwd()))
    root=tmp_path/"active"
    subprocess.run([sys.executable,"experiments/run_active_relationship.py","--output",str(root),"--preservation-context",str(context)],check=True,timeout=120)
    result=json.loads((root/"results.json").read_text())
    assert result["integrity_passed"]==result["integrity_total"] and result["quality_passed"]==result["quality_total"]==60
    assert result["model_calls"]==0
