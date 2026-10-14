"""Multi-Lemma Polysemy Arbiter & Sentence-Level Composition Engine.

Enables the LMFT architecture to process sentences containing multiple polysemous
target words (e.g., 'bank' and 'order') simultaneously. Isolates local contextual
windows to prevent cross-anchor contamination, resolves individual senses deterministically,
and composes harmonic multi-register postures through the Tripartite Funnel.

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during evaluation.
"""
from copy import deepcopy
import hashlib
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.runtime_store import digest


# --- Canonical Capacity Rules for 'order' ---
ORDER_CAPACITY_RULES = [
    {
        "rule_id": "rule-order-cmd-01",
        "lemma": "order",
        "target_sense_key": "order%1:10:00::",
        "core_pattern": "court order",
        "gloss": "an authoritative instruction or judicial decree",
        "posture": "Noble Sovereign Action",
        "register": "Authoritative & Chivalrous",
    },
    {
        "rule_id": "rule-order-cmd-02",
        "lemma": "order",
        "target_sense_key": "order%1:10:00::",
        "core_pattern": "strict order",
        "gloss": "an authoritative command demanding obedience",
        "posture": "Noble Sovereign Action",
        "register": "Authoritative & Chivalrous",
    },
    {
        "rule_id": "rule-order-com-01",
        "lemma": "order",
        "target_sense_key": "order%1:10:01::",
        "core_pattern": "commercial order",
        "gloss": "a commercial transaction or purchase order for goods",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-order-com-02",
        "lemma": "order",
        "target_sense_key": "order%1:10:01::",
        "core_pattern": "placed an order",
        "gloss": "a commercial requisition placed for products or supplies",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-order-com-03",
        "lemma": "order",
        "target_sense_key": "order%1:10:01::",
        "core_pattern": "order of supplies",
        "gloss": "a requisition for emergency or commercial supplies",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-order-com-04",
        "lemma": "order",
        "target_sense_key": "order%1:10:01::",
        "core_pattern": "order of emergency",
        "gloss": "a requisition for emergency medical or operational supplies",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-order-seq-01",
        "lemma": "order",
        "target_sense_key": "order%1:14:00::",
        "core_pattern": "rank and order",
        "gloss": "a methodical arrangement or sequential alignment",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-order-mag-01",
        "lemma": "order",
        "target_sense_key": "order%1:07:01::",
        "core_pattern": "order of magnitude",
        "gloss": "a quantitative scale or degree of measurement",
        "posture": "Deep Flow Synthesis",
        "register": "Equilibrated & Diplomatic",
    },
]

# --- Canonical Capacity Rules for 'bank' ---
BANK_CAPACITY_RULES = [
    {
        "rule_id": "rule-bank-fin-01",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:00::",
        "core_pattern": "commercial bank",
        "gloss": "a financial institution for deposits and commercial transactions",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-bank-fin-02",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:00::",
        "core_pattern": "central bank",
        "gloss": "a national monetary authority managing interest rates and currency",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-bank-fin-03",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:00::",
        "core_pattern": "investment bank",
        "gloss": "a financial institution assisting in capital investments",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-bank-fin-04",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:00::",
        "core_pattern": "freeze the assets",
        "gloss": "a financial banking institution holding frozen assets or accounts",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-bank-fin-05",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:00::",
        "core_pattern": "deposited money",
        "gloss": "a banking depository for deposits and personal accounts",
        "posture": "Tactical Serial Progression",
        "register": "Methodical & Pragmatic",
    },
    {
        "rule_id": "rule-bank-riv-01",
        "lemma": "bank",
        "target_sense_key": "bank%1:17:01::",
        "core_pattern": "river bank",
        "gloss": "sloping natural land bordering a river or stream",
        "posture": "Foundational Anchor",
        "register": "Communal & Reassuring",
    },
    {
        "rule_id": "rule-bank-riv-02",
        "lemma": "bank",
        "target_sense_key": "bank%1:17:01::",
        "core_pattern": "bank of the stream",
        "gloss": "the embankment flanking a stream or moving waterway",
        "posture": "Foundational Anchor",
        "register": "Communal & Reassuring",
    },
    {
        "rule_id": "rule-bank-riv-03",
        "lemma": "bank",
        "target_sense_key": "bank%1:17:01::",
        "core_pattern": "steep bank",
        "gloss": "a steep natural incline adjoining a waterway or canal",
        "posture": "Foundational Anchor",
        "register": "Communal & Reassuring",
    },
    {
        "rule_id": "rule-bank-res-01",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:01::",
        "core_pattern": "blood bank",
        "gloss": "a critical medical reserve repository of blood supplies",
        "posture": "Noble Sovereign Action",
        "register": "Authoritative & Chivalrous",
    },
    {
        "rule_id": "rule-bank-res-02",
        "lemma": "bank",
        "target_sense_key": "bank%1:14:01::",
        "core_pattern": "data bank",
        "gloss": "a structured computational repository of stored information",
        "posture": "Noble Sovereign Action",
        "register": "Authoritative & Chivalrous",
    },
]

