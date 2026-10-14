"""Persistent Dispositional State Vector & Momentum Drift Benchmark.

Evaluates continuous dispositional momentum (an ongoing temporal 'mood') across multi-turn sequential
interactions, idle equilibrium drift, and verified serialization round-trips.

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
from lmft_lab.dispositional_momentum import (
    CANONICAL_LEAF_IDS,
    PersistentDispositionalVector,
    OrdinaryMemoryDispositionalComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "dispositional-momentum-benchmark-1"

# 4 Sequential Interaction Stimuli
SEQUENTIAL_STIMULI = [
    {
        "turn": 1,
        "event_label": "authoritative_directive_stimulus",
        "stimulus": {
            "cultural/efficiency/power": 0.85,
            "philosophical/structure/order": 0.80,
            "psychological/will/intention": 0.90,
        },
    },
    {
        "turn": 2,
        "event_label": "unexpected_chaotic_disruption",
        "stimulus": {
            "philosophical/structure/chaos": 0.85,
            "experiential/reflection/novelty": 0.80,
            "experiential/phase/arousal": 0.75,
        },
    },
    {
        "turn": 3,
        "event_label": "epistemic_contemplation_and_fairness",
        "stimulus": {
            "cultural/justice/fairness": 0.85,
            "psychological/contemplation/clarity": 0.80,
            "philosophical/persistence/continuity": 0.75,
        },
    },
    {
        "turn": 4,
        "event_label": "neutral_pause_equilibrated",
        "stimulus": {
            "philosophical/structure/order": 0.50,
            "cultural/efficiency/power": 0.50,
        },
    },
]


def run_dispositional_momentum_study(output_dir=None):
    """Executes multi-turn dispositional momentum trajectory with export and parity verification."""
    vec = PersistentDispositionalVector(gamma=0.35, mu=0.05)
    comparator = OrdinaryMemoryDispositionalComparator(gamma=0.35, mu=0.05)

    turns_log = []
    parity_passed = True

    # 1. Multi-turn Sequential Interactions
    for item in SEQUENTIAL_STIMULI:
        p_res = vec.incorporate_situational_stimulus(item["stimulus"])
        c_res = comparator.incorporate(item["stimulus"])

        if digest(p_res) != digest(c_res):
            parity_passed = False

        turns_log.append({
            "turn": item["turn"],
            "event_label": item["event_label"],
            "epoch": p_res["epoch"],
            "deltas_sample": {
                k: p_res["deltas"][k]
                for k in ["cultural/efficiency/power", "philosophical/structure/order", "philosophical/structure/chaos"]
                if k in p_res["deltas"]
            },
            "resulting_order": p_res["current_dials"]["philosophical/structure/order"],
            "resulting_power": p_res["current_dials"]["cultural/efficiency/power"],
            "resulting_chaos": p_res["current_dials"]["philosophical/structure/chaos"],
            "digest": digest(p_res),
        })

    # 2. Idle Equilibrium Drift (5 steps)
    p_drift = vec.apply_idle_equilibrium_drift(steps=5)
    c_drift = comparator.idle_drift(steps=5)
    if digest(p_drift) != digest(c_drift):
        parity_passed = False

    # 3. Serialization Round-Trip
    exported_state = vec.export_state()
    comp_exported = comparator.export_state()
    if digest(exported_state) != digest(comp_exported):
        parity_passed = False

    restored_vec = PersistentDispositionalVector()
    restored_vec.import_state(exported_state)
    assert digest(restored_vec.export_state()) == digest(exported_state)

    # 4. Tampering & Seed Mutation Rejection Check
    tampered_state = deepcopy(exported_state)
    tampered_state["seed_fingerprint"] = "mutated_seed_geometry_41"
    seed_violation_caught = False
    try:
        restored_vec.import_state(tampered_state)
    except ValueError as e:
        if "Seed geometry violation" in str(e):
            seed_violation_caught = True

    # 5. Rule D001 Seed Inventory Check
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40, f"Seed corrupted: expected 40 nodes, found {len(seed_nodes)}"

    summary = {
        "kind": KIND,
        "total_turns_evaluated": len(SEQUENTIAL_STIMULI),
        "idle_drift_steps": 5,
        "consumer_parity": parity_passed,
        "round_trip_verified": True,
        "seed_invariant_enforced": seed_violation_caught,
        "final_epoch_count": vec.epoch_count,
        "final_state_digest": digest(exported_state),
        "turns_log": turns_log,
        "drift_summary": {
            "pre_drift_order": turns_log[-1]["resulting_order"],
            "post_drift_order": p_drift["current_dials"]["philosophical/structure/order"],
        },
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "dispositional-momentum-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Persistent Dispositional State Vector Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_dispositional_momentum_study(output_dir=args.output_dir)

    print("\n=== Persistent Dispositional State Vector Benchmark ===")
    print(f"Total Turns Evaluated: {summary['total_turns_evaluated']}")
    print(f"Idle Drift Steps: {summary['idle_drift_steps']}")
    print(f"Final Epoch Count: {summary['final_epoch_count']}")
    print(f"Pre-Drift Order: {summary['drift_summary']['pre_drift_order']:.4f} -> Post-Drift: {summary['drift_summary']['post_drift_order']:.4f}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['seed_invariant_enforced']}")
    print(f"Final State Digest: {summary['final_state_digest'][:16]}...")
    print("========================================================\n")


if __name__ == "__main__":
    main()
