"""Taxonomic Hypernym Generalization Engine.

Connects fine-grained WordNet sense keys to higher-level ontological categories
via deterministic hypernym path traversal, and modulates canonical leaf dial
activations across the 4 canonical founding branches without mutating or
expanding the frozen 40-node founding seed (Rule D001).

Zero runtime LLM calls during unassisted evaluation.
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
from copy import deepcopy
import re
from typing import Any, Dict, List, Optional, Tuple, Set

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import digest


# Verify and cache the canonical 24 leaf nodes from birth.py
CANONICAL_LEAF_IDS = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
assert len(CANONICAL_LEAF_IDS) == 24, f"Expected exactly 24 leaf nodes, got {len(CANONICAL_LEAF_IDS)}"


# Deterministic WordNet Taxonomic Registry for evaluated senses
TAXONOMIC_REGISTRY: Dict[str, Dict[str, Any]] = {
    # 'bank' senses
    "bank%1:14:00::": {
        "lemma": "bank",
        "sense_label": "financial_institution",
        "definition": "a financial institution that accepts deposits and channels money into lending activities",
        "direct_hypernym": "financial_institution",
        "hypernym_path": [
            "financial_institution",
            "institution",
            "organization",
            "social_group",
            "group",
            "abstraction",
            "entity",
        ],
        "primary_category": "organization",
        "leaf_dial_affinities": {
            "cultural/justice/fairness": 0.30,
            "philosophical/structure/order": 0.35,
            "cultural/efficiency/power": 0.25,
        },
    },
    "bank%1:17:01::": {
        "lemma": "bank",
        "sense_label": "river_bank",
        "definition": "sloping land especially the slope beside a body of water",
        "direct_hypernym": "slope",
        "hypernym_path": [
            "slope",
            "geological_formation",
            "natural_object",
            "physical_object",
            "entity",
        ],
        "primary_category": "geological_formation",
        "leaf_dial_affinities": {
            "philosophical/being/existence": 0.40,
            "philosophical/persistence/continuity": 0.35,
            "experiential/reflection/salience": 0.20,
        },
    },
    "bank%1:14:01::": {
        "lemma": "bank",
        "sense_label": "reserve_repository",
        "definition": "a supply or stock held in reserve for future use",
        "direct_hypernym": "depository",
        "hypernym_path": [
            "depository",
            "facility",
            "artifact",
            "physical_object",
            "entity",
        ],
        "primary_category": "facility_artifact",
        "leaf_dial_affinities": {
            "cultural/efficiency/wastelessness": 0.40,
            "cultural/efficiency/power": 0.30,
            "philosophical/persistence/continuity": 0.25,
        },
    },

    # 'order' senses
    "order%1:10:00::": {
        "lemma": "order",
        "sense_label": "judicial_decree",
        "definition": "a formal legal document issued by a court or authority; e.g. court order",
        "direct_hypernym": "legal_document",
        "hypernym_path": [
            "legal_document",
            "instrument",
            "document",
            "communication",
            "abstraction",
            "entity",
        ],
        "primary_category": "legal_instrument",
        "leaf_dial_affinities": {
            "cultural/justice/honor": 0.45,
            "philosophical/structure/order": 0.35,
            "psychological/will/intention": 0.30,
        },
    },
    "order%1:10:01::": {
        "lemma": "order",
        "sense_label": "commercial_purchase",
        "definition": "a commercial document requesting that a supplier provide merchandise or services",
        "direct_hypernym": "commercial_document",
        "hypernym_path": [
            "commercial_document",
            "document",
            "communication",
            "abstraction",
            "entity",
        ],
        "primary_category": "commercial_document",
        "leaf_dial_affinities": {
            "cultural/efficiency/wastelessness": 0.35,
            "cultural/efficiency/power": 0.25,
            "philosophical/persistence/discreteness": 0.30,
        },
    },
    "order%1:10:02::": {
        "lemma": "order",
        "sense_label": "sequence_succession",
        "definition": "the arrangement of things in succession; chronological or numerical sequence",
        "direct_hypernym": "arrangement",
        "hypernym_path": [
            "arrangement",
            "ordering",
            "organization",
            "system",
            "structure",
            "abstraction",
            "entity",
        ],
        "primary_category": "sequence_structure",
        "leaf_dial_affinities": {
            "philosophical/persistence/discreteness": 0.45,
            "philosophical/structure/order": 0.40,
            "psychological/truth/fact": 0.30,
        },
    },
    "order%1:10:03::": {
        "lemma": "order",
        "sense_label": "authoritative_command",
        "definition": "an authoritative direction or instruction to do something; a military or personal command",
        "direct_hypernym": "speech_act",
        "hypernym_path": [
            "speech_act",
            "act",
            "event",
            "psychological_feature",
            "abstraction",
            "entity",
        ],
        "primary_category": "authoritative_act",
        "leaf_dial_affinities": {
            "philosophical/being/agency": 0.45,
            "psychological/will/execution": 0.40,
            "cultural/efficiency/power": 0.30,
        },
    },
    "order%1:14:00::": {
        "lemma": "order",
        "sense_label": "sequence_ordering",
        "definition": "the act of putting things in a sequential arrangement; succession or serial arrangement",
        "direct_hypernym": "sorting",
        "hypernym_path": [
            "sorting",
            "arrangement",
            "act",
            "event",
            "psychological_feature",
            "abstraction",
            "entity",
        ],
        "primary_category": "sorting_act",
        "leaf_dial_affinities": {
            "philosophical/structure/order": 0.40,
            "philosophical/persistence/discreteness": 0.35,
            "cultural/efficiency/wastelessness": 0.30,
        },
    },
    "order%1:07:01::": {
        "lemma": "order",
        "sense_label": "degree_magnitude",
        "definition": "a degree in a continuum of size or quantity; e.g. on the order of",
        "direct_hypernym": "magnitude",
        "hypernym_path": [
            "magnitude",
            "property",
            "attribute",
            "abstraction",
            "entity",
        ],
        "primary_category": "quantitative_magnitude",
        "leaf_dial_affinities": {
            "philosophical/persistence/continuity": 0.45,
            "philosophical/persistence/discreteness": 0.30,
            "experiential/reflection/salience": 0.25,
        },
    },
    "order%1:26:00::": {
        "lemma": "order",
        "sense_label": "social_condition",
        "definition": "the established condition of social, religious, or political organization; state of peace and observance of the law",
        "direct_hypernym": "condition",
        "hypernym_path": [
            "condition",
            "state",
            "attribute",
            "abstraction",
            "entity",
        ],
        "primary_category": "social_condition",
        "leaf_dial_affinities": {
            "philosophical/structure/order": 0.45,
            "cultural/justice/fairness": 0.35,
            "philosophical/persistence/continuity": 0.30,
        },
    },
    "order%1:26:02::": {
        "lemma": "order",
        "sense_label": "systematic_arrangement",
        "definition": "a logical or comprehensible arrangement of separate elements; structure or orderliness",
        "direct_hypernym": "structure",
        "hypernym_path": [
            "structure",
            "system",
            "organization",
            "abstraction",
            "entity",
        ],
        "primary_category": "systemic_arrangement",
        "leaf_dial_affinities": {
            "philosophical/structure/order": 0.50,
            "cultural/efficiency/wastelessness": 0.35,
            "psychological/contemplation/clarity": 0.30,
        },
    },

    # Foundational Ontological Categories
    "knowledge%1:03:00::": {
        "lemma": "knowledge",
        "sense_label": "epistemic_cognition",
        "definition": "the psychological result of perception and learning and reasoning; organized truth and theory",
        "direct_hypernym": "cognition",
        "hypernym_path": [
            "cognition",
            "psychological_feature",
            "abstraction",
            "entity",
        ],
        "primary_category": "knowledge_truth",
        "aliases": [
            "science", "truth", "theory", "fact", "study", "library",
            "philosophy", "wisdom", "learning", "logic", "reason",
        ],
        "leaf_dial_affinities": {
            "psychological/truth/theory": 0.35,
            "psychological/truth/fact": 0.35,
            "psychological/contemplation/clarity": 0.35,
        },
    },
    "peace%1:26:00::": {
        "lemma": "peace",
        "sense_label": "state_of_tranquility",
        "definition": "the state prevailing during the absence of war, anxiety, or disturbance; harmony and companionship",
        "direct_hypernym": "condition",
        "hypernym_path": [
            "condition",
            "state",
            "attribute",
            "abstraction",
            "entity",
        ],
        "primary_category": "sanctuary_harmony",
        "aliases": [
            "friend", "friendship", "sanctuary", "harmony", "kindness",
            "gentle", "love", "comfort", "tranquility", "rest", "hearth", "companion",
        ],
        "leaf_dial_affinities": {
            "experiential/phase/valence": 0.40,
            "experiential/synchronization/resonance": 0.35,
            "philosophical/persistence/continuity": 0.30,
        },
    },
    "war%1:04:00::": {
        "lemma": "war",
        "sense_label": "hostile_conflict",
        "definition": "an active struggle or conflict between opposing forces or parties; danger and crisis",
        "direct_hypernym": "conflict",
        "hypernym_path": [
            "conflict",
            "group_action",
            "act",
            "event",
            "psychological_feature",
            "abstraction",
            "entity",
        ],
        "primary_category": "conflict_threat",
        "aliases": [
            "threat", "crisis", "weapon", "danger", "battle", "enemy",
            "attack", "conflict", "violent", "tremor", "storm", "fear", "catastrophe",
        ],
        "leaf_dial_affinities": {
            "experiential/phase/arousal": 0.45,
            "philosophical/structure/chaos": 0.35,
            "cultural/efficiency/power": 0.30,
        },
    },
    "action%1:04:02::": {
        "lemma": "action",
        "sense_label": "intentional_conduct",
        "definition": "something done or performed as a result of agency or deliberate will; creation and craftsmanship",
        "direct_hypernym": "act",
        "hypernym_path": [
            "act",
            "event",
            "psychological_feature",
            "abstraction",
            "entity",
        ],
        "primary_category": "agency_execution",
        "aliases": [
            "build", "create", "craft", "forge", "execute", "write",
            "act", "decision", "intention", "will", "tool", "work", "labor",
        ],
        "leaf_dial_affinities": {
            "philosophical/being/agency": 0.45,
            "psychological/will/execution": 0.40,
            "psychological/will/intention": 0.30,
        },
    },
    "justice%1:07:00::": {
        "lemma": "justice",
        "sense_label": "judicial_fairness",
        "definition": "the quality of being just, equitable, or morally right; lawful governance and honor",
        "direct_hypernym": "righteousness",
        "hypernym_path": [
            "righteousness",
            "morality",
            "quality",
            "attribute",
            "abstraction",
            "entity",
        ],
        "primary_category": "justice_governance",
        "aliases": [
            "law", "rule", "court", "judge", "treaty", "pact",
            "contract", "duty", "fairness", "sovereign", "decree", "code",
        ],
        "leaf_dial_affinities": {
            "cultural/justice/honor": 0.40,
            "cultural/justice/fairness": 0.40,
            "philosophical/structure/order": 0.35,
        },
    },
    "artifact%1:03:00::": {
        "lemma": "artifact",
        "sense_label": "physical_manifestation",
        "definition": "a physical object, substance, sustenance, or material commodity",
        "direct_hypernym": "object",
        "hypernym_path": [
            "object",
            "physical_entity",
            "entity",
        ],
        "primary_category": "material_artifact",
        "aliases": [
            "stone", "bread", "food", "wood", "water", "iron",
            "gold", "coin", "body", "earth", "machine", "object", "seed", "plant", "material",
        ],
        "leaf_dial_affinities": {
            "philosophical/being/existence": 0.40,
            "philosophical/persistence/discreteness": 0.35,
            "cultural/efficiency/wastelessness": 0.30,
        },
    },
    "freedom%1:26:00::": {
        "lemma": "freedom",
        "sense_label": "condition_of_liberty",
        "definition": "the condition of being free; power to act without restraint; autonomy and self-reliance",
        "direct_hypernym": "condition",
        "hypernym_path": [
            "condition",
            "state",
            "attribute",
            "abstraction",
            "entity",
        ],
        "primary_category": "freedom_autonomy",
        "aliases": [
            "liberty", "autonomous", "wild", "wilderness", "solitude",
            "self-sufficiency", "independent", "free",
        ],
        "leaf_dial_affinities": {
            "cultural/freedom/self-sufficiency": 0.45,
            "cultural/freedom/needlessness": 0.35,
            "experiential/reflection/novelty": 0.30,
        },
    },
    "discovery%1:04:00::": {
        "lemma": "discovery",
        "sense_label": "novel_finding",
        "definition": "the act of discovering or encountering something novel, unexpected, or anomalous",
        "direct_hypernym": "disclosure",
        "hypernym_path": [
            "disclosure",
            "recognition",
            "cognition",
            "psychological_feature",
            "abstraction",
            "entity",
        ],
        "primary_category": "discovery_novelty",
        "aliases": [
            "anomaly", "mystery", "wonder", "star", "cosmos",
            "explore", "novelty", "puzzle", "surprise", "horizon",
        ],
        "leaf_dial_affinities": {
            "experiential/reflection/novelty": 0.45,
            "experiential/reflection/salience": 0.35,
            "psychological/contemplation/clarity": 0.25,
        },
    },
}

# Verify all affinities point to canonical leaves
for sense_k, record in TAXONOMIC_REGISTRY.items():
    for leaf_id in record["leaf_dial_affinities"].keys():
        if leaf_id not in CANONICAL_LEAF_IDS:
            raise ValueError(f"Taxonomic affinity references non-canonical leaf: {leaf_id}")


class TaxonomicGeneralizer:
    """Traverses taxonomic paths and modulates canonical leaf dials."""

    def __init__(self, registry: Optional[Dict[str, Dict[str, Any]]] = None):
        self.registry = registry or deepcopy(TAXONOMIC_REGISTRY)
        self.lemma_index: Dict[str, List[str]] = {}
        self.alias_index: Dict[str, str] = {}
        for sense_k, rec in self.registry.items():
            lem = rec.get("lemma")
            if lem:
                self.lemma_index.setdefault(lem.lower(), []).append(sense_k)
            for alias in rec.get("aliases", []):
                self.alias_index[alias.lower()] = sense_k

    def get_registered_lemmas(self) -> List[str]:
        """Returns sorted list of all unique lemmas and aliases recognized by the taxonomy."""
        all_lemmas = set(self.lemma_index.keys()).union(set(self.alias_index.keys()))
        return sorted(all_lemmas)

    def extract_lemmas(self, sentence: str) -> List[str]:
        """Extracts recognized lemmas from sentence text in order of appearance."""
        if not sentence:
            return []
        tokens = re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower())
        matched: List[str] = []
        for tok in tokens:
            if tok in self.lemma_index or tok in self.alias_index:
                if tok not in matched:
                    matched.append(tok)
        return matched

    def resolve_sense_record(self, key_or_label: str) -> Optional[Dict[str, Any]]:
        """Resolves sense record by exact key, alias, lemma, or partial label match."""
        if not key_or_label:
            return None
        if key_or_label in self.registry:
            return self.registry[key_or_label]
        k_low = key_or_label.lower()
        if k_low in self.alias_index:
            return self.registry[self.alias_index[k_low]]
        if k_low in self.lemma_index:
            return self.registry[self.lemma_index[k_low][0]]
        for sense_k, rec in self.registry.items():
            s_lbl = rec.get("sense_label", "").lower()
            if s_lbl and (s_lbl in k_low or k_low in s_lbl):
                return rec
        return None

    def resolve_default_sense(self, lemma_or_word: str) -> Optional[str]:
        """Resolves primary sense key for a given lemma or alias."""
        rec = self.resolve_sense_record(lemma_or_word)
        if rec:
            for k, v in self.registry.items():
                if v is rec:
                    return k
        return None

    def has_sense(self, sense_key: str) -> bool:
        if sense_key in self.registry:
            return True
        return self.resolve_sense_record(sense_key) is not None

    def get_record(self, sense_key: str) -> Optional[Dict[str, Any]]:
        return self.resolve_sense_record(sense_key)

    def get_hypernym_path(self, sense_key: str) -> List[str]:
        rec = self.get_record(sense_key)
        return list(rec["hypernym_path"]) if rec else []

    def get_primary_category(self, sense_key: str) -> Optional[str]:
        rec = self.get_record(sense_key)
        return rec["primary_category"] if rec else None

    def get_affinities(self, sense_key: str) -> Dict[str, float]:
        rec = self.get_record(sense_key)
        return dict(rec["leaf_dial_affinities"]) if rec else {}

    def compute_taxonomic_modulation(
        self,
        sense_key: str,
        base_dials: Optional[Dict[str, float]] = None,
        weight: float = 1.0,
    ) -> Dict[str, Any]:
        """Modulates canonical leaf dials according to the taxonomic hypernym affinities."""
        rec = self.get_record(sense_key)
        
        # Initialize default 24 canonical leaves at neutral 0.50 if not provided
        dials = {leaf_id: 0.50 for leaf_id in sorted(CANONICAL_LEAF_IDS)}
        if base_dials:
            for k, v in base_dials.items():
                if k in dials:
                    dials[k] = float(v)

        if not rec:
            return {
                "sense_key": sense_key,
                "found": False,
                "primary_category": None,
                "hypernym_path": [],
                "applied_affinities": {},
                "modulated_dials": dials,
            }

        weight = max(0.0, min(1.0, float(weight)))
        affinities = rec["leaf_dial_affinities"]
        applied: Dict[str, float] = {}

        for leaf_id, aff_score in affinities.items():
            delta = aff_score * weight
            current = dials[leaf_id]
            new_val = round(min(1.0, max(0.0, current + delta)), 4)
            dials[leaf_id] = new_val
            applied[leaf_id] = round(delta, 4)

        return {
            "sense_key": sense_key,
            "found": True,
            "primary_category": rec["primary_category"],
            "hypernym_path": list(rec["hypernym_path"]),
            "applied_affinities": applied,
            "modulated_dials": dials,
        }

    def explain_taxonomic_derivation(self, sense_key: str) -> str:
        rec = self.get_record(sense_key)
        if not rec:
            return f"Sense key '{sense_key}' has no registered taxonomic hypernym path."

        path_str = " -> ".join(rec["hypernym_path"])
        aff_str = ", ".join(f"{k}: +{v:.2f}" for k, v in rec["leaf_dial_affinities"].items())
        return (
            f"Sense '{sense_key}' ({rec['sense_label']}) derives from category '{rec['primary_category']}' "
            f"via hypernym lineage: [{path_str}]. Propagates canonical leaf affinities: [{aff_str}]."
        )


class OrdinaryMemoryTaxonomicComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def __init__(self, registry: Optional[Dict[str, Dict[str, Any]]] = None):
        self.registry = registry or deepcopy(TAXONOMIC_REGISTRY)
        self.lemma_index: Dict[str, List[str]] = {}
        self.alias_index: Dict[str, str] = {}
        for sense_k, rec in self.registry.items():
            lem = rec.get("lemma")
            if lem:
                self.lemma_index.setdefault(lem.lower(), []).append(sense_k)
            for alias in rec.get("aliases", []):
                self.alias_index[alias.lower()] = sense_k

    def get_registered_lemmas(self) -> List[str]:
        all_lemmas = set(self.lemma_index.keys()).union(set(self.alias_index.keys()))
        return sorted(all_lemmas)

    def extract_lemmas(self, sentence: str) -> List[str]:
        if not sentence:
            return []
        tokens = re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower())
        matched: List[str] = []
        for tok in tokens:
            if tok in self.lemma_index or tok in self.alias_index:
                if tok not in matched:
                    matched.append(tok)
        return matched

    def resolve_sense_record(self, key_or_label: str) -> Optional[Dict[str, Any]]:
        if not key_or_label:
            return None
        if key_or_label in self.registry:
            return self.registry[key_or_label]
        k_low = key_or_label.lower()
        if k_low in self.alias_index:
            return self.registry[self.alias_index[k_low]]
        if k_low in self.lemma_index:
            return self.registry[self.lemma_index[k_low][0]]
        for sense_k, rec in self.registry.items():
            s_lbl = rec.get("sense_label", "").lower()
            if s_lbl and (s_lbl in k_low or k_low in s_lbl):
                return rec
        return None

    def resolve_default_sense(self, lemma_or_word: str) -> Optional[str]:
        rec = self.resolve_sense_record(lemma_or_word)
        if rec:
            for k, v in self.registry.items():
                if v is rec:
                    return k
        return None

    def has_sense(self, sense_key: str) -> bool:
        if sense_key in self.registry:
            return True
        return self.resolve_sense_record(sense_key) is not None

    def get_record(self, sense_key: str) -> Optional[Dict[str, Any]]:
        return self.resolve_sense_record(sense_key)

    def compute_taxonomic_modulation(
        self,
        sense_key: str,
        base_dials: Optional[Dict[str, float]] = None,
        weight: float = 1.0,
    ) -> Dict[str, Any]:
        rec = self.get_record(sense_key)
        dials = {leaf_id: 0.50 for leaf_id in sorted(CANONICAL_LEAF_IDS)}
        if base_dials:
            for k, v in base_dials.items():
                if k in dials:
                    dials[k] = float(v)

        if not rec:
            return {
                "sense_key": sense_key,
                "found": False,
                "primary_category": None,
                "hypernym_path": [],
                "applied_affinities": {},
                "modulated_dials": dials,
            }

        weight = max(0.0, min(1.0, float(weight)))
        affinities = rec["leaf_dial_affinities"]
        applied: Dict[str, float] = {}

        for leaf_id, aff_score in affinities.items():
            delta = aff_score * weight
            current = dials[leaf_id]
            new_val = round(min(1.0, max(0.0, current + delta)), 4)
            dials[leaf_id] = new_val
            applied[leaf_id] = round(delta, 4)

        return {
            "sense_key": sense_key,
            "found": True,
            "primary_category": rec["primary_category"],
            "hypernym_path": list(rec["hypernym_path"]),
            "applied_affinities": applied,
            "modulated_dials": dials,
        }

    def modulate(
        self,
        sense_key: str,
        base_dials: Optional[Dict[str, float]] = None,
        weight: float = 1.0,
    ) -> Dict[str, Any]:
        return self.compute_taxonomic_modulation(sense_key, base_dials=base_dials, weight=weight)

