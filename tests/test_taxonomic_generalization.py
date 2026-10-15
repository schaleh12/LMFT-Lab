"""Unit tests for Taxonomic Hypernym Generalization Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
from lmft_lab.taxonomic_generalization import (
    CANONICAL_LEAF_IDS,
    TAXONOMIC_REGISTRY,
    TaxonomicGeneralizer,
    OrdinaryMemoryTaxonomicComparator,
)


def test_canonical_seed_integrity():
    """All 24 leaf targets strictly exist in the frozen founding seed (Rule D001)."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    assert len(inventory_leaf_ids) == 24
    assert inventory_leaf_ids == CANONICAL_LEAF_IDS

    # Verify all registry affinities only target canonical leaves
    for sense_key, rec in TAXONOMIC_REGISTRY.items():
        for leaf_id in rec["leaf_dial_affinities"].keys():
            assert leaf_id in inventory_leaf_ids, f"Non-canonical leaf: {leaf_id}"


def test_hypernym_path_and_primary_category():
    """Extracts hypernym paths and primary categories for bank and order senses."""
    generalizer = TaxonomicGeneralizer()

    # Bank financial
    path_fin = generalizer.get_hypernym_path("bank%1:14:00::")
    assert path_fin[0] == "financial_institution"
    assert path_fin[-1] == "entity"
    assert generalizer.get_primary_category("bank%1:14:00::") == "organization"

    # Bank river
    path_riv = generalizer.get_hypernym_path("bank%1:17:01::")
    assert path_riv[0] == "slope"
    assert path_riv[-1] == "entity"
    assert generalizer.get_primary_category("bank%1:17:01::") == "geological_formation"

    # Order judicial decree
    path_jud = generalizer.get_hypernym_path("order%1:10:00::")
    assert path_jud[0] == "legal_document"
    assert path_jud[-1] == "entity"
    assert generalizer.get_primary_category("order%1:10:00::") == "legal_instrument"

    # Order command
    path_cmd = generalizer.get_hypernym_path("order%1:10:03::")
    assert path_cmd[0] == "speech_act"
    assert path_cmd[-1] == "entity"
    assert generalizer.get_primary_category("order%1:10:03::") == "authoritative_act"


def test_taxonomic_modulation_bounds():
    """Modulates canonical leaf dials bounded strictly within [0.0, 1.0]."""
    generalizer = TaxonomicGeneralizer()
    
    # Base dials all 0.50, weight 1.0
    res = generalizer.compute_taxonomic_modulation("bank%1:14:00::", weight=1.0)
    assert res["found"] is True
    assert res["primary_category"] == "organization"
    dials = res["modulated_dials"]
    
    # Fairness should be 0.50 + 0.30 = 0.80
    assert dials["cultural/justice/fairness"] == 0.80
    # Order should be 0.50 + 0.35 = 0.85
    assert dials["philosophical/structure/order"] == 0.85
    # Power should be 0.50 + 0.25 = 0.75
    assert dials["cultural/efficiency/power"] == 0.75

    # Check bounds when saturated
    high_base = {k: 0.95 for k in CANONICAL_LEAF_IDS}
    res_sat = generalizer.compute_taxonomic_modulation("bank%1:14:00::", base_dials=high_base, weight=1.0)
    for k, v in res_sat["modulated_dials"].items():
        assert 0.0 <= v <= 1.0


def test_cross_lemma_conceptual_overlap():
    """Cross-lemma senses sharing categories activate common canonical leaves."""
    generalizer = TaxonomicGeneralizer()

    # bank (organization) vs order (social condition / rule of law)
    res_bank = generalizer.compute_taxonomic_modulation("bank%1:14:00::")
    res_order = generalizer.compute_taxonomic_modulation("order%1:26:00::")

    # Both activate structural order and justice fairness
    assert res_bank["applied_affinities"]["philosophical/structure/order"] > 0
    assert res_order["applied_affinities"]["philosophical/structure/order"] > 0
    assert res_bank["applied_affinities"]["cultural/justice/fairness"] > 0
    assert res_order["applied_affinities"]["cultural/justice/fairness"] > 0


def test_unregistered_sense_handling():
    """Unregistered sense keys gracefully return found=False without mutation."""
    generalizer = TaxonomicGeneralizer()
    res = generalizer.compute_taxonomic_modulation("unknown_sense%1:00:00::")
    assert res["found"] is False
    assert res["primary_category"] is None
    assert res["applied_affinities"] == {}
    for v in res["modulated_dials"].values():
        assert v == 0.50


def test_ordinary_memory_baseline_parity():
    """Primary generalizer and ordinary memory baseline achieve byte-for-byte digest parity (Rule D004)."""
    generalizer = TaxonomicGeneralizer()
    comparator = OrdinaryMemoryTaxonomicComparator()

    for sense_key in TAXONOMIC_REGISTRY.keys():
        primary_res = generalizer.compute_taxonomic_modulation(sense_key, weight=0.85)
        comparator_res = comparator.modulate(sense_key, weight=0.85)

        assert digest(primary_res) == digest(comparator_res)


def test_dynamic_lemma_extraction_and_alias_resolution():
    """Extracts open-world vocabulary and maps aliases to canonical hypernym senses."""
    generalizer = TaxonomicGeneralizer()

    # Dynamic extraction of registered concepts from natural text
    lemmas = generalizer.extract_lemmas("The library preserved truth and philosophical wisdom during the crisis.")
    assert "library" in lemmas
    assert "truth" in lemmas
    assert "crisis" in lemmas

    # Alias resolution to canonical sense
    res_lib = generalizer.compute_taxonomic_modulation("library")
    assert res_lib["found"] is True
    assert res_lib["primary_category"] == "knowledge_truth"
    assert res_lib["applied_affinities"]["psychological/truth/theory"] > 0

    res_crisis = generalizer.compute_taxonomic_modulation("crisis")
    assert res_crisis["found"] is True
    assert res_crisis["primary_category"] == "conflict_threat"
    assert res_crisis["applied_affinities"]["experiential/phase/arousal"] > 0


def test_comparator_extended_parity():
    """Comparator and generalizer achieve digest parity across aliases and sentences (Rule D004)."""
    generalizer = TaxonomicGeneralizer()
    comparator = OrdinaryMemoryTaxonomicComparator()

    test_words = ["library", "peace", "threat", "craft", "treaty", "bread", "freedom", "anomaly"]
    for word in test_words:
        p_res = generalizer.compute_taxonomic_modulation(word, weight=0.7)
        c_res = comparator.compute_taxonomic_modulation(word, weight=0.7)
        assert digest(p_res) == digest(c_res)

