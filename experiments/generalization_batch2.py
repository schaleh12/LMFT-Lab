"""Generalization benchmark evaluating Batch 1 persistent capacity memory on unseen Batch 2."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

from lmft_lab.runtime_store import Store, digest, atomic_json
import persistent_disambiguation as pd

KIND = 'generalization-batch2-1'


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def run_batch2_generalization(checkpoint_path, dev_path, output_dir=None):
    """Executes unassisted generalization evaluation on unseen SemCor Batch 2 instances."""
    checkpoint_file = Path(checkpoint_path)
    if not checkpoint_file.is_file():
        raise FileNotFoundError(f'checkpoint missing: {checkpoint_path}')

    dev_file = Path(dev_path)
    if not dev_file.is_file():
        raise FileNotFoundError(f'dev export missing: {dev_path}')

    all_rows = json.loads(dev_file.read_text(encoding='utf-8'))
    batch2_examples = [r for r in all_rows if r.get('stage') == 'development_batch_2']
    if len(batch2_examples) != 13:
        raise ValueError(f'expected exactly 13 development_batch_2 examples, found {len(batch2_examples)}')

    # Sort deterministically
    batch2_examples = sorted(batch2_examples, key=lambda r: r['example_id'])

    # Primary consumer
    store = Store(checkpoint_file.parent)
    primary_state = store.read()
    memory_state = json.loads(checkpoint_file.read_text(encoding='utf-8'))['state']

    if digest(primary_state) != digest(memory_state):
        raise ValueError('consumer parity failure at state read')

    # Compile rules from Batch 1 neutral records
    primary_rules = pd.compile_rules(primary_state['records'], all_rows)
    memory_rules = pd.compile_rules(memory_state['records'], all_rows)

    if digest(primary_rules) != digest(memory_rules):
        raise ValueError('consumer parity failure at rule compilation')

    # Evaluate on unseen Batch 2 examples
    eval_core = pd.evaluate_dataset(primary_rules, batch2_examples, strategy='core')
    eval_exact = pd.evaluate_dataset(primary_rules, batch2_examples, strategy='exact')

    # Memory baseline comparator
    memory_eval_core = pd.evaluate_dataset(memory_rules, batch2_examples, strategy='core')
    if digest(eval_core) != digest(memory_eval_core):
        raise ValueError('consumer parity failure at core evaluation')

    summary = {
        'kind': KIND,
        'checkpoint_sha256': hashlib.sha256(checkpoint_file.read_bytes()).hexdigest(),
        'development_sha256': hashlib.sha256(dev_file.read_bytes()).hexdigest(),
        'compiled_rules_count': len(primary_rules),
        'batch2_cases_evaluated': len(batch2_examples),
        'consumer_parity': True,
        'evaluation_digest': digest(eval_core),
        'core_strategy_metrics': {k: v for k, v in eval_core.items() if k != 'predictions'},
        'exact_strategy_metrics': {k: v for k, v in eval_exact.items() if k != 'predictions'},
        'batch2_predictions': eval_core['predictions'],
    }

    if output_dir:
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        atomic_json(out_p / 'generalization_summary.json', summary)
        atomic_json(out_p / 'predictions.json', eval_core['predictions'])

    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    res = run_batch2_generalization(args.checkpoint, args.dev_export, args.output_dir)
    print(canonical(res))
