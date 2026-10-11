"""Routine teacher tests use mocked inference; actual offline run is separate."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import pytest
from lmft_lab import teacher as t, teacher_fixture as f
from lmft_lab.local_models import load_config
from lmft_lab.model_assets import ModelError, BACKEND_VERSION, BACKEND_FILES
from lmft_lab.runtime import initial_state, advance, software_manifest
from lmft_lab.runtime_store import Store, digest, atomic_json
from lmft_lab.teacher_adapter import teach_once
from lmft_lab.teacher_profile import load_profile, make_request, validate_lesson

CONFIG = Path(__file__).resolve().parents[1] / "config" / "teacher_models.json"


def message(key, op, record, reply=None, source="registered-route-calibration-1"):
    result = {"schema_version": 1, "id": key, "sender": "fixture-owner", "source": source,
              "type": "teacher_reply" if reply else "observation",
              "content": {"text": "Attributed input.", "operation": op, "record": record}}
    if reply:
        result["reply_to"] = reply
    return result


def step(state, msg):
    return advance(state, (state["cursor"] + 1, msg, None, None), None)


def ready(mode="teacher-lmft"):
    manifest = software_manifest(None, "fixture")
    manifest.update(teacher_profile=load_profile(), teacher_config=load_config(CONFIG))
    state = initial_state("teacher-study", True, manifest, mode)
    for key, record in f.TRAINING.items():
        state = step(state, message(key, "calibration", deepcopy(record)))
    return step(state, message("ask", "ask_teacher", {}))


def lesson():
    return {"route": "B", "weight": .75, "supporting_evidence": ["train-B1", "train-B2"],
            "reason": "Two registered B measurements were available.", "uncertainty": "Availability may change outside these cases."}


class MockModels:
    calls = 0
    fail = False
    def __init__(self, config, **kwargs):
        self.config = config
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def generate(self, role, request, version, validator):
        type(self).calls += 1
        if self.fail:
            raise ModelError("mock unavailable backend")
        raw = json.dumps(lesson())
        key = self.config["roles"][role]
        trace = {"role": role, "request": request, "prompt_version": version, "status": "validated",
                 "model_key": key, "model": self.config["models"][key], "generation": self.config["generation"],
                 "backend": "llama.cpp", "backend_version": BACKEND_VERSION, "backend_archive_sha256": BACKEND_FILES,
                 "execution": "mock", "request_sha256": hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest(),
                 "response": {"choices": [{"finish_reason": "stop", "message": {"content": raw}}]}}
        return validator(raw), trace


def reply(state):
    q = state["outbox"][-1]
    config = state["manifest"]["teacher_config"]
    request = make_request(load_profile(), q["content"]["context"], config["generation"])
    proposal, trace = MockModels(config).generate("teacher", request, load_profile()["selector"], validate_lesson)
    return message("lesson", "lesson", {"exchange_id": t.question_identity(q), "profile": load_profile(),
        "configuration": config, "trace": trace, "proposal": proposal}, q["id"], "local-model-teacher-1")


def test_profile_config_selection_and_prompt_recording():
    p = load_profile()
    assert p["sha256"] == hashlib.sha256(p["exact_text"].encode()).hexdigest()
    assert p["profile"]["version"] == 1
    with pytest.raises(ValueError):
        load_profile("invented-stage")
    config = load_config(CONFIG)
    assert config["roles"]["teacher"] != config["roles"]["interpretation"]
    assert set(load_config(CONFIG.parent / "local_models.json")["roles"]) == {"interpretation", "digestion", "contemplation"}
    state = ready()
    q = state["outbox"][-1]["content"]["context"]
    assert set(q) == {"question", "training_evidence", "weights", "supported_judgments", "capabilities"}
    assert set(x["evidence_id"] for x in q["training_evidence"]) == set(f.TRAINING)
    assert "e1" not in json.dumps(q) and "actual_success" not in json.dumps(q)


@pytest.mark.parametrize("mode,accepted", [("teacher-lmft", True), ("teacher-memory", True), ("teacher-none", False)])
def test_acceptance_control_and_provenance(mode, accepted):
    state = ready(mode)
    before = deepcopy(state)
    msg = reply(state)
    after = step(state, msg)
    event = after["judgment"]["lessons"][0]
    assert event["accepted"] == accepted
    assert event["exchange"] == msg["content"]["record"]
    assert event["validation"]["after"]["resolved"] == 2
    assert after["judgment"]["weights"]["B"] == (.75 if accepted else .5)
    assert after["birth"] == before["birth"]
    assert after["judgment"]["updates"] == []
    assert after["judgment"]["branches"] == before["judgment"]["branches"]
    duplicate = step(after, msg)
    assert duplicate["judgment"] == after["judgment"]
    msg["id"] = "new-delivery"
    repeated = step(duplicate, msg)
    assert repeated["judgment"] == after["judgment"]


@pytest.mark.parametrize("edit", [
    lambda r: r.update(profile={}),
    lambda r: r.update(configuration={}),
    lambda r: r.update(exchange_id="wrong"),
    lambda r: r.update(trace=[]),
    lambda r: r["trace"].update(request={}),
    lambda r: r["trace"].update(backend_version="other"),
    lambda r: r["proposal"].update(weight=.25),
    lambda r: r.update(code="edit seed"),
])
def test_untrusted_exchange_cannot_modify_state(edit):
    state = ready()
    msg = reply(state)
    edit(msg["content"]["record"])
    after = step(state, msg)
    assert after["judgment"]["weights"] == state["judgment"]["weights"]
    assert not after["judgment"]["lessons"][0]["accepted"]


def test_reply_linkage_and_learning_disabled():
    state = ready()
    msg = reply(state)
    msg["reply_to"] = "out-unknown"
    after = step(state, msg)
    assert not after["judgment"]["lessons"]
    state["learning"] = False
    after = step(state, reply(state))
    assert after["judgment"]["lessons"][0]["reason"] == "lesson acceptance disabled"


@pytest.mark.parametrize("patch", [{"weight": True}, {"weight": float("nan")}, {"weight": 1}, {"route": "invented"},
    {"supporting_evidence": ["train-B1", "train-B1"]}, {"reason": ""}, {"seed": "replace"}])
def test_schema_is_independent_of_prompt(patch):
    value = lesson()
    value.update(patch)
    with pytest.raises(ValueError):
        validate_lesson(json.dumps(value))


def test_acceptance_never_reads_held_out_and_schema_is_not_enough(monkeypatch):
    state = ready()
    def forbidden(*args):
        raise AssertionError("hidden evaluation access")
    monkeypatch.setattr(f, "actual_success", forbidden)
    monkeypatch.setattr(f, "verify_evaluation", forbidden)
    assert t.assess(state["judgment"], lesson())["accepted"]
    p = lesson()
    p["supporting_evidence"] = ["e1/B", "e2/B"]
    assert not t.assess(state["judgment"], p)["accepted"]
    p = lesson(); p["weight"] = .25
    assert not t.assess(state["judgment"], p)["accepted"]
    p = lesson(); p.update(route="A", weight=.25, supporting_evidence=["train-A1", "train-A2"])
    assert t.assess(state["judgment"], p)["accepted"]


def test_adapter_outbox_only_dedup_and_checkpoint_restart(tmp_path, monkeypatch):
    state = ready()
    store = Store(tmp_path)
    store.commit(state)
    MockModels.calls = 0
    def forbidden(*args):
        raise AssertionError("adapter must not inspect full state")
    monkeypatch.setattr(Store, "inspect", forbidden)
    output = teach_once(tmp_path, config_path=CONFIG, offline=True, models_factory=MockModels)
    assert output["calls"] == 1
    assert teach_once(tmp_path, config_path=CONFIG, offline=True, models_factory=MockModels)["calls"] == 0
    assert MockModels.calls == 1
    queued = store.next_input(0)
    msg = queued[1]
    after = step(state, msg)
    store.commit(after)
    assert digest(store.read()) == digest(after)
    assert teach_once(tmp_path, config_path=CONFIG, models_factory=MockModels)["calls"] == 0
    assert after["judgment"]["weights"]["B"] == .75


def test_explicit_bounded_retry_failure_no_fake_reply(tmp_path):
    class Failing(MockModels):
        fail = True
    store = Store(tmp_path); store.commit(ready())
    with pytest.raises(ModelError):
        teach_once(tmp_path, config_path=CONFIG, models_factory=Failing)
    assert store.next_input(0) is None
    with pytest.raises(ValueError, match="retry"):
        teach_once(tmp_path, config_path=CONFIG, models_factory=MockModels)
    with pytest.raises(ModelError):
        teach_once(tmp_path, config_path=CONFIG, retry=True, models_factory=Failing)
    with pytest.raises(ValueError, match="budget"):
        teach_once(tmp_path, config_path=CONFIG, retry=True, models_factory=MockModels)
    journal = json.loads(next(tmp_path.rglob("journal.json")).read_text())
    assert len(journal["attempts"]) == 2 and all(a["status"] == "failed" for a in journal["attempts"])


def test_retry_can_recover_and_publish_once(tmp_path):
    class Failing(MockModels):
        fail = True
    store = Store(tmp_path); store.commit(ready())
    with pytest.raises(ModelError):
        teach_once(tmp_path, config_path=CONFIG, models_factory=Failing)
    assert teach_once(tmp_path, config_path=CONFIG, retry=True, models_factory=MockModels)["calls"] == 1
    journal_path = next(tmp_path.rglob("journal.json"))
    journal = json.loads(journal_path.read_text()); journal["published"] = False
    atomic_json(journal_path, journal)
    assert teach_once(tmp_path, config_path=CONFIG, models_factory=MockModels)["calls"] == 0
    messages = [json.loads(p.read_text()) for p in (tmp_path / "inbox").glob("*.json")]
    assert len(messages) == 2 and messages[0] == messages[1]


def test_fresh_scope_and_no_evaluation_learning():
    initial = ready()
    state = step(initial, reply(initial))
    weights = deepcopy(state["judgment"]["weights"])
    for key in f.EVALUATION:
        state = step(state, message("case-"+key, "case", f.public_case(key)))
        out = state["outbox"][-1]
        if out["type"] == "clarification_request":
            record = f.verify_evaluation(key, out["content"]["candidate"])
            state = step(state, message("verify-"+key, "verification", record, out["id"], "registered-teacher-evaluation-1"))
    assert state["judgment"]["weights"] == weights
    cases = state["judgment"]["cases"]
    assert sum(x["resolved"] for x in cases.values()) == 3
    assert cases["e5"]["result"]["decision"] == "abstain"
    assert cases["e6"]["selected"] is None
