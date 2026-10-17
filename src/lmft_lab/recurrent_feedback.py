"""Recurrent Post-Action Echo & Homeostatic Feedback Loop Engine.

Closes the cybernetic loop by feeding emitted speaking registers and executive postures
back into sensory and affective roots (Experiential leaves) without mutating or expanding
the frozen 40-node founding seed (Rule D001).

Zero runtime LLM calls during unassisted evaluation.
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest


CANONICAL_LEAF_IDS = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}

EXPERIENTIAL_LEAF_IDS = [
    "experiential/reflection/novelty",
    "experiential/reflection/salience",
    "experiential/phase/valence",
    "experiential/phase/arousal",
    "experiential/synchronization/resonance",
    "experiential/synchronization/entrainment",
]

for leaf_id in EXPERIENTIAL_LEAF_IDS:
    assert leaf_id in CANONICAL_LEAF_IDS, f"Non-canonical leaf: {leaf_id}"


class RecurrentFeedbackEngine:
    """Computes the post-action echo that loops executive postures back into affective leaves."""

    def compute_echo(
        self,
        experiential_dials: Optional[Dict[str, float]] = None,
        psychological_state: Optional[Dict[str, Any]] = None,
        action_posture: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Calculates post-action deltas and updates experiential leaf states."""
        exp = {k: 0.50 for k in EXPERIENTIAL_LEAF_IDS}
        if experiential_dials:
            for k, v in experiential_dials.items():
                norm_k = "experiential/synchronization/entrainment" if k == "experiential/synchronization/retention" else k
                if norm_k in exp:
                    exp[norm_k] = max(0.0, min(1.0, float(v)))

        posture = action_posture or "Equilibrated Synthesis"
        psy = psychological_state or {}

        intention = float(psy.get("psychological/will/intention", 0.50))
        execution = float(psy.get("psychological/will/execution", 0.50))
        clarity = float(psy.get("psychological/contemplation/clarity", 0.50))
        confidence = float(psy.get("psychological/contemplation/confidence", 0.50))

        delta = {k: 0.0 for k in EXPERIENTIAL_LEAF_IDS}

        # 1. Action Outcome Regimes
        if "Abstention" in posture or "Silence" in posture:
            # Epistemic Modesty / Honest Silence:
            # Calms arousal, maintains neutral valence, preserves salience for future investigation
            delta["experiential/phase/arousal"] = -0.10
            delta["experiential/reflection/salience"] = +0.10
            delta["experiential/synchronization/resonance"] = +0.05
            echo_type = "Honest Silence Echo (Epistemic Calibrated Relief)"

        elif "Conflict" in posture or "Dissonance" in posture or clarity < 0.30:
            # Epistemic Conflict / Ambiguity:
            # Heightens alertness/arousal, lowers valence (dissonance), spikes salience for clarification
            delta["experiential/phase/arousal"] = +0.15
            delta["experiential/phase/valence"] = -0.12
            delta["experiential/reflection/salience"] = +0.25
            delta["experiential/reflection/novelty"] = +0.10
            echo_type = "Cognitive Conflict Echo (Alerted Clarification Demand)"

        elif intention > 0.65 and execution > 0.60:
            # Decisive Sovereign Enactment:
            # Resolves tension (damps arousal), elevates valence (satisfaction), reinforces entrainment & resonance
            delta["experiential/phase/arousal"] = -0.15
            delta["experiential/phase/valence"] = +0.12
            delta["experiential/synchronization/resonance"] = +0.15
            delta["experiential/synchronization/entrainment"] = +0.10
            delta["experiential/reflection/salience"] = -0.05
            echo_type = "Harmonic Enactment Echo (Decisive Volitional Satisfaction)"

        else:
            # Methodical / Pragmatic Equilibrated Synthesis:
            # Mild arousal dampening, steady entrainment, balanced valence
            delta["experiential/phase/arousal"] = -0.05
            delta["experiential/phase/valence"] = +0.05
            delta["experiential/synchronization/resonance"] = +0.08
            delta["experiential/synchronization/entrainment"] = +0.05
            echo_type = "Equilibrated Synthesis Echo (Methodical Baseline Steadying)"

        # Apply deltas with strict [0.0, 1.0] bound enforcement
        echoed_exp = {}
        for k in EXPERIENTIAL_LEAF_IDS:
            new_val = round(min(1.0, max(0.0, exp[k] + delta[k])), 4)
            echoed_exp[k] = new_val

        return {
            "initial_experiential": exp,
            "posture": posture,
            "echo_type": echo_type,
            "echo_deltas": {k: round(v, 4) for k, v in delta.items()},
            "echoed_experiential": echoed_exp,
            "arousal_damped": delta["experiential/phase/arousal"] < 0,
            "valence_reinforced": delta["experiential/phase/valence"] > 0,
        }


class OrdinaryMemoryRecurrentComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def compute_echo(
        self,
        experiential_dials: Optional[Dict[str, float]] = None,
        psychological_state: Optional[Dict[str, Any]] = None,
        action_posture: Optional[str] = None,
    ) -> Dict[str, Any]:
        exp = {k: 0.50 for k in EXPERIENTIAL_LEAF_IDS}
        if experiential_dials:
            for k, v in experiential_dials.items():
                norm_k = "experiential/synchronization/entrainment" if k == "experiential/synchronization/retention" else k
                if norm_k in exp:
                    exp[norm_k] = max(0.0, min(1.0, float(v)))

        posture = action_posture or "Equilibrated Synthesis"
        psy = psychological_state or {}

        intention = float(psy.get("psychological/will/intention", 0.50))
        execution = float(psy.get("psychological/will/execution", 0.50))
        clarity = float(psy.get("psychological/contemplation/clarity", 0.50))

        delta = {k: 0.0 for k in EXPERIENTIAL_LEAF_IDS}

        if "Abstention" in posture or "Silence" in posture:
            delta["experiential/phase/arousal"] = -0.10
            delta["experiential/reflection/salience"] = +0.10
            delta["experiential/synchronization/resonance"] = +0.05
            echo_type = "Honest Silence Echo (Epistemic Calibrated Relief)"
        elif "Conflict" in posture or "Dissonance" in posture or clarity < 0.30:
            delta["experiential/phase/arousal"] = +0.15
            delta["experiential/phase/valence"] = -0.12
            delta["experiential/reflection/salience"] = +0.25
            delta["experiential/reflection/novelty"] = +0.10
            echo_type = "Cognitive Conflict Echo (Alerted Clarification Demand)"
        elif intention > 0.65 and execution > 0.60:
            delta["experiential/phase/arousal"] = -0.15
            delta["experiential/phase/valence"] = +0.12
            delta["experiential/synchronization/resonance"] = +0.15
            delta["experiential/synchronization/entrainment"] = +0.10
            delta["experiential/reflection/salience"] = -0.05
            echo_type = "Harmonic Enactment Echo (Decisive Volitional Satisfaction)"
        else:
            delta["experiential/phase/arousal"] = -0.05
            delta["experiential/phase/valence"] = +0.05
            delta["experiential/synchronization/resonance"] = +0.08
            delta["experiential/synchronization/entrainment"] = +0.05
            echo_type = "Equilibrated Synthesis Echo (Methodical Baseline Steadying)"

        echoed_exp = {}
        for k in EXPERIENTIAL_LEAF_IDS:
            new_val = round(min(1.0, max(0.0, exp[k] + delta[k])), 4)
            echoed_exp[k] = new_val

        return {
            "initial_experiential": exp,
            "posture": posture,
            "echo_type": echo_type,
            "echo_deltas": {k: round(v, 4) for k, v in delta.items()},
            "echoed_experiential": echoed_exp,
            "arousal_damped": delta["experiential/phase/arousal"] < 0,
            "valence_reinforced": delta["experiential/phase/valence"] > 0,
        }
