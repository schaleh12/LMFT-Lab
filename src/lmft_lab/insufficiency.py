"""Explicit hypothesis-family insufficiency; isolated from runtime and seed."""
from copy import deepcopy
from dataclasses import asdict
from . import capacity_relations as relations, insufficiency_fixture as fixture
from .birth import create_birth_state
from .runtime_store import digest

VERSION = "insufficiency-study-1"
SCOPE = {"procedure": fixture.PROCEDURE, "minimum": 0, "maximum": 8,
         "conditions": "noiseless empty bounded-write device; all length-two payloads refused"}


def configuration():
    return {"version": VERSION, "train": fixture.TRAIN, "validation": fixture.VALIDATION,
            "held_features": fixture.HELD, "hypotheses": relations.candidates(), "scope": SCOPE,
            "source": fixture.SOURCE, "verification_acquisition_budget": 0,
            "random_seed": 42, "model_calls": 0}


def case(identifier, pair):
    return {"case_id": identifier, "procedure": fixture.PROCEDURE,
            "length": pair[0], "capacity": pair[1]}


def in_scope(observation):
    return (isinstance(observation, dict) and set(observation) == {"case_id", "procedure", "length", "capacity"}
            and isinstance(observation["case_id"], str) and bool(observation["case_id"])
            and observation["procedure"] == fixture.PROCEDURE
            and all(type(observation[k]) is int and 0 <= observation[k] <= 8 for k in ("length", "capacity")))


def evaluate(hypothesis, observation):
    # Reuse the unchanged comparison language, with explicitly NEW study scope.
    if not relations.valid(hypothesis) or not in_scope(observation):
        raise ValueError("unsupported relationship or task scope")
    return relations.OPS[hypothesis["op"]](observation["length"], observation["capacity"])


def support_status(hypotheses):
    return "no_supported_hypothesis" if not hypotheses else "supported" if len(hypotheses) == 1 else "ambiguous"


def newborn(mode, scenario):
    if mode not in ("lmft", "memory") or scenario not in fixture.TRAIN:
        raise ValueError("unsupported study condition")
    return {"schema_version": 1, "version": VERSION, "mode": mode, "scenario": scenario,
            "birth": asdict(create_birth_state("insufficiency", birth_event_id="birth", random_seed=42)) if mode == "lmft" else None,
            "phase": "train", "support_status": "untrained", "survivors": [],
            "evidence": {"train": {}, "validation": {}}, "provenance": {},
            "derivation": None, "acceptance": None, "trace": []}


def admit(state, record, source=fixture.SOURCE):
    def finish(status, reason):
        state["trace"].append({"operation": "admit", "source": source,
                               "record": deepcopy(record), "status": status, "reason": reason})
        return status
    if source != fixture.SOURCE:
        return finish("rejected", "unregistered source")
    if not fixture.registered(record, state["scenario"]):
        return finish("rejected", "malformed or unregistered evidence")
    split, eid = record["split"], record["evidence_id"]
    prior = state["evidence"][split].get(eid)
    if prior is not None:
        return finish("duplicate" if prior == record else "rejected",
                      "duplicate evidence" if prior == record else "conflicting evidence identity")
    if state["phase"] != split:
        return finish("rejected", "evidence phase closed")
    if not fixture.verify(record, state["scenario"]):
        return finish("rejected", "unverified label; not a hypothesis contradiction")
    state["evidence"][split][eid] = deepcopy(record)
    state["provenance"][split + "/" + eid] = {
        "source": source, "record_digest": digest(record),
        "verification": "registered noiseless blocked-length-two device simulation"}
    return finish("accepted", "verified registered outcome")


def select(state):
    if state["phase"] != "train" or set(state["evidence"]["train"]) != set(fixture.TRAIN[state["scenario"]]):
        raise ValueError("complete training required; selection is one-shot")
    records = state["evidence"]["train"]
    evaluations = []
    for h in relations.candidates():
        checks = [{"evidence_id": eid, "predicted": evaluate(h, case(eid, (r["length"], r["capacity"]))),
                   "observed": r["success"]} for eid, r in records.items()]
        errors = [r["evidence_id"] for r in checks if r["predicted"] != r["observed"]]
        evaluations.append({"hypothesis": deepcopy(h), "checks": checks, "error_refs": errors, "consistent": not errors})
    state["survivors"] = [deepcopy(r["hypothesis"]) for r in evaluations if r["consistent"]]
    state["support_status"] = support_status(state["survivors"])
    state["derivation"] = {"candidate_evaluations": evaluations, "training_refs": list(records),
                           "training_digest": digest(records), "survivors": deepcopy(state["survivors"]),
                           "support_status": state["support_status"],
                           "reason": "retained exactly the training-consistent hypotheses; no fallback"}
    state["phase"] = "validation"
    state["trace"].append({"operation": "select", "derivation": deepcopy(state["derivation"])})


def accept(state):
    if state["phase"] != "validation" or set(state["evidence"]["validation"]) != set(fixture.VALIDATION):
        raise ValueError("complete validation required; acceptance is one-shot")
    if digest(state["evidence"]["train"]) != state["derivation"]["training_digest"]:
        raise ValueError("training changed after selection")
    if state["survivors"] != state["derivation"]["survivors"]:
        raise ValueError("hypothesis set changed after selection")
    checks = [{"hypothesis": deepcopy(h), "evidence_id": eid,
               "predicted": evaluate(h, case(eid, (r["length"], r["capacity"]))), "observed": r["success"]}
              for h in state["survivors"] for eid, r in state["evidence"]["validation"].items()]
    accepted = bool(state["survivors"]) and all(r["predicted"] == r["observed"] for r in checks)
    reason = "no_supported_hypothesis" if not state["survivors"] else "validated_retained_set" if accepted else "validation_rejected"
    state["acceptance"] = {"accepted": accepted, "reason": reason, "checks": checks,
                           "hypotheses": deepcopy(state["survivors"]),
                           "validation_refs": list(state["evidence"]["validation"]),
                           "validation_digest": digest(state["evidence"]["validation"])}
    state["phase"] = "evaluation"
    state["trace"].append({"operation": "accept", "acceptance": deepcopy(state["acceptance"])})


def predict(state, observation):
    result = {"case": deepcopy(observation), "decision": "out_of_scope", "reason": "outside_task_scope",
              "support_status": state["support_status"], "votes": [], "evidence_digest": digest(state["evidence"])}
    if not in_scope(observation):
        return result
    result["decision"] = "abstain"
    if state["support_status"] == "untrained":
        result["reason"] = "untrained"
    elif not state["survivors"]:
        result["reason"] = "no_supported_hypothesis"
    elif state["acceptance"] is None:
        result["reason"] = "not_validated"
    elif not state["acceptance"]["accepted"]:
        result["reason"] = state["acceptance"]["reason"]
    else:
        result["votes"] = [{"hypothesis": deepcopy(h), "value": evaluate(h, observation)} for h in state["survivors"]]
        values = {r["value"] for r in result["votes"]}
        result["reason"] = "hypothesis_disagreement"
        if len(values) == 1:
            result["decision"] = "success" if values.pop() else "failure"
            result["reason"] = "unanimous_supported_hypotheses"
    return result
