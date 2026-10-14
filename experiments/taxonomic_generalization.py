"""Taxonomic Hypernym Generalization Benchmark.

Evaluates hypernym path traversal, abstract category extraction, and canonical leaf dial
modulation across 11 WordNet senses from 'bank' and 'order' plus control instances.

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
from lmft_lab.taxonomic_generalization import (
    CANONICAL_LEAF_IDS,
    TAXONOMIC_REGISTRY,
    TaxonomicGeneralizer,
    OrdinaryMemoryTaxonomicComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "taxonomic-generalization-benchmark-1"

# 12 Evaluation instances (11 registered senses + 1 unregistered control)
BENCHMARK_SENSES = [
    # Bank senses
    "bank%1:14:00::",  # financial_institution
    "bank%1:17:01::",  # river_bank / slope
    "bank%1:14:01::",  # reserve_repository / depository
    # Order senses
    "order%1:10:00::",  # judicial_decree / legal_document
    "order%1:10:01::",  # commercial_purchase / commercial_document
    "order%1:10:02::",  # sequence_succession / arrangement
    "order%1:10:03::",  # authoritative_command / speech_act
    "order%1:14:00::",  # sequence_ordering / sorting
    "order%1:07:01::",  # degree_magnitude / magnitude
    "order%1:26:00::",  # social_condition / condition
    "order%1:26:02::",  # systematic_arrangement / structure
    # Control instance
    "unregistered%1:00:00::",  # unanchored out-of-domain control
]


def run_taxonomic_generalization_study(output_dir=None):
    """Executes taxonomic generalization and parity checks across all benchmark senses."""
    generalizer = TaxonomicGeneralizer()
    comparator = OrdinaryMemoryTaxonomicComparator()

    results = []
    category_counts = {}
    total_modulations = 0
    parity_passed = True

    for sense_key in BENCHMARK_SENSES:
        p_res = generalizer.compute_taxonomic_modulation(sense_key, weight=0.70)
        c_res = comparator.modulate(sense_key, weight=0.70)

        # Rule D004: byte-for-byte evaluation digest parity
        if digest(p_res) != digest(c_res):
            parity_passed = False

        if p_res["found"]:
            cat = p_res["primary_category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1
            total_modulations += len(p_res["applied_affinities"])

        explanation = generalizer.explain_taxonomic_derivation(sense_key)

        results.append({
            "sense_key": sense_key,
            "found": p_res["found"],
            "primary_category": p_res["primary_category"],
            "hypernym_depth": len(p_res["hypernym_path"]),
            "hypernym_path": p_res["hypernym_path"],
            "applied_affinities": p_res["applied_affinities"],
            "explanation": explanation,
            "digest": digest(p_res),
        })

    # Rule D001: seed inventory check
    seed_nodes = list(_inventory())
    assert len(seed_nodes) == 40, f"Seed corrupted: expected 40 nodes, found {len(seed_nodes)}"

    summary = {
        "kind": KIND,
        "total_evaluated_senses": len(BENCHMARK_SENSES),
        "registered_senses_count": len([r for r in results if r["found"]]),
        "control_senses_count": len([r for r in results if not r["found"]]),
        "primary_categories_count": len(category_counts),
        "category_distribution": category_counts,
        "total_leaf_modulations_applied": total_modulations,
        "consumer_parity": parity_passed,
        "frozen_seed_invariant_enforced": True,
        "evaluation_digest": digest(results),
        "results": results,
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "taxonomic-generalization-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Taxonomic Hypernym Generalization Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    summary = run_taxonomic_generalization_study(output_dir=args.output_dir)

    print("\n=== Taxonomic Hypernym Generalization Benchmark ===")
    print(f"Total Senses Evaluated: {summary['total_evaluated_senses']}")
    print(f"Registered Senses: {summary['registered_senses_count']}")
    print(f"Control Senses: {summary['control_senses_count']}")
    print(f"Unique Abstract Categories: {summary['primary_categories_count']}")
    print(f"Total Canonical Leaf Modulations: {summary['total_leaf_modulations_applied']}")
    print(f"Rule D004 Matched Parity: {summary['consumer_parity']}")
    print(f"Rule D001 Seed Invariant: {summary['frozen_seed_invariant_enforced']}")
    print("===================================================\n")


if __name__ == "__main__":
    main()
