"""Supervised file-backed runtime. No automatic teacher bridge or idle cognition."""
import argparse
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

from . import reliability, contextual, attention, scoped_attention, consistent_attention, correction, teacher
from .birth import create_birth_state
from .judgment import newborn, probe, revise, RULE_VERSION
from .local_models import LocalModels, load_config, strict_json
from .model_assets import ModelError
from .processing import process_observation
from .runtime_store import Store, atomic_json, digest, locked

ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}\Z")


def validate_message(message, *, contextual_content=False):
    required = {"schema_version", "id", "sender", "source", "type", "content"}
    if not isinstance(message, dict) or not required <= set(message) or set(message) - required - {"reply_to", "timestamp"}:
        raise ValueError("invalid message envelope fields")
    if type(message["schema_version"]) is not int or message["schema_version"] != 1:
        raise ValueError("unsupported message version")
    for key in ("id", "sender", "source"):
        if not isinstance(message[key], str) or not ID.fullmatch(message[key]):
            raise ValueError("invalid message identity/source")
    if message["type"] not in ("observation", "teacher_reply"):
        raise ValueError("unsupported incoming type")
    content = message["content"]
    if (not isinstance(content, dict) or "text" not in content or set(content) - ({"text", "evidence", "operation", "record"} if contextual_content else {"text", "evidence"})
            or not isinstance(content["text"], str) or not 1 <= len(content["text"].strip()) <= 6000):
        raise ValueError("content requires text (1..6000 characters), with optional evidence")
    if "timestamp" in message and (not isinstance(message["timestamp"], str) or len(message["timestamp"]) > 100):
        raise ValueError("timestamp must be metadata text")
    reply = message.get("reply_to")
    if message["type"] == "teacher_reply":
        if not isinstance(reply, str) or not ID.fullmatch(reply):
            raise ValueError("teacher_reply requires reply_to")
    elif reply is not None:
        raise ValueError("observation cannot answer a request")
    if len(json.dumps(message, ensure_ascii=False).encode("utf-8")) > 30000:
        raise ValueError("message exceeds 30000 bytes")
    return message


def message_identity(message):
    # Delivery timestamps are metadata, not a new message or source of learning.
    return digest({k: v for k, v in message.items() if k != "timestamp"})


def software_manifest(config, mode):
    return {"sources": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(Path(__file__).parent.glob("*.py"))},
            "model_config": config, "mode": mode, "rule_version": RULE_VERSION,
            "python": sys.version}


class FixtureModels:
    """Explicitly authored proposals for the mechanical experiment; no inference."""
    def complete(self, role, observation, node_ids, context):
        request = {"role": role, "observation": observation, "context": context}
        proposal = {"summary": "Authored mechanical observation.", "memberships": [],
            "uncertainties": ["Only a matching fixture measurement is eligible evidence."],
            "questions": [], "proposed_judgment": None}
        return proposal, {"role": role, "execution": "mock", "fixture": "channel-agreement-1",
                          "request": request, "request_sha256": digest(request), "proposal": proposal}

    def close(self):
        pass


def initial_state(individual, learning, manifest, experiment="channel"):
    birth = create_birth_state(individual, birth_event_id="birth-" + individual, random_seed=42)
    result = {"schema_version": 1, "individual_id": individual, "birth": asdict(birth),
            "manifest": manifest, "learning": learning, "cycle": 0, "cursor": 0,
            "judgment": newborn(), "processed": {}, "receipts": [], "outbox": [],
            "questions": {}, "asked_issues": [], "diagnostics": []}
    if experiment != "channel":
        result.update(experiment=experiment, judgment=teacher.newborn(experiment, manifest.get("teacher_study")) if experiment in teacher.MODES else correction.newborn(experiment, manifest.get("correction_policy")) if experiment in correction.MODES else consistent_attention.newborn(experiment) if experiment in consistent_attention.MODES else scoped_attention.newborn(experiment) if experiment in scoped_attention.MODES else attention.newborn(experiment) if experiment in attention.MODES else contextual.newborn(experiment) if experiment in contextual.MODES else reliability.newborn())
    return result


