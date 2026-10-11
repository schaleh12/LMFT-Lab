"""Preregistered attention study. Live access is outbox/lifecycle only."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import time
from lmft_lab import attention as a, attention_fixture as f
from lmft_lab.runtime_store import Store, atomic_json
from run_comparative import start, halt, wait_for, check_boundary


def message(identifier,op,record,reply=None):
    result={"schema_version":1,"id":identifier,"source":"registered-attention-1","sender":"teacher",
        "type":"teacher_reply" if reply else "observation","content":{"text":"Attributed fixture input.","operation":op,"record":record}}
    if reply:result["reply_to"]=reply
    return result


def send(store,process,items):
    for item in items:store.submit(item)
    wait_for(lambda:any(x["reply_to"]==items[-1]["id"] for x in store.receive()),process)


def exercise(store,process,key,malformed=False):
    request_message=message("case-"+key,"case",f.public_case(key))
    send(store,process,[request_message])
    out=next(x for x in store.receive() if x["reply_to"]==request_message["id"])
    if out["type"]!="clarification_request":return None
    # Only the selected public outbox request is given to the verifier.
    record=f.verify(key,out["content"]["candidate"])
    reply=message("reply-"+key,"verification",record,out["id"])
    if malformed:
        bad=deepcopy(reply);bad["id"]="bad-"+key;bad["content"]["record"]["value"]="unverified claim"
        send(store,process,[bad])
    send(store,process,[reply])
    return reply


def metrics(store,state):
    current=state["judgment"]
    return {"checkpoint_bytes":(store.root/"checkpoint.json").stat().st_size,
        "individual_bytes":sum(p.stat().st_size for p in store.root.rglob("*") if p.is_file()),
        "compute_seconds":sum(r.get("processing_seconds",0) for r in state["receipts"]),"model_calls":0,
        "counts":{**{k:len(current[k]) for k in ("cases","evidence","updates","rejected","outcomes")},
                  **{k:len(state[k]) for k in ("receipts","outbox","diagnostics","processed","questions")}}}


def quality(state,keys):
    cases=state["judgment"]["cases"]
    rows=[{"case_id":k,"route":cases[k]["selected"]["route"] if cases[k]["selected"] else None,
           "relevant":bool(cases[k]["selected"] and cases[k]["selected"]["field"]=="shielded"),
           "resolved":cases[k]["resolved"],"prediction":cases[k]["result"]["decision"],
           "actual_success":f.actual_success(k)} for k in keys]
    decided=[r for r in rows if r["prediction"]!="abstain"]
    correct=sum((r["prediction"]=="success")==r["actual_success"] for r in decided)
    return {"cases":rows,"relevant":sum(r["relevant"] for r in rows),
            "resolved":sum(r["resolved"] for r in rows),"unresolved":sum(not r["resolved"] for r in rows),
            "decided":len(decided),"correct":correct,"abstained":len(rows)-len(decided),
            "accuracy":correct/len(decided) if decided else None,
            "coverage":len(decided)/len(rows),
            "unnecessary_verifications":sum(r["route"] is not None and not r["resolved"] for r in rows)}


def run_condition(root,mode,uninterrupted=False):
    store=Store(root/"individual");process=None;checks={};stages={};started=time.perf_counter()
    try:
        process=start(store.root,mode,new=True)
        checks["live_inspection_refused"]=check_boundary(store)
        initial=halt(store,process);stages["initial"]=metrics(store,initial)
        checks["initial_abstain"]=a.decision(initial["judgment"],True)["decision"]=="abstain"
        process=start(store.root,mode)
        send(store,process,[message(k,"outcome",f.training_record(k)) for k in list(f.contextual.TRIALS)[:8]])
        exercise(store,process,"p1")
        t1=exercise(store,process,"t1",malformed=True)
        exercise(store,process,"t2")
        if not uninterrupted:
            trained=halt(store,process);stages["trained"]=metrics(store,trained)
            atomic_json(root/"trained-halted.json",trained)
            process=start(store.root,mode);restored=halt(store,process)
            checks["restart_exact"]=restored==trained
            process=start(store.root,mode)
        else: trained=None
        # A new-ID case request cannot spend another verification budget.
        send(store,process,[message("budget-repeat","case",f.public_case("t1"))])
        # Repetition has no output of its own; an explicit barrier is the completion ack.
        copies=[]
        for i in range(5):
            copy=deepcopy(t1);copy["id"]="copy-"+str(i);copies.append(copy)
        send(store,process,copies+[deepcopy(t1) for _ in range(5)]+[message("repeat-barrier","barrier",{})])
        if not uninterrupted:
            repeated=halt(store,process);stages["repeated"]=metrics(store,repeated)
            checks["dedup_no_learning"]=repeated["judgment"]==trained["judgment"]
            checks["dedup_no_traces"]=repeated["diagnostics"]==trained["diagnostics"]
            checks["no_extra_requests"]=repeated["questions"]==trained["questions"]
            process=start(store.root,mode)
        for key in ("h1","h2","h3","h4","h5","n1"):exercise(store,process,key)
        final=halt(store,process);process=None
        stages["final"]=metrics(store,final)
        atomic_json(root/"final-halted.json",final)
        current=final["judgment"];held=quality(final,["h1","h2","h3","h4","h5"])
        learning=mode in ("attention-lmft","attention-memory")
        checks["weights"]=current["weights"]==(dict(A=.25,B=.75,D=.5) if learning else dict(A=.5,B=.5,D=.5))
        checks["heldout_counts"]=(held["decided"],held["correct"],held["resolved"])==((4,2,4) if learning else (0,0,0))
        checks["training_only_learning"]=all(u["evidence_id"].split("/")[0] in ("t1","t2") for u in current["updates"] if u["accepted"])
        checks["malformed_rejected"]=any(r.get("message_id")=="bad-t1" and r["status"]=="rejected" for r in final["receipts"])
        checks["one_request_per_case"]=len(final["questions"])==8
        checks["no_independent_conflict_abstains"]=current["cases"]["n1"]["selected"] is None
        checks["existing_counter_scores"]=[b["score"] for b in current["branches"].values()]==[1/3,-1/3]
        checks["seed_unchanged"]=final["birth"]==initial["birth"]
        return {"checks":checks,"stages":stages,"prelearning":quality(final,["p1"]),
                "heldout":held,"wall_seconds":time.perf_counter()-started,"weights":current["weights"]},final
    finally:
        if process is not None and process.poll() is None:halt(store,process)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);args=parser.parse_args()
    root=Path(args.output);root.mkdir(parents=True,exist_ok=False)
    files=sorted(set(Path("src").rglob("*.py"))|set(Path("tests").rglob("*.py"))|set(Path("config").rglob("*.json"))|
        {Path("experiments/ATTENTION_PROTOCOL.md"),Path(__file__),Path("experiments/run_comparative.py")})
    hashes={}
    for source in files:
        relative=source.relative_to(Path.cwd()) if source.is_absolute() else source
        target=root/"archive"/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        hashes[str(relative)]=hashlib.sha256(source.read_bytes()).hexdigest()
    atomic_json(root/"archive-manifest.json",hashes)
    results={"conditions":{},"checks":{}};states={}
    try:
        for mode in a.MODES:
            results["conditions"][mode],states[mode]=run_condition(root/mode,mode)
        result,uninterrupted=run_condition(root/"uninterrupted","attention-lmft",True)
        results["uninterrupted"]=result
        results["checks"]["restart_uninterrupted_judgment"]=states["attention-lmft"]["judgment"]==uninterrupted["judgment"]
        results["checks"]["restart_uninterrupted_questions"]=states["attention-lmft"]["questions"]==uninterrupted["questions"]
        results["checks"]["baseline_equivalence"]=all(results["conditions"]["attention-lmft"][k]==results["conditions"]["attention-memory"][k] for k in ("prelearning","heldout","weights"))
        results["checks"]["causal_counterfactual"]=states["attention-lmft"]["judgment"]["cases"]["p1"]["selected"]["route"]=="A" and states["attention-disabled"]["judgment"]["cases"]["p1"]["selected"]["route"]=="D"
        checks=list(results["checks"].values())+[v for c in results["conditions"].values() for v in c["checks"].values()]+list(result["checks"].values())
        results["passed"]=sum(checks);results["total"]=len(checks)
        atomic_json(root/"results.json",results)
        print(json.dumps({"passed":sum(checks),"total":len(checks),"output":str(root)}))
        if not all(checks):raise AssertionError("Experiment check failed; inspect preserved results")
    except Exception as exc:
        atomic_json(root/"failure.json",{"error":repr(exc)});raise

if __name__=="__main__":main()
