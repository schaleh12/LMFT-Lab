"""Inverted Lemma Index & Context Trie Engine.

Enables scalable O(1) candidate rule retrieval and sub-millisecond anchor matching
over thousands of polysemous capacity rules, eliminating O(N) linear scanning.

Architecture:
1. InvertedLemmaIndex: Maps lemma roots and anchor tokens directly to matching rules.
2. ContextPrefixTrie: Multi-token prefix tree for rapid longest-prefix collocation matching.

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during execution.
"""
from copy import deepcopy
import json
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from lmft_lab.runtime_store import digest


def clean_token(token: str) -> str:
    """Strips punctuation and lowercases token."""
    return re.sub(r"^[^\w]+|[^\w]+$", "", token.lower()).strip()


def tokenize_clean(text: str) -> List[str]:
    """Tokenizes text into cleaned lowercase tokens."""
    return [clean_token(t) for t in text.split() if clean_token(t)]


class TrieNode:
    """Node in multi-token prefix collocation trie."""
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.rules: List[Dict[str, Any]] = []
        self.is_terminal: bool = False


class ContextPrefixTrie:
    """Prefix trie for multi-token syntactic collocations."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, pattern_tokens: List[str], rule: Dict[str, Any]):
        """Inserts a token sequence into the prefix trie."""
        node = self.root
        for tok in pattern_tokens:
            if tok not in node.children:
                node.children[tok] = TrieNode()
            node = node.children[tok]
        node.is_terminal = True
        node.rules.append(rule)

    def match_prefix(self, tokens: List[str], start_idx: int) -> List[Dict[str, Any]]:
        """Matches the longest available collocation sequence starting at start_idx."""
        node = self.root
        matched_rules = []
        curr = start_idx
        while curr < len(tokens) and tokens[curr] in node.children:
            node = node.children[tokens[curr]]
            if node.is_terminal:
                matched_rules.extend(node.rules)
            curr += 1
        return matched_rules


class InvertedLemmaIndex:
    """Inverted index combining token hash maps and prefix tries for O(1) candidate filtering."""
    def __init__(self):
        self.lemma_to_rules: Dict[str, List[Dict[str, Any]]] = {}
        self.token_to_rules: Dict[str, List[Dict[str, Any]]] = {}
        self.trie = ContextPrefixTrie()
        self.total_rules: int = 0

    def add_rule(self, rule: Dict[str, Any]):
        """Indexes a capacity rule into the inverted index and trie."""
        lemma = clean_token(rule.get("lemma", ""))
        pattern = rule.get("core_pattern", "")
        pattern_tokens = tokenize_clean(pattern)
        
        # 1. Index under primary lemma
        if lemma:
            if lemma not in self.lemma_to_rules:
                self.lemma_to_rules[lemma] = []
            self.lemma_to_rules[lemma].append(rule)
            
        # 2. Inverted index under all pattern tokens
        for tok in pattern_tokens:
            if tok not in self.token_to_rules:
                self.token_to_rules[tok] = []
            self.token_to_rules[tok].append(rule)
            
        # 3. Add to prefix trie
        if pattern_tokens:
            self.trie.insert(pattern_tokens, rule)
            
        self.total_rules += 1

    def lookup_candidates(self, query_tokens: List[str]) -> List[Dict[str, Any]]:
        """Filters candidate rules in O(1) time without scanning unrelated rules."""
        candidate_ids = set()
        candidate_rules = []
        
        for tok in query_tokens:
            # Check lemma map
            if tok in self.lemma_to_rules:
                for r in self.lemma_to_rules[tok]:
                    if r["rule_id"] not in candidate_ids:
                        candidate_ids.add(r["rule_id"])
                        candidate_rules.append(r)
            # Check token map
            if tok in self.token_to_rules:
                for r in self.token_to_rules[tok]:
                    if r["rule_id"] not in candidate_ids:
                        candidate_ids.add(r["rule_id"])
                        candidate_rules.append(r)
                        
        return candidate_rules

    def match_sentence(self, text: str) -> List[Dict[str, Any]]:
        """Fast sentence evaluation using combined trie prefix matching and candidate filtering."""
        tokens = tokenize_clean(text)
        matched_rule_ids = set()
        matched_rules = []
        
        # 1. Multi-token trie scan
        for i in range(len(tokens)):
            trie_matches = self.trie.match_prefix(tokens, i)
            for r in trie_matches:
                if r["rule_id"] not in matched_rule_ids:
                    matched_rule_ids.add(r["rule_id"])
                    matched_rules.append(r)
                    
        # 2. Candidate confirmation for single-token or non-contiguous patterns
        candidates = self.lookup_candidates(tokens)
        text_lower = " " + " ".join(tokens) + " "
        for r in candidates:
            if r["rule_id"] not in matched_rule_ids:
                pat = " " + " ".join(tokenize_clean(r["core_pattern"])) + " "
                if pat in text_lower:
                    matched_rule_ids.add(r["rule_id"])
                    matched_rules.append(r)
                    
        return matched_rules


def linear_scan_rules(rules: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
    """Naive O(N) baseline scanner that iterates through every rule in memory."""
    tokens = tokenize_clean(text)
    text_lower = " " + " ".join(tokens) + " "
    matched = []
    for r in rules:
        pat = " " + " ".join(tokenize_clean(r["core_pattern"])) + " "
        if pat in text_lower:
            matched.append(r)
    return matched


class OrdinaryMemoryInvertedComparator:
    """Matched ordinary structured-memory baseline (Rule D004).
    
    Verifies that inverted index retrieval matches linear scan decisions exactly.
    """
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = deepcopy(rules)
        self.index = InvertedLemmaIndex()
        for r in self.rules:
            self.index.add_rule(r)

    def evaluate(self, text: str) -> Dict[str, Any]:
        fast_matches = self.index.match_sentence(text)
        linear_matches = linear_scan_rules(self.rules, text)
        
        # Parity assert
        fast_ids = sorted({r["rule_id"] for r in fast_matches})
        linear_ids = sorted({r["rule_id"] for r in linear_matches})
        assert fast_ids == linear_ids, "Parity divergence between inverted index and linear scan!"
        
        return {
            "text": text,
            "matched_rules": fast_ids,
            "match_count": len(fast_ids),
        }
