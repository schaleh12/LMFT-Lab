"""Preregistered zero-inference outcome repair; inspect only halted individuals."""
import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import time
from lmft_lab import outcome_correction as c, outcome_fixture as f
from lmft_lab.runtime_store import Store, atomic_json, digest
from run_comparative import start, halt, check_boundary
from run_correction import send, lineage_valid


def message(identifier, op, record):
    return {"schema_version":1,"id":identifier,"sender":f.AUTHORITY,"source":f.SOURCE,"type":"observation",
            "content":{"text":"Attributed instrument report or proposed correction; verify independently.","operation":op,"record":record}}


def metrics(store,state):
    current=state["judgment"]
    return {"checkpoint_bytes":(store.root/"checkpoint.json").stat().st_size,
        "individual_bytes":sum(p.stat().st_size for p in store.root.rglob("*") if p.is_file()),
        "processing_seconds":sum(r.get("processing_seconds",0) for r in state["receipts"]),"model_calls":0,
        "counts":{**{k:len(current[k]) for k in ("ledger","heads","corrections","correction_index","recomputations","cache")},
                  **{k:len(state[k]) for k in ("receipts","processed","questions","diagnostics","outbox")}},
        "effective_outcomes":c.state_ref(current)["outcome_count"]}


def semantic_outbox(state):
    return [{k:v for k,v in out.items() if k!="timestamp"} for out in state["outbox"]]


