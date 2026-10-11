"""Scoped evidence appraisal and isolated outgoing-influence ablations."""
from copy import deepcopy
from dataclasses import asdict
from . import attention
from .attention import N,S,T,F,C,Q
from .birth import create_birth_state
from .propagation import Association,PropagationConfig,propagate_activation
from .runtime_store import digest

RULE="scoped-support-1"
MODES=("scoped-full","scoped-no-fact","scoped-no-confidence","scoped-neither","scoped-memory")
PARTS={"shielded":("check1","check2"),"payload_valid":("check1",)}

def newborn(mode):
    current=attention.newborn(mode)
    current.update(rule_version=RULE,weights=dict(A=.25,B=.75,D=.5),ledger={},changes=[])
    return current

def support(current,case,field):
    required=PARTS[field]
    applicable=[entry for entry in current["ledger"].values()
                if entry["record"]["case_id"]==case["case_id"]
                and entry["record"]["scope"]==case["scope"]
                and entry["record"]["question"]==field
                and entry["record"]["part"] in required]
    values={part:{entry["record"]["value"] for entry in applicable if entry["record"]["part"]==part} for part in required}
    complete=all(len(v)==1 for v in values.values())
    all_values=set().union(*values.values())
    resolved=complete and len(all_values)==1
    return {"resolved":resolved,"value":next(iter(all_values)) if resolved else None,
            "fact_fraction":sum(len(v)==1 for v in values.values())/len(required),
            "evidence_refs":sorted(e["record"]["evidence_id"] for e in applicable),
            "part_values":{p:sorted(v) for p,v in values.items()}}

def predict(current,case):
    shield=support(current,case,"shielded");payload=support(current,case,"payload_valid")
    eligible=shield["resolved"] and payload["resolved"] and payload["value"] is True
    return {**attention.decision(current,shield["value"] if eligible else None),
            "support":{"shielded":shield,"payload_valid":payload},
            "scope_gate":"both resolved and valid payload required"}

def select(current,case):
    # Only supplied reports and accepted ledger entries; no verifier/fixture access.
    ranked=[];traces=[]
    for candidate in case["candidates"]:
        status=support(current,case,candidate["field"])
        conflict,_=attention.appraisal(case,candidate)
        if not conflict:
            traces.append({"candidate":candidate,"gate":"no independent conflicting reports"});continue
        if current["mode"]=="scoped-memory":
            score=current["weights"][candidate["route"]] if not status["resolved"] else 0.
            trace={"gate":"explicit unresolved-question gate","support":status,"score":score}
        else:
            direct={N:1.,S:1.,T:.5,F:status["fact_fraction"],Q:float(status["resolved"]),C:0.}
            specs=((N,T,.5),(S,C,current["weights"][candidate["route"]]),(T,C,.5),(F,Q,1.),(Q,C,-1.),(F,C,-1.))
            disabled_fact=current["mode"] in ("scoped-no-fact","scoped-neither")
            disabled_conf=current["mode"] in ("scoped-no-confidence","scoped-neither")
            edges=tuple(Association("scoped-"+str(i),src,dst,w,.1,.5,RULE,RULE,
                 active=not ((src==F and disabled_fact) or (src==Q and disabled_conf)))
                 for i,(src,dst,w) in enumerate(specs))
            birth=create_birth_state("scoped-frame",birth_event_id="scoped-birth",random_seed=42)
            propagated=propagate_activation(birth,direct,edges,event_id="select-"+candidate["id"],
                source_instance=RULE,relationship_source=RULE,config=PropagationConfig(passes=2,gain=.25))
            score=propagated.activations[C]
            trace={"gate":"positive final Clarity only; no resolved-state gate","support":status,
                   "propagation":asdict(propagated),"score":score}
        traces.append({"candidate":candidate,**trace})
        if score>0:ranked.append((score,candidate["id"],candidate))
    ranked.sort(key=lambda item:(-item[0],item[1]))
    return (deepcopy(ranked[0][2]) if ranked else None),traces

def handle(state,message,models,receipt):
    from .runtime import emit
    from . import scoped_fixture as fixture
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
