"""Unit tests for Dual-Coded Episodic Saliency Journal Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest
from lmft_lab.episodic_journal import (
    CANONICAL_LEAF_IDS,
    SALIENCY_ADMISSION_THRESHOLD,
    NOVELTY_SURPRISE_THRESHOLD,
    EpisodicSaliencyJournal,
    OrdinaryMemoryJournalComparator,
)


def test_canonical_seed_integrity():
    """All leaf attributes referenced in episodic journal exist in the frozen founding seed (Rule D001)."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    assert len(inventory_leaf_ids) == 24
    assert CANONICAL_LEAF_IDS == inventory_leaf_ids

    monitored_leaves = {
        "experiential/reflection/salience",
        "experiential/reflection/novelty",
        "experiential/phase/arousal",
        "experiential/phase/valence",
        "psychological/contemplation/clarity",
        "philosophical/structure/order",
    }
    for leaf in monitored_leaves:
        assert leaf in inventory_leaf_ids


def test_saliency_admission_gate():
    """Events below saliency and novelty thresholds without conflict are rejected to prevent bloat."""
    journal = EpisodicSaliencyJournal(capacity=10)

    # Sub-threshold mundane event
    mundane_dials = {
        "experiential/reflection/salience": 0.50,
        "experiential/reflection/novelty": 0.50,
        "experiential/phase/arousal": 0.50,
        "psychological/contemplation/clarity": 0.50,
    }
    res1 = journal.record_episode(
        cycle=1,
        sentence="The bird sat quietly on the branch.",
        target_lemmas=["bird"],
        resolved_senses={"bird": "animal 01"},
        leaf_dials=mundane_dials,
        speaking_register="Neutral Observant Silence",
        action_bid="Observe passively",
    )
    assert res1["admitted"] is False
    assert len(journal.entries) == 0

    # High salience event
    salient_dials = dict(mundane_dials)
    salient_dials["experiential/reflection/salience"] = 0.75
    res2 = journal.record_episode(
        cycle=2,
        sentence="The bank issued a strict sovereign directive.",
        target_lemmas=["bank"],
        resolved_senses={"bank": "financial_institution 01"},
        leaf_dials=salient_dials,
        speaking_register="Authoritative & Chivalrous",
        action_bid="Enact sovereign decree",
    )
    assert res2["admitted"] is True
    assert len(journal.entries) == 1

    # Conflict event with low clarity
    conflict_dials = dict(mundane_dials)
    conflict_dials["psychological/contemplation/clarity"] = 0.20
    res3 = journal.record_episode(
        cycle=3,
        sentence="Ambiguous input triggered conflicting evidence.",
        target_lemmas=["order"],
        resolved_senses={"order": "ambiguous"},
        leaf_dials=conflict_dials,
        speaking_register="Methodical & Pragmatic",
        action_bid="Request clarification",
        is_conflict=True,
    )
    assert res3["admitted"] is True
    assert len(journal.entries) == 2


def test_dual_coded_entry_structure_and_synthesis():
    """Admitted episodes contain 24-leaf math and coherent English narrative reflection."""
    journal = EpisodicSaliencyJournal(capacity=10)
    dials = {
        "experiential/reflection/salience": 0.80,
        "experiential/reflection/novelty": 0.72,
        "experiential/phase/arousal": 0.65,
        "experiential/phase/valence": 0.70,
        "psychological/contemplation/clarity": 0.85,
        "philosophical/structure/order": 0.90,
    }

    res = journal.record_episode(
        cycle=5,
        sentence="He deposited gold into the bank vault.",
        target_lemmas=["bank"],
        resolved_senses={"bank": "depository_financial_institution (financial institution)"},
        leaf_dials=dials,
        speaking_register="Methodical & Pragmatic",
        action_bid="Commit transaction",
    )

    assert res["admitted"] is True
    ep = res["episode"]
    assert ep["cycle"] == 5
    assert ep["factual_anchor"]["sentence"] == "He deposited gold into the bank vault."
    assert ep["factual_anchor"]["target_lemmas"] == ["bank"]
    assert ep["affective_snapshot"]["salience"] == 0.80
    assert ep["affective_snapshot"]["order"] == 0.90
    assert ep["actuation_enacted"]["speaking_register"] == "Methodical & Pragmatic"
    assert "Cycle 5: I resolved 'bank'" in ep["english_narrative_reflection"]
    assert "Methodical & Pragmatic" in ep["english_narrative_reflection"]


