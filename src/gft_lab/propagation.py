"""Bounded synchronous activation over explicitly supplied associations."""

from collections.abc import Mapping
from dataclasses import dataclass
from math import fsum, isfinite

from gft_lab.activation import ActivationFrame, activate_direct
from gft_lab.birth import BirthState


def _text(name, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")


def _bounded(name, value, lower=0):
    if (type(value) not in (int, float) or not lower <= value <= 1
            or not isfinite(value)):
        raise ValueError(f"{name} must be finite in [{lower}, 1]")


@dataclass(frozen=True)
class Association:
    """A directed, authored relationship; no learning or semantic inference."""

    id: str
    source_id: str
    target_id: str
    weight: float
    confidence: float
    plasticity: float
    created_event_id: str
    last_updated_event_id: str
    active: bool = True
    kind: str = "association"

    def __post_init__(self):
        for name in ("id", "source_id", "target_id", "created_event_id",
                     "last_updated_event_id"):
            _text(name, getattr(self, name))
        _bounded("weight", self.weight, -1)
        _bounded("confidence", self.confidence)
        _bounded("plasticity", self.plasticity)
        if type(self.active) is not bool or self.kind != "association":
            raise ValueError("only association records with boolean active are supported")


@dataclass(frozen=True)
class PropagationConfig:
    passes: int = 2
    gain: float = 0.25

    def __post_init__(self):
        # Diagnostic resource guard, not a proposed property of GFT cognition.
        if type(self.passes) is not int or not 0 <= self.passes <= 100:
            raise ValueError("passes must be an integer in [0, 100]")
        _bounded("gain", self.gain)


@dataclass(frozen=True)
class Contribution:
    relationship_id: str
    source_activation: float
    weighted_input: float


@dataclass(frozen=True)
class PropagationEntry:
    node_id: str
    direct: float
    contributions: tuple[Contribution, ...]
    incoming: float
    unclamped: float
    activation: float


@dataclass(frozen=True)
class PropagationResult:
    direct_frame: ActivationFrame
    relationships: tuple[Association, ...]
    config: PropagationConfig
    relationship_source: str
    passes: tuple[tuple[PropagationEntry, ...], ...]
    rule_version: str = "synchronous-association-1"

    @property
    def activations(self) -> dict[str, float]:
        entries = self.passes[-1] if self.passes else self.direct_frame.entries
        return {entry.node_id: entry.activation for entry in entries}

    def format_trace(self) -> str:
        lines = [self.direct_frame.format_trace(),
                 f"Propagation {self.rule_version}: {self.config.passes} passes, "
                 f"gain {self.config.gain:g}; source: {self.relationship_source}"]
        for edge in self.relationships:
            lines.append(f"{edge.id}: {edge.source_id} -> {edge.target_id}; "
                         f"weight={edge.weight:g}, active={edge.active}; "
                         f"created={edge.created_event_id}, updated={edge.last_updated_event_id}")
        for number, entries in enumerate(self.passes, 1):
            lines.append(f"Pass {number}")
            for entry in entries:
                terms = ", ".join(
                    f"{c.relationship_id}: source={c.source_activation:g}, "
                    f"weighted={c.weighted_input:g}" for c in entry.contributions
                ) or "none"
                lines.append(f"{entry.node_id}: direct={entry.direct:g}, incoming={entry.incoming:g}, "
                             f"unclamped={entry.unclamped:g}, activation={entry.activation:g}; "
                             f"inputs=[{terms}]")
        lines.append("No persistent state or relationship changes.")
        return "\n".join(lines)


def propagate_activation(
    state: BirthState,
    proposed_memberships: Mapping[str, float],
    relationships: tuple[Association, ...],
    *,
    event_id: str,
    source_instance: str,
    relationship_source: str,
    config: PropagationConfig = PropagationConfig(),
) -> PropagationResult:
    """Apply Runtime 9.2 without inferring edges from genealogy or labels.

    Start at direct activation. Every pass reads only the previous pass, retains
    the original direct term, then clamps once after summing signed inputs.
    Confidence and plasticity are recorded but do not weight this formula.
    """
    _text("relationship_source", relationship_source)
    if not isinstance(config, PropagationConfig):
        raise ValueError("config must be PropagationConfig")
    config.__post_init__()
    direct_frame = activate_direct(state, proposed_memberships, event_id=event_id,
                                   source_instance=source_instance)
    if not isinstance(relationships, tuple):
        raise ValueError("relationships must be an immutable tuple")
    known = {n.id for n in state.nodes}
    seen = set()
    pairs = set()
    for edge in relationships:
        if not isinstance(edge, Association):
            raise ValueError("relationships must contain Association records")
        edge.__post_init__()
        if edge.source_id not in known or edge.target_id not in known:
            raise ValueError(f"unknown relationship endpoint: {edge.id}")
        pair = (edge.source_id, edge.target_id)
        if edge.id in seen or pair in pairs:
            raise ValueError("duplicate relationship ID or directed pair")
        seen.add(edge.id)
        pairs.add(pair)
    edges = tuple(sorted(relationships, key=lambda e: e.id))
    incoming_edges = {node_id: [] for node_id in sorted(known)}
    for edge in edges:
        if edge.active:
            incoming_edges[edge.target_id].append(edge)
    direct = {e.node_id: e.activation for e in direct_frame.entries}
    previous = direct.copy()
    passes = []
    for _ in range(config.passes):
        entries = []
        for node_id, incoming in incoming_edges.items():
            contributions = tuple(
                Contribution(e.id, previous[e.source_id], previous[e.source_id] * e.weight)
                for e in incoming
            )
            total = fsum(c.weighted_input for c in contributions)
            raw = direct[node_id] + config.gain * total
            entries.append(PropagationEntry(node_id, direct[node_id], contributions,
                                            total, raw, min(1.0, max(0.0, raw))))
        passes.append(tuple(entries))
        previous = {e.node_id: e.activation for e in entries}
    return PropagationResult(direct_frame, edges, config, relationship_source, tuple(passes))
