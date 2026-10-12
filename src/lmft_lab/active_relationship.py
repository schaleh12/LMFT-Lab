"""One explicit investigation episode; real runtime request/reply, no models."""
from copy import deepcopy
import json
from . import ambiguity, insufficiency as learner, insufficiency_fixture as fixture
from .capacity_relations import candidates
from .runtime_store import digest

RULE = "active-relationship-acquisition-1"
MODES = ("relationship-acquire-lmft", "relationship-acquire-memory")
POLICIES = ("disagreement", "noninformative", "unavailable")
QUERIES = {"q1": (0, 2), "q2": (5, 5), "q3": (7, 7), "q4": (7, 6)}


def policy(scenario, acquisition_policy, receiver_attempt_budget=None):
    if scenario not in fixture.TRAIN or acquisition_policy not in POLICIES:
        raise ValueError("unsupported active relationship policy")
    if receiver_attempt_budget is not None and (type(receiver_attempt_budget) is not int or not 0 <= receiver_attempt_budget <= 8):
        raise ValueError("receiver attempt budget must be a strict integer in 0..8 or omitted")
    result = json.loads(json.dumps({"rule_version": RULE, "scenario": scenario, "acquisition_policy": acquisition_policy,
        "task": learner.configuration(), "queries": QUERIES, "request_budget": 1,
        "episode_rule": "one fixed episode per individual; no reset", "model_calls": 0}))
    if receiver_attempt_budget is not None:
        result.update(receiver_attempt_budget=receiver_attempt_budget, receiver_attempt_rule="checkpoint-accounted-receiver-attempts-1",
                      receiver_guarantee="committed attempts capped; pre-commit rollback can repeat physical computation")
    return result


def newborn(mode, scenario, acquisition_policy, individual, receiver_attempt_budget=None):
    if mode not in MODES: raise ValueError("unsupported active relationship mode")
    policy(scenario, acquisition_policy, receiver_attempt_budget)
    result = {"mode": mode, "rule_version": RULE, "candidate_space": candidates(),
        "learner": learner.newborn("memory", scenario), "survivors": [], "support_status": "untrained",
        "acceptance": None, "acquired": {}, "filter_trace": [], "evidence_links": {},
        "episode": {"id": individual + ":relationship-episode-1", "policy": acquisition_policy,
            "phase": "unselected", "request_count": 0, "request_id": None, "selection": None,
            "closed_reason": None, "verified_observations": 0}}
    if receiver_attempt_budget is not None:
        result["episode"].update(receiver_attempt_budget=receiver_attempt_budget, receiver_attempts=0, receiver_exhausted=False)
    return result


def scientific(current):
    return {k: deepcopy(v) for k, v in current.items() if k != "mode"}


def snapshot(current):
    accepted = current["acceptance"]
    return {"rule_version": RULE, "mode": current["mode"], "support_status": current["support_status"],
        "training_support_status": current["learner"]["support_status"],
        "validation_status": "not_validated" if accepted is None else "validated" if accepted["accepted"] else accepted["reason"],
        "survivors": deepcopy(current["survivors"]), "episode": deepcopy(current["episode"]),
        "acquisition_refs": sorted(current["acquired"])}


def predict(current, observation):
    view = deepcopy(current["learner"])
    view.update(survivors=deepcopy(current["survivors"]), support_status=current["support_status"], acceptance=deepcopy(current["acceptance"]))
    result = learner.predict(view, observation)
    result["acquisition_refs"] = sorted(current["acquired"])
    result["complete_evidence_digest"] = digest({"reserved": view["evidence"], "acquired": current["acquired"]})
    return result


def choose(current):
    """Reuse the numeric selector; original task scope remains explicit."""
    ids = ("q1", "q4") if current["episode"]["policy"] == "unavailable" else tuple(QUERIES)
    result = ambiguity.choose(current["survivors"], [ambiguity.case(eid, QUERIES[eid]) for eid in ids])
    for row in result["scored"]:
        case = row["case"]; row["case"] = learner.case(case["case_id"], (case["length"], case["capacity"]))
    if result["selected"] is not None:
        case = result["selected"]; result["selected"] = learner.case(case["case_id"], (case["length"], case["capacity"]))
    if current["episode"]["policy"] == "noninformative": result["selected"] = learner.case("q1", QUERIES["q1"])
    result["selector"] = "unchanged ambiguity.choose"
    result["scope_adapter"] = {"task": fixture.PROCEDURE, "numeric_selector_scope": ambiguity.relations.SCOPE["procedure"],
                               "reason": "same bounded integer comparison operands; no device outcomes"}
    return result


def verification_record(current):
    """Scripted service ONLY; selection/prediction never calls this function."""
    ep = current["episode"]; selected = ep["selection"]["selected"]
    return {"episode_id": ep["id"], "request_id": ep["request_id"], "evidence": {
        "evidence_id": selected["case_id"], "scenario": current["learner"]["scenario"], "split": "acquisition",
        "procedure": fixture.PROCEDURE, "length": selected["length"], "capacity": selected["capacity"],
        "success": fixture.execute(selected["length"], selected["capacity"])}}


