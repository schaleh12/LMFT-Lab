"""Independent effect truth table and boundaries for the isolated comparison."""
from copy import deepcopy
import importlib.util
from itertools import product
from pathlib import Path
import sys

import pytest
from lmft_lab import action_policy as policy, correction_fixture as fixture
from lmft_lab.runtime_store import digest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
import run_investigation_priority as h


def independent_table(current, case, offer):
    # No production support/predict/normalize/annotation calls in this oracle.
    records = [deepcopy(current['ledger'][head]['record']) for head in current['heads'].values()]
    parts = offer.get('parts', [offer.get('coordinate', {}).get('part')])
    rows = []
    for bits in product((False, True), repeat=len(parts)):
        changed = deepcopy(records)
        if offer['kind'] == 'correction':
            target = current['ledger'][offer['target_id']]['record']['evidence_id']
            next(r for r in changed if r['evidence_id'] == target)['value'] = bits[0]
        else:
            changed.extend({'case_id': case['case_id'], 'scope': case['scope'], 'question': offer['field'],
                            'part': p, 'value': v} for p, v in zip(parts, bits))
        resolved = {}; result_values = {}
        for field, required in [('shielded', ['check1', 'check2']), ('payload_valid', ['check1'])]:
            slots = []
            for part in required:
                values = []
                for r in changed:
                    if (r['case_id'], r['scope'], r['question'], r['part']) == (case['case_id'], case['scope'], field, part):
                        value = r['value']
                        if field == 'shielded' and part == 'check2' and case['relation'] == 'complement':
                            value = not value
                        values.append(value)
                slots.append(values)
            flat = [v for slot in slots for v in slot]
            resolved[field] = all(slots) and all(v == flat[0] for v in flat)
            result_values[field] = flat[0] if resolved[field] else None
        gate = resolved['shielded'] and resolved['payload_valid'] and result_values['payload_valid'] is True
        branch = 'shielded' if result_values['shielded'] else 'unshielded'
        final = gate and abs(current['branches'][branch]['score']) >= .2
        rows.append({'values': list(bits), 'target': bool(resolved[offer['field']]), 'support_gate': bool(gate), 'final': bool(final)})
    return rows


@pytest.mark.parametrize('relation', ['equal', 'complement'])
@pytest.mark.parametrize('slots', list(product(((), (False,), (True,), (False, True)), repeat=3)))
def test_exhaustive_independent_boolean_table(relation, slots):
    b = policy.prepare('r9'); c = b['state']['judgment']; case = b['case']; case['relation'] = relation
    template = deepcopy(c['ledger']['c1/shielded/check1']['record'])
    c['ledger'] = {}; c['heads'] = {}; c['roots'] = {}
    for (field, part), values in zip((('shielded', 'check1'), ('shielded', 'check2'), ('payload_valid', 'check1')), slots):
        for n, value in enumerate(values):
            eid = 'c1/' + field + '/' + part + ('-extra' if n else '')
            record = {**template, 'evidence_id': eid, 'question': field, 'part': part, 'value': value}
            c['ledger'][eid] = {'record': record, 'root': eid, 'parent': None}; c['heads'][eid] = eid; c['roots'][eid] = eid
    offers = []
    for field, indices in [('shielded', (0, 1)), ('payload_valid', (2,))]:
        parts = ['check' + str(i+1) for i, n in enumerate(indices) if not slots[n]]
        offers.append({'id': 'g-'+field, 'kind': 'gather', 'field': field, 'case_id': 'c1', 'scope': case['scope'], 'available': True, 'parts': parts})
    if slots[0]:
        offer = deepcopy(b['offers'][0]);offer['expected_digest'] = digest(c['ledger'][offer['target_id']]['record']);offers.append(offer)
    for offer in offers:
        if policy.preflight(c, case, offer) is not None:
            continue
        before = digest(c); a = h.annotate(c, case, offer); expected = independent_table(c, case, offer)
        assert a['witnesses'] == expected
        for key in ('target', 'support_gate', 'final'):
            assert a[key] == ('possible' if any(r[key] for r in expected) else 'ruled_out')
        assert a['admission'] == 'unknown' and digest(c) == before


def test_x2_decision_only_and_partial_information_sacrifice():
    b = h.x2_probe()
    assert h.choose(b, 'current')[0]['field'] == 'shielded'
    assert h.choose(b, 'target')[0]['field'] == 'payload_valid'
    assert h.choose(b, 'final')[0] is None
    b['offers'] = b['offers'][:1]
    assert h.choose(b, 'current')[0]['parts'] == ['check2']
    assert h.choose(b, 'target')[0] is None


def test_future_access_forbidden_and_r9_tie(monkeypatch):
    b = policy.prepare('r9')
    def fail(*a, **kw): pytest.fail('future information accessed')
    for name in ('service_reply', 'proposal'): monkeypatch.setattr(policy, name, fail)
    for name in ('actual_success', 'replacement_valid'): monkeypatch.setattr(fixture, name, fail)
    assert h.choose(b, 'target')[0]['kind'] == 'correction'
    assert h.choose(b, 'final')[0] is None
    b['offers'][0]['id'] = 'z-correction'
    assert h.choose(b, 'target')[0]['kind'] == 'gather'


