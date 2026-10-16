"""Persistent Dispositional State Vector & Momentum Drift Engine.

Maintains continuous dispositional momentum (an ongoing temporal 'mood') across sequential
interactions for all 24 canonical leaves in birth.py, applying exponential moving average (EMA)
momentum updates and gentle equilibrium drift without mutating the frozen 40-node founding seed (Rule D001).

Zero runtime LLM calls during unassisted evaluation.
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.birth import _inventory
from lmft_lab.individual_package import get_canonical_seed_fingerprint
from lmft_lab.runtime_store import digest


CANONICAL_LEAF_IDS = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
assert len(CANONICAL_LEAF_IDS) == 24, f"Expected 24 canonical leaves, found {len(CANONICAL_LEAF_IDS)}"

DEFAULT_GAMMA = 0.35  # Situational responsiveness vs dispositional inertia
DEFAULT_MU = 0.05     # Idle equilibrium drift rate towards 0.50


class PersistentDispositionalVector:
    """Maintains continuous 24-leaf dispositional baseline across sequential interactions."""

    def __init__(
        self,
        initial_dials: Optional[Dict[str, float]] = None,
        gamma: float = DEFAULT_GAMMA,
        mu: float = DEFAULT_MU,
        epoch_count: int = 0,
    ):
        self.gamma = max(0.05, min(0.95, float(gamma)))
        self.mu = max(0.01, min(0.50, float(mu)))
        self.epoch_count = int(epoch_count)
        self.seed_fingerprint = get_canonical_seed_fingerprint()

        self.dials: Dict[str, float] = {k: 0.50 for k in sorted(CANONICAL_LEAF_IDS)}
        if initial_dials:
            for k, v in initial_dials.items():
                if k in self.dials:
                    self.dials[k] = round(max(0.0, min(1.0, float(v))), 4)

    def incorporate_situational_stimulus(
        self,
        situational_dials: Dict[str, float],
        gamma_override: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Incorporates new situational activations using EMA momentum drift."""
        gamma = self.gamma if gamma_override is None else max(0.05, min(0.95, float(gamma_override)))
        self.epoch_count += 1

        prior_state = deepcopy(self.dials)
        deltas = {}

        for k in sorted(CANONICAL_LEAF_IDS):
            sit_val = float(situational_dials.get(k, self.dials[k]))
            sit_val = max(0.0, min(1.0, sit_val))

            # EMA: D_t = (1 - gamma) * D_{t-1} + gamma * S_t
            updated = (1.0 - gamma) * self.dials[k] + gamma * sit_val
            new_val = round(min(1.0, max(0.0, updated)), 4)
            deltas[k] = round(new_val - self.dials[k], 4)
            self.dials[k] = new_val

        return {
            "epoch": self.epoch_count,
            "gamma": gamma,
            "prior_dials": prior_state,
            "deltas": deltas,
            "current_dials": deepcopy(self.dials),
        }

    def apply_idle_equilibrium_drift(self, steps: int = 1) -> Dict[str, Any]:
        """Gently relaxes activations towards neutral equilibrium 0.50 during idle intervals."""
        steps = max(1, int(steps))
        prior_state = deepcopy(self.dials)

        for _ in range(steps):
            for k in sorted(CANONICAL_LEAF_IDS):
                diff = 0.50 - self.dials[k]
                self.dials[k] = round(self.dials[k] + self.mu * diff, 4)

        return {
            "steps": steps,
            "mu": self.mu,
            "prior_dials": prior_state,
            "current_dials": deepcopy(self.dials),
        }

    def compute_hierarchical_tree(self) -> Dict[str, Any]:
        """Aggregates the 24 leaf dials up into the 12 Depth-1 Branches and 4 Depth-0 Domains (40 nodes total)."""
        inv = list(_inventory())
        leaves_by_branch: Dict[str, List[float]] = {}
        branches_by_domain: Dict[str, List[str]] = {}
        for node_id, _label, domain, parent_id, depth in inv:
            if depth == 1:
                leaves_by_branch.setdefault(node_id, [])
                branches_by_domain.setdefault(domain, []).append(node_id)
            elif depth == 2 and parent_id:
                leaves_by_branch.setdefault(parent_id, []).append(float(self.dials.get(node_id, 0.50)))

        branch_dials: Dict[str, float] = {}
        for branch_id in sorted(leaves_by_branch.keys()):
            vals = leaves_by_branch[branch_id]
            branch_dials[branch_id] = round(sum(vals) / max(1, len(vals)), 4)

        domain_dials: Dict[str, float] = {}
        for domain_id in sorted(branches_by_domain.keys()):
            b_vals = [branch_dials[b_id] for b_id in branches_by_domain[domain_id]]
            domain_dials[domain_id] = round(sum(b_vals) / max(1, len(b_vals)), 4)

        all_40_nodes: Dict[str, float] = {}
        all_40_nodes.update(domain_dials)
        all_40_nodes.update(branch_dials)
        all_40_nodes.update(deepcopy(self.dials))
        return {
            "domain_dials": domain_dials,
            "branch_dials": branch_dials,
            "leaf_dials": deepcopy(self.dials),
            "all_40_nodes": all_40_nodes,
        }

    def export_state(self) -> Dict[str, Any]:
        """Serializes dispositional vector for packaging and persistence."""
        payload = {
            "epoch_count": self.epoch_count,
            "gamma": self.gamma,
            "mu": self.mu,
            "seed_fingerprint": self.seed_fingerprint,
            "dials": deepcopy(self.dials),
        }
        payload["state_digest"] = digest({k: v for k, v in payload.items() if k != "state_digest"})
        return payload

    def import_state(self, state_dict: Dict[str, Any]) -> None:
        """Restores dispositional vector, strictly validating Rule D001 seed invariant."""
        incoming_fingerprint = state_dict.get("seed_fingerprint")
        if incoming_fingerprint != self.seed_fingerprint:
            raise ValueError(
                f"Seed geometry violation: incoming fingerprint {incoming_fingerprint} "
                f"does not match frozen canonical seed fingerprint {self.seed_fingerprint}"
            )

        self.epoch_count = int(state_dict.get("epoch_count", 0))
        self.gamma = float(state_dict.get("gamma", DEFAULT_GAMMA))
        self.mu = float(state_dict.get("mu", DEFAULT_MU))

        incoming_dials = state_dict.get("dials", {})
        for k in sorted(CANONICAL_LEAF_IDS):
            if k in incoming_dials:
                self.dials[k] = round(max(0.0, min(1.0, float(incoming_dials[k]))), 4)


class OrdinaryMemoryDispositionalComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def __init__(
        self,
        initial_dials: Optional[Dict[str, float]] = None,
        gamma: float = DEFAULT_GAMMA,
        mu: float = DEFAULT_MU,
        epoch_count: int = 0,
    ):
        self.gamma = max(0.05, min(0.95, float(gamma)))
        self.mu = max(0.01, min(0.50, float(mu)))
        self.epoch_count = int(epoch_count)
        self.seed_fingerprint = get_canonical_seed_fingerprint()

        self.dials: Dict[str, float] = {k: 0.50 for k in sorted(CANONICAL_LEAF_IDS)}
        if initial_dials:
            for k, v in initial_dials.items():
                if k in self.dials:
                    self.dials[k] = round(max(0.0, min(1.0, float(v))), 4)

    def incorporate(
        self,
        situational_dials: Dict[str, float],
        gamma_override: Optional[float] = None,
    ) -> Dict[str, Any]:
        gamma = self.gamma if gamma_override is None else max(0.05, min(0.95, float(gamma_override)))
        self.epoch_count += 1

        prior_state = deepcopy(self.dials)
        deltas = {}

        for k in sorted(CANONICAL_LEAF_IDS):
            sit_val = float(situational_dials.get(k, self.dials[k]))
            sit_val = max(0.0, min(1.0, sit_val))

            updated = (1.0 - gamma) * self.dials[k] + gamma * sit_val
            new_val = round(min(1.0, max(0.0, updated)), 4)
            deltas[k] = round(new_val - self.dials[k], 4)
            self.dials[k] = new_val

        return {
            "epoch": self.epoch_count,
            "gamma": gamma,
            "prior_dials": prior_state,
            "deltas": deltas,
            "current_dials": deepcopy(self.dials),
        }

    def idle_drift(self, steps: int = 1) -> Dict[str, Any]:
        steps = max(1, int(steps))
        prior_state = deepcopy(self.dials)

        for _ in range(steps):
            for k in sorted(CANONICAL_LEAF_IDS):
                diff = 0.50 - self.dials[k]
                self.dials[k] = round(self.dials[k] + self.mu * diff, 4)

        return {
            "steps": steps,
            "mu": self.mu,
            "prior_dials": prior_state,
            "current_dials": deepcopy(self.dials),
        }

    def export_state(self) -> Dict[str, Any]:
        payload = {
            "epoch_count": self.epoch_count,
            "gamma": self.gamma,
            "mu": self.mu,
            "seed_fingerprint": self.seed_fingerprint,
            "dials": deepcopy(self.dials),
        }
        payload["state_digest"] = digest({k: v for k, v in payload.items() if k != "state_digest"})
        return payload
