"""Unit tests for Epistemic Curiosity & Value Consonance Engine."""
import pytest

from lmft_lab.dispositional_momentum import CANONICAL_LEAF_IDS
from lmft_lab.value_consonance import ValueConsonanceEngine


def test_epistemic_mode_curious_inquiry_socratic_wonder():
    """High novelty without prerequisite distortions triggers Curious Inquiry (Socratic wonder)."""
    engine = ValueConsonanceEngine()
    dials = {k: 0.50 for k in CANONICAL_LEAF_IDS}
    dials["experiential/reflection/novelty"] = 0.82
    dials["experiential/phase/arousal"] = 0.75  # elevated arousal from new lesson

    res = engine.evaluate(candidate_dials=dials, is_conflict=False, distortions_count=0)

    assert res["epistemic_mode"] == "Curious Inquiry"
    assert res["is_curious"] is True
    assert res["inquiry_posture"] == "Explore and formulate inquisitive inquiry"
    assert res["recommended_register"] == "Inquisitive & Contemplative"
    
    # Verify wonder modulation: arousal calmed to 0.52 and intention elevated
    assert res["harmonized_dials"]["experiential/phase/arousal"] == 0.52
    assert res["harmonized_dials"]["psychological/will/intention"] >= 0.68
    assert res["harmonized_dials"]["experiential/synchronization/resonance"] >= 0.65


def test_epistemic_mode_epistemic_defense():
    """Contradictions or distortions activate Epistemic Defense instead of curiosity."""
    engine = ValueConsonanceEngine()
    dials = {k: 0.50 for k in CANONICAL_LEAF_IDS}
    dials["experiential/reflection/novelty"] = 0.82

    # Case A: Explicit cognitive conflict
    res_conflict = engine.evaluate(candidate_dials=dials, is_conflict=True, distortions_count=0)
    assert res_conflict["epistemic_mode"] == "Epistemic Defense"
    assert res_conflict["is_curious"] is False
    assert res_conflict["inquiry_posture"] == "Halt and issue clarification request"

    # Case B: Prerequisite distortions detected (e.g. Coerced Compliance)
    res_distort = engine.evaluate(candidate_dials=dials, is_conflict=False, distortions_count=1)
    assert res_distort["epistemic_mode"] == "Epistemic Defense"
    assert res_distort["is_curious"] is False


def test_value_consonance_truth_vs_comfort():
    """High truth causing low comfort is anchored by contemplative fortitude."""
    engine = ValueConsonanceEngine()
    dials = {k: 0.50 for k in CANONICAL_LEAF_IDS}
    dials["psychological/truth/fact"] = 0.85
    dials["experiential/phase/valence"] = 0.15
    dials["psychological/contemplation/clarity"] = 0.80

    res = engine.evaluate(candidate_dials=dials)

    assert res["tensions_count"] >= 1
    t = next(t for t in res["tensions_detected"] if t["dyad"] == "Truth vs. Comfort")
    assert t["harmonized_val"] > 0.15
    assert res["harmonized_dials"]["psychological/truth/fact"] == 0.85  # truth is not compromised
    assert res["consonance_regime"] in ("Balanced Moral Synthesis", "Active Value Accommodation")


def test_value_consonance_power_vs_freedom():
    """Power is subordinated to prevent crushing individual freedom."""
    engine = ValueConsonanceEngine()
    dials = {k: 0.50 for k in CANONICAL_LEAF_IDS}
    dials["cultural/efficiency/power"] = 0.88
    dials["cultural/freedom/self-sufficiency"] = 0.25

    res = engine.evaluate(candidate_dials=dials)

    assert res["tensions_count"] >= 1
    t = next(t for t in res["tensions_detected"] if t["dyad"] == "Power vs. Freedom")
    assert t["harmonized_power"] < 0.88
    assert t["harmonized_freedom"] > 0.25
    assert res["harmonized_dials"]["cultural/freedom/self-sufficiency"] > 0.25


def test_value_consonance_order_vs_fairness():
    """Rigid systemic order is tempered by equitable fairness."""
    engine = ValueConsonanceEngine()
    dials = {k: 0.50 for k in CANONICAL_LEAF_IDS}
    dials["philosophical/structure/order"] = 0.85
    dials["cultural/justice/fairness"] = 0.30

    res = engine.evaluate(candidate_dials=dials)

    assert res["tensions_count"] >= 1
    t = next(t for t in res["tensions_detected"] if t["dyad"] == "Order vs. Fairness")
    assert t["harmonized_val"] > 0.30
    assert res["harmonized_dials"]["cultural/justice/fairness"] > 0.30


def test_harmonic_integrity_clean_baseline():
    """Balanced baseline yields 1.0 consonance index and Harmonic Integrity."""
    engine = ValueConsonanceEngine()
    dials = {k: 0.50 for k in CANONICAL_LEAF_IDS}

    res = engine.evaluate(candidate_dials=dials)

    assert res["consonance_index"] == 1.0
    assert res["tensions_count"] == 0
    assert res["consonance_regime"] == "Harmonic Integrity"
