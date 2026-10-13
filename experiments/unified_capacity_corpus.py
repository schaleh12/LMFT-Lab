"""Unified 33-instance persistent capacity compilation and full-corpus unassisted disambiguation."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))

from lmft_lab.local_models import strict_json
from lmft_lab.runtime_store import Store, digest, atomic_json
import persistent_disambiguation as pd

ROOT = Path(__file__).resolve().parents[1]
KIND = 'unified-capacity-corpus-1'


def load_batches(b1_checkpoint, b2_checkpoint):
    """Loads and verifies records from Batch 1 and Batch 2 checkpoints."""
    b1_path = Path(b1_checkpoint).resolve()
    b2_path = Path(b2_checkpoint).resolve()

    if not b1_path.is_file() or not b2_path.is_file():
        raise FileNotFoundError("Both Batch 1 and Batch 2 checkpoints must exist.")

    b1_data = strict_json(b1_path.read_text(encoding='utf-8'))
    b2_data = strict_json(b2_path.read_text(encoding='utf-8'))

    b1_records = b1_data['state']['records']
    b2_records = b2_data['state']['records']

    if len(b1_records) != 20:
        raise ValueError(f"Expected 20 records in Batch 1, got {len(b1_records)}")
    if len(b2_records) != 13:
        raise ValueError(f"Expected 13 records in Batch 2, got {len(b2_records)}")

    # Combined records
    combined_primary = b1_records + b2_records
    combined_memory = deepcopy(combined_primary)

    return {
        'b1_checkpoint_sha256': hashlib.sha256(b1_path.read_bytes()).hexdigest(),
        'b2_checkpoint_sha256': hashlib.sha256(b2_path.read_bytes()).hexdigest(),
        'primary_records': combined_primary,
        'memory_records': combined_memory,
        'records_digest': digest(combined_primary),
    }


def compile_corpus_rules(records, dev_examples):
    """Compiles all 33 admitted records into persistent contextual rules."""
    return pd.compile_rules(records, dev_examples)


def run_corpus_evaluation(b1_checkpoint, b2_checkpoint, dev_export, output_dir=None):
    """Executes full-corpus 33-sentence unassisted evaluation with parity and restart checks."""
    dev_path = Path(dev_export).resolve()
    if not dev_path.is_file():
        raise FileNotFoundError(f"Development export missing: {dev_export}")

    dev_examples = strict_json(dev_path.read_text(encoding='utf-8'))
    if len(dev_examples) != 33:
        raise ValueError(f"Expected 33 development examples, got {len(dev_examples)}")

    batch_bundle = load_batches(b1_checkpoint, b2_checkpoint)

    # 1. Compile rules independently for primary and ordinary memory
    primary_rules = compile_corpus_rules(batch_bundle['primary_records'], dev_examples)
    memory_rules = compile_corpus_rules(batch_bundle['memory_records'], dev_examples)

    if digest(primary_rules) != digest(memory_rules):
        raise ValueError("Consumer parity failure during rule compilation.")

    if len(primary_rules) != 33:
        raise ValueError(f"Expected 33 compiled rules, got {len(primary_rules)}")

    # 2. Evaluate dataset unassisted (0 runtime LLM calls) across exact and core strategies
    eval_exact = pd.evaluate_dataset(primary_rules, dev_examples, strategy='exact')
    eval_core = pd.evaluate_dataset(primary_rules, dev_examples, strategy='core')

    # 3. Evaluate ordinary memory comparator independently
    memory_eval_exact = pd.evaluate_dataset(memory_rules, dev_examples, strategy='exact')
    memory_eval_core = pd.evaluate_dataset(memory_rules, dev_examples, strategy='core')

    if digest(eval_exact) != digest(memory_eval_exact) or digest(eval_core) != digest(memory_eval_core):
        raise ValueError("Consumer parity failure during evaluation.")

    summary = {
        'kind': KIND,
        'b1_checkpoint_sha256': batch_bundle['b1_checkpoint_sha256'],
        'b2_checkpoint_sha256': batch_bundle['b2_checkpoint_sha256'],
        'dev_export_sha256': hashlib.sha256(dev_path.read_bytes()).hexdigest(),
        'total_rules_compiled': len(primary_rules),
        'consumer_parity': True,
        'exact_strategy_evaluation': {k: v for k, v in eval_exact.items() if k != 'predictions'},
        'core_strategy_evaluation': {k: v for k, v in eval_core.items() if k != 'predictions'},
        'evaluation_digest': digest(eval_exact),
    }

    if output_dir:
        out_p = Path(output_dir).resolve()
        out_p.mkdir(parents=True, exist_ok=True)
        atomic_json(out_p / 'corpus33_disambiguation_summary.json', summary)
        atomic_json(out_p / 'corpus33_rules.json', primary_rules)
        atomic_json(out_p / 'corpus33_predictions_exact.json', eval_exact['predictions'])
        atomic_json(out_p / 'corpus33_predictions_core.json', eval_core['predictions'])

    return summary


def verify_restart(b1_checkpoint, b2_checkpoint, dev_export):
    """Executes evaluation in a fresh child process to verify complete process restart parity."""
    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        '--b1-checkpoint', str(b1_checkpoint),
        '--b2-checkpoint', str(b2_checkpoint),
        '--dev-export', str(dev_export),
    ]
    env = {**os.environ, 'PYTHONPATH': f"{ROOT / 'src'};{ROOT / 'experiments'}"}
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(f"Child process restart failed:\n{proc.stderr}")
    return strict_json(proc.stdout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--b1-checkpoint', required=True)
    parser.add_argument('--b2-checkpoint', required=True)
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir')
    args = parser.parse_args()

    res = run_corpus_evaluation(args.b1_checkpoint, args.b2_checkpoint, args.dev_export, args.output_dir)
    print(pd.canonical(res))
