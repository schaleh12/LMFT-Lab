"""Bounded teacher proposals around existing developmental route associations."""
from copy import deepcopy
import hashlib
import json
from . import attention as a, teacher_fixture as f
from .teacher_profile import make_request, validate_lesson
from .runtime_store import digest
from .model_assets import BACKEND_VERSION, BACKEND_FILES

RULE = "local-teacher-routes-1"
MODES = ("teacher-lmft", "teacher-none", "teacher-memory")


def newborn(mode, study=None):
    current = a.newborn("attention-memory" if mode == "teacher-memory" else "attention-lmft")
    current.update(teacher_mode=mode, calibration={}, lessons=[], teaching_request=None)
    if study is not None:
        current["briefing_study"] = study["situation"]
        current["weights"] = deepcopy(study["initial_weights"])
    return current


def selection(current, case):
    return a.select(current, case)


def validation(current):
    rows = []
    for key in f.VALIDATION:
        selected, _ = selection(current, f.public_case(key))
        rows.append({"case_id": key, "selected": selected,
                     "resolved": f.validation_resolves(key, selected),
                     "irrelevant": bool(selected and selected["field"] != "shielded")})
    return {"rows": rows, "resolved": sum(x["resolved"] for x in rows),
            "irrelevant": sum(x["irrelevant"] for x in rows)}


def assess(current, proposal):
    refs = proposal["supporting_evidence"]
    records = [current["calibration"].get(x) for x in refs]
    route, weight = proposal["route"], proposal["weight"]
    before = validation(current)
    candidate = deepcopy(current)
    candidate["weights"][route] = weight
    after = validation(candidate)
    direction = weight > current["weights"][route]
    grounded = (weight != current["weights"][route] and all(r and r["record"]["route"] == route
                and r["record"]["available"] == direction for r in records))
    accepted = bool(grounded and after["resolved"] > before["resolved"] and after["irrelevant"] <= before["irrelevant"])
    return {"accepted": accepted, "reason": "grounded direction and strict validation improvement" if accepted
            else "unsupported direction or no strict validation improvement", "before": before, "after": after}


def context(state):
    current = state["judgment"]
    result = {"question": "What single reusable route preference is justified by these calibration observations?",
            "training_evidence": [deepcopy(x["record"]) for x in current["calibration"].values()],
            "weights": deepcopy(current["weights"]),
            "supported_judgments": {k: {"score": b["score"], "evidence_refs": sorted(b["evidence"])} for k, b in current["branches"].items()},
            "capabilities": state["manifest"]["teacher_profile"]["profile"]["capabilities"]}
    if state["manifest"]["teacher_profile"]["profile"]["version"] == 2:
        result.update(deepcopy(state["manifest"]["teacher_briefing"]["context"]))
        result["current_validation"] = {"resolved": validation(current)["resolved"], "total": len(f.VALIDATION)}
    return result


def question_identity(question):
    return digest({k: v for k, v in question.items() if k != "timestamp"})


def validate_exchange(state, message, question):
    record = message["content"]["record"]
    if set(record) != {"exchange_id", "profile", "configuration", "trace", "proposal"}:
        raise ValueError("unexpected exchange fields")
    if digest(record["profile"]) != digest(state["manifest"]["teacher_profile"]) or digest(record["configuration"]) != digest(state["manifest"]["teacher_config"]):
        raise ValueError("profile/configuration differs from frozen selection")
    if record["exchange_id"] != question_identity(question):
        raise ValueError("exchange does not identify the committed question")
    trace = record["trace"]
    if not isinstance(trace, dict):
        raise ValueError("trace must be an object")
    expected = make_request(record["profile"], question["content"]["context"], record["configuration"]["generation"])
    model_key = record["configuration"]["roles"]["teacher"]
    if (trace.get("backend") != "llama.cpp" or trace.get("backend_version") != BACKEND_VERSION
            or trace.get("backend_archive_sha256") != BACKEND_FILES
            or digest(trace.get("request")) != digest(expected) or trace.get("role") != "teacher"
            or trace.get("status") != "validated" or trace.get("model_key") != model_key
            or trace.get("model") != record["configuration"]["models"][model_key]
            or trace.get("prompt_version") != record["profile"]["selector"]
            or digest(trace.get("generation")) != digest(record["configuration"]["generation"])
            or trace.get("request_sha256") != hashlib.sha256(json.dumps(expected, sort_keys=True).encode()).hexdigest()):
        raise ValueError("model request provenance does not match the question")
    choice = trace["response"]["choices"][0]
    if not isinstance(choice, dict) or choice.get("finish_reason") != "stop":
        raise ValueError("incomplete model output")
    proposal = validate_lesson(choice["message"]["content"])
    if digest(proposal) != digest(record["proposal"]):
        raise ValueError("proposal differs from actual structured response")
    return proposal


