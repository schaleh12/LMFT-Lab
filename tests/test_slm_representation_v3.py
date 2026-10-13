"""Synthetic contract/transport tests for Protocol 3; no model or natural corpus access."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'experiments'))
import slm_representation_v3 as c
import run_slm_representation_v3 as runner
from lmft_lab.local_models import load_config
from lmft_lab.model_assets import ModelError
from lmft_lab.runtime_store import Store, digest


def source():
    return {'tokens': ['Please', 'order', 'blue widgets', '.'],
            'target': {'start': 1, 'end': 2, 'quote': 'order'}}


def proposal():
    return {'schema_version': 1, 'status': 'one_reading', 'target': source()['target'],
            'readings': [{'gloss': 'Synthetic request to obtain objects.',
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


@pytest.mark.parametrize('mutate', [
    lambda p: p.update(schema_version=True),
    lambda p: p.update(schema_version=1.0),
    lambda p: p.update(extra='forbidden'),
    lambda p: p.pop('target'),
    lambda p: p['target'].update(start=True),
    lambda p: p['target'].update(start=1.0),
    lambda p: p['target'].update(end=1),
    lambda p: p['target'].update(end=99),
    lambda p: p['target'].update(quote='invented'),
    lambda p: p.update(target={'start': 0, 'end': 1, 'quote': 'Please'}),
    lambda p: p.update(status='confident'),
    lambda p: p.update(status='alternatives'),
    lambda p: p.update(readings=[]),
    lambda p: p.update(uncertainties=['']),
    lambda p: p.update(uncertainties=['valid reason under one_reading']),
    lambda p: p['readings'][0].pop('context_quote'),
    lambda p: p['readings'][0].update(context_quote=''),
    lambda p: p['readings'][0].update(context_quote='not found anywhere in sentence'),
    lambda p: p['readings'][0].update(context_quote='order'),  # target-only must reject
    lambda p: p['readings'][0].update(gloss='x'*241),
    lambda p: p['readings'][0].update(extra='forbidden_field'),
])
def test_invalid_output_rejected_without_source_mutation(mutate):
    s = source()
    before = digest(s)
    p = proposal()
    mutate(p)
    result = c.validation_report(json.dumps(p), s)
    assert not result['admissible'] and result['proposal'] is None and result['errors']
    assert digest(s) == before


def test_target_only_quote_strictly_rejected():
    s = source()
    p = proposal()
    p['readings'][0]['context_quote'] = 'order'
    report = c.validation_report(json.dumps(p), s)
    assert not report['admissible']
    assert any('non-target' in err for err in report['errors'])


def test_context_quotes_resolve_to_canonical_anchors():
    s = source()
    p = proposal()
    # Left context quote
    p['readings'][0]['context_quote'] = 'Please order'
    res = c.validate(json.dumps(p), s)
    assert res['readings'][0]['context_anchor'] == {'start': 0, 'end': 2, 'quote': 'Please order'}

    # Right context quote
    p['readings'][0]['context_quote'] = 'blue widgets'
    res = c.validate(json.dumps(p), s)
    assert res['readings'][0]['context_anchor'] == {'start': 2, 'end': 3, 'quote': 'blue widgets'}

    # Whole phrase with target
    p['readings'][0]['context_quote'] = 'Please order blue widgets'
    res = c.validate(json.dumps(p), s)
    assert res['readings'][0]['context_anchor'] == {'start': 0, 'end': 3, 'quote': 'Please order blue widgets'}


def test_insufficient_context_contract():
    s = source()
    p = proposal()
    p.update(status='insufficient_context', readings=[], uncertainties=['Synthetic missing context.'])
    assert c.validate(json.dumps(p), s) == p

    # Missing uncertainty
    p['uncertainties'] = []
    assert not c.validation_report(json.dumps(p), s)['admissible']

    # More than 2 uncertainties
    p['uncertainties'] = ['u1', 'u2', 'u3']
    assert not c.validation_report(json.dumps(p), s)['admissible']


def test_duplicate_conflict_and_consumer_nonmutation():
    s = c.newborn()
    r = record()
    s = c.append(s, r)
    before = digest(s)
    assert c.append(s, r) == s
    assert c.retrieve(s, r['id'], 'primary') == c.retrieve(s, r['id'], 'ordinary_memory') == r
    retrieved = c.retrieve(s, r['id'], 'primary')
    retrieved['raw'] = 'modified copy'
    other = record('[]')
    with pytest.raises(ValueError, match='conflicting'):
        c.append(s, other)
    assert digest(s) == before


def test_request_contains_sentence_and_schema():
    config = load_config(c.ROOT/'config/local_models.json')
    req = c.request(source(), config['generation'])
    user = json.loads(req['messages'][1]['content'])
    assert set(user) == {'sentence', 'surface_tokens', 'target'}
    assert user['sentence'] == 'Please order blue widgets .'
    schema = req['response_format']['schema']
    assert schema['properties']['readings']['maxItems'] == 1
    assert set(schema['properties']['status']['enum']) == {'one_reading', 'insufficient_context'}


def test_actual_process_restart_identical_retrieval(tmp_path):
    s = c.append(c.newborn(), record())
    s = c.append(s, {**record('[]'), 'id': 'synthetic-rejected'})
    store = Store(tmp_path)
    store.commit(s)
    before = (tmp_path/'checkpoint.json').read_bytes()
    command = [sys.executable, str(c.ROOT/'experiments/slm_representation_v3.py'), '--state-dir', str(tmp_path)]
    env = {**os.environ, 'PYTHONPATH': str(c.ROOT/'src')}
    response = subprocess.run(command, capture_output=True, text=True, env=env, check=True)
    restored = json.loads(response.stdout)
    assert restored['state_sha256'] == digest(s)
    assert all(v['primary'] == v['ordinary_memory'] for v in restored['record_hashes'].values())
    assert before == (tmp_path/'checkpoint.json').read_bytes()
    s['schema_version'] = True
    store.commit(s)
    assert subprocess.run(command, capture_output=True, text=True, env=env).returncode != 0
