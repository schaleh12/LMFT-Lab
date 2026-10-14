"""Recurrent Post-Action Echo Benchmark.

Evaluates the closed cybernetic feedback loop echoing emitted actions back into Experiential leaves
across 6 standardized behavioral postures.

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
from lmft_lab.recurrent_feedback import (
    EXPERIENTIAL_LEAF_IDS,
    RecurrentFeedbackEngine,
    OrdinaryMemoryRecurrentComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "recurrent-feedback-benchmark-1"

BENCHMARK_SCENARIOS = [
    {
        "scenario_id": "noble_resolute_action_satisfaction",
        "description": "Decisive action damps arousal (-0.15), elevates valence (+0.12), boosts resonance (+0.15)",
        "posture": "Noble Resolute Action: decisive execution guided by honor",
        "psychological": {
            "psychological/will/intention": 0.85,
            "psychological/will/execution": 0.80,
            "psychological/contemplation/clarity": 0.90,
            "psychological/contemplation/confidence": 0.95,
        },
        "experiential": {
            "experiential/phase/arousal": 0.65,
            "experiential/phase/valence": 0.50,
            "experiential/reflection/salience": 0.60,
        },
    },
    {
        "scenario_id": "honest_silence_epistemic_calm",
        "description": "Honest silence/abstention calms arousal (-0.10) while preserving salience (+0.10)",
        "posture": "Neutral Observant Silence (Honest Abstention)",
        "psychological": {
            "psychological/will/intention": 0.20,
            "psychological/will/execution": 0.10,
            "psychological/contemplation/clarity": 0.50,
            "psychological/contemplation/confidence": 0.40,
        },
        "experiential": {
            "experiential/phase/arousal": 0.50,
            "experiential/reflection/salience": 0.40,
        },
    },
    {
        "scenario_id": "cognitive_conflict_alert",
        "description": "Low clarity / conflict heightens alertness (arousal +0.15, salience +0.25)",
        "posture": "Cognitive Conflict: unresolved epistemic ambiguity",
        "psychological": {
            "psychological/will/intention": 0.40,
            "psychological/will/execution": 0.20,
            "psychological/contemplation/clarity": 0.15,
            "psychological/contemplation/confidence": 0.20,
        },
        "experiential": {
            "experiential/phase/arousal": 0.45,
            "experiential/phase/valence": 0.50,
            "experiential/reflection/salience": 0.35,
        },
    },
    {
        "scenario_id": "methodical_equilibrated_synthesis",
        "description": "Equilibrated synthesis stabilizes arousal (-0.05) and valence (+0.05)",
        "posture": "Methodical & Pragmatic Equilibrated Synthesis",
        "psychological": {
            "psychological/will/intention": 0.60,
            "psychological/will/execution": 0.55,
            "psychological/contemplation/clarity": 0.70,
            "psychological/contemplation/confidence": 0.70,
        },
        "experiential": {
            "experiential/phase/arousal": 0.50,
            "experiential/phase/valence": 0.50,
        },
    },
    {
        "scenario_id": "dissonance_clarification_demand",
        "description": "Severe dissonance triggers alerted clarification demand",
        "posture": "Severe Cognitive Dissonance",
        "psychological": {
            "psychological/contemplation/clarity": 0.10,
        },
        "experiential": {
            "experiential/phase/arousal": 0.50,
        },
    },
    {
        "scenario_id": "neutral_posture_baseline",
        "description": "Baseline neutral inputs verify smooth stabilization",
        "posture": "Equilibrated Synthesis",
        "psychological": {},
        "experiential": {},
    },
]


def run_recurrent_feedback_study(output_dir=None):
    """Executes recurrent feedback benchmark and verifies baseline parity across scenarios."""
    engine = RecurrentFeedbackEngine()
    comparator = OrdinaryMemoryRecurrentComparator()

    results = []
    parity_passed = True

    for scen in BENCHMARK_SCENARIOS:
        p_res = engine.compute_echo(
            experiential_dials=scen["experiential"],
            psychological_state=scen["psychological"],
            action_posture=scen["posture"],
        )
        c_res = comparator.compute_echo(
            experiential_dials=scen["experiential"],
            psychological_state=scen["psychological"],
            action_posture=scen["posture"],
        )

        if digest(p_res) != digest(c_res):
            parity_passed = False

        results.append({
            "scenario_id": scen["scenario_id"],
            "description": scen["description"],
            "posture": scen["posture"],
            "echo_type": p_res["echo_type"],
            "echo_deltas": p_res["echo_deltas"],
            "echoed_experiential": p_res["echoed_experiential"],
            "arousal_damped": p_res["arousal_damped"],
            "valence_reinforced": p_res["valence_reinforced"],
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
        atomic_json(out_path / "recurrent-feedback-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Recurrent Post-Action Echo Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_recurrent_feedback_study(output_dir=args.output_dir)

    print("\n=== Recurrent Post-Action Echo Benchmark ===")
    print(f"Total Scenarios Evaluated: {summary['total_scenarios_evaluated']}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['frozen_seed_invariant_enforced']}")
    print(f"Evaluation Digest: {summary['evaluation_digest'][:16]}...")
    print("============================================\n")


if __name__ == "__main__":
    main()
