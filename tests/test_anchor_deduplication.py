"""Unit tests for Anchor Normalization & Deduplication Engine.

Verifies:
1. Deterministic stripping of leading/trailing determiners, articles, and punctuation.
2. Grouping and merging of candidate proposals sharing identical canonical anchors.
3. Witness aggregation and confidence weight reinforcement on duplicate confirmations.
4. Matched ordinary-memory baseline parity (Rule D004).
5. Invariance of canonical 40 founding nodes in birth.py (Rule D001).
"""
import pytest
from lmft_lab.birth import _inventory
from lmft_lab.anchor_deduplication import (
    normalize_anchor_text,
    merge_duplicate_rules,
    deduplicate_rules,
    OrdinaryMemoryDeduplicationComparator,
)
from lmft_lab.runtime_store import digest


def test_normalize_anchor_text_variations():
    """Verifies that diverse surface phrasings reduce to identical canonical anchors."""
    assert normalize_anchor_text("The commercial bank.") == "commercial bank"
    assert normalize_anchor_text("a commercial bank") == "commercial bank"
    assert normalize_anchor_text("their commercial bank!") == "commercial bank"
    assert normalize_anchor_text("  commercial bank  ") == "commercial bank"
    assert normalize_anchor_text("a strict court order") == "strict court order"
    assert normalize_anchor_text("the river bank") == "river bank"
    assert normalize_anchor_text("Order & Chaos") == "order chaos"
    assert normalize_anchor_text("A - B / C") == "b c"
    assert normalize_anchor_text(normalize_anchor_text("The Sovereign & The Hearth - A")) == normalize_anchor_text("The Sovereign & The Hearth - A")


def test_merge_duplicate_rules_aggregation():
    """Verifies that merging duplicate candidates unions witnesses and reinforces weight."""
    r1 = {
        "rule_id": "rule-01",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:00::",
        "core_pattern": "the commercial bank",
        "gloss": "short gloss",
        "witnesses": ["witness-a", "witness-b"],
        "weight": 0.50,
    }
    r2 = {
        "rule_id": "rule-02",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:00::",
        "core_pattern": "commercial bank.",
        "gloss": "a significantly richer explanatory gloss for commercial bank",
        "witnesses": ["witness-b", "witness-c"],
        "weight": 0.50,
    }
    
    merged = merge_duplicate_rules([r1, r2])
    
    assert merged["core_pattern"] == "commercial bank"
    assert merged["witnesses"] == ["witness-a", "witness-b", "witness-c"]
    assert merged["gloss"] == "a significantly richer explanatory gloss for commercial bank"
    assert merged["merge_count"] == 2
    # Weight reinforced: 0.50 + 0.15 * (1 - 0.50) = 0.575
    assert merged["weight"] == 0.575


def test_deduplicate_rules_full_set():
    """Verifies deduplication across a full set of candidate rules containing duplicates."""
    candidates = [
        # Duplicate pair 1 (commercial bank)
        {"rule_id": "c1", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "the commercial bank", "gloss": "g1", "witnesses": ["w1"]},
        {"rule_id": "c2", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "commercial bank", "gloss": "g2", "witnesses": ["w2"]},
        # Duplicate pair 2 (court order)
        {"rule_id": "c3", "lemma": "order", "target_sense_key": "order%1:10:00::", "core_pattern": "a court order", "gloss": "g3", "witnesses": ["w3"]},
        {"rule_id": "c4", "lemma": "order", "target_sense_key": "order%1:10:00::", "core_pattern": "the court order.", "gloss": "g4", "witnesses": ["w4"]},
        # Unique rule (river bank)
        {"rule_id": "c5", "lemma": "bank", "target_sense_key": "bank%1:17:01::", "core_pattern": "river bank", "gloss": "g5", "witnesses": ["w5"]},
    ]
    
    canonical, stats = deduplicate_rules(candidates)
    
    assert stats["initial_candidates_count"] == 5
    assert stats["canonical_rules_count"] == 3
    assert stats["duplicates_merged"] == 2
    assert len(canonical) == 3


def test_ordinary_memory_baseline_parity():
    """Verifies byte-for-byte evaluation parity with the matched ordinary-memory comparator (Rule D004)."""
    comparator = OrdinaryMemoryDeduplicationComparator()
    
    candidates = [
        {"rule_id": "c1", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "the commercial bank", "gloss": "g1", "witnesses": ["w1"]},
        {"rule_id": "c2", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "commercial bank", "gloss": "g2", "witnesses": ["w2"]},
        {"rule_id": "c3", "lemma": "order", "target_sense_key": "order%1:10:00::", "core_pattern": "court order", "gloss": "g3", "witnesses": ["w3"]},
    ]
    
    p_rules, p_stats = deduplicate_rules(candidates)
    c_rules, c_stats = comparator.deduplicate(candidates)
    
    assert digest(p_rules) == digest(c_rules)
    assert digest(p_stats) == digest(c_stats)


def test_frozen_seed_invariant_preserved():
    """Verifies that the canonical 40 founding nodes in birth.py remain strictly invariant (Rule D001)."""
    inventory = list(_inventory())
    assert len(inventory) == 40
    domains = {item[2] for item in inventory}
    assert domains == {"cultural", "philosophical", "experiential", "psychological"}
