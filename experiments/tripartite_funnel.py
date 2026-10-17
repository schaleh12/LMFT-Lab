"""Tripartite Psychological Funnel Engine for LMFT.

Formally connects the 3 founding branches into the Psychological leaf nodes:
1. Cultural (Efficiency, Justice, Freedom) -> Will (Intention, Execution)
2. Philosophical (Being, Structure, Persistence) -> Truth (Theory, Fact)
3. Experiential (Reflection, Phase, Synchronization) -> Contemplation (Clarity, Confidence)

All 24 leaf nodes are strictly verified against the frozen canonical seed in birth.py (Rule D001).
Evaluated in parallel with matched ordinary structured memory (Rule D004).
"""
import argparse
import hashlib
import json
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

ROOT = Path(__file__).resolve().parents[1]
KIND = 'tripartite-funnel-1'


def verify_canonical_leaves():
    """Verify that all 24 leaf nodes match birth.py canonical inventory."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    expected = set(mr.CANONICAL_LEAF_MAP.keys())
    if inventory_leaf_ids != expected:
        raise ValueError(f"Canonical inventory divergence: expected {expected}, got {inventory_leaf_ids}")


verify_canonical_leaves()


def transform_cultural_to_will(cultural_dials):
    """Transforms Cultural leaves (Efficiency, Justice, Freedom) into Will leaves (Intention, Execution)."""
    p = cultural_dials.get('cultural/efficiency/power', 0.5)
    w = cultural_dials.get('cultural/efficiency/wastelessness', 0.5)
    h = cultural_dials.get('cultural/justice/honor', 0.5)
    f = cultural_dials.get('cultural/justice/fairness', 0.5)
    s = cultural_dials.get('cultural/freedom/self-sufficiency', 0.5)
    n = cultural_dials.get('cultural/freedom/needlessness', 0.5)

    # Intention: moral resolve and virtue-alignment to act decisively
    intention = round(min(1.0, 0.40 * h + 0.30 * s + 0.20 * p + 0.10 * f), 3)

    # Execution: disciplined enactment minimizing systemic waste
    execution = round(min(1.0, 0.45 * w + 0.35 * (p * intention) + 0.20 * n), 3)

    return {
        'psychological/will/intention': intention,
        'psychological/will/execution': execution,
        'will_posture_descriptor': (
            'Noble Resolute Action' if intention > 0.7 and execution > 0.6
            else 'Prudent Deliberation' if intention > 0.5
            else 'Latent Readiness'
        ),
    }


def transform_philosophical_to_truth(philosophical_dials, prediction):
    """Transforms Philosophical leaves (Being, Structure, Persistence) into Truth leaves (Theory, Fact)."""
    a = philosophical_dials.get('philosophical/being/agency', 0.5)
    x = philosophical_dials.get('philosophical/being/existence', 0.5)
    o = philosophical_dials.get('philosophical/structure/order', 0.5)
    k = philosophical_dials.get('philosophical/structure/chaos', 0.5)
    c = philosophical_dials.get('philosophical/persistence/continuity', 0.5)
    d = philosophical_dials.get('philosophical/persistence/discreteness', 0.5)

    theory_text = prediction.get('explanation', '')
    has_theory = bool(theory_text and theory_text != 'No matching persistent contextual anchor.')
    
    # Theory: high-level explanatory framing and perspective
    if has_theory:
        theory_score = round(min(1.0, 0.50 * o + 0.30 * c + 0.20 * a + 0.10), 3)
    else:
        theory_score = 0.10

    # Fact: deterministic syntactic collocate anchor verification
    is_anchored = prediction.get('decision') == 'single' and bool(prediction.get('selected_sense'))
    fact_score = 1.00 if is_anchored else 0.00

    return {
        'psychological/truth/theory': theory_score,
        'psychological/truth/fact': fact_score,
        'theory_text': theory_text if has_theory else 'Hypothesis withheld',
        'truth_epistemic_grade': (
            'Empirically Grounded Truth' if (theory_score > 0.6 and fact_score == 1.0)
            else 'Unanchored Conjecture' if (theory_score > 0.6 and fact_score < 1.0)
            else 'Awaiting Observation'
        ),
    }


def transform_experiential_to_contemplation(experiential_dials):
    """Transforms Experiential leaves (Reflection, Phase, Synchronization) into Contemplation leaves."""
    nov = experiential_dials.get('experiential/reflection/novelty', 0.15)
    sal = experiential_dials.get('experiential/reflection/salience', 0.5)
    val = experiential_dials.get('experiential/phase/valence', 0.5)
    aro = experiential_dials.get('experiential/phase/arousal', 0.5)
    res = experiential_dials.get('experiential/synchronization/resonance', 0.5)
    ret = experiential_dials.get('experiential/synchronization/entrainment', 0.5)

    # Clarity: how sharply defined the digested sensory signal is (damping erratic arousal)
    stability = 1.0 - abs(aro - 0.5)
    clarity = round(min(1.0, max(0.1, 0.50 * res + 0.30 * stability + 0.20 * sal)), 3)

    # Confidence: persistent retention and affective resonance
    confidence = round(min(1.0, 0.60 * ret + 0.40 * res), 3)

    return {
        'psychological/contemplation/clarity': clarity,
        'psychological/contemplation/confidence': confidence,
        'contemplation_state_descriptor': (
            'Luminous Clarity' if clarity > 0.7 and confidence > 0.8
            else 'Focused Poise' if clarity > 0.5
            else 'Diffused Stasis'
        ),
    }


def compute_tripartite_funnel(full_24_leaf_dials, prediction):
    """Executes the complete Tripartite Psychological Funnel transformation across all 4 domains."""
    if prediction.get('decision') == 'abstain' or not prediction.get('selected_sense'):
        return {
            'epistemic_abstention': True,
            'funnel_status': 'quiescent_stasis',
            'will_funnel': {
                'psychological/will/intention': 0.0,
                'psychological/will/execution': 0.0,
                'will_posture_descriptor': 'Latent Readiness',
            },
            'truth_funnel': {
                'psychological/truth/theory': 0.1,
                'psychological/truth/fact': 0.0,
                'theory_text': 'Hypothesis withheld',
                'truth_epistemic_grade': 'Awaiting Observation',
            },
            'contemplation_funnel': {
                'psychological/contemplation/clarity': 1.0,
                'psychological/contemplation/confidence': 0.0,
                'contemplation_state_descriptor': 'Diffused Stasis',
            },
            'unified_psychological_cluster': {
                'psychological/will/intention': 0.0,
                'psychological/will/execution': 0.0,
                'psychological/truth/theory': 0.1,
                'psychological/truth/fact': 0.0,
                'psychological/contemplation/clarity': 1.0,
                'psychological/contemplation/confidence': 0.0,
            },
        }

    will = transform_cultural_to_will(full_24_leaf_dials)
    truth = transform_philosophical_to_truth(full_24_leaf_dials, prediction)
    contemplation = transform_experiential_to_contemplation(full_24_leaf_dials)

    psych_cluster = {
        'psychological/will/intention': will['psychological/will/intention'],
        'psychological/will/execution': will['psychological/will/execution'],
        'psychological/truth/theory': truth['psychological/truth/theory'],
        'psychological/truth/fact': truth['psychological/truth/fact'],
        'psychological/contemplation/clarity': contemplation['psychological/contemplation/clarity'],
        'psychological/contemplation/confidence': contemplation['psychological/contemplation/confidence'],
    }

    return {
        'epistemic_abstention': False,
        'funnel_status': 'active_funnel_convergence',
        'will_funnel': will,
        'truth_funnel': truth,
        'contemplation_funnel': contemplation,
        'unified_psychological_cluster': psych_cluster,
        'funnel_synthesis': (
            f"Under {contemplation['contemplation_state_descriptor']} (Clarity={psych_cluster['psychological/contemplation/clarity']}), "
            f"the system synthesizes {truth['truth_epistemic_grade']} (Fact={psych_cluster['psychological/truth/fact']}) "
            f"into {will['will_posture_descriptor']} (Execution={psych_cluster['psychological/will/execution']})."
        ),
    }


def evaluate_tripartite_funnel(compiled_rules, examples):
    """Evaluates SemCor examples producing complete tripartite funnel records unassisted."""
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
        funnel = compute_tripartite_funnel(regulation['all_24_canonical_leaf_dials'], pred)

        records.append({
            'example_id': ex['example_id'],
            'gold_sense_key': ex['target_sense_key'],
            'prediction': pred,
            'meditative_regulation': regulation,
            'tripartite_funnel': funnel,
        })
    return records


def run_tripartite_study(checkpoints, dev_path, output_dir=None):
    """Executes the Tripartite Funnel Study enforcing Rule D004 matched ordinary memory parity."""
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

    primary_results = evaluate_tripartite_funnel(primary_rules, all_rows)
    memory_results = evaluate_tripartite_funnel(memory_rules, all_rows)

    if digest(primary_results) != digest(memory_results):
        raise ValueError('consumer parity failure at funnel evaluation')

    will_postures = {}
    epistemic_grades = {}
    contemplation_states = {}

    for r in primary_results:
        f = r['tripartite_funnel']
        if not f['epistemic_abstention']:
            wp = f['will_funnel']['will_posture_descriptor']
            eg = f['truth_funnel']['truth_epistemic_grade']
            cs = f['contemplation_funnel']['contemplation_state_descriptor']
            will_postures[wp] = will_postures.get(wp, 0) + 1
            epistemic_grades[eg] = epistemic_grades.get(eg, 0) + 1
            contemplation_states[cs] = contemplation_states.get(cs, 0) + 1

    summary = {
        'kind': KIND,
        'checkpoint_hashes': checkpoint_hashes,
        'development_sha256': hashlib.sha256(dev_file.read_bytes()).hexdigest(),
        'total_instances_evaluated': len(primary_results),
        'consumer_parity': True,
        'evaluation_digest': digest(primary_results),
        'will_posture_distribution': will_postures,
        'epistemic_grade_distribution': epistemic_grades,
        'contemplation_state_distribution': contemplation_states,
        'canonical_domains_verified': ['cultural', 'philosophical', 'experiential', 'psychological'],
        'canonical_leaf_nodes_verified': list(mr.CANONICAL_LEAF_MAP.keys()),
        'samples': primary_results[:5],
    }

    if output_dir:
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        atomic_json(out_p / 'tripartite_funnel_summary.json', summary)
        atomic_json(out_p / 'full_tripartite_funnel_records.json', primary_results)

    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', nargs='+', required=True)
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    res = run_tripartite_study(args.checkpoint, args.dev_export, args.output_dir)
    print(pd.canonical(res))
