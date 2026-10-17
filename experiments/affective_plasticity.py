"""Affective Plasticity Regulation Benchmark.

Evaluates dynamic learning rates (alpha), habituation decay (lambda), and contradiction damping (delta)
across 6 standardized affective-epistemic conditions.

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
from lmft_lab.affective_plasticity import (
    AffectivePlasticityEngine,
    OrdinaryMemoryAffectivePlasticityComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "affective-plasticity-benchmark-1"

BENCHMARK_CONDITIONS = [
    {
        "condition_id": "high_novelty_high_arousal_surprise",
        "description": "High surprise (Novelty=0.95, Arousal=0.90) spikes learning plasticity (alpha > 0.28)",
        "experiential": {
            "experiential/reflection/novelty": 0.95,
            "experiential/phase/arousal": 0.90,
            "experiential/phase/valence": 0.50,
            "experiential/synchronization/entrainment": 0.50,
        },
        "psychological": {
            "psychological/contemplation/clarity": 0.20,
            "psychological/contemplation/confidence": 0.20,
        },
        "test_event": "reinforce",
        "initial_weight": 0.50,
    },
    {
        "condition_id": "high_clarity_high_confidence_mastery",
        "description": "High mastery (Clarity=0.95, Confidence=0.95) throttles plasticity (alpha < 0.15)",
        "experiential": {
            "experiential/reflection/novelty": 0.10,
            "experiential/phase/arousal": 0.10,
            "experiential/phase/valence": 0.80,
            "experiential/synchronization/entrainment": 0.90,
        },
        "psychological": {
            "psychological/contemplation/clarity": 0.95,
            "psychological/contemplation/confidence": 0.95,
        },
        "test_event": "reinforce",
        "initial_weight": 0.50,
    },
    {
        "condition_id": "high_retention_positive_valence_preservation",
        "description": "High retention (0.95) and positive valence (0.90) slow decay (lambda < 0.035)",
        "experiential": {
            "experiential/reflection/novelty": 0.20,
            "experiential/phase/arousal": 0.20,
            "experiential/phase/valence": 0.90,
            "experiential/synchronization/entrainment": 0.95,
        },
        "psychological": {
            "psychological/contemplation/clarity": 0.80,
            "psychological/contemplation/confidence": 0.80,
        },
        "test_event": "decay",
        "initial_weight": 0.80,
    },
    {
        "condition_id": "low_retention_negative_valence_volatility",
        "description": "Low retention (0.10) and negative valence (0.10) accelerates decay (lambda > 0.055)",
        "experiential": {
            "experiential/reflection/novelty": 0.50,
            "experiential/phase/arousal": 0.50,
            "experiential/phase/valence": 0.10,
            "experiential/synchronization/entrainment": 0.10,
        },
        "psychological": {
            "psychological/contemplation/clarity": 0.30,
            "psychological/contemplation/confidence": 0.30,
        },
        "test_event": "decay",
        "initial_weight": 0.80,
    },
    {
        "condition_id": "high_arousal_low_confidence_contradiction",
        "description": "High arousal and low confidence intensify contradiction damping (delta > 0.40)",
        "experiential": {
            "experiential/reflection/novelty": 0.80,
            "experiential/phase/arousal": 0.90,
            "experiential/phase/valence": 0.20,
            "experiential/synchronization/entrainment": 0.40,
        },
        "psychological": {
            "psychological/contemplation/clarity": 0.20,
            "psychological/contemplation/confidence": 0.10,
        },
        "test_event": "damp",
        "initial_weight": 0.70,
    },
    {
        "condition_id": "neutral_equilibrium_baseline",
        "description": "Neutral baselines (0.50) replicate default standard rates (alpha=0.20, lambda=0.05)",
        "experiential": {},
        "psychological": {},
        "test_event": "reinforce",
        "initial_weight": 0.50,
    },
]


def run_affective_plasticity_study(output_dir=None):
    """Executes affective plasticity benchmark and verifies baseline parity across conditions."""
    engine = AffectivePlasticityEngine()
    comparator = OrdinaryMemoryAffectivePlasticityComparator()

    results = []
    parity_passed = True

    for cond in BENCHMARK_CONDITIONS:
        p_res = engine.update_rule_weight(
            current_weight=cond["initial_weight"],
            event_type=cond["test_event"],
            experiential_dials=cond["experiential"],
            psychological_dials=cond["psychological"],
        )
        c_res = comparator.update_rule_weight(
            current_weight=cond["initial_weight"],
            event_type=cond["test_event"],
            experiential_dials=cond["experiential"],
            psychological_dials=cond["psychological"],
        )

        if digest(p_res) != digest(c_res):
            parity_passed = False

        results.append({
            "condition_id": cond["condition_id"],
            "description": cond["description"],
            "event_type": cond["test_event"],
            "initial_weight": p_res["initial_weight"],
            "new_weight": p_res["new_weight"],
            "rates": p_res["rates"],
            "digest": digest(p_res),
        })

    # Rule D001 verification
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40, f"Seed corrupted: expected 40 nodes, found {len(seed_nodes)}"

    summary = {
        "kind": KIND,
        "total_conditions_evaluated": len(BENCHMARK_CONDITIONS),
        "consumer_parity": parity_passed,
        "frozen_seed_invariant_enforced": True,
        "evaluation_digest": digest(results),
        "results": results,
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "affective-plasticity-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Affective Plasticity Regulation Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_affective_plasticity_study(output_dir=args.output_dir)

    print("\n=== Affective Plasticity Regulation Benchmark ===")
    print(f"Total Conditions Evaluated: {summary['total_conditions_evaluated']}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['frozen_seed_invariant_enforced']}")
    print(f"Evaluation Digest: {summary['evaluation_digest'][:16]}...")
    print("=================================================\n")


if __name__ == "__main__":
    main()
