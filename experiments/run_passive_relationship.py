"""Real supervised runtime integration, not a synthetic lifecycle substitute."""
import argparse
from copy import deepcopy
from dataclasses import asdict
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from lmft_lab import passive_relationship as p, insufficiency as s, insufficiency_fixture as f
from lmft_lab import preservation_context
from lmft_lab.runtime_store import Store, atomic_json, digest
from lmft_lab.birth import create_birth_state
from run_comparative import start, halt, check_boundary
from run_correction import send
from run_insufficiency import file_hash, quality

PROTOCOL = Path("experiments/PASSIVE_RELATIONSHIP_PROTOCOL.md")
PREWORK = Path("outputs/passive-runtime-prework-001/protected-hashes.json")


def message(identifier, operation, record, source=f.SOURCE):
    return {"schema_version": 1, "id": identifier, "sender": "fixture-operator", "source": source,
            "type": "observation", "content": {"text": "Passive synthetic relationship operation; independently verify evidence.",
                                                   "operation": operation, "record": deepcopy(record)}}


def invalid_inputs(scenario):
    first = f.outcome(scenario, "t1", "train")
    teacher = message("teacher-reply", "outcome", first)
    teacher.update(type="teacher_reply", reply_to="out-does-not-exist")
    malformed = message("malformed-envelope", "outcome", first)
    malformed["content"]["unknown"] = "unpermitted"
    return [message("false-label", "outcome", {**first, "success": False}),
            message("bad-source", "outcome", first, "external"),
            message("bad-type", "outcome", {**first, "length": True}),
            message("bad-feature", "outcome", {**first, "capacity": 8}),
            message("held-injection", "outcome", {**first, "split": "heldout", "evidence_id": "h1"}),
            message("proposal", "proposal", {"code": "add a new hypothesis"}),
            message("request", "request", {}), teacher, malformed,
            message("early-accept", "accept", {})]


def initial_messages(scenario):
    original = message("t1", "outcome", f.outcome(scenario, "t1", "train"))
    conflict = deepcopy(original); conflict["content"]["record"]["success"] = False
    return [message("untrained", "evaluate", s.case("before", (1, 4))), *invalid_inputs(scenario),
            *[message(eid, "outcome", f.outcome(scenario, eid, "train")) for eid in f.TRAIN[scenario]],
            deepcopy(original), conflict,
            message("evidence-copy", "outcome", f.outcome(scenario, "t1", "train")),
            message("identity-conflict", "outcome", {**f.outcome(scenario, "t1", "train"), "success": False}),
            message("select", "select", {}), message("unvalidated", "evaluate", s.case("before", (1, 4)))]


def final_messages(scenario):
    first = f.outcome(scenario, "t1", "train")
    return [message("before-noops", "evaluate", s.case("unchanged", (1, 4))),
            message("post-duplicate", "outcome", first),
            message("post-heldout", "outcome", {**first, "evidence_id": "h1", "split": "heldout"}),
            message("post-proposal", "proposal", p.candidates()[1]),
            message("post-select", "select", {}), message("post-accept", "accept", {}),
            message("after-noops", "evaluate", s.case("unchanged", (1, 4))),
            *[message("probe-" + eid, "evaluate", s.case(eid, pair)) for eid, pair in f.HELD.items()],
            message("final-barrier", "barrier", {})]


def standalone(scenario):
    state = s.newborn("memory", scenario)
    for eid in f.TRAIN[scenario]:
        s.admit(state, f.outcome(scenario, eid, "train"))
    s.select(state)
    for eid in f.VALIDATION:
        s.admit(state, f.outcome(scenario, eid, "validation"))
    s.accept(state)
    return state


def semantic(state):
    outbox = deepcopy(state["outbox"])
    receipts = deepcopy(state["receipts"])
    for record in outbox: record.pop("timestamp", None)
    for record in receipts: record.pop("processing_seconds", None)
    return {"outbox": outbox, "receipts": receipts, "processed": state["processed"], "cursor": state["cursor"]}


