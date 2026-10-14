"""Affective Homeostasis Governor (Mood Stabilizer Engine).

Protects the LMFT from catastrophic affective destabilization, emotional runaway loops,
and violent volatility spikes (|Δ| > threshold or extreme boundary saturation).

Rooted in the frozen canonical seed architecture (Rule D001):
- Uses Philosophical/Structure/Order, Philosophical/Persistence/Continuity,
  and Psychological/Contemplation/Clarity as stabilizing anchors.
- Regulates Experiential/Phase/Arousal and Valence towards sustainable dynamic equilibrium.
- Enforces Rule D001 (frozen 40-node founding seed) and Rule D004 (matched baselines).
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.dispositional_momentum import CANONICAL_LEAF_IDS


# Stabilizing anchor leaves from canonical founding seed
ANCHOR_CLARITY = "psychological/contemplation/clarity"
ANCHOR_ORDER = "philosophical/structure/order"
ANCHOR_CONTINUITY = "philosophical/persistence/continuity"
LEAF_AROUSAL = "experiential/phase/arousal"
LEAF_VALENCE = "experiential/phase/valence"


class AffectiveHomeostasisGovernor:
    """Autonomic homeostatic governor that dampens severe dispositional volatility."""

    def __init__(
        self,
        volatility_threshold: float = 0.35,
        extreme_lower: float = 0.05,
        extreme_upper: float = 0.95,
        base_dampening: float = 0.40,
        equilibrium_setpoint: float = 0.50,
    ):
        self.volatility_threshold = volatility_threshold
        self.extreme_lower = extreme_lower
        self.extreme_upper = extreme_upper
        self.base_dampening = base_dampening
        self.equilibrium_setpoint = equilibrium_setpoint

    def compute_anchor_support(self, dials: Dict[str, float]) -> float:
        """Calculates grounding anchor strength from Clarity, Order, and Continuity."""
        c = dials.get(ANCHOR_CLARITY, self.equilibrium_setpoint)
        o = dials.get(ANCHOR_ORDER, self.equilibrium_setpoint)
        p = dials.get(ANCHOR_CONTINUITY, self.equilibrium_setpoint)
        return round((c + o + p) / 3.0, 4)

    def stabilize(
        self,
        candidate_dials: Dict[str, float],
        previous_dials: Dict[str, float],
    ) -> Dict[str, Any]:
        """Stabilizes candidate disposition vector against extreme swings and saturation."""
        stabilized = deepcopy(candidate_dials)
        anchor_support = self.compute_anchor_support(candidate_dials)
        effective_dampening = min(0.85, self.base_dampening * (1.0 + anchor_support))

        arousal = candidate_dials.get(LEAF_AROUSAL, self.equilibrium_setpoint)
        arousal_tension = round(abs(arousal - self.equilibrium_setpoint) * 2.0, 4)

        interventions: List[Dict[str, Any]] = []
        deltas: Dict[str, float] = {}

        for leaf_id in CANONICAL_LEAF_IDS:
            curr_val = candidate_dials.get(leaf_id, self.equilibrium_setpoint)
            prev_val = previous_dials.get(leaf_id, curr_val)
            delta = curr_val - prev_val
            deltas[leaf_id] = round(delta, 4)
            abs_delta = abs(delta)

            needs_stabilization = False
            reasons = []

            # 1. Check volatility jump
            if abs_delta > self.volatility_threshold:
                needs_stabilization = True
                reasons.append(f"volatility_jump (|delta|={abs_delta:.3f} > {self.volatility_threshold})")

            # 2. Check boundary saturation
            if curr_val < self.extreme_lower:
                needs_stabilization = True
                reasons.append(f"lower_boundary_saturation (val={curr_val:.3f} < {self.extreme_lower})")
            elif curr_val > self.extreme_upper:
                needs_stabilization = True
                reasons.append(f"upper_boundary_saturation (val={curr_val:.3f} > {self.extreme_upper})")

            if needs_stabilization:
                new_val = curr_val

                # Clamp volatility jump
                if abs_delta > self.volatility_threshold:
                    excess = abs_delta - self.volatility_threshold
                    damped_excess = excess * (1.0 - effective_dampening)
                    clamped_delta = (1.0 if delta > 0 else -1.0) * (self.volatility_threshold + damped_excess)
                    new_val = prev_val + clamped_delta

                # Soft-boundary reflection away from absolute saturation
                if new_val < self.extreme_lower:
                    deficit = self.extreme_lower - new_val
                    new_val = self.extreme_lower + (deficit * (1.0 - effective_dampening) * 0.5) + 0.02
                elif new_val > self.extreme_upper:
                    overshoot = new_val - self.extreme_upper
                    new_val = self.extreme_upper - (overshoot * (1.0 - effective_dampening) * 0.5) - 0.02

                new_val = round(max(0.0, min(1.0, new_val)), 4)
                stabilized[leaf_id] = new_val

                interventions.append({
                    "leaf_id": leaf_id,
                    "original_value": round(curr_val, 4),
                    "stabilized_value": new_val,
                    "delta_before": round(delta, 4),
                    "delta_after": round(new_val - prev_val, 4),
                    "reasons": reasons,
                })

        # Calculate summary metrics
        volatility_index = round(sum(abs(d) for d in deltas.values()) / max(1, len(deltas)), 4)
        max_leaf = max(deltas.items(), key=lambda item: abs(item[1])) if deltas else ("none", 0.0)

        # Emotional balance score: 1.0 = perfectly calm and centered
        balance_penalty = max(volatility_index * 1.5, arousal_tension * 0.4)
        emotional_balance_score = round(max(0.05, min(1.0, 1.0 - balance_penalty)), 4)

        if not interventions:
            regime = "Calm Equilibrium" if volatility_index < 0.10 else "Adaptive Dynamic Response"
        elif any("volatility_jump" in r for inv in interventions for r in inv["reasons"]):
            regime = "Active Volatility Clamping"
        else:
            regime = "Boundary Saturation Buffering"

        return {
            "stabilized_dials": stabilized,
            "interventions": interventions,
            "interventions_count": len(interventions),
            "volatility_index": volatility_index,
            "max_delta_leaf": {"leaf_id": max_leaf[0], "delta": max_leaf[1]},
            "anchor_support": anchor_support,
            "arousal_tension": arousal_tension,
            "emotional_balance_score": emotional_balance_score,
            "homeostatic_regime": regime,
        }
