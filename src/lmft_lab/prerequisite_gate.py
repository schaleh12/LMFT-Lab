"""Fuzzy Prerequisite Coherence Gate Engine.

Evaluates symbolic conditional dependencies across canonical seed leaves:
1. Cultural Justice requires Freedom (Freedom -> Justice).
2. Psychological Confidence requires Clarity (Clarity -> Confidence).
3. Psychological Will/Intention requires Being/Agency (Agency -> Intention).
4. Philosophical Order requires Persistence (Persistence -> Order).

Flags hollow rhetoric, coerced compliance, and dogmatic distortions without
mutating or expanding the frozen 40-node founding seed (Rule D001).

Zero runtime LLM calls during unassisted evaluation.
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest


CANONICAL_LEAF_IDS = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}

CONDITIONAL_LEAF_TARGETS = [
    "cultural/justice/fairness",
    "cultural/freedom/self-sufficiency",
    "cultural/freedom/needlessness",
    "psychological/contemplation/confidence",
    "psychological/contemplation/clarity",
    "psychological/will/intention",
    "philosophical/being/agency",
    "philosophical/structure/order",
    "philosophical/persistence/continuity",
    "philosophical/persistence/discreteness",
]

for leaf_id in CONDITIONAL_LEAF_TARGETS:
    assert leaf_id in CANONICAL_LEAF_IDS, f"Non-canonical leaf: {leaf_id}"


class PrerequisiteCoherenceGate:
    """Evaluates whether higher-order claims satisfy necessary prerequisite conditions."""

    def evaluate_coherence(self, leaf_dials: Dict[str, float]) -> Dict[str, Any]:
        """Calculates authentic gated scores and detects epistemic distortions."""
        dials = {k: 0.50 for k in CONDITIONAL_LEAF_TARGETS}
        for k, v in leaf_dials.items():
            if k in dials:
                dials[k] = max(0.0, min(1.0, float(v)))

        fairness = dials["cultural/justice/fairness"]
        self_suff = dials["cultural/freedom/self-sufficiency"]
        needless = dials["cultural/freedom/needlessness"]
        freedom_prereq = (self_suff + needless) / 2.0

        confidence = dials["psychological/contemplation/confidence"]
        clarity_prereq = dials["psychological/contemplation/clarity"]

        intention = dials["psychological/will/intention"]
        agency_prereq = dials["philosophical/being/agency"]

        order = dials["philosophical/structure/order"]
        continuity = dials["philosophical/persistence/continuity"]
        discreteness = dials["philosophical/persistence/discreteness"]
        persistence_prereq = (continuity + discreteness) / 2.0

        distortions = []

        # 1. Freedom -> Justice Gate
        # Genuine justice requires freedom; coerced compliance is not authentic justice
        justice_factor = min(1.0, 0.40 + 0.60 * freedom_prereq)
        authentic_justice = round(fairness * justice_factor, 4)
        if fairness > 0.70 and freedom_prereq < 0.30:
            distortions.append("Coerced Compliance Distortion (Justice asserted without Freedom)")

        # 2. Clarity -> Confidence Gate
        # Genuine confidence requires clarity; high confidence without clarity is dogmatism
        confidence_factor = min(1.0, 0.30 + 0.70 * clarity_prereq)
        authentic_confidence = round(confidence * confidence_factor, 4)
        if confidence > 0.75 and clarity_prereq < 0.30:
            distortions.append("Dogmatic Hallucination Distortion (Confidence asserted without Clarity)")

        # 3. Agency -> Intention Gate
        # Sane intention requires agency; intention without agency is unanchored fantasy
        intention_factor = min(1.0, 0.40 + 0.60 * agency_prereq)
        authentic_intention = round(intention * intention_factor, 4)
        if intention > 0.75 and agency_prereq < 0.30:
            distortions.append("Unanchored Volition Distortion (Intention asserted without Agency)")

        # 4. Persistence -> Order Gate
        # Order requires persistence; order without continuity is ephemeral illusion
        order_factor = min(1.0, 0.40 + 0.60 * persistence_prereq)
        authentic_order = round(order * order_factor, 4)
        if order > 0.75 and persistence_prereq < 0.30:
            distortions.append("Ephemeral Symmetry Distortion (Order asserted without Persistence)")

        # Global Coherence Index: ratio of authentic realization to nominal assertion
        nominal_sum = fairness + confidence + intention + order
        authentic_sum = authentic_justice + authentic_confidence + authentic_intention + authentic_order
        if nominal_sum > 0.05:
            global_coherence = round(min(1.0, authentic_sum / nominal_sum), 4)
        else:
            global_coherence = 1.0000

        return {
            "nominal_scores": {
                "justice": fairness,
                "confidence": confidence,
                "intention": intention,
                "order": order,
            },
            "prerequisites": {
                "freedom": round(freedom_prereq, 4),
                "clarity": round(clarity_prereq, 4),
                "agency": round(agency_prereq, 4),
                "persistence": round(persistence_prereq, 4),
            },
            "authentic_scores": {
                "authentic_justice": authentic_justice,
                "authentic_confidence": authentic_confidence,
                "authentic_intention": authentic_intention,
                "authentic_order": authentic_order,
            },
            "global_coherence_index": global_coherence,
            "distortions_detected": distortions,
            "is_authentic": len(distortions) == 0 and global_coherence >= 0.80,
        }


class OrdinaryMemoryPrerequisiteComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def evaluate(self, leaf_dials: Dict[str, float]) -> Dict[str, Any]:
        dials = {k: 0.50 for k in CONDITIONAL_LEAF_TARGETS}
        for k, v in leaf_dials.items():
            if k in dials:
                dials[k] = max(0.0, min(1.0, float(v)))

        fairness = dials["cultural/justice/fairness"]
        self_suff = dials["cultural/freedom/self-sufficiency"]
        needless = dials["cultural/freedom/needlessness"]
        freedom_prereq = (self_suff + needless) / 2.0

        confidence = dials["psychological/contemplation/confidence"]
        clarity_prereq = dials["psychological/contemplation/clarity"]

        intention = dials["psychological/will/intention"]
        agency_prereq = dials["philosophical/being/agency"]

        order = dials["philosophical/structure/order"]
        continuity = dials["philosophical/persistence/continuity"]
        discreteness = dials["philosophical/persistence/discreteness"]
        persistence_prereq = (continuity + discreteness) / 2.0

        distortions = []

        justice_factor = min(1.0, 0.40 + 0.60 * freedom_prereq)
        authentic_justice = round(fairness * justice_factor, 4)
        if fairness > 0.70 and freedom_prereq < 0.30:
            distortions.append("Coerced Compliance Distortion (Justice asserted without Freedom)")

        confidence_factor = min(1.0, 0.30 + 0.70 * clarity_prereq)
        authentic_confidence = round(confidence * confidence_factor, 4)
        if confidence > 0.75 and clarity_prereq < 0.30:
            distortions.append("Dogmatic Hallucination Distortion (Confidence asserted without Clarity)")

        intention_factor = min(1.0, 0.40 + 0.60 * agency_prereq)
        authentic_intention = round(intention * intention_factor, 4)
        if intention > 0.75 and agency_prereq < 0.30:
            distortions.append("Unanchored Volition Distortion (Intention asserted without Agency)")

        order_factor = min(1.0, 0.40 + 0.60 * persistence_prereq)
        authentic_order = round(order * order_factor, 4)
        if order > 0.75 and persistence_prereq < 0.30:
            distortions.append("Ephemeral Symmetry Distortion (Order asserted without Persistence)")

        nominal_sum = fairness + confidence + intention + order
        authentic_sum = authentic_justice + authentic_confidence + authentic_intention + authentic_order
        if nominal_sum > 0.05:
            global_coherence = round(min(1.0, authentic_sum / nominal_sum), 4)
        else:
            global_coherence = 1.0000

        return {
            "nominal_scores": {
                "justice": fairness,
                "confidence": confidence,
                "intention": intention,
                "order": order,
            },
            "prerequisites": {
                "freedom": round(freedom_prereq, 4),
                "clarity": round(clarity_prereq, 4),
                "agency": round(agency_prereq, 4),
                "persistence": round(persistence_prereq, 4),
            },
            "authentic_scores": {
                "authentic_justice": authentic_justice,
                "authentic_confidence": authentic_confidence,
                "authentic_intention": authentic_intention,
                "authentic_order": authentic_order,
            },
            "global_coherence_index": global_coherence,
            "distortions_detected": distortions,
            "is_authentic": len(distortions) == 0 and global_coherence >= 0.80,
        }
