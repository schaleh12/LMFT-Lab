"""Authored mechanical fixture, separate from founding seed and node equations."""
from copy import deepcopy

RULE_VERSION = "channel-agreement-1"
TARGET = "fixture/channel-agreement"
SAMPLES = {"sample-a": (3, 3), "sample-b": (4, 5), "sample-c": (7, 7), "sample-d": (8, 9)}


def newborn():
    return {"target": TARGET, "rule_version": RULE_VERSION, "score": 0.0, "evidence": {}, "revisions": []}


def probe(judgment):
    score = judgment["score"]
    return {"target": TARGET, "score": score,
            "decision": "support" if score >= 0.2 else "oppose" if score <= -0.2 else "undetermined"}


def revise(judgment, message, *, learning=True, rejection=None):
    result = deepcopy(judgment)
    evidence = message["content"].get("evidence")
    reason = rejection
    if reason is None:
        if evidence is None:
            reason = "no eligible measurement supplied"
        elif (not isinstance(evidence, dict) or set(evidence) != {"sample_id", "channel", "reference"}
              or not isinstance(evidence["sample_id"], str)
              or evidence["sample_id"] not in SAMPLES
              or type(evidence["channel"]) is not int or type(evidence["reference"]) is not int
              or (evidence["channel"], evidence["reference"]) != SAMPLES[evidence["sample_id"]]):
            reason = "measurement does not match frozen fixture"
        elif evidence["sample_id"] in result["evidence"]:
            reason = "sample already counted; repeated attribution is not independent evidence"
        elif not learning:
            reason = "learning disabled control"
    return apply_validated(judgment, message, reason)


def apply_validated(judgment, message, reason, *, sign=None,
                    verification="exact frozen fixture match"):
    """Shared existing counter update, after a fixture's explicit eligibility gate."""
    result = deepcopy(judgment)
    evidence = message["content"].get("evidence")
    accepted = reason is None
    if accepted:
        if sign is None:
            sign = 1 if evidence["channel"] == evidence["reference"] else -1
        result["evidence"][evidence["sample_id"]] = {"measurement": deepcopy(evidence), "sign": sign,
            "message_id": message["id"], "sender": message["sender"], "source": message["source"],
            "original_content": deepcopy(message["content"]), "verification": verification}
        values = result["evidence"].values()
        result["score"] = sum(e["sign"] for e in values) / (len(result["evidence"]) + 2)
        reason = "verified unique fixture sample; score = sum(signs)/(sample count + 2)"
    record = {"message_id": message["id"], "target": judgment["target"], "rule_version": judgment["rule_version"],
        "proposal": deepcopy(evidence), "accepted": accepted, "reason": reason,
        "before": judgment["score"], "after": result["score"],
        "supporting": [k for k, v in sorted(result["evidence"].items()) if v["sign"] == 1],
        "contradicting": [k for k, v in sorted(result["evidence"].items()) if v["sign"] == -1]}
    result["revisions"].append(record)
    return result, record
