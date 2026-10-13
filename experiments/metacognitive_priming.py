"""Metacognitive Priming Console Prototype: connecting disambiguated meanings to the Philosophical seed dials."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'experiments'))

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

HEXADIC_PALETTE = {
    'agency': {
        'node_id': 'philosophical/being/agency',
        'color_name': 'red',
        'rgb': [255, 0, 68],
        'dimension': 'extra-dimensional',
        'materia_type': 'summoning',
        'chess_archetype': 'queen',
        'element': 'fire',
        'shadow_pathology': 'psychosis',
        'shadow_description': 'Agentive ungrounded projection; hallucinated volition',
        'creature_kingdom': 'reptile',
        'kingdom_description': 'Creature of the sun; cold-blooded volitional basking',
        'archetype_role': 'Volition, directive command, telekinetic movement',
    },
    'existence': {
        'node_id': 'philosophical/being/existence',
        'color_name': 'cyan',
        'rgb': [0, 240, 255],
        'dimension': 'extra-dimensional',
        'materia_type': 'white_magic',
        'chess_archetype': 'king',
        'element': 'ice/water',
        'shadow_pathology': 'paranoia',
        'shadow_description': 'Existential siege; persecutory stasis under external threat',
        'creature_kingdom': 'mammal',
        'kingdom_description': 'Warmth, communal bond, light, embodied ground of being',
        'archetype_role': 'Ground of being, ontological stasis, essential reality',
    },
    'order': {
        'node_id': 'philosophical/structure/order',
        'color_name': 'green',
        'rgb': [0, 255, 102],
        'dimension': 'inter-dimensional',
        'materia_type': 'instrument_magic',
        'chess_archetype': 'knight',
        'element': 'wind',
        'shadow_pathology': 'prejudice',
        'shadow_description': 'Rigid distorted order; unbending preconception',
        'creature_kingdom': 'bird',
        'kingdom_description': 'Master of wind, aerial geometry, flock flight of law',
        'archetype_role': 'Harmonic structure, medium mobility, law of organization',
    },
    'chaos': {
        'node_id': 'philosophical/structure/chaos',
        'color_name': 'magenta',
        'rgb': [255, 0, 170],
        'dimension': 'inter-dimensional',
        'materia_type': 'status_poison',
        'chess_archetype': 'bishop',
        'element': 'poison',
        'shadow_pathology': 'corruption',
        'shadow_description': 'Structural rot, systemic entropy, moral and institutional decay',
        'creature_kingdom': 'amphibian',
        'kingdom_description': 'Creature of the shadow/twilight threshold, shifting boundaries',
        'archetype_role': 'Entropy, absurdity, corruption, disruptive anomaly',
    },
    'continuity': {
        'node_id': 'philosophical/persistence/continuity',
        'color_name': 'blue',
        'rgb': [0, 102, 255],
        'dimension': 'hyper-dimensional',
        'materia_type': 'support_black_magic',
        'chess_archetype': 'rook',
        'element': 'deep_flow',
        'shadow_pathology': 'mania_greed',
        'shadow_description': 'Unstoppable runaway momentum; insatiable accumulation',
        'creature_kingdom': 'fish',
        'kingdom_description': 'Creature of deep oceanic flow, unbroken continuous currents',
        'archetype_role': 'Continuous scale, scientific continuum, sustained duration',
    },
    'discreteness': {
        'node_id': 'philosophical/persistence/discreteness',
        'color_name': 'yellow',
        'rgb': [255, 215, 0],
        'dimension': 'hyper-dimensional',
        'materia_type': 'command_tactics',
        'chess_archetype': 'pawn',
        'element': 'earth/steps',
        'shadow_pathology': 'narcissism',
        'shadow_description': 'Discrete self-enclosure; hyper-isolated ego fixation',
        'creature_kingdom': 'insect',
        'kingdom_description': 'Creature of the soil and swarm; quantized burning earth',
        'archetype_role': 'Discrete steps, tactical command, serial succession',
    },
}


def verify_canonical_nodes():
    """Verify that all philosophical target nodes exist in the frozen seed inventory."""
    inventory_ids = {node_id for node_id, _, domain, _, depth in _inventory() if domain == 'philosophical' and depth == 2}
    expected = set(PHILOSOPHICAL_LEAF_NODES.values())
    if inventory_ids != expected:
        raise ValueError(f'seed inventory divergence: expected {expected}, got {inventory_ids}')


verify_canonical_nodes()


def compute_chromatic_aura(dials):
    """Computes composite RGB/HEX color aura from dial activations."""
    total = sum(dials.values())
    if total <= 1e-6:
        return {'hex': '#808080', 'rgb': [128, 128, 128], 'tone': 'neutral_slate'}
    r = int(sum(HEXADIC_PALETTE[k]['rgb'][0] * dials[k] for k in dials) / total)
    g = int(sum(HEXADIC_PALETTE[k]['rgb'][1] * dials[k] for k in dials) / total)
    b = int(sum(HEXADIC_PALETTE[k]['rgb'][2] * dials[k] for k in dials) / total)
    hex_code = f'#{r:02X}{g:02X}{b:02X}'
    return {'hex': hex_code, 'rgb': [r, g, b]}


def compute_priming_dials(prediction):
    """Computes continuous fuzzy priming activations on the Philosophical dials."""
    if prediction.get('decision') == 'abstain' or not prediction.get('selected_sense'):
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
            'materia_profile': {k: 0.0 for k in HEXADIC_PALETTE},
            'chromatic_aura': {'hex': '#808080', 'rgb': [128, 128, 128], 'tone': 'neutral_slate'},
            'dimensional_resonance': {
                'extra_dimensional_being': 'unactivated',
                'inter_dimensional_structure': 'unactivated',
                'hyper_dimensional_persistence': 'unactivated',
            },
            'shadow_profile': {
                k: {
                    'pathology': HEXADIC_PALETTE[k]['shadow_pathology'],
                    'description': HEXADIC_PALETTE[k]['shadow_description'],
                    'vulnerability_score': 0.0,
                }
                for k in HEXADIC_PALETTE
            },
            'kingdom_profile': {
                k: {
                    'kingdom': HEXADIC_PALETTE[k]['creature_kingdom'],
                    'description': HEXADIC_PALETTE[k]['kingdom_description'],
                    'resonance_level': 0.0,
                }
                for k in HEXADIC_PALETTE
            },
            'poetic_action_bid': 'Resting in quiet contemplation: zero active collocate bids; neutral slate aura (#808080); kingdoms silent.',
            'epistemic_mirror': {
                'theory': 'Hypothesis withheld due to unobserved context',
                'fact': 'Zero matching syntactic context anchors observed',
                'clarity': 1.0,
                'confidence': 0.0,
            },
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
            'materia_profile': {k: 0.50 for k in HEXADIC_PALETTE},
            'chromatic_aura': {'hex': '#AAAAAA', 'rgb': [170, 170, 170], 'tone': 'deliberative_gray'},
            'dimensional_resonance': {
                'extra_dimensional_being': 'split',
                'inter_dimensional_structure': 'split',
                'hyper_dimensional_persistence': 'split',
            },
            'shadow_profile': {
                k: {
                    'pathology': HEXADIC_PALETTE[k]['shadow_pathology'],
                    'description': HEXADIC_PALETTE[k]['shadow_description'],
                    'vulnerability_score': 0.5,
                }
                for k in HEXADIC_PALETTE
            },
            'kingdom_profile': {
                k: {
                    'kingdom': HEXADIC_PALETTE[k]['creature_kingdom'],
                    'description': HEXADIC_PALETTE[k]['kingdom_description'],
                    'resonance_level': 0.5,
                }
                for k in HEXADIC_PALETTE
            },
            'poetic_action_bid': 'Deliberative split across competing interpretations: balanced gray aura (#AAAAAA); dual kingdom threshold; awaiting clarity.',
            'epistemic_mirror': {
                'theory': 'Competing hypotheses detected',
                'fact': 'Ambiguous syntactic context anchors observed',
                'clarity': 0.0,
                'confidence': 0.50,
            },
        }

    sense = prediction['selected_sense']
    dials = {}

    # 1. Being Dyad: Agency vs Existence (Extra-dimensional)
    if sense in ('order%1:10:03::', 'order%1:10:01::'):
        # Directive action / commercial execution (Red / Summoning / Queen / Reptile)
        dials['agency'] = 0.85
        dials['existence'] = 0.40
    elif sense == 'order%1:26:00::':
        # Condition of society / established state (Cyan / White Magic / King / Mammal)
        dials['agency'] = 0.20
        dials['existence'] = 0.85
    elif sense == 'order%1:26:02::':
        # Systematic arrangement in structure
        dials['agency'] = 0.35
        dials['existence'] = 0.75
    else:
        dials['agency'] = 0.45
        dials['existence'] = 0.55

    # 2. Structure Dyad: Order vs Chaos (Inter-dimensional)
    if sense in ('order%1:26:00::', 'order%1:26:02::'):
        # Social stability, cosmic order, logical arrangement (Green / Wind / Knight / Bird)
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

    # 3. Persistence Dyad: Continuity vs Discreteness (Hyper-dimensional)
    if sense == 'order%1:07:01::':
        # Degree / magnitude on a continuous scale (Blue / Black Magic / Rook / Fish)
        dials['continuity'] = 0.85
        dials['discreteness'] = 0.15
    elif sense in ('order%1:14:00::', 'order%1:10:02::'):
        # Sequential steps / discrete succession (Yellow / Command / Pawn / Insect)
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

    # Compute chromatic aura and archetypal profiles
    aura = compute_chromatic_aura(dials)
    materia_profile = {
        k: {
            'activation': dials[k],
            'color': HEXADIC_PALETTE[k]['color_name'],
            'materia': HEXADIC_PALETTE[k]['materia_type'],
            'archetype': HEXADIC_PALETTE[k]['chess_archetype'],
            'dimension': HEXADIC_PALETTE[k]['dimension'],
            'element': HEXADIC_PALETTE[k]['element'],
        }
        for k in dials
    }

    dimensional_res = {
        'extra_dimensional_being': f"{'agency_queen_fire' if b_agency > 0 else 'existence_king_water'} (bias: {round(b_agency, 2)})",
        'inter_dimensional_structure': f"{'order_knight_wind' if b_order > 0 else 'chaos_bishop_poison'} (bias: {round(b_order, 2)})",
        'hyper_dimensional_persistence': f"{'continuity_rook_black_magic' if b_persistence > 0 else 'discreteness_pawn_command'} (bias: {round(b_persistence, 2)})",
    }

    shadow_profile = {
        k: {
            'pathology': HEXADIC_PALETTE[k]['shadow_pathology'],
            'description': HEXADIC_PALETTE[k]['shadow_description'],
            'vulnerability_score': round(dials[k] * (1.0 - min(dials.values())), 3),
        }
        for k in dials
    }

    kingdom_profile = {
        k: {
            'kingdom': HEXADIC_PALETTE[k]['creature_kingdom'],
            'description': HEXADIC_PALETTE[k]['kingdom_description'],
            'resonance_level': dials[k],
        }
        for k in dials
    }

    sorted_dials = sorted(dials.items(), key=lambda x: x[1], reverse=True)
    top_key = sorted_dials[0][0]
    top_arch = HEXADIC_PALETTE[top_key]['chess_archetype'].title()
    top_king = HEXADIC_PALETTE[top_key]['creature_kingdom'].title()
    top_elem = HEXADIC_PALETTE[top_key]['element']
    top_shadow = HEXADIC_PALETTE[top_key]['shadow_pathology']
    top_materia = HEXADIC_PALETTE[top_key]['materia_type'].replace('_', ' ').title()

    theory_text = prediction.get('explanation', '')
    poetic_bid = (
        f"A {top_arch} of {top_king} ({top_materia}) chord in {aura['hex']} aura: "
        f"enacting {stance.replace('_', ' ')} via {top_elem}; "
        f"guarded against {top_shadow}; "
        f"grounding theory '{theory_text}' into observed fact."
    )

    # Epistemic Mirror (Psychological: Truth & Contemplation)
    clarity = round(max(dials.values()) - min(dials.values()), 3)
    epistemic_mirror = {
        'theory': theory_text,
        'fact': f"Observed syntactic collocate for sense {sense}",
        'clarity': clarity,
        'confidence': 1.0,
    }

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
        'chromatic_aura': aura,
        'materia_profile': materia_profile,
        'dimensional_resonance': dimensional_res,
        'shadow_profile': shadow_profile,
        'kingdom_profile': kingdom_profile,
        'poetic_action_bid': poetic_bid,
        'epistemic_mirror': epistemic_mirror,
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


def run_priming_study(checkpoints, dev_path, output_dir=None):
    """Full study execution enforcing Rule D004 baseline parity."""
    if isinstance(checkpoints, (str, Path)):
        checkpoint_list = [Path(checkpoints)]
    else:
        checkpoint_list = [Path(p) for p in checkpoints]

    for cp in checkpoint_list:
        if not cp.is_file():
            raise FileNotFoundError(f'checkpoint missing: {cp}')

    dev_file = Path(dev_path)
    if not dev_file.is_file():
        raise FileNotFoundError(f'dev export missing: {dev_path}')

    all_rows = json.loads(dev_file.read_text(encoding='utf-8'))

    # Load from primary and ordinary memory across all checkpoints
    all_primary_records = []
    all_memory_records = []
    checkpoint_hashes = {}

    for cp in checkpoint_list:
        store = Store(cp.parent)
        primary_state = store.read()
        memory_state = json.loads(cp.read_text(encoding='utf-8'))['state']

        if digest(primary_state) != digest(memory_state):
            raise ValueError(f'consumer parity failure at state read for {cp}')

        all_primary_records.extend(primary_state['records'])
        all_memory_records.extend(memory_state['records'])
        checkpoint_hashes[str(cp)] = hashlib.sha256(cp.read_bytes()).hexdigest()

    primary_rules = pd.compile_rules(all_primary_records, all_rows)
    memory_rules = pd.compile_rules(all_memory_records, all_rows)

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
        'checkpoint_hashes': checkpoint_hashes,
        'checkpoint_sha256': list(checkpoint_hashes.values())[0] if len(checkpoint_hashes) == 1 else None,
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
    parser.add_argument('--checkpoint', nargs='+', required=True, help='One or more checkpoint files')
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    res = run_priming_study(args.checkpoint, args.dev_export, args.output_dir)
    print(json.dumps(res, sort_keys=True, indent=2))
