"""Opt-in bounded relationship learning, isolated from the canonical seed."""
from copy import deepcopy
from . import capacity_fixture as fixture, capacity_relations as relations, contextual, judgment
from .runtime_store import digest

RULE="capacity-study-1"
MODES=("capacity-aggregate","capacity-lookup","capacity-lmft","capacity-memory","capacity-authored")
LEARNERS=("capacity-lmft","capacity-memory")


def newborn(mode):
    return {"mode":mode,"rule_version":RULE,"phase":"train","evidence":{"train":{},"validation":{}},
            "coarse":contextual.branch(),"lookup":{},"selection":None,"acceptance":None,
            "accepted_relationship":None,"rejected":[],"evaluations":[]}


def records(current,split):
    return {eid:entry["record"] for eid,entry in current["evidence"][split].items()}


def counter_decision(counter):
    return {"support":"success","oppose":"failure","undetermined":"abstain"}[judgment.probe(counter)["decision"]]


def predict(current,case):
    result={"case":deepcopy(case),"predictor":current["mode"],"decision":"out_of_scope","score":None,
            "coarse_counterfactual":{"score":current["coarse"]["score"],"decision":counter_decision(current["coarse"])},
            "relationship_ref":None,"trace":None,"uncertainty":"bounded synthetic scope; no calibrated confidence"}
    if not relations.in_scope(case):return result
    result["decision"]="abstain"
    mode=current["mode"]
    if mode=="capacity-aggregate":
        selected=current["coarse"]
    elif mode=="capacity-lookup":
        selected=current["lookup"].get(str((case["length"],case["capacity"])))
        if selected is None:
            result["trace"]={"reason":"unknown exact feature pair; no backoff"}
            return result
    else:
        accepted=current["accepted_relationship"]
        if mode=="capacity-authored":
            relation={"version":relations.VERSION,"left":"length","op":"le","right":"capacity"}
            ref="authored-diagnostic-le"
        elif accepted:
            relation=accepted["representation"];ref=accepted["id"]
        else:
            result["trace"]={"reason":"no accepted relationship"}
            return result
        value=relations.evaluate(relation,case)
        result.update(decision="success" if value else "failure",relationship_ref=ref,
            trace={"representation":deepcopy(relation),"length":case["length"],"capacity":case["capacity"],
                   "value":value,"origin":"authored" if mode=="capacity-authored" else "training-selected and validated"})
        return result
    result.update(decision=counter_decision(selected),score=selected["score"],
                  trace={"evidence_refs":sorted(selected["evidence"]),"rule":"unchanged sum(signs)/(n+2)"})
    return result


def handle(state,message,models,receipt):
    from .runtime import emit
    current=state["judgment"];content=message["content"]
    def respond(text,**extra):emit(state,"response",{"text":text,**extra},message["id"])
    def reject(reason):
        receipt.update(status="rejected",reason=reason)
        current["rejected"].append({"message_id":message["id"],"reason":reason,"content":deepcopy(content)})
        respond("Rejected: "+reason)
        return state
    if message["type"]!="observation" or set(content)!={"text","operation","record"} or not isinstance(content["record"],dict):
        return reject("invalid capacity-study input")
    op=content["operation"];record=content["record"]
    if op=="barrier" and not record:
        respond("Input barrier reached.");return state
    if op=="proposal":
        return reject("malformed relationship" if not relations.valid(record) else "external proposals cannot install or select relationships")
    if op=="outcome":
        eid=record.get("evidence_id")
        if not isinstance(eid,str):return reject("invalid evidence identity")
        prior=next((v[eid] for v in current["evidence"].values() if eid in v),None)
        if prior:
            if digest(record)!=digest(prior["record"]):return reject("conflicting evidence identity")
            receipt.update(status="duplicate_evidence",evidence_ref=eid);receipt.pop("message",None);return state
        split=record.get("split")
        if split not in ("train","validation") or current["phase"]!=split:return reject("evidence split/phase is closed or ineligible")
        if message["source"]!=fixture.SOURCE or not fixture.verify(record):return reject("unverified registered outcome")
        if not state["learning"]:return reject("learning disabled")
        current["evidence"][split][eid]={"record":deepcopy(record),"message_id":message["id"],"source":message["source"],
            "sender":message["sender"],"verification":"registered bounded-write procedure executed"}
        if split=="train":
            adapted={**message,"content":{"evidence":{**record,"sample_id":eid}}}
            sign=1 if record["success"] else -1
            current["coarse"],_=judgment.apply_validated(current["coarse"],adapted,None,sign=sign,verification="registered capacity procedure")
            key=str((record["length"],record["capacity"]))
            current["lookup"][key],_=judgment.apply_validated(current["lookup"].get(key,contextual.branch()),adapted,None,sign=sign,verification="registered capacity procedure")
        receipt.update(status="accepted_evidence",evidence_ref=eid)
        respond("Verified outcome recorded in reserved split.",split=split,evidence_id=eid);return state
    if op=="select" and not record:
        if current["phase"]!="train" or set(current["evidence"]["train"])!=set(fixture.TRAIN):return reject("complete training required; selection is one-shot")
        if not state["learning"]:return reject("learning disabled")
        if current["mode"] in LEARNERS:current["selection"]=relations.select(records(current,"train"))
        current["phase"]="validation"
        receipt["status"]="training_closed"
        respond("Training closed; candidate selection is fixed before validation.");return state
    if op=="accept" and not record:
        if current["phase"]!="validation" or set(current["evidence"]["validation"])!=set(fixture.VALIDATION):return reject("complete reserved validation required; acceptance is one-shot")
        if not state["learning"]:return reject("learning disabled")
        if current["mode"] in LEARNERS:
            selection=current["selection"]
            if selection["training_digest"]!=digest(records(current,"train")):return reject("training changed after selection")
            acceptance=relations.validate(selection,records(current,"validation"));current["acceptance"]=acceptance
            if acceptance["accepted"]:
                current["accepted_relationship"]={"id":"capacity-relationship-1","version":1,
                    "representation":deepcopy(selection["selected"]),"applicability":deepcopy(relations.SCOPE),
                    "derivation":deepcopy(selection),"validation":deepcopy(acceptance),"accepted_by":message["id"],
                    "reason":acceptance["reason"]}
            receipt["status"]="relationship_accepted" if acceptance["accepted"] else "relationship_rejected"
        current["phase"]="evaluation"
        respond("Validation complete; acceptance is fixed.",accepted=current["accepted_relationship"] is not None);return state
    if op=="evaluate":
        result=predict(current,record)
        current["evaluations"].append({"message_id":message["id"],"result":deepcopy(result)})
        receipt["status"]="evaluated"
        respond("Current prediction: "+result["decision"]+".",result=result);return state
    return reject("unsupported capacity-study operation")
