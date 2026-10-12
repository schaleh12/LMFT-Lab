"""Experiment-only downstream limits of unchanged Clarity->Execution wiring."""
import argparse
from copy import deepcopy
from dataclasses import asdict
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from lmft_lab import consistent_attention as circuit, attention, contextual, judgment
from lmft_lab import preservation_context as preservation
from lmft_lab.runtime_store import atomic_json,digest

PROTOCOL=Path("experiments/SEED_CONTRIBUTION_PROTOCOL.md")
MODES=("intact","ablated","scalar-intact","scalar-ablated")
# Public fixture definitions only: accepted evidence patterns, candidate routes/gates.
DEFS={"x1":("SC","PM","B","A",False,True),"x2":("SP","PM","B","A",True,True),
      "x3":("SM","PC","A","B",False,True),"x4":("SC","PR","B","A",False,True),
      "x5":("SM","PM","B","B",False,True),"x6":("SR","PM","A","B",False,True),
      "x7":("SR","PM","A","B",False,True),"x8":("SM","PR","A","B",False,True),
      "x9":("SR","PR","B","B",False,True),"x10":("SM","PM","B","B",False,False)}
_OUTCOMES={"x1":True,"x2":True,"x3":False,"x4":False,"x5":True,"x6":True,"x7":False,"x8":False,"x9":True,"x10":True}
EXPECTED_FIELDS={"intact":["shielded","shielded","payload_valid","shielded","shielded","payload_valid","payload_valid","shielded",None,None],
                 "ablated":["payload_valid","payload_valid","shielded","shielded","shielded","payload_valid","payload_valid","shielded",None,None]}
EXPECTED_GAIN={"intact":[0,0,0,0,1,1,1,1,0,0],"ablated":[1,1,1,0,1,1,1,1,0,0]}
EXPECTED_DECISIONS=["abstain"]*5+["success","success","failure","success","abstain"]
SOURCE="authored-seed-contribution-fixture-1"


def prior():
    state=circuit.newborn("consistent-full")
    # Frozen replay of historical authored samples; NOT new association learning.
    for eid in list(contextual.TRIALS)[:8]:
        record=contextual.outcome(eid); branch="shielded" if record["shielded"] else "unshielded"
        item={"id":"prior-"+eid,"sender":"fixture","source":"registered-contextual-prior","content":{"evidence":{"sample_id":eid,**record}}}
        state["branches"][branch],_=judgment.apply_validated(state["branches"][branch],item,None,
            sign=1 if record["output"]==record["payload"] else -1,verification="replayed existing authored contextual fixture")
    return state


def record(eid,key,field,part,value):
    return {"evidence_id":eid,"case_id":key,"scope":"seed-budget-1","question":field,"part":part,"value":value,"source":SOURCE}


def inputs(key):
    shield,payload,sroute,proute,swap,conflict=DEFS[key]
    case={"case_id":key,"scope":"seed-budget-1","relation":"equal","decision_questions":["shielded","payload_valid"],
          "reports":[{"id":key+"/"+field+"/report"+str(i),"source":"sensor-"+str(i),"field":field,"value":bool(i)}
                     for field in ("shielded","payload_valid") for i in ((0,1) if conflict else (0,))],
          "candidates":[{"id":"2-shielded" if swap else "1-shielded","field":"shielded","route":sroute},
                        {"id":"1-payload" if swap else "2-payload","field":"payload_valid","route":proute}]}
    entries=[]
    if shield=="SC": entries += [("shielded","check1",False),("shielded","check2",True)]
    elif shield=="SP": entries += [("shielded","check1",False),("shielded","check1",True)]
    elif shield=="SR": entries += [("shielded","check1",True),("shielded","check2",True)]
    if payload=="PC": entries += [("payload_valid","check1",False),("payload_valid","check1",True)]
    elif payload=="PR": entries += [("payload_valid","check1",True)]
    return case,[record(key+"/initial/"+str(i),key,field,part,value) for i,(field,part,value) in enumerate(entries)]


def retain(state,records):
    for item in records:
        eid=item["evidence_id"]
        if eid in state["ledger"] and state["ledger"][eid]["record"]!=item: raise ValueError("conflicting record identity")
        state["ledger"].setdefault(eid,{"record":deepcopy(item),"source":SOURCE,"verification":"exact authored experiment fixture; no correction"})


