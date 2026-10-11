"""Finite briefing-study initializations and fresh evaluation fixture; no new policy."""
from copy import deepcopy
from pathlib import Path
from .local_models import strict_json
from .attention_fixture import CANDIDATES

SITUATIONS = ("beneficial", "no-change")
EVALUATION = ("b1", "b2", "b3", "b4", "b5", "b6")


def load_briefing():
    path = Path(__file__).resolve().parents[2] / "config" / "teacher_briefing.json"
    value = strict_json(path.read_text(encoding="utf-8"))
    if value["version"] != "route-briefing-2" or set(value["situations"]) != set(SITUATIONS):
        raise ValueError("unsupported teacher briefing study")
    for weights in value["situations"].values():
        if set(weights) != {"A", "B", "D"} or any(type(w) not in (int, float) or w not in (.25, .5, .75) for w in weights.values()):
            raise ValueError("invalid study initialization")
    return value


def public_case(key):
    if key not in EVALUATION:
        raise ValueError("unknown briefing evaluation case")
    reports = [{"id": key + field + str(i), "source": "new-sensor-" + str(i),
                "field": field, "value": bool(i)} for field in ("shielded", "color") for i in (0, 1)]
    if key == "b6":
        reports = reports[:1]
    return {"case_id": key, "reports": reports, "candidates": deepcopy(CANDIDATES)}


def verify_evaluation(key, candidate):
    if key not in EVALUATION or candidate not in CANDIDATES or key == "b6":
        raise ValueError("unregistered fresh request")
    available = (candidate["route"] == "D" or candidate["route"] == "A" and key == "b5"
                 or candidate["route"] == "B" and key in ("b1", "b2", "b3"))
    value = (key == "b2") if available else None
    return {"evidence_id": key + "/" + candidate["route"], "case_id": key,
            "candidate": deepcopy(candidate), "value": value, "source": "registered-teacher-evaluation-1"}


def actual_success(key):
    if key not in EVALUATION:
        raise ValueError("unknown held-out case")
    return key not in ("b1", "b5")
