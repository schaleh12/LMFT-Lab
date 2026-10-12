"""New synthetic device; does not change the historical capacity procedure."""
from .capacity_fixture import execute as bounded_write

PROCEDURE = "capacity-blocked-two-1"
SOURCE = "registered-insufficiency-1"
TRAIN = {
    "unsupported": {"t1": (1, 3), "t2": (4, 2), "t3": (2, 4), "t4": (3, 3)},
    "supported": {"t1": (1, 3), "t2": (4, 2), "t3": (3, 3), "t4": (5, 1)},
    "ambiguous": {"t1": (1, 3), "t2": (4, 2), "t3": (3, 5), "t4": (5, 1)},
}
VALIDATION = {"v1": (0, 3), "v2": (3, 6), "v3": (6, 1), "v4": (7, 4)}
HELD = {"h1": (1, 1), "h2": (2, 2), "h3": (4, 4), "h4": (6, 6),
        "h5": (2, 5), "h6": (1, 4), "h7": (6, 3), "h8": (8, 7), "x1": (9, 8)}
FIELDS = {"evidence_id", "scenario", "split", "procedure", "length", "capacity", "success"}


def execute(length, capacity):
    """Known synthetic device fault: length-two payloads are refused."""
    return False if length == 2 else bounded_write(length, capacity)


def table(scenario, split):
    return TRAIN[scenario] if split == "train" else VALIDATION if split == "validation" else {}


def outcome(scenario, identifier, split):
    length, capacity = table(scenario, split)[identifier]
    return {"evidence_id": identifier, "scenario": scenario, "split": split,
            "procedure": PROCEDURE, "length": length, "capacity": capacity,
            "success": execute(length, capacity)}


def registered(record, scenario):
    """Reject eligibility errors without executing device truth."""
    if not isinstance(record, dict) or set(record) != FIELDS:
        return False
    if any(not isinstance(record[k], str) for k in ("evidence_id", "scenario", "split", "procedure")):
        return False
    if record["scenario"] != scenario or record["procedure"] != PROCEDURE:
        return False
    if record["split"] not in ("train", "validation") or record["evidence_id"] not in table(scenario, record["split"]):
        return False
    if type(record["success"]) is not bool or any(type(record[k]) is not int for k in ("length", "capacity")):
        return False
    return (record["length"], record["capacity"]) == table(scenario, record["split"])[record["evidence_id"]]


def verify(record, scenario):
    return registered(record, scenario) and record["success"] == execute(record["length"], record["capacity"])
