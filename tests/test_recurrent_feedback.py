"""Unit tests for Recurrent Post-Action Echo Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
from lmft_lab.recurrent_feedback import (
    EXPERIENTIAL_LEAF_IDS,
    CANONICAL_LEAF_IDS,
    RecurrentFeedbackEngine,
    OrdinaryMemoryRecurrentComparator,
)


def test_canonical_seed_integrity():
    """All 6 Experiential leaves strictly exist in the frozen founding seed (Rule D001)."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    assert len(inventory_leaf_ids) == 24

    for leaf_id in EXPERIENTIAL_LEAF_IDS:
        assert leaf_id in inventory_leaf_ids


def test_decisive_action_resolves_arousal():
    """Decisive action damps arousal (-0.15) and elevates valence (+0.12)."""
    engine = RecurrentFeedbackEngine()
    psy = {
        "psychological/will/intention": 0.85,
        "psychological/will/execution": 0.80,
        "psychological/contemplation/clarity": 0.90,
    }
    exp = {"experiential/phase/arousal": 0.60, "experiential/phase/valence": 0.50}

    res = engine.compute_echo(experiential_dials=exp, psychological_state=psy, action_posture="Noble Resolute Action")

    assert res["arousal_damped"] is True
    assert res["valence_reinforced"] is True
    assert res["echoed_experiential"]["experiential/phase/arousal"] == 0.45
    assert res["echoed_experiential"]["experiential/phase/valence"] == 0.62
    assert res["echoed_experiential"]["experiential/synchronization/resonance"] == 0.65


def test_honest_silence_echo():
    """Honest silence/abstention calms arousal while keeping salience for future investigation."""
    engine = RecurrentFeedbackEngine()
    exp = {"experiential/phase/arousal": 0.50, "experiential/reflection/salience": 0.30}

    res = engine.compute_echo(experiential_dials=exp, action_posture="Neutral Observant Silence (Honest Abstention)")

    assert res["arousal_damped"] is True
    assert res["echoed_experiential"]["experiential/phase/arousal"] == 0.40
    assert res["echoed_experiential"]["experiential/reflection/salience"] == 0.40


def test_cognitive_conflict_spikes_alertness():
    """Conflict or low clarity heightens arousal (+0.15) and spikes salience (+0.25)."""
    engine = RecurrentFeedbackEngine()
    psy = {
        "psychological/contemplation/clarity": 0.15,
        "psychological/contemplation/confidence": 0.20,
    }
    exp = {"experiential/phase/arousal": 0.40, "experiential/reflection/salience": 0.30}

    res = engine.compute_echo(experiential_dials=exp, psychological_state=psy, action_posture="Cognitive Dissonance")

    assert res["echo_deltas"]["experiential/phase/arousal"] == 0.15
    assert res["echo_deltas"]["experiential/reflection/salience"] == 0.25
    assert res["echoed_experiential"]["experiential/phase/arousal"] == 0.55
    assert res["echoed_experiential"]["experiential/reflection/salience"] == 0.55


def test_bound_enforcement_extremes():
    """Boundary conditions strictly respect [0.0, 1.0]."""
    engine = RecurrentFeedbackEngine()
    exp_high = {k: 0.98 for k in EXPERIENTIAL_LEAF_IDS}
    exp_low = {k: 0.02 for k in EXPERIENTIAL_LEAF_IDS}

    res_high = engine.compute_echo(experiential_dials=exp_high, action_posture="Cognitive Dissonance")
    res_low = engine.compute_echo(experiential_dials=exp_low, action_posture="Noble Resolute Action")

    for v in res_high["echoed_experiential"].values():
        assert 0.0 <= v <= 1.0
    for v in res_low["echoed_experiential"].values():
        assert 0.0 <= v <= 1.0


def test_ordinary_memory_comparator_parity():
    """Primary engine and matched ordinary memory baseline achieve byte-for-byte digest parity (Rule D004)."""
    engine = RecurrentFeedbackEngine()
    comparator = OrdinaryMemoryRecurrentComparator()

    configs = [
        ("Noble Resolute Action", {"psychological/will/intention": 0.80, "psychological/will/execution": 0.75, "psychological/contemplation/clarity": 0.85}),
        ("Neutral Observant Silence", {}),
        ("Cognitive Conflict", {"psychological/contemplation/clarity": 0.10}),
        ("Equilibrated Synthesis", {"psychological/will/intention": 0.50, "psychological/will/execution": 0.50, "psychological/contemplation/clarity": 0.60}),
    ]

    for posture, psy in configs:
        p_res = engine.compute_echo(action_posture=posture, psychological_state=psy)
        c_res = comparator.compute_echo(action_posture=posture, psychological_state=psy)
        assert digest(p_res) == digest(c_res)
