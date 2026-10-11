"""Reproduce the frozen mechanical protocol or separate actual local-model smoke.
Outputs are local and ignored. Run from the repository root with PYTHONPATH=src.
"""
import argparse
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import time

from lmft_lab.judgment import SAMPLES, probe
from lmft_lab.runtime_store import Store, atomic_json


def wait_for(predicate, process, timeout=420):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(process.communicate())
        result = predicate()
        if result:
            return result
        time.sleep(0.1)
    raise TimeoutError("Experiment deadline exceeded")


def start(root, new=False, local=False, control=False):
    command = [sys.executable, "-m", "lmft_lab.runtime", "--root", str(root), "start",
               "--mode", "local" if local else "fixture"]
    if new:
        command += ["--new", "experiment"]
    if local:
        command += ["--offline"]
    if control:
        command += ["--learning-disabled"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    wait_for(lambda: (root / "lifecycle.json").exists(), process)
    line = process.stdout.readline()
    if '"started"' not in line:
        raise RuntimeError(line + str(process.communicate()))
    return process


def stop(process, store):
    store.stop()
    output, error = process.communicate(timeout=420)
    if process.returncode != 0:
        raise RuntimeError(error)
    return store.inspect()


def message(identifier, sample=None, reply=None, text="Evaluate the synthetic channel measurement."):
    item = {"schema_version": 1, "id": identifier, "sender": "codex", "source": "supervised-fixture",
            "type": "teacher_reply" if reply else "observation", "content": {"text": text}}
    if sample:
        channel, reference = SAMPLES[sample]
        item["content"]["evidence"] = {"sample_id": sample, "channel": channel, "reference": reference}
    if reply:
        item["reply_to"] = reply
    return item


def exchange(store, process, item, expected):
    store.submit(item)
    return wait_for(lambda: store.receive() if len(store.receive()) >= expected else None, process)


def mechanical(root):
    results = {}
    for name, sample, control in (("restarted", "sample-a", False), ("uninterrupted", "sample-a", False),
                                  ("control", "sample-a", True), ("contrary", "sample-b", False)):
        directory = root / name
        store = Store(directory)
        process = start(directory, new=True, control=control)
        try:
            # Establish the baseline through the post-halt diagnostic interface.
            baseline = stop(process, store)
            assert probe(baseline["judgment"])["decision"] == "undetermined"
            process = start(directory, control=control)
            try:
                store.inspect()
                raise AssertionError("live inspection was allowed")
            except RuntimeError:
                pass
            outgoing = exchange(store, process, message("observation"), 2)
            assert outgoing[-1]["type"] == "clarification_request"
            reply = message("reply", sample, outgoing[-1]["id"])
            exchange(store, process, reply, 3)
            learned = stop(process, store)
            expected = 0 if control else 1/3 if sample == "sample-a" else -1/3
            assert learned["judgment"]["score"] == expected
            results[name] = {"baseline": probe(baseline["judgment"]), "learned": learned["judgment"],
                             "manifest": learned["manifest"]}
            if name == "restarted":
                process = start(directory)
                store.submit(reply)
                exchange(store, process, message("reattributed", sample), 4)
                recovered = stop(process, store)
                assert recovered["judgment"]["evidence"] == learned["judgment"]["evidence"]
                assert recovered["judgment"]["revisions"][:2] == learned["judgment"]["revisions"]
                assert recovered["receipts"][-2]["status"] == "duplicate"
                results[name]["recovered"] = recovered["judgment"]
                process = start(directory)
                exchange(store, process, message("contradiction", "sample-b"), 6)
                conflict = stop(process, store)
                assert conflict["judgment"]["score"] == 0
                assert len(conflict["judgment"]["evidence"]) == 2
                results[name]["conflict"] = conflict["judgment"]
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate()
    assert results["restarted"]["learned"] == results["uninterrupted"]["learned"]
    return {"execution": "mock", "protocol": "INTERACTIVE_REVISION_PROTOCOL.md", "passed": True,
            "comparisons": results}


def local_smoke(root):
    store = Store(root / "individual")
    process = start(store.root, new=True, local=True)
    try:
        exchange(store, process, message("local-1", text="A measurement was reported, but its reference has not been checked."), 2)
        exchange(store, process, message("local-2", text="The earlier claim remains unverified. Ask for the original measurement before accepting it."), 3)
        state = stop(process, store)
        diagnostics = state["diagnostics"]
        assert len(diagnostics) == 2
        assert all(d["processing"]["status"] == "completed" for d in diagnostics)
        assert all(c["execution"] == "local" for d in diagnostics for c in d["processing"]["calls"])
        pids = [d["model_server_pid"] for d in diagnostics]
        assert pids[0] is not None and pids[0] == pids[1]
        assert not state["judgment"]["evidence"]
        return {"execution": "actual-local-offline", "passed": True, "server_pids": pids,
                "calls": [{"role": c["role"], "elapsed_seconds": c["elapsed_seconds"],
                           "request_sha256": c["request_sha256"]} for d in diagnostics for c in d["processing"]["calls"]],
                "outbox": state["outbox"], "manifest": state["manifest"]}
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--local", action="store_true")
    args = parser.parse_args()
    root = Path(args.output)
    root.mkdir(parents=True, exist_ok=False)
    for pattern in ("src/lmft_lab/*.py", "tests/test_runtime.py", "config/local_models.json",
                    "experiments/run_interactive.py", "experiments/INTERACTIVE_REVISION_PROTOCOL.md"):
        for source in Path(".").glob(pattern):
            destination = root / "source_snapshot" / source
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    started = time.monotonic()
    try:
        result = local_smoke(root) if args.local else mechanical(root)
    except BaseException as exc:
        atomic_json(root / "failure.json", {"error": str(exc), "type": type(exc).__name__})
        raise
    result["elapsed_seconds"] = time.monotonic() - started
    atomic_json(root / "result.json", result)
    print(json.dumps({"passed": result["passed"], "execution": result["execution"],
                      "elapsed_seconds": result["elapsed_seconds"], "result": str(root / "result.json")}))


if __name__ == "__main__":
    main()
