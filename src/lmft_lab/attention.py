"""Bounded authored selection and separate learned association weights."""
from copy import deepcopy
from dataclasses import asdict
from .birth import create_birth_state
from .propagation import Association, PropagationConfig, propagate_activation
from .judgment import probe as judgment_probe, apply_validated
from . import contextual
from .runtime_store import digest

RULE = "attention-verification-1"
MODES = ("attention-lmft", "attention-frozen", "attention-disabled", "attention-memory")
N = "experiential/reflection/novelty"
S = "experiential/reflection/salience"
T = "psychological/truth/theory"
F = "psychological/truth/fact"
C = "psychological/contemplation/clarity"
Q = "psychological/contemplation/confidence"

def newborn(mode):
    return {"mode":mode,"rule_version":RULE,"weights":dict(A=.5,B=.5,D=.5),
            "branches":{k:contextual.branch() for k in ("shielded","unshielded")},
            "outcomes":{},"cases":{},"evidence":{},"updates":[],"rejected":[]}

def appraisal(record, candidate):
    unique = {}
    for report in record["reports"]:
        old = unique.get(report["id"])
        if old is not None and old != report: raise ValueError("conflicting report identity")
        unique[report["id"]] = report
    relevant = [r for r in unique.values() if r["field"] == candidate["field"]]
    conflict = any(a["value"] != b["value"] and a["source"] != b["source"] for a in relevant for b in relevant)
    return conflict, candidate["field"] == "shielded"

def frame(candidate, conflict, relevant, weight, *, verified=False):
    direct = {N:float(conflict),S:float(relevant),T:.5*float(conflict and not verified),
              F:float(verified),C:0.,Q:0.}
    specs = ((N,T,.5),(S,C,weight),(T,C,.5),(F,Q,1.),(Q,C,-1.))
    edges = tuple(Association("attention-"+str(i),a,b,w,.1,.5,RULE,RULE) for i,(a,b,w) in enumerate(specs))
    birth = create_birth_state("attention-frame",birth_event_id="attention-birth",random_seed=42)
    result = propagate_activation(birth,direct,edges,event_id="candidate-"+candidate["id"],
        source_instance=RULE,relationship_source=RULE,config=PropagationConfig(passes=2,gain=.25))
    return result.activations[C], asdict(result)

def select(current, record):
    # No fixture/verifier/hidden outcome access here.
    ranked=[]; traces=[]
    for candidate in record["candidates"]:
        conflict,relevant=appraisal(record,candidate)
        if not conflict: continue
        mode=current["mode"]; weight=current["weights"][candidate["route"]]
        if mode == "attention-disabled": score=1.
        elif mode == "attention-memory": score=float(relevant)*2+weight
        else:
            score,trace=frame(candidate,conflict,relevant,weight)
            traces.append({"candidate":candidate,"trace":trace,"score":score})
        if score>0: ranked.append((score,candidate["id"],candidate))
    ranked.sort(key=lambda x:(-x[0],x[1]))
    return (deepcopy(ranked[0][2]) if ranked else None),traces

def decision(current, value):
    if type(value) is not bool: return {"decision":"abstain","score":None,"evidence_refs":[]}
    branch=current["branches"]["shielded" if value else "unshielded"]
    result=judgment_probe(branch)
    return {"decision":{"support":"success","oppose":"failure","undetermined":"abstain"}[result["decision"]],
            "score":result["score"],"evidence_refs":sorted(branch["evidence"])}

def updated_weight(before, resolved):
    return min(1.,max(0.,before+.25*(1 if resolved else -1)))

