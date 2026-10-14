"""Anchor Normalization & Deduplication Benchmark.

Evaluates surface variation normalization, redundant rule consolidation, witness aggregation,
and fuzzy confidence boost across candidate proposals extracted from corpora.

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.anchor_deduplication import (
    deduplicate_rules,
    OrdinaryMemoryDeduplicationComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "anchor-deduplication-benchmark-1"

# 20 Raw Candidate Proposals containing realistic surface phrasing variations
CANDIDATE_POOL_20 = [
    # Cluster 1: commercial bank (4 duplicate variations)
    {"rule_id": "c01", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "the commercial bank", "gloss": "a commercial financial depository", "witnesses": ["inst-01"], "weight": 0.50},
    {"rule_id": "c02", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "commercial bank.", "gloss": "a commercial financial institution for deposits and loans", "witnesses": ["inst-02"], "weight": 0.50},
    {"rule_id": "c03", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "a commercial bank", "gloss": "commercial bank institution", "witnesses": ["inst-03"], "weight": 0.50},
    {"rule_id": "c04", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "commercial bank", "gloss": "financial institution", "witnesses": ["inst-04"], "weight": 0.50},

    # Cluster 2: central bank (3 duplicate variations)
    {"rule_id": "c05", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "the central bank", "gloss": "national monetary authority", "witnesses": ["inst-05"], "weight": 0.50},
    {"rule_id": "c06", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "central bank.", "gloss": "a central bank managing currency and interest rates", "witnesses": ["inst-06"], "weight": 0.50},
    {"rule_id": "c07", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "central bank", "gloss": "monetary authority", "witnesses": ["inst-07"], "weight": 0.50},

    # Cluster 3: river bank (3 duplicate variations)
    {"rule_id": "c08", "lemma": "bank", "target_sense_key": "bank%1:17:01::", "core_pattern": "the river bank", "gloss": "sloping natural land bordering a river", "witnesses": ["inst-08"], "weight": 0.50},
    {"rule_id": "c09", "lemma": "bank", "target_sense_key": "bank%1:17:01::", "core_pattern": "river bank", "gloss": "natural river embankment", "witnesses": ["inst-09"], "weight": 0.50},
    {"rule_id": "c10", "lemma": "bank", "target_sense_key": "bank%1:17:01::", "core_pattern": "a river bank.", "gloss": "sloping land alongside a river", "witnesses": ["inst-10"], "weight": 0.50},

    # Cluster 4: court order (4 duplicate variations)
    {"rule_id": "c11", "lemma": "order", "target_sense_key": "order%1:10:00::", "core_pattern": "a court order", "gloss": "a formal court order or judicial decree", "witnesses": ["inst-11"], "weight": 0.50},
    {"rule_id": "c12", "lemma": "order", "target_sense_key": "order%1:10:00::", "core_pattern": "court order.", "gloss": "authoritative judicial command", "witnesses": ["inst-12"], "weight": 0.50},
    {"rule_id": "c13", "lemma": "order", "target_sense_key": "order%1:10:00::", "core_pattern": "the court order", "gloss": "judicial instruction", "witnesses": ["inst-13"], "weight": 0.50},
    {"rule_id": "c14", "lemma": "order", "target_sense_key": "order%1:10:00::", "core_pattern": "court order", "gloss": "authoritative instruction from a judge", "witnesses": ["inst-14"], "weight": 0.50},

    # Cluster 5: rank and order (3 duplicate variations)
    {"rule_id": "c15", "lemma": "order", "target_sense_key": "order%1:14:00::", "core_pattern": "rank and order", "gloss": "methodical alignment or sequence", "witnesses": ["inst-15"], "weight": 0.50},
    {"rule_id": "c16", "lemma": "order", "target_sense_key": "order%1:14:00::", "core_pattern": "the rank and order.", "gloss": "sequential arrangement of ranks", "witnesses": ["inst-16"], "weight": 0.50},
    {"rule_id": "c17", "lemma": "order", "target_sense_key": "order%1:14:00::", "core_pattern": "their rank and order", "gloss": "ordered ranks", "witnesses": ["inst-17"], "weight": 0.50},

    # Unique Standalone Rules (3 rules)
    {"rule_id": "c18", "lemma": "bank", "target_sense_key": "bank%1:14:01::", "core_pattern": "blood bank", "gloss": "medical reserve repository of blood supplies", "witnesses": ["inst-18"], "weight": 0.50},
    {"rule_id": "c19", "lemma": "order", "target_sense_key": "order%1:10:01::", "core_pattern": "placed an order", "gloss": "commercial purchase order requisition", "witnesses": ["inst-19"], "weight": 0.50},
    {"rule_id": "c20", "lemma": "order", "target_sense_key": "order%1:07:01::", "core_pattern": "order of magnitude", "gloss": "scale of quantitative degree or magnitude", "witnesses": ["inst-20"], "weight": 0.50},
]


def run_anchor_deduplication_study(output_dir=None):
    """Executes anchor normalization and deduplication benchmark with baseline parity."""
    comparator = OrdinaryMemoryDeduplicationComparator()
    
    primary_canonical, p_stats = deduplicate_rules(CANDIDATE_POOL_20)
    baseline_canonical, b_stats = comparator.deduplicate(CANDIDATE_POOL_20)
    
    # Parity check
    assert digest(primary_canonical) == digest(baseline_canonical)
    assert digest(p_stats) == digest(b_stats)
    
    # Assertions
    assert p_stats["initial_candidates_count"] == 20
    assert p_stats["canonical_rules_count"] == 8
    assert p_stats["duplicates_merged"] == 12
    assert p_stats["compression_ratio"] == 0.40
    
    # Verify seed invariant
    assert len(list(_inventory())) == 40
    
    summary = {
        "kind": KIND,
        "initial_candidates_count": p_stats["initial_candidates_count"],
        "canonical_rules_count": p_stats["canonical_rules_count"],
        "duplicates_merged": p_stats["duplicates_merged"],
        "compression_ratio": p_stats["compression_ratio"],
        "consumer_parity": True,
        "evaluation_digest": digest(primary_canonical),
        "canonical_rules": primary_canonical,
    }
    
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "anchor-deduplication-summary.json", summary)
        
    return summary


def main():
    parser = argparse.ArgumentParser(description="Anchor Normalization & Deduplication Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()
    
    res = run_anchor_deduplication_study(output_dir=args.output_dir)
    print("\n=== Anchor Normalization & Deduplication Results ===")
    print(f"Initial Candidate Proposals: {res['initial_candidates_count']}")
    print(f"Canonical Consolidated Rules: {res['canonical_rules_count']}")
    print(f"Redundant Duplicates Merged: {res['duplicates_merged']}")
    print(f"Memory Compression Ratio: {res['compression_ratio'] * 100}%")
    print(f"Consumer Parity Verified: {res['consumer_parity']}")
    print("\nConsolidated Canonical Rules:")
    for r in res["canonical_rules"]:
        print(f"  [{r['lemma']}] '{r['core_pattern']}' -> weight: {r['weight']} (witnesses: {len(r['witnesses'])})")
    print("====================================================\n")


if __name__ == "__main__":
    main()
