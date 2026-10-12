"""Preregistered one-request investigation through actual runtime processes."""
import argparse
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import shutil
import subprocess
import sys
from lmft_lab import active_relationship as a, insufficiency as s, insufficiency_fixture as f, ambiguity
from lmft_lab import preservation_context as preservation
from lmft_lab.birth import create_birth_state
from lmft_lab.runtime_store import Store, atomic_json, digest
from run_comparative import start, halt, check_boundary
from run_correction import send
from run_insufficiency import quality
from run_passive_relationship import semantic

PROTOCOL=Path("experiments/ACTIVE_ACQUISITION_PROTOCOL_V1_2.md")
CONDITIONS=(("ambiguous","disagreement"),("ambiguous","noninformative"),("ambiguous","unavailable"),
            ("supported","disagreement"),("unsupported","disagreement"))
EXPECTED_OPS={
    ("ambiguous","disagreement"):["le"],("ambiguous","noninformative"):["lt","le"],
    ("ambiguous","unavailable"):["lt","le"],("supported","disagreement"):["le"],("unsupported","disagreement"):[]}
EXPECTED_QUALITY={
    ("ambiguous","disagreement"):{"equality":(4,3),"non_equality":(4,3),"overall":(8,6)},
    ("ambiguous","noninformative"):{"equality":(0,0),"non_equality":(4,3),"overall":(4,3)},
    ("ambiguous","unavailable"):{"equality":(0,0),"non_equality":(4,3),"overall":(4,3)},
    ("supported","disagreement"):{"equality":(4,3),"non_equality":(4,3),"overall":(8,6)},
    ("unsupported","disagreement"):{"equality":(0,0),"non_equality":(0,0),"overall":(0,0)}}


def quality_expectations(row):
    return EXPECTED_QUALITY[row["scenario"],row["policy"]]


def message(mid,op,record,reply_to=None,source=f.SOURCE):
    result={"schema_version":1,"id":mid,"sender":"fixture-operator","source":source,
        "type":"teacher_reply" if reply_to else "observation","content":{"text":"Bounded relationship investigation; claims need verification.","operation":op,"record":deepcopy(record)}}
    if reply_to: result["reply_to"]=reply_to
    return result


def service_record(request,scenario):
    case=request["content"]["candidate"]
    return {"episode_id":request["content"]["episode_id"],"request_id":request["id"],"evidence":{
        "evidence_id":case["case_id"],"scenario":scenario,"split":"acquisition","procedure":f.PROCEDURE,
        "length":case["length"],"capacity":case["capacity"],"success":f.execute(case["length"],case["capacity"])}}


def invalid_replies(request,scenario):
    candidate=request["content"]["candidate"]
    allegation={"episode_id":request["content"]["episode_id"],"request_id":request["id"],"evidence":{
        "evidence_id":candidate["case_id"],"scenario":scenario,"split":"acquisition","procedure":f.PROCEDURE,
        "length":candidate["length"],"capacity":candidate["capacity"],"success":False}}
    variants=[]
    for mid,change in (("wrong-episode",{"episode_id":"other-episode"}),("wrong-request",{"request_id":"out-other"})):
        variants.append(message(mid,"verification",{**allegation,**change},request["id"]))
    variants += [message("wrong-source","verification",allegation,request["id"],"external"),
                 message("wrong-envelope-correlation","verification",allegation,"out-other")]
    bad=deepcopy(allegation); bad["evidence"]["length"]=8
    variants.append(message("wrong-candidate","verification",bad,request["id"]))
    bad=deepcopy(allegation); bad["evidence"]["success"]=1
    variants.append(message("malformed-value","verification",bad,request["id"]))
    variants += [message("malformed-verification","verification",{"unexpected":"payload"},request["id"]),
                 message("false-label","verification",allegation,request["id"])]
    return variants


