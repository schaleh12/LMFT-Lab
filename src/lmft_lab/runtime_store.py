"""Local single-writer storage. Checkpoint replacement is the cycle commit point."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import time
import uuid

from .local_models import strict_json


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    allow_nan=False).encode("utf-8")).hexdigest()


@contextmanager
def locked(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+b")
    handle.seek(0)
    if os.fstat(handle.fileno()).st_size == 0:
        handle.write(b"0")
        handle.flush()
    handle.seek(0)
    try:
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        raise RuntimeError("Individual is running or interface is busy; retry after halt/boundary.") from None
    try:
        yield
    finally:
        handle.seek(0)
        if os.name == "nt":
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(handle, fcntl.LOCK_UN)
        handle.close()


def retry_sharing(operation):
    """Windows can briefly deny open/replace during a concurrent checkpoint read.

    Retry only PermissionError for at most 0.5 seconds; never hide corrupt data.
    """
    for attempt in range(21):
        try:
            return operation()
        except PermissionError:
            if attempt == 20:
                raise
            time.sleep(0.025)


def atomic_json(path, value, fault=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".partial")
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, allow_nan=False)
        stream.flush()
        os.fsync(stream.fileno())
    if fault:
        fault("before_replace")
    retry_sharing(lambda: os.replace(temporary, path))
    if fault:
        fault("after_replace")


class Store:
    def __init__(self, root):
        self.root = Path(root)

    def read(self):
        record = strict_json(retry_sharing(lambda: (self.root / "checkpoint.json").read_text(encoding="utf-8")))
        if set(record) != {"sha256", "state"} or digest(record["state"]) != record["sha256"]:
            raise ValueError("Checkpoint checksum mismatch; refusing recovery.")
        if record["state"].get("schema_version") != 1:
            raise ValueError("Unsupported checkpoint; explicit migration required.")
        return record["state"]

    def commit(self, state, fault=None):
        atomic_json(self.root / "checkpoint.json", {"sha256": digest(state), "state": state}, fault)

    def submit(self, message):
        # Queue publication is separate from scientific acceptance.
        with locked(self.root / "queue.lock"):
            if not (self.root / "checkpoint.json").exists():
                raise ValueError("Start a new individual before submitting.")
            inbox = self.root / "inbox"
            inbox.mkdir(exist_ok=True)
            sequence = max((int(p.stem) for p in inbox.glob("[0-9]*.json")), default=0) + 1
            atomic_json(inbox / f"{sequence:012d}.json", message)
        return {"lifecycle": "queued", "sequence": sequence, "message_id": message["id"]}

    def next_input(self, cursor):
        inbox = self.root / "inbox"
        files = sorted(p for p in inbox.glob("[0-9]*.json") if int(p.stem) > cursor)
        if not files:
            return None
        path = files[0]
        # Bounded publication format; malformed bytes are retained, never silently removed.
        raw = path.read_bytes()
        if len(raw) > 32000:
            return int(path.stem), None, "oversized inbox record", hashlib.sha256(raw).hexdigest()
        try:
            return int(path.stem), strict_json(raw.decode("utf-8-sig")), None, raw.decode("utf-8-sig")
        except (ValueError, UnicodeError):
            return int(path.stem), None, "malformed inbox JSON", raw.hex()

    def receive(self, after=0):
        if type(after) is not int or after < 0:
            raise ValueError("after must be a nonnegative outbox sequence")
        return [m for m in self.read()["outbox"] if m["sequence"] > after]

    def inspect(self):
        with locked(self.root / "runtime.lock"):
            return self.read()

    def stop(self):
        if not (self.root / "checkpoint.json").exists():
            raise ValueError("Unknown individual")
        atomic_json(self.root / "stop.json", {"requested_at": time.time()})
        return {"lifecycle": "stop_requested", "scope": "finish active cycle; leave queued inputs for restart"}