def test_order_scope_superseded_duplicate_and_unknown():
    b = policy.prepare('r2'); c = b['state']['judgment']; offer = b['offers'][0]
    assert len(c['ledger']) > len(c['heads'])  # preparation left a superseded record
    before = h.annotate(c, b['case'], offer)
    assert before['target'] == 'possible'
    c['ledger'] = dict(reversed(list(c['ledger'].items()))); c['heads'] = dict(reversed(list(c['heads'].items())))
    assert h.annotate(c, b['case'], offer) == before
    c['branches']['shielded']['score'] = 0; c['branches']['unshielded']['score'] = 0
    a = h.annotate(c, b['case'], offer)
    assert a['support_gate'] == 'possible' and a['final'] == 'ruled_out'
    b['case']['relation'] = 'unsupported'
    assert h.annotate(c, b['case'], offer)['target'] == 'unknown'
    b = h.x2_probe(); c = b['state']['judgment']; key = next(iter(c['heads']))
    rec = deepcopy(c['ledger'][key]); rec['record']['evidence_id'] = 'duplicate'
    c['ledger']['duplicate'] = rec; c['heads']['duplicate'] = 'duplicate'; c['roots']['duplicate'] = 'duplicate'
    assert h.annotate(c, b['case'], b['offers'][0])['target'] == 'ruled_out'
    rec = deepcopy(rec); rec['record'].update(evidence_id='foreign', scope='foreign')
    c['ledger']['foreign'] = rec; c['heads']['foreign'] = 'foreign'; c['roots']['foreign'] = 'foreign'
    assert h.annotate(c, b['case'], b['offers'][0])['target'] == 'ruled_out'


@pytest.mark.parametrize('key', h.CASES)
def test_receiver_parity_budget_and_preservation(key):
    b = policy.prepare(key)
    for objective in h.POLICIES:
        selected, trace = h.choose(b, objective)
        assert selected == h.choose(b, objective, True)[0]
        reversed_bundle = deepcopy(b); reversed_bundle['offers'].reverse()
        assert selected == h.choose(reversed_bundle, objective)[0]
        state = h.pending(b, objective)
        assert state == h.pending({**b, 'state': state}, objective)
        row = h.finish(state, b['case'])
        assert all(row['checks'].values())
        assert row['final'] == h.pending({**b, 'state': row['final']}, objective)


@pytest.mark.parametrize('value', [[False], {'value': False}, None, 0, 1, 'false', 0.0])
@pytest.mark.parametrize('location', ['target', 'other-question', 'normalization-check2',
                                     'unrelated-field', 'foreign-case', 'foreign-scope', 'superseded'])
def test_malformed_value_boundary_before_support_and_selection(value, location, monkeypatch):
    b = policy.prepare('r9'); c = b['state']['judgment']
    baseline = {objective: h.choose(b, objective) for objective in h.POLICIES}
    baseline_annotation = h.annotate(c, b['case'], b['offers'][0])
    entry = deepcopy(c['ledger']['c1/shielded/check1'])
    entry['record'].update(evidence_id='domain-probe', value=deepcopy(value))
    entry.update(root='domain-probe', parent=None)
    if location == 'other-question': entry['record']['question'] = 'payload_valid'
    if location == 'normalization-check2':
        entry['record']['part'] = 'check2'; b['case']['relation'] = 'complement'
    if location == 'unrelated-field': entry['record']['question'] = 'color'
    if location == 'foreign-case': entry['record']['case_id'] = 'other-case'
    if location == 'foreign-scope': entry['record']['scope'] = 'other-scope'
    c['ledger']['domain-probe'] = entry
    if location != 'superseded':
        c['heads']['domain-probe'] = 'domain-probe'; c['roots']['domain-probe'] = 'domain-probe'
    before = digest(b)
    guarded = location not in ('foreign-case', 'foreign-scope', 'superseded')
    if guarded:
        def forbidden(*args, **kwargs): pytest.fail('malformed value reached support/preflight/selection')
        monkeypatch.setattr(policy, 'preflight', forbidden)
        monkeypatch.setattr(policy, 'select', forbidden)
        monkeypatch.setattr(h.circuit, 'support', forbidden)
    annotation = h.annotate(c, b['case'], b['offers'][0])
    if guarded:
        assert annotation == h.unknown_annotation('unsupported value domain')
    else:
        assert annotation == baseline_annotation
    for objective in h.POLICIES:
        for scalar in (False, True):
            selected, trace = h.choose(b, objective, scalar)
            if guarded:
                assert selected is None and trace['domain'] == 'unknown'
                assert trace['questions'] == []
                assert all(row['score'] is None and row['feasibility'] == annotation for row in trace['actions'])
            else:
                assert selected == baseline[objective][0]
    assert digest(b) == before


def test_missing_value_is_unknown_but_boolean_contradiction_is_supported():
    b = policy.prepare('r9'); c = b['state']['judgment']
    del c['ledger']['c1/shielded/check1']['record']['value']
    before = digest(b)
    assert h.annotate(c, b['case'], b['offers'][0])['target'] == 'unknown'
    assert h.choose(b, 'current')[0] is None
    assert digest(b) == before
    b = h.x2_probe()
    assert h.annotate(b['state']['judgment'], b['case'], b['offers'][0])['target'] == 'ruled_out'
    assert h.choose(b, 'current')[0]['field'] == 'shielded'
