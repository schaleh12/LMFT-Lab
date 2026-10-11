"""Versioned append-only correction lineage; ordinary policy, not seed learning."""
from copy import deepcopy
import json
from pathlib import Path
from . import attention,consistent_attention as circuit
from .runtime_store import digest

RULE="correction-ledger-1"
MODES=("correction-lmft","correction-disabled","correction-memory")

def load_policy(filename="correction_authority.json"):
    policy=json.loads((Path(__file__).resolve().parents[2]/"config"/filename).read_text(encoding="utf-8"))
    if set(policy)!={"version","permits"} or policy["version"]!="synthetic-correction-permits-1":
        raise ValueError("unknown correction authority policy")
    return policy

def newborn(mode,policy=None):
    current=circuit.newborn(mode)
    current.update(rule_version=RULE,policy=deepcopy(policy if policy is not None else load_policy()),
        heads={},roots={},corrections=[],correction_index={},cache={})
    return current

def effective(current):
    view=deepcopy(current)
    view["mode"]="consistent-memory" if current["mode"]=="correction-memory" else "consistent-full"
    view["ledger"]={eid:deepcopy(current["ledger"][eid]) for eid in current["heads"].values()}
    return view

def effective_ref(current):
    records={root:current["ledger"][head]["record"] for root,head in sorted(current["heads"].items())}
    return {"heads":deepcopy(current["heads"]),"digest":digest(records),"independent_count":len(records)}

def predict(current,case):return circuit.predict(effective(current),case)

def cache_key(current,case):
    relevant={root:current["ledger"][head]["record"] for root,head in current["heads"].items()
              if current["ledger"][head]["record"]["case_id"]==case["case_id"]
              and current["ledger"][head]["record"]["scope"]==case["scope"]
              and current["ledger"][head]["record"]["question"] in case["decision_questions"]}
    return digest({"case":case,"effective":relevant,"mode":current["mode"],
                   "weights":current["weights"],"branches":current["branches"]})

def correct(state,message,receipt,*,fixture=None,target_check=None,after_accept=None,
            state_ref=effective_ref,acceptance_disabled=False):
    from .runtime import emit
    if fixture is None:
        from . import correction_fixture as fixture
    current=state["judgment"];record=message["content"]["record"];cid=record.get("correction_id")
    identity=digest(record)
    prior=current["correction_index"].get(cid) if isinstance(cid,str) else None
    if prior and prior["payload_digest"]==identity:
        receipt.update(status="duplicate_correction",correction_ref=prior["event_id"])
        receipt.pop("message",None)
        return state
    event={"event_id":"correction-event-"+str(len(current["corrections"])+1),"correction_id":cid,
        "proposal":deepcopy(record),"payload_digest":identity,"sender":message["sender"],"source":message["source"],
        "message_id":message["id"],"before":state_ref(current),
        "authorization":{"checked":False,"passed":False},"eligibility":{"checked":False,"passed":False},
        "verification":{"checked":False,"passed":False},"accepted":False,"cache_invalidated":[],"closed_questions":[]}
    reason=None
    required={"correction_id","authority","target_id","expected_digest","reason","replacement"}
    if prior:reason="conflicting correction ID reuse"
    elif (set(record)!=required or not all(isinstance(record[k],str) and record[k].strip() for k in required-{"replacement"})
          or not isinstance(record["replacement"],dict)):
        reason="malformed correction envelope"
    if reason is None:
        permit=current["policy"]["permits"].get(cid)
        allowed=bool(permit and permit["payload_sha256"]==identity and permit["authority"]==record["authority"]==message["sender"])
        event["authorization"]={"checked":True,"passed":allowed,"policy_digest":digest(current["policy"]),
             "reason":"exact configured operation and authority match" if allowed else "no matching trusted operation permit"}
        if not allowed:reason="unauthorized correction"
    target=None;root=None
    if reason is None:
        target=current["ledger"].get(record["target_id"])
        root=current["roots"].get(record["target_id"])
        replacement=record["replacement"]
        if target is None:reason="target does not exist in scoped evidence"
        elif current["heads"].get(root)!=record["target_id"]:reason="stale target: a newer accepted head exists"
        elif digest(target["record"])!=record["expected_digest"]:reason="stale target digest"
        elif target_check is not None and (target_reason:=target_check(target["record"],replacement)):
            reason=target_reason
        elif target_check is None and any(replacement.get(k)!=target["record"][k] for k in ("case_id","scope","question","part")):
            reason="replacement changes target scope or measurement coordinate"
        elif replacement.get("evidence_id")!="replacement/"+cid or replacement.get("evidence_id") in current["ledger"]:
            reason="replacement identity is not a fresh correction record"
        event["eligibility"]={"checked":True,"passed":reason is None,"reason":reason or "active exact target; same scoped coordinate","root":root}
    if reason is None:
        valid=fixture.replacement_valid(record["replacement"],cid)
        event["verification"]={"checked":True,"passed":valid,"validator":getattr(fixture,"VALIDATOR","registered-coordinate-reference-1"),
            "coordinate":{k:record["replacement"].get(k) for k in getattr(fixture,"COORDINATES",("case_id","scope","question","part"))},
            "reason":"exact independent reference match" if valid else "malformed or unverifiable replacement"}
        if not valid:reason="replacement validation failed"
    if reason is None and (acceptance_disabled or current["mode"]=="correction-disabled" or not state["learning"]):
        reason="correction acceptance disabled"
    if reason is None:
        replacement=deepcopy(record["replacement"]);eid=replacement["evidence_id"]
        current["ledger"][eid]={"record":replacement,"message_id":message["id"],"sender":message["sender"],
            "source":message["source"],"verification":event["verification"],"correction_event":event["event_id"],
            "parent":record["target_id"],"root":root}
        current["roots"][eid]=root;current["heads"][root]=eid
        event["accepted"]=True
        reason="verified authorized replacement supersedes active target; same independent root"
        if after_accept is not None:
            after_accept(state,event)
        else:
            for key,item in current["cases"].items():
                case=item["input"]
                cached=current["cache"].get(key)
                if cached and cached["key"]!=cache_key(current,case):
                    current["cache"].pop(key);event["cache_invalidated"].append(key)
                for qid,q in state["questions"].items():
                    if q["case_id"]==key and q["status"]=="open" and circuit.support(effective(current),case,q["question"])["resolved"]:
                        q.update(status="resolved_by_correction",closed_by=event["event_id"])
                        event["closed_questions"].append(qid)
    event["reason"]=reason;event["after"]=state_ref(current)
    current["corrections"].append(event)
    if isinstance(cid,str) and not prior:
        current["correction_index"][cid]={"event_id":event["event_id"],"payload_digest":identity}
    receipt.update(status="correction_accepted" if event["accepted"] else "correction_rejected",correction_ref=event["event_id"])
    emit(state,"response",{"text":"Correction accepted." if event["accepted"] else "Correction rejected.",
        "correction_id":cid,"accepted":event["accepted"],"reason":reason},message["id"])
    return state

