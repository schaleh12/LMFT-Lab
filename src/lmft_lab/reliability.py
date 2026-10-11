"""Preregistered one-pass sorting fixture, not a general reliability estimator."""
from copy import deepcopy

from . import judgment
from .propagation import Association, PropagationConfig
from .runtime_store import digest

PROCEDURE = "adjacent-pass-1"
TARGET = "fixture/one-pass-sort-reliability"
RULE = "procedure-reliability-1"
TRIALS = {"t1": [1, 3, 2], "t2": [2, 1, 3], "t3": [3, 2, 1],
          "t4": [2, 3, 1], "t5": [4, 3, 2], "t6": [5, 4, 3]}
FACT = "psychological/truth/fact"
EXECUTION = "psychological/will/execution"
CONFIDENCE = "psychological/contemplation/confidence"
ASSOCIATIONS = tuple(Association(f"reliability-{i}", source, target, 1.0, 0.1, 0.5,
    "reliability-fixture-1", "reliability-fixture-1") for i, (source, target) in
    enumerate(((FACT, EXECUTION), (EXECUTION, CONFIDENCE))))
HELD_OUT = (
    {"id": "h1", "procedure": PROCEDURE, "input": [0, 2, 1]},
    {"id": "h2", "procedure": PROCEDURE, "input": [9, 7, 8]},
    {"id": "h3", "procedure": PROCEDURE, "input": [8, 9, 6]},
    {"id": "h4", "procedure": PROCEDURE, "input": [4, 1, 0]},
    {"id": "scope-length", "procedure": PROCEDURE, "input": [1, 2, 3, 4]},
    {"id": "scope-procedure", "procedure": "full-sort", "input": [0, 2, 1]},
)


def in_scope(procedure, values):
    return (procedure == PROCEDURE and isinstance(values, list) and len(values) == 3
            and all(type(x) is int and 0 <= x <= 9 for x in values))


def execute(values):
    result = list(values)
    for index in range(len(result) - 1):
        if result[index] > result[index + 1]:
            result[index], result[index + 1] = result[index + 1], result[index]
    return result


def evidence(sample_id):
    values = TRIALS[sample_id]
    return {"sample_id": sample_id, "procedure": PROCEDURE,
            "input": list(values), "output": execute(values)}


def newborn():
    result = judgment.newborn()
    result.update(target=TARGET, rule_version=RULE)
    return result


def eligibility(current, message, learning, rejection):
    item = message["content"].get("evidence")
    if rejection is not None:
        return rejection, None
    if item is None:
        return "no eligible procedure outcome supplied", None
    if (not isinstance(item, dict) or set(item) != {"sample_id", "procedure", "input", "output"}
            or not isinstance(item["sample_id"], str) or item["sample_id"] not in TRIALS
            or not in_scope(item["procedure"], item["input"])
            or item["input"] != TRIALS[item["sample_id"]]
            or not isinstance(item["output"], list) or any(type(x) is not int for x in item["output"])
            or item["output"] != execute(item["input"])):
        return "outcome fails registered trial and executable procedure verification", None
    if item["sample_id"] in current["evidence"]:
        return "sample already counted; repeated attribution is not independent evidence", None
    if not learning:
        return "learning disabled control", None
    return None, 1 if item["output"] == sorted(item["input"]) else -1


def revise(current, message, *, learning=True, rejection=None):
    reason, sign = eligibility(current, message, learning, rejection)
    return judgment.apply_validated(current, message, reason, sign=sign,
                                    verification="registered trial; executed adjacent pass; compared with sorted")


def baseline_revise(current, message, *, learning=True, rejection=None):
    """Independent ordinary-memory recount; no activation or shared update helper."""
    reason, sign = eligibility(current, message, learning, rejection)
    result = deepcopy(current)
    item = message["content"].get("evidence")
    accepted = reason is None
    if accepted:
        result["evidence"][item["sample_id"]] = {"measurement": deepcopy(item), "sign": sign,
            "message_id": message["id"], "sender": message["sender"], "source": message["source"],
            "original_content": deepcopy(message["content"]),
            "verification": "registered trial; executed adjacent pass; compared with sorted"}
        records = list(result["evidence"].values())
        successes = sum(record["sign"] == 1 for record in records)
        failures = sum(record["sign"] == -1 for record in records)
        result["score"] = (successes - failures) / (successes + failures + 2)
        reason = "verified unique fixture sample; score = sum(signs)/(sample count + 2)"
    record = {"message_id": message["id"], "target": TARGET, "rule_version": RULE,
        "proposal": deepcopy(item), "accepted": accepted, "reason": reason,
        "before": current["score"], "after": result["score"],
        "supporting": sorted(k for k, v in result["evidence"].items() if v["sign"] == 1),
        "contradicting": sorted(k for k, v in result["evidence"].items() if v["sign"] == -1)}
    result["revisions"].append(record)
    return result, record


def probe(current, case=None):
    case = case or HELD_OUT[0]
    basic = judgment.probe(current)
    scope = in_scope(case.get("procedure"), case.get("input"))
    action = {"support": "trial_with_verification", "oppose": "use_full_sort",
              "undetermined": "request_more_evidence"}[basic["decision"]] if scope else "out_of_scope"
    return {**basic, "target": TARGET, "in_scope": scope, "action": action,
            "uncertainty": "limited synthetic evidence; not a success guarantee"}


def wording(current):
    result = probe(current)
    support = sum(e["sign"] == 1 for e in current["evidence"].values())
    contrary = len(current["evidence"]) - support
    return (f"One-pass sort: {result['decision']} within the three-integer scope; "
            f"{support} verified successes, {contrary} verified failures. "
            f"Suggested probe action: {result['action']}. Limited synthetic evidence; not a success guarantee.")


class AuthoredModels:
    """Three labeled mock roles; memberships are authored, never inferred."""
    def complete(self, role, observation, node_ids, context):
        request = {"role": role, "observation": observation, "context": context}
        proposal = {"summary": "Authored procedure-fixture interpretation.",
            "memberships": [{"node_id": FACT, "relevance": 0.8,
                             "reason": "Authored association fixture, not semantic validation.",
                             "evidence_quote": observation[:20]}],
            "uncertainties": ["The aggregate score cannot guarantee the next outcome."],
            "questions": [], "proposed_judgment": None}
        return proposal, {"role": role, "execution": "mock", "fixture": RULE,
            "request": request, "request_sha256": digest(request), "proposal": proposal}

    def close(self):
        pass
