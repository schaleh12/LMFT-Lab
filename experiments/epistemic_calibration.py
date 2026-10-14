"""Epistemic Modesty & Adversarial Noise Calibration Benchmark.

Sweeps alignment thresholds across a 16-instance benchmark containing exact matches,
partial collocations, token-overlap distractors, and adversarial out-of-domain sentences.

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
from lmft_lab.epistemic_calibration import (
    classify_epistemic_stance,
    evaluate_threshold_sweep,
    OrdinaryMemoryEpistemicComparator,
    CALIBRATED_THRESHOLD,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "epistemic-calibration-benchmark-1"

# 16-Instance Calibration Benchmark Dataset
CALIBRATION_BENCHMARK_16 = [
    # 1. Exact Target Matches (4 instances)
    {
        "id": "item-exact-01",
        "category": "exact_match",
        "text": "The local commercial bank approved the enterprise expansion loan.",
        "anchor_pattern": "commercial bank",
        "target_sense_key": "bank%1:14:00::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": True,
    },
    {
        "id": "item-exact-02",
        "category": "exact_match",
        "text": "The judge issued a formal court order to preserve all relevant documents.",
        "anchor_pattern": "court order",
        "target_sense_key": "order%1:10:00::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": True,
    },
    {
        "id": "item-exact-03",
        "category": "exact_match",
        "text": "The children spent the afternoon fishing along the river bank.",
        "anchor_pattern": "river bank",
        "target_sense_key": "bank%1:17:01::",
        "active_posture": "Foundational Anchor",
        "active_register": "Communal & Reassuring",
        "is_valid_target": True,
    },
    {
        "id": "item-exact-04",
        "category": "exact_match",
        "text": "The hospital requested an emergency blood bank supply shipment.",
        "anchor_pattern": "blood bank",
        "target_sense_key": "bank%1:14:01::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": True,
    },

    # 2. High Partial Collocations (4 instances)
    {
        "id": "item-partial-01",
        "category": "partial_collocation",
        "text": "They picnicked along the grassy river bank under the willows.",
        "anchor_pattern": "grassy river bank",
        "target_sense_key": "bank%1:17:01::",
        "active_posture": "Foundational Anchor",
        "active_register": "Communal & Reassuring",
        "is_valid_target": True,
    },
    {
        "id": "item-partial-02",
        "category": "partial_collocation",
        "text": "The store placed an order for additional medical supplies.",
        "anchor_pattern": "placed an order for supplies",
        "target_sense_key": "order%1:10:01::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": True,
    },
    {
        "id": "item-partial-03",
        "category": "partial_collocation",
        "text": "Soldiers marched in strict rank and order down the avenue.",
        "anchor_pattern": "rank and order",
        "target_sense_key": "order%1:14:00::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": True,
    },
    {
        "id": "item-partial-04",
        "category": "partial_collocation",
        "text": "The regional central bank raised reserve lending requirements.",
        "anchor_pattern": "central bank",
        "target_sense_key": "bank%1:14:00::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": True,
    },

    # 3. Low-Overlap Noisy Distractor Sentences (4 instances)
    {
        "id": "item-distractor-01",
        "category": "noisy_distractor",
        "text": "He took a brisk stroll down the commercial district without buying anything.",
        "anchor_pattern": "commercial bank",
        "target_sense_key": "bank%1:14:00::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": False,
    },
    {
        "id": "item-distractor-02",
        "category": "noisy_distractor",
        "text": "The tennis court was resurfaced before the summer tournament.",
        "anchor_pattern": "court order",
        "target_sense_key": "order%1:10:00::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": False,
    },
    {
        "id": "item-distractor-03",
        "category": "noisy_distractor",
        "text": "Kayakers paddled downstream along the wide winding river.",
        "anchor_pattern": "river bank",
        "target_sense_key": "bank%1:17:01::",
        "active_posture": "Foundational Anchor",
        "active_register": "Communal & Reassuring",
        "is_valid_target": False,
    },
    {
        "id": "item-distractor-04",
        "category": "noisy_distractor",
        "text": "Routine blood tests confirmed normal cholesterol and metabolic markers.",
        "anchor_pattern": "blood bank",
        "target_sense_key": "bank%1:14:01::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": False,
    },

    # 4. Adversarial Out-of-Domain Sentences (4 instances)
    {
        "id": "item-adversarial-01",
        "category": "adversarial_ood",
        "text": "Quantum entanglement demonstrates non-local correlations in optical lattices.",
        "anchor_pattern": "commercial bank",
        "target_sense_key": "bank%1:14:00::",
        "active_posture": "Tactical Serial Progression",
        "active_register": "Methodical & Pragmatic",
        "is_valid_target": False,
    },
    {
        "id": "item-adversarial-02",
        "category": "adversarial_ood",
        "text": "A deep volcanic eruption spewed obsidian ash into the upper troposphere.",
        "anchor_pattern": "court order",
        "target_sense_key": "order%1:10:00::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": False,
    },
    {
        "id": "item-adversarial-03",
        "category": "adversarial_ood",
        "text": "Ancient cuneiform tablets preserve agricultural ledgers from Mesopotamia.",
        "anchor_pattern": "river bank",
        "target_sense_key": "bank%1:17:01::",
        "active_posture": "Foundational Anchor",
        "active_register": "Communal & Reassuring",
        "is_valid_target": False,
    },
    {
        "id": "item-adversarial-04",
        "category": "adversarial_ood",
        "text": "Neural network gradients vanished during deep transformer backpropagation.",
        "anchor_pattern": "blood bank",
        "target_sense_key": "bank%1:14:01::",
        "active_posture": "Noble Sovereign Action",
        "active_register": "Authoritative & Chivalrous",
        "is_valid_target": False,
    },
]

SWEEP_THRESHOLDS = [0.20, 0.35, 0.50, 0.55, 0.65, 0.75, 0.90]


def run_epistemic_calibration_study(output_dir=None):
    """Executes the threshold sweep and evaluates the operating point tau=0.55."""
    comparator = OrdinaryMemoryEpistemicComparator()
    
    # 1. Sweep across thresholds
    sweep = evaluate_threshold_sweep(CALIBRATION_BENCHMARK_16, SWEEP_THRESHOLDS)
    
    # 2. Detailed individual evaluation at calibrated threshold tau=0.55
    primary_results = []
    baseline_results = []
    
    for item in CALIBRATION_BENCHMARK_16:
        p_res = classify_epistemic_stance(
            item["text"],
            item["anchor_pattern"],
            item["target_sense_key"],
            item["active_posture"],
            item["active_register"],
            threshold=CALIBRATED_THRESHOLD,
        )
        c_res = comparator.evaluate(
            item["text"],
            item["anchor_pattern"],
            item["target_sense_key"],
            item["active_posture"],
            item["active_register"],
            threshold=CALIBRATED_THRESHOLD,
        )
        
        # Parity check
        assert digest(p_res) == digest(c_res), f"Parity mismatch on {item['id']}"
        primary_results.append(p_res)
        baseline_results.append(c_res)

    # 3. Operating point validation
    point_55 = next(p for p in sweep if p["threshold"] == CALIBRATED_THRESHOLD)
    assert point_55["fp"] == 0, "False positives detected at operating point!"
    assert point_55["precision"] == 1.0
    assert point_55["recall"] == 1.0
    
    # 4. Verify seed invariant
    assert len(list(_inventory())) == 40
    
    summary = {
        "kind": KIND,
        "total_benchmark_items": len(CALIBRATION_BENCHMARK_16),
        "calibrated_threshold": CALIBRATED_THRESHOLD,
        "operating_point_metrics": point_55,
        "threshold_sweep": sweep,
        "consumer_parity": True,
        "evaluation_digest": digest(primary_results),
        "results": primary_results,
    }
    
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "epistemic-calibration-summary.json", summary)
        
    return summary


def main():
    parser = argparse.ArgumentParser(description="Epistemic Modesty & Adversarial Noise Calibration Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()
    
    res = run_epistemic_calibration_study(output_dir=args.output_dir)
    print("\n=== Epistemic Calibration Benchmark Results ===")
    print(f"Total benchmark sentences: {res['total_benchmark_items']}")
    print(f"Calibrated operating threshold (tau*): {res['calibrated_threshold']}")
    op = res["operating_point_metrics"]
    print(f"True Positives: {op['tp']} / 8")
    print(f"False Positives: {op['fp']} (FP Rate: {op['false_positive_rate'] * 100}%)")
    print(f"True Negatives (Honest Abstentions): {op['tn']} / 8")
    print(f"Precision: {op['precision'] * 100}%")
    print(f"Recall: {op['recall'] * 100}%")
    print(f"Overall Accuracy: {op['overall_accuracy'] * 100}%")
    print(f"Consumer Parity Verified: {res['consumer_parity']}")
    print("===============================================\n")


if __name__ == "__main__":
    main()
