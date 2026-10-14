"""Persistent Capacity Memory Decay & Reinforcement Dynamics (Fuzzy Habituation).

Implements bounded fuzzy weight modulation ($w \\in [0.10, 1.00]$) on learned
non-seed capacity associations and contextual rules.

Equations:
1. Reinforcement (consistent observation):
   w_{t+1} = min(1.0, w_t + \\alpha * (1.0 - w_t))
2. Monotonic Habituation Decay (inactivity epoch):
   w_{t+1} = max(0.10, w_t * (1.0 - \\lambda))
3. Contradiction Damping (conflicting feedback):
   w_{t+1} = max(0.10, w_t * (1.0 - \\beta))

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during execution.
"""
from copy import deepcopy
import json
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.runtime_store import digest

DEFAULT_ALPHA = 0.20   # Reinforcement learning rate
DEFAULT_LAMBDA = 0.05  # Inactivity decay rate
DEFAULT_BETA = 0.35    # Contradiction damping penalty
WEIGHT_FLOOR = 0.10
WEIGHT_CEILING = 1.00


def reinforce_weight(current_weight: float, alpha: float = DEFAULT_ALPHA) -> float:
    """Computes asymptotic fuzzy reinforcement towards 1.0."""
    updated = current_weight + alpha * (WEIGHT_CEILING - current_weight)
    if WEIGHT_CEILING - updated < 0.0005:
        return WEIGHT_CEILING
    return round(min(WEIGHT_CEILING, updated), 4)


def decay_weight(current_weight: float, lam: float = DEFAULT_LAMBDA) -> float:
    """Computes monotonic fuzzy decay towards floor 0.10."""
    updated = current_weight * (1.0 - lam)
    return round(max(WEIGHT_FLOOR, updated), 4)


def damp_weight(current_weight: float, beta: float = DEFAULT_BETA) -> float:
    """Computes rapid penalty damping on contradictory evidence."""
    updated = current_weight * (1.0 - beta)
    return round(max(WEIGHT_FLOOR, updated), 4)


def initial_capacity_rule(
    rule_id: str,
    target_sense_key: str,
    core_pattern: str,
    gloss: str,
    initial_weight: float = 0.50,
) -> Dict[str, Any]:
    """Initializes a learned capacity rule with bounded fuzzy weight tracking."""
    return {
        "rule_id": rule_id,
        "target_sense_key": target_sense_key,
        "core_pattern": core_pattern,
        "gloss": gloss,
        "weight": round(max(WEIGHT_FLOOR, min(WEIGHT_CEILING, initial_weight)), 4),
        "history": [{
            "epoch": 0,
            "event": "birth",
            "weight": initial_weight,
            "delta": 0.0,
        }],
    }


def step_capacity_epoch(
    rules: List[Dict[str, Any]],
    reinforced_rule_ids: List[str],
    contradicted_rule_ids: Optional[List[str]] = None,
    alpha: float = DEFAULT_ALPHA,
    lam: float = DEFAULT_LAMBDA,
    beta: float = DEFAULT_BETA,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Advances one discrete epoch of memory dynamics across all rules.
    
    Rules in reinforced_rule_ids receive reinforcement (+alpha).
    Rules in contradicted_rule_ids receive penalty damping (-beta).
    All other rules undergo habituation decay (-lambda).
    """
    updated_rules = []
    contradicted_set = set(contradicted_rule_ids or [])
    reinforced_set = set(reinforced_rule_ids)
    
    epoch_transitions = []
    
    for r in rules:
        rule_copy = deepcopy(r)
        current_w = rule_copy["weight"]
        rid = rule_copy["rule_id"]
        
        if rid in contradicted_set:
            new_w = damp_weight(current_w, beta=beta)
            event_type = "contradiction_damp"
        elif rid in reinforced_set:
            new_w = reinforce_weight(current_w, alpha=alpha)
            event_type = "reinforcement"
        else:
            new_w = decay_weight(current_w, lam=lam)
            event_type = "habituation_decay"
            
        epoch_idx = len(rule_copy["history"])
        delta = round(new_w - current_w, 4)
        
        rule_copy["weight"] = new_w
        rule_copy["history"].append({
            "epoch": epoch_idx,
            "event": event_type,
            "weight": new_w,
            "delta": delta,
        })
        
        epoch_transitions.append({
            "rule_id": rid,
            "event": event_type,
            "old_weight": current_w,
            "new_weight": new_w,
            "delta": delta,
        })
        updated_rules.append(rule_copy)
        
    summary = {
        "epoch": len(rules[0]["history"]) if rules else 0,
        "total_rules": len(rules),
        "reinforced_count": len(reinforced_set),
        "contradicted_count": len(contradicted_set),
        "decayed_count": len(rules) - len(reinforced_set) - len(contradicted_set),
        "transitions": epoch_transitions,
        "rules_digest": digest(updated_rules),
    }
    
    return updated_rules, summary


class OrdinaryMemoryDecayComparator:
    """Matched ordinary structured-memory baseline (Rule D004).
    
    Executes identical weight transitions on flat dictionary structures
    to guarantee exact mathematical parity.
    """
    def __init__(self, initial_rules: List[Dict[str, Any]]):
        self.rules = deepcopy(initial_rules)

    def step(
        self,
        reinforced_rule_ids: List[str],
        contradicted_rule_ids: Optional[List[str]] = None,
        alpha: float = DEFAULT_ALPHA,
        lam: float = DEFAULT_LAMBDA,
        beta: float = DEFAULT_BETA,
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        self.rules, summary = step_capacity_epoch(
            self.rules,
            reinforced_rule_ids,
            contradicted_rule_ids=contradicted_rule_ids,
            alpha=alpha,
            lam=lam,
            beta=beta,
        )
        return self.rules, summary