def run_case(root, mode, scenario, uninterrupted, preservation_root=None, preservation_sha256=None):
    store = Store(root / "individual"); process = None; checks = {}; pids = []
    extra = ("--relationship-scenario", scenario)

    def launch(new=False):
        if preservation_root is not None:
            preservation_context.pinned_current(preservation_root, Path.cwd(), preservation_sha256)
        proc = start(store.root, mode, new=new, extra_args=extra)
        pids.append(proc.pid)
        return proc

    try:
        process = launch(True)
        checks["live_inspection_denied"] = check_boundary(store)
        send(store, process, initial_messages(scenario))
        if not uninterrupted:
            training = halt(store, process); process = None
            atomic_json(root / "training-halted.json", training)
            process = launch(); restored = halt(store, process); process = None
            checks["training_restart_exact"] = restored == training
            process = launch()
        validation = [message(eid, "outcome", f.outcome(scenario, eid, "validation")) for eid in f.VALIDATION]
        send(store, process, validation + [message("accept", "accept", {})])
        if not uninterrupted:
            accepted = halt(store, process); process = None
            atomic_json(root / "accepted-halted.json", accepted)
            process = launch(); restored = halt(store, process); process = None
            checks["accepted_restart_exact"] = restored == accepted
            process = launch()
        send(store, process, final_messages(scenario))
        final = halt(store, process); process = None
        atomic_json(root / "final-halted.json", final)
        current = final["judgment"]
        outputs = {o["reply_to"]: o["content"] for o in final["outbox"]}
        predictions = {eid: outputs["probe-" + eid]["result"] for eid in f.HELD}
        atomic_json(root / "frozen-predictions.json", predictions)
        reference = standalone(scenario)
        atomic_json(root / "standalone-state.json", reference)
        checks["standalone_state_parity"] = current["learner"] == reference
        checks["standalone_prediction_parity"] = all(s.predict(reference, s.case(eid, pair)) == predictions[eid] for eid, pair in f.HELD.items())
        checks["candidate_space_persisted"] = current["candidate_space"] == p.candidates()
        checks["untrained_abstains"] = outputs["untrained"]["result"]["reason"] == "untrained"
        checks["unvalidated_reason"] = outputs["unvalidated"]["result"]["reason"] == ("no_supported_hypothesis" if scenario == "unsupported" else "not_validated")
        checks["scientific_noop_invariance"] = outputs["before-noops"]["scientific_digest"] == outputs["after-noops"]["scientific_digest"]
        checks["provenance_noop_invariance"] = outputs["before-noops"]["evidence_links_digest"] == outputs["after-noops"]["evidence_links_digest"]
        receipts = final["receipts"]
        checks["message_dedup"] = sum(r.get("status") == "duplicate" for r in receipts) == 1
        checks["message_conflict"] = sum(r.get("status") == "id_conflict" for r in receipts) == 1
        checks["evidence_dedup"] = sum(r.get("status") == "duplicate_evidence" for r in receipts) == 2
        rejected = {r.get("message_id"): r for r in receipts if r.get("status") == "rejected"}
        expected_rejected = {"false-label", "bad-source", "bad-type", "bad-feature", "held-injection", "proposal", "request", "teacher-reply", "early-accept", "identity-conflict", "post-heldout", "post-proposal", "post-select", "post-accept"}
        checks["rejection_records"] = expected_rejected <= set(rejected) and all("reason" in rejected[eid] and "message" in rejected[eid] for eid in expected_rejected)
        checks["malformed_receipt"] = any(r.get("status") == "rejected" and "raw" in r for r in receipts)
        checks["evidence_links"] = len(current["evidence_links"]) == 8 and all(v["source"] == f.SOURCE and v["sender"] == "fixture-operator" for v in current["evidence_links"].values())
        checks["no_questions_or_models"] = not final["questions"] and not final["diagnostics"] and all(o["type"] == "response" for o in final["outbox"])
        checks["scope"] = predictions["x1"]["decision"] == "out_of_scope"
        checks["manifest_policy"] = final["manifest"]["relationship_policy"] == p.policy(scenario)
        canonical = asdict(create_birth_state(final["individual_id"], birth_event_id=final["birth"]["birth_event_id"], random_seed=42))
        checks["birth_unchanged"] = digest(final["birth"]) == digest(canonical) and (uninterrupted or final["birth"] == accepted["birth"])
        checkpoint = store.root / "checkpoint.json"
        before_bytes = checkpoint.read_bytes(); before_state = digest(final)
        for eid, pair in f.HELD.items(): assert p.predict(current, s.case(eid, pair)) == predictions[eid]
        cli_probe = subprocess.run([sys.executable, "-m", "lmft_lab.runtime", "--root", str(store.root), "probe"], capture_output=True, text=True, check=True)
        checks["halted_cli_probe"] = json.loads(cli_probe.stdout) == p.snapshot(current)
        checks["read_only_probes"] = digest(final) == before_state and checkpoint.read_bytes() == before_bytes
        if not uninterrupted:
            checks["evaluation_preserved_judgment"] = current == accepted["judgment"]
        row = {"checks": checks, "mode": mode, "scenario": scenario, "pids": pids,
               "snapshot": p.snapshot(current), "checkpoint_bytes": len(before_bytes)}
        atomic_json(root / "integration-checks.json", row)
        return row, final, predictions
    finally:
        if process is not None and process.poll() is None:
            halt(store, process)


