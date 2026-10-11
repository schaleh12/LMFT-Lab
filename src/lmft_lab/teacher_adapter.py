"""Supervised one-question local teacher command; no checkpoint mutation or polling."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
from .local_models import LocalModels, load_config, strict_json
from .model_assets import ModelError, ModelSpec, ensure_backend, ensure_model, cache_root
from .runtime import validate_message
from .runtime_store import Store, atomic_json, digest, locked
from .teacher import question_identity
from .teacher_profile import DEFAULT, load_profile, make_request, validate_lesson


def teach_once(root, *, config_path="config/teacher_models.json", profile_selector=DEFAULT,
               offline=False, retry=False, models_factory=LocalModels):
    store = Store(root)
    profile, config = load_profile(profile_selector), load_config(config_path)
    if "teacher" not in config["roles"]:
        raise ValueError("configuration has no teacher role")
    # Receive returns deliberate messages only. Never inspect/read the cognitive checkpoint.
    with locked(store.root / "teacher.lock"):
        outbox = store.receive()
        questions = [x for x in outbox if x["type"] == "teaching_request"]
        if not questions:
            raise ValueError("no eligible deliberate teaching request")
        disposed = {x["content"].get("teaching_request") for x in outbox}
        pending = [q for q in questions if q["id"] not in disposed]
        if not pending:
            return {"lifecycle": "teacher_already_disposed", "calls": 0}
        question = pending[0]
        if question["content"]["profile"] != profile or question["content"]["configuration_sha256"] != digest(config):
            raise ValueError("selected profile/config differs from the frozen outbox request")
        exchange_id = question_identity(question)
        folder = store.root / "teacher_exchanges" / exchange_id
        folder.mkdir(parents=True, exist_ok=True)
        journal_path = folder / "journal.json"
        journal = strict_json(journal_path.read_text(encoding="utf-8")) if journal_path.exists() else {"exchange_id": exchange_id, "attempts": []}
        if journal.get("message"):
            # Crash after completion/before publication: safely redeliver stable message ID.
            if not journal.get("published"):
                store.submit(journal["message"])
                journal["published"] = True
                atomic_json(journal_path, journal)
            return {"lifecycle": "teacher_already_completed", "exchange_id": exchange_id, "calls": 0}
        if journal["attempts"] and not retry:
            raise ValueError("prior failed/interrupted attempt retained; use --retry explicitly")
        if len(journal["attempts"]) >= 2:
            raise ValueError("teacher attempt budget exhausted")
        request = make_request(profile, question["content"]["context"], config["generation"])
        attempt = {"number": len(journal["attempts"]) + 1, "status": "started", "profile": profile,
                   "configuration": config, "question": question, "request": request}
        journal["attempts"].append(attempt)
        atomic_json(journal_path, journal)  # Reserve attempt before inference, including crash ambiguity.
        try:
            with models_factory(config, offline=offline) as models:
                proposal, trace = models.generate("teacher", request, profile["selector"], validate_lesson)
            record = {"exchange_id": exchange_id, "profile": profile, "configuration": config,
                      "trace": trace, "proposal": proposal}
            message = {"schema_version": 1, "id": "teacher-" + exchange_id,
                       "sender": "local-teacher", "source": "local-model-teacher-1", "type": "teacher_reply",
                       "reply_to": question["id"], "content": {"text": "Attributed local model proposal; independent acceptance required.",
                                                              "operation": "lesson", "record": record}}
            validate_message(message, contextual_content=True)
            attempt.update(status="completed", trace=trace)
            journal.update(message=deepcopy(message), published=False)
            atomic_json(journal_path, journal)
            acknowledgment = store.submit(message)
            journal["published"] = True
            atomic_json(journal_path, journal)
            return {"lifecycle": "teacher_reply_queued", "exchange_id": exchange_id, "calls": 1,
                    "message_id": acknowledgment["message_id"]}
        except (ModelError, ValueError, OSError, RuntimeError) as exc:
            attempt.update(status="failed", error=str(exc), trace=getattr(exc, "trace", None))
            atomic_json(journal_path, journal)
            raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root")
    parser.add_argument("--config", default="config/teacher_models.json")
    parser.add_argument("--profile", default=DEFAULT)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--retry", action="store_true")
    parser.add_argument("--provision", action="store_true", help="Verify/download teacher and existing backend, no inference")
    args = parser.parse_args(argv)
    try:
        if args.provision:
            config = load_config(args.config)
            load_profile(args.profile)
            spec = ModelSpec(**config["models"][config["roles"]["teacher"]])
            ensure_model(spec, cache_root(), offline=args.offline)
            ensure_backend(cache_root(), offline=args.offline)
            result = {"lifecycle": "teacher_assets_ready", "offline": args.offline}
        else:
            if not args.root:
                raise ValueError("--root is required for a teaching exchange")
            result = teach_once(args.root, config_path=args.config, profile_selector=args.profile,
                                offline=args.offline, retry=args.retry)
        print(json.dumps(result))
        return 0
    except (ModelError, ValueError, OSError, RuntimeError) as exc:
        print(json.dumps({"lifecycle": "teacher_error", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
