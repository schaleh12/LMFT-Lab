"""Observation -> model proposals -> temporary activation; no state mutation."""
from dataclasses import asdict
import hashlib
import json
from .birth import validate_birth_state
from .local_models import ROLES, validate_proposal
from .model_assets import ModelError
from .propagation import propagate_activation, PropagationConfig


def process_observation(state, observation, *, event_id, models, relationships=(),
                        relationship_source="no-authored-associations",
                        propagation_config=PropagationConfig()):
    validate_birth_state(state)
    if not isinstance(observation, str) or not observation.strip() or len(observation) > 6000:
        raise ValueError("observation must contain 1..6000 characters")
    if not isinstance(event_id, str) or not event_id.strip() or event_id == state.birth_event_id:
        raise ValueError("a distinct nonempty observation event_id is required")
    # Validate wiring before an expensive model call.
    propagate_activation(state, {}, relationships, event_id=event_id,
                         source_instance="preflight", relationship_source=relationship_source,
                         config=propagation_config)
    node_ids = tuple(n.id for n in state.nodes)
    trace = {"schema_version": 1, "event_id": event_id,
             "individual_id": state.individual_id, "birth_event_id": state.birth_event_id,
             "seed_version": state.seed_version, "state_version": state.version,
             "input_state": asdict(state),
             "state_sha256": hashlib.sha256(json.dumps(asdict(state), sort_keys=True).encode()).hexdigest(),
             "observation": observation, "calls": [], "persistent_changes": [],
             "revision_status": "not_applied_revision_engine_not_implemented"}
    context = {}
    try:
        for role in ROLES:
            proposal, call = models.complete(role, observation, node_ids, context)
            trace["calls"].append(call)
            # Revalidate at the LMFT boundary, even with an injected adapter.
            proposal = validate_proposal(json.dumps(proposal), node_ids, observation)
            trace[role] = proposal
            if role == "interpretation":
                values = {m["node_id"]: m["relevance"] for m in proposal["memberships"]}
                result = propagate_activation(state, values, relationships, event_id=event_id,
                    source_instance=call["request_sha256"], relationship_source=relationship_source,
                    config=propagation_config, source="llm")
                trace["activation"] = asdict(result)
                context = {"interpretation": proposal, "activation": result.activations}
            elif role == "digestion":
                context = {**context, "digestion": proposal}
        trace["status"] = "completed"
        return trace
    except ModelError as exc:
        if hasattr(exc, "trace"):
            trace["calls"].append(exc.trace)
        trace.update(status="failed", error=str(exc))
        exc.processing_trace = trace
        raise