def scalar_select(state,case,ablated=False):
    rows=[]; ranked=[]
    for candidate in case["candidates"]:
        if candidate["field"] not in case["decision_questions"]: continue
        status=circuit.support(state,case,candidate["field"])
        conflict,_=attention.appraisal(case,candidate)
        if not conflict: rows.append({"candidate":candidate,"gate":"no independent attributed conflict"}); continue
        terms={"weight":state["weights"][candidate["route"]],"theory_pass1_to_execution":.3125,
               "coverage":status["coverage"],"resolved":int(status["resolved"]),"inconsistent":0 if ablated else int(status["inconsistent"])}
        score=max(0.,min(1.,.25*(terms["weight"]+.3125-terms["coverage"]-terms["resolved"]+terms["inconsistent"])))
        rows.append({"candidate":deepcopy(candidate),"support":status,"terms":terms,"score":score})
        if score>0: ranked.append((score,candidate["id"],candidate))
    ranked.sort(key=lambda x:(-x[0],x[1]))
    return (deepcopy(ranked[0][2]) if ranked else None),rows


def selected_reply(key,selected):
    if selected is None: return []
    field=selected["field"]; value=False if key=="x8" and field=="shielded" else True
    parts=circuit.PARTS[field]
    return [record("reply/"+key+"/"+field+"/"+part,key,field,part,value) for part in parts]


def evaluate(base,key,mode,public_inputs=None):
    state=deepcopy(base)
    if public_inputs is None: case,initial=inputs(key)
    else: case,initial=deepcopy(public_inputs["case"]),deepcopy(public_inputs["initial_records"])
    retain(state,initial)
    state["mode"]="consistent-no-clarity" if mode=="ablated" else "consistent-full"
    before=digest(state); prediction=circuit.predict(state,case)
    selected,traces=scalar_select(state,case,mode=="scalar-ablated") if mode.startswith("scalar") else circuit.select(state,case)
    if digest(state)!=before: raise AssertionError("selection/prediction mutated prior")
    prior_ledger=deepcopy(state["ledger"]); weights=deepcopy(state["weights"]); branches=deepcopy(state["branches"])
    # Selection is fixed BEFORE fetching only the selected field.
    reply=selected_reply(key,selected); retain(state,reply); after=circuit.predict(state,case)
    prior_support=prediction["support"]; final_support=after["support"]
    gain=sum(final_support[f]["resolved"] and not prior_support[f]["resolved"] for f in prior_support)
    coverage_gain=sum(final_support[f]["coverage"]-prior_support[f]["coverage"] for f in prior_support)
    contradictions=[f for f in prior_support if prior_support[f]["inconsistent"]]
    checks={"immutable_prior":all(state["ledger"][k]==v for k,v in prior_ledger.items()),"frozen_weights":weights==state["weights"],
            "frozen_counters":branches==state["branches"],"preserved_contradictions":all(final_support[f]["inconsistent"] and not final_support[f]["resolved"] for f in contradictions),
            "one_query":int(selected is not None)<=1}
    return {"case_id":key,"mode":mode,"case":case,"initial_records":initial,"before":prediction,"selected":selected,"selection_trace":traces,
            "verified_reply":reply,"after":after,"final_ledger":state["ledger"],"request_count":int(selected is not None),
            "newly_resolved_questions":gain,"coverage_gain":coverage_gain,"checks":checks}


