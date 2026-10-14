"""Unit tests for Second Lemma Generalization Benchmark (Bank)."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from lmft_lab.birth import _inventory
import second_lemma_bank as slb


def test_bank_capacity_rules_structure():
    """All bank rules conform to capacity schema and map to valid WordNet senses."""
    assert len(slb.BANK_CAPACITY_RULES) == 9
    for r in slb.BANK_CAPACITY_RULES:
        assert r["target_sense_key"].startswith("bank%1:")
        assert len(r["exact_quote"]) > 0
        assert len(r["core_pattern"]) > 0
        assert len(r["gloss"]) > 10


def test_predict_bank_item_senses():
    """Predicts financial, river, and reserve senses with precise glosses."""
    rules = slb.BANK_CAPACITY_RULES

    # Financial
    item_fin = {"id": "test-fin", "surface_tokens": ["Deposit", "money", "in", "the", "commercial", "bank", "."]}
    pred_fin = slb.predict_bank_item(rules, item_fin)
    assert pred_fin["decision"] == "single"
    assert pred_fin["selected_sense"] == "bank%1:14:00::"
    assert "financial institution" in pred_fin["explanation"]

    # River
    item_riv = {"id": "test-riv", "surface_tokens": ["They", "walked", "along", "the", "green", "river", "bank", "."]}
    pred_riv = slb.predict_bank_item(rules, item_riv)
    assert pred_riv["decision"] == "single"
    assert pred_riv["selected_sense"] == "bank%1:17:01::"
    assert "sloping natural land" in pred_riv["explanation"]

    # Reserve
    item_res = {"id": "test-res", "surface_tokens": ["The", "clinic", "needed", "a", "fresh", "blood", "bank", "."]}
    pred_res = slb.predict_bank_item(rules, item_res)
    assert pred_res["decision"] == "single"
    assert pred_res["selected_sense"] == "bank%1:14:01::"
    assert "reserve repository" in pred_res["explanation"]


def test_predict_bank_item_calibrated_abstention():
    """Unanchored and non-target sentences honestly abstain."""
    rules = slb.BANK_CAPACITY_RULES

    # Unanchored ambiguous target
    item_ambig = {"id": "test-unanchored", "surface_tokens": ["He", "went", "to", "the", "bank", "."]}
    pred_ambig = slb.predict_bank_item(rules, item_ambig)
    assert pred_ambig["decision"] == "abstain"
    assert pred_ambig["selected_sense"] is None

    # OOD sentence
    item_ood = {"id": "test-ood", "surface_tokens": ["A", "warm", "sun", "shone", "down", "."]}
    pred_ood = slb.predict_bank_item(rules, item_ood)
    assert pred_ood["decision"] == "abstain"
    assert pred_ood["selected_sense"] is None


def test_second_lemma_benchmark_parity_and_registers():
    """Full second lemma benchmark satisfies Rule D004 parity and maps into distinct registers."""
    summary = slb.run_second_lemma_study()

    assert summary["consumer_parity"] is True
    assert summary["total_instances"] == 11
    assert summary["correct_fired"] == 9
    assert summary["honest_abstentions"] == 2
    assert summary["wrong_singletons"] == 0
    assert summary["precision_on_fired"] == 1.0

    regs = summary["register_distribution"]
    assert regs["Methodical & Pragmatic"] == 4
    assert regs["Communal & Reassuring"] == 3
    assert regs["Authoritative & Chivalrous"] == 2
    assert regs["Neutral Observant Silence"] == 2

    # Verify 24 canonical leaves in all active records
    for r in summary["results"]:
        dials = r["regulation"]["all_24_canonical_leaf_dials"]
        assert len(dials) == 24
        for k, v in dials.items():
            assert 0.0 <= v <= 1.0