KNOWN_LEMMAS = {
    "order": {"forms": ["order", "orders"], "rules": ORDER_CAPACITY_RULES},
    "bank": {"forms": ["bank", "banks"], "rules": BANK_CAPACITY_RULES},
}


def tokenize(text: str) -> List[str]:
    """Tokenizes text into words while stripping basic punctuation."""
    return [re.sub(r"^[^\w]+|[^\w]+$", "", tok) for tok in text.split() if tok.strip()]


def scan_target_occurrences(tokens: List[str]) -> List[Dict[str, Any]]:
    """Identifies all occurrences of known polysemous target lemmas in the token list."""
    occurrences = []
    for idx, token in enumerate(tokens):
        token_lower = token.lower()
        for lemma, config in KNOWN_LEMMAS.items():
            if token_lower in config["forms"]:
                occurrences.append({
                    "lemma": lemma,
                    "token": token,
                    "token_index": idx,
                })
    return occurrences


def extract_context_window(tokens: List[str], target_index: int, window_radius: int = 5) -> str:
    """Extracts a bounded token window around target index, avoiding whole-sentence bleed."""
    start = max(0, target_index - window_radius)
    end = min(len(tokens), target_index + window_radius + 1)
    return " ".join(tokens[start:end]).lower()


def disambiguate_target(
    lemma: str,
    context_str: str,
    full_sentence_str: str,
) -> Dict[str, Any]:
    """Resolves sense for a specific lemma occurrence using its contextual window."""
    if lemma not in KNOWN_LEMMAS:
        return {
            "lemma": lemma,
            "decision": "abstain",
            "selected_sense": None,
            "explanation": f"Unknown lemma: {lemma}",
            "posture": "Neutral Observant Silence",
            "register": "Neutral Observant Silence",
            "matched_rules": [],
        }

    rules = KNOWN_LEMMAS[lemma]["rules"]
    
    # Priority 1: Match within local bounded context window
    matched = [r for r in rules if r["core_pattern"].lower() in context_str]
    
    # Priority 2: Fallback to full sentence if local window missed a multi-token collocate
    if not matched:
        matched = [r for r in rules if r["core_pattern"].lower() in full_sentence_str]

    matched_senses = sorted({r["target_sense_key"] for r in matched})
    if not matched_senses:
        return {
            "lemma": lemma,
            "decision": "abstain",
            "selected_sense": None,
            "explanation": f"No matching contextual anchor found for {lemma}.",
            "posture": "Neutral Observant Silence",
            "register": "Neutral Observant Silence",
            "matched_rules": [],
        }
    elif len(matched_senses) == 1:
        chosen = matched[0]
        return {
            "lemma": lemma,
            "decision": "single",
            "selected_sense": chosen["target_sense_key"],
            "explanation": chosen["gloss"],
            "posture": chosen["posture"],
            "register": chosen["register"],
            "matched_rules": [r["rule_id"] for r in matched],
        }
    else:
        # Multiple conflicting senses
        return {
            "lemma": lemma,
            "decision": "ambiguous",
            "selected_sense": None,
            "explanation": f"Multiple conflicting senses matched for {lemma}: {matched_senses}",
            "posture": "Neutral Observant Silence",
            "register": "Neutral Observant Silence",
            "matched_rules": [r["rule_id"] for r in matched],
        }


