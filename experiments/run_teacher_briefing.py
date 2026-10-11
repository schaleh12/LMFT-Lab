"""Four preregistered offline calls; no retries or replacement proposals."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from lmft_lab import teacher as t, teacher_briefing as b, teacher_fixture as f, attention_fixture
from lmft_lab.runtime_store import Store, atomic_json
from lmft_lab.teacher_profile import validate_lesson
from run_comparative import start, halt, wait_for, check_boundary
from run_teacher import send, message, measure

ALLOCATION = ((1, "beneficial"), (2, "beneficial"), (1, "no-change"), (2, "no-change"))


def enumerate_candidates(situation):
    state = t.newborn("teacher-lmft", {"situation": situation, "initial_weights": b.load_briefing()["situations"][situation]})
    state["calibration"] = {k: {"record": r} for k, r in f.TRAINING.items()}
    rows = []
    for route in ("A", "B", "D"):
        refs = [k for k, r in f.TRAINING.items() if r["route"] == route] or ["train-A1", "train-A2"]
        for weight in (.25, .5, .75):
            proposal = {"route": route, "weight": weight, "supporting_evidence": refs,
                        "reason": "Pre-inference finite feasibility enumeration.", "uncertainty": "Validation only."}
            validate_lesson(json.dumps(proposal))
            rows.append({"route": route, "weight": weight, "assessment": t.assess(state, proposal)})
    return rows


def quality(state):
    rows = []
    for key in b.EVALUATION:
        item = state["judgment"]["cases"][key]; selected = item["selected"]
        rows.append({"case_id": key, "route": selected["route"] if selected else None,
            "resolved": item["resolved"], "prediction": item["result"]["decision"],
            "actual_success": b.actual_success(key), "irrelevant": bool(selected and selected["field"] != "shielded")})
    decided = [r for r in rows if r["prediction"] != "abstain"]
    correct = sum((r["prediction"] == "success") == r["actual_success"] for r in decided)
    return {"rows": rows, "resolved": sum(r["resolved"] for r in rows),
        "requests": sum(r["route"] is not None for r in rows), "irrelevant": sum(r["irrelevant"] for r in rows),
        "inconclusive_requests": sum(r["route"] is not None and not r["resolved"] for r in rows),
        "correct": correct, "decided": len(decided), "abstentions": len(rows)-len(decided),
        "accuracy": correct/len(decided) if decided else None, "coverage": len(decided)/len(rows)}


def operational_metrics(event, situation):
    if not event or "proposal" not in event:
        return {"schema_valid": False, "operationally_appropriate": False}
    p = event["proposal"]
    refs = p["supporting_evidence"]
    eligible = all(k in f.TRAINING and f.TRAINING[k]["route"] == p["route"] for k in refs)
    no_op = p["weight"] == event["before"][p["route"]]
    direction = eligible and not no_op and all(f.TRAINING[k]["available"] == (p["weight"] > event["before"][p["route"]]) for k in refs)
    return {"schema_valid": True, "same_route_eligible_evidence": eligible, "no_op": no_op,
        "grounded_change_direction": direction, "accepted": event["accepted"],
        "operationally_appropriate": bool(event["accepted"] if situation == "beneficial" else eligible and no_op)}


def run_condition(root, mode, version, situation, actual_reply=None):
    store = Store(root / "individual"); process = None
    extra = ["--teacher-profile", f"foundational-teacher-v{version}", "--teacher-study", situation]
    checks = {}; command_record = None
    try:
        process = start(store.root, mode, new=True, extra_args=extra)
        checks["live_inspection_refused"] = check_boundary(store)
        send(store, process, [message(k, "outcome", attention_fixture.training_record(k)) for k in list(attention_fixture.contextual.TRIALS)[:8]])
        send(store, process, [message(k, "calibration", r) for k, r in f.TRAINING.items()])
        question = send(store, process, [message("ask", "ask_teacher", {})])
        if mode == "teacher-lmft":
            command = [sys.executable, "-m", "lmft_lab.teacher_adapter", "--root", str(store.root),
                       "--offline", "--profile", f"foundational-teacher-v{version}"]
            atomic_json(root / "call-reservation.json", {"attempt": 1, "command": command, "retry_permitted": False})
            began = time.perf_counter()
            try:
                completed = subprocess.run(command, capture_output=True, text=True, timeout=360)
                command_record = {"returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
            except subprocess.TimeoutExpired:
                command_record = {"returncode": -1, "error": "adapter process deadline; slot consumed"}
            command_record["wall_seconds"] = time.perf_counter()-began
            atomic_json(root / "adapter-command.json", command_record)
            if command_record["returncode"] == 0:
                wait_for(lambda: any(x["content"].get("teaching_request") == question["id"] for x in store.receive()), process)
        elif actual_reply is not None:
            send(store, process, [actual_reply])
        trained = halt(store, process); process = None
        atomic_json(root / "trained-halted.json", trained)
        if mode == "teacher-lmft":
            journals = [json.loads(p.read_text(encoding="utf-8")) for p in store.root.rglob("journal.json")]
            actual_reply = journals[0].get("message") if journals else None
        before = measure(store, trained)
        selections = {k: t.selection(trained["judgment"], b.public_case(k))[0] for k in b.EVALUATION}
        process = start(store.root, mode, extra_args=extra)
        restored = halt(store, process); process = None
        checks["restart_exact"] = restored == trained
        process = start(store.root, mode, extra_args=extra)
        began = time.perf_counter()
        for key in b.EVALUATION:
            out = send(store, process, [message("case-"+key, "case", b.public_case(key))])
            if out["type"] == "clarification_request":
                record = b.verify_evaluation(key, out["content"]["candidate"])
                send(store, process, [message("verify-"+key, "verification", record, out["id"], "registered-teacher-evaluation-1")])
        final = halt(store, process); process = None
        elapsed = time.perf_counter()-began
        atomic_json(root / "final-halted.json", final)
        after = measure(store, final)
        for field in ("lessons", "weights", "branches"):
            checks[field+"_retained"] = final["judgment"][field] == trained["judgment"][field]
        checks["seed_retained"] = final["birth"] == trained["birth"]
        checks["restart_behavior"] = all(final["judgment"]["cases"][k]["selected"] == v for k, v in selections.items())
        checks["no_experience_updates"] = final["judgment"]["updates"] == []
        checks["one_request_per_case"] = len(final["questions"]) == 6
        events = final["judgment"]["lessons"]
        return {"checks": checks, "quality": quality(final), "weights": final["judgment"]["weights"],
            "disposition": {k: v for k, v in events[0].items() if k != "exchange"} if events else None,
            "operational": operational_metrics(events[0] if events else None, situation),
            "evaluation_wall_seconds": elapsed, "evaluation_core_seconds": after["processing_seconds"]-before["processing_seconds"],
            "stages": {"trained": before, "final": after}}, actual_reply
    finally:
        if process is not None and process.poll() is None:
            halt(store, process)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True); args = parser.parse_args()
    root = Path(args.output); root.mkdir(parents=True, exist_ok=False)
    files = set(Path("src").rglob("*.py")) | set(Path("tests").rglob("*.py")) | set(Path("config").rglob("*.json"))
    files |= set(Path("experiments").glob("*RESULTS.md")) | {Path(__file__), Path("experiments/run_teacher.py"), Path("experiments/run_comparative.py"), Path("experiments/TEACHER_BRIEFING_PROTOCOL.md")}
    hashes = {}
    for path in sorted(files):
        relative = path.relative_to(Path.cwd()) if path.is_absolute() else path
        target = root / "archive" / relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target); hashes[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
    atomic_json(root / "archive-manifest.json", hashes)
    feasibility = {s: enumerate_candidates(s) for s in b.SITUATIONS}
    atomic_json(root / "pre-inference-feasibility.json", feasibility)
    assert sum(r["assessment"]["accepted"] for r in feasibility["beneficial"]) == 2
    assert not any(r["assessment"]["accepted"] for r in feasibility["no-change"])
    atomic_json(root / "call-allocation.json", {"allocation": ALLOCATION, "seed": 42, "max_calls": 4, "retries": 0})
    results = {"slots": {}, "checks": {}}
    try:
        for number, (version, situation) in enumerate(ALLOCATION, 1):
            slot_id = f"slot-{number}-v{version}-{situation}"
            slot = {"profile": version, "situation": situation, "conditions": {}}
            actual_reply = None
            for mode in t.MODES:
                slot["conditions"][mode], actual_reply = run_condition(root / slot_id / mode, mode, version, situation, actual_reply)
            journals = [json.loads(p.read_text(encoding="utf-8")) for p in (root / slot_id / "teacher-lmft").rglob("journal.json")]
            attempts = [a for j in journals for a in j["attempts"]]
            trace = attempts[0].get("trace") if attempts else None
            response = (trace or {}).get("response", {})
            slot["inference"] = {"attempts": len(attempts), "completed": bool(actual_reply), "latency_seconds": (trace or {}).get("elapsed_seconds"),
                "offline": (trace or {}).get("offline"), "usage": response.get("usage"),
                "finish_reason": response.get("choices", [{}])[0].get("finish_reason")}
            results["checks"][slot_id+"-call-bound"] = len(attempts) <= 1
            results["checks"][slot_id+"-memory-quality"] = slot["conditions"]["teacher-lmft"]["quality"] == slot["conditions"]["teacher-memory"]["quality"]
            results["checks"][slot_id+"-memory-weights"] = slot["conditions"]["teacher-lmft"]["weights"] == slot["conditions"]["teacher-memory"]["weights"]
            results["slots"][slot_id] = slot
            atomic_json(root / "results.json", results)
            print(json.dumps({"slot": slot_id, "inference": slot["inference"], "operational": slot["conditions"]["teacher-lmft"]["operational"]}), flush=True)
        checks = list(results["checks"].values()) + [v for slot in results["slots"].values() for c in slot["conditions"].values() for v in c["checks"].values()]
        results.update(passed=sum(checks), total=len(checks), model_calls=sum(s["inference"]["attempts"] for s in results["slots"].values()))
        atomic_json(root / "results.json", results)
        if not all(checks):
            raise AssertionError("integrity check failed; preserve run")
    except Exception as exc:
        atomic_json(root / "failure.json", {"error": repr(exc)}); raise


if __name__ == "__main__":
    main()
