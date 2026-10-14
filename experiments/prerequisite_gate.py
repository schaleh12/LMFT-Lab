"""Fuzzy Prerequisite Coherence Gate Benchmark.

Evaluates symbolic conditional dependencies and authenticity gating across 6 standardized test scenarios:
1. Coerced Compliance (Justice without Freedom)
2. Dogmatic Hallucination (Confidence without Clarity)
3. Unanchored Volition (Intention without Agency)
4. Ephemeral Symmetry (Order without Persistence)
5. Authentic Harmonic Virtue (Fulfill prerequisites)
6. Neutral Baseline Quiescence

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
from lmft_lab.prerequisite_gate import (
    CONDITIONAL_LEAF_TARGETS,
    PrerequisiteCoherenceGate,
    OrdinaryMemoryPrerequisiteComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "prerequisite-gate-benchmark-1"

BENCHMARK_SCENARIOS = [
    {
        "scenario_id": "coerced_compliance_distortion",
        "description": "High nominal Justice (0.90) under crushed Freedom (0.10)",
        "dials": {
            "cultural/justice/fairness": 0.90,
            "cultural/freedom/self-sufficiency": 0.10,
            "cultural/freedom/needlessness": 0.10,
        },
    },
    {
        "scenario_id": "dogmatic_hallucination_distortion",
        "description": "High Confidence (0.95) without empirical Clarity (0.05)",
        "dials": {
            "psychological/contemplation/confidence": 0.95,
            "psychological/contemplation/clarity": 0.05,
        },
    },
    {
        "scenario_id": "unanchored_volition_distortion",
        "description": "High Intention (0.85) without ontological Agency (0.15)",
        "dials": {
            "psychological/will/intention": 0.85,
            "philosophical/being/agency": 0.15,
        },
    },
    {
        "scenario_id": "ephemeral_symmetry_distortion",
        "description": "High Order (0.90) without Persistence (0.10)",
        "dials": {
            "philosophical/structure/order": 0.90,
            "philosophical/persistence/continuity": 0.10,
            "philosophical/persistence/discreteness": 0.10,
        },
    },
    {
        "scenario_id": "authentic_harmonic_virtue",
        "description": "Harmonic alignment where all virtues satisfy necessary prerequisites",
        "dials": {
            "cultural/justice/fairness": 0.85,
            "cultural/freedom/self-sufficiency": 0.90,
            "cultural/freedom/needlessness": 0.90,
            "psychological/contemplation/confidence": 0.90,
            "psychological/contemplation/clarity": 0.90,
            "psychological/will/intention": 0.85,
            "philosophical/being/agency": 0.90,
            "philosophical/structure/order": 0.85,
            "philosophical/persistence/continuity": 0.90,
            "philosophical/persistence/discreteness": 0.90,
        },
    },
    {
        "scenario_id": "neutral_quiescent_baseline",
        "description": "All baseline coordinates at 0.50 verify balanced coherence",
        "dials": {},
    },
]


def run_prerequisite_gate_study(output_dir=None):
    """Executes prerequisite gate benchmark and verifies baseline parity across scenarios."""
    gate = PrerequisiteCoherenceGate()
    comparator = OrdinaryMemoryPrerequisiteComparator()

    results = []
    parity_passed = True

    for scen in BENCHMARK_SCENARIOS:
        p_res = gate.evaluate_coherence(scen["dials"])
        c_res = comparator.evaluate(scen["dials"])

        if digest(p_res) != digest(c_res):
            parity_passed = False

        results.append({
            "scenario_id": scen["scenario_id"],
            "description": scen["description"],
            "distortions_detected": p_res["distortions_detected"],
            "global_coherence_index": p_res["global_coherence_index"],
            "is_authentic": p_res["is_authentic"],
            "authentic_scores": p_res["authentic_scores"],
            "digest": digest(p_res),
        })

    # Rule D001 verification
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40, f"Seed corrupted: expected 40 nodes, found {len(seed_nodes)}"

    summary = {
        "kind": KIND,
        "total_scenarios_evaluated": len(BENCHMARK_SCENARIOS),
        "consumer_parity": parity_passed,
        "frozen_seed_invariant_enforced": True,
        "evaluation_digest": digest(results),
        "results": results,
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "prerequisite-gate-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Fuzzy Prerequisite Coherence Gate Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_prerequisite_gate_study(output_dir=args.output_dir)

    print("\n=== Fuzzy Prerequisite Coherence Gate Benchmark ===")
    print(f"Total Scenarios Evaluated: {summary['total_scenarios_evaluated']}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['frozen_seed_invariant_enforced']}")
    print(f"Evaluation Digest: {summary['evaluation_digest'][:16]}...")
    print("===================================================\n")


if __name__ == "__main__":
    main()
