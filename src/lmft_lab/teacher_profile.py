"""One explicit developmental profile, stored outside runtime control flow."""
import hashlib
import json
from pathlib import Path
from .local_models import strict_json

DEFAULT = "foundational-teacher-v1"
DIRECTORY = Path(__file__).resolve().parents[2] / "config" / "teacher_profiles"


def load_profile(selector=DEFAULT):
    if selector not in (DEFAULT, "foundational-teacher-v2"):
        raise ValueError("unsupported teacher profile")
    raw = (DIRECTORY / (selector + ".json")).read_text(encoding="utf-8")
    profile = strict_json(raw)
    if (set(profile) != {"profile_id", "version", "boundary", "capabilities", "guidance", "reply_schema"}
            or profile["profile_id"] != "foundational-teacher" or type(profile["version"]) is not int
            or profile["version"] != (1 if selector == DEFAULT else 2)):
        raise ValueError("unsupported profile structure/version")
    return {"selector": selector, "profile": profile, "exact_text": raw,
            "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()}


def make_request(profile, context, generation):
    p = profile["profile"]
    system = "\n\n".join((p["boundary"], p["capabilities"], p["guidance"],
        "Supported reply schema: " + json.dumps(p["reply_schema"], sort_keys=True)))
    return {"messages": [{"role": "system", "content": system},
                         {"role": "user", "content": json.dumps(context, sort_keys=True)}],
            "temperature": generation["temperature"], "seed": generation["seed"],
            "max_tokens": generation["max_tokens"], "stream": False, "cache_prompt": False,
            "chat_template_kwargs": {"enable_thinking": False},
            "response_format": {"type": "json_object", "schema": p["reply_schema"]}}


def validate_lesson(raw):
    lesson = strict_json(raw)
    if not isinstance(lesson, dict) or set(lesson) != {"route", "weight", "supporting_evidence", "reason", "uncertainty"}:
        raise ValueError("unsupported lesson fields")
    if not isinstance(lesson["route"], str) or lesson["route"] not in ("A", "B", "D"):
        raise ValueError("unknown route")
    if type(lesson["weight"]) not in (int, float) or lesson["weight"] not in (.25, .5, .75):
        raise ValueError("unsupported route weight")
    refs = lesson["supporting_evidence"]
    if not isinstance(refs, list) or not 2 <= len(refs) <= 4 or not all(isinstance(x, str) for x in refs) or len(set(refs)) != len(refs):
        raise ValueError("lesson requires distinct evidence references")
    for name in ("reason", "uncertainty"):
        if not isinstance(lesson[name], str) or not 1 <= len(lesson[name].strip()) <= 1200:
            raise ValueError("reason and uncertainty must be bounded nonempty text")
    return lesson
