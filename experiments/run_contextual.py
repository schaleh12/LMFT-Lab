"""Frozen contextual experiment; supervised files only, diagnostics after halt."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import time

from lmft_lab import contextual as c
from lmft_lab.runtime_store import Store, atomic_json, digest
from run_comparative import start, halt, check_boundary, wait_for


def message(identifier, operation, record, reply=None):
    item = {"schema_version":1,"id":identifier,"sender":"codex","source":"registered-transmission-fixture",
            "type":"teacher_reply" if reply else "observation",
            "content":{"text":"Recorded fixture information.","operation":operation,"record":record}}
    if reply: item["reply_to"] = reply
    return item


def training():
    return [message("outcome-"+key,"outcome",c.outcome(key)) for key in list(c.TRIALS)[:8]]


def evaluations():
    return [message("eval-"+key,"evaluate",c.case(key, key.startswith("m")))
            for key in list(c.CASES)]


def send(store, process, items):
    for item in items: store.submit(item)
    last = items[-1]["id"]
    wait_for(lambda:any(m["reply_to"]==last for m in store.receive()),process)


def question_ids(outbox):
    return {m["content"]["evaluation"]["case_id"]:m["id"] for m in outbox if m["type"]=="clarification_request"}


def answers(refs, invalid=False):
    if invalid:
        return [message("irrelevant","condition",{"evidence_id":"condition/m2","case_id":"m2","shielded":False},refs["m1"]),
                message("malformed","condition",{"evidence_id":"condition/m1","case_id":"m1","shielded":"true"},refs["m1"])]
    return [message("answer-"+key,"condition",{"evidence_id":"condition/"+key,"case_id":key,"shielded":c.CASES[key][1]},refs[key]) for key in ("m1","m2")]


def repeats():
    return ([message(f"retransmit-{i}","outcome",c.outcome("s1")) for i in range(5)]
        + [training()[0] for _ in range(5)] + [message("repeat-barrier","barrier",{})])


def contrary():
    changed=c.outcome("s1");changed["output"]=9
    return [message("conflict","outcome",changed),message("cache-1","evaluate",c.case("h1")),
        message("cache-2","evaluate",c.case("h1"))]+[
        message(key,"outcome",c.outcome(key)) for key in ("c1","c2","c3","c4")]+[
        message("after-contrary","evaluate",c.case("h1"))]


def quality(state):
    current=state["judgment"]
    before=digest(current)
    result={}
    for group,keys in (("known",[f"h{i}" for i in range(1,7)]),("missing",["m1","m2"]),("scope",["x1","x2"])):
        cases=[]
        for key in keys:
            outcome=c.probe(current,c.case(key,group=="missing"))
            payload,shielded,disturbance=c.CASES[key]
            actual=c.execute(payload,shielded,disturbance)==payload
            cases.append({"id":key,"evaluation":outcome,"actual_success":actual if group!="scope" else None})
        decided=[x for x in cases if x["evaluation"]["decision"] in ("success","failure")]
        correct=sum((x["evaluation"]["decision"]=="success")==x["actual_success"] for x in decided)
        result[group]={"cases":cases,"decisions":len(decided),"correct":correct,
                       "withheld":sum(x["evaluation"]["decision"] in ("abstain","pending_condition") for x in cases),
                       "accuracy":correct/len(decided) if decided else None}
    assert before==digest(current)
    return result


def metrics(store,state,wall):
    current=state["judgment"]
    revisions=[r for b in current["branches"].values() for r in b["revisions"]]
    return {"quality":quality(state),"scores":c.probe(current)["scores"],"wall_seconds":wall,
        "compute_seconds":sum(r.get("processing_seconds",0) for r in state["receipts"]),
        "model_calls":len(state["diagnostics"]),
        "counts":{"evidence":len(current["evidence"]),"revisions":len(revisions),
                  "conditions":len(current["conditions"]),"cache":len(current["cache"]),"rejected":len(current["rejected"]),
                  **{k:len(state[k]) for k in ("receipts","outbox","diagnostics","processed","questions")}},
        "checkpoint_bytes":(store.root/"checkpoint.json").stat().st_size,
        "individual_bytes":sum(p.stat().st_size for p in store.root.rglob('*') if p.is_file())}


def retrieval(state):
    current=state["judgment"]
    for branch in current["branches"].values():
        for revision in branch["revisions"]:
            if not revision["reason"]:return False
            for key in revision["supporting"]+revision["contradicting"]:
                record=current["evidence"][key]
                if record["record"]!=c.outcome(key) or not record["source"] or not record["message_id"]:return False
    return True


def run_condition(root,name,mode,control=False):
    store=Store(root/name/"individual")
    process=start(store.root,mode,new=True,control=control)
    stages={};checks={}
    try:
        initial=halt(store,process);stages["initial"]=metrics(store,initial,0)
        started=time.perf_counter();process=start(store.root,mode,control=control)
        checks["boundary"]=check_boundary(store)
        send(store,process,training()+evaluations())
        pending=halt(store,process);stages["pending"]=metrics(store,pending,time.perf_counter()-started)
        refs=question_ids(pending["outbox"])
        atomic_json(root/name/"pending-halted.json",pending)
        process=start(store.root,mode,control=control)
        before=store.receive();time.sleep(.3)
        checks["idle_outbox"]=store.receive()==before
        restored=halt(store,process)
        checks["restart"]=restored["judgment"]==pending["judgment"] and restored["questions"]==pending["questions"]
        checks["idle_records"]=restored["receipts"]==pending["receipts"] and restored["diagnostics"]==pending["diagnostics"]
        started=time.perf_counter();process=start(store.root,mode,control=control)
        send(store,process,answers(refs,True));invalid=halt(store,process)
        checks["invalid_pending"]=all(q["answered_by"] is None for q in invalid["questions"].values())
        stages["invalid"]=metrics(store,invalid,time.perf_counter()-started)
        started=time.perf_counter();process=start(store.root,mode,control=control)
        send(store,process,answers(refs));clarified=halt(store,process)
        stages["clarified"]=metrics(store,clarified,time.perf_counter()-started)
        started=time.perf_counter();process=start(store.root,mode,control=control)
        send(store,process,repeats());repeated=halt(store,process)
        stages["repeated"]=metrics(store,repeated,time.perf_counter()-started)
        checks["repeat_no_learning"]=repeated["judgment"]["evidence"]==clarified["judgment"]["evidence"]
        if not control:
            checks["repeat_no_large_records"]=all(stages["repeated"]["counts"][key]==stages["clarified"]["counts"][key] for key in ("revisions","diagnostics","cache"))
        started=time.perf_counter();process=start(store.root,mode,control=control)
        send(store,process,contrary());final=halt(store,process)
        stages["final"]=metrics(store,final,time.perf_counter()-started)
        checks["retrieval"]=retrieval(final)
        receipts={x.get("message_id"):x for x in final["receipts"]}
        checks["cache_hit"]=receipts["cache-1"]["status"]=="evaluation_cache_hit" and receipts["cache-2"]["status"]=="evaluation_cache_hit"
        if not control:checks["cache_invalidation"]=receipts["after-contrary"]["status"]=="evaluated"
        checks["conflicting_id"]=receipts["conflict"]["status"]=="rejected"
        checks["scopes"]=all(x["evaluation"]["decision"]=="out_of_scope" for x in stages["pending"]["quality"]["scope"]["cases"])
        checks["missing_withheld"]=stages["pending"]["quality"]["missing"]["decisions"]==0
        expected_known=0 if mode=="context-aggregate" or control else 4
        checks["known_quality"]=stages["pending"]["quality"]["known"]["correct"]==expected_known
        checks["clarification_quality"]=stages["clarified"]["quality"]["missing"]["correct"]==(0 if mode=="context-aggregate" or control else 2)
        checks["pending_resolved"]=all(q["answered_by"] for q in final["questions"].values())
        checks["final_quality"]=stages["final"]["quality"]["known"]["correct"]==(0 if control else 3)
        expected_scores={"all":-2/7} if mode=="context-aggregate" else {"shielded":-.2,"unshielded":-1/3}
        checks["final_scores"]=stages["final"]["scores"]==({k:0 for k in expected_scores} if control else expected_scores)
        atomic_json(root/name/"final-halted.json",final)
        return {"stages":stages,"checks":checks,"judgment":final["judgment"],"questions":final["questions"]}
    finally:
        if process.poll() is None:store.stop();process.communicate(timeout=420)


def uninterrupted(root):
    store=Store(root/"uninterrupted/individual");process=start(store.root,"context-lmft",new=True)
    try:
        send(store,process,training()+evaluations());refs=question_ids(store.receive())
        send(store,process,answers(refs,True));send(store,process,answers(refs))
        send(store,process,repeats());send(store,process,contrary())
        return halt(store,process)
    finally:
        if process.poll() is None:store.stop();process.communicate(timeout=420)


def deterministic(root):
    results={name:run_condition(root,name,mode,control) for name,mode,control in (
        ("aggregate","context-aggregate",False),("memory","context-memory",False),
        ("lmft","context-lmft",False),("control","context-lmft",True))}
    checks={f"{name}:{key}":value for name,result in results.items() for key,value in result["checks"].items()}
    continuous=uninterrupted(root)
    checks["uninterrupted"]=continuous["judgment"]==results["lmft"]["judgment"] and continuous["questions"]==results["lmft"]["questions"]
    checks["conditional_equivalence"]=all(results["memory"]["stages"][stage]["quality"]==results["lmft"]["stages"][stage]["quality"] for stage in results["lmft"]["stages"])
    checks["zero_model_calls"]=all(r["stages"]["final"]["model_calls"]==0 for r in results.values())
    return {"execution":"deterministic-no-model","passed":all(checks.values()),"checks":checks,"conditions":results}


def local(root):
    store=Store(root/"individual");process=start(store.root,"context-lmft",new=True,local=True)
    started=time.perf_counter()
    try:
        boundary=check_boundary(store)
        send(store,process,training()+[message("known","evaluate",c.case("h1")),message("missing","evaluate",c.case("m1",True))])
        refs=question_ids(store.receive());before=store.receive();time.sleep(.3);idle=store.receive()==before
        send(store,process,[message("answer-m1","condition",{"evidence_id":"condition/m1","case_id":"m1","shielded":True},refs["m1"])])
        send(store,process,repeats())
        send(store,process,[message("cached-known","evaluate",c.case("h1"))]+[
            message(key,"outcome",c.outcome(key)) for key in ("c1","c2","c3","c4")]+[
            message("changed-known","evaluate",c.case("h1"))])
        state=halt(store,process)
        calls=state["diagnostics"]
        # Independent semantic field checks, not the rendering producer as oracle.
        faithful=True
        for output in state["outbox"]:
            content=output["content"]
            if "evaluation" not in content:continue
            evaluation=content["evaluation"];text=content["text"]
            if evaluation["decision"]=="pending_condition":
                faithful &= "shielded is missing" in text and "No prediction until clarified" in text
            else:
                faithful &= (f"prediction {evaluation['decision']}" in text and
                    f"score={evaluation['score']}" in text and
                    f"evidence={','.join(evaluation['evidence_refs']) or 'none'}" in text and "not a guarantee" in text)
        pids={call.get("server_pid") for call in calls}
        receipts={x.get("message_id"):x for x in state["receipts"]}
        checks={"four_actual_calls":len(calls)==4 and all(x["execution"]=="local" and x["status"]=="validated" for x in calls),
            "server_reuse":len(pids)==1 and None not in pids,"faithful_wording":bool(faithful),"boundary":boundary,"idle":idle,
            "duplicate_no_calls":all(receipts[f"retransmit-{i}"]["status"]=="duplicate_evidence" for i in range(5)),
            "cache_hit":receipts["cached-known"]["status"]=="evaluation_cache_hit",
            "cache_invalidated":receipts["changed-known"]["status"]=="evaluated",
            "correct_revision":state["judgment"]["branches"]["shielded"]["score"]==-.2}
        return {"execution":"actual-local-offline-constrained-wording","passed":all(checks.values()),"checks":checks,
                "metrics":metrics(store,state,time.perf_counter()-started),"calls":calls,"outbox":state["outbox"]}
    finally:
        if process.poll() is None:store.stop();process.communicate(timeout=420)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True);parser.add_argument('--local',action='store_true')
    args=parser.parse_args();root=Path(args.output);root.mkdir(parents=True,exist_ok=False)
    for pattern in ('src/lmft_lab/*.py','tests/*.py','config/local_models.json','experiments/run_contextual.py','experiments/run_comparative.py','experiments/CONTEXTUAL_PROTOCOL.md'):
        for source in Path('.').glob(pattern):
            destination=root/'source_snapshot'/source;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
    atomic_json(root/'archive_manifest.json',{str(p.relative_to(root/'source_snapshot')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'source_snapshot').rglob('*') if p.is_file()})
    started=time.perf_counter()
    try:
        result=local(root) if args.local else deterministic(root)
        result['total_wall_seconds']=time.perf_counter()-started;atomic_json(root/'result.json',result)
        print(json.dumps({'passed':result['passed'],'seconds':result['total_wall_seconds'],'failed':[k for k,v in result['checks'].items() if not v],'result':str(root/'result.json')}))
        return 0 if result['passed'] else 1
    except BaseException as exc:
        atomic_json(root/'failure.json',{'type':type(exc).__name__,'error':str(exc)});raise


if __name__=='__main__':raise SystemExit(main())