def registered_acquisition(record, current):
    if not isinstance(record, dict) or set(record) != fixture.FIELDS: return False
    if any(not isinstance(record[k], str) for k in ("evidence_id", "scenario", "split", "procedure")): return False
    if type(record["success"]) is not bool or any(type(record[k]) is not int for k in ("length", "capacity")): return False
    selected = current["episode"]["selection"]["selected"]
    return (record["evidence_id"] == selected["case_id"] and record["scenario"] == current["learner"]["scenario"]
        and record["split"] == "acquisition" and record["procedure"] == fixture.PROCEDURE
        and (record["length"], record["capacity"]) == (selected["length"], selected["capacity"]))


def accept(current):
    state = current["learner"]
    if current["episode"]["phase"] != "closed" or state["phase"] != "validation" or set(state["evidence"]["validation"]) != set(fixture.VALIDATION):
        raise ValueError("closed investigation and complete reserved validation required")
    if digest(state["evidence"]["train"]) != state["derivation"]["training_digest"]: raise ValueError("training changed after selection")
    retained = ambiguity.filter_hypotheses(state["derivation"]["survivors"], {eid:e["record"] for eid,e in current["acquired"].items()})
    if retained != current["survivors"]: raise ValueError("effective hypothesis set changed outside verified acquisition")
    checks = [{"hypothesis":deepcopy(h), "evidence_id":eid,
               "predicted":learner.evaluate(h, learner.case(eid, (r["length"],r["capacity"]))), "observed":r["success"]}
              for h in retained for eid,r in state["evidence"]["validation"].items()]
    accepted = bool(retained) and all(c["predicted"] == c["observed"] for c in checks)
    current["acceptance"] = {"accepted":accepted, "reason":"no_supported_hypothesis" if not retained else
        "validated_retained_set" if accepted else "validation_rejected", "hypotheses":deepcopy(retained), "checks":checks,
        "validation_digest":digest(state["evidence"]["validation"]), "acquisition_refs":sorted(current["acquired"])}
    state["phase"] = "evaluation"


