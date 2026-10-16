"""Dual-Coded Episodic Saliency Journal Engine.

Maintains a bounded autobiographical memory buffer of memorable episodes dual-coded in both
24-leaf mathematical activations and natural English narrative reflections.

Gated by Experiential Salience (salience >= 0.65 or surprise/conflict) to prevent memory bloat,
without mutating or expanding the frozen 40-node founding seed (Rule D001).

Zero runtime LLM calls during unassisted evaluation.
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
from collections import deque
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest


CANONICAL_LEAF_IDS = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}

SALIENCY_ADMISSION_THRESHOLD = 0.65
NOVELTY_SURPRISE_THRESHOLD = 0.70
DEFAULT_JOURNAL_CAPACITY = 50


class EpisodicSaliencyJournal:
    """Maintains a bounded autobiographical ring buffer of dual-coded experiences."""

    def __init__(self, capacity: int = DEFAULT_JOURNAL_CAPACITY):
        self.capacity = max(1, int(capacity))
        self.entries: deque = deque(maxlen=self.capacity)
        self.total_episodes_recorded = 0

    def record_episode(
        self,
        cycle: int,
        sentence: str,
        target_lemmas: List[str],
        resolved_senses: Dict[str, str],
        leaf_dials: Dict[str, float],
        speaking_register: str,
        action_bid: str,
        post_action_echo: Optional[Dict[str, Any]] = None,
        is_conflict: bool = False,
        custom_id: Optional[str] = None,
        core_pattern: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Evaluates saliency admission and pens dual-coded journal entry if criteria met."""
        salience = float(leaf_dials.get("experiential/reflection/salience", 0.50))
        novelty = float(leaf_dials.get("experiential/reflection/novelty", 0.50))
        arousal = float(leaf_dials.get("experiential/phase/arousal", 0.50))
        clarity = float(leaf_dials.get("psychological/contemplation/clarity", 0.50))

        # Saliency Admission Gate: only memorable or disrupted events are journaled
        qualifies = (
            salience >= SALIENCY_ADMISSION_THRESHOLD
            or novelty >= NOVELTY_SURPRISE_THRESHOLD
            or is_conflict
        )

        if not qualifies:
            return {
                "admitted": False,
                "reason": f"Sub-threshold salience ({salience:.2f} < {SALIENCY_ADMISSION_THRESHOLD}) and no disruption",
                "episode": None,
            }

        self.total_episodes_recorded += 1
        ep_id = custom_id or f"ep-{cycle:04d}-{self.total_episodes_recorded:03d}"

        # Synthesize English Narrative Reflection
        lemma_str = ", ".join(target_lemmas)
        if is_conflict or clarity < 0.35:
            narrative = (
                f"Cycle {cycle}: I faced a cognitive conflict regarding '{lemma_str}' in sentence '{sentence}'. "
                f"My cognitive arousal was elevated ({arousal:.2f}) and clarity dropped to {clarity:.2f}. "
                f"I enacted an alarmed posture while seeking clarification."
            )
        else:
            senses_str = "; ".join(f"{k} as {v.split()[0]}" for k, v in resolved_senses.items())
            narrative = (
                f"Cycle {cycle}: I resolved '{lemma_str}' ({senses_str}) in context '{sentence}'. "
                f"My structural order harmonized with {speaking_register}, stabilizing clarity at {clarity:.2f}."
            )

        echo = post_action_echo or {"arousal_delta": -0.05, "valence_delta": +0.05}

        factual = {
            "sentence": sentence,
            "target_lemmas": list(target_lemmas),
            "resolved_senses": dict(resolved_senses),
        }
        if core_pattern:
            factual["core_pattern"] = core_pattern

        full_leaf_dials = {
            k: round(float(leaf_dials.get(k, 0.50)), 4)
            for k in sorted(CANONICAL_LEAF_IDS)
        }

        entry = {
            "episode_id": ep_id,
            "cycle": int(cycle),
            "factual_anchor": factual,
            "affective_snapshot": {
                "arousal": round(arousal, 4),
                "valence": round(float(leaf_dials.get("experiential/phase/valence", 0.50)), 4),
                "novelty": round(novelty, 4),
                "salience": round(salience, 4),
                "clarity": round(clarity, 4),
                "order": round(float(leaf_dials.get("philosophical/structure/order", 0.50)), 4),
            },
            "leaf_dials": full_leaf_dials,
            "actuation_enacted": {
                "speaking_register": speaking_register,
                "action_bid": action_bid,
            },
            "english_narrative_reflection": narrative,
            "post_action_echo": echo,
        }

        self.entries.append(entry)

        return {
            "admitted": True,
            "reason": "Salience / disruption threshold satisfied",
            "episode": deepcopy(entry),
        }

    def recall_precedents(self, lemma: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Retrieves relevant past autobiographical episodes for context priming."""
        lemma_lower = lemma.lower()
        matched = []
        for ep in reversed(self.entries):
            lemmas = [l.lower() for l in ep["factual_anchor"]["target_lemmas"]]
            if lemma_lower in lemmas or lemma_lower in ep["factual_anchor"]["sentence"].lower():
                matched.append(deepcopy(ep))
                if len(matched) >= limit:
                    break
        return matched

    def export_journal(self) -> Dict[str, Any]:
        """Serializes journal state for standalone packaging."""
        payload = {
            "capacity": self.capacity,
            "total_episodes_recorded": self.total_episodes_recorded,
            "current_buffer_length": len(self.entries),
            "episodes": list(self.entries),
        }
        payload["journal_digest"] = digest({k: v for k, v in payload.items() if k != "journal_digest"})
        return payload

    def import_journal(self, data: Dict[str, Any]) -> None:
        """Restores journal state from serialized payload."""
        self.capacity = int(data.get("capacity", DEFAULT_JOURNAL_CAPACITY))
        self.total_episodes_recorded = int(data.get("total_episodes_recorded", 0))
        self.entries = deque(data.get("episodes", []), maxlen=self.capacity)


class OrdinaryMemoryJournalComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def __init__(self, capacity: int = DEFAULT_JOURNAL_CAPACITY):
        self.capacity = max(1, int(capacity))
        self.entries: deque = deque(maxlen=self.capacity)
        self.total_episodes_recorded = 0

    def record(
        self,
        cycle: int,
        sentence: str,
        target_lemmas: List[str],
        resolved_senses: Dict[str, str],
        leaf_dials: Dict[str, float],
        speaking_register: str,
        action_bid: str,
        post_action_echo: Optional[Dict[str, Any]] = None,
        is_conflict: bool = False,
        custom_id: Optional[str] = None,
        core_pattern: Optional[str] = None,
    ) -> Dict[str, Any]:
        salience = float(leaf_dials.get("experiential/reflection/salience", 0.50))
        novelty = float(leaf_dials.get("experiential/reflection/novelty", 0.50))
        arousal = float(leaf_dials.get("experiential/phase/arousal", 0.50))
        clarity = float(leaf_dials.get("psychological/contemplation/clarity", 0.50))

        qualifies = (
            salience >= SALIENCY_ADMISSION_THRESHOLD
            or novelty >= NOVELTY_SURPRISE_THRESHOLD
            or is_conflict
        )

        if not qualifies:
            return {
                "admitted": False,
                "reason": f"Sub-threshold salience ({salience:.2f} < {SALIENCY_ADMISSION_THRESHOLD}) and no disruption",
                "episode": None,
            }

        self.total_episodes_recorded += 1
        ep_id = custom_id or f"ep-{cycle:04d}-{self.total_episodes_recorded:03d}"

        lemma_str = ", ".join(target_lemmas)
        if is_conflict or clarity < 0.35:
            narrative = (
                f"Cycle {cycle}: I faced a cognitive conflict regarding '{lemma_str}' in sentence '{sentence}'. "
                f"My cognitive arousal was elevated ({arousal:.2f}) and clarity dropped to {clarity:.2f}. "
                f"I enacted an alarmed posture while seeking clarification."
            )
        else:
            senses_str = "; ".join(f"{k} as {v.split()[0]}" for k, v in resolved_senses.items())
            narrative = (
                f"Cycle {cycle}: I resolved '{lemma_str}' ({senses_str}) in context '{sentence}'. "
                f"My structural order harmonized with {speaking_register}, stabilizing clarity at {clarity:.2f}."
            )

        echo = post_action_echo or {"arousal_delta": -0.05, "valence_delta": +0.05}

        factual = {
            "sentence": sentence,
            "target_lemmas": list(target_lemmas),
            "resolved_senses": dict(resolved_senses),
        }
        if core_pattern:
            factual["core_pattern"] = core_pattern

        full_leaf_dials = {
            k: round(float(leaf_dials.get(k, 0.50)), 4)
            for k in sorted(CANONICAL_LEAF_IDS)
        }

        entry = {
            "episode_id": ep_id,
            "cycle": int(cycle),
            "factual_anchor": factual,
            "affective_snapshot": {
                "arousal": round(arousal, 4),
                "valence": round(float(leaf_dials.get("experiential/phase/valence", 0.50)), 4),
                "novelty": round(novelty, 4),
                "salience": round(salience, 4),
                "clarity": round(clarity, 4),
                "order": round(float(leaf_dials.get("philosophical/structure/order", 0.50)), 4),
            },
            "leaf_dials": full_leaf_dials,
            "actuation_enacted": {
                "speaking_register": speaking_register,
                "action_bid": action_bid,
            },
            "english_narrative_reflection": narrative,
            "post_action_echo": echo,
        }

        self.entries.append(entry)

        return {
            "admitted": True,
            "reason": "Salience / disruption threshold satisfied",
            "episode": deepcopy(entry),
        }

    def recall(self, lemma: str, limit: int = 3) -> List[Dict[str, Any]]:
        lemma_lower = lemma.lower()
        matched = []
        for ep in reversed(self.entries):
            lemmas = [l.lower() for l in ep["factual_anchor"]["target_lemmas"]]
            if lemma_lower in lemmas or lemma_lower in ep["factual_anchor"]["sentence"].lower():
                matched.append(deepcopy(ep))
                if len(matched) >= limit:
                    break
        return matched

    def export_journal(self) -> Dict[str, Any]:
        payload = {
            "capacity": self.capacity,
            "total_episodes_recorded": self.total_episodes_recorded,
            "current_buffer_length": len(self.entries),
            "episodes": list(self.entries),
        }
        payload["journal_digest"] = digest({k: v for k, v in payload.items() if k != "journal_digest"})
        return payload
