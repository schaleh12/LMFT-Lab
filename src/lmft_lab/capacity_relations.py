"""Six authored hypotheses; data selects a rule, no generated executable code."""
from copy import deepcopy
import operator
from .runtime_store import digest

VERSION="capacity-comparison-1"
OPS={"lt":operator.lt,"le":operator.le,"eq":operator.eq,"ge":operator.ge,"gt":operator.gt,"ne":operator.ne}
SCOPE={"procedure":"capacity-transmit-1","minimum":0,"maximum":8,
       "conditions":"empty buffer; noiseless; no draining, compression, overhead or concurrent writer"}


def candidates():
    return [{"version":VERSION,"left":"length","op":op,"right":"capacity"} for op in OPS]


def valid(relation):
    return (isinstance(relation,dict) and set(relation)=={"version","left","op","right"}
            and relation["version"]==VERSION and relation["left"]=="length" and relation["right"]=="capacity"
            and isinstance(relation["op"],str) and relation["op"] in OPS)


def in_scope(case):
    return (isinstance(case,dict) and set(case)=={"case_id","procedure","length","capacity"}
            and isinstance(case["case_id"],str) and bool(case["case_id"])
            and case["procedure"]==SCOPE["procedure"]
            and all(type(case[k]) is int and 0<=case[k]<=8 for k in ("length","capacity")))


def evaluate(relation,case):
    if not valid(relation):raise ValueError("malformed or unsupported relationship")
    if not in_scope(case):raise ValueError("outside relationship applicability")
    return OPS[relation["op"]](case["length"],case["capacity"])


def input_case(record):
    return {"case_id":record["evidence_id"],**{k:record[k] for k in ("procedure","length","capacity")}}


def select(records):
    """Receives verified training records only, never a verifier or held-out table."""
    eligible=len(records)>=4 and {r["success"] for r in records.values()}=={True,False}
    evaluations=[]
    for candidate in candidates():
        errors=[eid for eid,r in sorted(records.items()) if evaluate(candidate,input_case(r))!=r["success"]]
        evaluations.append({"relationship":candidate,"error_refs":errors,"consistent":not errors})
    survivors=[e["relationship"] for e in evaluations if e["consistent"]]
    return {"version":"capacity-induction-1","candidate_evaluations":evaluations,"consistent":survivors,
            "selected":deepcopy(survivors[0]) if eligible and len(survivors)==1 else None,
            "training_refs":sorted(records),"training_digest":digest(records),
            "reason":"unique zero-error training candidate" if eligible and len(survivors)==1 else "insufficient evidence or ambiguity; no tie broken"}


def validate(selection,records):
    selected=selection["selected"]
    checks=[{"evidence_id":eid,"predicted":evaluate(selected,input_case(r)),"observed":r["success"]}
            for eid,r in sorted(records.items())] if selected else []
    accepted=selected is not None and len(checks)==4 and all(c["predicted"]==c["observed"] for c in checks)
    return {"accepted":accepted,"checks":checks,"validation_refs":sorted(records),"validation_digest":digest(records),
            "reason":"unique training candidate passed all four reserved validation events" if accepted else "no unique candidate or validation mismatch; no fallback selection"}