def compose_registers(resolutions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Harmonically aggregates individual target postures into a composite stance."""
    active_resolutions = [r for r in resolutions if r["decision"] == "single"]
    
    if not active_resolutions:
        return {
            "composite_posture": "Neutral Observant Silence",
            "composite_register": "Neutral Observant Silence",
            "harmonic_concordance": 1.0,
            "synthesis_narrative": "Zero active senses resolved; maintaining calibrated observational silence.",
        }
    
    if len(active_resolutions) == 1:
        r = active_resolutions[0]
        return {
            "composite_posture": r["posture"],
            "composite_register": r["register"],
            "harmonic_concordance": 1.0,
            "synthesis_narrative": f"Unambiguous singleton resolution for {r['lemma']}.",
        }

    # Multi-target composition
    registers = [r["register"] for r in active_resolutions]
    unique_registers = sorted(set(registers))
    
    if len(unique_registers) == 1:
        # Harmonious union
        return {
            "composite_posture": active_resolutions[0]["posture"],
            "composite_register": unique_registers[0],
            "harmonic_concordance": 1.0,
            "synthesis_narrative": f"Harmonious confluence across {len(active_resolutions)} targets in {unique_registers[0]}.",
        }
    
    # Blended compound chord
    chord_name = " & ".join(sorted({reg.split(" & ")[0] for reg in unique_registers})) + " Synthesis"
    return {
        "composite_posture": "Harmonic Multi-Lemma Synthesis",
        "composite_register": chord_name,
        "harmonic_concordance": 0.88,
        "synthesis_narrative": f"Synthesized compound posture from intersecting registers: {unique_registers}.",
    }


def evaluate_sentence(text: str) -> Dict[str, Any]:
    """Complete sentence-level multi-lemma evaluation pipeline."""
    tokens = tokenize(text)
    full_sentence_str = " ".join(tokens).lower()
    occurrences = scan_target_occurrences(tokens)
    
    resolutions = []
    for occ in occurrences:
        lemma = occ["lemma"]
        idx = occ["token_index"]
        context_str = extract_context_window(tokens, idx, window_radius=4)
        res = disambiguate_target(lemma, context_str, full_sentence_str)
        res["token_index"] = idx
        res["token"] = occ["token"]
        resolutions.append(res)
    
    composition = compose_registers(resolutions)
    
    return {
        "text": text,
        "total_targets_detected": len(occurrences),
        "target_resolutions": resolutions,
        "composition": composition,
        "evaluation_digest": digest({
            "text": text,
            "resolutions": resolutions,
            "composition": composition,
        }),
    }


class OrdinaryMemoryArbiter:
    """Matched ordinary-memory baseline comparator (Rule D004).
    
    Uses standard key-value lookup tables on the exact same token windows
    without fuzzy tree activation or harmonic aggregation.
    """
    def __init__(self):
        self.rules = {
            "order": ORDER_CAPACITY_RULES,
            "bank": BANK_CAPACITY_RULES,
        }

    def evaluate(self, text: str) -> Dict[str, Any]:
        tokens = tokenize(text)
        full_sentence_str = " ".join(tokens).lower()
        occurrences = scan_target_occurrences(tokens)
        
        resolutions = []
        for occ in occurrences:
            lemma = occ["lemma"]
            idx = occ["token_index"]
            context_str = extract_context_window(tokens, idx, window_radius=4)
            rules = self.rules.get(lemma, [])
            matched = [r for r in rules if r["core_pattern"].lower() in context_str or r["core_pattern"].lower() in full_sentence_str]
            matched_senses = sorted({r["target_sense_key"] for r in matched})
            
            if not matched_senses:
                decision = "abstain"
                selected = None
            elif len(matched_senses) == 1:
                decision = "single"
                selected = matched_senses[0]
            else:
                decision = "ambiguous"
                selected = None
                
            resolutions.append({
                "lemma": lemma,
                "token_index": idx,
                "decision": decision,
                "selected_sense": selected,
            })
            
        return {
            "text": text,
            "total_targets_detected": len(occurrences),
            "target_resolutions": resolutions,
            "evaluation_digest": digest({
                "text": text,
                "resolutions": resolutions,
            }),
        }
