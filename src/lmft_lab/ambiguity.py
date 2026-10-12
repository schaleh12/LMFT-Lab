"""Isolated, finite hypothesis-set study; no runtime/model/seed revision."""
from copy import deepcopy
from dataclasses import asdict
from . import capacity_relations as relations
from .birth import create_birth_state
from .runtime_store import digest

VERSION = "ambiguity-study-1"
SOURCE = "registered-ambiguity-1"
TRAIN = {"t1": (1, 3), "t2": (2, 4), "t3": (4, 2), "t4": (3, 1)}
QUERIES = {"q1": (0, 2), "q2": (5, 5), "q3": (6, 6), "q4": (7, 6)}
VALIDATION = {"v1": (0, 3), "v2": (2, 5), "v3": (5, 2), "v4": (7, 4)}
HELD = {"h1": (2, 2), "h2": (3, 3), "h3": (7, 7), "h4": (8, 8),
        "h5": (0, 1), "h6": (4, 6), "h7": (6, 4), "h8": (8, 7), "x1": (9, 8)}
POLICIES = ("disagreement", "noninformative", "unavailable", "no-evidence")


def case(identifier, pair):
    return {"case_id": identifier, "procedure": relations.SCOPE["procedure"],
            "length": pair[0], "capacity": pair[1]}


def configuration():
    return {"version": VERSION, "train": TRAIN, "queries": QUERIES,
            "validation": VALIDATION, "held_features": HELD, "policies": POLICIES,
            "hypotheses": relations.candidates(), "scope": relations.SCOPE,
            "verification_budget": 1, "random_seed": 42, "model_calls": 0}


def newborn(mode, policy):
    if mode not in ("lmft", "memory") or policy not in POLICIES:
        raise ValueError("unsupported study condition")
    return {"schema_version": 1, "version": VERSION, "mode": mode, "policy": policy,
            "birth": asdict(create_birth_state("ambiguity", birth_event_id="birth", random_seed=42)) if mode == "lmft" else None,
            "phase": "train", "evidence": {"train": {}, "acquisition": {}, "validation": {}},
            "survivors": [], "initial_survivors": [], "selection": None,
            "verified_requests": 0, "acceptance": None, "trace": []}


def filter_hypotheses(hypotheses, records):
    return [deepcopy(h) for h in hypotheses if all(
        relations.evaluate(h, case(eid, (r["length"], r["capacity"]))) == r["success"]
        for eid, r in records.items())]


def choose(hypotheses, observations):
    """Feature-only acquisition; no verifier, outcomes or equality preference."""
    scored = []
    for observation in observations:
        if not relations.in_scope(observation):
            raise ValueError("invalid candidate features")
        votes = [relations.evaluate(h, observation) for h in hypotheses]
        score = sum(votes) * (len(votes) - sum(votes))
        scored.append({"case": deepcopy(observation), "votes": votes, "score": score})
    best = max((row["score"] for row in scored), default=0)
    selected = next((row["case"] for row in scored if row["score"] == best), None) if best else None
    return {"scored": scored, "selected": deepcopy(selected), "tie_policy": "first in declared order"}


def outcome(identifier, split):
    # Independent simulator is confined to evidence acquisition/scoring callers.
    from .capacity_fixture import execute
    pair = {"train": TRAIN, "acquisition": QUERIES, "validation": VALIDATION}[split][identifier]
    return {"evidence_id": identifier, "split": split, "procedure": relations.SCOPE["procedure"],
            "length": pair[0], "capacity": pair[1], "success": execute(*pair)}