def handle(state, message, models, receipt):
    from .runtime import emit
    current = state["judgment"]; ep = current["episode"]; content = message["content"]
    def respond(text, **extra): emit(state, "response", {"text":text, **extra}, message["id"])
    def reject(reason):
        receipt.update(status="rejected", reason=reason); respond("Rejected: " + reason); return state
    if set(content) != {"text", "operation", "record"} or not isinstance(content["record"],dict): return reject("invalid active relationship content")
    operation, record = content["operation"], content["record"]
    if operation == "verification":
        if not state["learning"]: return reject("learning disabled")
        if message["type"] != "teacher_reply" or message["source"] != fixture.SOURCE: return reject("verification requires registered correlated reply")
        if set(record) != {"episode_id", "request_id", "evidence"}: return reject("malformed verification record")
        if (ep["request_count"] != 1 or ep["request_id"] is None or record["episode_id"] != ep["id"]
                or record["request_id"] != ep["request_id"] or message.get("reply_to") != ep["request_id"]):
            return reject("unrelated episode/request correlation")
        evidence = record["evidence"]
        if not registered_acquisition(evidence,current): return reject("malformed or unregistered acquisition evidence")
        eid = evidence["evidence_id"]; previous = current["acquired"].get(eid)
        if previous is not None:
            if digest(evidence) != digest(previous["record"]): return reject("conflicting acquisition evidence identity")
            receipt.update(status="duplicate_evidence", evidence_ref=eid)
            respond("Duplicate acquisition; no revision or budget change."); return state
        question = state["questions"].get(ep["request_id"])
        limit = ep.get("receiver_attempt_budget")
        if limit is not None and ep["receiver_exhausted"]:
            receipt.update(status="verification_budget_exhausted",reason="receiver verification budget exhausted; episode closed")
            respond("Receiver verification budget exhausted; no new computation or resolution."); return state
        if ep["phase"] != "pending" or question is None or question["status"] != "pending" or question["answered_by"] is not None:
            return reject("verification requires the still-pending request")
        def exhaust():
            ep.update(phase="closed",closed_reason="receiver_budget_exhausted",receiver_exhausted=True)
            question.update(status="receiver_budget_exhausted",closed_by=message["id"])
            receipt["receiver_exhaustion_transition"] = True
        if limit is not None:
            receipt["eligible_verification_checks"] = 1
            if ep["receiver_attempts"] >= limit:
                exhaust()
                receipt.update(status="verification_budget_exhausted",reason="receiver verification budget exhausted")
                respond("Receiver verification budget exhausted; hypotheses remain unresolved."); return state
            ep["receiver_attempts"] += 1
            receipt.update(receiver_attempt_charged=1,receiver_attempts_after=ep["receiver_attempts"])
        receipt["verification_executions"] = 1
        if evidence["success"] != fixture.execute(evidence["length"],evidence["capacity"]):
            if limit is not None and ep["receiver_attempts"] >= limit: exhaust()
            return reject("unverified acquisition label; receiver budget exhausted" if limit is not None and ep["receiver_exhausted"] else "unverified acquisition label")
        before = deepcopy(current["survivors"])
        current["survivors"] = ambiguity.filter_hypotheses(before, {eid:evidence})
        current["support_status"] = learner.support_status(current["survivors"])
        current["acquired"][eid] = {"record":deepcopy(evidence), "message_id":message["id"], "source":message["source"],
            "sender":message["sender"], "reply_to":message["reply_to"], "episode_id":ep["id"],
            "verification":"selected correlated noiseless device outcome"}
        current["filter_trace"].append({"evidence_ref":eid, "before":before, "after":deepcopy(current["survivors"]),
                                       "selector":"unchanged ambiguity.filter_hypotheses"})
        ep.update(phase="closed",closed_reason="verified_reply",verified_observations=1)
        question.update(answered_by=message["id"],status="answered")
        receipt.update(status="accepted_acquisition",evidence_ref=eid)
        respond("Verified acquisition retained; validation still required.",support_status=current["support_status"]); return state
    if message["type"] != "observation": return reject("reply is only eligible for verification")
    if operation == "barrier" and not record: receipt["status"]="barrier"; respond("Input barrier reached."); return state
    if operation == "evaluate":
        result = predict(current,record); receipt["status"]="evaluated"
        respond("Current prediction: " + result["decision"] + ".", result=result,
                scientific_digest=digest(scientific(current)),questions_digest=digest(state["questions"])); return state
    if operation not in ("outcome","select","investigate","close_investigation","accept"): return reject("unsupported active operation; no episode reset")
    if not state["learning"]: return reject("learning disabled")
    if operation == "outcome":
        if record.get("split") == "validation" and ep["phase"] != "closed": return reject("investigation must close before validation")
        reserved = current["learner"]
        if (message["source"] == fixture.SOURCE and fixture.registered(record,reserved["scenario"])
                and reserved["phase"] == record["split"] and record["evidence_id"] not in reserved["evidence"][record["split"]]):
            receipt.update(reserved_verification_executions=1,verification_split=record["split"])
        changed = deepcopy(current["learner"])
        status = learner.admit(changed,record,message["source"]); reason = changed["trace"][-1]["reason"]
        if status == "rejected": return reject(reason)
        if status == "duplicate": receipt["status"]="duplicate_evidence"; respond("Duplicate reserved evidence; no revision."); return state
        current["learner"]=changed
        current["evidence_links"][record["split"]+"/"+record["evidence_id"]] = {"message_id":message["id"],"source":message["source"],"sender":message["sender"]}
        receipt["status"]="accepted_evidence"; respond("Verified reserved outcome recorded."); return state
    if record: return reject("operation requires an empty record")
    if operation == "select":
        changed = deepcopy(current["learner"])
        try: learner.select(changed)
        except ValueError as exc: return reject(str(exc))
        current.update(learner=changed,survivors=deepcopy(changed["survivors"]),support_status=changed["support_status"])
        ep["phase"]="ready"; receipt["status"]="training_closed"; respond("Training closed; investigation may begin."); return state
    if operation == "investigate":
        if ep["phase"] != "ready" or ep["request_count"] != 0 or ep["request_id"] is not None:
            return reject("investigation is one-shot; no request budget reset")
        selection = choose(current) if len(current["survivors"]) > 1 else None
        ep["selection"] = selection
        selected = selection["selected"] if selection else None
        if selected is None:
            reason = "no_supported_hypothesis" if not current["survivors"] else "already_unique" if len(current["survivors"]) == 1 else "no_informative_candidate"
            ep.update(phase="closed",closed_reason=reason)
            receipt["status"]="investigation_closed"; respond("Investigation closed: " + reason + "."); return state
        ep.update(phase="pending",request_count=1)
        request = emit(state,"clarification_request",{"text":"Verify the selected synthetic observation; the request unit is already spent.",
            "episode_id":ep["id"],"candidate":deepcopy(selected),"expected_source":fixture.SOURCE,
            "request_count":1,"budget_remaining":0},message["id"])
        ep["request_id"]=request
        state["questions"][request]={"issue":"relationship_ambiguity","episode_id":ep["id"],"candidate":deepcopy(selected),
                                     "answered_by":None,"closed_by":None,"status":"pending"}
        receipt.update(status="request_issued",request_id=request,request_cost_units=1); return state
    if operation == "close_investigation":
        if ep["phase"] != "pending": return reject("only a pending investigation can be cancelled")
        ep.update(phase="closed",closed_reason="cancelled_without_verified_reply")
        state["questions"][ep["request_id"]].update(status="cancelled",closed_by=message["id"])
        receipt["status"]="investigation_cancelled"; respond("Investigation closed without refund or new episode."); return state
    try: accept(current)
    except ValueError as exc: return reject(str(exc))
    receipt["status"]="set_accepted" if current["acceptance"]["accepted"] else "set_rejected"
    respond("Validation complete; no fallback selection.",accepted=current["acceptance"]["accepted"]); return state
