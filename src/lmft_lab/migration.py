"""Explicit conversion of historical structural birth records; no file writes."""

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from types import MappingProxyType

from .birth import BirthState, SEED_VERSION, create_birth_state


LEGACY_SEED_VERSION = "minimal-v0.1-seed-1"
LEGACY_ID_MAP = MappingProxyType({
    "psychological/discipline": "psychological/contemplation",
    "psychological/discipline/clarity": "psychological/contemplation/clarity",
    "psychological/discipline/confidence": "psychological/contemplation/confidence",
})


@dataclass(frozen=True)
class SeedMigration:
    state: BirthState
    source_seed_version: str = LEGACY_SEED_VERSION
    target_seed_version: str = SEED_VERSION
    rule_version: str = "discipline-to-contemplation-1"
    renamed_ids: tuple[tuple[str, str], ...] = tuple(LEGACY_ID_MAP.items())


def migrate_legacy_birth_record(record: Mapping) -> SeedMigration:
    """Convert an asdict/JSON-shaped neutral birth record, leaving it untouched.

    Exact schema and value validation deliberately rejects developed states,
    mixed-version IDs, unknown fields, and altered historical seed inventories.
    Associated evidence, traces, or edges are not silently rewritten.
    """
    if not isinstance(record, Mapping):
        raise ValueError("expected a historical birth record")
    if record.get("seed_version") != LEGACY_SEED_VERSION:
        raise ValueError("unsupported source seed version")
    try:
        state = create_birth_state(record["individual_id"],
                                   birth_event_id=record["birth_event_id"],
                                   random_seed=record["random_seed"])
    except (KeyError, TypeError) as exc:
        raise ValueError("invalid historical birth metadata") from exc
    expected = asdict(state)
    expected["seed_version"] = LEGACY_SEED_VERSION
    reverse = {new: old for old, new in LEGACY_ID_MAP.items()}
    for node in expected["nodes"]:
        node["id"] = reverse.get(node["id"], node["id"])
        node["parent_id"] = reverse.get(node["parent_id"], node["parent_id"])
        if node["label"] == "Contemplation":
            node["label"] = "Discipline"

    def matches(actual, reference):
        if isinstance(reference, dict):
            return (isinstance(actual, Mapping) and actual.keys() == reference.keys()
                    and all(matches(actual[k], v) for k, v in reference.items()))
        if isinstance(reference, tuple):
            return (type(actual) in (tuple, list) and len(actual) == len(reference)
                    and all(matches(a, b) for a, b in zip(actual, reference)))
        return type(actual) is type(reference) and actual == reference

    if not matches(record, expected):
        raise ValueError("record does not match the complete historical birth schema")
    return SeedMigration(state)