def standalone(scenario,policy,observations):
    state=s.newborn("memory",scenario)
    for eid in f.TRAIN[scenario]: s.admit(state,f.outcome(scenario,eid,"train"))
    s.select(state); retained=deepcopy(state["survivors"])
    selection=None
    if len(retained)>1:
        ids=("q1","q4") if policy=="unavailable" else tuple(a.QUERIES)
        selection=ambiguity.choose(retained,[ambiguity.case(eid,a.QUERIES[eid]) for eid in ids])
        if policy=="noninformative": selection["selected"]=ambiguity.case("q1",a.QUERIES["q1"])
    expected_selected=selection["selected"]["case_id"] if selection and selection["selected"] else None
    if set(observations)!=(set() if expected_selected is None else {expected_selected}): raise AssertionError("standalone budget/selection mismatch")
    retained=ambiguity.filter_hypotheses(retained,observations)
    for eid in f.VALIDATION: s.admit(state,f.outcome(scenario,eid,"validation"))
    checks=[{"hypothesis":deepcopy(h),"evidence_id":eid,"predicted":s.evaluate(h,s.case(eid,(r["length"],r["capacity"]))),"observed":r["success"]}
            for h in retained for eid,r in state["evidence"]["validation"].items()]
    accepted=bool(retained) and all(c["predicted"]==c["observed"] for c in checks)
    acceptance={"accepted":accepted,"reason":"no_supported_hypothesis" if not retained else "validated_retained_set" if accepted else "validation_rejected",
        "hypotheses":deepcopy(retained),"checks":checks,"validation_digest":digest(state["evidence"]["validation"]),"acquisition_refs":sorted(observations)}
    state["phase"]="evaluation"
    return {"learner":state,"survivors":retained,"support_status":s.support_status(retained),"acceptance":acceptance}


