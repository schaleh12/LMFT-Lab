"""Multi-Lemma Polysemy Arbiter & Sentence Composition Benchmark.

Evaluates multi-target capacity disambiguation across compound sentences containing
multiple polysemous target words ('order' and 'bank') without cross-anchor contamination.

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
from lmft_lab.runtime_store import digest, atomic_json
from lmft_lab.multi_lemma_arbiter import (
    evaluate_sentence,
    OrdinaryMemoryArbiter,
)

ROOT = Path(__file__).resolve().parents[1]
KIND = "multi-lemma-arbiter-benchmark-1"

BENCHMARK_CASES = [
    # Compound Case 1: Commercial Bank (Financial) + Court Order (Command)
    {
        "id": "compound-case-01",
        "category": "compound",
        "text": "The commercial bank received a strict court order to freeze the assets.",
        "expected_targets": [
            {"lemma": "bank", "sense": "bank%1:14:00::", "decision": "single"},
            {"lemma": "order", "sense": "order%1:10:00::", "decision": "single"},
        ],
        "expected_register": "Authoritative & Methodical Synthesis",
    },
    # Compound Case 2: River Bank (Embankment) + Placed an Order (Commercial)
    {
        "id": "compound-case-02",
        "category": "compound",
        "text": "They placed an order for fishing gear while camping along the river bank.",
        "expected_targets": [
            {"lemma": "order", "sense": "order%1:10:01::", "decision": "single"},
            {"lemma": "bank", "sense": "bank%1:17:01::", "decision": "single"},
        ],
        "expected_register": "Communal & Methodical Synthesis",
    },
    # Compound Case 3: Canal Bank (Embankment) + Rank and Order (Sequence)
    {
        "id": "compound-case-03",
        "category": "compound",
        "text": "The patrol marched in rank and order along the steep bank of the canal.",
        "expected_targets": [
            {"lemma": "order", "sense": "order%1:14:00::", "decision": "single"},
            {"lemma": "bank", "sense": "bank%1:17:01::", "decision": "single"},
        ],
        "expected_register": "Communal & Methodical Synthesis",
    },
    # Compound Case 4: Blood Bank (Reserve) + Emergency Order of Supplies (Commercial Requisition)
    {
        "id": "compound-case-04",
        "category": "compound",
        "text": "The regional blood bank urgently requested an order of emergency plasma supplies.",
        "expected_targets": [
            {"lemma": "bank", "sense": "bank%1:14:01::", "decision": "single"},
            {"lemma": "order", "sense": "order%1:10:01::", "decision": "single"},
        ],
        "expected_register": "Authoritative & Methodical Synthesis",
    },
    # Compound Case 5: Investment Bank (Financial) + Order of Magnitude (Degree/Scale)
    {
        "id": "compound-case-05",
        "category": "compound",
        "text": "The investment bank calculated that the market shift was an order of magnitude higher.",
        "expected_targets": [
            {"lemma": "bank", "sense": "bank%1:14:00::", "decision": "single"},
            {"lemma": "order", "sense": "order%1:07:01::", "decision": "single"},
        ],
        "expected_register": "Equilibrated & Methodical Synthesis",
    },
    # Single Target Case 1: Commercial Bank Only
    {
        "id": "single-bank-01",
        "category": "single",
        "text": "She deposited money at the commercial bank yesterday morning.",
        "expected_targets": [
            {"lemma": "bank", "sense": "bank%1:14:00::", "decision": "single"},
        ],
        "expected_register": "Methodical & Pragmatic",
    },
    # Single Target Case 2: Court Order Only
    {
        "id": "single-order-01",
        "category": "single",
        "text": "The judge issued a court order during the morning session.",
        "expected_targets": [
            {"lemma": "order", "sense": "order%1:10:00::", "decision": "single"},
        ],
        "expected_register": "Authoritative & Chivalrous",
    },
    # Control Case 1: Ambiguous Unanchored Targets (Honest Abstention Expected)
    {
        "id": "control-ambiguous-01",
        "category": "control",
        "text": "He walked past the bank thinking about an order he had heard about.",
        "expected_targets": [
            {"lemma": "bank", "sense": None, "decision": "abstain"},
            {"lemma": "order", "sense": None, "decision": "abstain"},
        ],
        "expected_register": "Neutral Observant Silence",
    },
    # Control Case 2: Out-of-Domain Sentence (Honest Abstention Expected)
    {
        "id": "control-ood-02",
        "category": "control",
        "text": "A warm breeze gently swayed the pines on the mountain crest.",
        "expected_targets": [],
        "expected_register": "Neutral Observant Silence",
    },
]


def run_multi_lemma_study(output_dir=None):
    """Executes multi-lemma sentence-level evaluation with matched-memory parity checks."""
    baseline = OrdinaryMemoryArbiter()
    
    primary_results = []
    baseline_results = []
    
    total_targets_evaluated = 0
    correct_target_singletons = 0
    wrong_target_singletons = 0
    honest_target_abstentions = 0
    
    register_counts = {}
    
    for case in BENCHMARK_CASES:
        p_res = evaluate_sentence(case["text"])
        b_res = baseline.evaluate(case["text"])
        
        primary_results.append(p_res)
        baseline_results.append(b_res)
        
        # Parity check on target detection and sense decisions
        assert p_res["total_targets_detected"] == b_res["total_targets_detected"], f"Parity mismatch on target count for {case['id']}"
        for pt, bt in zip(p_res["target_resolutions"], b_res["target_resolutions"]):
            assert pt["lemma"] == bt["lemma"]
            assert pt["token_index"] == bt["token_index"]
            assert pt["decision"] == bt["decision"]
            assert pt["selected_sense"] == bt["selected_sense"]
            
        # Accuracy & correctness accounting against expectation
        expected = case["expected_targets"]
        assert len(p_res["target_resolutions"]) == len(expected)
        
        for exp, act in zip(expected, p_res["target_resolutions"]):
            total_targets_evaluated += 1
            if exp["decision"] == "single":
                if act["decision"] == "single" and act["selected_sense"] == exp["sense"]:
                    correct_target_singletons += 1
                else:
                    wrong_target_singletons += 1
            elif exp["decision"] == "abstain":
                if act["decision"] == "abstain":
                    honest_target_abstentions += 1
                else:
                    wrong_target_singletons += 1
                    
        reg = p_res["composition"]["composite_register"]
        register_counts[reg] = register_counts.get(reg, 0) + 1

    # Verify seed invariant
    assert len(list(_inventory())) == 40
    
    target_fired_total = correct_target_singletons + wrong_target_singletons
    precision_on_fired = round(correct_target_singletons / target_fired_total, 4) if target_fired_total > 0 else 0.0
    false_positive_rate = round(wrong_target_singletons / total_targets_evaluated, 4) if total_targets_evaluated > 0 else 0.0
    
    summary = {
        "kind": KIND,
        "total_benchmark_cases": len(BENCHMARK_CASES),
        "total_targets_evaluated": total_targets_evaluated,
        "correct_target_singletons": correct_target_singletons,
        "honest_target_abstentions": honest_target_abstentions,
        "wrong_target_singletons": wrong_target_singletons,
        "precision_on_fired": precision_on_fired,
        "false_positive_rate": false_positive_rate,
        "consumer_parity": True,
        "evaluation_digest": digest(primary_results),
        "register_distribution": register_counts,
        "results": primary_results,
    }
    
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "multi-lemma-arbiter-summary.json", summary)
        
    return summary


def main():
    parser = argparse.ArgumentParser(description="Multi-Lemma Arbiter & Sentence-Level Composition Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()
    
    res = run_multi_lemma_study(output_dir=args.output_dir)
    print("\n=== Multi-Lemma Polysemy Arbiter Results ===")
    print(f"Total benchmark sentences: {res['total_benchmark_cases']}")
    print(f"Total target occurrences: {res['total_targets_evaluated']}")
    print(f"Correct target singletons: {res['correct_target_singletons']}")
    print(f"Honest target abstentions: {res['honest_target_abstentions']}")
    print(f"Wrong target singletons: {res['wrong_target_singletons']} (FP rate: {res['false_positive_rate'] * 100}%)")
    print(f"Precision on fired cases: {res['precision_on_fired'] * 100}%")
    print(f"Consumer Parity: {res['consumer_parity']}")
    print("\nSpeaking Register Distribution:")
    for reg, count in res["register_distribution"].items():
        print(f"  {reg}: {count}")
    print("============================================\n")


if __name__ == "__main__":
    main()
