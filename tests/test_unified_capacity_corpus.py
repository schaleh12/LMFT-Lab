"""Tests for unified 33-instance capacity compilation and unassisted corpus disambiguation."""
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
import unified_capacity_corpus as ucc

B1_CHECKPOINT = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json')
B2_CHECKPOINT = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v6-20261013-001\neutral-state\checkpoint.json')
DEV_EXPORT = Path(r'C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json')


def test_load_batches():
    if not (B1_CHECKPOINT.exists() and B2_CHECKPOINT.exists()):
        pytest.skip("Research archives not found in local environment")

    bundle = ucc.load_batches(B1_CHECKPOINT, B2_CHECKPOINT)
    assert len(bundle['primary_records']) == 33
    assert len(bundle['memory_records']) == 33
    assert bundle['primary_records'] == bundle['memory_records']


def test_full_corpus_disambiguation(tmp_path):
    if not (B1_CHECKPOINT.exists() and B2_CHECKPOINT.exists() and DEV_EXPORT.exists()):
        pytest.skip("Research archives or dev export not found")

    summary = ucc.run_corpus_evaluation(B1_CHECKPOINT, B2_CHECKPOINT, DEV_EXPORT, output_dir=tmp_path)

    assert summary['total_rules_compiled'] == 33
    assert summary['consumer_parity'] is True

    exact_eval = summary['exact_strategy_evaluation']
    assert exact_eval['total_cases'] == 33
    assert exact_eval['correct_singletons'] == 33
    assert exact_eval['wrong_singletons'] == 0
    assert exact_eval['abstentions'] == 0
    assert exact_eval['ambiguities'] == 0
    assert exact_eval['precision_on_fired'] == 1.0
    assert exact_eval['false_positive_rate'] == 0.0

    core_eval = summary['core_strategy_evaluation']
    assert core_eval['total_cases'] == 33
    assert core_eval['correct_singletons'] == 33
    assert core_eval['wrong_singletons'] == 0
    assert core_eval['precision_on_fired'] == 1.0

    # Verify output files written
    assert (tmp_path / 'corpus33_disambiguation_summary.json').exists()
    assert (tmp_path / 'corpus33_rules.json').exists()
    assert (tmp_path / 'corpus33_predictions_exact.json').exists()


def test_corpus_restart_verification():
    if not (B1_CHECKPOINT.exists() and B2_CHECKPOINT.exists() and DEV_EXPORT.exists()):
        pytest.skip("Research archives or dev export not found")

    summary = ucc.run_corpus_evaluation(B1_CHECKPOINT, B2_CHECKPOINT, DEV_EXPORT)
    restart_res = ucc.verify_restart(B1_CHECKPOINT, B2_CHECKPOINT, DEV_EXPORT)

    assert restart_res['evaluation_digest'] == summary['evaluation_digest']
    assert restart_res['exact_strategy_evaluation']['correct_singletons'] == 33