def worker(root):
    base=json.loads((root/"frozen-prior.json").read_text())
    bundle=json.loads((root/"frozen-case-inputs.json").read_text()); public=bundle["cases"]
    results={mode:[evaluate(base,key,mode,public[key]) for key in bundle["case_order"]] for mode in MODES}
    atomic_json(root/"restarted-evaluations.json",{"pid":os.getpid(),"prior_digest":digest(base),"conditions":results})


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output"); parser.add_argument("--preservation-context"); parser.add_argument("--reload")
    args=parser.parse_args()
    if args.reload: worker(Path(args.reload)); return
    if not args.output or not args.preservation_context: parser.error("output and complete preservation context required")
    root=Path(args.output); root.mkdir(parents=True,exist_ok=False)
    context=json.loads(Path(args.preservation_context).read_text()); preservation.verify_current(context,Path.cwd())
    for name in context["files"]:
        target=root/"archive"/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(name,target)
    atomic_json(root/"archive-manifest.json",context["files"]); shutil.copy2(args.preservation_context,root/"current-preservation-context.json")
    atomic_json(root/"configuration.json",{"definitions":DEFS,"conditions":MODES,"expected_fields":EXPECTED_FIELDS,"expected_question_gains":EXPECTED_GAIN,
        "expected_decisions":EXPECTED_DECISIONS,"weights_source":"unchanged initializer, matching historical sidecar values; frozen","query_budget":1,"model_calls":0})
    atomic_json(root/"provenance.json",{"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        "working_tree":subprocess.check_output(["git","status","--short"],text=True),"protocol_sha256":preservation.file_hash(PROTOCOL),
        "preservation_kind":preservation.KIND,"preservation_context_sha256":preservation.file_hash(args.preservation_context),"python":sys.version,"model_calls":0})
    try:
        base=prior(); atomic_json(root/"frozen-prior.json",base)
        public={key:{"case":inputs(key)[0],"initial_records":inputs(key)[1]} for key in DEFS}
        atomic_json(root/"frozen-case-inputs.json",{"case_order":list(DEFS),"cases":public})
        continuous={mode:[evaluate(base,key,mode,public[key]) for key in DEFS] for mode in MODES}
        subprocess.run([sys.executable,str(Path(__file__).resolve()),"--reload",str(root)],check=True)
        restarted=json.loads((root/"restarted-evaluations.json").read_text())
        checks={"actual_process":restarted["pid"]!=os.getpid(),"prior_restart":restarted["prior_digest"]==digest(base),
                "exact_restart":digest(restarted["conditions"])==digest(continuous)}
        atomic_json(root/"frozen-predictions.json",{m:[r["after"] for r in rows] for m,rows in continuous.items()})
        for original,scalar in (("intact","scalar-intact"),("ablated","scalar-ablated")):
            checks[original+"_memory_action_parity"]=all(l["selected"]==r["selected"] and l["after"]==r["after"] for l,r in zip(continuous[original],continuous[scalar]))
        metrics={}
        for mode,rows in continuous.items():
            expected="ablated" if mode.endswith("ablated") else "intact"
            checks[mode+"_frozen_choices"]=[r["selected"]["field"] if r["selected"] else None for r in rows]==EXPECTED_FIELDS[expected]
            checks[mode+"_frozen_gains"]=[r["newly_resolved_questions"] for r in rows]==EXPECTED_GAIN[expected]
            checks[mode+"_frozen_decisions"]=[r["after"]["decision"] for r in rows]==EXPECTED_DECISIONS
            decided=[r for r in rows if r["after"]["decision"]!="abstain"]
            correct=sum((r["after"]["decision"]=="success")==_OUTCOMES[r["case_id"]] for r in decided)
            metrics[mode]={"requests":sum(r["request_count"] for r in rows),"new_resolved":sum(r["newly_resolved_questions"] for r in rows),
                "coverage_gain":sum(r["coverage_gain"] for r in rows),"decided":len(decided),"correct":correct,"decision_coverage":len(decided)/len(rows),
                "decision_accuracy":correct/len(decided) if decided else None,"case_outcomes":{r["case_id"]:_OUTCOMES[r["case_id"]] for r in rows}}
            checks[mode+"_frozen_metrics"]=metrics[mode]["requests"]==8 and len(decided)==4 and correct==3 and metrics[mode]["coverage_gain"]==(7 if expected=="ablated" else 4.5)
        preservation.pinned_current(root,Path.cwd())
        checks["source_archive"]=all(preservation.file_hash(name)==h==preservation.file_hash(root/"archive"/name) for name,h in context["files"].items())
        values=list(checks.values())+[v for rows in continuous.values() for r in rows for v in r["checks"].values()]
        result={"conditions":continuous,"metrics":metrics,"checks":checks,"integrity_passed":sum(values),"integrity_total":len(values),"model_calls":0}
        atomic_json(root/"results.json",result); print(json.dumps({"integrity_passed":sum(values),"integrity_total":len(values),"metrics":metrics}))
        if not all(values): raise AssertionError("Frozen seed-contribution expectations failed; preserve outcome")
    except Exception as exc: atomic_json(root/"failure.json",{"error":repr(exc)}); raise


if __name__=="__main__":main()
