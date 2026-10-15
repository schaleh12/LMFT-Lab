"""Unit tests for Unified Cognitive Heartbeat Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.cognitive_heartbeat import (
    CognitiveHeartbeat,
    OrdinaryMemoryHeartbeatComparator,
)
from lmft_lab.individual_package import export_individual, import_individual
from lmft_lab.runtime_store import digest


def test_canonical_seed_integrity():
    """Founding seed 40 nodes strictly unmutated (Rule D001)."""
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40
    leaf_nodes = [node_id for node_id, _, _, _, depth in seed_nodes if depth == 2]
    assert len(leaf_nodes) == 24


def test_waking_interaction_cycle():
    """Waking interact() cycle executes full multi-faculty cognitive pipeline."""
    heartbeat = CognitiveHeartbeat()

    res = heartbeat.interact("The national bank issued an executive credit guarantee.")

    assert res["cycle"] == 1
    assert "bank" in res["target_lemmas"]
    assert res["speaking_register"] == "Authoritative & Chivalrous"
    assert res["action_bid"] == "Execute financial transaction"
    assert len(res["coherence"]["distortions_detected"]) == 0
    assert res["coherence"]["global_coherence_index"] > 0.60
    assert res["plasticity"]["dynamic_alpha"] > 0.0
    assert "experiential/phase/arousal" in res["post_action_echo"]
    assert res["journal_result"]["admitted"] is True
    assert len(heartbeat.journal.entries) == 1


def test_epistemic_conflict_handling():
    """Cognitive conflict disruption triggers alarm posture and is journaled."""
    heartbeat = CognitiveHeartbeat()

    res = heartbeat.interact(
        sentence="Contradictory directives were simultaneously received.",
        target_lemmas=["order"],
        is_conflict=True,
    )

    assert res["cycle"] == 1
    assert res["action_bid"] == "Halt and issue clarification request"
    assert res["journal_result"]["admitted"] is True
    assert res["journal_result"]["episode"]["affective_snapshot"]["clarity"] <= 0.30
    assert "faced a cognitive conflict" in res["journal_result"]["episode"]["english_narrative_reflection"]


def test_sleep_consolidation_cycle():
    """Sleep cycle consolidates recurring patterns into long-term rules and relaxes disposition."""
    heartbeat = CognitiveHeartbeat(min_confirmations=2)

    # Two interactions with the same novel pattern
    heartbeat.interact("Wild ferns covered the river bank at sunset.", forced_senses={"bank": "river"})
    heartbeat.interact("Gentle moss grew on the river bank at dawn.", forced_senses={"bank": "river"})

    assert len(heartbeat.journal.entries) == 2
    initial_rule_count = len(heartbeat.consolidator.long_term_rules)

    # Sleep cycle
    sleep_res = heartbeat.sleep(prune_buffer=True)

    assert sleep_res["sleep_cycle"] == 1
    assert sleep_res["consolidation_summary"]["promoted_rules_count"] == 1
    assert sleep_res["active_long_term_rules"] == initial_rule_count + 1
    assert sleep_res["drift_result"]["steps"] == 1


def test_full_individual_package_export_import(tmp_path):
    """Complete developmental individual state exports, verifies, and imports with 100% fidelity."""
    heartbeat = CognitiveHeartbeat()
    heartbeat.interact("The national bank approved the new treaty.")
    heartbeat.interact("A formal court order was read aloud.")

    pkg_data = heartbeat.export_individual_package()
    pkg_file = tmp_path / "test_individual.lmft.json"

    # Export to verified file bundle
    export_individual(pkg_data, pkg_file, description="Test Developmental Snapshot")
    assert pkg_file.is_file()

    # Import back and verify integrity
    restored_raw = import_individual(pkg_file, verify_seed=True)
    assert restored_raw["individual_id"] == "lmft-individual-01"

    # Restore into fresh heartbeat instance
    restored_heartbeat = CognitiveHeartbeat()
    restored_heartbeat.import_individual_package(restored_raw)

    assert restored_heartbeat.cycle_count == 2
    assert len(restored_heartbeat.journal.entries) == 2
    assert len(restored_heartbeat.consolidator.long_term_rules) >= 2


def test_ordinary_memory_comparator_parity():
    """Primary cognitive heartbeat and ordinary memory comparator achieve byte-for-byte parity (Rule D004)."""
    heartbeat = CognitiveHeartbeat()
    comparator = OrdinaryMemoryHeartbeatComparator()

    sentences = [
        ("The national bank announced monetary reserves.", False),
        ("A court order was dispatched by royal messenger.", False),
        ("Conflicting orders threw the battalion into disarray.", True),
    ]

    for sent, conf in sentences:
        h_res = heartbeat.interact(sent, is_conflict=conf)
        c_res = comparator.interact(sent, is_conflict=conf)
        assert digest(h_res) == digest(c_res)

    h_sleep = heartbeat.sleep(prune_buffer=True)
    c_sleep = comparator.sleep(prune_buffer=True)
    assert digest(h_sleep) == digest(c_sleep)


def test_affective_homeostasis_in_heartbeat():
    """Verify heartbeat invokes AffectiveHomeostasisGovernor and buffers sudden shock."""
    heartbeat = CognitiveHeartbeat()

    # Induce massive sudden shock via custom dials
    res = heartbeat.interact(
        "A sudden catastrophic tremor shook the foundations.",
        custom_dials={"experiential/phase/arousal": 0.99, "experiential/phase/valence": 0.01},
    )

    assert "homeostasis" in res
    homeostasis = res["homeostasis"]
    assert homeostasis["interventions_count"] >= 1
    assert homeostasis["homeostatic_regime"] in ("Active Volatility Clamping", "Boundary Saturation Buffering")
    assert res["disposition_dials"]["experiential/phase/arousal"] < 0.99
    assert res["disposition_dials"]["experiential/phase/valence"] > 0.01


def test_value_consonance_in_heartbeat():
    """Verify heartbeat invokes ValueConsonanceEngine and triggers Curious Inquiry on novel lesson."""
    heartbeat = CognitiveHeartbeat()

    # Present completely novel lesson without conflict (unanchored lemma)
    res = heartbeat.interact(
        "Luminescent aurora particles danced across the high polar atmosphere.",
        custom_dials={"experiential/reflection/novelty": 0.85},
    )

    assert "consonance" in res
    consonance = res["consonance"]
    assert consonance["epistemic_mode"] == "Curious Inquiry"
    assert consonance["is_curious"] is True
    assert res["speaking_register"] == "Inquisitive & Contemplative"
    assert res["action_bid"] == "Explore and formulate inquisitive inquiry"
    assert consonance["consonance_index"] >= 0.80


def test_open_world_vocabulary_taxonomic_modulation():
    """Verify open-world sentences dynamically engage taxonomic hypernyms and preserve Rule D004 parity."""
    heartbeat = CognitiveHeartbeat()
    comparator = OrdinaryMemoryHeartbeatComparator()

    sentences = [
        "In the quiet library, philosophers debated the theory of truth.",
        "The sovereign decree enforced strict justice and lawful honor.",
        "A sudden enemy attack threatened the fortress in war.",
        "Gentle friends shared warm bread by the hearth in peace.",
    ]

    for sent in sentences:
        h_res = heartbeat.interact(sent)
        c_res = comparator.interact(sent)

        # Confirm lemmas extracted and modulated
        assert len(h_res["target_lemmas"]) > 0
        assert len(h_res["taxonomic_modulations"]) > 0
        assert len(h_res["coherence"]["distortions_detected"]) == 0
        assert h_res["coherence"]["global_coherence_index"] > 0.50

        # Rule D004 byte-for-byte baseline parity
        assert digest(h_res) == digest(c_res)



