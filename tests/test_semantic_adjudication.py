"""Tests for semantic adjudication module."""
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
import semantic_adjudication as sa


def test_adjudicate_gloss_tautology():
    # Detects target word repetition
    res1 = sa.adjudicate_gloss("Payment according to the court's order.")
    assert res1['tautology_present'] is True
    assert res1['target_substituted'] is False
    assert res1['tautology_occurrences'] == 1

    res2 = sa.adjudicate_gloss("Curtailed all pending orders.")
    assert res2['tautology_present'] is True
    assert res2['target_substituted'] is False
    assert res2['tautology_occurrences'] == 1


def test_adjudicate_gloss_substitution():
    # Detects true semantic replacement
    res = sa.adjudicate_gloss("in the sequence of award creation")
    assert res['tautology_present'] is False
    assert res['target_substituted'] is True
    assert res['tautology_occurrences'] == 0
    assert res['char_length'] == len("in the sequence of award creation")
    assert res['token_count'] == 6


def test_adjudicate_gloss_invalid():
    with pytest.raises(ValueError, match='nonempty string gloss'):
        sa.adjudicate_gloss("")
    with pytest.raises(ValueError, match='nonempty string gloss'):
        sa.adjudicate_gloss(None)


def test_adjudicate_concordance_sequence():
    # Sequence sense: order%1:10:02::
    proposal_sub = {
        'readings': [{
            'gloss': 'in the sequence of award creation',
            'context_quote': 'in the order of the making of such awards',
        }]
    }
    res = sa.adjudicate_concordance('test-case', proposal_sub, 'order%1:10:02::')
    assert res['status'] == 'concordant'
    assert res['score'] == 2

    # Tautological sequence
    proposal_taut = {
        'readings': [{
            'gloss': 'arranged in order of priority',
            'context_quote': 'in the order of the making of such awards',
        }]
    }
    res_taut = sa.adjudicate_concordance('test-case', proposal_taut, 'order%1:10:02::')
    assert res_taut['status'] == 'partially_concordant'
    assert res_taut['score'] == 1


def test_adjudicate_concordance_magnitude():
    proposal = {
        'readings': [{
            'gloss': 'When increases are on the order of 3% per annum, resistance is less.',
            'context_quote': 'on the order of 3 % per_annum',
        }]
    }
    res = sa.adjudicate_concordance('test-case', proposal, 'order%1:07:01::')
    assert res['status'] == 'partially_concordant'
    assert res['score'] == 1


def test_adjudicate_concordance_unrecognized_sense():
    proposal = {'readings': [{'gloss': 'test', 'context_quote': 'test'}]}
    with pytest.raises(ValueError, match='unrecognized gold sense'):
        sa.adjudicate_concordance('test-case', proposal, 'order%9:99:99::')


def test_adjudicate_concordance_no_readings():
    proposal = {'readings': []}
    res = sa.adjudicate_concordance('test-case', proposal, 'order%1:07:01::')
    assert res['status'] == 'discordant'
    assert res['score'] == 0


def test_adjudicate_discriminability_synthetic():
    dev_examples = [
        {'example_id': 'ex-1', 'target_sense_key': 'sense-A', 'surface_tokens': ['on', 'the', 'order', 'of', '3%']},
        {'example_id': 'ex-2', 'target_sense_key': 'sense-A', 'surface_tokens': ['on', 'the', 'order', 'of', '5%']},
        {'example_id': 'ex-3', 'target_sense_key': 'sense-B', 'surface_tokens': ['court', 'issued', 'an', 'order']},
        {'example_id': 'ex-4', 'target_sense_key': 'sense-C', 'surface_tokens': ['an', 'order', 'for', 'goods']},
    ]

    res = sa.adjudicate_discriminability('on the order of', 'sense-A', dev_examples)
    assert res['true_positives'] == 2
    assert res['false_positives'] == 0
    assert res['false_negatives'] == 0
    assert res['precision'] == 1.0
    assert res['recall'] == 1.0
    assert res['false_positive_rate'] == 0.0

    # Pattern with false positives
    res_broad = sa.adjudicate_discriminability('order', 'sense-A', dev_examples)
    assert res_broad['true_positives'] == 2
    assert res_broad['false_positives'] == 2
    assert res_broad['precision'] == 0.5


def test_adjudicate_discriminability_no_matches():
    dev_examples = [
        {'example_id': 'ex-1', 'target_sense_key': 'sense-A', 'surface_tokens': ['a', 'b', 'c']},
    ]
    res = sa.adjudicate_discriminability('xyz', 'sense-A', dev_examples)
    assert res['matched_count'] == 0
    assert res['true_positives'] == 0
    assert res['precision'] == 0.0
    assert res['recall'] == 0.0


def test_run_adjudication_on_v3_results(tmp_path):
    checkpoint = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v3-20261013-001\neutral-state\checkpoint.json')
    dev_export = Path(r'C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json')

    if not checkpoint.exists() or not dev_export.exists():
        pytest.skip('External archive files not found on local path')

    summary = sa.run_adjudication(checkpoint, dev_export, output_dir=tmp_path)

    assert summary['kind'] == 'semantic-adjudication-1'
    assert summary['total_cases_adjudicated'] == 4
    assert summary['consumer_parity'] is True
    assert summary['aggregate_metrics']['concordant_cases'] == 1  # representation-04
    assert summary['aggregate_metrics']['partially_concordant_cases'] == 3  # cases 01, 02, 03
    assert summary['aggregate_metrics']['substituted_glosses'] == 1
    assert summary['aggregate_metrics']['tautological_glosses'] == 3
    assert summary['aggregate_metrics']['average_discriminative_precision'] == 1.0
    assert summary['aggregate_metrics']['total_false_positives'] == 0
    assert (tmp_path / 'adjudication_summary.json').exists()