def handle(state,message,models,receipt):
    from .runtime import emit
    from . import attention_fixture as fixture
    current=state["judgment"]; content=message["content"]
    def respond(text, **extra):
        emit(state,"response",{"text":text,**extra},message["id"])
    def reject(reason):
        receipt.update(status="rejected",reason=reason)
        current["rejected"].append({"message_id":message["id"],"reason":reason})
        respond("Rejected: "+reason)
        return state
    if set(content)!={"text","operation","record"} or not isinstance(content["record"],dict):
        return reject("invalid attention content")
    op=content["operation"]; record=content["record"]
    if op=="barrier" and record=={}:
        respond("Completed queued inputs."); return state
    if op=="outcome":
        key=record.get("evidence_id")
        if not isinstance(key,str) or key not in list(contextual.TRIALS)[:8] or record!=fixture.training_record(key):
            return reject("outcome does not match registered training evidence")
        # JSON numeric equality must not admit Boolean/integer substitutions.
        if digest(record)!=digest(fixture.training_record(key)): return reject("outcome types mismatch")
        if key in current["outcomes"]:
            receipt["status"]="duplicate_evidence"; return state
        branch="shielded" if record["shielded"] else "unshielded"
        adapted=deepcopy(message);adapted["content"]["evidence"]={"sample_id":key,**record}
        current["branches"][branch],_=apply_validated(current["branches"][branch],adapted,None,
            sign=1 if record["output"]==record["payload"] else -1,verification="registered contextual outcome")
        current["outcomes"][key]={"record":record,"source":message["source"],"message_id":message["id"]}
        respond("Verified outcome retained."); return state
    if op=="case":
        key=record.get("case_id")
        if not isinstance(key,str) or key not in fixture.IDS or digest(record)!=digest(fixture.public_case(key)):
            return reject("case does not match public fixture; claims are not facts")
        if key in current["cases"]:
            receipt["status"]="budget_exhausted";respond("No further request: case budget already allocated.");return state
        selected,traces=select(current,record)
        item={"input":record,"message_id":message["id"],"source":message["source"],
              "selected":selected,"resolved":False,"result":decision(current,None),"reply":None}
        current["cases"][key]=item
        if traces: state["diagnostics"].append({"case_id":key,"selection":traces})
        if selected is None:
            respond("No independent conflict warrants verification.",case_id=key,result=item["result"])
        else:
            request=emit(state,"clarification_request",{"text":"Please verify the selected condition; reports remain attributed claims.",
                "case_id":key,"candidate":selected,"budget_remaining":0},message["id"])
            item["request"]=request
            state["questions"][request]={"case_id":key,"answered_by":None}
        return state
    if op=="verification":
        eid=record.get("evidence_id")
        if isinstance(eid,str) and eid in current["evidence"]:
            if digest(record)!=digest(current["evidence"][eid]["record"]): return reject("conflicting evidence identity")
            receipt.update(status="duplicate_evidence",evidence_ref=eid)
            receipt.pop("message",None)
            return state
        question=state["questions"].get(message.get("reply_to"))
        if message["type"]!="teacher_reply" or not question or question["answered_by"] is not None:
            return reject("verification requires open selected request")
        key=question["case_id"]; item=current["cases"][key]; selected=item["selected"]
        if message["source"]!="registered-attention-1" or not fixture.validate_reply(record,key,selected):
            return reject("reply is not a matching registered verification")
        evidence={"record":deepcopy(record),"message_id":message["id"],"source":message["source"],
                  "sender":message["sender"],"reply_to":message["reply_to"],"verification":"selected registered request only"}
        current["evidence"][eid]=evidence
        question["answered_by"]=message["id"]; item["reply"]=eid
        relevant=selected["field"]=="shielded"
        resolved=relevant and type(record["value"]) is bool
        item["resolved"]=resolved;item["result"]=decision(current,record["value"] if resolved else None)
        route=selected["route"];before=current["weights"][route]
        eligible=(key in ("t1","t2") and relevant and state["learning"]
                  and current["mode"] in ("attention-lmft","attention-memory"))
        after=updated_weight(before,resolved) if eligible else before
        current["weights"][route]=after
        current["updates"].append({"evidence_id":eid,"route":route,"before":before,"after":after,
            "accepted":eligible,"resolved":resolved,"reason":"verified training resolution outcome" if eligible else "evaluation, irrelevant route, or learning-disabled condition",
            "provenance":evidence})
        if current["mode"] in ("attention-lmft","attention-frozen"):
            _,trace=frame(selected,True,relevant,after,verified=resolved)
            state["diagnostics"].append({"case_id":key,"post_verification":trace})
        respond("Verification resolved the condition." if resolved else "Verification did not resolve the decision; withholding prediction.",
                case_id=key,resolved=resolved,result=item["result"])
        return state
    return reject("unsupported operation")
