"""Anchor Normalization & Deduplication Engine.

Standardizes surface phrasing variations and merges duplicate candidate proposals
extracted across repeated corpus passes into canonical capacity rules.

Normalization pipeline:
1. Strips leading/trailing determiners, articles, and possessive pronouns.
2. Strips surrounding punctuation, standardizes internal whitespace, and lowercases.
3. Groups proposals by (lemma, target_sense_key, normalized_pattern).
4. Merges duplicates: unions observation witness IDs, selects richest gloss,
   and applies fuzzy reinforcement confidence boost (+0.15 * (1 - w)).

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during execution.
"""
from copy import deepcopy
import json
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from lmft_lab.runtime_store import digest

DETERMINERS = {
    "the", "a", "an", "this", "that", "these", "those",
    "my", "your", "his", "her", "its", "our", "their",
}


def normalize_anchor_text(text: str) -> str:
    """Normalizes raw collocate strings into clean canonical syntactic anchors."""
    # Strip leading/trailing punctuation
    cleaned = re.sub(r"^[^\w]+|[^\w]+$", "", text.strip().lower())
    
    # Split into words and filter out standalone punctuation tokens that strip to empty
    raw_words = [re.sub(r"^[^\w]+|[^\w]+$", "", w) for w in cleaned.split() if w.strip()]
    words = [w for w in raw_words if w]
    
    # Strip leading determiners
    while words and words[0] in DETERMINERS:
        words.pop(0)
        
    # Strip trailing determiners
    while words and words[-1] in DETERMINERS:
        words.pop(-1)
        
    return " ".join(words).strip()


def merge_duplicate_rules(rule_group: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merges a list of duplicate candidate proposals into a single reinforced canonical rule."""
    if not rule_group:
        raise ValueError("Cannot merge empty rule group")
    if len(rule_group) == 1:
        base = deepcopy(rule_group[0])
        base["core_pattern"] = normalize_anchor_text(base.get("core_pattern", ""))
        base["witnesses"] = sorted(set(base.get("witnesses", [])))
        return base

    # Sort by rule_id for determinism
    sorted_group = sorted(rule_group, key=lambda r: r.get("rule_id", ""))
    primary = deepcopy(sorted_group[0])
    
    canonical_pattern = normalize_anchor_text(primary.get("core_pattern", ""))
    primary["core_pattern"] = canonical_pattern
    
    # Union all witnesses
    all_witnesses: Set[str] = set()
    for r in sorted_group:
        all_witnesses.update(r.get("witnesses", []))
    primary["witnesses"] = sorted(all_witnesses)
    
    # Select longest / richest gloss
    richest_gloss = primary.get("gloss", "")
    for r in sorted_group[1:]:
        g = r.get("gloss", "")
        if len(g) > len(richest_gloss):
            richest_gloss = g
    primary["gloss"] = richest_gloss
    
    # Apply fuzzy reinforcement boost for duplicate confirmations
    w = primary.get("weight", 0.50)
    for _ in range(len(sorted_group) - 1):
        w = w + 0.15 * (1.0 - w)
    primary["weight"] = round(min(1.0, w), 4)
    primary["merge_count"] = len(sorted_group)
    
    return primary


def deduplicate_rules(candidate_rules: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Deduplicates a list of candidate rules, returning canonical rules and merge statistics."""
    grouped: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = {}
    
    for r in candidate_rules:
        lemma = r.get("lemma", "").strip().lower()
        sense = r.get("target_sense_key", "").strip()
        raw_pat = r.get("core_pattern", "")
        norm_pat = normalize_anchor_text(raw_pat)
        
        key = (lemma, sense, norm_pat)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(r)
        
    canonical_rules = []
    total_duplicates_merged = 0
    
    for key, group in sorted(grouped.items(), key=lambda item: item[0]):
        merged = merge_duplicate_rules(group)
        if len(group) > 1:
            total_duplicates_merged += (len(group) - 1)
        canonical_rules.append(merged)
        
    stats = {
        "initial_candidates_count": len(candidate_rules),
        "canonical_rules_count": len(canonical_rules),
        "duplicates_merged": total_duplicates_merged,
        "compression_ratio": round(len(canonical_rules) / len(candidate_rules), 4) if candidate_rules else 1.0,
        "rules_digest": digest(canonical_rules),
    }
    
    return canonical_rules, stats


class OrdinaryMemoryDeduplicationComparator:
    """Matched ordinary structured-memory baseline (Rule D004).
    
    Executes identical normalization and merging on flat dicts.
    """
    def deduplicate(self, rules: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        return deduplicate_rules(rules)
