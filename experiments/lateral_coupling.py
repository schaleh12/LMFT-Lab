"""Lateral Ethical-Ontological Coupling Benchmark.

Evaluates mutual regulation between Cultural leaves (Ethics/Governance) and Philosophical leaves
(Metaphysics/Ontology) across 6 standardized test scenarios.

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
from lmft_lab.lateral_coupling import (
    CULTURAL_LEAF_IDS,
    PHILOSOPHICAL_LEAF_IDS,
    LateralCouplingEngine,
    OrdinaryMemoryLateralComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "lateral-coupling-benchmark-1"

BENCHMARK_SCENARIOS = [
    {
        "scenario_id": "tyranny_risk_power_overreach",
        "description": "High Cultural Power (0.90) induces compensatory Philosophical Order (preventing tyranny)",
        "cultural": {"cultural/efficiency/power": 0.90},
        "philosophical": {"philosophical/structure/order": 0.40},
    },
    {
        "scenario_id": "existential_volatility_chaos",
        "description": "High Philosophical Chaos (0.95) triggers moral ballast (Honor and Self-Sufficiency)",
        "cultural": {},
        "philosophical": {"philosophical/structure/chaos": 0.95},
    },
    {
        "scenario_id": "societal_equity_continuity",
        "description": "High Cultural Fairness (0.85) reinforces Being Existence and Persistence Continuity",
        "cultural": {"cultural/justice/fairness": 0.85},
        "philosophical": {},
    },
    {
        "scenario_id": "ascetic_sovereignty",
        "description": "High Freedom Needlessness (0.90) reinforces serene Existence and Agency",
        "cultural": {"cultural/freedom/needlessness": 0.90},
        "philosophical": {},
    },
    {
        "scenario_id": "atomic_frugality",
        "description": "High Efficiency Wastelessness (0.85) reinforces Persistence Discreteness",
        "cultural": {"cultural/efficiency/wastelessness": 0.85},
        "philosophical": {},
    },
    {
        "scenario_id": "neutral_equilibrium_quiescence",
        "description": "All coordinates at 0.50 baseline remain strictly quiescent",
        "cultural": {},
        "philosophical": {},
    },
]


def run_lateral_coupling_study(output_dir=None):
    """Executes lateral coupling study and verifies baseline parity across scenarios."""
    engine = LateralCouplingEngine()
    comparator = OrdinaryMemoryLateralComparator()

    results = []
    parity_passed = True

    for scen in BENCHMARK_SCENARIOS:
        p_res = engine.couple(
            cultural_dials=scen["cultural"],
            philosophical_dials=scen["philosophical"],
            coupling_gain=1.0,
        )
        c_res = comparator.couple(
            cultural_dials=scen["cultural"],
            philosophical_dials=scen["philosophical"],
            coupling_gain=1.0,
        )

        if digest(p_res) != digest(c_res):
            parity_passed = False

        results.append({
            "scenario_id": scen["scenario_id"],
            "description": scen["description"],
            "delta_cultural": p_res["delta_cultural"],
            "delta_philosophical": p_res["delta_philosophical"],
            "coupled_cultural": p_res["coupled_cultural"],
            "coupled_philosophical": p_res["coupled_philosophical"],
            "cohesion_metrics": p_res["cohesion_metrics"],
            "digest": digest(p_res),
        })

    # Rule D001 verification
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40, f"Seed corrupted: expected 40 nodes, got {len(seed_nodes)}"

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
        atomic_json(out_path / "lateral-coupling-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Lateral Ethical-Ontological Coupling Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_lateral_coupling_study(output_dir=args.output_dir)

    print("\n=== Lateral Ethical-Ontological Coupling Benchmark ===")
    print(f"Total Scenarios Evaluated: {summary['total_scenarios_evaluated']}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['frozen_seed_invariant_enforced']}")
    print(f"Evaluation Digest: {summary['evaluation_digest'][:16]}...")
    print("======================================================\n")


if __name__ == "__main__":
    main()
