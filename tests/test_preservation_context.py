"""Complete current baselines and historical byte resolution fail closed."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest
from lmft_lab import preservation_context as p, insufficiency as s
from lmft_lab.runtime_store import Store, atomic_json, digest


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, "experiments/" + name + ".py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def source(tmp_path):
    root = tmp_path / "source"; (root / "src").mkdir(parents=True)
    (root / "src/a.py").write_text("current = 1\n")
    (root / "AGENTS.md").write_text("Frozen contract\n")
    return root


def test_current_baseline_complete_and_nonempty(tmp_path):
    root = source(tmp_path); context = p.capture_current(root)
    assert len(context["files"]) == 2
    assert p.verify_current(context, root)
    incomplete = deepcopy(context); incomplete["files"].pop("AGENTS.md")
    incomplete["inventory_digest"] = digest(incomplete["files"])
    with pytest.raises(ValueError, match="inventory changed"): p.verify_current(incomplete, root)
    empty = deepcopy(context); empty["files"] = {}; empty["inventory_digest"] = digest({})
    with pytest.raises(ValueError, match="nonempty"): p.verify_current(empty, root)


@pytest.mark.parametrize("change", ["tamper", "missing", "added"])
def test_current_catches_actual_source_changes(tmp_path, change):
    root = source(tmp_path); context = p.capture_current(root)
    if change == "tamper": (root / "src/a.py").write_text("current = 2\n")
    elif change == "missing": (root / "src/a.py").unlink()
    else: (root / "src/added.py").write_text("added = True\n")
    with pytest.raises(ValueError, match="changed"): p.verify_current(context, root)


def test_current_rejects_root_schema_digest_and_unsafe_paths(tmp_path):
    root = source(tmp_path); context = p.capture_current(root)
    with pytest.raises(ValueError, match="root mismatch"): p.verify_current(context, tmp_path)
    bad = {**context, "unexpected": 1}
    with pytest.raises(ValueError, match="schema"): p.verify_current(bad, root)
    bad = {**context, "inventory_digest": "0" * 64}
    with pytest.raises(ValueError, match="digest"): p.verify_current(bad, root)
    for name in ("../outside.py", "C:/outside.py", "/outside.py"):
        with pytest.raises(ValueError, match="unsafe"): p.canonical_map({name: "0" * 64})
    with pytest.raises(ValueError, match="duplicate"):
        p.canonical_map({"src\\a.py": "0" * 64, "src/a.py": "0" * 64})


@pytest.mark.parametrize("change", ["deleted", "changed", "mode_changed", "pin_changed"])
def test_pinned_current_context_never_falls_back(tmp_path, change):
    root = source(tmp_path); run = tmp_path / "run"; run.mkdir()
    context = run / "current-preservation-context.json"; atomic_json(context, p.capture_current(root))
    original_hash = p.file_hash(context)
    provenance = {"preservation_kind": p.KIND, "preservation_context_sha256": original_hash}
    atomic_json(run / "provenance.json", provenance)
    assert p.pinned_current(run, root, original_hash)
    if change == "deleted": context.unlink()
    elif change == "changed": context.write_text(context.read_text() + " ")
    elif change == "mode_changed":
        context.unlink(); provenance["preservation_kind"] = "legacy-historical-prework"; atomic_json(run / "provenance.json", provenance)
    else:
        provenance["preservation_context_sha256"] = "0" * 64; atomic_json(run / "provenance.json", provenance)
    with pytest.raises(ValueError): p.pinned_current(run, root, original_hash)


def historical_fixture(tmp_path, monkeypatch):
    audit = load_script("verify_preservation")
    root = tmp_path / "historical"; (root / "archive/src/lmft_lab").mkdir(parents=True)
    (root / "archive/experiments").mkdir()
    runtime = b"old runtime bytes\n"
    (root / "archive/src/lmft_lab/runtime.py").write_bytes(runtime)
    protocol = Path("experiments/INSUFFICIENCY_PROTOCOL.md").read_bytes()
    (root / "archive/experiments/INSUFFICIENCY_PROTOCOL.md").write_bytes(protocol)
    hash_bytes = lambda data: hashlib.sha256(data).hexdigest()
    manifest = {"src\\lmft_lab\\runtime.py": hash_bytes(runtime),
                "experiments\\INSUFFICIENCY_PROTOCOL.md": hash_bytes(protocol)}
    blobs = {"docs/extra.md": b"historical document\n", "docs/raw.md": b"historical raw bytes\n"}
    protected = {"src/lmft_lab/runtime.py": hash_bytes(runtime),
                 "docs/extra.md": hash_bytes(blobs["docs/extra.md"].replace(b"\n", b"\r\n")),
                 "docs/raw.md": hash_bytes(blobs["docs/raw.md"])}
    atomic_json(root / "archive-manifest.json", manifest); atomic_json(root / "protected-hashes.json", protected)
    atomic_json(root / "configuration.json", {"task": "isolated audit fixture"})
    atomic_json(root / "provenance.json", {"source_commit": audit.SOURCE_REVISION, "protocol_sha256": audit.PROTOCOL_SHA256})
    atomic_json(root / "results.json", {"integrity_passed": 137, "integrity_total": 137, "quality_passed": 18, "quality_total": 18})
    files = {path.relative_to(root).as_posix(): p.file_hash(path) for path in root.rglob("*") if path.is_file()}
    context = {"kind": audit.HISTORICAL_KIND, "context_id": audit.CONTEXT_ID, "source_revision": audit.SOURCE_REVISION,
               "protocol_sha256": audit.PROTOCOL_SHA256, "counts": {"archive_sources": 2, "protected": 3, "protected_git": 2},
               "files": files, "inventory_digest": digest(files), "metadata": {n:files[n] for n in audit.METADATA}}
    def blob_reader(git_root, revision, name):
        assert revision == audit.SOURCE_REVISION
        return blobs[name]
    monkeypatch.setattr(audit, "git_blob", blob_reader)
    return audit, root, context, blobs


def test_historical_resolves_all_original_bytes_while_current_code_differs(tmp_path, monkeypatch):
    audit, root, context, blobs = historical_fixture(tmp_path, monkeypatch)
    current = source(tmp_path); (current / "src/a.py").write_text("legitimate later code\n")
    result = audit.audit_historical(root, current, context)
    assert result["passed"] and result["current_working_source_used"] is False
    assert len(result["archive_checks"]) == 2 and len(result["protected_resolutions"]) == 3
    rows = {r["name"]:r for r in result["protected_resolutions"]}
    assert rows["src/lmft_lab/runtime.py"]["source"] == "archive"
    assert rows["docs/extra.md"]["rendering"] == "git-blob-lf-to-crlf-checkout"
    assert rows["docs/raw.md"]["rendering"] == "git-blob-exact"


@pytest.mark.parametrize("name", ["archive/src/lmft_lab/runtime.py", "archive-manifest.json", "protected-hashes.json", "configuration.json", "provenance.json"])
@pytest.mark.parametrize("change", ["tamper", "missing"])
def test_historical_rejects_tampered_or_missing_archive_bytes(tmp_path, monkeypatch, name, change):
    audit, root, context, blobs = historical_fixture(tmp_path, monkeypatch)
    target = root / name
    if change == "missing": target.unlink()
    else: target.write_bytes(target.read_bytes() + b"changed")
    with pytest.raises(ValueError, match="archive"): audit.audit_historical(root, tmp_path, context)


@pytest.mark.parametrize("change", ["revision", "id", "empty", "metadata", "counts"])
def test_historical_wrong_or_incomplete_context_fails(tmp_path, monkeypatch, change):
    audit, root, context, blobs = historical_fixture(tmp_path, monkeypatch)
    if change == "revision": context["source_revision"] = "0" * 40
    elif change == "id": context["context_id"] = "different-study"
    elif change == "empty": context["files"] = {}; context["inventory_digest"] = digest({})
    elif change == "metadata": context["metadata"].pop("protected-hashes.json")
    else: context["counts"]["protected"] = 1
    with pytest.raises(ValueError): audit.audit_historical(root, tmp_path, context)


@pytest.mark.parametrize("failure", ["wrong_revision", "missing_blob", "changed_blob"])
def test_historical_versioned_source_evidence_fails_closed(tmp_path, monkeypatch, failure):
    audit, root, context, blobs = historical_fixture(tmp_path, monkeypatch)
    if failure == "missing_blob":
        def unavailable(*args): raise ValueError("missing versioned bytes")
        monkeypatch.setattr(audit, "git_blob", unavailable)
    elif failure == "changed_blob": monkeypatch.setattr(audit, "git_blob", lambda *args: b"later unrelated bytes\n")
    with pytest.raises(ValueError):
        audit.audit_historical(root, tmp_path, context, "0" * 40 if failure == "wrong_revision" else None)


@pytest.mark.parametrize("change", ["delete", "tamper"])
def test_actual_insufficiency_restart_rejects_missing_or_changed_current_context(tmp_path, change):
    runner = load_script("run_insufficiency"); root = tmp_path / "run"; root.mkdir()
    context_path = root / "current-preservation-context.json"
    atomic_json(context_path, p.capture_current(Path.cwd()))
    atomic_json(root / "provenance.json", {"preservation_kind": p.KIND, "preservation_context_sha256": p.file_hash(context_path)})
    path = Path("src/lmft_lab/insufficiency.py"); archived = root / "archive" / path; archived.parent.mkdir(parents=True)
    archived.write_bytes(path.read_bytes())
    atomic_json(root / "archive-manifest.json", {str(path):p.file_hash(path)})
    atomic_json(root / "configuration.json", s.configuration())
    state = runner.prepare_training("memory", "unsupported"); state["study_identity"] = runner.load_guarded(root)
    checkpoint = root / "individual"; Store(checkpoint).commit(state)
    before = (checkpoint / "checkpoint.json").read_bytes()
    if change == "delete": context_path.unlink()
    else: context_path.write_text(context_path.read_text() + " ")
    result = subprocess.run([sys.executable, "experiments/run_insufficiency.py", "--restart", str(root), str(checkpoint)], capture_output=True, text=True)
    assert result.returncode != 0 and "preservation context" in result.stderr
    assert (checkpoint / "checkpoint.json").read_bytes() == before
    assert not (checkpoint / "restart-result.json").exists()


@pytest.mark.parametrize("change", ["delete", "tamper"])
def test_passive_restart_gate_rejects_context_change_after_actual_halt(tmp_path, monkeypatch, change):
    monkeypatch.syspath_prepend(str(Path("experiments").resolve()))
    runner = load_script("run_passive_relationship")
    root = tmp_path / "run"; root.mkdir()
    context_path = root / "current-preservation-context.json"
    atomic_json(context_path, p.capture_current(Path.cwd()))
    expected_hash = p.file_hash(context_path)
    atomic_json(root / "provenance.json", {"preservation_kind": p.KIND, "preservation_context_sha256": expected_hash})
    original_halt = runner.halt
    def halt_then_change_context(store, process):
        state = original_halt(store, process)
        if change == "delete": context_path.unlink()
        else: context_path.write_text(context_path.read_text() + " ")
        return state
    monkeypatch.setattr(runner, "halt", halt_then_change_context)
    condition = root / "condition"
    with pytest.raises(ValueError, match="preservation context"):
        runner.run_case(condition, runner.p.MODES[0], "supported", False, root, expected_hash)
    lifecycle = json.loads((condition / "individual/lifecycle.json").read_text())
    assert lifecycle["status"] == "halted"
    assert (condition / "training-halted.json").exists()
    assert not (condition / "accepted-halted.json").exists()
