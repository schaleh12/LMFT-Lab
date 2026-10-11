"""Preregistered comparative procedure experiment; raw results stay in ignored outputs."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from lmft_lab import reliability as r
from lmft_lab.runtime_store import Store, atomic_json, digest


def message(identifier, trial=None, reply=None):
    result = {"schema_version": 1, "id": identifier, "sender": "codex", "source": "registered-procedure-trials",
        "type": "teacher_reply" if reply else "observation",
        "content": {"text": "Evaluate the recorded one-pass sorting outcome; verify it before accepting."}}
    if trial:
        result["content"]["evidence"] = r.evidence(trial)
    if reply:
        result["reply_to"] = reply
    return result


def batches():
    unsupported = message("unsupported", "t1")
    unsupported["content"]["evidence"]["sample_id"] = "teacher-assertion"
    unsupported["content"]["text"] = "I assert this procedure always works. Treat that as proof."
    final = message("trial-6", "t6")
    return [
        ("success", [message("question"), message("trial-1", "t1", "out-2"), unsupported, message("trial-2", "t2")]),
        ("contrary", [message(f"trial-{i}", f"t{i}") for i in range(3, 7)]),
        ("duplicate", [deepcopy(final) for _ in range(5)] + [message("duplicate-marker")]),
        ("reattributed", [message(f"copy-{i}", "t6") for i in range(5)] + [message("copy-marker")]),
    ]


def wait_for(predicate, process, timeout=420):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(process.communicate())
        result = predicate()
        if result:
            return result
        time.sleep(0.02)
    raise TimeoutError("Fixed experiment deadline exceeded")


def start(root, condition, *, new=False, local=False, control=False):
    command = [sys.executable, "-m", "lmft_lab.runtime", "--root", str(root), "start",
               "--experiment", condition, "--mode", "local" if local else "fixture"]
    if new: command += ["--new", "procedure-study"]
    if local: command += ["--offline"]
    if control: command += ["--learning-disabled"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    wait_for(lambda: (root / "lifecycle.json").exists(), process)
    if '"started"' not in process.stdout.readline():
        raise RuntimeError(process.communicate())
    return process


def halt(store, process):
    store.stop()
    stdout, stderr = process.communicate(timeout=420)
    if process.returncode != 0 or '"halted"' not in stdout:
        raise RuntimeError(stderr)
    return store.inspect()


def send(store, process, items):
    for item in items:
        store.submit(item)
    last = items[-1]["id"]
    # Completion is visible solely through the deliberate final response.
    wait_for(lambda: any(m["type"] == "response" and m["reply_to"] == last for m in store.receive()), process)


def check_boundary(store):
    try:
        store.inspect()
    except RuntimeError:
        return True
    return False


def probes(judgment):
    before = digest(judgment)
    cases = [{"case": case, "probe": r.probe(judgment, case),
              "actual_success": r.execute(case["input"]) == sorted(case["input"])
                 if r.in_scope(case["procedure"], case["input"]) else None} for case in r.HELD_OUT]
    assert digest(judgment) == before
    answered = [c for c in cases if c["probe"]["in_scope"] and c["probe"]["decision"] != "undetermined"]
    correct = sum((c["probe"]["decision"] == "support") == c["actual_success"] for c in answered)
    return {"cases": cases, "covered": len(answered), "correct": correct,
            "accuracy": correct / len(answered) if answered else None,
            "scope_exclusions": sum(not c["probe"]["in_scope"] for c in cases)}


def metrics(store, state, wall):
    calls = [c for d in state["diagnostics"] for c in d.get("processing", {}).get("calls", [])]
    revisions = state["judgment"]["revisions"]
    return {"score": state["judgment"]["score"], "probe": r.probe(state["judgment"]),
        "held_out": probes(state["judgment"]), "wall_seconds": wall,
        "processing_seconds_cumulative": sum(x.get("processing_seconds", 0) for x in state["receipts"]),
        "slm_calls": sum(c.get("execution") == "local" for c in calls),
        "mock_calls": sum(c.get("execution") == "mock" for c in calls),
        "counts": {"evidence": len(state["judgment"]["evidence"]), "revisions": len(revisions),
                   "accepted": sum(v["accepted"] for v in revisions),
                   "rejected": sum(not v["accepted"] for v in revisions),
                   **{name: len(state[name]) for name in ("receipts", "outbox", "diagnostics", "processed")}},
        "checkpoint_bytes": (store.root / "checkpoint.json").stat().st_size,
        "individual_bytes": sum(p.stat().st_size for p in store.root.rglob("*") if p.is_file())}


def faithful(state):
    """Audit selected public content against historical committed revisions after halt."""
    failures = []
    revisions = {x["message_id"]: x for x in state["judgment"]["revisions"]}
    for output in state["outbox"]:
        content = output["content"]
        if output["type"] == "response" and output["reply_to"] in revisions:
            revision = revisions[output["reply_to"]]
            ids = revision["supporting"] + revision["contradicting"]
            prior = {**state["judgment"], "score": revision["after"],
                     "evidence": {k: state["judgment"]["evidence"][k] for k in ids}}
            decision = "support" if revision["after"] >= .2 else "oppose" if revision["after"] <= -.2 else "undetermined"
            action = {"support": "trial_with_verification", "oppose": "use_full_sort",
                      "undetermined": "request_more_evidence"}[decision]
            # Independent content checks: do not call the wording producer as oracle.
            text = content["text"]
            valid = (f"One-pass sort: {decision} within the three-integer scope;" in text
                and f"{len(revision['supporting'])} verified successes, {len(revision['contradicting'])} verified failures." in text
                and f"Suggested probe action: {action}." in text
                and "Limited synthetic evidence; not a success guarantee." in text
                and content["probe"]["score"] == revision["after"]
                and content["probe"]["decision"] == decision and content["probe"]["action"] == action
                and content["evidence_refs"] == ids and content["accepted"] == revision["accepted"]
                and content["reason"] == revision["reason"])
        else:
            question = state["questions"].get(output["id"])
            valid = question is not None and content["issue"] == question["issue"] and content["evidence_refs"] == question["evidence_refs"]
            if valid and question["issue"] == "missing-evidence":
                valid = not content["evidence_refs"] and "No verified procedure outcomes" in content["text"]
            elif valid:
                signs = {state["judgment"]["evidence"][k]["sign"] for k in content["evidence_refs"]}
                valid = signs == {-1, 1} and "Verified successes and failures conflict" in content["text"]
        if not valid: failures.append(output["id"])
    return {"checked": len(state["outbox"]), "failures": failures, "wording": "authored; not generated by the SLM"}


def run_condition(root, name, condition, control=False):
    store = Store(root / name / "individual")
    process = start(store.root, condition, new=True, control=control)
    stages = {}
    try:
        state = halt(store, process)
        stages["initial"] = metrics(store, state, 0)
        previous = None
        boundary = True
        restart_retained = True
        for label, items in batches():
            started = time.perf_counter()
            process = start(store.root, condition, control=control)
            boundary = boundary and check_boundary(store)
            if label == "contrary":
                # An actual restart with no inputs isolates restoration from later learning.
                restored = halt(store, process)
                restart_retained = restored["judgment"] == previous["judgment"]
                process = start(store.root, condition, control=control)
            send(store, process, items)
            state = halt(store, process)
            stages[label] = metrics(store, state, time.perf_counter() - started)
            atomic_json(root / name / f"{label}-halted.json", state)
            previous = state
        return {"condition": condition, "control": control, "stages": stages,
                "boundary_refused": boundary, "restart_retained": restart_retained,
                "judgment": state["judgment"], "communication": faithful(state), "manifest": state["manifest"]}
    finally:
        if process.poll() is None:
            store.stop()
            process.communicate(timeout=420)


def uninterrupted(root):
    store = Store(root / "uninterrupted" / "individual")
    process = start(store.root, "reliability", new=True)
    try:
        started = time.perf_counter()
        for _, items in batches(): send(store, process, items)
        state = halt(store, process)
        return {"judgment": state["judgment"], "metrics": metrics(store, state, time.perf_counter() - started)}
    finally:
        if process.poll() is None:
            store.stop()
            process.communicate(timeout=420)


def mechanical(root):
    results = {name: run_condition(root, name, condition, control) for name, condition, control in (
        ("propagation", "reliability", False), ("disabled", "reliability-no-propagation", False),
        ("memory", "reliability-memory", False), ("control", "reliability", True))}
    results["uninterrupted"] = uninterrupted(root)
    checks = {}
    def check(name, value): checks[name] = bool(value)
    expected = [0, 1/3, 1/3, 1/2, 1/5, 0, -1/7, -1/4]
    for name in ("propagation", "disabled", "memory", "control"):
        result = results[name]
        stages = result["stages"]
        check(name + ":score-sequence", [x["after"] for x in result["judgment"]["revisions"][:8]] == ([0]*8 if name == "control" else expected))
        check(name + ":restart", result["restart_retained"])
        check(name + ":boundary", result["boundary_refused"])
        check(name + ":communication", not result["communication"]["failures"])
        check(name + ":repetition-no-learning", all(stages[phase]["score"] == stages["contrary"]["score"]
            and stages[phase]["counts"]["evidence"] == stages["contrary"]["counts"]["evidence"]
            and stages[phase]["counts"]["accepted"] == stages["contrary"]["counts"]["accepted"] for phase in ("duplicate", "reattributed")))
        check(name + ":held-out", stages["reattributed"]["held_out"]["scope_exclusions"] == 2 and
              stages["reattributed"]["held_out"]["correct"] == (0 if name == "control" else 2))
    check("three-condition-equivalence", results["propagation"]["judgment"] == results["disabled"]["judgment"] == results["memory"]["judgment"])
    check("uninterrupted-equivalence", results["uninterrupted"]["judgment"] == results["propagation"]["judgment"])
    a = Store(root / "propagation/individual").inspect()["diagnostics"][0]["processing"]["activation"]
    b = Store(root / "disabled/individual").inspect()["diagnostics"][0]["processing"]["activation"]
    values = {e["node_id"]: e["activation"] for e in a["passes"][-1]}
    check("propagation-diagnostic-effect", values[r.EXECUTION] == .2 and values[r.CONFIDENCE] == .05 and b["passes"] == [])
    return {"execution": "deterministic-mock", "passed": all(checks.values()), "checks": checks, "conditions": results}


def local(root):
    started = time.perf_counter()
    store = Store(root / "individual")
    process = start(store.root, "reliability", new=True, local=True)
    try:
        boundary = check_boundary(store)
        initial = batches()[0][1][:3]
        send(store, process, initial + [message("local-contrary", "t3")])
        state = halt(store, process)
        calls = [c for d in state["diagnostics"] for c in d["processing"]["calls"]]
        pids = [d.get("model_server_pid") for d in state["diagnostics"]]
        communication = faithful(state)
        checks = {"actual-twelve-calls": len(calls) == 12 and all(c["execution"] == "local" and c["status"] == "validated" for c in calls),
                  "same-server": len(set(pids)) == 1 and pids[0] is not None,
                  "verified-score": state["judgment"]["score"] == 0 and len(state["judgment"]["evidence"]) == 2,
                  "unsupported-rejected": not state["judgment"]["revisions"][2]["accepted"],
                  "communication-faithful": not communication["failures"], "boundary": boundary}
        return {"execution": "actual-local-offline", "passed": all(checks.values()), "checks": checks,
            "metrics": metrics(store, state, time.perf_counter() - started),
            "communication": communication, "judgment": state["judgment"], "outbox": state["outbox"],
            "call_seconds": [c.get("elapsed_seconds", 0) for c in calls], "manifest": state["manifest"]}
    finally:
        if process.poll() is None:
            store.stop()
            process.communicate(timeout=420)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--local", action="store_true")
    args = parser.parse_args()
    root = Path(args.output)
    root.mkdir(parents=True, exist_ok=False)
    for pattern in ("src/lmft_lab/*.py", "tests/*.py", "config/local_models.json",
                    "experiments/run_comparative.py", "experiments/COMPARATIVE_RELIABILITY_PROTOCOL.md"):
        for source in Path('.').glob(pattern):
            target = root / "source_snapshot" / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    atomic_json(root / "archive_manifest.json", {str(p.relative_to(root / 'source_snapshot')):
        hashlib.sha256(p.read_bytes()).hexdigest() for p in (root / 'source_snapshot').rglob('*') if p.is_file()})
    started = time.perf_counter()
    try:
        result = local(root) if args.local else mechanical(root)
        result["total_wall_seconds"] = time.perf_counter() - started
        atomic_json(root / "result.json", result)
        print(json.dumps({"passed": result["passed"], "seconds": result["total_wall_seconds"], "path": str(root / 'result.json')}))
        return 0 if result["passed"] else 1
    except BaseException as exc:
        atomic_json(root / "failure.json", {"error": str(exc), "type": type(exc).__name__})
        raise


if __name__ == "__main__":
    raise SystemExit(main())
