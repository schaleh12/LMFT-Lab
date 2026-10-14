"""Inverted Lemma Index & Context Trie Scalability Benchmark.

Evaluates sub-millisecond retrieval latency, exact candidate filtering, and 100% equivalence
against linear scanning across 1,000 synthetic capacity rules and multi-target queries.

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.inverted_trie import (
    InvertedLemmaIndex,
    linear_scan_rules,
    OrdinaryMemoryInvertedComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "inverted-trie-benchmark-1"

# Base real capacity rules
BASE_RULES = [
    {"rule_id": "rule-bank-com", "lemma": "bank", "core_pattern": "commercial bank", "target_sense_key": "bank%1:14:00::"},
    {"rule_id": "rule-bank-cen", "lemma": "bank", "core_pattern": "central bank", "target_sense_key": "bank%1:14:00::"},
    {"rule_id": "rule-bank-inv", "lemma": "bank", "core_pattern": "investment bank", "target_sense_key": "bank%1:14:00::"},
    {"rule_id": "rule-bank-riv", "lemma": "bank", "core_pattern": "river bank", "target_sense_key": "bank%1:17:01::"},
    {"rule_id": "rule-bank-str", "lemma": "bank", "core_pattern": "bank of the stream", "target_sense_key": "bank%1:17:01::"},
    {"rule_id": "rule-bank-bld", "lemma": "bank", "core_pattern": "blood bank", "target_sense_key": "bank%1:14:01::"},
    {"rule_id": "rule-order-cmd", "lemma": "order", "core_pattern": "court order", "target_sense_key": "order%1:10:00::"},
    {"rule_id": "rule-order-str", "lemma": "order", "core_pattern": "strict order", "target_sense_key": "order%1:10:00::"},
    {"rule_id": "rule-order-com", "lemma": "order", "core_pattern": "placed an order", "target_sense_key": "order%1:10:01::"},
    {"rule_id": "rule-order-seq", "lemma": "order", "core_pattern": "rank and order", "target_sense_key": "order%1:14:00::"},
    {"rule_id": "rule-order-mag", "lemma": "order", "core_pattern": "order of magnitude", "target_sense_key": "order%1:07:01::"},
]

BENCHMARK_TEST_SENTENCES = [
    "The local commercial bank received a strict court order to freeze the assets.",
    "They placed an order for emergency supplies while resting along the river bank.",
    "The patrol marched in rank and order along the steep bank of the stream.",
    "The blood bank calculated the order of magnitude of required reserves.",
    "He walked toward the central bank without further explanation.",
    "A calm evening in the forest without any matching polysemous anchors.",
]


def generate_scale_rules(total_target: int = 1000) -> List[Dict[str, Any]]:
    """Synthesizes a realistic large-scale capacity rule pool for stress-testing."""
    rules = list(BASE_RULES)
    remaining = total_target - len(rules)
    
    prefixes = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]
    nouns = ["system", "process", "device", "entity", "structure", "channel", "circuit", "protocol"]
    
    for i in range(remaining):
        p = prefixes[i % len(prefixes)]
        n = nouns[(i // len(prefixes)) % len(nouns)]
        rules.append({
            "rule_id": f"syn-rule-{i:04d}",
            "lemma": f"term_{i % 50}",
            "core_pattern": f"{p} {n} variant {i}",
            "target_sense_key": f"sense%1:{i % 20}:00::",
        })
    return rules


def run_inverted_trie_study(output_dir=None, rule_count: int = 1000):
    """Executes scalability benchmark comparing InvertedLemmaIndex vs Linear Scan."""
    rule_pool = generate_scale_rules(rule_count)
    
    # 1. Build Inverted Index & Comparator
    build_start = time.perf_counter()
    index = InvertedLemmaIndex()
    for r in rule_pool:
        index.add_rule(r)
    build_time_ms = round((time.perf_counter() - build_start) * 1000, 2)
    
    comparator = OrdinaryMemoryInvertedComparator(rule_pool)
    
    # 2. Benchmark Queries
    query_results = []
    total_fast_time = 0.0
    total_linear_time = 0.0
    
    for sent in BENCHMARK_TEST_SENTENCES:
        # Measure Inverted Index
        t0 = time.perf_counter()
        fast_matches = index.match_sentence(sent)
        fast_elapsed_ms = (time.perf_counter() - t0) * 1000
        total_fast_time += fast_elapsed_ms
        
        # Measure Linear Scan
        t1 = time.perf_counter()
        linear_matches = linear_scan_rules(rule_pool, sent)
        linear_elapsed_ms = (time.perf_counter() - t1) * 1000
        total_linear_time += linear_elapsed_ms
        
        # Parity check
        fast_ids = sorted({r["rule_id"] for r in fast_matches})
        linear_ids = sorted({r["rule_id"] for r in linear_matches})
        assert fast_ids == linear_ids, f"Equivalence divergence on sentence: '{sent}'"
        
        # Comparator check
        comp_res = comparator.evaluate(sent)
        assert comp_res["matched_rules"] == fast_ids
        
        query_results.append({
            "sentence": sent,
            "matched_rules": fast_ids,
            "fast_latency_ms": round(fast_elapsed_ms, 3),
            "linear_latency_ms": round(linear_elapsed_ms, 3),
        })

    # Verify seed invariant
    assert len(list(_inventory())) == 40
    
    avg_fast_ms = round(total_fast_time / len(BENCHMARK_TEST_SENTENCES), 3)
    avg_linear_ms = round(total_linear_time / len(BENCHMARK_TEST_SENTENCES), 3)
    speedup = round(avg_linear_ms / avg_fast_ms, 2) if avg_fast_ms > 0 else 1.0
    
    summary = {
        "kind": KIND,
        "total_rules_indexed": len(rule_pool),
        "index_build_time_ms": build_time_ms,
        "test_sentences_count": len(BENCHMARK_TEST_SENTENCES),
        "average_inverted_latency_ms": avg_fast_ms,
        "average_linear_latency_ms": avg_linear_ms,
        "latency_speedup_factor": speedup,
        "consumer_parity": True,
        "evaluation_digest": digest(query_results),
        "query_results": query_results,
    }
    
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "inverted-trie-summary.json", summary)
        
    return summary


def main():
    parser = argparse.ArgumentParser(description="Inverted Lemma Index & Context Trie Scalability Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    parser.add_argument("--rules", type=int, default=1000, help="Number of rules to index")
    args = parser.parse_args()
    
    res = run_inverted_trie_study(output_dir=args.output_dir, rule_count=args.rules)
    print("\n=== Inverted Lemma Index & Context Trie Benchmark Results ===")
    print(f"Total Rules Indexed: {res['total_rules_indexed']}")
    print(f"Index Construction Time: {res['index_build_time_ms']} ms")
    print(f"Average Inverted Index Latency: {res['average_inverted_latency_ms']} ms")
    print(f"Average Linear Scan Latency: {res['average_linear_latency_ms']} ms")
    print(f"Speedup Factor: {res['latency_speedup_factor']}x faster")
    print(f"Consumer Parity Verified: {res['consumer_parity']}")
    print("=============================================================\n")


if __name__ == "__main__":
    main()
