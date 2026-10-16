"""Unit tests for Persistent Dispositional State Vector & Momentum Drift Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
from lmft_lab.dispositional_momentum import (
    CANONICAL_LEAF_IDS,
    PersistentDispositionalVector,
    OrdinaryMemoryDispositionalComparator,
)


def test_canonical_seed_integrity():
    """All 24 tracked leaves strictly exist in the frozen founding seed (Rule D001)."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    assert len(inventory_leaf_ids) == 24
    assert inventory_leaf_ids == CANONICAL_LEAF_IDS


def test_momentum_incorporation():
    """Successive interactions accumulate dispositional momentum without abrupt reset."""
    vec = PersistentDispositionalVector(gamma=0.40)
    assert vec.dials["philosophical/structure/order"] == 0.50

    # Interaction 1: high Order stimulus (0.90)
    # New = 0.60 * 0.50 + 0.40 * 0.90 = 0.30 + 0.36 = 0.66
    res1 = vec.incorporate_situational_stimulus({"philosophical/structure/order": 0.90})
    assert res1["current_dials"]["philosophical/structure/order"] == 0.66
    assert vec.epoch_count == 1

    # Interaction 2: high Order stimulus again (0.90)
    # New = 0.60 * 0.66 + 0.40 * 0.90 = 0.396 + 0.36 = 0.756
    res2 = vec.incorporate_situational_stimulus({"philosophical/structure/order": 0.90})
    assert res2["current_dials"]["philosophical/structure/order"] == 0.756
    assert vec.epoch_count == 2

    # Interaction 3: neutral stimulus (0.50)
    # New = 0.60 * 0.756 + 0.40 * 0.50 = 0.4536 + 0.20 = 0.6536
    res3 = vec.incorporate_situational_stimulus({"philosophical/structure/order": 0.50})
    assert res3["current_dials"]["philosophical/structure/order"] == 0.6536
    # Note that it does NOT immediately drop back to 0.50; it retains dispositional momentum!
    assert res3["current_dials"]["philosophical/structure/order"] > 0.60


def test_idle_equilibrium_drift():
    """Inactivity gently relaxes elevated dials back towards neutral 0.50."""
    vec = PersistentDispositionalVector(initial_dials={"philosophical/structure/order": 0.90}, mu=0.10)
    assert vec.dials["philosophical/structure/order"] == 0.90

    # Step 1: 0.90 + 0.10 * (0.50 - 0.90) = 0.90 - 0.04 = 0.86
    res1 = vec.apply_idle_equilibrium_drift(steps=1)
    assert res1["current_dials"]["philosophical/structure/order"] == 0.86

    # 10 steps later, significantly closer to 0.50
    res10 = vec.apply_idle_equilibrium_drift(steps=10)
    assert res10["current_dials"]["philosophical/structure/order"] < 0.65


def test_serialization_round_trip():
    """State exports and imports with 100% field and digest fidelity."""
    vec1 = PersistentDispositionalVector(gamma=0.30, mu=0.08)
    vec1.incorporate_situational_stimulus({"cultural/justice/fairness": 0.85})

    exported = vec1.export_state()
    assert "state_digest" in exported
    assert exported["epoch_count"] == 1

    vec2 = PersistentDispositionalVector()
    vec2.import_state(exported)

    assert vec2.epoch_count == 1
    assert vec2.gamma == 0.30
    assert vec2.mu == 0.08
    assert vec2.dials == vec1.dials
    assert digest(vec2.export_state()) == digest(exported)


def test_seed_geometry_mutation_rejected():
    """Importing a state with an altered seed fingerprint is rejected (Rule D001)."""
    vec = PersistentDispositionalVector()
    tampered = vec.export_state()
    tampered["seed_fingerprint"] = "forged_non_canonical_geometry"

    with pytest.raises(ValueError, match="Seed geometry violation"):
        vec.import_state(tampered)


def test_ordinary_memory_comparator_parity():
    """Primary vector and matched ordinary memory baseline produce byte-for-byte parity (Rule D004)."""
    vec = PersistentDispositionalVector(gamma=0.35, mu=0.05)
    comparator = OrdinaryMemoryDispositionalComparator(gamma=0.35, mu=0.05)

    stimuli = [
        {"cultural/efficiency/power": 0.80, "philosophical/structure/order": 0.75},
        {"experiential/phase/arousal": 0.70, "experiential/phase/valence": 0.60},
        {"psychological/truth/fact": 0.90},
    ]

    for sit in stimuli:
        p_res = vec.incorporate_situational_stimulus(sit)
        c_res = comparator.incorporate(sit)
        assert digest(p_res) == digest(c_res)

    # Drift step parity
    p_drift = vec.apply_idle_equilibrium_drift(steps=3)
    c_drift = comparator.idle_drift(steps=3)
    assert digest(p_drift) == digest(c_drift)

    # Export parity
    assert digest(vec.export_state()) == digest(comparator.export_state())


def test_hierarchical_40_node_tree_rollup():
    """Verifies 24 leaves roll up into 12 branches and 4 domains covering all 40 canonical seed nodes."""
    vec = PersistentDispositionalVector(initial_dials={
        "psychological/contemplation/clarity": 0.90,
        "psychological/contemplation/confidence": 0.70,
    })
    tree = vec.compute_hierarchical_tree()
    assert len(tree["leaf_dials"]) == 24
    assert len(tree["branch_dials"]) == 12
    assert len(tree["domain_dials"]) == 4
    assert len(tree["all_40_nodes"]) == 40
    assert tree["branch_dials"]["psychological/contemplation"] == 0.80
    assert set(tree["all_40_nodes"].keys()) == {node_id for node_id, _, _, _, _ in _inventory()}