def compatibility_and_control(root):
    mode = p.MODES[0]; scenario = "supported"; store = Store(root / "individual"); process = None
    try:
        process = start(store.root, mode, new=True, control=True, extra_args=("--relationship-scenario", scenario))
        initial_science = p.scientific(p.newborn(mode, scenario))
        send(store, process, [message("disabled-evidence", "outcome", f.outcome(scenario, "t1", "train")),
                             message("disabled-select", "select", {}), message("disabled-accept", "accept", {}),
                             message("disabled-evaluate", "evaluate", s.case("disabled", (1, 4)))])
        state = halt(store, process); process = None
        atomic_json(root / "disabled-halted.json", state)
        checks = {"learning_disabled_scientific_invariance": p.scientific(state["judgment"]) == initial_science,
                  "learning_disabled_rejections": all(r["status"] == "rejected" and r["reason"] == "learning disabled" for r in state["receipts"][:3])}
        checkpoint = store.root / "checkpoint.json"; before = checkpoint.read_bytes()
        base = [sys.executable, "-m", "lmft_lab.runtime", "--root", str(store.root), "start", "--mode", "fixture", "--experiment", mode]
        for name, arguments in (("changed_scenario", ["--relationship-scenario", "ambiguous", "--learning-disabled"]),
                                ("changed_control", ["--relationship-scenario", scenario])):
            result = subprocess.run(base + arguments, capture_output=True, text=True, timeout=15)
            checks[name + "_refused"] = result.returncode == 1 and "Code/config/control changed" in result.stderr and checkpoint.read_bytes() == before
            atomic_json(root / (name + ".json"), {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        result = subprocess.run(base[:-4] + ["--mode", "local", "--experiment", mode], capture_output=True, text=True, timeout=15)
        checks["local_mode_refused"] = result.returncode == 1 and "require --mode fixture" in result.stderr and checkpoint.read_bytes() == before
        atomic_json(root / "checks.json", checks)
        return checks
    finally:
        if process is not None and process.poll() is None: halt(store, process)


def archive(root, preservation_context_path=None):
    context = None; context_hash = None
    if preservation_context_path is not None:
        context = json.loads(Path(preservation_context_path).read_text(encoding="utf-8"))
        preservation_context.verify_current(context, Path.cwd())
        context_hash = file_hash(preservation_context_path)
        shutil.copy2(preservation_context_path, root / "current-preservation-context.json")
    paths = set(Path("src").rglob("*.py")) | set(Path("tests").rglob("*.py")) | set(Path("config").rglob("*")) | set(Path("experiments").glob("*.py")) | {PROTOCOL, Path("AGENTS.md")}
    if context is not None: paths |= {Path(name) for name in context["files"]}
    manifest = {}
    for path in sorted(p for p in paths if p.is_file()):
        target = root / "archive" / path; target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(path, target)
        manifest[str(path)] = file_hash(path)
    atomic_json(root / "archive-manifest.json", manifest)
    atomic_json(root / "configuration.json", {scenario: p.policy(scenario) for scenario in p.SCENARIOS})
    atomic_json(root / "provenance.json", {"source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "working_tree": subprocess.check_output(["git", "status", "--short"], text=True), "python": sys.version,
        "model_calls": 0, "protocol_sha256": file_hash(PROTOCOL),
        "preservation_kind": preservation_context.KIND if context is not None else "legacy-passive-prework",
        "preservation_context_sha256": context_hash})
    protected = context["files"] if context is not None else json.loads(PREWORK.read_text(encoding="utf-8-sig")) if PREWORK.exists() else {}
    atomic_json(root / "protected-hashes.json", protected)
    return manifest, protected


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    parser.add_argument("--preservation-context", help="Explicit nonempty complete current-source regression context; historical default unchanged")
    args = parser.parse_args()
    root = Path(args.output); root.mkdir(parents=True, exist_ok=False)
    manifest, protected = archive(root, args.preservation_context)
    pinned = preservation_context.pinned_current(root, Path.cwd())
    results = {"restarted": {}, "uninterrupted": {}, "comparisons": {}, "model_calls": 0,
               "preservation_kind": preservation_context.KIND if pinned is not None else "legacy-passive-prework",
               "preservation_context_sha256": file_hash(root / "current-preservation-context.json") if pinned is not None else None,
               "preservation_count": len(protected)}; states = {}; predictions = {}
    try:
        for scenario in p.SCENARIOS:
            for mode in p.MODES:
                name = mode + "-" + scenario
                for uninterrupted in (False, True):
                    branch = "uninterrupted" if uninterrupted else "restarted"
                    row, state, pred = run_case(root / branch / name, mode, scenario, uninterrupted,
                        root if pinned is not None else None, results["preservation_context_sha256"])
                    results[branch][name] = row; states[branch, name] = state; predictions[branch + "/" + name] = pred
                l = states["restarted", name]; r = states["uninterrupted", name]
                results["comparisons"][name + "-restart"] = l["judgment"] == r["judgment"] and l["birth"] == r["birth"] and semantic(l) == semantic(r)
            a = states["restarted", p.MODES[0] + "-" + scenario]; b = states["restarted", p.MODES[1] + "-" + scenario]
            results["comparisons"][scenario + "-memory"] = p.scientific(a["judgment"]) == p.scientific(b["judgment"]) and a["judgment"]["evidence_links"] == b["judgment"]["evidence_links"] and semantic(a) == semantic(b)
        atomic_json(root / "frozen-predictions.json", predictions)
        results["control_compatibility"] = compatibility_and_control(root / "control-compatibility")
        expected = {"unsupported": {"equality": (0, 0), "non_equality": (0, 0), "overall": (0, 0)},
                    "supported": {"equality": (4, 3), "non_equality": (4, 3), "overall": (8, 6)},
                    "ambiguous": {"equality": (0, 0), "non_equality": (4, 3), "overall": (4, 3)}}
        for branch in ("restarted", "uninterrupted"):
            for name, row in results[branch].items():
                pred = predictions[branch + "/" + name]
                groups = {"equality": quality(pred, list(f.HELD)[:4]), "non_equality": quality(pred, list(f.HELD)[4:8]), "overall": quality(pred, list(f.HELD)[:8])}
                row["groups"] = groups
                row["quality_checks"] = {g: (r["decided"], r["correct"]) == expected[row["scenario"]][g] for g, r in groups.items()}
        results["comparisons"]["archive_hashes"] = all(file_hash(name) == h == file_hash(root / "archive" / name) for name, h in manifest.items())
        results["comparisons"]["protected_files"] = all(file_hash(name) == h for name, h in protected.items())
        if pinned is not None:
            preservation_context.pinned_current(root, Path.cwd(), results["preservation_context_sha256"])
        integrity = list(results["comparisons"].values()) + list(results["control_compatibility"].values()) + [v for branch in ("restarted", "uninterrupted") for r in results[branch].values() for v in r["checks"].values()]
        quality_checks = [v for branch in ("restarted", "uninterrupted") for r in results[branch].values() for v in r["quality_checks"].values()]
        results.update(integrity_passed=sum(integrity), integrity_total=len(integrity), quality_passed=sum(quality_checks), quality_total=len(quality_checks))
        atomic_json(root / "results.json", results)
        print(json.dumps({k: v for k, v in results.items() if k.endswith(("passed", "total"))}))
        if not all(integrity + quality_checks): raise AssertionError("Frozen passive integration checks failed; preserve failure")
    except Exception as exc:
        atomic_json(root / "failure.json", {"error": repr(exc)}); raise


if __name__ == "__main__": main()
