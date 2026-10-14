"""Unit tests for Lateral Ethical-Ontological Coupling Matrix Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
from lmft_lab.lateral_coupling import (
    CULTURAL_LEAF_IDS,
    PHILOSOPHICAL_LEAF_IDS,
    CANONICAL_LEAF_IDS,
    LateralCouplingEngine,
    OrdinaryMemoryLateralComparator,
)


def test_canonical_seed_integrity():
    """All 12 coupled leaves strictly exist in the frozen founding seed (Rule D001)."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    assert len(inventory_leaf_ids) == 24

    for leaf_id in CULTURAL_LEAF_IDS:
        assert leaf_id in inventory_leaf_ids
    for leaf_id in PHILOSOPHICAL_LEAF_IDS:
        assert leaf_id in inventory_leaf_ids


def test_neutral_baseline_quiescence():
    """Neutral baselines (0.50) produce zero deltas and remain quiescent."""
    engine = LateralCouplingEngine()
    res = engine.couple()

    for delta in res["delta_cultural"].values():
        assert delta == 0.0
    for delta in res["delta_philosophical"].values():
        assert delta == 0.0

    for v in res["coupled_cultural"].values():
        assert v == 0.50
    for v in res["coupled_philosophical"].values():
        assert v == 0.50


def test_power_induces_order_and_agency():
    """High Cultural Power induces compensatory Structure/Order and elevates Agency."""
    engine = LateralCouplingEngine()
    cult = {"cultural/efficiency/power": 0.90}  # +0.40 deviation
    res = engine.couple(cultural_dials=cult)

    # Power -> Order (0.40 * 0.20 = +0.08)
    assert res["delta_philosophical"]["philosophical/structure/order"] == 0.08
    assert res["coupled_philosophical"]["philosophical/structure/order"] == 0.58

    # Power -> Agency (0.40 * 0.25 = +0.10)
    assert res["delta_philosophical"]["philosophical/being/agency"] == 0.10
    assert res["coupled_philosophical"]["philosophical/being/agency"] == 0.60


def test_chaos_triggers_moral_ballast():
    """High Philosophical Chaos activates Justice/Honor and Freedom/Self-Sufficiency."""
    engine = LateralCouplingEngine()
    phil = {"philosophical/structure/chaos": 0.90}  # +0.40 deviation
    res = engine.couple(philosophical_dials=phil)

    # Chaos -> Honor (0.40 * 0.25 = +0.10)
    assert res["delta_cultural"]["cultural/justice/honor"] == 0.10
    assert res["coupled_cultural"]["cultural/justice/honor"] == 0.60

    # Chaos -> Self-Sufficiency (0.40 * 0.20 = +0.08)
    assert res["delta_cultural"]["cultural/freedom/self-sufficiency"] == 0.08
    assert res["coupled_cultural"]["cultural/freedom/self-sufficiency"] == 0.58


def test_bound_enforcement_under_extreme_gain():
    """Extreme saturation with gain=2.0 strictly respects [0.0, 1.0] dial bounds."""
    engine = LateralCouplingEngine()
    high_cult = {k: 1.0 for k in CULTURAL_LEAF_IDS}
    high_phil = {k: 1.0 for k in PHILOSOPHICAL_LEAF_IDS}

    res = engine.couple(cultural_dials=high_cult, philosophical_dials=high_phil, coupling_gain=2.0)

    for v in res["coupled_cultural"].values():
        assert 0.0 <= v <= 1.0
    for v in res["coupled_philosophical"].values():
        assert 0.0 <= v <= 1.0


def test_ordinary_memory_comparator_parity():
    """Primary engine and matched ordinary memory baseline achieve byte-for-byte parity (Rule D004)."""
    engine = LateralCouplingEngine()
    comparator = OrdinaryMemoryLateralComparator()

    configs = [
        ({}, {}),
        ({"cultural/efficiency/power": 0.85}, {"philosophical/structure/chaos": 0.75}),
        ({"cultural/justice/fairness": 0.90}, {"philosophical/persistence/continuity": 0.80}),
        ({"cultural/freedom/needlessness": 0.30}, {"philosophical/being/agency": 0.20}),
    ]

    for cult, phil in configs:
        p_res = engine.couple(cultural_dials=cult, philosophical_dials=phil, coupling_gain=1.2)
        c_res = comparator.couple(cultural_dials=cult, philosophical_dials=phil, coupling_gain=1.2)
        assert digest(p_res) == digest(c_res)
