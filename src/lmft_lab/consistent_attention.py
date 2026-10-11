"""Consistent-support-1 mapping; external relation policy is explicitly traced."""
from copy import deepcopy
from dataclasses import asdict
from . import attention,scoped_attention as old
from .attention import N,S,T,F,C,Q
from .birth import create_birth_state
from .propagation import Association,PropagationConfig,propagate_activation
from .runtime_store import digest

RULE="consistent-support-1"
MODES=("consistent-historical","consistent-full","consistent-no-clarity","consistent-no-fact","consistent-no-confidence","consistent-memory")
E="psychological/will/execution"
PARTS=old.PARTS

def newborn(mode):
    current=old.newborn(mode);current["rule_version"]=RULE
    return current

def normalized(current,case):
    view=deepcopy(current)
    for entry in view["ledger"].values():
        r=entry["record"]
        if (case["relation"]=="complement" and r["case_id"]==case["case_id"]
                and r["scope"]==case["scope"] and r["question"]=="shielded" and r["part"]=="check2"):
            r["value"]=not r["value"]
    return view

def support(current,case,field):
    view=normalized(current,case)
    result=old.support(view,case,field)
    observed=set(v for values in result["part_values"].values() for v in values)
    result.update(coverage=sum(bool(v) for v in result["part_values"].values())/len(PARTS[field]),
                  inconsistent=len(observed)>1,relation=case["relation"] if field=="shielded" else "single-check")
    return result

def predict(current,case):
    shield=support(current,case,"shielded");payload=support(current,case,"payload_valid")
    eligible=shield["resolved"] and payload["resolved"] and payload["value"] is True
    return {**attention.decision(current,shield["value"] if eligible else None),
            "support":{"shielded":shield,"payload_valid":payload},
            "scope_gate":"both relevant questions resolved and valid payload required"}

def select(current,case):
    # The external relation rule, not geometry, supplies normalized consistency.
    candidates=[c for c in case["candidates"] if c["field"] in case["decision_questions"]]
    adapter={"relevance_gate":"declared decision questions only",
             "excluded":[c for c in case["candidates"] if c not in candidates],
             "relation_rule":case["relation"],"raw_evidence_preserved":True}
    if current["mode"]=="consistent-historical":
        view=normalized(current,case);view["mode"]="scoped-full"
        eligible={**case,"candidates":candidates}
        selected,traces=old.select(view,eligible)
        return selected,[{"adapter":adapter,"historical_selection":traces}]
    ranked=[];traces=[{"adapter":adapter}]
    for candidate in candidates:
        status=support(current,case,candidate["field"])
        conflict,_=attention.appraisal(case,candidate)
        if not conflict:
            traces.append({"candidate":candidate,"gate":"no independent attributed conflict"});continue
        if current["mode"]=="consistent-memory":
            score=(1+float(status["inconsistent"])+current["weights"][candidate["route"]]) if not status["resolved"] else 0.
            trace={"gate":"explicit insufficient-only; inconsistency first","support":status,"score":score}
        else:
            direct={N:1.,S:1.,T:.5,F:status["coverage"],Q:float(status["resolved"]),C:float(status["inconsistent"]),E:0.}
            specs=((N,T,.5),(S,E,current["weights"][candidate["route"]]),(T,E,.5),(F,E,-1.),(Q,E,-1.),(C,E,1.))
            disabled={"consistent-no-clarity":C,"consistent-no-fact":F,"consistent-no-confidence":Q}.get(current["mode"])
            edges=tuple(Association("consistent-"+str(i),src,dst,w,.1,.5,RULE,RULE,active=src!=disabled)
                        for i,(src,dst,w) in enumerate(specs))
            birth=create_birth_state("consistent-frame",birth_event_id="consistent-birth",random_seed=42)
            propagation=propagate_activation(birth,direct,edges,event_id="select-"+candidate["id"],
                source_instance=RULE,relationship_source=RULE,config=PropagationConfig(passes=2,gain=.25))
            score=propagation.activations[E]
            trace={"gate":"positive final Execution; no resolved override","support":status,
                   "propagation":asdict(propagation),"score":score}
        traces.append({"candidate":candidate,**trace})
        if score>0:ranked.append((score,candidate["id"],candidate))
    ranked.sort(key=lambda item:(-item[0],item[1]))
    return (deepcopy(ranked[0][2]) if ranked else None),traces

