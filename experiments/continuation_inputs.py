"""Frozen continuation messages and independent rational expectations; evaluator only."""
from copy import deepcopy
from fractions import Fraction
from lmft_lab import outcome_fixture as f

SCENARIOS = {
    "crossing": {"key":"o2", "events":[("o8",0),("o9",0),("o3",1)],
                 "expected":[(0,2,"abstain"),(-Fraction(1,5),3,"failure"),(0,4,"abstain")],
                 "corrected":(Fraction(1,3),1,"success")},
    "same-category": {"key":"o12", "events":[("o8",0)],
                      "expected":[(Fraction(1,5),3,"success")], "corrected":(Fraction(1,2),2,"success")},
    "unresolved": {"key":"o4", "events":[("o8",0),("o3",1)],
                   "expected":[(-Fraction(1,7),5,"abstain"),(0,6,"abstain")], "corrected":(0,4,"abstain")},
}
CONDITIONS = ("restarted", "uninterrupted", "memory", "frozen")


def message(identifier,op,record):
    return {"schema_version":1,"id":identifier,"sender":f.AUTHORITY,"source":f.SOURCE,"type":"observation",
        "content":{"text":"Registered report or correction; attribution is not authority.","operation":op,"record":deepcopy(record)}}


def evaluation(identifier,key,variant="warm"):
    return message(identifier,"evaluate",f.public_case(key,variant))


def initial(name):
    key=SCENARIOS[name]["key"]
    items=[message("initial-"+str(i),"evidence",r) for i,r in enumerate(f.initial_records(key))]
    items += [evaluation("initial-probe",key),message("repair","correction",f.corrections(key)[0]),
              evaluation("corrected",key),evaluation("corrected-repeat",key),evaluation("other-before",key,"other")]
    return items


def batches(name):
    spec=SCENARIOS[name];key=spec["key"];result=[]
    for i,(source,index) in enumerate(spec["events"]):
        m=message("new-"+str(i),"evidence",f.initial_records(source)[index])
        result.append(("new-"+str(i),[m,evaluation("stage-"+str(i),key),evaluation("stage-repeat-"+str(i),key)]))
        if i==0:
            duplicates=[deepcopy(m) for _ in range(5)]
            for j in range(5):
                copy=deepcopy(m);copy["id"]="copy-"+str(j);duplicates.append(copy)
            result.append(("duplicates",duplicates+[evaluation("after-duplicates",key)]))
            conflict=deepcopy(f.initial_records(key)[0]);conflict["output"]+=7
            alias=deepcopy(conflict);alias["evidence_id"]="attempted-new-alias"
            result.append(("conflicts",[message("identity-conflict","evidence",conflict),message("identity-alias","evidence",alias),evaluation("after-conflicts",key)]))
    outside=deepcopy(f.initial_records("o10")[0]);outside["scope"]="batch-2"
    result.append(("scope",[message("other-event","evidence",f.initial_records("o6")[-1]),
        evaluation("after-other-target",key),evaluation("after-other-branch",key,"other"),
        message("outside-scope","evidence",outside),evaluation("after-scope-target",key)]))
    result.append(("fresh",[evaluation("fresh-1",key,"fresh-1"),evaluation("fresh-2",key,"fresh-2")]))
    return result
