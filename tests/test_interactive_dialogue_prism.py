"""Tests for Interactive Dialogue Prism Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from lmft_lab.birth import _inventory
import interactive_dialogue_prism as idp


def test_tokenize_input():
    """Deterministic tokenization handles words and punctuation cleanly."""
    tokens = idp.tokenize_input("The court issued an order.")
    assert tokens == ["The", "court", "issued", "an", "order", "."]

    tokens_empty = idp.tokenize_input("   ")
    assert tokens_empty == [""]


def test_locate_target_indices():
    """Locates 'order' or 'orders' case-insensitively, or falls back to [0]."""
    tokens = ["The", "officer", "gave", "Orders", "to", "march"]
    indices = idp.locate_target_indices(tokens)
    assert indices == [3]

    tokens_no_target = ["A", "peaceful", "river", "flowed"]
    indices_fallback = idp.locate_target_indices(tokens_no_target)
    assert indices_fallback == [0]


def test_project_interactive_dialogue_matched():
    """Matched sentence projects through all 24 canonical leaves into active register."""
    sentence = "The court issued a formal order of the court."
    res = idp.project_interactive_dialogue(sentence)

    assert res["prediction"]["decision"] == "single"
    assert res["prediction"]["selected_sense"] == "order%1:10:00::"

    # Verify 24 canonical leaf dials present and bounded
    dials = res["meditative_regulation"]["all_24_canonical_leaf_dials"]
    assert len(dials) == 24
    for k, v in dials.items():
        assert 0.0 <= v <= 1.0

    k = res["kaleidoscopic_response"]
    pv = k["prism_vector"]
    assert 0.0 <= pv["theta_contemplation"] < 360.0
    assert 0.0 <= pv["theta_truth"] < 360.0
    assert 0.0 <= pv["theta_will"] < 360.0
    assert 0.0 <= k["harmonic_concordance"] <= 1.0

    act = k["social_exchange_actuation"]
    assert act["speaking_register"] in [
        "Methodical & Pragmatic",
        "Authoritative & Chivalrous",
        "Communal & Reassuring",
        "Equilibrated & Diplomatic",
        "Analytical & Scientific",
    ]
    assert len(act["actionable_social_strategy"]) > 10
    assert len(act["dialogue_exemplar"]) > 10


def test_project_interactive_dialogue_abstain():
    """Unseen sentence without matching anchor cleanly triggers calibrated epistemic modesty."""
    sentence = "The sun rose gently over the distant horizon."
    res = idp.project_interactive_dialogue(sentence)

    assert res["prediction"]["decision"] == "abstain"
    assert res["prediction"]["selected_sense"] is None

    k = res["kaleidoscopic_response"]
    assert k["epistemic_abstention"] is True
    assert k["prism_vector"]["theta_contemplation"] == 0.0
    assert k["prism_vector"]["theta_truth"] == 0.0
    assert k["prism_vector"]["theta_will"] == 0.0
    assert k["harmonic_concordance"] == 1.0

    act = k["social_exchange_actuation"]
    assert act["speaking_register"] == "Neutral Observant Silence"
    assert "epistemic modesty" in act["actionable_social_strategy"]


def test_verify_interactive_parity():
    """Rule D004 parity check proves byte-for-byte evaluation equivalence."""
    res = idp.verify_interactive_parity("The court issued a formal order of the court.")
    assert res["consumer_parity"] is True
    assert len(res["projection_digest"]) == 64
