"""Only new briefing selection, context isolation and initialization behavior."""
from copy import deepcopy
import json
import pytest
from lmft_lab import teacher as t, teacher_briefing as b, teacher_fixture as f
from lmft_lab.teacher_profile import load_profile, make_request, validate_lesson
from lmft_lab.runtime import initial_state
from test_teacher import ready, step, message, reply


def study_state(situation, version=2):
    old = ready()
    manifest = deepcopy(old["manifest"])
    manifest["teacher_profile"] = load_profile(f"foundational-teacher-v{version}")
    manifest["teacher_briefing"] = b.load_briefing()
    manifest["teacher_study"] = {"situation": situation, "initial_weights": b.load_briefing()["situations"][situation]}
    state = initial_state("briefing", True, manifest, "teacher-lmft")
    for key, record in f.TRAINING.items():
        state = step(state, message(key, "calibration", deepcopy(record)))
    return step(state, message("ask", "ask_teacher", {}))


def test_v2_preserves_boundary_schema_and_scopes_operational_context(monkeypatch):
    v1, v2 = load_profile(), load_profile("foundational-teacher-v2")
    assert v1["profile"]["boundary"] == v2["profile"]["boundary"]
    assert v1["profile"]["reply_schema"] == v2["profile"]["reply_schema"]
    assert v2["profile"]["version"] == 2
    def forbidden(*args):
        raise AssertionError("held-out access during briefing")
    monkeypatch.setattr(b, "actual_success", forbidden)
    monkeypatch.setattr(b, "verify_evaluation", forbidden)
    state = study_state("no-change")
    context = state["outbox"][-1]["content"]["context"]
    assert context["current_validation"] == {"resolved": 2, "total": 2}
    assert context["context_version"] == "route-briefing-2"
    assert context["training_evidence"] == ready()["outbox"][-1]["content"]["context"]["training_evidence"]
    request = make_request(v2, context, state["manifest"]["teacher_config"]["generation"])
    assert "Requests color" not in request["messages"][0]["content"]
    assert "Requests color" in request["messages"][1]["content"]
    assert '"b1"' not in json.dumps(context)


@pytest.mark.parametrize("situation,expected", [("beneficial", [("A", .25), ("B", .75)]), ("no-change", [])])
def test_feasibility_enumeration_uses_unchanged_policy(situation, expected):
    state = study_state(situation)
    accepted = []
    for route in ("A", "B", "D"):
        refs = [k for k, r in f.TRAINING.items() if r["route"] == route] or ["train-A1", "train-A2"]
        for weight in (.25, .5, .75):
            proposal = {"route": route, "weight": weight, "supporting_evidence": refs,
                        "reason": "Enumerated test candidate.", "uncertainty": "Finite validation only."}
            validate_lesson(json.dumps(proposal))
            if t.assess(state["judgment"], proposal)["accepted"]:
                accepted.append((route, weight))
    assert accepted == expected


def test_v1_format_unchanged_and_context_cannot_switch_profile():
    historical = ready()["outbox"][-1]["content"]["context"]
    new = study_state("beneficial", 1)
    assert new["outbox"][-1]["content"]["context"] == historical
    msg = reply(new)
    msg["content"]["record"]["profile"] = load_profile("foundational-teacher-v2")
    after = step(new, msg)
    assert not after["judgment"]["lessons"][0]["accepted"]
    assert after["manifest"] == new["manifest"]


def test_new_fixture_is_separate_and_rejects_historical_cases():
    state = study_state("beneficial")
    rejected = step(state, message("old", "case", f.public_case("e1")))
    assert rejected["receipts"][-1]["status"] == "rejected"
    result = step(state, message("fresh", "case", b.public_case("b1")))
    assert "b1" in result["judgment"]["cases"]
    assert result["judgment"]["weights"] == state["judgment"]["weights"]
