"""Capacity Memory Decay & Reinforcement Benchmark.

Evaluates multi-epoch fuzzy habituation, reinforcement curves, and contradiction
damping on learned capacity rules without mutating the canonical 40-node seed geometry.

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
from lmft_lab.capacity_decay import (
    initial_capacity_rule,
    step_capacity_epoch,
    OrdinaryMemoryDecayComparator,
    WEIGHT_FLOOR,
    WEIGHT_CEILING,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "capacity-decay-benchmark-1"

# Initial benchmark rule set (5 representative rules across order and bank)
BENCHMARK_RULES = [
    initial_capacity_rule("rule-bank-com", "bank%1:14:00::", "commercial bank", "financial institution", 0.50),
    initial_capacity_rule("rule-bank-riv", "bank%1:17:01::", "river bank", "river embankment", 0.50),
    initial_capacity_rule("rule-order-cmd", "order%1:10:00::", "court order", "authoritative command", 0.50),
    initial_capacity_rule("rule-order-com", "order%1:10:01::", "placed an order", "commercial transaction", 0.50),
    initial_capacity_rule("rule-order-mag", "order%1:07:01::", "order of magnitude", "scale of degree", 0.50),
]

# 10-Epoch simulated interaction schedule
EPOCH_SCHEDULE = [
    # Epoch 1: Bank commercial reinforced, order commercial reinforced
    {"reinforced": ["rule-bank-com", "rule-order-com"], "contradicted": []},
    # Epoch 2: River bank reinforced, order command reinforced
    {"reinforced": ["rule-bank-riv", "rule-order-cmd"], "contradicted": []},
    # Epoch 3: Commercial bank reinforced again, order magnitude reinforced
    {"reinforced": ["rule-bank-com", "rule-order-mag"], "contradicted": []},
    # Epoch 4: Contradiction on order magnitude (e.g. false trigger reported)
    {"reinforced": ["rule-order-com"], "contradicted": ["rule-order-mag"]},
    # Epoch 5: Idle epoch across all rules (system inactive / habituation test)
    {"reinforced": [], "contradicted": []},
    # Epoch 6: River bank reinforced
    {"reinforced": ["rule-bank-riv"], "contradicted": []},
    # Epoch 7: Commercial bank reinforced (approaching ceiling)
    {"reinforced": ["rule-bank-com"], "contradicted": []},
    # Epoch 8: Court order reinforced
    {"reinforced": ["rule-order-cmd"], "contradicted": []},
    # Epoch 9: Prolonged idle decay test
    {"reinforced": [], "contradicted": []},
    # Epoch 10: Final reinforcement test on bank commercial & river bank
    {"reinforced": ["rule-bank-com", "rule-bank-riv"], "contradicted": []},
]


def run_capacity_decay_study(output_dir=None):
    """Executes multi-epoch decay and reinforcement study with baseline parity."""
    primary_rules = deepcopy(BENCHMARK_RULES)
    comparator = OrdinaryMemoryDecayComparator(BENCHMARK_RULES)
    
    epoch_history = []
    
    for epoch_idx, step in enumerate(EPOCH_SCHEDULE, 1):
        reinf = step["reinforced"]
        cont = step["contradicted"]
        
        primary_rules, p_sum = step_capacity_epoch(primary_rules, reinf, contradicted_rule_ids=cont)
        comp_rules, c_sum = comparator.step(reinf, contradicted_rule_ids=cont)
        
        # Parity check
        assert digest(primary_rules) == digest(comp_rules), f"Parity mismatch at epoch {epoch_idx}"
        assert digest(p_sum) == digest(c_sum), f"Summary parity mismatch at epoch {epoch_idx}"
        
        # Invariant checks: all weights bounded in [0.10, 1.00]
        for r in primary_rules:
            assert WEIGHT_FLOOR <= r["weight"] <= WEIGHT_CEILING
            
        epoch_history.append(p_sum)

    # Verify seed invariant
    assert len(list(_inventory())) == 40
    
    final_weights = {r["rule_id"]: r["weight"] for r in primary_rules}
    
    summary = {
        "kind": KIND,
        "total_epochs": len(EPOCH_SCHEDULE),
        "total_rules": len(BENCHMARK_RULES),
        "final_weights": final_weights,
        "consumer_parity": True,
        "evaluation_digest": digest(primary_rules),
        "epoch_history": epoch_history,
        "final_rules": primary_rules,
    }
    
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "capacity-decay-summary.json", summary)
        
    return summary


def main():
    parser = argparse.ArgumentParser(description="LMFT Capacity Memory Decay & Reinforcement Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()
    
    res = run_capacity_decay_study(output_dir=args.output_dir)
    print("\n=== Capacity Memory Decay & Reinforcement Results ===")
    print(f"Total simulated epochs: {res['total_epochs']}")
    print(f"Total rules tracked: {res['total_rules']}")
    print(f"Consumer Parity Verified: {res['consumer_parity']}")
    print("\nFinal Rule Weights:")
    for rid, w in res["final_weights"].items():
        print(f"  {rid}: {w}")
    print("====================================================\n")


if __name__ == "__main__":
    main()
