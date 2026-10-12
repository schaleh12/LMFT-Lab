"""No vacuous consensus, no rejected-input contamination, real restart parity."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest
from lmft_lab import insufficiency as s, insufficiency_fixture as f
from lmft_lab.runtime_store import Store, atomic_json, digest


def trained(scenario="unsupported", mode="lmft"):
    state = s.newborn(mode, scenario)
    for eid in f.TRAIN[scenario]:
        assert s.admit(state, f.outcome(scenario, eid, "train")) == "accepted"
    s.select(state)
    return state


def validated(scenario="unsupported", mode="lmft"):
    state = trained(scenario, mode)
    for eid in f.VALIDATION:
        assert s.admit(state, f.outcome(scenario, eid, "validation")) == "accepted"
    s.accept(state)
    return state


@pytest.mark.parametrize("scenario,ops,status", [
    ("unsupported", [], "no_supported_hypothesis"),
    ("supported", ["le"], "supported"),
    ("ambiguous", ["lt", "le"], "ambiguous")])
def test_explicit_sets_and_baseline_parity(scenario, ops, status):
    l, m = validated(scenario), validated(scenario, "memory")
    assert [h["op"] for h in l["survivors"]] == ops
    assert l["support_status"] == status
    assert l["derivation"]["survivors"] == l["survivors"] == l["acceptance"]["hypotheses"]
    assert l["acceptance"]["accepted"] == bool(ops)
    for eid, pair in f.HELD.items():
        assert s.predict(l, s.case(eid, pair)) == s.predict(m, s.case(eid, pair))
    assert len(l["birth"]["nodes"]) == 40 and m["birth"] is None


def test_empty_set_no_vacuous_consensus_or_resurrection():
    state = trained()
    assert state["survivors"] == []
    assert all(r["error_refs"] for r in state["derivation"]["candidate_evaluations"])
    assert len(state["derivation"]["candidate_evaluations"]) == 6
    before = deepcopy(state["derivation"])
    for eid in f.VALIDATION:
        s.admit(state, f.outcome("unsupported", eid, "validation"))
    s.accept(state)
    assert state["acceptance"]["checks"] == []
    assert state["acceptance"]["accepted"] is False
    assert state["acceptance"]["reason"] == "no_supported_hypothesis"
    assert state["derivation"] == before and state["survivors"] == []
    for eid, pair in f.HELD.items():
        p = s.predict(state, s.case(eid, pair))
        if eid != "x1":
            assert (p["decision"], p["reason"], p["votes"]) == ("abstain", "no_supported_hypothesis", [])


def test_controls_prevent_blanket_abstention_and_preserve_known_errors():
    supported, ambiguous = validated("supported"), validated("ambiguous")
    assert s.predict(supported, s.case("equal", (4, 4)))["decision"] == "success"
    assert s.predict(ambiguous, s.case("equal", (4, 4)))["reason"] == "hypothesis_disagreement"
    assert s.predict(ambiguous, s.case("non_equal", (1, 4)))["decision"] == "success"
    assert s.predict(ambiguous, s.case("failure", (6, 3)))["decision"] == "failure"
    # The supported rule is not a correct rule for the entire new device.
    assert s.predict(supported, s.case("fault", (2, 5)))["decision"] == "success"
    assert f.execute(2, 5) is False


@pytest.mark.parametrize("mutation", [
    {"success": 1}, {"length": True}, {"capacity": False}, {"length": 8},
    {"scenario": "foreign"}, {"split": "heldout"}, {"split": []},
    {"evidence_id": []}, {"procedure": "capacity-transmit-1"}, {"extra": "field"}])
def test_malformed_inputs_are_not_contradictions(mutation, monkeypatch):
    state = s.newborn("memory", "supported")
    record = {**f.outcome("supported", "t1", "train"), **mutation}
    monkeypatch.setattr(f, "execute", lambda *args: pytest.fail("oracle must not execute"))
    assert s.admit(state, record) == "rejected"
    assert state["evidence"] == {"train": {}, "validation": {}}
    assert state["support_status"] == "untrained"
    assert not state["provenance"]


def test_false_label_does_not_eliminate_a_rule():
    state = s.newborn("lmft", "supported")
    wrong = {**f.outcome("supported", "t1", "train"), "success": False}
    assert s.admit(state, wrong) == "rejected"
    assert state["trace"][-1]["reason"] == "unverified label; not a hypothesis contradiction"
    for eid in f.TRAIN["supported"]:
        s.admit(state, f.outcome("supported", eid, "train"))
    s.select(state)
    assert [h["op"] for h in state["survivors"]] == ["le"]
    assert all("t1" not in r["error_refs"] for r in state["derivation"]["candidate_evaluations"] if r["hypothesis"]["op"] == "le")


def test_duplicate_source_conflict_and_proposals_do_not_modify_evidence(monkeypatch):
    state = trained("supported")
    before = digest(state["evidence"]), deepcopy(state["survivors"]), deepcopy(state["derivation"])
    record = f.outcome("supported", "t1", "train")
    monkeypatch.setattr(f, "execute", lambda *args: pytest.fail("must reject before oracle"))
    assert s.admit(state, record) == "duplicate"
    assert s.admit(state, {**record, "success": False}) == "rejected"
    assert state["trace"][-1]["reason"] == "conflicting evidence identity"
    assert s.admit(state, record, "foreign") == "rejected"
    assert s.admit(state, {"code": "add a rule"}) == "rejected"
    assert before == (digest(state["evidence"]), state["survivors"], state["derivation"])


def test_selection_validation_prediction_oracle_isolation(monkeypatch):
    state = validated("supported")
    monkeypatch.setattr(f, "execute", lambda *args: pytest.fail("oracle accessed"))
    before = digest(state)
    for pair in f.HELD.values():
        s.predict(state, s.case("fresh", pair))
    assert before == digest(state)
    state["phase"] = "train"
    s.select(state)
    state["phase"] = "validation"
    s.accept(state)


def test_validation_failure_rejects_without_fallback():
    state = validated("ambiguous")
    retained = deepcopy(state["survivors"])
    state["phase"] = "validation"
    state["evidence"]["validation"]["v1"]["success"] = False
    s.accept(state)
    assert state["survivors"] == retained
    assert not state["acceptance"]["accepted"]
    assert s.predict(state, s.case("fresh", (1, 4)))["reason"] == "validation_rejected"


def test_changed_training_and_resurrection_guard():
    state = validated()
    state["phase"] = "validation"
    state["survivors"] = [s.relations.candidates()[1]]
    with pytest.raises(ValueError, match="hypothesis set changed"):
        s.accept(state)
    state = validated("supported"); state["phase"] = "validation"
    state["evidence"]["train"]["t1"]["success"] = False
    with pytest.raises(ValueError, match="training changed"):
        s.accept(state)


def test_incomplete_closed_phases_and_untrained_status():
    state = s.newborn("memory", "supported")
    assert s.predict(state, s.case("fresh", (1, 3)))["reason"] == "untrained"
    with pytest.raises(ValueError): s.select(state)
    state = trained("supported")
    assert s.predict(state, s.case("fresh", (1, 3)))["reason"] == "not_validated"
    with pytest.raises(ValueError): s.select(state)
    with pytest.raises(ValueError): s.accept(state)
    state = validated("supported")
    with pytest.raises(ValueError): s.accept(state)


@pytest.mark.parametrize("pair", [(True, 3), (3, False), (-1, 3), (9, 8)])
def test_scope(pair):
    assert s.predict(validated(), s.case("x", pair))["decision"] == "out_of_scope"


def test_old_fixture_and_seed_remain_independent():
    from lmft_lab.capacity_fixture import execute
    assert execute(2, 4) is True and f.execute(2, 4) is False
    state = validated("supported")
    before = s.predict(state, s.case("fresh", (4, 4)))
    state["birth"] = None
    assert s.predict(state, s.case("fresh", (4, 4))) == before


def harness():
    spec = importlib.util.spec_from_file_location("insufficiency_harness", "experiments/run_insufficiency.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def test_guard_and_checksum_failures(tmp_path):
    runner = harness(); path = Path("src/lmft_lab/insufficiency.py")
    archive = tmp_path / "archive" / path; archive.parent.mkdir(parents=True)
    archive.write_bytes(path.read_bytes())
    atomic_json(tmp_path / "archive-manifest.json", {str(path): runner.file_hash(path)})
    atomic_json(tmp_path / "configuration.json", s.configuration())
    runner.load_guarded(tmp_path)
    wrong = s.configuration(); wrong["model_calls"] = 1
    atomic_json(tmp_path / "configuration.json", wrong)
    with pytest.raises(ValueError, match="configuration drift"): runner.load_guarded(tmp_path)
    atomic_json(tmp_path / "configuration.json", s.configuration())
    archive.write_text("modified")
    with pytest.raises(ValueError, match="drift"): runner.load_guarded(tmp_path)
    atomic_json(tmp_path / "checkpoint.json", {"sha256": "wrong", "state": validated()})
    with pytest.raises(ValueError, match="checksum"): Store(tmp_path).read()


def test_full_frozen_study_with_actual_restarts(tmp_path):
    root = tmp_path / "study"
    subprocess.run([sys.executable, "experiments/run_insufficiency.py", "--output", str(root)], check=True)
    results = json.loads((root / "results.json").read_text())
    assert results["integrity_passed"] == results["integrity_total"]
    assert results["quality_passed"] == results["quality_total"] == 18
    assert results["model_calls"] == 0
    assert not (root / "failure.json").exists()
    for mode in ("lmft", "memory"):
        p = root / (mode + "-unsupported")
        for stage in ("training", "final"):
            restored = json.loads((p / stage / "restart-result.json").read_text())
            assert restored["survivors"] == []
            assert restored["support_status"] == "no_supported_hypothesis"
            assert len(restored["rejections"]) == 9
    # Existing archives cannot be reused/overwritten.
    again = subprocess.run([sys.executable, "experiments/run_insufficiency.py", "--output", str(root)], capture_output=True)
    assert again.returncode != 0
