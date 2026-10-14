"""Unit tests for Fuzzy Prerequisite Coherence Gate Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
from lmft_lab.prerequisite_gate import (
    CONDITIONAL_LEAF_TARGETS,
    CANONICAL_LEAF_IDS,
    PrerequisiteCoherenceGate,
    OrdinaryMemoryPrerequisiteComparator,
)


def test_canonical_seed_integrity():
    """All 10 evaluated leaves strictly exist in the frozen founding seed (Rule D001)."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    assert len(inventory_leaf_ids) == 24

    for leaf_id in CONDITIONAL_LEAF_TARGETS:
        assert leaf_id in inventory_leaf_ids


def test_coerced_compliance_distortion():
    """Justice claimed under crushed Freedom triggers Coerced Compliance Distortion."""
    gate = PrerequisiteCoherenceGate()
    dials = {
        "cultural/justice/fairness": 0.90,
        "cultural/freedom/self-sufficiency": 0.10,
        "cultural/freedom/needlessness": 0.10,
    }
    res = gate.evaluate_coherence(dials)

    assert "Coerced Compliance Distortion (Justice asserted without Freedom)" in res["distortions_detected"]
    # Justice factor = 0.40 + 0.60 * 0.10 = 0.46; Authentic = 0.90 * 0.46 = 0.414
    assert res["authentic_scores"]["authentic_justice"] <= 0.45
    assert res["is_authentic"] is False


def test_dogmatic_hallucination_distortion():
    """Confidence claimed without Clarity triggers Dogmatic Hallucination Distortion."""
    gate = PrerequisiteCoherenceGate()
    dials = {
        "psychological/contemplation/confidence": 0.95,
        "psychological/contemplation/clarity": 0.10,
    }
    res = gate.evaluate_coherence(dials)

    assert "Dogmatic Hallucination Distortion (Confidence asserted without Clarity)" in res["distortions_detected"]
    # Confidence factor = 0.30 + 0.70 * 0.10 = 0.37; Authentic = 0.95 * 0.37 = 0.3515
    assert res["authentic_scores"]["authentic_confidence"] <= 0.40
    assert res["is_authentic"] is False


def test_unanchored_volition_distortion():
    """Intention claimed without Agency triggers Unanchored Volition Distortion."""
    gate = PrerequisiteCoherenceGate()
    dials = {
        "psychological/will/intention": 0.85,
        "philosophical/being/agency": 0.10,
    }
    res = gate.evaluate_coherence(dials)

    assert "Unanchored Volition Distortion (Intention asserted without Agency)" in res["distortions_detected"]
    assert res["is_authentic"] is False


def test_harmonic_authenticity():
    """When prerequisites are fulfilled, claims are authentic and coherence is high."""
    gate = PrerequisiteCoherenceGate()
    dials = {
        "cultural/justice/fairness": 0.85,
        "cultural/freedom/self-sufficiency": 0.90,
        "cultural/freedom/needlessness": 0.90,
        "psychological/contemplation/confidence": 0.90,
        "psychological/contemplation/clarity": 0.90,
        "psychological/will/intention": 0.85,
        "philosophical/being/agency": 0.90,
        "philosophical/structure/order": 0.85,
        "philosophical/persistence/continuity": 0.90,
        "philosophical/persistence/discreteness": 0.90,
    }
    res = gate.evaluate_coherence(dials)

    assert len(res["distortions_detected"]) == 0
    assert res["global_coherence_index"] >= 0.90
    assert res["is_authentic"] is True


def test_ordinary_memory_comparator_parity():
    """Primary gate and matched ordinary memory baseline achieve byte-for-byte digest parity (Rule D004)."""
    gate = PrerequisiteCoherenceGate()
    comparator = OrdinaryMemoryPrerequisiteComparator()

    configs = [
        {},
        {"cultural/justice/fairness": 0.90, "cultural/freedom/self-sufficiency": 0.10},
        {"psychological/contemplation/confidence": 0.85, "psychological/contemplation/clarity": 0.15},
        {"philosophical/structure/order": 0.95, "philosophical/persistence/continuity": 0.10},
        {"cultural/justice/fairness": 0.80, "cultural/freedom/self-sufficiency": 0.80},
    ]

    for cfg in configs:
        p_res = gate.evaluate_coherence(cfg)
        c_res = comparator.evaluate(cfg)
        assert digest(p_res) == digest(c_res)