def handle(state,message,models,receipt):
    from .runtime import emit
    from . import correction_fixture as fixture
    current=state["judgment"];content=message["content"]
    def respond(text,**extra):emit(state,"response",{"text":text,**extra},message["id"])
    def reject(reason):
        receipt.update(status="rejected",reason=reason);current["rejected"].append({"message_id":message["id"],"reason":reason})
        respond("Rejected: "+reason);return state
    if set(content)!={"text","operation","record"} or not isinstance(content["record"],dict):return reject("invalid correction-study content")
    op=content["operation"];record=content["record"]
    if op in ("outcome","barrier"):return attention.handle(state,message,models,receipt)
    if op=="correction":return correct(state,message,receipt)
    if op=="evidence":
        eid=record.get("evidence_id")
        if not isinstance(eid,str):return reject("invalid evidence identity")
        if eid in current["ledger"]:
            if digest(record)!=digest(current["ledger"][eid]["record"]):return reject("conflicting evidence identity")
            receipt.update(status="duplicate_evidence",evidence_ref=eid);receipt.pop("message",None);return state
        if message["source"]!=fixture.SOURCE or not fixture.admitted(record):return reject("not a registered instrument report")
        current["ledger"][eid]={"record":deepcopy(record),"message_id":message["id"],"sender":message["sender"],
            "source":message["source"],"verification":"registered instrument log only; report may be erroneous","root":eid,"parent":None}
        current["roots"][eid]=eid;current["heads"][eid]=eid
        current["changes"].append({"evidence_id":eid,"reason":"admitted instrument report, not independent truth"})
        respond("Instrument report retained with provenance.");return state
    if op=="evaluate":
        key=record.get("case_id")
        if not isinstance(key,str) or key not in fixture.IDS or digest(record)!=digest(fixture.public_case(key)):return reject("invalid public case")
        item=current["cases"].setdefault(key,{"input":deepcopy(record),"request":None,"evaluations":[]})
        signature=cache_key(current,record);cached=current["cache"].get(key)
        if cached and cached["key"]==signature:
            receipt["status"]="evaluation_cache_hit"
            result=deepcopy(cached["result"]);selected=deepcopy(cached["selected"])
        else:
            receipt["status"]="evaluated"
            result=predict(current,record);selected,traces=circuit.select(effective(current),record)
            state["diagnostics"].append({"case_id":key,"message_id":message["id"],"effective":effective_ref(current),"selection":traces})
            current["cache"][key]={"key":signature,"result":deepcopy(result),"selected":deepcopy(selected)}
        item["evaluations"].append({"message_id":message["id"],"key":signature,"result":result,"selected":selected,
                                   "budget_available":item["request"] is None})
        if selected and item["request"] is None:
            qid=emit(state,"clarification_request",{"text":"Requesting scoped verification; no additional fixture measurement is available yet.",
                "case_id":key,"candidate":selected,"budget_remaining":0,"result":result},message["id"])
            item["request"]=qid;state["questions"][qid]={"case_id":key,"question":selected["field"],"status":"open","closed_by":None}
        else:
            text="Current scoped judgment: "+result["decision"]+". "
            text+="Relevant support remains unresolved." if any(not v["resolved"] for v in result["support"].values()) else "Relevant condition evidence is sufficient; prediction is not guaranteed."
            respond(text,case_id=key,result=result,budget_remaining=int(item["request"] is None))
        return state
    return reject("unsupported correction-study operation")
