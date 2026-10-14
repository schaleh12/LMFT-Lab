"""Epistemic Curiosity & Value Consonance Engine.

Resolves two fundamental boundary challenges in the LMFT cognitive architecture:
1. The Socratic Paradox: Distinguishes between hostile contradiction (adversarial distortion
   triggering epistemic defense) and benevolent novelty (unanchored mysteries triggering
   curious inquiry and wonder rather than panic).
2. Cross-Domain Value Consonance: Arbitrates internal tensions when virtues pull in
   opposite directions across domains (e.g. Truth vs. Comfort, Power vs. Freedom, Order vs. Fairness),
   preventing cognitive thrashing and synthesizing harmonic equilibria.

Preserves Rule D001 (frozen 40-node founding seed) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.dispositional_momentum import CANONICAL_LEAF_IDS


# Canonical Leaf handles
LEAF_TRUTH_FACT = "psychological/truth/fact"
LEAF_TRUTH_THEORY = "psychological/truth/theory"
LEAF_WILL_INTENTION = "psychological/will/intention"
LEAF_WILL_EXECUTION = "psychological/will/execution"
LEAF_CLARITY = "psychological/contemplation/clarity"
LEAF_CONFIDENCE = "psychological/contemplation/confidence"

LEAF_NOVELTY = "experiential/reflection/novelty"
LEAF_SALIENCE = "experiential/reflection/salience"
LEAF_VALENCE = "experiential/phase/valence"
LEAF_AROUSAL = "experiential/phase/arousal"
LEAF_RESONANCE = "experiential/synchronization/resonance"

LEAF_JUSTICE_FAIRNESS = "cultural/justice/fairness"
LEAF_JUSTICE_HONOR = "cultural/justice/honor"
LEAF_FREEDOM_SELF = "cultural/freedom/self-sufficiency"
LEAF_EFFICIENCY_POWER = "cultural/efficiency/power"
LEAF_EFFICIENCY_WASTELESS = "cultural/efficiency/wastelessness"

LEAF_ORDER = "philosophical/structure/order"
LEAF_CHAOS = "philosophical/structure/chaos"
LEAF_CONTINUITY = "philosophical/persistence/continuity"


# Key cross-domain value dyads in tension
VALUE_TENSION_DYADS = [
    {
        "name": "Truth vs. Comfort",
        "primary_leaf": LEAF_TRUTH_FACT,
        "opposing_leaf": LEAF_VALENCE,
        "description": "Hard objective reality causing emotional distress or vulnerability",
    },
    {
        "name": "Power vs. Freedom",
        "primary_leaf": LEAF_EFFICIENCY_POWER,
        "opposing_leaf": LEAF_FREEDOM_SELF,
        "description": "Organizational potency/efficiency threatening individual self-sufficiency",
    },
    {
        "name": "Order vs. Fairness",
        "primary_leaf": LEAF_ORDER,
        "opposing_leaf": LEAF_JUSTICE_FAIRNESS,
        "description": "Rigid systemic structure versus compassionate, equitable flexibility",
    },
    {
        "name": "Honor vs. Chaos",
        "primary_leaf": LEAF_JUSTICE_HONOR,
        "opposing_leaf": LEAF_CHAOS,
        "description": "Moral integrity maintaining dignity amid surrounding disorder",
    },
]


class ValueConsonanceEngine:
    """Evaluates epistemic curiosity stance and arbitrates cross-domain value consonance."""

    def __init__(
        self,
        curiosity_threshold: float = 0.55,
        consonance_tolerance: float = 0.30,
    ):
        self.curiosity_threshold = curiosity_threshold
        self.consonance_tolerance = consonance_tolerance

    def classify_epistemic_mode(
        self,
        candidate_dials: Dict[str, float],
        is_conflict: bool = False,
        distortions_count: int = 0,
    ) -> Dict[str, Any]:
        """Classifies input into Curious Inquiry, Epistemic Defense, or Standard Reflection."""
        novelty = candidate_dials.get(LEAF_NOVELTY, 0.50)
        clarity = candidate_dials.get(LEAF_CLARITY, 0.50)
        arousal = candidate_dials.get(LEAF_AROUSAL, 0.50)

        # 1. Epistemic Defense (Hostile / Distorted)
        if is_conflict or distortions_count > 0:
            return {
                "mode": "Epistemic Defense",
                "rationale": "Direct contradiction or prerequisite distortion detected; activate integrity guard.",
                "inquiry_posture": "Halt and issue clarification request",
                "recommended_register": "Methodical & Pragmatic",
                "is_curious": False,
            }

        # 2. Curious Inquiry (Socratic Wonder)
        # Novelty is high, but there are no prerequisite distortions: benevolent mystery
        if novelty >= self.curiosity_threshold or (clarity < 0.60 and distortions_count == 0):
            return {
                "mode": "Curious Inquiry",
                "rationale": "High novelty without ethical/ontological distortion; activate Socratic wonder.",
                "inquiry_posture": "Explore and formulate inquisitive inquiry",
                "recommended_register": "Inquisitive & Contemplative",
                "is_curious": True,
            }

        # 3. Standard Cognitive Processing
        return {
            "mode": "Harmonic Processing",
            "rationale": "Familiar or calibrated concepts within steady baseline parameters.",
            "inquiry_posture": "Proceed with calibrated execution",
            "recommended_register": "Authoritative & Chivalrous" if clarity >= 0.70 else "Methodical & Pragmatic",
            "is_curious": False,
        }

    def arbitrate_consonance(
        self,
        candidate_dials: Dict[str, float],
        epistemic_mode: str,
    ) -> Dict[str, Any]:
        """Detects and harmonizes cross-domain value tensions into a coherent synthesis."""
        harmonized = deepcopy(candidate_dials)
        tensions_detected = []
        consonance_penalties = []

        # 1. Socratic Wonder Tuning for Curious Inquiry Mode
        if epistemic_mode == "Curious Inquiry":
            # Reframe low clarity as productive wonder rather than panic:
            # Gently modulate arousal into calm, alert engagement (~0.52)
            curr_arousal = harmonized.get(LEAF_AROUSAL, 0.50)
            if curr_arousal > 0.60:
                harmonized[LEAF_AROUSAL] = 0.52

            # Boost intentional curiosity
            curr_intention = harmonized.get(LEAF_WILL_INTENTION, 0.50)
            harmonized[LEAF_WILL_INTENTION] = round(max(curr_intention, 0.68), 4)

            # Receptive openness
            harmonized[LEAF_RESONANCE] = round(max(harmonized.get(LEAF_RESONANCE, 0.50), 0.65), 4)

        # 2. Check and Resolve Value Dyads
        for dyad in VALUE_TENSION_DYADS:
            val_p = candidate_dials.get(dyad["primary_leaf"], 0.50)
            val_o = candidate_dials.get(dyad["opposing_leaf"], 0.50)

            # Tension occurs when both leaves push strongly into opposing stances,
            # or when one vital leaf is crushed by the other
            divergence = abs(val_p - val_o)

            # Specific Moral/Philosophical Arbitration Cases:
            if dyad["name"] == "Truth vs. Comfort":
                # If Truth is high (fact verified) but Valence has collapsed,
                # anchor Valence through Stoic fortitude / Clarity
                if val_p > 0.70 and val_o < 0.35:
                    clarity = candidate_dials.get(LEAF_CLARITY, 0.50)
                    fortitude_buffer = round(clarity * 0.20, 4)
                    harmonized_val = round(min(0.55, val_o + fortitude_buffer), 4)
                    harmonized[dyad["opposing_leaf"]] = harmonized_val
                    tensions_detected.append({
                        "dyad": dyad["name"],
                        "resolution": "Anchored emotional fortitude in contemplative clarity",
                        "adjusted_leaf": dyad["opposing_leaf"],
                        "prior_val": val_o,
                        "harmonized_val": harmonized_val,
                    })
                    consonance_penalties.append(0.10)

            elif dyad["name"] == "Power vs. Freedom":
                # Power must never overwhelm Freedom (prerequisite: freedom is condition for virtue)
                if val_p > 0.75 and val_o < 0.40:
                    damped_power = round(val_p - 0.15, 4)
                    elevated_freedom = round(val_o + 0.15, 4)
                    harmonized[dyad["primary_leaf"]] = damped_power
                    harmonized[dyad["opposing_leaf"]] = elevated_freedom
                    tensions_detected.append({
                        "dyad": dyad["name"],
                        "resolution": "Subordinated raw efficiency to preserve essential self-sufficiency",
                        "adjusted_leaf": "both",
                        "prior_power": val_p,
                        "harmonized_power": damped_power,
                        "prior_freedom": val_o,
                        "harmonized_freedom": elevated_freedom,
                    })
                    consonance_penalties.append(0.15)

            elif dyad["name"] == "Order vs. Fairness":
                # Rigid order must not crush compassionate fairness
                if val_p > 0.80 and val_o < 0.40:
                    harmonized_fairness = round(min(0.70, val_o + 0.18), 4)
                    harmonized[dyad["opposing_leaf"]] = harmonized_fairness
                    tensions_detected.append({
                        "dyad": dyad["name"],
                        "resolution": "Tempered strict systemic order with equitable fairness",
                        "adjusted_leaf": dyad["opposing_leaf"],
                        "prior_val": val_o,
                        "harmonized_val": harmonized_fairness,
                    })
                    consonance_penalties.append(0.08)

        # 3. Overall Value Consonance Index
        total_penalty = sum(consonance_penalties)
        consonance_index = round(max(0.20, min(1.0, 1.0 - total_penalty)), 4)

        if not tensions_detected:
            consonance_regime = "Harmonic Integrity"
        elif consonance_index >= 0.80:
            consonance_regime = "Balanced Moral Synthesis"
        else:
            consonance_regime = "Active Value Accommodation"

        return {
            "harmonized_dials": harmonized,
            "consonance_index": consonance_index,
            "consonance_regime": consonance_regime,
            "tensions_detected": tensions_detected,
            "tensions_count": len(tensions_detected),
        }

    def evaluate(
        self,
        candidate_dials: Dict[str, float],
        is_conflict: bool = False,
        distortions_count: int = 0,
    ) -> Dict[str, Any]:
        """Executes complete Epistemic Curiosity and Value Consonance evaluation."""
        mode_info = self.classify_epistemic_mode(
            candidate_dials=candidate_dials,
            is_conflict=is_conflict,
            distortions_count=distortions_count,
        )

        consonance_info = self.arbitrate_consonance(
            candidate_dials=candidate_dials,
            epistemic_mode=mode_info["mode"],
        )

        return {
            "epistemic_mode": mode_info["mode"],
            "rationale": mode_info["rationale"],
            "inquiry_posture": mode_info["inquiry_posture"],
            "recommended_register": mode_info["recommended_register"],
            "is_curious": mode_info["is_curious"],
            "consonance_index": consonance_info["consonance_index"],
            "consonance_regime": consonance_info["consonance_regime"],
            "tensions_detected": consonance_info["tensions_detected"],
            "tensions_count": consonance_info["tensions_count"],
            "harmonized_dials": consonance_info["harmonized_dials"],
        }
