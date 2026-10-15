"""Unified Cognitive Heartbeat Engine.

Orchestrates the complete integrated cycle of the LMFT architecture:
1. Input Sentence & Target Lemma Extraction
2. Long-Term Capacity Rule Matching
3. Lateral Ethical-Ontological Coupling Matrix (D064)
4. Fuzzy Prerequisite Coherence Gate & Distortion Detection (D068)
5. Executive Speaking Register & Action Bid Determination (D050, D052)
6. Recurrent Post-Action Echo into Experiential Roots (D066)
7. Dynamic Affective Plasticity Regulation (D065)
8. Persistent Dispositional State Momentum Drift (D067)
9. Dual-Coded Episodic Saliency Journal Recording (D069)
10. Offline Dual-Speed Memory Consolidation Replay & Buffer Pruning (D070)

Preserves Rule D001 (frozen 40-node founding seed) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""
from copy import deepcopy
import re
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.affective_homeostasis import AffectiveHomeostasisGovernor
from lmft_lab.affective_plasticity import AffectivePlasticityEngine
from lmft_lab.anchor_deduplication import normalize_anchor_text
from lmft_lab.birth import _inventory, create_birth_state
from lmft_lab.dispositional_momentum import PersistentDispositionalVector, CANONICAL_LEAF_IDS
from lmft_lab.episodic_journal import EpisodicSaliencyJournal
from lmft_lab.judgment import newborn
from lmft_lab.lateral_coupling import LateralCouplingEngine
from lmft_lab.memory_consolidation import MemoryConsolidationEngine
from lmft_lab.prerequisite_gate import PrerequisiteCoherenceGate
from lmft_lab.recurrent_feedback import RecurrentFeedbackEngine
from lmft_lab.runtime_store import digest
from lmft_lab.taxonomic_generalization import (
    TaxonomicGeneralizer,
    OrdinaryMemoryTaxonomicComparator,
)
from lmft_lab.value_consonance import ValueConsonanceEngine


DEFAULT_INITIAL_RULES = [
    {
        "rule_id": "rule-bank-fin-01",
        "lemma": "bank",
        "target_sense_key": "depository_financial_institution (financial institution)",
        "core_pattern": "national bank",
        "gloss": "a financial institution that accepts deposits and channels money into lending",
        "weight": 0.60,
        "speaking_register": "Authoritative & Chivalrous",
        "action_bid": "Execute financial transaction",
        "witnesses": ["genesis-bank-01"],
    },
    {
        "rule_id": "rule-order-cmd-01",
        "lemma": "order",
        "target_sense_key": "order%1:10:00::",
        "core_pattern": "court order",
        "gloss": "an authoritative instruction or judicial decree",
        "weight": 0.60,
        "speaking_register": "Authoritative & Chivalrous",
        "action_bid": "Enforce sovereign decree",
        "witnesses": ["genesis-order-01"],
    },
]


class CognitiveHeartbeat:
    """Integrated cognitive heartbeat pipeline orchestrating all developmental faculties."""

    def __init__(
        self,
        individual_id: str = "lmft-individual-01",
        initial_rules: Optional[List[Dict[str, Any]]] = None,
        journal_capacity: int = 50,
        min_confirmations: int = 2,
    ):
        self.individual_id = individual_id
        self.cycle_count = 0

        rules = initial_rules if initial_rules is not None else deepcopy(DEFAULT_INITIAL_RULES)
        self.consolidator = MemoryConsolidationEngine(initial_rules=rules, min_confirmations=min_confirmations)
        self.journal = EpisodicSaliencyJournal(capacity=journal_capacity)
        self.disposition = PersistentDispositionalVector()
        self.lateral_coupling = LateralCouplingEngine()
        self.prerequisite_gate = PrerequisiteCoherenceGate()
        self.recurrent_feedback = RecurrentFeedbackEngine()
        self.plasticity_engine = AffectivePlasticityEngine()
        self.homeostasis_governor = AffectiveHomeostasisGovernor()
        self.consonance_engine = ValueConsonanceEngine()
        self.taxonomic_generalizer = TaxonomicGeneralizer()

    def interact(
        self,
        sentence: str,
        target_lemmas: Optional[List[str]] = None,
        forced_senses: Optional[Dict[str, str]] = None,
        custom_dials: Optional[Dict[str, float]] = None,
        is_conflict: bool = False,
    ) -> Dict[str, Any]:
        """Executes a single waking cognitive cycle over input text."""
        self.cycle_count += 1
        current_cycle = self.cycle_count

        # 1. Extract Target Lemmas & Resolve Senses via Capacity Rules & Taxonomy
        norm_sent = normalize_anchor_text(sentence)
        lemmas = list(target_lemmas) if target_lemmas is not None else []
        if not lemmas:
            for r in self.consolidator.long_term_rules.values():
                l = r.get("lemma")
                if l and (l in norm_sent or l in sentence.lower()) and l not in lemmas:
                    lemmas.append(l)
            for l in self.taxonomic_generalizer.extract_lemmas(sentence):
                if l not in lemmas:
                    lemmas.append(l)
            if not lemmas:
                for l in ["bank", "order"]:
                    if l in sentence.lower() and l not in lemmas:
                        lemmas.append(l)

        resolved_senses: Dict[str, str] = {}
        speaking_register = "Methodical & Pragmatic"
        action_bid = "Process statement"

        if forced_senses:
            resolved_senses = dict(forced_senses)
        else:
            for l in lemmas:
                matched_rule = None
                for r in self.consolidator.long_term_rules.values():
                    if r.get("lemma") == l:
                        pat = normalize_anchor_text(r.get("core_pattern", ""))
                        if pat in norm_sent or pat in sentence.lower():
                            matched_rule = r
                            break
                if matched_rule:
                    resolved_senses[l] = matched_rule["target_sense_key"]
                    speaking_register = matched_rule.get("speaking_register", speaking_register)
                    action_bid = matched_rule.get("action_bid", action_bid)
                else:
                    tax_sense = self.taxonomic_generalizer.resolve_default_sense(l)
                    if tax_sense:
                        resolved_senses[l] = tax_sense
                    else:
                        resolved_senses[l] = "unanchored_general_sense"

        # 2. Formulate Candidate Dials
        candidate_dials = deepcopy(self.disposition.dials)

        if forced_senses or any(v != "unanchored_general_sense" for v in resolved_senses.values()):
            candidate_dials["experiential/reflection/salience"] = 0.78
            candidate_dials["psychological/contemplation/clarity"] = 0.85
            candidate_dials["philosophical/structure/order"] = 0.75

        # Apply taxonomic hypernym modulation for resolved senses
        taxonomic_modulations = []
        for l, sense_k in resolved_senses.items():
            if sense_k != "unanchored_general_sense" and self.taxonomic_generalizer.has_sense(sense_k):
                mod = self.taxonomic_generalizer.compute_taxonomic_modulation(
                    sense_key=sense_k,
                    base_dials=candidate_dials,
                    weight=0.35,
                )
                candidate_dials = mod["modulated_dials"]
                taxonomic_modulations.append(mod)

        if is_conflict:
            candidate_dials["psychological/contemplation/clarity"] = 0.20
            candidate_dials["experiential/phase/arousal"] = 0.80
            candidate_dials["experiential/reflection/salience"] = 0.75
            speaking_register = "Methodical & Pragmatic"
            action_bid = "Halt and issue clarification request"

        if custom_dials:
            for k, v in custom_dials.items():
                if k in candidate_dials:
                    candidate_dials[k] = round(max(0.0, min(1.0, float(v))), 4)

        # 3. Lateral Ethical-Ontological Coupling
        cult_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("cultural/")}
        phil_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("philosophical/")}
        coupling_result = self.lateral_coupling.couple(cult_dials, phil_dials)
        for k, v in coupling_result["coupled_cultural"].items():
            candidate_dials[k] = v
        for k, v in coupling_result["coupled_philosophical"].items():
            candidate_dials[k] = v

        # 4. Prerequisite Coherence Gate & Distortion Detection
        coherence_result = self.prerequisite_gate.evaluate_coherence(candidate_dials)

        # 5. Epistemic Curiosity & Value Consonance Engine
        consonance_result = self.consonance_engine.evaluate(
            candidate_dials=candidate_dials,
            is_conflict=is_conflict,
            distortions_count=len(coherence_result["distortions_detected"]),
        )
        candidate_dials = consonance_result["harmonized_dials"]
        if consonance_result["is_curious"] and action_bid == "Process statement":
            speaking_register = consonance_result["recommended_register"]
            action_bid = consonance_result["inquiry_posture"]

        # 6. Recurrent Post-Action Echo
        exp_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("experiential/")}
        psy_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("psychological/")}
        echo_result = self.recurrent_feedback.compute_echo(
            experiential_dials=exp_dials,
            psychological_state=psy_dials,
            action_posture=action_bid,
        )
        for k, v in echo_result["echoed_experiential"].items():
            candidate_dials[k] = v

        # 7. Affective Homeostasis Governor & Volatility Dampening
        homeostasis_result = self.homeostasis_governor.stabilize(
            candidate_dials=candidate_dials,
            previous_dials=self.disposition.dials,
        )
        candidate_dials = homeostasis_result["stabilized_dials"]

        # 8. Dynamic Affective Plasticity Regulation
        exp_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("experiential/")}
        psy_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("psychological/")}
        plasticity_result = self.plasticity_engine.compute_dynamic_rates(
            experiential_dials=exp_dials,
            psychological_dials=psy_dials,
        )
        effective_alpha = plasticity_result["dynamic_alpha"]

        # 9. Persistent Dispositional Momentum Update
        momentum_result = self.disposition.incorporate_situational_stimulus(
            situational_dials=candidate_dials,
            gamma_override=effective_alpha,
        )

        # 10. Dual-Coded Episodic Journal Recording
        journal_res = self.journal.record_episode(
            cycle=current_cycle,
            sentence=sentence,
            target_lemmas=lemmas,
            resolved_senses=resolved_senses,
            leaf_dials=candidate_dials,
            speaking_register=speaking_register,
            action_bid=action_bid,
            post_action_echo=echo_result["echo_deltas"],
            is_conflict=is_conflict,
        )

        return {
            "cycle": current_cycle,
            "sentence": sentence,
            "target_lemmas": lemmas,
            "resolved_senses": resolved_senses,
            "speaking_register": speaking_register,
            "action_bid": action_bid,
            "coherence": coherence_result,
            "consonance": consonance_result,
            "homeostasis": homeostasis_result,
            "plasticity": plasticity_result,
            "momentum": momentum_result,
            "post_action_echo": echo_result["echo_deltas"],
            "journal_result": journal_res,
            "disposition_dials": deepcopy(self.disposition.dials),
            "taxonomic_modulations": taxonomic_modulations,
        }

    def sleep(self, prune_buffer: bool = True) -> Dict[str, Any]:
        """Executes offline memory consolidation and equilibrium drift ('sleep')."""
        summary, remaining = self.consolidator.consolidate_sleep_cycle(
            episodic_buffer=list(self.journal.entries),
            prune_buffer=prune_buffer,
        )
        if prune_buffer:
            self.journal.entries.clear()
            for ep in remaining:
                self.journal.entries.append(ep)

        # Gentle equilibrium relaxation during rest
        drift_res = self.disposition.apply_idle_equilibrium_drift(steps=1)

        return {
            "consolidation_summary": summary,
            "remaining_journal_episodes": len(self.journal.entries),
            "drift_result": drift_res,
            "active_long_term_rules": len(self.consolidator.long_term_rules),
            "sleep_cycle": summary["sleep_cycle"],
        }

    def export_individual_package(self) -> Dict[str, Any]:
        """Packages complete developmental state into portable dictionary."""
        birth_state = create_birth_state(self.individual_id, birth_event_id=f"birth-{self.individual_id}", random_seed=42)
        birth_dict = {
            "individual_id": birth_state.individual_id,
            "birth_event_id": birth_state.birth_event_id,
            "seed_version": birth_state.seed_version,
            "initialization_version": birth_state.initialization_version,
        }
        return {
            "individual_id": self.individual_id,
            "cycle": self.cycle_count,
            "birth": birth_dict,
            "judgment": newborn(),
            "capacity": {"rules": list(self.consolidator.long_term_rules.values())},
            "disposition": self.disposition.export_state(),
            "episodic_journal": self.journal.export_journal(),
            "memory_consolidation": self.consolidator.export_state(),
        }

    def import_individual_package(self, package: Dict[str, Any]) -> None:
        """Restores complete developmental state from package dictionary."""
        self.individual_id = package.get("individual_id", self.individual_id)
        self.cycle_count = int(package.get("cycle", 0))

        if "disposition" in package and package["disposition"]:
            self.disposition.import_state(package["disposition"])

        if "episodic_journal" in package and package["episodic_journal"]:
            self.journal.import_journal(package["episodic_journal"])

        if "memory_consolidation" in package and package["memory_consolidation"]:
            self.consolidator.import_state(package["memory_consolidation"])


class OrdinaryMemoryHeartbeatComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def __init__(
        self,
        individual_id: str = "lmft-individual-01",
        initial_rules: Optional[List[Dict[str, Any]]] = None,
        journal_capacity: int = 50,
        min_confirmations: int = 2,
    ):
        self.individual_id = individual_id
        self.cycle_count = 0

        rules = initial_rules if initial_rules is not None else deepcopy(DEFAULT_INITIAL_RULES)
        self.consolidator = MemoryConsolidationEngine(initial_rules=rules, min_confirmations=min_confirmations)
        self.journal = EpisodicSaliencyJournal(capacity=journal_capacity)
        self.disposition = PersistentDispositionalVector()
        self.lateral_coupling = LateralCouplingEngine()
        self.prerequisite_gate = PrerequisiteCoherenceGate()
        self.recurrent_feedback = RecurrentFeedbackEngine()
        self.plasticity_engine = AffectivePlasticityEngine()
        self.homeostasis_governor = AffectiveHomeostasisGovernor()
        self.consonance_engine = ValueConsonanceEngine()
        self.taxonomic_generalizer = OrdinaryMemoryTaxonomicComparator()

    def interact(
        self,
        sentence: str,
        target_lemmas: Optional[List[str]] = None,
        forced_senses: Optional[Dict[str, str]] = None,
        custom_dials: Optional[Dict[str, float]] = None,
        is_conflict: bool = False,
    ) -> Dict[str, Any]:
        self.cycle_count += 1
        current_cycle = self.cycle_count

        norm_sent = normalize_anchor_text(sentence)
        lemmas = list(target_lemmas) if target_lemmas is not None else []
        if not lemmas:
            for r in self.consolidator.long_term_rules.values():
                l = r.get("lemma")
                if l and (l in norm_sent or l in sentence.lower()) and l not in lemmas:
                    lemmas.append(l)
            for l in self.taxonomic_generalizer.extract_lemmas(sentence):
                if l not in lemmas:
                    lemmas.append(l)
            if not lemmas:
                for l in ["bank", "order"]:
                    if l in sentence.lower() and l not in lemmas:
                        lemmas.append(l)

        resolved_senses: Dict[str, str] = {}
        speaking_register = "Methodical & Pragmatic"
        action_bid = "Process statement"

        if forced_senses:
            resolved_senses = dict(forced_senses)
        else:
            for l in lemmas:
                matched_rule = None
                for r in self.consolidator.long_term_rules.values():
                    if r.get("lemma") == l:
                        pat = normalize_anchor_text(r.get("core_pattern", ""))
                        if pat in norm_sent or pat in sentence.lower():
                            matched_rule = r
                            break
                if matched_rule:
                    resolved_senses[l] = matched_rule["target_sense_key"]
                    speaking_register = matched_rule.get("speaking_register", speaking_register)
                    action_bid = matched_rule.get("action_bid", action_bid)
                else:
                    tax_sense = self.taxonomic_generalizer.resolve_default_sense(l)
                    if tax_sense:
                        resolved_senses[l] = tax_sense
                    else:
                        resolved_senses[l] = "unanchored_general_sense"

        candidate_dials = deepcopy(self.disposition.dials)

        if forced_senses or any(v != "unanchored_general_sense" for v in resolved_senses.values()):
            candidate_dials["experiential/reflection/salience"] = 0.78
            candidate_dials["psychological/contemplation/clarity"] = 0.85
            candidate_dials["philosophical/structure/order"] = 0.75

        taxonomic_modulations = []
        for l, sense_k in resolved_senses.items():
            if sense_k != "unanchored_general_sense" and self.taxonomic_generalizer.has_sense(sense_k):
                mod = self.taxonomic_generalizer.compute_taxonomic_modulation(
                    sense_key=sense_k,
                    base_dials=candidate_dials,
                    weight=0.35,
                )
                candidate_dials = mod["modulated_dials"]
                taxonomic_modulations.append(mod)

        if is_conflict:
            candidate_dials["psychological/contemplation/clarity"] = 0.20
            candidate_dials["experiential/phase/arousal"] = 0.80
            candidate_dials["experiential/reflection/salience"] = 0.75
            speaking_register = "Methodical & Pragmatic"
            action_bid = "Halt and issue clarification request"

        if custom_dials:
            for k, v in custom_dials.items():
                if k in candidate_dials:
                    candidate_dials[k] = round(max(0.0, min(1.0, float(v))), 4)

        cult_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("cultural/")}
        phil_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("philosophical/")}
        coupling_result = self.lateral_coupling.couple(cult_dials, phil_dials)
        for k, v in coupling_result["coupled_cultural"].items():
            candidate_dials[k] = v
        for k, v in coupling_result["coupled_philosophical"].items():
            candidate_dials[k] = v

        coherence_result = self.prerequisite_gate.evaluate_coherence(candidate_dials)

        consonance_result = self.consonance_engine.evaluate(
            candidate_dials=candidate_dials,
            is_conflict=is_conflict,
            distortions_count=len(coherence_result["distortions_detected"]),
        )
        candidate_dials = consonance_result["harmonized_dials"]
        if consonance_result["is_curious"] and action_bid == "Process statement":
            speaking_register = consonance_result["recommended_register"]
            action_bid = consonance_result["inquiry_posture"]

        exp_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("experiential/")}
        psy_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("psychological/")}
        echo_result = self.recurrent_feedback.compute_echo(
            experiential_dials=exp_dials,
            psychological_state=psy_dials,
            action_posture=action_bid,
        )
        for k, v in echo_result["echoed_experiential"].items():
            candidate_dials[k] = v

        # Affective Homeostasis Governor & Volatility Dampening
        homeostasis_result = self.homeostasis_governor.stabilize(
            candidate_dials=candidate_dials,
            previous_dials=self.disposition.dials,
        )
        candidate_dials = homeostasis_result["stabilized_dials"]

        exp_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("experiential/")}
        psy_dials = {k: candidate_dials[k] for k in candidate_dials if k.startswith("psychological/")}
        plasticity_result = self.plasticity_engine.compute_dynamic_rates(
            experiential_dials=exp_dials,
            psychological_dials=psy_dials,
        )
        effective_alpha = plasticity_result["dynamic_alpha"]

        momentum_result = self.disposition.incorporate_situational_stimulus(
            situational_dials=candidate_dials,
            gamma_override=effective_alpha,
        )

        journal_res = self.journal.record_episode(
            cycle=current_cycle,
            sentence=sentence,
            target_lemmas=lemmas,
            resolved_senses=resolved_senses,
            leaf_dials=candidate_dials,
            speaking_register=speaking_register,
            action_bid=action_bid,
            post_action_echo=echo_result["echo_deltas"],
            is_conflict=is_conflict,
        )

        return {
            "cycle": current_cycle,
            "sentence": sentence,
            "target_lemmas": lemmas,
            "resolved_senses": resolved_senses,
            "speaking_register": speaking_register,
            "action_bid": action_bid,
            "coherence": coherence_result,
            "consonance": consonance_result,
            "homeostasis": homeostasis_result,
            "plasticity": plasticity_result,
            "momentum": momentum_result,
            "post_action_echo": echo_result["echo_deltas"],
            "journal_result": journal_res,
            "disposition_dials": deepcopy(self.disposition.dials),
            "taxonomic_modulations": taxonomic_modulations,
        }

    def sleep(self, prune_buffer: bool = True) -> Dict[str, Any]:
        summary, remaining = self.consolidator.consolidate_sleep_cycle(
            episodic_buffer=list(self.journal.entries),
            prune_buffer=prune_buffer,
        )
        if prune_buffer:
            self.journal.entries.clear()
            for ep in remaining:
                self.journal.entries.append(ep)

        drift_res = self.disposition.apply_idle_equilibrium_drift(steps=1)

        return {
            "consolidation_summary": summary,
            "remaining_journal_episodes": len(self.journal.entries),
            "drift_result": drift_res,
            "active_long_term_rules": len(self.consolidator.long_term_rules),
            "sleep_cycle": summary["sleep_cycle"],
        }
