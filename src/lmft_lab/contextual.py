"""Authored-feature conditional lookup and verifiable clarification, not fuzzy inference."""
from copy import deepcopy
from .judgment import apply_validated
from .runtime_store import digest
from .context_wording import formulate, renderings

RULE = "context-transmission-1"
PROCEDURE = "transmit-1"
MODES = ("context-lmft", "context-memory", "context-aggregate")
TRIALS = {"s1": (0, True, 0), "s2": (1, True, 1), "s3": (2, True, 0), "s4": (3, True, 2),
          "u1": (4, False, 1), "u2": (5, False, 2), "u3": (6, False, 1), "u4": (7, False, 0),
          **{f"c{i}": (i + 3, True, 2) for i in range(1, 5)}}
CASES = {"h1": (8, True, 0), "h2": (9, True, 1), "h3": (8, True, 2),
         "h4": (8, False, 1), "h5": (9, False, 2), "h6": (8, False, 0),
         "m1": (9, True, 0), "m2": (9, False, 1), "x1": (8, True, 0), "x2": (10, True, 0)}


def execute(payload, shielded, disturbance):
    return payload if disturbance == 0 or shielded and disturbance == 1 else (payload + 1) % 10


def outcome(identifier):
    payload, shielded, disturbance = TRIALS[identifier]
    return {"evidence_id": identifier, "procedure": PROCEDURE, "payload": payload, "shielded": shielded,
            "disturbance": disturbance, "output": execute(payload, shielded, disturbance)}


def case(identifier, missing=False):
    payload, shielded, _ = CASES[identifier]
    return {"case_id": identifier, "procedure": "other-1" if identifier == "x1" else PROCEDURE,
            "payload": payload, "shielded": None if missing else shielded}


def branch():
    return {"target": "fixture/transmission", "rule_version": RULE, "score": 0.0, "evidence": {}, "revisions": []}


def newborn(mode):
    keys = ["all"] if mode == "context-aggregate" else ["shielded", "unshielded"]
    return {"target": "fixture/contextual-transmission", "rule_version": RULE, "mode": mode, "version": 0,
            "branches": {key: branch() for key in keys}, "evidence": {}, "conditions": {},
            "cache": {}, "rejected": []}


def valid_case(record):
    return (isinstance(record, dict) and set(record) == {"case_id", "procedure", "payload", "shielded"}
            and isinstance(record["case_id"], str) and record["case_id"] in CASES
            and type(record["payload"]) is int and isinstance(record["procedure"], str)
            and (record["shielded"] is None or type(record["shielded"]) is bool))


def probe(current, record=None):
    if record is None:
        return {"version": current["version"], "scores": {k: v["score"] for k, v in current["branches"].items()}}
    supplied = record.get("shielded")
    known = current["conditions"].get(record.get("case_id"))
    condition = supplied if supplied is not None else known["record"]["shielded"] if known else None
    result = {"case_id": record.get("case_id"), "condition": condition, "score": None,
              "decision": "out_of_scope", "evidence_refs": [], "version": current["version"],
              "uncertainty": "limited synthetic evidence, not a guarantee"}
    if not valid_case(record) or record["procedure"] != PROCEDURE or not 0 <= record["payload"] <= 9:
        return result
    if record["payload"] != CASES[record["case_id"]][0]:
        return result
    if condition is None:
        result["decision"] = "pending_condition"
        return result
    key = "all" if current["mode"] == "context-aggregate" else "shielded" if condition else "unshielded"
    selected = current["branches"][key]
    value = selected["score"]
    result.update(branch=key, score=value, evidence_refs=sorted(selected["evidence"]),
                  decision="success" if value >= .2 else "failure" if value <= -.2 else "abstain")
    return result


def _publish(state, message, record, models):
    from .runtime import emit
    current = state["judgment"]
    result = probe(current, record)
    if result["decision"] == "pending_condition":
        for identifier, request in state["questions"].items():
            if request["case"]["case_id"] == record["case_id"] and request["answered_by"] is None:
                return {"status": "pending_existing", "request_id": identifier}
    key = digest({"case": record, "version": current["version"], "mode": current["mode"], "rule": RULE,
                  "condition": current["conditions"].get(record["case_id"])})
    cached = current["cache"].get(key)
    if cached:
        content = deepcopy(cached)
        status = "evaluation_cache_hit"
    else:
        text = renderings(result)[0]
        origin = "authored"
        if state["manifest"]["mode"] == "local":
            text, trace = formulate(models, result)
            trace.update(message_id=message["id"], context_key=key)
            state["diagnostics"].append(trace)
            origin = "model-constrained" if trace["status"] == "validated" else "authored-fallback"
        content = {"text": text, "evaluation": result, "wording_origin": origin}
        current["cache"][key] = deepcopy(content)
        status = "evaluated"
    kind = "clarification_request" if result["decision"] == "pending_condition" else "response"
    identifier = emit(state, kind, content, message["id"])
    state["outbox"][-1]["source"] = "context-communication-1"
    if kind == "clarification_request":
        state["questions"][identifier] = {"case": deepcopy(record), "answered_by": None,
                                          "trigger_message": message["id"]}
    return {"status": status, "context_key": key, "output_id": identifier}


