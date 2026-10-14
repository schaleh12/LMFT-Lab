"""Unit tests for Calibrated Epistemic Modesty & Adversarial Noise Profiling.

Verifies:
1. Exact anchor matches fire active postures with alignment 1.00.
2. Partial valid matches above threshold tau=0.55 fire reliably.
3. Noisy distractors and adversarial out-of-domain text honestly abstain.
4. Optimal operating point tau=0.55 achieves 0.0% false-positive rate.
5. Matched ordinary-memory baseline parity (Rule D004).
6. Invariance of canonical 40 founding nodes in birth.py (Rule D001).
"""
import pytest
from lmft_lab.birth import _inventory
from lmft_lab.epistemic_calibration import (
    compute_anchor_alignment,
    classify_epistemic_stance,
    evaluate_threshold_sweep,
    OrdinaryMemoryEpistemicComparator,
    CALIBRATED_THRESHOLD,
)
from lmft_lab.runtime_store import digest


CALIBRATION_TEST_DATASET = [
    # 1. Exact Valid Matches (alignment = 1.00)
    {
        "id": "exact-01",
        "text": "The local commercial bank approved the enterprise expansion loan.",
        "anchor_pattern": "commercial bank",
        "target_sense_key": "bank%1:14:00::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": True,
    },
    {
        "id": "exact-02",
        "text": "The judge issued a formal court order to preserve the documents.",
        "anchor_pattern": "court order",
        "target_sense_key": "order%1:10:00::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": True,
    },
    # 2. High Partial Valid Matches (alignment >= 0.60)
    {
        "id": "partial-01",
        "text": "They relaxed along the grassy river bank enjoying the cool breeze.",
        "anchor_pattern": "grassy river bank",
        "target_sense_key": "bank%1:17:01::",
        "active_posture": "Foundational Anchor",
        "active_register": "Communal & Reassuring",
        "is_valid_target": True,
    },
    {
        "id": "partial-02",
        "text": "The logistics team placed an order for emergency supplies.",
        "anchor_pattern": "placed an order for supplies",
        "target_sense_key": "order%1:10:01::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": True,
    },
    # 3. Low Overlap / Noisy Distractor Sentences (is_valid_target = False, alignment <= 0.40)
    {
        "id": "noise-01",
        "text": "He took a long walk down the commercial boulevard without seeing anyone.",
        "anchor_pattern": "commercial bank",
        "target_sense_key": "bank%1:14:00::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": False,
    },
    {
        "id": "noise-02",
        "text": "The tennis court was closed for the seasonal tournament.",
        "anchor_pattern": "court order",
        "target_sense_key": "order%1:10:00::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": False,
    },
    # 4. Adversarial Out-of-Domain Sentences (is_valid_target = False, alignment = 0.0)
    {
        "id": "adversarial-01",
        "text": "Quantum entanglement demonstrates non-local correlations in photonic lattices.",
        "anchor_pattern": "commercial bank",
        "target_sense_key": "bank%1:14:00::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": False,
    },
    {
        "id": "adversarial-02",
        "text": "A crimson sunset illuminated the distant snowcapped mountain ridges.",
        "anchor_pattern": "court order",
        "target_sense_key": "order%1:10:00::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": False,
    },
]


def test_anchor_alignment_calculation():
    """Verifies precision of token overlap metric."""
    window = ["the", "commercial", "bank", "opened"]
    anchor = ["commercial", "bank"]
    assert compute_anchor_alignment(window, anchor) == 1.00
    
    partial_window = ["the", "bank", "opened"]
    assert compute_anchor_alignment(partial_window, anchor) == 0.50
    
    empty_window = ["irrelevant", "text"]
    assert compute_anchor_alignment(empty_window, anchor) == 0.00


def test_calibrated_classification_behavior():
    """Verifies that valid targets fire and noise/adversarial cases honestly abstain."""
    for item in CALIBRATION_TEST_DATASET:
        res = classify_epistemic_stance(
            item["text"],
            item["anchor_pattern"],
            item["target_sense_key"],
            item["active_posture"],
            item["active_register"],
            threshold=CALIBRATED_THRESHOLD,
        )
        if item["is_valid_target"]:
            assert res["decision"] == "active"
            assert res["selected_sense"] == item["target_sense_key"]
            assert res["posture"] == item["active_posture"]
            assert res["register"] == item["active_register"]
        else:
            assert res["decision"] == "abstain"
            assert res["selected_sense"] is None
            assert res["posture"] == "Neutral Observant Silence"
            assert res["register"] == "Neutral Observant Silence"


def test_threshold_sweep_pareto_optimality():
    """Verifies that threshold tau=0.55 guarantees 0.0% false-positive rate."""
    thresholds = [0.30, 0.40, 0.50, 0.55, 0.60, 0.70, 0.80]
    sweep = evaluate_threshold_sweep(CALIBRATION_TEST_DATASET, thresholds)
    
    # Locate operating point tau = 0.55
    point_55 = next(p for p in sweep if p["threshold"] == 0.55)
    assert point_55["fp"] == 0
    assert point_55["false_positive_rate"] == 0.0
    assert point_55["precision"] == 1.0
    assert point_55["recall"] == 1.0
    assert point_55["overall_accuracy"] == 1.0


def test_ordinary_memory_baseline_parity():
    """Verifies byte-for-byte evaluation parity with the matched ordinary-memory comparator (Rule D004)."""
    comparator = OrdinaryMemoryEpistemicComparator()
    
    for item in CALIBRATION_TEST_DATASET:
        p_res = classify_epistemic_stance(
            item["text"],
            item["anchor_pattern"],
            item["target_sense_key"],
            item["active_posture"],
            item["active_register"],
            threshold=CALIBRATED_THRESHOLD,
        )
        c_res = comparator.evaluate(
            item["text"],
            item["anchor_pattern"],
            item["target_sense_key"],
            item["active_posture"],
            item["active_register"],
            threshold=CALIBRATED_THRESHOLD,
        )
        assert digest(p_res) == digest(c_res)


def test_frozen_seed_invariant_preserved():
    """Verifies that the canonical 40 founding nodes in birth.py remain strictly invariant (Rule D001)."""
    inventory = list(_inventory())
    assert len(inventory) == 40
    domains = {item[2] for item in inventory}
    assert domains == {"cultural", "philosophical", "experiential", "psychological"}
