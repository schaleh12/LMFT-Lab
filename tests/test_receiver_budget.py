"""Checkpoint-accounted receiver caps and explicit physical rollback limits."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import pytest
from lmft_lab import active_relationship as a, insufficiency_fixture as f, insufficiency as s
from lmft_lab.runtime import initial_state, software_manifest, advance
from lmft_lab.runtime_store import Store, atomic_json, digest


def message(mid,op,record,reply_to=None,source=f.SOURCE):
    result={"schema_version":1,"id":mid,"sender":"fixture-operator","source":source,"type":"teacher_reply" if reply_to else "observation",
            "content":{"text":"Budgeted receiver fixture input.","operation":op,"record":deepcopy(record)}}
    if reply_to: result["reply_to"]=reply_to
    return result


def step(state,item): return advance(state,(state["cursor"]+1,item,None,json.dumps(item)),None)


def pending(budget=2,mode=a.MODES[0]):
    manifest=software_manifest(None,"fixture"); manifest["active_relationship_policy"]=a.policy("ambiguous","disagreement",budget)
    state=initial_state("budget-test",True,manifest,mode)
    for eid in f.TRAIN["ambiguous"]: state=step(state,message(eid,"outcome",f.outcome("ambiguous",eid,"train")))
    state=step(state,message("select","select",{})); return step(state,message("investigate","investigate",{}))


def reply(state,mid,success=True):
    record=a.verification_record(state["judgment"]); record["evidence"]["success"]=success
    return message(mid,"verification",record,record["request_id"])


@pytest.mark.parametrize("budget,labels,attempts,admitted,exhausted",[(0,[True],0,0,True),(1,[True],1,1,False),
    (2,[True],1,1,False),(2,[False,True],2,1,False),(2,[False,False,True],2,0,True),
    (2,[False]*6+[True],2,0,True)])
def test_frozen_budget_sequences_and_memory_parity(budget,labels,attempts,admitted,exhausted):
    left,right=pending(budget),pending(budget,a.MODES[1])
    for i,label in enumerate(labels):
        left=step(left,reply(left,"reply-"+str(i),label)); right=step(right,reply(right,"reply-"+str(i),label))
    ep=left["judgment"]["episode"]
    assert ep["receiver_attempts"]==attempts and ep["receiver_exhausted"]==exhausted
    assert ep["request_count"]==1 and len(left["judgment"]["acquired"])==admitted
    assert sum(r.get("verification_executions",0) for r in left["receipts"])==attempts
    assert a.scientific(left["judgment"])==a.scientific(right["judgment"])
    for eid in f.VALIDATION:
        left=step(left,message(eid,"outcome",f.outcome("ambiguous",eid,"validation")))
    left=step(left,message("accept","accept",{}))
    assert a.predict(left["judgment"],s.case("fresh",(4,4)))["decision"]==("success" if admitted else "abstain")


def test_legacy_omission_preserves_unlimited_shape_and_bounded_reference():
    state=pending(None)
    assert "receiver_attempt_budget" not in a.policy("ambiguous","disagreement")
    assert "receiver_attempts" not in state["judgment"]["episode"]
    for i in range(6): state=step(state,reply(state,"false-"+str(i),False))
    state=step(state,reply(state,"valid"))
    assert sum(r.get("verification_executions",0) for r in state["receipts"])==7
    assert len(state["judgment"]["acquired"])==1


@pytest.mark.parametrize("budget",[-1,9,True,False,1.0,"2"])
def test_strict_nonnegative_small_budget(budget):
    with pytest.raises(ValueError): a.policy("ambiguous","disagreement",budget)


def test_cheap_rejections_and_exact_duplicates_do_not_spend(monkeypatch):
    state=pending(); actual=reply(state,"false",False)
    bad=deepcopy(actual); bad["source"]="external"; bad["id"]="wrong-source"
    before=deepcopy(state["judgment"]); questions=deepcopy(state["questions"])
    monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("cheap input invoked verifier"))
    state=step(state,bad)
    bad=deepcopy(actual); bad["reply_to"]="out-other"; bad["id"]="unrelated"; state=step(state,bad)
    bad=deepcopy(actual); bad["content"]["record"]["evidence"]["success"]=1; bad["id"]="bad-type"; state=step(state,bad)
    assert state["judgment"]==before and state["questions"]==questions
    state=step(state,bad); assert state["receipts"][-1]["status"]=="duplicate"


def test_false_last_attempt_closes_and_denies_late_valid(monkeypatch):
    state=pending(1); false=reply(state,"false",False); valid=reply(state,"late-valid")
    state=step(state,false); ep=state["judgment"]["episode"]
    assert ep["receiver_attempts"]==1 and ep["phase"]=="closed" and ep["receiver_exhausted"]
    assert not state["judgment"]["acquired"] and [h["op"] for h in state["judgment"]["survivors"]]==["lt","le"]
    before=deepcopy(state["judgment"]); questions=deepcopy(state["questions"])
    monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("exhausted verifier invoked"))
    state=step(state,valid); assert state["receipts"][-1]["status"]=="verification_budget_exhausted"
    assert state["judgment"]==before and state["questions"]==questions
    for op in ("investigate","reset_episode","close_investigation"):
        state=step(state,message(op,op,{})); assert state["judgment"]==before


def test_valid_last_attempt_is_success_and_duplicates_conflicts_are_cheap(monkeypatch):
    state=pending(1); valid=reply(state,"valid"); state=step(state,valid)
    ep=state["judgment"]["episode"]; assert ep["receiver_attempts"]==1 and not ep["receiver_exhausted"]
    before=deepcopy(state["judgment"]); questions=deepcopy(state["questions"])
    monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("duplicate or identity conflict reverified"))
    state=step(state,valid); assert state["receipts"][-1]["status"]=="duplicate"
    copy=deepcopy(valid); copy["id"]="copy"; state=step(state,copy); assert state["receipts"][-1]["status"]=="duplicate_evidence"
    bad=deepcopy(copy); bad["id"]="conflict"; bad["content"]["record"]["evidence"]["success"]=False; state=step(state,bad)
    assert state["receipts"][-1]["reason"]=="conflicting acquisition evidence identity"
    assert state["judgment"]==before and state["questions"]==questions


def test_cancellation_never_refunds_and_evaluation_does_not_compute(monkeypatch):
    state=pending(2); state=step(state,reply(state,"false",False)); assert state["judgment"]["episode"]["receiver_attempts"]==1
    state=step(state,message("cancel","close_investigation",{})); before=deepcopy(state["judgment"])
    monkeypatch.setattr(f,"execute",lambda *args:pytest.fail("cancelled or evaluated verifier"))
    state=step(state,message("probe","evaluate",s.case("fresh",(4,4))))
    assert state["judgment"]==before and before["episode"]["receiver_attempts"]==1


def test_nonactive_modes_reject_receiver_budget_before_checkpoint(tmp_path):
    from lmft_lab.runtime import run
    with pytest.raises(ValueError,match="requires an active relationship mode"):
        run(tmp_path,individual="nonactive",mode="fixture",experiment="relationship-set-lmft",receiver_attempt_budget=2)
    assert not (tmp_path/"checkpoint.json").exists()


def test_actual_restart_budget_change_refused_with_checkpoint_unchanged(tmp_path,monkeypatch):
    monkeypatch.syspath_prepend(str(Path("experiments").resolve()))
    from run_comparative import start,halt
    from run_correction import send
    store=Store(tmp_path/"individual"); child=None
    extra=("--relationship-scenario","ambiguous","--receiver-attempt-budget","2")
    try:
        child=start(store.root,a.MODES[0],new=True,extra_args=extra)
        send(store,child,[*[message(eid,"outcome",f.outcome("ambiguous",eid,"train")) for eid in f.TRAIN["ambiguous"]],
            message("select","select",{}),message("investigate","investigate",{})])
        pending_state=halt(store,child); child=None
        before=store.root.joinpath("checkpoint.json").read_bytes()
        command=[sys.executable,"-m","lmft_lab.runtime","--root",str(store.root),"start","--experiment",a.MODES[0],
                 "--mode","fixture","--relationship-scenario","ambiguous","--receiver-attempt-budget","3"]
        refused=subprocess.run(command,capture_output=True,text=True,timeout=15)
        atomic_json(tmp_path/"changed-budget-refusal.json",{"returncode":refused.returncode,"stderr":refused.stderr})
        assert refused.returncode==1 and "Code/config/control changed" in refused.stderr
        assert store.root.joinpath("checkpoint.json").read_bytes()==before
        child=start(store.root,a.MODES[0],extra_args=extra); restored=halt(store,child); child=None
        assert restored==pending_state and restored["judgment"]["episode"]["receiver_attempt_budget"]==2
    finally:
        if child is not None and child.poll() is None: halt(store,child)


@pytest.mark.parametrize("point,physical",[("before_replace",2),("after_replace",1)])
def test_actual_child_process_atomic_rollback_exceeds_only_physical_bound(tmp_path,point,physical):
    state=pending(1); item=reply(state,"false",False)
    store=Store(tmp_path/"individual"); store.commit(state); atomic_json(tmp_path/"input.json",item)
    worker=Path(__file__).resolve().parents[1]/"experiments/receiver_fault_worker.py"
    first=subprocess.run([sys.executable,str(worker),"--root",str(tmp_path),"--fault",point],capture_output=True,text=True,check=True)
    restored=store.read()
    assert restored["judgment"]["episode"]["receiver_attempts"]==(0 if point=="before_replace" else 1)
    second=subprocess.run([sys.executable,str(worker),"--root",str(tmp_path)],capture_output=True,text=True,check=True)
    lines=[json.loads(x) for x in (tmp_path/"physical-calls.jsonl").read_text().splitlines()]
    assert len(lines)==physical
    assert json.loads(first.stdout)["pid"]!=json.loads(second.stdout)["pid"]
    final=store.read(); assert final["judgment"]["episode"]["receiver_attempts"]==1 and final["judgment"]["episode"]["receiver_exhausted"]
    assert not final["judgment"]["acquired"] and final["judgment"]["episode"]["request_count"]==1
    assert sum(r.get("verification_executions",0) for r in final["receipts"])==1


def test_real_receiver_budget_study(tmp_path):
    from lmft_lab.preservation_context import capture_current
    context=tmp_path/"context.json"; atomic_json(context,capture_current(Path.cwd()))
    root=tmp_path/"study"
    subprocess.run([sys.executable,"experiments/run_receiver_budget.py","--output",str(root),"--preservation-context",str(context)],check=True)
    result=json.loads((root/"results.json").read_text())
    assert result["integrity_passed"]==result["integrity_total"] and result["quality_passed"]==result["quality_total"]==84
    assert result["model_calls"]==0
