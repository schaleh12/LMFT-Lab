"""Preregistered actual offline teaching, followed by deterministic fresh evaluation."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from lmft_lab import teacher as t, teacher_fixture as f, attention_fixture
from lmft_lab.runtime_store import Store, atomic_json, digest
from run_comparative import start, halt, wait_for, check_boundary


def message(key, op, record, reply=None, source="registered-route-calibration-1"):
    result = {"schema_version": 1, "id": key, "sender": "fixture-owner", "source": source,
              "type": "teacher_reply" if reply else "observation",
              "content": {"text": "Attributed registered input.", "operation": op, "record": record}}
    if reply:
        result["reply_to"] = reply
    return result


def send(store, process, items):
    for msg in items:
        store.submit(msg)
    return wait_for(lambda: next((x for x in store.receive() if x["reply_to"] == items[-1]["id"]), None), process)


def measure(store, state):
    c = state["judgment"]
    return {"processing_seconds": sum(x.get("processing_seconds", 0) for x in state["receipts"]),
            "checkpoint_bytes": (store.root / "checkpoint.json").stat().st_size,
            "individual_bytes": sum(p.stat().st_size for p in store.root.rglob("*") if p.is_file()),
            "records": {**{k: len(c[k]) for k in ("calibration", "lessons", "cases", "evidence", "updates", "outcomes")},
                        **{k: len(state[k]) for k in ("receipts", "outbox", "diagnostics", "questions")}}}


def quality(state):
    rows = []
    for key in f.EVALUATION:
        item = state["judgment"]["cases"][key]
        selected = item["selected"]
        rows.append({"case_id": key, "route": selected["route"] if selected else None,
                     "resolved": item["resolved"], "prediction": item["result"]["decision"],
                     "actual_success": f.actual_success(key),
                     "irrelevant": bool(selected and selected["field"] != "shielded")})
    decisions = [x for x in rows if x["prediction"] != "abstain"]
    correct = sum((x["prediction"] == "success") == x["actual_success"] for x in decisions)
    return {"rows": rows, "resolved": sum(x["resolved"] for x in rows),
            "requests": sum(x["route"] is not None for x in rows),
            "irrelevant": sum(x["irrelevant"] for x in rows),
            "unresolved_verifications": sum(x["route"] is not None and not x["resolved"] for x in rows),
            "decided": len(decisions), "correct": correct, "abstentions": len(rows)-len(decisions),
            "accuracy": correct/len(decisions) if decisions else None, "coverage": len(decisions)/len(rows)}


def run_condition(root, mode, actual_reply=None):
    store = Store(root / "individual")
    process = None
    checks, commands = {}, []
    started = time.perf_counter()
    try:
        process = start(store.root, mode, new=True)
        checks["live_inspection_refused"] = check_boundary(store)
        send(store, process, [message(k, "outcome", attention_fixture.training_record(k))
                             for k in list(attention_fixture.contextual.TRIALS)[:8]])
        send(store, process, [message(k, "calibration", record) for k, record in f.TRAINING.items()])
        question = send(store, process, [message("ask", "ask_teacher", {})])
        checks["deliberate_teaching_question"] = question["type"] == "teaching_request"
        if mode == "teacher-lmft":
            for attempt in range(2):
                command = [sys.executable, "-m", "lmft_lab.teacher_adapter", "--root", str(store.root), "--offline"]
                if attempt:
                    command.append("--retry")
                completed = subprocess.run(command, capture_output=True, text=True, timeout=360)
                commands.append({"command": command, "returncode": completed.returncode,
                                 "stdout": completed.stdout, "stderr": completed.stderr})
                if completed.returncode == 0:
                    wait_for(lambda: any(x["content"].get("teaching_request") == question["id"] for x in store.receive()), process)
                    break
            # Duplicate command must not infer again after completion/disposition.
            if commands[-1]["returncode"] == 0:
                duplicate = subprocess.run(command, capture_output=True, text=True, timeout=30)
                commands.append({"command": command, "returncode": duplicate.returncode,
                                 "stdout": duplicate.stdout, "stderr": duplicate.stderr})
                checks["duplicate_adapter_no_call"] = duplicate.returncode == 0 and json.loads(duplicate.stdout)["calls"] == 0
        elif actual_reply is not None:
            send(store, process, [actual_reply])
        trained = halt(store, process); process = None
        atomic_json(root / "trained-halted.json", trained)
        atomic_json(root / "adapter-commands.json", commands)
        if mode == "teacher-lmft":
            journals = [json.loads(p.read_text(encoding="utf-8")) for p in store.root.rglob("journal.json")]
            actual_reply = journals[0].get("message") if journals else None
        predicted_selections = {k: t.selection(trained["judgment"], f.public_case(k))[0] for k in f.EVALUATION}
        stages = {"trained": measure(store, trained)}
        process = start(store.root, mode)
        restored = halt(store, process); process = None
        checks["restart_exact"] = restored == trained
        process = start(store.root, mode)
        if actual_reply:
            copied = deepcopy(actual_reply); copied["id"] = "new-id-lesson-repeat"
            send(store, process, [deepcopy(actual_reply), copied, message("repeat-barrier", "barrier", {})])
        repeated = halt(store, process); process = None
        checks["duplicate_lesson_no_learning"] = repeated["judgment"] == trained["judgment"]
        stages["repeated"] = measure(store, repeated)
        process = start(store.root, mode)
        evaluation_start = time.perf_counter()
        for key in f.EVALUATION:
            out = send(store, process, [message("case-"+key, "case", f.public_case(key))])
            if out["type"] == "clarification_request":
                evidence = f.verify_evaluation(key, out["content"]["candidate"])
                send(store, process, [message("verify-"+key, "verification", evidence, out["id"], "registered-teacher-evaluation-1")])
        final = halt(store, process); process = None
        evaluation_wall = time.perf_counter()-evaluation_start
        atomic_json(root / "final-halted.json", final)
        stages["final"] = measure(store, final)
        checks["post_restart_selection_matches_readonly"] = all(final["judgment"]["cases"][k]["selected"] == v for k, v in predicted_selections.items())
        checks["teacher_disabled_evaluation_weights_fixed"] = final["judgment"]["weights"] == trained["judgment"]["weights"]
        checks["seed_preserved"] = final["birth"] == trained["birth"]
        checks["counters_preserved"] = final["judgment"]["branches"] == trained["judgment"]["branches"]
        checks["prior_scores"] = [b["score"] for b in final["judgment"]["branches"].values()] == [1/3, -1/3]
        checks["one_request_per_fresh_case"] = len(final["questions"]) == 6
        checks["experience_updates_untouched"] = final["judgment"]["updates"] == []
        checks["exchange_retained"] = final["judgment"]["lessons"] == trained["judgment"]["lessons"]
        return {"checks": checks, "quality": quality(final), "weights": final["judgment"]["weights"],
                "lessons": [{k: v for k, v in x.items() if k != "exchange"} for x in final["judgment"]["lessons"]],
                "stages": stages, "evaluation_wall_seconds": evaluation_wall,
                "evaluation_processing_seconds": stages["final"]["processing_seconds"] - stages["repeated"]["processing_seconds"],
                "wall_seconds": time.perf_counter()-started}, actual_reply
    finally:
        if process is not None and process.poll() is None:
            halt(store, process)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True); args = parser.parse_args()
    root = Path(args.output); root.mkdir(parents=True, exist_ok=False)
    files = set(Path("src").rglob("*.py")) | set(Path("tests").rglob("*.py")) | set(Path("config").rglob("*.json"))
    files |= set(Path("experiments").glob("*RESULTS.md")) | {Path("experiments/TEACHER_PROTOCOL.md"), Path("experiments/run_comparative.py"), Path(__file__)}
    hashes = {}
    for source in sorted(files):
        relative = source.relative_to(Path.cwd()) if source.is_absolute() else source
        target = root / "archive" / relative; target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, target)
        hashes[str(relative)] = hashlib.sha256(source.read_bytes()).hexdigest()
    atomic_json(root / "archive-manifest.json", hashes)
    hardware = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,memory.free,driver_version", "--format=csv"], capture_output=True, text=True)
    ram = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory | ConvertTo-Json"], capture_output=True, text=True)
    atomic_json(root / "hardware.json", {"gpu": hardware.stdout, "ram": ram.stdout})
    results = {"conditions": {}, "checks": {}}
    try:
        actual_reply = None
        for mode in t.MODES:
            results["conditions"][mode], actual_reply = run_condition(root / mode, mode, actual_reply)
        journals = [json.loads(p.read_text(encoding="utf-8")) for p in (root / "teacher-lmft").rglob("journal.json")]
        attempts = [a for j in journals for a in j["attempts"]]
        results["teacher"] = {"attempts": len(attempts), "completed": sum(a["status"] == "completed" for a in attempts),
            "latency_seconds": sum((a.get("trace") or {}).get("elapsed_seconds", 0) for a in attempts),
            "offline": all((a.get("trace") or {}).get("offline", False) for a in attempts)}
        results["checks"]["bounded_calls"] = len(attempts) <= 2
        results["checks"]["memory_equivalent_quality"] = results["conditions"]["teacher-lmft"]["quality"] == results["conditions"]["teacher-memory"]["quality"]
        results["checks"]["memory_equivalent_weights"] = results["conditions"]["teacher-lmft"]["weights"] == results["conditions"]["teacher-memory"]["weights"]
        checks = list(results["checks"].values()) + [v for c in results["conditions"].values() for v in c["checks"].values()]
        results.update(passed=sum(checks), total=len(checks))
        atomic_json(root / "results.json", results)
        print(json.dumps({"passed": sum(checks), "total": len(checks), "teacher": results["teacher"]}))
        if not all(checks):
            raise AssertionError("integrity check failed; retain run")
    except Exception as exc:
        atomic_json(root / "failure.json", {"error": repr(exc)}); raise


if __name__ == "__main__":
    main()
