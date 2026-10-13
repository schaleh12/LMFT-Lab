"""Tests for unassisted persistent contextual disambiguation engine."""
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
import persistent_disambiguation as pd


def synthetic_rules():
    return [
        {
            'rule_id': 'rule-1',
            'source_record_id': 'rep-1',
            'target_sense_key': 'sense-magnitude',
            'exact_quote': 'on the order of 3%',
            'core_pattern': 'on the order of',
            'gloss': 'a level or magnitude',
            'witnesses': ['rep-1', 'ex-1'],
        },
        {
            'rule_id': 'rule-2',
            'source_record_id': 'rep-2',
            'target_sense_key': 'sense-court',
            'exact_quote': 'order of the court',
            'core_pattern': 'order of the court',
            'gloss': 'a judicial decree',
            'witnesses': ['rep-2', 'ex-2'],
        },
    ]


def test_validate_public_item_valid():
    valid = {'id': 'test-1', 'tokens': ['Please', 'examine', 'order', '.'], 'target_indices': [2]}
    pd.validate_public_item(valid)


@pytest.mark.parametrize('bad_item', [
    {'id': 'test-1', 'tokens': ['a']},  # missing target_indices
    {'id': 'test-1', 'tokens': ['a'], 'target_indices': [0], 'gold': 'leak'},  # gold leak / extra key
    {'id': '', 'tokens': ['a'], 'target_indices': [0]},  # empty id
    {'id': 'test-1', 'tokens': [], 'target_indices': [0]},  # empty tokens
    {'id': 'test-1', 'tokens': ['a'], 'target_indices': []},  # empty target_indices
])
def test_validate_public_item_invalid(bad_item):
    with pytest.raises(ValueError, match='invalid'):
        pd.validate_public_item(bad_item)


def test_predict_item_single_match():
    rules = synthetic_rules()
    item = {'id': 'item-1', 'tokens': ['increases', 'are', 'on', 'the', 'order', 'of', '5%'], 'target_indices': [4]}
    pred = pd.predict_item(rules, item)

    assert pred['decision'] == 'single'
    assert pred['selected_sense'] == 'sense-magnitude'
    assert pred['explanation'] == 'a level or magnitude'
    assert 'rep-1' in pred['witnesses']


def test_predict_item_abstain():
    rules = synthetic_rules()
    item = {'id': 'item-2', 'tokens': ['a', 'completely', 'unrelated', 'sentence', 'here'], 'target_indices': [2]}
    pred = pd.predict_item(rules, item)

    assert pred['decision'] == 'abstain'
    assert pred['selected_sense'] is None
    assert pred['matched_senses'] == []


def test_predict_item_ambiguous():
    rules = synthetic_rules()
    # Sentence containing both patterns
    item = {'id': 'item-3', 'tokens': ['on', 'the', 'order', 'of', 'an', 'order', 'of', 'the', 'court'], 'target_indices': [2, 5]}
    pred = pd.predict_item(rules, item)

    assert pred['decision'] == 'ambiguous'
    assert pred['selected_sense'] is None
    assert len(pred['matched_senses']) == 2
    assert 'sense-magnitude' in pred['matched_senses']
    assert 'sense-court' in pred['matched_senses']


def test_evaluate_dataset_synthetic():
    rules = synthetic_rules()
    examples = [
        {'example_id': 'ex-1', 'target_sense_key': 'sense-magnitude', 'surface_tokens': ['on', 'the', 'order', 'of', '10%'], 'target_index': 4},
        {'example_id': 'ex-2', 'target_sense_key': 'sense-court', 'surface_tokens': ['by', 'order', 'of', 'the', 'court'], 'target_index': 1},
        {'example_id': 'ex-3', 'target_sense_key': 'sense-unknown', 'surface_tokens': ['just', 'an', 'apple'], 'target_index': 2},
    ]

    res = pd.evaluate_dataset(rules, examples)
    assert res['total_cases'] == 3
    assert res['correct_singletons'] == 2
    assert res['wrong_singletons'] == 0
    assert res['abstentions'] == 1
    assert res['ambiguities'] == 0
    assert res['precision_on_fired'] == 1.0
    assert res['accuracy'] == 2 / 3


def test_run_disambiguation_study_integration(tmp_path):
    checkpoint = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v4-20261013-002\neutral-state\checkpoint.json')
    dev_export = Path(r'C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json')

    if not checkpoint.exists() or not dev_export.exists():
        pytest.skip('Research archives not available')

    summary = pd.run_disambiguation_study(checkpoint, dev_export, output_dir=tmp_path)

    assert summary['kind'] == 'persistent-disambiguation-1'
    assert summary['consumer_parity'] is True
    assert summary['compiled_rules_count'] == 4

    core = summary['eval_core_strategy']
    assert core['total_cases'] == 33
    assert core['wrong_singletons'] == 0
    assert core['precision_on_fired'] == 1.0
    assert core['correct_singletons'] >= 4
    assert (tmp_path / 'persistent_disambiguation_summary.json').exists()


def test_run_disambiguation_study_v5_batch1_integration(tmp_path):
    checkpoint = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json')
    dev_export = Path(r'C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json')

    if not checkpoint.exists() or not dev_export.exists():
        pytest.skip('Research archives not available')

    summary = pd.run_disambiguation_study(checkpoint, dev_export, output_dir=tmp_path)

    assert summary['kind'] == 'persistent-disambiguation-1'
    assert summary['consumer_parity'] is True
    assert summary['compiled_rules_count'] == 20

    core = summary['eval_core_strategy']
    assert core['total_cases'] == 33
    assert core['correct_singletons'] == 20
    assert core['wrong_singletons'] == 0
    assert core['abstentions'] == 13
    assert core['ambiguities'] == 0
    assert core['precision_on_fired'] == 1.0
    assert core['accuracy'] == 20 / 33
    assert (tmp_path / 'persistent_disambiguation_summary.json').exists()
    assert (tmp_path / 'full_predictions.json').exists()

