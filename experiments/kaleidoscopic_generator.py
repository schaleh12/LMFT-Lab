"""Kaleidoscopic Linguistic Prismatic Generator Prototype for LMFT.

Translates the tripartite psychological funnel (Contemplation, Truth, Will)
into a multi-lens kaleidoscopic prism that twists three angular lenses:
  - Lens 1: Contemplation Lens (theta_C) - Sensory tone & cognitive temperature
  - Lens 2: Truth Lens (theta_T) - Metaphysical depth & empirical grounding
  - Lens 3: Will Lens (theta_W) - Social delivery & actionable strategy

Evaluates across the 33 SemCor development instances with 100% deterministic unassisted inference (0 LLM calls).
Enforces Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))

from lmft_lab.birth import _inventory
from lmft_lab.local_models import strict_json
from lmft_lab.runtime_store import Store, digest, atomic_json
import meditative_regulation as mr
import metacognitive_priming as mp
import persistent_disambiguation as pd
import tripartite_funnel as tf

ROOT = Path(__file__).resolve().parents[1]
KIND = 'kaleidoscopic-generator-1'


def calculate_lens_angles(funnel_record, regulation_dials):
    """Calculates the 3 kaleidoscopic lens angles from the tripartite funnel and regulation dials."""
    if funnel_record['epistemic_abstention']:
        return {
            'theta_contemplation': 0.0,
            'theta_truth': 0.0,
            'theta_will': 0.0,
            'contemplation_lens': 'Quiescent Stasis',
            'truth_lens': 'Awaiting Observation',
            'will_lens': 'Latent Readiness',
            'harmonic_concordance': 1.0,
        }

    psych = funnel_record['unified_psychological_cluster']
    clarity = psych['psychological/contemplation/clarity']
    confidence = psych['psychological/contemplation/confidence']
    theory = psych['psychological/truth/theory']
    fact = psych['psychological/truth/fact']
    intention = psych['psychological/will/intention']
    execution = psych['psychological/will/execution']

    val = regulation_dials.get('experiential/phase/valence', 0.5)
    aro = regulation_dials.get('experiential/phase/arousal', 0.5)
    order = regulation_dials.get('philosophical/structure/order', 0.5)
    honor = regulation_dials.get('cultural/justice/honor', 0.5)

    # 1. Contemplation Lens Angle (0 to 360)
    theta_c = round((clarity * 180.0 + val * 90.0 + aro * 90.0) % 360.0, 1)
    if theta_c < 90.0:
        lens_c = 'Lucid Dawn (Crisp analytical detachment)'
    elif theta_c < 180.0:
        lens_c = 'Sunlit Zenith (Warm expansive communion)'
    elif theta_c < 270.0:
        lens_c = 'Twilight Threshold (Reflective liminal caution)'
    else:
        lens_c = 'Midnight Depth (Deep oceanic quietude)'

    # 2. Truth Lens Angle (0 to 360)
    theta_t = round((theory * 180.0 + fact * 90.0 + order * 90.0) % 360.0, 1)
    if theta_t < 90.0:
        lens_t = 'Geometric Axiom (Structured crystalline law)'
    elif theta_t < 180.0:
        lens_t = 'Empirical Revelation (Direct grounded testimony)'
    elif theta_t < 270.0:
        lens_t = 'Anamorphic Paradox (Challenging dogmatic assumptions)'
    else:
        lens_t = 'Holistic Synthesis (Seamless multi-coordinate unity)'

    # 3. Will Lens Angle (0 to 360)
    theta_w = round((intention * 180.0 + execution * 90.0 + honor * 90.0) % 360.0, 1)
    if theta_w < 90.0:
        lens_w = 'Sovereign Decree (Authoritative protective stewardship)'
    elif theta_w < 180.0:
        lens_w = 'Harmonic Consensus (Diplomatic communal reconciliation)'
    elif theta_w < 270.0:
        lens_w = 'Tactical Economy (Frugal methodical optimization)'
    else:
        lens_w = 'Quiet Ingestion (Active observant patience)'

    # Angular spread and Harmonic Concordance
    def angle_diff(a1, a2):
        d = abs(a1 - a2) % 360.0
        return d if d <= 180.0 else 360.0 - d

    d_ct = angle_diff(theta_c, theta_t)
    d_tw = angle_diff(theta_t, theta_w)
    d_wc = angle_diff(theta_w, theta_c)
    total_spread = d_ct + d_tw + d_wc
    concordance = round(max(0.0, 1.0 - (total_spread / 540.0)), 3)

    return {
        'theta_contemplation': theta_c,
        'theta_truth': theta_t,
        'theta_will': theta_w,
        'contemplation_lens': lens_c,
        'truth_lens': lens_t,
        'will_lens': lens_w,
        'harmonic_concordance': concordance,
    }


def synthesize_actionable_social_strategy(lens_data, prediction, stance):
    """Synthesizes actionable linguistic social exchange strategy from the aligned lenses."""
    if prediction.get('decision') == 'abstain' or not prediction.get('selected_sense'):
        return {
            'speaking_register': 'Neutral Observant Silence',
            'actionable_social_strategy': 'Maintain quiet epistemic modesty; seek context before formulating assertion.',
            'dialogue_exemplar': 'I observe the context, but reserve judgment until further evidence arrives.',
        }

    c_lens = lens_data['contemplation_lens'].split(' (')[0]
    t_lens = lens_data['truth_lens'].split(' (')[0]
    w_lens = lens_data['will_lens'].split(' (')[0]
    sense = prediction.get('selected_sense', '')
    gloss = prediction.get('explanation', '')

    if 'Sovereign Decree' in w_lens or stance == 'authoritative_directive_execution':
        register = 'Authoritative & Chivalrous'
        strategy = (
            f"Deliver the directive with noble clarity and unyielding honor; "
            f"ground instructions directly in observed factual requirements ('{gloss}') "
            f"to avert authoritarian overextension while ensuring decisive compliance."
        )
        dialogue = f"Under clear authority, we proceed as directed: '{gloss}' must be fulfilled with precision and honor."
    elif 'Harmonic Consensus' in w_lens or stance == 'stable_ontological_equilibrium':
        register = 'Communal & Reassuring'
        strategy = (
            f"Reassure the social circle by affirming established collective peace ('{gloss}'); "
            f"temper unbending dogma with compassionate listening to reinforce long-term communal stability."
        )
        dialogue = f"Let us anchor our discussion in the shared foundation: maintaining '{gloss}' protects us all."
    elif 'Tactical Economy' in w_lens or stance == 'discrete_sequential_operation':
        register = 'Methodical & Pragmatic'
        strategy = (
            f"Break the complex problem into quantized sequential milestones ('{gloss}'); "
            f"minimize friction and waste by executing one verified step at a time."
        )
        dialogue = f"Taking this step by step: organizing '{gloss}' allows us to advance without wasted effort."
    elif stance == 'quantitative_continuum_awareness':
        register = 'Analytical & Scientific'
        strategy = (
            f"Frame the conversation in continuous scientific scale and measurement ('{gloss}'); "
            f"maintain deep flow awareness while cautioning against manic over-accumulation."
        )
        dialogue = f"Measuring this across the continuum: we must gauge '{gloss}' against our sustained capacity."
    else:
        register = 'Equilibrated & Diplomatic'
        strategy = (
            f"Balance competing perspectives across truth and duty; "
            f"synthesize observed facts ('{gloss}') into mutual understanding without premature rigidity."
        )
        dialogue = f"Balancing both structure and perspective: '{gloss}' guides our shared course."

    return {
        'speaking_register': register,
        'actionable_social_strategy': strategy,
        'dialogue_exemplar': dialogue,
    }


def compute_kaleidoscopic_response(funnel_record, regulation_record, prediction):
    """Generates the full kaleidoscopic prismatic response for a single instance."""
    dials = regulation_record['all_24_canonical_leaf_dials']
    stance = regulation_record['regulated_stance']
    lens_data = calculate_lens_angles(funnel_record, dials)
    social_strategy = synthesize_actionable_social_strategy(lens_data, prediction, stance)

    prismatic_gloss = (
        f"Kaleidoscope Prismatic Chord [{lens_data['theta_contemplation']} deg C / {lens_data['theta_truth']} deg T / {lens_data['theta_will']} deg W]: "
        f"Lenses [{lens_data['contemplation_lens'].split(' (')[0]} | {lens_data['truth_lens'].split(' (')[0]} | {lens_data['will_lens'].split(' (')[0]}] "
        f"reach Concordance {lens_data['harmonic_concordance']}, speaking in {social_strategy['speaking_register']} register."
    )

    return {
        'epistemic_abstention': funnel_record['epistemic_abstention'],
        'prism_vector': {
            'theta_contemplation': lens_data['theta_contemplation'],
            'theta_truth': lens_data['theta_truth'],
            'theta_will': lens_data['theta_will'],
        },
        'lens_orientations': {
            'contemplation_lens': lens_data['contemplation_lens'],
            'truth_lens': lens_data['truth_lens'],
            'will_lens': lens_data['will_lens'],
        },
        'harmonic_concordance': lens_data['harmonic_concordance'],
        'prismatic_gloss': prismatic_gloss,
        'social_exchange_actuation': social_strategy,
    }


def evaluate_kaleidoscopic_corpus(compiled_rules, examples):
    """Evaluates SemCor examples producing full kaleidoscopic records unassisted."""
    records = []
    for ex in examples:
        item = {
            'id': ex['example_id'],
            'tokens': ex['surface_tokens'],
            'target_indices': [ex['target_index']],
        }
        pred = pd.predict_item(compiled_rules, item)
        raw_priming = mp.compute_priming_dials(pred)
        regulation = mr.compute_homeostatic_regulation(raw_priming, pred)
        funnel = tf.compute_tripartite_funnel(regulation['all_24_canonical_leaf_dials'], pred)
        kaleidoscope = compute_kaleidoscopic_response(funnel, regulation, pred)

        records.append({
            'example_id': ex['example_id'],
            'gold_sense_key': ex['target_sense_key'],
            'prediction': pred,
            'meditative_regulation': regulation,
            'tripartite_funnel': funnel,
            'kaleidoscopic_response': kaleidoscope,
        })
    return records


def run_kaleidoscopic_study(checkpoints, dev_path, output_dir=None):
    """Runs the full Kaleidoscopic study enforcing Rule D004 matched ordinary memory baseline parity."""
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

    all_rows = strict_json(dev_file.read_text(encoding='utf-8'))

    all_primary_records = []
    all_memory_records = []
    checkpoint_hashes = {}

    for cp in checkpoint_list:
        store = Store(cp.parent)
        primary_state = store.read()
        memory_state = strict_json(cp.read_text(encoding='utf-8'))['state']

        if digest(primary_state) != digest(memory_state):
            raise ValueError(f'consumer parity failure at state read for {cp}')

        all_primary_records.extend(primary_state['records'])
        all_memory_records.extend(memory_state['records'])
        checkpoint_hashes[str(cp)] = hashlib.sha256(cp.read_bytes()).hexdigest()

    primary_rules = pd.compile_rules(all_primary_records, all_rows)
    memory_rules = pd.compile_rules(all_memory_records, all_rows)

    if digest(primary_rules) != digest(memory_rules):
        raise ValueError('consumer parity failure at rule compilation')

    primary_results = evaluate_kaleidoscopic_corpus(primary_rules, all_rows)
    memory_results = evaluate_kaleidoscopic_corpus(memory_rules, all_rows)

    if digest(primary_results) != digest(memory_results):
        raise ValueError('consumer parity failure at kaleidoscopic evaluation')

    register_counts = {}
    concordance_sum = 0.0

    for r in primary_results:
        k = r['kaleidoscopic_response']
        if not k['epistemic_abstention']:
            reg = k['social_exchange_actuation']['speaking_register']
            register_counts[reg] = register_counts.get(reg, 0) + 1
            concordance_sum += k['harmonic_concordance']

    total_active = len([r for r in primary_results if not r['kaleidoscopic_response']['epistemic_abstention']])
    avg_concordance = round(concordance_sum / total_active, 3) if total_active > 0 else 0.0

    summary = {
        'kind': KIND,
        'checkpoint_hashes': checkpoint_hashes,
        'development_sha256': hashlib.sha256(dev_file.read_bytes()).hexdigest(),
        'total_instances_evaluated': len(primary_results),
        'consumer_parity': True,
        'evaluation_digest': digest(primary_results),
        'speaking_register_distribution': register_counts,
        'average_harmonic_concordance': avg_concordance,
        'samples': primary_results[:5],
    }

    if output_dir:
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        atomic_json(out_p / 'kaleidoscopic_summary.json', summary)
        atomic_json(out_p / 'full_kaleidoscopic_records.json', primary_results)

    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', nargs='+', required=True)
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    res = run_kaleidoscopic_study(args.checkpoint, args.dev_export, args.output_dir)
    print(pd.canonical(res))
