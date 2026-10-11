"""Constrained local-model formulation; only complete verified renderings may leave."""
import json
import time
from .local_models import strict_json
from .model_assets import BACKEND_FILES, BACKEND_VERSION
from .runtime_store import digest


def renderings(result):
    case = result["case_id"]
    if result["decision"] == "pending_condition":
        core = f"Case {case}: shielded is missing. Is this transmission shielded? No prediction until clarified."
    else:
        core = (f"Case {case}: prediction {result['decision']}; shielded={result['condition']}; "
                f"score={result['score']}; evidence={','.join(result['evidence_refs']) or 'none'}. "
                "Limited synthetic evidence, not a guarantee.")
    return [core, "Fixture evaluation. " + core]


def formulate(models, result):
    options = renderings(result)
    name = models.config["roles"]["contemplation"]
    generation = models.config["generation"]
    request = {"messages": [{"role": "system", "content": "Choose one complete faithful rendering. Return JSON only. /no_think"},
        {"role": "user", "content": json.dumps({"verified_result": result, "allowed_renderings": options})}],
        "temperature": generation["temperature"], "seed": generation["seed"],
        "max_tokens": generation["max_tokens"], "stream": False, "cache_prompt": False,
        "chat_template_kwargs": {"enable_thinking": False},
        "response_format": {"type": "json_object", "schema": {"type": "object", "additionalProperties": False,
            "required": ["text"], "properties": {"text": {"type": "string", "enum": options}}}}}
    trace = {"execution": "local", "role": "constrained-formulation", "prompt_version": "context-wording-1",
        "model": models.config["models"][name], "generation": generation,
        "backend": BACKEND_VERSION, "backend_archive_sha256": BACKEND_FILES,
        "offline": models.offline, "request": request, "request_sha256": digest(request)}
    started = time.perf_counter()
    try:
        models._start(name)
        trace["server_pid"] = models.process.pid
        response = models._request("/v1/chat/completions", request, generation["timeout_seconds"])
        trace["response"] = response
        choice = response["choices"][0]
        value = strict_json(choice["message"]["content"])
        if choice.get("finish_reason") != "stop" or not isinstance(value, dict) or set(value) != {"text"} or value["text"] not in options:
            raise ValueError("unapproved or incomplete rendering")
        trace["status"] = "validated"
        text = value["text"]
    except (OSError, ValueError, KeyError, IndexError, TypeError, RuntimeError) as exc:
        trace.update(status="rejected", error=type(exc).__name__)
        text = options[0]
        models.close()
    trace["elapsed_seconds"] = time.perf_counter() - started
    return text, trace
