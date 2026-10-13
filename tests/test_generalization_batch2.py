"""Tests for Batch 2 generalization benchmark."""
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
import generalization_batch2 as gb
import persistent_disambiguation as pd


def test_batch2_generalization_study_integration(tmp_path):
    checkpoint = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json')
    dev_export = Path(r'C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json')

    if not checkpoint.exists() or not dev_export.exists():
        pytest.skip('External archive files not found on local path')

    summary = gb.run_batch2_generalization(checkpoint, dev_export, output_dir=tmp_path)

    assert summary['kind'] == 'generalization-batch2-1'
    assert summary['batch2_cases_evaluated'] == 13
    assert summary['compiled_rules_count'] == 20
    assert summary['consumer_parity'] is True

    core = summary['core_strategy_metrics']
    assert core['total_cases'] == 13
    assert core['correct_singletons'] == 0
    assert core['wrong_singletons'] == 0
    assert core['abstentions'] == 13
    assert core['ambiguities'] == 0
    assert core['false_positive_rate'] == 0.0

    assert (tmp_path / 'generalization_summary.json').exists()
    assert (tmp_path / 'predictions.json').exists()


def test_batch2_synthetic_generalization():
    rules = [
        {
            'rule_id': 'rule-synthetic-1',
            'target_sense_key': 'order%1:07:01::',
            'exact_quote': 'on the order of',
            'core_pattern': 'on the order of',
            'gloss': 'a level or magnitude',
            'witnesses': ['w1'],
        }
    ]

    unseen_item = {
        'id': 'unseen-item-1',
        'tokens': ['The', 'galaxy', 'is', 'on', 'the', 'order', 'of', 'ten', 'light_years', 'across', '.'],
        'target_indices': [5],
    }

    pred = pd.predict_item(rules, unseen_item)
    assert pred['decision'] == 'single'
    assert pred['selected_sense'] == 'order%1:07:01::'
    assert pred['explanation'] == 'a level or magnitude'
