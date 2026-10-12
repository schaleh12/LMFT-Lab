"""Passive runtime behavior, evidence gates, compatibility and atomic transactions."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest
from lmft_lab import passive_relationship as p, insufficiency as s, insufficiency_fixture as f
from lmft_lab.runtime import initial_state, software_manifest, advance, run
from lmft_lab.runtime_store import Store, digest, atomic_json


def message(mid, operation, record, source=f.SOURCE):
    return {"schema_version": 1, "id": mid, "sender": "fixture-operator", "source": source,
            "type": "observation", "content": {"text": "Passive registered synthetic input.", "operation": operation, "record": deepcopy(record)}}


def step(state, item):
    class NoModels:
        def complete(self, *args): pytest.fail("passive mode called model")
    return advance(state, (state["cursor"] + 1, item, None, json.dumps(item)), NoModels())


def new(mode=p.MODES[0], scenario="supported", learning=True):
    manifest = software_manifest(None, "fixture"); manifest["relationship_policy"] = p.policy(scenario)
    return initial_state("passive", learning, manifest, mode)


def prepared(scenario="supported", mode=p.MODES[0], accepted=True):
    state = new(mode, scenario)
    for eid in f.TRAIN[scenario]: state = step(state, message(eid, "outcome", f.outcome(scenario, eid, "train")))
    state = step(state, message("select", "select", {}))
    for eid in f.VALIDATION: state = step(state, message(eid, "outcome", f.outcome(scenario, eid, "validation")))
    return step(state, message("accept", "accept", {})) if accepted else state


@pytest.mark.parametrize("scenario,ops", [("unsupported", []), ("supported", ["le"]), ("ambiguous", ["lt", "le"])])
def test_states_standalone_and_memory_parity(scenario, ops):
    a, b = prepared(scenario), prepared(scenario, p.MODES[1])
    assert p.scientific(a["judgment"]) == p.scientific(b["judgment"])
    status = p.snapshot(a["judgment"])
    assert [h["op"] for h in status["survivors"]] == ops
    assert status["validation_status"] == ("no_supported_hypothesis" if not ops else "validated")
    assert a["birth"] == b["birth"] and len(a["birth"]["nodes"]) == 40
    assert not a["questions"] and not a["diagnostics"]
    for eid, pair in f.HELD.items():
        result = p.predict(a["judgment"], s.case(eid, pair))
        assert result == s.predict(a["judgment"]["learner"], s.case(eid, pair))
    assert len(a["judgment"]["candidate_space"]) == 6 and len(a["judgment"]["evidence_links"]) == 8


def test_unvalidated_and_unsupported_are_distinct():
    state = new(); status = p.snapshot(state["judgment"])
    assert (status["support_status"], status["validation_status"]) == ("untrained", "not_validated")
    state = prepared(accepted=False)
    assert p.snapshot(state["judgment"])["support_status"] == "supported"
    assert p.snapshot(state["judgment"])["validation_status"] == "not_validated"
    assert p.predict(state["judgment"], s.case("fresh", (1, 4)))["reason"] == "not_validated"
    state = prepared("unsupported")
    assert p.predict(state["judgment"], s.case("fresh", (1, 4)))["reason"] == "no_supported_hypothesis"
    state = prepared("ambiguous")
    assert p.predict(state["judgment"], s.case("fresh", (3, 3)))["reason"] == "hypothesis_disagreement"
    assert p.predict(state["judgment"], s.case("fresh", (1, 4)))["decision"] == "success"


@pytest.mark.parametrize("operation,record", [("select", {"nonempty": 1}), ("accept", {"nonempty": 1}),
    ("proposal", {"code": "replace mechanisms"}), ("request", {}), ("acquire", {})])
def test_rejections_leave_entire_judgment_unchanged(operation, record):
    state = prepared(); before = deepcopy(state["judgment"])
    result = step(state, message("rejected", operation, record))
    assert result["judgment"] == before
    assert result["receipts"][-1]["status"] == "rejected"
    assert result["receipts"][-1]["message"]["content"]["record"] == record


def test_malformed_and_false_labels_never_become_contradictions(monkeypatch):
    state = new(); initial = deepcopy(state["judgment"])
    record = f.outcome("supported", "t1", "train")
    state = step(state, message("false", "outcome", {**record, "success": False}))
    assert state["judgment"] == initial
    assert "unverified label" in state["receipts"][-1]["reason"]
    monkeypatch.setattr(f, "execute", lambda *args: pytest.fail("oracle called"))
    for i, (changes, source) in enumerate((({"length": True}, f.SOURCE), ({"split": "heldout"}, f.SOURCE), ({}, "foreign"))):
        state = step(state, message("bad-" + str(i), "outcome", {**record, **changes}, source))
        assert state["judgment"] == initial
    malformed = message("malformed", "outcome", record); malformed["content"]["unknown"] = "bad"
    state = step(state, malformed)
    assert state["judgment"] == initial and "raw" in state["receipts"][-1]
    teacher = message("teacher", "outcome", record); teacher.update(type="teacher_reply", reply_to="unknown")
    state = step(state, teacher)
    assert state["judgment"] == initial


def test_message_and_evidence_dedup_conflicts_and_outbox():
    state = new(); original = message("t1", "outcome", f.outcome("supported", "t1", "train"))
    state = step(state, original); before = deepcopy(state["judgment"]); outbox = deepcopy(state["outbox"])
    state = step(state, original)
    assert state["receipts"][-1]["status"] == "duplicate" and state["outbox"] == outbox
    changed = deepcopy(original); changed["content"]["record"]["success"] = False
    state = step(state, changed)
    assert state["receipts"][-1]["status"] == "id_conflict" and state["judgment"] == before
    state = step(state, message("copy", "outcome", original["content"]["record"]))
    assert state["receipts"][-1]["status"] == "duplicate_evidence" and state["judgment"] == before
    state = step(state, message("conflict", "outcome", changed["content"]["record"]))
    assert state["receipts"][-1]["reason"] == "conflicting evidence identity" and state["judgment"] == before


def test_evaluation_is_communication_only_and_pure_probe_is_read_only(monkeypatch):
    state = prepared("ambiguous"); before = deepcopy(state["judgment"])
    monkeypatch.setattr(f, "execute", lambda *args: pytest.fail("oracle during prediction"))
    record = s.case("fresh", (4, 4)); result = p.predict(state["judgment"], record)
    state = step(state, message("evaluate", "evaluate", record))
    assert state["judgment"] == before
    assert state["outbox"][-1]["content"]["result"] == result
    assert state["receipts"][-1]["status"] == "evaluated"
    assert state["outbox"][-1]["content"]["scientific_digest"] == digest(p.scientific(before))


def test_learning_disabled_gate_precedes_verifier(monkeypatch):
    state = new(learning=False); before = deepcopy(state["judgment"])
    record = f.outcome("supported", "t1", "train")
    monkeypatch.setattr(f, "verify", lambda *args: pytest.fail("disabled verifier called"))
    for op, item in (("outcome", record), ("select", {}), ("accept", {})):
        state = step(state, message(op, op, item))
        assert state["receipts"][-1]["reason"] == "learning disabled" and state["judgment"] == before
    state = step(state, message("probe", "evaluate", s.case("fresh", (1, 4))))
    assert state["receipts"][-1]["status"] == "evaluated" and state["judgment"] == before


@pytest.mark.parametrize("point", ["before_replace", "after_replace"])
@pytest.mark.parametrize("operation", ["outcome", "select", "accept", "evaluate"])
def test_atomic_runtime_transaction_and_replay(tmp_path, point, operation):
    if operation == "outcome":
        state = new(); item = message("new-outcome", operation, f.outcome("supported", "t1", "train"))
    elif operation == "select":
        state = new()
        for eid in f.TRAIN["supported"]: state = step(state, message(eid, "outcome", f.outcome("supported", eid, "train")))
        item = message("new-select", operation, {})
    elif operation == "accept":
        state = prepared(accepted=False); item = message("new-accept", operation, {})
    else:
        state = prepared(); item = message("new-evaluate", operation, s.case("fresh", (1, 4)))
    store = Store(tmp_path); store.commit(state); changed = step(state, item)
    def fault(where):
        if where == point: raise RuntimeError("injected interruption")
    with pytest.raises(RuntimeError, match="interruption"): store.commit(changed, fault=fault)
    restored = store.inspect()
    assert digest(restored) == digest(state if point == "before_replace" else changed)
    if point == "before_replace": restored = step(restored, item)
    def semantic_transaction(value):
        result = deepcopy(value)
        for out in result["outbox"]: out.pop("timestamp", None)
        return result
    # Recalculation can produce a later wall-clock timestamp, but the entire
    # cursor/processed/receipt/output/scientific transaction must match.
    assert digest(semantic_transaction(restored)) == digest(semantic_transaction(changed))
    replayed = step(restored, item)
    assert replayed["judgment"] == restored["judgment"]
    assert replayed["outbox"] == restored["outbox"]
    assert replayed["receipts"][-1]["status"] == "duplicate"


def test_new_modes_reject_local_execution_before_model_setup(monkeypatch, tmp_path):
    import lmft_lab.runtime as runtime
    monkeypatch.setattr(runtime, "load_config", lambda *args: pytest.fail("model configuration loaded"))
    with pytest.raises(ValueError, match="require --mode fixture"):
        run(tmp_path, individual="passive", experiment=p.MODES[0], mode="local")
    assert not (tmp_path / "checkpoint.json").exists()


def test_policy_pins_and_source_manifest_old_checkpoint_refusal(tmp_path):
    state = new(); store = Store(tmp_path); store.commit(state)
    before = (tmp_path / "checkpoint.json").read_bytes()
    # Simulate a different/older software manifest in a NEW test checkpoint, never a historical archive.
    state["manifest"]["sources"]["runtime.py"] = "old-source-hash"
    store.commit(state); changed_bytes = (tmp_path / "checkpoint.json").read_bytes()
    result = subprocess.run([sys.executable, "-m", "lmft_lab.runtime", "--root", str(tmp_path), "start",
        "--experiment", p.MODES[0], "--mode", "fixture", "--relationship-scenario", "supported"], capture_output=True, text=True, timeout=10)
    assert result.returncode == 1 and "Code/config/control changed" in result.stderr
    assert (tmp_path / "checkpoint.json").read_bytes() == changed_bytes and changed_bytes != before


def test_validation_failure_and_closed_phases_preserve_selected_set():
    state = prepared("ambiguous", accepted=False)
    state["judgment"]["learner"]["evidence"]["validation"]["v1"]["success"] = False
    retained = deepcopy(state["judgment"]["learner"]["survivors"])
    state = step(state, message("accept", "accept", {}))
    assert p.snapshot(state["judgment"])["validation_status"] == "validation_rejected"
    assert state["judgment"]["learner"]["survivors"] == retained
    before = deepcopy(state["judgment"])
    for op in ("accept", "select"):
        state = step(state, message("closed-" + op, op, {})); assert state["judgment"] == before
    assert p.predict(state["judgment"], s.case("fresh", (1, 4)))["reason"] == "validation_rejected"


def test_real_runtime_frozen_suite(tmp_path):
    from lmft_lab.preservation_context import capture_current
    context = tmp_path / "current-source-context.json"
    atomic_json(context, capture_current(Path.cwd()))
    root = tmp_path / "passive"
    subprocess.run([sys.executable, "experiments/run_passive_relationship.py", "--output", str(root), "--preservation-context", str(context)], check=True, timeout=90)
    results = json.loads((root / "results.json").read_text())
    assert results["integrity_passed"] == results["integrity_total"]
    assert results["quality_passed"] == results["quality_total"] == 36
    assert results["model_calls"] == 0
    assert results["preservation_kind"] == "current-regression-preservation-1" and results["preservation_count"] > 0
    assert not (root / "failure.json").exists()
    for branch in ("restarted", "uninterrupted"):
        for row in results[branch].values(): assert all(row["checks"].values())