def run_case(root,mode,key,uninterrupted=False):
    store=Store(root/"individual");process=None;checks={};stages={};began=time.perf_counter()
    try:
        process=start(store.root,mode,new=True);checks["communication_boundary"]=check_boundary(store)
        items=[message("initial-"+str(i),"evidence",r) for i,r in enumerate(f.initial_records(key))]
        for variant in ("warm","other"):
            items += [message("before-"+variant,"evaluate",f.public_case(key,variant)),
                      message("before-repeat-"+variant,"evaluate",f.public_case(key,variant))]
        send(store,process,items)
        if not uninterrupted:
            before=halt(store,process);process=None;stages["before"]=metrics(store,before)
            atomic_json(root/"before-halted.json",before)
            process=start(store.root,mode)
        repairs=[message("repair-"+str(i),"correction",r) for i,r in enumerate(f.corrections(key))]
        send(store,process,repairs+[message("repair-barrier","barrier",{})])
        if not uninterrupted:
            repaired=halt(store,process);process=None;stages["repaired"]=metrics(store,repaired)
            atomic_json(root/"repaired-halted.json",repaired)
            process=start(store.root,mode);restored=halt(store,process);process=None
            checks["exact_restart"]=restored==repaired
            process=start(store.root,mode)
        if key=="o8":
            copies=[]
            for i in range(5):
                item=deepcopy(repairs[0]);item["id"]="copy-"+str(i);copies.append(item)
            send(store,process,[deepcopy(repairs[0]) for _ in range(5)]+copies+[message("repeat-barrier","barrier",{})])
            repeated=halt(store,process);process=None;stages["repeated"]=metrics(store,repeated)
            atomic_json(root/"repeated-halted.json",repeated)
            checks["duplicates_no_learning"]=repeated["judgment"]==repaired["judgment"]
            checks["duplicates_no_questions_or_diagnostics"]=repeated["questions"]==repaired["questions"] and repeated["diagnostics"]==repaired["diagnostics"]
            process=start(store.root,mode)
        items=[message("after-warm","evaluate",f.public_case(key)),message("after-repeat","evaluate",f.public_case(key)),
               message("after-other","evaluate",f.public_case(key,"other"))]
        items += [message("after-"+variant,"evaluate",f.public_case(key,variant)) for variant in ("fresh-1","fresh-2")]
        send(store,process,items+[message("final-barrier","barrier",{})])
        final=halt(store,process);process=None;stages["final"]=metrics(store,final)
        atomic_json(root/"final-halted.json",final)
        current=final["judgment"];events=current["corrections"];accepted=sum(e["accepted"] for e in events)
        initial=current["cases"][key+"-warm"]["evaluations"][0]["result"]
        result=c.predict(current,f.public_case(key));ref=c.state_ref(current)
        expected_scores={"o1":-1/3,"o3":1/3,"o4":0,"o5":-1/3,"o6":-1/3,"o7":-1/3,"o12":.5}
        checks["expected_score"]=result["score"]==(initial["score"] if mode=="outcome-disabled" else expected_scores.get(key,1/3))
        checks["originals_immutable"]=all(current["ledger"][r["evidence_id"]]["record"]==r for r in f.initial_records(key))
        checks["one_head_per_event"]=len(current["heads"])==len(f.initial_records(key)) and ref["outcome_count"]==sum(r["kind"]=="outcome" for r in f.initial_records(key))
        checks["lineage"]=lineage_valid(current)
        checks["one_record_per_accepted_replacement"]=len(current["ledger"])==len(current["heads"])+accepted
        checks["rejection_invariance"]=all(e["before"]==e["after"] and not e["cache_invalidated"] and not e["closed_questions"] for e in events if not e["accepted"])
        checks["exact_arithmetic"]=all(b["score"]==float(Fraction(len(b["supporting"])-len(b["contradicting"]),b["count"]+2)) for b in ref["branches"].values())
        checks["scope_isolation"]=ref["branches"]["unshielded"]["score"]==1/3 and ref["branches"]["unshielded"]["count"]==1
        checks["fixed_routes"]=current["weights"]==dict(A=.25,B=.75,D=.5)
        receipts={r.get("message_id"):r for r in final["receipts"]}
        checks["affected_cache"]=receipts["after-warm"]["status"]==("evaluated" if accepted else "evaluation_cache_hit")
        checks["unaffected_and_repeat_cache"]=all(receipts[k]["status"]=="evaluation_cache_hit" for k in ("after-other","after-repeat","before-repeat-warm","before-repeat-other"))
        checks["fresh_wording"]=all(out["content"]["result"]==c.predict(current,f.public_case(key,variant)) for variant in ("warm","fresh-1","fresh-2") for out in final["outbox"] if out["reply_to"]=="after-"+variant)
        checks["question_criteria"]=all((q["status"]=="open") == (not c.predict(current,current["cases"][q["case_id"]]["input"])["resolved"]) for q in final["questions"].values())
        checks["question_budget"]=all(sum(q["case_id"]==k for q in final["questions"].values())<=1 for k in current["cases"])
        prior=digest(current)
        probes=[c.predict(current,f.public_case(key,v)) for v in ("fresh-1","fresh-2")]
        checks["read_only_probe"]=digest(current)==prior
        if not uninterrupted:checks["birth_preserved"]=final["birth"]==before["birth"]
        correct=sum(p["decision"]!="abstain" and (p["decision"]=="success")==f.actual_success(key,v) for p,v in zip(probes,("fresh-1","fresh-2")))
        row={"case_id":key,"initial":initial,"final":result,"accepted":accepted,"rejected":len(events)-accepted,
             "effective_outcomes":ref["outcome_count"],"ledger_records":len(current["ledger"]),
             "decided":sum(p["decision"]!="abstain" for p in probes),"correct":correct,
             "decision_changed":initial["decision"]!=result["decision"],"score_changed":initial["score"]!=result["score"],
             "pending_questions":sum(q["status"]=="open" for q in final["questions"].values()),
             "closed_questions":sum(q["status"]=="resolved_by_correction" for q in final["questions"].values()),
             "checks":checks,"stages":stages,"wall_seconds":time.perf_counter()-began}
        return row,final
    finally:
        if process is not None and process.poll() is None:halt(store,process)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);args=parser.parse_args()
    root=Path(args.output);root.mkdir(parents=True,exist_ok=False)
    paths=set(Path("src").rglob("*.py"))|set(Path("tests").rglob("*.py"))|set(Path("config").rglob("*.json"))|set(Path("experiments").glob("*.md"))
    paths|={Path("experiments/run_outcome_correction.py"),Path("experiments/run_correction.py"),Path("experiments/run_comparative.py"),Path("AGENTS.md"),Path("docs/EVIDENCE_LEARNING_HANDOFF.md")}
    hashes={}
    for source in sorted(paths):
        target=root/"archive"/source;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        hashes[str(source)]=hashlib.sha256(source.read_bytes()).hexdigest()
    atomic_json(root/"archive-manifest.json",hashes)
    atomic_json(root/"configuration.json",{"rule":c.RULE,"conditions":c.MODES,"cases":f.IDS,"policy":c.load_policy(),"model_calls":0,"seed":42})
    results={"conditions":{},"uninterrupted":{},"checks":{}};states={};checks=[]
    try:
        for mode in c.MODES:
            rows=[]
            for key in f.IDS:
                row,state=run_case(root/mode/key,mode,key);rows.append(row);checks.extend(row["checks"].values())
                states[mode,key]=state
            summary={k:sum(int(r[k]) for r in rows) for k in ("accepted","rejected","effective_outcomes","ledger_records","decided","correct","decision_changed","score_changed","pending_questions","closed_questions")}
            summary.update(abstentions=24-summary["decided"],accuracy=summary["correct"]/summary["decided"],coverage=summary["decided"]/24,
                model_calls=0,processing_seconds=sum(r["stages"]["final"]["processing_seconds"] for r in rows),
                checkpoint_bytes=sum(r["stages"]["final"]["checkpoint_bytes"] for r in rows),
                individual_bytes=sum(r["stages"]["final"]["individual_bytes"] for r in rows))
            results["conditions"][mode]={"cases":rows,"summary":summary}
            for key in ("o11","o12"):
                row,state=run_case(root/"uninterrupted"/mode/key,mode,key,True)
                results["uninterrupted"][mode+"-"+key]=row;checks.extend(row["checks"].values())
                other=states[mode,key]
                results["checks"][mode+"-"+key+"-uninterrupted"]=(state["judgment"]==other["judgment"] and state["questions"]==other["questions"] and semantic_outbox(state)==semantic_outbox(other))
            results["checks"][mode+"-acceptance"]=(summary["accepted"],summary["rejected"])==((0,19) if mode=="outcome-disabled" else (10,9))
            results["checks"][mode+"-quality"]=(summary["decided"],summary["correct"],summary["abstentions"])==(22,11,2)
            results["checks"][mode+"-counts"]=(summary["effective_outcomes"],summary["ledger_records"])==(31,32 if mode=="outcome-disabled" else 42)
        results["checks"]["memory_equivalence"]=all(c.state_ref(states["outcome-lmft",k]["judgment"])==c.state_ref(states["outcome-memory",k]["judgment"]) and semantic_outbox(states["outcome-lmft",k])==semantic_outbox(states["outcome-memory",k]) for k in f.IDS)
        checks.extend(results["checks"].values());results.update(passed=sum(checks),total=len(checks))
        atomic_json(root/"results.json",results)
        print(json.dumps({"passed":sum(checks),"total":len(checks),"output":str(root)}))
        if not all(checks):raise AssertionError("Experiment checks failed; preserve results")
    except Exception as exc:
        atomic_json(root/"failure.json",{"error":repr(exc)});raise

if __name__=="__main__":main()
