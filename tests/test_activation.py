"""Direct-input mechanics, not evidence of semantic understanding."""

from dataclasses import FrozenInstanceError, asdict

import pytest

from lmft_lab.activation import activate_direct
from lmft_lab.birth import create_birth_state


AGENCY = "philosophical/being/agency"
EXISTENCE = "philosophical/being/existence"


@pytest.fixture
def state():
    return create_birth_state("seed-a", birth_event_id="birth-a", random_seed=42)


def inspect(state, memberships, event_id="input-1"):
    return activate_direct(state, memberships, event_id=event_id,
                           source_instance="mechanical-fixture-1")


def test_direct_values_no_propagation_and_no_persistent_change(state):
    before = asdict(state)
    frame = inspect(state, {AGENCY: 0.8, EXISTENCE: 0.3})
    values = {entry.node_id: entry.activation for entry in frame.entries}
    assert len(values) == 40
    assert values[AGENCY] == 0.8
    assert values[EXISTENCE] == 0.3
    assert all(value == 0 for key, value in values.items()
               if key not in (AGENCY, EXISTENCE))
    assert asdict(state) == before
    assert frame.individual_id == state.individual_id
    assert frame.birth_event_id == state.birth_event_id
    assert frame.source == "developer"


def test_new_input_replaces_activation_without_altering_previous_trace(state):
    first = inspect(state, {AGENCY: 0.8, EXISTENCE: 0.3})
    second = inspect(state, {EXISTENCE: 0.1}, event_id="input-2")
    assert next(e.activation for e in second.entries if e.node_id == AGENCY) == 0
    assert next(e.activation for e in first.entries if e.node_id == AGENCY) == 0.8
    assert all(e.activation == 0 for e in inspect(state, {}).entries)


def test_input_is_copied_and_order_does_not_affect_result(state):
    supplied = {AGENCY: 0.8, EXISTENCE: 0.3}
    frame = inspect(state, supplied)
    assert frame == inspect(state, dict(reversed(list(supplied.items()))))
    supplied[AGENCY] = 0
    assert next(e.activation for e in frame.entries if e.node_id == AGENCY) == 0.8
    with pytest.raises(FrozenInstanceError):
        frame.entries[0].activation = 1


def test_trace_distinguishes_explicit_zero_from_missing_input(state):
    frame = inspect(state, {AGENCY: 0, EXISTENCE: 1})
    trace = frame.format_trace()
    assert f"{AGENCY}: 0 (supplied membership 0)" in trace
    assert f"{EXISTENCE}: 1 (supplied membership 1)" in trace
    assert "philosophical/being: 0 (omitted -> zero)" in trace
    assert "mechanical-fixture-1" in trace


@pytest.mark.parametrize("value", [-0.1, 1.1, float("nan"), float("inf"),
                                  float("-inf"), True, "0.8", None, 10**400])
def test_invalid_memberships_leave_state_unchanged(state, value):
    before = asdict(state)
    with pytest.raises(ValueError):
        inspect(state, {EXISTENCE: 0.3, AGENCY: value})
    assert asdict(state) == before


@pytest.mark.parametrize("memberships", [{"missing": 0.5}, {"Agency": 0.8}, [], None])
def test_invalid_references_and_payloads(state, memberships):
    with pytest.raises(ValueError):
        inspect(state, memberships)


@pytest.mark.parametrize("event_id", ["", " ", "birth-a", None])
def test_invalid_input_identity(state, event_id):
    with pytest.raises(ValueError):
        inspect(state, {}, event_id=event_id)


def test_source_identity_is_required(state):
    with pytest.raises(ValueError):
        activate_direct(state, {}, event_id="input-1", source_instance="")
