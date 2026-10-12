"""Safety boundaries and causal isolation of the frozen ambiguity protocol."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import subprocess
import sys
import pytest
from lmft_lab import ambiguity as a, capacity_fixture
from lmft_lab.runtime_store import Store, atomic_json, digest


def trained(policy="disagreement", mode="lmft"):
    state = a.newborn(mode, policy)
    for eid in a.TRAIN:
        assert a.admit(state, a.outcome(eid, "train")) == "accepted"
    a.select(state)
    return state


def validated(policy="disagreement", mode="lmft"):
    state = trained(policy, mode)
    if state["selection"]["selected"]:
        a.admit(state, a.outcome(state["selection"]["selected"]["case_id"], "acquisition"))
    a.close_acquisition(state)
    for eid in a.VALIDATION:
        a.admit(state, a.outcome(eid, "validation"))
    a.accept(state)
    return state


@pytest.mark.parametrize("policy", a.POLICIES)
def test_resolution_consensus_and_parity(policy):
    left, right = validated(policy), validated(policy, "memory")
    expected = ["le"] if policy == "disagreement" else ["lt", "le"]
    assert [h["op"] for h in left["initial_survivors"]] == ["lt", "le"]
    assert [h["op"] for h in left["survivors"]] == expected
    assert left["acceptance"]["hypotheses"] == left["survivors"]
    before = digest(left)
    for eid, pair in a.HELD.items():
        assert a.predict(left, a.case(eid, pair)) == a.predict(right, a.case(eid, pair))
    assert digest(left) == before
    assert a.predict(left, a.case("fresh", (3, 3)))["decision"] == ("success" if len(expected) == 1 else "abstain")
    assert a.predict(left, a.case("fresh", (3, 4)))["decision"] == "success"
    assert a.predict(left, a.case("fresh", (4, 3)))["decision"] == "failure"
    assert a.predict(left, a.case("x", (9, 8)))["decision"] == "out_of_scope"


def test_selection_uses_general_disagreement_not_equality(monkeypatch):
    monkeypatch.setattr(capacity_fixture, "execute", lambda *args: pytest.fail("oracle accessed"))
    hypotheses = a.relations.candidates()[2:4]  # eq/ge disagree on greater-than, not equality
    observations = [a.case("equal", (2, 2)), a.case("greater", (3, 2))]
    assert a.choose(hypotheses, observations)["selected"]["case_id"] == "greater"
    hypotheses = a.relations.candidates()[:2]
    selected = a.choose(hypotheses, [a.case("z", (6, 6)), a.case("a", (5, 5))])
    assert selected["selected"]["case_id"] == "z"  # declared order, not lexical ID
    assert a.choose(hypotheses, [a.case("only", (1, 3))])["selected"] is None


def test_induction_acceptance_and_prediction_never_call_oracle(monkeypatch):
    state = validated()
    monkeypatch.setattr(capacity_fixture, "execute", lambda *args: pytest.fail("oracle accessed"))
    assert a.filter_hypotheses(a.relations.candidates(), state["evidence"]["train"]) == state["initial_survivors"]
    state["phase"] = "validation"
    a.accept(state)
    a.predict(state, a.case("new", (7, 7)))


def test_duplicate_conflict_budget_and_rejection_before_oracle(monkeypatch):
    state = trained()
    record = a.outcome("q2", "acquisition")
    assert a.admit(state, record) == "accepted"
    hypotheses = deepcopy(state["survivors"])
    monkeypatch.setattr(capacity_fixture, "execute", lambda *args: pytest.fail("unexpected verification"))
    assert a.admit(state, record) == "duplicate"
    assert a.admit(state, {**record, "success": False}) == "rejected"
    assert a.admit(state, {**record, "evidence_id": "q3", "length": 6, "capacity": 6}) == "rejected"
    assert a.admit(state, {**record, "split": "heldout", "evidence_id": "h1"}) == "rejected"
    assert a.admit(state, record, "foreign") == "rejected"
    assert a.admit(state, {"code": "proposal"}) == "rejected"
    assert state["verified_requests"] == 1 and state["survivors"] == hypotheses


@pytest.mark.parametrize("mutation", [{"success": 1}, {"length": True}, {"length": 8}, {"procedure": "other"}, {"split": []}, {"evidence_id": []}])
def test_malformed_and_unverified_records(mutation):
    state = a.newborn("lmft", "disagreement")
    record = {**a.outcome("t1", "train"), **mutation}
    assert a.admit(state, record) == "rejected"
    assert not state["evidence"]["train"]


def test_false_outcome_and_no_bypass():
    state = a.newborn("memory", "disagreement")
    assert a.admit(state, {**a.outcome("t1", "train"), "success": False}) == "rejected"
    with pytest.raises(ValueError):
        a.select(state)
    state = trained()
    with pytest.raises(ValueError):
        a.select(state)
    with pytest.raises(ValueError):
        a.close_acquisition(state)
    with pytest.raises(ValueError):
        a.accept(state)
    assert a.predict(state, a.case("fresh", (1, 2)))["decision"] == "abstain"


def test_validation_failure_rejects_whole_set_without_fallback():
    state = validated("no-evidence")
    retained = deepcopy(state["survivors"])
    # Inject an already-verified mismatch to unit-test acceptance independently of admission.
    state["evidence"]["validation"]["v1"]["success"] = False
    state["phase"] = "validation"
    a.accept(state)
    assert not state["acceptance"]["accepted"]
    assert state["survivors"] == retained
    assert a.predict(state, a.case("fresh", (1, 2)))["decision"] == "abstain"
    with pytest.raises(ValueError):
        a.accept(state)


def test_seed_cannot_cause_prediction():
    state = validated()
    before = a.predict(state, a.case("fresh", (7, 7)))
    assert len(state["birth"]["nodes"]) == 40
    state["birth"] = None
    assert a.predict(state, a.case("fresh", (7, 7))) == before


def test_changed_training_cannot_be_accepted():
    state = validated()
    state["phase"] = "validation"
    state["evidence"]["train"]["t1"]["success"] = False
    with pytest.raises(ValueError, match="training changed"):
        a.accept(state)


def harness():
    spec = importlib.util.spec_from_file_location("ambiguity_harness", "experiments/run_ambiguity.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checkpoint_corruption_and_actual_process_restart(tmp_path):
    state = validated()
    store = Store(tmp_path)
    store.commit(state)
    before = (tmp_path / "checkpoint.json").read_bytes()
    code = "from pathlib import Path; from lmft_lab.runtime_store import Store,atomic_json; from lmft_lab.ambiguity import predict,case; import sys; s=Store(sys.argv[1]).read(); atomic_json(Path(sys.argv[1])/'prediction.json',predict(s,case('fresh',(7,7))))"
    subprocess.run([sys.executable, "-c", code, str(tmp_path)], check=True)
    import json
    assert json.loads((tmp_path / "prediction.json").read_text()) == a.predict(state, a.case("fresh", (7, 7)))
    assert (tmp_path / "checkpoint.json").read_bytes() == before
    atomic_json(tmp_path / "checkpoint.json", {"sha256": "wrong", "state": state})
    with pytest.raises(ValueError, match="checksum"):
        store.read()


def test_manifest_configuration_and_archive_guards(tmp_path):
    runner = harness()
    target = Path("src/lmft_lab/ambiguity.py")
    archive = tmp_path / "archive" / target
    archive.parent.mkdir(parents=True)
    archive.write_bytes(target.read_bytes())
    atomic_json(tmp_path / "archive-manifest.json", {str(target): runner.file_hash(target)})
    atomic_json(tmp_path / "configuration.json", a.configuration())
    runner.load_guarded(tmp_path)
    configuration = a.configuration(); configuration["verification_budget"] = 2
    atomic_json(tmp_path / "configuration.json", configuration)
    with pytest.raises(ValueError, match="configuration drift"):
        runner.load_guarded(tmp_path)
    atomic_json(tmp_path / "configuration.json", a.configuration())
    archive.write_text("altered")
    with pytest.raises(ValueError, match="drift"):
        runner.load_guarded(tmp_path)


def test_full_frozen_suite(tmp_path):
    root = tmp_path / "run"
    subprocess.run([sys.executable, "experiments/run_ambiguity.py", "--output", str(root)], check=True)
    import json
    results = json.loads((root / "results.json").read_text())
    assert results["integrity_passed"] == results["integrity_total"]
    assert results["quality_passed"] == results["quality_total"] == 24
    assert results["model_calls"] == 0
    assert not (root / "failure.json").exists()
