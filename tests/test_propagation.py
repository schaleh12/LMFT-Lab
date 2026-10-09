"""Synthetic wiring fixtures: these edges make no claims about concept meaning."""

from dataclasses import asdict, replace

import pytest

from lmft_lab.birth import create_birth_state
from lmft_lab.propagation import Association, PropagationConfig, propagate_activation


# Existing records are just addresses A/B/C for numerical tests.
A, B, C = "cultural", "philosophical", "experiential"


def edge(name, source, target, weight=1.0, **kwargs):
    return Association(name, source, target, weight, 0.1, 0.5,
                       "synthetic-wiring-1", "synthetic-wiring-1", **kwargs)


@pytest.fixture
def state():
    return create_birth_state("test", birth_event_id="birth", random_seed=42)


def run(state, memberships, edges=(), config=PropagationConfig()):
    return propagate_activation(state, memberships, edges, event_id="input",
                                source_instance="synthetic-input-1",
                                relationship_source="synthetic-wiring-1", config=config)


def test_chain_uses_previous_pass_and_preserves_state(state):
    before = asdict(state)
    edges = (edge("ab", A, B), edge("bc", B, C))
    result = run(state, {A: 0.8}, edges)
    first = {e.node_id: e.activation for e in result.passes[0]}
    assert first[B] == pytest.approx(0.2)
    assert first[C] == 0
    assert result.activations[C] == pytest.approx(0.05)
    assert result.activations[B] == pytest.approx(0.2)
    assert result.activations[A] == 0.8
    assert asdict(state) == before
    assert result == run(state, {A: 0.8}, tuple(reversed(edges)))
    assert "synthetic-wiring-1" in result.format_trace()
    c_trace = next(e for e in result.passes[1] if e.node_id == C)
    assert c_trace.contributions[0].relationship_id == "bc"
    assert c_trace.contributions[0].source_activation == pytest.approx(0.2)


def test_no_implicit_hierarchy_edges(state):
    result = run(state, {"philosophical/being/agency": 0.8})
    assert result.activations["philosophical/being"] == 0
    assert sum(result.activations.values()) == 0.8


def test_cycle_is_bounded_and_direct_is_not_accumulated(state):
    result = run(state, {A: 0.8}, (edge("ab", A, B), edge("ba", B, A)))
    assert len(result.passes) == 2
    assert result.activations[A] == pytest.approx(0.85)
    assert result.activations[B] == pytest.approx(0.2)


def test_signed_inputs_are_summed_before_clamping(state):
    edges = (edge("ab", A, B, 1), edge("cb", C, B, -1))
    result = run(state, {A: 1, B: 0.9, C: 1}, edges, PropagationConfig(1, 1))
    assert result.activations[B] == pytest.approx(0.9)
    assert run(state, {A: 1, B: 0.9}, edges[:1]).activations[B] == 1
    assert run(state, {C: 1, B: 0.1}, edges[1:]).activations[B] == 0


def test_inactive_and_zero_passes_and_zero_gain(state):
    edges = (edge("ab", A, B, active=False),)
    assert run(state, {A: 1}, edges).activations[B] == 0
    for config in (PropagationConfig(0), PropagationConfig(2, 0)):
        result = run(state, {A: 1}, (edge("ab", A, B),), config)
        assert result.activations[B] == 0
        assert result.activations[A] == 1


def test_new_input_has_no_residual_activation(state):
    edges = (edge("ab", A, B),)
    first = run(state, {A: 1}, edges)
    assert all(v == 0 for v in run(state, {}, edges).activations.values())
    assert first.activations[B] == 0.25
    view = first.activations
    view[B] = 1
    assert first.activations[B] == 0.25


@pytest.mark.parametrize("edges", [
    (edge("bad", "missing", B),),
    (edge("bad", A, "missing"),),
    (edge("dup", A, B), edge("dup", B, C)),
    (edge("one", A, B), edge("two", A, B)),
    ("not an association",), [],
])
def test_invalid_edges_rejected_without_state_changes(state, edges):
    before = asdict(state)
    with pytest.raises(ValueError):
        run(state, {A: 1}, edges)
    assert asdict(state) == before


@pytest.mark.parametrize("change", [
    {"weight": float("nan")}, {"weight": float("inf")}, {"weight": -1.1},
    {"weight": 1.1}, {"weight": True}, {"confidence": -0.1},
    {"plasticity": 1.1}, {"active": 1}, {"kind": "inhibition"},
    {"created_event_id": ""}, {"id": " "},
])
def test_relationship_validation(change):
    with pytest.raises(ValueError):
        replace(edge("test", A, B), **change)


@pytest.mark.parametrize("passes,gain", [(-1, .25), (101, .25), (True, .25),
                                        (1.5, .25), (2, -1), (2, float("nan")),
                                        (2, float("inf")), (2, True), (2, 2)])
def test_config_validation(passes, gain):
    with pytest.raises(ValueError):
        PropagationConfig(passes, gain)