def emit(state, kind, content, reply_to):
    sequence = len(state["outbox"]) + 1
    message = {"schema_version": 1, "id": f"out-{sequence}", "sender": state["individual_id"],
               "source": "authored-communication-rule-1", "type": kind, "content": content,
               "reply_to": reply_to, "sequence": sequence, "cycle": state["cycle"],
               "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    state["outbox"].append(message)
    return message["id"]


def advance(previous, queued, models):
    """Pure state transition apart from bounded model inference. Caller commits once."""
    state = deepcopy(previous)
    experiment = state.get("experiment", "channel")
    comparative = experiment != "channel"
    sequence, message, malformed, raw = queued
    state["cursor"] = sequence
    state["cycle"] += 1
    receipt = {"sequence": sequence, "cycle": state["cycle"]}
    state["receipts"].append(receipt)
    try:
        if malformed:
            raise ValueError(malformed)
        validate_message(message, contextual_content=experiment in (*contextual.MODES, *attention.MODES, *scoped_attention.MODES, *consistent_attention.MODES, *correction.MODES, *teacher.MODES))
    except (ValueError, TypeError) as exc:
        receipt.update(status="rejected", reason=str(exc), raw=raw)
        emit(state, "response", {"text": "Inbox record rejected: invalid message format.",
                                 "queue_sequence": sequence}, None)
        return state
    identity = message_identity(message)
    prior = state["processed"].get(message["id"])
    if prior:
        receipt.update(message_id=message["id"], status="duplicate" if prior == identity else "id_conflict")
        # Redelivery has no new utterance; receive can replay original stable outbox IDs.
        if prior != identity:
            receipt["rejected_message"] = message
            emit(state, "response", {"text": "Message ID conflicts with an earlier input; rejected."}, message["id"])
        return state
    state["processed"][message["id"]] = identity
    receipt.update(message_id=message["id"], status="processed", message=message)
    if experiment in teacher.MODES:
        return teacher.handle(state, message, models, receipt)
    if experiment in correction.MODES:
        return correction.handle(state, message, models, receipt)
    if experiment in consistent_attention.MODES:
        return consistent_attention.handle(state, message, models, receipt)
    if experiment in scoped_attention.MODES:
        return scoped_attention.handle(state, message, models, receipt)
    if experiment in attention.MODES:
        return attention.handle(state, message, models, receipt)
    if experiment in contextual.MODES:
        return contextual.handle(state, message, models, receipt)
    rejection = None
    if message["type"] == "teacher_reply":
        question = state["questions"].get(message["reply_to"])
        if question is None or question["answered_by"] is not None:
            rejection = "reply does not address an open clarification request"
        else:
            question["answered_by"] = message["id"]
    diagnostic = {"cycle": state["cycle"], "message_id": message["id"]}
    if rejection is None and experiment == "reliability-memory":
        diagnostic["processing"] = {"status": "completed", "calls": [], "execution": "structured-memory"}
    elif rejection is None:
        birth = create_birth_state(state["individual_id"],
                                   birth_event_id=state["birth"]["birth_event_id"], random_seed=42)
        # Structured evidence is visible as attributed input, never model authority.
        observation = json.dumps(message["content"], ensure_ascii=False)
        if len(observation) > 6000:
            rejection = "serialized content exceeds model input limit"
        else:
            try:
                diagnostic["processing"] = process_observation(birth, observation,
                    event_id="input-" + message["id"], models=models,
                    **({"relationships": reliability.ASSOCIATIONS,
                        "relationship_source": "reliability-fixture-1",
                        "propagation_config": reliability.PropagationConfig(
                            passes=0 if experiment == "reliability-no-propagation" else 2)} if comparative else {}))
                process = getattr(models, "process", None)
                diagnostic["model_server_pid"] = process.pid if process else None
            except ModelError as exc:
                diagnostic["processing"] = getattr(exc, "processing_trace", {"error": str(exc)})
                rejection = "model processing failed; no revision applied"
                receipt["status"] = "model_failed"
    updater = (reliability.baseline_revise if experiment == "reliability-memory" else
               reliability.revise if comparative else revise)
    state["judgment"], revision = updater(state["judgment"], message,
                                         learning=state["learning"], rejection=rejection)
    diagnostic["revision"] = revision
    state["diagnostics"].append(diagnostic)
    emit(state, "response", {"text": reliability.wording(state["judgment"]) if comparative else "Fixture evaluation completed.",
        "probe": reliability.probe(state["judgment"]) if comparative else probe(state["judgment"]),
        "accepted": revision["accepted"], "reason": revision["reason"],
        "evidence_refs": revision["supporting"] + revision["contradicting"]}, message["id"])
    evidence = state["judgment"]["evidence"]
    signs = {e["sign"] for e in evidence.values()}
    issue = "missing-evidence" if not evidence else "conflicting-evidence" if len(signs) == 2 else None
    unresolved = {"issue": issue, "evidence_refs": sorted(evidence)}
    diagnostic["unresolved"] = unresolved
    if (issue and issue not in state["asked_issues"] and
            not any(q["answered_by"] is None for q in state["questions"].values())):
        wording = ("No eligible measurement is recorded. Can you supply a frozen fixture sample?"
                   if issue == "missing-evidence" else
                   "Recorded samples both agree and disagree. Can you provide another unused fixture sample?")
        if comparative:
            wording = ("No verified procedure outcomes are recorded. Can you supply a registered trial?"
                       if issue == "missing-evidence" else
                       "Verified successes and failures conflict. Can you supply another unused registered trial?")
        identifier = emit(state, "clarification_request", {"text": wording, **unresolved}, message["id"])
        state["questions"][identifier] = {**unresolved, "trigger_message": message["id"], "answered_by": None}
        state["asked_issues"].append(issue)
    return state


def run(root, *, individual=None, mode="local", config_path="config/local_models.json", offline=False,
        learning=True, experiment="channel", teacher_profile="foundational-teacher-v1",
        teacher_config="config/teacher_models.json", teacher_study="historical"):
    store = Store(root)
    config = load_config(config_path) if mode == "local" else None
    manifest = software_manifest(config, mode)
    if experiment in teacher.MODES:
        from .teacher_profile import load_profile
        manifest["teacher_profile"] = load_profile(teacher_profile)
        manifest["teacher_config"] = load_config(teacher_config)
        if teacher_profile == "foundational-teacher-v2" or teacher_study != "historical":
            from .teacher_briefing import load_briefing
            manifest["teacher_briefing"] = load_briefing()
        if teacher_study != "historical":
            manifest["teacher_study"] = {"situation": teacher_study,
                "initial_weights": manifest["teacher_briefing"]["situations"][teacher_study]}
        if "teacher" not in manifest["teacher_config"]["roles"]:
            raise ValueError("teacher model role required")
    if experiment in correction.MODES:
        manifest["correction_policy"] = correction.load_policy()
    if experiment != "channel":
        manifest.update(experiment=experiment, fixture_rule=teacher.RULE if experiment in teacher.MODES else correction.RULE if experiment in correction.MODES else consistent_attention.RULE if experiment in consistent_attention.MODES else scoped_attention.RULE if experiment in scoped_attention.MODES else attention.RULE if experiment in attention.MODES else contextual.RULE if experiment in contextual.MODES else reliability.RULE)
    with locked(store.root / "runtime.lock"):
        if (store.root / "checkpoint.json").exists():
            state = store.read()
            if individual is not None:
                raise ValueError("Individual already exists; omit --new to restart")
            if state["manifest"] != manifest or state["learning"] != learning:
                raise ValueError("Code/config/control changed; use original version or an explicitly new experiment")
        else:
            if individual is None or not ID.fullmatch(individual):
                raise ValueError("A valid --new individual ID is required")
            state = initial_state(individual, learning, manifest, experiment)
            store.commit(state)
        (store.root / "stop.json").unlink(missing_ok=True)
        atomic_json(store.root / "lifecycle.json", {"status": "running", "pid": os.getpid()})
        models = LocalModels(config, offline=offline) if mode == "local" else (
            FixtureModels() if experiment == "channel" else reliability.AuthoredModels())
        print(json.dumps({"lifecycle": "started", "individual_id": state["individual_id"]}), flush=True)
        try:
            while not (store.root / "stop.json").exists():
                queued = store.next_input(state["cursor"])
                if queued is None:
                    time.sleep(0.1)
                    continue
                started = time.perf_counter()
                changed = advance(state, queued, models)
                changed["receipts"][-1]["processing_seconds"] = time.perf_counter() - started
                store.commit(changed)
                state = changed
        except KeyboardInterrupt:
            # Incomplete calculation has no checkpoint; it will be retried on restart.
            pass
        finally:
            models.close()
            atomic_json(store.root / "lifecycle.json", {"status": "halted", "pid": os.getpid()})
        print(json.dumps({"lifecycle": "halted"}), flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Individual directory, preferably under ignored outputs/")
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("start")
    start.add_argument("--new", dest="individual")
    start.add_argument("--experiment", choices=("channel", "reliability", "reliability-no-propagation", "reliability-memory", *contextual.MODES, *attention.MODES, *scoped_attention.MODES, *consistent_attention.MODES, *correction.MODES, *teacher.MODES), default="channel")
    start.add_argument("--mode", choices=("local", "fixture"), default="local")
    start.add_argument("--config", default="config/local_models.json")
    start.add_argument("--teacher-profile", default="foundational-teacher-v1")
    start.add_argument("--teacher-config", default="config/teacher_models.json")
    start.add_argument("--teacher-study", choices=("historical", "beneficial", "no-change"), default="historical")
    start.add_argument("--offline", action="store_true")
    start.add_argument("--learning-disabled", action="store_true")
    submit = commands.add_parser("submit")
    submit.add_argument("--file", required=True)
    receive = commands.add_parser("receive")
    receive.add_argument("--after", type=int, default=0)
    commands.add_parser("stop")
    commands.add_parser("inspect", help="Internal diagnostics; refused while runtime holds its lock")
    commands.add_parser("probe", help="Read-only probe; available only after halt")
    args = parser.parse_args(argv)
    store = Store(args.root)
    try:
        if args.command == "start":
            run(args.root, individual=args.individual, mode=args.mode, config_path=args.config,
                offline=args.offline, learning=not args.learning_disabled, experiment=args.experiment,
                teacher_profile=args.teacher_profile, teacher_config=args.teacher_config, teacher_study=args.teacher_study)
            return 0
        if args.command == "submit":
            message = validate_message(strict_json(Path(args.file).read_text(encoding="utf-8-sig")), contextual_content=True)
            output = store.submit(message)
        elif args.command == "receive":
            output = store.receive(args.after)
        elif args.command == "stop":
            output = store.stop()
        else:
            state = store.inspect()
            output = ({"weights":state["judgment"]["weights"]} if args.command == "probe" and state.get("experiment") in (*attention.MODES, *scoped_attention.MODES, *consistent_attention.MODES, *correction.MODES, *teacher.MODES) else contextual.probe(state["judgment"]) if args.command == "probe" and state.get("experiment") in contextual.MODES else
                      ((reliability.probe(state["judgment"]) if state.get("experiment", "channel") != "channel"
                       else probe(state["judgment"])) if args.command == "probe" else state))
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, ModelError) as exc:
        # No model trace/state is exposed through lifecycle stderr.
        print(json.dumps({"lifecycle": "error", "reason": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
