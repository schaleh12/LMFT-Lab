"""Outcome projection over the shared correction ledger; no inference or propagation."""
from copy import deepcopy
from . import correction, contextual, judgment, outcome_fixture as fixture
from .runtime_store import digest

RULE = "outcome-correction-1"
MODES = ("outcome-lmft", "outcome-disabled", "outcome-memory")


def load_policy():
    return correction.load_policy("outcome_correction_authority.json")


def newborn(mode, policy=None):
    current = correction.newborn(mode, policy if policy is not None else load_policy())
    current.update(rule_version=RULE, recomputations=[])
    return current


def effective_samples(current, branch):
    return {root: current["ledger"][head] for root, head in sorted(current["heads"].items())
            if current["ledger"][head]["record"].get("kind") == "outcome"
            and current["ledger"][head]["record"]["branch"] == branch
            and current["ledger"][head]["record"]["scope"] == "batch-1"
            and current["ledger"][head]["record"]["procedure"] == "outcome-transmit-1"}


def snapshot(current):
    result = {}
    for name, branch in current["branches"].items():
        samples = effective_samples(current, name)
        positive = [{"event_id": root, "head": current["heads"][root]} for root, e in samples.items()
                    if e["record"]["output"] == e["record"]["payload"]]
        negative = [{"event_id": root, "head": current["heads"][root]} for root, e in samples.items()
                    if e["record"]["output"] != e["record"]["payload"]]
        category = judgment.probe(branch)["decision"]
        result[name] = {"score": branch["score"], "decision": {"support": "success", "oppose": "failure", "undetermined": "abstain"}[category],
                        "count": len(samples), "supporting": positive, "contradicting": negative,
                        "mixed": bool(positive and negative), "resolved": bool(samples) and not (positive and negative)}
    return result


def state_ref(current):
    branches = snapshot(current)
    return {**correction.effective_ref(current), "branches": branches,
            "outcome_count": sum(b["count"] for b in branches.values())}


def recompute(current, trigger, reason):
    before = deepcopy(current["branches"])
    for name in current["branches"]:
        branch = contextual.branch()
        samples = effective_samples(current, name)
        if current["mode"] == "outcome-memory":
            # Ordinary memory independently recounts the identical active records.
            branch["evidence"] = {root: {"sign": 1 if entry["record"]["output"] == entry["record"]["payload"] else -1,
                                         "head": current["heads"][root]} for root, entry in samples.items()}
            branch["score"] = sum(e["sign"] for e in branch["evidence"].values()) / (len(samples) + 2)
        else:
            # A derived projection, not new admissions or additional independent events.
            for root, entry in samples.items():
                record = entry["record"]
                message = {"id": entry["message_id"], "sender": entry["sender"], "source": entry["source"],
                           "content": {"evidence": {**record, "sample_id": root}}}
                branch, _ = judgment.apply_validated(branch, message, None,
                    sign=1 if record["output"] == record["payload"] else -1,
                    verification=entry["verification"])
        current["branches"][name] = branch
    current["recomputations"].append({"trigger": trigger, "reason": reason,
        "before_scores": {k: b["score"] for k, b in before.items()}, "after": snapshot(current)})


def predict(current, case):
    return {"case_id": case["case_id"], "scope": case["scope"], "branch": case["branch"],
            "payload": case["payload"], **snapshot(current)[case["branch"]]}


def cache_key(current, case):
    return digest({"case": case, "effective": {root: e["record"] for root, e in effective_samples(current, case["branch"]).items()}})


def synchronize(state, event):
    current = state["judgment"]
    for key, item in current["cases"].items():
        case = item["input"]
        cached = current["cache"].get(key)
        if cached and cached["key"] != cache_key(current, case):
            current["cache"].pop(key)
            event["cache_invalidated"].append(key)
        for qid, question in state["questions"].items():
            if question["case_id"] != key:
                continue
            resolved = predict(current, case)["resolved"]
            if resolved and question["status"] == "open":
                question.update(status="resolved_by_correction", closed_by=event["event_id"])
                event["closed_questions"].append(qid)
            elif not resolved and question["status"] != "open":
                question.update(status="open", closed_by=None, reopened_by=event["event_id"])
                event.setdefault("reopened_questions", []).append(qid)


