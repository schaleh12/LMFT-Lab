"""Structural birth checks, without claiming developmental behavior."""

from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import re

import pytest

from gft_lab.birth import InitialValues, create_birth_state


def newborn():
    return create_birth_state("individual-a", birth_event_id="birth-a", random_seed=42)


def test_seed_matches_controlling_document():
    spec = (Path(__file__).resolve().parents[1] / "docs" / "MINIMAL_GFT_SPEC.md")
    diagram = spec.read_text(encoding="utf-8").split("GFT V0.1 SEED GEOMETRY", 1)[1]
    diagram = diagram.split("```", 1)[0]
    expected = []
    parents = {}
    for line in diagram.splitlines():
        match = re.search(r"[├└]── (.+)", line)
        if match:
            depth = match.start() // 4
            label = match.group(1)
            expected.append((label, parents.get(depth - 1), depth))
            parents[depth] = label
    state = newborn()
    labels = {node.id: node.label for node in state.nodes}
    assert [(n.label, labels.get(n.parent_id), n.depth) for n in state.nodes] == expected
    assert len(state.nodes) == len({n.id for n in state.nodes}) == 40
    assert [sum(n.depth == d for n in state.nodes) for d in range(3)] == [4, 12, 24]


def test_determinism_provenance_and_individual_isolation():
    first, second = newborn(), newborn()
    assert first == second
    assert first.nodes[0] is not second.nodes[0]
    assert first.random_seed == 42
    assert all(n.created_event_id == n.last_updated_event_id == "birth-a"
               for n in first.nodes)
    assert all(n.values == InitialValues() for n in first.nodes)
    assert replace(first, random_seed=7).nodes == first.nodes
    with pytest.raises(FrozenInstanceError):
        first.nodes[0].label = "changed"


@pytest.mark.parametrize("field", ["baseline", "activation", "salience", "confidence",
                                  "plasticity", "retention"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -1.01, 1.01, True, "0.1"])
def test_invalid_numbers_are_rejected(field, value):
    with pytest.raises(ValueError):
        InitialValues(**{field: value})


def test_numeric_boundaries():
    assert InitialValues(baseline=-1).baseline == -1
    for value in (0, 1):
        InitialValues(value, value, value, value, value, value)
    with pytest.raises(ValueError):
        InitialValues(activation=-0.1)


@pytest.mark.parametrize("change", [
    {"parent_id": "missing"}, {"parent_id": "cultural/efficiency"},
    {"id": "duplicate"}, {"depth": 2}, {"domain": "derived"},
    {"last_updated_event_id": "unknown"}, {"active": False},
    {"values": InitialValues(baseline=0.2)},
])
def test_altered_seed_records_are_rejected(change):
    state = newborn()
    with pytest.raises(ValueError):
        replace(state, nodes=(replace(state.nodes[0], **change),) + state.nodes[1:])


def test_missing_and_duplicate_nodes_are_rejected():
    state = newborn()
    for nodes in (state.nodes[:-1], (state.nodes[1],) + state.nodes[1:]):
        with pytest.raises(ValueError):
            replace(state, nodes=nodes)


@pytest.mark.parametrize("change", [{"individual_id": " "}, {"birth_event_id": ""},
                                   {"random_seed": True}, {"version": 1}])
def test_invalid_birth_metadata(change):
    with pytest.raises(ValueError):
        replace(newborn(), **change)
