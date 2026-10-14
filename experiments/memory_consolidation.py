"""Dual-Speed Memory Consolidation Benchmark ("Sleep / Replay").

Evaluates hippocampal-style offline memory consolidation:
- Replays episodic memories across consecutive sleep cycles.
- Promotes recurring patterns (N >= 2) into persistent long-term capacity rules.
- Habituates/reinforces existing capacity rules upon recurrence.
- Prunes transient singleton noise while preserving unresolved conflicts.

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
from lmft_lab.memory_consolidation import (
    MemoryConsolidationEngine,
    OrdinaryMemoryConsolidationComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "memory-consolidation-benchmark-1"

INITIAL_RULES = [
    {
        "rule_id": "rule-order-cmd-01",
        "lemma": "order",
        "target_sense_key": "order%1:10:00::",
        "core_pattern": "court order",
        "gloss": "an authoritative instruction or judicial decree",
        "weight": 0.50,
        "witnesses": ["genesis-01"],
    }
]

SLEEP_CYCLE_1_EPISODES = [
    {
        "episode_id": "ep-001",
        "cycle": 1,
        "factual_anchor": {
            "sentence": "The national bank issued an executive guarantee for the treasury.",
            "target_lemmas": ["bank"],
            "resolved_senses": {"bank": "depository_financial_institution (financial institution)"},
            "core_pattern": "national bank",
        },
        "affective_snapshot": {"salience": 0.85, "clarity": 0.90, "arousal": 0.60},
        "actuation_enacted": {"speaking_register": "Authoritative & Chivalrous", "action_bid": "Execute guarantee"},
        "is_conflict": False,
    },
    {
        "episode_id": "ep-002",
        "cycle": 2,
        "factual_anchor": {
            "sentence": "The local national bank branch opened downtown.",
            "target_lemmas": ["bank"],
            "resolved_senses": {"bank": "depository_financial_institution (financial institution)"},
            "core_pattern": "national bank",
        },
        "affective_snapshot": {"salience": 0.80, "clarity": 0.88, "arousal": 0.55},
        "actuation_enacted": {"speaking_register": "Methodical & Pragmatic", "action_bid": "Record branch"},
        "is_conflict": False,
    },
    {
        "episode_id": "ep-003",
        "cycle": 3,
        "factual_anchor": {
            "sentence": "A formal court order was served to the witness.",
            "target_lemmas": ["order"],
            "resolved_senses": {"order": "order%1:10:00::"},
            "core_pattern": "court order",
        },
        "affective_snapshot": {"salience": 0.88, "clarity": 0.92, "arousal": 0.65},
        "actuation_enacted": {"speaking_register": "Authoritative & Chivalrous", "action_bid": "Serve writ"},
        "is_conflict": False,
    },
    {
        "episode_id": "ep-004",
        "cycle": 4,
        "factual_anchor": {
            "sentence": "A single wandering sparrow chirped atop the fence.",
            "target_lemmas": ["sparrow"],
            "resolved_senses": {"sparrow": "passerine (bird)"},
            "core_pattern": "wandering sparrow",
        },
        "affective_snapshot": {"salience": 0.68, "clarity": 0.70, "arousal": 0.40},
        "actuation_enacted": {"speaking_register": "Neutral Observant Silence", "action_bid": "Observe"},
        "is_conflict": False,
    },
    {
        "episode_id": "ep-005",
        "cycle": 5,
        "factual_anchor": {
            "sentence": "The commander received a contradictory order regarding troop movements.",
            "target_lemmas": ["order"],
            "resolved_senses": {"order": "ambiguous_conflict"},
            "core_pattern": "contradictory order",
        },
        "affective_snapshot": {"salience": 0.75, "clarity": 0.25, "arousal": 0.80},
        "actuation_enacted": {"speaking_register": "Methodical & Pragmatic", "action_bid": "Halt and request guidance"},
        "is_conflict": True,
    },
]

SLEEP_CYCLE_2_EPISODES = [
    {
        "episode_id": "ep-006",
        "cycle": 6,
        "factual_anchor": {
            "sentence": "The national bank disbursed infrastructure credits to the municipal council.",
            "target_lemmas": ["bank"],
            "resolved_senses": {"bank": "depository_financial_institution (financial institution)"},
            "core_pattern": "national bank",
        },
        "affective_snapshot": {"salience": 0.82, "clarity": 0.90, "arousal": 0.58},
        "actuation_enacted": {"speaking_register": "Methodical & Pragmatic", "action_bid": "Disburse credit"},
        "is_conflict": False,
    },
    {
        "episode_id": "ep-007",
        "cycle": 7,
        "factual_anchor": {
            "sentence": "Wild lilies bloomed along the river bank at dawn.",
            "target_lemmas": ["bank"],
            "resolved_senses": {"bank": "sloping_land (river bank)"},
            "core_pattern": "river bank",
        },
        "affective_snapshot": {"salience": 0.72, "clarity": 0.85, "arousal": 0.50},
        "actuation_enacted": {"speaking_register": "Communal & Reassuring", "action_bid": "Appreciate flora"},
        "is_conflict": False,
    },
    {
        "episode_id": "ep-008",
        "cycle": 8,
        "factual_anchor": {
            "sentence": "Gentle reeds grew on the river bank where water flowed slowly.",
            "target_lemmas": ["bank"],
            "resolved_senses": {"bank": "sloping_land (river bank)"},
            "core_pattern": "river bank",
        },
        "affective_snapshot": {"salience": 0.70, "clarity": 0.84, "arousal": 0.48},
        "actuation_enacted": {"speaking_register": "Communal & Reassuring", "action_bid": "Record ecosystem"},
        "is_conflict": False,
    },
]


def run_memory_consolidation_study(output_dir=None):
    """Executes multi-cycle memory consolidation study and verifies baseline parity."""
    engine = MemoryConsolidationEngine(initial_rules=INITIAL_RULES, min_confirmations=2, reinforcement_rate=0.20)
    comparator = OrdinaryMemoryConsolidationComparator(initial_rules=INITIAL_RULES, min_confirmations=2, reinforcement_rate=0.20)

    cycles_results = []
    parity_passed = True

    # --- Sleep Cycle 1 ---
    e_summary_1, e_rem_1 = engine.consolidate_sleep_cycle(SLEEP_CYCLE_1_EPISODES, prune_buffer=True)
    c_summary_1, c_rem_1 = comparator.consolidate(SLEEP_CYCLE_1_EPISODES, prune_buffer=True)

    if digest(e_summary_1) != digest(c_summary_1) or digest(e_rem_1) != digest(c_rem_1):
        parity_passed = False

    cycles_results.append({
        "cycle": 1,
        "summary": e_summary_1,
        "remaining_buffer": e_rem_1,
        "digest": digest(e_summary_1),
    })

    # --- Sleep Cycle 2 ---
    e_summary_2, e_rem_2 = engine.consolidate_sleep_cycle(SLEEP_CYCLE_2_EPISODES, prune_buffer=True)
    c_summary_2, c_rem_2 = comparator.consolidate(SLEEP_CYCLE_2_EPISODES, prune_buffer=True)

    if digest(e_summary_2) != digest(c_summary_2) or digest(e_rem_2) != digest(c_rem_2):
        parity_passed = False

    cycles_results.append({
        "cycle": 2,
        "summary": e_summary_2,
        "remaining_buffer": e_rem_2,
        "digest": digest(e_summary_2),
    })

    # Export serialization check
    e_export = engine.export_state()
    c_export = comparator.export_state()
    if digest(e_export) != digest(c_export):
        parity_passed = False

    # Rule D001 verification
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40, f"Seed corrupted: expected 40 nodes, found {len(seed_nodes)}"

    summary = {
        "kind": KIND,
        "total_sleep_cycles_evaluated": 2,
        "total_episodes_replayed": len(SLEEP_CYCLE_1_EPISODES) + len(SLEEP_CYCLE_2_EPISODES),
        "total_long_term_rules_final": len(engine.long_term_rules),
        "consumer_parity": parity_passed,
        "frozen_seed_invariant_enforced": True,
        "evaluation_digest": digest(cycles_results),
        "cycles": cycles_results,
        "final_rules": list(engine.long_term_rules.values()),
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "memory-consolidation-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Dual-Speed Memory Consolidation Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_memory_consolidation_study(output_dir=args.output_dir)

    print("\n=== Dual-Speed Memory Consolidation Benchmark ===")
    print(f"Total Sleep Cycles: {summary['total_sleep_cycles_evaluated']}")
    print(f"Total Episodes Replayed: {summary['total_episodes_replayed']}")
    print(f"Final Long-Term Rules: {summary['total_long_term_rules_final']}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['frozen_seed_invariant_enforced']}")
    print(f"Evaluation Digest: {summary['evaluation_digest'][:16]}...")
    print("=================================================\n")


if __name__ == "__main__":
    main()