def after_accept(state, event):
    recompute(state["judgment"], event["event_id"], "verified replacement; replay one active version per independent outcome")
    synchronize(state, event)


def handle(state, message, models, receipt):
    from .runtime import emit
    current = state["judgment"]
    content = message["content"]
    def respond(text, **extra):
        emit(state, "response", {"text": text, **extra}, message["id"])
    def reject(reason):
        receipt.update(status="rejected", reason=reason)
        current["rejected"].append({"message_id": message["id"], "reason": reason})
        respond("Rejected: " + reason)
        return state
    if set(content) != {"text", "operation", "record"} or not isinstance(content["record"], dict):
        return reject("invalid outcome-study content")
    op, record = content["operation"], content["record"]
    if op == "barrier":
        respond("Input barrier reached.")
        return state
    if op == "correction":
        return correction.correct(state, message, receipt, fixture=fixture, target_check=fixture.target_error,
            after_accept=after_accept, state_ref=state_ref, acceptance_disabled=current["mode"] == "outcome-disabled")
    if op == "evidence":
        eid = record.get("evidence_id")
        if not isinstance(eid, str):
            return reject("invalid evidence identity")
        if eid in current["ledger"]:
            if digest(record) != digest(current["ledger"][eid]["record"]):
                return reject("conflicting evidence identity")
            receipt.update(status="duplicate_evidence", evidence_ref=eid)
            receipt.pop("message", None)
            return state
        if message["source"] != fixture.SOURCE or not fixture.admitted(record):
            return reject("not a registered outcome instrument report")
        current["ledger"][eid] = {"record": deepcopy(record), "message_id": message["id"], "sender": message["sender"],
            "source": message["source"], "verification": "registered instrument log only; report may be erroneous", "root": eid, "parent": None}
        current["roots"][eid] = eid
        current["heads"][eid] = eid
        current["changes"].append({"evidence_id": eid, "reason": "admitted instrument report, not independent truth"})
        if record["kind"] == "outcome":
            recompute(current, eid, "initial registered outcome report")
            # Initial reports can also alter previously evaluated projections.
            synchronize(state, {"event_id": eid, "cache_invalidated": [], "closed_questions": []})
        respond("Instrument report retained with provenance; its accuracy remains revisable.")
        return state
    if op == "evaluate":
        if not fixture.valid_case(record):
            return reject("invalid public outcome probe")
        key = record["case_id"]
        item = current["cases"].setdefault(key, {"input": deepcopy(record), "request": None, "evaluations": []})
        signature = cache_key(current, record)
        cached = current["cache"].get(key)
        if cached and cached["key"] == signature:
            receipt["status"] = "evaluation_cache_hit"
            result = deepcopy(cached["result"])
        else:
            receipt["status"] = "evaluated"
            result = predict(current, record)
            current["cache"][key] = {"key": signature, "result": deepcopy(result)}
        item["evaluations"].append({"message_id": message["id"], "key": signature, "result": result})
        text = "Current scoped judgment: " + result["decision"] + ". Score " + str(result["score"]) + ". "
        text += "Outcome reports conflict; consistency remains unresolved." if result["mixed"] else "No conflicting effective reports; prediction is not guaranteed."
        if not result["count"]:
            text = "No outcome evidence; judgment abstains."
        if not result["resolved"] and item["request"] is None:
            qid = emit(state, "clarification_request", {"text": text + " Requesting independent outcome verification.", "result": result}, message["id"])
            item["request"] = qid
            state["questions"][qid] = {"case_id": key, "question": "outcome_consistency", "status": "open", "closed_by": None}
        else:
            respond(text, result=result)
        return state
    return reject("unsupported outcome-study operation")
