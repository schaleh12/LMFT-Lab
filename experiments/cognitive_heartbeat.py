"""Unified Cognitive Heartbeat Benchmark.

Evaluates the integrated developmental architecture across an end-to-end multi-turn cognitive lifecycle:
1. Waking Interaction Phase:
   - Polysemous sense resolution via capacity rules.
   - Lateral ethical-ontological coupling.
   - Prerequisite coherence gate & distortion monitoring.
   - Post-action echo into experiential roots.
   - Dynamic affective plasticity modulation.
   - Continuous dispositional momentum updates.
   - Dual-coded episodic saliency journal admission.
2. Offline Sleep Consolidation Phase:
   - Hippocampal replay of episodic records.
   - Promotion of recurring patterns into long-term rules.
   - Progressive habituation of established weights.
   - Anti-bloat buffer pruning with conflict retention.
   - Idle dispositional equilibrium relaxation.
3. Standalone Packaging & Migration (.lmft.json):
   - Cryptographic SHA-256 signature verification.
   - Frozen founding seed fingerprint enforcement (Rule D001).
   - 100% state restoration fidelity.

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
from lmft_lab.cognitive_heartbeat import (
    CognitiveHeartbeat,
    OrdinaryMemoryHeartbeatComparator,
)
from lmft_lab.individual_package import export_individual, import_individual
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "cognitive-heartbeat-benchmark-1"

WAKING_PHASE_1_SENTENCES = [
    {
        "cycle": 1,
        "sentence": "The national bank established monetary reserve requirements for the year.",
        "target_lemmas": ["bank"],
        "forced_senses": None,
        "is_conflict": False,
    },
    {
        "cycle": 2,
        "sentence": "A formal court order was affirmed by the high magistrate.",
        "target_lemmas": ["order"],
        "forced_senses": None,
        "is_conflict": False,
    },
    {
        "cycle": 3,
        "sentence": "Wild watercress drifted quietly near the river bank.",
        "target_lemmas": ["bank"],
        "forced_senses": {"bank": "sloping_land (river bank)"},
        "is_conflict": False,
    },
    {
        "cycle": 4,
        "sentence": "The edict declared unconditional surrender while commanding an immediate assault.",
        "target_lemmas": ["order"],
        "forced_senses": {"order": "ambiguous_conflict"},
        "is_conflict": True,
    },
]

WAKING_PHASE_2_SENTENCES = [
    {
        "cycle": 5,
        "sentence": "Gentle willows shaded the river bank at noon where the water ran clear.",
        "target_lemmas": ["bank"],
        "forced_senses": {"bank": "sloping_land (river bank)"},
        "is_conflict": False,
    },
    {
        "cycle": 6,
        "sentence": "The national bank updated interest schedules for institutional borrowers.",
        "target_lemmas": ["bank"],
        "forced_senses": None,
        "is_conflict": False,
    },
]


def run_cognitive_heartbeat_study(output_dir=None):
    """Executes integrated cognitive heartbeat study across waking, sleep, and packaging phases."""
    heartbeat = CognitiveHeartbeat(individual_id="lmft-integrated-individual-01", min_confirmations=2)
    comparator = OrdinaryMemoryHeartbeatComparator(individual_id="lmft-integrated-individual-01", min_confirmations=2)

    waking_step_results = []
    parity_passed = True

    # --- Phase 1: Waking Interactions (Cycles 1-4) ---
    for item in WAKING_PHASE_1_SENTENCES:
        h_res = heartbeat.interact(
            sentence=item["sentence"],
            target_lemmas=item["target_lemmas"],
            forced_senses=item["forced_senses"],
            is_conflict=item["is_conflict"],
        )
        c_res = comparator.interact(
            sentence=item["sentence"],
            target_lemmas=item["target_lemmas"],
            forced_senses=item["forced_senses"],
            is_conflict=item["is_conflict"],
        )

        if digest(h_res) != digest(c_res):
            parity_passed = False

        waking_step_results.append({
            "cycle": h_res["cycle"],
            "sentence": h_res["sentence"],
            "speaking_register": h_res["speaking_register"],
            "action_bid": h_res["action_bid"],
            "global_coherence": h_res["coherence"]["global_coherence_index"],
            "distortions_count": len(h_res["coherence"]["distortions_detected"]),
            "dynamic_alpha": h_res["plasticity"]["dynamic_alpha"],
            "journal_admitted": h_res["journal_result"]["admitted"],
            "digest": digest(h_res),
        })

    # --- Phase 2: First Sleep Consolidation Cycle ---
    h_sleep_1 = heartbeat.sleep(prune_buffer=True)
    c_sleep_1 = comparator.sleep(prune_buffer=True)
    if digest(h_sleep_1) != digest(c_sleep_1):
        parity_passed = False

    # --- Phase 3: Waking Interactions (Cycles 5-6) ---
    for item in WAKING_PHASE_2_SENTENCES:
        h_res = heartbeat.interact(
            sentence=item["sentence"],
            target_lemmas=item["target_lemmas"],
            forced_senses=item["forced_senses"],
            is_conflict=item["is_conflict"],
        )
        c_res = comparator.interact(
            sentence=item["sentence"],
            target_lemmas=item["target_lemmas"],
            forced_senses=item["forced_senses"],
            is_conflict=item["is_conflict"],
        )

        if digest(h_res) != digest(c_res):
            parity_passed = False

        waking_step_results.append({
            "cycle": h_res["cycle"],
            "sentence": h_res["sentence"],
            "speaking_register": h_res["speaking_register"],
            "action_bid": h_res["action_bid"],
            "global_coherence": h_res["coherence"]["global_coherence_index"],
            "distortions_count": len(h_res["coherence"]["distortions_detected"]),
            "dynamic_alpha": h_res["plasticity"]["dynamic_alpha"],
            "journal_admitted": h_res["journal_result"]["admitted"],
            "digest": digest(h_res),
        })

    # --- Phase 4: Second Sleep Consolidation Cycle ---
    h_sleep_2 = heartbeat.sleep(prune_buffer=True)
    c_sleep_2 = comparator.sleep(prune_buffer=True)
    if digest(h_sleep_2) != digest(c_sleep_2):
        parity_passed = False

    # --- Phase 5: Standalone Packaging & Migration Check ---
    out_dir_path = Path(output_dir) if output_dir else Path("outputs/temp_pkg")
    out_dir_path.mkdir(parents=True, exist_ok=True)
    pkg_file = out_dir_path / "integrated_individual.lmft.json"

    pkg_data = heartbeat.export_individual_package()
    export_individual(pkg_data, pkg_file, description="Autobiographical Integrated Individual Snapshot")
    restored_raw = import_individual(pkg_file, verify_seed=True)

    restored_heartbeat = CognitiveHeartbeat()
    restored_heartbeat.import_individual_package(restored_raw)

    round_trip_fidelity = (
        restored_heartbeat.cycle_count == heartbeat.cycle_count
        and len(restored_heartbeat.consolidator.long_term_rules) == len(heartbeat.consolidator.long_term_rules)
        and digest(restored_heartbeat.disposition.dials) == digest(heartbeat.disposition.dials)
    )

    # Rule D001 verification
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40, f"Seed corrupted: expected 40 nodes, found {len(seed_nodes)}"

    summary = {
        "kind": KIND,
        "total_waking_cycles": len(waking_step_results),
        "total_sleep_cycles": 2,
        "final_long_term_rules_count": len(heartbeat.consolidator.long_term_rules),
        "consumer_parity": parity_passed,
        "frozen_seed_invariant_enforced": True,
        "round_trip_fidelity": round_trip_fidelity,
        "evaluation_digest": digest(waking_step_results),
        "sleep_cycle_1": h_sleep_1,
        "sleep_cycle_2": h_sleep_2,
        "waking_cycles": waking_step_results,
        "final_rules": list(heartbeat.consolidator.long_term_rules.values()),
    }

    if output_dir:
        atomic_json(out_dir_path / "cognitive-heartbeat-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Unified Cognitive Heartbeat Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_cognitive_heartbeat_study(output_dir=args.output_dir)

    print("\n=== Unified Cognitive Heartbeat Benchmark ===")
    print(f"Total Waking Cycles: {summary['total_waking_cycles']}")
    print(f"Total Sleep Cycles: {summary['total_sleep_cycles']}")
    print(f"Final Long-Term Rules: {summary['final_long_term_rules_count']}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['frozen_seed_invariant_enforced']}")
    print(f"Round-Trip Package Fidelity: {summary['round_trip_fidelity']}")
    print(f"Evaluation Digest: {summary['evaluation_digest'][:16]}...")
    print("=============================================\n")


if __name__ == "__main__":
    main()
