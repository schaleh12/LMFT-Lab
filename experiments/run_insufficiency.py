"""Preregistered family-insufficiency study, with two actual restart boundaries."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from lmft_lab import insufficiency as study, insufficiency_fixture as fixture
from lmft_lab.runtime_store import Store, atomic_json, digest
from lmft_lab import preservation_context

PREWORK = Path("outputs/insufficiency-prework-001/protected-hashes.json")


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_guarded(root):
    manifest = json.loads((root / "archive-manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest.items():
        if file_hash(name) != expected or file_hash(root / "archive" / name) != expected:
            raise ValueError("source/config/protocol/archive drift: " + name)
    configuration = json.loads((root / "configuration.json").read_text(encoding="utf-8"))
    if digest(configuration) != digest(study.configuration()):
        raise ValueError("configuration drift")
    identity = {"manifest": manifest, "configuration": configuration}
    context = preservation_context.pinned_current(root, Path.cwd())
    if context is not None:
        identity["current_preservation_context_sha256"] = file_hash(root / "current-preservation-context.json")
    return digest(identity)


def preserved(root):
    context = preservation_context.pinned_current(root, Path.cwd())
    if context is not None:
        return preservation_context.verify_current(context, Path.cwd())
    expected = json.loads((root / "protected-hashes.json").read_text(encoding="utf-8-sig"))
    return all(file_hash(name) == value for name, value in expected.items())


def probes(state):
    before = digest(state)
    predictions = {eid: study.predict(state, study.case(eid, pair)) for eid, pair in fixture.HELD.items()}
    if before != digest(state):
        raise AssertionError("prediction mutated scientific state")
    return predictions


def invalid_attempts(state):
    scenario = state["scenario"]
    original = fixture.outcome(scenario, "t1", "train")
    # Rejected inputs are attempted BEFORE true training, so a false label cannot
    # be dismissed merely because the genuine identity was already stored.
    attempts = [({**original, "success": False}, fixture.SOURCE),
                (original, "external-unverified"), ({**original, "success": 1}, fixture.SOURCE),
                ({**original, "length": True}, fixture.SOURCE),
                ({**original, "length": 8}, fixture.SOURCE),
                ({"code": "install an extra hypothesis"}, fixture.SOURCE),
                ({**original, "evidence_id": "h1", "split": "heldout", "length": 1, "capacity": 1}, fixture.SOURCE),
                ({**original, "scenario": "foreign"}, fixture.SOURCE)]
    for record, source in attempts:
        assert study.admit(state, record, source) == "rejected"
        assert not state["evidence"]["train"]
        assert state["support_status"] == "untrained"


def prepare_training(mode, scenario):
    state = study.newborn(mode, scenario)
    invalid_attempts(state)
    for eid in fixture.TRAIN[scenario]:
        assert study.admit(state, fixture.outcome(scenario, eid, "train")) == "accepted"
    original = fixture.outcome(scenario, "t1", "train")
    assert study.admit(state, original) == "duplicate"
    assert study.admit(state, {**original, "success": False}) == "rejected"
    study.select(state)
    return state


def complete_validation(training):
    state = deepcopy(training)
    for eid in fixture.VALIDATION:
        assert study.admit(state, fixture.outcome(state["scenario"], eid, "validation")) == "accepted"
    original = fixture.outcome(state["scenario"], "v1", "validation")
    assert study.admit(state, original) == "duplicate"
    study.accept(state)
    return state


def restart_worker(root, checkpoint):
    identity = load_guarded(root)
    state = Store(checkpoint).read()
    if state["study_identity"] != identity or state["version"] != study.VERSION:
        raise ValueError("incompatible study checkpoint")
    before = file_hash(checkpoint / "checkpoint.json")
    predictions = probes(state)
    atomic_json(checkpoint / "restart-result.json", {
        "state_digest": digest(state), "pid": os.getpid(), "predictions": predictions,
        "survivors": state["survivors"], "support_status": state["support_status"],
        "rejections": [r for r in state["trace"] if r.get("status") == "rejected"],
        "checkpoint_unchanged": before == file_hash(checkpoint / "checkpoint.json")})


def quality(predictions, identifiers):
    rows = []
    for eid in identifiers:
        actual = fixture.execute(*fixture.HELD[eid])
        decided = predictions[eid]["decision"] in ("success", "failure")
        rows.append({"case_id": eid, "actual_success": actual, "decision": predictions[eid]["decision"],
                     "reason": predictions[eid]["reason"], "decided": decided,
                     "correct": decided and (predictions[eid]["decision"] == "success") == actual})
    n = len(rows); decided = sum(r["decided"] for r in rows); correct = sum(r["correct"] for r in rows)
    return {"rows": rows, "total": n, "decided": decided, "correct": correct,
            "abstentions": n - decided, "coverage": decided / n,
            "accuracy": correct / decided if decided else None}


def run(root, preservation_context_path=None):
    root.mkdir(parents=True, exist_ok=False)
    context = None
    context_hash = None
    if preservation_context_path is not None:
        context = json.loads(Path(preservation_context_path).read_text(encoding="utf-8"))
        preservation_context.verify_current(context, Path.cwd())
        context_hash = file_hash(preservation_context_path)
        shutil.copy2(preservation_context_path, root / "current-preservation-context.json")
    paths = set(Path("src").rglob("*.py")) | set(Path("tests").rglob("*.py")) | set(Path("config").rglob("*"))
    paths |= set(Path("experiments").glob("*.py")) | {Path("AGENTS.md"), Path("experiments/INSUFFICIENCY_PROTOCOL.md")}
    if context is not None:
        paths |= {Path(name) for name in context["files"]}
    manifest = {}
    for path in sorted(p for p in paths if p.is_file()):
        target = root / "archive" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        manifest[str(path)] = file_hash(path)
    atomic_json(root / "archive-manifest.json", manifest)
    atomic_json(root / "configuration.json", study.configuration())
    atomic_json(root / "provenance.json", {
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "working_tree": subprocess.check_output(["git", "status", "--short"], text=True),
        "python": sys.version, "model_calls": 0, "random_seed": 42,
        "protocol_sha256": file_hash("experiments/INSUFFICIENCY_PROTOCOL.md"),
        "preservation_kind": preservation_context.KIND if context is not None else "legacy-historical-prework",
        "preservation_context_sha256": context_hash})
    # A reproduction on a checkout without the local prework directory remains
    # possible; record that preservation evidence is unavailable rather than invent it.
    atomic_json(root / "protected-hashes.json", context["files"] if context is not None else json.loads(PREWORK.read_text(encoding="utf-8-sig")) if PREWORK.exists() else {})
    identity = load_guarded(root)
    results = {"conditions": {}, "checks": {}, "model_calls": 0, "parent_pid": os.getpid(),
               "prework_available": PREWORK.exists(),
               "preservation_kind": preservation_context.KIND if context is not None else "legacy-historical-prework",
               "preservation_context_sha256": context_hash,
               "preservation_count": len(context["files"]) if context is not None else len(json.loads((root / "protected-hashes.json").read_text()))}
    frozen = {}; final_states = {}
    expected_ops = {"unsupported": [], "supported": ["le"], "ambiguous": ["lt", "le"]}
    try:
        for scenario in fixture.TRAIN:
            for mode in ("lmft", "memory"):
                name = mode + "-" + scenario
                condition = root / name
                training = prepare_training(mode, scenario); training["study_identity"] = identity
                reference_training = prepare_training(mode, scenario); reference_training["study_identity"] = identity
                final = complete_validation(training)
                reference_final = complete_validation(reference_training)
                checks = {}; restarts = {}
                for stage, state, reference in (("training", training, reference_training), ("final", final, reference_final)):
                    if stage == "final":
                        # Continue from persisted training after its actual restart,
                        # rather than carrying the in-memory training object forward.
                        final = complete_validation(Store(condition / "training").read())
                        state = final
                    checkpoint = condition / stage
                    Store(checkpoint).commit(state)
                    before = file_hash(checkpoint / "checkpoint.json")
                    subprocess.run([sys.executable, str(Path(__file__).resolve()), "--restart", str(root), str(checkpoint)], check=True)
                    restored = json.loads((checkpoint / "restart-result.json").read_text(encoding="utf-8"))
                    restarts[stage] = restored
                    checks[stage + "-state-parity"] = restored["state_digest"] == digest(state) == digest(reference)
                    checks[stage + "-prediction-parity"] = restored["predictions"] == probes(reference)
                    checks[stage + "-actual-process"] = restored["pid"] != os.getpid()
                    checks[stage + "-read-only"] = restored["checkpoint_unchanged"] and before == file_hash(checkpoint / "checkpoint.json")
                    checks[stage + "-rejections-preserved"] = restored["rejections"] == [r for r in state["trace"] if r.get("status") == "rejected"]
                    atomic_json(checkpoint / "uninterrupted-state.json", reference)
                    atomic_json(checkpoint / "uninterrupted-predictions.json", probes(reference))
                predictions = restarts["final"]["predictions"]
                frozen[name] = predictions; final_states[name] = final
                candidates = final["derivation"]["candidate_evaluations"]
                checks.update({
                    "expected-set": [h["op"] for h in final["survivors"]] == expected_ops[scenario],
                    "explicit-support-status": final["support_status"] == study.support_status(final["survivors"]),
                    "six-derivations": len(candidates) == 6 and all(len(r["checks"]) == 4 for r in candidates),
                    "no-resurrection": training["survivors"] == final["survivors"] == final["acceptance"]["hypotheses"],
                    "nonvacuous-acceptance": final["acceptance"]["accepted"] == (scenario != "unsupported"),
                    "evidence-counts": [len(final["evidence"][s]) for s in ("train", "validation")] == [4, 4],
                    "provenance-count": len(final["provenance"]) == 8,
                    "duplicate-count": sum(r.get("status") == "duplicate" for r in final["trace"]) == 2,
                    "rejection-count": sum(r.get("status") == "rejected" for r in final["trace"]) == 9,
                    "scope": predictions["x1"]["decision"] == "out_of_scope",
                    "birth-preserved": digest(final["birth"]) == digest(study.newborn(mode, scenario)["birth"]),
                    "specific-empty-reason": scenario != "unsupported" or all(p["reason"] == "no_supported_hypothesis" and not p["votes"] for eid, p in predictions.items() if eid != "x1"),
                })
                results["conditions"][name] = {"checks": checks, "support_status": final["support_status"],
                    "survivors": final["survivors"], "acceptance": final["acceptance"], "derivation": final["derivation"]}
        atomic_json(root / "frozen-predictions.json", frozen)
        for scenario in fixture.TRAIN:
            l = deepcopy(final_states["lmft-" + scenario]); m = deepcopy(final_states["memory-" + scenario])
            for state in (l, m):
                state.pop("birth"); state.pop("mode")
            results["checks"][scenario + "-memory-parity"] = l == m and frozen["lmft-" + scenario] == frozen["memory-" + scenario]
        expected_quality = {"unsupported": {"equality": (0, 0), "non_equality": (0, 0), "overall": (0, 0)},
                            "supported": {"equality": (4, 3), "non_equality": (4, 3), "overall": (8, 6)},
                            "ambiguous": {"equality": (0, 0), "non_equality": (4, 3), "overall": (4, 3)}}
        for name, predictions in frozen.items():
            groups = {"equality": quality(predictions, list(fixture.HELD)[:4]),
                      "non_equality": quality(predictions, list(fixture.HELD)[4:8]),
                      "overall": quality(predictions, list(fixture.HELD)[:8])}
            results["conditions"][name]["groups"] = groups
            scenario = final_states[name]["scenario"]
            results["conditions"][name]["quality_checks"] = {
                group: (r["decided"], r["correct"]) == expected_quality[scenario][group] for group, r in groups.items()}
        results["checks"]["archive-guard"] = load_guarded(root) == identity
        results["checks"]["protected-files-preserved"] = preserved(root)
        if context is not None and file_hash(root / "current-preservation-context.json") != context_hash:
            raise ValueError("current preservation context bytes changed")
        integrity = list(results["checks"].values()) + [v for r in results["conditions"].values() for v in r["checks"].values()]
        quality_checks = [v for r in results["conditions"].values() for v in r["quality_checks"].values()]
        results.update(integrity_passed=sum(integrity), integrity_total=len(integrity),
                       quality_passed=sum(quality_checks), quality_total=len(quality_checks))
        atomic_json(root / "results.json", results)
        print(json.dumps({k: v for k, v in results.items() if k.endswith(("passed", "total"))}))
        if not all(integrity + quality_checks):
            raise AssertionError("frozen study checks failed; preserve outcome")
    except Exception as exc:
        atomic_json(root / "failure.json", {"error": repr(exc)})
        raise


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output"); parser.add_argument("--restart", nargs=2)
    parser.add_argument("--preservation-context", help="Explicit nonempty complete current-source regression context; historical default unchanged")
    args = parser.parse_args()
    if args.restart:
        restart_worker(*(Path(p) for p in args.restart))
    elif args.output:
        run(Path(args.output).resolve(), args.preservation_context)
    else:
        parser.error("--output required")


if __name__ == "__main__":
    main()
