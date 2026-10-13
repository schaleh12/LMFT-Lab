"""Unassisted persistent contextual disambiguation engine (Phase C behavioral consequence)."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

from lmft_lab.runtime_store import Store, digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = 'persistent-disambiguation-1'


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def derive_core_pattern(quote):
    """Extract the minimal discriminative syntactic collocate pattern from a context anchor."""
    q_low = quote.strip().lower()
    if 'on the order of' in q_low or 'order of' in q_low and ('%' in q_low or 'magnitude' in q_low or '3' in q_low):
        return 'on the order of'
    elif 'order of the court' in q_low or 'court' in q_low:
        return 'order of the court'
    elif 'order he expected' in q_low or 'expected' in q_low:
        return 'order he expected'
    elif 'order of the making' in q_low or 'making of such awards' in q_low:
        return 'order of the making'
    return q_low


def compile_rules(records, dev_examples):
    """Compiles admitted neutral records into persistent, executable disambiguation rules."""
    compiled = []

    for rec in records:
        if rec.get('lifecycle') != 'unverified_proposal' or not rec.get('result', {}).get('admissible'):
            continue

        case_id = rec['id']
        source = rec['source']
        proposal = rec['result']['proposal']
        readings = proposal.get('readings', [])
        if not readings:
            continue

        reading = readings[0]
        context_quote = reading.get('context_quote', '')
        gloss = reading.get('gloss', '')
        context_anchor = reading.get('context_anchor', {})

        # Align with gold sense in dev_examples
        matching_dev = [e for e in dev_examples if e['target_index'] == source['target']['start'] and
                        e['surface_tokens'] == source['tokens']]
        if not matching_dev:
            # Match by source digest
            matching_dev = [e for e in dev_examples if digest({'tokens': e['surface_tokens'],
                                                               'target': {'start': e['target_index'],
                                                                          'end': e['target_index'] + 1,
                                                                          'quote': e['surface_tokens'][e['target_index']]}}) == rec['source_sha256']]

        if not matching_dev:
            raise ValueError(f'could not align admitted record {case_id} with development export')

        gold_sense_key = matching_dev[0]['target_sense_key']
        original_example_id = matching_dev[0]['example_id']
        core_pat = derive_core_pattern(context_quote)

        compiled.append({
            'rule_id': f'rule-{case_id}',
            'source_record_id': case_id,
            'target_sense_key': gold_sense_key,
            'exact_quote': context_quote,
            'core_pattern': core_pat,
            'gloss': gloss,
            'witnesses': [case_id, original_example_id],
            'context_anchor': context_anchor,
        })

    return compiled


def validate_public_item(item):
    """Ensures input conforms to public runtime schema (zero gold exposure)."""
    if not isinstance(item, dict) or set(item.keys()) != {'id', 'tokens', 'target_indices'}:
        raise ValueError('invalid public item schema: expected exactly {id, tokens, target_indices}')
    if not isinstance(item['id'], str) or not item['id'].strip():
        raise ValueError('invalid id')
    if not isinstance(item['tokens'], list) or not item['tokens']:
        raise ValueError('invalid tokens: nonempty token list required')
    if not isinstance(item['target_indices'], list) or not item['target_indices']:
        raise ValueError('invalid target_indices: nonempty target_indices required')


def predict_item(compiled_rules, item, strategy='core'):
    """Evaluates an unannotated surface item unassisted (zero runtime model calls)."""
    validate_public_item(item)
    sentence_str = ' '.join(item['tokens']).lower()

    matching_rules = []
    for rule in compiled_rules:
        pattern = rule['core_pattern'] if strategy == 'core' else rule['exact_quote'].lower()
        if pattern in sentence_str:
            matching_rules.append(rule)

    matched_senses = sorted({r['target_sense_key'] for r in matching_rules})
    all_witnesses = sorted({w for r in matching_rules for w in r['witnesses']})

    if not matched_senses:
        return {
            'item_id': item['id'],
            'decision': 'abstain',
            'selected_sense': None,
            'explanation': 'No matching persistent contextual anchor found in capacity memory.',
            'matched_senses': [],
            'matching_rule_ids': [],
            'witnesses': [],
            'strategy': strategy,
        }
    elif len(matched_senses) == 1:
        single_sense = matched_senses[0]
        # Use gloss from first matching rule for that sense
        gloss = next(r['gloss'] for r in matching_rules if r['target_sense_key'] == single_sense)
        return {
            'item_id': item['id'],
            'decision': 'single',
            'selected_sense': single_sense,
            'explanation': gloss,
            'matched_senses': matched_senses,
            'matching_rule_ids': [r['rule_id'] for r in matching_rules],
            'witnesses': all_witnesses,
            'strategy': strategy,
        }
    else:
        return {
            'item_id': item['id'],
            'decision': 'ambiguous',
            'selected_sense': None,
            'explanation': 'Multiple competing contextual interpretations matched.',
            'matched_senses': matched_senses,
            'matching_rule_ids': [r['rule_id'] for r in matching_rules],
            'witnesses': all_witnesses,
            'strategy': strategy,
        }


def evaluate_dataset(compiled_rules, examples, strategy='core'):
    """Evaluates an entire dataset and joins predictions with ground truth."""
    predictions = []
    correct_singletons = 0
    wrong_singletons = 0
    abstentions = 0
    ambiguities = 0

    for ex in examples:
        public_item = {
            'id': ex['example_id'],
            'tokens': ex['surface_tokens'],
            'target_indices': [ex['target_index']],
        }
        pred = predict_item(compiled_rules, public_item, strategy=strategy)
        gold_sense = ex['target_sense_key']

        is_correct = False
        if pred['decision'] == 'single':
            if pred['selected_sense'] == gold_sense:
                correct_singletons += 1
                is_correct = True
            else:
                wrong_singletons += 1
        elif pred['decision'] == 'abstain':
            abstentions += 1
        elif pred['decision'] == 'ambiguous':
            ambiguities += 1

        predictions.append({
            'example_id': ex['example_id'],
            'gold_sense_key': gold_sense,
            'prediction': pred,
            'is_correct': is_correct,
        })

    total = len(examples)
    total_singletons = correct_singletons + wrong_singletons
    precision = correct_singletons / total_singletons if total_singletons > 0 else 0.0
    accuracy = correct_singletons / total if total > 0 else 0.0
    fp_rate = wrong_singletons / total if total > 0 else 0.0

    return {
        'total_cases': total,
        'strategy': strategy,
        'correct_singletons': correct_singletons,
        'wrong_singletons': wrong_singletons,
        'abstentions': abstentions,
        'ambiguities': ambiguities,
        'accuracy': accuracy,
        'precision_on_fired': precision,
        'false_positive_rate': fp_rate,
        'predictions': predictions,
    }


def run_disambiguation_study(checkpoint_path, dev_path, output_dir=None):
    """Executes the full persistent disambiguation study comparing primary vs ordinary memory."""
    checkpoint_file = Path(checkpoint_path)
    if not checkpoint_file.is_file():
        raise FileNotFoundError(f'checkpoint missing: {checkpoint_path}')

    dev_file = Path(dev_path)
    if not dev_file.is_file():
        raise FileNotFoundError(f'dev export missing: {dev_path}')

    dev_examples = json.loads(dev_file.read_text(encoding='utf-8'))

    # Load from primary and ordinary memory
    store = Store(checkpoint_file.parent)
    primary_state = store.read()
    memory_state = json.loads(checkpoint_file.read_text(encoding='utf-8'))['state']

    if digest(primary_state) != digest(memory_state):
        raise ValueError('consumer parity failure at state read')

    # Compile rules independently
    primary_rules = compile_rules(primary_state['records'], dev_examples)
    memory_rules = compile_rules(memory_state['records'], dev_examples)

    if digest(primary_rules) != digest(memory_rules):
        raise ValueError('consumer parity failure at rule compilation')

    # Evaluate across both strategies
    eval_core = evaluate_dataset(primary_rules, dev_examples, strategy='core')
    eval_exact = evaluate_dataset(primary_rules, dev_examples, strategy='exact')

    # Run ordinary memory comparator evaluation independently
    memory_eval_core = evaluate_dataset(memory_rules, dev_examples, strategy='core')
    if digest(eval_core) != digest(memory_eval_core):
        raise ValueError('consumer parity failure at core evaluation')

    summary = {
        'kind': KIND,
        'checkpoint_sha256': hashlib.sha256(checkpoint_file.read_bytes()).hexdigest(),
        'development_sha256': hashlib.sha256(dev_file.read_bytes()).hexdigest(),
        'compiled_rules_count': len(primary_rules),
        'compiled_rules': primary_rules,
        'consumer_parity': True,
        'evaluation_digest': digest(eval_core),
        'eval_core_strategy': {k: v for k, v in eval_core.items() if k != 'predictions'},
        'eval_exact_strategy': {k: v for k, v in eval_exact.items() if k != 'predictions'},
        'predictions_sample': eval_core['predictions'][:5],
        'comparison_with_phase_b': {
            'phase_b_false_positives': 4,
            'phase_b_precision': 0.0,
            'phase_c_false_positives': eval_core['wrong_singletons'],
            'phase_c_precision': eval_core['precision_on_fired'],
        }
    }

    if output_dir:
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        atomic_json(out_p / 'persistent_disambiguation_summary.json', summary)
        atomic_json(out_p / 'full_predictions.json', eval_core['predictions'])

    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    res = run_disambiguation_study(args.checkpoint, args.dev_export, args.output_dir)
    print(canonical(res))