def run_case(root,mode,scenario,policy,uninterrupted,context_root,context_sha):
    store=Store(root/"individual"); process=None; pids=[]; checks={}; training=None
    extra=("--relationship-scenario",scenario,"--acquisition-policy",policy)
    def launch(new=False):
        preservation.pinned_current(context_root,Path.cwd(),context_sha)
        proc=start(store.root,mode,new=new,extra_args=extra); pids.append(proc.pid); return proc
    def recover(stage):
        nonlocal process
        state=halt(store,process); process=None; atomic_json(root/(stage+"-halted.json"),state)
        process=launch(); restored=halt(store,process); process=None
        checks[stage+"_restart_exact"]=restored==state
        process=launch(); return state
    try:
        process=launch(True); checks["live_inspection_denied"]=check_boundary(store)
        original=message("t1","outcome",f.outcome(scenario,"t1","train"))
        bad=deepcopy(original); bad["id"]="false-training"; bad["content"]["record"]["success"]=False
        send(store,process,[message("untrained","evaluate",s.case("before",(1,4))),bad,
            *[message(eid,"outcome",f.outcome(scenario,eid,"train")) for eid in f.TRAIN[scenario]],
            deepcopy(original),message("training-copy","outcome",original["content"]["record"]),
            message("select","select",{}),message("investigate","investigate",{}),message("initial-barrier","barrier",{})])
        requests=[o for o in store.receive() if o["type"]=="clarification_request"]
        request=requests[0] if requests else None
        if not uninterrupted: training=recover("pending")
        before=[message("before-invalid","evaluate",s.case("invariant",(1,4))),
            message("second-investigate","investigate",{}),message("reset","reset_episode",{}),
            message("second-select","select",{}),message("early-accept","accept",{})]
        if request: before += [message("early-validation","outcome",f.outcome(scenario,"v1","validation")),*invalid_replies(request,scenario)]
        else: before += [message("unsolicited","verification",{"episode_id":"unrelated","request_id":"out-none","evidence":{}},"out-none")]
        send(store,process,before+[message("after-invalid","evaluate",s.case("invariant",(1,4))),message("invalid-barrier","barrier",{})])
        service_observations=0
        if request:
            record=service_record(request,scenario); service_observations=1
            reply=message("verified","verification",record,request["id"])
            conflict=deepcopy(reply); conflict["content"]["record"]["evidence"]["success"]=False
            copy=deepcopy(reply); copy["id"]="verification-copy"
            evidence_conflict=deepcopy(conflict); evidence_conflict["id"]="acquisition-conflict"
            wrong_source=deepcopy(copy); wrong_source.update(id="duplicate-wrong-source",source="external")
            send(store,process,[reply,deepcopy(reply),conflict,copy,evidence_conflict,wrong_source,
                message("post-reply-investigate","investigate",{}),message("resolved-unvalidated","evaluate",s.case("before-validation",(4,4))),
                message("reply-barrier","barrier",{})])
        else: send(store,process,[message("resolved-unvalidated","evaluate",s.case("before-validation",(4,4))),message("reply-barrier","barrier",{})])
        if not uninterrupted: replied=recover("replied")
        send(store,process,[*[message(eid,"outcome",f.outcome(scenario,eid,"validation")) for eid in f.VALIDATION],
            message("accept","accept",{}),message("before-evaluation","evaluate",s.case("constant",(1,4))),
            message("heldout-injection","outcome",{**f.outcome(scenario,"t1","train"),"split":"heldout","evidence_id":"h1"}),
            *[message("probe-"+eid,"evaluate",s.case(eid,pair)) for eid,pair in f.HELD.items()],
            message("after-evaluation","evaluate",s.case("constant",(1,4))),message("final-barrier","barrier",{})])
        final=halt(store,process); process=None; atomic_json(root/"final-halted.json",final)
        current=final["judgment"]; outputs={o["reply_to"]:o["content"] for o in final["outbox"] if o["type"]=="response"}
        predictions={eid:outputs["probe-"+eid]["result"] for eid in f.HELD}; atomic_json(root/"frozen-predictions.json",predictions)
        observed={eid:e["record"] for eid,e in current["acquired"].items()}; reference=standalone(scenario,policy,observed)
        atomic_json(root/"standalone-state.json",reference)
        ep=current["episode"]; expected_request=scenario=="ambiguous" and policy in ("disagreement","noninformative")
        checks.update({"standalone_parity":all(current[k]==reference[k] for k in reference),
            "frozen_effective_ops":[h["op"] for h in current["survivors"]]==EXPECTED_OPS[scenario,policy],
            "frozen_resolution":(len(current["survivors"])==1)==(len(EXPECTED_OPS[scenario,policy])==1),
            "request_count":ep["request_count"]==len(requests)==int(expected_request),
            "admitted_count":ep["verified_observations"]==len(current["acquired"])==int(expected_request),
            "episode_closed":ep["phase"]=="closed", "no_reset":ep["id"]==final["individual_id"]+":relationship-episode-1",
            "original_training_trace":current["learner"]["derivation"]==reference["learner"]["derivation"],
            "invalid_reply_invariance":outputs["before-invalid"]["scientific_digest"]==outputs["after-invalid"]["scientific_digest"] and outputs["before-invalid"]["questions_digest"]==outputs["after-invalid"]["questions_digest"],
            "unvalidated_abstention":outputs["resolved-unvalidated"]["result"]["decision"]=="abstain",
            "evaluation_invariance":outputs["before-evaluation"]["scientific_digest"]==outputs["after-evaluation"]["scientific_digest"] and outputs["before-evaluation"]["questions_digest"]==outputs["after-evaluation"]["questions_digest"],
            "untrained":outputs["untrained"]["result"]["reason"]=="untrained", "no_models":not final["diagnostics"],
            "scope":predictions["x1"]["decision"]=="out_of_scope", "policy_pinned":final["manifest"]["active_relationship_policy"]==a.policy(scenario,policy)})
        costs={"request_count":ep["request_count"],"request_cost_units":sum(r.get("request_cost_units",0) for r in final["receipts"]),
            "admitted_observations":len(current["acquired"]),"service_observations":service_observations,
            "receiver_verification_executions":sum(r.get("verification_executions",0) for r in final["receipts"]),
            "admitted_training_observations":len(current["learner"]["evidence"]["train"]),
            "admitted_validation_observations":len(current["learner"]["evidence"]["validation"]),
            "training_verification_executions":sum(r.get("reserved_verification_executions",0) for r in final["receipts"] if r.get("verification_split")=="train"),
            "validation_verification_executions":sum(r.get("reserved_verification_executions",0) for r in final["receipts"] if r.get("verification_split")=="validation")}
        checks["distinct_costs"]=costs=={"request_count":int(expected_request),"request_cost_units":int(expected_request),"admitted_observations":int(expected_request),
            "service_observations":int(expected_request),"receiver_verification_executions":2*int(expected_request),
            "admitted_training_observations":4,"admitted_validation_observations":4,
            "training_verification_executions":5,"validation_verification_executions":4}
        checks["single_admission"]=sum(r["status"]=="accepted_acquisition" for r in final["receipts"])==int(expected_request)
        checks["message_duplicates"]=sum(r["status"]=="duplicate" for r in final["receipts"])==1+int(expected_request)
        checks["identity_conflicts"]=sum(r["status"]=="id_conflict" for r in final["receipts"])==int(expected_request)
        if request:
            checks["selected_features"]=ep["selection"]["selected"]["case_id"]==("q1" if policy=="noninformative" else "q2")
            checks["answered_request"]=final["questions"][request["id"]]["answered_by"]=="verified" and final["questions"][request["id"]]["status"]=="answered"
            checks["provenance"]=all(e["reply_to"]==request["id"] and e["episode_id"]==ep["id"] and e["source"]==f.SOURCE for e in current["acquired"].values())
            if training: checks["pending_spent_survived"]=training["judgment"]["episode"]["request_count"]==1 and training["judgment"]["episode"]["phase"]=="pending" and training["questions"][request["id"]]["answered_by"] is None
        else: checks["no_question_or_acquisition"]=not final["questions"] and not current["acquired"]
        canonical=asdict(create_birth_state(final["individual_id"],birth_event_id=final["birth"]["birth_event_id"],random_seed=42))
        checks["birth_unchanged"]=digest(final["birth"])==digest(canonical)
        before=store.root.joinpath("checkpoint.json").read_bytes(); original_digest=digest(final)
        for eid,pair in f.HELD.items(): assert a.predict(current,s.case(eid,pair))==predictions[eid]
        summary=subprocess.run([sys.executable,"-m","lmft_lab.runtime","--root",str(store.root),"probe"],capture_output=True,text=True,check=True)
        checks["cli_probe"]=json.loads(summary.stdout)==a.snapshot(current)
        checks["pure_read_only"]=digest(final)==original_digest and store.root.joinpath("checkpoint.json").read_bytes()==before
        row={"checks":checks,"mode":mode,"scenario":scenario,"policy":policy,"snapshot":a.snapshot(current),"costs":costs,"pids":pids,"resolved":len(current["survivors"])==1}
        atomic_json(root/"case-results.json",row); return row,final,predictions
    finally:
        if process is not None and process.poll() is None: halt(store,process)


