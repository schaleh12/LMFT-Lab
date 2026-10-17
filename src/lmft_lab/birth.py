"""Deterministic, in-memory seed construction; not a complete runtime birth."""

from dataclasses import dataclass, fields
from math import isfinite


SEED_VERSION = "lmft-v0.1-seed-1"
INITIALIZATION_VERSION = "neutral-structural-scaffold-1"

# Minimal LMFT Specification, section 4. These labels are inspection handles.
SEED_HIERARCHY = (
    ("CULTURAL", (
        ("Efficiency", ("Power", "Wastelessness")),
        ("Justice", ("Honor", "Fairness")),
        ("Freedom", ("Self-Sufficiency", "Needlessness")),
    )),
    ("PHILOSOPHICAL", (
        ("Being", ("Agency", "Existence")),
        ("Structure", ("Order", "Chaos")),
        ("Persistence", ("Continuity", "Discreteness")),
    )),
    ("EXPERIENTIAL", (
        ("Reflection", ("Novelty", "Salience")),
        ("Phase", ("Valence", "Arousal")),
        ("Synchronization", ("Resonance", "Entrainment")),
    )),
    ("PSYCHOLOGICAL", (
        ("Will", ("Intention", "Execution")),
        ("Truth", ("Theory", "Fact")),
        ("Contemplation", ("Clarity", "Confidence")),
    )),
)


def _inventory():
    """Yield stable path IDs, labels, domains, parents, and depths."""
    for label, branches in SEED_HIERARCHY:
        domain = label.lower()
        yield domain, label, domain, None, 0
        for branch, leaves in branches:
            parent_id = f"{domain}/{branch.lower()}"
            yield parent_id, branch, domain, domain, 1
            for leaf in leaves:
                yield f"{parent_id}/{leaf.lower()}", leaf, domain, parent_id, 2


@dataclass(frozen=True)
class InitialValues:
    """Runtime section 6.2 defaults, not calibrated developmental priors."""

    baseline: float = 0.0
    activation: float = 0.0
    salience: float = 0.10
    confidence: float = 0.10
    plasticity: float = 0.50
    retention: float = 0.70

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            lower = -1.0 if field.name == "baseline" else 0.0
            if (type(value) not in (int, float) or not isfinite(value)
                    or not lower <= value <= 1.0):
                raise ValueError(f"{field.name} must be finite in [{lower}, 1]")


@dataclass(frozen=True)
class SeedNode:
    id: str
    label: str
    domain: str
    parent_id: str | None
    depth: int
    values: InitialValues
    created_event_id: str
    last_updated_event_id: str
    seeded: bool = True
    version_created: int = 0
    active: bool = True


@dataclass(frozen=True)
class BirthState:
    individual_id: str
    birth_event_id: str
    random_seed: int
    nodes: tuple[SeedNode, ...]
    seed_version: str = SEED_VERSION
    initialization_version: str = INITIALIZATION_VERSION
    version: int = 0

    def __post_init__(self):
        validate_birth_state(self)


def validate_birth_state(state: BirthState) -> None:
    """Reject incomplete, altered, or invalid structural birth records."""
    for name in ("individual_id", "birth_event_id"):
        value = getattr(state, name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a nonempty string")
    if type(state.random_seed) is not int:
        raise ValueError("random_seed must be an integer")
    if (state.seed_version != SEED_VERSION
            or state.initialization_version != INITIALIZATION_VERSION
            or type(state.version) is not int or state.version != 0):
        raise ValueError("unsupported birth version")
    expected = tuple(_inventory())
    if not isinstance(state.nodes, tuple) or len(state.nodes) != len(expected):
        raise ValueError("birth must contain the complete 40-node seed tuple")
    for node, record in zip(state.nodes, expected):
        if not isinstance(node, SeedNode):
            raise ValueError("birth contains a non-node record")
        actual = (node.id, node.label, node.domain, node.parent_id, node.depth)
        if actual != record or type(node.depth) is not int:
            raise ValueError(f"invalid seed identity, parent, depth, or order: {node.id}")
        if not isinstance(node.values, InitialValues):
            raise ValueError(f"invalid numerical state: {node.id}")
        node.values.__post_init__()
        if node.values != InitialValues():
            raise ValueError("this scaffold supports only the recorded neutral defaults")
        if (node.created_event_id != state.birth_event_id
                or node.last_updated_event_id != state.birth_event_id
                or node.seeded is not True or node.active is not True
                or type(node.version_created) is not int or node.version_created != 0):
            raise ValueError(f"invalid birth provenance or flags: {node.id}")


def create_birth_state(
    individual_id: str, *, birth_event_id: str, random_seed: int
) -> BirthState:
    """Build the approved hierarchy without randomness, timestamps, or I/O.

    IDs are caller-supplied for reproducibility. The seed is recorded but not
    consumed. No event archive, checkpoint, memberships, or cross-links exist yet.
    """
    nodes = tuple(
        SeedNode(node_id, label, domain, parent_id, depth, InitialValues(),
                 birth_event_id, birth_event_id)
        for node_id, label, domain, parent_id, depth in _inventory()
    )
    return BirthState(individual_id, birth_event_id, random_seed, nodes)
