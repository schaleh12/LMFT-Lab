"""Unit tests for Persistent Capacity Memory Decay & Reinforcement Dynamics.

Verifies:
1. Asymptotic reinforcement towards ceiling 1.00 under repeated consistent evidence.
2. Monotonic habituation decay towards floor 0.10 under inactivity.
3. Rapid penalty damping on contradiction.
4. Boundedness: weights never exceed [0.10, 1.00].
5. Matched ordinary-memory baseline parity (Rule D004).
6. Invariance of canonical 40 founding nodes in birth.py (Rule D001).
"""
import pytest
from lmft_lab.birth import _inventory
from lmft_lab.capacity_decay import (
    reinforce_weight,
    decay_weight,
    damp_weight,
    initial_capacity_rule,
    step_capacity_epoch,
    OrdinaryMemoryDecayComparator,
    WEIGHT_FLOOR,
    WEIGHT_CEILING,
)
from lmft_lab.runtime_store import digest


def test_reinforcement_asymptotic_convergence():
    """Verifies that repeated reinforcement asymptotically approaches 1.00."""
    w = 0.50
    weights = [w]
    for _ in range(35):
        w = reinforce_weight(w, alpha=0.25)
        weights.append(w)
        assert WEIGHT_FLOOR <= w <= WEIGHT_CEILING

    # Verify strictly non-decreasing and reaches ceiling
    for i in range(len(weights) - 1):
        assert weights[i+1] >= weights[i]
    assert weights[-1] == 1.00


def test_decay_monotonic_floor():
    """Verifies that repeated inactivity monotonically approaches floor 0.10 without falling below."""
    w = 0.90
    weights = [w]
    for _ in range(30):
        w = decay_weight(w, lam=0.10)
        weights.append(w)
        assert WEIGHT_FLOOR <= w <= WEIGHT_CEILING

    # Verify strictly non-increasing and reaches floor
    for i in range(len(weights) - 1):
        assert weights[i+1] <= weights[i]
    assert weights[-1] == 0.10


def test_damping_penalty_on_contradiction():
    """Verifies that contradiction applies immediate, bounded penalty."""
    w_start = 0.80
    w_damped = damp_weight(w_start, beta=0.35)
    assert w_damped == 0.52
    
    # Repeated damping clamps to floor
    for _ in range(10):
        w_damped = damp_weight(w_damped, beta=0.50)
    assert w_damped == WEIGHT_FLOOR


def test_multi_rule_epoch_progression():
    """Verifies discrete multi-rule epoch dynamics."""
    r1 = initial_capacity_rule("r1", "sense-a", "core-a", "gloss a", initial_weight=0.50)
    r2 = initial_capacity_rule("r2", "sense-b", "core-b", "gloss b", initial_weight=0.70)
    r3 = initial_capacity_rule("r3", "sense-c", "core-c", "gloss c", initial_weight=0.60)
    
    rules = [r1, r2, r3]
    
    # Epoch 1: r1 reinforced, r2 idle (decay), r3 contradicted (damped)
    rules, summary = step_capacity_epoch(
        rules,
        reinforced_rule_ids=["r1"],
        contradicted_rule_ids=["r3"],
        alpha=0.20,
        lam=0.05,
        beta=0.30,
    )
    
    assert summary["epoch"] == 1
    assert summary["reinforced_count"] == 1
    assert summary["decayed_count"] == 1
    assert summary["contradicted_count"] == 1
    
    # r1: 0.50 + 0.20 * (1 - 0.50) = 0.60
    assert rules[0]["weight"] == 0.60
    # r2: 0.70 * (1 - 0.05) = 0.665 -> 0.665
    assert rules[1]["weight"] == 0.665
    # r3: 0.60 * (1 - 0.30) = 0.42
    assert rules[2]["weight"] == 0.42


def test_ordinary_memory_baseline_parity():
    """Verifies byte-for-byte evaluation parity with the matched ordinary-memory comparator (Rule D004)."""
    initial_rules = [
        initial_capacity_rule("r1", "sense-a", "pattern-a", "gloss a", 0.50),
        initial_capacity_rule("r2", "sense-b", "pattern-b", "gloss b", 0.60),
        initial_capacity_rule("r3", "sense-c", "pattern-c", "gloss c", 0.70),
    ]
    
    comparator = OrdinaryMemoryDecayComparator(initial_rules)
    primary_rules = initial_rules
    
    # Run 5 simulated epochs
    schedule = [
        (["r1"], ["r3"]),
        (["r2"], []),
        (["r1", "r2"], []),
        ([], ["r1"]),
        (["r3"], []),
    ]
    
    for reinf, cont in schedule:
        primary_rules, p_sum = step_capacity_epoch(primary_rules, reinf, contradicted_rule_ids=cont)
        comp_rules, c_sum = comparator.step(reinf, contradicted_rule_ids=cont)
        
        assert digest(primary_rules) == digest(comp_rules)
        assert digest(p_sum) == digest(c_sum)


def test_frozen_seed_invariant_preserved():
    """Verifies that the canonical 40 founding nodes in birth.py remain strictly invariant (Rule D001)."""
    inventory = list(_inventory())
    assert len(inventory) == 40
    domains = {item[2] for item in inventory}
    assert domains == {"cultural", "philosophical", "experiential", "psychological"}
