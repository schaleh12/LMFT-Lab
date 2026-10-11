"""Replay preserved real teacher messages; NEVER call a model or replace a proposal."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from lmft_lab.runtime_store import Store, atomic_json
from run_comparative import start, halt
from run_teacher import send, message, quality


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source, root = Path(args.source), Path(args.output)
    root.mkdir(parents=True, exist_ok=False)
    hashes = {}
    files = set(Path("src").rglob("*.py")) | set(Path("tests").rglob("*.py")) | set(Path("config").rglob("*.json"))
    files |= {Path(__file__), Path("experiments/run_teacher.py"), Path("experiments/run_comparative.py"), Path("experiments/TEACHER_PROTOCOL.md")}
    for path in files:
        relative = path.relative_to(Path.cwd()) if path.is_absolute() else path
        target = root / "archive" / relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target); hashes[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
    atomic_json(root / "archive-manifest.json", hashes)
    results = {"execution": "deterministic replay of archived actual model reply", "model_calls": 0, "conditions": {}}
    for mode in ("teacher-lmft", "teacher-none", "teacher-memory"):
        store = Store(root / mode / "individual")
        process = start(store.root, mode, new=True)
        try:
            items = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((source / mode / "individual" / "inbox").glob("*.json"))]
            send(store, process, items + [message("replay-barrier", "barrier", {})])
            final = halt(store, process)
            previous = json.loads((source / mode / "final-halted.json").read_text(encoding="utf-8"))
            checks = {k + "_identical": final[k] == previous[k] for k in ("judgment", "questions", "birth")}
            atomic_json(root / mode / "final-halted.json", final)
            results["conditions"][mode] = {"checks": checks, "quality": quality(final)}
        finally:
            if process.poll() is None:
                halt(store, process)
    checks = [v for c in results["conditions"].values() for v in c["checks"].values()]
    results.update(passed=sum(checks), total=len(checks))
    atomic_json(root / "results.json", results)
    print(json.dumps({"passed": sum(checks), "total": len(checks), "model_calls": 0}))
    if not all(checks):
        raise AssertionError("Replay differs; preserve both results")


if __name__ == "__main__":
    main()