def test_bounded_capacity_ring_buffer():
    """Buffer strictly respects maximum capacity and evicts oldest entries FIFO."""
    journal = EpisodicSaliencyJournal(capacity=3)
    salient_dials = {"experiential/reflection/salience": 0.80}

    for i in range(1, 6):
        journal.record_episode(
            cycle=i,
            sentence=f"Sentence {i}",
            target_lemmas=[f"lemma_{i}"],
            resolved_senses={f"lemma_{i}": f"sense_{i}"},
            leaf_dials=salient_dials,
            speaking_register="Register",
            action_bid="Bid",
        )

    assert len(journal.entries) == 3
    assert journal.total_episodes_recorded == 5
    # Oldest entries 1 and 2 should have been evicted; remaining should be 3, 4, 5
    cycles = [ep["cycle"] for ep in journal.entries]
    assert cycles == [3, 4, 5]


def test_precedent_recall():
    """Precedent retrieval recalls relevant episodes in reverse chronological order."""
    journal = EpisodicSaliencyJournal(capacity=10)
    salient_dials = {"experiential/reflection/salience": 0.80}

    journal.record_episode(1, "The bank issued loans.", ["bank"], {"bank": "financial"}, salient_dials, "Reg", "Bid")
    journal.record_episode(2, "The king gave an order.", ["order"], {"order": "decree"}, salient_dials, "Reg", "Bid")
    journal.record_episode(3, "The river bank was muddy.", ["bank"], {"bank": "sloping land"}, salient_dials, "Reg", "Bid")

    recalled = journal.recall_precedents("bank", limit=2)
    assert len(recalled) == 2
    assert recalled[0]["cycle"] == 3
    assert recalled[1]["cycle"] == 1


def test_export_import_serialization():
    """Export and import preserve state fidelity and calculate deterministic digest."""
    journal = EpisodicSaliencyJournal(capacity=5)
    salient_dials = {"experiential/reflection/salience": 0.80}
    journal.record_episode(1, "Text 1", ["l1"], {"l1": "s1"}, salient_dials, "Reg1", "Bid1")
    journal.record_episode(2, "Text 2", ["l2"], {"l2": "s2"}, salient_dials, "Reg2", "Bid2")

    payload = journal.export_journal()
    assert payload["total_episodes_recorded"] == 2
    assert payload["current_buffer_length"] == 2
    assert "journal_digest" in payload

    restored = EpisodicSaliencyJournal()
    restored.import_journal(payload)
    assert restored.capacity == 5
    assert restored.total_episodes_recorded == 2
    assert len(restored.entries) == 2
    assert restored.entries[0]["cycle"] == 1
    assert restored.entries[1]["cycle"] == 2


def test_ordinary_memory_comparator_parity():
    """Primary journal and ordinary structured memory comparator achieve byte-for-byte digest parity (Rule D004)."""
    journal = EpisodicSaliencyJournal(capacity=5)
    comparator = OrdinaryMemoryJournalComparator(capacity=5)

    test_events = [
        (1, "Mundane event", ["dog"], {"dog": "canine"}, {"experiential/reflection/salience": 0.40}, "Reg", "Bid", False),
        (2, "High salience", ["bank"], {"bank": "fin"}, {"experiential/reflection/salience": 0.85, "psychological/contemplation/clarity": 0.90}, "Reg", "Bid", False),
        (3, "Conflict event", ["order"], {"order": "ambig"}, {"experiential/reflection/salience": 0.50, "psychological/contemplation/clarity": 0.20}, "Reg", "Bid", True),
        (4, "High novelty", ["cat"], {"cat": "feline"}, {"experiential/reflection/novelty": 0.88, "experiential/reflection/salience": 0.55}, "Reg", "Bid", False),
    ]

    for cycle, sent, lemmas, senses, dials, reg, bid, is_conf in test_events:
        j_res = journal.record_episode(
            cycle=cycle,
            sentence=sent,
            target_lemmas=lemmas,
            resolved_senses=senses,
            leaf_dials=dials,
            speaking_register=reg,
            action_bid=bid,
            is_conflict=is_conf,
        )
        c_res = comparator.record(
            cycle=cycle,
            sentence=sent,
            target_lemmas=lemmas,
            resolved_senses=senses,
            leaf_dials=dials,
            speaking_register=reg,
            action_bid=bid,
            is_conflict=is_conf,
        )
        assert digest(j_res) == digest(c_res)

    assert digest(journal.export_journal()) == digest(comparator.export_journal())
