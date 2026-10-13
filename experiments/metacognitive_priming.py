"""Metacognitive Priming Console Prototype: connecting disambiguated meanings to the Philosophical seed dials."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from lmft_lab.birth import _inventory
from lmft_lab.runtime_store import Store, digest, atomic_json
import persistent_disambiguation as pd

KIND = 'metacognitive-priming-1'

PHILOSOPHICAL_LEAF_NODES = {
    'agency': 'philosophical/being/agency',
    'existence': 'philosophical/being/existence',
    'order': 'philosophical/structure/order',
    'chaos': 'philosophical/structure/chaos',
    'continuity': 'philosophical/persistence/continuity',
    'discreteness': 'philosophical/persistence/discreteness',
}


def verify_canonical_nodes():
    """Verify that all philosophical target nodes exist in the frozen seed inventory."""
    inventory_ids = {node_id for node_id, _, domain, _, depth in _inventory() if domain == 'philosophical' and depth == 2}
    expected = set(PHILOSOPHICAL_LEAF_NODES.values())
    if inventory_ids != expected:
        raise ValueError(f'seed inventory divergence: expected {expected}, got {inventory_ids}')


verify_canonical_nodes()


def compute_priming_dials(prediction):
    """Computes continuous fuzzy priming activations on the Philosophical dials."""
    if prediction['decision'] == 'abstain':
        return {
            'epistemic_abstention': True,
            'dominant_stance': 'neutral_open',
            'dials': {node_id: 0.0 for node_id in PHILOSOPHICAL_LEAF_NODES.values()},
            'dyadic_biases': {
                'being_agency_vs_existence': 0.0,
                'structure_order_vs_chaos': 0.0,
                'persistence_continuity_vs_discreteness': 0.0,
            },
            'confidence': 0.0,
        }
    elif prediction['decision'] == 'ambiguous':
        return {
            'epistemic_abstention': False,
            'ambiguity_detected': True,
            'dominant_stance': 'deliberative_split',
            'dials': {node_id: 0.50 for node_id in PHILOSOPHICAL_LEAF_NODES.values()},
            'dyadic_biases': {
                'being_agency_vs_existence': 0.0,
                'structure_order_vs_chaos': 0.0,
                'persistence_continuity_vs_discreteness': 0.0,
            },
            'confidence': 0.50,
        }

    sense = prediction['selected_sense']
    dials = {}

    # 1. Being Dyad: Agency vs Existence
    if sense in ('order%1:10:03::', 'order%1:10:01::'):
        # Directive action / commercial execution
        dials['agency'] = 0.85
        dials['existence'] = 0.40
    elif sense == 'order%1:26:00::':
        # Condition of society / established state
        dials['agency'] = 0.20
        dials['existence'] = 0.85
    elif sense == 'order%1:26:02::':
        # Systematic arrangement in structure
        dials['agency'] = 0.35
        dials['existence'] = 0.75
    else:
        dials['agency'] = 0.45
        dials['existence'] = 0.55

    # 2. Structure Dyad: Order vs Chaos
    if sense in ('order%1:26:00::', 'order%1:26:02::'):
        # Social stability, cosmic order, logical arrangement
        dials['order'] = 0.85
        dials['chaos'] = 0.05
    elif sense == 'order%1:10:03::':
        # Authoritative command / obedience hierarchy
        dials['order'] = 0.75
        dials['chaos'] = 0.10
    elif sense in ('order%1:14:00::', 'order%1:10:02::'):
        # Serial sequence / orderly presentation
        dials['order'] = 0.70
        dials['chaos'] = 0.10
    else:
        dials['order'] = 0.60
        dials['chaos'] = 0.15

    # 3. Persistence Dyad: Continuity vs Discreteness
    if sense == 'order%1:07:01::':
        # Degree / magnitude on a continuous scale
        dials['continuity'] = 0.85
        dials['discreteness'] = 0.15
    elif sense in ('order%1:14:00::', 'order%1:10:02::'):
        # Sequential steps / discrete succession
        dials['continuity'] = 0.15
        dials['discreteness'] = 0.85
    else:
        dials['continuity'] = 0.50
        dials['discreteness'] = 0.50

    mapped_dials = {PHILOSOPHICAL_LEAF_NODES[k]: v for k, v in dials.items()}

    b_agency = dials['agency'] - dials['existence']
    b_order = dials['order'] - dials['chaos']
    b_persistence = dials['continuity'] - dials['discreteness']

    # Qualitative stance descriptor
    if b_agency > 0.3 and b_order > 0.5:
        stance = 'authoritative_directive_execution'
    elif b_agency < -0.3 and b_order > 0.5:
        stance = 'stable_ontological_equilibrium'
    elif b_persistence > 0.4:
        stance = 'quantitative_continuum_awareness'
    elif b_persistence < -0.4:
        stance = 'discrete_sequential_operation'
    else:
        stance = 'balanced_contextual_stance'

    return {
        'epistemic_abstention': False,
        'dominant_stance': stance,
        'dials': mapped_dials,
        'dyadic_biases': {
            'being_agency_vs_existence': round(b_agency, 3),
            'structure_order_vs_chaos': round(b_order, 3),
            'persistence_continuity_vs_discreteness': round(b_persistence, 3),
        },
        'confidence': 1.0,
    }


def evaluate_priming(compiled_rules, examples):
    """Evaluates examples unassisted, producing joined disambiguations and metacognitive stances."""
    priming_results = []
    for ex in examples:
        item = {
            'id': ex['example_id'],
            'tokens': ex['surface_tokens'],
            'target_indices': [ex['target_index']],
        }
        pred = pd.predict_item(compiled_rules, item)
        priming = compute_priming_dials(pred)
        priming_results.append({
            'example_id': ex['example_id'],
            'gold_sense_key': ex['target_sense_key'],
            'prediction': pred,
            'metacognitive_priming': priming,
        })
    return priming_results


def run_priming_study(checkpoint_path, dev_path, output_dir=None):
    """Full study execution enforcing Rule D004 baseline parity."""
    checkpoint_file = Path(checkpoint_path)
    if not checkpoint_file.is_file():
        raise FileNotFoundError(f'checkpoint missing: {checkpoint_path}')

    dev_file = Path(dev_path)
    if not dev_file.is_file():
        raise FileNotFoundError(f'dev export missing: {dev_path}')

    all_rows = json.loads(dev_file.read_text(encoding='utf-8'))

    # Load from primary and ordinary memory
    store = Store(checkpoint_file.parent)
    primary_state = store.read()
    memory_state = json.loads(checkpoint_file.read_text(encoding='utf-8'))['state']

    if digest(primary_state) != digest(memory_state):
        raise ValueError('consumer parity failure at state read')

    primary_rules = pd.compile_rules(primary_state['records'], all_rows)
    memory_rules = pd.compile_rules(memory_state['records'], all_rows)

    if digest(primary_rules) != digest(memory_rules):
        raise ValueError('consumer parity failure at rule compilation')

    primary_priming = evaluate_priming(primary_rules, all_rows)
    memory_priming = evaluate_priming(memory_rules, all_rows)

    if digest(primary_priming) != digest(memory_priming):
        raise ValueError('consumer parity failure at priming calculation')

    # Aggregate stance distribution
    stance_counts = {}
    for r in primary_priming:
        st = r['metacognitive_priming']['dominant_stance']
        stance_counts[st] = stance_counts.get(st, 0) + 1

    summary = {
        'kind': KIND,
        'checkpoint_sha256': hashlib.sha256(checkpoint_file.read_bytes()).hexdigest(),
        'development_sha256': hashlib.sha256(dev_file.read_bytes()).hexdigest(),
        'total_instances_primed': len(primary_priming),
        'consumer_parity': True,
        'evaluation_digest': digest(primary_priming),
        'stance_distribution': stance_counts,
        'canonical_nodes_verified': list(PHILOSOPHICAL_LEAF_NODES.values()),
        'samples': primary_priming[:6],
    }

    if output_dir:
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        atomic_json(out_p / 'metacognitive_priming_summary.json', summary)
        atomic_json(out_p / 'full_priming_records.json', primary_priming)

    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    res = run_priming_study(args.checkpoint, args.dev_export, args.output_dir)
    print(json.dumps(res, sort_keys=True, indent=2))
