"""Synthetic contract/transport tests for Protocol 4; no model or natural corpus access."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'experiments'))
import slm_representation_v4 as c
import run_slm_representation_v4 as runner
from lmft_lab.local_models import load_config
from lmft_lab.runtime_store import Store, digest


def source():
    return {'tokens': ['Please', 'order', 'blue widgets', '.'],
            'target': {'start': 1, 'end': 2, 'quote': 'order'}}


def proposal():
    return {'schema_version': 1, 'status': 'one_reading', 'target': source()['target'],
            'readings': [{'gloss': 'Synthetic request to acquire objects.',
                          'context_quote': 'Please order blue widgets'}],
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


def test_valid_substitution_proposal():
    # True substitution without target word
    raw = json.dumps(proposal())
    report = c.validation_report(raw, source())
    assert report['admissible'] is True
    assert report['errors'] == []
    assert report['proposal']['readings'][0]['context_anchor'] == {'start': 0, 'end': 3, 'quote': 'Please order blue widgets'}


def test_tautological_gloss_rejected():
    # Gloss repeating target lemma 'order'
    bad_proposal = proposal()
    bad_proposal['readings'][0]['gloss'] = 'An order to obtain blue widgets.'
    raw = json.dumps(bad_proposal)
    report = c.validation_report(raw, source())
    assert report['admissible'] is False
    assert any('gloss tautology: target word repeated in gloss' in e for e in report['errors'])

    # Gloss repeating plural 'orders'
    bad_proposal2 = proposal()
    bad_proposal2['readings'][0]['gloss'] = 'Submitting all orders promptly.'
    report2 = c.validation_report(json.dumps(bad_proposal2), source())
    assert report2['admissible'] is False
    assert any('gloss tautology' in e for e in report2['errors'])


def test_target_only_context_quote_rejected():
    bad = proposal()
    bad['readings'][0]['context_quote'] = 'order'
    report = c.validation_report(json.dumps(bad), source())
    assert report['admissible'] is False
    assert any('cover at least one non-target token' in e for e in report['errors'])


def test_context_quote_not_found():
    bad = proposal()
    bad['readings'][0]['context_quote'] = 'completely fabricated non-existent sentence'
    report = c.validation_report(json.dumps(bad), source())
    assert report['admissible'] is False
    assert any('not found in source tokens' in e for e in report['errors'])


def test_insufficient_context_valid():
    insuf = {'schema_version': 1, 'status': 'insufficient_context', 'target': source()['target'],
             'readings': [], 'uncertainties': ['Underdetermined without surrounding text.']}
    report = c.validation_report(json.dumps(insuf), source())
    assert report['admissible'] is True
    assert report['errors'] == []


@pytest.mark.parametrize('mutate', [
    lambda p: p.update(schema_version=True),
    lambda p: p.update(schema_version=2),
    lambda p: p.update(extra='forbidden'),
    lambda p: p.pop('target'),
    lambda p: p['target'].update(start=-1),
    lambda p: p['target'].update(quote='mismatched'),
    lambda p: p.update(status='confident'),
    lambda p: p.update(readings=[p['readings'][0], p['readings'][0]]),  # count mismatch
    lambda p: p.update(uncertainties=['extra']),  # non-empty with one_reading
])
def test_schema_violations_rejected(mutate):
    prop = proposal()
    mutate(prop)
    report = c.validation_report(json.dumps(prop), source())
    assert report['admissible'] is False
    assert len(report['errors']) > 0


def test_neutral_state_and_consumer_parity(tmp_path):
    state = c.newborn()
    rec = record()
    state = c.append(state, rec)
    store = Store(tmp_path)
    store.commit(state)

    # Process restart simulation
    restored = store.read()
    p_view, m_view = c.consumer_views(restored['records'])
    assert p_view == m_view
    assert digest(p_view) == digest(m_view)
    assert restored['records'][0]['lifecycle'] == 'unverified_proposal'
