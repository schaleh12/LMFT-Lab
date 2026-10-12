"""Opt-in passive relationship sets through the existing supervised runtime."""
from copy import deepcopy
import json
from . import insufficiency as learner
from .capacity_relations import candidates
from .runtime_store import digest

RULE = "passive-relationship-set-1"
MODES = ("relationship-set-lmft", "relationship-set-memory")
SCENARIOS = tuple(learner.fixture.TRAIN)


def policy(scenario):
    if scenario not in SCENARIOS:
        raise ValueError("unsupported relationship scenario")
    # Manifest equality must survive JSON persistence (fixture pairs are tuples).
    return json.loads(json.dumps({"rule_version": RULE, "scenario": scenario, "task": learner.configuration(),
                                 "acquisition": "disabled; passive operations only", "model_calls": 0}))


def newborn(mode, scenario):
    if mode not in MODES:
        raise ValueError("unsupported relationship runtime mode")
    policy(scenario)
    # Both comparators use identical finite memory; runtime owns the birth scaffold.
    return {"mode": mode, "rule_version": RULE, "candidate_space": candidates(),
            "learner": learner.newborn("memory", scenario), "evidence_links": {}}


def scientific(current):
    """Comparable scientific projection; excludes condition/delivery identity."""
    return {"candidate_space": deepcopy(current["candidate_space"]),
            "learner": deepcopy(current["learner"])}


def snapshot(current):
    state = current["learner"]
    acceptance = state["acceptance"]
    validation = "not_validated" if acceptance is None else "validated" if acceptance["accepted"] else acceptance["reason"]
    return {"rule_version": RULE, "mode": current["mode"], "phase": state["phase"],
            "support_status": state["support_status"], "validation_status": validation,
            "candidate_space": deepcopy(current["candidate_space"]),
            "survivors": deepcopy(state["survivors"]),
            "evidence_refs": {split: sorted(records) for split, records in state["evidence"].items()}}


def predict(current, observation):
    return learner.predict(current["learner"], observation)


def handle(state, message, models, receipt):
    from .runtime import emit
    current = state["judgment"]
    content = message["content"]

    def respond(text, **extra):
        emit(state, "response", {"text": text, **extra}, message["id"])

    def reject(reason):
        receipt.update(status="rejected", reason=reason)
        respond("Rejected: " + reason)
        return state

    if (message["type"] != "observation" or set(content) != {"text", "operation", "record"}
            or not isinstance(content["record"], dict)):
        return reject("invalid passive relationship input")
    operation, record = content["operation"], content["record"]
    if operation == "barrier" and not record:
        receipt["status"] = "barrier"
        respond("Input barrier reached.")
        return state
    if operation == "evaluate":
        result = predict(current, record)
        receipt["status"] = "evaluated"
        respond("Current prediction: " + result["decision"] + ".", result=result,
                scientific_digest=digest(scientific(current)), evidence_links_digest=digest(current["evidence_links"]))
        return state
    if operation not in ("outcome", "select", "accept"):
        return reject("unsupported passive operation; no requests or proposals")
    if not state["learning"]:
        return reject("learning disabled")
    changed = deepcopy(current["learner"])
    if operation == "outcome":
        status = learner.admit(changed, record, message["source"])
        reason = changed["trace"][-1]["reason"]
        if status == "rejected":
            return reject(reason)
        if status == "duplicate":
            receipt.update(status="duplicate_evidence", evidence_ref=record["evidence_id"], reason=reason)
            respond("Duplicate evidence; no scientific revision.", evidence_id=record["evidence_id"])
            return state
        current["learner"] = changed
        ref = record["split"] + "/" + record["evidence_id"]
        current["evidence_links"][ref] = {"message_id": message["id"], "source": message["source"],
                                           "sender": message["sender"], "cycle": state["cycle"]}
        receipt.update(status="accepted_evidence", evidence_ref=record["evidence_id"], reason=reason)
        respond("Verified synthetic outcome recorded.", split=record["split"], evidence_id=record["evidence_id"])
        return state
    if record:
        return reject("select and accept require an empty record")
    try:
        learner.select(changed) if operation == "select" else learner.accept(changed)
    except ValueError as exc:
        return reject(str(exc))
    current["learner"] = changed
    receipt["status"] = "training_closed" if operation == "select" else "set_accepted" if changed["acceptance"]["accepted"] else "set_rejected"
    status = snapshot(current)
    respond("Training closed." if operation == "select" else "Validation complete.",
            support_status=status["support_status"], validation_status=status["validation_status"])
    return state
