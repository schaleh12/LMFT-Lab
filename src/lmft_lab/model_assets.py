"""Pinned local assets; no credentials or downloaded bytes belong in Git."""
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import tempfile
import urllib.error
import urllib.request
import zipfile

BACKEND_VERSION = "b11429"
BACKEND_FILES = {
    "llama-b11429-bin-win-cuda-12.4-x64.zip":
        "dd6df685c1024e6aa55ca55ad35038692d5e284d4dc895e7a646c3245d3d14ff",
    "cudart-llama-bin-win-cuda-12.4-x64.zip":
        "8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6",
}


class ModelError(RuntimeError):
    """A bounded, user-visible asset, backend, or model failure."""


@dataclass(frozen=True)
class ModelSpec:
    repo_id: str
    revision: str
    filename: str
    sha256: str

    def __post_init__(self):
        if not re.fullmatch(r"[\w-]+/[\w.-]+", self.repo_id):
            raise ValueError("model repo_id must be owner/repository")
        if not re.fullmatch(r"[a-f0-9]{40}", self.revision):
            raise ValueError("pin revision to a full Hugging Face commit SHA")
        if not re.fullmatch(r"[\w.-]+\.gguf", self.filename) or ".." in self.filename:
            raise ValueError("model filename must be a single GGUF file")
        if not re.fullmatch(r"[a-f0-9]{64}", self.sha256):
            raise ValueError("model SHA256 is required")


def cache_root():
    override = os.environ.get("LMFT_CACHE_DIR")
    if override:
        return Path(override).expanduser().resolve()
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".cache"))
    return base / "LMFT-Lab" / "cache"


def digest_file(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is not None:
            # HF/CDN signed redirects need no bearer credential.
            redirected.remove_header("Authorization")
        return redirected


def fetch_verified(url, destination, sha256, *, offline=False, token=None):
    """Verify cached content each time; atomic placement after complete download.

    An interrupted download never becomes a valid cache entry. Retries are
    explicit: rerun the command. No request occurs in offline mode.
    """
    destination = Path(destination)
    if destination.exists():
        if digest_file(destination) != sha256:
            raise ModelError(f"Cached asset failed SHA256 verification: {destination}")
        return destination
    if offline:
        raise ModelError(f"Offline cache miss: {destination}. Run once online first.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "LMFT-Lab/local-models-1"}
    if token:
        headers["Authorization"] = "Bearer " + token
    partial = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".partial",
                                         delete=False) as out:
            partial = Path(out.name)
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.build_opener(_SafeRedirect()).open(request, timeout=60) as response:
                while block := response.read(1024 * 1024):
                    out.write(block)
            out.flush()
            os.fsync(out.fileno())
        if digest_file(partial) != sha256:
            raise ModelError("Downloaded asset failed SHA256 verification; not installed.")
        os.replace(partial, destination)
        return destination
    except urllib.error.HTTPError as exc:
        raise ModelError(f"Asset download HTTP {exc.code}; for gated HF models check HF_TOKEN/access.") from None
    except (OSError, urllib.error.URLError) as exc:
        # Do not leak authorization headers, URLs with signatures, or token values.
        raise ModelError(f"Asset download failed ({type(exc).__name__}); rerun to retry.") from None
    finally:
        if partial is not None:
            partial.unlink(missing_ok=True)


def ensure_model(spec, root, *, offline=False):
    target = Path(root) / "models" / spec.repo_id.replace("/", "--") / spec.revision / spec.filename
    return fetch_verified(
        f"https://huggingface.co/{spec.repo_id}/resolve/{spec.revision}/{spec.filename}",
        target, spec.sha256, offline=offline, token=os.environ.get("HF_TOKEN"))


def ensure_backend(root, *, offline=False):
    """Official prebuilt CUDA 12.4 Windows x64 backend, no compiler required."""
    if os.name != "nt":
        raise ModelError("The bundled backend is Windows x64 only.")
    root = Path(root) / "backend" / BACKEND_VERSION
    install = root / "bin"
    install.mkdir(parents=True, exist_ok=True)
    for filename, checksum in BACKEND_FILES.items():
        archive = fetch_verified(
            f"https://github.com/ggml-org/llama.cpp/releases/download/{BACKEND_VERSION}/{filename}",
            root / filename, checksum, offline=offline)
        with zipfile.ZipFile(archive) as z:
            for item in z.infolist():
                target = (install / item.filename).resolve()
                if not target.is_relative_to(install.resolve()):
                    raise ModelError("Unsafe backend archive member.")
                if item.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                # Compare extracted assets with the verified archive, including on offline runs.
                content = z.read(item)
                if target.exists() and digest_file(target) == hashlib.sha256(content).hexdigest():
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
    candidates = list(install.rglob("llama-server.exe"))
    if len(candidates) != 1:
        raise ModelError("Pinned backend archive did not contain exactly one llama-server.exe.")
    return candidates[0]
