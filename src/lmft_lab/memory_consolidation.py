"""Dual-Speed Memory Consolidation Engine ("Sleep / Replay").

Mirrors hippocampal-neocortical memory consolidation by replaying episodic records
during idle/sleep phases, consolidating recurring patterns (N >= min_confirmations) into
persistent long-term capacity rules and pruning transient buffer noise.

Preserves Rule D001 (frozen 40-node founding seed) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""
from copy import deepcopy
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from lmft_lab.anchor_deduplication import normalize_anchor_text
from lmft_lab.birth import _inventory
from lmft_lab.capacity_decay import reinforce_weight, decay_weight
from lmft_lab.runtime_store import digest


DEFAULT_MIN_CONFIRMATIONS = 2
DEFAULT_CONSOLIDATION_ALPHA = 0.20


class MemoryConsolidationEngine:
    """Manages offline memory replay, capacity rule promotion, and buffer pruning."""

    def __init__(
        self,
        initial_rules: Optional[List[Dict[str, Any]]] = None,
        min_confirmations: int = DEFAULT_MIN_CONFIRMATIONS,
        reinforcement_rate: float = DEFAULT_CONSOLIDATION_ALPHA,
    ):
        self.min_confirmations = max(1, int(min_confirmations))
        self.reinforcement_rate = float(reinforcement_rate)
        self.long_term_rules: Dict[str, Dict[str, Any]] = {}
        self.sleep_cycles_completed = 0
        self.history: List[Dict[str, Any]] = []

        if initial_rules:
            for r in initial_rules:
                rule_id = r.get("rule_id") or f"rule-{len(self.long_term_rules)+1:03d}"
                rule_copy = deepcopy(r)
                rule_copy["rule_id"] = rule_id
                rule_copy["weight"] = float(rule_copy.get("weight", 0.50))
                rule_copy["witnesses"] = sorted(set(rule_copy.get("witnesses", [])))
                self.long_term_rules[rule_id] = rule_copy

    def _extract_pattern_key(self, sentence: str, lemma: str, sense: str, explicit_pattern: Optional[str] = None) -> Tuple[str, str, str]:
        """Extracts canonical (lemma, sense, normalized_pattern) tuple."""
        clean_lemma = lemma.strip().lower()
        clean_sense = sense.strip()
        if explicit_pattern:
            norm_pattern = normalize_anchor_text(explicit_pattern)
        else:
            words = [re.sub(r"^[^\w]+|[^\w]+$", "", w.lower()) for w in sentence.split() if w.strip()]
            lemma_idx = -1
            for i, w in enumerate(words):
                if clean_lemma in w:
                    lemma_idx = i
                    break
            if lemma_idx >= 0:
                if lemma_idx > 0 and normalize_anchor_text(words[lemma_idx - 1]):
                    collocate = f"{words[lemma_idx - 1]} {words[lemma_idx]}"
                elif lemma_idx + 1 < len(words) and normalize_anchor_text(words[lemma_idx + 1]):
                    collocate = f"{words[lemma_idx]} {words[lemma_idx + 1]}"
                else:
                    collocate = words[lemma_idx]
                norm_pattern = normalize_anchor_text(collocate)
            else:
                norm_pattern = normalize_anchor_text(sentence)

        return (clean_lemma, clean_sense, norm_pattern)

    def _find_matching_long_term_rule(self, lemma: str, sense: str, pattern: str) -> Optional[str]:
        """Finds existing long-term rule matching the canonical pattern using token boundaries."""
        norm_pat = normalize_anchor_text(pattern)
        best_rule_id = None
        best_weight = -1.0
        for rule_id, rule in self.long_term_rules.items():
            r_lemma = rule.get("lemma", "").strip().lower()
            r_sense = rule.get("target_sense_key", "").strip()
            r_pattern = normalize_anchor_text(rule.get("core_pattern", ""))

            if r_lemma == lemma and r_sense == sense:
                matched = False
                if r_pattern == norm_pat and norm_pat != "":
                    matched = True
                elif r_pattern and norm_pat:
                    padded_r = f" {r_pattern} "
                    padded_p = f" {norm_pat} "
                    if padded_r in padded_p or padded_p in padded_r:
                        matched = True
                if matched:
                    w = float(rule.get("weight", 0.50))
                    if w > best_weight:
                        best_weight = w
                        best_rule_id = rule_id
        return best_rule_id

    def consolidate_sleep_cycle(
        self,
        episodic_buffer: List[Dict[str, Any]],
        prune_buffer: bool = True,
        retain_unconfirmed: bool = False,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Replays episodic buffer, reinforces/promotes rules, and prunes transient noise."""
        self.sleep_cycles_completed += 1
        current_sleep_cycle = self.sleep_cycles_completed

        # 1. Group episodic occurrences by pattern
        pattern_groups: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = {}

        for ep in episodic_buffer:
            sentence = ep["factual_anchor"]["sentence"]
            target_lemmas = ep["factual_anchor"]["target_lemmas"]
            resolved_senses = ep["factual_anchor"]["resolved_senses"]
            explicit_pattern = ep["factual_anchor"].get("core_pattern")

            for lemma in target_lemmas:
                sense = resolved_senses.get(lemma, "unknown")
                key = self._extract_pattern_key(sentence, lemma, sense, explicit_pattern)
                if key not in pattern_groups:
                    pattern_groups[key] = []
                pattern_groups[key].append(ep)

        promoted_rules: List[Dict[str, Any]] = []
        reinforced_rules: List[Dict[str, Any]] = []
        transient_noise_count = 0
        admitted_episode_ids: Set[str] = set()

        # 2. Evaluate consolidation for each pattern
        for (lemma, sense, pattern), eps in sorted(pattern_groups.items(), key=lambda x: str(x[0])):
            existing_rule_id = self._find_matching_long_term_rule(lemma, sense, pattern)

            if existing_rule_id:
                # Rule already in long-term memory: reinforce habituated weight
                rule = self.long_term_rules[existing_rule_id]
                old_weight = rule.get("weight", 0.50)
                new_weight = old_weight
                for _ in range(len(eps)):
                    new_weight = reinforce_weight(new_weight, self.reinforcement_rate)
                rule["weight"] = new_weight

                # Add new episode witnesses
                witnesses = set(rule.get("witnesses", []))
                for ep in eps:
                    witnesses.add(ep.get("episode_id", f"ep-cycle-{ep['cycle']}"))
                    admitted_episode_ids.add(ep.get("episode_id", ""))
                rule["witnesses"] = sorted(witnesses)
                rule["last_consolidated_cycle"] = current_sleep_cycle

                reinforced_rules.append({
                    "rule_id": existing_rule_id,
                    "lemma": lemma,
                    "target_sense_key": sense,
                    "pattern": pattern,
                    "old_weight": old_weight,
                    "new_weight": new_weight,
                    "witness_count": len(rule["witnesses"]),
                })

            elif len(eps) >= self.min_confirmations:
                # Pattern confirmed across multiple observations: promote to new long-term rule
                clean_sense_prefix = sense.split()[0].replace("%", "_").replace(":", "_")
                new_rule_id = f"rule-{lemma}-{clean_sense_prefix}-{len(self.long_term_rules)+1:02d}"

                # Calculate habituated weight
                base_weight = 0.50
                for _ in range(len(eps) - 1):
                    base_weight = reinforce_weight(base_weight, self.reinforcement_rate)

                witness_ids = [ep.get("episode_id", f"ep-cycle-{ep['cycle']}") for ep in eps]
                for ep in eps:
                    admitted_episode_ids.add(ep.get("episode_id", ""))

                # Rich narrative reflection or posture from most recent episode
                latest_ep = eps[-1]
                speaking_register = latest_ep.get("actuation_enacted", {}).get("speaking_register", "Methodical & Pragmatic")
                action_bid = latest_ep.get("actuation_enacted", {}).get("action_bid", "Enforce consolidated pattern")

                new_rule = {
                    "rule_id": new_rule_id,
                    "lemma": lemma,
                    "target_sense_key": sense,
                    "core_pattern": pattern,
                    "gloss": f"Consolidated concept for {lemma} ({sense})",
                    "weight": base_weight,
                    "speaking_register": speaking_register,
                    "action_bid": action_bid,
                    "witnesses": sorted(witness_ids),
                    "promoted_at_sleep_cycle": current_sleep_cycle,
                    "last_consolidated_cycle": current_sleep_cycle,
                }

                # Consolidate 24-leaf fuzzy membership centroid and affinities if present on episodes
                ep_leaf_vectors = [ep["leaf_dials"] for ep in eps if isinstance(ep.get("leaf_dials"), dict) and ep["leaf_dials"]]
                if ep_leaf_vectors:
                    all_keys = sorted({k for vec in ep_leaf_vectors for k in vec.keys()})
                    centroid = {
                        k: round(sum(float(vec.get(k, 0.50)) for vec in ep_leaf_vectors) / len(ep_leaf_vectors), 4)
                        for k in all_keys
                    }
                    affinities = {
                        k: round(val - 0.50, 4)
                        for k, val in centroid.items()
                        if abs(val - 0.50) >= 0.02
                    }
                    new_rule["leaf_dials"] = centroid
                    new_rule["leaf_dial_affinities"] = affinities

                self.long_term_rules[new_rule_id] = new_rule
                promoted_rules.append(deepcopy(new_rule))

            else:
                # Sub-threshold singleton observation: transient noise
                transient_noise_count += len(eps)

        # 3. Buffer pruning
        if prune_buffer:
            if retain_unconfirmed:
                remaining_buffer = [
                    deepcopy(ep) for ep in episodic_buffer
                    if ep.get("is_conflict", False) or ep.get("episode_id") not in admitted_episode_ids
                ]
            else:
                remaining_buffer = [
                    deepcopy(ep) for ep in episodic_buffer
                    if ep.get("is_conflict", False) and ep.get("episode_id") not in admitted_episode_ids
                ]
        else:
            remaining_buffer = deepcopy(episodic_buffer)

        # 4. Generate cycle summary
        rules_dict_for_digest = {k: v for k, v in sorted(self.long_term_rules.items())}
        summary = {
            "sleep_cycle": current_sleep_cycle,
            "replayed_episode_count": len(episodic_buffer),
            "promoted_rules_count": len(promoted_rules),
            "promoted_rules": promoted_rules,
            "reinforced_rules_count": len(reinforced_rules),
            "reinforced_rules": reinforced_rules,
            "transient_noise_pruned_count": transient_noise_count,
            "remaining_buffer_count": len(remaining_buffer),
            "total_long_term_rules": len(self.long_term_rules),
            "consolidation_digest": digest(rules_dict_for_digest),
        }

        self.history.append(deepcopy(summary))
        return summary, remaining_buffer

    def export_state(self) -> Dict[str, Any]:
        """Serializes consolidation state for persistence and packaging."""
        rules_dict_for_digest = {k: v for k, v in sorted(self.long_term_rules.items())}
        payload = {
            "sleep_cycles_completed": self.sleep_cycles_completed,
            "min_confirmations": self.min_confirmations,
            "reinforcement_rate": self.reinforcement_rate,
            "total_long_term_rules": len(self.long_term_rules),
            "long_term_rules": list(self.long_term_rules.values()),
            "history_length": len(self.history),
            "consolidation_digest": digest(rules_dict_for_digest),
        }
        return payload

    def import_state(self, data: Dict[str, Any]) -> None:
        """Restores consolidation state from serialized payload."""
        self.sleep_cycles_completed = int(data.get("sleep_cycles_completed", 0))
        self.min_confirmations = int(data.get("min_confirmations", DEFAULT_MIN_CONFIRMATIONS))
        self.reinforcement_rate = float(data.get("reinforcement_rate", DEFAULT_CONSOLIDATION_ALPHA))
        self.long_term_rules = {r["rule_id"]: deepcopy(r) for r in data.get("long_term_rules", [])}


class OrdinaryMemoryConsolidationComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def __init__(
        self,
        initial_rules: Optional[List[Dict[str, Any]]] = None,
        min_confirmations: int = DEFAULT_MIN_CONFIRMATIONS,
        reinforcement_rate: float = DEFAULT_CONSOLIDATION_ALPHA,
    ):
        self.min_confirmations = max(1, int(min_confirmations))
        self.reinforcement_rate = float(reinforcement_rate)
        self.long_term_rules: Dict[str, Dict[str, Any]] = {}
        self.sleep_cycles_completed = 0
        self.history: List[Dict[str, Any]] = []

        if initial_rules:
            for r in initial_rules:
                rule_id = r.get("rule_id") or f"rule-{len(self.long_term_rules)+1:03d}"
                rule_copy = deepcopy(r)
                rule_copy["rule_id"] = rule_id
                rule_copy["weight"] = float(rule_copy.get("weight", 0.50))
                rule_copy["witnesses"] = sorted(set(rule_copy.get("witnesses", [])))
                self.long_term_rules[rule_id] = rule_copy

    def _extract_pattern_key(self, sentence: str, lemma: str, sense: str, explicit_pattern: Optional[str] = None) -> Tuple[str, str, str]:
        clean_lemma = lemma.strip().lower()
        clean_sense = sense.strip()
        if explicit_pattern:
            norm_pattern = normalize_anchor_text(explicit_pattern)
        else:
            words = [re.sub(r"^[^\w]+|[^\w]+$", "", w.lower()) for w in sentence.split() if w.strip()]
            lemma_idx = -1
            for i, w in enumerate(words):
                if clean_lemma in w:
                    lemma_idx = i
                    break
            if lemma_idx >= 0:
                if lemma_idx > 0 and normalize_anchor_text(words[lemma_idx - 1]):
                    collocate = f"{words[lemma_idx - 1]} {words[lemma_idx]}"
                elif lemma_idx + 1 < len(words) and normalize_anchor_text(words[lemma_idx + 1]):
                    collocate = f"{words[lemma_idx]} {words[lemma_idx + 1]}"
                else:
                    collocate = words[lemma_idx]
                norm_pattern = normalize_anchor_text(collocate)
            else:
                norm_pattern = normalize_anchor_text(sentence)

        return (clean_lemma, clean_sense, norm_pattern)

    def _find_matching_long_term_rule(self, lemma: str, sense: str, pattern: str) -> Optional[str]:
        norm_pat = normalize_anchor_text(pattern)
        best_rule_id = None
        best_weight = -1.0
        for rule_id, rule in self.long_term_rules.items():
            r_lemma = rule.get("lemma", "").strip().lower()
            r_sense = rule.get("target_sense_key", "").strip()
            r_pattern = normalize_anchor_text(rule.get("core_pattern", ""))

            if r_lemma == lemma and r_sense == sense:
                matched = False
                if r_pattern == norm_pat and norm_pat != "":
                    matched = True
                elif r_pattern and norm_pat:
                    padded_r = f" {r_pattern} "
                    padded_p = f" {norm_pat} "
                    if padded_r in padded_p or padded_p in padded_r:
                        matched = True
                if matched:
                    w = float(rule.get("weight", 0.50))
                    if w > best_weight:
                        best_weight = w
                        best_rule_id = rule_id
        return best_rule_id

    def consolidate(
        self,
        episodic_buffer: List[Dict[str, Any]],
        prune_buffer: bool = True,
        retain_unconfirmed: bool = False,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        self.sleep_cycles_completed += 1
        current_sleep_cycle = self.sleep_cycles_completed

        pattern_groups: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = {}

        for ep in episodic_buffer:
            sentence = ep["factual_anchor"]["sentence"]
            target_lemmas = ep["factual_anchor"]["target_lemmas"]
            resolved_senses = ep["factual_anchor"]["resolved_senses"]
            explicit_pattern = ep["factual_anchor"].get("core_pattern")

            for lemma in target_lemmas:
                sense = resolved_senses.get(lemma, "unknown")
                key = self._extract_pattern_key(sentence, lemma, sense, explicit_pattern)
                if key not in pattern_groups:
                    pattern_groups[key] = []
                pattern_groups[key].append(ep)

        promoted_rules: List[Dict[str, Any]] = []
        reinforced_rules: List[Dict[str, Any]] = []
        transient_noise_count = 0
        admitted_episode_ids: Set[str] = set()

        for (lemma, sense, pattern), eps in sorted(pattern_groups.items(), key=lambda x: str(x[0])):
            existing_rule_id = self._find_matching_long_term_rule(lemma, sense, pattern)

            if existing_rule_id:
                rule = self.long_term_rules[existing_rule_id]
                old_weight = rule.get("weight", 0.50)
                new_weight = old_weight
                for _ in range(len(eps)):
                    new_weight = reinforce_weight(new_weight, self.reinforcement_rate)
                rule["weight"] = new_weight

                witnesses = set(rule.get("witnesses", []))
                for ep in eps:
                    witnesses.add(ep.get("episode_id", f"ep-cycle-{ep['cycle']}"))
                    admitted_episode_ids.add(ep.get("episode_id", ""))
                rule["witnesses"] = sorted(witnesses)
                rule["last_consolidated_cycle"] = current_sleep_cycle

                reinforced_rules.append({
                    "rule_id": existing_rule_id,
                    "lemma": lemma,
                    "target_sense_key": sense,
                    "pattern": pattern,
                    "old_weight": old_weight,
                    "new_weight": new_weight,
                    "witness_count": len(rule["witnesses"]),
                })

            elif len(eps) >= self.min_confirmations:
                clean_sense_prefix = sense.split()[0].replace("%", "_").replace(":", "_")
                new_rule_id = f"rule-{lemma}-{clean_sense_prefix}-{len(self.long_term_rules)+1:02d}"

                base_weight = 0.50
                for _ in range(len(eps) - 1):
                    base_weight = reinforce_weight(base_weight, self.reinforcement_rate)

                witness_ids = [ep.get("episode_id", f"ep-cycle-{ep['cycle']}") for ep in eps]
                for ep in eps:
                    admitted_episode_ids.add(ep.get("episode_id", ""))

                latest_ep = eps[-1]
                speaking_register = latest_ep.get("actuation_enacted", {}).get("speaking_register", "Methodical & Pragmatic")
                action_bid = latest_ep.get("actuation_enacted", {}).get("action_bid", "Enforce consolidated pattern")

                new_rule = {
                    "rule_id": new_rule_id,
                    "lemma": lemma,
                    "target_sense_key": sense,
                    "core_pattern": pattern,
                    "gloss": f"Consolidated concept for {lemma} ({sense})",
                    "weight": base_weight,
                    "speaking_register": speaking_register,
                    "action_bid": action_bid,
                    "witnesses": sorted(witness_ids),
                    "promoted_at_sleep_cycle": current_sleep_cycle,
                    "last_consolidated_cycle": current_sleep_cycle,
                }

                ep_leaf_vectors = [ep["leaf_dials"] for ep in eps if isinstance(ep.get("leaf_dials"), dict) and ep["leaf_dials"]]
                if ep_leaf_vectors:
                    all_keys = sorted({k for vec in ep_leaf_vectors for k in vec.keys()})
                    centroid = {
                        k: round(sum(float(vec.get(k, 0.50)) for vec in ep_leaf_vectors) / len(ep_leaf_vectors), 4)
                        for k in all_keys
                    }
                    affinities = {
                        k: round(val - 0.50, 4)
                        for k, val in centroid.items()
                        if abs(val - 0.50) >= 0.02
                    }
                    new_rule["leaf_dials"] = centroid
                    new_rule["leaf_dial_affinities"] = affinities

                self.long_term_rules[new_rule_id] = new_rule
                promoted_rules.append(deepcopy(new_rule))

            else:
                transient_noise_count += len(eps)

        if prune_buffer:
            if retain_unconfirmed:
                remaining_buffer = [
                    deepcopy(ep) for ep in episodic_buffer
                    if ep.get("is_conflict", False) or ep.get("episode_id") not in admitted_episode_ids
                ]
            else:
                remaining_buffer = [
                    deepcopy(ep) for ep in episodic_buffer
                    if ep.get("is_conflict", False) and ep.get("episode_id") not in admitted_episode_ids
                ]
        else:
            remaining_buffer = deepcopy(episodic_buffer)

        rules_dict_for_digest = {k: v for k, v in sorted(self.long_term_rules.items())}
        summary = {
            "sleep_cycle": current_sleep_cycle,
            "replayed_episode_count": len(episodic_buffer),
            "promoted_rules_count": len(promoted_rules),
            "promoted_rules": promoted_rules,
            "reinforced_rules_count": len(reinforced_rules),
            "reinforced_rules": reinforced_rules,
            "transient_noise_pruned_count": transient_noise_count,
            "remaining_buffer_count": len(remaining_buffer),
            "total_long_term_rules": len(self.long_term_rules),
            "consolidation_digest": digest(rules_dict_for_digest),
        }

        self.history.append(deepcopy(summary))
        return summary, remaining_buffer

    def export_state(self) -> Dict[str, Any]:
        rules_dict_for_digest = {k: v for k, v in sorted(self.long_term_rules.items())}
        payload = {
            "sleep_cycles_completed": self.sleep_cycles_completed,
            "min_confirmations": self.min_confirmations,
            "reinforcement_rate": self.reinforcement_rate,
            "total_long_term_rules": len(self.long_term_rules),
            "long_term_rules": list(self.long_term_rules.values()),
            "history_length": len(self.history),
            "consolidation_digest": digest(rules_dict_for_digest),
        }
        return payload
