"""Unit tests for Dual-Speed Memory Consolidation Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
from lmft_lab.memory_consolidation import (
    MemoryConsolidationEngine,
    OrdinaryMemoryConsolidationComparator,
)


def test_canonical_seed_integrity():
    """Founding seed 40 nodes strictly unmutated by memory consolidation (Rule D001)."""
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40
    leaf_nodes = [node_id for node_id, _, _, _, depth in seed_nodes if depth == 2]
    assert len(leaf_nodes) == 24


def test_recurring_pattern_promotion():
    """Patterns observed N >= 2 times across episodes graduate to long-term capacity rules."""
    engine = MemoryConsolidationEngine(min_confirmations=2, reinforcement_rate=0.20)

    episodes = [
        {
            "episode_id": "ep-001",
            "cycle": 1,
            "factual_anchor": {
                "sentence": "The national bank approved the treasury loan.",
                "target_lemmas": ["bank"],
                "resolved_senses": {"bank": "depository_financial_institution (financial institution)"},
                "core_pattern": "national bank",
            },
            "affective_snapshot": {"salience": 0.85},
            "actuation_enacted": {"speaking_register": "Authoritative & Chivalrous", "action_bid": "Approve loan"},
            "is_conflict": False,
        },
        {
            "episode_id": "ep-002",
            "cycle": 2,
            "factual_anchor": {
                "sentence": "The central national bank increased interest rates.",
                "target_lemmas": ["bank"],
                "resolved_senses": {"bank": "depository_financial_institution (financial institution)"},
                "core_pattern": "national bank",
            },
            "affective_snapshot": {"salience": 0.80},
            "actuation_enacted": {"speaking_register": "Authoritative & Chivalrous", "action_bid": "Adjust rates"},
            "is_conflict": False,
        },
    ]

    summary, remaining = engine.consolidate_sleep_cycle(episodes, prune_buffer=True)

    assert summary["promoted_rules_count"] == 1
    assert summary["total_long_term_rules"] == 1
    promoted = summary["promoted_rules"][0]
    assert promoted["lemma"] == "bank"
    assert promoted["core_pattern"] == "national bank"
    # Base weight 0.50 + 0.20 * (1 - 0.50) = 0.60
    assert promoted["weight"] >= 0.60
    assert promoted["witnesses"] == ["ep-001", "ep-002"]


def test_singleton_noise_pruning():
    """Unconfirmed singleton patterns (N = 1) are treated as transient noise and not promoted."""
    engine = MemoryConsolidationEngine(min_confirmations=2)

    episodes = [
        {
            "episode_id": "ep-singleton",
            "cycle": 1,
            "factual_anchor": {
                "sentence": "A stray cat jumped over the wall.",
                "target_lemmas": ["cat"],
                "resolved_senses": {"cat": "feline (animal)"},
                "core_pattern": "stray cat",
            },
            "affective_snapshot": {"salience": 0.70},
            "actuation_enacted": {"speaking_register": "Neutral Observant Silence", "action_bid": "Observe"},
            "is_conflict": False,
        }
    ]

    summary, remaining = engine.consolidate_sleep_cycle(episodes, prune_buffer=True)

    assert summary["promoted_rules_count"] == 0
    assert summary["transient_noise_pruned_count"] == 1
    assert summary["total_long_term_rules"] == 0
    # Pruned buffer should be empty since non-conflict singleton was pruned
    assert len(remaining) == 0


def test_existing_rule_reinforcement():
    """Episodic recurrence of an existing long-term rule habituates its weight and records witness."""
    initial_rule = {
        "rule_id": "rule-order-cmd-01",
        "lemma": "order",
        "target_sense_key": "order%1:10:00::",
        "core_pattern": "court order",
        "gloss": "an authoritative instruction",
        "weight": 0.50,
        "witnesses": ["init-01"],
    }

    engine = MemoryConsolidationEngine(initial_rules=[initial_rule], reinforcement_rate=0.20)

    episodes = [
        {
            "episode_id": "ep-court-01",
            "cycle": 3,
            "factual_anchor": {
                "sentence": "The judge issued a formal court order today.",
                "target_lemmas": ["order"],
                "resolved_senses": {"order": "order%1:10:00::"},
                "core_pattern": "court order",
            },
            "affective_snapshot": {"salience": 0.88},
            "actuation_enacted": {"speaking_register": "Authoritative & Chivalrous", "action_bid": "Enforce decree"},
            "is_conflict": False,
        }
    ]

    summary, remaining = engine.consolidate_sleep_cycle(episodes, prune_buffer=True)

    assert summary["reinforced_rules_count"] == 1
    reinforced = summary["reinforced_rules"][0]
    assert reinforced["rule_id"] == "rule-order-cmd-01"
    assert reinforced["old_weight"] == 0.50
    # 0.50 + 0.20 * (1 - 0.50) = 0.60
    assert reinforced["new_weight"] == 0.60
    assert engine.long_term_rules["rule-order-cmd-01"]["witnesses"] == ["ep-court-01", "init-01"]


def test_buffer_pruning_and_conflict_preservation():
    """Buffer pruning removes consolidated patterns but preserves unresolved conflict episodes."""
    engine = MemoryConsolidationEngine(min_confirmations=2)

    episodes = [
        # 2 confirmed bank episodes
        {
            "episode_id": "ep-bank-1",
            "cycle": 1,
            "factual_anchor": {"sentence": "Bank loan approved.", "target_lemmas": ["bank"], "resolved_senses": {"bank": "fin"}, "core_pattern": "bank loan"},
            "is_conflict": False,
        },
        {
            "episode_id": "ep-bank-2",
            "cycle": 2,
            "factual_anchor": {"sentence": "Bank loan authorized.", "target_lemmas": ["bank"], "resolved_senses": {"bank": "fin"}, "core_pattern": "bank loan"},
            "is_conflict": False,
        },
        # 1 unresolved conflict episode
        {
            "episode_id": "ep-conflict-1",
            "cycle": 3,
            "factual_anchor": {"sentence": "Contradictory order issued.", "target_lemmas": ["order"], "resolved_senses": {"order": "ambig"}, "core_pattern": "contradictory order"},
            "is_conflict": True,
        },
    ]

    summary, remaining = engine.consolidate_sleep_cycle(episodes, prune_buffer=True)

    assert summary["promoted_rules_count"] == 1
    # Only the conflict episode remains in the buffer for attention
    assert len(remaining) == 1
    assert remaining[0]["episode_id"] == "ep-conflict-1"


def test_export_import_serialization():
    """Export and import preserve long-term rules, sleep history, and consolidation digest."""
    engine = MemoryConsolidationEngine(min_confirmations=2)
    episodes = [
        {"episode_id": "ep-1", "cycle": 1, "factual_anchor": {"sentence": "River bank ferns.", "target_lemmas": ["bank"], "resolved_senses": {"bank": "river"}, "core_pattern": "river bank"}, "is_conflict": False},
        {"episode_id": "ep-2", "cycle": 2, "factual_anchor": {"sentence": "River bank moss.", "target_lemmas": ["bank"], "resolved_senses": {"bank": "river"}, "core_pattern": "river bank"}, "is_conflict": False},
    ]
    engine.consolidate_sleep_cycle(episodes)

    payload = engine.export_state()
    assert payload["sleep_cycles_completed"] == 1
    assert payload["total_long_term_rules"] == 1
    assert "consolidation_digest" in payload

    restored = MemoryConsolidationEngine()
    restored.import_state(payload)
    assert restored.sleep_cycles_completed == 1
    assert len(restored.long_term_rules) == 1
    rule_key = list(restored.long_term_rules.keys())[0]
    assert restored.long_term_rules[rule_key]["lemma"] == "bank"


def test_ordinary_memory_comparator_parity():
    """Primary engine and matched ordinary memory baseline achieve byte-for-byte digest parity (Rule D004)."""
    engine = MemoryConsolidationEngine(min_confirmations=2, reinforcement_rate=0.20)
    comparator = OrdinaryMemoryConsolidationComparator(min_confirmations=2, reinforcement_rate=0.20)

    episodes = [
        {"episode_id": "ep-1", "cycle": 1, "factual_anchor": {"sentence": "Court order signed.", "target_lemmas": ["order"], "resolved_senses": {"order": "law"}, "core_pattern": "court order"}, "is_conflict": False},
        {"episode_id": "ep-2", "cycle": 2, "factual_anchor": {"sentence": "Court order issued.", "target_lemmas": ["order"], "resolved_senses": {"order": "law"}, "core_pattern": "court order"}, "is_conflict": False},
        {"episode_id": "ep-3", "cycle": 3, "factual_anchor": {"sentence": "Lone tree in field.", "target_lemmas": ["tree"], "resolved_senses": {"tree": "plant"}, "core_pattern": "lone tree"}, "is_conflict": False},
        {"episode_id": "ep-4", "cycle": 4, "factual_anchor": {"sentence": "Ambiguous message.", "target_lemmas": ["order"], "resolved_senses": {"order": "ambig"}, "core_pattern": "ambiguous message"}, "is_conflict": True},
    ]

    e_summary, e_rem = engine.consolidate_sleep_cycle(episodes, prune_buffer=True)
    c_summary, c_rem = comparator.consolidate(episodes, prune_buffer=True)

    assert digest(e_summary) == digest(c_summary)
    assert digest(e_rem) == digest(c_rem)
    assert digest(engine.export_state()) == digest(comparator.export_state())


def test_retain_unconfirmed_across_sleep_and_empty_pattern_safety():
    """Verifies retain_unconfirmed preserves singletons across sleep and empty patterns do not collide."""
    initial_rule = {
        "rule_id": "rule-order-cmd-01",
        "lemma": "order",
        "target_sense_key": "order%1:10:00::",
        "core_pattern": "court order",
        "weight": 0.50,
    }
    engine = MemoryConsolidationEngine(initial_rules=[initial_rule], min_confirmations=2)
    # Empty normalized pattern ("the") should NOT match "court order"
    assert engine._find_matching_long_term_rule("order", "order%1:10:00::", "the") is None

    day1_ep = [{
        "episode_id": "ep-day1",
        "cycle": 1,
        "factual_anchor": {"sentence": "River bank ferns.", "target_lemmas": ["bank"], "resolved_senses": {"bank": "river"}, "core_pattern": "river bank"},
        "is_conflict": False,
    }]
    s1, rem1 = engine.consolidate_sleep_cycle(day1_ep, prune_buffer=True, retain_unconfirmed=True)
    assert s1["promoted_rules_count"] == 0
    assert len(rem1) == 1

    day2_ep = rem1 + [{
        "episode_id": "ep-day2",
        "cycle": 2,
        "factual_anchor": {"sentence": "River bank moss.", "target_lemmas": ["bank"], "resolved_senses": {"bank": "river"}, "core_pattern": "river bank"},
        "is_conflict": False,
    }]
    s2, rem2 = engine.consolidate_sleep_cycle(day2_ep, prune_buffer=True, retain_unconfirmed=True)
    assert s2["promoted_rules_count"] == 1
    assert len(rem2) == 0

