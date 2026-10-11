"""Frozen scoped-support records and selected-question synthetic verifier."""
from copy import deepcopy
from .scoped_attention import PARTS

IDS = tuple("q"+str(i) for i in range(1,8))
SOURCE = "registered-scoped-support-1"
# Evaluator-only outcomes; selectors and predictors never call this table.
_OUTCOMES = dict(q1=True,q2=False,q3=False,q4=False,q5=True,q6=True,q7=False)
_VALUES = dict(q1=True,q2=True,q3=False,q4=True,q5=True,q6=True,q7=False)

def public_case(key):
    if key not in IDS: raise ValueError("unknown scoped case")
    reports=[{"id":key+field+str(i),"source":"sensor-"+str(i),"field":field,"value":bool(i)}
             for field in PARTS for i in (0,1)]
    if key=="q3":
        reports.append({"id":"confident-assertion","source":"teacher","field":"shielded","value":True})
    return {"case_id":key,"scope":"batch-1","reports":reports,
            "assertion_text":"I am absolutely certain shielded is true." if key=="q3" else "Attributed reports conflict.",
            "candidates":[{"id":"1-shielded","field":"shielded","route":"B"},
                          {"id":"2-payload_valid","field":"payload_valid","route":"B"}]}

def record(eid,key,field,part,value,scope="batch-1"):
    return {"evidence_id":eid,"case_id":key,"scope":scope,"question":field,
            "part":part,"value":value,"source":SOURCE}

def initial_records(key,contrary=True):
    result=[]
    def add(field,part,value,*,case=None,scope="batch-1",suffix=""):
        result.append(record(key+"/"+field+"/"+part+suffix,case or key,field,part,value,scope))
    if key!="q1":add("payload_valid","check1",True)
    if key in ("q1","q2","q4","q6","q7"):
        add("shielded","check1",key!="q7")
        if key!="q2":add("shielded","check2",key!="q7")
    if key=="q5":
        for part in PARTS["shielded"]:
            add("shielded",part,True,case="other-case",suffix="-foreign")
            add("shielded",part,True,scope="old-batch",suffix="-old")
    if key=="q6" and contrary:add("shielded","check1",False,suffix="-contrary")
    if key=="q4":result.append(deepcopy(result[1]))
    return result

def registered_evidence(record):
    from .runtime_store import digest
    return any(digest(record)==digest(r) for key in IDS for r in initial_records(key))

def verify(case_id,question):
    if case_id not in IDS or question not in PARTS:raise ValueError("unknown selected request")
    value=True if question=="payload_valid" else _VALUES[case_id]
    return {"case_id":case_id,"question":question,"records":[
        record("reply/"+case_id+"/"+question+"/"+part,case_id,question,part,value)
        for part in PARTS[question]]}

def actual_success(case_id):
    return _OUTCOMES[case_id]