def controls(root,context_root,context_sha):
    preservation.pinned_current(context_root,Path.cwd(),context_sha)
    store=Store(root/"individual"); process=None
    try:
        process=start(store.root,a.MODES[0],new=True,control=True,extra_args=("--relationship-scenario","ambiguous"))
        send(store,process,[message("disabled-outcome","outcome",f.outcome("ambiguous","t1","train")),
            message("disabled-select","select",{}),message("disabled-investigate","investigate",{}),message("disabled-evaluate","evaluate",s.case("disabled",(1,4)))])
        state=halt(store,process); process=None; atomic_json(root/"disabled-halted.json",state)
        checks={"disabled_no_request":not state["questions"] and state["judgment"]["episode"]["request_count"]==0,
                "disabled_no_evidence":not state["judgment"]["learner"]["evidence"]["train"],
                "disabled_rejects":all(r["status"]=="rejected" and r["reason"]=="learning disabled" for r in state["receipts"][:3])}
        before=store.root.joinpath("checkpoint.json").read_bytes()
        command=[sys.executable,"-m","lmft_lab.runtime","--root",str(store.root),"start","--experiment",a.MODES[0],"--mode","fixture","--relationship-scenario","ambiguous","--learning-disabled","--acquisition-policy","noninformative"]
        result=subprocess.run(command,capture_output=True,text=True,timeout=15)
        checks["changed_policy_refused"]=result.returncode==1 and "Code/config/control changed" in result.stderr and store.root.joinpath("checkpoint.json").read_bytes()==before
        atomic_json(root/"changed-policy.json",{"returncode":result.returncode,"stderr":result.stderr}); return checks
    finally:
        if process is not None and process.poll() is None: halt(store,process)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True); parser.add_argument("--preservation-context",required=True); args=parser.parse_args()
    root=Path(args.output); root.mkdir(parents=True,exist_ok=False)
    context=json.loads(Path(args.preservation_context).read_text()); preservation.verify_current(context,Path.cwd())
    context_sha=preservation.file_hash(args.preservation_context); shutil.copy2(args.preservation_context,root/"current-preservation-context.json")
    manifest={}
    for name,h in context["files"].items():
        target=root/"archive"/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(name,target); manifest[name]=h
    atomic_json(root/"archive-manifest.json",manifest)
    atomic_json(root/"configuration.json",{"conditions":CONDITIONS,"policies":{scenario+"/"+policy:a.policy(scenario,policy) for scenario,policy in CONDITIONS},"model_calls":0})
    atomic_json(root/"provenance.json",{"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        "working_tree":subprocess.check_output(["git","status","--short"],text=True),"python":sys.version,"protocol_sha256":preservation.file_hash(PROTOCOL),
        "preservation_kind":preservation.KIND,"preservation_context_sha256":context_sha,"preservation_count":len(context["files"]),"model_calls":0})
    result={"restarted":{},"uninterrupted":{},"comparisons":{},"model_calls":0}; states={}; predictions={}
    try:
        for scenario,policy in CONDITIONS:
            for mode in a.MODES:
                name=mode+"-"+scenario+"-"+policy
                for uninterrupted in (False,True):
                    branch="uninterrupted" if uninterrupted else "restarted"
                    row,state,pred=run_case(root/branch/name,mode,scenario,policy,uninterrupted,root,context_sha)
                    result[branch][name]=row; states[branch,name]=state; predictions[branch+"/"+name]=pred
                l=states["restarted",name]; r=states["uninterrupted",name]
                result["comparisons"][name+"-restart"]=l["judgment"]==r["judgment"] and l["questions"]==r["questions"] and semantic(l)==semantic(r) and l["birth"]==r["birth"]
            l=states["restarted",a.MODES[0]+"-"+scenario+"-"+policy]; r=states["restarted",a.MODES[1]+"-"+scenario+"-"+policy]
            result["comparisons"][scenario+"-"+policy+"-memory"]=a.scientific(l["judgment"])==a.scientific(r["judgment"]) and l["questions"]==r["questions"] and semantic(l)==semantic(r)
        atomic_json(root/"frozen-predictions.json",predictions)
        result["controls"]=controls(root/"controls",root,context_sha)
        for branch in ("restarted","uninterrupted"):
            for name,row in result[branch].items():
                pred=predictions[branch+"/"+name]
                groups={"equality":quality(pred,list(f.HELD)[:4]),"non_equality":quality(pred,list(f.HELD)[4:8]),"overall":quality(pred,list(f.HELD)[:8])}
                row["groups"]=groups
                expected=quality_expectations(row)
                row["quality_checks"]={g:(m["decided"],m["correct"])==expected[g] for g,m in groups.items()}
        preservation.pinned_current(root,Path.cwd(),context_sha)
        result["comparisons"]["complete_archive"]=all(preservation.file_hash(name)==h==preservation.file_hash(root/"archive"/name) for name,h in manifest.items())
        integrity=list(result["comparisons"].values())+list(result["controls"].values())+[v for branch in ("restarted","uninterrupted") for row in result[branch].values() for v in row["checks"].values()]
        quality_checks=[v for branch in ("restarted","uninterrupted") for row in result[branch].values() for v in row["quality_checks"].values()]
        result.update(integrity_passed=sum(integrity),integrity_total=len(integrity),quality_passed=sum(quality_checks),quality_total=len(quality_checks))
        atomic_json(root/"results.json",result); print(json.dumps({k:v for k,v in result.items() if k.endswith(("passed","total"))}))
        if not all(integrity+quality_checks): raise AssertionError("Frozen active checks failed; preserve outcome")
    except Exception as exc:
        atomic_json(root/"failure.json",{"error":repr(exc)}); raise


if __name__=="__main__": main()
