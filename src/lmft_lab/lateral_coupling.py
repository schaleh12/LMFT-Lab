"""Lateral Ethical-Ontological Coupling Matrix.

Cross-couples the 6 Cultural leaves (Ethics/Governance) with the 6 Philosophical leaves
(Metaphysics/Ontology), establishing continuous mutual regulation between moral conscience
and existential reality without mutating or expanding the frozen 40-node founding seed (Rule D001).

Zero runtime LLM calls during unassisted evaluation.
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest


# Verify and cache canonical leaf IDs from birth.py
CANONICAL_LEAF_IDS = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}

CULTURAL_LEAF_IDS = [
    "cultural/efficiency/power",
    "cultural/efficiency/wastelessness",
    "cultural/justice/honor",
    "cultural/justice/fairness",
    "cultural/freedom/self-sufficiency",
    "cultural/freedom/needlessness",
]

PHILOSOPHICAL_LEAF_IDS = [
    "philosophical/being/agency",
    "philosophical/being/existence",
    "philosophical/structure/order",
    "philosophical/structure/chaos",
    "philosophical/persistence/continuity",
    "philosophical/persistence/discreteness",
]

# Ensure all tracked IDs belong strictly to the canonical 24 leaf inventory
for leaf_id in CULTURAL_LEAF_IDS + PHILOSOPHICAL_LEAF_IDS:
    assert leaf_id in CANONICAL_LEAF_IDS, f"Invalid canonical leaf ID: {leaf_id}"


# Principled Cross-Coupling Weights: Cultural -> Philosophical
CULTURAL_TO_PHILOSOPHICAL_WEIGHTS: Dict[str, Dict[str, float]] = {
    # Power demands Order to prevent tyranny and elevates Agency
    "cultural/efficiency/power": {
        "philosophical/being/agency": 0.25,
        "philosophical/structure/order": 0.20,
    },
    # Wastelessness aligns with Discreteness (bounded atomic resources)
    "cultural/efficiency/wastelessness": {
        "philosophical/persistence/discreteness": 0.25,
    },
    # Honor strengthens Agency and Order
    "cultural/justice/honor": {
        "philosophical/being/agency": 0.20,
        "philosophical/structure/order": 0.25,
    },
    # Fairness reinforces Existence and Continuity across time
    "cultural/justice/fairness": {
        "philosophical/being/existence": 0.20,
        "philosophical/persistence/continuity": 0.25,
    },
    # Self-Sufficiency reinforces Agency
    "cultural/freedom/self-sufficiency": {
        "philosophical/being/agency": 0.30,
    },
    # Needlessness reinforces serene Existence
    "cultural/freedom/needlessness": {
        "philosophical/being/existence": 0.25,
        "philosophical/being/agency": 0.15,
    },
}

# Principled Cross-Coupling Weights: Philosophical -> Cultural
PHILOSOPHICAL_TO_CULTURAL_WEIGHTS: Dict[str, Dict[str, float]] = {
    # Agency elevates Power and Self-Sufficiency
    "philosophical/being/agency": {
        "cultural/efficiency/power": 0.25,
        "cultural/freedom/self-sufficiency": 0.25,
    },
    # Existence elevates Fairness and Needlessness
    "philosophical/being/existence": {
        "cultural/justice/fairness": 0.20,
        "cultural/freedom/needlessness": 0.20,
    },
    # Order reinforces Honor and Wastelessness
    "philosophical/structure/order": {
        "cultural/justice/honor": 0.25,
        "cultural/efficiency/wastelessness": 0.20,
    },
    # Chaos triggers moral ballast: activates Honor and Self-Sufficiency under volatility
    "philosophical/structure/chaos": {
        "cultural/justice/honor": 0.25,
        "cultural/freedom/self-sufficiency": 0.20,
    },
    # Continuity supports societal Fairness and Needlessness
    "philosophical/persistence/continuity": {
        "cultural/justice/fairness": 0.25,
        "cultural/freedom/needlessness": 0.15,
    },
    # Discreteness supports Wastelessness
    "philosophical/persistence/discreteness": {
        "cultural/efficiency/wastelessness": 0.25,
    },
}


class LateralCouplingEngine:
    """Executes mutual ethical-ontological regulation between Cultural and Philosophical leaves."""

    def __init__(
        self,
        c_to_p_weights: Optional[Dict[str, Dict[str, float]]] = None,
        p_to_c_weights: Optional[Dict[str, Dict[str, float]]] = None,
    ):
        self.c_to_p = c_to_p_weights or deepcopy(CULTURAL_TO_PHILOSOPHICAL_WEIGHTS)
        self.p_to_c = p_to_c_weights or deepcopy(PHILOSOPHICAL_TO_CULTURAL_WEIGHTS)

    def couple(
        self,
        cultural_dials: Optional[Dict[str, float]] = None,
        philosophical_dials: Optional[Dict[str, float]] = None,
        coupling_gain: float = 1.0,
    ) -> Dict[str, Any]:
        """Calculates bidirectional lateral adjustments and returns unified coupled states."""
        gain = max(0.0, min(2.0, float(coupling_gain)))

        # Default all tracked leaves to 0.50 if not specified
        cult = {k: 0.50 for k in CULTURAL_LEAF_IDS}
        if cultural_dials:
            for k, v in cultural_dials.items():
                if k in cult:
                    cult[k] = float(v)

        phil = {k: 0.50 for k in PHILOSOPHICAL_LEAF_IDS}
        if philosophical_dials:
            for k, v in philosophical_dials.items():
                if k in phil:
                    phil[k] = float(v)

        # 1. Compute delta on Philosophical from Cultural deviations
        delta_phil = {k: 0.0 for k in PHILOSOPHICAL_LEAF_IDS}
        for c_id, targets in self.c_to_p.items():
            c_dev = cult[c_id] - 0.50
            for p_id, weight in targets.items():
                if p_id in delta_phil:
                    delta_phil[p_id] += c_dev * weight * gain

        # 2. Compute delta on Cultural from Philosophical deviations
        delta_cult = {k: 0.0 for k in CULTURAL_LEAF_IDS}
        for p_id, targets in self.p_to_c.items():
            p_dev = phil[p_id] - 0.50
            for c_id, weight in targets.items():
                if c_id in delta_cult:
                    delta_cult[c_id] += p_dev * weight * gain

        # 3. Apply deltas with strict [0.0, 1.0] bound enforcement
        coupled_phil = {}
        for k in PHILOSOPHICAL_LEAF_IDS:
            new_val = round(min(1.0, max(0.0, phil[k] + delta_phil[k])), 4)
            coupled_phil[k] = new_val

        coupled_cult = {}
        for k in CULTURAL_LEAF_IDS:
            new_val = round(min(1.0, max(0.0, cult[k] + delta_cult[k])), 4)
            coupled_cult[k] = new_val

        # 4. Synthesize Cohesion Metrics
        governance_balance = round(
            1.0 - abs(coupled_cult["cultural/efficiency/power"] - coupled_phil["philosophical/structure/order"]), 4
        )
        moral_ballast = round(
            (coupled_cult["cultural/justice/honor"] + coupled_cult["cultural/freedom/self-sufficiency"]) / 2.0, 4
        )

        return {
            "initial_cultural": cult,
            "initial_philosophical": phil,
            "delta_cultural": {k: round(v, 4) for k, v in delta_cult.items()},
            "delta_philosophical": {k: round(v, 4) for k, v in delta_phil.items()},
            "coupled_cultural": coupled_cult,
            "coupled_philosophical": coupled_phil,
            "cohesion_metrics": {
                "governance_balance": governance_balance,
                "moral_ballast": moral_ballast,
            },
        }


class OrdinaryMemoryLateralComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def __init__(
        self,
        c_to_p_weights: Optional[Dict[str, Dict[str, float]]] = None,
        p_to_c_weights: Optional[Dict[str, Dict[str, float]]] = None,
    ):
        self.c_to_p = c_to_p_weights or deepcopy(CULTURAL_TO_PHILOSOPHICAL_WEIGHTS)
        self.p_to_c = p_to_c_weights or deepcopy(PHILOSOPHICAL_TO_CULTURAL_WEIGHTS)

    def couple(
        self,
        cultural_dials: Optional[Dict[str, float]] = None,
        philosophical_dials: Optional[Dict[str, float]] = None,
        coupling_gain: float = 1.0,
    ) -> Dict[str, Any]:
        gain = max(0.0, min(2.0, float(coupling_gain)))

        cult = {k: 0.50 for k in CULTURAL_LEAF_IDS}
        if cultural_dials:
            for k, v in cultural_dials.items():
                if k in cult:
                    cult[k] = float(v)

        phil = {k: 0.50 for k in PHILOSOPHICAL_LEAF_IDS}
        if philosophical_dials:
            for k, v in philosophical_dials.items():
                if k in phil:
                    phil[k] = float(v)

        delta_phil = {k: 0.0 for k in PHILOSOPHICAL_LEAF_IDS}
        for c_id, targets in self.c_to_p.items():
            c_dev = cult[c_id] - 0.50
            for p_id, weight in targets.items():
                if p_id in delta_phil:
                    delta_phil[p_id] += c_dev * weight * gain

        delta_cult = {k: 0.0 for k in CULTURAL_LEAF_IDS}
        for p_id, targets in self.p_to_c.items():
            p_dev = phil[p_id] - 0.50
            for c_id, weight in targets.items():
                if c_id in delta_cult:
                    delta_cult[c_id] += p_dev * weight * gain

        coupled_phil = {}
        for k in PHILOSOPHICAL_LEAF_IDS:
            new_val = round(min(1.0, max(0.0, phil[k] + delta_phil[k])), 4)
            coupled_phil[k] = new_val

        coupled_cult = {}
        for k in CULTURAL_LEAF_IDS:
            new_val = round(min(1.0, max(0.0, cult[k] + delta_cult[k])), 4)
            coupled_cult[k] = new_val

        governance_balance = round(
            1.0 - abs(coupled_cult["cultural/efficiency/power"] - coupled_phil["philosophical/structure/order"]), 4
        )
        moral_ballast = round(
            (coupled_cult["cultural/justice/honor"] + coupled_cult["cultural/freedom/self-sufficiency"]) / 2.0, 4
        )

        return {
            "initial_cultural": cult,
            "initial_philosophical": phil,
            "delta_cultural": {k: round(v, 4) for k, v in delta_cult.items()},
            "delta_philosophical": {k: round(v, 4) for k, v in delta_phil.items()},
            "coupled_cultural": coupled_cult,
            "coupled_philosophical": coupled_phil,
            "cohesion_metrics": {
                "governance_balance": governance_balance,
                "moral_ballast": moral_ballast,
            },
        }