def handle(state, message, models, receipt):
    from .runtime import emit
    current = state["judgment"]
    evaluation = f
    if "briefing_study" in current:
        from . import teacher_briefing as evaluation
    content = message["content"]
    def respond(text, **extra):
        emit(state, "response", {"text": text, **extra}, message["id"])
    def reject(reason):
        receipt.update(status="rejected", reason=reason)
        current["rejected"].append({"message_id": message["id"], "reason": reason})
        respond("Rejected: " + reason)
        return state
    if set(content) != {"text", "operation", "record"} or not isinstance(content["record"], dict):
        return reject("invalid teacher study content")
    op, record = content["operation"], content["record"]
    if op in ("outcome", "barrier"):
        return a.handle(state, message, models, receipt)
    if op == "calibration":
        key = record.get("evidence_id")
        if not isinstance(key, str) or key not in f.TRAINING or digest(record) != digest(f.TRAINING[key]) or message["source"] != "registered-route-calibration-1":
            return reject("not registered calibration evidence")
        if key in current["calibration"]:
            receipt["status"] = "duplicate_evidence"
        else:
            current["calibration"][key] = {"record": deepcopy(record), "message_id": message["id"], "source": message["source"]}
        respond("Calibration observation retained; no online experience update.")
        return state
    if op == "ask_teacher" and record == {}:
        if set(current["calibration"]) != set(f.TRAINING):
            return reject("all registered calibration observations required")
        if current["teaching_request"] is not None:
            return reject("one teaching request already allocated")
        profile = state["manifest"]["teacher_profile"]
        request = emit(state, "teaching_request", {"text": "Please propose one evidence-backed developmental route preference.",
            "context": context(state), "profile": profile, "configuration_sha256": digest(state["manifest"]["teacher_config"])}, message["id"])
        current["teaching_request"] = request
        state["questions"][request] = {"kind": "teaching", "answered_by": None}
        return state
    if op == "lesson":
        question = state["questions"].get(message.get("reply_to"))
        if message["type"] != "teacher_reply" or not question or question.get("kind") != "teaching":
            return reject("lesson requires linked teaching question")
        if question["answered_by"] is not None:
            receipt["status"] = "duplicate_lesson"
            respond("Teaching question already disposed; no additional learning.")
            return state
        before = deepcopy(current["weights"])
        event = {"message_id": message["id"], "source": message["source"], "sender": message["sender"],
                 "reply_to": message["reply_to"], "exchange": deepcopy(record), "before": before, "accepted": False}
        try:
            out = next(x for x in state["outbox"] if x["id"] == message["reply_to"])
            proposal = validate_exchange(state, message, out)
            result = assess(current, proposal)
            event.update(proposal=proposal, validation=result, reason=result["reason"])
            if result["accepted"] and state["learning"] and current["teacher_mode"] != "teacher-none":
                current["weights"][proposal["route"]] = proposal["weight"]
                event["accepted"] = True
            elif result["accepted"]:
                event["reason"] = "lesson acceptance disabled"
        except (ValueError, TypeError, KeyError, IndexError, StopIteration) as exc:
            event["reason"] = "invalid or unlinked teacher proposal: " + str(exc)
        event["after"] = deepcopy(current["weights"])
        current["lessons"].append(event)
        question["answered_by"] = message["id"]
        receipt["status"] = "accepted_lesson" if event["accepted"] else "rejected_lesson"
        respond("Teacher proposal evaluated; explanation is not evidence.", accepted=event["accepted"], reason=event["reason"], weights=event["after"], teaching_request=message["reply_to"])
        return state
    if op == "case":
        key = record.get("case_id")
        if not isinstance(key, str) or key not in evaluation.EVALUATION or digest(record) != digest(evaluation.public_case(key)):
            return reject("not a registered public evaluation case")
        if key in current["cases"]:
            return reject("case request budget exhausted")
        selected, traces = selection(current, record)
        item = {"input": deepcopy(record), "selected": selected, "resolved": False, "result": a.decision(current, None)}
        current["cases"][key] = item
        if traces:
            state["diagnostics"].append({"case_id": key, "selection": traces})
        if selected:
            request = emit(state, "clarification_request", {"text": "Verify the selected condition; teacher assistance is disabled.",
                "case_id": key, "candidate": selected, "budget_remaining": 0}, message["id"])
            item["request"] = request
            state["questions"][request] = {"kind": "verification", "case_id": key, "answered_by": None}
        else:
            respond("No independent conflict to investigate; abstaining.", case_id=key, result=item["result"])
        return state
    if op == "verification":
        question = state["questions"].get(message.get("reply_to"))
        if message["type"] != "teacher_reply" or not question or question.get("kind") != "verification" or question["answered_by"]:
            return reject("verification requires an open evaluation request")
        key = question["case_id"]
        item = current["cases"][key]
        expected = evaluation.verify_evaluation(key, item["selected"])
        if message["source"] != "registered-teacher-evaluation-1" or digest(record) != digest(expected):
            return reject("not registered selected-request evidence")
        current["evidence"][record["evidence_id"]] = {"record": deepcopy(record), "message_id": message["id"], "source": message["source"]}
        question["answered_by"] = message["id"]
        item["resolved"] = item["selected"]["field"] == "shielded" and type(record["value"]) is bool
        item["result"] = a.decision(current, record["value"] if item["resolved"] else None)
        respond("Condition verified." if item["resolved"] else "Verification inconclusive; abstaining.", case_id=key, result=item["result"])
        return state
    return reject("unsupported teacher operation")
