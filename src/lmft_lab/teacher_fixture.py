"""Registered calibration, validation and held-out fixture accessors, kept separate."""
from copy import deepcopy
from .attention_fixture import CANDIDATES

TRAINING = {f"train-{route}{i}": {"evidence_id": f"train-{route}{i}", "route": route,
    "available": route == "B", "source": "registered-route-calibration-1"}
    for route in ("A", "B") for i in (1, 2)}
VALIDATION = ("v1", "v2")
EVALUATION = ("e1", "e2", "e3", "e4", "e5", "e6")


def public_case(key):
    if key not in (*VALIDATION, *EVALUATION):
        raise ValueError("unknown teacher case")
    reports = [{"id": key + field + str(i), "source": "sensor-" + str(i),
                "field": field, "value": bool(i)} for field in ("shielded", "color") for i in (0, 1)]
    if key == "e6":
        reports = reports[:1]
    return {"case_id": key, "reports": reports, "candidates": deepcopy(CANDIDATES)}


def validation_resolves(key, candidate):
    if key not in VALIDATION:
        raise ValueError("acceptance cannot access evaluation cases")
    return candidate is not None and candidate["field"] == "shielded" and candidate["route"] == "B"


def verify_evaluation(key, candidate):
    if key not in EVALUATION or candidate not in CANDIDATES or key == "e6":
        raise ValueError("unregistered evaluation request")
    available = candidate["route"] == "D" or (candidate["route"] == "A" and key == "e5") or (candidate["route"] == "B" and key in ("e1", "e2", "e3"))
    value = (key != "e2") if available else None
    return {"evidence_id": key + "/" + candidate["route"], "case_id": key,
            "candidate": deepcopy(candidate), "value": value, "source": "registered-teacher-evaluation-1"}


def actual_success(key):
    if key not in EVALUATION:
        raise ValueError("unknown held-out case")
    return key not in ("e2", "e3")
