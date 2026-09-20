"""Direct activation inspection, before the full runtime event cycle exists."""

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite

from gft_lab.birth import BirthState, validate_birth_state


@dataclass(frozen=True)
class ActivationEntry:
    node_id: str
    label: str
    proposed_membership: float | None
    activation: float


@dataclass(frozen=True)
class ActivationFrame:
    """Temporary activation and its input trace; does not mutate birth state."""

    event_id: str
    individual_id: str
    birth_event_id: str
    seed_version: str
    initialization_version: str
    state_version: int
    source_instance: str
    entries: tuple[ActivationEntry, ...]
    source: str = "developer"
    rule_version: str = "direct-only-1"

    def format_trace(self) -> str:
        """Show all nodes, including explicit zeros and omitted inputs."""
        lines = [
            f"Input {self.event_id} | individual {self.individual_id}",
            f"Source: {self.source}/{self.source_instance} | rule: {self.rule_version}",
            "Temporary direct activation; no propagation or persistent change.",
        ]
        for entry in self.entries:
            reason = ("omitted -> zero" if entry.proposed_membership is None
                      else f"supplied membership {entry.proposed_membership:g}")
            lines.append(f"{entry.node_id}: {entry.activation:g} ({reason})")
        return "\n".join(lines)


def activate_direct(
    state: BirthState,
    proposed_memberships: Mapping[str, float],
    *,
    event_id: str,
    source_instance: str,
) -> ActivationFrame:
    """Inspect one developer-authored input under runtime section 9.1.

    Each call starts from zero temporary activation. Input values must already
    be finite and in [0, 1]; invalid values are rejected rather than concealed
    by clamping. Missing membership means zero relevance, not opposition.

    This is a pure calculation, not event archival, sequencing, or learning.
    The frame records the proposed memberships; they are not stored concepts.
    """
    validate_birth_state(state)
    for name, value in (("event_id", event_id), ("source_instance", source_instance)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a nonempty string")
    if event_id == state.birth_event_id:
        raise ValueError("activation input must have a different ID from birth")
    if not isinstance(proposed_memberships, Mapping):
        raise ValueError("proposed_memberships must be a mapping")
    supplied = dict(proposed_memberships)
    known_ids = {node.id for node in state.nodes}
    for node_id, value in supplied.items():
        if node_id not in known_ids:
            raise ValueError(f"unknown node ID: {node_id!r}")
        if (type(value) not in (int, float) or not 0 <= value <= 1
                or not isfinite(value)):
            raise ValueError(f"membership for {node_id} must be finite in [0, 1]")
    entries = tuple(
        ActivationEntry(
            node.id, node.label,
            float(supplied[node.id]) if node.id in supplied else None,
            float(supplied.get(node.id, 0.0)),
        )
        for node in state.nodes
    )
    return ActivationFrame(
        event_id=event_id,
        individual_id=state.individual_id,
        birth_event_id=state.birth_event_id,
        seed_version=state.seed_version,
        initialization_version=state.initialization_version,
        state_version=state.version,
        source_instance=source_instance,
        entries=entries,
    )