def _reject(state, message, reason):
    from .runtime import emit
    state["judgment"]["rejected"].append({"message_id": message["id"], "reason": reason})
    emit(state, "response", {"status": "rejected", "reason": reason, "text": "Input rejected; no judgment or pending answer changed."}, message["id"])
    return {"status": "rejected", "reason": reason}


def _lightweight(receipt, message, status, current):
    receipt.pop("message", None)
    receipt.update(status=status, sender=message["sender"], source=message["source"],
                   payload_sha256=digest(message["content"]["record"]), context_version=current["version"])


def handle(state, message, models, receipt):
    """Common envelope/delivery validation has already run; mutate private cycle copy."""
    from .runtime import emit
    current = state["judgment"]
    content = message["content"]
    if set(content) != {"text", "operation", "record"} or not isinstance(content["record"], dict):
        receipt.update(_reject(state, message, "invalid contextual content"))
        return state
    operation, record = content["operation"], content["record"]
    if (operation == "condition") != (message["type"] == "teacher_reply"):
        receipt.update(_reject(state, message, "condition requires a linked teacher reply; other operations require observation"))
        return state
    if operation == "barrier" and record == {}:
        emit(state, "response", {"status": "barrier", "text": "Cycle boundary reached."}, message["id"])
    elif operation == "outcome":
        identifier = record.get("evidence_id")
        prior = current["evidence"].get(identifier) if isinstance(identifier, str) else None
        if prior:
            if digest(prior["record"]) == digest(record):
                _lightweight(receipt, message, "duplicate_evidence", current)
                receipt["original_message_id"] = prior["message_id"]
                return state
            receipt.update(_reject(state, message, "conflicting reuse of evidence ID"))
            return state
        valid = (isinstance(identifier, str) and identifier in TRIALS and record == outcome(identifier)
                 and type(record.get("shielded")) is bool
                 and all(type(record.get(k)) is int for k in ("payload", "disturbance", "output")))
        if not valid or not state["learning"]:
            receipt.update(_reject(state, message, "unverified outcome" if not valid else "learning disabled control"))
            return state
        sign = 1 if record["output"] == record["payload"] else -1
        key = "all" if current["mode"] == "context-aggregate" else "shielded" if record["shielded"] else "unshielded"
        selected = current["branches"][key]
        adapted = {**message, "content": {"text": content["text"], "evidence": {**record, "sample_id": identifier}}}
        if current["mode"] == "context-lmft":
            updated, revision = apply_validated(selected, adapted, None, sign=sign,
                                                verification="registered transmission executed")
        else:
            # Independent transparent conditional/aggregate memory recount.
            updated = deepcopy(selected)
            updated["evidence"][identifier] = {"sign": sign, "message_id": message["id"], "record": deepcopy(record)}
            signs = [e["sign"] for e in updated["evidence"].values()]
            updated["score"] = (signs.count(1) - signs.count(-1)) / (len(signs) + 2)
            revision = {"message_id": message["id"], "accepted": True, "before": selected["score"],
                        "after": updated["score"], "reason": "verified unique outcome; sum(signs)/(n+2)",
                        "supporting": sorted(k for k,v in updated["evidence"].items() if v["sign"] == 1),
                        "contradicting": sorted(k for k,v in updated["evidence"].items() if v["sign"] == -1)}
            updated["revisions"].append(revision)
        current["branches"][key] = updated
        current["evidence"][identifier] = {"record": deepcopy(record), "sign": sign,
            "message_id": message["id"], "sender": message["sender"], "source": message["source"], "text": content["text"]}
        current["version"] += 1
        emit(state, "response", {"status": "accepted", "evidence_id": identifier, "branch": key,
            "score": updated["score"], "reason": revision["reason"], "text": "Verified outcome recorded."}, message["id"])
    elif operation == "evaluate":
        if not valid_case(record):
            receipt.update(_reject(state, message, "malformed evaluation case"))
        elif record["shielded"] is not None and record["shielded"] != CASES[record["case_id"]][1]:
            receipt.update(_reject(state, message, "provided condition disagrees with registered case"))
        else:
            receipt.update(_publish(state, message, record, models))
    elif operation == "condition":
        request = state["questions"].get(message.get("reply_to"))
        identifier = record.get("case_id")
        existing = current["conditions"].get(identifier) if isinstance(identifier, str) else None
        if existing and digest(existing["record"]) == digest(record) and request and request["answered_by"] == existing["message_id"]:
            _lightweight(receipt, message, "duplicate_condition", current)
            return state
        valid = (request is not None and request["answered_by"] is None
                 and set(record) == {"evidence_id", "case_id", "shielded"}
                 and identifier == request["case"]["case_id"]
                 and record["evidence_id"] == "condition/" + identifier
                 and type(record["shielded"]) is bool and record["shielded"] == CASES[identifier][1])
        if not valid:
            receipt.update(_reject(state, message, "reply does not verify the pending case condition"))
            return state
        current["conditions"][identifier] = {"record": deepcopy(record), "message_id": message["id"],
            "sender": message["sender"], "source": message["source"], "reply_to": message["reply_to"]}
        request["answered_by"] = message["id"]
        receipt.update(_publish(state, message, request["case"], models))
    else:
        receipt.update(_reject(state, message, "unknown operation"))
    return state
