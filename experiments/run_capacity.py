"""Preregistered finite capacity relationship experiment; zero inference."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import time
from lmft_lab import capacity as c, capacity_fixture as f, capacity_relations as r
from lmft_lab.runtime_store import Store,atomic_json,digest
from run_comparative import start,halt,check_boundary
from run_correction import send


def message(mid,op,record):
    return {"schema_version":1,"id":mid,"sender":"fixture-operator","source":f.SOURCE,"type":"observation",
            "content":{"text":"Registered capacity evidence or bounded control.","operation":op,"record":deepcopy(record)}}


def training_messages():
    items=[message(eid,"outcome",f.outcome(eid,"train")) for eid in f.TRAIN]
    original=deepcopy(items[0]);items += [deepcopy(original) for _ in range(5)]
    for i in range(5):
        copy=deepcopy(original);copy["id"]="copy-"+str(i);items.append(copy)
    conflict=f.outcome("t1","train");conflict["success"]=False
    # Submitted allegation, not executed held-out truth. Gate must reject it regardless of value.
    hidden={"evidence_id":"h1","split":"heldout","procedure":f.PROCEDURE,"length":1,"capacity":4,"success":False}
    items += [message("conflict","outcome",conflict),message("heldout-injection","outcome",hidden),
        message("malformed-proposal","proposal",{"code":"arbitrary code is not permitted"}),
        message("external-proposal","proposal",r.candidates()[1]),message("select","select",{})]
    items += [message(eid,"outcome",f.outcome(eid,"validation")) for eid in f.VALIDATION]
    items += [message("before-accept","evaluate",f.case("h1")),message("accept","accept",{})]
    return items


def resources(store,state):
    current=state["judgment"]
    return {"checkpoint_bytes":(store.root/"checkpoint.json").stat().st_size,
        "individual_bytes":sum(p.stat().st_size for p in store.root.rglob("*") if p.is_file()),
        "processing_seconds":sum(x.get("processing_seconds",0) for x in state["receipts"]),"model_calls":0,
        "counts":{"train":len(current["evidence"]["train"]),"validation":len(current["evidence"]["validation"]),
            "candidate_evaluations":len(current["selection"]["candidate_evaluations"]) if current["selection"] else 0,
            "accepted_relationships":int(current["accepted_relationship"] is not None),"rejected_inputs":len(current["rejected"]),
            "coarse_revisions":len(current["coarse"]["revisions"]),"evaluations":len(current["evaluations"]),
            **{k:len(state[k]) for k in ("receipts","outbox","questions","diagnostics")}}}


def semantic(state):
    # The predictor name is an explicit condition label; all other scientific output must match.
    result=deepcopy(state["outbox"])
    for out in result:
        out.pop("timestamp",None)
        if "result" in out["content"]:out["content"]["result"].pop("predictor",None)
    return result


def quality(predictions,ids):
    rows=[]
    for eid in ids:
        case=f.case(eid);label=f.execute(case["length"],case["capacity"])
        p=predictions[eid];decided=p["decision"] in ("success","failure")
        rows.append({"case_id":eid,"prediction":p,"actual_success":label,"decided":decided,
            "correct":decided and (p["decision"]=="success")==label})
    n=len(rows);decided=sum(x["decided"] for x in rows);correct=sum(x["correct"] for x in rows)
    return {"cases":rows,"total":n,"decided":decided,"correct":correct,"abstentions":n-decided,
            "accuracy":correct/decided if decided else None,"coverage":decided/n}


def run_case(root,mode,uninterrupted=False):
    store=Store(root/"individual");process=None;checks={};stages={};began=time.perf_counter()
    try:
        process=start(store.root,mode,new=True);checks["live_inspection_denied"]=check_boundary(store)
        send(store,process,training_messages())
        if not uninterrupted:
            accepted=halt(store,process);process=None
            atomic_json(root/"accepted-halted.json",accepted);stages["accepted"]=resources(store,accepted)
            process=start(store.root,mode);restored=halt(store,process);process=None
            checks["exact_restart"]=restored==accepted
            process=start(store.root,mode)
        send(store,process,[message("probe-"+eid,"evaluate",f.case(eid)) for eid in f.HELD])
        final=halt(store,process);process=None
        atomic_json(root/"final-halted.json",final);stages["final"]=resources(store,final)
        current=final["judgment"]
        outputs={o["reply_to"]:o for o in final["outbox"]}
        predictions={eid:outputs["probe-"+eid]["content"]["result"] for eid in f.HELD}
        # Publish the complete prediction set before evaluating any held-out outcome.
        atomic_json(root/"frozen-predictions.json",predictions)
        receipts={}
        for item in final["receipts"]:receipts.setdefault(item.get("message_id"),item)
        checks["verified_evidence_counts"]=set(current["evidence"]["train"])==set(f.TRAIN) and set(current["evidence"]["validation"])==set(f.VALIDATION)
        checks["coarse_unchanged_rule"]=current["coarse"]["score"]==0 and len(current["coarse"]["revisions"])==6 and len(current["coarse"]["evidence"])==6
        checks["lookup_counts"]=len(current["lookup"])==6 and all(abs(v["score"])==1/3 for v in current["lookup"].values())
        checks["duplicates"]=sum(x["status"]=="duplicate" for x in final["receipts"])==5 and sum(x["status"]=="duplicate_evidence" for x in final["receipts"])==5
        checks["unsupported_inputs_rejected"]=all(receipts[eid]["status"]=="rejected" for eid in ("conflict","heldout-injection","malformed-proposal","external-proposal"))
        checks["no_hidden_evidence"]=not (set(current["evidence"]["train"])|set(current["evidence"]["validation"]))&set(f.HELD)
        checks["scope_guard"]=predictions["x1"]["decision"]=="out_of_scope"
        checks["no_model_traces"]=not final["diagnostics"] and not final["questions"]
        old=digest(final)
        for eid in f.HELD:assert c.predict(current,f.case(eid))==predictions[eid]
        checks["probe_read_only"]=digest(final)==old
        if mode in c.LEARNERS:
            selection=current["selection"];relation=current["accepted_relationship"]
            checks["unique_le"]=selection["selected"]["op"]=="le" and len(selection["consistent"])==1
            checks["five_inconsistent_rejected"]=sum(not x["consistent"] for x in selection["candidate_evaluations"])==5
            checks["training_only_selection"]=selection==r.select(c.records(current,"train")) and selection["training_refs"]==sorted(f.TRAIN)
            checks["four_validation_checks"]=len(current["acceptance"]["checks"])==4 and current["acceptance"]["accepted"]
            checks["relationship_provenance"]=relation["derivation"]==selection and relation["validation"]==current["acceptance"] and relation["applicability"]==r.SCOPE and relation["accepted_by"]=="accept"
            checks["behavioral_consequence"]=outputs["before-accept"]["content"]["result"]["decision"]=="abstain" and predictions["h1"]["decision"]=="success"
            checks["prediction_trace"]=all(p["relationship_ref"]==relation["id"] and p["trace"]["representation"]==relation["representation"] for eid,p in predictions.items() if eid!="x1")
        else:checks["no_learned_rule_claim"]=current["accepted_relationship"] is None and current["selection"] is None
        if not uninterrupted:
            checks["birth_preserved"]=final["birth"]==accepted["birth"]
            checks["heldout_cannot_change_accepted_state"]=all(current[k]==accepted["judgment"][k] for k in ("evidence","coarse","lookup","selection","acceptance","accepted_relationship"))
        groups={"seen":quality(predictions,f.SEEN),"unseen":quality(predictions,f.UNSEEN),"shift":quality(predictions,f.SHIFT),
                "equality":quality(predictions,[eid for eid,pair in f.HELD.items() if pair[0]==pair[1]])}
        expected={}
        for group,metrics in groups.items():
            count=0 if mode=="capacity-aggregate" else (len(f.SEEN) if group=="seen" else 1 if group=="equality" else 0) if mode=="capacity-lookup" else metrics["total"]
            expected[group]=(metrics["decided"],metrics["correct"])==(count,count)
        row={"mode":mode,"checks":checks,"quality_checks":expected,"groups":groups,"stages":stages,
            "wall_seconds":time.perf_counter()-began,"selection":current["selection"],"acceptance":current["acceptance"]}
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
    atomic_json(root/"configuration.json",{"rule":c.RULE,"modes":c.MODES,"candidates":r.candidates(),"scope":r.SCOPE,
        "train":f.TRAIN,"validation":f.VALIDATION,"heldout_observables":f.HELD,"model_calls":0,"seed":42})
    results={"restarted":{},"uninterrupted":{},"comparisons":{}};states={};mechanical=[];quality_checks=[]
    try:
        for mode in c.MODES:
            for continuous in (False,True):
                name="uninterrupted" if continuous else "restarted"
                row,state=run_case(root/name/mode,mode,continuous)
                results[name][mode]=row;states[name,mode]=state
                mechanical.extend(row["checks"].values());quality_checks.extend(row["quality_checks"].values())
            a=states["restarted",mode];b=states["uninterrupted",mode]
            results["comparisons"][mode+"-restart"]=(a["judgment"]==b["judgment"] and semantic(a)==semantic(b) and a["birth"]==b["birth"])
        a=states["restarted","capacity-lmft"];b=states["restarted","capacity-memory"]
        results["comparisons"]["memory_equal_access_and_results"]=(a["judgment"]["selection"]==b["judgment"]["selection"] and a["judgment"]["accepted_relationship"]==b["judgment"]["accepted_relationship"] and semantic(a)==semantic(b))
        mechanical.extend(results["comparisons"].values())
        results.update(integrity_passed=sum(mechanical),integrity_total=len(mechanical),quality_passed=sum(quality_checks),quality_total=len(quality_checks))
        atomic_json(root/"results.json",results)
        print(json.dumps({k:v for k,v in results.items() if k.endswith(("passed","total"))}))
        if not all(mechanical+quality_checks):raise AssertionError("Frozen capacity checks failed; preserve outcome")
    except Exception as exc:
        atomic_json(root/"failure.json",{"error":repr(exc)});raise

if __name__=="__main__":main()
