"""Frozen ambiguity harness; restart predictions occur in a separate process."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from lmft_lab import ambiguity as a
from lmft_lab.capacity_fixture import execute
from lmft_lab.runtime_store import Store, atomic_json, digest


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_guarded(root):
    manifest = json.loads((root / "archive-manifest.json").read_text())
    for name, expected in manifest.items():
        if file_hash(name) != expected or file_hash(root / "archive" / name) != expected:
            raise ValueError("source/config/protocol drift: " + name)
    configuration = json.loads((root / "configuration.json").read_text())
    if digest(configuration) != digest(a.configuration()):
        raise ValueError("configuration drift")
    return digest({"manifest": manifest, "configuration": configuration})


def probes(state):
    before = digest(state)
    predictions = {eid: a.predict(state, a.case(eid, pair)) for eid, pair in a.HELD.items()}
    if digest(state) != before:
        raise AssertionError("prediction mutated state")
    return predictions


def prepare(mode, policy):
    state = a.newborn(mode, policy)
    for eid in a.TRAIN:
        assert a.admit(state, a.outcome(eid, "train")) == "accepted"
    original = a.outcome("t1", "train")
    assert a.admit(state, original) == "duplicate"
    conflict = {**original, "success": not original["success"]}
    assert a.admit(state, conflict) == "rejected"
    assert a.admit(state, original, "external") == "rejected"
    assert a.admit(state, {"code": "install a relationship"}) == "rejected"
    hidden = {"evidence_id": "h1", "split": "heldout", "procedure": a.relations.SCOPE["procedure"],
              "length": 2, "capacity": 2, "success": False}
    assert a.admit(state, hidden) == "rejected"
    a.select(state)
    selected = state["selection"]["selected"]
    # Allegation is never verified: non-selected acquisition must reject first.
    unselected = "q3"
    allegation = {"evidence_id": unselected, "split": "acquisition", "procedure": a.relations.SCOPE["procedure"],
                  "length": 6, "capacity": 6, "success": False}
    assert a.admit(state, allegation) == "rejected"
    if selected:
        record = a.outcome(selected["case_id"], "acquisition")
        assert a.admit(state, record) == "accepted"
        assert a.admit(state, record) == "duplicate"
        assert a.admit(state, allegation) == "rejected"
    a.close_acquisition(state)
    for eid in a.VALIDATION:
        assert a.admit(state, a.outcome(eid, "validation")) == "accepted"
    a.accept(state)
    return state


def quality(predictions, identifiers):
    rows = []
    for eid in identifiers:
        label = execute(*a.HELD[eid])
        decided = predictions[eid]["decision"] in ("success", "failure")
        rows.append({"case_id": eid, "actual_success": label, "decided": decided,
                     "correct": decided and (predictions[eid]["decision"] == "success") == label})
    decided = sum(r["decided"] for r in rows)
    correct = sum(r["correct"] for r in rows)
    return {"rows": rows, "total": len(rows), "decided": decided, "correct": correct,
            "abstentions": len(rows) - decided, "coverage": decided / len(rows),
            "accuracy": correct / decided if decided else None}


def restart_worker(root, condition):
    identity = load_guarded(root)
    store = Store(condition)
    state = store.read()
    if state["study_identity"] != identity:
        raise ValueError("checkpoint study identity mismatch")
    before = file_hash(condition / "checkpoint.json")
    predictions = probes(state)
    atomic_json(condition / "restart-result.json", {
        "state_digest": digest(state), "predictions": predictions, "pid": os.getpid(),
        "checkpoint_unchanged": before == file_hash(condition / "checkpoint.json")})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--restart", nargs=2)
    args = parser.parse_args()
    if args.restart:
        restart_worker(*(Path(p) for p in args.restart))
        return
    if not args.output:
        parser.error("--output required")
    root = Path(args.output).resolve()
    root.mkdir(parents=True, exist_ok=False)
    paths = set(Path("src").rglob("*.py")) | set(Path("tests").rglob("*.py")) | set(Path("config").rglob("*"))
    paths |= {Path(__file__).relative_to(Path.cwd()) if Path(__file__).is_absolute() else Path(__file__),
              Path("experiments/AMBIGUITY_PROTOCOL.md"), Path("AGENTS.md")}
    paths = {p for p in paths if p.is_file()}
    manifest = {}
    for path in sorted(paths):
        target = root / "archive" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        manifest[str(path)] = file_hash(path)
    atomic_json(root / "archive-manifest.json", manifest)
    atomic_json(root / "configuration.json", a.configuration())
    provenance = {"source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
                  "working_tree": subprocess.check_output(["git", "status", "--short"], text=True),
                  "python": sys.version, "model_calls": 0, "random_seed": 42,
                  "protocol_sha256": file_hash("experiments/AMBIGUITY_PROTOCOL.md")}
    atomic_json(root / "provenance.json", provenance)
    identity = load_guarded(root)
    results = {"conditions": {}, "checks": {}, "model_calls": 0, "parent_pid": os.getpid()}
    frozen = {}
    try:
        for policy in a.POLICIES:
            for mode in ("lmft", "memory"):
                name = mode + "-" + policy
                condition = root / name
                state = prepare(mode, policy)
                state["study_identity"] = identity
                Store(condition).commit(state)
                continuous = prepare(mode, policy)
                continuous["study_identity"] = identity
                before = file_hash(condition / "checkpoint.json")
                subprocess.run([sys.executable, str(Path(__file__).resolve()), "--restart", str(root), str(condition)], check=True)
                restored = json.loads((condition / "restart-result.json").read_text())
                predictions = restored["predictions"]
                frozen[name] = predictions
                atomic_json(condition / "uninterrupted-state.json", continuous)
                atomic_json(condition / "uninterrupted-predictions.json", probes(continuous))
                expected_ops = ["le"] if policy == "disagreement" else ["lt", "le"]
                checks = {
                    "initial_ambiguity": [h["op"] for h in state["initial_survivors"]] == ["lt", "le"],
                    "expected_survivors": [h["op"] for h in state["survivors"]] == expected_ops,
                    "budget": state["verified_requests"] == (1 if policy in ("disagreement", "noninformative") else 0),
                    "validation_no_filter": state["acceptance"]["hypotheses"] == state["survivors"],
                    "validation_accepted": state["acceptance"]["accepted"],
                    "restart_state_equal": restored["state_digest"] == digest(state) == digest(continuous),
                    "restart_predictions_equal": predictions == probes(continuous),
                    "actual_new_process": restored["pid"] != os.getpid(),
                    "read_only_checkpoint": restored["checkpoint_unchanged"] and before == file_hash(condition / "checkpoint.json"),
                    "scope": predictions["x1"]["decision"] == "out_of_scope",
                    "evidence_counts": [len(state["evidence"][s]) for s in ("train", "acquisition", "validation")] == [4, state["verified_requests"], 4],
                    "birth_preserved": state["birth"] == a.newborn(mode, policy)["birth"],
                    "selection_expected": (state["selection"]["selected"] or {}).get("case_id") == ({"disagreement": "q2", "noninformative": "q1"}.get(policy)),
                }
                results["conditions"][name] = {"checks": checks, "resolved": len(state["survivors"]) == 1,
                    "verified_requests": state["verified_requests"], "survivors": state["survivors"],
                    "selection": state["selection"], "checkpoint_bytes": (condition / "checkpoint.json").stat().st_size}
        # Freeze EVERY condition before scoring ANY held-out labels.
        atomic_json(root / "frozen-predictions.json", frozen)
        for policy in a.POLICIES:
            l = Store(root / ("lmft-" + policy)).read()
            m = Store(root / ("memory-" + policy)).read()
            l.pop("mode"); m.pop("mode"); l.pop("birth"); m.pop("birth")
            results["checks"][policy + "-memory-parity"] = l == m and frozen["lmft-" + policy] == frozen["memory-" + policy]
        for name, predictions in frozen.items():
            groups = {"equality": quality(predictions, list(a.HELD)[:4]),
                      "non_equality": quality(predictions, list(a.HELD)[4:8]),
                      "overall": quality(predictions, list(a.HELD)[:8])}
            row = results["conditions"][name]
            row["groups"] = groups
            resolved = row["resolved"]
            row["quality_checks"] = {group: (metric["decided"], metric["correct"]) ==
                ((metric["total"], metric["total"]) if resolved or group == "non_equality" else
                 (0, 0) if group == "equality" else (4, 4)) for group, metric in groups.items()}
        results["checks"]["archive_still_matches"] = load_guarded(root) == identity
        checks = list(results["checks"].values()) + [v for row in results["conditions"].values() for v in row["checks"].values()]
        quality_checks = [v for row in results["conditions"].values() for v in row["quality_checks"].values()]
        results.update(integrity_passed=sum(checks), integrity_total=len(checks), quality_passed=sum(quality_checks), quality_total=len(quality_checks))
        atomic_json(root / "results.json", results)
        print(json.dumps({k: v for k, v in results.items() if k.endswith(("passed", "total"))}))
        if not all(checks + quality_checks):
            raise AssertionError("frozen checks failed; preserve negative outcome")
    except Exception as exc:
        atomic_json(root / "failure.json", {"error": repr(exc)})
        raise


if __name__ == "__main__":
    main()
