"""Finite zero-model continuation experiment with real runtime processes."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import time
from lmft_lab import outcome_correction as c, outcome_fixture as f
from lmft_lab.runtime_store import Store, atomic_json, digest
from continuation_inputs import SCENARIOS, CONDITIONS, initial, batches, message
from run_comparative import start, halt, check_boundary
from run_correction import send, lineage_valid
from run_outcome_correction import metrics, semantic_outbox


def run_case(root,name,condition):
    mode="outcome-memory" if condition=="memory" else "outcome-lmft"
    extra=("--freeze-outcomes-after-correction",) if condition=="frozen" else ()
    store=Store(root/"individual");process=None;checks={};stages={};began=time.perf_counter()
    def launch(new=False):return start(store.root,mode,new=new,extra_args=extra)
    try:
        process=launch(True);checks["live_inspection_denied"]=check_boundary(store)
        send(store,process,initial(name))
        if condition!="uninterrupted":
            repaired=halt(store,process);process=None
            atomic_json(root/"corrected-halted.json",repaired);stages["corrected"]=metrics(store,repaired)
            process=launch();restored=halt(store,process);process=None
            checks["restart_exact"]=restored==repaired
            process=launch()
        for label,items in batches(name):
            send(store,process,items)
        final=halt(store,process);process=None
        atomic_json(root/"final-halted.json",final);stages["final"]=metrics(store,final)
        current=final["judgment"];spec=SCENARIOS[name];key=spec["key"];frozen=condition=="frozen"
        # Post-halt only: reconstruct checks from committed receipts/outbox and immutable traces.
        receipts={}
        for receipt in final["receipts"]:
            receipts.setdefault(receipt.get("message_id"),receipt)
        outputs={o["reply_to"]:o for o in final["outbox"]}
        def result(mid):return outputs[mid]["content"]["result"]
        def triple(r):return (r["score"],r["count"],r["decision"])
        corrected=spec["corrected"]
        checks["corrected_expected"]=triple(result("corrected"))==(float(corrected[0]),*corrected[1:])
        event=current["corrections"][0]
        checks["correction_count_fixed"]=event["before"]["outcome_count"]==event["after"]["outcome_count"]
        checks["one_accepted_correction"]=len(current["corrections"])==1 and event["accepted"]
        observations=[]
        for i,expected in enumerate(spec["expected"]):
            expected=corrected if frozen else expected
            actual=result("stage-"+str(i))
            checks["stage-"+str(i)+"-arithmetic"]=triple(actual)==(float(expected[0]),*expected[1:])
            checks["stage-"+str(i)+"-cache"]=receipts["stage-"+str(i)]["status"]==("evaluation_cache_hit" if frozen else "evaluated")
            checks["stage-"+str(i)+"-repeat"]=receipts["stage-repeat-"+str(i)]["status"]=="evaluation_cache_hit"
            source,index=spec["events"][i];record=f.initial_records(source)[index]
            checks["stage-"+str(i)+"-identity"]=((record["event_id"] in current["heads"])== (not frozen))
            observations.append({"event_id":record["event_id"],"input":record,"expected_score":str(expected[0]),
                "expected_count":expected[1],"expected_decision":expected[2],"observed":actual,
                "receipt":receipts["new-"+str(i)]})
        for label in ("after-duplicates","after-conflicts"):
            checks[label+"-unchanged"]=result(label)==result("stage-0") and receipts[label]["status"]=="evaluation_cache_hit"
        checks["exact_duplicates"]=sum(r["status"]=="duplicate" for r in final["receipts"])==5
        checks["reattributed_duplicates"]=all(receipts["copy-"+str(i)]["status"]==("rejected" if frozen else "duplicate_evidence") for i in range(5))
        checks["conflicting_identity"]=receipts["identity-conflict"]["reason"]=="conflicting evidence identity"
        checks["alias_rejected"]=receipts["identity-alias"]["status"]=="rejected"
        checks["scope_rejected"]=receipts["outside-scope"]["status"]=="rejected"
        checks["target_scope_isolation"]=result("after-other-target")==result("after-scope-target")==result("stage-"+str(len(spec["events"])-1))
        checks["target_scope_cache"]=receipts["after-other-target"]["status"]==receipts["after-scope-target"]["status"]=="evaluation_cache_hit"
        checks["other_branch"]=triple(result("after-other-branch"))==((1/3,1,"success") if frozen else (.5,2,"success"))
        checks["other_branch_cache"]=receipts["after-other-branch"]["status"]==("evaluation_cache_hit" if frozen else "evaluated")
        checks["lineage"]=lineage_valid(current) and current["heads"][key+"/event-1"]=="replacement/"+key+"-a"
        checks["originals_preserved"]=all(current["ledger"][r["evidence_id"]]["record"]==r for r in f.initial_records(key))
        checks["exact_root_count"]=len(current["heads"])==len(f.initial_records(key))+(0 if frozen else len(spec["events"])+1)
        checks["one_replacement"]=len(current["ledger"])==len(current["heads"])+1
        checks["no_duplicate_recomputation"]=len(current["recomputations"])==len(current["heads"])+1
        checks["unchanged_routes"]=current["weights"]==dict(A=.25,B=.75,D=.5)
        checks["questions_match_criterion"]=all((q["status"]=="open")== (not c.predict(current,current["cases"][q["case_id"]]["input"])["resolved"]) for q in final["questions"].values())
        checks["one_request_per_case"]=all(sum(q["case_id"]==k for q in final["questions"].values())<=1 for k in current["cases"])
        if name=="same-category":
            qid=current["cases"]["o12-warm"]["request"];q=final["questions"][qid]
            checks["closed_then_reopened"]=qid in event["closed_questions"] and q["status"]==("resolved_by_correction" if frozen else "open")
            if not frozen:checks["new_evidence_reopen_ref"]=q["reopened_by"]=="o8/event-1"
        if condition!="uninterrupted":
            checks["birth_preserved"]=final["birth"]==repaired["birth"]
            if frozen:checks["control_retains_corrected_state"]=c.state_ref(current)==c.state_ref(repaired["judgment"])
        prior=digest(final);probes=[c.predict(current,f.public_case(key,v)) for v in ("fresh-1","fresh-2")]
        checks["probe_read_only"]=digest(final)==prior
        checks["fresh_response_consistent"]=all(result(v)==p for v,p in zip(("fresh-1","fresh-2"),probes))
        checks["fresh_payloads_unseen"]=all(p["payload"] not in {e["record"].get("payload") for e in current["ledger"].values()} for p in probes)
        decided=sum(p["decision"]!="abstain" for p in probes)
        correct=sum(p["decision"]!="abstain" and (p["decision"]=="success")==f.actual_success(key,v) for v,p in zip(("fresh-1","fresh-2"),probes))
        row={"scenario":name,"condition":condition,"initial":result("initial-probe"),"corrected":result("corrected"),
            "continuation":observations,"final":c.snapshot(current),"decided":decided,"correct":correct,"abstentions":2-decided,
            "accepted_new":0 if frozen else len(spec["events"])+1,"rejected_inputs":sum(r["status"]=="rejected" for r in final["receipts"]),
            "checks":checks,"stages":stages,"wall_seconds":time.perf_counter()-began}
        atomic_json(root/"case-results.json",row)
        return row,final
    finally:
        if process is not None and process.poll() is None:halt(store,process)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);args=parser.parse_args()
    root=Path(args.output);root.mkdir(parents=True,exist_ok=False)
    paths=set(Path("src").rglob("*.py"))|set(Path("tests").rglob("*.py"))|set(Path("config").rglob("*.json"))|set(Path("experiments").glob("*.py"))|set(Path("experiments").glob("*.md"))|set(Path("docs").glob("*.md"))|{Path("AGENTS.md")}
    hashes={}
    for p in sorted(paths):
        target=root/"archive"/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
        hashes[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
    atomic_json(root/"archive-manifest.json",hashes)
    atomic_json(root/"configuration.json",{"conditions":CONDITIONS,"scenarios":list(SCENARIOS),"model_calls":0,"policy":c.load_policy(),"seed":42})
    results={"conditions":{},"comparisons":{}};states={};checks=[]
    try:
        for condition in CONDITIONS:
            rows=[]
            for name in SCENARIOS:
                row,state=run_case(root/condition/name,name,condition);rows.append(row);states[condition,name]=state;checks.extend(row["checks"].values())
            summary={k:sum(r[k] for r in rows) for k in ("decided","correct","abstentions","accepted_new","rejected_inputs")}
            summary.update(accuracy=summary["correct"]/summary["decided"],coverage=summary["decided"]/6,
                model_calls=0,checkpoint_bytes=sum(r["stages"]["final"]["checkpoint_bytes"] for r in rows),
                processing_seconds=sum(r["stages"]["final"]["processing_seconds"] for r in rows),
                roots=sum(len(states[condition,n]["judgment"]["heads"]) for n in SCENARIOS),
                ledger_records=sum(len(states[condition,n]["judgment"]["ledger"]) for n in SCENARIOS))
            results["conditions"][condition]={"cases":rows,"summary":summary}
            results["comparisons"][condition+"-quality"]=(summary["decided"],summary["correct"],summary["abstentions"])==((4,2,2) if condition=="frozen" else (2,1,4))
            results["comparisons"][condition+"-counts"]=(summary["roots"],summary["ledger_records"])==((10,13) if condition=="frozen" else (19,22))
        for name in SCENARIOS:
            a=states["restarted",name];b=states["uninterrupted",name];m=states["memory",name]
            results["comparisons"][name+"-restart-uninterrupted"]=(a["judgment"]==b["judgment"] and a["questions"]==b["questions"] and semantic_outbox(a)==semantic_outbox(b))
            results["comparisons"][name+"-memory"]=(c.state_ref(a["judgment"])==c.state_ref(m["judgment"]) and a["questions"]==m["questions"] and semantic_outbox(a)==semantic_outbox(m))
        checks.extend(results["comparisons"].values());results.update(passed=sum(checks),total=len(checks))
        atomic_json(root/"results.json",results)
        print(json.dumps({"passed":sum(checks),"total":len(checks),"output":str(root)}))
        if not all(checks):raise AssertionError("Frozen experiment checks failed; preserve results")
    except Exception as exc:
        atomic_json(root/"failure.json",{"error":repr(exc)});raise

if __name__=="__main__":main()
