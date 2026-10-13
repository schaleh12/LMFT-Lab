"""Synthetic contract/transport tests for Protocol 5; no model or natural corpus access."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'experiments'))
import slm_representation_v5 as c
import run_slm_representation_v5 as runner
from lmft_lab.local_models import load_config
from lmft_lab.runtime_store import Store, digest


def source():
    return {'tokens': ['General', 'issued', 'an', 'order', 'to', 'advance', '.'],
            'target': {'start': 3, 'end': 4, 'quote': 'order'}}


def proposal():
    return {'schema_version': 1, 'status': 'one_reading', 'target': source()['target'],
            'readings': [{'gloss': 'an authoritative military directive or command',
                          'context_quote': 'issued an order to advance'}],
            'uncertainties': []}


def trace(raw):
    config = load_config(c.ROOT/'config/local_models.json')
    req = c.request(source(), config['generation'])
    return {'model': config['models']['qwen3_4b'], 'generation': config['generation'],
            'role': 'interpretation', 'request_sha256': hashlib.sha256(json.dumps(req, sort_keys=True).encode()).hexdigest(),
            'response': {'choices': [{'message': {'content': raw}, 'finish_reason': 'stop'}],
                        'usage': {'completion_tokens': 1}}, 'elapsed_seconds': 0.0}


def record(raw=None):
    raw = json.dumps(proposal()) if raw is None else raw
    return c.record('synthetic-1', source(), '0'*64, raw, trace(raw))


def test_valid_v5_proposal():
    raw = json.dumps(proposal())
    report = c.validation_report(raw, source())
    assert report['admissible'] is True
    assert report['errors'] == []
    anchor = report['proposal']['readings'][0]['context_anchor']
    assert anchor == {'start': 1, 'end': 6, 'quote': 'issued an order to advance'}


def test_v5_tautological_gloss_rejected():
    bad = proposal()
    bad['readings'][0]['gloss'] = 'An order to move forward.'
    report = c.validation_report(json.dumps(bad), source())
    assert report['admissible'] is False
    assert any('gloss tautology' in e for e in report['errors'])


def test_v5_consumer_parity(tmp_path):
    state = c.newborn()
    rec = record()
    state = c.append(state, rec)
    store = Store(tmp_path)
    store.commit(state)

    restored = store.read()
    p_view, m_view = c.consumer_views(restored['records'])
    assert p_view == m_view
    assert digest(p_view) == digest(m_view)


def test_v5_context_quote_missing_from_tokens():
    bad = proposal()
    bad['readings'][0]['context_quote'] = 'completely unrelated phrase not in sentence'
    report = c.validation_report(json.dumps(bad), source())
    assert report['admissible'] is False
    assert any('context_quote not found' in e for e in report['errors'])


def test_v5_multiple_context_matches_proximity():
    src = {'tokens': ['the', 'quick', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog', 'near', 'the', 'fence'],
           'target': {'start': 3, 'end': 4, 'quote': 'jumped'}}
    # 'the' appears at index 0, 5, 9. The match closest to target 'jumped' (index 3) is index 5 or 0.
    res = c.resolve_token_slice('the', src['tokens'], src['target'])
    assert res['start'] == 5 and res['end'] == 6


def test_v5_non_one_reading_rejected():
    bad = proposal()
    bad['status'] = 'multiple_readings'
    report = c.validation_report(json.dumps(bad), source())
    assert report['admissible'] is False
    assert any('invalid proposal status' in e for e in report['errors'])


def test_v5_select_batch1():
    dev_json = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\linguistic-application-v1-20261012-001\development.json')
    if dev_json.exists():
        rows = json.loads(dev_json.read_text(encoding='utf-8'))
        b1 = runner.select(rows)
        assert len(b1) == 20
        assert all(r['stage'] == 'development_batch_1' for r in b1)