def admit(state, record, source=SOURCE):
    """Admission is separate from hypothesis selection; preserve rejected inputs."""
    def finish(status, reason):
        state["trace"].append({"operation": "admit", "source": source, "record": deepcopy(record),
                               "status": status, "reason": reason})
        return status
    if not isinstance(record, dict) or set(record) != {"evidence_id", "split", "procedure", "length", "capacity", "success"}:
        return finish("rejected", "invalid record schema")
    eid, split = record["evidence_id"], record["split"]
    if source != SOURCE or not isinstance(eid, str) or not isinstance(split, str):
        return finish("rejected", "invalid source or identity")
    if type(record["success"]) is not bool or any(type(record[k]) is not int for k in ("length", "capacity")):
        return finish("rejected", "invalid value type")
    prior = next((records[eid] for records in state["evidence"].values() if eid in records), None)
    if prior is not None:
        return finish("duplicate" if prior == record else "rejected", "existing evidence identity")
    if split not in state["evidence"] or state["phase"] != split:
        return finish("rejected", "ineligible split or phase")
    table = {"train": TRAIN, "acquisition": QUERIES, "validation": VALIDATION}[split]
    if eid not in table or (record["length"], record["capacity"]) != table[eid] or record["procedure"] != relations.SCOPE["procedure"]:
        return finish("rejected", "unregistered features")
    if split == "acquisition":
        selected = state["selection"]["selected"]
        if state["verified_requests"] >= 1 or selected is None or selected["case_id"] != eid:
            return finish("rejected", "not selected or budget exhausted")
    if record != outcome(eid, split):
        return finish("rejected", "verifier mismatch")
    state["evidence"][split][eid] = deepcopy(record)
    if split == "acquisition":
        state["verified_requests"] += 1
        prior_hypotheses = deepcopy(state["survivors"])
        state["survivors"] = filter_hypotheses(state["survivors"], {eid: record})
        state["trace"].append({"operation": "filter", "evidence_ref": eid,
                               "before": prior_hypotheses, "after": deepcopy(state["survivors"])})
    return finish("accepted", "registered bounded-write verification")


def select(state):
    if state["phase"] != "train" or set(state["evidence"]["train"]) != set(TRAIN):
        raise ValueError("complete training required; selection is one-shot")
    state["survivors"] = filter_hypotheses(relations.candidates(), state["evidence"]["train"])
    state["initial_survivors"] = deepcopy(state["survivors"])
    ids = ("q1", "q4") if state["policy"] == "unavailable" else tuple(QUERIES)
    selection = choose(state["survivors"], [case(eid, QUERIES[eid]) for eid in ids])
    if state["policy"] == "noninformative":
        selection["selected"] = case("q1", QUERIES["q1"])
    elif state["policy"] == "no-evidence":
        selection["selected"] = None
    selection["policy"] = state["policy"]
    selection["training_digest"] = digest(state["evidence"]["train"])
    state["selection"] = selection
    state["phase"] = "acquisition"
    state["trace"].append({"operation": "select", "selection": deepcopy(selection),
                           "survivors": deepcopy(state["survivors"])})


def close_acquisition(state):
    if state["phase"] != "acquisition":
        raise ValueError("acquisition already closed")
    if state["selection"]["selected"] is not None and state["verified_requests"] != 1:
        raise ValueError("selected observation requires verification")
    state["phase"] = "validation"


def accept(state):
    if state["phase"] != "validation" or set(state["evidence"]["validation"]) != set(VALIDATION):
        raise ValueError("complete validation required; acceptance is one-shot")
    if digest(state["evidence"]["train"]) != state["selection"]["training_digest"]:
        raise ValueError("training changed after selection")
    checks = [{"hypothesis": deepcopy(h), "evidence_id": eid,
               "predicted": relations.evaluate(h, case(eid, (r["length"], r["capacity"]))),
               "observed": r["success"]} for h in state["survivors"]
              for eid, r in state["evidence"]["validation"].items()]
    state["acceptance"] = {"accepted": bool(state["survivors"]) and all(r["predicted"] == r["observed"] for r in checks),
                           "checks": checks, "validation_digest": digest(state["evidence"]["validation"]),
                           "hypotheses": deepcopy(state["survivors"])}
    state["phase"] = "evaluation"
    state["trace"].append({"operation": "accept", "acceptance": deepcopy(state["acceptance"])})


def predict(state, observation):
    result = {"case": deepcopy(observation), "decision": "out_of_scope", "votes": [],
              "evidence_digest": digest(state["evidence"])}
    if not relations.in_scope(observation):
        return result
    result["decision"] = "abstain"
    if state["acceptance"] and state["acceptance"]["accepted"]:
        result["votes"] = [{"hypothesis": deepcopy(h), "value": relations.evaluate(h, observation)}
                           for h in state["acceptance"]["hypotheses"]]
        values = {v["value"] for v in result["votes"]}
        if len(values) == 1:
            result["decision"] = "success" if values.pop() else "failure"
    return result
