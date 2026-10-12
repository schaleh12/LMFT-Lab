"""Finite receiver accounting study with a bounded legacy replay reference."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
from lmft_lab import active_relationship as a, insufficiency as s, insufficiency_fixture as f
from lmft_lab import preservation_context as preservation
from lmft_lab.runtime_store import Store,atomic_json,digest
from run_comparative import start,halt,check_boundary
from run_correction import send
from run_active_relationship import message,service_record,invalid_replies,standalone
from run_passive_relationship import semantic
from run_insufficiency import quality

PROTOCOL=Path("experiments/RECEIVER_BUDGET_PROTOCOL.md")
CASES=(
    {"id":"zero","budget":0,"labels":[True],"checks":0,"eligible":1,"admissions":0,"exhausted":True},
    {"id":"valid-first","budget":2,"labels":[True],"checks":1,"eligible":1,"admissions":1,"exhausted":False},
    {"id":"false-valid","budget":2,"labels":[False,True],"checks":2,"eligible":2,"admissions":1,"exhausted":False},
    {"id":"exhausted-late","budget":2,"labels":[False,False,True],"checks":2,"eligible":2,"admissions":0,"exhausted":True},
    {"id":"fresh-ID-flood","budget":2,"labels":[False]*6+[True],"checks":2,"eligible":2,"admissions":0,"exhausted":True},
    {"id":"last-valid","budget":1,"labels":[True],"checks":1,"eligible":1,"admissions":1,"exhausted":False},
    {"id":"legacy-flood","budget":None,"labels":[False]*6+[True],"checks":7,"eligible":7,"admissions":1,"exhausted":False})


def reference_attempts(case):
    """Standalone cap/rejection policy, using provided fixed script/verifier truth."""
    spent=0; admitted=0; exhausted=False
    for label in case["labels"]:
        if admitted or exhausted: continue
        if case["budget"] is not None and spent>=case["budget"]:
            exhausted=True; continue
        spent+=1
        if label: admitted=1
        elif case["budget"] is not None and spent>=case["budget"]: exhausted=True
    return spent,admitted,exhausted


def run_case(root,mode,case,continuous,context_root,context_sha):
    store=Store(root/"individual"); process=None; checks={}; pids=[]
    extra=["--relationship-scenario","ambiguous"]
    if case["budget"] is not None: extra += ["--receiver-attempt-budget",str(case["budget"])]
    def launch(new=False):
        preservation.pinned_current(context_root,Path.cwd(),context_sha)
        child=start(store.root,mode,new=new,extra_args=extra); pids.append(child.pid); return child
    def recover(stage):
        nonlocal process
        old=halt(store,process); process=None; atomic_json(root/(stage+"-halted.json"),old)
        process=launch(); restored=halt(store,process); process=None; checks[stage+"_restart_exact"]=restored==old
        process=launch(); return old
    try:
        process=launch(True); checks["live_inspection_denied"]=check_boundary(store)
        send(store,process,[*[message(eid,"outcome",f.outcome("ambiguous",eid,"train")) for eid in f.TRAIN["ambiguous"]],
            message("select","select",{}),message("investigate","investigate",{}),message("pending-barrier","barrier",{})])
        requests=[out for out in store.receive() if out["type"]=="clarification_request"]; request=requests[0]
        if not continuous:
            pending=recover("pending")
            checks["pending_counter_zero"]=pending["judgment"]["episode"].get("receiver_attempts",0)==0
        # Cheap rejection controls exclude the one false-label attack from old helper.
        cheap=invalid_replies(request,"ambiguous")[:-1]
        send(store,process,[message("before-cheap","evaluate",s.case("constant",(1,4))),*cheap,
            message("after-cheap","evaluate",s.case("constant",(1,4))),message("cheap-barrier","barrier",{})])
        real=service_record(request,"ambiguous")
        script=[]
        for i,label in enumerate(case["labels"]):
            record=deepcopy(real); record["evidence"]["success"]=label
            item=message("reply-"+str(i),"verification",record,request["id"]); script.append(item)
            if i==0:
                script.append(deepcopy(item))
                conflict=deepcopy(item); conflict["content"]["record"]["evidence"]["success"]=not label
                script.append(conflict)
        if case["admissions"]:
            good=message("accepted-copy","verification",real,request["id"])
            conflict=deepcopy(good); conflict["id"]="accepted-evidence-conflict"; conflict["content"]["record"]["evidence"]["success"]=False
            wrong=deepcopy(good); wrong.update(id="accepted-wrong-source",source="external")
            script += [good,conflict,wrong]
        script += [message("no-reset","reset_episode",{}),message("no-second-request","investigate",{}),message("reply-barrier","barrier",{})]
        send(store,process,script)
        if not continuous: replied=recover("replied")
        send(store,process,[*[message(eid,"outcome",f.outcome("ambiguous",eid,"validation")) for eid in f.VALIDATION],
            message("accept","accept",{}),message("before-probes","evaluate",s.case("constant",(1,4))),
            *[message("probe-"+eid,"evaluate",s.case(eid,pair)) for eid,pair in f.HELD.items()],
            message("after-probes","evaluate",s.case("constant",(1,4))),message("final-barrier","barrier",{})])
        final=halt(store,process); process=None; atomic_json(root/"final-halted.json",final)
        current=final["judgment"]; ep=current["episode"]; receipts=final["receipts"]
        outputs={out["reply_to"]:out["content"] for out in final["outbox"] if out["type"]=="response"}
        predictions={eid:outputs["probe-"+eid]["result"] for eid in f.HELD}; atomic_json(root/"frozen-predictions.json",predictions)
        physical=sum(r.get("verification_executions",0) for r in receipts)
        accounted=ep.get("receiver_attempts",physical)
        eligible=sum(r.get("eligible_verification_checks",0) for r in receipts) if case["budget"] is not None else physical
        ref=reference_attempts(case)
        # Existing standalone learner receives the actually admitted observation only;
        # acquisition selection/request budget remains unchanged across receiver policies.
        if case["admissions"]:
            sci=standalone("ambiguous","disagreement",{eid:v["record"] for eid,v in current["acquired"].items()})
        else:
            # No admission: direct original ambiguous state with reserved validation.
            state=s.newborn("memory","ambiguous")
            for eid in f.TRAIN["ambiguous"]: s.admit(state,f.outcome("ambiguous",eid,"train"))
            s.select(state)
            for eid in f.VALIDATION: s.admit(state,f.outcome("ambiguous",eid,"validation"))
            s.accept(state)
            sci={"survivors":state["survivors"],"support_status":state["support_status"]}
        atomic_json(root/"standalone-reference.json",{"receiver":ref,"scientific":sci})
        checks.update({"fixed_verifier_count":physical==accounted==case["checks"],
            "fixed_eligibility_count":eligible==case["eligible"],"fixed_admissions":len(current["acquired"])==case["admissions"],
            "fixed_exhaustion":ep.get("receiver_exhausted",False)==case["exhausted"],
            "fixed_effective_set":[h["op"] for h in current["survivors"]]==(["le"] if case["admissions"] else ["lt","le"]),
            "logical_cap":case["budget"] is None or accounted<=case["budget"],
            "standalone_receiver":ref==(case["checks"],case["admissions"],case["exhausted"]),
            "standalone_hypotheses":current["survivors"]==sci["survivors"] and current["support_status"]==sci["support_status"],
            "one_request":ep["request_count"]==len(requests)==1,
            "cheap_rejection_invariance":outputs["before-cheap"]["scientific_digest"]==outputs["after-cheap"]["scientific_digest"] and outputs["before-cheap"]["questions_digest"]==outputs["after-cheap"]["questions_digest"],
            "evaluation_invariance":outputs["before-probes"]["scientific_digest"]==outputs["after-probes"]["scientific_digest"] and outputs["before-probes"]["questions_digest"]==outputs["after-probes"]["questions_digest"],
            "cheap_duplicate":sum(r["status"]=="duplicate" for r in receipts)==1,
            "cheap_message_conflict":sum(r["status"]=="id_conflict" for r in receipts)==1,
            "message_bound":len(receipts)<=100,"no_models":not final["diagnostics"],
            "scope":predictions["x1"]["decision"]=="out_of_scope",
            "policy_pin":final["manifest"]["active_relationship_policy"]==a.policy("ambiguous","disagreement",case["budget"])})
        if case["exhausted"]:
            checks["exhausted_question"]=final["questions"][request["id"]]["status"]=="receiver_budget_exhausted" and ep["closed_reason"]=="receiver_budget_exhausted"
            if not continuous: checks["exhaustion_survived"]=replied["judgment"]["episode"]["receiver_exhausted"] and replied["questions"]==final["questions"]
        if case["budget"] is None: checks["legacy_shape"]="receiver_attempt_budget" not in ep and "receiver_attempts" not in ep
        before=store.root.joinpath("checkpoint.json").read_bytes(); old=digest(final)
        for eid,pair in f.HELD.items(): assert a.predict(current,s.case(eid,pair))==predictions[eid]
        checks["pure_probe_readonly"]=digest(final)==old and store.root.joinpath("checkpoint.json").read_bytes()==before
        costs={"requests":ep["request_count"],"request_units":sum(r.get("request_cost_units",0) for r in receipts),
            "eligible_checks":eligible,"committed_attempts":accounted,"normal_physical_verifier_calls":physical,
            "admissions":len(current["acquired"]),"budget_denied_replies":sum(r["status"]=="verification_budget_exhausted" for r in receipts),
            "exhaustion_transitions":sum(bool(r.get("receiver_exhaustion_transition")) for r in receipts),"messages":len(receipts)}
        row={"checks":checks,"case":case,"costs":costs,"snapshot":a.snapshot(current),"pids":pids}
        atomic_json(root/"case-results.json",row); return row,final,predictions
    finally:
        if process is not None and process.poll() is None: halt(store,process)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True); parser.add_argument("--preservation-context",required=True); args=parser.parse_args()
    root=Path(args.output); root.mkdir(parents=True,exist_ok=False)
    context=json.loads(Path(args.preservation_context).read_text()); preservation.verify_current(context,Path.cwd())
    sha=preservation.file_hash(args.preservation_context); shutil.copy2(args.preservation_context,root/"current-preservation-context.json")
    for name in context["files"]:
        target=root/"archive"/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(name,target)
    atomic_json(root/"archive-manifest.json",context["files"])
    atomic_json(root/"configuration.json",{"cases":CASES,"policy_guarantee":"checkpoint-accounted only; physical rollback repeats permitted","model_calls":0})
    atomic_json(root/"provenance.json",{"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        "working_tree":subprocess.check_output(["git","status","--short"],text=True),"python":sys.version,"protocol_sha256":preservation.file_hash(PROTOCOL),
        "preservation_kind":preservation.KIND,"preservation_context_sha256":sha,"model_calls":0})
    result={"restarted":{},"uninterrupted":{},"comparisons":{},"model_calls":0}; states={}; predictions={}
    try:
        for case in CASES:
            for mode in a.MODES:
                name=mode+"-"+case["id"]
                for continuous in (False,True):
                    branch="uninterrupted" if continuous else "restarted"
                    row,state,pred=run_case(root/branch/name,mode,case,continuous,root,sha)
                    result[branch][name]=row; states[branch,name]=state; predictions[branch+"/"+name]=pred
                left=states["restarted",name]; right=states["uninterrupted",name]
                result["comparisons"][name+"-restart"]=left["judgment"]==right["judgment"] and left["questions"]==right["questions"] and semantic(left)==semantic(right) and left["birth"]==right["birth"]
            left=states["restarted",a.MODES[0]+"-"+case["id"]]; right=states["restarted",a.MODES[1]+"-"+case["id"]]
            result["comparisons"][case["id"]+"-memory"]=a.scientific(left["judgment"])==a.scientific(right["judgment"]) and left["questions"]==right["questions"] and semantic(left)==semantic(right)
        atomic_json(root/"frozen-predictions.json",predictions)
        for branch in ("restarted","uninterrupted"):
            for name,row in result[branch].items():
                pred=predictions[branch+"/"+name]
                groups={"equality":quality(pred,list(f.HELD)[:4]),"non_equality":quality(pred,list(f.HELD)[4:8]),"overall":quality(pred,list(f.HELD)[:8])}
                expected={"equality":(4,3),"non_equality":(4,3),"overall":(8,6)} if row["case"]["admissions"] else {"equality":(0,0),"non_equality":(4,3),"overall":(4,3)}
                row["groups"]=groups; row["quality_checks"]={g:(m["decided"],m["correct"])==expected[g] for g,m in groups.items()}
        preservation.pinned_current(root,Path.cwd(),sha)
        result["comparisons"]["full_archive"]=all(preservation.file_hash(name)==h==preservation.file_hash(root/"archive"/name) for name,h in context["files"].items())
        integrity=list(result["comparisons"].values())+[v for branch in ("restarted","uninterrupted") for row in result[branch].values() for v in row["checks"].values()]
        quality_checks=[v for branch in ("restarted","uninterrupted") for row in result[branch].values() for v in row["quality_checks"].values()]
        result.update(integrity_passed=sum(integrity),integrity_total=len(integrity),quality_passed=sum(quality_checks),quality_total=len(quality_checks))
        atomic_json(root/"results.json",result); print(json.dumps({k:v for k,v in result.items() if k.endswith(("passed","total"))}))
        if not all(integrity+quality_checks): raise AssertionError("Frozen receiver-budget checks failed; preserve result")
    except Exception as exc: atomic_json(root/"failure.json",{"error":repr(exc)}); raise


if __name__=="__main__": main()
