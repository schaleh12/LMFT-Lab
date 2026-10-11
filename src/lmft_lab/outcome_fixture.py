"""Separately versioned outcome instrument log and independent reference fixture."""
from copy import deepcopy
from .runtime_store import digest

RULE = "outcome-instrument-log-1"
SOURCE = "registered-outcome-log-1"
AUTHORITY = "fixture-curator"
VALIDATOR = "registered-outcome-reference-1"
COORDINATES = ("event_id", "kind", "scope", "branch", "procedure", "payload")
IDS = tuple("o" + str(i) for i in range(1, 13))


def initial_records(key):
    if key not in IDS:
        raise ValueError("unknown outcome scenario")
    signs = {"o1": [1], "o3": [1, 1, 1, 1], "o4": [1, 1, 1, -1], "o12": [-1, 1]}.get(key, [-1])
    def outcome(index, branch, sign):
        eid = key + "/event-" + str(index)
        return {"evidence_id": eid, "event_id": eid, "kind": "outcome", "scope": "batch-1",
                "branch": branch, "procedure": "outcome-transmit-1", "payload": index,
                "output": index if sign == 1 else index + 1, "source": SOURCE}
    records = [outcome(i+1, "shielded", sign) for i, sign in enumerate(signs)]
    records.append(outcome(99, "unshielded", 1))
    if key == "o7":
        records.append({"evidence_id": key + "/annotation", "kind": "observation", "scope": "batch-1",
                        "branch": "shielded", "note": "instrument maintenance", "source": SOURCE})
    return records


def admitted(record):
    return any(digest(record) == digest(r) for key in IDS for r in initial_records(key))


def target_error(target, replacement):
    if target.get("kind") != "outcome":
        return "target is not an outcome sample"
    if any(replacement.get(k) != target.get(k) for k in COORDINATES):
        return "replacement changes independent event, scope, branch or measurement coordinate"
    return None


def replacement_valid(record, correction_id):
    fields = {"evidence_id", "event_id", "kind", "scope", "branch", "procedure", "payload", "output", "source"}
    if set(record) != fields or type(record["payload"]) is not int or type(record["output"]) is not int:
        return False
    # Independent reference is queried only for the proposed stable event, never held-out truth.
    for key in IDS:
        original = initial_records(key)[0]
        if record["event_id"] == original["event_id"]:
            expected = original["payload"] + (1 if key in ("o1", "o3", "o4") else 0)
            return (record["evidence_id"] == "replacement/" + correction_id
                    and record["source"] == VALIDATOR and target_error(original, record) is None
                    and record["output"] == expected)
    return False


def proposal(cid, target, output):
    replacement = {**target, "evidence_id": "replacement/"+cid, "output": output, "source": VALIDATOR}
    return {"correction_id": cid, "authority": AUTHORITY, "target_id": target["evidence_id"],
            "expected_digest": digest(target), "reason": "Independent registered reference verifies the same outcome event.",
            "replacement": replacement}


def corrections(key):
    records = initial_records(key); target = records[0]
    output = target["payload"] + (1 if key in ("o1", "o3", "o4") else 0)
    first = proposal(key+"-a", target, output)
    if key == "o6":
        wrong = deepcopy(first); wrong["replacement"]["output"] = output+5
        malformed = proposal(key+"-b", target, output); malformed["replacement"]["output"] = True
        return [wrong, malformed]
    if key == "o7":
        missing = deepcopy(first); missing["target_id"] = "nonexistent"
        scope = proposal(key+"-b", target, output); scope["replacement"]["branch"] = "unshielded"
        annotation = proposal(key+"-c", records[-1], output)
        return [missing, scope, annotation]
    if key == "o9":
        conflict = deepcopy(first); conflict["replacement"]["output"] += 1
        return [first, conflict]
    if key == "o10":
        competing = proposal(key+"-b", target, output)
        stale = proposal(key+"-c", first["replacement"], output); stale["expected_digest"] = "0"*64
        return [first, competing, stale]
    if key == "o11":
        return [first, proposal(key+"-b", first["replacement"], output)]
    return [first]


def public_case(key, variant="warm"):
    if key not in IDS or variant not in ("warm", "fresh-1", "fresh-2", "other"):
        raise ValueError("unknown outcome probe")
    return {"case_id": key+"-"+variant, "scope": "batch-1", "procedure": "outcome-transmit-1",
            "branch": "unshielded" if variant == "other" else "shielded",
            "payload": {"warm": 20, "fresh-1": 31, "fresh-2": 47, "other": 53}[variant]}


def valid_case(record):
    return any(digest(record) == digest(public_case(key, variant)) for key in IDS for variant in ("warm", "fresh-1", "fresh-2", "other"))


def actual_success(key, variant):
    if key not in IDS or variant not in ("fresh-1", "fresh-2"):
        raise ValueError("outcomes are available only to held-out evaluation")
    # Opposite outcomes across the two fresh payloads prevent repair implying perfect prediction.
    return (key != "o1") if variant == "fresh-1" else (key == "o1")
