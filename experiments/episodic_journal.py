"""Dual-Coded Episodic Saliency Journal Benchmark.

Evaluates autobiographical memory recording, saliency admission gating, dual-coded narrative reflection,
and precedent retrieval across 6 standardized test scenarios:
1. Sovereign Financial Action (High Salience -> Admitted)
2. Mundane Ambient Observation (Sub-threshold -> Rejected)
3. Cognitive Conflict Disruption (Disruption -> Admitted, Conflict Narrative)
4. River Collocation Discovery (High Novelty -> Admitted)
5. Tactical Order Execution (High Salience -> Admitted)
6. Precedent Primed Query (Recall accuracy across history)

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.episodic_journal import (
    EpisodicSaliencyJournal,
    OrdinaryMemoryJournalComparator,
    SALIENCY_ADMISSION_THRESHOLD,
    NOVELTY_SURPRISE_THRESHOLD,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "episodic-journal-benchmark-1"

BENCHMARK_SCENARIOS = [
    {
        "cycle": 1,
        "scenario_id": "sovereign_financial_action",
        "description": "High salience (0.85) transaction enacting Authoritative & Chivalrous posture",
        "sentence": "The national bank issued an executive financial guarantee for the treasury.",
        "target_lemmas": ["bank"],
        "resolved_senses": {"bank": "depository_financial_institution (financial institution)"},
        "leaf_dials": {
            "experiential/reflection/salience": 0.85,
            "experiential/reflection/novelty": 0.60,
            "experiential/phase/arousal": 0.65,
            "experiential/phase/valence": 0.70,
            "psychological/contemplation/clarity": 0.90,
            "philosophical/structure/order": 0.88,
        },
        "speaking_register": "Authoritative & Chivalrous",
        "action_bid": "Execute sovereign treasury guarantee",
        "is_conflict": False,
        "expected_admission": True,
    },
    {
        "cycle": 2,
        "scenario_id": "mundane_ambient_observation",
        "description": "Sub-threshold ambient observation (salience 0.45, novelty 0.40) filtered out",
        "sentence": "A stray leaf drifted quietly across the cobblestone pathway.",
        "target_lemmas": ["leaf"],
        "resolved_senses": {"leaf": "foliage_part (plant structure)"},
        "leaf_dials": {
            "experiential/reflection/salience": 0.45,
            "experiential/reflection/novelty": 0.40,
            "experiential/phase/arousal": 0.40,
            "experiential/phase/valence": 0.50,
            "psychological/contemplation/clarity": 0.60,
            "philosophical/structure/order": 0.50,
        },
        "speaking_register": "Neutral Observant Silence",
        "action_bid": "Observe passively",
        "is_conflict": False,
        "expected_admission": False,
    },
    {
        "cycle": 3,
        "scenario_id": "cognitive_conflict_disruption",
        "description": "Epistemic conflict with low clarity (0.25) admitted as alarmed narrative",
        "sentence": "The contradictory edict commanded immediate retreat while demanding holding ground.",
        "target_lemmas": ["order"],
        "resolved_senses": {"order": "ambiguous_conflict"},
        "leaf_dials": {
            "experiential/reflection/salience": 0.55,
            "experiential/reflection/novelty": 0.65,
            "experiential/phase/arousal": 0.80,
            "experiential/phase/valence": 0.25,
            "psychological/contemplation/clarity": 0.25,
            "philosophical/structure/order": 0.30,
        },
        "speaking_register": "Methodical & Pragmatic",
        "action_bid": "Halt and issue clarification request",
        "is_conflict": True,
        "expected_admission": True,
    },
    {
        "cycle": 4,
        "scenario_id": "river_collocation_discovery",
        "description": "High novelty (0.85) natural landscape discovery admitted to journal",
        "sentence": "Wild ferns flourished along the gentle river bank in the morning mist.",
        "target_lemmas": ["bank"],
        "resolved_senses": {"bank": "sloping_land (river bank)"},
        "leaf_dials": {
            "experiential/reflection/salience": 0.58,
            "experiential/reflection/novelty": 0.85,
            "experiential/phase/arousal": 0.55,
            "experiential/phase/valence": 0.75,
            "psychological/contemplation/clarity": 0.85,
            "philosophical/structure/order": 0.70,
        },
        "speaking_register": "Communal & Reassuring",
        "action_bid": "Record environmental ecology",
        "is_conflict": False,
        "expected_admission": True,
    },
    {
        "cycle": 5,
        "scenario_id": "tactical_order_execution",
        "description": "High salience (0.78) procedural execution admitted to journal",
        "sentence": "The commander established strict chronological order for the tactical deployment.",
        "target_lemmas": ["order"],
        "resolved_senses": {"order": "sequence_arrangement (order)"},
        "leaf_dials": {
            "experiential/reflection/salience": 0.78,
            "experiential/reflection/novelty": 0.50,
            "experiential/phase/arousal": 0.60,
            "experiential/phase/valence": 0.65,
            "psychological/contemplation/clarity": 0.92,
            "philosophical/structure/order": 0.95,
        },
        "speaking_register": "Methodical & Pragmatic",
        "action_bid": "Enforce sequential arrangement",
        "is_conflict": False,
        "expected_admission": True,
    },
]


def run_episodic_journal_study(output_dir=None):
    """Executes episodic journal benchmark and verifies baseline parity across scenarios."""
    journal = EpisodicSaliencyJournal(capacity=10)
    comparator = OrdinaryMemoryJournalComparator(capacity=10)

    results = []
    parity_passed = True

    for scen in BENCHMARK_SCENARIOS:
        j_res = journal.record_episode(
            cycle=scen["cycle"],
            sentence=scen["sentence"],
            target_lemmas=scen["target_lemmas"],
            resolved_senses=scen["resolved_senses"],
            leaf_dials=scen["leaf_dials"],
            speaking_register=scen["speaking_register"],
            action_bid=scen["action_bid"],
            is_conflict=scen["is_conflict"],
        )
        c_res = comparator.record(
            cycle=scen["cycle"],
            sentence=scen["sentence"],
            target_lemmas=scen["target_lemmas"],
            resolved_senses=scen["resolved_senses"],
            leaf_dials=scen["leaf_dials"],
            speaking_register=scen["speaking_register"],
            action_bid=scen["action_bid"],
            is_conflict=scen["is_conflict"],
        )

        if digest(j_res) != digest(c_res):
            parity_passed = False

        results.append({
            "cycle": scen["cycle"],
            "scenario_id": scen["scenario_id"],
            "admitted": j_res["admitted"],
            "reason": j_res["reason"],
            "episode": j_res["episode"],
            "digest": digest(j_res),
        })

    # Precedent recall scenario (Recall 'bank' and 'order')
    bank_precedents = journal.recall_precedents("bank", limit=3)
    order_precedents = journal.recall_precedents("order", limit=3)
    comp_bank_precedents = comparator.recall("bank", limit=3)
    comp_order_precedents = comparator.recall("order", limit=3)

    if digest(bank_precedents) != digest(comp_bank_precedents) or digest(order_precedents) != digest(comp_order_precedents):
        parity_passed = False

    # Export serialization check
    j_export = journal.export_journal()
    c_export = comparator.export_journal()
    if digest(j_export) != digest(c_export):
        parity_passed = False

    # Rule D001 verification
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40, f"Seed corrupted: expected 40 nodes, found {len(seed_nodes)}"

    summary = {
        "kind": KIND,
        "total_episodes_evaluated": len(BENCHMARK_SCENARIOS),
        "total_episodes_admitted": journal.total_episodes_recorded,
        "current_buffer_length": len(journal.entries),
        "consumer_parity": parity_passed,
        "frozen_seed_invariant_enforced": True,
        "evaluation_digest": digest(results),
        "precedent_recall": {
            "bank_count": len(bank_precedents),
            "order_count": len(order_precedents),
            "most_recent_bank_cycle": bank_precedents[0]["cycle"] if bank_precedents else None,
            "most_recent_order_cycle": order_precedents[0]["cycle"] if order_precedents else None,
        },
        "results": results,
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "episodic-journal-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Dual-Coded Episodic Saliency Journal Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_episodic_journal_study(output_dir=args.output_dir)

    print("\n=== Dual-Coded Episodic Saliency Journal Benchmark ===")
    print(f"Total Episodes Evaluated: {summary['total_episodes_evaluated']}")
    print(f"Total Episodes Admitted: {summary['total_episodes_admitted']}")
    print(f"Buffer Length (FIFO): {summary['current_buffer_length']}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['frozen_seed_invariant_enforced']}")
    print(f"Evaluation Digest: {summary['evaluation_digest'][:16]}...")
    print("======================================================\n")


if __name__ == "__main__":
    main()
