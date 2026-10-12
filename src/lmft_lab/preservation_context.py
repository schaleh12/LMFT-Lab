"""Explicit current source preservation; historical science remains separate."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from .runtime_store import digest

KIND = "current-regression-preservation-1"
SCOPE = "repository-source-inventory-1"
ROOTS = ("src", "tests", "config", "experiments", "docs")
ROOT_SUFFIXES = {".py", ".md", ".txt", ".json", ".toml", ".cfg", ".ini"}


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_map(mapping):
    if not isinstance(mapping, dict) or not mapping:
        raise ValueError("preservation manifest must be nonempty")
    result = {}
    for name, value in mapping.items():
        if not isinstance(name, str) or not name or not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError("malformed preservation identity/hash")
        canonical = name.replace("\\", "/")
        path = PurePosixPath(canonical)
        if path.is_absolute() or ":" in canonical or any(p in ("", ".", "..") for p in canonical.split("/")):
            raise ValueError("unsafe preservation path")
        if canonical in result:
            raise ValueError("duplicate canonical preservation identity")
        result[canonical] = value
    return result


def source_files(root):
    root = Path(root).resolve()
    files = set()
    for name in ROOTS:
        for path in (root / name).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in (".pyc", ".pyo"):
                files.add(path)
    files.update(p for p in root.iterdir() if p.is_file() and (p.suffix in ROOT_SUFFIXES or p.name == ".gitignore"))
    return {p.relative_to(root).as_posix(): p for p in sorted(files)}


def capture_current(root):
    root = Path(root).resolve()
    files = canonical_map({name: file_hash(path) for name, path in source_files(root).items()})
    return {"kind": KIND, "scope": SCOPE, "root": str(root), "files": files,
            "inventory_digest": digest(files)}


def verify_current(context, root):
    if not isinstance(context, dict) or set(context) != {"kind", "scope", "root", "files", "inventory_digest"}:
        raise ValueError("invalid current preservation context schema")
    if context["kind"] != KIND or context["scope"] != SCOPE:
        raise ValueError("wrong preservation context kind/scope")
    if not isinstance(context["root"], str) or Path(context["root"]).resolve() != Path(root).resolve():
        raise ValueError("current preservation root mismatch")
    files = canonical_map(context["files"])
    if files != context["files"] or digest(files) != context["inventory_digest"]:
        raise ValueError("current preservation context digest/identity mismatch")
    actual = source_files(root)
    if set(files) != set(actual):
        raise ValueError("current source inventory changed: added or missing files")
    for name, path in actual.items():
        if file_hash(path) != files[name]:
            raise ValueError("current source bytes changed: " + name)
    return True


def pinned_current(run_root, source_root, expected_sha256=None):
    """Provenance selects the mode; missing context never selects a fallback."""
    run_root = Path(run_root)
    provenance_path = run_root / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8")) if provenance_path.exists() else {}
    context_path = run_root / "current-preservation-context.json"
    if provenance.get("preservation_kind") != KIND:
        if context_path.exists() or expected_sha256 is not None:
            raise ValueError("unregistered current preservation context")
        return None
    expected_hash = provenance.get("preservation_context_sha256")
    if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        raise ValueError("missing current preservation context pin")
    if expected_sha256 is not None and expected_hash != expected_sha256:
        raise ValueError("current preservation identity changed")
    if not context_path.is_file():
        raise ValueError("missing pinned current preservation context")
    if file_hash(context_path) != expected_hash:
        raise ValueError("pinned current preservation context bytes changed")
    context = json.loads(context_path.read_text(encoding="utf-8"))
    verify_current(context, source_root)
    return context
