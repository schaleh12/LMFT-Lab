"""Tests for Meditative Homeostatic Regulation & Multi-Domain Android Heartbeat Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
import meditative_regulation as mr
import metacognitive_priming as mp


def test_canonical_leaf_nodes_match_inventory():
    """All 24 leaf nodes used in meditative regulation must match birth.py exactly."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    expected = set(mr.CANONICAL_LEAF_MAP.keys())
    assert expected == inventory_leaf_ids
    assert len(expected) == 24


def test_homeostatic_damping_on_extreme_being_skew():
    """Homeostatic regulation dampens extreme Being skew (agency vs existence)."""
    # High agency, low existence
    pred = {"selected_sense": "order%1:10:03::", "explanation": "military directive", "decision": "single"}
    raw_priming = mp.compute_priming_dials(pred)
    assert raw_priming["dials"]["philosophical/being/agency"] == 0.85
    assert raw_priming["dials"]["philosophical/being/existence"] == 0.40

    reg = mr.compute_homeostatic_regulation(raw_priming, pred)
    assert not reg["epistemic_abstention"]
    assert reg["homeostatic_damping"]["applied"] is True
    assert "psychosis_volitional_overextension" in reg["homeostatic_damping"]["mitigated_shadows"]
    # Existence dial should have been increased as a balancing counterweight
    assert reg["all_24_canonical_leaf_dials"]["philosophical/being/existence"] == 0.55
    assert reg["emitted_actuation_posture"].startswith("Noble Sovereign Action")


def test_homeostatic_damping_on_extreme_structure_skew():
    """Homeostatic regulation dampens extreme Structure skew (order vs chaos)."""
    pred = {"selected_sense": "order%1:26:00::", "explanation": "unbroken harmony", "decision": "single"}
    raw_priming = mp.compute_priming_dials(pred)
    # Order is 0.85, Chaos is 0.05 -> skew is 0.80 > 0.70 threshold
    reg = mr.compute_homeostatic_regulation(raw_priming, pred)
    assert reg["homeostatic_damping"]["applied"] is True
    assert "prejudice_hyper_rigidity" in reg["homeostatic_damping"]["mitigated_shadows"]
    assert reg["all_24_canonical_leaf_dials"]["philosophical/structure/chaos"] == 0.15
    assert reg["emitted_actuation_posture"].startswith("Foundational Anchor")


def test_abstention_produces_quiet_ingestion():
    """Epistemic abstentions produce zeroed leaf dials and quiet ingestion posture."""
    pred = {"selected_sense": None, "decision": "abstain"}
    raw_priming = mp.compute_priming_dials(pred)
    assert raw_priming["epistemic_abstention"] is True

    reg = mr.compute_homeostatic_regulation(raw_priming, pred)
    assert reg["epistemic_abstention"] is True
    assert reg["regulated_stance"] == "neutral_open"
    assert reg["emitted_actuation_posture"].startswith("Quiet Ingestion")
    assert all(v == 0.0 for v in reg["all_24_canonical_leaf_dials"].values())


def test_all_24_leaf_nodes_populated_for_active_instances():
    """All 24 leaf dials across all 4 domains must have non-negative values."""
    pred = {"selected_sense": "order%1:04:00::", "explanation": "sequential series", "decision": "single"}
    raw_priming = mp.compute_priming_dials(pred)
    reg = mr.compute_homeostatic_regulation(raw_priming, pred)

    leaf_dials = reg["all_24_canonical_leaf_dials"]
    assert len(leaf_dials) == 24
    for key, val in leaf_dials.items():
        assert isinstance(val, (int, float))
        assert 0.0 <= val <= 1.0


def test_actuation_posture_distribution_mapping():
    """Each of the 5 canonical stances maps to a distinct behavioral actuation posture."""
    stances = [
        "authoritative_directive_execution",
        "stable_ontological_equilibrium",
        "quantitative_continuum_awareness",
        "discrete_sequential_operation",
        "general_systemic_ordering",
    ]
    postures = set()
    for s in stances:
        fake_priming = {
            "epistemic_abstention": False,
            "dominant_stance": s,
            "dials": {
                "philosophical/being/agency": 0.5,
                "philosophical/being/existence": 0.5,
                "philosophical/structure/order": 0.5,
                "philosophical/structure/chaos": 0.5,
                "philosophical/persistence/continuity": 0.5,
                "philosophical/persistence/discreteness": 0.5,
            },
            "chromatic_aura": {"hex": "#FFFFFF", "rgb": [255, 255, 255]},
        }
        reg = mr.compute_homeostatic_regulation(fake_priming, {"explanation": "test"})
        postures.add(reg["emitted_actuation_posture"])

    assert len(postures) == 5
