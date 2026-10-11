"""Frozen scoped-support study; only outbox/lifecycle access during runtime."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import time
from lmft_lab import scoped_attention as s,scoped_fixture as f,contextual
from lmft_lab.runtime_store import Store,atomic_json
from run_comparative import start,halt,wait_for,check_boundary


def message(identifier,op,record,reply=None):
    result={"schema_version":1,"id":identifier,"source":f.SOURCE,"sender":"teacher",
        "type":"teacher_reply" if reply else "observation","content":{"text":"Attributed scoped fixture information.","operation":op,"record":record}}
    if reply:result["reply_to"]=reply
    return result


def send(store,process,items):
    for item in items:store.submit(item)
    wait_for(lambda:any(out["reply_to"]==items[-1]["id"] for out in store.receive()),process)


def initialize(store,process,key,contrary=True):
    training=[message("prior-"+k,"outcome",contextual.outcome(k)) for k in list(contextual.TRIALS)[:8]]
    evidence=[message("initial-"+str(i),"evidence",r) for i,r in enumerate(f.initial_records(key,contrary))]
    send(store,process,training+evidence+[message("initial-barrier","barrier",{})])
    return evidence


def evaluate(store,process,key,identifier):
    send(store,process,[message(identifier,"evaluate",f.public_case(key))])
    output=next(out for out in store.receive() if out["reply_to"]==identifier)
    if output["type"]=="clarification_request":
        # Retrieve only the selected question, never unselected truth.
        reply=message("answer-"+identifier,"verification",f.verify(key,output["content"]["candidate"]["field"]),output["id"])
        send(store,process,[reply])
    return output


def metrics(store,state):
    current=state["judgment"]
    return {"checkpoint_bytes":(store.root/"checkpoint.json").stat().st_size,
            "individual_bytes":sum(p.stat().st_size for p in store.root.rglob("*") if p.is_file()),
            "compute_seconds":sum(r.get("processing_seconds",0) for r in state["receipts"]),
            "model_calls":0,"counts":{**{k:len(current[k]) for k in ("ledger","changes","updates","outcomes","cases")},
                                       **{k:len(state[k]) for k in ("receipts","outbox","diagnostics","questions","processed")}}}


def score_case(state,key):
    current=state["judgment"];evaluation=current["cases"][key]["evaluations"][0]
    initial=evaluation["before"];selected=evaluation["selected"]
    final=s.predict(current,f.public_case(key));decision=final["decision"]
    unresolved=[field for field,v in initial["support"].items() if not v["resolved"]]
    field=selected["field"] if selected else None
    return {"case_id":key,"initial":initial,"final":final,"selected":field,
            "verification_calls":int(selected is not None),
            "redundant":int(field is not None and initial["support"][field]["resolved"]),
            "appropriate":int(field in unresolved),
            "inappropriate_suppression":int(bool(unresolved) and field is None),
            "missed_unresolved":int(bool(unresolved) and field not in unresolved),
            "fully_resolved":all(v["resolved"] for v in final["support"].values()),
            "decided":decision!="abstain","correct":decision!="abstain" and (decision=="success")==f.actual_success(key),
            "actual_success":f.actual_success(key)}


def primary(root,mode,key):
    store=Store(root/"individual");process=None;began=time.perf_counter()
    try:
        process=start(store.root,mode,new=True)
        boundary=check_boundary(store)
        initialize(store,process,key)
        evaluate(store,process,key,"evaluate")
        state=halt(store,process);process=None
        atomic_json(root/"final-halted.json",state)
        result=score_case(state,key);result["metrics"]=metrics(store,state);result["wall_seconds"]=time.perf_counter()-began
        expected="payload_valid" if key=="q1" and mode!="scoped-neither" else None if key in ("q4","q7") and mode in ("scoped-full","scoped-memory") else "shielded"
        result["checks"]={"boundary":boundary,"selection":result["selected"]==expected,
            "one_request":len(state["questions"])<=1,
            "weights_fixed":state["judgment"]["weights"]==dict(A=.25,B=.75,D=.5) and not state["judgment"]["updates"],
            "counter_scores_fixed":[b["score"] for b in state["judgment"]["branches"].values()]==[1/3,-1/3]}
        return result
    finally:
        if process is not None and process.poll() is None:halt(store,process)


def sequential(root,mode,uninterrupted=False):
    store=Store(root/"individual");process=None;checks={};stages={};began=time.perf_counter()
    try:
        process=start(store.root,mode,new=True);checks["boundary"]=check_boundary(store)
        originals=initialize(store,process,"q6",contrary=False)
        before_output=evaluate(store,process,"q6","before")
        if not uninterrupted:
            before=halt(store,process);stages["before"]=metrics(store,before)
            atomic_json(root/"before-halted.json",before)
            process=start(store.root,mode);restored=halt(store,process)
            checks["restart_exact"]=restored==before
            process=start(store.root,mode)
        repeats=[]
        for i in range(5):
            copy=deepcopy(originals[0]);copy["id"]="copy-"+str(i);repeats.append(copy)
        send(store,process,repeats+[deepcopy(originals[0]) for _ in range(5)]+[message("repeat-barrier","barrier",{})])
        if not uninterrupted:
            repeated=halt(store,process);stages["repeated"]=metrics(store,repeated)
            checks["dedup_science"]=repeated["judgment"]==before["judgment"]
            checks["dedup_traces"]=repeated["diagnostics"]==before["diagnostics"]
            checks["dedup_requests"]=repeated["questions"]==before["questions"]
            process=start(store.root,mode)
        send(store,process,[message("contrary","evidence",f.initial_records("q6")[-1])])
        after_output=evaluate(store,process,"q6","after")
        final=halt(store,process);process=None;stages["final"]=metrics(store,final)
        atomic_json(root/"final-halted.json",final)
        first_no_request=mode in ("scoped-full","scoped-memory")
        checks["initial_choice"]=(before_output["type"]!="clarification_request")==first_no_request
        checks["reopening_request_or_spent_budget"]=(after_output["type"]=="clarification_request")==first_no_request
        checks["conflict_retained"]=not s.support(final["judgment"],f.public_case("q6"),"shielded")["resolved"]
        checks["one_request"]=len(final["questions"])==1
        return {"checks":checks,"stages":stages,"wall_seconds":time.perf_counter()-began,
                "before_type":before_output["type"],"after_type":after_output["type"]},final
    finally:
        if process is not None and process.poll() is None:halt(store,process)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);args=parser.parse_args()
    root=Path(args.output);root.mkdir(parents=True,exist_ok=False)
    paths=set(Path("src").rglob("*.py"))|set(Path("tests").rglob("*.py"))|set(Path("config").rglob("*.json"))
    paths|={Path("experiments/SCOPED_ATTENTION_PROTOCOL.md"),Path("experiments/run_scoped_attention.py"),Path("experiments/run_comparative.py")}
    hashes={}
    for path in sorted(paths):
        target=root/"archive"/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
        hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
    atomic_json(root/"archive-manifest.json",hashes)
    atomic_json(root/"configuration.json",{"modes":s.MODES,"cases":f.IDS,"passes":2,"gain":.25,
        "fixed_weights":dict(A=.25,B=.75,D=.5),"verification_budget":1,"model_calls":0,"seed":42})
    result={"conditions":{},"sequential":{},"checks":{}};seqstates={};checks=[]
    try:
        for mode in s.MODES:
            rows=[primary(root/mode/key,mode,key) for key in f.IDS]
            summary={k:sum(int(row[k]) for row in rows) for k in ("verification_calls","redundant","appropriate","inappropriate_suppression","missed_unresolved","fully_resolved","decided","correct")}
            summary.update(abstentions=7-summary["decided"],accuracy=summary["correct"]/summary["decided"] if summary["decided"] else None,coverage=summary["decided"]/7)
            result["conditions"][mode]={"cases":rows,"summary":summary}
            for row in rows:checks.extend(row["checks"].values())
            result["sequential"][mode],seqstates[mode]=sequential(root/"sequential"/mode,mode)
            checks.extend(result["sequential"][mode]["checks"].values())
        reference=result["conditions"]["scoped-neither"]["summary"]["verification_calls"]
        for value in result["conditions"].values():value["summary"]["calls_saved_vs_neither"]=reference-value["summary"]["verification_calls"]
        result["uninterrupted"],continuous=sequential(root/"uninterrupted","scoped-full",True)
        checks.extend(result["uninterrupted"]["checks"].values())
        result["checks"]["restart_matches_uninterrupted"]=seqstates["scoped-full"]["judgment"]==continuous["judgment"] and seqstates["scoped-full"]["questions"]==continuous["questions"]
        result["checks"]["baseline_equivalence"]=result["conditions"]["scoped-full"]["summary"]==result["conditions"]["scoped-memory"]["summary"]
        for mode in s.MODES:
            value=result["conditions"][mode]["summary"]
            result["checks"][mode+"-quality"]=(value["decided"],value["correct"] )==((5,3) if mode=="scoped-neither" else (6,4))
        checks.extend(result["checks"].values());result.update(passed=sum(checks),total=len(checks))
        atomic_json(root/"results.json",result)
        print(json.dumps({"passed":sum(checks),"total":len(checks),"output":str(root)}))
        if not all(checks):raise AssertionError("Preserved experiment check failure")
    except Exception as exc:
        atomic_json(root/"failure.json",{"error":repr(exc)});raise

if __name__=="__main__":main()
