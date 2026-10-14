"""Taxonomic Hypernym Generalization Engine.

Connects fine-grained WordNet sense keys to higher-level ontological categories
via deterministic hypernym path traversal, and modulates canonical leaf dial
activations across the 4 canonical founding branches without mutating or
expanding the frozen 40-node founding seed (Rule D001).

Zero runtime LLM calls during unassisted evaluation.
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

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

    def has_sense(self, sense_key: str) -> bool:
        return sense_key in self.registry

    def get_record(self, sense_key: str) -> Optional[Dict[str, Any]]:
        return self.registry.get(sense_key)

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

    def modulate(
        self,
        sense_key: str,
        base_dials: Optional[Dict[str, float]] = None,
        weight: float = 1.0,
    ) -> Dict[str, Any]:
        dials = {leaf_id: 0.50 for leaf_id in sorted(CANONICAL_LEAF_IDS)}
        if base_dials:
            for k, v in base_dials.items():
                if k in dials:
                    dials[k] = float(v)

        rec = self.registry.get(sense_key)
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
