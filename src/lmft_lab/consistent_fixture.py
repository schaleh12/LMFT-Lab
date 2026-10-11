"""Versioned consistent-support cases; truth is verifier/evaluator-only."""
from copy import deepcopy
from . import scoped_fixture as old

SOURCE=old.SOURCE
FRESH=tuple("f"+str(i) for i in range(1,10))
REGRESSION=old.IDS
IDS=FRESH+REGRESSION+("known",)
_OUTCOMES=dict(f1=True,f2=False,f3=True,f4=True,f5=False,f6=False,f7=True,f8=False,f9=False)

def public_case(key):
    if key not in IDS:raise ValueError("unknown consistent-support case")
    if key not in FRESH:
        result=old.public_case("q6" if key=="known" else key)
    else:
        result=old.public_case("q1")
        result["case_id"]=key
        for report in result["reports"]:report["id"]=key+report["id"][2:]
        if key=="f5":
            result["candidates"].append({"id":"0-color","field":"color","route":"B"})
            result["reports"] += [{"id":"color-"+str(i),"source":"sensor-"+str(i),"field":"color","value":bool(i)} for i in (0,1)]
        if key=="f6":
            result["assertion_text"]="I am absolutely certain shielded is false."
            result["reports"].append({"id":"confident-claim","source":"teacher","field":"shielded","value":False})
    result.update(relation="complement" if key=="f9" else "equal",decision_questions=["shielded","payload_valid"])
    return result

def initial_records(key,contrary=True):
    if key=="known":
        return [r for r in old.initial_records("q6") if r["question"]=="payload_valid" or r["part"]=="check2" or r["value"] is False]
    if key in REGRESSION:return old.initial_records(key,contrary)
    if key not in FRESH:raise ValueError("unknown case")
    result=[]
    def add(field,part,value,case=None,scope="batch-1",suffix=""):
        result.append(old.record(key+"/"+field+"/"+part+suffix,case or key,field,part,value,scope))
    if key!="f8":add("payload_valid","check1",True)
    if key in ("f2","f7"):add("shielded","check1",True)
    else:
        add("shielded","check1",key not in ("f3","f5","f8","f9"))
        add("shielded","check2",key!="f5")
    if key=="f4" and contrary:add("shielded","check2",False,suffix="-contrary")
    if key=="f5":
        add("color","check1",False);add("color","check2",True)
    if key=="f7":
        result.append(deepcopy(result[-1]))
        for part in ("check1","check2"):
            add("shielded",part,True,case="other-case",suffix="-foreign")
            add("shielded",part,True,scope="old-batch",suffix="-old")
    return result

def registered_evidence(record):
    from .runtime_store import digest
    return any(digest(record)==digest(r) for key in IDS for r in initial_records(key))

def verify(case_id,question):
    if case_id in REGRESSION:return old.verify(case_id,question)
    if case_id not in FRESH or question not in ("shielded","payload_valid"):raise ValueError("unknown selected request")
    parts=("check1","check2") if question=="shielded" else ("check1",)
    records=[]
    for part in parts:
        value=True if question=="payload_valid" else False if case_id=="f5" else part=="check2" if case_id=="f9" else True
        records.append(old.record("reply/"+case_id+"/"+question+"/"+part,case_id,question,part,value))
    return {"case_id":case_id,"question":question,"records":records}

def actual_success(key):
    return _OUTCOMES[key] if key in FRESH else old.actual_success("q6" if key=="known" else key)
