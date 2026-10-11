"""Additional hostile metadata and backend failures; no actual model calls."""
from copy import deepcopy
import json
import socket
import pytest
from test_teacher import ready, reply, step, CONFIG
from lmft_lab.local_models import LocalModels, load_config
from lmft_lab.model_assets import ModelError
from lmft_lab.runtime_store import Store
from lmft_lab.teacher_adapter import teach_once


@pytest.mark.parametrize("choice", [None, "not-an-object", [], 12])
def test_malformed_choice_is_rejected_without_crashing(choice):
    state = ready(); msg = reply(state)
    msg["content"]["record"]["trace"]["response"]["choices"] = [choice]
    after = step(state, msg)
    assert not after["judgment"]["lessons"][0]["accepted"]
    assert after["judgment"]["weights"] == state["judgment"]["weights"]


def test_profile_configuration_comparison_is_type_exact():
    state = ready(); msg = reply(state)
    msg["content"]["record"]["configuration"]["generation"]["temperature"] = False
    after = step(state, msg)
    assert not after["judgment"]["lessons"][0]["accepted"]


@pytest.mark.parametrize("failure", ["malformed", "timeout", "invalid_choice"])
def test_failed_inference_retained_no_fabricated_inbox(tmp_path, monkeypatch, failure):
    store = Store(tmp_path); store.commit(ready())
    monkeypatch.setattr(LocalModels, "_start", lambda *args: None)
    def request(*args):
        if failure == "timeout":
            raise socket.timeout("mock timeout")
        if failure == "invalid_choice":
            return {"choices": [None]}
        return {"choices": [{"finish_reason": "stop", "message": {"content": '{"seed":"rewrite"}'}}]}
    monkeypatch.setattr(LocalModels, "_request", request)
    with pytest.raises(ModelError):
        teach_once(tmp_path, config_path=CONFIG, offline=True)
    assert store.next_input(0) is None
    journal = json.loads(next(tmp_path.rglob("journal.json")).read_text())
    attempt = journal["attempts"][0]
    assert attempt["status"] == "failed"
    assert attempt["trace"]["status"] == "failed"
    assert attempt["trace"]["offline"]
    if failure == "malformed":
        assert attempt["trace"]["response"]["choices"][0]["message"]["content"] == '{"seed":"rewrite"}'
