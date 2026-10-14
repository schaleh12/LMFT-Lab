"""Tests for Affective Homeostasis Governor (Mood Stabilizer)."""
import pytest

from lmft_lab.affective_homeostasis import AffectiveHomeostasisGovernor
from lmft_lab.dispositional_momentum import CANONICAL_LEAF_IDS


def test_homeostasis_calm_equilibrium():
    governor = AffectiveHomeostasisGovernor()
    prev = {k: 0.50 for k in CANONICAL_LEAF_IDS}
    curr = {k: 0.52 for k in CANONICAL_LEAF_IDS}

    res = governor.stabilize(curr, prev)
    assert res["interventions_count"] == 0
    assert res["homeostatic_regime"] in ("Calm Equilibrium", "Adaptive Dynamic Response")
    assert res["emotional_balance_score"] > 0.85
    assert res["stabilized_dials"] == curr


def test_homeostasis_dampens_severe_volatility_spike():
    governor = AffectiveHomeostasisGovernor(volatility_threshold=0.35)
    prev = {k: 0.50 for k in CANONICAL_LEAF_IDS}
    curr = dict(prev)

    # Induce massive shock: arousal jumps by +0.48
    curr["experiential/phase/arousal"] = 0.98

    res = governor.stabilize(curr, prev)
    assert res["interventions_count"] >= 1
    assert res["homeostatic_regime"] == "Active Volatility Clamping"
    arousal_inv = next(inv for inv in res["interventions"] if inv["leaf_id"] == "experiential/phase/arousal")
    
    # Verify stabilized value is damped below 0.98
    assert arousal_inv["stabilized_value"] < 0.98
    assert arousal_inv["stabilized_value"] > 0.50
    # Volatility was clamped
    assert arousal_inv["delta_after"] < arousal_inv["delta_before"]


def test_homeostasis_prevents_lower_boundary_saturation():
    governor = AffectiveHomeostasisGovernor(extreme_lower=0.05)
    prev = {k: 0.50 for k in CANONICAL_LEAF_IDS}
    curr = dict(prev)

    # Valence crashes towards total collapse (0.01)
    curr["experiential/phase/valence"] = 0.01

    res = governor.stabilize(curr, prev)
    valence_inv = next(inv for inv in res["interventions"] if inv["leaf_id"] == "experiential/phase/valence")
    assert valence_inv["stabilized_value"] > 0.05
    assert any("lower_boundary_saturation" in r for r in valence_inv["reasons"])


def test_anchor_support_strengthens_dampening():
    governor = AffectiveHomeostasisGovernor(volatility_threshold=0.35)
    prev = {k: 0.50 for k in CANONICAL_LEAF_IDS}

    # Case A: Low anchors (confused, chaotic mind)
    curr_low = dict(prev)
    curr_low["psychological/contemplation/clarity"] = 0.10
    curr_low["philosophical/structure/order"] = 0.10
    curr_low["philosophical/persistence/continuity"] = 0.10
    curr_low["experiential/phase/arousal"] = 0.95

    res_low = governor.stabilize(curr_low, prev)

    # Case B: High anchors (clear, grounded, continuous mind)
    curr_high = dict(prev)
    curr_high["psychological/contemplation/clarity"] = 0.90
    curr_high["philosophical/structure/order"] = 0.90
    curr_high["philosophical/persistence/continuity"] = 0.90
    curr_high["experiential/phase/arousal"] = 0.95

    res_high = governor.stabilize(curr_high, prev)

    assert res_high["anchor_support"] > res_low["anchor_support"]
    arousal_low = next(inv for inv in res_low["interventions"] if inv["leaf_id"] == "experiential/phase/arousal")
    arousal_high = next(inv for inv in res_high["interventions"] if inv["leaf_id"] == "experiential/phase/arousal")

    # The grounded mind dampens the spike more effectively (closer to equilibrium)
    assert arousal_high["stabilized_value"] <= arousal_low["stabilized_value"]