def handle(state,message,models,receipt):
    from .runtime import emit
    from . import consistent_fixture as fixture
    current=state["judgment"];content=message["content"]
    def respond(text,**extra):emit(state,"response",{"text":text,**extra},message["id"])
    def reject(reason):
        receipt.update(status="rejected",reason=reason)
        current["rejected"].append({"message_id":message["id"],"reason":reason})
        respond("Rejected: "+reason);return state
    def retain(record):
        eid=record["evidence_id"]
        current["ledger"][eid]={"record":deepcopy(record),"message_id":message["id"],
            "sender":message["sender"],"source":message["source"],"reply_to":message.get("reply_to"),
            "verification":"exact registered synthetic evidence; scope checked separately"}
        current["changes"].append({"evidence_id":eid,"message_id":message["id"],
            "accepted":True,"reason":"unique registered evidence; neither overwrites nor outvotes conflicts"})
    if set(content)!={"text","operation","record"} or not isinstance(content["record"],dict):
        return reject("invalid scoped content")
    op=content["operation"];record=content["record"]
    if op in ("outcome","barrier"):
        return attention.handle(state,message,models,receipt)
    if op=="evidence":
        eid=record.get("evidence_id")
        if not isinstance(eid,str):return reject("invalid evidence identity")
        if eid in current["ledger"]:
            if digest(record)!=digest(current["ledger"][eid]["record"]):return reject("conflicting evidence identity")
            receipt.update(status="duplicate_evidence",evidence_ref=eid);receipt.pop("message",None);return state
        if message["source"]!=fixture.SOURCE or not fixture.registered_evidence(record):
            return reject("not registered evidence; assertion is not fact")
        retain(record);respond("Registered evidence retained with its original scope.",evidence_id=eid);return state
    if op=="evaluate":
        key=record.get("case_id")
        if not isinstance(key,str) or key not in fixture.IDS or digest(record)!=digest(fixture.public_case(key)):
            return reject("invalid public case")
        item=current["cases"].setdefault(key,{"input":deepcopy(record),"evaluations":[],"request":None})
        result=predict(current,record)
        if item["request"] is not None:
            receipt["status"]="budget_exhausted"
            respond("No additional verification budget.",case_id=key,result=result);return state
        selected,traces=select(current,record)
        state["diagnostics"].append({"case_id":key,"message_id":message["id"],"selection":traces})
        item["evaluations"].append({"message_id":message["id"],"selected":selected,"before":result})
        if selected is None:
            respond("No candidate has positive priority.",case_id=key,result=result)
        else:
            request=emit(state,"clarification_request",{"text":"Verify only this scoped question.",
                "case_id":key,"scope":record["scope"],"candidate":selected,"budget_remaining":0},message["id"])
            item["request"]=request
            state["questions"][request]={"case_id":key,"question":selected["field"],"answered_by":None}
        return state
    if op=="verification":
        question=state["questions"].get(message.get("reply_to"))
        if message["type"]!="teacher_reply" or question is None or question["answered_by"] is not None:
            return reject("reply requires an open selected request")
        if message["source"]!=fixture.SOURCE or digest(record)!=digest(fixture.verify(question["case_id"],question["question"])):
            return reject("reply does not match selected registered verification")
        for evidence in record["records"]:
            old=current["ledger"].get(evidence["evidence_id"])
            if old and digest(old["record"])!=digest(evidence):return reject("conflicting evidence identity")
        for evidence in record["records"]:
            if evidence["evidence_id"] not in current["ledger"]:retain(evidence)
        question["answered_by"]=message["id"]
        case=current["cases"][question["case_id"]]["input"]
        respond("Verification retained; unresolved contradictions remain visible.",case_id=question["case_id"],result=predict(current,case))
        return state
    return reject("unsupported scoped operation")
