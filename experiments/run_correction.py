"""Frozen correction experiment: communication while live, diagnostics after halt."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import time
from lmft_lab import correction as c,correction_fixture as f,contextual
from lmft_lab.runtime_store import Store,atomic_json
from run_comparative import start,halt,wait_for,check_boundary


def message(identifier,op,record):
    return {"schema_version":1,"id":identifier,"sender":f.AUTHORITY,"source":f.SOURCE,"type":"observation",
            "content":{"text":"Instrument record or proposed correction; verify independently.","operation":op,"record":record}}


def send(store,process,items):
    for item in items:store.submit(item)
    wait_for(lambda:any(out["reply_to"]==items[-1]["id"] for out in store.receive()),process)


def metrics(store,state):
    current=state["judgment"]
    return {"checkpoint_bytes":(store.root/"checkpoint.json").stat().st_size,
            "individual_bytes":sum(p.stat().st_size for p in store.root.rglob("*") if p.is_file()),
            "compute_seconds":sum(r.get("processing_seconds",0) for r in state["receipts"]),"model_calls":0,
            "counts":{**{k:len(current[k]) for k in ("ledger","heads","corrections","correction_index","cache","outcomes")},
                      **{k:len(state[k]) for k in ("receipts","processed","diagnostics","questions","outbox")}}}


def lineage_valid(current):
    for root,head in current["heads"].items():
        seen=set();node=head
        while node!=root:
            if node in seen or node not in current["ledger"]:return False
            seen.add(node);entry=current["ledger"][node]
            if entry["root"]!=root:return False
            node=entry["parent"]
        if current["ledger"][root]["parent"] is not None:return False
    return True


def run_case(root,mode,key,uninterrupted=False):
    store=Store(root/"individual");process=None;checks={};stages={};began=time.perf_counter()
    try:
        process=start(store.root,mode,new=True);checks["boundary"]=check_boundary(store)
        items=[message("prior-"+k,"outcome",contextual.outcome(k)) for k in list(contextual.TRIALS)[:8]]
        items += [message("initial-"+str(i),"evidence",record) for i,record in enumerate(f.initial_records(key))]
        items += [message("before","evaluate",f.public_case(key)),message("before-cache","evaluate",f.public_case(key))]
        send(store,process,items)
        if not uninterrupted:
            before=halt(store,process);stages["before"]=metrics(store,before)
            atomic_json(root/"before-halted.json",before)
            process=start(store.root,mode);restored=halt(store,process)
            checks["restart_exact"]=restored==before
            process=start(store.root,mode)
        repairs=[message("correction-"+str(i),"correction",r) for i,r in enumerate(f.corrections(key))]
        send(store,process,repairs+[message("correction-barrier","barrier",{})])
        if key=="c8":
            pre_repeat=halt(store,process);stages["pre_repeat"]=metrics(store,pre_repeat)
            process=start(store.root,mode)
            copies=[]
            for i in range(5):
                item=deepcopy(repairs[0]);item["id"]="copy-"+str(i);copies.append(item)
            send(store,process,copies+[deepcopy(repairs[0]) for _ in range(5)]+[message("repeat-barrier","barrier",{})])
            repeated=halt(store,process);stages["repeated"]=metrics(store,repeated)
            checks["duplicates_no_state_change"]=repeated["judgment"]==pre_repeat["judgment"]
            checks["duplicates_no_trace_or_questions"]=repeated["diagnostics"]==pre_repeat["diagnostics"] and repeated["questions"]==pre_repeat["questions"]
            process=start(store.root,mode)
        send(store,process,[message("after","evaluate",f.public_case(key)),message("after-cache","evaluate",f.public_case(key)),message("final-barrier","barrier",{})])
        final=halt(store,process);process=None;stages["final"]=metrics(store,final)
        atomic_json(root/"final-halted.json",final)
        current=final["judgment"];case=f.public_case(key)
        initial=current["cases"][key]["evaluations"][0]["result"];result=c.predict(current,case)
        events=current["corrections"];accepted=sum(e["accepted"] for e in events)
        checks["originals_immutable"]=all(current["ledger"][r["evidence_id"]]["record"]==r for r in f.initial_records(key))
        checks["independent_count"]=len(current["heads"])==len(f.initial_records(key))
        checks["lineage"]=lineage_valid(current)
        checks["rejection_invariance"]=all(e["before"]==e["after"] and not e["cache_invalidated"] and not e["closed_questions"] for e in events if not e["accepted"])
        checks["no_extra_samples"]=len(current["ledger"])==len(current["heads"])+accepted
        checks["one_request"]=len(final["questions"])<=1
        checks["counters_fixed"]=[b["score"] for b in current["branches"].values()]==[1/3,-1/3]
        checks["weights_fixed"]=current["weights"]==dict(A=.25,B=.75,D=.5)
        receipts={v.get("message_id"):v for v in final["receipts"]}
        should_invalidate=accepted>0 and key!="c12"
        checks["cache_freshness"]=receipts["after"]["status"]==("evaluated" if should_invalidate else "evaluation_cache_hit")
        checks["cache_repeat"]=receipts["before-cache"]["status"]==receipts["after-cache"]["status"]=="evaluation_cache_hit"
        checks["wording_fresh"]=all(out["content"]["result"]==result for out in final["outbox"] if out["reply_to"] in ("after","after-cache"))
        checks["no_inappropriate_closure"]=all(c.circuit.support(c.effective(current),case,q["question"])["resolved"] for q in final["questions"].values() if q["status"]=="resolved_by_correction")
        if not uninterrupted:checks["birth_preserved"]=final["birth"]==before["birth"]
        requests=[ev for ev in current["cases"][key]["evaluations"] if ev["selected"] and ev["budget_available"]]
        redundant=sum(ev["result"]["support"][ev["selected"]["field"]]["resolved"] for ev in requests)
        decided=result["decision"]!="abstain"
        row={"case_id":key,"initial":initial,"final":result,"accepted":accepted,"rejected":len(events)-accepted,
             "decided":decided,"correct":decided and (result["decision"]=="success")==f.actual_success(key),
             "actual_success":f.actual_success(key),"verification_requests":len(requests),"redundant":redundant,
             "useful":len(requests)-redundant,"closed_questions":sum(q["status"]=="resolved_by_correction" for q in final["questions"].values()),
             "pending_questions":sum(q["status"]=="open" for q in final["questions"].values()),
             "effective_independent":len(current["heads"]),"stored_observations":len(current["ledger"]),
             "checks":checks,"stages":stages,"wall_seconds":time.perf_counter()-began}
        return row,final
    finally:
        if process is not None and process.poll() is None:halt(store,process)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);args=parser.parse_args()
    root=Path(args.output);root.mkdir(parents=True,exist_ok=False)
    paths=set(Path("src").rglob("*.py"))|set(Path("tests").rglob("*.py"))|set(Path("config").rglob("*.json"))|set(Path("experiments").glob("*RESULTS.md"))
    paths|={Path("experiments/CORRECTION_PROTOCOL.md"),Path("experiments/run_correction.py"),Path("experiments/run_comparative.py")}
    hashes={}
    for source in sorted(paths):
        target=root/"archive"/source;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        hashes[str(source)]=hashlib.sha256(source.read_bytes()).hexdigest()
    atomic_json(root/"archive-manifest.json",hashes)
    atomic_json(root/"configuration.json",{"version":c.RULE,"conditions":c.MODES,"cases":f.IDS,
        "correction_policy":c.load_policy(),"mapping":"consistent-support-1","weights":dict(A=.25,B=.75,D=.5),"verification_budget":1,"model_calls":0})
    results={"conditions":{},"checks":{},"uninterrupted":{}};states={};checks=[]
    try:
        for mode in c.MODES:
            rows=[]
            for key in f.IDS:
                row,state=run_case(root/mode/key,mode,key);rows.append(row);checks.extend(row["checks"].values())
                if key=="c11":states[mode]=state
            summary={k:sum(int(row[k]) for row in rows) for k in ("accepted","rejected","decided","correct","verification_requests","redundant","useful","closed_questions","pending_questions","effective_independent","stored_observations")}
            summary.update(abstentions=12-summary["decided"],accuracy=summary["correct"]/summary["decided"],coverage=summary["decided"]/12)
            results["conditions"][mode]={"cases":rows,"summary":summary}
            continuous,final=run_case(root/"uninterrupted"/mode,mode,"c11",True)
            results["uninterrupted"][mode]=continuous;checks.extend(continuous["checks"].values())
            results["checks"][mode+"-uninterrupted"]=states[mode]["judgment"]==final["judgment"] and states[mode]["questions"]==final["questions"]
            results["checks"][mode+"-quality"]=(summary["decided"],summary["correct"])==((3,1) if mode=="correction-disabled" else (7,6))
            expected=0 if mode=="correction-disabled" else 11
            results["checks"][mode+"-acceptance"]=summary["accepted"]==expected
        results["checks"]["baseline_equivalence"]=results["conditions"]["correction-lmft"]["summary"]==results["conditions"]["correction-memory"]["summary"]
        checks.extend(results["checks"].values());results.update(passed=sum(checks),total=len(checks))
        atomic_json(root/"results.json",results)
        print(json.dumps({"passed":sum(checks),"total":len(checks),"output":str(root)}))
        if not all(checks):raise AssertionError("Experiment checks failed; preserve results")
    except Exception as exc:
        atomic_json(root/"failure.json",{"error":repr(exc)});raise

if __name__=="__main__":main()
