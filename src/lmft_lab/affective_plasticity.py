"""Affective Plasticity Regulation Engine.

Dynamically modulates capacity learning rate (reinforcement plasticity alpha) and habituation
decay (lambda) as a function of the live Experiential (Novelty, Arousal, Valence, Entrainment)
and Psychological (Contemplation Clarity, Confidence) leaf states without mutating or
expanding the frozen 40-node founding seed (Rule D001).

Zero runtime LLM calls during unassisted evaluation.
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.birth import _inventory
from lmft_lab.capacity_decay import reinforce_weight, decay_weight, damp_weight
from lmft_lab.runtime_store import digest


CANONICAL_LEAF_IDS = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}

EXPERIENTIAL_AFFECTIVE_LEAVES = [
    "experiential/reflection/novelty",
    "experiential/reflection/salience",
    "experiential/phase/valence",
    "experiential/phase/arousal",
    "experiential/synchronization/resonance",
    "experiential/synchronization/entrainment",
]

PSYCHOLOGICAL_EPISTEMIC_LEAVES = [
    "psychological/contemplation/clarity",
    "psychological/contemplation/confidence",
]

for leaf_id in EXPERIENTIAL_AFFECTIVE_LEAVES + PSYCHOLOGICAL_EPISTEMIC_LEAVES:
    assert leaf_id in CANONICAL_LEAF_IDS, f"Non-canonical leaf: {leaf_id}"


DEFAULT_BASE_ALPHA = 0.20
DEFAULT_BASE_LAMBDA = 0.05
DEFAULT_BASE_DELTA = 0.35


class AffectivePlasticityEngine:
    """Modulates learning rates dynamically based on affective arousal and epistemic certainty."""

    def __init__(
        self,
        base_alpha: float = DEFAULT_BASE_ALPHA,
        base_lambda: float = DEFAULT_BASE_LAMBDA,
        base_delta: float = DEFAULT_BASE_DELTA,
    ):
        self.base_alpha = float(base_alpha)
        self.base_lambda = float(base_lambda)
        self.base_delta = float(base_delta)

    def compute_dynamic_rates(
        self,
        experiential_dials: Optional[Dict[str, float]] = None,
        psychological_dials: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """Calculates affective plasticity alpha, decay lambda, and damping delta."""
        exp = {
            "experiential/reflection/novelty": 0.50,
            "experiential/phase/arousal": 0.50,
            "experiential/phase/valence": 0.50,
            "experiential/synchronization/entrainment": 0.50,
        }
        if experiential_dials:
            for k, v in experiential_dials.items():
                norm_k = "experiential/synchronization/entrainment" if k == "experiential/synchronization/retention" else k
                if norm_k in exp:
                    exp[norm_k] = max(0.0, min(1.0, float(v)))

        psy = {
            "psychological/contemplation/clarity": 0.50,
            "psychological/contemplation/confidence": 0.50,
        }
        if psychological_dials:
            for k, v in psychological_dials.items():
                if k in psy:
                    psy[k] = max(0.0, min(1.0, float(v)))

        novelty = exp["experiential/reflection/novelty"]
        arousal = exp["experiential/phase/arousal"]
        valence = exp["experiential/phase/valence"]
        entrainment = exp["experiential/synchronization/entrainment"]

        clarity = psy["psychological/contemplation/clarity"]
        confidence = psy["psychological/contemplation/confidence"]

        # Surprise factor: novelty + arousal drives need to learn
        surprise_factor = 0.60 * novelty + 0.40 * arousal

        # Mastery factor: clarity + confidence protects established knowledge
        mastery_factor = 0.50 * clarity + 0.50 * confidence

        # Dynamic Reinforcement Plasticity: alpha
        # Base alpha boosted by surprise, throttled by mastery
        raw_alpha = self.base_alpha * (1.0 + surprise_factor - 0.70 * mastery_factor)
        dynamic_alpha = round(min(0.45, max(0.05, raw_alpha)), 4)

        # Dynamic Habituation Decay: lambda
        # High entrainment and positive valence slow down forgetting
        raw_lambda = self.base_lambda * (1.0 - 0.50 * entrainment + 0.30 * (1.0 - valence))
        dynamic_lambda = round(min(0.15, max(0.01, raw_lambda)), 4)

        # Dynamic Contradiction Damping: delta
        # High arousal and low confidence intensify damping
        raw_delta = self.base_delta * (1.0 + 0.30 * arousal - 0.20 * confidence)
        dynamic_delta = round(min(0.60, max(0.20, raw_delta)), 4)

        return {
            "surprise_factor": round(surprise_factor, 4),
            "mastery_factor": round(mastery_factor, 4),
            "dynamic_alpha": dynamic_alpha,
            "dynamic_lambda": dynamic_lambda,
            "dynamic_delta": dynamic_delta,
            "plasticity_regime": (
                "Hyper-Adaptive (Surprise / Disruption)" if dynamic_alpha > 0.28
                else "Protected Mastery (Habituation / Stability)" if dynamic_alpha < 0.15
                else "Equilibrated Plasticity"
            ),
        }

    def update_rule_weight(
        self,
        current_weight: float,
        event_type: str,
        experiential_dials: Optional[Dict[str, float]] = None,
        psychological_dials: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """Applies single-event weight transition with live affective rates."""
        rates = self.compute_dynamic_rates(experiential_dials, psychological_dials)

        w = float(current_weight)
        if event_type == "reinforce":
            new_w = reinforce_weight(w, alpha=rates["dynamic_alpha"])
        elif event_type == "decay":
            new_w = decay_weight(w, lam=rates["dynamic_lambda"])
        elif event_type == "damp":
            new_w = damp_weight(w, beta=rates["dynamic_delta"])
        else:
            raise ValueError(f"Unknown event type: {event_type}")

        return {
            "initial_weight": round(w, 4),
            "event_type": event_type,
            "new_weight": new_w,
            "rates": rates,
        }


class OrdinaryMemoryAffectivePlasticityComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def __init__(
        self,
        base_alpha: float = DEFAULT_BASE_ALPHA,
        base_lambda: float = DEFAULT_BASE_LAMBDA,
        base_delta: float = DEFAULT_BASE_DELTA,
    ):
        self.base_alpha = float(base_alpha)
        self.base_lambda = float(base_lambda)
        self.base_delta = float(base_delta)

    def compute_dynamic_rates(
        self,
        experiential_dials: Optional[Dict[str, float]] = None,
        psychological_dials: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        exp = {
            "experiential/reflection/novelty": 0.50,
            "experiential/phase/arousal": 0.50,
            "experiential/phase/valence": 0.50,
            "experiential/synchronization/entrainment": 0.50,
        }
        if experiential_dials:
            for k, v in experiential_dials.items():
                norm_k = "experiential/synchronization/entrainment" if k == "experiential/synchronization/retention" else k
                if norm_k in exp:
                    exp[norm_k] = max(0.0, min(1.0, float(v)))

        psy = {
            "psychological/contemplation/clarity": 0.50,
            "psychological/contemplation/confidence": 0.50,
        }
        if psychological_dials:
            for k, v in psychological_dials.items():
                if k in psy:
                    psy[k] = max(0.0, min(1.0, float(v)))

        novelty = exp["experiential/reflection/novelty"]
        arousal = exp["experiential/phase/arousal"]
        valence = exp["experiential/phase/valence"]
        entrainment = exp["experiential/synchronization/entrainment"]

        clarity = psy["psychological/contemplation/clarity"]
        confidence = psy["psychological/contemplation/confidence"]

        surprise_factor = 0.60 * novelty + 0.40 * arousal
        mastery_factor = 0.50 * clarity + 0.50 * confidence

        raw_alpha = self.base_alpha * (1.0 + surprise_factor - 0.70 * mastery_factor)
        dynamic_alpha = round(min(0.45, max(0.05, raw_alpha)), 4)

        raw_lambda = self.base_lambda * (1.0 - 0.50 * entrainment + 0.30 * (1.0 - valence))
        dynamic_lambda = round(min(0.15, max(0.01, raw_lambda)), 4)

        raw_delta = self.base_delta * (1.0 + 0.30 * arousal - 0.20 * confidence)
        dynamic_delta = round(min(0.60, max(0.20, raw_delta)), 4)

        return {
            "surprise_factor": round(surprise_factor, 4),
            "mastery_factor": round(mastery_factor, 4),
            "dynamic_alpha": dynamic_alpha,
            "dynamic_lambda": dynamic_lambda,
            "dynamic_delta": dynamic_delta,
            "plasticity_regime": (
                "Hyper-Adaptive (Surprise / Disruption)" if dynamic_alpha > 0.28
                else "Protected Mastery (Habituation / Stability)" if dynamic_alpha < 0.15
                else "Equilibrated Plasticity"
            ),
        }

    def update_rule_weight(
        self,
        current_weight: float,
        event_type: str,
        experiential_dials: Optional[Dict[str, float]] = None,
        psychological_dials: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        rates = self.compute_dynamic_rates(experiential_dials, psychological_dials)

        w = float(current_weight)
        if event_type == "reinforce":
            new_w = reinforce_weight(w, alpha=rates["dynamic_alpha"])
        elif event_type == "decay":
            new_w = decay_weight(w, lam=rates["dynamic_lambda"])
        elif event_type == "damp":
            new_w = damp_weight(w, beta=rates["dynamic_delta"])
        else:
            raise ValueError(f"Unknown event type: {event_type}")

        return {
            "initial_weight": round(w, 4),
            "event_type": event_type,
            "new_weight": new_w,
            "rates": rates,
        }
