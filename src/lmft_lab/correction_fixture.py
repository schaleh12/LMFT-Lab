"""Instrument-log admission and separate synthetic replacement reference."""
from copy import deepcopy
from . import consistent_fixture as prior
from .runtime_store import digest

RULE="correction-fixture-1"
SOURCE="registered-instrument-log-1"
AUTHORITY="fixture-curator"
IDS=tuple("c"+str(i) for i in range(1,13))

def public_case(key):
    if key not in IDS:raise ValueError("unknown correction case")
    result=prior.public_case("f1");result["case_id"]=key
    for report in result["reports"]:report["id"]=key+report["id"][2:]
    return result

def initial_records(key):
    if key not in IDS:raise ValueError("unknown correction case")
    def record(field,part,value):
        return {"evidence_id":key+"/"+field+"/"+part,"case_id":key,"scope":"batch-1",
                "question":field,"part":part,"value":value,"source":SOURCE}
    result=[record("payload_valid","check1",True),record("shielded","check1",key in ("c2","c3","c12"))]
    if key!="c4":result.append(record("shielded","check2",True))
    if key=="c12":result.append(record("color","check1",False))
    return result

def admitted(record):
    # Certifies the frozen instrument report, explicitly NOT its factual correctness.
    return any(digest(record)==digest(r) for key in IDS for r in initial_records(key))

def replacement_valid(record,correction_id):
    fields={"evidence_id","case_id","scope","question","part","value","source"}
    if set(record)!=fields or type(record["value"]) is not bool:return False
    key=record["case_id"]
    if key not in IDS:return False
    # Reference access limited to the submitted replacement coordinate.
    expected=False if key in ("c2","c3") and record["question"]=="shielded" else True
    return (record["evidence_id"]=="replacement/"+correction_id and record["source"]=="correction-reference-1"
            and record["scope"]=="batch-1" and record["question"] in ("shielded","payload_valid","color")
            and record["part"] in ("check1","check2") and record["value"] is expected)

def proposal(cid,target,value):
    replacement={**target,"evidence_id":"replacement/"+cid,"value":value,"source":"correction-reference-1"}
    return {"correction_id":cid,"authority":AUTHORITY,"target_id":target["evidence_id"],
            "expected_digest":digest(target),"reason":"Registered independent reference corrects the instrument report.","replacement":replacement}

def corrections(key):
    records=initial_records(key);target=records[-1] if key=="c12" else records[1]
    first=proposal(key+"-a",target,False if key in ("c2","c3") else True)
    if key=="c3":return [first,proposal(key+"-b",records[2],False)]
    if key=="c6":
        bad=deepcopy(first);bad["replacement"]["value"]=False
        malformed=proposal(key+"-b",target,True);malformed["replacement"].pop("value")
        return [bad,malformed]
    if key=="c7":
        wrong=deepcopy(first);wrong["replacement"]["scope"]="other-batch"
        missing=proposal(key+"-b",target,True);missing["target_id"]="nonexistent"
        return [wrong,missing]
    if key=="c9":
        conflict=deepcopy(first);conflict["replacement"]["value"]=False
        return [first,conflict]
    if key=="c10":
        competing=proposal(key+"-b",target,True)
        stale=proposal(key+"-c",first["replacement"],True);stale["expected_digest"]="0"*64
        return [first,competing,stale]
    if key=="c11":return [first,proposal(key+"-b",first["replacement"],True)]
    return [first]

def actual_success(key):
    return key not in ("c2","c3","c9")
