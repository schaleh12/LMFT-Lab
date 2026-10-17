"""Unit tests for Affective Plasticity Regulation Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
from lmft_lab.affective_plasticity import (
    CANONICAL_LEAF_IDS,
    EXPERIENTIAL_AFFECTIVE_LEAVES,
    PSYCHOLOGICAL_EPISTEMIC_LEAVES,
    AffectivePlasticityEngine,
    OrdinaryMemoryAffectivePlasticityComparator,
)


def test_canonical_seed_integrity():
    """All tracked leaves strictly exist in the frozen founding seed (Rule D001)."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    assert len(inventory_leaf_ids) == 24

    for leaf_id in EXPERIENTIAL_AFFECTIVE_LEAVES:
        assert leaf_id in inventory_leaf_ids
    for leaf_id in PSYCHOLOGICAL_EPISTEMIC_LEAVES:
        assert leaf_id in inventory_leaf_ids


def test_surprise_amplifies_plasticity():
    """High novelty and arousal trigger Hyper-Adaptive plasticity (alpha > 0.28)."""
    engine = AffectivePlasticityEngine()
    exp = {
        "experiential/reflection/novelty": 0.95,
        "experiential/phase/arousal": 0.90,
    }
    psy = {
        "psychological/contemplation/clarity": 0.20,
        "psychological/contemplation/confidence": 0.20,
    }
    rates = engine.compute_dynamic_rates(exp, psy)

    assert rates["surprise_factor"] > 0.90
    assert rates["mastery_factor"] == 0.20
    assert rates["dynamic_alpha"] > 0.28
    assert rates["plasticity_regime"] == "Hyper-Adaptive (Surprise / Disruption)"

    # Reinforcement step with elevated alpha adapts faster
    res = engine.update_rule_weight(0.50, "reinforce", exp, psy)
    assert res["new_weight"] > 0.60


def test_mastery_protects_established_rules():
    """High clarity and confidence throttle plasticity down (alpha < 0.15) to prevent noise drift."""
    engine = AffectivePlasticityEngine()
    exp = {
        "experiential/reflection/novelty": 0.10,
        "experiential/phase/arousal": 0.10,
    }
    psy = {
        "psychological/contemplation/clarity": 0.95,
        "psychological/contemplation/confidence": 0.95,
    }
    rates = engine.compute_dynamic_rates(exp, psy)

    assert rates["mastery_factor"] == 0.95
    assert rates["dynamic_alpha"] < 0.15
    assert rates["plasticity_regime"] == "Protected Mastery (Habituation / Stability)"

    res = engine.update_rule_weight(0.50, "reinforce", exp, psy)
    # With throttled alpha, delta is gentle
    assert res["new_weight"] < 0.55


def test_retention_slows_habituation_decay():
    """High retention and positive valence slow down forgetting (lambda < 0.035)."""
    engine = AffectivePlasticityEngine()
    exp_high_ret = {
        "experiential/phase/valence": 0.90,
        "experiential/synchronization/entrainment": 0.95,
    }
    exp_low_ret = {
        "experiential/phase/valence": 0.10,
        "experiential/synchronization/entrainment": 0.10,
    }

    rates_high = engine.compute_dynamic_rates(exp_high_ret, {})
    rates_low = engine.compute_dynamic_rates(exp_low_ret, {})

    assert rates_high["dynamic_lambda"] < rates_low["dynamic_lambda"]
    assert rates_high["dynamic_lambda"] < 0.035
    assert rates_low["dynamic_lambda"] > 0.055


def test_rule_weight_bounds_and_clamping():
    """Weight transitions remain bounded within [0.10, 1.00]."""
    engine = AffectivePlasticityEngine()
    
    # Reinforcement near 1.0
    res_high = engine.update_rule_weight(0.99, "reinforce", {"experiential/reflection/novelty": 1.0}, {})
    assert 0.10 <= res_high["new_weight"] <= 1.0

    # Snapping tolerance near ceiling
    res_snap = engine.update_rule_weight(0.9998, "reinforce", {"experiential/reflection/novelty": 1.0}, {})
    assert res_snap["new_weight"] == 1.0

    # Decay near 0.10
    res_low = engine.update_rule_weight(0.11, "decay", {"experiential/synchronization/entrainment": 0.0}, {})
    assert res_low["new_weight"] >= 0.10


def test_ordinary_memory_comparator_parity():
    """Primary engine and matched ordinary memory comparator achieve byte-for-byte digest parity (Rule D004)."""
    engine = AffectivePlasticityEngine()
    comparator = OrdinaryMemoryAffectivePlasticityComparator()

    configs = [
        ({}, {}),
        ({"experiential/reflection/novelty": 0.85}, {"psychological/contemplation/clarity": 0.15}),
        ({"experiential/phase/arousal": 0.90}, {"psychological/contemplation/confidence": 0.90}),
        ({"experiential/synchronization/entrainment": 0.95}, {}),
    ]

    for exp, psy in configs:
        p_res = engine.update_rule_weight(0.60, "reinforce", exp, psy)
        c_res = comparator.update_rule_weight(0.60, "reinforce", exp, psy)
        assert digest(p_res) == digest(c_res)
