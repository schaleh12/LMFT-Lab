"""Separate current regression baselines and read-only historical byte audits."""
import argparse
import json
from pathlib import Path
import subprocess
from lmft_lab import preservation_context as current
from lmft_lab.runtime_store import atomic_json, digest

HISTORICAL_KIND = "historical-insufficiency-1"
CONTEXT_ID = "insufficiency-primary-2026-10-12"
SOURCE_REVISION = "5e45ab365688c7b0b0ac246fd8e7db558e509704"
PROTOCOL_SHA256 = "1cb49361efc3d33249f75aaa01d40b0d06836aefd4bbd350f2ec710182852369"
CONTEXT_PATH = Path("experiments/INSUFFICIENCY_HISTORICAL_CONTEXT.json")
METADATA = {"archive-manifest.json", "protected-hashes.json", "configuration.json", "provenance.json", "results.json"}


def git_blob(root, revision, name):
    result = subprocess.run(["git", "-C", str(root), "cat-file", "blob", revision + ":" + name], capture_output=True)
    if result.returncode:
        raise ValueError("missing versioned historical bytes: " + name)
    return result.stdout


def audit_historical(root, git_root, context, source_revision=None):
    required = {"kind", "context_id", "source_revision", "protocol_sha256", "counts", "files", "inventory_digest", "metadata"}
    if not isinstance(context, dict) or set(context) != required:
        raise ValueError("invalid historical context schema")
    if (context["kind"] != HISTORICAL_KIND or context["context_id"] != CONTEXT_ID
            or context["source_revision"] != SOURCE_REVISION or context["protocol_sha256"] != PROTOCOL_SHA256):
        raise ValueError("wrong historical context identity/revision/protocol")
    revision = source_revision or context["source_revision"]
    if revision != context["source_revision"]:
        raise ValueError("wrong historical source revision")
    expected = current.canonical_map(context["files"])
    if expected != context["files"] or digest(expected) != context["inventory_digest"]:
        raise ValueError("historical context inventory digest mismatch")
    if not isinstance(context["metadata"], dict) or set(context["metadata"]) != METADATA:
        raise ValueError("incomplete historical metadata pins")
    if any(context["metadata"][name] != expected.get(name) for name in METADATA):
        raise ValueError("historical metadata/context disagreement")
    root = Path(root).resolve()
    actual = {path.relative_to(root).as_posix(): path for path in root.rglob("*") if path.is_file()}
    if set(actual) != set(expected):
        raise ValueError("historical archive inventory changed: missing/added bytes")
    for name, path in actual.items():
        if current.file_hash(path) != expected[name]:
            raise ValueError("historical archive bytes changed: " + name)
    manifest = current.canonical_map(json.loads((root / "archive-manifest.json").read_text(encoding="utf-8")))
    protected = current.canonical_map(json.loads((root / "protected-hashes.json").read_text(encoding="utf-8-sig")))
    omitted = set(protected) - set(manifest)
    counts = {"archive_sources": len(manifest), "protected": len(protected), "protected_git": len(omitted)}
    if counts != context["counts"] or any(type(v) is not int or v <= 0 for v in context["counts"].values()):
        raise ValueError("historical manifest/context counts mismatch")
    provenance = json.loads((root / "provenance.json").read_text(encoding="utf-8"))
    if provenance["source_commit"] != revision or provenance["protocol_sha256"] != PROTOCOL_SHA256:
        raise ValueError("historical provenance/context mismatch")
    if current.file_hash(root / "archive" / "experiments/INSUFFICIENCY_PROTOCOL.md") != PROTOCOL_SHA256:
        raise ValueError("historical protocol mismatch")
    archive_checks = []
    for name, expected_hash in sorted(manifest.items()):
        path = root / "archive" / name
        if current.file_hash(path) != expected_hash:
            raise ValueError("historical archived source mismatch: " + name)
        archive_checks.append({"name": name, "source": "archive/" + name, "sha256": expected_hash})
    resolutions = []
    for name, expected_hash in sorted(protected.items()):
        if name in manifest:
            if manifest[name] != expected_hash:
                raise ValueError("historical archive/protected disagreement: " + name)
            resolutions.append({"name": name, "source": "archive", "path": "archive/" + name,
                                "revision": None, "rendering": "exact", "sha256": expected_hash})
        else:
            blob = git_blob(git_root, revision, name)
            rendering = "git-blob-exact"
            import hashlib
            blob_hash = hashlib.sha256(blob).hexdigest()
            if blob_hash != expected_hash:
                blob_hash = hashlib.sha256(blob.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest()
                rendering = "git-blob-lf-to-crlf-checkout"
            if blob_hash != expected_hash:
                raise ValueError("versioned historical byte mismatch: " + name)
            resolutions.append({"name": name, "source": "git", "path": name, "revision": revision,
                                "rendering": rendering, "sha256": blob_hash})
    scientific = json.loads((root / "results.json").read_text(encoding="utf-8"))
    if (scientific["integrity_passed"], scientific["integrity_total"], scientific["quality_passed"], scientific["quality_total"]) != (137, 137, 18, 18):
        raise ValueError("original recorded scientific totals mismatch")
    return {"audit_kind": HISTORICAL_KIND, "context_id": CONTEXT_ID, "source_revision": revision,
            "protocol_sha256": PROTOCOL_SHA256, "archive_inventory_digest": context["inventory_digest"],
            "tree_files_verified": len(actual), "counts": counts, "archive_checks": archive_checks,
            "protected_resolutions": resolutions, "original_scientific_totals": {"integrity": [137, 137], "quality": [18, 18]},
            "passed": True, "current_working_source_used": False, "model_calls": 0}


def write_new(path, value):
    path = Path(path)
    if path.exists():
        raise ValueError("refusing existing output: " + str(path))
    atomic_json(path, value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    capture = commands.add_parser("capture-current")
    capture.add_argument("--root", default="."); capture.add_argument("--output", required=True)
    audit = commands.add_parser("audit-historical")
    audit.add_argument("--run", default="outputs/insufficiency-001"); audit.add_argument("--git-root", default=".")
    audit.add_argument("--context", default=str(CONTEXT_PATH)); audit.add_argument("--source-revision")
    audit.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.command == "capture-current":
            context = current.capture_current(args.root)
            write_new(args.output, context)
            current.verify_current(context, args.root)
            print(json.dumps({"kind": context["kind"], "files": len(context["files"]), "sha256": current.file_hash(args.output)}))
        else:
            if Path(args.output).resolve().is_relative_to(Path(args.run).resolve()):
                raise ValueError("audit output must be outside original archive")
            context = json.loads(Path(args.context).read_text(encoding="utf-8"))
            result = audit_historical(args.run, args.git_root, context, args.source_revision)
            result["context_sha256"] = current.file_hash(args.context)
            write_new(args.output, result)
            print(json.dumps({"passed": result["passed"], **result["counts"], "tree_files": result["tree_files_verified"],
                              "context_sha256": result["context_sha256"]}))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}))
        return 1
    return 0


if __name__ == "__main__": raise SystemExit(main())
